import random
import string
import redis
from datetime import datetime, timedelta
from flask import current_app
from flask_mail import Mail, Message
from app import create_app

class EmailService:
    """邮箱服务类"""
    
    def __init__(self):
        self.app = create_app()
        self.mail = Mail(self.app)
        self.redis_client = None
    
    def get_redis_client(self):
        """获取Redis客户端"""
        if self.redis_client is None:
            self.redis_client = redis.Redis(
                host=current_app.config['REDIS_HOST'],
                port=current_app.config['REDIS_PORT'],
                db=current_app.config['REDIS_DB'],
                decode_responses=True
            )
        return self.redis_client
    
    def generate_verification_code(self, length=6):
        """生成验证码"""
        return ''.join(random.choices(string.digits, k=length))
    
    def send_verification_email(self, email, code_type='register'):
        """发送验证码邮件"""
        try:
            with self.app.app_context():
                # 生成验证码
                code = self.generate_verification_code(current_app.config['VERIFICATION_CODE_LENGTH'])
                
                # 存储验证码到Redis，设置过期时间
                key = f"verification_code:{code_type}:{email}"
                expire_time = current_app.config['VERIFICATION_CODE_EXPIRE']
                redis_client = self.get_redis_client()
                redis_client.setex(key, expire_time, code)
                
                # 创建邮件内容
                if code_type == 'register':
                    subject = '校园跳蚤市场 - 邮箱验证码'
                    body = f"""
                    <html>
                    <body>
                        <h2>欢迎注册校园跳蚤市场智能推荐平台！</h2>
                        <p>您的验证码是：<strong style="color: #007bff; font-size: 24px;">{code}</strong></p>
                        <p>验证码有效期为 {expire_time // 60} 分钟，请及时使用。</p>
                        <p>如果这不是您的操作，请忽略此邮件。</p>
                        <hr>
                        <p style="color: #666; font-size: 12px;">此邮件由系统自动发送，请勿回复。</p>
                    </body>
                    </html>
                    """
                else:
                    subject = '校园跳蚤市场 - 验证码'
                    body = f"""
                    <html>
                    <body>
                        <h2>校园跳蚤市场验证码</h2>
                        <p>您的验证码是：<strong style="color: #007bff; font-size: 24px;">{code}</strong></p>
                        <p>验证码有效期为 {expire_time // 60} 分钟，请及时使用。</p>
                        <p>如果这不是您的操作，请忽略此邮件。</p>
                        <hr>
                        <p style="color: #666; font-size: 12px;">此邮件由系统自动发送，请勿回复。</p>
                    </body>
                    </html>
                    """
                
                # 创建邮件消息
                msg = Message(
                    subject=subject,
                    recipients=[email],
                    html=body,
                    sender=current_app.config['MAIL_DEFAULT_SENDER']
                )
                
                # 发送邮件
                self.mail.send(msg)
                
                return {
                    'success': True,
                    'message': '验证码发送成功',
                    'code': code  # 开发环境返回验证码，生产环境应删除
                }
                
        except Exception as e:
            current_app.logger.error(f"发送验证码邮件失败: {str(e)}")
            return {
                'success': False,
                'message': f'发送失败: {str(e)}'
            }
    
    def verify_code(self, email, code, code_type='register'):
        """验证验证码"""
        try:
            key = f"verification_code:{code_type}:{email}"
            redis_client = self.get_redis_client()
            stored_code = redis_client.get(key)
            
            if not stored_code:
                return {
                    'success': False,
                    'message': '验证码已过期或不存在'
                }
            
            if stored_code != code:
                return {
                    'success': False,
                    'message': '验证码错误'
                }
            
            # 验证成功后删除验证码
            redis_client.delete(key)
            
            return {
                'success': True,
                'message': '验证码验证成功'
            }
            
        except Exception as e:
            current_app.logger.error(f"验证验证码失败: {str(e)}")
            return {
                'success': False,
                'message': f'验证失败: {str(e)}'
            }
    
    def check_email_send_limit(self, email, code_type='register'):
        """检查邮箱发送限制（防止频繁发送）"""
        try:
            key = f"email_send_limit:{code_type}:{email}"
            redis_client = self.get_redis_client()
            count = redis_client.get(key)
            
            if count is None:
                # 第一次发送，设置计数器和过期时间（1小时）
                redis_client.setex(key, 3600, 1)
                return True
            elif int(count) < 5:  # 限制1小时内最多发送5次
                redis_client.incr(key)
                return True
            else:
                return False
                
        except Exception as e:
            current_app.logger.error(f"检查邮箱发送限制失败: {str(e)}")
            return True  # 出错时允许发送

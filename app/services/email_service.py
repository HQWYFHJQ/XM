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
    
    def send_email(self, email, subject, body):
        """发送邮件"""
        try:
            with self.app.app_context():
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
                    'message': '邮件发送成功'
                }
                
        except Exception as e:
            current_app.logger.error(f"发送邮件失败: {str(e)}")
            return {
                'success': False,
                'message': f'发送失败: {str(e)}'
            }
    
    def send_transaction_notification(self, email, transaction_type, transaction_data):
        """发送交易通知邮件"""
        try:
            with self.app.app_context():
                if transaction_type == 'purchase':
                    subject = '校园跳蚤市场 - 商品售出通知'
                    body = f"""
                    <html>
                    <body>
                        <h2>🎉 恭喜！您的商品已售出</h2>
                        <p>亲爱的 {transaction_data['seller_name']}，</p>
                        <p>您的商品《{transaction_data['item_title']}》已被用户 {transaction_data['buyer_name']} 购买！</p>
                        <p>商品信息：</p>
                        <ul>
                            <li>商品名称：{transaction_data['item_title']}</li>
                            <li>售价：¥{transaction_data['price']}</li>
                            <li>买家：{transaction_data['buyer_name']}</li>
                            <li>购买时间：{transaction_data['created_at']}</li>
                        </ul>
                        <p>请及时登录系统确认发货，买家正在等待您的商品！</p>
                        <p><a href="{transaction_data['admin_url']}" style="background-color: #007bff; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px;">查看交易详情</a></p>
                        <hr>
                        <p style="color: #666; font-size: 12px;">此邮件由系统自动发送，请勿回复。</p>
                    </body>
                    </html>
                    """
                
                elif transaction_type == 'payment_confirmed':
                    subject = '校园跳蚤市场 - 支付确认，请及时发货'
                    body = f"""
                    <html>
                    <body>
                        <h2>💰 买家已确认支付，请及时发货</h2>
                        <p>亲爱的 {transaction_data['seller_name']}，</p>
                        <p>买家 {transaction_data['buyer_name']} 已确认支付，请及时发货！</p>
                        <p>交易信息：</p>
                        <ul>
                            <li>商品：{transaction_data['item_title']}</li>
                            <li>价格：¥{transaction_data['price']}</li>
                            <li>买家：{transaction_data['buyer_name']}</li>
                            <li>支付确认时间：{transaction_data['payment_confirmed_at']}</li>
                        </ul>
                        <p><a href="{transaction_data['admin_url']}" style="background-color: #28a745; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px;">确认发货</a></p>
                        <hr>
                        <p style="color: #666; font-size: 12px;">此邮件由系统自动发送，请勿回复。</p>
                    </body>
                    </html>
                    """
                
                elif transaction_type == 'shipped':
                    subject = '校园跳蚤市场 - 商品已发货'
                    body = f"""
                    <html>
                    <body>
                        <h2>📦 您的商品已发货</h2>
                        <p>亲爱的 {transaction_data['buyer_name']}，</p>
                        <p>您购买的商品《{transaction_data['item_title']}》已发货！</p>
                        <p>交易信息：</p>
                        <ul>
                            <li>商品：{transaction_data['item_title']}</li>
                            <li>价格：¥{transaction_data['price']}</li>
                            <li>卖家：{transaction_data['seller_name']}</li>
                            <li>发货时间：{transaction_data['shipped_at']}</li>
                            {f'<li>发货备注：{transaction_data["shipping_notes"]}</li>' if transaction_data.get('shipping_notes') else ''}
                        </ul>
                        <p>请及时确认收货，如有问题请联系卖家。</p>
                        <p><a href="{transaction_data['profile_url']}" style="background-color: #17a2b8; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px;">查看交易详情</a></p>
                        <hr>
                        <p style="color: #666; font-size: 12px;">此邮件由系统自动发送，请勿回复。</p>
                    </body>
                    </html>
                    """
                
                elif transaction_type == 'delivered':
                    subject = '校园跳蚤市场 - 买家已确认收货'
                    body = f"""
                    <html>
                    <body>
                        <h2>✅ 买家已确认收货</h2>
                        <p>亲爱的 {transaction_data['seller_name']}，</p>
                        <p>买家 {transaction_data['buyer_name']} 已确认收货，交易完成！</p>
                        <p>交易信息：</p>
                        <ul>
                            <li>商品：{transaction_data['item_title']}</li>
                            <li>价格：¥{transaction_data['price']}</li>
                            <li>买家：{transaction_data['buyer_name']}</li>
                            <li>确认收货时间：{transaction_data['delivered_at']}</li>
                            {f'<li>收货备注：{transaction_data["delivery_notes"]}</li>' if transaction_data.get('delivery_notes') else ''}
                        </ul>
                        <p>感谢您使用校园跳蚤市场！</p>
                        <hr>
                        <p style="color: #666; font-size: 12px;">此邮件由系统自动发送，请勿回复。</p>
                    </body>
                    </html>
                    """
                
                elif transaction_type == 'timeout':
                    subject = '校园跳蚤市场 - 交易超时通知'
                    body = f"""
                    <html>
                    <body>
                        <h2>⏰ 交易超时通知</h2>
                        <p>亲爱的 {transaction_data['user_name']}，</p>
                        <p>您的交易《{transaction_data['item_title']}》已超时，系统已自动取消该交易。</p>
                        <p>交易信息：</p>
                        <ul>
                            <li>商品：{transaction_data['item_title']}</li>
                            <li>价格：¥{transaction_data['price']}</li>
                            <li>超时原因：{transaction_data['timeout_reason']}</li>
                            <li>超时时间：{transaction_data['timeout_at']}</li>
                        </ul>
                        <p>如有疑问，请联系系统管理员：21641685@qq.com</p>
                        <hr>
                        <p style="color: #666; font-size: 12px;">此邮件由系统自动发送，请勿回复。</p>
                    </body>
                    </html>
                    """
                
                else:
                    return {
                        'success': False,
                        'message': '不支持的交易通知类型'
                    }
                
                return self.send_email(email, subject, body)
                
        except Exception as e:
            current_app.logger.error(f"发送交易通知邮件失败: {str(e)}")
            return {
                'success': False,
                'message': f'发送失败: {str(e)}'
            }
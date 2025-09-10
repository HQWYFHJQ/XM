import random
import string
import redis
import hashlib
import time
from datetime import datetime, timedelta
from flask import current_app
from captcha.image import ImageCaptcha
import io
import base64

class CaptchaService:
    """验证码服务类"""
    
    def __init__(self):
        self.app = current_app
        self.redis_client = None
        self.image_captcha = ImageCaptcha(width=200, height=80)
    
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
    
    def generate_math_captcha(self):
        """生成数学运算验证码"""
        try:
            # 生成简单的数学运算题
            num1 = random.randint(1, 20)
            num2 = random.randint(1, 20)
            operation = random.choice(['+', '-', '*'])
            
            if operation == '+':
                answer = num1 + num2
                question = f"{num1} + {num2} = ?"
            elif operation == '-':
                # 确保结果为正数
                if num1 < num2:
                    num1, num2 = num2, num1
                answer = num1 - num2
                question = f"{num1} - {num2} = ?"
            else:  # *
                answer = num1 * num2
                question = f"{num1} × {num2} = ?"
            
            # 生成验证码ID
            captcha_id = self._generate_captcha_id()
            
            # 存储验证信息到Redis
            key = f"math_captcha:{captcha_id}"
            data = {
                'question': question,
                'answer': str(answer),
                'created_at': str(time.time()),
                'used': 'False'
            }
            redis_client = self.get_redis_client()
            redis_client.hset(key, mapping=data)
            redis_client.expire(key, 300)  # 5分钟过期
            
            return {
                'success': True,
                'captcha_id': captcha_id,
                'question': question,
                'message': '数学验证码生成成功'
            }
            
        except Exception as e:
            current_app.logger.error(f"生成数学验证码失败: {str(e)}")
            return {
                'success': False,
                'message': f'生成失败: {str(e)}'
            }
    
    def verify_math_captcha(self, captcha_id, user_answer):
        """验证数学运算验证码"""
        try:
            key = f"math_captcha:{captcha_id}"
            redis_client = self.get_redis_client()
            data = redis_client.hgetall(key)
            
            if not data:
                return {
                    'success': False,
                    'message': '验证码已过期或不存在'
                }
            
            if data.get('used') == 'True':
                return {
                    'success': False,
                    'message': '验证码已被使用'
                }
            
            # 比较答案（转换为字符串比较）
            if data['answer'] == str(user_answer).strip():
                # 验证成功，标记为已使用
                redis_client.hset(key, 'used', 'True')
                return {
                    'success': True,
                    'message': '数学验证码验证成功'
                }
            else:
                return {
                    'success': False,
                    'message': '答案错误'
                }
                
        except Exception as e:
            current_app.logger.error(f"验证数学验证码失败: {str(e)}")
            return {
                'success': False,
                'message': f'验证失败: {str(e)}'
            }
    
    def verify_slider_captcha(self, captcha_id, user_x, user_y, user_angle):
        """验证滑块验证码"""
        try:
            key = f"slider_captcha:{captcha_id}"
            redis_client = self.get_redis_client()
            data = redis_client.hgetall(key)
            
            if not data:
                return {
                    'success': False,
                    'message': '验证码已过期或不存在'
                }
            
            if data.get('used') == 'True':
                return {
                    'success': False,
                    'message': '验证码已被使用'
                }
            
            # 获取目标值
            target_x = float(data['target_x'])
            target_y = float(data['target_y'])
            target_angle = float(data['target_angle'])
            
            # 计算误差（允许一定范围的误差）
            x_error = abs(float(user_x) - target_x)
            y_error = abs(float(user_y) - target_y)
            angle_error = abs(float(user_angle) - target_angle)
            
            # 允许的误差范围
            x_tolerance = 10
            y_tolerance = 10
            angle_tolerance = 15
            
            if x_error <= x_tolerance and y_error <= y_tolerance and angle_error <= angle_tolerance:
                # 验证成功，标记为已使用
                redis_client.hset(key, 'used', True)
                return {
                    'success': True,
                    'message': '滑块验证成功'
                }
            else:
                return {
                    'success': False,
                    'message': '滑块位置或角度不正确'
                }
                
        except Exception as e:
            current_app.logger.error(f"验证滑块验证码失败: {str(e)}")
            return {
                'success': False,
                'message': f'验证失败: {str(e)}'
            }
    
    def generate_image_captcha(self):
        """生成图片验证码"""
        try:
            # 生成随机字符串
            captcha_text = ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))
            
            # 生成验证码ID
            captcha_id = self._generate_captcha_id()
            
            # 生成图片
            image_data = self.image_captcha.generate(captcha_text)
            
            # 转换为base64
            image_base64 = base64.b64encode(image_data.getvalue()).decode('utf-8')
            
            # 存储验证信息到Redis
            key = f"image_captcha:{captcha_id}"
            data = {
                'text': captcha_text.upper(),
                'created_at': str(time.time()),
                'used': 'False'
            }
            redis_client = self.get_redis_client()
            redis_client.hset(key, mapping=data)
            redis_client.expire(key, 300)  # 5分钟过期
            
            return {
                'success': True,
                'captcha_id': captcha_id,
                'image': f"data:image/png;base64,{image_base64}",
                'message': '图片验证码生成成功'
            }
            
        except Exception as e:
            current_app.logger.error(f"生成图片验证码失败: {str(e)}")
            return {
                'success': False,
                'message': f'生成失败: {str(e)}'
            }
    
    def verify_image_captcha(self, captcha_id, user_text):
        """验证图片验证码"""
        try:
            key = f"image_captcha:{captcha_id}"
            redis_client = self.get_redis_client()
            data = redis_client.hgetall(key)
            
            if not data:
                return {
                    'success': False,
                    'message': '验证码已过期或不存在'
                }
            
            if data.get('used') == 'True':
                return {
                    'success': False,
                    'message': '验证码已被使用'
                }
            
            # 比较验证码（不区分大小写）
            if data['text'].upper() == user_text.upper():
                # 验证成功，标记为已使用
                self.redis_client.hset(key, 'used', True)
                return {
                    'success': True,
                    'message': '图片验证码验证成功'
                }
            else:
                return {
                    'success': False,
                    'message': '验证码错误'
                }
                
        except Exception as e:
            current_app.logger.error(f"验证图片验证码失败: {str(e)}")
            return {
                'success': False,
                'message': f'验证失败: {str(e)}'
            }
    
    def _generate_captcha_id(self):
        """生成验证码ID"""
        timestamp = str(int(time.time() * 1000))
        random_str = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
        return hashlib.md5(f"{timestamp}{random_str}".encode()).hexdigest()[:16]
    
    def cleanup_expired_captchas(self):
        """清理过期的验证码"""
        try:
            # Redis会自动清理过期的key，这里可以添加额外的清理逻辑
            pass
        except Exception as e:
            current_app.logger.error(f"清理过期验证码失败: {str(e)}")

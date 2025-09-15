import os
from dotenv import load_dotenv
from datetime import timezone, timedelta

load_dotenv()

# 北京时间 (UTC+8)
BEIJING_TZ = timezone(timedelta(hours=8))

class Config:
    """基础配置类"""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = os.environ.get('UPLOAD_FOLDER') or 'app/static/uploads'
    MAX_CONTENT_LENGTH = int(os.environ.get('MAX_CONTENT_LENGTH') or 16777216)  # 16MB
    
    # 时区配置
    TIMEZONE = BEIJING_TZ
    
    # 数据库配置
    DB_HOST = os.environ.get('DB_HOST') or 'localhost'
    DB_PORT = int(os.environ.get('DB_PORT') or 5081)
    DB_USER = os.environ.get('DB_USER') or 'root'
    DB_PASSWORD = os.environ.get('DB_PASSWORD') or '4mapg]zj2Am"]9(;'
    DB_NAME = os.environ.get('DB_NAME') or 'campus_market'
    
    SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    
    # Redis配置
    REDIS_HOST = os.environ.get('REDIS_HOST') or 'localhost'
    REDIS_PORT = int(os.environ.get('REDIS_PORT') or 6379)
    REDIS_DB = int(os.environ.get('REDIS_DB') or 0)
    
    # 邮件配置
    MAIL_SERVER = os.environ.get('MAIL_SERVER') or 'smtp.126.com'
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 25)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS', 'true').lower() in ['true', 'on', '1']
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME') or 'secondhandmarket@126.com'
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD') or 'EZb4jm8bQcgw9JQr'
    MAIL_DEFAULT_SENDER = os.environ.get('MAIL_DEFAULT_SENDER') or 'secondhandmarket@126.com'
    
    # 验证码配置
    VERIFICATION_CODE_EXPIRE = int(os.environ.get('VERIFICATION_CODE_EXPIRE') or 300)  # 5分钟
    VERIFICATION_CODE_LENGTH = int(os.environ.get('VERIFICATION_CODE_LENGTH') or 6)
    
    # 应用端口
    MAIN_PORT = int(os.environ.get('MAIN_PORT') or 8000)
    ADMIN_PORT = int(os.environ.get('ADMIN_PORT') or 8080)
    
    # AI模型配置
    DEEPSEEK_API_KEY = os.environ.get('DEEPSEEK_API_KEY') or 'sk-16a9e21d4c024d4d9ec6b107741c5797'
    DEEPSEEK_BASE_URL = os.environ.get('DEEPSEEK_BASE_URL') or 'https://api.deepseek.com'
    
    # 向量化服务配置
    VECTOR_DIM = int(os.environ.get('VECTOR_DIM') or 384)
    EMBEDDING_MODEL = os.environ.get('EMBEDDING_MODEL') or os.path.abspath('./models')
    
    # 推荐系统配置
    MAX_RECOMMENDATIONS = int(os.environ.get('MAX_RECOMMENDATIONS') or 5)
    SIMILARITY_THRESHOLD = float(os.environ.get('SIMILARITY_THRESHOLD') or 0.1)

class DevelopmentConfig(Config):
    """开发环境配置"""
    DEBUG = True
    FLASK_ENV = 'development'

class ProductionConfig(Config):
    """生产环境配置"""
    DEBUG = False
    FLASK_ENV = 'production'

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': ProductionConfig
}

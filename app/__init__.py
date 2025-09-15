from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_cors import CORS
try:
    from flask_mail import Mail
except ImportError:
    Mail = None
from config import config
import redis
import os

# 初始化扩展
db = SQLAlchemy()
login_manager = LoginManager()
mail = Mail() if Mail else None
redis_client = None

def create_app(config_name='default'):
    """应用工厂函数"""
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    
    # 初始化扩展
    db.init_app(app)
    login_manager.init_app(app)
    if mail:
        mail.init_app(app)
    CORS(app)
    
    # 初始化Redis
    global redis_client
    redis_client = redis.Redis(
        host=app.config['REDIS_HOST'],
        port=app.config['REDIS_PORT'],
        db=app.config['REDIS_DB'],
        decode_responses=True
    )
    
    # 配置登录管理器
    login_manager.login_view = 'main.login'
    login_manager.login_message = '请先登录以访问此页面'
    login_manager.login_message_category = 'info'
    
    @login_manager.user_loader
    def load_user(user_id):
        from app.models import User
        return User.query.get(int(user_id))
    
    # 创建上传目录
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    os.makedirs(os.path.join(app.config['UPLOAD_FOLDER'], 'avatars'), exist_ok=True)
    os.makedirs(os.path.join(app.config['UPLOAD_FOLDER'], 'items'), exist_ok=True)
    
    # 注册蓝图
    from app.views.main import main_bp
    from app.views.admin import admin_bp
    from app.views.api import api_bp
    from app.views.data_viz import data_viz_bp
    from app.views.message import message_bp
    from app.views.message_api import message_api_bp
    from app.views.announcement_api import announcement_api_bp
    from app.views.transaction_api import transaction_api_bp
    
    app.register_blueprint(main_bp)
    app.register_blueprint(admin_bp, url_prefix='/admin')
    app.register_blueprint(api_bp, url_prefix='/api')
    app.register_blueprint(data_viz_bp, url_prefix='/data-viz')
    app.register_blueprint(message_bp, url_prefix='/messages')
    app.register_blueprint(message_api_bp, url_prefix='/api/messages')
    app.register_blueprint(announcement_api_bp)
    app.register_blueprint(transaction_api_bp, url_prefix='/api/transactions')
    
    # 添加模板上下文处理器
    @app.context_processor
    def inject_categories():
        from app.models import Category
        parent_categories = Category.query.filter_by(parent_id=None, is_active=True).order_by(Category.sort_order).all()
        return dict(parent_categories=parent_categories)
    
    @app.context_processor
    def inject_announcements():
        from app.models import Announcement
        from flask_login import current_user
        # 只有登录用户才能看到系统公告
        if current_user.is_authenticated:
            announcements = Announcement.get_active_announcements_for_users(limit=5)
        else:
            announcements = []
        return dict(announcements=announcements)
    
    # 添加时间格式化过滤器
    @app.template_filter('beijing_time')
    def beijing_time_filter(dt, format_str='%Y-%m-%d %H:%M:%S'):
        """将UTC时间转换为北京时间并格式化"""
        from app.utils import format_beijing_time
        return format_beijing_time(dt, format_str)
    
    @app.template_filter('beijing_date')
    def beijing_date_filter(dt):
        """将UTC时间转换为北京时间并格式化为日期"""
        from app.utils import format_beijing_time
        from datetime import datetime
        
        # 如果输入是字符串，尝试解析为datetime对象
        if isinstance(dt, str):
            try:
                # 尝试解析ISO格式的时间字符串
                dt = datetime.fromisoformat(dt.replace('Z', '+00:00'))
            except (ValueError, AttributeError):
                # 如果解析失败，返回原始字符串
                return dt
        
        return format_beijing_time(dt, '%Y-%m-%d')
    
    @app.template_filter('beijing_datetime')
    def beijing_datetime_filter(dt):
        """将UTC时间转换为北京时间并格式化为日期时间"""
        from app.utils import format_beijing_time
        from datetime import datetime
        
        # 如果输入是字符串，尝试解析为datetime对象
        if isinstance(dt, str):
            try:
                # 尝试解析ISO格式的时间字符串
                dt = datetime.fromisoformat(dt.replace('Z', '+00:00'))
            except (ValueError, AttributeError):
                # 如果解析失败，返回原始字符串
                return dt
        
        return format_beijing_time(dt, '%Y-%m-%d %H:%M')
    
    # 创建数据库表
    with app.app_context():
        try:
            db.create_all()
        except Exception as e:
            print(f"警告: 数据库初始化失败: {e}")
            print("请确保MySQL服务正在运行并且配置正确")
    
    return app

# 导出app实例供Gunicorn使用
# 注意：这里不能直接调用create_app()，因为会导致循环导入
# 需要在运行时动态创建

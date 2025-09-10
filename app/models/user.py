from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import db

class User(UserMixin, db.Model):
    """用户模型"""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    real_name = db.Column(db.String(100), nullable=True)
    phone = db.Column(db.String(20), nullable=True)
    student_id = db.Column(db.String(20), nullable=True)
    avatar = db.Column(db.String(255), nullable=True)
    bio = db.Column(db.Text, nullable=True)
    interests = db.Column(db.Text, nullable=True)  # JSON格式存储兴趣标签
    is_active = db.Column(db.Boolean, default=True)
    is_admin = db.Column(db.Boolean, default=False)
    audit_status = db.Column(db.Enum('pending', 'approved', 'rejected'), default='pending')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_login = db.Column(db.DateTime, nullable=True)
    
    # 关系
    items = db.relationship('Item', backref='seller', lazy='dynamic', cascade='all, delete-orphan')
    behaviors = db.relationship('UserBehavior', backref='user', lazy='dynamic', cascade='all, delete-orphan')
    recommendations = db.relationship('Recommendation', backref='user', lazy='dynamic', cascade='all, delete-orphan')
    # 交易关系（通过Transaction模型的backref访问）
    # purchases = db.relationship('Transaction', foreign_keys='Transaction.buyer_id', lazy='dynamic')
    # sales = db.relationship('Transaction', foreign_keys='Transaction.seller_id', lazy='dynamic')
    
    def set_password(self, password):
        """设置密码"""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """验证密码"""
        return check_password_hash(self.password_hash, password)
    
    def get_interests_list(self):
        """获取兴趣列表"""
        if self.interests:
            import json
            try:
                return json.loads(self.interests)
            except:
                return []
        return []
    
    def set_interests_list(self, interests_list):
        """设置兴趣列表"""
        import json
        self.interests = json.dumps(interests_list, ensure_ascii=False)
    
    @property
    def role(self):
        """获取用户角色"""
        return 'admin' if self.is_admin else 'user'
    
    def to_dict(self):
        """转换为字典"""
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'real_name': self.real_name,
            'phone': self.phone,
            'student_id': self.student_id,
            'avatar': self.avatar,
            'bio': self.bio,
            'interests': self.get_interests_list(),
            'is_active': self.is_active,
            'audit_status': self.audit_status,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'last_login': self.last_login.isoformat() if self.last_login else None
        }
    
    @classmethod
    def get_next_available_id(cls):
        """获取下一个可用的最小ID"""
        # 获取所有已使用的ID
        used_ids = set(row[0] for row in db.session.query(cls.id).all())
        
        # 从1开始查找第一个未使用的ID
        next_id = 1
        while next_id in used_ids:
            next_id += 1
        
        return next_id
    
    @classmethod
    def create_with_min_id(cls, **kwargs):
        """创建用户并分配最小可用ID"""
        user = cls(**kwargs)
        user.id = cls.get_next_available_id()
        return user
    
    def __repr__(self):
        return f'<User {self.username}>'

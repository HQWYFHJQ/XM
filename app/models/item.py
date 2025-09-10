from datetime import datetime
from decimal import Decimal
from sqlalchemy import DECIMAL
from app import db

class Category(db.Model):
    """商品分类模型"""
    __tablename__ = 'categories'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    description = db.Column(db.Text, nullable=True)
    icon = db.Column(db.String(100), nullable=True)
    parent_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=True)
    sort_order = db.Column(db.Integer, default=0)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # 关系
    parent = db.relationship('Category', remote_side=[id], backref='children')
    items = db.relationship('Item', backref='category', lazy='dynamic')
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'icon': self.icon,
            'parent_id': self.parent_id,
            'sort_order': self.sort_order,
            'is_active': self.is_active
        }
    
    def __repr__(self):
        return f'<Category {self.name}>'

class Item(db.Model):
    """商品模型"""
    __tablename__ = 'items'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False, index=True)
    description = db.Column(db.Text, nullable=False)
    price = db.Column(DECIMAL(10, 2), nullable=False)
    original_price = db.Column(DECIMAL(10, 2), nullable=True)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False)
    seller_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    condition = db.Column(db.Enum('new', 'like_new', 'good', 'fair', 'poor'), default='good')
    images = db.Column(db.Text, nullable=True)  # JSON格式存储图片路径列表
    tags = db.Column(db.Text, nullable=True)  # JSON格式存储标签列表
    location = db.Column(db.String(200), nullable=True)
    contact_method = db.Column(db.String(50), default='message')  # message, phone, wechat
    contact_info = db.Column(db.String(200), nullable=True)
    status = db.Column(db.Enum('active', 'sold', 'inactive', 'deleted'), default='active')
    audit_status = db.Column(db.Enum('pending', 'approved', 'rejected'), default='pending')
    view_count = db.Column(db.Integer, default=0)
    like_count = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    sold_at = db.Column(db.DateTime, nullable=True)
    
    # 关系
    behaviors = db.relationship('UserBehavior', backref='item', lazy='dynamic', cascade='all, delete-orphan')
    recommendations = db.relationship('Recommendation', backref='item', lazy='dynamic', cascade='all, delete-orphan')
    transactions = db.relationship('Transaction', backref='item', lazy='dynamic', cascade='all, delete-orphan')
    
    def get_images_list(self):
        """获取图片列表"""
        if self.images:
            import json
            try:
                return json.loads(self.images)
            except:
                return []
        return []
    
    def set_images_list(self, images_list):
        """设置图片列表"""
        import json
        self.images = json.dumps(images_list, ensure_ascii=False)
    
    def get_tags_list(self):
        """获取标签列表"""
        if self.tags:
            import json
            try:
                return json.loads(self.tags)
            except:
                return []
        return []
    
    def set_tags_list(self, tags_list):
        """设置标签列表"""
        import json
        self.tags = json.dumps(tags_list, ensure_ascii=False)
    
    def get_main_image(self):
        """获取主图片"""
        images = self.get_images_list()
        return images[0] if images else None
    
    def increment_view_count(self):
        """增加浏览次数"""
        self.view_count += 1
        db.session.commit()
    
    def to_dict(self, include_seller=False):
        """转换为字典"""
        result = {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'price': float(self.price),
            'original_price': float(self.original_price) if self.original_price else None,
            'category_id': self.category_id,
            'category_name': self.category.name if self.category else None,
            'condition': self.condition,
            'images': self.get_images_list(),
            'main_image': self.get_main_image(),
            'tags': self.get_tags_list(),
            'location': self.location,
            'contact_method': self.contact_method,
            'status': self.status,
            'audit_status': self.audit_status,
            'view_count': self.view_count,
            'like_count': self.like_count,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
        
        if include_seller:
            result['seller'] = self.seller.to_dict()
        
        return result
    
    def __repr__(self):
        return f'<Item {self.title}>'

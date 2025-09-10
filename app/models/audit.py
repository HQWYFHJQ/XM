from datetime import datetime
from app import db

class UserAudit(db.Model):
    """用户注册审核模型"""
    __tablename__ = 'user_audits'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    status = db.Column(db.Enum('pending', 'approved', 'rejected'), default='pending')
    admin_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    admin_notes = db.Column(db.Text, nullable=True)
    rejection_reason = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    reviewed_at = db.Column(db.DateTime, nullable=True)
    
    # 关系
    user = db.relationship('User', foreign_keys=[user_id], backref='audit_records')
    admin = db.relationship('User', foreign_keys=[admin_id], backref='audit_actions')
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'status': self.status,
            'admin_id': self.admin_id,
            'admin_notes': self.admin_notes,
            'rejection_reason': self.rejection_reason,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'reviewed_at': self.reviewed_at.isoformat() if self.reviewed_at else None,
            'user': self.user.to_dict() if self.user else None,
            'admin': self.admin.to_dict() if self.admin else None
        }
    
    def __repr__(self):
        return f'<UserAudit {self.id}: {self.status}>'

class ItemAudit(db.Model):
    """商品发布审核模型"""
    __tablename__ = 'item_audits'
    
    id = db.Column(db.Integer, primary_key=True)
    item_id = db.Column(db.Integer, db.ForeignKey('items.id'), nullable=False)
    status = db.Column(db.Enum('pending', 'approved', 'rejected'), default='pending')
    admin_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    admin_notes = db.Column(db.Text, nullable=True)
    rejection_reason = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    reviewed_at = db.Column(db.DateTime, nullable=True)
    
    # 添加唯一约束，防止同一商品有多条待审核记录
    __table_args__ = (
        db.Index('idx_item_pending_audit', 'item_id', 'status', unique=True),
    )
    
    # 关系
    item = db.relationship('Item', backref='audit_records')
    admin = db.relationship('User', backref='item_audit_actions')
    
    def to_dict(self):
        return {
            'id': self.id,
            'item_id': self.item_id,
            'status': self.status,
            'admin_id': self.admin_id,
            'admin_notes': self.admin_notes,
            'rejection_reason': self.rejection_reason,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'reviewed_at': self.reviewed_at.isoformat() if self.reviewed_at else None,
            'item': self.item.to_dict() if self.item else None,
            'admin': self.admin.to_dict() if self.admin else None
        }
    
    def __repr__(self):
        return f'<ItemAudit {self.id}: {self.status}>'

class UserProfileAudit(db.Model):
    """用户资料修改审核模型"""
    __tablename__ = 'user_profile_audits'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    status = db.Column(db.Enum('pending', 'approved', 'rejected'), default='pending')
    admin_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    admin_notes = db.Column(db.Text, nullable=True)
    rejection_reason = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    reviewed_at = db.Column(db.DateTime, nullable=True)
    
    # 修改前的数据（JSON格式）
    old_data = db.Column(db.Text, nullable=True)
    # 修改后的数据（JSON格式）
    new_data = db.Column(db.Text, nullable=True)
    
    # 单项审核状态（JSON格式，存储每个字段的审核状态）
    item_status = db.Column(db.Text, nullable=True)  # {"real_name": "approved", "phone": "rejected", ...}
    # 单项审核备注（JSON格式，存储每个字段的审核备注）
    item_notes = db.Column(db.Text, nullable=True)  # {"real_name": "通过", "phone": "电话号码格式不正确", ...}
    
    # 关系
    user = db.relationship('User', foreign_keys=[user_id], backref='profile_audit_records')
    admin = db.relationship('User', foreign_keys=[admin_id], backref='profile_audit_actions')
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'status': self.status,
            'admin_id': self.admin_id,
            'admin_notes': self.admin_notes,
            'rejection_reason': self.rejection_reason,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'reviewed_at': self.reviewed_at.isoformat() if self.reviewed_at else None,
            'old_data': self.old_data,
            'new_data': self.new_data,
            'user': self.user.to_dict() if self.user else None,
            'admin': self.admin.to_dict() if self.admin else None
        }
    
    def __repr__(self):
        return f'<UserProfileAudit {self.id}: {self.status}>'

class ItemProfileAudit(db.Model):
    """商品资料修改审核模型"""
    __tablename__ = 'item_profile_audits'
    
    id = db.Column(db.Integer, primary_key=True)
    item_id = db.Column(db.Integer, db.ForeignKey('items.id'), nullable=False)
    status = db.Column(db.Enum('pending', 'approved', 'rejected'), default='pending')
    admin_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    admin_notes = db.Column(db.Text, nullable=True)
    rejection_reason = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    reviewed_at = db.Column(db.DateTime, nullable=True)
    
    # 修改前的数据（JSON格式）
    old_data = db.Column(db.Text, nullable=True)
    # 修改后的数据（JSON格式）
    new_data = db.Column(db.Text, nullable=True)
    
    # 单项审核状态（JSON格式，存储每个字段的审核状态）
    item_status = db.Column(db.Text, nullable=True)  # {"title": "approved", "price": "rejected", ...}
    # 单项审核备注（JSON格式，存储每个字段的审核备注）
    item_notes = db.Column(db.Text, nullable=True)  # {"title": "通过", "price": "价格不合理", ...}
    
    # 关系
    item = db.relationship('Item', backref='profile_audit_records')
    admin = db.relationship('User', foreign_keys=[admin_id], backref='item_profile_audit_actions')
    
    def to_dict(self):
        return {
            'id': self.id,
            'item_id': self.item_id,
            'status': self.status,
            'admin_id': self.admin_id,
            'admin_notes': self.admin_notes,
            'rejection_reason': self.rejection_reason,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'reviewed_at': self.reviewed_at.isoformat() if self.reviewed_at else None,
            'old_data': self.old_data,
            'new_data': self.new_data,
            'item': self.item.to_dict() if self.item else None,
            'admin': self.admin.to_dict() if self.admin else None
        }
    
    def __repr__(self):
        return f'<ItemProfileAudit {self.id}: {self.status}>'

class UserAvatarAudit(db.Model):
    """用户头像修改审核模型"""
    __tablename__ = 'user_avatar_audits'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    status = db.Column(db.Enum('pending', 'approved', 'rejected'), default='pending')
    admin_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    admin_notes = db.Column(db.Text, nullable=True)
    rejection_reason = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    reviewed_at = db.Column(db.DateTime, nullable=True)
    
    # 修改前的头像URL
    old_avatar = db.Column(db.String(500), nullable=True)
    # 修改后的头像URL
    new_avatar = db.Column(db.String(500), nullable=True)
    
    # 关系
    user = db.relationship('User', foreign_keys=[user_id], backref='avatar_audit_records')
    admin = db.relationship('User', foreign_keys=[admin_id], backref='avatar_audit_actions')
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'status': self.status,
            'admin_id': self.admin_id,
            'admin_notes': self.admin_notes,
            'rejection_reason': self.rejection_reason,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'reviewed_at': self.reviewed_at.isoformat() if self.reviewed_at else None,
            'old_avatar': self.old_avatar,
            'new_avatar': self.new_avatar,
            'user': self.user.to_dict() if self.user else None,
            'admin': self.admin.to_dict() if self.admin else None
        }
    
    def __repr__(self):
        return f'<UserAvatarAudit {self.id}: {self.status}>'

class ItemImageAudit(db.Model):
    """商品图片修改审核模型"""
    __tablename__ = 'item_image_audits'
    
    id = db.Column(db.Integer, primary_key=True)
    item_id = db.Column(db.Integer, db.ForeignKey('items.id'), nullable=False)
    status = db.Column(db.Enum('pending', 'approved', 'rejected'), default='pending')
    admin_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    admin_notes = db.Column(db.Text, nullable=True)
    rejection_reason = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    reviewed_at = db.Column(db.DateTime, nullable=True)
    
    # 修改前的图片URLs（JSON格式）
    old_images = db.Column(db.Text, nullable=True)
    # 修改后的图片URLs（JSON格式）
    new_images = db.Column(db.Text, nullable=True)
    
    # 关系
    item = db.relationship('Item', foreign_keys=[item_id], backref='image_audit_records')
    admin = db.relationship('User', foreign_keys=[admin_id], backref='item_image_audit_actions')
    
    def to_dict(self):
        return {
            'id': self.id,
            'item_id': self.item_id,
            'status': self.status,
            'admin_id': self.admin_id,
            'admin_notes': self.admin_notes,
            'rejection_reason': self.rejection_reason,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'reviewed_at': self.reviewed_at.isoformat() if self.reviewed_at else None,
            'old_images': self.old_images,
            'new_images': self.new_images,
            'item': self.item.to_dict() if self.item else None,
            'admin': self.admin.to_dict() if self.admin else None
        }
    
    def __repr__(self):
        return f'<ItemImageAudit {self.id}: {self.status}>'

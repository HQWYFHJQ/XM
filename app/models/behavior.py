from datetime import datetime
from app import db

class UserBehavior(db.Model):
    """用户行为模型"""
    __tablename__ = 'user_behaviors'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    item_id = db.Column(db.Integer, db.ForeignKey('items.id'), nullable=False)
    behavior_type = db.Column(db.Enum('view', 'like', 'favorite', 'contact', 'purchase'), nullable=False)
    duration = db.Column(db.Integer, nullable=True)  # 浏览时长（秒）
    ip_address = db.Column(db.String(45), nullable=True)
    user_agent = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    
    # 复合索引
    __table_args__ = (
        db.Index('idx_user_item_behavior', 'user_id', 'item_id', 'behavior_type'),
        db.Index('idx_user_behavior_time', 'user_id', 'behavior_type', 'created_at'),
    )
    
    def to_dict(self):
        """转换为字典"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'item_id': self.item_id,
            'behavior_type': self.behavior_type,
            'duration': self.duration,
            'ip_address': self.ip_address,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
    
    def __repr__(self):
        return f'<UserBehavior {self.user_id}-{self.item_id}-{self.behavior_type}>'

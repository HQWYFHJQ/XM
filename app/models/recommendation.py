from datetime import datetime
from app import db

class Recommendation(db.Model):
    """推荐记录模型"""
    __tablename__ = 'recommendations'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    item_id = db.Column(db.Integer, db.ForeignKey('items.id'), nullable=False)
    algorithm_type = db.Column(db.Enum('collaborative_filtering', 'content_based', 'hybrid', 'popularity'), nullable=False)
    score = db.Column(db.Float, nullable=False)
    reason = db.Column(db.Text, nullable=True)  # 推荐理由
    is_clicked = db.Column(db.Boolean, default=False)  # 是否被点击
    is_purchased = db.Column(db.Boolean, default=False)  # 是否被购买
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    clicked_at = db.Column(db.DateTime, nullable=True)
    purchased_at = db.Column(db.DateTime, nullable=True)
    
    # 复合索引
    __table_args__ = (
        db.Index('idx_user_recommendation', 'user_id', 'created_at'),
        db.Index('idx_algorithm_score', 'algorithm_type', 'score'),
    )
    
    def to_dict(self):
        """转换为字典"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'item_id': self.item_id,
            'algorithm_type': self.algorithm_type,
            'score': self.score,
            'reason': self.reason,
            'is_clicked': self.is_clicked,
            'is_purchased': self.is_purchased,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'clicked_at': self.clicked_at.isoformat() if self.clicked_at else None,
            'purchased_at': self.purchased_at.isoformat() if self.purchased_at else None
        }
    
    def __repr__(self):
        return f'<Recommendation {self.user_id}-{self.item_id}-{self.algorithm_type}>'

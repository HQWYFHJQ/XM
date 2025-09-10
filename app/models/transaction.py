from datetime import datetime
from sqlalchemy import DECIMAL
from app import db

class Transaction(db.Model):
    """交易记录模型"""
    __tablename__ = 'transactions'
    
    id = db.Column(db.Integer, primary_key=True)
    item_id = db.Column(db.Integer, db.ForeignKey('items.id'), nullable=False)
    buyer_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    seller_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    price = db.Column(DECIMAL(10, 2), nullable=False)
    status = db.Column(db.Enum('pending', 'confirmed', 'completed', 'cancelled'), default='pending')
    payment_method = db.Column(db.String(50), nullable=True)  # cash, wechat, alipay, etc.
    meeting_location = db.Column(db.String(200), nullable=True)
    meeting_time = db.Column(db.DateTime, nullable=True)
    buyer_notes = db.Column(db.Text, nullable=True)
    seller_notes = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    completed_at = db.Column(db.DateTime, nullable=True)
    
    # 关系
    buyer = db.relationship('User', foreign_keys=[buyer_id], backref='purchases')
    seller = db.relationship('User', foreign_keys=[seller_id], backref='sales')
    
    def to_dict(self):
        """转换为字典"""
        return {
            'id': self.id,
            'item_id': self.item_id,
            'item_title': self.item.title if self.item else None,
            'buyer_id': self.buyer_id,
            'buyer_name': self.buyer.username if self.buyer else None,
            'seller_id': self.seller_id,
            'seller_name': self.seller.username if self.seller else None,
            'price': float(self.price),
            'status': self.status,
            'payment_method': self.payment_method,
            'meeting_location': self.meeting_location,
            'meeting_time': self.meeting_time.isoformat() if self.meeting_time else None,
            'buyer_notes': self.buyer_notes,
            'seller_notes': self.seller_notes,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'completed_at': self.completed_at.isoformat() if self.completed_at else None
        }
    
    def __repr__(self):
        return f'<Transaction {self.id}-{self.buyer_id}-{self.seller_id}>'

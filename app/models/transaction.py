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
    status = db.Column(db.Enum('pending', 'paid', 'shipped', 'delivered', 'completed', 'cancelled', 'timeout'), default='pending')
    payment_method = db.Column(db.String(50), nullable=True)  # cash, wechat, alipay, etc.
    meeting_location = db.Column(db.String(200), nullable=True)
    meeting_time = db.Column(db.DateTime, nullable=True)
    buyer_notes = db.Column(db.Text, nullable=True)
    seller_notes = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    completed_at = db.Column(db.DateTime, nullable=True)
    
    # 新增字段
    payment_confirmed_at = db.Column(db.DateTime, nullable=True)  # 支付确认时间
    shipped_at = db.Column(db.DateTime, nullable=True)  # 发货时间
    delivered_at = db.Column(db.DateTime, nullable=True)  # 收货确认时间
    timeout_at = db.Column(db.DateTime, nullable=True)  # 超时时间
    shipping_notes = db.Column(db.Text, nullable=True)  # 发货备注
    delivery_notes = db.Column(db.Text, nullable=True)  # 收货备注
    dispute_reason = db.Column(db.Text, nullable=True)  # 争议原因
    admin_notes = db.Column(db.Text, nullable=True)  # 管理员备注
    
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
            'completed_at': self.completed_at.isoformat() if self.completed_at else None,
            'payment_confirmed_at': self.payment_confirmed_at.isoformat() if self.payment_confirmed_at else None,
            'shipped_at': self.shipped_at.isoformat() if self.shipped_at else None,
            'delivered_at': self.delivered_at.isoformat() if self.delivered_at else None,
            'timeout_at': self.timeout_at.isoformat() if self.timeout_at else None,
            'shipping_notes': self.shipping_notes,
            'delivery_notes': self.delivery_notes,
            'dispute_reason': self.dispute_reason,
            'admin_notes': self.admin_notes
        }
    
    def confirm_payment(self):
        """确认支付"""
        self.status = 'paid'
        self.payment_confirmed_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()
    
    def mark_shipped(self, shipping_notes=None):
        """标记为已发货"""
        self.status = 'shipped'
        self.shipped_at = datetime.utcnow()
        self.shipping_notes = shipping_notes
        self.updated_at = datetime.utcnow()
    
    def mark_delivered(self, delivery_notes=None):
        """标记为已收货"""
        self.status = 'delivered'
        self.delivered_at = datetime.utcnow()
        self.delivery_notes = delivery_notes
        self.updated_at = datetime.utcnow()
    
    def complete_transaction(self):
        """完成交易"""
        self.status = 'completed'
        self.completed_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()
        
        # 更新商品状态为已出售
        if hasattr(self, 'item') and self.item:
            self.item.status = 'sold'
            if not self.item.sold_at:
                self.item.sold_at = datetime.utcnow()
    
    def cancel_transaction(self, reason=None):
        """取消交易"""
        self.status = 'cancelled'
        self.dispute_reason = reason
        self.updated_at = datetime.utcnow()
        
        # 恢复商品状态为活跃
        if hasattr(self, 'item') and self.item:
            self.item.status = 'active'
            self.item.sold_at = None
    
    def timeout_transaction(self):
        """交易超时"""
        self.status = 'timeout'
        self.timeout_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()
        
        # 恢复商品状态为活跃
        if hasattr(self, 'item') and self.item:
            self.item.status = 'active'
            self.item.sold_at = None
    
    def is_payment_timeout(self, hours=72):
        """检查支付是否超时（默认72小时）"""
        if self.status != 'pending':
            return False
        from datetime import timedelta
        return datetime.utcnow() > self.created_at + timedelta(hours=hours)
    
    def is_shipping_timeout(self, hours=72):
        """检查发货是否超时（默认72小时）"""
        if self.status != 'paid':
            return False
        from datetime import timedelta
        return datetime.utcnow() > self.payment_confirmed_at + timedelta(hours=hours)
    
    def is_delivery_timeout(self, hours=72):
        """检查收货是否超时（默认72小时）"""
        if self.status != 'shipped':
            return False
        from datetime import timedelta
        return datetime.utcnow() > self.shipped_at + timedelta(hours=hours)
    
    def __repr__(self):
        return f'<Transaction {self.id}-{self.buyer_id}-{self.seller_id}>'

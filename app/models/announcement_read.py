from datetime import datetime
from app import db

class AnnouncementRead(db.Model):
    """公告已读记录模型"""
    __tablename__ = 'announcement_reads'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, comment='用户ID')
    announcement_id = db.Column(db.Integer, db.ForeignKey('announcements.id'), nullable=False, comment='公告ID')
    read_at = db.Column(db.DateTime, default=datetime.utcnow, comment='阅读时间')
    
    # 关联关系
    user = db.relationship('User', backref='announcement_reads', lazy='select')
    announcement = db.relationship('Announcement', backref='read_records', lazy='select')
    
    # 唯一约束：一个用户只能对同一个公告记录一次已读
    __table_args__ = (
        db.UniqueConstraint('user_id', 'announcement_id', name='unique_user_announcement_read'),
        db.Index('idx_announcement_read_user', 'user_id'),
        db.Index('idx_announcement_read_announcement', 'announcement_id'),
        db.Index('idx_announcement_read_time', 'read_at'),
    )
    
    def __repr__(self):
        return f'<AnnouncementRead user_id={self.user_id} announcement_id={self.announcement_id}>'
    
    def to_dict(self):
        """转换为字典"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'announcement_id': self.announcement_id,
            'read_at': self.read_at.isoformat() if self.read_at else None
        }
    
    @classmethod
    def mark_as_read(cls, user_id, announcement_id):
        """标记公告为已读"""
        # 检查是否已经记录过
        existing = cls.query.filter_by(
            user_id=user_id, 
            announcement_id=announcement_id
        ).first()
        
        if not existing:
            read_record = cls(
                user_id=user_id,
                announcement_id=announcement_id
            )
            db.session.add(read_record)
            db.session.commit()
            return read_record
        return existing
    
    @classmethod
    def get_read_announcement_ids(cls, user_id):
        """获取用户已读的公告ID列表"""
        records = cls.query.filter_by(user_id=user_id).all()
        return [record.announcement_id for record in records]
    
    @classmethod
    def is_read(cls, user_id, announcement_id):
        """检查用户是否已读某个公告"""
        return cls.query.filter_by(
            user_id=user_id, 
            announcement_id=announcement_id
        ).first() is not None

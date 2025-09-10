# -*- coding: utf-8 -*-
"""
消息系统数据模型
"""

from app import db
from datetime import datetime, timedelta
from sqlalchemy import Index


class Conversation(db.Model):
    """对话模型"""
    __tablename__ = 'conversations'
    
    id = db.Column(db.Integer, primary_key=True)
    # 参与者ID列表，用JSON存储
    participants = db.Column(db.JSON, nullable=False)
    # 对话类型：item_chat（商品咨询）、general（一般聊天）
    conversation_type = db.Column(db.String(20), default='general', nullable=False)
    # 关联的商品ID（如果是商品咨询）
    item_id = db.Column(db.Integer, db.ForeignKey('items.id'), nullable=True)
    # 最后一条消息的时间
    last_message_at = db.Column(db.DateTime, default=datetime.utcnow)
    # 创建时间
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    # 更新时间
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    # 是否已删除
    is_deleted = db.Column(db.Boolean, default=False)
    
    # 关联关系
    item = db.relationship('Item', backref='conversations')
    messages = db.relationship('Message', backref='conversation', lazy='dynamic', cascade='all, delete-orphan')
    
    # 索引
    __table_args__ = (
        Index('idx_conversation_participants', 'participants'),
        Index('idx_conversation_type', 'conversation_type'),
        Index('idx_conversation_item', 'item_id'),
        Index('idx_conversation_last_message', 'last_message_at'),
    )
    
    def __repr__(self):
        return f'<Conversation {self.id}>'
    
    def get_other_participant(self, user_id):
        """获取对话中的另一个参与者"""
        if len(self.participants) != 2:
            return None
        return self.participants[0] if self.participants[1] == user_id else self.participants[1]
    
    def get_unread_count(self, user_id):
        """获取用户未读消息数量"""
        return self.messages.filter(
            Message.sender_id != user_id,
            Message.is_read == False,
            Message.is_deleted == False
        ).count()
    
    def mark_as_read(self, user_id):
        """标记对话为已读"""
        self.messages.filter(
            Message.sender_id != user_id,
            Message.is_read == False
        ).update({'is_read': True})
        db.session.commit()


class Message(db.Model):
    """消息模型"""
    __tablename__ = 'messages'
    
    id = db.Column(db.Integer, primary_key=True)
    # 对话ID
    conversation_id = db.Column(db.Integer, db.ForeignKey('conversations.id'), nullable=False)
    # 发送者ID
    sender_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    # 消息内容
    content = db.Column(db.Text, nullable=False)
    # 消息类型：text（文本）、image（图片）、file（文件）
    message_type = db.Column(db.String(20), default='text', nullable=False)
    # 附件URL（图片、文件等）
    attachment_url = db.Column(db.String(500), nullable=True)
    # 是否已读
    is_read = db.Column(db.Boolean, default=False)
    # 是否已删除
    is_deleted = db.Column(db.Boolean, default=False)
    # 创建时间
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    # 更新时间
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # 关联关系
    sender = db.relationship('User', backref='sent_messages')
    
    # 索引
    __table_args__ = (
        Index('idx_message_conversation', 'conversation_id'),
        Index('idx_message_sender', 'sender_id'),
        Index('idx_message_created', 'created_at'),
        Index('idx_message_read', 'is_read'),
    )
    
    def __repr__(self):
        return f'<Message {self.id}>'
    
    def to_dict(self):
        """转换为字典格式"""
        return {
            'id': self.id,
            'conversation_id': self.conversation_id,
            'sender_id': self.sender_id,
            'sender_name': self.sender.username if self.sender else '未知用户',
            'content': self.content,
            'message_type': self.message_type,
            'attachment_url': self.attachment_url,
            'is_read': self.is_read,
            'created_at': self.created_at.isoformat(),
            'formatted_time': self.get_formatted_time()
        }
    
    def get_formatted_time(self):
        """获取格式化的时间显示"""
        now = datetime.utcnow()
        diff = now - self.created_at
        
        if diff.days > 0:
            return self.created_at.strftime('%m-%d %H:%M')
        elif diff.seconds > 3600:
            hours = diff.seconds // 3600
            return f'{hours}小时前'
        elif diff.seconds > 60:
            minutes = diff.seconds // 60
            return f'{minutes}分钟前'
        else:
            return '刚刚'


class MessageNotification(db.Model):
    """消息通知模型"""
    __tablename__ = 'message_notifications'
    
    id = db.Column(db.Integer, primary_key=True)
    # 接收者ID
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    # 对话ID
    conversation_id = db.Column(db.Integer, db.ForeignKey('conversations.id'), nullable=False)
    # 消息ID
    message_id = db.Column(db.Integer, db.ForeignKey('messages.id'), nullable=False)
    # 通知类型：new_message（新消息）、mention（提及）
    notification_type = db.Column(db.String(20), default='new_message', nullable=False)
    # 是否已读
    is_read = db.Column(db.Boolean, default=False)
    # 创建时间
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # 关联关系
    user = db.relationship('User', backref='message_notifications')
    conversation = db.relationship('Conversation', backref='notifications')
    message = db.relationship('Message', backref='notifications')
    
    # 索引
    __table_args__ = (
        Index('idx_notification_user', 'user_id'),
        Index('idx_notification_conversation', 'conversation_id'),
        Index('idx_notification_read', 'is_read'),
        Index('idx_notification_created', 'created_at'),
    )
    
    def __repr__(self):
        return f'<MessageNotification {self.id}>'


class ChatSession(db.Model):
    """聊天会话模型（用于存储用户在线状态等）"""
    __tablename__ = 'chat_sessions'
    
    id = db.Column(db.Integer, primary_key=True)
    # 用户ID
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, unique=True)
    # 会话ID（用于WebSocket连接）
    session_id = db.Column(db.String(100), nullable=False)
    # 是否在线
    is_online = db.Column(db.Boolean, default=False)
    # 最后活跃时间
    last_active_at = db.Column(db.DateTime, default=datetime.utcnow)
    # 创建时间
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    # 更新时间
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # 关联关系
    user = db.relationship('User', backref='chat_session')
    
    # 索引
    __table_args__ = (
        Index('idx_chat_session_user', 'user_id'),
        Index('idx_chat_session_online', 'is_online'),
        Index('idx_chat_session_active', 'last_active_at'),
    )
    
    def __repr__(self):
        return f'<ChatSession {self.id}>'
    
    def is_recently_active(self, minutes=5):
        """检查是否最近活跃"""
        return (datetime.utcnow() - self.last_active_at).seconds < minutes * 60


# 消息清理任务相关
class MessageCleanupLog(db.Model):
    """消息清理日志"""
    __tablename__ = 'message_cleanup_logs'
    
    id = db.Column(db.Integer, primary_key=True)
    # 清理时间
    cleanup_time = db.Column(db.DateTime, default=datetime.utcnow)
    # 清理的消息数量
    messages_deleted = db.Column(db.Integer, default=0)
    # 清理的对话数量
    conversations_deleted = db.Column(db.Integer, default=0)
    # 清理的过期时间（天）
    retention_days = db.Column(db.Integer, default=30)
    
    def __repr__(self):
        return f'<MessageCleanupLog {self.id}>'

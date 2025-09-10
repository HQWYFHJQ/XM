# -*- coding: utf-8 -*-
"""
消息服务类
"""

from app import db
from app.models import Conversation, Message, MessageNotification, ChatSession, User, Item
from datetime import datetime, timedelta
from sqlalchemy import and_, or_, desc
import json


class MessageService:
    """消息服务类"""
    
    @staticmethod
    def create_conversation(participants, conversation_type='general', item_id=None):
        """创建对话"""
        # 检查是否已存在相同的对话
        existing_conversation = Conversation.query.filter(
            Conversation.participants == participants,
            Conversation.conversation_type == conversation_type,
            Conversation.item_id == item_id,
            Conversation.is_deleted == False
        ).first()
        
        if existing_conversation:
            return existing_conversation
        
        conversation = Conversation(
            participants=participants,
            conversation_type=conversation_type,
            item_id=item_id
        )
        
        db.session.add(conversation)
        db.session.commit()
        return conversation
    
    @staticmethod
    def get_conversation(conversation_id):
        """获取对话"""
        return Conversation.query.get(conversation_id)
    
    @staticmethod
    def get_user_conversations(user_id, page=1, per_page=20):
        """获取用户的所有对话"""
        from app import db
        conversations = Conversation.query.filter(
            db.func.json_contains(Conversation.participants, str(user_id)),
            Conversation.is_deleted == False
        ).order_by(desc(Conversation.last_message_at)).paginate(
            page=page, per_page=per_page, error_out=False
        )
        
        return conversations
    
    @staticmethod
    def get_conversation_by_participants(participants, conversation_type='general', item_id=None):
        """根据参与者获取对话"""
        return Conversation.query.filter(
            Conversation.participants == participants,
            Conversation.conversation_type == conversation_type,
            Conversation.item_id == item_id,
            Conversation.is_deleted == False
        ).first()
    
    @staticmethod
    def send_message(conversation_id, sender_id, content, message_type='text', attachment_url=None):
        """发送消息"""        
        conversation = Conversation.query.get(conversation_id)
        if not conversation:
            return None
        
        
        # 检查发送者是否有权限发送消息
        if sender_id not in conversation.participants:
            return None
        
        message = Message(
            conversation_id=conversation_id,
            sender_id=sender_id,
            content=content,
            message_type=message_type,
            attachment_url=attachment_url
        )
        
        db.session.add(message)
        
        # 更新对话的最后消息时间
        conversation.last_message_at = datetime.utcnow()
        
        # 先提交消息以获取ID
        db.session.flush()  # 刷新以获取message.id
        
        # 创建通知
        MessageService._create_notifications(conversation, message, sender_id)
        
        db.session.commit()
        return message
    
    @staticmethod
    def _create_notifications(conversation, message, sender_id):
        """创建消息通知"""
        for participant_id in conversation.participants:
            if participant_id != sender_id:
                notification = MessageNotification(
                    user_id=participant_id,
                    conversation_id=conversation.id,
                    message_id=message.id,
                    notification_type='new_message'
                )
                db.session.add(notification)
    
    @staticmethod
    def get_messages(conversation_id, page=1, per_page=50):
        """获取对话的消息列表"""
        messages = Message.query.filter(
            Message.conversation_id == conversation_id,
            Message.is_deleted == False
        ).order_by(Message.created_at).paginate(
            page=page, per_page=per_page, error_out=False
        )
        
        return messages
    
    @staticmethod
    def mark_messages_as_read(conversation_id, user_id):
        """标记消息为已读"""
        # 标记消息为已读
        Message.query.filter(
            Message.conversation_id == conversation_id,
            Message.sender_id != user_id,
            Message.is_read == False
        ).update({'is_read': True})
        
        # 标记通知为已读
        MessageNotification.query.filter(
            MessageNotification.conversation_id == conversation_id,
            MessageNotification.user_id == user_id,
            MessageNotification.is_read == False
        ).update({'is_read': True})
        
        db.session.commit()
    
    @staticmethod
    def get_unread_count(user_id):
        """获取用户未读消息总数"""
        # 只统计未删除对话的通知
        count = MessageNotification.query.join(Conversation).filter(
            MessageNotification.user_id == user_id,
            MessageNotification.is_read == False,
            Conversation.is_deleted == False
        ).count()
        return count
    
    @staticmethod
    def get_conversation_unread_count(conversation_id, user_id):
        """获取对话的未读消息数"""
        return Message.query.filter(
            Message.conversation_id == conversation_id,
            Message.sender_id != user_id,
            Message.is_read == False,
            Message.is_deleted == False
        ).count()
    
    @staticmethod
    def delete_message(message_id, user_id):
        """删除消息（软删除）"""
        message = Message.query.get(message_id)
        if not message or message.sender_id != user_id:
            return False
        
        message.is_deleted = True
        db.session.commit()
        return True
    
    @staticmethod
    def delete_conversation(conversation_id, user_id):
        """删除对话（软删除）"""
        conversation = Conversation.query.get(conversation_id)
        if not conversation or user_id not in conversation.participants:
            return False
        
        # 检查删除前的通知数量
        before_notifications = MessageNotification.query.filter(
            MessageNotification.conversation_id == conversation_id
        ).count()
        
        # 软删除对话
        conversation.is_deleted = True
        
        # 软删除对话中的所有消息
        Message.query.filter(
            Message.conversation_id == conversation_id,
            Message.is_deleted == False
        ).update({'is_deleted': True})
        
        # 删除相关的通知记录（硬删除，因为对话已删除）
        deleted_notifications = MessageNotification.query.filter(
            MessageNotification.conversation_id == conversation_id
        ).delete()
        
        db.session.commit()
        
        # 检查删除后的通知数量
        after_notifications = MessageNotification.query.filter(
            MessageNotification.conversation_id == conversation_id
        ).count()
        
        return True
    
    @staticmethod
    def batch_delete_conversations(conversation_ids, user_id):
        """批量删除对话（软删除）"""
        deleted_count = 0
        
        for conversation_id in conversation_ids:
            conversation = Conversation.query.get(conversation_id)
            if conversation and user_id in conversation.participants:
                
                # 检查删除前的通知数量
                before_notifications = MessageNotification.query.filter(
                    MessageNotification.conversation_id == conversation_id
                ).count()
                
                # 软删除对话
                conversation.is_deleted = True
                
                # 软删除对话中的所有消息
                Message.query.filter(
                    Message.conversation_id == conversation_id,
                    Message.is_deleted == False
                ).update({'is_deleted': True})
                
                # 删除相关的通知记录（硬删除，因为对话已删除）
                deleted_notifications = MessageNotification.query.filter(
                    MessageNotification.conversation_id == conversation_id
                ).delete()
                
                deleted_count += 1
        
        db.session.commit()
        return deleted_count
    
    @staticmethod
    def search_messages(user_id, query, page=1, per_page=20):
        """搜索消息"""
        from app import db
        # 获取用户参与的对话
        user_conversations = Conversation.query.filter(
            db.func.json_contains(Conversation.participants, str(user_id)),
            Conversation.is_deleted == False
        ).all()
        
        conversation_ids = [conv.id for conv in user_conversations]
        
        # 搜索消息
        messages = Message.query.filter(
            Message.conversation_id.in_(conversation_ids),
            Message.content.contains(query),
            Message.is_deleted == False
        ).order_by(desc(Message.created_at)).paginate(
            page=page, per_page=per_page, error_out=False
        )
        
        return messages
    
    @staticmethod
    def get_recent_conversations(user_id, limit=10):
        """获取最近的对话"""
        from app import db
        conversations = Conversation.query.filter(
            db.func.json_contains(Conversation.participants, str(user_id)),
            Conversation.is_deleted == False
        ).order_by(desc(Conversation.last_message_at)).limit(limit).all()
        
        return conversations
    
    @staticmethod
    def create_item_chat(seller_id, buyer_id, item_id):
        """创建商品咨询对话"""
        participants = sorted([seller_id, buyer_id])
        return MessageService.create_conversation(
            participants=participants,
            conversation_type='item_chat',
            item_id=item_id
        )
    
    @staticmethod
    def get_item_chat(seller_id, buyer_id, item_id):
        """获取商品咨询对话"""
        participants = sorted([seller_id, buyer_id])
        return MessageService.get_conversation_by_participants(
            participants=participants,
            conversation_type='item_chat',
            item_id=item_id
        )
    
    @staticmethod
    def update_chat_session(user_id, session_id, is_online=True):
        """更新聊天会话状态"""
        session = ChatSession.query.filter_by(user_id=user_id).first()
        
        if session:
            session.session_id = session_id
            session.is_online = is_online
            session.last_active_at = datetime.utcnow()
        else:
            session = ChatSession(
                user_id=user_id,
                session_id=session_id,
                is_online=is_online
            )
            db.session.add(session)
        
        db.session.commit()
        return session
    
    @staticmethod
    def get_online_users():
        """获取在线用户列表"""
        five_minutes_ago = datetime.utcnow() - timedelta(minutes=5)
        
        sessions = ChatSession.query.filter(
            ChatSession.is_online == True,
            ChatSession.last_active_at >= five_minutes_ago
        ).all()
        
        return [session.user for session in sessions if session.user]
    
    @staticmethod
    def cleanup_old_messages(retention_days=30):
        """清理过期消息"""
        cutoff_date = datetime.utcnow() - timedelta(days=retention_days)
        
        # 删除过期消息
        deleted_messages = Message.query.filter(
            Message.created_at < cutoff_date
        ).count()
        
        Message.query.filter(
            Message.created_at < cutoff_date
        ).delete()
        
        # 删除没有消息的对话
        empty_conversations = Conversation.query.filter(
            ~Conversation.id.in_(
                db.session.query(Message.conversation_id).distinct()
            ),
            Conversation.created_at < cutoff_date
        ).count()
        
        Conversation.query.filter(
            ~Conversation.id.in_(
                db.session.query(Message.conversation_id).distinct()
            ),
            Conversation.created_at < cutoff_date
        ).delete()
        
        # 记录清理日志
        cleanup_log = MessageCleanupLog(
            messages_deleted=deleted_messages,
            conversations_deleted=empty_conversations,
            retention_days=retention_days
        )
        db.session.add(cleanup_log)
        
        db.session.commit()
        
        return {
            'messages_deleted': deleted_messages,
            'conversations_deleted': empty_conversations
        }
    
    @staticmethod
    def get_conversation_with_user_info(conversation_id, current_user_id):
        """获取包含用户信息的对话详情"""
        conversation = Conversation.query.get(conversation_id)
        if not conversation:
            return None
        
        # 获取其他参与者信息
        other_participant_id = conversation.get_other_participant(current_user_id)
        other_participant = User.query.get(other_participant_id) if other_participant_id else None
        
        # 获取商品信息（如果是商品咨询）
        item = None
        if conversation.item_id:
            item = Item.query.get(conversation.item_id)
        
        return {
            'conversation': conversation,
            'other_participant': other_participant,
            'item': item,
            'unread_count': conversation.get_unread_count(current_user_id)
        }

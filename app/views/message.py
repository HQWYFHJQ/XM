# -*- coding: utf-8 -*-
"""
消息相关视图
"""

from flask import Blueprint, render_template, request, jsonify, current_app
from flask_login import login_required, current_user
from app import db
from app.services.message_service import MessageService
from app.models import User, Item, Message
import json

message_bp = Blueprint('message', __name__)


@message_bp.route('/')
@login_required
def messages():
    """我的消息页面"""
    page = request.args.get('page', 1, type=int)
    conversations = MessageService.get_user_conversations(current_user.id, page=page)
    
    # 获取每个对话的详细信息
    conversation_list = []
    for conv in conversations.items:
        other_participant_id = conv.get_other_participant(current_user.id)
        other_participant = User.query.get(other_participant_id) if other_participant_id else None
        
        # 获取最后一条消息
        last_message = conv.messages.filter_by(is_deleted=False).order_by(Message.created_at.desc()).first()
        
        # 获取商品信息（如果是商品咨询）
        item = None
        if conv.item_id:
            item = Item.query.get(conv.item_id)
        
        conversation_list.append({
            'conversation': conv,
            'other_participant': other_participant,
            'last_message': last_message,
            'item': item,
            'unread_count': conv.get_unread_count(current_user.id)
        })
    
    return render_template('message/messages.html', 
                         conversations=conversations,
                         conversation_list=conversation_list)


@message_bp.route('/<int:conversation_id>')
@login_required
def conversation_detail(conversation_id):
    """对话详情页面"""
    conversation_data = MessageService.get_conversation_with_user_info(conversation_id, current_user.id)
    
    if not conversation_data:
        return jsonify({'error': '对话不存在'}), 404
    
    # 检查用户是否有权限访问此对话
    if current_user.id not in conversation_data['conversation'].participants:
        return jsonify({'error': '无权限访问此对话'}), 403
    
    # 标记消息为已读
    MessageService.mark_messages_as_read(conversation_id, current_user.id)
    
    # 获取消息列表
    page = request.args.get('page', 1, type=int)
    messages = MessageService.get_messages(conversation_id, page=page)
    
    return render_template('message/conversation_detail.html',
                         conversation_data=conversation_data,
                         messages=messages)



















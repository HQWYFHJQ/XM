# -*- coding: utf-8 -*-
"""
消息相关API视图
"""

from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from app import db
from app.services.message_service import MessageService
from app.models import User, Item, Message
import json

message_api_bp = Blueprint('message_api', __name__)


@message_api_bp.route('/send', methods=['POST'])
@login_required
def send_message():
    """发送消息API"""
    data = request.get_json()
    
    conversation_id = data.get('conversation_id')
    content = data.get('content', '').strip()
    message_type = data.get('message_type', 'text')
    attachment_url = data.get('attachment_url')
    
    print(f"DEBUG: 发送消息请求 - conversation_id: {conversation_id}, content: {content}, sender: {current_user.id}")
    
    if not conversation_id or not content:
        return jsonify({'error': '参数不完整'}), 400
    
    # 检查对话是否存在且用户有权限
    conversation = MessageService.get_conversation(conversation_id)
    if not conversation:
        return jsonify({'error': '对话不存在'}), 404
    if current_user.id not in conversation.participants:
        return jsonify({'error': '无权限访问此对话'}), 403
    
    # 发送消息
    message = MessageService.send_message(
        conversation_id=conversation_id,
        sender_id=current_user.id,
        content=content,
        message_type=message_type,
        attachment_url=attachment_url
    )
    
    if not message:
        return jsonify({'error': '发送失败'}), 500
    
    return jsonify({
        'success': True,
        'message': message.to_dict()
    })


@message_api_bp.route('/conversations')
@login_required
def get_conversations():
    """获取对话列表API"""
    page = request.args.get('page', 1, type=int)
    conversations = MessageService.get_user_conversations(current_user.id, page=page)
    
    conversation_list = []
    for conv in conversations.items:
        other_participant_id = conv.get_other_participant(current_user.id)
        other_participant = User.query.get(other_participant_id) if other_participant_id else None
        
        # 获取最后一条消息
        last_message = conv.messages.filter_by(is_deleted=False).order_by(Message.created_at.desc()).first()
        
        # 获取商品信息
        item = None
        if conv.item_id:
            item = Item.query.get(conv.item_id)
        
        conversation_list.append({
            'id': conv.id,
            'other_participant': {
                'id': other_participant.id if other_participant else None,
                'username': other_participant.username if other_participant else '未知用户',
                'avatar': other_participant.avatar if other_participant else None
            },
            'item': {
                'id': item.id if item else None,
                'title': item.title if item else None,
                'main_image': item.get_main_image() if item else None
            } if item else None,
            'last_message': {
                'content': last_message.content if last_message else '',
                'created_at': last_message.created_at.isoformat() if last_message else None,
                'sender_id': last_message.sender_id if last_message else None
            } if last_message else None,
            'unread_count': conv.get_unread_count(current_user.id),
            'last_message_at': conv.last_message_at.isoformat()
        })
    
    return jsonify({
        'success': True,
        'conversations': conversation_list,
        'pagination': {
            'page': conversations.page,
            'pages': conversations.pages,
            'per_page': conversations.per_page,
            'total': conversations.total,
            'has_next': conversations.has_next,
            'has_prev': conversations.has_prev
        }
    })


@message_api_bp.route('/<int:conversation_id>/messages')
@login_required
def get_messages(conversation_id):
    """获取消息列表API"""
    # 检查权限
    conversation = MessageService.get_conversation(conversation_id)
    if not conversation:
        return jsonify({'error': '对话不存在'}), 404
    if current_user.id not in conversation.participants:
        return jsonify({'error': '无权限访问此对话'}), 403
    
    page = request.args.get('page', 1, type=int)
    messages = MessageService.get_messages(conversation_id, page=page)
    
    message_list = []
    for msg in messages.items:
        message_list.append(msg.to_dict())
    
    return jsonify({
        'success': True,
        'messages': message_list,
        'pagination': {
            'page': messages.page,
            'pages': messages.pages,
            'per_page': messages.per_page,
            'total': messages.total,
            'has_next': messages.has_next,
            'has_prev': messages.has_prev
        }
    })


@message_api_bp.route('/<int:conversation_id>/read', methods=['POST'])
@login_required
def mark_as_read(conversation_id):
    """标记消息为已读API"""
    # 检查权限
    conversation = MessageService.get_conversation(conversation_id)
    if not conversation:
        return jsonify({'error': '对话不存在'}), 404
    if current_user.id not in conversation.participants:
        return jsonify({'error': '无权限访问此对话'}), 403
    
    MessageService.mark_messages_as_read(conversation_id, current_user.id)
    
    return jsonify({'success': True})


@message_api_bp.route('/unread-count')
@login_required
def get_unread_count():
    """获取未读消息数量API"""
    count = MessageService.get_unread_count(current_user.id)
    return jsonify({
        'success': True,
        'unread_count': count
    })


@message_api_bp.route('/start-chat', methods=['POST'])
@login_required
def start_chat():
    """开始聊天API"""
    data = request.get_json()
    
    user_id = data.get('user_id')
    item_id = data.get('item_id')  # 可选，商品咨询时使用
    
    if not user_id:
        return jsonify({'error': '缺少用户ID'}), 400
    
    if user_id == current_user.id:
        return jsonify({'error': '不能与自己聊天'}), 400
    
    # 检查用户是否存在
    target_user = User.query.get(user_id)
    if not target_user:
        return jsonify({'error': '用户不存在'}), 404
    
    # 检查商品是否存在（如果提供了item_id）
    item = None
    if item_id:
        item = Item.query.get(item_id)
        if not item:
            return jsonify({'error': '商品不存在'}), 404
    
    # 创建或获取对话
    if item_id:
        # 商品咨询
        conversation = MessageService.get_item_chat(current_user.id, user_id, item_id)
        if not conversation:
            conversation = MessageService.create_item_chat(current_user.id, user_id, item_id)
    else:
        # 一般聊天
        participants = sorted([current_user.id, user_id])
        conversation = MessageService.get_conversation_by_participants(participants)
        if not conversation:
            conversation = MessageService.create_conversation(participants)
    
    return jsonify({
        'success': True,
        'conversation_id': conversation.id
    })


@message_api_bp.route('/search')
@login_required
def search_messages():
    """搜索消息API"""
    query = request.args.get('q', '').strip()
    if not query:
        return jsonify({'error': '搜索关键词不能为空'}), 400
    
    page = request.args.get('page', 1, type=int)
    messages = MessageService.search_messages(current_user.id, query, page=page)
    
    message_list = []
    for msg in messages.items:
        message_list.append(msg.to_dict())
    
    return jsonify({
        'success': True,
        'messages': message_list,
        'query': query,
        'pagination': {
            'page': messages.page,
            'pages': messages.pages,
            'per_page': messages.per_page,
            'total': messages.total,
            'has_next': messages.has_next,
            'has_prev': messages.has_prev
        }
    })


@message_api_bp.route('/online-users')
@login_required
def get_online_users():
    """获取在线用户列表API"""
    online_users = MessageService.get_online_users()
    
    user_list = []
    for user in online_users:
        user_list.append({
            'id': user.id,
            'username': user.username,
            'avatar': user.avatar,
            'is_online': True
        })
    
    return jsonify({
        'success': True,
        'online_users': user_list
    })


@message_api_bp.route('/update-session', methods=['POST'])
@login_required
def update_chat_session():
    """更新聊天会话状态API"""
    data = request.get_json()
    session_id = data.get('session_id', '')
    
    if not session_id:
        return jsonify({'error': '会话ID不能为空'}), 400
    
    # 更新用户在线状态
    MessageService.update_chat_session(current_user.id, session_id)
    
    return jsonify({'success': True})


@message_api_bp.route('/<int:conversation_id>/delete', methods=['POST'])
@login_required
def delete_conversation(conversation_id):
    """删除对话API"""
    # 检查权限
    conversation = MessageService.get_conversation(conversation_id)
    if not conversation:
        return jsonify({'error': '对话不存在'}), 404
    if current_user.id not in conversation.participants:
        return jsonify({'error': '无权限删除此对话'}), 403
    
    # 删除对话
    success = MessageService.delete_conversation(conversation_id, current_user.id)
    if not success:
        return jsonify({'error': '删除失败'}), 500
    
    return jsonify({'success': True, 'message': '对话已删除'})


@message_api_bp.route('/batch-delete', methods=['POST'])
@login_required
def batch_delete_conversations():
    """批量删除对话API"""
    data = request.get_json()
    conversation_ids = data.get('conversation_ids', [])
    
    if not conversation_ids:
        return jsonify({'error': '请选择要删除的对话'}), 400
    
    try:
        # 使用批量删除方法
        deleted_count = MessageService.batch_delete_conversations(conversation_ids, current_user.id)
        
        return jsonify({
            'success': True,
            'deleted_count': deleted_count,
            'message': f'成功删除 {deleted_count} 个对话'
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'批量删除失败: {str(e)}'
        }), 500

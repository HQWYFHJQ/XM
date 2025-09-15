from flask import Blueprint, request, jsonify, current_app
from flask_login import login_required, current_user
from app import db
from app.models import Announcement, AnnouncementRead
from app.services.announcement_service import AnnouncementService
from app.utils import get_beijing_utc_now
import logging

announcement_api_bp = Blueprint('announcement_api', __name__)

@announcement_api_bp.route('/api/announcements/unread', methods=['GET'])
@login_required
def get_unread_announcements():
    """获取用户未读公告"""
    try:
        # 获取用户已读的公告ID列表
        read_announcement_ids = AnnouncementRead.get_read_announcement_ids(current_user.id)
        
        # 获取当前有效的公告
        announcement_service = AnnouncementService()
        active_announcements = announcement_service.get_active_announcements_for_users(limit=10)
        
        # 过滤出未读公告
        unread_announcements = []
        for announcement in active_announcements:
            if announcement.id not in read_announcement_ids:
                unread_announcements.append(announcement)
        
        # 按优先级和创建时间排序
        unread_announcements.sort(key=lambda x: (
            x.priority == 'urgent',  # urgent 最高
            x.priority == 'high',    # high 次之
            x.priority == 'normal',  # normal 再次
            x.priority == 'low',     # low 最低
            -x.created_at.timestamp()  # 时间倒序
        ), reverse=True)
        
        return jsonify({
            'success': True,
            'unread_count': len(unread_announcements),
            'announcements': [announcement.to_dict() for announcement in unread_announcements]
        })
        
    except Exception as e:
        current_app.logger.error(f"获取未读公告失败: {str(e)}")
        return jsonify({
            'success': False,
            'message': '获取未读公告失败'
        }), 500

@announcement_api_bp.route('/api/announcements/<int:announcement_id>/mark-read', methods=['POST'])
@login_required
def mark_announcement_read(announcement_id):
    """标记公告为已读"""
    try:
        # 检查公告是否存在
        announcement = Announcement.query.get(announcement_id)
        if not announcement:
            return jsonify({
                'success': False,
                'message': '公告不存在'
            }), 404
        
        # 标记为已读
        AnnouncementRead.mark_as_read(current_user.id, announcement_id)
        
        return jsonify({
            'success': True,
            'message': '已标记为已读'
        })
        
    except Exception as e:
        current_app.logger.error(f"标记公告已读失败: {str(e)}")
        return jsonify({
            'success': False,
            'message': '标记失败'
        }), 500

@announcement_api_bp.route('/api/announcements/mark-all-read', methods=['POST'])
@login_required
def mark_all_announcements_read():
    """标记所有公告为已读"""
    try:
        # 获取当前有效的公告
        announcement_service = AnnouncementService()
        active_announcements = announcement_service.get_active_announcements_for_users()
        
        # 标记所有公告为已读
        for announcement in active_announcements:
            AnnouncementRead.mark_as_read(current_user.id, announcement.id)
        
        return jsonify({
            'success': True,
            'message': f'已标记 {len(active_announcements)} 个公告为已读'
        })
        
    except Exception as e:
        current_app.logger.error(f"标记所有公告已读失败: {str(e)}")
        return jsonify({
            'success': False,
            'message': '标记失败'
        }), 500

@announcement_api_bp.route('/api/announcements/check-login', methods=['GET'])
@login_required
def check_login_announcements():
    """检查登录时是否有未读公告（用于弹窗提示）"""
    try:
        # 获取用户已读的公告ID列表
        read_announcement_ids = AnnouncementRead.get_read_announcement_ids(current_user.id)
        
        # 获取当前有效的公告
        announcement_service = AnnouncementService()
        active_announcements = announcement_service.get_active_announcements_for_users(limit=5)
        
        # 过滤出未读公告
        unread_announcements = []
        for announcement in active_announcements:
            if announcement.id not in read_announcement_ids:
                unread_announcements.append(announcement)
        
        # 返回所有未读公告用于弹窗（包括所有优先级）
        popup_announcements = unread_announcements
        
        return jsonify({
            'success': True,
            'has_unread': len(unread_announcements) > 0,
            'has_popup': len(popup_announcements) > 0,
            'unread_count': len(unread_announcements),
            'popup_announcements': [announcement.to_dict() for announcement in popup_announcements]
        })
        
    except Exception as e:
        current_app.logger.error(f"检查登录公告失败: {str(e)}")
        return jsonify({
            'success': False,
            'message': '检查失败'
        }), 500

from datetime import datetime, timedelta
from app import db
from app.models import Announcement, User
from app.utils import get_beijing_utc_now

class AnnouncementService:
    """公告服务类"""
    
    def __init__(self):
        pass
    
    def create_announcement(self, title, content, announcement_type='system', 
                          priority='normal', is_pinned=False, start_time=None, 
                          end_time=None, created_by=None):
        """创建公告"""
        try:
            announcement = Announcement(
                title=title,
                content=content,
                type=announcement_type,
                priority=priority,
                is_pinned=is_pinned,
                start_time=start_time,
                end_time=end_time,
                created_by=created_by
            )
            
            db.session.add(announcement)
            db.session.commit()
            
            return {
                'success': True,
                'message': '公告创建成功',
                'announcement': announcement
            }
        except Exception as e:
            db.session.rollback()
            return {
                'success': False,
                'message': f'创建公告失败: {str(e)}'
            }
    
    def update_announcement(self, announcement_id, **kwargs):
        """更新公告"""
        try:
            announcement = Announcement.query.get_or_404(announcement_id)
            
            # 更新字段
            for key, value in kwargs.items():
                if hasattr(announcement, key):
                    setattr(announcement, key, value)
            
            announcement.updated_at = get_beijing_utc_now()
            db.session.commit()
            
            return {
                'success': True,
                'message': '公告更新成功',
                'announcement': announcement
            }
        except Exception as e:
            db.session.rollback()
            return {
                'success': False,
                'message': f'更新公告失败: {str(e)}'
            }
    
    def delete_announcement(self, announcement_id):
        """删除公告"""
        try:
            announcement = Announcement.query.get_or_404(announcement_id)
            db.session.delete(announcement)
            db.session.commit()
            
            return {
                'success': True,
                'message': '公告删除成功'
            }
        except Exception as e:
            db.session.rollback()
            return {
                'success': False,
                'message': f'删除公告失败: {str(e)}'
            }
    
    def toggle_announcement_status(self, announcement_id):
        """切换公告状态"""
        try:
            announcement = Announcement.query.get_or_404(announcement_id)
            announcement.is_active = not announcement.is_active
            announcement.updated_at = get_beijing_utc_now()
            db.session.commit()
            
            return {
                'success': True,
                'message': f'公告已{"启用" if announcement.is_active else "禁用"}',
                'is_active': announcement.is_active
            }
        except Exception as e:
            db.session.rollback()
            return {
                'success': False,
                'message': f'操作失败: {str(e)}'
            }
    
    def toggle_pin_status(self, announcement_id):
        """切换置顶状态"""
        try:
            announcement = Announcement.query.get_or_404(announcement_id)
            announcement.is_pinned = not announcement.is_pinned
            announcement.updated_at = get_beijing_utc_now()
            db.session.commit()
            
            return {
                'success': True,
                'message': f'公告已{"置顶" if announcement.is_pinned else "取消置顶"}',
                'is_pinned': announcement.is_pinned
            }
        except Exception as e:
            db.session.rollback()
            return {
                'success': False,
                'message': f'操作失败: {str(e)}'
            }
    
    def get_announcements(self, page=1, per_page=20, status='all', 
                         announcement_type='all', priority='all', search=''):
        """获取公告列表（分页）"""
        query = Announcement.query
        
        # 状态筛选
        if status == 'active':
            query = query.filter_by(is_active=True)
        elif status == 'inactive':
            query = query.filter_by(is_active=False)
        
        # 类型筛选
        if announcement_type != 'all':
            query = query.filter_by(type=announcement_type)
        
        # 优先级筛选
        if priority != 'all':
            query = query.filter_by(priority=priority)
        
        # 搜索
        if search:
            query = query.filter(
                Announcement.title.contains(search) |
                Announcement.content.contains(search)
            )
        
        # 排序：置顶 > 优先级 > 创建时间
        query = query.order_by(
            Announcement.is_pinned.desc(),
            Announcement.priority.desc(),
            Announcement.created_at.desc()
        )
        
        return query.paginate(
            page=page, per_page=per_page, error_out=False
        )
    
    def get_active_announcements_for_users(self, limit=5):
        """获取用户可见的有效公告"""
        now = get_beijing_utc_now()
        
        # 获取置顶公告
        pinned_announcements = Announcement.query.filter_by(
            is_active=True, is_pinned=True
        ).filter(
            (Announcement.start_time.is_(None) | (Announcement.start_time <= now)),
            (Announcement.end_time.is_(None) | (Announcement.end_time >= now))
        ).order_by(
            Announcement.priority.desc(),
            Announcement.created_at.desc()
        ).all()
        
        # 获取普通公告
        regular_announcements = Announcement.query.filter_by(
            is_active=True, is_pinned=False
        ).filter(
            (Announcement.start_time.is_(None) | (Announcement.start_time <= now)),
            (Announcement.end_time.is_(None) | (Announcement.end_time >= now))
        ).order_by(
            Announcement.priority.desc(),
            Announcement.created_at.desc()
        ).limit(limit - len(pinned_announcements)).all()
        
        return pinned_announcements + regular_announcements
    
    def get_announcement_stats(self):
        """获取公告统计信息"""
        total = Announcement.query.count()
        active = Announcement.query.filter_by(is_active=True).count()
        inactive = Announcement.query.filter_by(is_active=False).count()
        pinned = Announcement.query.filter_by(is_pinned=True).count()
        
        # 按类型统计
        type_stats = db.session.query(
            Announcement.type,
            db.func.count(Announcement.id)
        ).group_by(Announcement.type).all()
        
        # 按优先级统计
        priority_stats = db.session.query(
            Announcement.priority,
            db.func.count(Announcement.id)
        ).group_by(Announcement.priority).all()
        
        return {
            'total': total,
            'active': active,
            'inactive': inactive,
            'pinned': pinned,
            'type_stats': dict(type_stats),
            'priority_stats': dict(priority_stats)
        }
    
    def get_recent_announcements(self, days=7, limit=10):
        """获取最近几天的公告"""
        since_date = get_beijing_utc_now() - timedelta(days=days)
        
        return Announcement.query.filter(
            Announcement.created_at >= since_date
        ).order_by(
            Announcement.created_at.desc()
        ).limit(limit).all()
    
    def cleanup_expired_announcements(self):
        """清理过期的公告（可选功能）"""
        now = get_beijing_utc_now()
        
        # 查找已过期的公告
        expired_announcements = Announcement.query.filter(
            Announcement.end_time < now,
            Announcement.is_active == True
        ).all()
        
        # 自动禁用过期公告
        for announcement in expired_announcements:
            announcement.is_active = False
            announcement.updated_at = now
        
        if expired_announcements:
            db.session.commit()
            return {
                'success': True,
                'message': f'已自动禁用 {len(expired_announcements)} 个过期公告',
                'count': len(expired_announcements)
            }
        
        return {
            'success': True,
            'message': '没有发现过期公告',
            'count': 0
        }

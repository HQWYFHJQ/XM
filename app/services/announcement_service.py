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
                          end_time=None, created_by=None, use_min_id=True,
                          target_type='all', target_user_ids=None, target_conditions=None,
                          is_direct_push=False):
        """创建公告"""
        try:
            # 如果启用最小可用ID分配
            if use_min_id:
                announcement_id = self._get_next_available_id()
            else:
                announcement_id = None
            
            # 处理目标用户ID列表
            import json
            target_user_ids_json = None
            if target_user_ids:
                target_user_ids_json = json.dumps(target_user_ids)
            
            # 处理推送条件
            target_conditions_json = None
            if target_conditions:
                target_conditions_json = json.dumps(target_conditions)
            
            announcement = Announcement(
                id=announcement_id,
                title=title,
                content=content,
                type=announcement_type,
                priority=priority,
                is_pinned=is_pinned,
                start_time=start_time,
                end_time=end_time,
                created_by=created_by,
                target_type=target_type,
                target_user_ids=target_user_ids_json,
                target_conditions=target_conditions_json,
                is_direct_push=is_direct_push
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
            
            # 先删除所有相关的已读记录
            from app.models.announcement_read import AnnouncementRead
            AnnouncementRead.query.filter_by(announcement_id=announcement_id).delete()
            
            # 再删除公告
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
                         announcement_type='all', priority='all', search='', 
                         sort_by='created_at', sort_order='desc'):
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
        
        # 排序
        if sort_by == 'id':
            if sort_order == 'asc':
                query = query.order_by(Announcement.id.asc())
            else:
                query = query.order_by(Announcement.id.desc())
        elif sort_by == 'created_at':
            if sort_order == 'asc':
                query = query.order_by(Announcement.created_at.asc())
            else:
                query = query.order_by(Announcement.created_at.desc())
        elif sort_by == 'priority':
            if sort_order == 'asc':
                query = query.order_by(Announcement.priority.asc())
            else:
                query = query.order_by(Announcement.priority.desc())
        else:
            # 默认排序：置顶 > 优先级 > 创建时间
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
    
    def _get_next_available_id(self):
        """获取下一个可用的最小ID"""
        # 获取所有已使用的ID
        used_ids = set(db.session.query(Announcement.id).all())
        used_ids = {id_tuple[0] for id_tuple in used_ids}
        
        # 从1开始查找第一个未使用的ID
        next_id = 1
        while next_id in used_ids:
            next_id += 1
        
        return next_id
    
    def get_announcement_read_stats(self, announcement_id):
        """获取公告的已读统计"""
        from app.models.announcement_read import AnnouncementRead
        from app.models import User
        
        # 获取总用户数
        total_users = User.query.count()
        
        # 获取已读用户数
        read_count = AnnouncementRead.query.filter_by(announcement_id=announcement_id).count()
        
        # 计算已读率
        read_rate = (read_count / total_users * 100) if total_users > 0 else 0
        
        return {
            'total_users': total_users,
            'read_count': read_count,
            'unread_count': total_users - read_count,
            'read_rate': round(read_rate, 2)
        }
    
    def get_announcement_push_status(self, announcement_id):
        """获取公告的推送状态"""
        announcement = Announcement.query.get(announcement_id)
        if not announcement:
            return None
        
        now = get_beijing_utc_now()
        
        # 检查是否已推送（创建时间小于当前时间）
        is_pushed = announcement.created_at <= now
        
        # 检查是否在有效期内
        is_valid = True
        if announcement.start_time and announcement.start_time > now:
            is_valid = False
        if announcement.end_time and announcement.end_time < now:
            is_valid = False
        
        # 检查是否启用
        is_active = announcement.is_active
        
        return {
            'is_pushed': is_pushed,
            'is_valid': is_valid,
            'is_active': is_active,
            'status': self._get_push_status_text(is_pushed, is_valid, is_active)
        }
    
    def _get_push_status_text(self, is_pushed, is_valid, is_active):
        """获取推送状态文本"""
        if not is_active:
            return "已禁用"
        elif not is_valid:
            return "已过期"
        elif not is_pushed:
            return "待推送"
        else:
            return "已推送"
    
    def send_direct_push(self, announcement_id):
        """发送定向推送"""
        try:
            announcement = Announcement.query.get(announcement_id)
            if not announcement:
                return {
                    'success': False,
                    'message': '公告不存在'
                }
            
            if not announcement.is_direct_push:
                return {
                    'success': False,
                    'message': '该公告不是定向推送公告'
                }
            
            if announcement.push_sent:
                return {
                    'success': False,
                    'message': '该公告已经发送过推送'
                }
            
            # 获取目标用户
            target_users = announcement.get_target_users()
            
            if not target_users:
                return {
                    'success': False,
                    'message': '没有找到目标用户'
                }
            
            # 发送邮件通知
            from app.services.email_service import EmailService
            email_service = EmailService()
            
            success_count = 0
            failed_count = 0
            
            for user in target_users:
                try:
                    # 检查是否应该向该用户推送
                    if not announcement.should_push_to_user(user):
                        continue
                    
                    # 发送邮件
                    subject = f'校园跳蚤市场 - {announcement.title}'
                    body = f"""
                    <html>
                    <body>
                        <h2>{announcement.title}</h2>
                        <div>{announcement.render_content()}</div>
                        <hr>
                        <p style="color: #666; font-size: 12px;">此邮件由系统自动发送，请勿回复。</p>
                    </body>
                    </html>
                    """
                    
                    result = email_service.send_email(user.email, subject, body)
                    if result['success']:
                        success_count += 1
                    else:
                        failed_count += 1
                        
                except Exception as e:
                    failed_count += 1
                    print(f"发送邮件给用户 {user.username} 失败: {str(e)}")
            
            # 标记为已发送
            announcement.mark_as_sent()
            
            return {
                'success': True,
                'message': f'定向推送完成，成功发送 {success_count} 条，失败 {failed_count} 条',
                'success_count': success_count,
                'failed_count': failed_count
            }
            
        except Exception as e:
            return {
                'success': False,
                'message': f'发送定向推送失败: {str(e)}'
            }
    
    def create_transaction_announcement(self, transaction, announcement_type='notice'):
        """为交易创建定向公告"""
        try:
            if announcement_type == 'shipping_reminder':
                # 发货提醒公告
                title = f"发货提醒 - {transaction.item.title}"
                content = f"""
                <p>您有商品需要发货：</p>
                <ul>
                    <li>商品：{transaction.item.title}</li>
                    <li>价格：¥{transaction.price}</li>
                    <li>买家：{transaction.buyer.username}</li>
                    <li>购买时间：{transaction.created_at.strftime('%Y-%m-%d %H:%M:%S')}</li>
                </ul>
                <p>请及时登录系统确认发货！</p>
                """
                
                # 只推送给卖家
                return self.create_announcement(
                    title=title,
                    content=content,
                    announcement_type=announcement_type,
                    priority='high',
                    created_by=1,  # 系统管理员
                    target_type='specific',
                    target_user_ids=[transaction.seller_id],
                    is_direct_push=True
                )
            
            elif announcement_type == 'delivery_reminder':
                # 收货提醒公告
                title = f"收货提醒 - {transaction.item.title}"
                content = f"""
                <p>您购买的商品已发货：</p>
                <ul>
                    <li>商品：{transaction.item.title}</li>
                    <li>价格：¥{transaction.price}</li>
                    <li>卖家：{transaction.seller.username}</li>
                    <li>发货时间：{transaction.shipped_at.strftime('%Y-%m-%d %H:%M:%S')}</li>
                </ul>
                <p>请及时确认收货！</p>
                """
                
                # 只推送给买家
                return self.create_announcement(
                    title=title,
                    content=content,
                    announcement_type=announcement_type,
                    priority='high',
                    created_by=1,  # 系统管理员
                    target_type='specific',
                    target_user_ids=[transaction.buyer_id],
                    is_direct_push=True
                )
            
            elif announcement_type == 'timeout_notification':
                # 超时通知公告
                title = f"交易超时通知 - {transaction.item.title}"
                content = f"""
                <p>您的交易已超时：</p>
                <ul>
                    <li>商品：{transaction.item.title}</li>
                    <li>价格：¥{transaction.price}</li>
                    <li>超时原因：{transaction.dispute_reason or '系统超时'}</li>
                    <li>超时时间：{transaction.timeout_at.strftime('%Y-%m-%d %H:%M:%S')}</li>
                </ul>
                <p>如有疑问，请联系系统管理员：21641685@qq.com</p>
                """
                
                # 推送给买家和卖家
                return self.create_announcement(
                    title=title,
                    content=content,
                    announcement_type=announcement_type,
                    priority='urgent',
                    created_by=1,  # 系统管理员
                    target_type='specific',
                    target_user_ids=[transaction.buyer_id, transaction.seller_id],
                    is_direct_push=True
                )
            
            return {
                'success': False,
                'message': '不支持的公告类型'
            }
            
        except Exception as e:
            return {
                'success': False,
                'message': f'创建交易公告失败: {str(e)}'
            }

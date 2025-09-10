from datetime import datetime
from flask import current_app
from app import db
from app.models import User, Item, UserAudit, ItemAudit, UserProfileAudit, ItemProfileAudit, UserAvatarAudit, ItemImageAudit
from app.services.email_service import EmailService
from app.utils import get_beijing_utc_now

class AuditService:
    """审核服务类"""
    
    def __init__(self):
        self.email_service = EmailService()
    
    def create_user_audit(self, user_id):
        """创建用户审核记录"""
        try:
            audit = UserAudit(
                user_id=user_id,
                status='pending'
            )
            db.session.add(audit)
            db.session.commit()
            return audit
        except Exception as e:
            db.session.rollback()
            raise e
    
    def create_item_audit(self, item_id):
        """创建商品审核记录"""
        try:
            # 检查是否已存在待审核记录
            existing_audit = ItemAudit.query.filter_by(
                item_id=item_id, 
                status='pending'
            ).first()
            
            if existing_audit:
                return existing_audit
            
            audit = ItemAudit(
                item_id=item_id,
                status='pending'
            )
            db.session.add(audit)
            db.session.commit()
            return audit
        except Exception as e:
            db.session.rollback()
            raise e
    
    def approve_user(self, user_id, admin_id, admin_notes=None):
        """审核通过用户"""
        try:
            user = User.query.get(user_id)
            if not user:
                return {'success': False, 'message': '用户不存在'}
            
            # 更新用户审核状态
            user.audit_status = 'approved'
            user.is_active = True
            
            # 更新审核记录
            audit = UserAudit.query.filter_by(user_id=user_id, status='pending').first()
            if audit:
                audit.status = 'approved'
                audit.admin_id = admin_id
                audit.admin_notes = admin_notes
                audit.reviewed_at = get_beijing_utc_now()
            
            db.session.commit()
            
            # 发送邮件通知
            self._send_user_audit_notification(user, 'approved', admin_notes)
            
            return {'success': True, 'message': '用户审核通过'}
        except Exception as e:
            db.session.rollback()
            return {'success': False, 'message': f'审核失败: {str(e)}'}
    
    def reject_user(self, user_id, admin_id, rejection_reason, admin_notes=None):
        """审核拒绝用户"""
        try:
            user = User.query.get(user_id)
            if not user:
                return {'success': False, 'message': '用户不存在'}
            
            # 更新用户审核状态
            user.audit_status = 'rejected'
            user.is_active = False
            
            # 更新审核记录
            audit = UserAudit.query.filter_by(user_id=user_id, status='pending').first()
            if audit:
                audit.status = 'rejected'
                audit.admin_id = admin_id
                audit.admin_notes = admin_notes
                audit.rejection_reason = rejection_reason
                audit.reviewed_at = get_beijing_utc_now()
            
            db.session.commit()
            
            # 发送邮件通知
            self._send_user_audit_notification(user, 'rejected', admin_notes, rejection_reason)
            
            return {'success': True, 'message': '用户审核拒绝'}
        except Exception as e:
            db.session.rollback()
            return {'success': False, 'message': f'审核失败: {str(e)}'}
    
    def approve_item(self, item_id, admin_id, admin_notes=None):
        """审核通过商品"""
        try:
            item = Item.query.get(item_id)
            if not item:
                return {'success': False, 'message': '商品不存在'}
            
            # 更新商品审核状态
            item.audit_status = 'approved'
            item.status = 'active'
            
            # 更新审核记录
            audit = ItemAudit.query.filter_by(item_id=item_id, status='pending').first()
            if audit:
                audit.status = 'approved'
                audit.admin_id = admin_id
                audit.admin_notes = admin_notes
                audit.reviewed_at = get_beijing_utc_now()
            
            db.session.commit()
            
            # 发送邮件通知
            self._send_item_audit_notification(item, 'approved', admin_notes)
            
            return {'success': True, 'message': '商品审核通过'}
        except Exception as e:
            db.session.rollback()
            return {'success': False, 'message': f'审核失败: {str(e)}'}
    
    def reject_item(self, item_id, admin_id, rejection_reason, admin_notes=None):
        """审核拒绝商品"""
        try:
            item = Item.query.get(item_id)
            if not item:
                return {'success': False, 'message': '商品不存在'}
            
            # 更新商品审核状态
            item.audit_status = 'rejected'
            item.status = 'inactive'
            
            # 更新审核记录
            audit = ItemAudit.query.filter_by(item_id=item_id, status='pending').first()
            if audit:
                audit.status = 'rejected'
                audit.admin_id = admin_id
                audit.admin_notes = admin_notes
                audit.rejection_reason = rejection_reason
                audit.reviewed_at = get_beijing_utc_now()
            
            db.session.commit()
            
            # 发送邮件通知
            self._send_item_audit_notification(item, 'rejected', admin_notes, rejection_reason)
            
            return {'success': True, 'message': '商品审核拒绝'}
        except Exception as e:
            db.session.rollback()
            return {'success': False, 'message': f'审核失败: {str(e)}'}
    
    def get_pending_user_audits(self):
        """获取待审核的用户列表"""
        return UserAudit.query.filter_by(status='pending').order_by(UserAudit.created_at.asc()).all()
    
    def get_pending_item_audits(self):
        """获取待审核的商品列表"""
        return ItemAudit.query.filter_by(status='pending').order_by(ItemAudit.created_at.asc()).all()
    
    def get_audit_stats(self):
        """获取审核统计信息"""
        pending_users = UserAudit.query.filter_by(status='pending').count()
        pending_items = ItemAudit.query.filter_by(status='pending').count()
        pending_user_profiles = UserProfileAudit.query.filter_by(status='pending').count()
        pending_item_profiles = ItemProfileAudit.query.filter_by(status='pending').count()
        
        return {
            'pending_users': pending_users,
            'pending_items': pending_items,
            'pending_user_profiles': pending_user_profiles,
            'pending_item_profiles': pending_item_profiles,
            'total_pending': pending_users + pending_items + pending_user_profiles + pending_item_profiles
        }
    
    # 用户资料修改审核方法
    def create_user_profile_audit(self, user_id, old_data, new_data):
        """创建用户资料修改审核记录"""
        try:
            import json
            audit = UserProfileAudit(
                user_id=user_id,
                status='pending',
                old_data=json.dumps(old_data, ensure_ascii=False),
                new_data=json.dumps(new_data, ensure_ascii=False)
            )
            db.session.add(audit)
            db.session.commit()
            return audit
        except Exception as e:
            db.session.rollback()
            raise e
    
    def approve_user_profile(self, audit_id, admin_id, admin_notes=None):
        """审核通过用户资料修改"""
        try:
            audit = UserProfileAudit.query.get(audit_id)
            if not audit:
                return {'success': False, 'message': '审核记录不存在'}
            
            user = User.query.get(audit.user_id)
            if not user:
                return {'success': False, 'message': '用户不存在'}
            
            # 应用修改后的数据
            import json
            new_data = json.loads(audit.new_data)
            for field, value in new_data.items():
                if field == 'interests':
                    # 特殊处理interests字段
                    user.set_interests_list(value)
                elif hasattr(user, field):
                    setattr(user, field, value)
            
            # 更新审核记录
            audit.status = 'approved'
            audit.admin_id = admin_id
            audit.admin_notes = admin_notes
            audit.reviewed_at = get_beijing_utc_now()
            
            db.session.commit()
            
            # 发送邮件通知
            self._send_user_profile_audit_notification(user, 'approved', admin_notes)
            
            return {'success': True, 'message': '用户资料修改审核通过'}
        except Exception as e:
            db.session.rollback()
            return {'success': False, 'message': f'审核失败: {str(e)}'}
    
    def reject_user_profile(self, audit_id, admin_id, rejection_reason, admin_notes=None):
        """审核拒绝用户资料修改"""
        try:
            audit = UserProfileAudit.query.get(audit_id)
            if not audit:
                return {'success': False, 'message': '审核记录不存在'}
            
            user = User.query.get(audit.user_id)
            if not user:
                return {'success': False, 'message': '用户不存在'}
            
            # 更新审核记录
            audit.status = 'rejected'
            audit.admin_id = admin_id
            audit.admin_notes = admin_notes
            audit.rejection_reason = rejection_reason
            audit.reviewed_at = get_beijing_utc_now()
            
            db.session.commit()
            
            # 发送邮件通知
            self._send_user_profile_audit_notification(user, 'rejected', admin_notes, rejection_reason)
            
            return {'success': True, 'message': '用户资料修改审核拒绝'}
        except Exception as e:
            db.session.rollback()
            return {'success': False, 'message': f'审核失败: {str(e)}'}
    
    def get_pending_user_profile_audits(self):
        """获取待审核的用户资料修改列表"""
        return UserProfileAudit.query.filter_by(status='pending').order_by(UserProfileAudit.created_at.asc()).all()
    
    # 商品资料修改审核方法
    def create_item_profile_audit(self, item_id, old_data, new_data):
        """创建商品资料修改审核记录"""
        try:
            import json
            audit = ItemProfileAudit(
                item_id=item_id,
                status='pending',
                old_data=json.dumps(old_data, ensure_ascii=False),
                new_data=json.dumps(new_data, ensure_ascii=False)
            )
            db.session.add(audit)
            db.session.commit()
            return audit
        except Exception as e:
            db.session.rollback()
            raise e
    
    def approve_item_profile(self, audit_id, admin_id, admin_notes=None):
        """审核通过商品资料修改"""
        try:
            audit = ItemProfileAudit.query.get(audit_id)
            if not audit:
                return {'success': False, 'message': '审核记录不存在'}
            
            item = Item.query.get(audit.item_id)
            if not item:
                return {'success': False, 'message': '商品不存在'}
            
            # 应用修改后的数据
            import json
            new_data = json.loads(audit.new_data)
            for field, value in new_data.items():
                if hasattr(item, field):
                    setattr(item, field, value)
            
            # 更新审核记录
            audit.status = 'approved'
            audit.admin_id = admin_id
            audit.admin_notes = admin_notes
            audit.reviewed_at = get_beijing_utc_now()
            
            db.session.commit()
            
            # 发送邮件通知
            self._send_item_profile_audit_notification(item, 'approved', admin_notes)
            
            return {'success': True, 'message': '商品资料修改审核通过'}
        except Exception as e:
            db.session.rollback()
            return {'success': False, 'message': f'审核失败: {str(e)}'}
    
    def reject_item_profile(self, audit_id, admin_id, rejection_reason, admin_notes=None):
        """审核拒绝商品资料修改"""
        try:
            audit = ItemProfileAudit.query.get(audit_id)
            if not audit:
                return {'success': False, 'message': '审核记录不存在'}
            
            item = Item.query.get(audit.item_id)
            if not item:
                return {'success': False, 'message': '商品不存在'}
            
            # 更新审核记录
            audit.status = 'rejected'
            audit.admin_id = admin_id
            audit.admin_notes = admin_notes
            audit.rejection_reason = rejection_reason
            audit.reviewed_at = get_beijing_utc_now()
            
            db.session.commit()
            
            # 发送邮件通知
            self._send_item_profile_audit_notification(item, 'rejected', admin_notes, rejection_reason)
            
            return {'success': True, 'message': '商品资料修改审核拒绝'}
        except Exception as e:
            db.session.rollback()
            return {'success': False, 'message': f'审核失败: {str(e)}'}
    
    def get_pending_item_profile_audits(self):
        """获取待审核的商品资料修改列表"""
        return ItemProfileAudit.query.filter_by(status='pending').order_by(ItemProfileAudit.created_at.asc()).all()
    
    def _send_user_audit_notification(self, user, result, admin_notes=None, rejection_reason=None):
        """发送用户审核结果邮件通知"""
        try:
            if result == 'approved':
                subject = '校园跳蚤市场 - 用户注册审核通过 ✓'
                body = f"""
                <html>
                <body>
                    <h2>✓ 恭喜！您的用户注册已审核通过</h2>
                    <p>亲爱的 {user.username}，</p>
                    <p>您的用户注册申请已通过管理员审核，现在可以正常使用校园跳蚤市场平台了！</p>
                    <p>您可以：</p>
                    <ul>
                        <li>✓ 浏览和搜索商品</li>
                        <li>✓ 发布自己的商品</li>
                        <li>✓ 联系其他用户</li>
                        <li>✓ 享受个性化推荐服务</li>
                    </ul>
                    {f'<p><strong>管理员备注：</strong>{admin_notes}</p>' if admin_notes else ''}
                    <p>感谢您使用校园跳蚤市场！</p>
                    <hr>
                    <p style="color: #666; font-size: 12px;">此邮件由系统自动发送，请勿回复。</p>
                </body>
                </html>
                """
            else:
                subject = '校园跳蚤市场 - 用户注册审核未通过 ✗'
                body = f"""
                <html>
                <body>
                    <h2>✗ 很抱歉，您的用户注册申请未通过审核</h2>
                    <p>亲爱的 {user.username}，</p>
                    <p>很抱歉，您的用户注册申请未通过管理员审核。</p>
                    {f'<p><strong>拒绝原因：</strong>{rejection_reason}</p>' if rejection_reason else ''}
                    {f'<p><strong>管理员备注：</strong>{admin_notes}</p>' if admin_notes else ''}
                    <p>您可以重新注册并完善信息后再次提交申请。</p>
                    <p>如有疑问，请联系平台管理员。</p>
                    <hr>
                    <p style="color: #666; font-size: 12px;">此邮件由系统自动发送，请勿回复。</p>
                </body>
                </html>
                """
            
            # 发送邮件
            from flask_mail import Message
            from flask import current_app
            
            msg = Message(
                subject=subject,
                recipients=[user.email],
                html=body,
                sender=current_app.config['MAIL_DEFAULT_SENDER']
            )
            
            self.email_service.mail.send(msg)
            
        except Exception as e:
            # 邮件发送失败不影响审核流程
            print(f"发送用户审核通知邮件失败: {e}")
    
    def _send_item_audit_notification(self, item, result, admin_notes=None, rejection_reason=None):
        """发送商品审核结果邮件通知"""
        try:
            if result == 'approved':
                subject = '校园跳蚤市场 - 商品发布审核通过 ✓'
                body = f"""
                <html>
                <body>
                    <h2>✓ 恭喜！您的商品已审核通过</h2>
                    <p>亲爱的 {item.seller.username}，</p>
                    <p>您发布的商品《{item.title}》已通过管理员审核，现在可以在平台上正常显示了！</p>
                    <p>商品信息：</p>
                    <ul>
                        <li>✓ 商品名称：{item.title}</li>
                        <li>✓ 价格：¥{item.price}</li>
                        <li>✓ 分类：{item.category.name if item.category else '未分类'}</li>
                    </ul>
                    {f'<p><strong>管理员备注：</strong>{admin_notes}</p>' if admin_notes else ''}
                    <p>感谢您使用校园跳蚤市场！</p>
                    <hr>
                    <p style="color: #666; font-size: 12px;">此邮件由系统自动发送，请勿回复。</p>
                </body>
                </html>
                """
            else:
                subject = '校园跳蚤市场 - 商品发布审核未通过 ✗'
                body = f"""
                <html>
                <body>
                    <h2>✗ 很抱歉，您的商品发布申请未通过审核</h2>
                    <p>亲爱的 {item.seller.username}，</p>
                    <p>很抱歉，您发布的商品《{item.title}》未通过管理员审核。</p>
                    {f'<p><strong>拒绝原因：</strong>{rejection_reason}</p>' if rejection_reason else ''}
                    {f'<p><strong>管理员备注：</strong>{admin_notes}</p>' if admin_notes else ''}
                    <p>您可以修改商品信息后重新提交审核。</p>
                    <p>如有疑问，请联系平台管理员。</p>
                    <hr>
                    <p style="color: #666; font-size: 12px;">此邮件由系统自动发送，请勿回复。</p>
                </body>
                </html>
                """
            
            # 发送邮件
            from flask_mail import Message
            from flask import current_app
            
            msg = Message(
                subject=subject,
                recipients=[item.seller.email],
                html=body,
                sender=current_app.config['MAIL_DEFAULT_SENDER']
            )
            
            self.email_service.mail.send(msg)
            
        except Exception as e:
            # 邮件发送失败不影响审核流程
            print(f"发送商品审核通知邮件失败: {e}")
    
    def _send_user_profile_audit_notification(self, user, result, admin_notes=None, rejection_reason=None):
        """发送用户资料修改审核结果邮件通知"""
        try:
            if result == 'approved':
                subject = '校园跳蚤市场 - 用户资料修改审核通过 ✓'
                body = f"""
                <html>
                <body>
                    <h2>✓ 恭喜！您的用户资料修改已审核通过</h2>
                    <p>亲爱的 {user.username}，</p>
                    <p>您的用户资料修改申请已通过管理员审核，修改已生效！</p>
                    {f'<p><strong>管理员备注：</strong>{admin_notes}</p>' if admin_notes else ''}
                    <p>感谢您使用校园跳蚤市场！</p>
                    <hr>
                    <p style="color: #666; font-size: 12px;">此邮件由系统自动发送，请勿回复。</p>
                </body>
                </html>
                """
            else:
                subject = '校园跳蚤市场 - 用户资料修改审核未通过 ✗'
                body = f"""
                <html>
                <body>
                    <h2>✗ 很抱歉，您的用户资料修改申请未通过审核</h2>
                    <p>亲爱的 {user.username}，</p>
                    <p>很抱歉，您的用户资料修改申请未通过管理员审核。</p>
                    {f'<p><strong>拒绝原因：</strong>{rejection_reason}</p>' if rejection_reason else ''}
                    {f'<p><strong>管理员备注：</strong>{admin_notes}</p>' if admin_notes else ''}
                    <p>您可以重新修改资料后再次提交申请。</p>
                    <p>如有疑问，请联系平台管理员。</p>
                    <hr>
                    <p style="color: #666; font-size: 12px;">此邮件由系统自动发送，请勿回复。</p>
                </body>
                </html>
                """
            
            # 发送邮件
            from flask_mail import Message
            from flask import current_app
            
            msg = Message(
                subject=subject,
                recipients=[user.email],
                html=body,
                sender=current_app.config['MAIL_DEFAULT_SENDER']
            )
            
            self.email_service.mail.send(msg)
            
        except Exception as e:
            # 邮件发送失败不影响审核流程
            print(f"发送用户资料修改审核通知邮件失败: {e}")
    
    def _send_item_profile_audit_notification(self, item, result, admin_notes=None, rejection_reason=None):
        """发送商品资料修改审核结果邮件通知"""
        try:
            if result == 'approved':
                subject = '校园跳蚤市场 - 商品资料修改审核通过 ✓'
                body = f"""
                <html>
                <body>
                    <h2>✓ 恭喜！您的商品资料修改已审核通过</h2>
                    <p>亲爱的 {item.seller.username}，</p>
                    <p>您对商品《{item.title}》的资料修改申请已通过管理员审核，修改已生效！</p>
                    {f'<p><strong>管理员备注：</strong>{admin_notes}</p>' if admin_notes else ''}
                    <p>感谢您使用校园跳蚤市场！</p>
                    <hr>
                    <p style="color: #666; font-size: 12px;">此邮件由系统自动发送，请勿回复。</p>
                </body>
                </html>
                """
            else:
                subject = '校园跳蚤市场 - 商品资料修改审核未通过 ✗'
                body = f"""
                <html>
                <body>
                    <h2>✗ 很抱歉，您的商品资料修改申请未通过审核</h2>
                    <p>亲爱的 {item.seller.username}，</p>
                    <p>很抱歉，您对商品《{item.title}》的资料修改申请未通过管理员审核。</p>
                    {f'<p><strong>拒绝原因：</strong>{rejection_reason}</p>' if rejection_reason else ''}
                    {f'<p><strong>管理员备注：</strong>{admin_notes}</p>' if admin_notes else ''}
                    <p>您可以重新修改商品资料后再次提交申请。</p>
                    <p>如有疑问，请联系平台管理员。</p>
                    <hr>
                    <p style="color: #666; font-size: 12px;">此邮件由系统自动发送，请勿回复。</p>
                </body>
                </html>
                """
            
            # 发送邮件
            from flask_mail import Message
            from flask import current_app
            
            msg = Message(
                subject=subject,
                recipients=[item.seller.email],
                html=body,
                sender=current_app.config['MAIL_DEFAULT_SENDER']
            )
            
            self.email_service.mail.send(msg)
            
        except Exception as e:
            # 邮件发送失败不影响审核流程
            print(f"发送商品资料修改审核通知邮件失败: {e}")
    
    # ==================== 头像审核相关方法 ====================
    
    def create_user_avatar_audit(self, user_id, old_avatar, new_avatar):
        """创建用户头像修改审核记录"""
        try:
            audit = UserAvatarAudit(
                user_id=user_id,
                old_avatar=old_avatar,
                new_avatar=new_avatar,
                status='pending'
            )
            db.session.add(audit)
            db.session.commit()
            return audit
        except Exception as e:
            db.session.rollback()
            print(f"创建用户头像审核记录失败: {e}")
            return None
    
    def approve_user_avatar(self, audit_id, admin_id, admin_notes=None):
        """审核通过用户头像修改"""
        try:
            audit = UserAvatarAudit.query.get(audit_id)
            if not audit:
                return {'success': False, 'message': '审核记录不存在'}
            
            user = User.query.get(audit.user_id)
            if not user:
                return {'success': False, 'message': '用户不存在'}
            
            # 应用新的头像
            user.avatar = audit.new_avatar
            
            # 更新审核记录
            audit.status = 'approved'
            audit.admin_id = admin_id
            audit.admin_notes = admin_notes
            audit.reviewed_at = get_beijing_utc_now()
            
            db.session.commit()
            
            # 发送邮件通知
            self._send_user_avatar_audit_notification(user, 'approved', admin_notes)
            
            return {'success': True, 'message': '用户头像修改审核通过'}
        except Exception as e:
            db.session.rollback()
            return {'success': False, 'message': f'审核失败: {str(e)}'}
    
    def reject_user_avatar(self, audit_id, admin_id, rejection_reason, admin_notes=None):
        """审核拒绝用户头像修改"""
        try:
            audit = UserAvatarAudit.query.get(audit_id)
            if not audit:
                return {'success': False, 'message': '审核记录不存在'}
            
            # 更新审核记录
            audit.status = 'rejected'
            audit.admin_id = admin_id
            audit.admin_notes = admin_notes
            audit.rejection_reason = rejection_reason
            audit.reviewed_at = get_beijing_utc_now()
            
            db.session.commit()
            
            # 发送邮件通知
            user = User.query.get(audit.user_id)
            if user:
                self._send_user_avatar_audit_notification(user, 'rejected', admin_notes, rejection_reason)
            
            return {'success': True, 'message': '用户头像修改审核拒绝'}
        except Exception as e:
            db.session.rollback()
            return {'success': False, 'message': f'审核失败: {str(e)}'}
    
    def _send_user_avatar_audit_notification(self, user, result, admin_notes=None, rejection_reason=None):
        """发送用户头像审核结果邮件通知"""
        try:
            if result == 'approved':
                subject = '校园跳蚤市场 - 头像修改审核通过 ✓'
                body = f"""
                <html>
                <body>
                    <h2>✓ 恭喜！您的头像修改已审核通过</h2>
                    <p>亲爱的 {user.username}，</p>
                    <p>您的头像修改申请已通过管理员审核，新头像现在可以在平台上正常显示了！</p>
                    {f'<p><strong>管理员备注：</strong>{admin_notes}</p>' if admin_notes else ''}
                    <p>感谢您使用校园跳蚤市场！</p>
                    <hr>
                    <p style="color: #666; font-size: 12px;">此邮件由系统自动发送，请勿回复。</p>
                </body>
                </html>
                """
            else:
                subject = '校园跳蚤市场 - 头像修改审核未通过 ✗'
                body = f"""
                <html>
                <body>
                    <h2>✗ 很抱歉，您的头像修改申请未通过审核</h2>
                    <p>亲爱的 {user.username}，</p>
                    <p>很抱歉，您的头像修改申请未通过管理员审核。</p>
                    {f'<p><strong>拒绝原因：</strong>{rejection_reason}</p>' if rejection_reason else ''}
                    {f'<p><strong>管理员备注：</strong>{admin_notes}</p>' if admin_notes else ''}
                    <p>您可以重新上传符合要求的头像后再次提交审核。</p>
                    <p>如有疑问，请联系平台管理员。</p>
                    <hr>
                    <p style="color: #666; font-size: 12px;">此邮件由系统自动发送，请勿回复。</p>
                </body>
                </html>
                """
            
            msg = self.email_service.Message(
                subject=subject,
                recipients=[user.email],
                html=body,
                sender=current_app.config['MAIL_DEFAULT_SENDER']
            )
            
            self.email_service.mail.send(msg)
            
        except Exception as e:
            # 邮件发送失败不影响审核流程
            print(f"发送用户头像审核通知邮件失败: {e}")
    
    # ==================== 商品图片审核相关方法 ====================
    
    def create_item_image_audit(self, item_id, old_images, new_images):
        """创建商品图片修改审核记录"""
        try:
            import json
            audit = ItemImageAudit(
                item_id=item_id,
                old_images=json.dumps(old_images, ensure_ascii=False),
                new_images=json.dumps(new_images, ensure_ascii=False),
                status='pending'
            )
            db.session.add(audit)
            db.session.commit()
            return audit
        except Exception as e:
            db.session.rollback()
            print(f"创建商品图片审核记录失败: {e}")
            return None
    
    def approve_item_image(self, audit_id, admin_id, admin_notes=None):
        """审核通过商品图片修改"""
        try:
            audit = ItemImageAudit.query.get(audit_id)
            if not audit:
                return {'success': False, 'message': '审核记录不存在'}
            
            item = Item.query.get(audit.item_id)
            if not item:
                return {'success': False, 'message': '商品不存在'}
            
            # 应用新的图片
            import json
            new_images = json.loads(audit.new_images)
            item.images = json.dumps(new_images, ensure_ascii=False)
            
            # 更新审核记录
            audit.status = 'approved'
            audit.admin_id = admin_id
            audit.admin_notes = admin_notes
            audit.reviewed_at = get_beijing_utc_now()
            
            db.session.commit()
            
            # 发送邮件通知
            self._send_item_image_audit_notification(item, 'approved', admin_notes)
            
            return {'success': True, 'message': '商品图片修改审核通过'}
        except Exception as e:
            db.session.rollback()
            return {'success': False, 'message': f'审核失败: {str(e)}'}
    
    def reject_item_image(self, audit_id, admin_id, rejection_reason, admin_notes=None):
        """审核拒绝商品图片修改"""
        try:
            audit = ItemImageAudit.query.get(audit_id)
            if not audit:
                return {'success': False, 'message': '审核记录不存在'}
            
            # 更新审核记录
            audit.status = 'rejected'
            audit.admin_id = admin_id
            audit.admin_notes = admin_notes
            audit.rejection_reason = rejection_reason
            audit.reviewed_at = get_beijing_utc_now()
            
            db.session.commit()
            
            # 发送邮件通知
            item = Item.query.get(audit.item_id)
            if item:
                self._send_item_image_audit_notification(item, 'rejected', admin_notes, rejection_reason)
            
            return {'success': True, 'message': '商品图片修改审核拒绝'}
        except Exception as e:
            db.session.rollback()
            return {'success': False, 'message': f'审核失败: {str(e)}'}
    
    def _send_item_image_audit_notification(self, item, result, admin_notes=None, rejection_reason=None):
        """发送商品图片审核结果邮件通知"""
        try:
            if result == 'approved':
                subject = '校园跳蚤市场 - 商品图片修改审核通过 ✓'
                body = f"""
                <html>
                <body>
                    <h2>✓ 恭喜！您的商品图片修改已审核通过</h2>
                    <p>亲爱的 {item.seller.username}，</p>
                    <p>您的商品《{item.title}》的图片修改申请已通过管理员审核，新图片现在可以在平台上正常显示了！</p>
                    <p>商品信息：</p>
                    <ul>
                        <li>✓ 商品名称：{item.title}</li>
                        <li>✓ 价格：¥{item.price}</li>
                        <li>✓ 分类：{item.category.name if item.category else '未分类'}</li>
                    </ul>
                    {f'<p><strong>管理员备注：</strong>{admin_notes}</p>' if admin_notes else ''}
                    <p>感谢您使用校园跳蚤市场！</p>
                    <hr>
                    <p style="color: #666; font-size: 12px;">此邮件由系统自动发送，请勿回复。</p>
                </body>
                </html>
                """
            else:
                subject = '校园跳蚤市场 - 商品图片修改审核未通过 ✗'
                body = f"""
                <html>
                <body>
                    <h2>✗ 很抱歉，您的商品图片修改申请未通过审核</h2>
                    <p>亲爱的 {item.seller.username}，</p>
                    <p>很抱歉，您的商品《{item.title}》的图片修改申请未通过管理员审核。</p>
                    {f'<p><strong>拒绝原因：</strong>{rejection_reason}</p>' if rejection_reason else ''}
                    {f'<p><strong>管理员备注：</strong>{admin_notes}</p>' if admin_notes else ''}
                    <p>您可以重新上传符合要求的图片后再次提交审核。</p>
                    <p>如有疑问，请联系平台管理员。</p>
                    <hr>
                    <p style="color: #666; font-size: 12px;">此邮件由系统自动发送，请勿回复。</p>
                </body>
                </html>
                """
            
            msg = self.email_service.Message(
                subject=subject,
                recipients=[item.seller.email],
                html=body,
                sender=current_app.config['MAIL_DEFAULT_SENDER']
            )
            
            self.email_service.mail.send(msg)
            
        except Exception as e:
            # 邮件发送失败不影响审核流程
            print(f"发送商品图片审核通知邮件失败: {e}")
    
    # ==================== 单项审核相关方法 ====================
    
    def audit_user_profile_item(self, audit_id, field_name, status, admin_id, admin_notes=None):
        """审核用户资料修改的单个字段"""
        try:
            audit = UserProfileAudit.query.get(audit_id)
            if not audit:
                return {'success': False, 'message': '审核记录不存在'}
            
            import json
            
            # 获取现有的单项审核状态和备注
            item_status = json.loads(audit.item_status) if audit.item_status else {}
            item_notes = json.loads(audit.item_notes) if audit.item_notes else {}
            
            # 更新指定字段的审核状态和备注
            item_status[field_name] = status
            if admin_notes:
                item_notes[field_name] = admin_notes
            
            # 保存更新后的状态
            audit.item_status = json.dumps(item_status, ensure_ascii=False)
            audit.item_notes = json.dumps(item_notes, ensure_ascii=False)
            audit.admin_id = admin_id
            
            # 检查是否所有字段都已审核
            new_data = json.loads(audit.new_data)
            all_fields_reviewed = all(field in item_status for field in new_data.keys())
            
            if all_fields_reviewed:
                # 所有字段都已审核，确定整体审核状态
                has_rejected = any(status == 'rejected' for status in item_status.values())
                audit.status = 'rejected' if has_rejected else 'approved'
                audit.reviewed_at = get_beijing_utc_now()
                
                # 如果整体通过，应用所有通过的修改
                if audit.status == 'approved':
                    user = User.query.get(audit.user_id)
                    if user:
                        for field, value in new_data.items():
                            if item_status.get(field) == 'approved':
                                if field == 'interests':
                                    user.set_interests_list(value)
                                elif hasattr(user, field):
                                    setattr(user, field, value)
                
                # 发送邮件通知
                user = User.query.get(audit.user_id)
                if user:
                    if audit.status == 'approved':
                        self._send_user_profile_audit_notification(user, 'approved', audit.admin_notes)
                    else:
                        # 生成拒绝原因
                        rejected_fields = [field for field, status in item_status.items() if status == 'rejected']
                        rejection_reason = f"以下字段未通过审核: {', '.join(rejected_fields)}"
                        self._send_user_profile_audit_notification(user, 'rejected', audit.admin_notes, rejection_reason)
            
            db.session.commit()
            
            return {'success': True, 'message': f'字段 {field_name} 审核完成'}
        except Exception as e:
            db.session.rollback()
            return {'success': False, 'message': f'审核失败: {str(e)}'}
    
    def complete_user_profile_audit(self, audit_id, audit_results, admin_id):
        """完成用户资料修改的单项审核"""
        try:
            audit = UserProfileAudit.query.get(audit_id)
            if not audit:
                return {'success': False, 'message': '审核记录不存在'}
            
            import json
            
            # 更新所有字段的审核状态和备注
            item_status = {}
            item_notes = {}
            
            for field_name, result in audit_results.items():
                item_status[field_name] = result['status']
                if result.get('notes'):
                    item_notes[field_name] = result['notes']
            
            # 保存审核状态
            audit.item_status = json.dumps(item_status, ensure_ascii=False)
            audit.item_notes = json.dumps(item_notes, ensure_ascii=False)
            audit.admin_id = admin_id
            audit.reviewed_at = get_beijing_utc_now()
            
            # 检查是否有任何字段被拒绝
            has_rejected = any(status == 'rejected' for status in item_status.values())
            
            if has_rejected:
                # 有字段被拒绝，整个审核不通过
                audit.status = 'rejected'
                # 生成拒绝原因
                rejected_fields = [field for field, status in item_status.items() if status == 'rejected']
                rejection_reason = f"以下字段未通过审核: {', '.join(rejected_fields)}"
            else:
                # 所有字段都通过，应用修改
                audit.status = 'approved'
                user = User.query.get(audit.user_id)
                if user:
                    new_data = json.loads(audit.new_data)
                    for field, value in new_data.items():
                        if item_status.get(field) == 'approved':
                            if field == 'interests':
                                user.set_interests_list(value)
                            elif hasattr(user, field):
                                setattr(user, field, value)
            
            # 发送邮件通知
            user = User.query.get(audit.user_id)
            if user:
                if audit.status == 'approved':
                    self._send_user_profile_audit_notification(user, 'approved', audit.admin_notes)
                else:
                    self._send_user_profile_audit_notification(user, 'rejected', audit.admin_notes, rejection_reason)
            
            db.session.commit()
            
            status_text = "通过" if audit.status == 'approved' else "拒绝"
            return {'success': True, 'message': f'用户资料修改审核{status_text}完成'}
        except Exception as e:
            db.session.rollback()
            return {'success': False, 'message': f'审核失败: {str(e)}'}
    
    def audit_item_profile_item(self, audit_id, field_name, status, admin_id, admin_notes=None):
        """审核商品资料修改的单个字段"""
        try:
            audit = ItemProfileAudit.query.get(audit_id)
            if not audit:
                return {'success': False, 'message': '审核记录不存在'}
            
            import json
            
            # 获取现有的单项审核状态和备注
            item_status = json.loads(audit.item_status) if audit.item_status else {}
            item_notes = json.loads(audit.item_notes) if audit.item_notes else {}
            
            # 更新指定字段的审核状态和备注
            item_status[field_name] = status
            if admin_notes:
                item_notes[field_name] = admin_notes
            
            # 保存更新后的状态
            audit.item_status = json.dumps(item_status, ensure_ascii=False)
            audit.item_notes = json.dumps(item_notes, ensure_ascii=False)
            audit.admin_id = admin_id
            
            # 检查是否所有字段都已审核
            new_data = json.loads(audit.new_data)
            all_fields_reviewed = all(field in item_status for field in new_data.keys())
            
            if all_fields_reviewed:
                # 所有字段都已审核，确定整体审核状态
                has_rejected = any(status == 'rejected' for status in item_status.values())
                audit.status = 'rejected' if has_rejected else 'approved'
                audit.reviewed_at = get_beijing_utc_now()
                
                # 如果整体通过，应用所有通过的修改
                if audit.status == 'approved':
                    item = Item.query.get(audit.item_id)
                    if item:
                        for field, value in new_data.items():
                            if item_status.get(field) == 'approved':
                                if field == 'images':
                                    item.images = json.dumps(value, ensure_ascii=False)
                                elif hasattr(item, field):
                                    setattr(item, field, value)
                
                # 发送邮件通知
                item = Item.query.get(audit.item_id)
                if item:
                    if audit.status == 'approved':
                        self._send_item_profile_audit_notification(item, 'approved', audit.admin_notes)
                    else:
                        # 生成拒绝原因
                        rejected_fields = [field for field, status in item_status.items() if status == 'rejected']
                        rejection_reason = f"以下字段未通过审核: {', '.join(rejected_fields)}"
                        self._send_item_profile_audit_notification(item, 'rejected', audit.admin_notes, rejection_reason)
            
            db.session.commit()
            
            return {'success': True, 'message': f'字段 {field_name} 审核完成'}
        except Exception as e:
            db.session.rollback()
            return {'success': False, 'message': f'审核失败: {str(e)}'}
    
    def complete_item_profile_audit(self, audit_id, audit_results, admin_id):
        """完成商品资料修改的单项审核"""
        try:
            audit = ItemProfileAudit.query.get(audit_id)
            if not audit:
                return {'success': False, 'message': '审核记录不存在'}
            
            import json
            
            # 更新所有字段的审核状态和备注
            item_status = {}
            item_notes = {}
            
            for field_name, result in audit_results.items():
                item_status[field_name] = result['status']
                if result.get('notes'):
                    item_notes[field_name] = result['notes']
            
            # 保存审核状态
            audit.item_status = json.dumps(item_status, ensure_ascii=False)
            audit.item_notes = json.dumps(item_notes, ensure_ascii=False)
            audit.admin_id = admin_id
            audit.reviewed_at = get_beijing_utc_now()
            
            # 检查是否有任何字段被拒绝
            has_rejected = any(status == 'rejected' for status in item_status.values())
            
            if has_rejected:
                # 有字段被拒绝，整个审核不通过
                audit.status = 'rejected'
                # 生成拒绝原因
                rejected_fields = [field for field, status in item_status.items() if status == 'rejected']
                rejection_reason = f"以下字段未通过审核: {', '.join(rejected_fields)}"
            else:
                # 所有字段都通过，应用修改
                audit.status = 'approved'
                item = Item.query.get(audit.item_id)
                if item:
                    new_data = json.loads(audit.new_data)
                    for field, value in new_data.items():
                        if item_status.get(field) == 'approved':
                            if field == 'images':
                                item.images = json.dumps(value, ensure_ascii=False)
                            elif hasattr(item, field):
                                setattr(item, field, value)
            
            # 发送邮件通知
            item = Item.query.get(audit.item_id)
            if item:
                if audit.status == 'approved':
                    self._send_item_profile_audit_notification(item, 'approved', audit.admin_notes)
                else:
                    self._send_item_profile_audit_notification(item, 'rejected', audit.admin_notes, rejection_reason)
            
            db.session.commit()
            
            status_text = "通过" if audit.status == 'approved' else "拒绝"
            return {'success': True, 'message': f'商品资料修改审核{status_text}完成'}
        except Exception as e:
            db.session.rollback()
            return {'success': False, 'message': f'审核失败: {str(e)}'}

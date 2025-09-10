from app import db
from app.models import User, UserBehavior, Item
from datetime import datetime, timedelta
from app.utils import get_beijing_utc_now
import json

class UserService:
    """用户服务类"""
    
    @staticmethod
    def create_user(username, email, password, **kwargs):
        """创建用户"""
        # 使用最小可用ID创建用户
        user = User.create_with_min_id(
            username=username,
            email=email,
            real_name=kwargs.get('real_name'),
            phone=kwargs.get('phone'),
            student_id=kwargs.get('student_id'),
            bio=kwargs.get('bio')
        )
        user.set_password(password)
        
        if kwargs.get('interests'):
            user.set_interests_list(kwargs['interests'])
        
        db.session.add(user)
        db.session.commit()
        
        return user
    
    @staticmethod
    def update_user_profile(user_id, **kwargs):
        """更新用户资料（需要审核）"""
        user = User.query.get(user_id)
        if not user:
            return None
        
        # 保存修改前的数据
        old_data = {
            'real_name': user.real_name,
            'phone': user.phone,
            'student_id': user.student_id,
            'bio': user.bio,
            'interests': user.get_interests_list()
        }
        
        # 准备修改后的数据
        new_data = old_data.copy()
        for field in ['real_name', 'phone', 'student_id', 'bio']:
            if field in kwargs:
                new_data[field] = kwargs[field]
        
        if 'interests' in kwargs:
            new_data['interests'] = kwargs['interests']
        
        # 检查是否有实际修改
        has_changes = False
        for key, value in new_data.items():
            if old_data.get(key) != value:
                has_changes = True
                break
        
        if not has_changes:
            return user
        
        # 如果是管理员，直接更新资料，不需要审核
        if user.is_admin:
            # 直接应用修改
            for field, value in new_data.items():
                if field == 'interests':
                    user.set_interests_list(value)
                elif hasattr(user, field):
                    setattr(user, field, value)
            
            db.session.commit()
            return user
        
        # 普通用户需要创建审核记录
        from app.services.audit_service import AuditService
        audit_service = AuditService()
        audit = audit_service.create_user_profile_audit(user_id, old_data, new_data)
        
        return user
    
    @staticmethod
    def get_user_stats(user_id):
        """获取用户统计信息"""
        user = User.query.get(user_id)
        if not user:
            return {}
        
        # 发布商品数
        items_count = Item.query.filter_by(seller_id=user_id).count()
        
        # 活跃商品数
        active_items_count = Item.query.filter_by(seller_id=user_id, status='active').count()
        
        # 已售商品数
        sold_items_count = Item.query.filter_by(seller_id=user_id, status='sold').count()
        
        # 总浏览量
        total_views = db.session.query(db.func.sum(Item.view_count)).filter_by(seller_id=user_id).scalar() or 0
        
        # 最近30天行为统计
        thirty_days_ago = get_beijing_utc_now() - timedelta(days=30)
        
        view_count = UserBehavior.query.filter(
            UserBehavior.user_id == user_id,
            UserBehavior.behavior_type == 'view',
            UserBehavior.created_at >= thirty_days_ago
        ).count()
        
        like_count = UserBehavior.query.filter(
            UserBehavior.user_id == user_id,
            UserBehavior.behavior_type == 'like',
            UserBehavior.created_at >= thirty_days_ago
        ).count()
        
        contact_count = UserBehavior.query.filter(
            UserBehavior.user_id == user_id,
            UserBehavior.behavior_type == 'contact',
            UserBehavior.created_at >= thirty_days_ago
        ).count()
        
        return {
            'items_count': items_count,
            'active_items_count': active_items_count,
            'sold_items_count': sold_items_count,
            'total_views': total_views,
            'recent_view_count': view_count,
            'recent_like_count': like_count,
            'recent_contact_count': contact_count
        }
    
    @staticmethod
    def get_user_behavior_history(user_id, limit=50):
        """获取用户行为历史"""
        behaviors = UserBehavior.query.filter_by(user_id=user_id).order_by(
            UserBehavior.created_at.desc()
        ).limit(limit).all()
        
        return behaviors
    
    @staticmethod
    def get_user_interests(user_id):
        """获取用户兴趣分析"""
        user = User.query.get(user_id)
        if not user:
            return {}
        
        # 从用户行为中分析兴趣
        behaviors = UserBehavior.query.filter_by(
            user_id=user_id,
            behavior_type='view'
        ).order_by(UserBehavior.created_at.desc()).limit(100).all()
        
        category_interests = {}
        tag_interests = {}
        price_interests = {}
        
        for behavior in behaviors:
            if not behavior.item:
                continue
            
            item = behavior.item
            
            # 分类兴趣
            category_name = item.category.name if item.category else '其他'
            category_interests[category_name] = category_interests.get(category_name, 0) + 1
            
            # 标签兴趣
            tags = item.get_tags_list()
            for tag in tags:
                tag_interests[tag] = tag_interests.get(tag, 0) + 1
            
            # 价格兴趣
            price_range = UserService._get_price_range(item.price)
            price_interests[price_range] = price_interests.get(price_range, 0) + 1
        
        return {
            'category_interests': category_interests,
            'tag_interests': tag_interests,
            'price_interests': price_interests,
            'explicit_interests': user.get_interests_list()
        }
    
    @staticmethod
    def _get_price_range(price):
        """获取价格区间"""
        if price <= 50:
            return "50元以下"
        elif price <= 100:
            return "50-100元"
        elif price <= 200:
            return "100-200元"
        elif price <= 500:
            return "200-500元"
        else:
            return "500元以上"
    
    @staticmethod
    def search_users(query, limit=20):
        """搜索用户"""
        users = User.query.filter(
            User.username.contains(query) |
            User.real_name.contains(query) |
            User.email.contains(query)
        ).filter_by(is_active=True).limit(limit).all()
        
        return users
    
    @staticmethod
    def get_active_users(limit=20):
        """获取活跃用户"""
        # 最近30天有行为的用户
        thirty_days_ago = get_beijing_utc_now() - timedelta(days=30)
        
        active_user_ids = db.session.query(UserBehavior.user_id).filter(
            UserBehavior.created_at >= thirty_days_ago
        ).distinct().limit(limit).all()
        
        user_ids = [user_id[0] for user_id in active_user_ids]
        users = User.query.filter(User.id.in_(user_ids)).all()
        
        return users

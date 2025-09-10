from app import db
from app.models import Item, Category, UserBehavior
from datetime import datetime, timedelta
import json

class ItemService:
    """商品服务类"""
    
    @staticmethod
    def create_item(seller_id, title, description, price, category_id, **kwargs):
        """创建商品"""
        # 检查用户是否为管理员
        from app.models import User
        seller = User.query.get(seller_id)
        is_admin = seller and seller.role == 'admin'
        
        item = Item(
            title=title,
            description=description,
            price=price,
            category_id=category_id,
            seller_id=seller_id,
            condition=kwargs.get('condition', 'good'),
            location=kwargs.get('location'),
            contact_method=kwargs.get('contact_method', 'message'),
            contact_info=kwargs.get('contact_info'),
            audit_status='approved' if is_admin else 'pending',
            status='active' if is_admin else 'inactive'
        )
        
        if kwargs.get('tags'):
            item.set_tags_list(kwargs['tags'])
        
        if kwargs.get('images'):
            item.set_images_list(kwargs['images'])
        
        db.session.add(item)
        db.session.commit()
        
        # 只有非管理员才创建审核记录
        if not is_admin:
            from app.services.audit_service import AuditService
            audit_service = AuditService()
            audit_service.create_item_audit(item.id)
        
        return item
    
    @staticmethod
    def update_item(item_id, **kwargs):
        """更新商品（需要审核）"""
        item = Item.query.get(item_id)
        if not item:
            return None
        
        # 保存修改前的数据
        old_data = {
            'title': item.title,
            'description': item.description,
            'price': float(item.price) if item.price else None,
            'original_price': float(item.original_price) if item.original_price else None,
            'category_id': item.category_id,
            'condition': item.condition,
            'location': item.location,
            'contact_method': item.contact_method,
            'contact_info': item.contact_info,
            'tags': item.get_tags_list(),
            'images': item.get_images_list()
        }
        
        # 准备修改后的数据
        new_data = old_data.copy()
        for field in ['title', 'description', 'price', 'original_price', 'category_id', 
                     'condition', 'location', 'contact_method', 'contact_info']:
            if field in kwargs:
                new_data[field] = kwargs[field]
        
        if 'tags' in kwargs:
            new_data['tags'] = kwargs['tags']
        
        if 'images' in kwargs:
            new_data['images'] = kwargs['images']
        
        # 检查是否有实际修改
        has_changes = False
        for key, value in new_data.items():
            if old_data.get(key) != value:
                has_changes = True
                break
        
        if not has_changes:
            return item
        
        # 如果是管理员，直接更新商品，不需要审核
        if item.seller.is_admin:
            # 直接应用修改
            for field, value in new_data.items():
                if field == 'tags':
                    item.set_tags_list(value)
                elif field == 'images':
                    item.set_images_list(value)
                elif hasattr(item, field):
                    setattr(item, field, value)
            
            db.session.commit()
            return item
        
        # 普通用户需要创建审核记录
        from app.services.audit_service import AuditService
        audit_service = AuditService()
        audit = audit_service.create_item_profile_audit(item_id, old_data, new_data)
        
        return item
    
    @staticmethod
    def get_item_stats(item_id):
        """获取商品统计信息"""
        item = Item.query.get(item_id)
        if not item:
            return {}
        
        # 行为统计
        view_count = UserBehavior.query.filter_by(
            item_id=item_id,
            behavior_type='view'
        ).count()
        
        like_count = UserBehavior.query.filter_by(
            item_id=item_id,
            behavior_type='like'
        ).count()
        
        contact_count = UserBehavior.query.filter_by(
            item_id=item_id,
            behavior_type='contact'
        ).count()
        
        # 最近7天统计
        seven_days_ago = datetime.utcnow() - timedelta(days=7)
        
        recent_views = UserBehavior.query.filter(
            UserBehavior.item_id == item_id,
            UserBehavior.behavior_type == 'view',
            UserBehavior.created_at >= seven_days_ago
        ).count()
        
        recent_likes = UserBehavior.query.filter(
            UserBehavior.item_id == item_id,
            UserBehavior.behavior_type == 'like',
            UserBehavior.created_at >= seven_days_ago
        ).count()
        
        recent_contacts = UserBehavior.query.filter(
            UserBehavior.item_id == item_id,
            UserBehavior.behavior_type == 'contact',
            UserBehavior.created_at >= seven_days_ago
        ).count()
        
        return {
            'total_views': view_count,
            'total_likes': like_count,
            'total_contacts': contact_count,
            'recent_views': recent_views,
            'recent_likes': recent_likes,
            'recent_contacts': recent_contacts,
            'view_count': item.view_count,
            'like_count': item.like_count
        }
    
    @staticmethod
    def get_popular_items(limit=20, days=30):
        """获取热门商品"""
        days_ago = datetime.utcnow() - timedelta(days=days)
        
        popular_items = db.session.query(Item).join(UserBehavior).filter(
            Item.status == 'active',
            UserBehavior.created_at >= days_ago,
            UserBehavior.behavior_type == 'view'
        ).group_by(Item.id).order_by(
            db.func.count(UserBehavior.id).desc(),
            Item.view_count.desc()
        ).limit(limit).all()
        
        return popular_items
    
    @staticmethod
    def get_latest_items(limit=20):
        """获取最新商品"""
        latest_items = Item.query.filter_by(status='active').order_by(
            Item.created_at.desc()
        ).limit(limit).all()
        
        return latest_items
    
    @staticmethod
    def get_items_by_category(category_id, limit=20):
        """获取分类商品"""
        items = Item.query.filter_by(
            category_id=category_id,
            status='active'
        ).order_by(Item.created_at.desc()).limit(limit).all()
        
        return items
    
    @staticmethod
    def search_items(query, category_id=None, min_price=None, max_price=None, 
                    condition=None, limit=20, offset=0):
        """搜索商品"""
        query_obj = Item.query.filter_by(status='active')
        
        # 文本搜索
        if query:
            query_obj = query_obj.filter(
                Item.title.contains(query) |
                Item.description.contains(query)
            )
        
        # 分类筛选
        if category_id:
            query_obj = query_obj.filter_by(category_id=category_id)
        
        # 价格筛选
        if min_price is not None:
            query_obj = query_obj.filter(Item.price >= min_price)
        
        if max_price is not None:
            query_obj = query_obj.filter(Item.price <= max_price)
        
        # 成色筛选
        if condition:
            query_obj = query_obj.filter_by(condition=condition)
        
        items = query_obj.order_by(Item.created_at.desc()).offset(offset).limit(limit).all()
        total_count = query_obj.count()
        
        return items, total_count
    
    @staticmethod
    def get_related_items(item_id, limit=5):
        """获取相关商品"""
        item = Item.query.get(item_id)
        if not item:
            return []
        
        # 同分类商品
        related_items = Item.query.filter(
            Item.category_id == item.category_id,
            Item.id != item_id,
            Item.status == 'active'
        ).order_by(Item.created_at.desc()).limit(limit).all()
        
        return related_items
    
    @staticmethod
    def get_user_items(user_id, status=None, limit=20):
        """获取用户商品"""
        query = Item.query.filter_by(seller_id=user_id)
        
        if status:
            query = query.filter_by(status=status)
        
        items = query.order_by(Item.created_at.desc()).limit(limit).all()
        
        return items
    
    @staticmethod
    def mark_item_sold(item_id):
        """标记商品已售"""
        item = Item.query.get(item_id)
        if not item:
            return None
        
        item.status = 'sold'
        item.sold_at = datetime.utcnow()
        db.session.commit()
        
        return item
    
    @staticmethod
    def get_category_stats():
        """获取分类统计"""
        stats = db.session.query(
            Category.name,
            db.func.count(Item.id)
        ).join(Item).filter(
            Item.status == 'active'
        ).group_by(Category.id, Category.name).all()
        
        return dict(stats)
    
    @staticmethod
    def get_price_distribution():
        """获取价格分布"""
        price_ranges = [
            (0, 50, "50元以下"),
            (50, 100, "50-100元"),
            (100, 200, "100-200元"),
            (200, 500, "200-500元"),
            (500, 1000, "500-1000元"),
            (1000, float('inf'), "1000元以上")
        ]
        
        distribution = {}
        for min_price, max_price, label in price_ranges:
            if max_price == float('inf'):
                count = Item.query.filter(
                    Item.price >= min_price,
                    Item.status == 'active'
                ).count()
            else:
                count = Item.query.filter(
                    Item.price >= min_price,
                    Item.price < max_price,
                    Item.status == 'active'
                ).count()
            
            distribution[label] = count
        
        return distribution

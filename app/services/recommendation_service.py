from typing import List, Dict, Any, Tuple
from flask import current_app
from app.models import Item, Category, User, Recommendation
import json
from datetime import datetime

class RecommendationService:
    def __init__(self):
        pass
    
    def get_db(self):
        """获取数据库实例"""
        from app import db
        return db
    
    def get_personalized_recommendations(self, user_id: int, limit: int = 5) -> List[Dict]:
        """获取个性化推荐"""
        try:
            # 构建查询
            query = self.get_db().session.query(Item).filter(
                Item.status == 'active',
                Item.audit_status == 'approved'
            )
            
            # 获取推荐商品
            items = query.order_by(Item.created_at.desc()).limit(limit * 2).all()
            
            # 返回Item对象而不是字典，以便模板可以调用方法
            return items[:limit]
            
        except Exception as e:
            print(f"获取个性化推荐失败: {e}")
            return []
    
    def get_recommendation_stats(self):
        """获取推荐统计信息"""
        try:
            from datetime import datetime, timedelta
            
            # 获取基础统计
            total_recommendations = Recommendation.query.count()
            
            # 最近7天统计
            seven_days_ago = datetime.utcnow() - timedelta(days=7)
            recent_recommendations = Recommendation.query.filter(
                Recommendation.created_at >= seven_days_ago
            ).count()
            
            # 点击率统计
            clicked_recommendations = Recommendation.query.filter_by(is_clicked=True).count()
            click_rate = (clicked_recommendations / total_recommendations * 100) if total_recommendations > 0 else 0
            
            # 购买率统计
            purchased_recommendations = Recommendation.query.filter_by(is_purchased=True).count()
            purchase_rate = (purchased_recommendations / total_recommendations * 100) if total_recommendations > 0 else 0
            
            # 算法类型统计
            algorithm_stats = self.get_db().session.query(
                Recommendation.algorithm_type,
                self.get_db().func.count(Recommendation.id)
            ).group_by(Recommendation.algorithm_type).all()
            
            return {
                'total_recommendations': total_recommendations,
                'recent_recommendations': recent_recommendations,
                'click_rate': round(click_rate, 2),
                'purchase_rate': round(purchase_rate, 2),
                'algorithm_stats': dict(algorithm_stats)
            }
            
        except Exception as e:
            print(f"获取推荐统计失败: {e}")
            return {
                'total_recommendations': 0,
                'recent_recommendations': 0,
                'click_rate': 0,
                'purchase_rate': 0,
                'algorithm_stats': {}
            }
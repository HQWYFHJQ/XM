from typing import List, Dict, Any, Tuple, Optional
from flask import current_app
from app.models import Item, Category, User, Recommendation, UserBehavior
from app import db
from app.services.cache_service import cache_service
import json
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.decomposition import TruncatedSVD
from surprise import Dataset, Reader, SVD, KNNBasic
from surprise.model_selection import train_test_split
import logging

logger = logging.getLogger(__name__)

class RecommendationService:
    def __init__(self):
        self.cache_timeout = 3600  # 缓存1小时
        self.min_interactions = 5  # 最小交互次数
        self.similarity_threshold = 0.1  # 相似度阈值
    
    def get_db(self):
        """获取数据库实例"""
        return db
    
    def get_personalized_recommendations(self, user_id: int, algorithm: str = 'hybrid', limit: int = 10) -> List[Dict]:
        """获取个性化推荐"""
        try:
            # 生成缓存键
            cache_key = f"recommendations:{user_id}:{algorithm}:{limit}"
            
            # 尝试从缓存获取
            cached_recommendations = cache_service.get(cache_key)
            if cached_recommendations:
                logger.info(f"从缓存获取推荐结果: 用户{user_id}, 算法{algorithm}")
                return cached_recommendations
            
            # 缓存未命中，生成推荐
            if algorithm == 'collaborative_filtering':
                recommendations = self._get_collaborative_filtering_recommendations(user_id, limit)
            elif algorithm == 'content_based':
                recommendations = self._get_content_based_recommendations(user_id, limit)
            elif algorithm == 'popularity':
                recommendations = self._get_popularity_recommendations(user_id, limit)
            elif algorithm == 'hybrid':
                recommendations = self._get_hybrid_recommendations(user_id, limit)
            else:
                # 默认返回热门推荐
                recommendations = self._get_popularity_recommendations(user_id, limit)
            
            # 缓存推荐结果（缓存30分钟）
            cache_service.set(cache_key, recommendations, timeout=1800)
            
            return recommendations
        except Exception as e:
            logger.error(f"获取个性化推荐失败: {e}")
            # 降级到热门推荐
            return self._get_popularity_recommendations(user_id, limit)
    
    def _get_collaborative_filtering_recommendations(self, user_id: int, limit: int) -> List[Dict]:
        """协同过滤推荐算法"""
        try:
            # 获取用户行为数据
            user_behaviors = self._get_user_behavior_data()
            if len(user_behaviors) < self.min_interactions:
                logger.info(f"用户{user_id}行为数据不足，降级到热门推荐")
                return self._get_popularity_recommendations(user_id, limit)
            
            # 构建用户-物品评分矩阵
            rating_matrix = self._build_rating_matrix(user_behaviors)
            
            # 使用SVD进行协同过滤
            recommendations = self._svd_collaborative_filtering(user_id, rating_matrix, limit)
            
            # 记录推荐结果
            self._record_recommendations(user_id, recommendations, 'collaborative_filtering')
            
            return recommendations
            
        except Exception as e:
            logger.error(f"协同过滤推荐失败: {e}")
            return self._get_popularity_recommendations(user_id, limit)
    
    def _get_content_based_recommendations(self, user_id: int, limit: int) -> List[Dict]:
        """基于内容的推荐算法"""
        try:
            # 获取用户历史行为
            user_items = self._get_user_interacted_items(user_id)
            if not user_items:
                logger.info(f"用户{user_id}无历史行为，降级到热门推荐")
                return self._get_popularity_recommendations(user_id, limit)
            
            # 构建商品特征矩阵
            item_features = self._build_item_feature_matrix()
            
            # 计算用户偏好向量
            user_profile = self._build_user_profile(user_id, user_items, item_features)
            
            # 计算相似度并推荐
            recommendations = self._content_based_recommend(user_profile, item_features, user_items, limit)
            
            # 记录推荐结果
            self._record_recommendations(user_id, recommendations, 'content_based')
            
            return recommendations
            
        except Exception as e:
            logger.error(f"内容推荐失败: {e}")
            return self._get_popularity_recommendations(user_id, limit)
    
    def _get_popularity_recommendations(self, user_id: int, limit: int) -> List[Dict]:
        """热门推荐算法"""
        try:
            # 使用缓存获取热门商品分数
            cache_key = "popularity_scores"
            popularity_scores = cache_service.get_or_set(
                cache_key, 
                self._calculate_popularity_scores, 
                timeout=3600  # 缓存1小时
            )
            
            # 获取用户已交互的商品
            user_interacted_items = self._get_user_interacted_items(user_id)
            user_interacted_ids = {item['id'] for item in user_interacted_items}
            
            # 过滤已交互的商品并排序
            filtered_items = [
                item for item in popularity_scores 
                if item['id'] not in user_interacted_ids
            ]
            
            recommendations = filtered_items[:limit]
            
            # 记录推荐结果
            self._record_recommendations(user_id, recommendations, 'popularity')
            
            return recommendations
            
        except Exception as e:
            logger.error(f"热门推荐失败: {e}")
            return []
    
    def _get_hybrid_recommendations(self, user_id: int, limit: int) -> List[Dict]:
        """混合推荐算法"""
        try:
            # 获取各种算法的推荐结果
            cf_recommendations = self._get_collaborative_filtering_recommendations(user_id, limit * 2)
            cb_recommendations = self._get_content_based_recommendations(user_id, limit * 2)
            pop_recommendations = self._get_popularity_recommendations(user_id, limit * 2)
            
            # 混合推荐权重
            weights = {
                'collaborative_filtering': 0.4,
                'content_based': 0.3,
                'popularity': 0.3
            }
            
            # 合并和重排序推荐结果
            hybrid_recommendations = self._merge_recommendations(
                cf_recommendations, cb_recommendations, pop_recommendations, weights, limit
            )
            
            # 记录推荐结果
            self._record_recommendations(user_id, hybrid_recommendations, 'hybrid')
            
            return hybrid_recommendations
            
        except Exception as e:
            logger.error(f"混合推荐失败: {e}")
            return self._get_popularity_recommendations(user_id, limit)
    
    def _get_user_behavior_data(self) -> List[Dict]:
        """获取用户行为数据"""
        behaviors = UserBehavior.query.filter(
            UserBehavior.behavior_type.in_(['view', 'like', 'favorite', 'contact'])
        ).all()
        
        return [
            {
                'user_id': b.user_id,
                'item_id': b.item_id,
                'behavior_type': b.behavior_type,
                'created_at': b.created_at
            }
            for b in behaviors
        ]
    
    def _build_rating_matrix(self, behaviors: List[Dict]) -> pd.DataFrame:
        """构建用户-物品评分矩阵"""
        # 行为权重
        behavior_weights = {
            'view': 1,
            'like': 3,
            'favorite': 5,
            'contact': 4
        }
        
        # 时间衰减因子
        now = datetime.utcnow()
        
        data = []
        for behavior in behaviors:
            # 计算时间衰减分数
            days_ago = (now - behavior['created_at']).days
            time_decay = max(0.1, 1.0 - days_ago * 0.01)  # 每天衰减1%
            
            # 计算最终分数
            score = behavior_weights.get(behavior['behavior_type'], 1) * time_decay
            
            data.append({
                'user_id': behavior['user_id'],
                'item_id': behavior['item_id'],
                'rating': score
            })
        
        return pd.DataFrame(data)
    
    def _svd_collaborative_filtering(self, user_id: int, rating_matrix: pd.DataFrame, limit: int) -> List[Dict]:
        """使用SVD进行协同过滤"""
        try:
            # 创建Surprise数据集
            reader = Reader(rating_scale=(0, 5))
            data = Dataset.load_from_df(rating_matrix, reader)
            
            # 训练SVD模型
            trainset = data.build_full_trainset()
            algo = SVD(n_factors=50, random_state=42)
            algo.fit(trainset)
            
            # 获取所有商品ID
            all_items = Item.query.filter(
                Item.status == 'active',
                Item.audit_status == 'approved'
            ).all()
            
            # 预测用户对所有商品的评分
            predictions = []
            for item in all_items:
                pred = algo.predict(user_id, item.id)
                predictions.append({
                    'id': item.id,
                    'title': item.title,
                    'price': float(item.price),
                    'description': item.description,
                    'category_name': item.category.name if item.category else '未分类',
                    'view_count': item.view_count,
                    'created_at': item.created_at,
                    'score': pred.est,
                    'reason': f'基于相似用户喜好推荐，预测评分: {pred.est:.2f}'
                })
            
            # 按评分排序
            predictions.sort(key=lambda x: x['score'], reverse=True)
            return predictions[:limit]
            
        except Exception as e:
            logger.error(f"SVD协同过滤失败: {e}")
            return []
    
    def _build_item_feature_matrix(self) -> pd.DataFrame:
        """构建商品特征矩阵"""
        items = Item.query.filter(
            Item.status == 'active',
            Item.audit_status == 'approved'
        ).all()
        
        features = []
        for item in items:
            # 组合商品特征文本
            feature_text = f"{item.title} {item.description} {item.category.name if item.category else ''}"
            if item.tags:
                feature_text += f" {item.tags}"
            
            features.append({
                'item_id': item.id,
                'feature_text': feature_text,
                'category_id': item.category_id,
                'price': float(item.price)
            })
        
        return pd.DataFrame(features)
    
    def _build_user_profile(self, user_id: int, user_items: List[Dict], item_features: pd.DataFrame) -> np.ndarray:
        """构建用户偏好向量"""
        # 获取用户交互过的商品特征
        user_item_ids = [item['id'] for item in user_items]
        user_features = item_features[item_features['item_id'].isin(user_item_ids)]
        
        if user_features.empty:
            return np.zeros(100)  # 返回零向量
        
        # 使用TF-IDF向量化
        vectorizer = TfidfVectorizer(max_features=100, stop_words=None)
        feature_matrix = vectorizer.fit_transform(user_features['feature_text'])
        
        # 计算用户偏好向量（平均）
        user_profile = np.mean(feature_matrix.toarray(), axis=0)
        
        return user_profile
    
    def _content_based_recommend(self, user_profile: np.ndarray, item_features: pd.DataFrame, 
                                user_items: List[Dict], limit: int) -> List[Dict]:
        """基于内容推荐"""
        # 获取用户未交互的商品
        user_item_ids = {item['id'] for item in user_items}
        candidate_items = item_features[~item_features['item_id'].isin(user_item_ids)]
        
        if candidate_items.empty:
            return []
        
        # 向量化候选商品
        vectorizer = TfidfVectorizer(max_features=100, stop_words=None)
        candidate_matrix = vectorizer.fit_transform(candidate_items['feature_text'])
        
        # 计算相似度
        similarities = cosine_similarity([user_profile], candidate_matrix)[0]
        
        # 获取商品详细信息
        recommendations = []
        for idx, similarity in enumerate(similarities):
            if similarity > self.similarity_threshold:
                item_id = candidate_items.iloc[idx]['item_id']
                item = Item.query.get(item_id)
                if item:
                    recommendations.append({
                        'id': item.id,
                        'title': item.title,
                        'price': float(item.price),
                        'description': item.description,
                        'category_name': item.category.name if item.category else '未分类',
                        'view_count': item.view_count,
                        'created_at': item.created_at,
                        'score': similarity,
                        'reason': f'基于商品特征相似度推荐，相似度: {similarity:.2f}'
                    })
        
        # 按相似度排序
        recommendations.sort(key=lambda x: x['score'], reverse=True)
        return recommendations[:limit]
    
    def _calculate_popularity_scores(self) -> List[Dict]:
        """计算商品热度分数"""
        items = Item.query.filter(
            Item.status == 'active',
            Item.audit_status == 'approved'
        ).all()
        
        popularity_scores = []
        for item in items:
            # 计算热度分数
            view_score = item.view_count * 0.1
            like_score = item.like_count * 0.5
            favorite_score = item.favorite_count * 1.0
            contact_score = item.contact_count * 0.8
            
            # 时间衰减
            days_ago = (datetime.utcnow() - item.created_at).days
            time_decay = max(0.1, 1.0 - days_ago * 0.005)  # 每天衰减0.5%
            
            total_score = (view_score + like_score + favorite_score + contact_score) * time_decay
            
            popularity_scores.append({
                'id': item.id,
                'title': item.title,
                'price': float(item.price),
                'description': item.description,
                'category_name': item.category.name if item.category else '未分类',
                'view_count': item.view_count,
                'created_at': item.created_at,
                'score': total_score,
                'reason': f'热门商品推荐，热度分数: {total_score:.2f}'
            })
        
        # 按热度分数排序
        popularity_scores.sort(key=lambda x: x['score'], reverse=True)
        return popularity_scores
    
    def _get_user_interacted_items(self, user_id: int) -> List[Dict]:
        """获取用户交互过的商品"""
        behaviors = UserBehavior.query.filter_by(user_id=user_id).all()
        
        interacted_items = {}
        for behavior in behaviors:
            item_id = behavior.item_id
            if item_id not in interacted_items:
                interacted_items[item_id] = {
                    'id': item_id,
                    'behaviors': []
                }
            interacted_items[item_id]['behaviors'].append(behavior.behavior_type)
        
        return list(interacted_items.values())
    
    def _merge_recommendations(self, cf_recs: List[Dict], cb_recs: List[Dict], 
                              pop_recs: List[Dict], weights: Dict[str, float], limit: int) -> List[Dict]:
        """合并推荐结果"""
        # 创建商品分数字典
        item_scores = {}
        
        # 添加协同过滤分数
        for i, rec in enumerate(cf_recs):
            item_id = rec['id']
            if item_id not in item_scores:
                item_scores[item_id] = {'scores': {}, 'item': rec}
            item_scores[item_id]['scores']['cf'] = rec['score'] * weights['collaborative_filtering']
        
        # 添加内容推荐分数
        for i, rec in enumerate(cb_recs):
            item_id = rec['id']
            if item_id not in item_scores:
                item_scores[item_id] = {'scores': {}, 'item': rec}
            item_scores[item_id]['scores']['cb'] = rec['score'] * weights['content_based']
        
        # 添加热门推荐分数
        for i, rec in enumerate(pop_recs):
            item_id = rec['id']
            if item_id not in item_scores:
                item_scores[item_id] = {'scores': {}, 'item': rec}
            item_scores[item_id]['scores']['pop'] = rec['score'] * weights['popularity']
        
        # 计算最终分数
        final_recommendations = []
        for item_id, data in item_scores.items():
            final_score = sum(data['scores'].values())
            item = data['item'].copy()
            item['score'] = final_score
            item['reason'] = f'混合推荐，综合分数: {final_score:.2f}'
            final_recommendations.append(item)
        
        # 按最终分数排序
        final_recommendations.sort(key=lambda x: x['score'], reverse=True)
        return final_recommendations[:limit]
    
    def _record_recommendations(self, user_id: int, recommendations: List[Dict], algorithm_type: str):
        """记录推荐结果"""
        try:
            for rec in recommendations:
                recommendation = Recommendation(
                    user_id=user_id,
                    item_id=rec['id'],
                    algorithm_type=algorithm_type,
                    score=rec['score'],
                    reason=rec.get('reason', '')
                )
                db.session.add(recommendation)
            
            db.session.commit()
        except Exception as e:
            logger.error(f"记录推荐结果失败: {e}")
            db.session.rollback()
    
    def record_recommendation_click(self, user_id: int, item_id: int, algorithm_type: str):
        """记录推荐点击"""
        try:
            # 查找最近的推荐记录
            recommendation = Recommendation.query.filter_by(
                user_id=user_id,
                item_id=item_id,
                algorithm_type=algorithm_type,
                is_clicked=False
            ).order_by(Recommendation.created_at.desc()).first()
            
            if recommendation:
                recommendation.is_clicked = True
                recommendation.clicked_at = datetime.utcnow()
                db.session.commit()
                
                # 清理用户相关的推荐缓存
                self._clear_user_recommendation_cache(user_id)
                
                logger.info(f"记录推荐点击: 用户{user_id}, 商品{item_id}, 算法{algorithm_type}")
        except Exception as e:
            logger.error(f"记录推荐点击失败: {e}")
            db.session.rollback()
    
    def _clear_user_recommendation_cache(self, user_id: int):
        """清理用户相关的推荐缓存"""
        try:
            # 清理用户的所有推荐缓存
            cache_service.clear_pattern(f"recommendations:{user_id}:*")
            logger.info(f"清理用户{user_id}的推荐缓存")
        except Exception as e:
            logger.error(f"清理用户推荐缓存失败: {e}")
    
    def clear_all_recommendation_cache(self):
        """清理所有推荐缓存"""
        try:
            cache_service.clear_pattern("recommendations:*")
            cache_service.clear_pattern("popularity_scores")
            logger.info("清理所有推荐缓存")
        except Exception as e:
            logger.error(f"清理推荐缓存失败: {e}")
    
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
            algorithm_stats = db.session.query(
                Recommendation.algorithm_type,
                db.func.count(Recommendation.id)
            ).group_by(Recommendation.algorithm_type).all()
            
            return {
                'total_recommendations': total_recommendations,
                'recent_recommendations': recent_recommendations,
                'click_rate': round(click_rate, 2),
                'purchase_rate': round(purchase_rate, 2),
                'algorithm_stats': dict(algorithm_stats)
            }
            
        except Exception as e:
            logger.error(f"获取推荐统计失败: {e}")
            return {
                'total_recommendations': 0,
                'recent_recommendations': 0,
                'click_rate': 0,
                'purchase_rate': 0,
                'algorithm_stats': {}
            }
    
    def evaluate_recommendation_performance(self, days: int = 30) -> Dict[str, Any]:
        """评估推荐算法性能"""
        try:
            from datetime import datetime, timedelta
            
            # 获取指定时间范围内的推荐数据
            start_date = datetime.utcnow() - timedelta(days=days)
            recommendations = Recommendation.query.filter(
                Recommendation.created_at >= start_date
            ).all()
            
            if not recommendations:
                return {
                    'error': '没有找到推荐数据',
                    'period_days': days
                }
            
            # 按算法类型分组统计
            algorithm_performance = {}
            algorithms = ['collaborative_filtering', 'content_based', 'popularity', 'hybrid']
            
            for algorithm in algorithms:
                algo_recs = [r for r in recommendations if r.algorithm_type == algorithm]
                if not algo_recs:
                    continue
                
                total_count = len(algo_recs)
                clicked_count = len([r for r in algo_recs if r.is_clicked])
                purchased_count = len([r for r in algo_recs if r.is_purchased])
                
                click_rate = (clicked_count / total_count * 100) if total_count > 0 else 0
                purchase_rate = (purchased_count / total_count * 100) if total_count > 0 else 0
                
                # 计算平均推荐分数
                avg_score = sum(r.score for r in algo_recs) / total_count if total_count > 0 else 0
                
                algorithm_performance[algorithm] = {
                    'total_recommendations': total_count,
                    'clicked_recommendations': clicked_count,
                    'purchased_recommendations': purchased_count,
                    'click_rate': round(click_rate, 2),
                    'purchase_rate': round(purchase_rate, 2),
                    'average_score': round(avg_score, 3),
                    'conversion_rate': round(purchase_rate / click_rate * 100, 2) if click_rate > 0 else 0
                }
            
            # 计算整体性能指标
            total_recommendations = len(recommendations)
            total_clicked = len([r for r in recommendations if r.is_clicked])
            total_purchased = len([r for r in recommendations if r.is_purchased])
            
            overall_click_rate = (total_clicked / total_recommendations * 100) if total_recommendations > 0 else 0
            overall_purchase_rate = (total_purchased / total_recommendations * 100) if total_recommendations > 0 else 0
            
            return {
                'period_days': days,
                'total_recommendations': total_recommendations,
                'overall_click_rate': round(overall_click_rate, 2),
                'overall_purchase_rate': round(overall_purchase_rate, 2),
                'algorithm_performance': algorithm_performance,
                'best_algorithm': self._get_best_algorithm(algorithm_performance),
                'evaluation_date': datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            logger.error(f"评估推荐性能失败: {e}")
            return {
                'error': f'评估失败: {str(e)}',
                'period_days': days
            }
    
    def _get_best_algorithm(self, algorithm_performance: Dict[str, Dict]) -> str:
        """获取最佳推荐算法"""
        if not algorithm_performance:
            return 'popularity'  # 默认算法
        
        # 基于综合指标选择最佳算法
        best_algorithm = None
        best_score = -1
        
        for algorithm, metrics in algorithm_performance.items():
            # 综合评分：点击率 * 0.4 + 购买率 * 0.6
            composite_score = metrics['click_rate'] * 0.4 + metrics['purchase_rate'] * 0.6
            
            if composite_score > best_score:
                best_score = composite_score
                best_algorithm = algorithm
        
        return best_algorithm or 'popularity'
    
    def get_user_recommendation_history(self, user_id: int, limit: int = 50) -> List[Dict]:
        """获取用户推荐历史"""
        try:
            recommendations = Recommendation.query.filter_by(
                user_id=user_id
            ).order_by(Recommendation.created_at.desc()).limit(limit).all()
            
            return [rec.to_dict() for rec in recommendations]
        except Exception as e:
            logger.error(f"获取用户推荐历史失败: {e}")
            return []
    
    def get_recommendation_insights(self) -> Dict[str, Any]:
        """获取推荐洞察分析"""
        try:
            # 获取最近30天的数据
            performance_data = self.evaluate_recommendation_performance(30)
            
            if 'error' in performance_data:
                return performance_data
            
            # 分析趋势
            trends = self._analyze_recommendation_trends()
            
            # 用户行为分析
            user_behavior_analysis = self._analyze_user_behavior_patterns()
            
            return {
                'performance_summary': performance_data,
                'trends': trends,
                'user_behavior_analysis': user_behavior_analysis,
                'recommendations': self._generate_insight_recommendations(performance_data)
            }
            
        except Exception as e:
            logger.error(f"获取推荐洞察失败: {e}")
            return {'error': f'分析失败: {str(e)}'}
    
    def _analyze_recommendation_trends(self) -> Dict[str, Any]:
        """分析推荐趋势"""
        try:
            from datetime import datetime, timedelta
            
            # 分析最近7天的趋势
            trends = {}
            for i in range(7):
                date = datetime.utcnow() - timedelta(days=i)
                start_of_day = date.replace(hour=0, minute=0, second=0, microsecond=0)
                end_of_day = start_of_day + timedelta(days=1)
                
                day_recommendations = Recommendation.query.filter(
                    Recommendation.created_at >= start_of_day,
                    Recommendation.created_at < end_of_day
                ).all()
                
                if day_recommendations:
                    clicked_count = len([r for r in day_recommendations if r.is_clicked])
                    click_rate = (clicked_count / len(day_recommendations) * 100) if day_recommendations else 0
                    
                    trends[date.strftime('%Y-%m-%d')] = {
                        'total_recommendations': len(day_recommendations),
                        'click_rate': round(click_rate, 2)
                    }
            
            return trends
        except Exception as e:
            logger.error(f"分析推荐趋势失败: {e}")
            return {}
    
    def _analyze_user_behavior_patterns(self) -> Dict[str, Any]:
        """分析用户行为模式"""
        try:
            # 分析用户活跃度
            active_users = db.session.query(
                db.func.count(db.func.distinct(Recommendation.user_id))
            ).filter(
                Recommendation.created_at >= datetime.utcnow() - timedelta(days=7)
            ).scalar()
            
            # 分析最活跃的用户
            top_users = db.session.query(
                Recommendation.user_id,
                db.func.count(Recommendation.id).label('rec_count')
            ).filter(
                Recommendation.created_at >= datetime.utcnow() - timedelta(days=30)
            ).group_by(Recommendation.user_id).order_by(
                db.desc('rec_count')
            ).limit(10).all()
            
            return {
                'active_users_7days': active_users or 0,
                'top_active_users': [
                    {'user_id': user_id, 'recommendation_count': count}
                    for user_id, count in top_users
                ]
            }
        except Exception as e:
            logger.error(f"分析用户行为模式失败: {e}")
            return {}
    
    def _generate_insight_recommendations(self, performance_data: Dict[str, Any]) -> List[str]:
        """生成洞察建议"""
        recommendations = []
        
        if 'algorithm_performance' in performance_data:
            algo_perf = performance_data['algorithm_performance']
            
            # 分析各算法表现
            for algorithm, metrics in algo_perf.items():
                if metrics['click_rate'] < 5:
                    recommendations.append(f"{algorithm}算法的点击率较低({metrics['click_rate']}%)，建议优化算法参数")
                
                if metrics['purchase_rate'] < 1:
                    recommendations.append(f"{algorithm}算法的转化率较低({metrics['purchase_rate']}%)，建议改进推荐质量")
            
            # 整体建议
            if performance_data['overall_click_rate'] < 10:
                recommendations.append("整体点击率偏低，建议增加推荐多样性")
            
            if performance_data['overall_purchase_rate'] < 2:
                recommendations.append("整体转化率偏低，建议优化推荐精准度")
        
        return recommendations
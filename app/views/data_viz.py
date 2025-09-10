from flask import Blueprint, render_template, jsonify, request
from flask_login import login_required, current_user
from app import db
from app.models import User, Item, Category, UserBehavior, Recommendation
from app.services.recommendation_service import RecommendationService
from app.services.user_service import UserService
from app.services.item_service import ItemService
from datetime import datetime, timedelta
import json

data_viz_bp = Blueprint('data_viz', __name__)

@data_viz_bp.route('/dashboard')
@login_required
def dashboard():
    """数据可视化仪表板"""
    if not current_user.is_admin:
        return render_template('errors/403.html'), 403
    
    return render_template('admin/data_dashboard.html')

@data_viz_bp.route('/api/user-growth')
@login_required
def user_growth_data():
    """用户增长数据API"""
    if not current_user.is_admin:
        return jsonify({'error': '无权限'}), 403
    
    days = request.args.get('days', 30, type=int)
    end_date = datetime.utcnow()
    start_date = end_date - timedelta(days=days)
    
    # 获取每日新增用户数
    daily_users = db.session.query(
        db.func.date(User.created_at).label('date'),
        db.func.count(User.id).label('count')
    ).filter(
        User.created_at >= start_date
    ).group_by(
        db.func.date(User.created_at)
    ).order_by('date').all()
    
    # 转换为图表数据格式
    data = []
    for record in daily_users:
        data.append({
            'date': record.date.strftime('%Y-%m-%d'),
            'count': record.count
        })
    
    return jsonify({
        'success': True,
        'data': data
    })

@data_viz_bp.route('/api/item-growth')
@login_required
def item_growth_data():
    """商品增长数据API"""
    if not current_user.is_admin:
        return jsonify({'error': '无权限'}), 403
    
    days = request.args.get('days', 30, type=int)
    end_date = datetime.utcnow()
    start_date = end_date - timedelta(days=days)
    
    # 获取每日新增商品数
    daily_items = db.session.query(
        db.func.date(Item.created_at).label('date'),
        db.func.count(Item.id).label('count')
    ).filter(
        Item.created_at >= start_date
    ).group_by(
        db.func.date(Item.created_at)
    ).order_by('date').all()
    
    # 转换为图表数据格式
    data = []
    for record in daily_items:
        data.append({
            'date': record.date.strftime('%Y-%m-%d'),
            'count': record.count
        })
    
    return jsonify({
        'success': True,
        'data': data
    })

@data_viz_bp.route('/api/category-distribution')
@login_required
def category_distribution_data():
    """分类分布数据API"""
    if not current_user.is_admin:
        return jsonify({'error': '无权限'}), 403
    
    # 获取各分类商品数量
    category_stats = db.session.query(
        Category.name,
        db.func.count(Item.id).label('count')
    ).join(Item).filter(
        Item.status == 'active'
    ).group_by(Category.id, Category.name).all()
    
    # 转换为图表数据格式
    data = []
    for record in category_stats:
        data.append({
            'name': record.name,
            'value': record.count
        })
    
    return jsonify({
        'success': True,
        'data': data
    })

@data_viz_bp.route('/api/price-distribution')
@login_required
def price_distribution_data():
    """价格分布数据API"""
    if not current_user.is_admin:
        return jsonify({'error': '无权限'}), 403
    
    # 获取价格分布
    price_ranges = [
        (0, 50, "50元以下"),
        (50, 100, "50-100元"),
        (100, 200, "100-200元"),
        (200, 500, "200-500元"),
        (500, 1000, "500-1000元"),
        (1000, float('inf'), "1000元以上")
    ]
    
    data = []
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
        
        data.append({
            'name': label,
            'value': count
        })
    
    return jsonify({
        'success': True,
        'data': data
    })

@data_viz_bp.route('/api/behavior-stats')
@login_required
def behavior_stats_data():
    """用户行为统计API"""
    if not current_user.is_admin:
        return jsonify({'error': '无权限'}), 403
    
    days = request.args.get('days', 7, type=int)
    end_date = datetime.utcnow()
    start_date = end_date - timedelta(days=days)
    
    # 获取行为统计
    behavior_stats = db.session.query(
        UserBehavior.behavior_type,
        db.func.count(UserBehavior.id).label('count')
    ).filter(
        UserBehavior.created_at >= start_date
    ).group_by(UserBehavior.behavior_type).all()
    
    # 转换为图表数据格式
    data = []
    for record in behavior_stats:
        data.append({
            'name': record.behavior_type,
            'value': record.count
        })
    
    return jsonify({
        'success': True,
        'data': data
    })

@data_viz_bp.route('/api/recommendation-stats')
@login_required
def recommendation_stats_data():
    """推荐统计API"""
    if not current_user.is_admin:
        return jsonify({'error': '无权限'}), 403
    
    # 获取推荐统计
    recommendation_service = RecommendationService()
    stats = recommendation_service.get_recommendation_stats()
    
    return jsonify({
        'success': True,
        'data': stats
    })

@data_viz_bp.route('/api/user-interests')
@login_required
def user_interests_data():
    """用户兴趣分析API"""
    if not current_user.is_admin:
        return jsonify({'error': '无权限'}), 403
    
    # 获取所有用户的兴趣标签
    users = User.query.filter(User.interests.isnot(None)).all()
    
    interest_count = {}
    for user in users:
        interests = user.get_interests_list()
        for interest in interests:
            interest_count[interest] = interest_count.get(interest, 0) + 1
    
    # 转换为图表数据格式
    data = []
    for interest, count in sorted(interest_count.items(), key=lambda x: x[1], reverse=True)[:10]:
        data.append({
            'name': interest,
            'value': count
        })
    
    return jsonify({
        'success': True,
        'data': data
    })

@data_viz_bp.route('/api/popular-items')
@login_required
def popular_items_data():
    """热门商品数据API"""
    if not current_user.is_admin:
        return jsonify({'error': '无权限'}), 403
    
    limit = request.args.get('limit', 10, type=int)
    
    # 获取热门商品
    popular_items = ItemService.get_popular_items(limit=limit)
    
    # 转换为图表数据格式
    data = []
    for item in popular_items:
        data.append({
            'name': item.title,
            'value': item.view_count
        })
    
    return jsonify({
        'success': True,
        'data': data
    })

@data_viz_bp.route('/api/active-users')
@login_required
def active_users_data():
    """活跃用户数据API"""
    if not current_user.is_admin:
        return jsonify({'error': '无权限'}), 403
    
    days = request.args.get('days', 7, type=int)
    end_date = datetime.utcnow()
    start_date = end_date - timedelta(days=days)
    
    # 获取活跃用户（有行为记录的用户）
    active_users = db.session.query(
        User.username,
        db.func.count(UserBehavior.id).label('activity_count')
    ).join(UserBehavior).filter(
        UserBehavior.created_at >= start_date
    ).group_by(User.id, User.username).order_by(
        db.func.count(UserBehavior.id).desc()
    ).limit(10).all()
    
    # 转换为图表数据格式
    data = []
    for record in active_users:
        data.append({
            'name': record.username,
            'value': record.activity_count
        })
    
    return jsonify({
        'success': True,
        'data': data
    })

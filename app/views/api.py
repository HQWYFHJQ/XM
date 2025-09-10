from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from app import db
from app.models import User, Item, Category, UserBehavior, Recommendation
from app.services.recommendation_service import RecommendationService
from app.services.user_service import UserService
from app.services.item_service import ItemService
from app.services.message_service import MessageService
from datetime import datetime
import json

api_bp = Blueprint('api', __name__)

@api_bp.route('/items', methods=['GET'])
def get_items():
    """获取商品列表API"""
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    category_id = request.args.get('category_id', type=int)
    search = request.args.get('search', '')
    min_price = request.args.get('min_price', type=float)
    max_price = request.args.get('max_price', type=float)
    sort_by = request.args.get('sort', 'latest')
    
    items, total_count = ItemService.search_items(
        query=search,
        category_id=category_id,
        min_price=min_price,
        max_price=max_price,
        limit=per_page,
        offset=(page - 1) * per_page
    )
    
    return jsonify({
        'success': True,
        'data': {
            'items': [item.to_dict() for item in items],
            'total_count': total_count,
            'page': page,
            'per_page': per_page,
            'total_pages': (total_count + per_page - 1) // per_page
        }
    })

@api_bp.route('/items/<int:item_id>', methods=['GET'])
def get_item(item_id):
    """获取商品详情API"""
    item = Item.query.get_or_404(item_id)
    
    # 记录浏览行为
    if current_user.is_authenticated:
        behavior = UserBehavior(
            user_id=current_user.id,
            item_id=item_id,
            behavior_type='view',
            ip_address=request.remote_addr,
            user_agent=request.headers.get('User-Agent')
        )
        db.session.add(behavior)
        db.session.commit()
    
    return jsonify({
        'success': True,
        'data': item.to_dict(include_seller=True)
    })

@api_bp.route('/items', methods=['POST'])
@login_required
def create_item():
    """创建商品API"""
    data = request.get_json()
    
    required_fields = ['title', 'description', 'price', 'category_id']
    for field in required_fields:
        if field not in data:
            return jsonify({'success': False, 'message': f'缺少必填字段: {field}'})
    
    try:
        item = ItemService.create_item(
            seller_id=current_user.id,
            title=data['title'],
            description=data['description'],
            price=float(data['price']),
            category_id=int(data['category_id']),
            condition=data.get('condition', 'good'),
            location=data.get('location'),
            contact_method=data.get('contact_method', 'message'),
            contact_info=data.get('contact_info'),
            tags=data.get('tags', []),
            images=data.get('images', [])
        )
        
        return jsonify({
            'success': True,
            'data': item.to_dict(),
            'message': '商品创建成功'
        })
        
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

@api_bp.route('/items/<int:item_id>', methods=['PUT'])
@login_required
def update_item(item_id):
    """更新商品API"""
    item = Item.query.get_or_404(item_id)
    
    # 检查权限
    if item.seller_id != current_user.id and not current_user.is_admin:
        return jsonify({'success': False, 'message': '无权限修改此商品'})
    
    data = request.get_json()
    
    try:
        updated_item = ItemService.update_item(item_id, **data)
        
        return jsonify({
            'success': True,
            'data': updated_item.to_dict(),
            'message': '商品更新成功'
        })
        
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

@api_bp.route('/items/<int:item_id>/like', methods=['POST'])
@login_required
def like_item(item_id):
    """点赞商品API"""
    item = Item.query.get_or_404(item_id)
    
    # 检查是否已经点赞
    existing_behavior = UserBehavior.query.filter_by(
        user_id=current_user.id,
        item_id=item_id,
        behavior_type='like'
    ).first()
    
    if existing_behavior:
        # 取消点赞
        db.session.delete(existing_behavior)
        item.like_count = max(0, item.like_count - 1)
        is_liked = False
    else:
        # 添加点赞
        behavior = UserBehavior(
            user_id=current_user.id,
            item_id=item_id,
            behavior_type='like',
            ip_address=request.remote_addr
        )
        db.session.add(behavior)
        item.like_count += 1
        is_liked = True
    
    db.session.commit()
    
    return jsonify({
        'success': True,
        'data': {
            'is_liked': is_liked,
            'like_count': item.like_count
        }
    })

@api_bp.route('/items/<int:item_id>/contact', methods=['POST'])
@login_required
def contact_seller(item_id):
    """联系卖家API"""
    item = Item.query.get_or_404(item_id)
    
    if item.seller_id == current_user.id:
        return jsonify({'success': False, 'message': '不能联系自己'})
    
    # 记录联系行为
    behavior = UserBehavior(
        user_id=current_user.id,
        item_id=item_id,
        behavior_type='contact',
        ip_address=request.remote_addr
    )
    db.session.add(behavior)
    db.session.commit()
    
    return jsonify({
        'success': True,
        'data': {
            'contact_info': item.contact_info,
            'contact_method': item.contact_method
        },
        'message': '联系记录已保存'
    })

@api_bp.route('/recommendations', methods=['GET'])
@login_required
def get_recommendations():
    """获取推荐商品API"""
    algorithm = request.args.get('algorithm', 'hybrid')
    limit = request.args.get('limit', 10, type=int)
    
    recommendation_service = RecommendationService()
    recommendations = recommendation_service.get_personalized_recommendations(
        current_user.id, limit=limit
    )
    
    return jsonify({
        'success': True,
        'data': [item.to_dict() for item in recommendations]
    })

@api_bp.route('/recommendations/<int:item_id>/click', methods=['POST'])
@login_required
def record_recommendation_click(item_id):
    """记录推荐点击API"""
    algorithm = request.json.get('algorithm', 'hybrid')
    
    recommendation_service = RecommendationService()
    recommendation_service.record_recommendation_click(
        current_user.id, item_id, algorithm
    )
    
    return jsonify({'success': True, 'message': '点击记录已保存'})

@api_bp.route('/categories', methods=['GET'])
def get_categories():
    """获取分类列表API"""
    categories = Category.query.filter_by(is_active=True).order_by(
        Category.sort_order, Category.name
    ).all()
    
    return jsonify({
        'success': True,
        'data': [category.to_dict() for category in categories]
    })

@api_bp.route('/users/profile', methods=['GET'])
@login_required
def get_profile():
    """获取用户资料API"""
    return jsonify({
        'success': True,
        'data': current_user.to_dict()
    })

@api_bp.route('/users/profile', methods=['PUT'])
@login_required
def update_profile():
    """更新用户资料API"""
    data = request.get_json()
    
    try:
        updated_user = UserService.update_user_profile(current_user.id, **data)
        
        return jsonify({
            'success': True,
            'data': updated_user.to_dict(),
            'message': '资料更新成功'
        })
        
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

@api_bp.route('/users/stats', methods=['GET'])
@login_required
def get_user_stats():
    """获取用户统计API"""
    stats = UserService.get_user_stats(current_user.id)
    
    return jsonify({
        'success': True,
        'data': stats
    })

@api_bp.route('/users/interests', methods=['GET'])
@login_required
def get_user_interests():
    """获取用户兴趣API"""
    interests = UserService.get_user_interests(current_user.id)
    
    return jsonify({
        'success': True,
        'data': interests
    })

@api_bp.route('/search', methods=['GET'])
def search():
    """搜索API"""
    query = request.args.get('q', '')
    category_id = request.args.get('category_id', type=int)
    min_price = request.args.get('min_price', type=float)
    max_price = request.args.get('max_price', type=float)
    limit = request.args.get('limit', 20, type=int)
    
    if not query:
        return jsonify({'success': False, 'message': '搜索关键词不能为空'})
    
    items, total_count = ItemService.search_items(
        query=query,
        category_id=category_id,
        min_price=min_price,
        max_price=max_price,
        limit=limit
    )
    
    return jsonify({
        'success': True,
        'data': {
            'items': [item.to_dict() for item in items],
            'total_count': total_count,
            'query': query
        }
    })

@api_bp.route('/stats/overview', methods=['GET'])
def get_overview_stats():
    """获取概览统计API"""
    stats = {
        'total_users': User.query.count(),
        'total_items': Item.query.count(),
        'active_items': Item.query.filter_by(status='active').count(),
        'categories': ItemService.get_category_stats(),
        'price_distribution': ItemService.get_price_distribution()
    }
    
    return jsonify({
        'success': True,
        'data': stats
    })

@api_bp.route('/items/popular', methods=['GET'])
def get_popular_items():
    """获取热门商品API"""
    limit = request.args.get('limit', 20, type=int)
    days = request.args.get('days', 30, type=int)
    
    items = ItemService.get_popular_items(limit=limit, days=days)
    
    return jsonify({
        'success': True,
        'data': [item.to_dict() for item in items]
    })

@api_bp.route('/items/latest', methods=['GET'])
def get_latest_items():
    """获取最新商品API"""
    limit = request.args.get('limit', 20, type=int)
    
    items = ItemService.get_latest_items(limit=limit)
    
    return jsonify({
        'success': True,
        'data': [item.to_dict() for item in items]
    })

@api_bp.route('/items/<int:item_id>/status', methods=['PUT'])
@login_required
def update_item_status(item_id):
    """更新商品状态API"""
    item = Item.query.get_or_404(item_id)
    
    # 检查权限
    if item.seller_id != current_user.id and not current_user.is_admin:
        return jsonify({'success': False, 'message': '无权限修改此商品'})
    
    data = request.get_json()
    new_status = data.get('status')
    
    if new_status not in ['active', 'inactive', 'sold', 'deleted']:
        return jsonify({'success': False, 'message': '无效的状态'})
    
    item.status = new_status
    if new_status == 'sold':
        item.sold_at = datetime.utcnow()
    
    db.session.commit()
    
    return jsonify({
        'success': True,
        'message': f'商品状态已更新为{new_status}'
    })

@api_bp.route('/items/<int:item_id>', methods=['DELETE'])
@login_required
def delete_item(item_id):
    """删除商品API"""
    item = Item.query.get_or_404(item_id)
    
    # 检查权限
    if item.seller_id != current_user.id and not current_user.is_admin:
        return jsonify({'success': False, 'message': '无权限删除此商品'})
    
    db.session.delete(item)
    db.session.commit()
    
    return jsonify({
        'success': True,
        'message': '商品删除成功'
    })

@api_bp.route('/users/behaviors', methods=['GET'])
@login_required
def get_user_behaviors():
    """获取用户行为历史API"""
    limit = request.args.get('limit', 20, type=int)
    
    behaviors = UserService.get_user_behavior_history(current_user.id, limit=limit)
    
    return jsonify({
        'success': True,
        'data': [behavior.to_dict() for behavior in behaviors]
    })

@api_bp.route('/send-verification-code', methods=['POST'])
def send_verification_code():
    """发送邮箱验证码API"""
    from app.services.email_service import EmailService
    
    data = request.get_json()
    email = data.get('email')
    code_type = data.get('type', 'register')
    
    if not email:
        return jsonify({
            'success': False,
            'message': '邮箱地址不能为空'
        }), 400
    
    # 检查邮箱格式
    import re
    email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(email_pattern, email):
        return jsonify({
            'success': False,
            'message': '邮箱格式不正确'
        }), 400
    
    # 检查邮箱是否已被注册（仅注册时检查）
    if code_type == 'register':
        if User.query.filter_by(email=email).first():
            return jsonify({
                'success': False,
                'message': '该邮箱已被注册'
            }), 400
    
    email_service = EmailService()
    
    # 检查发送频率限制
    if not email_service.check_email_send_limit(email, code_type):
        return jsonify({
            'success': False,
            'message': '发送过于频繁，请稍后再试'
        }), 429
    
    result = email_service.send_verification_email(email, code_type)
    
    if result['success']:
        return jsonify({
            'success': True,
            'message': '验证码发送成功'
        })
    else:
        return jsonify({
            'success': False,
            'message': result['message']
        }), 500

@api_bp.route('/verify-email-code', methods=['POST'])
def verify_email_code():
    """验证邮箱验证码API"""
    from app.services.email_service import EmailService
    
    data = request.get_json()
    email = data.get('email')
    code = data.get('code')
    code_type = data.get('type', 'register')
    
    if not all([email, code]):
        return jsonify({
            'success': False,
            'message': '邮箱和验证码不能为空'
        }), 400
    
    email_service = EmailService()
    result = email_service.verify_code(email, code, code_type)
    
    return jsonify(result)

@api_bp.route('/generate-captcha', methods=['POST'])
def generate_captcha():
    """生成验证码API"""
    from app.services.captcha_service import CaptchaService
    
    data = request.get_json()
    captcha_type = data.get('type', 'slider')
    
    captcha_service = CaptchaService()
    
    if captcha_type == 'math':
        result = captcha_service.generate_math_captcha()
    elif captcha_type == 'slider':
        result = captcha_service.generate_slider_captcha()
    elif captcha_type == 'image':
        result = captcha_service.generate_image_captcha()
    else:
        return jsonify({
            'success': False,
            'message': '不支持的验证码类型'
        }), 400
    
    return jsonify(result)

@api_bp.route('/verify-captcha', methods=['POST'])
def verify_captcha():
    """验证验证码API"""
    from app.services.captcha_service import CaptchaService
    
    data = request.get_json()
    captcha_id = data.get('captcha_id')
    captcha_type = data.get('type', 'slider')
    
    if not captcha_id:
        return jsonify({
            'success': False,
            'message': '验证码ID不能为空'
        }), 400
    
    captcha_service = CaptchaService()
    
    if captcha_type == 'math':
        user_answer = data.get('user_answer')
        
        if not user_answer:
            return jsonify({
                'success': False,
                'message': '请输入答案'
            }), 400
        
        result = captcha_service.verify_math_captcha(captcha_id, user_answer)
    elif captcha_type == 'slider':
        user_x = data.get('user_x')
        user_y = data.get('user_y')
        user_angle = data.get('user_angle')
        
        if not all([user_x, user_y, user_angle]):
            return jsonify({
                'success': False,
                'message': '滑块验证数据不完整'
            }), 400
        
        result = captcha_service.verify_slider_captcha(
            captcha_id, user_x, user_y, user_angle
        )
    elif captcha_type == 'image':
        captcha_text = data.get('captcha_text')
        
        if not captcha_text:
            return jsonify({
                'success': False,
                'message': '验证码文本不能为空'
            }), 400
        
        result = captcha_service.verify_image_captcha(captcha_id, captcha_text)
    else:
        return jsonify({
            'success': False,
            'message': '不支持的验证码类型'
        }), 400
    
    return jsonify(result)

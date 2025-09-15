from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify, current_app
from flask_login import login_required, current_user
from app import db
from app.models import User, Item, Category, UserBehavior, Recommendation, Transaction, UserAudit, ItemAudit, UserProfileAudit, ItemProfileAudit, UserAvatarAudit, ItemImageAudit, Conversation, Message, MessageNotification, Announcement
from app.services.recommendation_service import RecommendationService
from app.services.user_service import UserService
from app.services.item_service import ItemService
from app.forms import ItemEditForm
from datetime import datetime, timedelta
from app.utils import get_beijing_utc_now
from werkzeug.utils import secure_filename
import json
import os

admin_bp = Blueprint('admin', __name__)

def admin_required(f):
    """管理员权限装饰器"""
    from functools import wraps
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin:
            flash('需要管理员权限！', 'error')
            return redirect(url_for('main.index'))
        return f(*args, **kwargs)
    return decorated_function

def get_audit_counts():
    """获取审核统计信息，用于所有管理页面"""
    from app.services.audit_service import AuditService
    audit_service = AuditService()
    return audit_service.get_audit_stats()

@admin_bp.route('/')
@login_required
@admin_required
def dashboard():
    """管理后台首页"""
    # 基本统计
    total_users = User.query.count()
    total_items = Item.query.count()
    active_items = Item.query.filter_by(status='active').count()
    total_transactions = Transaction.query.count()
    
    # 最近7天统计
    seven_days_ago = get_beijing_utc_now() - timedelta(days=7)
    
    recent_users = User.query.filter(User.created_at >= seven_days_ago).count()
    recent_items = Item.query.filter(Item.created_at >= seven_days_ago).count()
    recent_behaviors = UserBehavior.query.filter(UserBehavior.created_at >= seven_days_ago).count()
    
    # 热门商品
    popular_items = ItemService.get_popular_items(limit=10)
    
    # 活跃用户
    active_users = UserService.get_active_users(limit=10)
    
    # 分类统计
    category_stats = ItemService.get_category_stats()
    
    # 价格分布
    price_distribution = ItemService.get_price_distribution()
    
    # 推荐统计
    recommendation_service = RecommendationService()
    recommendation_stats = recommendation_service.get_recommendation_stats()
    
    # 审核统计
    from app.services.audit_service import AuditService
    audit_service = AuditService()
    audit_stats = audit_service.get_audit_stats()
    
    # 公告统计
    total_announcements = Announcement.query.count()
    active_announcements = Announcement.query.filter_by(is_active=True).count()
    recent_announcements = Announcement.query.filter(Announcement.created_at >= seven_days_ago).count()
    
    return render_template('admin/dashboard.html',
                         total_users=total_users,
                         total_items=total_items,
                         active_items=active_items,
                         total_transactions=total_transactions,
                         recent_users=recent_users,
                         recent_items=recent_items,
                         recent_behaviors=recent_behaviors,
                         popular_items=popular_items,
                         active_users=active_users,
                         category_stats=category_stats,
                         price_distribution=price_distribution,
                         recommendation_stats=recommendation_stats,
                         audit_stats=audit_stats,
                         audit_counts=audit_stats,
                         total_announcements=total_announcements,
                         active_announcements=active_announcements,
                         recent_announcements=recent_announcements)

@admin_bp.route('/users')
@login_required
@admin_required
def users():
    """用户管理"""
    page = request.args.get('page', 1, type=int)
    search = request.args.get('search', '')
    status = request.args.get('status', 'all')
    
    query = User.query
    
    # 搜索
    if search:
        query = query.filter(
            User.username.contains(search) |
            User.email.contains(search) |
            User.real_name.contains(search)
        )
    
    # 状态筛选
    if status == 'active':
        query = query.filter_by(is_active=True)
    elif status == 'inactive':
        query = query.filter_by(is_active=False)
    elif status == 'admin':
        query = query.filter_by(is_admin=True)
    
    users = query.order_by(User.id.asc()).paginate(
        page=page, per_page=20, error_out=False
    )
    
    return render_template('admin/users.html',
                         users=users,
                         current_search=search,
                         current_status=status,
                         audit_counts=get_audit_counts())

@admin_bp.route('/users/<int:user_id>')
@login_required
@admin_required
def user_detail(user_id):
    """用户详情"""
    user = User.query.get_or_404(user_id)
    user_stats = UserService.get_user_stats(user_id)
    user_interests = UserService.get_user_interests(user_id)
    user_items = ItemService.get_user_items(user_id, limit=10)
    user_behaviors = UserService.get_user_behavior_history(user_id, limit=20)
    
    return render_template('admin/user_detail.html',
                         user=user,
                         user_stats=user_stats,
                         user_interests=user_interests,
                         user_items=user_items,
                         user_behaviors=user_behaviors,
                         audit_counts=get_audit_counts())

@admin_bp.route('/users/<int:user_id>/edit', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_user(user_id):
    """编辑用户信息"""
    user = User.query.get_or_404(user_id)
    
    if request.method == 'POST':
        try:
            # 更新基本信息
            user.username = request.form.get('username')
            user.email = request.form.get('email')
            user.real_name = request.form.get('real_name')
            user.phone = request.form.get('phone')
            user.student_id = request.form.get('student_id')
            user.bio = request.form.get('bio')
            
            # 更新状态
            user.is_active = bool(request.form.get('is_active'))
            user.is_admin = bool(request.form.get('is_admin'))
            
            # 更新密码（如果提供了新密码）
            new_password = request.form.get('new_password')
            if new_password and new_password.strip():
                user.set_password(new_password)
            
            # 检查用户名和邮箱唯一性
            existing_user = User.query.filter(
                User.id != user_id,
                (User.username == user.username) | (User.email == user.email)
            ).first()
            
            if existing_user:
                if existing_user.username == user.username:
                    flash('用户名已存在！', 'error')
                else:
                    flash('邮箱已存在！', 'error')
                return redirect(url_for('admin.user_detail', user_id=user_id))
            
            user.updated_at = get_beijing_utc_now()
            db.session.commit()
            
            flash('用户信息更新成功！', 'success')
            return redirect(url_for('admin.user_detail', user_id=user_id))
            
        except Exception as e:
            db.session.rollback()
            flash(f'更新失败：{str(e)}', 'error')
            return redirect(url_for('admin.user_detail', user_id=user_id))
    
    return redirect(url_for('admin.user_detail', user_id=user_id))

@admin_bp.route('/users/<int:user_id>/toggle_status', methods=['POST'])
@login_required
@admin_required
def toggle_user_status(user_id):
    """切换用户状态"""
    user = User.query.get_or_404(user_id)
    
    if user.id == current_user.id:
        return jsonify({'success': False, 'message': '不能修改自己的状态'})
    
    user.is_active = not user.is_active
    db.session.commit()
    
    return jsonify({
        'success': True,
        'is_active': user.is_active,
        'message': f'用户已{"激活" if user.is_active else "禁用"}'
    })

@admin_bp.route('/users/<int:user_id>/delete', methods=['POST'])
@login_required
@admin_required
def delete_user(user_id):
    """删除用户"""
    user = User.query.get_or_404(user_id)
    
    # 不能删除自己
    if user.id == current_user.id:
        flash('不能删除自己的账户！', 'error')
        return redirect(url_for('admin.users'))
    
    try:
        # 保存用户头像文件名，用于后续删除文件
        user_avatar = user.avatar
        
        # 删除用户相关的数据
        # 1. 删除用户审核记录
        UserAudit.query.filter_by(user_id=user_id).delete()
        
        # 2. 删除用户行为记录
        UserBehavior.query.filter_by(user_id=user_id).delete()
        
        # 3. 删除推荐记录
        Recommendation.query.filter_by(user_id=user_id).delete()
        
        # 4. 处理用户发布的商品（标记为已删除或转移给系统）
        user_items = Item.query.filter_by(seller_id=user_id).all()
        for item in user_items:
            item.status = 'deleted'
            item.title = f"[已删除用户] {item.title}"
            item.description = "该商品的原发布者已被删除"
        
        # 5. 处理交易记录（标记为已删除）
        user_transactions = Transaction.query.filter(
            (Transaction.buyer_id == user_id) | (Transaction.seller_id == user_id)
        ).all()
        for transaction in user_transactions:
            transaction.status = 'cancelled'
            if transaction.buyer_id == user_id:
                transaction.buyer_notes = "交易因用户删除而取消"
            if transaction.seller_id == user_id:
                transaction.seller_notes = "交易因用户删除而取消"
        
        # 6. 删除用户
        db.session.delete(user)
        db.session.commit()
        
        # 7. 删除用户头像文件
        if user_avatar:
            avatar_path = os.path.join(current_app.config['UPLOAD_FOLDER'], 'avatars', user_avatar)
            if os.path.exists(avatar_path):
                try:
                    os.remove(avatar_path)
                except OSError as e:
                    current_app.logger.warning(f"删除用户头像文件失败: {e}")
        
        flash(f'用户 {user.username} 已成功删除！', 'success')
        
    except Exception as e:
        db.session.rollback()
        flash(f'删除用户失败：{str(e)}', 'error')
    
    return redirect(url_for('admin.users'))

@admin_bp.route('/items')
@login_required
@admin_required
def items():
    """商品管理"""
    page = request.args.get('page', 1, type=int)
    search = request.args.get('search', '')
    status = request.args.get('status', 'all')
    category_id = request.args.get('category', type=int)
    
    query = Item.query
    
    # 搜索
    if search:
        query = query.filter(
            Item.title.contains(search) |
            Item.description.contains(search)
        )
    
    # 状态筛选
    if status != 'all':
        query = query.filter_by(status=status)
    
    # 分类筛选
    if category_id:
        query = query.filter_by(category_id=category_id)
    
    items = query.order_by(Item.created_at.desc()).paginate(
        page=page, per_page=20, error_out=False
    )
    
    categories = Category.query.filter_by(is_active=True).all()
    
    return render_template('admin/items.html',
                         items=items,
                         categories=categories,
                         current_search=search,
                         current_status=status,
                         current_category=category_id,
                         audit_counts=get_audit_counts())

@admin_bp.route('/items/<int:item_id>')
@login_required
@admin_required
def item_detail(item_id):
    """商品详情"""
    item = Item.query.get_or_404(item_id)
    item_stats = ItemService.get_item_stats(item_id)
    related_items = ItemService.get_related_items(item_id, limit=5)
    
    return render_template('admin/item_detail.html',
                         item=item,
                         item_stats=item_stats,
                         related_items=related_items,
                         audit_counts=get_audit_counts())

@admin_bp.route('/api/items/<int:item_id>')
@login_required
@admin_required
def api_item_detail(item_id):
    """商品详情API"""
    try:
        item = Item.query.get_or_404(item_id)
        
        # 获取商品图片
        images = []
        image_list = item.get_images_list()
        if image_list:
            for i, filename in enumerate(image_list):
                images.append({
                    'id': i,
                    'filename': filename,
                    'url': url_for('static', filename='uploads/items/' + filename)
                })
        
        # 获取商品分类
        category = {
            'id': item.category.id,
            'name': item.category.name
        } if item.category else None
        
        # 获取卖家信息
        seller = {
            'id': item.seller.id,
            'username': item.seller.username,
            'email': item.seller.email,
            'avatar': item.seller.avatar,
            'avatar_url': url_for('static', filename='uploads/avatars/' + item.seller.avatar) if item.seller.avatar and item.seller.avatar != 'None' and item.seller.avatar != '' and item.seller.avatar != 'null' else None
        }
        
        # 构建商品数据
        item_data = {
            'id': item.id,
            'title': item.title,
            'description': item.description,
            'price': float(item.price),
            'original_price': float(item.original_price) if item.original_price else None,
            'condition': item.condition,
            'status': item.status,
            'created_at': item.created_at.isoformat() if item.created_at else None,
            'updated_at': item.updated_at.isoformat() if item.updated_at else None,
            'category': category,
            'seller': seller,
            'images': images,
            'main_image': {
                'filename': item.get_main_image(),
                'url': url_for('static', filename='uploads/items/' + item.get_main_image()) if item.get_main_image() else None
            } if item.get_main_image() else None
        }
        
        return jsonify({
            'success': True,
            'data': item_data
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'获取商品详情失败: {str(e)}'
        }), 500

@admin_bp.route('/items/<int:item_id>/edit', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_item(item_id):
    """编辑商品信息"""
    item = Item.query.get_or_404(item_id)
    form = ItemEditForm(obj=item)
    
    if form.validate_on_submit():
        try:
            # 获取旧图片列表，用于后续删除
            old_images = item.get_images_list()
            
            # 更新商品信息
            item.title = form.title.data
            item.description = form.description.data
            item.price = form.price.data
            item.original_price = form.original_price.data if form.original_price.data else None
            item.condition = form.condition.data
            item.category_id = form.category_id.data
            item.location = form.location.data
            item.contact_method = form.contact_method.data
            item.contact_info = form.contact_info.data
            item.status = form.status.data
            
            # 处理图片上传
            if form.images.data and any(file.filename for file in form.images.data):
                new_images = []
                for i, file in enumerate(form.images.data):
                    if file and file.filename:
                        filename = secure_filename(file.filename)
                        if filename:
                            timestamp = get_beijing_utc_now().strftime('%Y%m%d_%H%M%S')
                            filename = f"{item.seller_id}_{timestamp}_{i+1}_{filename}"
                            
                            # 确保上传目录存在
                            upload_dir = os.path.join(current_app.config['UPLOAD_FOLDER'], 'items')
                            os.makedirs(upload_dir, exist_ok=True)
                            
                            upload_path = os.path.join(upload_dir, filename)
                            file.save(upload_path)
                            new_images.append(filename)
                
                if new_images:
                    # 更新图片列表
                    item.set_images_list(new_images)
                    
                    # 删除旧图片文件
                    for old_image in old_images:
                        old_path = os.path.join(current_app.config['UPLOAD_FOLDER'], 'items', old_image)
                        if os.path.exists(old_path):
                            try:
                                os.remove(old_path)
                            except Exception as e:
                                print(f"删除旧图片失败: {old_image}, 错误: {e}")
            
            # 更新修改时间
            item.updated_at = get_beijing_utc_now()
            
            db.session.commit()
            
            flash('商品信息更新成功！', 'success')
            return redirect(url_for('admin.item_detail', item_id=item_id))
            
        except Exception as e:
            db.session.rollback()
            flash(f'更新失败：{str(e)}', 'error')
    
    # 预填充表单数据
    if request.method == 'GET':
        form.title.data = item.title
        form.description.data = item.description
        form.price.data = item.price
        form.original_price.data = item.original_price
        form.condition.data = item.condition
        form.category_id.data = item.category_id
        form.location.data = item.location
        form.contact_method.data = item.contact_method
        form.contact_info.data = item.contact_info
        form.status.data = item.status
    
    return render_template('admin/edit_item.html', form=form, item=item)

@admin_bp.route('/items/<int:item_id>/toggle_status', methods=['POST'])
@login_required
@admin_required
def toggle_item_status(item_id):
    """切换商品状态"""
    item = Item.query.get_or_404(item_id)
    new_status = request.json.get('status')
    
    if new_status not in ['active', 'inactive', 'sold', 'deleted']:
        return jsonify({'success': False, 'message': '无效的状态'})
    
    item.status = new_status
    if new_status == 'sold':
        item.sold_at = get_beijing_utc_now()
    
    db.session.commit()
    
    return jsonify({
        'success': True,
        'status': item.status,
        'message': f'商品状态已更新为{new_status}'
    })

@admin_bp.route('/items/<int:item_id>/delete', methods=['POST'])
@login_required
@admin_required
def delete_item(item_id):
    """删除商品"""
    try:
        item = Item.query.get_or_404(item_id)
        
        # 检查是否有相关交易记录
        transaction_count = Transaction.query.filter_by(item_id=item_id).count()
        if transaction_count > 0:
            return jsonify({
                'success': False, 
                'message': f'该商品有 {transaction_count} 条交易记录，无法删除。请先处理相关交易。'
            })
        
        # 删除相关的用户行为记录
        UserBehavior.query.filter_by(item_id=item_id).delete()
        
        # 删除相关的推荐记录
        Recommendation.query.filter_by(item_id=item_id).delete()
        
        # 删除AI推荐记录（直接使用SQL避免外键约束问题）
        from sqlalchemy import text
        db.session.execute(
            text("DELETE FROM ai_recommendations WHERE item_id = :item_id"),
            {'item_id': item_id}
        )
        
        # 删除相关的审核记录
        ItemAudit.query.filter_by(item_id=item_id).delete()
        ItemProfileAudit.query.filter_by(item_id=item_id).delete()
        ItemImageAudit.query.filter_by(item_id=item_id).delete()
        
        # 删除相关的消息记录
        conversations = Conversation.query.filter_by(item_id=item_id).all()
        for conv in conversations:
            Message.query.filter_by(conversation_id=conv.id).delete()
            MessageNotification.query.filter_by(conversation_id=conv.id).delete()
        Conversation.query.filter_by(item_id=item_id).delete()
        
        # 删除商品本身
        db.session.delete(item)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': '商品删除成功'
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': f'删除失败: {str(e)}'
        })

@admin_bp.route('/categories')
@login_required
@admin_required
def categories():
    """分类管理"""
    categories = Category.query.order_by(Category.id.asc()).all()
    return render_template('admin/categories.html', 
                         categories=categories,
                         audit_counts=get_audit_counts())

@admin_bp.route('/categories/create', methods=['GET', 'POST'])
@login_required
@admin_required
def create_category():
    """创建分类"""
    if request.method == 'POST':
        try:
            name = request.form.get('name')
            description = request.form.get('description')
            icon = request.form.get('icon')
            parent_id = request.form.get('parent_id', type=int) or None
            sort_order = request.form.get('sort_order', type=int) or 0
            
            if not name:
                flash('分类名称不能为空！', 'error')
                return render_template('admin/create_category.html',
                                     audit_counts=get_audit_counts())
            
            if Category.query.filter_by(name=name).first():
                flash('分类名称已存在！', 'error')
                return render_template('admin/create_category.html',
                                     audit_counts=get_audit_counts())
            
            # 查找最小可用的ID
            existing_ids = [cat.id for cat in Category.query.all()]
            min_available_id = 1
            while min_available_id in existing_ids:
                min_available_id += 1
            
            category = Category(
                id=min_available_id,
                name=name,
                description=description,
                icon=icon,
                parent_id=parent_id,
                sort_order=sort_order
            )
            
            db.session.add(category)
            db.session.commit()
            
            flash('分类创建成功！', 'success')
            return redirect(url_for('admin.categories'))
            
        except Exception as e:
            db.session.rollback()
            flash(f'创建失败：{str(e)}', 'error')
            return render_template('admin/create_category.html')
    
    categories = Category.query.filter_by(parent_id=None).all()
    return render_template('admin/create_category.html', 
                         categories=categories,
                         audit_counts=get_audit_counts())

@admin_bp.route('/categories/<int:category_id>/edit', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_category(category_id):
    """编辑分类"""
    category = Category.query.get_or_404(category_id)
    
    if request.method == 'POST':
        try:
            # 检查分类名称唯一性
            existing_category = Category.query.filter(
                Category.id != category_id,
                Category.name == request.form.get('name')
            ).first()
            
            if existing_category:
                flash('分类名称已存在！', 'error')
                return redirect(url_for('admin.edit_category', category_id=category_id))
            
            category.name = request.form.get('name')
            category.description = request.form.get('description')
            category.icon = request.form.get('icon')
            category.parent_id = request.form.get('parent_id', type=int) or None
            category.sort_order = request.form.get('sort_order', type=int) or 0
            category.is_active = bool(request.form.get('is_active'))
            
            db.session.commit()
            
            flash('分类更新成功！', 'success')
            return redirect(url_for('admin.categories'))
            
        except Exception as e:
            db.session.rollback()
            flash(f'更新失败：{str(e)}', 'error')
            return redirect(url_for('admin.edit_category', category_id=category_id))
    
    categories = Category.query.filter(Category.id != category_id, Category.parent_id == None).all()
    return render_template('admin/edit_category.html', 
                         category=category, 
                         categories=categories,
                         audit_counts=get_audit_counts())

@admin_bp.route('/categories/<int:category_id>/toggle_status', methods=['POST'])
@login_required
@admin_required
def toggle_category_status(category_id):
    """切换分类状态"""
    try:
        category = Category.query.get_or_404(category_id)
        category.is_active = not category.is_active
        db.session.commit()
        
        return jsonify({
            'success': True,
            'is_active': category.is_active,
            'message': f'分类已{"启用" if category.is_active else "禁用"}'
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': f'操作失败：{str(e)}'
        })

@admin_bp.route('/categories/<int:category_id>/delete', methods=['POST'])
@login_required
@admin_required
def delete_category(category_id):
    """删除分类"""
    try:
        category = Category.query.get_or_404(category_id)
        
        # 检查是否有子分类
        if category.children:
            return jsonify({
                'success': False,
                'message': '该分类下还有子分类，无法删除'
            })
        
        # 检查是否有商品
        if category.items.count() > 0:
            return jsonify({
                'success': False,
                'message': '该分类下还有商品，无法删除'
            })
        
        db.session.delete(category)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': '分类删除成功'
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': f'删除失败：{str(e)}'
        })

@admin_bp.route('/behaviors')
@login_required
@admin_required
def behaviors():
    """用户行为管理"""
    page = request.args.get('page', 1, type=int)
    behavior_type = request.args.get('type', 'all')
    days = request.args.get('days', 7, type=int)
    
    query = UserBehavior.query
    
    # 行为类型筛选
    if behavior_type != 'all':
        query = query.filter_by(behavior_type=behavior_type)
    
    # 时间筛选
    if days > 0:
        days_ago = get_beijing_utc_now() - timedelta(days=days)
        query = query.filter(UserBehavior.created_at >= days_ago)
    
    behaviors = query.order_by(UserBehavior.created_at.desc()).paginate(
        page=page, per_page=50, error_out=False
    )
    
    return render_template('admin/behaviors.html',
                         behaviors=behaviors,
                         current_type=behavior_type,
                         current_days=days,
                         audit_counts=get_audit_counts())

@admin_bp.route('/recommendations')
@login_required
@admin_required
def recommendations():
    """推荐管理"""
    page = request.args.get('page', 1, type=int)
    algorithm_type = request.args.get('algorithm', 'all')
    
    query = Recommendation.query
    
    # 算法类型筛选
    if algorithm_type != 'all':
        query = query.filter_by(algorithm_type=algorithm_type)
    
    recommendations = query.order_by(Recommendation.created_at.desc()).paginate(
        page=page, per_page=50, error_out=False
    )
    
    return render_template('admin/recommendations.html',
                         recommendations=recommendations,
                         current_algorithm=algorithm_type,
                         audit_counts=get_audit_counts())

@admin_bp.route('/analytics')
@login_required
@admin_required
def analytics():
    """数据分析"""
    # 用户增长趋势（最近30天）
    thirty_days_ago = get_beijing_utc_now() - timedelta(days=30)
    user_growth = []
    
    for i in range(30):
        date = thirty_days_ago + timedelta(days=i)
        next_date = date + timedelta(days=1)
        
        count = User.query.filter(
            User.created_at >= date,
            User.created_at < next_date
        ).count()
        
        user_growth.append({
            'date': date.strftime('%Y-%m-%d'),
            'count': count
        })
    
    # 商品发布趋势
    item_growth = []
    
    for i in range(30):
        date = thirty_days_ago + timedelta(days=i)
        next_date = date + timedelta(days=1)
        
        count = Item.query.filter(
            Item.created_at >= date,
            Item.created_at < next_date
        ).count()
        
        item_growth.append({
            'date': date.strftime('%Y-%m-%d'),
            'count': count
        })
    
    # 行为统计
    behavior_stats = db.session.query(
        UserBehavior.behavior_type,
        db.func.count(UserBehavior.id)
    ).filter(UserBehavior.created_at >= thirty_days_ago).group_by(
        UserBehavior.behavior_type
    ).all()
    
    behavior_data = dict(behavior_stats)
    
    return render_template('admin/analytics.html',
                         user_growth=user_growth,
                         item_growth=item_growth,
                         behavior_data=behavior_data,
                         audit_counts=get_audit_counts())

@admin_bp.route('/audits')
@login_required
@admin_required
def audits():
    """审核管理首页"""
    from app.services.audit_service import AuditService
    audit_service = AuditService()
    
    # 获取待审核统计
    audit_stats = audit_service.get_audit_stats()
    
    # 获取最近的审核记录
    recent_user_audits = UserAudit.query.order_by(UserAudit.created_at.desc()).limit(10).all()
    recent_item_audits = ItemAudit.query.order_by(ItemAudit.created_at.desc()).limit(10).all()
    
    return render_template('admin/audits.html',
                         audit_stats=audit_stats,
                         audit_counts=audit_stats,  # 为了兼容模板中的变量名
                         recent_user_audits=recent_user_audits,
                         recent_item_audits=recent_item_audits)

@admin_bp.route('/audits/users')
@login_required
@admin_required
def user_audits():
    """用户审核管理"""
    page = request.args.get('page', 1, type=int)
    status = request.args.get('status', 'pending')
    
    query = UserAudit.query
    
    if status != 'all':
        query = query.filter_by(status=status)
    
    audits = query.order_by(UserAudit.created_at.asc()).paginate(
        page=page, per_page=20, error_out=False
    )
    
    return render_template('admin/user_audits.html',
                         audits=audits,
                         current_status=status,
                         audit_counts=get_audit_counts())

@admin_bp.route('/audits/items')
@login_required
@admin_required
def item_audits():
    """商品审核管理"""
    page = request.args.get('page', 1, type=int)
    status = request.args.get('status', 'pending')
    
    query = ItemAudit.query
    
    if status != 'all':
        query = query.filter_by(status=status)
    
    audits = query.order_by(ItemAudit.created_at.asc()).paginate(
        page=page, per_page=20, error_out=False
    )
    
    return render_template('admin/item_audits.html',
                         audits=audits,
                         current_status=status,
                         audit_counts=get_audit_counts())

@admin_bp.route('/audits/users/<int:audit_id>/approve', methods=['POST'])
@login_required
@admin_required
def approve_user_audit(audit_id):
    """审核通过用户"""
    from app.services.audit_service import AuditService
    
    audit = UserAudit.query.get_or_404(audit_id)
    admin_notes = request.json.get('admin_notes', '')
    
    audit_service = AuditService()
    result = audit_service.approve_user(audit.user_id, current_user.id, admin_notes)
    
    return jsonify(result)

@admin_bp.route('/audits/users/<int:audit_id>/reject', methods=['POST'])
@login_required
@admin_required
def reject_user_audit(audit_id):
    """审核拒绝用户"""
    from app.services.audit_service import AuditService
    
    audit = UserAudit.query.get_or_404(audit_id)
    rejection_reason = request.json.get('rejection_reason', '')
    admin_notes = request.json.get('admin_notes', '')
    
    if not rejection_reason:
        return jsonify({'success': False, 'message': '请填写拒绝原因'})
    
    audit_service = AuditService()
    result = audit_service.reject_user(audit.user_id, current_user.id, rejection_reason, admin_notes)
    
    return jsonify(result)

@admin_bp.route('/audits/items/<int:audit_id>/approve', methods=['POST'])
@login_required
@admin_required
def approve_item_audit(audit_id):
    """审核通过商品"""
    from app.services.audit_service import AuditService
    
    audit = ItemAudit.query.get_or_404(audit_id)
    admin_notes = request.json.get('admin_notes', '')
    
    audit_service = AuditService()
    result = audit_service.approve_item(audit.item_id, current_user.id, admin_notes)
    
    return jsonify(result)

@admin_bp.route('/audits/items/<int:audit_id>/reject', methods=['POST'])
@login_required
@admin_required
def reject_item_audit(audit_id):
    """审核拒绝商品"""
    from app.services.audit_service import AuditService
    
    audit = ItemAudit.query.get_or_404(audit_id)
    rejection_reason = request.json.get('rejection_reason', '')
    admin_notes = request.json.get('admin_notes', '')
    
    if not rejection_reason:
        return jsonify({'success': False, 'message': '请填写拒绝原因'})
    
    audit_service = AuditService()
    result = audit_service.reject_item(audit.item_id, current_user.id, rejection_reason, admin_notes)
    
    return jsonify(result)

@admin_bp.route('/audits/user-profiles')
@login_required
@admin_required
def user_profile_audits():
    """用户资料修改审核管理"""
    page = request.args.get('page', 1, type=int)
    status = request.args.get('status', 'pending')
    
    query = UserProfileAudit.query
    
    if status != 'all':
        query = query.filter_by(status=status)
    
    audits = query.order_by(UserProfileAudit.created_at.asc()).paginate(
        page=page, per_page=20, error_out=False
    )
    
    return render_template('admin/user_profile_audits.html',
                         audits=audits,
                         current_status=status,
                         audit_counts=get_audit_counts())

@admin_bp.route('/audits/item-profiles')
@login_required
@admin_required
def item_profile_audits():
    """商品资料修改审核管理"""
    page = request.args.get('page', 1, type=int)
    status = request.args.get('status', 'pending')
    
    query = ItemProfileAudit.query
    
    if status != 'all':
        query = query.filter_by(status=status)
    
    audits = query.order_by(ItemProfileAudit.created_at.asc()).paginate(
        page=page, per_page=20, error_out=False
    )
    
    return render_template('admin/item_profile_audits.html',
                         audits=audits,
                         current_status=status,
                         audit_counts=get_audit_counts())

@admin_bp.route('/audits/user-profiles/<int:audit_id>/approve', methods=['POST'])
@login_required
@admin_required
def approve_user_profile_audit(audit_id):
    """审核通过用户资料修改"""
    from app.services.audit_service import AuditService
    
    audit = UserProfileAudit.query.get_or_404(audit_id)
    admin_notes = request.json.get('admin_notes', '')
    
    audit_service = AuditService()
    result = audit_service.approve_user_profile(audit_id, current_user.id, admin_notes)
    
    return jsonify(result)

@admin_bp.route('/audits/user-profiles/<int:audit_id>/reject', methods=['POST'])
@login_required
@admin_required
def reject_user_profile_audit(audit_id):
    """审核拒绝用户资料修改"""
    from app.services.audit_service import AuditService
    
    audit = UserProfileAudit.query.get_or_404(audit_id)
    rejection_reason = request.json.get('rejection_reason', '')
    admin_notes = request.json.get('admin_notes', '')
    
    if not rejection_reason:
        return jsonify({'success': False, 'message': '请填写拒绝原因'})
    
    audit_service = AuditService()
    result = audit_service.reject_user_profile(audit_id, current_user.id, rejection_reason, admin_notes)
    
    return jsonify(result)

@admin_bp.route('/audits/user-profiles/batch-approve', methods=['POST'])
@login_required
@admin_required
def batch_approve_user_profiles():
    """批量审核通过用户资料修改"""
    from app.services.audit_service import AuditService
    
    data = request.get_json()
    audit_ids = data.get('audit_ids', [])
    admin_notes = data.get('admin_notes', '')
    
    if not audit_ids:
        return jsonify({'success': False, 'message': '请选择要审核的项目'})
    
    audit_service = AuditService()
    results = []
    
    for audit_id in audit_ids:
        result = audit_service.approve_user_profile(audit_id, current_user.id, admin_notes)
        results.append(result)
    
    success_count = sum(1 for r in results if r.get('success'))
    return jsonify({
        'success': True, 
        'message': f'成功审核 {success_count}/{len(audit_ids)} 个项目',
        'results': results
    })

@admin_bp.route('/audits/user-profiles/batch-reject', methods=['POST'])
@login_required
@admin_required
def batch_reject_user_profiles():
    """批量审核拒绝用户资料修改"""
    from app.services.audit_service import AuditService
    
    data = request.get_json()
    audit_ids = data.get('audit_ids', [])
    rejection_reason = data.get('rejection_reason', '')
    admin_notes = data.get('admin_notes', '')
    
    if not audit_ids:
        return jsonify({'success': False, 'message': '请选择要审核的项目'})
    
    if not rejection_reason:
        return jsonify({'success': False, 'message': '请填写拒绝原因'})
    
    audit_service = AuditService()
    results = []
    
    for audit_id in audit_ids:
        result = audit_service.reject_user_profile(audit_id, current_user.id, rejection_reason, admin_notes)
        results.append(result)
    
    success_count = sum(1 for r in results if r.get('success'))
    return jsonify({
        'success': True, 
        'message': f'成功审核 {success_count}/{len(audit_ids)} 个项目',
        'results': results
    })

@admin_bp.route('/audits/item-profiles/<int:audit_id>/approve', methods=['POST'])
@login_required
@admin_required
def approve_item_profile_audit(audit_id):
    """审核通过商品资料修改"""
    from app.services.audit_service import AuditService
    
    audit = ItemProfileAudit.query.get_or_404(audit_id)
    admin_notes = request.json.get('admin_notes', '')
    
    audit_service = AuditService()
    result = audit_service.approve_item_profile(audit_id, current_user.id, admin_notes)
    
    return jsonify(result)

@admin_bp.route('/audits/item-profiles/<int:audit_id>/reject', methods=['POST'])
@login_required
@admin_required
def reject_item_profile_audit(audit_id):
    """审核拒绝商品资料修改"""
    from app.services.audit_service import AuditService
    
    audit = ItemProfileAudit.query.get_or_404(audit_id)
    rejection_reason = request.json.get('rejection_reason', '')
    admin_notes = request.json.get('admin_notes', '')
    
    if not rejection_reason:
        return jsonify({'success': False, 'message': '请填写拒绝原因'})
    
    audit_service = AuditService()
    result = audit_service.reject_item_profile(audit_id, current_user.id, rejection_reason, admin_notes)
    
    return jsonify(result)

@admin_bp.route('/settings')
@login_required
@admin_required
def settings():
    """系统设置"""
    return render_template('admin/settings.html',
                         audit_counts=get_audit_counts())

# ==================== 单项审核相关路由 ====================

@admin_bp.route('/audit/user-profile-item', methods=['POST'])
@login_required
@admin_required
def audit_user_profile_item():
    """审核用户资料修改的单个字段"""
    from app.services.audit_service import AuditService
    
    data = request.json
    audit_id = data.get('audit_id')
    field_name = data.get('field_name')
    status = data.get('status')  # 'approved' 或 'rejected'
    admin_notes = data.get('admin_notes', '')
    
    if not all([audit_id, field_name, status]):
        return jsonify({'success': False, 'message': '参数不完整'})
    
    if status not in ['approved', 'rejected']:
        return jsonify({'success': False, 'message': '状态参数无效'})
    
    audit_service = AuditService()
    result = audit_service.audit_user_profile_item(audit_id, field_name, status, current_user.id, admin_notes)
    
    return jsonify(result)

@admin_bp.route('/audit/user-profile-complete', methods=['POST'])
@login_required
@admin_required
def complete_user_profile_audit():
    """完成用户资料修改的单项审核"""
    from app.services.audit_service import AuditService
    
    data = request.json
    audit_id = data.get('audit_id')
    audit_results = data.get('audit_results', {})
    
    if not audit_id or not audit_results:
        return jsonify({'success': False, 'message': '参数不完整'})
    
    audit_service = AuditService()
    result = audit_service.complete_user_profile_audit(audit_id, audit_results, current_user.id)
    
    return jsonify(result)

@admin_bp.route('/audit/item-profile-item', methods=['POST'])
@login_required
@admin_required
def audit_item_profile_item():
    """审核商品资料修改的单个字段"""
    from app.services.audit_service import AuditService
    
    data = request.json
    audit_id = data.get('audit_id')
    field_name = data.get('field_name')
    status = data.get('status')  # 'approved' 或 'rejected'
    admin_notes = data.get('admin_notes', '')
    
    if not all([audit_id, field_name, status]):
        return jsonify({'success': False, 'message': '参数不完整'})
    
    if status not in ['approved', 'rejected']:
        return jsonify({'success': False, 'message': '状态参数无效'})
    
    audit_service = AuditService()
    result = audit_service.audit_item_profile_item(audit_id, field_name, status, current_user.id, admin_notes)
    
    return jsonify(result)

@admin_bp.route('/audit/item-profile-complete', methods=['POST'])
@login_required
@admin_required
def complete_item_profile_audit():
    """完成商品资料修改的单项审核"""
    from app.services.audit_service import AuditService
    
    data = request.json
    audit_id = data.get('audit_id')
    audit_results = data.get('audit_results', {})
    
    if not audit_id or not audit_results:
        return jsonify({'success': False, 'message': '参数不完整'})
    
    audit_service = AuditService()
    result = audit_service.complete_item_profile_audit(audit_id, audit_results, current_user.id)
    
    return jsonify(result)

@admin_bp.route('/audit/user-avatar', methods=['POST'])
@login_required
@admin_required
def audit_user_avatar():
    """审核用户头像修改"""
    from app.services.audit_service import AuditService
    
    data = request.json
    audit_id = data.get('audit_id')
    action = data.get('action')  # 'approve' 或 'reject'
    admin_notes = data.get('admin_notes', '')
    rejection_reason = data.get('rejection_reason', '')
    
    if not audit_id or not action:
        return jsonify({'success': False, 'message': '参数不完整'})
    
    audit_service = AuditService()
    
    if action == 'approve':
        result = audit_service.approve_user_avatar(audit_id, current_user.id, admin_notes)
    elif action == 'reject':
        if not rejection_reason:
            return jsonify({'success': False, 'message': '请填写拒绝原因'})
        result = audit_service.reject_user_avatar(audit_id, current_user.id, rejection_reason, admin_notes)
    else:
        return jsonify({'success': False, 'message': '操作参数无效'})
    
    return jsonify(result)

@admin_bp.route('/audit/item-image', methods=['POST'])
@login_required
@admin_required
def audit_item_image():
    """审核商品图片修改"""
    from app.services.audit_service import AuditService
    
    data = request.json
    audit_id = data.get('audit_id')
    action = data.get('action')  # 'approve' 或 'reject'
    admin_notes = data.get('admin_notes', '')
    rejection_reason = data.get('rejection_reason', '')
    
    if not audit_id or not action:
        return jsonify({'success': False, 'message': '参数不完整'})
    
    audit_service = AuditService()
    
    if action == 'approve':
        result = audit_service.approve_item_image(audit_id, current_user.id, admin_notes)
    elif action == 'reject':
        if not rejection_reason:
            return jsonify({'success': False, 'message': '请填写拒绝原因'})
        result = audit_service.reject_item_image(audit_id, current_user.id, rejection_reason, admin_notes)
    else:
        return jsonify({'success': False, 'message': '操作参数无效'})
    
    return jsonify(result)

# ==================== 公告管理相关路由 ====================

@admin_bp.route('/announcements')
@login_required
@admin_required
def announcements():
    """公告管理"""
    from app.services.announcement_service import AnnouncementService
    
    page = request.args.get('page', 1, type=int)
    status = request.args.get('status', 'all')
    announcement_type = request.args.get('type', 'all')
    priority = request.args.get('priority', 'all')
    search = request.args.get('search', '')
    sort_by = request.args.get('sort_by', 'created_at')
    sort_order = request.args.get('sort_order', 'desc')
    
    announcement_service = AnnouncementService()
    announcements = announcement_service.get_announcements(
        page=page, per_page=20, status=status, 
        announcement_type=announcement_type, priority=priority, search=search,
        sort_by=sort_by, sort_order=sort_order
    )
    
    # 为每个公告添加推送状态和已读率统计
    for announcement in announcements.items:
        announcement.push_status = announcement_service.get_announcement_push_status(announcement.id)
        announcement.read_stats = announcement_service.get_announcement_read_stats(announcement.id)
    
    return render_template('admin/announcements.html',
                         announcements=announcements,
                         current_status=status,
                         current_type=announcement_type,
                         current_priority=priority,
                         current_search=search,
                         current_sort_by=sort_by,
                         current_sort_order=sort_order,
                         audit_counts=get_audit_counts())

@admin_bp.route('/announcements/preview', methods=['POST'])
@login_required
@admin_required
def preview_announcement():
    """预览Markdown内容"""
    try:
        data = request.get_json()
        content = data.get('content', '').strip()
        
        if not content:
            return jsonify({'success': False, 'error': '内容不能为空'})
        
        # 创建临时公告对象进行渲染
        from app.models.announcement import Announcement
        temp_announcement = Announcement()
        temp_announcement.content = content
        
        html_content = temp_announcement.render_content()
        
        return jsonify({
            'success': True,
            'html': html_content
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@admin_bp.route('/announcements/create', methods=['GET', 'POST'])
@login_required
@admin_required
def create_announcement():
    """创建公告"""
    from app.services.announcement_service import AnnouncementService
    
    if request.method == 'POST':
        try:
            title = request.form.get('title', '').strip()
            content = request.form.get('content', '').strip()
            announcement_type = request.form.get('type', 'system')
            priority = request.form.get('priority', 'normal')
            is_pinned = bool(request.form.get('is_pinned'))
            
            # 处理时间
            start_time_str = request.form.get('start_time')
            end_time_str = request.form.get('end_time')
            
            start_time = None
            end_time = None
            
            if start_time_str:
                try:
                    start_time = datetime.strptime(start_time_str, '%Y-%m-%dT%H:%M')
                except ValueError:
                    flash('开始时间格式错误！', 'error')
                    return render_template('admin/create_announcement.html',
                                         audit_counts=get_audit_counts())
            
            if end_time_str:
                try:
                    end_time = datetime.strptime(end_time_str, '%Y-%m-%dT%H:%M')
                except ValueError:
                    flash('结束时间格式错误！', 'error')
                    return render_template('admin/create_announcement.html',
                                         audit_counts=get_audit_counts())
            
            # 验证时间逻辑
            if start_time and end_time and start_time >= end_time:
                flash('开始时间必须早于结束时间！', 'error')
                return render_template('admin/create_announcement.html',
                                     audit_counts=get_audit_counts())
            
            if not title:
                flash('公告标题不能为空！', 'error')
                return render_template('admin/create_announcement.html',
                                     audit_counts=get_audit_counts())
            
            if not content:
                flash('公告内容不能为空！', 'error')
                return render_template('admin/create_announcement.html',
                                     audit_counts=get_audit_counts())
            
            announcement_service = AnnouncementService()
            result = announcement_service.create_announcement(
                title=title,
                content=content,
                announcement_type=announcement_type,
                priority=priority,
                is_pinned=is_pinned,
                start_time=start_time,
                end_time=end_time,
                created_by=current_user.id
            )
            
            if result['success']:
                flash('公告创建成功！', 'success')
                return redirect(url_for('admin.announcements'))
            else:
                flash(f'创建失败：{result["message"]}', 'error')
        
        except Exception as e:
            flash(f'创建失败：{str(e)}', 'error')
    
    return render_template('admin/create_announcement.html',
                         audit_counts=get_audit_counts())

@admin_bp.route('/announcements/<int:announcement_id>/edit', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_announcement(announcement_id):
    """编辑公告"""
    from app.services.announcement_service import AnnouncementService
    
    announcement = Announcement.query.get_or_404(announcement_id)
    announcement_service = AnnouncementService()
    
    if request.method == 'POST':
        try:
            title = request.form.get('title', '').strip()
            content = request.form.get('content', '').strip()
            announcement_type = request.form.get('type', 'system')
            priority = request.form.get('priority', 'normal')
            is_pinned = bool(request.form.get('is_pinned'))
            is_active = bool(request.form.get('is_active'))
            
            # 处理时间
            start_time_str = request.form.get('start_time')
            end_time_str = request.form.get('end_time')
            
            start_time = None
            end_time = None
            
            if start_time_str:
                try:
                    start_time = datetime.strptime(start_time_str, '%Y-%m-%dT%H:%M')
                except ValueError:
                    flash('开始时间格式错误！', 'error')
                    return redirect(url_for('admin.edit_announcement', announcement_id=announcement_id))
            
            if end_time_str:
                try:
                    end_time = datetime.strptime(end_time_str, '%Y-%m-%dT%H:%M')
                except ValueError:
                    flash('结束时间格式错误！', 'error')
                    return redirect(url_for('admin.edit_announcement', announcement_id=announcement_id))
            
            # 验证时间逻辑
            if start_time and end_time and start_time >= end_time:
                flash('开始时间必须早于结束时间！', 'error')
                return redirect(url_for('admin.edit_announcement', announcement_id=announcement_id))
            
            if not title:
                flash('公告标题不能为空！', 'error')
                return redirect(url_for('admin.edit_announcement', announcement_id=announcement_id))
            
            if not content:
                flash('公告内容不能为空！', 'error')
                return redirect(url_for('admin.edit_announcement', announcement_id=announcement_id))
            
            result = announcement_service.update_announcement(
                announcement_id,
                title=title,
                content=content,
                type=announcement_type,
                priority=priority,
                is_pinned=is_pinned,
                is_active=is_active,
                start_time=start_time,
                end_time=end_time
            )
            
            if result['success']:
                flash('公告更新成功！', 'success')
                return redirect(url_for('admin.announcements'))
            else:
                flash(f'更新失败：{result["message"]}', 'error')
        
        except Exception as e:
            flash(f'更新失败：{str(e)}', 'error')
    
    return render_template('admin/edit_announcement.html',
                         announcement=announcement,
                         audit_counts=get_audit_counts())

@admin_bp.route('/announcements/<int:announcement_id>/toggle_status', methods=['POST'])
@login_required
@admin_required
def toggle_announcement_status(announcement_id):
    """切换公告状态"""
    from app.services.announcement_service import AnnouncementService
    
    announcement_service = AnnouncementService()
    result = announcement_service.toggle_announcement_status(announcement_id)
    
    return jsonify(result)

@admin_bp.route('/announcements/<int:announcement_id>/toggle_pin', methods=['POST'])
@login_required
@admin_required
def toggle_announcement_pin(announcement_id):
    """切换公告置顶状态"""
    from app.services.announcement_service import AnnouncementService
    
    announcement_service = AnnouncementService()
    result = announcement_service.toggle_pin_status(announcement_id)
    
    return jsonify(result)

@admin_bp.route('/announcements/<int:announcement_id>/delete', methods=['POST'])
@login_required
@admin_required
def delete_announcement(announcement_id):
    """删除公告"""
    from app.services.announcement_service import AnnouncementService
    
    announcement_service = AnnouncementService()
    result = announcement_service.delete_announcement(announcement_id)
    
    return jsonify(result)

@admin_bp.route('/announcements/stats')
@login_required
@admin_required
def announcement_stats():
    """公告统计"""
    from app.services.announcement_service import AnnouncementService
    
    announcement_service = AnnouncementService()
    stats = announcement_service.get_announcement_stats()
    recent_announcements = announcement_service.get_recent_announcements(days=7, limit=10)
    
    return render_template('admin/announcement_stats.html',
                         stats=stats,
                         recent_announcements=recent_announcements,
                         audit_counts=get_audit_counts())

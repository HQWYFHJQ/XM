from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify, current_app
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.utils import secure_filename
from app import db, redis_client
from app.models import User, Item, Category, UserBehavior, Recommendation
from app.services.recommendation_service import RecommendationService
from app.services.user_service import UserService
from app.services.item_service import ItemService
from app.forms import UserItemEditForm
import os
import json
from datetime import datetime
from app.utils import get_beijing_utc_now

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    """首页"""
    # 获取热门商品
    popular_items = Item.query.filter_by(status='active', audit_status='approved').order_by(Item.view_count.desc()).limit(8).all()
    
    # 获取最新商品
    latest_items = Item.query.filter_by(status='active', audit_status='approved').order_by(Item.created_at.desc()).limit(8).all()
    
    # 获取父分类
    parent_categories = Category.query.filter_by(parent_id=None, is_active=True).order_by(Category.sort_order).all()
    
    # 如果用户已登录，获取推荐商品
    recommended_items = []
    if current_user.is_authenticated:
        recommendation_service = RecommendationService()
        recommended_items = recommendation_service.get_personalized_recommendations(current_user.id, limit=8)
    
    return render_template('main/index.html',
                         popular_items=popular_items,
                         latest_items=latest_items,
                         parent_categories=parent_categories,
                         recommended_items=recommended_items)


@main_bp.route('/login', methods=['GET', 'POST'])
def login():
    """用户登录"""
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        remember = bool(request.form.get('remember'))
        
        user = User.query.filter_by(username=username).first()
        
        if user and user.check_password(password) and user.is_active:
            login_user(user, remember=remember)
            user.last_login = get_beijing_utc_now()
            db.session.commit()
            
            next_page = request.args.get('next')
            if not next_page or not next_page.startswith('/'):
                next_page = url_for('main.index')
            
            flash('登录成功！', 'success')
            return redirect(next_page)
        else:
            flash('用户名或密码错误！', 'error')
    
    return render_template('main/login.html')

@main_bp.route('/register', methods=['GET', 'POST'])
def register():
    """用户注册"""
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    from app.forms import UserRegistrationForm
    from app.services.email_service import EmailService
    from app.services.captcha_service import CaptchaService
    
    form = UserRegistrationForm()
    
    if request.method == 'POST':
        if form.validate_on_submit():
            # 验证邮箱验证码
            email_service = EmailService()
            email_verify_result = email_service.verify_code(
                form.email.data, 
                form.verification_code.data, 
                'register'
            )
            
            if not email_verify_result['success']:
                flash(email_verify_result['message'], 'error')
                return render_template('main/register.html', form=form)
            
            # 验证行为验证码
            captcha_service = CaptchaService()
            if form.captcha_type.data == 'math':
                # 数学验证码
                if not form.math_answer.data:
                    flash('请输入数学验证码答案！', 'error')
                    return render_template('main/register.html', form=form)
                
                captcha_verify_result = captcha_service.verify_math_captcha(
                    form.captcha_id.data,
                    form.math_answer.data
                )
            elif form.captcha_type.data == 'slider':
                # 获取滑块验证数据
                user_x = request.form.get('user_x')
                user_y = request.form.get('user_y')
                user_angle = request.form.get('user_angle')
                
                if not all([user_x, user_y, user_angle]):
                    flash('请完成滑块验证！', 'error')
                    return render_template('main/register.html', form=form)
                
                captcha_verify_result = captcha_service.verify_slider_captcha(
                    form.captcha_id.data,
                    user_x,
                    user_y,
                    user_angle
                )
            else:
                # 图片验证码
                captcha_text = request.form.get('captcha_text')
                if not captcha_text:
                    flash('请输入图片验证码！', 'error')
                    return render_template('main/register.html', form=form)
                
                captcha_verify_result = captcha_service.verify_image_captcha(
                    form.captcha_id.data,
                    captcha_text
                )
            
            if not captcha_verify_result['success']:
                flash(captcha_verify_result['message'], 'error')
                return render_template('main/register.html', form=form)
            
            # 创建用户
            user = User(
                username=form.username.data,
                email=form.email.data,
                real_name=form.real_name.data,
                student_id=form.student_id.data,
                phone=form.phone.data,
                audit_status='pending',
                is_active=False  # 等待审核期间用户不能登录
            )
            user.set_password(form.password.data)
            
            db.session.add(user)
            db.session.commit()
            
            # 创建用户审核记录
            from app.services.audit_service import AuditService
            audit_service = AuditService()
            audit_service.create_user_audit(user.id)
            
            flash('注册成功！您的资料已提交审核，请等待管理员审核通过后即可登录使用。审核结果将通过邮件通知您。', 'success')
            return redirect(url_for('main.login'))
        else:
            # 表单验证失败，显示错误信息
            for field, errors in form.errors.items():
                for error in errors:
                    flash(f'{getattr(form, field).label.text}: {error}', 'error')
    
    # 生成初始验证码
    captcha_service = CaptchaService()
    captcha_result = captcha_service.generate_math_captcha()
    
    if captcha_result['success']:
        form.captcha_id.data = captcha_result['captcha_id']
        form.captcha_type.data = 'math'
    
    return render_template('main/register.html', form=form, captcha_data=captcha_result)

@main_bp.route('/logout')
@login_required
def logout():
    """用户登出"""
    logout_user()
    flash('已成功登出！', 'info')
    return redirect(url_for('main.index'))

@main_bp.route('/profile')
@login_required
def profile():
    """用户个人中心"""
    return render_template('main/profile.html')

@main_bp.route('/profile/edit', methods=['GET', 'POST'])
@login_required
def edit_profile():
    """编辑个人中心"""
    if request.method == 'POST':
        # 准备修改数据
        profile_data = {
            'real_name': request.form.get('real_name'),
            'phone': request.form.get('phone'),
            'bio': request.form.get('bio'),
            'student_id': request.form.get('student_id'),
            'interests': request.form.getlist('interests')
        }
        
        # 处理头像上传
        if 'avatar' in request.files:
            file = request.files['avatar']
            if file and file.filename:
                filename = secure_filename(file.filename)
                if filename:
                    # 生成唯一文件名
                    timestamp = get_beijing_utc_now().strftime('%Y%m%d_%H%M%S')
                    filename = f"{current_user.id}_{timestamp}_{filename}"
                    
                    # 保存新头像文件
                    upload_path = os.path.join(current_app.config['UPLOAD_FOLDER'], 'avatars', filename)
                    try:
                        file.save(upload_path)
                        
                        # 新头像保存成功后，删除旧头像
                        old_avatar = current_user.avatar
                        if old_avatar:
                            old_path = os.path.join(current_app.config['UPLOAD_FOLDER'], 'avatars', old_avatar)
                            if os.path.exists(old_path):
                                try:
                                    os.remove(old_path)
                                except OSError as e:
                                    current_app.logger.warning(f"删除旧头像失败: {e}")
                        
                        # 头像直接更新，不需要审核
                        current_user.avatar = filename
                        db.session.commit()
                        
                    except Exception as e:
                        current_app.logger.error(f"头像保存失败: {e}")
                        flash('头像上传失败，请重试！', 'error')
                        return redirect(url_for('main.edit_profile'))
        
        # 使用服务类更新资料（会创建审核记录）
        from app.services.user_service import UserService
        result = UserService.update_user_profile(current_user.id, **profile_data)
        
        if result:
            if current_user.is_admin:
                flash('资料修改已直接生效！', 'success')
            else:
                flash('资料修改申请已提交，等待管理员审核通过后生效！', 'info')
        else:
            flash('资料修改失败，请重试！', 'error')
        return redirect(url_for('main.profile'))
    
    return render_template('main/edit_profile.html')

@main_bp.route('/items')
def items():
    """商品列表页"""
    page = request.args.get('page', 1, type=int)
    category_id = request.args.get('category', type=int)
    parent_category_id = request.args.get('parent_category', type=int)
    search = request.args.get('search', '')
    sort_by = request.args.get('sort', 'latest')  # latest, price_asc, price_desc, popular
    
    query = Item.query.filter_by(status='active', audit_status='approved')
    
    # 分类筛选
    if category_id:
        query = query.filter_by(category_id=category_id)
    elif parent_category_id:
        # 如果选择了父分类但没有选择子分类，显示该父分类下的所有商品
        child_categories = Category.query.filter_by(parent_id=parent_category_id).all()
        child_ids = [child.id for child in child_categories]
        if child_ids:
            query = query.filter(Item.category_id.in_(child_ids))
    
    # 搜索
    if search:
        query = query.filter(Item.title.contains(search) | Item.description.contains(search))
    
    # 排序
    if sort_by == 'price_asc':
        query = query.order_by(Item.price.asc())
    elif sort_by == 'price_desc':
        query = query.order_by(Item.price.desc())
    elif sort_by == 'popular':
        query = query.order_by(Item.view_count.desc())
    else:  # latest
        query = query.order_by(Item.created_at.desc())
    
    items = query.paginate(
        page=page, per_page=12, error_out=False
    )
    
    # 获取分类数据
    parent_categories = Category.query.filter_by(parent_id=None, is_active=True).order_by(Category.sort_order).all()
    child_categories = []
    if parent_category_id:
        child_categories = Category.query.filter_by(parent_id=parent_category_id, is_active=True).order_by(Category.sort_order).all()
    
    # 构建分类数据用于JavaScript
    categories_data = []
    for parent in parent_categories:
        parent_data = {
            'id': parent.id,
            'name': parent.name,
            'children': []
        }
        children = Category.query.filter_by(parent_id=parent.id, is_active=True).order_by(Category.sort_order).all()
        for child in children:
            parent_data['children'].append({
                'id': child.id,
                'name': child.name
            })
        categories_data.append(parent_data)
    
    return render_template('main/items.html',
                         items=items,
                         parent_categories=parent_categories,
                         child_categories=child_categories,
                         categories_data=categories_data,
                         current_category=category_id,
                         current_parent_category=parent_category_id,
                         current_search=search,
                         current_sort=sort_by)

@main_bp.route('/item/<int:item_id>')
def item_detail(item_id):
    """商品详情页"""
    item = Item.query.get_or_404(item_id)
    
    # 增加浏览次数
    item.increment_view_count()
    
    # 记录用户行为
    if current_user.is_authenticated:
        behavior = UserBehavior(
            user_id=current_user.id,
            item_id=item.id,
            behavior_type='view',
            ip_address=request.remote_addr,
            user_agent=request.headers.get('User-Agent')
        )
        db.session.add(behavior)
        db.session.commit()
    
    # 获取相关推荐
    related_items = Item.query.filter(
        Item.category_id == item.category_id,
        Item.id != item.id,
        Item.status == 'active',
        Item.audit_status == 'approved'
    ).limit(4).all()
    
    return render_template('main/item_detail.html',
                         item=item,
                         related_items=related_items)

@main_bp.route('/item/create', methods=['GET', 'POST'])
@login_required
def create_item():
    """发布商品"""
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        price = request.form.get('price')
        category_id = request.form.get('category_id')
        condition = request.form.get('condition')
        location = request.form.get('location')
        contact_method = request.form.get('contact_method')
        contact_info = request.form.get('contact_info')
        tags = request.form.get('tags', '')
        
        # 验证数据
        if not all([title, description, price, category_id]):
            flash('请填写所有必填字段！', 'error')
            return render_template('main/create_item.html', categories=Category.query.all())
        
        try:
            price = float(price)
        except ValueError:
            flash('价格格式不正确！', 'error')
            return render_template('main/create_item.html', categories=Category.query.all())
        
        # 检查用户是否为管理员
        is_admin = current_user.role == 'admin'
        
        # 创建商品
        item = Item(
            title=title,
            description=description,
            price=price,
            category_id=int(category_id),
            seller_id=current_user.id,
            condition=condition,
            location=location,
            contact_method=contact_method,
            contact_info=contact_info,
            audit_status='approved' if is_admin else 'pending',
            status='active' if is_admin else 'inactive'  # 管理员发布直接激活
        )
        
        # 处理标签
        if tags:
            tag_list = [tag.strip() for tag in tags.split(',') if tag.strip()]
            item.set_tags_list(tag_list)
        
        # 处理图片上传
        images = []
        for i in range(1, 6):  # 最多5张图片
            file_key = f'image_{i}'
            if file_key in request.files:
                file = request.files[file_key]
                if file and file.filename:
                    filename = secure_filename(file.filename)
                    if filename:
                        timestamp = get_beijing_utc_now().strftime('%Y%m%d_%H%M%S')
                        filename = f"{current_user.id}_{timestamp}_{i}_{filename}"
                        
                        # 确保上传目录存在
                        upload_dir = os.path.join(current_app.config['UPLOAD_FOLDER'], 'items')
                        os.makedirs(upload_dir, exist_ok=True)
                        
                        upload_path = os.path.join(upload_dir, filename)
                        file.save(upload_path)
                        images.append(filename)
        
        if images:
            item.set_images_list(images)
        
        db.session.add(item)
        db.session.commit()
        
        # 只有非管理员才创建审核记录
        if not is_admin:
            from app.services.audit_service import AuditService
            audit_service = AuditService()
            audit_service.create_item_audit(item.id)
            
            flash('商品发布成功！您的商品已提交审核，请等待管理员审核通过后即可在平台上显示。审核结果将通过邮件通知您。', 'success')
        else:
            flash('商品发布成功！作为管理员，您的商品已直接上架。', 'success')
        
        return redirect(url_for('main.my_items'))
    
    # 获取一级分类和子分类数据
    parent_categories = Category.query.filter_by(parent_id=None, is_active=True).order_by(Category.sort_order).all()
    
    # 构建分类数据用于JavaScript
    categories_data = []
    for parent in parent_categories:
        parent_data = {
            'id': parent.id,
            'name': parent.name,
            'children': []
        }
        children = Category.query.filter_by(parent_id=parent.id, is_active=True).order_by(Category.sort_order).all()
        for child in children:
            parent_data['children'].append({
                'id': child.id,
                'name': child.name
            })
        categories_data.append(parent_data)
    
    return render_template('main/create_item.html', 
                         parent_categories=parent_categories,
                         categories_data=categories_data)

@main_bp.route('/my-items')
@login_required
def my_items():
    """我的商品"""
    page = request.args.get('page', 1, type=int)
    status = request.args.get('status', 'all')
    
    query = Item.query.filter_by(seller_id=current_user.id)
    
    if status != 'all':
        query = query.filter_by(status=status)
    
    items = query.order_by(Item.created_at.desc()).paginate(
        page=page, per_page=10, error_out=False
    )
    
    return render_template('main/my_items.html', items=items, current_status=status)

@main_bp.route('/my-items/<int:item_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_my_item(item_id):
    """编辑我的商品"""
    item = Item.query.get_or_404(item_id)
    
    # 检查权限：只有商品所有者可以编辑
    if item.seller_id != current_user.id:
        flash('您没有权限编辑此商品！', 'error')
        return redirect(url_for('main.my_items'))
    
    form = UserItemEditForm(obj=item)
    
    if form.validate_on_submit():
        try:
            # 准备修改数据
            item_data = {
                'title': form.title.data,
                'description': form.description.data,
                'price': float(form.price.data),
                'original_price': float(form.original_price.data) if form.original_price.data else None,
                'condition': form.condition.data,
                'category_id': form.category_id.data,
                'location': form.location.data,
                'contact_method': form.contact_method.data,
                'contact_info': form.contact_info.data,
                'status': form.status.data
            }
            
            # 处理图片上传
            if form.images.data and any(file.filename for file in form.images.data):
                new_images = []
                for i, file in enumerate(form.images.data):
                    if file and file.filename:
                        filename = secure_filename(file.filename)
                        if filename:
                            timestamp = get_beijing_utc_now().strftime('%Y%m%d_%H%M%S')
                            filename = f"{current_user.id}_{timestamp}_{i+1}_{filename}"
                            
                            # 确保上传目录存在
                            upload_dir = os.path.join(current_app.config['UPLOAD_FOLDER'], 'items')
                            os.makedirs(upload_dir, exist_ok=True)
                            
                            upload_path = os.path.join(upload_dir, filename)
                            file.save(upload_path)
                            new_images.append(filename)
                
                if new_images:
                    # 图片直接更新，不需要审核
                    item.set_images_list(new_images)
                    
                    # 删除旧图片文件
                    old_images = item.get_images_list()
                    for old_image in old_images:
                        old_path = os.path.join(current_app.config['UPLOAD_FOLDER'], 'items', old_image)
                        if os.path.exists(old_path):
                            try:
                                os.remove(old_path)
                            except Exception as e:
                                print(f"删除旧图片失败: {old_image}, 错误: {e}")
            
            # 使用服务类更新商品（会创建审核记录）
            from app.services.item_service import ItemService
            result = ItemService.update_item(item_id, **item_data)
            
            if result:
                if current_user.is_admin:
                    flash('商品信息修改已直接生效！', 'success')
                else:
                    flash('商品信息修改申请已提交，等待管理员审核通过后生效！', 'info')
            else:
                flash('商品信息修改失败，请重试！', 'error')
            
            return redirect(url_for('main.my_items'))
            
        except Exception as e:
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
    
    return render_template('main/edit_item.html', form=form, item=item)

@main_bp.route('/recommendations')
@login_required
def recommendations():
    """推荐页面"""
    recommendation_service = RecommendationService()
    recommendations = recommendation_service.get_personalized_recommendations(current_user.id, limit=20)
    
    return render_template('main/recommendations.html', recommendations=recommendations)

@main_bp.route('/api/like/<int:item_id>', methods=['POST'])
@login_required
def like_item(item_id):
    """点赞商品"""
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
        'is_liked': is_liked,
        'like_count': item.like_count
    })

@main_bp.route('/api/contact/<int:item_id>', methods=['POST'])
@login_required
def contact_seller(item_id):
    """联系卖家"""
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
    
    # 创建或获取商品咨询对话
    from app.services.message_service import MessageService
    conversation = MessageService.get_item_chat(item.seller_id, current_user.id, item_id)
    if not conversation:
        conversation = MessageService.create_item_chat(item.seller_id, current_user.id, item_id)
    
    db.session.commit()
    
    return jsonify({
        'success': True,
        'message': '已为您创建聊天对话',
        'conversation_id': conversation.id,
        'contact_info': item.contact_info,
        'contact_method': item.contact_method
    })

@main_bp.route('/service-agreement')
def service_agreement():
    """服务协议页面"""
    return render_template('main/service_agreement.html')

@main_bp.route('/privacy-policy')
def privacy_policy():
    """隐私声明页面"""
    return render_template('main/privacy_policy.html')

@main_bp.route('/account-agreement')
def account_agreement():
    """账号协议页面"""
    return render_template('main/account_agreement.html')

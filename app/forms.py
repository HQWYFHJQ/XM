from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import MultipleFileField
from wtforms import StringField, TextAreaField, DecimalField, SelectField, SubmitField, HiddenField, PasswordField, EmailField, BooleanField
from wtforms.validators import DataRequired, Length, NumberRange, Optional, ValidationError, EqualTo
import re
from app.models import Category, User

def validate_price_not_empty(form, field):
    """自定义价格验证器，允许0作为有效价格"""
    if field.data is None:
        raise ValidationError('价格不能为空')

def validate_original_price_range(form, field):
    """自定义原价验证器，处理可选字段的范围验证"""
    if field.data is not None:
        # 对于DecimalField，field.data已经是Decimal类型
        if field.data < 0 or field.data > 9999.99:
            raise ValidationError('原价必须在0-9999.99之间')

def validate_email_format(form, field):
    """自定义邮箱格式验证器"""
    if field.data:
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_pattern, field.data):
            raise ValidationError('请输入有效的邮箱地址')

class ItemEditForm(FlaskForm):
    """商品编辑表单"""
    title = StringField('商品名称', validators=[
        DataRequired(message='商品名称不能为空'),
        Length(min=1, max=200, message='商品名称长度必须在1-200个字符之间')
    ])
    
    description = TextAreaField('商品描述', validators=[
        DataRequired(message='商品描述不能为空'),
        Length(min=1, max=2000, message='商品描述长度必须在1-2000个字符之间')
    ])
    
    price = DecimalField('价格', validators=[
        validate_price_not_empty,
        NumberRange(min=0, max=9999.99, message='价格必须在0-9999.99之间')
    ], places=2)
    
    original_price = DecimalField('原价', validators=[
        validate_original_price_range
    ], places=2)
    
    condition = SelectField('成色', choices=[
        ('new', '全新'),
        ('like_new', '几乎全新'),
        ('good', '良好'),
        ('fair', '一般'),
        ('poor', '较差')
    ], validators=[DataRequired(message='请选择商品成色')])
    
    category_id = SelectField('分类', coerce=int, validators=[
        DataRequired(message='请选择商品分类')
    ])
    
    location = StringField('位置', validators=[
        Optional(),
        Length(max=200, message='位置信息不能超过200个字符')
    ])
    
    contact_method = SelectField('联系方式', choices=[
        ('message', '站内消息'),
        ('phone', '电话'),
        ('wechat', '微信'),
        ('qq', 'QQ')
    ], validators=[DataRequired(message='请选择联系方式')])
    
    contact_info = StringField('联系信息', validators=[
        Optional(),
        Length(max=200, message='联系信息不能超过200个字符')
    ])
    
    status = SelectField('状态', choices=[
        ('active', '在售'),
        ('inactive', '下架'),
        ('sold', '已售出'),
        ('deleted', '已删除')
    ], validators=[DataRequired(message='请选择商品状态')])
    
    # 图片上传字段
    images = MultipleFileField('商品图片', validators=[
        FileAllowed(['jpg', 'jpeg', 'png', 'gif', 'webp'], '只允许上传图片文件！')
    ])
    
    submit = SubmitField('保存修改')
    
    def __init__(self, *args, **kwargs):
        super(ItemEditForm, self).__init__(*args, **kwargs)
        # 动态加载分类选项
        try:
            self.category_id.choices = [(0, '请选择分类')] + [
                (cat.id, cat.name) for cat in Category.query.filter_by(is_active=True).order_by(Category.name).all()
            ]
        except:
            # 如果没有数据库上下文，使用默认选项
            self.category_id.choices = [(0, '请选择分类')]

class UserItemEditForm(FlaskForm):
    """用户商品编辑表单"""
    title = StringField('商品名称', validators=[
        DataRequired(message='商品名称不能为空'),
        Length(min=1, max=200, message='商品名称长度必须在1-200个字符之间')
    ])
    
    description = TextAreaField('商品描述', validators=[
        DataRequired(message='商品描述不能为空'),
        Length(min=1, max=2000, message='商品描述长度必须在1-2000个字符之间')
    ])
    
    price = DecimalField('价格', validators=[
        validate_price_not_empty,
        NumberRange(min=0, max=9999.99, message='价格必须在0-9999.99之间')
    ], places=2)
    
    original_price = DecimalField('原价', validators=[
        validate_original_price_range
    ], places=2)
    
    condition = SelectField('成色', choices=[
        ('new', '全新'),
        ('like_new', '几乎全新'),
        ('good', '良好'),
        ('fair', '一般'),
        ('poor', '较差')
    ], validators=[DataRequired(message='请选择商品成色')])
    
    category_id = SelectField('分类', coerce=int, validators=[
        DataRequired(message='请选择商品分类')
    ])
    
    location = StringField('位置', validators=[
        Optional(),
        Length(max=200, message='位置信息不能超过200个字符')
    ])
    
    contact_method = SelectField('联系方式', choices=[
        ('message', '站内消息'),
        ('phone', '电话'),
        ('wechat', '微信'),
        ('qq', 'QQ')
    ], validators=[DataRequired(message='请选择联系方式')])
    
    contact_info = StringField('联系信息', validators=[
        Optional(),
        Length(max=200, message='联系信息不能超过200个字符')
    ])
    
    status = SelectField('状态', choices=[
        ('active', '在售'),
        ('inactive', '下架'),
        ('sold', '已售出')
    ], validators=[DataRequired(message='请选择商品状态')])
    
    # 图片上传字段
    images = MultipleFileField('商品图片', validators=[
        FileAllowed(['jpg', 'jpeg', 'png', 'gif', 'webp'], '只允许上传图片文件！')
    ])
    
    submit = SubmitField('保存修改')
    
    def __init__(self, *args, **kwargs):
        super(UserItemEditForm, self).__init__(*args, **kwargs)
        # 动态加载分类选项
        try:
            self.category_id.choices = [(0, '请选择分类')] + [
                (cat.id, cat.name) for cat in Category.query.filter_by(is_active=True).order_by(Category.name).all()
            ]
        except:
            # 如果没有数据库上下文，使用默认选项
            self.category_id.choices = [(0, '请选择分类')]

class UserRegistrationForm(FlaskForm):
    """用户注册表单"""
    username = StringField('用户名', validators=[
        DataRequired(message='用户名不能为空'),
        Length(min=6, max=12, message='用户名长度必须在6-12个字符之间')
    ])
    
    email = EmailField('邮箱', validators=[
        DataRequired(message='邮箱不能为空'),
        validate_email_format
    ])
    
    password = PasswordField('密码', validators=[
        DataRequired(message='密码不能为空'),
        Length(min=8, max=16, message='密码长度必须在8-16个字符之间')
    ])
    
    confirm_password = PasswordField('确认密码', validators=[
        DataRequired(message='确认密码不能为空'),
        EqualTo('password', message='两次输入的密码不一致')
    ])
    
    real_name = StringField('真实姓名', validators=[
        Optional(),
        Length(max=50, message='真实姓名不能超过50个字符')
    ])
    
    student_id = StringField('学号', validators=[
        Optional(),
        Length(min=6, max=18, message='学号长度必须在6-18个字符之间')
    ])
    
    phone = StringField('手机号', validators=[
        Optional(),
        Length(max=20, message='手机号不能超过20个字符')
    ])
    
    verification_code = StringField('邮箱验证码', validators=[
        DataRequired(message='请输入邮箱验证码'),
        Length(min=6, max=6, message='验证码必须是6位数字')
    ])
    
    captcha_id = HiddenField('验证码ID')
    captcha_type = HiddenField('验证码类型', default='math')
    math_answer = StringField('数学验证码答案', validators=[
        DataRequired(message='请输入数学验证码答案')
    ])
    
    agree_terms = BooleanField('同意协议', validators=[
        DataRequired(message='请阅读并同意服务协议、隐私声明和账号协议')
    ])
    
    submit = SubmitField('注册')
    
    def validate_username(self, field):
        """验证用户名是否已存在"""
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('用户名已存在')
    
    def validate_password(self, field):
        """验证密码复杂度"""
        password = field.data
        if len(password) < 8 or len(password) > 16:
            raise ValidationError('密码长度必须在8-16个字符之间')
        
        # 检查是否包含至少两种字符类型
        has_upper = any(c.isupper() for c in password)
        has_lower = any(c.islower() for c in password)
        has_digit = any(c.isdigit() for c in password)
        has_special = any(c in '@#&' for c in password)
        
        char_types = sum([has_upper, has_lower, has_digit, has_special])
        if char_types < 2:
            raise ValidationError('密码必须包含大写字母、小写字母、数字或@#&符号中的至少两种')
    
    def validate_email(self, field):
        """验证邮箱是否已被注册"""
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('邮箱已被注册')
    
    def validate_verification_code(self, field):
        """验证邮箱验证码格式"""
        if not field.data.isdigit() or len(field.data) != 6:
            raise ValidationError('验证码必须是6位数字')
    

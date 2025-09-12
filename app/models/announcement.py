from datetime import datetime
from app import db
import markdown
import bleach

class Announcement(db.Model):
    """公告模型"""
    __tablename__ = 'announcements'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False, comment='公告标题')
    content = db.Column(db.Text, nullable=False, comment='公告内容')
    type = db.Column(db.Enum('system', 'maintenance', 'notice', 'warning'), 
                    default='system', comment='公告类型')
    priority = db.Column(db.Enum('low', 'normal', 'high', 'urgent'), 
                        default='normal', comment='优先级')
    is_active = db.Column(db.Boolean, default=True, comment='是否启用')
    is_pinned = db.Column(db.Boolean, default=False, comment='是否置顶')
    start_time = db.Column(db.DateTime, nullable=True, comment='开始显示时间')
    end_time = db.Column(db.DateTime, nullable=True, comment='结束显示时间')
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, comment='创建者ID')
    created_at = db.Column(db.DateTime, default=datetime.utcnow, comment='创建时间')
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, comment='更新时间')
    
    # 关系
    creator = db.relationship('User', backref='created_announcements', lazy='select')
    
    def to_dict(self):
        """转换为字典"""
        return {
            'id': self.id,
            'title': self.title,
            'content': self.content,
            'type': self.type,
            'priority': self.priority,
            'is_active': self.is_active,
            'is_pinned': self.is_pinned,
            'start_time': self.start_time.isoformat() if self.start_time else None,
            'end_time': self.end_time.isoformat() if self.end_time else None,
            'created_by': self.created_by,
            'creator_name': self.creator.username if self.creator else '未知',
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    @classmethod
    def get_active_announcements(cls, limit=None):
        """获取当前有效的公告"""
        now = datetime.utcnow()
        query = cls.query.filter_by(is_active=True).filter(
            (cls.start_time.is_(None) | (cls.start_time <= now)),
            (cls.end_time.is_(None) | (cls.end_time >= now))
        ).order_by(cls.is_pinned.desc(), cls.priority.desc(), cls.created_at.desc())
        
        if limit:
            return query.limit(limit).all()
        return query.all()
    
    @classmethod
    def get_active_announcements_for_users(cls, limit=None):
        """获取用户可见的当前有效公告"""
        return cls.get_active_announcements(limit=limit)
    
    @classmethod
    def get_pinned_announcements(cls):
        """获取置顶公告"""
        now = datetime.utcnow()
        return cls.query.filter_by(is_active=True, is_pinned=True).filter(
            (cls.start_time.is_(None) | (cls.start_time <= now)),
            (cls.end_time.is_(None) | (cls.end_time >= now))
        ).order_by(cls.priority.desc(), cls.created_at.desc()).all()
    
    @classmethod
    def get_announcement_history(cls, limit=10):
        """获取公告历史记录"""
        return cls.query.order_by(cls.created_at.desc()).limit(limit).all()
    
    def is_currently_active(self):
        """检查公告是否当前有效"""
        if not self.is_active:
            return False
        
        now = datetime.utcnow()
        
        # 检查开始时间
        if self.start_time and self.start_time > now:
            return False
        
        # 检查结束时间
        if self.end_time and self.end_time < now:
            return False
        
        return True
    
    def get_priority_class(self):
        """获取优先级对应的CSS类"""
        priority_classes = {
            'low': 'text-muted',
            'normal': 'text-primary',
            'high': 'text-warning',
            'urgent': 'text-danger'
        }
        return priority_classes.get(self.priority, 'text-primary')
    
    def get_type_icon(self):
        """获取类型对应的图标"""
        type_icons = {
            'system': 'fas fa-cog',
            'maintenance': 'fas fa-tools',
            'notice': 'fas fa-bell',
            'warning': 'fas fa-exclamation-triangle'
        }
        return type_icons.get(self.type, 'fas fa-info-circle')
    
    def render_content(self):
        """渲染Markdown内容为HTML"""
        if not self.content:
            return ""
        
        # 配置Markdown扩展
        md = markdown.Markdown(
            extensions=[
                'markdown.extensions.extra',
                'markdown.extensions.codehilite',
                'markdown.extensions.toc',
                'markdown.extensions.tables',
                'markdown.extensions.fenced_code',
                'markdown.extensions.nl2br'
            ],
            extension_configs={
                'markdown.extensions.codehilite': {
                    'css_class': 'highlight'
                }
            }
        )
        
        # 渲染Markdown
        html = md.convert(self.content)
        
        # 清理HTML，只允许安全的标签
        allowed_tags = [
            'p', 'br', 'strong', 'em', 'u', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6',
            'ul', 'ol', 'li', 'blockquote', 'code', 'pre', 'a', 'img',
            'table', 'thead', 'tbody', 'tr', 'th', 'td', 'div', 'span'
        ]
        allowed_attributes = {
            'a': ['href', 'title', 'target'],
            'img': ['src', 'alt', 'title', 'width', 'height'],
            'table': ['class'],
            'th': ['class'],
            'td': ['class'],
            'div': ['class'],
            'span': ['class'],
            'pre': ['class'],
            'code': ['class']
        }
        
        cleaned_html = bleach.clean(html, tags=allowed_tags, attributes=allowed_attributes)
        return cleaned_html
    
    def get_content_preview(self, max_length=100):
        """获取内容预览（纯文本）"""
        if not self.content:
            return ""
        
        # 移除Markdown标记
        import re
        # 移除代码块
        content = re.sub(r'```.*?```', '', self.content, flags=re.DOTALL)
        # 移除行内代码
        content = re.sub(r'`.*?`', '', content)
        # 移除链接
        content = re.sub(r'\[.*?\]\(.*?\)', '', content)
        # 移除图片
        content = re.sub(r'!\[.*?\]\(.*?\)', '', content)
        # 移除标题标记
        content = re.sub(r'^#+\s*', '', content, flags=re.MULTILINE)
        # 移除粗体和斜体标记
        content = re.sub(r'\*\*.*?\*\*', '', content)
        content = re.sub(r'\*.*?\*', '', content)
        # 移除列表标记
        content = re.sub(r'^[\s]*[-*+]\s*', '', content, flags=re.MULTILINE)
        content = re.sub(r'^[\s]*\d+\.\s*', '', content, flags=re.MULTILINE)
        
        # 清理多余空白
        content = re.sub(r'\s+', ' ', content).strip()
        
        if len(content) > max_length:
            return content[:max_length] + "..."
        return content
    
    def __repr__(self):
        return f'<Announcement {self.title}>'

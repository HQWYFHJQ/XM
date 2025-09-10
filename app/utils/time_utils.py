"""
时间工具函数
"""
from datetime import datetime, timezone, timedelta
from config import BEIJING_TZ

def utc_to_beijing(utc_dt):
    """
    将UTC时间转换为北京时间
    
    Args:
        utc_dt: UTC时间对象
        
    Returns:
        北京时间对象
    """
    if utc_dt is None:
        return None
    
    # 如果已经是带时区的时间对象，先转换为UTC
    if utc_dt.tzinfo is not None:
        utc_dt = utc_dt.astimezone(timezone.utc).replace(tzinfo=None)
    
    # 转换为北京时间
    beijing_dt = utc_dt.replace(tzinfo=timezone.utc).astimezone(BEIJING_TZ)
    return beijing_dt

def format_beijing_time(dt, format_str='%Y-%m-%d %H:%M:%S'):
    """
    格式化时间为北京时间字符串
    
    Args:
        dt: 时间对象
        format_str: 格式化字符串
        
    Returns:
        格式化的北京时间字符串
    """
    if dt is None:
        return '未知'
    
    beijing_dt = utc_to_beijing(dt)
    return beijing_dt.strftime(format_str)

def get_beijing_now():
    """
    获取当前北京时间
    
    Returns:
        当前北京时间对象
    """
    return datetime.now(BEIJING_TZ)

def get_beijing_utc_now():
    """
    获取当前北京时间对应的UTC时间（用于数据库存储）
    
    Returns:
        当前北京时间对应的UTC时间对象
    """
    beijing_now = get_beijing_now()
    return beijing_now.astimezone(timezone.utc).replace(tzinfo=None)

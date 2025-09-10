import json
import redis
from typing import Any, Optional, Union
from datetime import datetime, timedelta
from flask import current_app
import logging

logger = logging.getLogger(__name__)

class CacheService:
    def __init__(self):
        self.redis_client = None
        self._memory_cache = {}
        self._redis_initialized = False
    
    def _init_redis(self):
        """初始化Redis连接"""
        if self._redis_initialized:
            return
            
        try:
            # 检查是否有应用上下文
            if hasattr(current_app, 'config'):
                host = current_app.config.get('REDIS_HOST', 'localhost')
                port = current_app.config.get('REDIS_PORT', 6379)
                db = current_app.config.get('REDIS_DB', 0)
            else:
                # 没有应用上下文时使用默认配置
                host = 'localhost'
                port = 6379
                db = 0
                
            self.redis_client = redis.Redis(
                host=host,
                port=port,
                db=db,
                decode_responses=True
            )
            # 测试连接
            self.redis_client.ping()
            logger.info("Redis连接成功")
            self._redis_initialized = True
        except Exception as e:
            logger.warning(f"Redis连接失败，将使用内存缓存: {e}")
            self.redis_client = None
            self._redis_initialized = True
    
    def get(self, key: str) -> Optional[Any]:
        """获取缓存数据"""
        try:
            self._init_redis()
            if self.redis_client:
                data = self.redis_client.get(key)
                if data:
                    return json.loads(data)
            else:
                # 内存缓存
                cache_data = self._memory_cache.get(key)
                if cache_data and cache_data['expires'] > datetime.utcnow():
                    return cache_data['data']
                elif cache_data:
                    # 过期数据，删除
                    del self._memory_cache[key]
            return None
        except Exception as e:
            logger.error(f"获取缓存失败: {e}")
            return None
    
    def set(self, key: str, value: Any, timeout: int = 3600) -> bool:
        """设置缓存数据"""
        try:
            self._init_redis()
            if self.redis_client:
                return self.redis_client.setex(key, timeout, json.dumps(value, default=str))
            else:
                # 内存缓存
                self._memory_cache[key] = {
                    'data': value,
                    'expires': datetime.utcnow() + timedelta(seconds=timeout)
                }
                return True
        except Exception as e:
            logger.error(f"设置缓存失败: {e}")
            return False
    
    def delete(self, key: str) -> bool:
        """删除缓存数据"""
        try:
            self._init_redis()
            if self.redis_client:
                return bool(self.redis_client.delete(key))
            else:
                # 内存缓存
                if key in self._memory_cache:
                    del self._memory_cache[key]
                    return True
                return False
        except Exception as e:
            logger.error(f"删除缓存失败: {e}")
            return False
    
    def exists(self, key: str) -> bool:
        """检查缓存是否存在"""
        try:
            self._init_redis()
            if self.redis_client:
                return bool(self.redis_client.exists(key))
            else:
                cache_data = self._memory_cache.get(key)
                if cache_data and cache_data['expires'] > datetime.utcnow():
                    return True
                elif cache_data:
                    del self._memory_cache[key]
                return False
        except Exception as e:
            logger.error(f"检查缓存存在性失败: {e}")
            return False
    
    def get_or_set(self, key: str, func, timeout: int = 3600) -> Any:
        """获取缓存，如果不存在则执行函数并缓存结果"""
        cached_data = self.get(key)
        if cached_data is not None:
            return cached_data
        
        # 缓存不存在，执行函数
        try:
            data = func()
            self.set(key, data, timeout)
            return data
        except Exception as e:
            logger.error(f"执行缓存函数失败: {e}")
            return None
    
    def clear_pattern(self, pattern: str) -> int:
        """清除匹配模式的所有缓存"""
        try:
            self._init_redis()
            if self.redis_client:
                keys = self.redis_client.keys(pattern)
                if keys:
                    return self.redis_client.delete(*keys)
            else:
                # 内存缓存
                keys_to_delete = [key for key in self._memory_cache.keys() if pattern.replace('*', '') in key]
                for key in keys_to_delete:
                    del self._memory_cache[key]
                return len(keys_to_delete)
            return 0
        except Exception as e:
            logger.error(f"清除模式缓存失败: {e}")
            return 0

# 全局缓存服务实例
cache_service = CacheService()

import json
import redis
from typing import Optional, Dict, Any
from src.config import REDIS_URL, CACHE_TTL


class CacheManager:
    def __init__(self):
        self.redis_client = redis.from_url(REDIS_URL)
        self.default_ttl = CACHE_TTL

    def get(self, key: str) -> Optional[Dict[str, Any]]:
        """从缓存获取数据"""
        try:
            cached_data = self.redis_client.get(key)
            if cached_data:
                return json.loads(cached_data)
        except Exception:
            pass
        return None

    def set(self, key: str, data: Dict[str, Any], ttl: Optional[int] = None) -> bool:
        """设置缓存数据"""
        try:
            ttl = ttl or self.default_ttl
            serialized_data = json.dumps(data)
            self.redis_client.setex(key, ttl, serialized_data)
            return True
        except Exception:
            return False

    def delete(self, key: str) -> bool:
        """删除缓存数据"""
        try:
            self.redis_client.delete(key)
            return True
        except Exception:
            return False


# 创建全局缓存实例
cache_manager = CacheManager()
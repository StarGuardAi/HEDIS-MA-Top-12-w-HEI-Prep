"""
Caching Infrastructure

Centralized caching with TTL support and invalidation.
"""

from typing import Optional, Any, Callable
from functools import wraps
import hashlib
import json
from datetime import datetime, timedelta

from core.config import get_settings
from core.logging import get_logger

logger = get_logger(__name__)


class CacheManager:
    """Cache manager with TTL support"""
    
    def __init__(self):
        self.settings = get_settings()
        self.cache: Dict[str, tuple[Any, datetime]] = {}
        self.enabled = self.settings.cache.enabled
        self.default_ttl = self.settings.cache.ttl
        self.max_size = self.settings.cache.max_size
    
    def _make_key(self, prefix: str, *args, **kwargs) -> str:
        """Generate cache key from arguments"""
        key_data = {
            'prefix': prefix,
            'args': args,
            'kwargs': kwargs
        }
        key_string = json.dumps(key_data, sort_keys=True, default=str)
        return hashlib.md5(key_string.encode()).hexdigest()
    
    def get(self, key: str) -> Optional[Any]:
        """Get value from cache"""
        if not self.enabled:
            return None
        
        if key not in self.cache:
            return None
        
        value, expiry = self.cache[key]
        
        if datetime.now() > expiry:
            del self.cache[key]
            return None
        
        return value
    
    def set(self, key: str, value: Any, ttl: Optional[int] = None) -> None:
        """Set value in cache"""
        if not self.enabled:
            return
        
        # Enforce max size
        if len(self.cache) >= self.max_size:
            # Remove oldest entry (simple FIFO)
            oldest_key = next(iter(self.cache))
            del self.cache[oldest_key]
        
        ttl = ttl or self.default_ttl
        expiry = datetime.now() + timedelta(seconds=ttl)
        self.cache[key] = (value, expiry)
    
    def delete(self, key: str) -> None:
        """Delete key from cache"""
        if key in self.cache:
            del self.cache[key]
    
    def clear(self) -> None:
        """Clear all cache"""
        self.cache.clear()
    
    def invalidate_pattern(self, pattern: str) -> None:
        """Invalidate all keys matching pattern"""
        keys_to_delete = [k for k in self.cache.keys() if pattern in k]
        for key in keys_to_delete:
            self.delete(key)


# Singleton instance
_cache_manager: Optional[CacheManager] = None


def get_cache_manager() -> CacheManager:
    """Get cache manager instance (singleton)"""
    global _cache_manager
    if _cache_manager is None:
        _cache_manager = CacheManager()
    return _cache_manager


def cached(prefix: str = "default", ttl: Optional[int] = None):
    """
    Decorator for caching function results
    
    Args:
        prefix: Cache key prefix
        ttl: Time to live in seconds
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            cache = get_cache_manager()
            cache_key = cache._make_key(prefix, *args, **kwargs)
            
            # Try to get from cache
            cached_value = cache.get(cache_key)
            if cached_value is not None:
                logger.debug(f"Cache hit for {func.__name__}")
                return cached_value
            
            # Execute function and cache result
            logger.debug(f"Cache miss for {func.__name__}")
            result = func(*args, **kwargs)
            cache.set(cache_key, result, ttl)
            
            return result
        
        return wrapper
    return decorator


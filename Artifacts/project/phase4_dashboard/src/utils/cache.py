"""
Caching utilities and strategies
"""
import streamlit as st
from functools import wraps
import logging

logger = logging.getLogger(__name__)


def log_cache_stats(func):
    """Decorator to log cache hit/miss statistics"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        # Check if function is cached
        if hasattr(func, 'cache_info'):
            stats = func.cache_info()
            logger.info(f"{func.__name__} cache - Hits: {stats.hits}, Misses: {stats.misses}")
        return func(*args, **kwargs)
    return wrapper


def clear_all_caches():
    """Clear all Streamlit caches"""
    st.cache_data.clear()
    st.cache_resource.clear()
    logger.info("All caches cleared")


def get_cache_stats() -> dict:
    """Get statistics about cache usage"""
    # TODO: Implement cache statistics collection
    # This would require tracking cache decorators
    return {
        'cache_data_cleared': False,
        'cache_resource_cleared': False
    }


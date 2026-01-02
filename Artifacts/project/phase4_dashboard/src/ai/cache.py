"""
AI response caching utilities

Manages caching of expensive AI API calls to reduce costs and improve performance.
"""
import streamlit as st
import logging
from typing import Any, Optional
from functools import wraps

logger = logging.getLogger(__name__)


def cache_ai_response(ttl: int = 3600, key_prefix: str = "ai_"):
    """
    Decorator to cache AI API responses
    
    Args:
        ttl: Time to live in seconds (default: 1 hour)
        key_prefix: Prefix for cache key
    
    Returns:
        Decorated function with caching
    """
    def decorator(func):
        @wraps(func)
        @st.cache_data(ttl=ttl)
        def wrapper(*args, **kwargs):
            # Create cache key from function name and arguments
            cache_key = f"{key_prefix}{func.__name__}_{hash(str(args) + str(kwargs))}"
            logger.debug(f"Caching AI response with key: {cache_key}")
            return func(*args, **kwargs)
        return wrapper
    return decorator


def clear_ai_cache() -> None:
    """
    Clear all AI-related caches
    
    This clears all Streamlit caches, which includes AI responses.
    """
    st.cache_data.clear()
    logger.info("AI cache cleared")


def get_cache_stats() -> dict:
    """
    Get statistics about cache usage
    
    Returns:
        Dictionary with cache statistics
    """
    # Streamlit doesn't expose cache stats directly
    # This is a placeholder for future implementation
    return {
        'cache_enabled': True,
        'note': 'Streamlit cache stats not directly accessible'
    }


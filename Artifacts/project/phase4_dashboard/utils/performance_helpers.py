"""
Performance helper functions and decorators
For optimizing Streamlit app performance
"""
import streamlit as st
import functools
import time
import pandas as pd
from typing import Callable, Any
from utils.performance_monitor import get_performance_monitor


def cached_with_tracking(ttl: int = 3600, max_entries: int = 128):
    """
    Enhanced cache decorator with performance tracking.
    
    Usage:
        @cached_with_tracking(ttl=3600)
        def expensive_function(param):
            ...
    """
    def decorator(func: Callable) -> Callable:
        monitor = get_performance_monitor()
        
        @st.cache_data(ttl=ttl, max_entries=max_entries)
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            start_time = time.perf_counter()
            
            # Try to get from cache first
            cache_key = f"{func.__name__}_{args}_{kwargs}"
            
            # Check cache (simplified - Streamlit handles actual caching)
            result = func(*args, **kwargs)
            
            elapsed = time.perf_counter() - start_time
            
            # Track as cache hit if very fast (likely cached)
            if elapsed < 0.01:  # Very fast = likely cached
                monitor.track_cache(cache_key, hit=True)
            else:
                monitor.track_cache(cache_key, hit=False)
                monitor.track_data_fetch(elapsed)
            
            return result
        
        return wrapper
    return decorator


def track_render_time(component_name: str = None):
    """
    Decorator to track render time of Streamlit components.
    
    Usage:
        @track_render_time("chart")
        def render_chart():
            st.plotly_chart(...)
    """
    def decorator(func: Callable) -> Callable:
        name = component_name or func.__name__
        monitor = get_performance_monitor()
        
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            start_time = time.perf_counter()
            try:
                result = func(*args, **kwargs)
                return result
            finally:
                elapsed = time.perf_counter() - start_time
                monitor.track_render(elapsed)
        
        return wrapper
    return decorator


def track_filter_time():
    """
    Decorator to track filter application time.
    
    Usage:
        @track_filter_time()
        def apply_filters(data, filters):
            ...
    """
    monitor = get_performance_monitor()
    
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            start_time = time.perf_counter()
            try:
                result = func(*args, **kwargs)
                return result
            finally:
                elapsed = time.perf_counter() - start_time
                monitor.track_filter(elapsed)
        
        return wrapper
    return decorator


def track_export_time():
    """
    Decorator to track export generation time.
    
    Usage:
        @track_export_time()
        def export_to_csv(data):
            ...
    """
    monitor = get_performance_monitor()
    
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            start_time = time.perf_counter()
            try:
                result = func(*args, **kwargs)
                return result
            finally:
                elapsed = time.perf_counter() - start_time
                monitor.track_export(elapsed)
        
        return wrapper
    return decorator


def use_fragment(func: Callable) -> Callable:
    """
    Wrapper to use Streamlit fragments for granular updates.
    Reduces re-rendering of entire page.
    
    Usage:
        @use_fragment
        def update_chart():
            st.plotly_chart(...)
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # Use experimental_fragment if available
        if hasattr(st, 'experimental_fragment'):
            with st.experimental_fragment():
                return func(*args, **kwargs)
        else:
            # Fallback to regular execution
            return func(*args, **kwargs)
    
    return wrapper


def optimize_dataframe(df, optimize_types: bool = True, optimize_memory: bool = True):
    """
    Optimize pandas DataFrame for better performance.
    
    Args:
        df: DataFrame to optimize
        optimize_types: Convert to optimal dtypes
        optimize_memory: Reduce memory usage
    
    Returns:
        Optimized DataFrame
    """
    if df.empty:
        return df
    
    df = df.copy()
    
    if optimize_types:
        # Convert object columns to category if beneficial
        for col in df.select_dtypes(include=['object']).columns:
            num_unique = df[col].nunique()
            num_rows = len(df)
            if num_unique / num_rows < 0.5:  # Less than 50% unique values
                df[col] = df[col].astype('category')
    
    if optimize_memory:
        # Downcast numeric types
        for col in df.select_dtypes(include=['int64']).columns:
            df[col] = pd.to_numeric(df[col], downcast='integer')
        
        for col in df.select_dtypes(include=['float64']).columns:
            df[col] = pd.to_numeric(df[col], downcast='float')
    
    return df


def measure_page_load():
    """
    Context manager to measure page load time.
    
    Usage:
        with measure_page_load():
            # Page content
            ...
    """
    monitor = get_performance_monitor()
    
    class PageLoadContext:
        def __enter__(self):
            self.start_time = time.perf_counter()
            return self
        
        def __exit__(self, exc_type, exc_val, exc_tb):
            elapsed = time.perf_counter() - self.start_time
            monitor.metrics["timings"]["page_load"].append(elapsed)
            return False
    
    return PageLoadContext()


def log_performance_metric(metric_name: str, value: float, unit: str = "seconds"):
    """
    Log a custom performance metric.
    
    Usage:
        log_performance_metric("custom_operation", 0.5, "seconds")
    """
    monitor = get_performance_monitor()
    monitor.metrics["timings"][metric_name].append(value)


def get_performance_summary():
    """Get current performance summary."""
    monitor = get_performance_monitor()
    return monitor.get_performance_summary()


def check_benchmarks():
    """Check current performance against benchmarks."""
    monitor = get_performance_monitor()
    return monitor.check_benchmarks()


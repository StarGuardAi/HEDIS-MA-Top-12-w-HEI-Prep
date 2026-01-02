"""
Performance Optimization System for HEDIS Portfolio Optimizer
Comprehensive caching, monitoring, and optimization strategies
"""
import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Callable, Tuple
import time
import functools
import hashlib
import json


# ============================================================================
# DATA CACHING STRATEGY
# ============================================================================

@st.cache_data(ttl=3600, show_spinner=True)  # Cache for 1 hour
def load_member_data(
    start_date: Optional[str] = None,
    end_date: Optional[str] = None
) -> pd.DataFrame:
    """
    Load member data with caching.
    
    Args:
        start_date: Optional start date filter (YYYY-MM-DD)
        end_date: Optional end date filter (YYYY-MM-DD)
    
    Returns:
        DataFrame with member data
    
    Example:
        >>> df = load_member_data()
        >>> df = load_member_data('2024-10-01', '2024-12-31')
    """
    # Your data loading logic here
    # This is a placeholder - replace with actual data loading
    from utils.database import execute_query
    from utils.queries import get_portfolio_summary_query
    
    try:
        if start_date and end_date:
            query = get_portfolio_summary_query(start_date, end_date)
        else:
            query = get_portfolio_summary_query("2024-10-01", "2024-12-31")
        
        df = execute_query(query)
        return df
    except Exception as e:
        st.error(f"Error loading member data: {str(e)}")
        return pd.DataFrame()


@st.cache_data(ttl=1800, show_spinner=True)  # Cache for 30 minutes
def load_hedis_measures() -> pd.DataFrame:
    """
    Load HEDIS measures configuration.
    
    Returns:
        DataFrame with measure definitions
    """
    # Placeholder - replace with actual data loading
    measures_data = {
        'measure_code': ['HBA1C', 'BPC', 'BCS', 'CCS'],
        'measure_name': [
            'HbA1c Testing',
            'Blood Pressure Control',
            'Breast Cancer Screening',
            'Colorectal Cancer Screening'
        ],
        'category': ['Diabetes', 'Cardiovascular', 'Preventive', 'Preventive'],
        'star_rating_weight': [0.15, 0.12, 0.10, 0.10]
    }
    
    return pd.DataFrame(measures_data)


@st.cache_data(ttl=7200, show_spinner=False)  # Cache for 2 hours
def load_plan_context() -> Dict[str, Any]:
    """
    Load plan context data (changes infrequently).
    
    Returns:
        Dictionary with plan context information
    """
    from utils.plan_context import get_plan_context
    
    try:
        context = get_plan_context()
        return context if context else {}
    except Exception as e:
        st.warning(f"Could not load plan context: {str(e)}")
        return {}


@st.cache_data
def calculate_member_priorities(
    df: pd.DataFrame,
    financial_weight: float = 0.4,
    closure_weight: float = 0.4,
    star_weight: float = 0.2
) -> pd.DataFrame:
    """
    Cache expensive priority calculations.
    
    Args:
        df: Member DataFrame
        financial_weight: Weight for financial value (default: 0.4)
        closure_weight: Weight for closure probability (default: 0.4)
        star_weight: Weight for star rating impact (default: 0.2)
    
    Returns:
        DataFrame with priority_score column added
    
    Example:
        >>> df = load_member_data()
        >>> df = calculate_member_priorities(df, financial_weight=0.5)
    """
    if df.empty:
        return df
    
    df_work = df.copy()
    
    # Normalize values to 0-100 scale
    if 'financial_value' in df_work.columns:
        max_financial = df_work['financial_value'].max()
        if max_financial > 0:
            df_work['financial_normalized'] = (df_work['financial_value'] / max_financial) * 100
        else:
            df_work['financial_normalized'] = 0
    else:
        df_work['financial_normalized'] = 0
    
    if 'predicted_closure_probability' in df_work.columns:
        df_work['closure_normalized'] = df_work['predicted_closure_probability'] * 100
    else:
        df_work['closure_normalized'] = 0
    
    if 'star_rating_impact' in df_work.columns:
        df_work['star_normalized'] = df_work['star_rating_impact'] * 100
    else:
        df_work['star_normalized'] = 0
    
    # Calculate priority score
    df_work['priority_score'] = (
        df_work['financial_normalized'] * financial_weight +
        df_work['closure_normalized'] * closure_weight +
        df_work['star_normalized'] * star_weight
    )
    
    # Round to integer
    df_work['priority_score'] = df_work['priority_score'].round().astype(int)
    
    # Clamp to 0-100
    df_work['priority_score'] = df_work['priority_score'].clip(0, 100)
    
    return df_work


# ============================================================================
# ML MODEL CACHING
# ============================================================================

@st.cache_resource  # Cache ML models (not serializable)
def load_ml_model(model_path: str = "models/hedis_model.pkl"):
    """
    Load trained ML model once (cached as resource).
    
    Args:
        model_path: Path to model file
    
    Returns:
        Loaded ML model object
    
    Example:
        >>> model = load_ml_model()
        >>> predictions = model.predict(features)
    """
    try:
        import joblib
        
        # Try to load model
        model = joblib.load(model_path)
        return model
    except FileNotFoundError:
        st.warning(f"Model file not found: {model_path}")
        return None
    except Exception as e:
        st.error(f"Error loading model: {str(e)}")
        return None


@st.cache_data
def predict_closure_rates(df: pd.DataFrame, model_hash: str = "default") -> pd.DataFrame:
    """
    Cache predictions (use hash for model versioning).
    
    Args:
        df: DataFrame with features
        model_hash: Hash/version identifier for model
    
    Returns:
        DataFrame with predictions added
    
    Example:
        >>> df = load_member_data()
        >>> df = predict_closure_rates(df)
    """
    if df.empty:
        return df
    
    df_work = df.copy()
    
    # Placeholder prediction logic
    # In production, this would use the actual ML model
    if 'predicted_closure_probability' not in df_work.columns:
        # Simulate predictions
        np.random.seed(42)  # For reproducibility
        df_work['predicted_closure_probability'] = np.random.uniform(0.3, 0.9, len(df_work))
    
    return df_work


# ============================================================================
# QUERY OPTIMIZATION
# ============================================================================

@st.cache_data
def filter_data(
    df: pd.DataFrame,
    filters: Dict[str, Any]
) -> pd.DataFrame:
    """
    Cache filtered views for common filter combinations.
    
    Args:
        df: Source DataFrame
        filters: Dictionary of filter criteria
    
    Returns:
        Filtered DataFrame
    
    Example:
        >>> filters = {
        ...     'measures': ['HbA1c Testing'],
        ...     'min_value': 1000,
        ...     'status': ['Open', 'Pending']
        ... }
        >>> filtered_df = filter_data(df, filters)
    """
    if df.empty:
        return df
    
    filtered = df.copy()
    
    # Filter by measures
    if filters.get('measures') and 'measure_name' in filtered.columns:
        filtered = filtered[filtered['measure_name'].isin(filters['measures'])]
    
    # Filter by minimum financial value
    if filters.get('min_value') and 'financial_value' in filtered.columns:
        filtered = filtered[filtered['financial_value'] >= filters['min_value']]
    
    # Filter by status
    if filters.get('status') and 'gap_status' in filtered.columns:
        filtered = filtered[filtered['gap_status'].isin(filters['status'])]
    
    # Filter by date range
    if filters.get('start_date') and 'date' in filtered.columns:
        filtered = filtered[filtered['date'] >= filters['start_date']]
    
    if filters.get('end_date') and 'date' in filtered.columns:
        filtered = filtered[filtered['date'] <= filters['end_date']]
    
    # Filter by priority score
    if filters.get('min_priority') and 'priority_score' in filtered.columns:
        filtered = filtered[filtered['priority_score'] >= filters['min_priority']]
    
    return filtered


@st.cache_data
def aggregate_by_measure(df: pd.DataFrame) -> pd.DataFrame:
    """
    Cache aggregated measure-level statistics.
    
    Args:
        df: Member-level DataFrame
    
    Returns:
        Aggregated DataFrame by measure
    
    Example:
        >>> df = load_member_data()
        >>> summary = aggregate_by_measure(df)
    """
    if df.empty or 'measure_name' not in df.columns:
        return pd.DataFrame()
    
    aggregation = {
        'member_id': 'count',
        'financial_value': 'sum'
    }
    
    if 'predicted_closure_probability' in df.columns:
        aggregation['predicted_closure_probability'] = 'mean'
    
    if 'priority_score' in df.columns:
        aggregation['priority_score'] = 'mean'
    
    summary = df.groupby('measure_name').agg(aggregation).reset_index()
    summary.columns = ['measure_name', 'member_count', 'total_value', 'avg_closure_rate', 'avg_priority']
    
    return summary


# ============================================================================
# PERFORMANCE MONITORING
# ============================================================================

def performance_monitor(func: Callable) -> Callable:
    """
    Decorator to monitor function performance.
    
    Usage:
        @performance_monitor
        def my_function():
            # Your code
            pass
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        
        try:
            result = func(*args, **kwargs)
            success = True
            error = None
        except Exception as e:
            result = None
            success = False
            error = str(e)
            raise
        finally:
            end = time.time()
            duration = end - start
            
            # Log to session state
            if 'performance_log' not in st.session_state:
                st.session_state.performance_log = []
            
            st.session_state.performance_log.append({
                'function': func.__name__,
                'duration': duration,
                'timestamp': datetime.now(),
                'success': success,
                'error': error,
                'args_hash': hash(str(args)) if args else None,
                'kwargs_hash': hash(str(sorted(kwargs.items()))) if kwargs else None
            })
            
            # Keep only last 100 entries
            if len(st.session_state.performance_log) > 100:
                st.session_state.performance_log = st.session_state.performance_log[-100:]
        
        return result
    
    return wrapper


def get_performance_summary() -> Dict[str, Any]:
    """
    Get performance summary statistics.
    
    Returns:
        Dictionary with performance metrics
    """
    if 'performance_log' not in st.session_state or not st.session_state.performance_log:
        return {
            'total_calls': 0,
            'avg_duration': 0,
            'max_duration': 0,
            'min_duration': 0,
            'total_time': 0
        }
    
    log = st.session_state.performance_log
    
    durations = [entry['duration'] for entry in log if entry.get('success', True)]
    
    if not durations:
        return {
            'total_calls': len(log),
            'avg_duration': 0,
            'max_duration': 0,
            'min_duration': 0,
            'total_time': 0
        }
    
    return {
        'total_calls': len(log),
        'avg_duration': np.mean(durations),
        'max_duration': np.max(durations),
        'min_duration': np.min(durations),
        'total_time': np.sum(durations),
        'success_rate': sum(1 for e in log if e.get('success', True)) / len(log) * 100
    }


def render_performance_dashboard():
    """Render performance monitoring dashboard"""
    st.markdown("### ⚡ Performance Metrics")
    
    summary = get_performance_summary()
    
    if summary['total_calls'] == 0:
        st.info("No performance data collected yet.")
        return
    
    # Summary metrics
    col1, col2, col3, col4 = st.columns(4, gap="small")
    
    with col1:
        st.metric("Total Calls", summary['total_calls'])
    
    with col2:
        st.metric("Avg Duration", f"{summary['avg_duration']:.3f}s")
    
    with col3:
        st.metric("Max Duration", f"{summary['max_duration']:.3f}s")
    
    with col4:
        st.metric("Success Rate", f"{summary['success_rate']:.1f}%")
    
    st.markdown("---")
    
    # Function breakdown
    if 'performance_log' in st.session_state:
        log_df = pd.DataFrame(st.session_state.performance_log)
        
        if not log_df.empty:
            st.markdown("#### Function Performance")
            
            func_summary = log_df.groupby('function').agg({
                'duration': ['mean', 'max', 'count']
            }).round(3)
            
            func_summary.columns = ['Avg Duration (s)', 'Max Duration (s)', 'Call Count']
            func_summary = func_summary.sort_values('Avg Duration (s)', ascending=False)
            
            st.dataframe(func_summary, use_container_width=True)
            
            # Clear log button
            if st.button("🗑️ Clear Performance Log", use_container_width=True):
                st.session_state.performance_log = []
                st.rerun()


# ============================================================================
# LAZY LOADING STRATEGY
# ============================================================================

def lazy_load_section(
    section_name: str,
    load_func: Callable,
    placeholder_text: str = "Loading...",
    force_reload: bool = False
) -> Any:
    """
    Lazy load heavy sections on demand.
    
    Args:
        section_name: Unique identifier for section
        load_func: Function to load content
        placeholder_text: Text to show while loading
        force_reload: Force reload even if cached (default: False)
    
    Returns:
        Loaded content
    
    Example:
        >>> def load_heavy_chart():
        ...     # Expensive chart generation
        ...     return fig
        >>> fig = lazy_load_section('heavy_chart', load_heavy_chart)
    """
    cache_key = f'{section_name}_content'
    loaded_key = f'{section_name}_loaded'
    
    if force_reload or loaded_key not in st.session_state:
        with st.spinner(placeholder_text):
            try:
                content = load_func()
                st.session_state[cache_key] = content
                st.session_state[loaded_key] = True
                return content
            except Exception as e:
                st.error(f"Error loading {section_name}: {str(e)}")
                return None
    
    return st.session_state.get(cache_key)


def conditional_render(
    condition: bool,
    render_func: Callable,
    placeholder: Optional[str] = None
):
    """
    Conditionally render expensive components.
    
    Args:
        condition: Whether to render
        render_func: Function to render content
        placeholder: Placeholder text if not rendering
    
    Example:
        >>> if st.checkbox("Show detailed chart"):
        ...     conditional_render(True, lambda: render_expensive_chart())
    """
    if condition:
        render_func()
    elif placeholder:
        st.info(placeholder)


# ============================================================================
# MOBILE-SPECIFIC OPTIMIZATIONS
# ============================================================================

@st.cache_data(ttl=1800)  # Cache for 30 minutes
def get_mobile_summary_data() -> Dict[str, Any]:
    """
    Get lightweight summary data for mobile view.
    
    Returns:
        Dictionary with summary statistics
    """
    try:
        df = load_member_data()
        
        if df.empty:
            return {}
        
        summary = {
            'total_members': len(df),
            'total_value': df['financial_value'].sum() if 'financial_value' in df.columns else 0,
            'avg_closure_rate': df['predicted_closure_probability'].mean() * 100 if 'predicted_closure_probability' in df.columns else 0,
            'measures_count': df['measure_name'].nunique() if 'measure_name' in df.columns else 0
        }
        
        return summary
    except Exception as e:
        st.warning(f"Error generating mobile summary: {str(e)}")
        return {}


@st.cache_data
def get_top_opportunities(df: pd.DataFrame, top_n: int = 5) -> pd.DataFrame:
    """
    Get top N opportunities (cached for mobile quick view).
    
    Args:
        df: Member DataFrame
        top_n: Number of top items to return (default: 5)
    
    Returns:
        DataFrame with top opportunities
    """
    if df.empty:
        return pd.DataFrame()
    
    # Sort by priority or financial value
    if 'priority_score' in df.columns:
        top_df = df.nlargest(top_n, 'priority_score')
    elif 'financial_value' in df.columns:
        top_df = df.nlargest(top_n, 'financial_value')
    else:
        top_df = df.head(top_n)
    
    return top_df


# ============================================================================
# CACHE MANAGEMENT
# ============================================================================

def clear_all_caches():
    """Clear all Streamlit caches"""
    st.cache_data.clear()
    st.cache_resource.clear()
    
    # Clear session state caches
    keys_to_clear = [key for key in st.session_state.keys() if '_loaded' in key or '_content' in key]
    for key in keys_to_clear:
        del st.session_state[key]
    
    st.success("✅ All caches cleared!")


def clear_data_cache():
    """Clear only data caches"""
    st.cache_data.clear()
    st.success("✅ Data cache cleared!")


def clear_resource_cache():
    """Clear only resource caches (ML models, etc.)"""
    st.cache_resource.clear()
    st.success("✅ Resource cache cleared!")


def get_cache_info() -> Dict[str, Any]:
    """
    Get information about current cache state.
    
    Returns:
        Dictionary with cache statistics
    """
    # This is a placeholder - Streamlit doesn't expose cache stats directly
    # In production, you might track cache hits/misses manually
    
    return {
        'data_cache_active': True,
        'resource_cache_active': True,
        'performance_log_entries': len(st.session_state.get('performance_log', [])),
        'lazy_loaded_sections': len([k for k in st.session_state.keys() if '_loaded' in k])
    }


# ============================================================================
# BENCHMARKING TOOLS
# ============================================================================

class Benchmark:
    """Benchmarking utility for performance testing"""
    
    def __init__(self, name: str):
        """
        Initialize benchmark.
        
        Args:
            name: Benchmark name
        """
        self.name = name
        self.start_time = None
        self.end_time = None
        self.duration = None
    
    def __enter__(self):
        """Start benchmark"""
        self.start_time = time.time()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """End benchmark"""
        self.end_time = time.time()
        self.duration = self.end_time - self.start_time
        
        # Log to session state
        if 'benchmarks' not in st.session_state:
            st.session_state.benchmarks = []
        
        st.session_state.benchmarks.append({
            'name': self.name,
            'duration': self.duration,
            'timestamp': datetime.now()
        })
    
    def get_duration(self) -> float:
        """Get benchmark duration"""
        if self.duration is None and self.start_time:
            return time.time() - self.start_time
        return self.duration or 0


def benchmark_function(func: Callable, *args, **kwargs) -> Tuple[Any, float]:
    """
    Benchmark a function call.
    
    Args:
        func: Function to benchmark
        *args: Function arguments
        **kwargs: Function keyword arguments
    
    Returns:
        Tuple of (result, duration)
    
    Example:
        >>> result, duration = benchmark_function(load_member_data)
        >>> st.write(f"Loaded in {duration:.3f}s")
    """
    start = time.time()
    result = func(*args, **kwargs)
    duration = time.time() - start
    
    return result, duration


def render_benchmark_results():
    """Render benchmark results"""
    if 'benchmarks' not in st.session_state or not st.session_state.benchmarks:
        st.info("No benchmarks recorded yet.")
        return
    
    st.markdown("### 📊 Benchmark Results")
    
    benchmarks_df = pd.DataFrame(st.session_state.benchmarks)
    
    # Summary
    summary = benchmarks_df.groupby('name')['duration'].agg(['mean', 'min', 'max', 'count']).round(3)
    summary.columns = ['Avg (s)', 'Min (s)', 'Max (s)', 'Runs']
    
    st.dataframe(summary, use_container_width=True)
    
    # Clear button
    if st.button("🗑️ Clear Benchmarks", use_container_width=True):
        st.session_state.benchmarks = []
        st.rerun()


# ============================================================================
# OPTIMIZATION HELPERS
# ============================================================================

def optimize_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """
    Optimize DataFrame memory usage.
    
    Args:
        df: DataFrame to optimize
    
    Returns:
        Optimized DataFrame
    """
    if df.empty:
        return df
    
    df_opt = df.copy()
    
    # Optimize numeric columns
    for col in df_opt.select_dtypes(include=['int64']).columns:
        df_opt[col] = pd.to_numeric(df_opt[col], downcast='integer')
    
    for col in df_opt.select_dtypes(include=['float64']).columns:
        df_opt[col] = pd.to_numeric(df_opt[col], downcast='float')
    
    # Optimize string columns
    for col in df_opt.select_dtypes(include=['object']).columns:
        if df_opt[col].dtype == 'object':
            try:
                df_opt[col] = df_opt[col].astype('category')
            except:
                pass
    
    return df_opt


def create_filter_hash(filters: Dict[str, Any]) -> str:
    """
    Create hash for filter dictionary (for cache key).
    
    Args:
        filters: Filter dictionary
    
    Returns:
        Hash string
    """
    filter_str = json.dumps(filters, sort_keys=True)
    return hashlib.md5(filter_str.encode()).hexdigest()


# ============================================================================
# USAGE EXAMPLES
# ============================================================================

def example_caching_usage():
    """Example of caching usage"""
    
    # Load data (cached)
    df = load_member_data()
    
    # Calculate priorities (cached)
    df = calculate_member_priorities(df)
    
    # Filter data (cached)
    filters = {
        'measures': ['HbA1c Testing'],
        'min_value': 1000
    }
    filtered_df = filter_data(df, filters)
    
    # Aggregate (cached)
    summary = aggregate_by_measure(filtered_df)
    
    return summary


def example_lazy_loading():
    """Example of lazy loading"""
    
    def load_expensive_chart():
        import plotly.express as px
        df = load_member_data()
        fig = px.bar(df, x='measure_name', y='financial_value')
        return fig
    
    # Lazy load chart
    fig = lazy_load_section('expensive_chart', load_expensive_chart, "Generating chart...")
    
    if fig:
        st.plotly_chart(fig, use_container_width=True)


def example_benchmarking():
    """Example of benchmarking"""
    
    # Using context manager
    with Benchmark("load_data"):
        df = load_member_data()
    
    # Using function wrapper
    result, duration = benchmark_function(calculate_member_priorities, df)
    st.write(f"Calculation took {duration:.3f} seconds")


if __name__ == "__main__":
    print("Performance optimization system ready!")
    print("\nKey features:")
    print("- Data caching with TTL")
    print("- ML model caching")
    print("- Query optimization")
    print("- Performance monitoring")
    print("- Lazy loading")
    print("- Benchmarking tools")


"""
Performance monitoring usage examples
Demonstrates how to integrate performance tracking into dashboard pages
"""
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from utils.performance_monitor import track_performance, get_performance_monitor
from utils.performance_helpers import (
    cached_with_tracking,
    track_render_time,
    track_filter_time,
    track_export_time,
    use_fragment,
    optimize_dataframe
)


# Example 1: Track data fetching with caching
@cached_with_tracking(ttl=3600)
@track_performance("data_fetch")
def fetch_roi_data(start_date, end_date):
    """Fetch ROI data with performance tracking."""
    from utils.database import execute_query
    from utils.queries import get_roi_by_measure_query
    
    query = get_roi_by_measure_query(start_date, end_date)
    df = execute_query(query)
    
    # Optimize DataFrame
    df = optimize_dataframe(df)
    
    return df


# Example 2: Track chart rendering
@track_render_time("roi_chart")
@use_fragment
def render_roi_chart(df):
    """Render ROI chart with performance tracking."""
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=df['measure_code'],
        y=df['roi_ratio'],
        name='ROI Ratio'
    ))
    fig.update_layout(
        title="ROI by Measure",
        xaxis_title="Measure",
        yaxis_title="ROI Ratio"
    )
    st.plotly_chart(fig, use_container_width=True)


# Example 3: Track filter application
@track_filter_time()
def apply_measure_filter(df, selected_measures):
    """Apply measure filter with performance tracking."""
    if selected_measures:
        return df[df['measure_code'].isin(selected_measures)]
    return df


# Example 4: Track export generation
@track_export_time()
def export_to_csv(df, filename="export.csv"):
    """Export DataFrame to CSV with performance tracking."""
    return df.to_csv(index=False)


# Example 5: Complete page example
def example_performance_optimized_page():
    """Example of a performance-optimized dashboard page."""
    monitor = get_performance_monitor()
    
    st.title("Example Performance-Optimized Page")
    
    # Date filters
    start_date = st.date_input("Start Date", value=pd.Timestamp("2024-01-01"))
    end_date = st.date_input("End Date", value=pd.Timestamp("2024-12-31"))
    
    # Fetch data (cached and tracked)
    with st.spinner("Loading data..."):
        df = fetch_roi_data(
            start_date.strftime("%Y-%m-%d"),
            end_date.strftime("%Y-%m-%d")
        )
    
    if df.empty:
        st.warning("No data available")
        return
    
    # Measure filter (tracked)
    measures = df['measure_code'].unique().tolist()
    selected_measures = st.multiselect("Select Measures", measures, default=measures)
    
    # Apply filter (tracked)
    filtered_df = apply_measure_filter(df, selected_measures)
    
    # Display metrics
    st.metric("Total Measures", len(filtered_df))
    st.metric("Average ROI", f"{filtered_df['roi_ratio'].mean():.2f}")
    
    # Render chart (tracked and fragmented)
    render_roi_chart(filtered_df)
    
    # Export button (tracked)
    if st.button("Export to CSV"):
        csv = export_to_csv(filtered_df)
        st.download_button(
            "Download CSV",
            csv,
            file_name="roi_data.csv",
            mime="text/csv"
        )
    
    # Show performance summary
    with st.expander("Performance Metrics"):
        summary = monitor.get_performance_summary()
        st.json(summary)


# Example 6: Manual performance tracking
def example_manual_tracking():
    """Example of manual performance tracking."""
    import time
    from utils.performance_helpers import log_performance_metric
    
    # Start timing
    start_time = time.perf_counter()
    
    # Do some work
    result = expensive_operation()
    
    # Calculate elapsed time
    elapsed = time.perf_counter() - start_time
    
    # Log metric
    log_performance_metric("expensive_operation", elapsed)
    
    return result


def expensive_operation():
    """Simulate expensive operation."""
    import time
    time.sleep(0.1)  # Simulate work
    return "result"


# Example 7: Using fragments for granular updates
@use_fragment
def update_chart_only():
    """Update only the chart without re-rendering entire page."""
    st.plotly_chart(fig, use_container_width=True)


# Example 8: Memory monitoring
def example_memory_monitoring():
    """Example of memory usage monitoring."""
    monitor = get_performance_monitor()
    
    # Get memory usage
    memory = monitor.get_memory_usage()
    
    st.metric("Current Memory", f"{memory['current_mb']:.2f} MB")
    st.metric("Peak Memory", f"{memory['peak_mb']:.2f} MB")
    
    # Check if memory is high
    if memory['current_mb'] > 500:  # 500 MB threshold
        st.warning("High memory usage detected. Consider clearing cache.")
        if st.button("Clear Cache"):
            st.cache_data.clear()
            st.rerun()


# Example 9: Benchmark checking
def example_benchmark_checking():
    """Example of checking performance against benchmarks."""
    monitor = get_performance_monitor()
    benchmarks = monitor.check_benchmarks()
    
    st.header("Benchmark Status")
    
    for category, results in benchmarks.items():
        st.subheader(category.title())
        for metric, result in results.items():
            status_icon = "✅" if result["status"] == "pass" else "❌"
            st.write(f"{status_icon} {metric}: {result['actual']:.3f}s / {result['target']:.1f}s")


# Example 10: Session state optimization
def example_session_state_optimization():
    """Example of optimizing session state."""
    monitor = get_performance_monitor()
    
    # Get session state size
    session_size = monitor.get_session_state_size()
    st.metric("Session State Size", f"{session_size / 1024:.2f} KB")
    
    # Clear unused session state
    if st.button("Clear Unused Session State"):
        # Keep only essential keys
        essential_keys = ["user", "selected_measure"]
        keys_to_remove = [k for k in st.session_state.keys() if k not in essential_keys]
        
        for key in keys_to_remove:
            del st.session_state[key]
        
        st.success(f"Cleared {len(keys_to_remove)} unused keys")
        st.rerun()


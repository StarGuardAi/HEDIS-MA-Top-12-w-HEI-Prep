"""
Performance Dashboard Component
Visual performance monitoring and cache management UI
"""
import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta
from utils.performance import (
    get_performance_summary,
    render_performance_dashboard,
    get_cache_info,
    clear_all_caches,
    clear_data_cache,
    clear_resource_cache,
    render_benchmark_results
)


def render_performance_page():
    """Render complete performance monitoring page"""
    st.title("⚡ Performance Dashboard")
    
    # Cache management
    st.markdown("### 🗄️ Cache Management")
    
    col1, col2, col3 = st.columns(3, gap="small")
    
    with col1:
        if st.button("🗑️ Clear Data Cache", use_container_width=True):
            clear_data_cache()
            st.rerun()
    
    with col2:
        if st.button("🗑️ Clear Resource Cache", use_container_width=True):
            clear_resource_cache()
            st.rerun()
    
    with col3:
        if st.button("🗑️ Clear All Caches", use_container_width=True, type="primary"):
            clear_all_caches()
            st.rerun()
    
    st.markdown("---")
    
    # Cache information
    cache_info = get_cache_info()
    
    st.markdown("### 📊 Cache Status")
    info_col1, info_col2, info_col3 = st.columns(3, gap="small")
    
    with info_col1:
        st.metric("Data Cache", "Active" if cache_info['data_cache_active'] else "Inactive")
    
    with info_col2:
        st.metric("Resource Cache", "Active" if cache_info['resource_cache_active'] else "Inactive")
    
    with info_col3:
        st.metric("Lazy Loaded Sections", cache_info['lazy_loaded_sections'])
    
    st.markdown("---")
    
    # Performance metrics
    render_performance_dashboard()
    
    st.markdown("---")
    
    # Benchmark results
    render_benchmark_results()
    
    st.markdown("---")
    
    # Performance tips
    with st.expander("💡 Performance Tips", expanded=False):
        st.markdown("""
        **Caching Best Practices:**
        1. Use appropriate TTL values (300s-3600s)
        2. Cache at data loading level, not UI level
        3. Use lazy loading for heavy sections
        4. Monitor performance regularly
        
        **Optimization Tips:**
        1. Limit data loaded at once
        2. Use pagination for large datasets
        3. Optimize DataFrame memory usage
        4. Clear caches when data updates
        
        **Mobile Optimizations:**
        1. Use lightweight summary data
        2. Limit to top N items
        3. Reduce chart complexity
        4. Minimize re-renders
        """)


if __name__ == "__main__":
    render_performance_page()


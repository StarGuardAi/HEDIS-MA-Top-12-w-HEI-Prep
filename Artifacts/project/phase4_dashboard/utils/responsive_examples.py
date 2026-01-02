"""
Example Usage of Responsive Layout System

Demonstrates how to integrate responsive components into Streamlit app
"""
import streamlit as st
import pandas as pd
import plotly.express as px
from utils.responsive_layout import (
    DeviceDetector,
    ResponsiveColumns,
    ResponsiveConfig,
    ResponsiveNav,
    ResponsiveChart,
    ResponsiveTable,
    ResponsiveButton
)


# ============================================================================
# EXAMPLE 1: Basic Responsive App
# ============================================================================
def example_basic_responsive():
    """Basic example of responsive app"""
    
    # Page config
    st.set_page_config(
        page_title="HEDIS Responsive",
        page_icon="⭐",
        layout="wide"
    )
    
    # Initialize
    DeviceDetector.init()
    st.markdown(ResponsiveConfig.get_css(), unsafe_allow_html=True)
    
    # Device toggle (for testing)
    with st.sidebar:
        DeviceDetector.render_device_toggle()
    
    # Header
    st.title("⭐ HEDIS Portfolio Optimizer")
    
    # Responsive metrics
    rc = ResponsiveColumns()
    metrics = [
        {'label': 'Potential ROI', 'value': '498%', 'delta': '+$935K'},
        {'label': 'Star Rating', 'value': '4.5 ⭐', 'delta': '+0.5'},
        {'label': 'Members', 'value': '10,000+', 'delta': '+1,200'},
        {'label': 'Compliance', 'value': '93%', 'delta': '+8%'}
    ]
    rc.metric_grid(metrics)
    
    st.markdown("---")
    
    # Responsive chart
    df = pd.DataFrame({
        'Measure': ['HbA1c', 'BP Control', 'BCS', 'CCS'],
        'ROI': [1.38, 1.25, 1.32, 1.28]
    })
    
    fig = px.bar(df, x='Measure', y='ROI', title="ROI by Measure")
    ResponsiveChart.render(fig)


# ============================================================================
# EXAMPLE 2: Responsive Navigation
# ============================================================================
def example_responsive_navigation():
    """Example with responsive navigation"""
    
    DeviceDetector.init()
    st.markdown(ResponsiveConfig.get_css(), unsafe_allow_html=True)
    
    st.title("Responsive Navigation Example")
    
    # Define views
    views = {
        '📊 Dashboard': 'dashboard',
        '🎯 Opportunities': 'opportunities',
        '📈 Measures': 'measures',
        '👥 Members': 'members'
    }
    
    nav = ResponsiveNav(views)
    
    # Route based on device
    if ResponsiveConfig.get('use_tabs'):
        # Desktop/Tablet: Tabs
        for view_id in nav.render():
            if view_id == 'dashboard':
                st.write("Dashboard content")
            elif view_id == 'opportunities':
                st.write("Opportunities content")
            elif view_id == 'measures':
                st.write("Measures content")
            elif view_id == 'members':
                st.write("Members content")
    else:
        # Mobile: Selectbox
        view_id = nav.render()
        if view_id == 'dashboard':
            st.write("Dashboard content")
        elif view_id == 'opportunities':
            st.write("Opportunities content")
        elif view_id == 'measures':
            st.write("Measures content")
        elif view_id == 'members':
            st.write("Members content")


# ============================================================================
# EXAMPLE 3: Responsive Table
# ============================================================================
def example_responsive_table():
    """Example with responsive table"""
    
    DeviceDetector.init()
    st.markdown(ResponsiveConfig.get_css(), unsafe_allow_html=True)
    
    st.title("Responsive Table Example")
    
    # Sample data
    df = pd.DataFrame({
        'Measure': ['HbA1c Testing', 'Blood Pressure Control', 'Breast Cancer Screening'],
        'ROI': [1.38, 1.25, 1.32],
        'Members': [847, 623, 512],
        'Value': [285000, 320000, 275000],
        'Closure Rate': [93.2, 88.5, 85.1],
        'Priority': [85, 72, 68]
    })
    
    # Responsive table
    ResponsiveTable.render(df)
    
    # Show device info
    device = DeviceDetector.get_device_type()
    max_cols = ResponsiveConfig.get('max_table_columns')
    st.caption(f"Device: {device} | Max columns: {max_cols}")


# ============================================================================
# EXAMPLE 4: Complete Dashboard
# ============================================================================
def example_complete_dashboard():
    """Complete responsive dashboard example"""
    
    # Page config
    st.set_page_config(
        page_title="HEDIS Responsive Dashboard",
        page_icon="⭐",
        layout="wide",
        initial_sidebar_state="auto"
    )
    
    # Initialize
    DeviceDetector.init()
    st.markdown(ResponsiveConfig.get_css(), unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.markdown("### Device Preview")
        DeviceDetector.render_device_toggle()
        st.markdown("---")
        
        # Show current device info
        device = DeviceDetector.get_device_type()
        config = ResponsiveConfig.get_all()
        st.info(f"**Current Device:** {device.title()}")
        st.caption(f"Chart Height: {config['chart_height']}px")
        st.caption(f"Table Height: {config['table_height']}px")
        st.caption(f"Columns: {4 if device == 'desktop' else 2 if device == 'tablet' else 1}")
    
    # Header
    st.title("⭐ HEDIS Portfolio Optimizer")
    st.caption(f"Responsive View: {device.title()}")
    
    # Metrics
    rc = ResponsiveColumns()
    metrics = [
        {'label': 'Potential ROI', 'value': '498%', 'delta': '+$935K annually'},
        {'label': 'Star Rating Impact', 'value': '4.5 ⭐', 'delta': '+0.5 stars'},
        {'label': 'Members Optimized', 'value': '10,000+', 'delta': 'All eligible'},
        {'label': 'Compliance Rate', 'value': '93%', 'delta': '+8% improvement'}
    ]
    rc.metric_grid(metrics)
    
    st.markdown("---")
    
    # Navigation
    views = {
        '📊 Dashboard': 'dashboard',
        '🎯 Top Opportunities': 'opportunities',
        '📈 My Measures': 'measures'
    }
    
    nav = ResponsiveNav(views)
    
    # Content based on navigation
    if ResponsiveConfig.get('use_tabs'):
        tabs = list(nav.render())
        for view_id in tabs:
            if view_id == 'dashboard':
                render_dashboard_content()
            elif view_id == 'opportunities':
                render_opportunities_content()
            elif view_id == 'measures':
                render_measures_content()
    else:
        view_id = nav.render()
        if view_id == 'dashboard':
            render_dashboard_content()
        elif view_id == 'opportunities':
            render_opportunities_content()
        elif view_id == 'measures':
            render_measures_content()


def render_dashboard_content():
    """Render dashboard view content"""
    st.markdown("### Dashboard Overview")
    
    # Sample chart
    df = pd.DataFrame({
        'Month': ['Jan', 'Feb', 'Mar', 'Apr'],
        'Compliance': [85, 88, 90, 93]
    })
    
    fig = px.line(df, x='Month', y='Compliance', title="Compliance Trend")
    ResponsiveChart.render(fig)


def render_opportunities_content():
    """Render opportunities view content"""
    st.markdown("### Top Opportunities")
    
    df = pd.DataFrame({
        'Measure': ['HbA1c Testing', 'Blood Pressure Control', 'Breast Cancer Screening'],
        'ROI': [1.38, 1.25, 1.32],
        'Members': [847, 623, 512]
    })
    
    fig = px.bar(df, x='Measure', y='ROI', title="ROI by Measure")
    ResponsiveChart.render(fig)


def render_measures_content():
    """Render measures view content"""
    st.markdown("### My Measures")
    
    df = pd.DataFrame({
        'Measure': ['HbA1c Testing', 'Blood Pressure Control', 'Breast Cancer Screening'],
        'Current': [45.2, 52.8, 48.5],
        'Benchmark': [40.0, 45.0, 42.0]
    })
    
    ResponsiveTable.render(df)


# ============================================================================
# EXAMPLE 5: Conditional Rendering
# ============================================================================
def example_conditional_rendering():
    """Example of conditional rendering based on device"""
    
    DeviceDetector.init()
    st.markdown(ResponsiveConfig.get_css(), unsafe_allow_html=True)
    
    device = DeviceDetector.get_device_type()
    
    st.title("Conditional Rendering Example")
    
    # Show different content based on device
    if device == 'mobile':
        st.info("📱 Mobile View: Simplified content")
        # Show simplified version
        st.metric("ROI", "498%")
        st.metric("Star Rating", "4.5 ⭐")
        
    elif device == 'tablet':
        st.info("📱 Tablet View: Medium detail")
        # Show medium detail
        col1, col2 = st.columns(2)
        with col1:
            st.metric("ROI", "498%")
        with col2:
            st.metric("Star Rating", "4.5 ⭐")
        
    else:  # desktop
        st.info("🖥️ Desktop View: Full detail")
        # Show full detail
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("ROI", "498%")
        with col2:
            st.metric("Star Rating", "4.5 ⭐")
        with col3:
            st.metric("Members", "10,000+")
        with col4:
            st.metric("Compliance", "93%")


if __name__ == "__main__":
    print("Responsive layout examples ready!")
    print("\nRun examples:")
    print("1. example_basic_responsive()")
    print("2. example_responsive_navigation()")
    print("3. example_responsive_table()")
    print("4. example_complete_dashboard()")
    print("5. example_conditional_rendering()")


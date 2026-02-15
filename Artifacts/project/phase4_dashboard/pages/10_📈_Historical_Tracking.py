"""
Historical Performance Tracking - Desktop Version
Full interactive time-series explorer with forecasting
"""
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import numpy as np

from utils.database import execute_query
from utils.historical_tracking import HistoricalTracker
from utils.enhanced_charts import create_wow_bar_chart, create_wow_line_chart, create_wow_area_chart, create_wow_pie_chart
from utils.queries import get_roi_by_measure_query

# ============================================================================
# PAGE CONFIGURATION
# ============================================================================
st.set_page_config(
    page_title="Historical Tracking - HEDIS Portfolio",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="auto"
)

# Import sidebar styling function (same as Home page)
try:
    from utils.sidebar_styling import apply_sidebar_styling
except ImportError:
    def apply_sidebar_styling():
        pass

# Apply consistent sidebar styling (same as Home page)
apply_sidebar_styling()

# ============================================================================
# HEADER
# ============================================================================
st.markdown("""
<div class='starguard-header-container'>
    <div class='starguard-title'>⭐ StarGuard AI | Turning Data Into Stars</div>
    <div class='starguard-subtitle'>Healthcare AI Architect • $148M+ Documented Savings • HEDIS & Star Rating Expert<br>🔒 Zero PHI Exposure • Context Engineering + Agentic RAG • Production-Grade Analytics</div>
</div>
""", unsafe_allow_html=True)

# ============================================================================
# CSS STYLING
# ============================================================================
st.markdown("""
<style>
/* StarGuard Header Container */
.starguard-header-container {
    background: linear-gradient(135deg, #4A3D6F 0%, #6F5F96 100%);
    padding: 1rem 1.5rem 0.5rem 1.5rem !important;
    border-radius: 10px;
    margin-top: 0 !important;
    margin-bottom: 1rem !important;
    text-align: center;
    box-shadow: 0 4px 12px rgba(74, 61, 111, 0.25);
}

.starguard-title {
    color: white !important;
    font-size: 1.8rem !important;
    font-weight: 700 !important;
    text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
    margin: 0 0 0.5rem 0 !important;
    padding: 0 0 0.5rem 0 !important;
    line-height: 1.2 !important;
    border-bottom: 3px solid #4ade80 !important;
}

.starguard-subtitle {
    color: rgba(255, 255, 255, 0.92) !important;
    font-size: 0.85rem !important;
    margin: 0.5rem 0 0 0 !important;
    padding: 0 !important;
    line-height: 1.3 !important;
}

@media (max-width: 768px) {
    .starguard-header-container {
        padding: 0.8rem 1rem !important;
    }
    
    .starguard-title {
        font-size: 1.2rem !important;
    }
    
    .starguard-subtitle {
        font-size: 0.7rem !important;
    }
}

/* Page header h1 - centered with appropriate font size */
h1:first-of-type,
.stMarkdown h1:first-of-type,
div[data-testid="stMarkdownContainer"] h1:first-of-type {
    text-align: center !important;
    font-size: 1.8rem !important;
    font-weight: 600 !important;
    margin: 0.5rem 0 !important;
}

/* Sidebar purple background to match header */
[data-testid="stSidebar"] {
    background: linear-gradient(135deg, #4A3D6F 0%, #6F5F96 100%) !important;
}

[data-testid="stSidebar"] > div:first-child {
    background: linear-gradient(135deg, #4A3D6F 0%, #6F5F96 100%) !important;
}

/* Sidebar text color - white for visibility on purple */
[data-testid="stSidebar"] * {
    color: white !important;
}

[data-testid="stSidebar"] p,
[data-testid="stSidebar"] span,
[data-testid="stSidebar"] div,
[data-testid="stSidebar"] a,
[data-testid="stSidebar"] label,
[data-testid="stSidebar"] button {
    color: white !important;
}

/* Sidebar navigation links */
[data-testid="stSidebar"] a {
    color: white !important;
}

[data-testid="stSidebar"] a:hover {
    color: #4ade80 !important;
}

/* Sidebar selectbox and other widgets */
[data-testid="stSidebar"] .stSelectbox label,
[data-testid="stSidebar"] .stMultiSelect label,
[data-testid="stSidebar"] .stSlider label,
[data-testid="stSidebar"] .stRadio label {
    color: white !important;
}

/* Sidebar widget backgrounds - make them visible on purple */
[data-testid="stSidebar"] .stSelectbox > div > div,
[data-testid="stSidebar"] .stMultiSelect > div > div {
    background-color: rgba(255, 255, 255, 0.95) !important;
    border-radius: 5px !important;
}

[data-testid="stSidebar"] .stSelectbox > div > div *,
[data-testid="stSidebar"] .stMultiSelect > div > div * {
    color: #4A3D6F !important;
}

/* Sidebar success/info boxes */
[data-testid="stSidebar"] [data-testid="stSuccess"],
[data-testid="stSidebar"] [data-testid="stInfo"] {
    background-color: rgba(255, 255, 255, 0.1) !important;
    border: 1px solid rgba(255, 255, 255, 0.3) !important;
}

[data-testid="stSidebar"] [data-testid="stSuccess"] *,
[data-testid="stSidebar"] [data-testid="stInfo"] * {
    color: white !important;
}

/* Sidebar button styling */
[data-testid="stSidebar"] button {
    background-color: rgba(255, 255, 255, 0.2) !important;
    color: white !important;
    border: 1px solid rgba(255, 255, 255, 0.3) !important;
}

/* ========== HOME BUTTON STYLING ========== */
/* Hide the default "app" text and replace with "🏠 Home" */
[data-testid="stSidebarNav"] ul li:first-child a {
    font-size: 0 !important;  /* Hide original text */
    background: rgba(255, 255, 255, 0.2) !important;
    padding: 0.75rem 1rem !important;
    border-radius: 8px !important;
    border: 2px solid rgba(255, 255, 255, 0.3) !important;
    margin-bottom: 0.75rem !important;
    transition: all 0.2s ease !important;
}

/* Add "🏠 Home" text */
[data-testid="stSidebarNav"] ul li:first-child a::before {
    content: "🏠 Home" !important;
    font-size: 1.1rem !important;
    color: #FFFFFF !important;
    font-weight: 700 !important;
    display: block !important;
}

/* Hover effect for Home button */
[data-testid="stSidebarNav"] ul li:first-child a:hover {
    background: rgba(255, 255, 255, 0.3) !important;
    border-color: rgba(255, 255, 255, 0.5) !important;
    transform: translateY(-2px) !important;
}

@media (max-width: 768px) {
    [data-testid="stSidebar"] {
        background: linear-gradient(135deg, #4A3D6F 0%, #6F5F96 100%) !important;
    }
    
    [data-testid="stSidebar"] * {
        color: white !important;
    }
}
</style>
""", unsafe_allow_html=True)

# ============================================================================
# SIDEBAR
# ============================================================================
from utils.standard_sidebar import render_standard_sidebar, get_sidebar_date_range, get_sidebar_membership_size

with st.sidebar:
    st.markdown("### 📈 Historical Tracking Filters")
    
    # Date range
    start_date, end_date = get_sidebar_date_range()
    
    # Measure filter
    measure_options = ["All Measures"] + ["CDC", "CBP", "COL", "BCS", "EED", "KED", "SPC", "FUM", "AMM"]
    selected_measure = st.selectbox("Select Measure", measure_options)
    
    # Display mode
    display_mode = st.radio("Display Mode", ["Monthly Trends", "Year-over-Year", "Forecast"], index=0)
    
    # Database status
    try:
        from utils.database import get_connection
        conn, count = get_connection()
        if conn:
            st.success(f"✅ Database Connected ({count:,} records)")
        else:
            st.warning("⚠️ Database connection issue")
    except Exception as e:
        st.warning("⚠️ Database status unavailable")

# ============================================================================
# MAIN CONTENT
# ============================================================================
st.markdown("<h1 style='text-align: center; font-size: 1.8rem !important; font-weight: 600;'>📈 Historical Performance Tracking</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; margin-top: 0; margin-bottom: 0.75rem; font-size: 1rem;'>Track HEDIS measure performance over time with forecasting capabilities</p>", unsafe_allow_html=True)
try:
    from utils.validation_badges import validation_badge_html
    st.markdown(validation_badge_html("Validated against 20+ historical interventions and prior-year actuals", compact=True), unsafe_allow_html=True)
except ImportError:
    st.markdown("<div style='background:#f0fdf4;border:1px solid #10B981;border-radius:6px;padding:0.35rem 0.75rem;margin:0.5rem 0;font-size:0.85rem;'><span style='color:#065f46;font-weight:600;'>✓ Validated against 20+ historical interventions</span></div>", unsafe_allow_html=True)

# Status Overview Section
try:
    tracker_status = HistoricalTracker()
    status_df = tracker_status.get_all_measures_status(target_success_rate=85.0)
    
    if not status_df.empty:
        st.markdown("### 📊 Measure Status Overview")
        
        # Status counts
        col_status1, col_status2, col_status3, col_status4 = st.columns(4)
        with col_status1:
            on_track = len(status_df[status_df['status'] == 'on_track'])
            st.metric("✅ On Track", on_track, delta=None)
        with col_status2:
            at_risk = len(status_df[status_df['status'] == 'at_risk'])
            st.metric("⚠️ At Risk", at_risk, delta=None)
        with col_status3:
            critical = len(status_df[status_df['status'] == 'critical'])
            st.metric("🔴 Critical", critical, delta=None)
        with col_status4:
            unknown = len(status_df[status_df['status'] == 'unknown'])
            st.metric("❓ Unknown", unknown, delta=None)
        
        # Status table with color coding
        st.markdown("##### Status Table")
        status_display = status_df.copy()
        status_display['status_display'] = status_display['status'].map({
            'on_track': '✅ On Track',
            'at_risk': '⚠️ At Risk',
            'critical': '🔴 Critical',
            'unknown': '❓ Unknown'
        })
        status_display['trend_display'] = status_display['trend'].map({
            'improving': '📈 Improving',
            'declining': '📉 Declining',
            'stable': '➡️ Stable'
        })
        status_display = status_display.round(2)
        st.dataframe(
            status_display[['measure_name', 'status_display', 'current_rate', 'target_rate', 
                           'variance', 'trend_display']].rename(columns={
                'measure_name': 'Measure',
                'status_display': 'Status',
                'current_rate': 'Current Rate (%)',
                'target_rate': 'Target Rate (%)',
                'variance': 'Variance (%)',
                'trend_display': 'Trend'
            }),
            use_container_width=True,
            hide_index=True
        )
        
        # Status distribution pie chart
        if len(status_df[status_df['status'] != 'unknown']) > 0:
            status_counts = status_df[status_df['status'] != 'unknown']['status'].value_counts()
            status_labels = {
                'on_track': '✅ On Track',
                'at_risk': '⚠️ At Risk',
                'critical': '🔴 Critical'
            }
            status_counts_display = pd.DataFrame({
                'Status': [status_labels.get(s, s) for s in status_counts.index],
                'Count': status_counts.values
            })
            
            fig_status_pie = px.pie(
                status_counts_display,
                values='Count',
                names='Status',
                title="Measure Status Distribution",
                color_discrete_map={
                    '✅ On Track': '#4CAF50',
                    '⚠️ At Risk': '#FF9800',
                    '🔴 Critical': '#F44336'
                }
            )
            fig_status_pie.update_layout(height=400)
            st.plotly_chart(fig_status_pie, use_container_width=True)
        
        st.markdown("---")

except Exception as e:
    st.warning(f"⚠️ Could not load status overview: {str(e)}")

try:
    # Initialize tracker
    tracker = HistoricalTracker()
    
    # Get measure ID if not "All Measures"
    measure_id = None if selected_measure == "All Measures" else selected_measure
    
    if display_mode == "Monthly Trends":
        st.markdown("### Monthly Performance Trends")
        
        # Get monthly trends
        df = tracker.get_monthly_trends(
            measure_id=measure_id,
            start_date=start_date.strftime("%Y-%m-%d"),
            end_date=end_date.strftime("%Y-%m-%d")
        )
        
        if df.empty:
            st.info("📊 No data available for the selected date range and measure.")
        else:
            # Display summary metrics
            col1, col2, col3, col4, col5 = st.columns(5)
            with col1:
                st.metric("Total Interventions", f"{df['total_interventions'].sum():,}")
            with col2:
                st.metric("Successful Closures", f"{df['successful_closures'].sum():,}")
            with col3:
                avg_success_rate = df['success_rate'].mean() if 'success_rate' in df.columns else 0
                st.metric("Avg Success Rate", f"{avg_success_rate:.1f}%")
            with col4:
                total_cost = df['total_cost'].sum() if 'total_cost' in df.columns else 0
                st.metric("Total Cost", f"${total_cost:,.2f}")
            with col5:
                total_revenue = df['revenue'].sum() if 'revenue' in df.columns else 0
                st.metric("Total Revenue", f"${total_revenue:,.2f}")
            
            # Create tabs for different visualizations
            # Centered tab selection using radio buttons
            st.markdown("<div style='display: flex; justify-content: center; margin: 1rem 0;'>", unsafe_allow_html=True)
            selected_tab = st.radio(
                "Select View",
                [
                    "📈 Intervention Trends", 
                    "✅ Success Rate Trends", 
                    "💰 Cost & Revenue Analysis",
                    "📊 Measure Comparison",
                    "🌡️ Seasonal Patterns",
                    "📋 Data Tables"
                ],
                horizontal=True,
                label_visibility="collapsed",
                key="tabs_historical_1"
            )
            st.markdown("</div>", unsafe_allow_html=True)
            
            # CSS to center radio buttons
            st.markdown("""
            <style>
            div[data-testid="stRadio"] > div {
                justify-content: center !important;
                display: flex !important;
            }
            div[data-testid="stRadio"] > div[role="radiogroup"] {
                justify-content: center !important;
                display: flex !important;
                gap: 1rem !important;
            }
            </style>
            """, unsafe_allow_html=True)
            
            st.markdown("---")
            
            # Display content based on selection
            if selected_tab == "📈 Intervention Trends":
                st.markdown("#### Monthly Intervention Volume Trends")
                if 'month_start' in df.columns and 'total_interventions' in df.columns:
                    # Line chart for interventions
                    fig_line = px.line(
                        df,
                        x='month_start',
                        y='total_interventions',
                        color='measure_name' if 'measure_name' in df.columns else None,
                        title="Monthly Intervention Trends",
                        labels={'month_start': 'Month', 'total_interventions': 'Total Interventions'},
                        markers=True
                    )
                    fig_line.update_layout(height=500, xaxis_title="Month", yaxis_title="Interventions")
                    st.plotly_chart(fig_line, use_container_width=True)
                    
                    # Area chart for cumulative trends
                    df_sorted = df.sort_values('month_start')
                    df_sorted['cumulative_interventions'] = df_sorted.groupby('measure_name' if 'measure_name' in df.columns else None)['total_interventions'].cumsum()
                    
                    fig_area = px.area(
                        df_sorted,
                        x='month_start',
                        y='cumulative_interventions',
                        color='measure_name' if 'measure_name' in df.columns else None,
                        title="Cumulative Intervention Trends",
                        labels={'month_start': 'Month', 'cumulative_interventions': 'Cumulative Interventions'}
                    )
                    fig_area.update_layout(height=400, xaxis_title="Month", yaxis_title="Cumulative Interventions")
                    st.plotly_chart(fig_area, use_container_width=True)
            
            elif selected_tab == "✅ Success Rate Trends":
                st.markdown("#### Success Rate Trends Over Time")
                if 'month_start' in df.columns and 'success_rate' in df.columns:
                    # Success rate line chart
                    fig_success = px.line(
                        df,
                        x='month_start',
                        y='success_rate',
                        color='measure_name' if 'measure_name' in df.columns else None,
                        title="Success Rate Trends",
                        labels={'month_start': 'Month', 'success_rate': 'Success Rate (%)'},
                        markers=True
                    )
                    # Add target line at 85%
                    fig_success.add_hline(y=85, line_dash="dash", line_color="red", 
                                         annotation_text="Target: 85%", annotation_position="right")
                    fig_success.update_layout(height=500, xaxis_title="Month", yaxis_title="Success Rate (%)")
                    st.plotly_chart(fig_success, use_container_width=True)
                    
                    # Bar chart comparing success rates by measure
                    if 'measure_name' in df.columns:
                        measure_avg = df.groupby('measure_name')['success_rate'].mean().reset_index()
                        measure_avg = measure_avg.sort_values('success_rate', ascending=False)
                        
                        fig_bar = px.bar(
                            measure_avg,
                            x='measure_name',
                            y='success_rate',
                            title="Average Success Rate by Measure",
                            labels={'measure_name': 'Measure', 'success_rate': 'Average Success Rate (%)'},
                            color='success_rate',
                            color_continuous_scale='RdYlGn'
                        )
                        fig_bar.add_hline(y=85, line_dash="dash", line_color="red", 
                                         annotation_text="Target: 85%")
                        fig_bar.update_layout(height=400, xaxis_title="Measure", yaxis_title="Success Rate (%)")
                        st.plotly_chart(fig_bar, use_container_width=True)
            
            elif selected_tab == "💰 Cost & Revenue Analysis":
                st.markdown("#### Cost & Revenue Analysis")
                if 'month_start' in df.columns:
                    col_cost1, col_cost2 = st.columns(2)
                    
                    with col_cost1:
                        # Cost trend
                        if 'total_cost' in df.columns:
                            fig_cost = px.line(
                                df,
                                x='month_start',
                                y='total_cost',
                                color='measure_name' if 'measure_name' in df.columns else None,
                                title="Monthly Cost Trends",
                                labels={'month_start': 'Month', 'total_cost': 'Total Cost ($)'},
                                markers=True
                            )
                            fig_cost.update_layout(height=400, xaxis_title="Month", yaxis_title="Cost ($)")
                            st.plotly_chart(fig_cost, use_container_width=True)
                    
                    with col_cost2:
                        # Revenue trend
                        if 'revenue' in df.columns:
                            fig_revenue = px.line(
                                df,
                                x='month_start',
                                y='revenue',
                                color='measure_name' if 'measure_name' in df.columns else None,
                                title="Monthly Revenue Trends",
                                labels={'month_start': 'Month', 'revenue': 'Revenue ($)'},
                                markers=True
                            )
                            fig_revenue.update_layout(height=400, xaxis_title="Month", yaxis_title="Revenue ($)")
                            st.plotly_chart(fig_revenue, use_container_width=True)
                    
                    # ROI calculation and chart
                    if 'total_cost' in df.columns and 'revenue' in df.columns:
                        df_roi = df.copy()
                        df_roi['roi_ratio'] = df_roi['revenue'] / df_roi['total_cost'].replace(0, np.nan)
                        df_roi['roi_ratio'] = df_roi['roi_ratio'].fillna(0)
                        
                        st.markdown("##### ROI Trends")
                        fig_roi = px.line(
                            df_roi,
                            x='month_start',
                            y='roi_ratio',
                            color='measure_name' if 'measure_name' in df.columns else None,
                            title="ROI Ratio Trends Over Time",
                            labels={'month_start': 'Month', 'roi_ratio': 'ROI Ratio'},
                            markers=True
                        )
                        fig_roi.add_hline(y=1.0, line_dash="dash", line_color="gray", 
                                         annotation_text="Break-even: 1.0x")
                        fig_roi.update_layout(height=400, xaxis_title="Month", yaxis_title="ROI Ratio")
                        st.plotly_chart(fig_roi, use_container_width=True)
            
            elif selected_tab == "📊 Measure Comparison":
                st.markdown("#### Measure Comparison Charts")
                if 'measure_name' in df.columns:
                    # Grouped bar chart comparing measures
                    measure_summary = df.groupby('measure_name').agg({
                        'total_interventions': 'sum',
                        'successful_closures': 'sum',
                        'success_rate': 'mean',
                        'total_cost': 'sum',
                        'revenue': 'sum'
                    }).reset_index()
                    
                    col_comp1, col_comp2 = st.columns(2)
                    
                    with col_comp1:
                        # Interventions by measure
                        fig_interventions = px.bar(
                            measure_summary.sort_values('total_interventions', ascending=False),
                            x='measure_name',
                            y='total_interventions',
                            title="Total Interventions by Measure",
                            labels={'measure_name': 'Measure', 'total_interventions': 'Total Interventions'},
                            color='total_interventions',
                            color_continuous_scale='Blues'
                        )
                        fig_interventions.update_layout(height=400, xaxis_title="Measure", yaxis_title="Interventions")
                        st.plotly_chart(fig_interventions, use_container_width=True)
                    
                    with col_comp2:
                        # Success rate by measure
                        fig_success_comp = px.bar(
                            measure_summary.sort_values('success_rate', ascending=False),
                            x='measure_name',
                            y='success_rate',
                            title="Average Success Rate by Measure",
                            labels={'measure_name': 'Measure', 'success_rate': 'Success Rate (%)'},
                            color='success_rate',
                            color_continuous_scale='RdYlGn'
                        )
                        fig_success_comp.add_hline(y=85, line_dash="dash", line_color="red")
                        fig_success_comp.update_layout(height=400, xaxis_title="Measure", yaxis_title="Success Rate (%)")
                        st.plotly_chart(fig_success_comp, use_container_width=True)
                    
                    # Scatter plot: Cost vs Success Rate
                    if 'total_cost' in measure_summary.columns:
                        measure_summary['avg_cost_per_intervention'] = measure_summary['total_cost'] / measure_summary['total_interventions'].replace(0, np.nan)
                        
                        fig_scatter = px.scatter(
                            measure_summary,
                            x='avg_cost_per_intervention',
                            y='success_rate',
                            size='total_interventions',
                            color='measure_name',
                            title="Cost Efficiency vs Success Rate",
                            labels={
                                'avg_cost_per_intervention': 'Avg Cost per Intervention ($)',
                                'success_rate': 'Success Rate (%)'
                            },
                            hover_data=['measure_name', 'total_interventions']
                        )
                        fig_scatter.update_layout(height=500, xaxis_title="Avg Cost per Intervention ($)", 
                                                yaxis_title="Success Rate (%)")
                        st.plotly_chart(fig_scatter, use_container_width=True)
            
            elif selected_tab == "🌡️ Seasonal Patterns":
                st.markdown("#### Seasonal Pattern Analysis")
                # Detect seasonal patterns
                seasonal_data = tracker.detect_seasonal_patterns(
                    measure_id=measure_id,
                    start_date=start_date.strftime("%Y-%m-%d"),
                    end_date=end_date.strftime("%Y-%m-%d")
                )
                
                if seasonal_data.get('has_seasonality'):
                    col_season1, col_season2 = st.columns(2)
                    
                    with col_season1:
                        st.metric("Peak Performance Month", seasonal_data.get('peak_month', 'N/A'))
                    with col_season2:
                        st.metric("Lowest Performance Month", seasonal_data.get('low_month', 'N/A'))
                    
                    st.info(f"📊 Seasonal variance detected: {seasonal_data.get('seasonal_variance', 0):.2f}%")
                    
                    # Monthly averages heatmap
                    if 'monthly_averages' in seasonal_data:
                        monthly_avg = seasonal_data['monthly_averages']
                        months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 
                                 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
                        heatmap_data = []
                        for month in months:
                            month_num = months.index(month) + 1
                            if month_num in monthly_avg:
                                heatmap_data.append({'Month': month, 'Success Rate': monthly_avg[month_num]})
                        
                        if heatmap_data:
                            df_heatmap = pd.DataFrame(heatmap_data)
                            fig_heatmap = px.bar(
                                df_heatmap,
                                x='Month',
                                y='Success Rate',
                                title="Average Success Rate by Month",
                                labels={'Success Rate': 'Success Rate (%)'},
                                color='Success Rate',
                                color_continuous_scale='RdYlGn'
                            )
                            fig_heatmap.update_layout(height=400, xaxis_title="Month", yaxis_title="Success Rate (%)")
                            st.plotly_chart(fig_heatmap, use_container_width=True)
                else:
                    st.info("📊 No significant seasonal patterns detected in the data.")
            
            elif selected_tab == "📋 Data Tables":
                st.markdown("#### Detailed Data Tables")
                
                # Summary table by measure
                if 'measure_name' in df.columns:
                    st.markdown("##### Summary by Measure")
                    measure_summary_table = df.groupby('measure_name').agg({
                        'total_interventions': 'sum',
                        'successful_closures': 'sum',
                        'success_rate': 'mean',
                        'total_cost': 'sum',
                        'revenue': 'sum'
                    }).reset_index()
                    measure_summary_table['avg_cost_per_intervention'] = (
                        measure_summary_table['total_cost'] / 
                        measure_summary_table['total_interventions'].replace(0, np.nan)
                    )
                    measure_summary_table['roi_ratio'] = (
                        measure_summary_table['revenue'] / 
                        measure_summary_table['total_cost'].replace(0, np.nan)
                    )
                    measure_summary_table = measure_summary_table.round(2)
                    st.dataframe(measure_summary_table, use_container_width=True)
                
                # Monthly detailed table
                st.markdown("##### Monthly Detailed Data")
                with st.expander("📋 View All Monthly Data", expanded=False):
                    st.dataframe(df, use_container_width=True)
                
                # Export option
                st.download_button(
                    label="📥 Download Data as CSV",
                    data=df.to_csv(index=False),
                    file_name=f"historical_tracking_{start_date.strftime('%Y%m%d')}_{end_date.strftime('%Y%m%d')}.csv",
                    mime="text/csv"
                )
    
    elif display_mode == "Year-over-Year":
        st.markdown("### Year-over-Year Comparison")
        
        # Get YoY comparison
        current_year = datetime.now().year
        df_yoy = tracker.get_year_over_year_comparison(
            measure_id=measure_id,
            current_year=current_year
        )
        
        if df_yoy.empty:
            st.info("📊 No year-over-year data available.")
        else:
            # Summary metrics
            col_yoy1, col_yoy2, col_yoy3, col_yoy4 = st.columns(4)
            with col_yoy1:
                avg_change = df_yoy['success_rate_change'].mean() if 'success_rate_change' in df_yoy.columns else 0
                st.metric("Avg Success Rate Change", f"{avg_change:+.1f}%")
            with col_yoy2:
                total_revenue_change = df_yoy['revenue_change'].sum() if 'revenue_change' in df_yoy.columns else 0
                st.metric("Total Revenue Change", f"${total_revenue_change:+,.2f}")
            with col_yoy3:
                measures_improved = len(df_yoy[df_yoy['success_rate_change'] > 0]) if 'success_rate_change' in df_yoy.columns else 0
                st.metric("Measures Improved", f"{measures_improved}/{len(df_yoy)}")
            with col_yoy4:
                avg_revenue_pct = df_yoy['revenue_change_pct'].mean() if 'revenue_change_pct' in df_yoy.columns else 0
                st.metric("Avg Revenue Change %", f"{avg_revenue_pct:+.1f}%")
            
            # Create tabs for YoY visualizations
            # Centered tab selection using radio buttons
            st.markdown("<div style='display: flex; justify-content: center; margin: 1rem 0;'>", unsafe_allow_html=True)
            selected_tab_yoy = st.radio(
                "Select View",
                [
                    "📊 Comparison Charts",
                    "📈 Change Analysis",
                    "💰 Revenue Impact",
                    "📋 Data Tables"
                ],
                horizontal=True,
                label_visibility="collapsed",
                key="tabs_historical_2"
            )
            st.markdown("</div>", unsafe_allow_html=True)
            
            # CSS to center radio buttons
            st.markdown("""
            <style>
            div[data-testid="stRadio"] > div {
                justify-content: center !important;
                display: flex !important;
            }
            div[data-testid="stRadio"] > div[role="radiogroup"] {
                justify-content: center !important;
                display: flex !important;
                gap: 1rem !important;
            }
            </style>
            """, unsafe_allow_html=True)
            
            st.markdown("---")
            
            # Display content based on selection
            if selected_tab_yoy == "📊 Comparison Charts":
                st.markdown("#### Year-over-Year Comparison Charts")
                
                col_chart1, col_chart2 = st.columns(2)
                
                with col_chart1:
                    # Success rate comparison
                    if 'current_success_rate' in df_yoy.columns and 'previous_success_rate' in df_yoy.columns:
                        df_comparison = df_yoy[['measure_name', 'current_success_rate', 'previous_success_rate']].copy()
                        df_comparison = df_comparison.melt(
                            id_vars=['measure_name'],
                            value_vars=['current_success_rate', 'previous_success_rate'],
                            var_name='Period',
                            value_name='Success Rate'
                        )
                        df_comparison['Period'] = df_comparison['Period'].replace({
                            'current_success_rate': f'{current_year} YTD',
                            'previous_success_rate': f'{current_year - 1} Full Year'
                        })
                        
                        fig_comparison = px.bar(
                            df_comparison,
                            x='measure_name',
                            y='Success Rate',
                            color='Period',
                            barmode='group',
                            title="Success Rate: Current vs Previous Year",
                            labels={'measure_name': 'Measure', 'Success Rate': 'Success Rate (%)'}
                        )
                        fig_comparison.add_hline(y=85, line_dash="dash", line_color="red", 
                                                annotation_text="Target: 85%")
                        fig_comparison.update_layout(height=500, xaxis_title="Measure", yaxis_title="Success Rate (%)")
                        st.plotly_chart(fig_comparison, use_container_width=True)
                
                with col_chart2:
                    # Intervention volume comparison
                    if 'current_interventions' in df_yoy.columns and 'previous_interventions' in df_yoy.columns:
                        df_interventions = df_yoy[['measure_name', 'current_interventions', 'previous_interventions']].copy()
                        df_interventions = df_interventions.melt(
                            id_vars=['measure_name'],
                            value_vars=['current_interventions', 'previous_interventions'],
                            var_name='Period',
                            value_name='Interventions'
                        )
                        df_interventions['Period'] = df_interventions['Period'].replace({
                            'current_interventions': f'{current_year} YTD',
                            'previous_interventions': f'{current_year - 1} Full Year'
                        })
                        
                        fig_interventions_yoy = px.bar(
                            df_interventions,
                            x='measure_name',
                            y='Interventions',
                            color='Period',
                            barmode='group',
                            title="Intervention Volume: Current vs Previous Year",
                            labels={'measure_name': 'Measure', 'Interventions': 'Total Interventions'}
                        )
                        fig_interventions_yoy.update_layout(height=500, xaxis_title="Measure", yaxis_title="Interventions")
                        st.plotly_chart(fig_interventions_yoy, use_container_width=True)
            
            elif selected_tab_yoy == "📈 Change Analysis":
                st.markdown("#### Change Analysis")
                
                # Success rate change chart
                if 'success_rate_change' in df_yoy.columns:
                    df_yoy_sorted = df_yoy.sort_values('success_rate_change', ascending=True)
                    
                    fig_change = px.bar(
                        df_yoy_sorted,
                        x='measure_name',
                        y='success_rate_change',
                        title="Success Rate Change (Current vs Previous Year)",
                        labels={'measure_name': 'Measure', 'success_rate_change': 'Change (%)'},
                        color='success_rate_change',
                        color_continuous_scale='RdYlGn'
                    )
                    fig_change.add_hline(y=0, line_dash="dash", line_color="gray")
                    fig_change.update_layout(height=500, xaxis_title="Measure", yaxis_title="Change (%)")
                    st.plotly_chart(fig_change, use_container_width=True)
                    
                    # Waterfall-style chart showing improvements/declines
                    improving = df_yoy[df_yoy['success_rate_change'] > 0]
                    declining = df_yoy[df_yoy['success_rate_change'] <= 0]
                    
                    col_improve, col_decline = st.columns(2)
                    
                    with col_improve:
                        st.markdown("##### ✅ Improving Measures")
                        if not improving.empty:
                            fig_improve = px.bar(
                                improving.sort_values('success_rate_change', ascending=False),
                                x='measure_name',
                                y='success_rate_change',
                                title="Improving Measures",
                                labels={'measure_name': 'Measure', 'success_rate_change': 'Improvement (%)'},
                                color='success_rate_change',
                                color_continuous_scale='Greens'
                            )
                            fig_improve.update_layout(height=400, xaxis_title="Measure", yaxis_title="Improvement (%)")
                            st.plotly_chart(fig_improve, use_container_width=True)
                        else:
                            st.info("No measures showing improvement.")
                    
                    with col_decline:
                        st.markdown("##### ⚠️ Declining Measures")
                        if not declining.empty:
                            fig_decline = px.bar(
                                declining.sort_values('success_rate_change', ascending=True),
                                x='measure_name',
                                y='success_rate_change',
                                title="Declining Measures",
                                labels={'measure_name': 'Measure', 'success_rate_change': 'Decline (%)'},
                                color='success_rate_change',
                                color_continuous_scale='Reds'
                            )
                            fig_decline.update_layout(height=400, xaxis_title="Measure", yaxis_title="Decline (%)")
                            st.plotly_chart(fig_decline, use_container_width=True)
                        else:
                            st.info("No measures showing decline.")
            
            elif selected_tab_yoy == "💰 Revenue Impact":
                st.markdown("#### Revenue Impact Analysis")
                
                # Revenue change chart
                if 'revenue_change' in df_yoy.columns:
                    df_revenue_sorted = df_yoy.sort_values('revenue_change', ascending=True)
                    
                    fig_revenue_yoy = px.bar(
                        df_revenue_sorted,
                        x='measure_name',
                        y='revenue_change',
                        title="Revenue Change: Current vs Previous Year",
                        labels={'measure_name': 'Measure', 'revenue_change': 'Revenue Change ($)'},
                        color='revenue_change',
                        color_continuous_scale='RdYlGn'
                    )
                    fig_revenue_yoy.add_hline(y=0, line_dash="dash", line_color="gray")
                    fig_revenue_yoy.update_layout(height=500, xaxis_title="Measure", yaxis_title="Revenue Change ($)")
                    st.plotly_chart(fig_revenue_yoy, use_container_width=True)
                    
                    # Revenue percentage change
                    if 'revenue_change_pct' in df_yoy.columns:
                        fig_revenue_pct = px.bar(
                            df_yoy.sort_values('revenue_change_pct', ascending=True),
                            x='measure_name',
                            y='revenue_change_pct',
                            title="Revenue Change Percentage",
                            labels={'measure_name': 'Measure', 'revenue_change_pct': 'Change (%)'},
                            color='revenue_change_pct',
                            color_continuous_scale='RdYlGn'
                        )
                        fig_revenue_pct.add_hline(y=0, line_dash="dash", line_color="gray")
                        fig_revenue_pct.update_layout(height=400, xaxis_title="Measure", yaxis_title="Change (%)")
                        st.plotly_chart(fig_revenue_pct, use_container_width=True)
                    
                    # Summary metrics
                    st.markdown("##### Revenue Impact Summary")
                    col_rev1, col_rev2, col_rev3 = st.columns(3)
                    with col_rev1:
                        positive_revenue = df_yoy[df_yoy['revenue_change'] > 0]['revenue_change'].sum()
                        st.metric("Positive Revenue Impact", f"${positive_revenue:,.2f}")
                    with col_rev2:
                        negative_revenue = df_yoy[df_yoy['revenue_change'] < 0]['revenue_change'].sum()
                        st.metric("Negative Revenue Impact", f"${negative_revenue:,.2f}")
                    with col_rev3:
                        net_revenue = df_yoy['revenue_change'].sum()
                        st.metric("Net Revenue Change", f"${net_revenue:,.2f}")
            
            elif selected_tab_yoy == "📋 Data Tables":
                st.markdown("#### Year-over-Year Data Tables")
                
                # Formatted comparison table
                st.markdown("##### Detailed Comparison Table")
                df_yoy_display = df_yoy.copy()
                df_yoy_display = df_yoy_display.round(2)
                st.dataframe(df_yoy_display, use_container_width=True)
                
                # Summary table
                st.markdown("##### Summary Statistics")
                summary_stats = {
                    'Metric': [
                        'Total Measures',
                        'Measures Improved',
                        'Measures Declined',
                        'Avg Success Rate Change',
                        'Total Revenue Change',
                        'Avg Revenue Change %'
                    ],
                    'Value': [
                        len(df_yoy),
                        len(df_yoy[df_yoy['success_rate_change'] > 0]) if 'success_rate_change' in df_yoy.columns else 0,
                        len(df_yoy[df_yoy['success_rate_change'] <= 0]) if 'success_rate_change' in df_yoy.columns else 0,
                        f"{df_yoy['success_rate_change'].mean():+.2f}%" if 'success_rate_change' in df_yoy.columns else "N/A",
                        f"${df_yoy['revenue_change'].sum():,.2f}" if 'revenue_change' in df_yoy.columns else "N/A",
                        f"{df_yoy['revenue_change_pct'].mean():+.2f}%" if 'revenue_change_pct' in df_yoy.columns else "N/A"
                    ]
                }
                df_summary = pd.DataFrame(summary_stats)
                st.dataframe(df_summary, use_container_width=True, hide_index=True)
                
                # Export option
                st.download_button(
                    label="📥 Download YoY Data as CSV",
                    data=df_yoy.to_csv(index=False),
                    file_name=f"yoy_comparison_{current_year}.csv",
                    mime="text/csv"
                )
    
    elif display_mode == "Forecast":
        st.markdown("### Performance Forecast")
        
        # Get forecast data
        forecast_df = tracker.forecast_next_quarter(
            measure_id=measure_id,
            method="prophet"
        )
        
        if forecast_df.empty:
            st.info("🔮 Forecasting requires at least 3 months of historical data. Please select a date range with sufficient data.")
        else:
            # Get historical data for comparison
            historical_df = tracker.get_monthly_trends(
                measure_id=measure_id,
                start_date=(datetime.now() - timedelta(days=365)).strftime("%Y-%m-%d"),
                end_date=datetime.now().strftime("%Y-%m-%d")
            )
            
            # Display forecast summary metrics
            col_fc1, col_fc2, col_fc3, col_fc4 = st.columns(4)
            with col_fc1:
                avg_forecast_rate = forecast_df['forecasted_success_rate'].mean() if 'forecasted_success_rate' in forecast_df.columns else 0
                st.metric("Avg Forecasted Success Rate", f"{avg_forecast_rate:.1f}%")
            with col_fc2:
                total_forecast_interventions = forecast_df['forecasted_interventions'].sum() if 'forecasted_interventions' in forecast_df.columns else 0
                st.metric("Forecasted Interventions", f"{total_forecast_interventions:,.0f}")
            with col_fc3:
                total_forecast_revenue = forecast_df['forecasted_revenue'].sum() if 'forecasted_revenue' in forecast_df.columns else 0
                st.metric("Forecasted Revenue", f"${total_forecast_revenue:,.2f}")
            with col_fc4:
                total_forecast_closures = forecast_df['forecasted_closures'].sum() if 'forecasted_closures' in forecast_df.columns else 0
                st.metric("Forecasted Closures", f"{total_forecast_closures:,.0f}")
            
            # Create tabs for forecast visualizations
            # Centered tab selection using radio buttons
            st.markdown("<div style='display: flex; justify-content: center; margin: 1rem 0;'>", unsafe_allow_html=True)
            selected_tab_fc = st.radio(
                "Select View",
                [
                    "📈 Forecast Trends",
                    "📊 Historical vs Forecast",
                    "📋 Forecast Data"
                ],
                horizontal=True,
                label_visibility="collapsed",
                key="tabs_historical_3"
            )
            st.markdown("</div>", unsafe_allow_html=True)
            
            # CSS to center radio buttons
            st.markdown("""
            <style>
            div[data-testid="stRadio"] > div {
                justify-content: center !important;
                display: flex !important;
            }
            div[data-testid="stRadio"] > div[role="radiogroup"] {
                justify-content: center !important;
                display: flex !important;
                gap: 1rem !important;
            }
            </style>
            """, unsafe_allow_html=True)
            
            st.markdown("---")
            
            # Display content based on selection
            if selected_tab_fc == "📈 Forecast Trends":
                st.markdown("#### Next Quarter Forecast")
                
                # Forecast success rate chart
                if 'forecasted_success_rate' in forecast_df.columns:
                    fig_forecast_rate = px.line(
                        forecast_df,
                        x='month_start',
                        y='forecasted_success_rate',
                        title="Forecasted Success Rate - Next 3 Months",
                        labels={'month_start': 'Month', 'forecasted_success_rate': 'Success Rate (%)'},
                        markers=True
                    )
                    fig_forecast_rate.add_hline(y=85, line_dash="dash", line_color="red", 
                                               annotation_text="Target: 85%")
                    fig_forecast_rate.update_layout(height=400, xaxis_title="Month", yaxis_title="Success Rate (%)")
                    st.plotly_chart(fig_forecast_rate, use_container_width=True)
                
                # Forecast interventions chart
                if 'forecasted_interventions' in forecast_df.columns:
                    fig_forecast_int = px.bar(
                        forecast_df,
                        x='month_start',
                        y='forecasted_interventions',
                        title="Forecasted Intervention Volume - Next 3 Months",
                        labels={'month_start': 'Month', 'forecasted_interventions': 'Interventions'},
                        color='forecasted_interventions',
                        color_continuous_scale='Blues'
                    )
                    fig_forecast_int.update_layout(height=400, xaxis_title="Month", yaxis_title="Interventions")
                    st.plotly_chart(fig_forecast_int, use_container_width=True)
                
                # Forecast revenue chart
                if 'forecasted_revenue' in forecast_df.columns:
                    fig_forecast_rev = px.area(
                        forecast_df,
                        x='month_start',
                        y='forecasted_revenue',
                        title="Forecasted Revenue - Next 3 Months",
                        labels={'month_start': 'Month', 'forecasted_revenue': 'Revenue ($)'}
                    )
                    fig_forecast_rev.update_layout(height=400, xaxis_title="Month", yaxis_title="Revenue ($)")
                    st.plotly_chart(fig_forecast_rev, use_container_width=True)
            
            elif selected_tab_fc == "📊 Historical vs Forecast":
                st.markdown("#### Historical Trends vs Forecast")
                
                if not historical_df.empty and 'month_start' in historical_df.columns:
                    # Combine historical and forecast data
                    historical_df['month_start'] = pd.to_datetime(historical_df['month_start'])
                    forecast_df['month_start'] = pd.to_datetime(forecast_df['month_start'])
                    
                    # Success rate comparison
                    if 'success_rate' in historical_df.columns and 'forecasted_success_rate' in forecast_df.columns:
                        # Get last 6 months of historical data
                        recent_historical = historical_df.tail(6).copy()
                        
                        # Combine for visualization
                        recent_historical['type'] = 'Historical'
                        forecast_display = forecast_df[['month_start', 'forecasted_success_rate']].copy()
                        forecast_display = forecast_display.rename(columns={'forecasted_success_rate': 'success_rate'})
                        forecast_display['type'] = 'Forecast'
                        
                        combined_df = pd.concat([
                            recent_historical[['month_start', 'success_rate', 'type']],
                            forecast_display[['month_start', 'success_rate', 'type']]
                        ], ignore_index=True)
                        
                        fig_combined = px.line(
                            combined_df,
                            x='month_start',
                            y='success_rate',
                            color='type',
                            title="Historical vs Forecasted Success Rate",
                            labels={'month_start': 'Month', 'success_rate': 'Success Rate (%)', 'type': 'Data Type'},
                            markers=True,
                            line_dash='type'
                        )
                        fig_combined.add_hline(y=85, line_dash="dash", line_color="red", 
                                              annotation_text="Target: 85%")
                        fig_combined.update_layout(height=500, xaxis_title="Month", yaxis_title="Success Rate (%)")
                        st.plotly_chart(fig_combined, use_container_width=True)
                    
                    # Intervention volume comparison
                    if 'total_interventions' in historical_df.columns and 'forecasted_interventions' in forecast_df.columns:
                        recent_historical_int = historical_df.tail(6).copy()
                        recent_historical_int['type'] = 'Historical'
                        forecast_display_int = forecast_df[['month_start', 'forecasted_interventions']].copy()
                        forecast_display_int = forecast_display_int.rename(columns={'forecasted_interventions': 'total_interventions'})
                        forecast_display_int['type'] = 'Forecast'
                        
                        combined_int = pd.concat([
                            recent_historical_int[['month_start', 'total_interventions', 'type']],
                            forecast_display_int[['month_start', 'total_interventions', 'type']]
                        ], ignore_index=True)
                        
                        fig_combined_int = px.line(
                            combined_int,
                            x='month_start',
                            y='total_interventions',
                            color='type',
                            title="Historical vs Forecasted Intervention Volume",
                            labels={'month_start': 'Month', 'total_interventions': 'Interventions', 'type': 'Data Type'},
                            markers=True,
                            line_dash='type'
                        )
                        fig_combined_int.update_layout(height=500, xaxis_title="Month", yaxis_title="Interventions")
                        st.plotly_chart(fig_combined_int, use_container_width=True)
            
            elif selected_tab_fc == "📋 Forecast Data":
                st.markdown("#### Forecast Data Tables")
                
                # Forecast table
                st.markdown("##### Next Quarter Forecast")
                forecast_display_table = forecast_df.copy()
                forecast_display_table = forecast_display_table.round(2)
                st.dataframe(forecast_display_table, use_container_width=True)
                
                # Forecast summary
                st.markdown("##### Forecast Summary")
                forecast_summary = {
                    'Metric': [
                        'Forecast Period',
                        'Total Forecasted Interventions',
                        'Total Forecasted Closures',
                        'Average Forecasted Success Rate',
                        'Total Forecasted Revenue'
                    ],
                    'Value': [
                        f"{forecast_df['month_start'].min()} to {forecast_df['month_start'].max()}",
                        f"{forecast_df['forecasted_interventions'].sum():,.0f}" if 'forecasted_interventions' in forecast_df.columns else "N/A",
                        f"{forecast_df['forecasted_closures'].sum():,.0f}" if 'forecasted_closures' in forecast_df.columns else "N/A",
                        f"{forecast_df['forecasted_success_rate'].mean():.2f}%" if 'forecasted_success_rate' in forecast_df.columns else "N/A",
                        f"${forecast_df['forecasted_revenue'].sum():,.2f}" if 'forecasted_revenue' in forecast_df.columns else "N/A"
                    ]
                }
                df_forecast_summary = pd.DataFrame(forecast_summary)
                st.dataframe(df_forecast_summary, use_container_width=True, hide_index=True)
                
                # Export option
                st.download_button(
                    label="📥 Download Forecast Data as CSV",
                    data=forecast_df.to_csv(index=False),
                    file_name=f"forecast_{datetime.now().strftime('%Y%m%d')}.csv",
                    mime="text/csv"
                )

except Exception as e:
    st.error(f"❌ Error loading historical tracking data: {str(e)}")
    st.info("💡 Please check your database connection and ensure the required tables exist.")

# ============================================================================
# FOOTER
# ============================================================================
st.markdown("---")
st.markdown("""
<div style='text-align: left; padding: 1rem 0; color: #6b7280; font-size: 0.8rem;'>
    <p style='margin: 0.25rem 0;'><strong>HEDIS Portfolio Optimizer | StarGuard AI</strong></p>
    <p style='margin: 0.25rem 0;'>Built with Streamlit • Plotly • PostgreSQL | Development: 2024-2026</p>
    <p style='margin: 0.25rem 0;'>🔒 Secure AI Architect | Healthcare AI that sees everything, exposes nothing.</p>
    <p style='margin: 0.25rem 0;'>On-premises architecture delivers 2.8-4.1x ROI and $148M+ proven savings while keeping PHI locked down.</p>
    <p style='margin: 0.25rem 0;'>Zero API transmission • HIPAA-first design.</p>
    <p style='margin: 0.25rem 0;'>⚠️ Portfolio demonstration using synthetic data to showcase real methodology.</p>
    <p style='margin: 0.25rem 0;'>© 2024-2026 Robert Reichert | StarGuard AI™</p>
</div>
""", unsafe_allow_html=True)

"""
Page 1: ROI by Measure
Bar chart showing ROI performance across all HEDIS measures
"""
import streamlit as st

st.set_page_config(page_title="ROI by Measure", page_icon="📊", layout="wide")

# Test if CSS is working AT ALL
st.markdown("""
<style>
body {
    background-color: red !important;
}
</style>
""", unsafe_allow_html=True)

st.write("If the background is red, CSS is working")

# Force compact spacing globally
st.markdown("""
<style>
/* Force compact spacing globally */
.main .block-container {
    padding: 1rem 1rem 2rem 1rem !important;
    max-width: 100% !important;
}

/* Reduce gap between all elements */
div[data-testid="stVerticalBlock"] {
    gap: 0.4rem !important;
}

/* Compact columns */
div[data-testid="column"] {
    padding: 0 0.3rem !important;
}

/* Shrink metric cards dramatically */
div[data-testid="stVerticalBlock"] > div[data-testid="element-container"] {
    margin-bottom: 0.3rem !important;
}

/* KPI Card styling */
div[data-testid="stVerticalBlock"] > div > div {
    padding: 0.6rem 0.8rem !important;
    border-radius: 6px !important;
}

/* Compact headings */
h1, h2, h3 {
    margin-top: 0.5rem !important;
    margin-bottom: 0.3rem !important;
    line-height: 1.2 !important;
}

h1 { font-size: 1.6rem !important; }
h2 { font-size: 1.3rem !important; }
h3 { font-size: 0.95rem !important; }

/* Compact paragraphs */
p {
    font-size: 0.8rem !important;
    line-height: 1.35 !important;
    margin: 0.2rem 0 !important;
}

/* Key Insights compact styling */
.stAlert {
    padding: 0.5rem 0.7rem !important;
    margin: 0.4rem 0 !important;
}

.stAlert [data-testid="stMarkdownContainer"] {
    font-size: 0.8rem !important;
    line-height: 1.35 !important;
}

/* Icon adjustments */
.stAlert svg {
    width: 16px !important;
    height: 16px !important;
}

/* Remove excess spacing from metric values */
div[data-testid="stMetricValue"] {
    font-size: 1.6rem !important;
    padding: 0 !important;
    margin: 0.2rem 0 !important;
}

div[data-testid="stMetricLabel"] {
    font-size: 0.85rem !important;
    padding-bottom: 0.2rem !important;
}

div[data-testid="stMetricDelta"] {
    font-size: 0.75rem !important;
    padding-top: 0.1rem !important;
}

/* Mobile optimization */
@media (max-width: 768px) {
    .main .block-container {
        padding: 0.8rem 0.8rem 1.5rem 0.8rem !important;
    }
    
    div[data-testid="column"] > div {
        padding: 0.5rem !important;
    }
    
    h1 { font-size: 1.4rem !important; }
    h2 { font-size: 1.1rem !important; }
    h3 { font-size: 0.9rem !important; }
    
    .stAlert {
        padding: 0.4rem 0.6rem !important;
        font-size: 0.75rem !important;
    }
}

/* Compact ALL metric cards */
div[data-testid="stVerticalBlock"] > div[data-testid="stVerticalBlock"] {
    gap: 0.5rem !important;
}

/* Reduce KPI card padding and size */
div[data-testid="column"] > div {
    padding: 0.8rem !important;
    margin-bottom: 0.5rem !important;
}

/* Make metric titles smaller */
div[data-testid="stMarkdownContainer"] h3,
div[data-testid="stMarkdownContainer"] h2 {
    font-size: 0.95rem !important;
    margin-bottom: 0.4rem !important;
    padding-bottom: 0 !important;
}

/* Compact metric values */
div[data-testid="stMarkdownContainer"] h1 {
    font-size: 1.8rem !important;
    margin: 0.3rem 0 !important;
    line-height: 1.2 !important;
}

/* Compact subtitles */
div[data-testid="stMarkdownContainer"] p {
    font-size: 0.8rem !important;
    margin-top: 0.2rem !important;
    margin-bottom: 0 !important;
}

/* Compact Key Insights section */
.stAlert {
    padding: 0.6rem 0.8rem !important;
    margin-bottom: 0.6rem !important;
}

.stAlert p {
    font-size: 0.85rem !important;
    line-height: 1.4 !important;
    margin: 0 !important;
}

/* Reduce spacing between sections */
.block-container {
    padding-top: 2rem !important;
    padding-bottom: 1rem !important;
}

/* Mobile-specific adjustments */
@media (max-width: 768px) {
    div[data-testid="column"] > div {
        padding: 0.6rem !important;
    }
    
    div[data-testid="stMarkdownContainer"] h1 {
        font-size: 1.5rem !important;
    }
    
    .stAlert {
        padding: 0.5rem 0.6rem !important;
    }
}

/* Compact column layout */
[data-testid="column"] {
    padding: 0 0.4rem !important;
}

/* Reduce card padding */
[data-testid="column"] > div > div {
    padding: 0.7rem 0.9rem !important;
}

/* Compact metric styling */
[data-testid="stMarkdownContainer"] h3 {
    font-size: 0.9rem !important;
    margin-bottom: 0.3rem !important;
    font-weight: 600 !important;
}

[data-testid="stMarkdownContainer"] h1 {
    font-size: 1.7rem !important;
    margin: 0.2rem 0 !important;
    line-height: 1.1 !important;
}

[data-testid="stMarkdownContainer"] p {
    font-size: 0.78rem !important;
    margin-top: 0.2rem !important;
    color: #666 !important;
}

/* Compact row spacing */
.row-widget {
    margin-bottom: 0.6rem !important;
}

/* Key Insights compact */
[data-testid="stAlert"] {
    padding: 0.6rem 0.8rem !important;
    margin: 0.5rem 0 !important;
}

[data-testid="stAlert"] p {
    font-size: 0.82rem !important;
    line-height: 1.4 !important;
}

/* Force override everything */
.main .block-container {
    padding: 0.5rem 1rem !important;
}

section[data-testid="stVerticalBlock"] {
    gap: 0.3rem !important;
}

div[data-testid="column"] > div {
    gap: 0.3rem !important;
    padding: 0.4rem !important;
}

.stMetric, .stAlert, .element-container {
    margin: 0.3rem 0 !important;
    padding: 0.4rem !important;
}

h1, h2, h3 {
    margin: 0.4rem 0 0.2rem 0 !important;
    padding: 0 !important;
}

p, div {
    margin: 0.1rem 0 !important;
    line-height: 1.3 !important;
}

.stMetricValue {
    font-size: 1.4rem !important;
}

.stMetricLabel {
    font-size: 0.8rem !important;
}

/* Global compact spacing */
.main {
    padding-top: 1rem !important;
}

.block-container {
    padding-top: 1rem !important;
    padding-bottom: 1rem !important;
    max-width: 100% !important;
}

/* Remove extra margins */
.element-container {
    margin-bottom: 0.5rem !important;
}

/* Compact custom metric cards */
.kpi-card {
    background: white;
    padding: 0.7rem 0.9rem;
    border-radius: 8px;
    box-shadow: 0 1px 3px rgba(0,0,0,0.08);
    margin-bottom: 0.6rem;
}

.kpi-title {
    font-size: 0.85rem;
    color: #333;
    font-weight: 500;
    margin: 0 0 0.3rem 0;
}

.kpi-value {
    font-size: 1.6rem;
    font-weight: 700;
    margin: 0.2rem 0;
    line-height: 1.1;
}

.kpi-subtitle {
    font-size: 0.75rem;
    color: #666;
    margin: 0.2rem 0 0 0;
}

/* Compact insight boxes */
.insight-box {
    padding: 0.6rem 0.8rem;
    border-radius: 6px;
    margin-bottom: 0.5rem;
    font-size: 0.8rem;
    line-height: 1.4;
}

.insight-blue {
    background-color: #e3f2fd;
    border-left: 3px solid #2196f3;
}

.insight-green {
    background-color: #e8f5e9;
    border-left: 3px solid #4caf50;
}

.insight-icon {
    font-size: 1rem;
    margin-right: 0.3rem;
}

/* Section header compact */
.section-header {
    font-size: 1.1rem;
    font-weight: 600;
    margin: 0.8rem 0 0.5rem 0;
    color: #333;
}

/* Compact CSS for native Streamlit components */
.stAlert {
    padding: 0.5rem 0.7rem !important;
    margin-bottom: 0.5rem !important;
}

.stAlert > div {
    font-size: 0.8rem !important;
    line-height: 1.4 !important;
}

[data-testid="stVerticalBlock"] > [style*="flex-direction: column;"] > [data-testid="stVerticalBlock"] {
    gap: 0.5rem !important;
}

div[data-testid="column"] {
    padding: 0 0.3rem !important;
}
</style>
""", unsafe_allow_html=True)

import pandas as pd
from datetime import datetime

from utils.database import execute_query
from utils.queries import get_roi_by_measure_query
from utils.charts import create_bar_chart
from utils.data_helpers import show_data_availability_warning, get_data_date_range, format_date_display
from utils.plan_context import get_plan_context, get_plan_size_scenarios
from src.ui.layout import render_page_footer, render_sidebar_footer, render_header

st.sidebar.success("📱 Mobile Optimized")

# Sidebar footer
render_sidebar_footer()

# Page header
render_header()

# Initialize session state if not exists
if 'membership_size' not in st.session_state:
    st.session_state.membership_size = 10000

BASELINE_MEMBERS = 10000
scale_factor = st.session_state.membership_size / BASELINE_MEMBERS
membership_size = st.session_state.membership_size

st.title("💰 ROI Analysis by HEDIS Measure")
st.markdown(f"### Investment Efficiency Analysis - {membership_size:,} Member Plan")
st.markdown("**Proof of concept at 10K scale, ready to expand**")
st.markdown("Compare ROI performance across all 12 HEDIS measures")

# Get plan context for storytelling
plan_context = get_plan_context()
plan_scenarios = get_plan_size_scenarios()
current_scenario = plan_scenarios.get(membership_size, plan_scenarios[10000])

# Storytelling context
if membership_size == 10000:
    st.info("💡 **Small Plans:** Proves ROI before scaling - This baseline demonstrates measurable results at manageable scale.")
elif membership_size <= 25000:
    st.success("💡 **Mid-Size Plans:** Your typical turnaround scenario - Proven strategies drive significant impact with moderate investment.")
else:
    st.warning("💡 **Large/Enterprise Plans:** Enterprise-scale impact projection - Strategies proven at smaller scale adapted for larger operations.")

st.divider()

# Date range filter
col1, col2, col3 = st.columns([1, 1, 2], gap="small")
with col1:
    start_date = st.date_input("Start Date", value=datetime(2024, 10, 1), format="MM/DD/YYYY")
with col2:
    end_date = st.date_input("End Date", value=datetime(2024, 12, 31), format="MM/DD/YYYY")
with col3:
    st.info("💰 Revenue Impact = Successful Closures × $100 per closure")
    st.markdown(f"**Date Range:** {format_date_display(start_date)} to {format_date_display(end_date)}")

# Check data availability
show_data_availability_warning(start_date, end_date)

# Execute query
try:
    query = get_roi_by_measure_query(
        start_date.strftime("%Y-%m-%d"),
        end_date.strftime("%Y-%m-%d")
    )
    # Use query string as cache key to ensure date changes trigger rerun
    df = execute_query(query)
    
    if df.empty:
        from utils.data_helpers import get_data_date_range
        st.warning(f"⚠️ No data found for the selected date range: {format_date_display(start_date)} to {format_date_display(end_date)}")
        date_range = get_data_date_range()
        if date_range:
            st.info(f"💡 Available data: {format_date_display(date_range[0])} to {format_date_display(date_range[1])}")
    else:
        # Scale data - convert to float first to avoid Decimal type issues
        df_scaled = df.copy()
        df_scaled['total_investment'] = df_scaled['total_investment'].astype(float) * scale_factor
        df_scaled['revenue_impact'] = df_scaled['revenue_impact'].astype(float) * scale_factor
        df_scaled['successful_closures'] = df_scaled['successful_closures'].astype(float) * scale_factor
        df_scaled['total_interventions'] = df_scaled['total_interventions'].astype(float) * scale_factor
        
        # Summary metrics (scaled) - using compact column layout
        total_investment = df_scaled['total_investment'].sum()
        total_closures = int(df_scaled['successful_closures'].sum())
        total_interventions = int(df_scaled['total_interventions'].sum())
        avg_roi = df_scaled['roi_ratio'].mean()
        revenue_impact = df_scaled['revenue_impact'].sum()
        net_benefit = revenue_impact - total_investment
        success_rate = (total_closures / total_interventions * 100) if total_interventions > 0 else 0
        
        # KPI Section - using native Streamlit components
        st.header("📊 Key Performance Indicators")
        
        col1, col2 = st.columns(2)
        col1.metric("Total Investment", f"${total_investment:,.0f}", f"${total_investment/membership_size:.2f} per member" if membership_size > 0 else "")
        col2.metric("Successful Closures", f"{total_closures:,}", f"{success_rate:.1f}% success rate" if total_interventions > 0 else "")
        
        col3, col4 = st.columns(2)
        col3.metric("Revenue Impact", f"${revenue_impact:,.0f}", f"${revenue_impact/membership_size:.2f} per member" if membership_size > 0 else "")
        col4.metric("Net Benefit", f"${net_benefit:,.0f}", f"ROI: {avg_roi:.2f}x", delta_color="off")
        
        st.divider()
        
        # Chart (ROI ratio is constant, but title shows scale if not 10K)
        chart_title = "Return on Investment by HEDIS Measure"
        if membership_size != BASELINE_MEMBERS:
            chart_title += f" ({membership_size:,} member plan)"
        
        fig = create_bar_chart(
            df_scaled,
            x_col="measure_code",
            y_col="roi_ratio",
            title=chart_title,
            x_label="HEDIS Measure",
            y_label="ROI Ratio",
            color_col="roi_ratio",
        )
        st.plotly_chart(fig, use_container_width=True, config={'responsive': True, 'displayModeBar': False})
        
        # Data table with details (scaled)
        with st.expander("📋 View Detailed Data"):
            display_df = df_scaled[[
                "measure_code",
                "measure_name",
                "total_investment",
                "revenue_impact",
                "roi_ratio",
                "successful_closures",
                "total_interventions"
            ]].copy()
            display_df.columns = [
                "Measure Code",
                "Measure Name",
                "Total Investment ($)",
                "Revenue Impact ($)",
                "ROI Ratio",
                "Successful Closures",
                "Total Interventions"
            ]
            st.dataframe(display_df, use_container_width=True, hide_index=True)
            
            # Export button
            csv = display_df.to_csv(index=False)
            st.download_button(
                label="📥 Download as CSV",
                data=csv,
                file_name=f"roi_by_measure_{start_date.strftime('%Y%m%d')}_{end_date.strftime('%Y%m%d')}.csv",
                mime="text/csv",
            )
        
        # Key Insights Section - using native Streamlit components
        st.header("💡 Key Insights")
        
        top_measure = df_scaled.loc[df_scaled['roi_ratio'].idxmax()]
        bottom_measure = df_scaled.loc[df_scaled['roi_ratio'].idxmin()]
        
        # Calculate cost per closure for top measure
        top_cost_per_closure = top_measure['total_investment'] / top_measure['successful_closures'] if top_measure['successful_closures'] > 0 else 0
        
        st.info(f"🎯 **Top Performer:** {top_measure['measure_code']} - {top_measure['measure_name']} achieved **{top_measure['roi_ratio']:.2f}x ROI** with **${top_cost_per_closure:.2f} cost per closure** and **{int(top_measure['successful_closures']):,} closures**.")
        
        st.success(f"📊 **Financial Impact:** All 12 HEDIS measures delivered positive ROI **({df_scaled['roi_ratio'].min():.2f}x - {df_scaled['roi_ratio'].max():.2f}x)**, generating **${net_benefit:,.0f} net benefit** with **{success_rate:.1f}% overall success rate**.")
        
        st.info(f"💡 **Optimization Opportunity:** {bottom_measure['measure_code']} - {bottom_measure['measure_name']} shows **{bottom_measure['roi_ratio']:.2f}x ROI** (lowest). Consider reviewing intervention mix to improve efficiency.")
            
except Exception as e:
    st.error(f"Error loading data: {e}")

# Footer sections - desktop full text, mobile abbreviated
render_page_footer()  # Main content footer


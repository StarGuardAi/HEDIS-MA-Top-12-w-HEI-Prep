"""
Page 1: ROI by Measure
Bar chart showing ROI performance across all HEDIS measures
"""
import streamlit as st

st.set_page_config(page_title="ROI by Measure", page_icon="📊", layout="wide")

st.sidebar.success("📱 Mobile Optimized")

import pandas as pd
from datetime import datetime

from utils.database import execute_query
from utils.queries import get_roi_by_measure_query
from utils.charts import create_bar_chart
from utils.data_helpers import show_data_availability_warning, get_data_date_range, format_date_display
from utils.plan_context import get_plan_context, get_plan_size_scenarios

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
col1, col2, col3 = st.columns([1, 1, 2])
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
        
        # Summary metrics (scaled)
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Investment", f"${df_scaled['total_investment'].sum():,.0f}")
        with col2:
            st.metric("Total Closures", f"{int(df_scaled['successful_closures'].sum()):,}")
        with col3:
            avg_roi = df_scaled['roi_ratio'].mean()
            st.metric("Average ROI", f"{avg_roi:.2f}x", delta=f"{(avg_roi-1)*100:.1f}%")
        with col4:
            net_benefit = df_scaled['revenue_impact'].sum() - df_scaled['total_investment'].sum()
            st.metric("Net Benefit", f"${net_benefit:,.0f}")
        
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
        
        # Insights
        st.divider()
        st.subheader("💡 Key Insights")
        col1, col2 = st.columns(2)
        
        top_measure = df_scaled.loc[df_scaled['roi_ratio'].idxmax()]
        with col1:
            st.success(
                f"**Top Performer:** {top_measure['measure_code']} - {top_measure['measure_name']} "
                f"\n- ROI: {top_measure['roi_ratio']:.2f}x\n"
                f"- Investment: ${top_measure['total_investment']:,.0f}\n"
                f"- Closures: {int(top_measure['successful_closures'])}"
            )
        
        bottom_measure = df_scaled.loc[df_scaled['roi_ratio'].idxmin()]
        with col2:
            st.info(
                f"**Lowest ROI:** {bottom_measure['measure_code']} - {bottom_measure['measure_name']} "
                f"\n- ROI: {bottom_measure['roi_ratio']:.2f}x\n"
                f"- Investment: ${bottom_measure['total_investment']:,.0f}\n"
                f"- Closures: {int(bottom_measure['successful_closures'])}"
            )
            
except Exception as e:
    st.error(f"Error loading data: {e}")

# Disclaimer footer
st.markdown("---")
st.info("""
**⚠️ Demonstration Portfolio Project**

This dashboard contains synthetic data for demonstration purposes only.
Data, metrics, and analyses are not production data and do not represent any actual healthcare organization.
Built to showcase healthcare analytics capabilities and technical proficiency.
""")


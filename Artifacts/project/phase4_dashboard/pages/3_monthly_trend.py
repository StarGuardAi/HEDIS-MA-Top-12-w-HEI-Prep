"""
Page 3: Monthly Intervention Trend
Line chart showing intervention trends over time
"""
import streamlit as st
import pandas as pd
from datetime import datetime

from utils.database import execute_query
from utils.queries import get_monthly_intervention_trend_query
from utils.charts import create_line_chart
from utils.data_helpers import show_data_availability_warning, format_date_display, format_month_display
from utils.plan_context import get_plan_size_scenarios

st.set_page_config(page_title="Monthly Intervention Trend", layout="wide")

# Initialize session state if not exists
if 'membership_size' not in st.session_state:
    st.session_state.membership_size = 10000

BASELINE_MEMBERS = 10000
scale_factor = st.session_state.membership_size / BASELINE_MEMBERS
membership_size = st.session_state.membership_size

st.title("📊 Monthly Trends Analysis")
st.markdown(f"### Q4 2024 Turnaround Initiative Tracking - {membership_size:,} member plan")
st.markdown("**Intervention volume and success over time**")
st.markdown("Track intervention volume and success over time")

# Get plan context for storytelling
plan_scenarios = get_plan_size_scenarios()
current_scenario = plan_scenarios.get(membership_size, plan_scenarios[10000])

# Storytelling context
if membership_size == 10000:
    st.info("💡 **Small Plans:** Proves ROI before scaling - Monthly trends show consistent improvement during turnaround.")
elif membership_size <= 25000:
    st.success("💡 **Mid-Size Plans:** Your typical turnaround scenario - Proven monthly patterns at this scale.")
else:
    st.warning("💡 **Large/Enterprise Plans:** Enterprise-scale impact projection - Monthly trends scaled for larger operations.")

st.divider()

# Date range filter
col1, col2 = st.columns(2)
with col1:
    start_date = st.date_input("Start Date", value=datetime(2024, 10, 1), key="trend_start", format="MM/DD/YYYY")
    st.markdown(f"**Selected:** {format_date_display(start_date)}")
with col2:
    end_date = st.date_input("End Date", value=datetime(2024, 12, 31), key="trend_end", format="MM/DD/YYYY")
    st.markdown(f"**Selected:** {format_date_display(end_date)}")

# Check data availability
show_data_availability_warning(start_date, end_date)

# Execute query
try:
    query = get_monthly_intervention_trend_query(
        start_date.strftime("%Y-%m-%d"),
        end_date.strftime("%Y-%m-%d")
    )
    df = execute_query(query)
    
    if df.empty:
        st.warning("No data found for the selected date range.")
    else:
        # Scale data (success_rate and avg_cost are constants)
        # Convert to float first to avoid Decimal type issues
        df_scaled = df.copy()
        df_scaled['total_interventions'] = df_scaled['total_interventions'].astype(float) * scale_factor
        df_scaled['successful_closures'] = df_scaled['successful_closures'].astype(float) * scale_factor
        df_scaled['total_investment'] = df_scaled['total_investment'].astype(float) * scale_factor
        
        # Summary metrics (scaled)
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            total_interventions = df_scaled['total_interventions'].sum()
            st.metric("Total Interventions", f"{int(total_interventions):,}")
        with col2:
            total_closures = df_scaled['successful_closures'].sum()
            st.metric("Total Closures", f"{int(total_closures):,}")
        with col3:
            avg_success_rate = df_scaled['success_rate'].mean()
            st.metric("Avg Success Rate", f"{avg_success_rate:.1f}%")
        with col4:
            total_investment = df_scaled['total_investment'].sum()
            st.metric("Total Investment", f"${total_investment:,.0f}")
        
        st.divider()
        
        # Format month column for charts (use scaled data)
        df_chart = df_scaled.copy()
        df_chart["month"] = df_chart["month"].apply(format_month_display)
        
        # Chart titles with scale indicator if not 10K
        title_suffix = f" ({membership_size:,} member plan)" if membership_size != BASELINE_MEMBERS else ""
        
        # Line chart - interventions and closures
        col1, col2 = st.columns(2)
        
        with col1:
            fig1 = create_line_chart(
                df_chart,
                x_col="month",
                y_cols=["total_interventions", "successful_closures"],
                title=f"Intervention Volume and Success Trends{title_suffix}",
                x_label="Month",
                y_label="Count",
            )
            st.plotly_chart(fig1, use_container_width=True, config={'responsive': True, 'displayModeBar': False})
        
        with col2:
            fig2 = create_line_chart(
                df_chart,
                x_col="month",
                y_cols=["success_rate"],
                title="Success Rate Trend",
                x_label="Month",
                y_label="Success Rate (%)",
            )
            st.plotly_chart(fig2, use_container_width=True, config={'responsive': True, 'displayModeBar': False})
        
        # Full width chart - investment and cost
        fig3 = create_line_chart(
            df_chart,
            x_col="month",
            y_cols=["total_investment", "avg_cost"],
            title=f"Investment and Cost Trends{title_suffix}",
            x_label="Month",
            y_label="Amount ($)",
        )
        st.plotly_chart(fig3, use_container_width=True, config={'responsive': True, 'displayModeBar': False})
        
        # Data table (scaled)
        with st.expander("📋 View Detailed Data"):
            display_df = df_scaled[[
                "month",
                "total_interventions",
                "successful_closures",
                "success_rate",
                "avg_cost",
                "total_investment"
            ]].copy()
            # Format month column for display
            display_df["month"] = display_df["month"].apply(format_month_display)
            display_df.columns = [
                "Month",
                "Total Interventions",
                "Successful Closures",
                "Success Rate (%)",
                "Average Cost ($)",
                "Total Investment ($)"
            ]
            st.dataframe(display_df, use_container_width=True, hide_index=True)
            
            # Export button
            csv = display_df.to_csv(index=False)
            st.download_button(
                label="📥 Download as CSV",
                data=csv,
                file_name=f"monthly_trend_{start_date.strftime('%Y%m%d')}_{end_date.strftime('%Y%m%d')}.csv",
                mime="text/csv",
            )
        
        # Trend insights
        st.divider()
        st.subheader("💡 Trend Insights")
        
        col1, col2 = st.columns(2)
        
        # Calculate trend direction (using scaled data)
        if len(df_scaled) >= 2:
            first_rate = df_scaled.iloc[0]['success_rate']
            last_rate = df_scaled.iloc[-1]['success_rate']
            rate_change = last_rate - first_rate
            
            first_volume = df_scaled.iloc[0]['total_interventions']
            last_volume = df_scaled.iloc[-1]['total_interventions']
            volume_change = last_volume - first_volume
            
            with col1:
                if rate_change > 0:
                    st.success(f"✅ Success rate **increased** by {rate_change:.1f}% over the period")
                elif rate_change < 0:
                    st.warning(f"⚠️ Success rate **decreased** by {abs(rate_change):.1f}% over the period")
                else:
                    st.info("➡️ Success rate remained **stable**")
            
            with col2:
                if volume_change > 0:
                    st.info(f"📈 Intervention volume **increased** by {volume_change:.0f} over the period")
                elif volume_change < 0:
                    st.info(f"📉 Intervention volume **decreased** by {abs(volume_change):.0f} over the period")
                else:
                    st.info("➡️ Intervention volume remained **stable**")
        
        # Best and worst months (using scaled data)
        col3, col4 = st.columns(2)
        best_month = df_scaled.loc[df_scaled['success_rate'].idxmax()]
        worst_month = df_scaled.loc[df_scaled['success_rate'].idxmin()]
        
        with col3:
            st.success(
                f"**Best Month:** {format_month_display(best_month['month'])}\n"
                f"- Success Rate: {best_month['success_rate']:.1f}%\n"
                f"- Interventions: {int(best_month['total_interventions'])}\n"
                f"- Closures: {int(best_month['successful_closures'])}"
            )
        
        with col4:
            st.info(
                f"**Challenging Month:** {format_month_display(worst_month['month'])}\n"
                f"- Success Rate: {worst_month['success_rate']:.1f}%\n"
                f"- Interventions: {int(worst_month['total_interventions'])}\n"
                f"- Closures: {int(worst_month['successful_closures'])}"
            )
            
except Exception as e:
    st.error(f"Error loading data: {e}")


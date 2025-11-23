"""
Page 4: Budget Variance by Measure
Waterfall chart showing budget variance across measures
"""
import streamlit as st
import pandas as pd
from datetime import datetime

from utils.database import execute_query
from utils.queries import get_budget_variance_by_measure_query
from utils.charts import create_waterfall_chart, create_bar_chart
from utils.data_helpers import show_data_availability_warning, format_date_display
from utils.plan_context import get_plan_size_scenarios

st.set_page_config(page_title="Budget Variance by Measure", layout="wide")

# Initialize session state if not exists
if 'membership_size' not in st.session_state:
    st.session_state.membership_size = 10000

BASELINE_MEMBERS = 10000
scale_factor = st.session_state.membership_size / BASELINE_MEMBERS
membership_size = st.session_state.membership_size

st.title("💵 Budget Management by HEDIS Measure")
st.markdown(f"### Fiscal discipline during turnaround - {membership_size:,} member plan")
st.markdown("**Budget model adaptable to plan size**")
st.markdown("Monitor budget performance and identify over/under budget measures")

# Get plan context for storytelling
plan_scenarios = get_plan_size_scenarios()
current_scenario = plan_scenarios.get(membership_size, plan_scenarios[10000])

# Storytelling context
if membership_size == 10000:
    st.info("💡 **Small Plans:** Proves ROI before scaling - Budget discipline critical during turnaround.")
elif membership_size <= 25000:
    st.success("💡 **Mid-Size Plans:** Your typical turnaround scenario - Proven budget models adapt to your scale.")
else:
    st.warning("💡 **Large/Enterprise Plans:** Enterprise-scale impact projection - Budget models proven at smaller scale.")

st.divider()

# Date range filter
col1, col2 = st.columns(2)
with col1:
    start_date = st.date_input("Start Date", value=datetime(2024, 10, 1), key="budget_start", format="MM/DD/YYYY")
with col2:
    end_date = st.date_input("End Date", value=datetime(2024, 12, 31), key="budget_end", format="MM/DD/YYYY")

# Check data availability
show_data_availability_warning(start_date, end_date)

# Execute query
try:
    query = get_budget_variance_by_measure_query(
        start_date.strftime("%Y-%m-%d"),
        end_date.strftime("%Y-%m-%d")
    )
    df = execute_query(query)
    
    if df.empty:
        st.warning("No data found for the selected date range.")
    else:
        # Scale data (variance_pct is constant, but dollar amounts scale)
        # Convert to float first to avoid Decimal type issues
        df_scaled = df.copy()
        df_scaled['budget_allocated'] = df_scaled['budget_allocated'].astype(float) * scale_factor
        df_scaled['actual_spent'] = df_scaled['actual_spent'].astype(float) * scale_factor
        df_scaled['variance'] = df_scaled['variance'].astype(float) * scale_factor
        
        # Summary metrics (scaled)
        col1, col2, col3, col4 = st.columns(4)
        
        total_budget = df_scaled['budget_allocated'].sum()
        total_spent = df_scaled['actual_spent'].sum()
        total_variance = df_scaled['variance'].sum()
        variance_pct = (total_variance / total_budget * 100) if total_budget > 0 else 0
        
        with col1:
            st.metric("Total Budget", f"${total_budget:,.0f}")
        with col2:
            st.metric("Total Spent", f"${total_spent:,.0f}")
        with col3:
            st.metric("Total Variance", f"${total_variance:,.0f}", delta=f"{variance_pct:.1f}%")
        with col4:
            utilization = (total_spent / total_budget * 100) if total_budget > 0 else 0
            st.metric("Budget Utilization", f"{utilization:.1f}%")
        
        st.divider()
        
        # Filter by status
        budget_status_filter = st.multiselect(
            "Filter by Budget Status",
            options=["Over Budget", "Under Budget", "On Budget"],
            default=["Over Budget", "Under Budget", "On Budget"]
        )
        filtered_df = df_scaled[df_scaled['budget_status'].isin(budget_status_filter)] if budget_status_filter else df_scaled
        
        if filtered_df.empty:
            st.info("No measures match the selected filter criteria.")
        else:
            # Chart titles with scale indicator if not 10K
            title_suffix = f" ({membership_size:,} member plan)" if membership_size != BASELINE_MEMBERS else ""
            
            # Waterfall chart
            fig1 = create_waterfall_chart(
                filtered_df,
                measure_col="measure_code",
                budget_col="budget_allocated",
                actual_col="actual_spent",
                variance_col="variance",
                title=f"Budget Performance by HEDIS Measure{title_suffix}",
            )
            st.plotly_chart(fig1, use_container_width=True, config={'responsive': True, 'displayModeBar': False})
            
            # Variance percentage chart (variance_pct is constant, no scaling needed)
            fig2 = create_bar_chart(
                filtered_df,
                x_col="measure_code",
                y_col="variance_pct",
                title="Budget Variance Percentage by Measure",
                x_label="HEDIS Measure",
                y_label="Variance (%)",
                color_col="budget_status",
            )
            st.plotly_chart(fig2, use_container_width=True, config={'responsive': True, 'displayModeBar': False})
            
            # Data table
            with st.expander("📋 View Detailed Data"):
                display_df = filtered_df[[
                    "measure_code",
                    "measure_name",
                    "budget_allocated",
                    "actual_spent",
                    "variance",
                    "variance_pct",
                    "budget_status"
                ]].copy()
                display_df.columns = [
                    "Measure Code",
                    "Measure Name",
                    "Budget Allocated ($)",
                    "Actual Spent ($)",
                    "Variance ($)",
                    "Variance (%)",
                    "Status"
                ]
                st.dataframe(display_df, use_container_width=True, hide_index=True)
                
                # Export button
            csv = display_df.to_csv(index=False)
            st.download_button(
                label="📥 Download as CSV",
                data=csv,
                file_name=f"budget_variance_{start_date.strftime('%Y%m%d')}_{end_date.strftime('%Y%m%d')}.csv",
                mime="text/csv",
            )
            
            # Insights
            st.divider()
            st.subheader("💡 Budget Insights")
            
            col1, col2, col3 = st.columns(3)
            
            # Note: budget_status is based on variance_pct which is constant, so filtering works the same
            over_budget = filtered_df[filtered_df['budget_status'] == 'Over Budget']
            under_budget = filtered_df[filtered_df['budget_status'] == 'Under Budget']
            on_budget = filtered_df[filtered_df['budget_status'] == 'On Budget']
            
            with col1:
                if not over_budget.empty:
                    largest_over = over_budget.loc[over_budget['variance'].abs().idxmax()]
                    st.error(
                        f"**Largest Over Budget:** {largest_over['measure_code']}\n"
                        f"- Budget: ${largest_over['budget_allocated']:,.0f}\n"
                        f"- Spent: ${largest_over['actual_spent']:,.0f}\n"
                        f"- Variance: ${largest_over['variance']:,.0f} ({largest_over['variance_pct']:.1f}%)"
                    )
                else:
                    st.success("✅ No measures over budget")
            
            with col2:
                if not under_budget.empty:
                    largest_under = under_budget.loc[under_budget['variance'].abs().idxmax()]
                    st.info(
                        f"**Largest Under Budget:** {largest_under['measure_code']}\n"
                        f"- Budget: ${largest_under['budget_allocated']:,.0f}\n"
                        f"- Spent: ${largest_under['actual_spent']:,.0f}\n"
                        f"- Variance: ${largest_under['variance']:,.0f} ({largest_under['variance_pct']:.1f}%)"
                    )
                else:
                    st.info("ℹ️ No measures under budget")
            
            with col3:
                st.success(
                    f"**Budget Summary:**\n"
                    f"- Over Budget: {len(over_budget)} measures\n"
                    f"- Under Budget: {len(under_budget)} measures\n"
                    f"- On Budget: {len(on_budget)} measures\n"
                    f"- Total Analyzed: {len(filtered_df)} measures"
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


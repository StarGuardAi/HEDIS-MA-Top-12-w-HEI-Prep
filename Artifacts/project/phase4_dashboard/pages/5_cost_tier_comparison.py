"""
Page 5: Cost Tier Comparison
Grouped bar chart comparing Low/Medium/High touch interventions
"""
import streamlit as st
import pandas as pd
from datetime import datetime

from utils.database import execute_query
from utils.queries import get_cost_tier_comparison_query
from utils.charts import create_grouped_bar_chart, create_bar_chart
from utils.data_helpers import show_data_availability_warning, format_date_display
from utils.plan_context import get_plan_size_scenarios

st.set_page_config(page_title="Cost Tier Comparison", layout="wide")

# Initialize session state if not exists
if 'membership_size' not in st.session_state:
    st.session_state.membership_size = 10000

BASELINE_MEMBERS = 10000
scale_factor = st.session_state.membership_size / BASELINE_MEMBERS
membership_size = st.session_state.membership_size

st.title("🎯 Cost Efficiency Analysis")
st.markdown(f"### Cost-effective strategies identified - {membership_size:,} member plan")
st.markdown("**Replicable across larger member populations**")
st.markdown("Compare effectiveness of Low/Medium/High touch intervention strategies")

# Get plan context for storytelling
plan_scenarios = get_plan_size_scenarios()
current_scenario = plan_scenarios.get(membership_size, plan_scenarios[10000])

# Storytelling context
if membership_size == 10000:
    st.info("💡 **Small Plans:** Proves ROI before scaling - Cost-effective strategies identified for replication.")
elif membership_size <= 25000:
    st.success("💡 **Mid-Size Plans:** Your typical turnaround scenario - Strategies proven cost-effective at this scale.")
else:
    st.warning("💡 **Large/Enterprise Plans:** Enterprise-scale impact projection - Cost-effective strategies scaled for larger populations.")

st.divider()

# Date range filter
col1, col2 = st.columns(2)
with col1:
    start_date = st.date_input("Start Date", value=datetime(2024, 10, 1), key="tier_start", format="MM/DD/YYYY")
    st.markdown(f"**Selected:** {format_date_display(start_date)}")
with col2:
    end_date = st.date_input("End Date", value=datetime(2024, 12, 31), key="tier_end", format="MM/DD/YYYY")
    st.markdown(f"**Selected:** {format_date_display(end_date)}")

# Check data availability
show_data_availability_warning(start_date, end_date)

# Execute query
try:
    query = get_cost_tier_comparison_query(
        start_date.strftime("%Y-%m-%d"),
        end_date.strftime("%Y-%m-%d")
    )
    df = execute_query(query)
    
    if df.empty:
        st.warning("No data found for the selected date range.")
    else:
        # Scale data (success_rate, avg_cost, cost_per_closure are constants, but counts and investment scale)
        # Convert to float first to avoid Decimal type issues
        df_scaled = df.copy()
        df_scaled['interventions_count'] = df_scaled['interventions_count'].astype(float) * scale_factor
        df_scaled['successful_closures'] = df_scaled['successful_closures'].astype(float) * scale_factor
        df_scaled['total_investment'] = df_scaled['total_investment'].astype(float) * scale_factor
        
        # Summary metrics
        col1, col2, col3, col4 = st.columns(4)
        
        low_touch = df_scaled[df_scaled['cost_tier'] == 'Low Touch'].iloc[0] if 'Low Touch' in df_scaled['cost_tier'].values else None
        medium_touch = df_scaled[df_scaled['cost_tier'] == 'Medium Touch'].iloc[0] if 'Medium Touch' in df_scaled['cost_tier'].values else None
        high_touch = df_scaled[df_scaled['cost_tier'] == 'High Touch'].iloc[0] if 'High Touch' in df_scaled['cost_tier'].values else None
        
        best_tier = df_scaled.loc[df_scaled['success_rate'].idxmax()]
        
        with col1:
            if low_touch is not None:
                st.metric(
                    "Low Touch Success Rate",
                    f"{low_touch['success_rate']:.1f}%",
                    delta=f"${low_touch['avg_cost']:.2f} avg cost"
                )
        with col2:
            if medium_touch is not None:
                st.metric(
                    "Medium Touch Success Rate",
                    f"{medium_touch['success_rate']:.1f}%",
                    delta=f"${medium_touch['avg_cost']:.2f} avg cost"
                )
        with col3:
            if high_touch is not None:
                st.metric(
                    "High Touch Success Rate",
                    f"{high_touch['success_rate']:.1f}%",
                    delta=f"${high_touch['avg_cost']:.2f} avg cost"
                )
        with col4:
            st.metric(
                "Best Performing Tier",
                best_tier['cost_tier'],
                delta=f"{best_tier['success_rate']:.1f}% success"
            )
        
        st.divider()
        
        # Chart titles with scale indicator if not 10K
        title_suffix = f" ({membership_size:,} member plan)" if membership_size != BASELINE_MEMBERS else ""
        
        # Cost vs Success Rate comparison
        col1, col2 = st.columns(2)
        
        with col1:
            fig1 = create_grouped_bar_chart(
                df_scaled,
                x_col="cost_tier",
                y_cols=["avg_cost", "cost_per_closure"],
                title="Intervention Effectiveness by Cost Tier",
                x_label="Cost Tier",
                y_label="Amount ($)",
            )
            st.plotly_chart(fig1, use_container_width=True, config={'responsive': True, 'displayModeBar': False})
        
        with col2:
            fig2 = create_bar_chart(
                df_scaled,
                x_col="cost_tier",
                y_col="success_rate",
                title="Success Rate by Cost Tier",
                x_label="Cost Tier",
                y_label="Success Rate (%)",
                color_col="success_rate",
            )
            st.plotly_chart(fig2, use_container_width=True, config={'responsive': True, 'displayModeBar': False})
        
        # Volume and investment (scaled)
        fig3 = create_grouped_bar_chart(
            df_scaled,
            x_col="cost_tier",
            y_cols=["interventions_count", "successful_closures"],
            title=f"Intervention Volume by Tier{title_suffix}",
            x_label="Cost Tier",
            y_label="Count",
        )
        st.plotly_chart(fig3, use_container_width=True, config={'responsive': True, 'displayModeBar': False})
        
        # Investment comparison (scaled)
        fig4 = create_bar_chart(
            df_scaled,
            x_col="cost_tier",
            y_col="total_investment",
            title=f"Total Investment by Cost Tier{title_suffix}",
            x_label="Cost Tier",
            y_label="Total Investment ($)",
            color_col="total_investment",
        )
        st.plotly_chart(fig4, use_container_width=True, config={'responsive': True, 'displayModeBar': False})
        
        # Data table (scaled)
        with st.expander("📋 View Detailed Data"):
            display_df = df_scaled[[
                "cost_tier",
                "avg_cost",
                "success_rate",
                "interventions_count",
                "successful_closures",
                "total_investment",
                "cost_per_closure"
            ]].copy()
            display_df.columns = [
                "Cost Tier",
                "Average Cost ($)",
                "Success Rate (%)",
                "Interventions Count",
                "Successful Closures",
                "Total Investment ($)",
                "Cost per Closure ($)"
            ]
            st.dataframe(display_df, use_container_width=True, hide_index=True)
            
            # Export button
            csv = display_df.to_csv(index=False)
            st.download_button(
                label="📥 Download as CSV",
                data=csv,
                file_name=f"cost_tier_comparison_{start_date.strftime('%Y%m%d')}_{end_date.strftime('%Y%m%d')}.csv",
                mime="text/csv",
            )
        
        # Key insights
        st.divider()
        st.subheader("💡 Key Insights")
        
        if len(df_scaled) >= 2:
            col1, col2 = st.columns(2)
            
            # Best value analysis (using scaled data)
            df_with_value = df_scaled.copy()
            df_with_value['value_score'] = df_with_value['success_rate'] - (df_with_value['avg_cost'] / 10)
            best_value = df_with_value.loc[df_with_value['value_score'].idxmax()]
            
            with col1:
                st.success(
                    f"**Best Value Proposition:** {best_value['cost_tier']}\n"
                    f"- Success Rate: {best_value['success_rate']:.1f}%\n"
                    f"- Average Cost: ${best_value['avg_cost']:.2f}\n"
                    f"- Cost per Closure: ${best_value['cost_per_closure']:.2f}\n"
                    f"- Total Closures: {int(best_value['successful_closures'])}"
                )
            
            # ROI comparison (using scaled data)
            df_with_roi = df_scaled.copy()
            df_with_roi['roi'] = (df_with_roi['successful_closures'] * 100) / df_with_roi['total_investment']
            best_roi = df_with_roi.loc[df_with_roi['roi'].idxmax()]
            
            with col2:
                st.info(
                    f"**Highest ROI Tier:** {best_roi['cost_tier']}\n"
                    f"- ROI: {best_roi['roi']:.2f}x\n"
                    f"- Investment: ${best_roi['total_investment']:,.0f}\n"
                    f"- Revenue Impact: ${best_roi['successful_closures'] * 100:,.0f}\n"
                    f"- Net Benefit: ${(best_roi['successful_closures'] * 100) - best_roi['total_investment']:,.0f}"
                )
            
            # Cost efficiency analysis
            st.markdown("### 📊 Cost Efficiency Analysis")
            col3, col4, col5 = st.columns(3)
            
            with col3:
                if low_touch is not None:
                    st.metric(
                        "Low Touch Cost per Closure",
                        f"${low_touch['cost_per_closure']:.2f}",
                        delta=f"{low_touch['success_rate']:.1f}% success"
                    )
            
            with col4:
                if medium_touch is not None:
                    st.metric(
                        "Medium Touch Cost per Closure",
                        f"${medium_touch['cost_per_closure']:.2f}",
                        delta=f"{medium_touch['success_rate']:.1f}% success"
                    )
            
            with col5:
                if high_touch is not None:
                    st.metric(
                        "High Touch Cost per Closure",
                        f"${high_touch['cost_per_closure']:.2f}",
                        delta=f"{high_touch['success_rate']:.1f}% success"
                    )
            
            # Strategic recommendation
            if low_touch is not None and high_touch is not None:
                if low_touch['success_rate'] > high_touch['success_rate']:
                    st.warning(
                        "⚠️ **Strategic Insight:** Low-touch interventions show **higher success rates** "
                        f"({low_touch['success_rate']:.1f}% vs {high_touch['success_rate']:.1f}%) "
                        f"at a fraction of the cost (${low_touch['avg_cost']:.2f} vs ${high_touch['avg_cost']:.2f}). "
                        "Consider reallocating budget toward low-touch strategies for better ROI."
                    )
                else:
                    st.info(
                        "ℹ️ **Strategic Insight:** Higher-touch interventions show improved success rates. "
                        "Consider the balance between cost and effectiveness for optimal portfolio allocation."
                    )
            
except Exception as e:
    st.error(f"Error loading data: {e}")


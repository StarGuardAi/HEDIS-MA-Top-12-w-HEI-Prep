"""
Page 2: Cost per Closure by Activity
Scatter plot showing cost-effectiveness of intervention activities
"""
import streamlit as st
import pandas as pd
from datetime import datetime

from utils.database import execute_query
from utils.queries import get_cost_per_closure_by_activity_query
from utils.data_helpers import show_data_availability_warning, format_date_display
from utils.plan_context import get_plan_size_scenarios
import plotly.express as px

st.set_page_config(page_title="Cost Per Closure", page_icon="💰", layout="wide")

# Initialize session state if not exists
if 'membership_size' not in st.session_state:
    st.session_state.membership_size = 10000

BASELINE_MEMBERS = 10000
scale_factor = st.session_state.membership_size / BASELINE_MEMBERS
membership_size = st.session_state.membership_size

st.title("📈 Intervention Performance Analysis")
st.markdown(f"### Breakthrough: Low-touch digital outperforms traditional - {membership_size:,} member plan")
st.markdown("**Scalable strategy for plans of any size**")
st.markdown("Analyze cost-effectiveness of different intervention activities")

# Get plan context for storytelling
plan_scenarios = get_plan_size_scenarios()
current_scenario = plan_scenarios.get(membership_size, plan_scenarios[10000])

# Storytelling context
if membership_size == 10000:
    st.info("💡 **Small Plans:** Proves ROI before scaling - This demonstrates low-touch digital can outperform traditional methods.")
elif membership_size <= 25000:
    st.success("💡 **Mid-Size Plans:** Your typical turnaround scenario - Scalable strategies proven at smaller scale.")
else:
    st.warning("💡 **Large/Enterprise Plans:** Enterprise-scale impact projection - Strategies proven at smaller scale adapted for larger operations.")

st.divider()

# Filters
col1, col2, col3 = st.columns([1, 1, 1])
with col1:
    start_date = st.date_input("Start Date", value=datetime(2024, 10, 1), key="scatter_start", format="MM/DD/YYYY")
with col2:
    end_date = st.date_input("End Date", value=datetime(2024, 12, 31), key="scatter_end", format="MM/DD/YYYY")
with col3:
    min_uses = st.number_input("Minimum Uses", min_value=1, value=10, help="Filter activities with at least this many uses")
    st.markdown(f"**Range:** {format_date_display(start_date)} to {format_date_display(end_date)}")

# Check data availability
show_data_availability_warning(start_date, end_date)

# Execute query
try:
    query = get_cost_per_closure_by_activity_query(
        start_date.strftime("%Y-%m-%d"),
        end_date.strftime("%Y-%m-%d"),
        int(min_uses)
    )
    df = execute_query(query)
    
    if df.empty:
        st.warning("No data found for the selected criteria.")
    else:
        # Scale data (cost_per_closure and success_rate are constants, but times_used and successful_closures scale)
        # Convert to float first to avoid Decimal type issues
        df_scaled = df.copy()
        df_scaled['times_used'] = df_scaled['times_used'].astype(float) * scale_factor
        df_scaled['successful_closures'] = df_scaled['successful_closures'].astype(float) * scale_factor
        # Ensure success_rate is float (not Decimal or string)
        df_scaled['success_rate'] = df_scaled['success_rate'].astype(float)
        
        # Summary metrics (cost_per_closure and success_rate are constants)
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            most_cost_effective = df_scaled.loc[df_scaled['cost_per_closure'].idxmin()]
            st.metric(
                "Most Cost-Effective",
                f"${most_cost_effective['cost_per_closure']:.2f}",
                delta=f"{most_cost_effective['activity_name']}"
            )
        with col2:
            highest_success = df_scaled.loc[df_scaled['success_rate'].idxmax()]
            st.metric(
                "Highest Success Rate",
                f"{highest_success['success_rate']:.1f}%",
                delta=f"{highest_success['activity_name']}"
            )
        with col3:
            avg_cost = df_scaled['avg_cost'].mean()
            st.metric("Average Cost", f"${avg_cost:.2f}")
        with col4:
            avg_success = df_scaled['success_rate'].mean()
            st.metric("Average Success Rate", f"{avg_success:.1f}%")
        
        st.divider()
        
        # Scatter plot (scaled) - Simple version without text labels
        chart_title = "Cost Efficiency Analysis by Intervention Type"
        if membership_size != BASELINE_MEMBERS:
            chart_title += f" ({membership_size:,} member plan)"
        
        # Create simple scatter plot WITHOUT text labels - show names on hover only
        fig = px.scatter(
            df_scaled,
            x='avg_cost',
            y='success_rate',
            size='times_used',
            title=chart_title,
            labels={
                'avg_cost': 'Average Cost per Intervention ($)',
                'success_rate': 'Success Rate (%)',
                'times_used': 'Volume',
            },
            hover_name='activity_name',  # Show name on hover
            hover_data={
                'avg_cost': ':.2f',
                'success_rate': ':.1f',
                'times_used': ':,.0f',
                'cost_per_closure': ':.2f',
            },
            color_discrete_sequence=['#4e2a84'],  # Use theme color
        )
        
        # Update layout for mobile - no text labels
        fig.update_layout(
            height=600,
            autosize=True,
            margin=dict(l=80, r=40, t=120, b=80),
            title={
                'text': chart_title + '<br><sub>Hover over points for details</sub>',
                'y': 0.98,
                'x': 0.5,
                'xanchor': 'center',
                'yanchor': 'top',
                'font': {'size': 18, 'color': '#4e2a84'}
            },
            xaxis_title='Average Cost per Intervention ($)',
            yaxis_title='Success Rate (%)',
            showlegend=False,  # No legend needed for single color
            template='plotly_white',
            plot_bgcolor='white',
            paper_bgcolor='white',
        )
        
        # Remove any text labels completely (text=None removes labels, no textposition needed)
        fig.update_traces(text=None)
        
        st.plotly_chart(fig, use_container_width=True, config={'responsive': True, 'displayModeBar': False})
        
        # Data table (scaled)
        with st.expander("📋 View Detailed Data"):
            display_df = df_scaled[[
                "activity_name",
                "avg_cost",
                "success_rate",
                "times_used",
                "successful_closures",
                "cost_per_closure"
            ]].copy()
            display_df.columns = [
                "Activity Name",
                "Avg Cost ($)",
                "Success Rate (%)",
                "Times Used",
                "Successful Closures",
                "Cost per Closure ($)"
            ]
            st.dataframe(display_df.sort_values("Cost per Closure ($)"), use_container_width=True, hide_index=True)
            
            # Export button
            csv = display_df.to_csv(index=False)
            st.download_button(
                label="📥 Download as CSV",
                data=csv,
                file_name=f"cost_per_closure_{start_date.strftime('%Y%m%d')}_{end_date.strftime('%Y%m%d')}.csv",
                mime="text/csv",
            )
        
        # Insights
        st.divider()
        st.subheader("💡 Key Insights")
        
        # Best performers
        col1, col2 = st.columns(2)
        
        with col1:
            best_combo = df_scaled.loc[(df_scaled['success_rate'] - df_scaled['avg_cost']/10).idxmax()]
            st.success(
                f"**Best Value:** {best_combo['activity_name']}\n"
                f"- Cost: ${best_combo['avg_cost']:.2f}\n"
                f"- Success Rate: {best_combo['success_rate']:.1f}%\n"
                f"- Cost per Closure: ${best_combo['cost_per_closure']:.2f}"
            )
        
        with col2:
            st.info(
                f"**Activity Count:** {len(df_scaled)} activities analyzed\n"
                f"- Average usage: {df_scaled['times_used'].mean():.0f} times\n"
                f"- Total closures: {int(df_scaled['successful_closures'].sum())}\n"
                f"- Cost range: ${df_scaled['avg_cost'].min():.2f} - ${df_scaled['avg_cost'].max():.2f}"
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


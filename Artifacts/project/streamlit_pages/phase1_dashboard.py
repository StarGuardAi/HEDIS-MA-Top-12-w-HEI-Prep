"""
Phase 1 Database Dashboard
Real-time analytics from Phase 1 HEDIS Portfolio Optimizer database
"""

from typing import Optional
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from src.data.phase1_database import (
    get_revenue_at_risk,
    get_revenue_at_risk_summary,
    get_cost_per_closure,
    get_portfolio_roi,
    get_current_velocity,
    get_member_segmentation,
    get_geographic_performance,
    get_plans,
    get_measures,
    get_dashboard_summary,
    test_connection
)

# Cache database queries with plan_id as key to ensure updates when plan changes
@st.cache_data(ttl=60)  # Cache for 60 seconds
def cached_get_dashboard_summary(plan_id):
    """Cached version of get_dashboard_summary with plan_id as cache key."""
    return get_dashboard_summary(plan_id)


def render_phase1_dashboard():
    """Render Phase 1 database dashboard."""
    
    st.title("📊 Phase 1 Database Analytics")
    st.markdown("---")
    
    # Test connection
    if not test_connection():
        st.error("❌ Database connection failed. Please ensure PostgreSQL is running.")
        st.info("**To start database:** Run `setup_with_docker.bat` or start PostgreSQL service")
        return
    
    st.success("✅ Connected to Phase 1 database")
    
    # Get plans for filter
    try:
        plans_df = get_plans()
        plan_options = ["All Plans"] + plans_df['plan_id'].tolist()
        
        col1, col2, col3 = st.columns(3)
        with col1:
            selected_plan = st.selectbox("Select Plan", plan_options, key="plan_selector")
        with col2:
            refresh = st.button("🔄 Refresh Data", key="refresh_button")
        with col3:
            show_raw = st.checkbox("Show Raw Data", value=False, key="show_raw_checkbox")
        
        plan_id = None if selected_plan == "All Plans" else selected_plan
        
        # Dashboard Summary (force refresh when plan changes)
        st.markdown("### 📈 Dashboard Summary")
        # Use cached function with plan_id as key to ensure updates
        summary = cached_get_dashboard_summary(plan_id)
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Members", f"{summary.get('total_members', 0):,}")
        with col2:
            st.metric("Total Gaps", f"{summary.get('total_gaps', 0):,}")
        with col3:
            total_rar = summary.get('total_revenue_at_risk', 0) or 0
            st.metric("Revenue at Risk", f"${total_rar:,.0f}")
        with col4:
            st.metric("Active Plans", summary.get('total_plans', 0))
        
        st.markdown("---")
        
        # Revenue at Risk Section
        st.markdown("### 💰 Revenue at Risk Analysis")
        
        rar_df = get_revenue_at_risk(plan_id)
        
        if not rar_df.empty:
            # Top measures by revenue at risk
            col1, col2 = st.columns(2)
            
            with col1:
                top_rar = rar_df.head(10).copy()
                fig = px.bar(
                    top_rar,
                    x='revenue_at_risk',
                    y='measure_name',
                    orientation='h',
                    title='Top 10 Measures by Revenue at Risk',
                    labels={'revenue_at_risk': 'Revenue at Risk ($)', 'measure_name': 'Measure'},
                    color='revenue_at_risk',
                    color_continuous_scale='Reds'
                )
                fig.update_layout(height=400, yaxis={'categoryorder': 'total ascending'})
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                # Revenue by plan
                plan_rar = rar_df.groupby('plan_name')['revenue_at_risk'].sum().reset_index()
                plan_rar = plan_rar.sort_values('revenue_at_risk', ascending=False)
                
                fig = px.pie(
                    plan_rar,
                    values='revenue_at_risk',
                    names='plan_name',
                    title='Revenue at Risk by Plan',
                    hole=0.4
                )
                fig.update_layout(height=400)
                st.plotly_chart(fig, use_container_width=True)
            
            # Revenue at Risk Table
            if show_raw:
                st.markdown("#### Revenue at Risk Details")
                display_cols = [
                    'plan_name', 'measure_name', 'current_rate_pct', 
                    'measure_current_stars', 'measure_target_stars',
                    'members_needed', 'revenue_at_risk'
                ]
                st.dataframe(
                    rar_df[display_cols].style.format({
                        'current_rate_pct': '{:.1f}%',
                        'revenue_at_risk': '${:,.0f}'
                    }),
                    use_container_width=True,
                    height=300
                )
        
        st.markdown("---")
        
        # Cost & ROI Section
        st.markdown("### 💵 Cost & ROI Analysis")
        
        cost_df = get_cost_per_closure(plan_id)
        roi_df = get_portfolio_roi(plan_id)
        
        if not cost_df.empty:
            col1, col2 = st.columns(2)
            
            with col1:
                # Cost per closure by measure
                cost_by_measure = cost_df.groupby('measure_name')['cost_per_gap_closed'].mean().reset_index()
                cost_by_measure = cost_by_measure.sort_values('cost_per_gap_closed', ascending=False).head(10)
                
                fig = px.bar(
                    cost_by_measure,
                    x='cost_per_gap_closed',
                    y='measure_name',
                    orientation='h',
                    title='Average Cost per Closure by Measure',
                    labels={'cost_per_gap_closed': 'Cost ($)', 'measure_name': 'Measure'},
                    color='cost_per_gap_closed',
                    color_continuous_scale='Blues'
                )
                fig.update_layout(height=400, yaxis={'categoryorder': 'total ascending'})
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                # ROI by measure
                if not roi_df.empty:
                    roi_by_measure = roi_df.groupby('measure_name')['projected_roi_ratio'].mean().reset_index()
                    roi_by_measure = roi_by_measure.sort_values('projected_roi_ratio', ascending=False).head(10)
                    
                    fig = px.bar(
                        roi_by_measure,
                        x='projected_roi_ratio',
                        y='measure_name',
                        orientation='h',
                        title='Projected ROI Ratio by Measure',
                        labels={'projected_roi_ratio': 'ROI Ratio', 'measure_name': 'Measure'},
                        color='projected_roi_ratio',
                        color_continuous_scale='Greens'
                    )
                    fig.update_layout(height=400, yaxis={'categoryorder': 'total ascending'})
                    st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("---")
        
        # Velocity Section
        st.markdown("### ⚡ Gap Closure Velocity")
        
        velocity_df = get_current_velocity(plan_id)
        
        if not velocity_df.empty:
            col1, col2 = st.columns(2)
            
            with col1:
                # Velocity by measure
                vel_by_measure = velocity_df.groupby('measure_name')['gaps_per_week'].mean().reset_index()
                vel_by_measure = vel_by_measure.sort_values('gaps_per_week', ascending=False).head(10)
                
                fig = px.bar(
                    vel_by_measure,
                    x='gaps_per_week',
                    y='measure_name',
                    orientation='h',
                    title='Gap Closure Velocity (Gaps/Week)',
                    labels={'gaps_per_week': 'Gaps per Week', 'measure_name': 'Measure'},
                    color='gaps_per_week',
                    color_continuous_scale='Purples'
                )
                fig.update_layout(height=400, yaxis={'categoryorder': 'total ascending'})
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                # Closure rate by measure
                closure_by_measure = velocity_df.groupby('measure_name')['closure_rate_pct'].mean().reset_index()
                closure_by_measure = closure_by_measure.sort_values('closure_rate_pct', ascending=False).head(10)
                
                fig = px.bar(
                    closure_by_measure,
                    x='closure_rate_pct',
                    y='measure_name',
                    orientation='h',
                    title='Closure Rate by Measure (%)',
                    labels={'closure_rate_pct': 'Closure Rate %', 'measure_name': 'Measure'},
                    color='closure_rate_pct',
                    color_continuous_scale='Oranges'
                )
                fig.update_layout(height=400, yaxis={'categoryorder': 'total ascending'})
                st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("---")
        
        # Member Segmentation Section
        st.markdown("### 👥 Member Segmentation")
        
        seg_df = get_member_segmentation(plan_id)
        
        if not seg_df.empty:
            col1, col2 = st.columns(2)
            
            with col1:
                # Risk category distribution
                risk_dist = seg_df.groupby('risk_category')['member_count'].sum().reset_index()
                
                fig = px.pie(
                    risk_dist,
                    values='member_count',
                    names='risk_category',
                    title='Member Distribution by Risk Category',
                    hole=0.4
                )
                fig.update_layout(height=400)
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                # Age band distribution
                age_dist = seg_df.groupby('age_band')['member_count'].sum().reset_index()
                
                fig = px.bar(
                    age_dist,
                    x='age_band',
                    y='member_count',
                    title='Member Distribution by Age Band',
                    labels={'member_count': 'Members', 'age_band': 'Age Band'},
                    color='member_count',
                    color_continuous_scale='Viridis'
                )
                fig.update_layout(height=400)
                st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("---")
        
        # Geographic Performance Section
        st.markdown("### 🗺️ Geographic Performance")
        
        geo_df = get_geographic_performance()
        
        if not geo_df.empty:
            # Top zip codes by member count
            top_geo = geo_df.head(15).copy()
            
            fig = px.bar(
                top_geo,
                x='member_count',
                y='city',
                orientation='h',
                title='Top 15 Zip Codes by Member Count',
                labels={'member_count': 'Members', 'city': 'City'},
                color='closure_rate_pct',
                color_continuous_scale='RdYlGn',
                hover_data=['zip_code', 'total_gaps', 'closure_rate_pct']
            )
            fig.update_layout(height=500, yaxis={'categoryorder': 'total ascending'})
            st.plotly_chart(fig, use_container_width=True)
        
    except Exception as e:
        st.error(f"Error loading data: {str(e)}")
        st.exception(e)


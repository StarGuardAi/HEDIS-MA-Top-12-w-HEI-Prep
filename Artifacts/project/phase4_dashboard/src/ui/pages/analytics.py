"""
Analytics page
"""
import streamlit as st
import pandas as pd
import plotly.express as px
from src.data.loaders import load_measures_data, load_member_data
from src.models.calculator import ROICalculator, StarRatingCalculator


def render():
    """Render analytics page"""
    st.header("📈 Analytics")
    
    # Load data
    measures_df = load_measures_data()
    members_df = load_member_data()
    
    # ROI Analysis
    if not members_df.empty:
        st.subheader("ROI Analysis")
        calculator = ROICalculator()
        roi_result = calculator.calculate_intervention_roi(members_df)
        
        col1, col2, col3, col4 = st.columns(4, gap="small")
        with col1:
            st.metric("Total Members", roi_result['total_members'])
        with col2:
            st.metric("Predicted Value", f"${roi_result['predicted_value']:,.0f}")
        with col3:
            st.metric("Intervention Cost", f"${roi_result['intervention_cost']:,.0f}")
        with col4:
            st.metric("Net Value", f"${roi_result['net_value']:,.0f}")
    
    # Measures Performance Chart
    if not measures_df.empty and 'current_rate' in measures_df.columns:
        st.subheader("Measures Performance")
        fig = px.bar(
            measures_df,
            x='measure_name',
            y='current_rate',
            title='Current Compliance Rates by Measure'
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # Star Rating Impact
    st.subheader("Star Rating Impact Analysis")
    if not measures_df.empty:
        from config.settings import HEDIS_MEASURES
        
        impacts = {}
        for _, row in measures_df.iterrows():
            measure_name = row.get('measure_name', '')
            current_rate = row.get('current_rate', 0)
            predicted_rate = current_rate + 5  # Assume 5% improvement
            
            # Find measure weight
            measure_key = measure_name.replace(' ', '_')
            measure_weight = HEDIS_MEASURES.get(measure_key, {}).get('star_weight', 1.0)
            
            impact = StarRatingCalculator.calculate_measure_impact(
                current_rate=current_rate,
                predicted_rate=predicted_rate,
                measure_weight=measure_weight
            )
            impacts[measure_name] = impact
        
        if impacts:
            impact_df = pd.DataFrame([
                {'measure': k, 'impact': v} for k, v in impacts.items()
            ])
            
            fig = px.bar(
                impact_df,
                x='measure',
                y='impact',
                title='Star Rating Impact by Measure'
            )
            st.plotly_chart(fig, use_container_width=True)


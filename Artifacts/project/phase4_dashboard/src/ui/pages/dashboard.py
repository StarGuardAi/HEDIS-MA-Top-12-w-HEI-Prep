"""
Main dashboard page with AI insights integrated
"""
import streamlit as st
import pandas as pd
import logging
from typing import Dict, Any

from src.data.loaders import load_member_data, load_measures_data
from src.models.calculator import ROICalculator
from src.ui.components.metrics import render_kpi_summary
from src.ui.components.ai_insights import (
    render_executive_summary,
    render_smart_recommendations,
    render_ai_settings
)

logger = logging.getLogger(__name__)


def render() -> None:
    """Render main dashboard with AI insights"""
    
    st.title("⭐ HEDIS Portfolio Dashboard")
    
    # Load data
    try:
        members_df = load_member_data()
        measures_df = load_measures_data()
    except Exception as e:
        st.error(f"Error loading data: {str(e)}")
        logger.exception("Error loading dashboard data")
        return
    
    # Calculate metrics
    try:
        calculator = ROICalculator()
        portfolio_metrics: Dict[str, Any] = {
            'total_members': len(members_df),
            'total_gaps': len(members_df[members_df['gap_status'] == 'Open']) if 'gap_status' in members_df.columns else 0,
            'predicted_closure_rate': members_df['predicted_closure_probability'].mean() * 100 if 'predicted_closure_probability' in members_df.columns else 0.0,
            'total_financial_value': members_df['financial_value'].sum() if 'financial_value' in members_df.columns else 0.0,
            'star_rating_current': 4.0,
            'star_rating_predicted': 4.5,
            'top_measures': measures_df.nlargest(5, 'financial_impact').to_dict('records') if not measures_df.empty and 'financial_impact' in measures_df.columns else []
        }
    except Exception as e:
        st.error(f"Error calculating metrics: {str(e)}")
        logger.exception("Error calculating portfolio metrics")
        portfolio_metrics = {
            'total_members': 0,
            'total_gaps': 0,
            'predicted_closure_rate': 0.0,
            'total_financial_value': 0.0,
            'star_rating_current': 4.0,
            'star_rating_predicted': 4.5,
            'top_measures': []
        }
    
    # 🆕 AI EXECUTIVE SUMMARY (NEW!)
    render_executive_summary(portfolio_metrics)
    
    st.markdown("---")
    
    # KPIs
    try:
        roi_percentage = 498
        star_rating = 4.5
        member_count = portfolio_metrics.get('total_members', 10000)
        compliance_rate = portfolio_metrics.get('predicted_closure_rate', 85)
        
        render_kpi_summary(
            roi_percentage=roi_percentage,
            star_rating=star_rating,
            member_count=member_count,
            compliance_rate=compliance_rate
        )
    except Exception as e:
        st.error(f"Error rendering KPIs: {str(e)}")
        logger.exception("Error rendering KPIs")
    
    st.markdown("---")
    
    # 🆕 AI RECOMMENDATIONS (NEW!)
    if not measures_df.empty:
        render_smart_recommendations(measures_df)
        st.markdown("---")
    
    # Measures overview
    if not measures_df.empty:
        st.subheader("📋 Measures Overview")
        st.dataframe(measures_df, use_container_width=True)
    else:
        st.info("No measures data available")
    
    # AI Settings in sidebar
    render_ai_settings()

"""
Reusable metric card components
"""
import streamlit as st
from typing import Optional
from streamlit_extras.metric_cards import style_metric_cards


def render_metric_grid(metrics_data: list[dict]):
    """
    Render a responsive grid of metric cards
    
    Args:
        metrics_data: List of dicts with keys: label, value, delta
    """
    cols = st.columns(len(metrics_data), gap="small")
    
    for idx, metric in enumerate(metrics_data):
        with cols[idx]:
            st.metric(
                label=metric['label'],
                value=metric['value'],
                delta=metric.get('delta', None),
                help=metric.get('help', None)
            )
    
    style_metric_cards(
        background_color="#0066cc",
        border_left_color="#00cc66",
        border_size_px=3,
        box_shadow=True
    )


def render_kpi_summary(
    roi_percentage: float,
    star_rating: float,
    member_count: int,
    compliance_rate: float
):
    """
    Render standard KPI summary section
    
    Args:
        roi_percentage: ROI percentage
        star_rating: Current star rating
        member_count: Number of members
        compliance_rate: Compliance rate percentage
    """
    metrics = [
        {
            'label': 'Potential ROI',
            'value': f'{roi_percentage:.0f}%',
            'delta': '+$935K annually',
            'help': 'Return on investment for gap closure interventions'
        },
        {
            'label': 'Star Rating Impact',
            'value': f'{star_rating:.1f} ⭐',
            'delta': '+0.5 stars',
            'help': 'Projected improvement in Medicare Advantage rating'
        },
        {
            'label': 'Members Optimized',
            'value': f'{member_count:,}',
            'delta': '+1,200',
            'help': 'Total members in optimization cohort'
        },
        {
            'label': 'Predicted Compliance',
            'value': f'{compliance_rate:.0f}%',
            'delta': '+8%',
            'help': 'Predicted compliance rate after interventions'
        }
    ]
    
    render_metric_grid(metrics)


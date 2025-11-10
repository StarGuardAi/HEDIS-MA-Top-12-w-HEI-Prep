from __future__ import annotations

from typing import Any, Dict

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from src.data.kpi_engine import FinancialSnapshot


def _format_currency(value: float, digits: int = 2) -> str:
    """Format currency values with compact units for dashboard display."""
    if value is None or pd.isna(value):
        return "$0"

    sign = "-" if value < 0 else ""
    value = abs(value)

    if value >= 1_000_000_000:
        suffix = "B"
        divisor = 1_000_000_000
    elif value >= 1_000_000:
        suffix = "M"
        divisor = 1_000_000
    elif value >= 1_000:
        suffix = "K"
        divisor = 1_000
    else:
        suffix = ""
        divisor = 1

    formatted = f"{value / divisor:.{digits}f}{suffix}" if divisor != 1 else f"{value:,.0f}"
    return f"{sign}${formatted}"


def _build_roi_gauge(snapshot: FinancialSnapshot) -> go.Figure:
    """Build a gauge chart showing portfolio ROI health."""
    roi_value = snapshot.roi_percentage
    roi_max = max(120.0, abs(roi_value) + 40.0)

    gauge = go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=roi_value,
            number={"suffix": "%"},
            title={"text": "Portfolio ROI"},
            gauge={
                "axis": {"range": [-100, roi_max]},
                "bar": {"color": "#10B981"},
                "steps": [
                    {"range": [-100, 0], "color": "#fee2e2"},
                    {"range": [0, min(roi_max, 100)], "color": "#fef3c7"},
                    {"range": [min(roi_max, 100), roi_max], "color": "#dcfce7"},
                ],
            },
        )
    )

    gauge.update_layout(height=280, margin=dict(l=10, r=10, t=40, b=10))
    return gauge


def _build_waterfall(snapshot: FinancialSnapshot) -> go.Figure:
    """Build waterfall chart for the quality bonus revenue bridge."""
    labels = [entry.get("label", "") for entry in snapshot.waterfall]
    values = [entry.get("value", 0.0) for entry in snapshot.waterfall]
    measures = []
    for idx, entry in enumerate(snapshot.waterfall):
        entry_type = entry.get("type", "relative")
        if entry_type == "absolute":
            measures.append("absolute")
        elif entry_type == "total":
            measures.append("total")
        else:
            measures.append("relative")

    fig = go.Figure(
        go.Waterfall(
            orientation="v",
            measure=measures,
            x=labels,
            text=[_format_currency(v, 2) for v in values],
            y=values,
            connector={"line": {"color": "#2563EB"}},
        )
    )

    fig.update_layout(
        title="Quality Bonus Revenue Bridge",
        height=420,
        hovermode="x unified",
        margin=dict(l=40, r=40, t=60, b=40),
        yaxis_title="USD",
    )
    return fig


def _render_value_components(snapshot: FinancialSnapshot) -> None:
    components = pd.DataFrame(
        [
            {"Component": "Opportunity Value", "Amount": snapshot.opportunity_amount},
            {"Component": "Star Revenue Delta", "Amount": snapshot.star_revenue_delta},
            {"Component": "Retention Value", "Amount": snapshot.member_retention_value},
            {"Component": "Intervention Cost", "Amount": -snapshot.intervention_cost},
            {"Component": "Net Revenue Impact", "Amount": snapshot.net_revenue_impact},
        ]
    )

    fig = px.bar(
        components,
        x="Amount",
        y="Component",
        orientation="h",
        text=components["Amount"].apply(lambda v: _format_currency(v, 2)),
        color="Amount",
        color_continuous_scale=["#ef4444", "#fbbf24", "#10b981"],
    )
    fig.update_layout(coloraxis_showscale=False, height=320, margin=dict(l=10, r=10, t=40, b=10))
    st.plotly_chart(fig, use_container_width=True)


def _render_measure_breakdown(snapshot: FinancialSnapshot) -> None:
    breakdown = pd.DataFrame(snapshot.measure_breakdown)
    if breakdown.empty:
        st.info("Measure-level ROI breakdown is unavailable for the current dataset.")
        return

    display_df = (
        breakdown.assign(
            eligible_members=lambda df_: df_["eligible_members"].round().astype(int),
            gaps=lambda df_: df_["gaps"].round().astype(int),
            gap_rate_pct=lambda df_: (df_["gap_rate"] * 100).round(1),
            at_risk=lambda df_: df_["at_risk"].round(2),
            opportunity=lambda df_: df_["opportunity"].round(2),
            intervention_cost=lambda df_: df_["intervention_cost"].round(2),
            net_value=lambda df_: df_["net_value"].round(2),
            roi_pct=lambda df_: df_["roi_pct"].round(1),
        )
        .rename(
            columns={
                "measure": "Measure",
                "eligible_members": "Eligible",
                "gaps": "Gaps",
                "gap_rate_pct": "Gap Rate (%)",
                "at_risk": "Revenue at Risk ($)",
                "opportunity": "Opportunity ($)",
                "intervention_cost": "Cost ($)",
                "net_value": "Net Value ($)",
                "roi_pct": "ROI (%)",
            }
        )
        [[
            "Measure",
            "Eligible",
            "Gaps",
            "Gap Rate (%)",
            "Revenue at Risk ($)",
            "Opportunity ($)",
            "Cost ($)",
            "Net Value ($)",
            "ROI (%)",
        ]]
    )

    st.dataframe(display_df, use_container_width=True, hide_index=True)


def render_financial_overview(
    snapshot: FinancialSnapshot,
    star_summary: Dict[str, Any],
    measure_summary: pd.DataFrame,
) -> None:
    """Render the executive financial overview using enriched KPI snapshot data."""

    current_stars = float(star_summary.get("current_weighted_stars", 0.0) or 0.0)
    projected_stars = float(star_summary.get("projected_weighted_stars", current_stars) or current_stars)
    star_delta = projected_stars - current_stars
    payback_months = snapshot.payback_months
    payback_text = "N/A" if payback_months in (float("inf"),) else f"{payback_months:.1f} months"

    st.markdown('<p class="main-header">💰 Financial Impact Analyzer</p>', unsafe_allow_html=True)
    st.markdown(
        '<p class="sub-header">Convert HEDIS performance into quality bonus revenue, ROI, and retention value</p>',
        unsafe_allow_html=True,
    )

    st.markdown("## 📌 Executive KPI Snapshot")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Quality Bonus @ Risk", _format_currency(snapshot.at_risk_amount, 2), "Revenue exposed without action")
    with col2:
        st.metric("Opportunity Value", _format_currency(snapshot.opportunity_amount, 2), "Recovered by closing priority gaps")
    with col3:
        st.metric("Net Revenue Impact", _format_currency(snapshot.net_revenue_impact, 2), "After intervention costs")
    with col4:
        st.metric("Retention Protection", _format_currency(snapshot.member_retention_value, 2), "Value of churn avoided")

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric(
            "Weighted Star Rating",
            f"{current_stars:.2f}",
            delta=f"Target {projected_stars:.2f} (Δ {star_delta:+.2f})",
        )
    with col2:
        st.metric("Star Revenue Delta", _format_currency(snapshot.star_revenue_delta, 2), "Projected bonus uplift")
    with col3:
        st.metric(
            "Portfolio ROI",
            f"{snapshot.roi_percentage:.0f}%",
            delta=f"Payback {payback_text}",
        )
    with col4:
        st.metric(
            "Churn Risk Score",
            f"{snapshot.churn_risk_score * 100:.1f}%",
            delta="Average attrition probability",
        )

    st.caption(
        "ℹ️ Opportunity, Star Delta, and Retention values combine to form the portfolio ROI. "
        "Intervention costs reflect configurable per-gap investments."
    )

    st.markdown("---")

    col1, col2 = st.columns((1, 2))
    with col1:
        st.markdown("### 📈 ROI Health Gauge")
        st.plotly_chart(_build_roi_gauge(snapshot), use_container_width=True)

        st.markdown("### 🧮 Value Composition")
        _render_value_components(snapshot)

    with col2:
        st.markdown("### 💵 Quality Bonus Revenue Bridge")
        st.plotly_chart(_build_waterfall(snapshot), use_container_width=True)

    st.markdown("---")
    st.markdown("### 📊 Measure ROI Leaderboard")
    _render_measure_breakdown(snapshot)

    st.markdown("---")
    st.markdown("### 🗂️ Portfolio Measure Summary")
    if measure_summary.empty:
        st.info("Measure summary dataset is empty.")
    else:
        display_df = (
            measure_summary.copy()
            .assign(
                Eligible=lambda df_: df_["eligible_members"].round().astype(int),
                Compliant=lambda df_: df_["compliant_members"].round().astype(int),
                Gaps=lambda df_: df_["gaps"].round().astype(int),
                Compliance=lambda df_: (df_["compliance_rate"] * 100).round(1),
            )
            .rename(
                columns={
                    "measure": "Measure",
                    "measure_weight": "Weight",
                    "star_rating": "Star Rating",
                }
            )
            [["Measure", "Weight", "Eligible", "Compliant", "Gaps", "Compliance", "Star Rating"]]
            .sort_values(by=["Weight", "Measure"], ascending=[False, True])
        )
        st.dataframe(display_df, use_container_width=True, hide_index=True)

from __future__ import annotations

from typing import Any, Dict

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from src.data.kpi_engine import EquitySnapshot


def _format_currency(value: float, digits: int = 1) -> str:
    if value is None or pd.isna(value):
        return "$0"
    sign = "-" if value < 0 else ""
    value = abs(value)
    if value >= 1_000_000:
        formatted = f"{value / 1_000_000:.{digits}f}M"
    elif value >= 1_000:
        formatted = f"{value / 1_000:.{digits}f}K"
    else:
        formatted = f"{value:.0f}"
    return f"{sign}${formatted}"


def _compute_probability_breakdown(priority_df: pd.DataFrame) -> pd.DataFrame:
    if priority_df.empty:
        return pd.DataFrame(columns=["Tier", "Members", "Mean Probability", "Mean ROI"])

    bins = [0.0, 0.4, 0.7, 1.0]
    labels = ["Low", "Medium", "High"]
    df = priority_df.copy()
    df["Tier"] = pd.cut(df["Gap Probability"], bins=bins, labels=labels, include_lowest=True, right=True)
    grouped = df.groupby("Tier").agg(
        Members=("Gap Probability", "count"),
        Mean_Probability=("Gap Probability", "mean"),
        Mean_ROI=("Expected ROI", "mean"),
    ).reset_index()
    return grouped


def _priority_matrix_figure(priority_df: pd.DataFrame) -> go.Figure:
    df = priority_df.copy()
    if df.empty:
        return go.Figure()

    df["Probability %"] = df["Gap Probability"] * 100
    df["Financial Value (K)"] = df["Financial Value"] / 1_000

    fig = px.scatter(
        df,
        x="Probability %",
        y="Financial Value (K)",
        size="Expected ROI",
        color="Intervention Priority",
        hover_data={"Member ID": True, "Expected ROI": ':.2f', "Financial Value": ':.0f'},
        color_discrete_map={"High": "#EF4444", "Medium": "#F97316", "Low": "#22C55E"},
    )
    fig.update_traces(marker=dict(opacity=0.75, line=dict(width=0.5, color="#1f2937")))
    fig.update_layout(
        height=450,
        margin=dict(l=40, r=40, t=40, b=40),
        xaxis_title="Gap Closure Probability (%)",
        yaxis_title="Financial Value ($K)",
        legend_title="Intervention Priority",
    )
    return fig


def _lift_curve_chart(diagnostics: Dict[str, Any]) -> go.Figure:
    lift_df = diagnostics.get("lift_curve")
    if lift_df is None or lift_df.empty:
        return go.Figure()

    fig = px.line(
        lift_df,
        x="decile",
        y="lift",
        title="Model Lift vs. Random",
        markers=True,
    )
    fig.update_layout(
        height=320,
        margin=dict(l=40, r=40, t=60, b=40),
        xaxis_title="Targeted Percentile",
        yaxis_title="Lift",
    )
    return fig


def _hei_heatmap(snapshot: EquitySnapshot) -> go.Figure:
    heatmap_df = pd.DataFrame(snapshot.heatmap)
    if heatmap_df.empty:
        return go.Figure()

    melt_df = heatmap_df.melt(
        id_vars=["segment", "gap"],
        value_vars=["srf_rate", "non_srf_rate"],
        var_name="Group",
        value_name="Rate",
    )
    melt_df["Group"] = melt_df["Group"].map({"srf_rate": "SRF", "non_srf_rate": "Non-SRF"})

    fig = px.bar(
        melt_df,
        x="segment",
        y="Rate",
        color="Group",
        barmode="group",
        text=melt_df["Rate"].round(1),
        color_discrete_map={"SRF": "#0EA5E9", "Non-SRF": "#22C55E"},
    )
    fig.update_layout(
        height=360,
        margin=dict(l=40, r=40, t=50, b=80),
        xaxis_title="Population Segment",
        yaxis_title="Compliance Rate (%)",
        legend_title="Population",
    )
    fig.update_xaxes(tickangle=-35)
    return fig


def render_predictive_priority(
    priority_df: pd.DataFrame,
    diagnostics: Dict[str, Any],
    equity_snapshot: EquitySnapshot,
) -> None:
    st.markdown('<p class="main-header">🔮 Predictive Priority Command Center</p>', unsafe_allow_html=True)
    st.markdown(
        '<p class="sub-header">Align high-value members with equity-ready interventions</p>',
        unsafe_allow_html=True,
    )

    probability_breakdown = _compute_probability_breakdown(priority_df)

    col1, col2, col3 = st.columns(3)
    tier_defaults = {"High": 0, "Medium": 0, "Low": 0}
    tier_map = {row["Tier"]: row for _, row in probability_breakdown.iterrows()}

    with col1:
        high = tier_map.get("High", tier_defaults)
        members = high.get("Members", 0)
        mean_prob = high.get("Mean_Probability", 0.0)
        st.metric("High Probability Tier", f"{members}", delta=f"Avg prob {mean_prob * 100:.1f}%")
    with col2:
        medium = tier_map.get("Medium", tier_defaults)
        st.metric("Medium Probability Tier", f"{medium.get('Members', 0)}", delta=f"Avg prob {medium.get('Mean_Probability', 0.0) * 100:.1f}%")
    with col3:
        response_rate = diagnostics.get("auc", 0.0)
        st.metric("Model AUC", f"{response_rate:.2f}", delta="Predictive lift vs random")

    st.caption(
        "ℹ️ Probability tiers follow CMS care management guidance: High ≥70%, Medium 40-70%, Low <40%. "
        "ROI reflects expected financial value divided by intervention cost."
    )

    st.markdown("---")

    col1, col2 = st.columns((1.4, 1.0))
    with col1:
        st.markdown("### Member Priority Matrix")
        if priority_df.empty:
            st.warning("No priority members available; load member predictions to populate this view.")
        else:
            st.plotly_chart(_priority_matrix_figure(priority_df), use_container_width=True)

    with col2:
        st.markdown("### Probability Tier Summary")
        if probability_breakdown.empty:
            st.info("Probability tiers will populate once member scores are available.")
        else:
            display_breakdown = probability_breakdown.copy()
            display_breakdown["Mean Probability"] = (display_breakdown["Mean_Probability"] * 100).round(1)
            display_breakdown["Mean ROI"] = display_breakdown["Mean_ROI"].round(2)
            display_breakdown = display_breakdown.rename(
                columns={
                    "Mean Probability": "Avg Probability (%)",
                    "Mean ROI": "Avg ROI (x)",
                }
            )[ ["Tier", "Members", "Avg Probability (%)", "Avg ROI (x)"] ]
            st.dataframe(display_breakdown, hide_index=True, use_container_width=True)

        st.markdown("### Model Lift Curve")
        st.plotly_chart(_lift_curve_chart(diagnostics), use_container_width=True)

    st.markdown("---")

    st.markdown("### HEI Readiness Heatmap")
    if not equity_snapshot.heatmap:
        st.warning("Upload HEI-ready member data to populate the heatmap.")
    else:
        st.plotly_chart(_hei_heatmap(equity_snapshot), use_container_width=True)

        if equity_snapshot.disparity_segments:
            st.markdown("#### Priority Equity Segments")
            for segment in equity_snapshot.disparity_segments:
                st.markdown(
                    f"- **{segment['segment']}** — Gap {segment['gap']:.1f}pp, Population {segment['population_pct']:.1f}%, "
                    f"SRF {segment['srf_rate']:.1f}% vs Non-SRF {segment['non_srf_rate']:.1f}%"
                )

    st.markdown("---")
    st.markdown("### Top Priority Members")
    top_priority = priority_df.head(25) if not priority_df.empty else priority_df
    st.dataframe(top_priority, hide_index=True, use_container_width=True)
    st.download_button(
        label="⬇️ Download Predictive Priority List",
        data=priority_df.to_csv(index=False) if not priority_df.empty else "",
        file_name="predictive_priority_list.csv",
        mime="text/csv",
        disabled=priority_df.empty,
    )

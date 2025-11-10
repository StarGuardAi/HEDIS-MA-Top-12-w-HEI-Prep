from __future__ import annotations

from typing import Any

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from src.data.kpi_engine import OperationalSnapshot


def _format_rate(value: float) -> str:
    if value is None or pd.isna(value):
        return "0.0%"
    return f"{value * 100:.1f}%"


def _format_days(value: float) -> str:
    return f"{value:.1f} days" if value is not None else "N/A"


def _build_velocity_chart(snapshot: OperationalSnapshot, gap_history: pd.DataFrame) -> go.Figure:
    fig = go.Figure()

    if not gap_history.empty:
        fig.add_trace(
            go.Bar(
                x=gap_history["date"],
                y=gap_history["gaps_closed"],
                name="Gaps Closed",
                marker_color="#2563EB",
            )
        )

    if snapshot.rolling_velocity:
        rolling_df = pd.DataFrame(snapshot.rolling_velocity)
        fig.add_trace(
            go.Scatter(
                x=pd.to_datetime(rolling_df["date"]),
                y=rolling_df["rolling_avg"],
                mode="lines",
                name="Rolling Avg",
                line=dict(color="#EF4444", width=3),
            )
        )

    if snapshot.forecast_velocity:
        forecast_df = pd.DataFrame(snapshot.forecast_velocity)
        fig.add_trace(
            go.Scatter(
                x=pd.to_datetime(forecast_df["date"]),
                y=forecast_df["expected_gaps"],
                mode="lines",
                name="Forecast",
                line=dict(color="#10B981", width=2, dash="dash"),
            )
        )

    fig.update_layout(
        height=360,
        margin=dict(l=30, r=30, t=40, b=40),
        xaxis_title="Week Ending",
        yaxis_title="Gaps Closed",
        hovermode="x unified",
    )
    return fig


def _build_channel_chart(snapshot: OperationalSnapshot) -> go.Figure:
    channels_df = pd.DataFrame(snapshot.channel_performance)
    if channels_df.empty:
        return go.Figure()

    fig = px.bar(
        channels_df,
        x="channel",
        y="completed",
        color="contact_rate",
        text=channels_df["completed"].round().astype(int),
        labels={
            "channel": "Channel",
            "completed": "Closures",
            "contact_rate": "Contact Rate",
        },
        color_continuous_scale=["#f97316", "#10b981"],
    )
    fig.update_layout(
        height=320,
        margin=dict(l=30, r=30, t=40, b=30),
        coloraxis_colorbar=dict(title="Contact Rate"),
    )
    return fig


def render_operations_command(
    snapshot: OperationalSnapshot,
    gap_history: pd.DataFrame,
    outreach_df: pd.DataFrame,
) -> None:
    st.markdown("## ⚙️ Operational Performance Command Center")

    engagement = snapshot.engagement_summary or {}
    contact_rate = snapshot.outreach_summary.get("contact_success_rate", 0.0)
    conversion_rate = snapshot.outreach_summary.get("conversion_rate", 0.0)

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric(
            "Gap Velocity",
            f"{snapshot.gap_velocity_per_week:.0f}/week",
            delta=f"Trend {snapshot.recent_trend.capitalize()}",
        )
    with col2:
        st.metric("Avg Days to Close", _format_days(snapshot.avg_days_to_close), delta="Rolling window")
    with col3:
        st.metric(
            "Response Rate",
            _format_rate(contact_rate),
            delta=f"Conversion {_format_rate(conversion_rate)}",
        )
    with col4:
        st.metric(
            "Attempts / Member",
            f"{engagement.get('attempts_per_member', 0.0):.2f}",
            delta=f"Contacts {_format_rate(engagement.get('first_contact_rate', 0.0))}",
        )

    st.markdown("---")
    col1, col2 = st.columns((1.4, 1.0))
    with col1:
        st.markdown("### Weekly Closure Trend & Forecast")
        if gap_history.empty and not snapshot.velocity_series:
            st.info("Gap history data unavailable.")
        else:
            fig = _build_velocity_chart(snapshot, gap_history)
            st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown("### Outreach Funnel")
        if outreach_df.empty:
            st.info("Outreach funnel data unavailable.")
        else:
            funnel_row = outreach_df.iloc[0]
            figure = go.Figure(
                go.Funnel(
                    y=["Eligible", "Attempted", "Contacted", "Scheduled", "Completed"],
                    x=[
                        funnel_row.get("eligible_members", 0),
                        funnel_row.get("attempted", 0),
                        funnel_row.get("contacted", 0),
                        funnel_row.get("scheduled", 0),
                        funnel_row.get("completed", 0),
                    ],
                    textposition="inside",
                    textinfo="value+percent previous",
                    marker={"color": ["#0EA5E9", "#3B82F6", "#22C55E", "#F97316", "#10B981"]},
                )
            )
            figure.update_layout(height=320, margin=dict(l=10, r=10, t=40, b=10))
            st.plotly_chart(figure, use_container_width=True)

            conversions = snapshot.funnel_conversion
            st.markdown(
                f"""
                **Stage Conversions**
                - Eligible → Outreach: {conversions.get('eligible_to_outreach', 0):.1%}  \
                - Outreach → Contact: {conversions.get('outreach_to_contact', 0):.1%}  \
                - Contact → Scheduled: {conversions.get('contact_to_scheduled', 0):.1%}  \
                - Scheduled → Completed: {conversions.get('scheduled_to_completed', 0):.1%}  \
                - No-Show Rate: {_format_rate(snapshot.outreach_summary.get('no_show_rate', 0.0))}
                """
            )

    st.markdown("---")
    st.markdown("### Channel Performance")
    if snapshot.channel_performance:
        st.plotly_chart(_build_channel_chart(snapshot), use_container_width=True)
    else:
        st.info("Channel-level performance data unavailable.")

    if engagement:
        st.markdown("### Engagement Summary")
        engagement_df = pd.DataFrame(
            [
                {
                    "Metric": "Attempts per Member",
                    "Value": f"{engagement.get('attempts_per_member', 0.0):.2f}",
                },
                {
                    "Metric": "Contacts per Member",
                    "Value": f"{engagement.get('contacts_per_member', 0.0):.2f}",
                },
                {
                    "Metric": "Response Rate",
                    "Value": _format_rate(engagement.get('response_rate', 0.0)),
                },
                {
                    "Metric": "Completion Rate",
                    "Value": _format_rate(engagement.get('completion_rate', 0.0)),
                },
                {
                    "Metric": "No-Show Rate",
                    "Value": _format_rate(snapshot.outreach_summary.get('no_show_rate', 0.0)),
                },
            ]
        )
        st.dataframe(engagement_df, use_container_width=True, hide_index=True)

    if snapshot.channel_performance:
        export_channels = pd.DataFrame(snapshot.channel_performance)
        st.download_button(
            label="⬇️ Download Channel Performance",
            data=export_channels.to_csv(index=False),
            file_name="operations_channel_performance.csv",
            mime="text/csv",
        )

    if outreach_df is not None and not outreach_df.empty:
        st.download_button(
            label="⬇️ Download Outreach Funnel",
            data=outreach_df.to_csv(index=False),
            file_name="operations_outreach_funnel.csv",
            mime="text/csv",
        )

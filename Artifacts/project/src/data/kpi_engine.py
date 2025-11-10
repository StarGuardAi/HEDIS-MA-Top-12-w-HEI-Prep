"""
KPI Analytics Engine for HEDIS Portfolio Enhancements

Transforms prepared measure/member/provider data into high-value KPI
snapshots used by the Streamlit dashboard.

The module focuses on data computations only; visualization is handled
by downstream UI layers.
"""

from __future__ import annotations

import logging
from dataclasses import asdict, dataclass, field
from typing import Any, Dict, Iterable, List, Mapping, Optional

import numpy as np
import pandas as pd

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Utility helpers
# ---------------------------------------------------------------------------


def _safe_sum(values: Iterable[Any]) -> float:
    """Return numeric sum while ignoring None/NaN."""
    if isinstance(values, (pd.Series, pd.Index, list, tuple)):
        return float(np.nansum(values))
    return float(values or 0.0)


def _safe_div(numerator: float, denominator: float, default: float = 0.0) -> float:
    """Safe division with graceful fallback."""
    if denominator is None or denominator == 0 or np.isclose(denominator, 0):
        return default
    return float(numerator) / float(denominator)


def _get_nested(cfg: Optional[Mapping[str, Any]], path: str, default: Any = None) -> Any:
    """Retrieve nested configuration value using dot-notation path."""
    if not cfg:
        return default

    cursor: Any = cfg
    for key in path.split("."):
        if isinstance(cursor, Mapping) and key in cursor:
            cursor = cursor[key]
        else:
            return default
    return cursor


def _ensure_datetime(series: pd.Series) -> pd.Series:
    """Convert a pandas Series to datetime if possible."""
    if not isinstance(series, pd.Series):
        return pd.Series(dtype="datetime64[ns]")
    if pd.api.types.is_datetime64_any_dtype(series):
        return series
    return pd.to_datetime(series, errors="coerce")


# ---------------------------------------------------------------------------
# Dataclasses for structured outputs
# ---------------------------------------------------------------------------


@dataclass
class FinancialSnapshot:
    current_qbp: float
    projected_qbp: float
    at_risk_amount: float
    opportunity_amount: float
    intervention_cost: float
    net_revenue_impact: float
    star_revenue_delta: float
    member_retention_value: float
    churn_risk_score: float
    star_bridge: Dict[str, float]
    total_population: float
    gap_rate: float
    projected_gap_rate: float
    qbp_per_member: float
    roi_percentage: float
    payback_months: float
    gross_benefit: float
    value_components: Dict[str, float]
    waterfall: List[Dict[str, Any]] = field(default_factory=list)
    measure_breakdown: List[Dict[str, Any]] = field(default_factory=list)


@dataclass
class OperationalSnapshot:
    gap_velocity_per_week: float
    recent_trend: str
    avg_days_to_close: float
    funnel_conversion: Dict[str, float]
    outreach_summary: Dict[str, float]
    velocity_series: List[Dict[str, Any]] = field(default_factory=list)
    rolling_velocity: List[Dict[str, Any]] = field(default_factory=list)
    forecast_velocity: List[Dict[str, Any]] = field(default_factory=list)
    engagement_summary: Dict[str, float] = field(default_factory=dict)
    channel_performance: List[Dict[str, Any]] = field(default_factory=list)


@dataclass
class EquitySnapshot:
    srf_population_pct: float
    equity_gap_pct: float
    hei_reward_projection: float
    disparity_flag: bool
    hei_score: float = 0.0
    readiness_level: str = "Monitoring"
    disparity_segments: List[Dict[str, Any]] = field(default_factory=list)
    heatmap: List[Dict[str, Any]] = field(default_factory=list)
    trend_summary: Dict[str, float] = field(default_factory=dict)


@dataclass
class ProviderSnapshot:
    avg_gap_closure_rate: float
    high_performers: Iterable[Dict[str, Any]]
    low_performers: Iterable[Dict[str, Any]]
    outlier_providers: Iterable[Dict[str, Any]]


@dataclass
class CompetitiveSnapshot:
    market_percentile: float
    star_delta_vs_market: float
    enrollment_share: float
    projected_gain: float


@dataclass
class KPIBundle:
    financial: FinancialSnapshot
    operational: OperationalSnapshot
    equity: EquitySnapshot
    provider: ProviderSnapshot
    competitive: CompetitiveSnapshot

    def to_dict(self) -> Dict[str, Any]:
        """Serialize bundle to plain dictionary."""
        return {
            "financial": asdict(self.financial),
            "operational": asdict(self.operational),
            "equity": asdict(self.equity),
            "provider": {
                "avg_gap_closure_rate": self.provider.avg_gap_closure_rate,
                "high_performers": list(self.provider.high_performers),
                "low_performers": list(self.provider.low_performers),
                "outlier_providers": list(self.provider.outlier_providers),
            },
            "competitive": asdict(self.competitive),
        }


# ---------------------------------------------------------------------------
# Financial metrics
# ---------------------------------------------------------------------------


def calculate_financial_metrics(
    measure_summary: pd.DataFrame,
    star_summary: Optional[Mapping[str, Any]] = None,
    member_value_df: Optional[pd.DataFrame] = None,
    config: Optional[Mapping[str, Any]] = None,
) -> FinancialSnapshot:
    """
    Compute revenue and risk metrics needed for the executive financial view.
    """

    financial_cfg = _get_nested(config, "analytics.financial", {}) or {}

    qbp_per_member = financial_cfg.get("qbp_per_member", 372.0)
    default_gap_closure_rate = financial_cfg.get("default_gap_closure_rate", 0.3)
    intervention_cost_per_gap = financial_cfg.get(
        "intervention_cost_per_gap",
        _get_nested(config, "roi.intervention_costs.average", 150.0),
    )
    retention_value_per_member = financial_cfg.get("retention_value_per_member", 1200.0)
    churn_risk_multiplier = financial_cfg.get("churn_risk_multiplier", 0.15)

    revenue_per_star_point = _get_nested(
        config,
        "star_rating.revenue_per_star_point",
        financial_cfg.get("revenue_per_star_point", 50000.0),
    )

    # Expected columns: eligible_members / denominator, compliant_members / numerator, gaps
    eligible_col = next(
        (col for col in ("eligible_members", "denominator", "total_eligible") if col in measure_summary),
        None,
    )
    numerator_col = next(
        (col for col in ("compliant_members", "numerator", "in_numerator") if col in measure_summary),
        None,
    )
    gaps_col = next((col for col in ("gaps", "gap_members", "members_with_gaps") if col in measure_summary), None)

    total_population = _safe_sum(measure_summary[eligible_col]) if eligible_col else _safe_sum(len(measure_summary))
    compliant_members = _safe_sum(measure_summary[numerator_col]) if numerator_col else total_population

    if gaps_col:
        total_gaps = _safe_sum(measure_summary[gaps_col])
    else:
        total_gaps = max(total_population - compliant_members, 0.0)

    current_gap_rate = _safe_div(total_gaps, total_population)
    current_qbp = total_population * qbp_per_member
    at_risk_amount = current_qbp * current_gap_rate
    opportunity_amount = at_risk_amount * default_gap_closure_rate
    intervention_cost = total_gaps * intervention_cost_per_gap
    net_revenue_impact = opportunity_amount - intervention_cost

    # Star revenue bridge
    measure_weight_col = "measure_weight" if "measure_weight" in measure_summary else None
    star_rating_col = "star_rating" if "star_rating" in measure_summary else None

    if star_summary:
        current_star = star_summary.get("current_weighted_stars") or star_summary.get("current_stars")
        projected_star = (
            star_summary.get("projected_weighted_stars")
            or _get_nested(star_summary, "with_50pct_closure.stars")
            or star_summary.get("projected_stars")
        )
    elif star_rating_col:
        weights = measure_summary[measure_weight_col] if measure_weight_col else 1.0
        current_star = _safe_div((measure_summary[star_rating_col] * weights).sum(), np.sum(weights))
        projected_star = min(current_star + default_gap_closure_rate, 5.0)
    else:
        current_star = None
        projected_star = None

    star_delta = 0.0
    if current_star is not None and projected_star is not None:
        star_delta = projected_star - current_star

    star_revenue_delta = star_delta * 10 * revenue_per_star_point  # star delta is on 1-5 scale

    projected_qbp = current_qbp - at_risk_amount + opportunity_amount
    projected_gap_rate = max(current_gap_rate - default_gap_closure_rate, 0.0)

    star_bridge = {
        "current_revenue": current_qbp,
        "gap_impact": at_risk_amount,
        "intervention_value": opportunity_amount,
        "projected_revenue": projected_qbp,
    }

    if member_value_df is not None and {"churn_probability", "member_lifetime_value"} <= set(member_value_df.columns):
        retention_value = float(
            (member_value_df["churn_probability"] * member_value_df["member_lifetime_value"]).sum()
        )
        churn_risk_score = float(member_value_df["churn_probability"].mean())
    else:
        retention_value = total_population * retention_value_per_member * churn_risk_multiplier * current_gap_rate
        churn_risk_score = min(1.0, churn_risk_multiplier * (1 + current_gap_rate))

    gross_benefit = opportunity_amount + star_revenue_delta + retention_value
    roi_percentage = (
        _safe_div(gross_benefit - intervention_cost, intervention_cost, 0.0) * 100 if intervention_cost else 0.0
    )
    payback_months = (
        _safe_div(intervention_cost, gross_benefit, float("inf")) * 12 if gross_benefit else float("inf")
    )

    value_components = {
        "current_qbp": current_qbp,
        "at_risk": at_risk_amount,
        "opportunity": opportunity_amount,
        "intervention_cost": intervention_cost,
        "net_revenue": net_revenue_impact,
        "star_delta": star_revenue_delta,
        "retention": retention_value,
        "gross_benefit": gross_benefit,
    }

    waterfall = [
        {"label": "Current QBP", "value": current_qbp, "type": "absolute"},
        {"label": "Revenue at Risk", "value": -at_risk_amount, "type": "relative"},
        {"label": "Opportunity Value", "value": opportunity_amount, "type": "relative"},
        {"label": "Projected QBP", "value": projected_qbp, "type": "total"},
    ]

    measure_breakdown: List[Dict[str, Any]] = []
    if gaps_col:
        for idx, row in measure_summary.iterrows():
            measure_name = row.get("measure", f"Measure {idx + 1}")
            eligible_members = float(row.get(eligible_col, 0.0) or 0.0)
            compliant_count = float(row.get(numerator_col, 0.0) or 0.0)
            if eligible_col is None and numerator_col is not None:
                eligible_members = compliant_count + float(row.get(gaps_col, 0.0) or 0.0)

            gaps_value = float(row.get(gaps_col, max(eligible_members - compliant_count, 0.0)) or 0.0)
            gap_rate = _safe_div(gaps_value, eligible_members)
            measure_at_risk = eligible_members * qbp_per_member * gap_rate
            measure_opportunity = measure_at_risk * default_gap_closure_rate
            measure_cost = gaps_value * intervention_cost_per_gap
            measure_net = measure_opportunity - measure_cost
            measure_roi = (_safe_div(measure_net, measure_cost, 0.0) * 100) if measure_cost else 0.0

            measure_breakdown.append(
                {
                    "measure": measure_name,
                    "eligible_members": eligible_members,
                    "gaps": gaps_value,
                    "gap_rate": gap_rate,
                    "at_risk": measure_at_risk,
                    "opportunity": measure_opportunity,
                    "intervention_cost": measure_cost,
                    "net_value": measure_net,
                    "roi_pct": measure_roi,
                }
            )

        measure_breakdown.sort(key=lambda entry: entry["net_value"], reverse=True)

    return FinancialSnapshot(
        current_qbp=current_qbp,
        projected_qbp=projected_qbp,
        at_risk_amount=at_risk_amount,
        opportunity_amount=opportunity_amount,
        intervention_cost=intervention_cost,
        net_revenue_impact=net_revenue_impact,
        star_revenue_delta=star_revenue_delta,
        member_retention_value=retention_value,
        churn_risk_score=churn_risk_score,
        star_bridge=star_bridge,
        total_population=float(total_population),
        gap_rate=float(current_gap_rate),
        projected_gap_rate=float(projected_gap_rate),
        qbp_per_member=float(qbp_per_member),
        roi_percentage=float(roi_percentage),
        payback_months=float(payback_months),
        gross_benefit=float(gross_benefit),
        value_components=value_components,
        waterfall=waterfall,
        measure_breakdown=measure_breakdown,
    )


# ---------------------------------------------------------------------------
# Operational metrics
# ---------------------------------------------------------------------------


def _build_funnel_rates(outreach_df: Optional[pd.DataFrame]) -> Dict[str, float]:
    if outreach_df is None or outreach_df.empty:
        return {}

    funnel_cols = {
        "eligible": "eligible_members",
        "outreach": "attempted",
        "contact": "contacted",
        "scheduled": "scheduled",
        "completed": "completed",
    }
    available = {stage: col for stage, col in funnel_cols.items() if col in outreach_df.columns}
    if not available:
        return {}

    totals = {stage: float(outreach_df[col].sum()) for stage, col in available.items()}
    conversion: Dict[str, float] = {}
    stages = list(available.keys())
    for idx in range(1, len(stages)):
        prev = stages[idx - 1]
        curr = stages[idx]
        conversion[f"{prev}_to_{curr}"] = _safe_div(totals[curr], totals[prev])
    return conversion


def calculate_operational_metrics(
    gap_history_df: Optional[pd.DataFrame],
    outreach_df: Optional[pd.DataFrame] = None,
    config: Optional[Mapping[str, Any]] = None,
) -> OperationalSnapshot:
    """Derive operational velocity, funnel, and engagement metrics."""

    operational_cfg = _get_nested(config, "analytics.operational", {}) or {}
    velocity_window_weeks = int(operational_cfg.get("velocity_window_weeks", 4))
    resample_rule = operational_cfg.get("resample_rule", "W")
    forecast_horizon = int(operational_cfg.get("forecast_horizon_weeks", 4))

    velocity_series: List[Dict[str, Any]] = []
    rolling_points: List[Dict[str, Any]] = []
    forecast_points: List[Dict[str, Any]] = []
    if gap_history_df is not None and not gap_history_df.empty:
        df = gap_history_df.copy()
        if "date" in df.columns:
            df["date"] = _ensure_datetime(df["date"])
            df = df.dropna(subset=["date"])
            weekly = (
                df.set_index("date")
                .sort_index()
                .resample(resample_rule)["gaps_closed"]
                .sum()
                .tail(max(velocity_window_weeks * 2, velocity_window_weeks))
            )
        else:
            weekly = pd.Series(df["gaps_closed"]).tail(velocity_window_weeks * 2)

        gap_velocity = float(weekly.tail(velocity_window_weeks).mean()) if not weekly.empty else 0.0
        prev_velocity = float(weekly.head(velocity_window_weeks).mean()) if len(weekly) >= velocity_window_weeks * 2 else gap_velocity

        if isinstance(weekly, pd.Series) and not weekly.empty:
            weekly_df = weekly.reset_index()
            weekly_df.columns = ["period", "gaps_closed"]
            velocity_series = [
                {
                    "date": period.to_pydatetime() if hasattr(period, "to_pydatetime") else period,
                    "gaps_closed": float(value),
                }
                for period, value in weekly_df.itertuples(index=False)
            ]

            rolling = weekly.rolling(window=max(velocity_window_weeks, 1), min_periods=1).mean()
            rolling_points = [
                {
                    "date": idx.to_pydatetime() if hasattr(idx, "to_pydatetime") else idx,
                    "rolling_avg": float(val),
                }
                for idx, val in rolling.items()
            ]

            if not rolling.empty:
                last_period = weekly.index[-1]
                last_avg = float(rolling.iloc[-1])
                slope = (gap_velocity - prev_velocity) / max(velocity_window_weeks, 1)
                for step in range(1, forecast_horizon + 1):
                    future_date = last_period + pd.Timedelta(weeks=step)
                    expected = max(last_avg + slope * step, 0.0)
                    forecast_points.append(
                        {
                            "date": future_date.to_pydatetime() if hasattr(future_date, "to_pydatetime") else future_date,
                            "expected_gaps": expected,
                        }
                    )

        if np.isclose(prev_velocity, gap_velocity):
            recent_trend = "flat"
        else:
            recent_trend = "up" if gap_velocity > prev_velocity else "down"

        if "days_to_close" in df.columns:
            avg_days_to_close = float(df["days_to_close"].mean())
        else:
            avg_days_to_close = float(operational_cfg.get("default_days_to_close", 30))
    else:
        gap_velocity = 0.0
        recent_trend = "flat"
        avg_days_to_close = float(operational_cfg.get("default_days_to_close", 30))

    engagement_summary: Dict[str, float] = {}
    channel_performance: List[Dict[str, Any]] = []
    if outreach_df is not None and not outreach_df.empty:
        outreach_summary = {
            "contact_success_rate": _safe_div(outreach_df.get("contacted", 0).sum(), outreach_df.get("attempted", 0).sum()),
            "conversion_rate": _safe_div(outreach_df.get("completed", 0).sum(), outreach_df.get("scheduled", 0).sum()),
            "no_show_rate": _safe_div(outreach_df.get("no_show", 0).sum(), outreach_df.get("scheduled", 0).sum()),
        }

        eligible_total = float(outreach_df.get("eligible_members", 0).sum())
        attempted_total = float(outreach_df.get("attempted", 0).sum())
        contacted_total = float(outreach_df.get("contacted", 0).sum())
        scheduled_total = float(outreach_df.get("scheduled", 0).sum())
        completed_total = float(outreach_df.get("completed", 0).sum())

        engagement_summary = {
            "attempts_per_member": _safe_div(attempted_total, eligible_total),
            "contacts_per_member": _safe_div(contacted_total, eligible_total),
            "response_rate": _safe_div(contacted_total, attempted_total),
            "completion_rate": _safe_div(completed_total, max(scheduled_total, 1.0)),
            "first_contact_rate": _safe_div(contacted_total, eligible_total),
        }

        channel_metrics: Dict[str, Dict[str, float]] = {}
        for column in outreach_df.columns:
            if not column.startswith("channel_"):
                continue
            parts = column.split("_")
            if len(parts) < 3:
                continue
            _, channel_name, metric_name = parts[0], parts[1], "_".join(parts[2:])
            channel_entry = channel_metrics.setdefault(channel_name, {})
            channel_entry[metric_name] = float(outreach_df[column].sum())

        for channel_name, metrics in channel_metrics.items():
            attempts = metrics.get("attempts", 0.0)
            contacts = metrics.get("contacts", metrics.get("contacted", 0.0))
            scheduled = metrics.get("scheduled", metrics.get("appointments", 0.0))
            completed = metrics.get("completed", 0.0)

            channel_performance.append(
                {
                    "channel": channel_name.replace("-", " ").title(),
                    "attempts": attempts,
                    "contacts": contacts,
                    "scheduled": scheduled,
                    "completed": completed,
                    "contact_rate": _safe_div(contacts, attempts),
                    "completion_rate": _safe_div(completed, contacts if contacts else attempts),
                }
            )

        channel_performance.sort(key=lambda entry: entry.get("completed", 0.0), reverse=True)
    else:
        outreach_summary = {}

    funnel_conversion = _build_funnel_rates(outreach_df)

    return OperationalSnapshot(
        gap_velocity_per_week=gap_velocity,
        recent_trend=recent_trend,
        avg_days_to_close=avg_days_to_close,
        funnel_conversion=funnel_conversion,
        outreach_summary=outreach_summary,
        velocity_series=velocity_series,
        rolling_velocity=rolling_points,
        forecast_velocity=forecast_points,
        engagement_summary=engagement_summary,
        channel_performance=channel_performance,
    )


# ---------------------------------------------------------------------------
# HEI / Equity metrics
# ---------------------------------------------------------------------------


def calculate_equity_metrics(
    equity_df: Optional[pd.DataFrame],
    config: Optional[Mapping[str, Any]] = None,
    srf_column: str = "srf_flag",
    compliant_column: str = "compliant",
) -> EquitySnapshot:
    """Summarize SRF segmentation and health equity performance gaps."""

    hei_cfg = _get_nested(config, "analytics.hei", {}) or {}
    disparity_threshold = float(hei_cfg.get("disparity_threshold", 5.0))
    reward_factor_projection = float(hei_cfg.get("reward_factor_projection", 0.05))

    if equity_df is None or equity_df.empty or srf_column not in equity_df.columns:
        return EquitySnapshot(
            srf_population_pct=0.0,
            equity_gap_pct=0.0,
            hei_reward_projection=0.0,
            disparity_flag=False,
            hei_score=0.0,
            readiness_level="Monitoring",
        )

    df = equity_df.copy()
    df["is_srf"] = df[srf_column].astype(bool)
    compliant_series = df[compliant_column] if compliant_column in df.columns else pd.Series(1, index=df.index)

    total_members = len(df)
    srf_members = int(df["is_srf"].sum())
    srf_population_pct = _safe_div(srf_members, total_members)

    srf_compliance = _safe_div(compliant_series[df["is_srf"]].sum(), df["is_srf"].sum(), default=0.0)
    non_srf_compliance = _safe_div(compliant_series[~df["is_srf"]].sum(), (~df["is_srf"]).sum(), default=0.0)
    equity_gap = (non_srf_compliance - srf_compliance) * 100  # convert to percentage points

    disparity_flag = abs(equity_gap) >= disparity_threshold
    hei_reward_projection = max(0.0, reward_factor_projection * (1 - abs(equity_gap) / 100))

    hei_score = max(0.0, 100 - abs(equity_gap))
    if hei_score >= 85:
        readiness_level = "On Track"
    elif hei_score >= 70:
        readiness_level = "Monitoring"
    else:
        readiness_level = "Action Required"

    heatmap_rows: List[Dict[str, Any]] = []
    disparity_segments: List[Dict[str, Any]] = []

    segment_col = "segment" if "segment" in df.columns else None
    if segment_col:
        total_members = len(df)
        for segment_value, seg_df in df.groupby(segment_col):
            seg_total = len(seg_df)
            if seg_total == 0:
                continue
            srf_seg = seg_df[seg_df["is_srf"]]
            non_srf_seg = seg_df[~seg_df["is_srf"]]

            srf_rate = _safe_div(srf_seg[compliant_column].sum(), len(srf_seg), 0.0) if len(srf_seg) else 0.0
            non_srf_rate = _safe_div(non_srf_seg[compliant_column].sum(), len(non_srf_seg), 0.0) if len(non_srf_seg) else srf_rate
            gap_pp = (non_srf_rate - srf_rate) * 100

            heatmap_rows.append(
                {
                    "segment": segment_value,
                    "srf_rate": srf_rate * 100,
                    "non_srf_rate": non_srf_rate * 100,
                    "gap": gap_pp,
                    "population_pct": _safe_div(seg_total, total_members) * 100,
                }
            )

        disparity_segments = sorted(heatmap_rows, key=lambda item: abs(item["gap"]), reverse=True)[:3]

    trend_summary = {
        "srf_population_pct": float(srf_population_pct * 100),
        "equity_gap_pct": float(equity_gap),
        "hei_score": float(hei_score),
    }

    return EquitySnapshot(
        srf_population_pct=float(srf_population_pct),
        equity_gap_pct=float(equity_gap),
        hei_reward_projection=float(hei_reward_projection),
        disparity_flag=bool(disparity_flag),
        hei_score=float(hei_score),
        readiness_level=readiness_level,
        disparity_segments=disparity_segments,
        heatmap=heatmap_rows,
        trend_summary=trend_summary,
    )


# ---------------------------------------------------------------------------
# Provider metrics
# ---------------------------------------------------------------------------


def calculate_provider_metrics(
    provider_df: Optional[pd.DataFrame],
    config: Optional[Mapping[str, Any]] = None,
) -> ProviderSnapshot:
    """Aggregate provider-level performance metrics."""

    provider_cfg = _get_nested(config, "analytics.provider", {}) or {}
    leaderboard_limit = int(provider_cfg.get("top_provider_limit", 10))
    outlier_min_panel = int(provider_cfg.get("outlier_min_panel", 150))
    closure_col = provider_cfg.get("closure_rate_column", "gap_closure_rate")
    panel_col = provider_cfg.get("panel_size_column", "panel_size")

    if provider_df is None or provider_df.empty:
        return ProviderSnapshot(
            avg_gap_closure_rate=0.0,
            high_performers=[],
            low_performers=[],
            outlier_providers=[],
        )

    df = provider_df.copy()
    if closure_col not in df.columns or df[closure_col].isna().all():
        closed = df.get("gaps_closed")
        denominator = df.get("eligible_members")
        if denominator is None or denominator.isna().all():
            denominator = df.get("gaps_open")

        if closed is None:
            df[closure_col] = 0.0
        else:
            denominator = denominator.replace({0: np.nan}) if denominator is not None else None
            closure_rate_series = closed.div(denominator).fillna(0.0) if denominator is not None else closed * 0.0
            df[closure_col] = closure_rate_series
    if panel_col not in df.columns:
        df[panel_col] = df.get("panel_size", 0)

    df = df.replace([np.inf, -np.inf], np.nan).fillna(0)
    avg_rate = float(df[closure_col].mean())

    def _serialize(rows: pd.DataFrame) -> Iterable[Dict[str, Any]]:
        return rows[["provider_id", closure_col, panel_col, "gaps_closed", "gaps_open"]].to_dict(orient="records")

    high_performers = _serialize(df.sort_values(closure_col, ascending=False).head(leaderboard_limit))
    low_performers = _serialize(df.sort_values(closure_col, ascending=True).head(leaderboard_limit))
    outliers = _serialize(df[(df[panel_col] >= outlier_min_panel) & (df[closure_col] < avg_rate * 0.5)])

    return ProviderSnapshot(
        avg_gap_closure_rate=avg_rate,
        high_performers=high_performers,
        low_performers=low_performers,
        outlier_providers=outliers,
    )


# ---------------------------------------------------------------------------
# Competitive metrics
# ---------------------------------------------------------------------------


def calculate_competitive_metrics(
    benchmark_df: Optional[pd.DataFrame],
    config: Optional[Mapping[str, Any]] = None,
    plan_column: str = "plan_name",
    star_column: str = "star_rating",
    enrollment_column: str = "enrollment",
    focus_plan: Optional[str] = None,
) -> CompetitiveSnapshot:
    """Combine external benchmark data into competitive positioning KPIs."""

    comp_cfg = _get_nested(config, "analytics.competitive", {}) or {}
    default_market_share = float(comp_cfg.get("default_market_share", 0.12))
    star_gain_value_per_member = float(comp_cfg.get("star_gain_value_per_member", 120.0))

    if benchmark_df is None or benchmark_df.empty:
        return CompetitiveSnapshot(
            market_percentile=0.0,
            star_delta_vs_market=0.0,
            enrollment_share=default_market_share,
            projected_gain=0.0,
        )

    df = benchmark_df.copy()
    if focus_plan is None:
        focus_plan = comp_cfg.get("focus_plan") or df[plan_column].iloc[0]

    if focus_plan not in df[plan_column].values:
        logger.warning("Focus plan '%s' not present in benchmark data; defaulting to first entry.", focus_plan)
        focus_plan = df[plan_column].iloc[0]

    focus_row = df[df[plan_column] == focus_plan].iloc[0]
    focus_star = float(focus_row.get(star_column, 0.0))
    focus_enrollment = float(focus_row.get(enrollment_column, 0.0))

    market_percentile = _safe_div((df[star_column] < focus_star).sum(), len(df))
    star_delta_vs_market = focus_star - float(df[star_column].mean())

    total_enrollment = _safe_sum(df.get(enrollment_column, focus_enrollment))
    enrollment_share = _safe_div(focus_enrollment, total_enrollment, default_market_share)

    projected_gain = focus_enrollment * star_gain_value_per_member * max(star_delta_vs_market, 0)

    return CompetitiveSnapshot(
        market_percentile=float(market_percentile),
        star_delta_vs_market=float(star_delta_vs_market),
        enrollment_share=float(enrollment_share),
        projected_gain=float(projected_gain),
    )


# ---------------------------------------------------------------------------
# KPI bundle orchestrator
# ---------------------------------------------------------------------------


@dataclass
class KPIInputData:
    measure_summary: pd.DataFrame
    star_summary: Optional[Mapping[str, Any]] = None
    gap_history: Optional[pd.DataFrame] = None
    outreach: Optional[pd.DataFrame] = None
    member_value: Optional[pd.DataFrame] = None
    equity: Optional[pd.DataFrame] = None
    provider: Optional[pd.DataFrame] = None
    competitive: Optional[pd.DataFrame] = None


def build_kpi_bundle(inputs: KPIInputData, config: Optional[Mapping[str, Any]] = None) -> KPIBundle:
    """Generate an aggregated KPI bundle from prepared input dataframes."""

    financial = calculate_financial_metrics(
        inputs.measure_summary,
        star_summary=inputs.star_summary,
        member_value_df=inputs.member_value,
        config=config,
    )

    operational = calculate_operational_metrics(
        inputs.gap_history,
        outreach_df=inputs.outreach,
        config=config,
    )

    equity = calculate_equity_metrics(
        inputs.equity,
        config=config,
    )

    provider = calculate_provider_metrics(
        inputs.provider,
        config=config,
    )

    competitive = calculate_competitive_metrics(
        inputs.competitive,
        config=config,
    )

    return KPIBundle(
        financial=financial,
        operational=operational,
        equity=equity,
        provider=provider,
        competitive=competitive,
    )


__all__ = [
    "calculate_financial_metrics",
    "calculate_operational_metrics",
    "calculate_equity_metrics",
    "calculate_provider_metrics",
    "calculate_competitive_metrics",
    "build_kpi_bundle",
    "FinancialSnapshot",
    "OperationalSnapshot",
    "EquitySnapshot",
    "ProviderSnapshot",
    "CompetitiveSnapshot",
    "KPIBundle",
    "KPIInputData",
]


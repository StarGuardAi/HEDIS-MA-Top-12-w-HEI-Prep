"""
Unit tests for KPI analytics engine.
"""

import math
import sys
from pathlib import Path

import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.data.kpi_engine import (  # noqa: E402  pylint: disable=wrong-import-position
    KPIInputData,
    build_kpi_bundle,
    calculate_competitive_metrics,
    calculate_equity_metrics,
    calculate_financial_metrics,
    calculate_operational_metrics,
    calculate_provider_metrics,
)


def _base_config():
    return {
        "analytics": {
            "financial": {
                "qbp_per_member": 372,
                "default_gap_closure_rate": 0.3,
                "intervention_cost_per_gap": 150,
                "retention_value_per_member": 1200,
                "churn_risk_multiplier": 0.15,
            },
            "operational": {
                "velocity_window_weeks": 4,
                "resample_rule": "W",
                "default_days_to_close": 30,
            },
            "hei": {
                "disparity_threshold": 5.0,
                "reward_factor_projection": 0.05,
            },
            "provider": {
                "top_provider_limit": 5,
                "outlier_min_panel": 150,
                "closure_rate_column": "gap_closure_rate",
                "panel_size_column": "panel_size",
            },
            "competitive": {
                "default_market_share": 0.12,
                "star_gain_value_per_member": 120.0,
            },
        },
        "roi": {"intervention_costs": {"average": 150}},
        "star_rating": {"revenue_per_star_point": 50000},
    }


def test_calculate_financial_metrics_basic_scenario():
    measure_df = pd.DataFrame(
        {
            "measure": ["GSD", "KED"],
            "eligible_members": [100, 80],
            "compliant_members": [80, 56],
            "gaps": [20, 24],
            "star_rating": [4.0, 3.5],
            "measure_weight": [3.0, 3.0],
        }
    )

    metrics = calculate_financial_metrics(measure_df, config=_base_config())

    # Total population 180 * $372
    assert math.isclose(metrics.current_qbp, 180 * 372, rel_tol=1e-5)
    assert metrics.at_risk_amount > 0
    assert metrics.opportunity_amount > 0
    assert metrics.net_revenue_impact == metrics.opportunity_amount - metrics.intervention_cost
    assert metrics.star_bridge["projected_revenue"] == metrics.star_bridge["current_revenue"] - metrics.star_bridge["gap_impact"] + metrics.star_bridge["intervention_value"]


def test_operational_metrics_handles_gap_history_and_outreach():
    gap_history = pd.DataFrame(
        {
            "date": pd.date_range("2025-01-01", periods=8, freq="W"),
            "gaps_closed": [10, 12, 14, 16, 18, 20, 22, 24],
            "days_to_close": [30, 28, 27, 26, 25, 24, 23, 22],
        }
    )
    outreach = pd.DataFrame(
        {
            "eligible_members": [100],
            "attempted": [80],
            "contacted": [60],
            "scheduled": [40],
            "completed": [30],
            "no_show": [5],
        }
    )

    snapshot = calculate_operational_metrics(gap_history, outreach_df=outreach, config=_base_config())

    assert snapshot.gap_velocity_per_week > 0
    assert snapshot.recent_trend in {"up", "down", "flat"}
    assert "eligible_to_outreach" in snapshot.funnel_conversion
    assert "contact_success_rate" in snapshot.outreach_summary


def test_equity_metrics_flags_disparity():
    equity_df = pd.DataFrame(
        {
            "member_id": range(10),
            "srf_flag": [True] * 5 + [False] * 5,
            "compliant": [0, 0, 0, 0, 0, 1, 1, 1, 1, 1],
        }
    )

    snapshot = calculate_equity_metrics(equity_df, config=_base_config())

    assert snapshot.srf_population_pct == 0.5
    assert snapshot.disparity_flag is True
    assert snapshot.equity_gap_pct > 0


def test_provider_metrics_surface_outliers():
    provider_df = pd.DataFrame(
        {
            "provider_id": ["A", "B", "C"],
            "gaps_closed": [40, 10, 5],
            "gaps_open": [80, 50, 40],
            "panel_size": [400, 180, 220],
            "gap_closure_rate": [0.5, 0.2, 0.125],
        }
    )

    snapshot = calculate_provider_metrics(provider_df, config=_base_config())

    assert snapshot.avg_gap_closure_rate > 0
    assert len(list(snapshot.high_performers)) >= 1
    assert len(list(snapshot.low_performers)) >= 1


def test_competitive_metrics_returns_expected_fields():
    benchmark_df = pd.DataFrame(
        {
            "plan_name": ["Focus", "Competitor A", "Competitor B"],
            "star_rating": [4.2, 3.8, 4.0],
            "enrollment": [50000, 40000, 30000],
        }
    )

    snapshot = calculate_competitive_metrics(benchmark_df, config=_base_config(), focus_plan="Focus")

    assert snapshot.market_percentile >= 0
    assert snapshot.enrollment_share > 0


def test_build_kpi_bundle_combines_all_sections():
    inputs = KPIInputData(
        measure_summary=pd.DataFrame(
            {
                "measure": ["GSD"],
                "eligible_members": [100],
                "compliant_members": [80],
                "gaps": [20],
            }
        ),
        gap_history=pd.DataFrame({"date": pd.date_range("2025-01-01", periods=4, freq="W"), "gaps_closed": [5, 6, 7, 8]}),
        outreach=pd.DataFrame({"eligible_members": [50], "attempted": [40], "contacted": [30], "scheduled": [20], "completed": [15], "no_show": [2]}),
        equity=pd.DataFrame({"member_id": [1, 2], "srf_flag": [True, False], "compliant": [0, 1]}),
        provider=pd.DataFrame({"provider_id": ["A"], "gaps_closed": [10], "gaps_open": [20], "panel_size": [200]}),
        competitive=pd.DataFrame({"plan_name": ["Focus"], "star_rating": [4.0], "enrollment": [50000]}),
    )

    bundle = build_kpi_bundle(inputs, config=_base_config())
    bundle_dict = bundle.to_dict()

    assert "financial" in bundle_dict
    assert "operational" in bundle_dict
    assert "equity" in bundle_dict
    assert "provider" in bundle_dict
    assert "competitive" in bundle_dict


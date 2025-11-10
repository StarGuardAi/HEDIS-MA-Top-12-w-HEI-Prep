import pandas as pd
import pytest

from src.data.kpi_engine import calculate_financial_metrics


@pytest.fixture()
def sample_financial_inputs():
    measure_summary = pd.DataFrame(
        [
            {
                "measure": "BCS",
                "measure_weight": 3.0,
                "eligible_members": 600,
                "compliant_members": 420,
                "gaps": 180,
                "star_rating": 3.4,
            },
            {
                "measure": "CBP",
                "measure_weight": 2.0,
                "eligible_members": 400,
                "compliant_members": 260,
                "gaps": 140,
                "star_rating": 3.2,
            },
        ]
    )

    star_summary = {
        "current_weighted_stars": 3.4,
        "projected_weighted_stars": 3.8,
    }

    config = {
        "analytics": {
            "financial": {
                "qbp_per_member": 400.0,
                "default_gap_closure_rate": 0.25,
                "intervention_cost_per_gap": 120.0,
                "retention_value_per_member": 900.0,
            }
        },
        "roi": {"intervention_costs": {"average": 120.0}},
        "star_rating": {"revenue_per_star_point": 60000.0},
    }

    return measure_summary, star_summary, config


def test_financial_snapshot_includes_roi_details(sample_financial_inputs):
    measure_summary, star_summary, config = sample_financial_inputs

    snapshot = calculate_financial_metrics(
        measure_summary,
        star_summary=star_summary,
        member_value_df=None,
        config=config,
    )

    assert snapshot.total_population == pytest.approx(1000.0)
    assert snapshot.projected_qbp == pytest.approx(snapshot.current_qbp - snapshot.at_risk_amount + snapshot.opportunity_amount)
    assert snapshot.gross_benefit > snapshot.net_revenue_impact
    assert snapshot.roi_percentage > -100.0
    assert snapshot.payback_months != float("inf")
    assert snapshot.value_components["gross_benefit"] == pytest.approx(snapshot.gross_benefit)

    waterfall_labels = [entry["label"] for entry in snapshot.waterfall]
    assert waterfall_labels == ["Current QBP", "Revenue at Risk", "Opportunity Value", "Projected QBP"]


def test_measure_breakdown_sorted_by_net_value(sample_financial_inputs):
    measure_summary, star_summary, config = sample_financial_inputs

    snapshot = calculate_financial_metrics(
        measure_summary,
        star_summary=star_summary,
        member_value_df=None,
        config=config,
    )

    breakdown = snapshot.measure_breakdown
    assert len(breakdown) == 2
    assert breakdown[0]["net_value"] >= breakdown[1]["net_value"]
    assert all("roi_pct" in entry for entry in breakdown)

import pandas as pd

from src.data.kpi_engine import calculate_equity_metrics


def _sample_equity_dataframe() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "member_id": [f"M{i:03d}" for i in range(1, 101)],
            "srf_flag": [True] * 45 + [False] * 55,
            "compliant": [1] * 30 + [0] * 15 + [1] * 40 + [0] * 15,
            "segment": (['Dual Eligible'] * 20 + ['Limited English'] * 25 + ['Rural'] * 30 + ['Disability'] * 25 + ['Core Population'] * 0)[:100],
        }
    )


def test_equity_snapshot_contains_heatmap_and_disparities():
    equity_df = _sample_equity_dataframe()
    snapshot = calculate_equity_metrics(equity_df, config=None, srf_column="srf_flag", compliant_column="compliant")

    assert snapshot.heatmap, "Expected populated HEI heatmap data"
    assert snapshot.disparity_segments, "Expected at least one highlighted disparity segment"
    assert snapshot.heatmap[0]["segment"] in equity_df["segment"].unique()
    assert snapshot.readiness_level in {"On Track", "Monitoring", "Action Required"}


def test_equity_snapshot_readiness_trend_summary():
    equity_df = _sample_equity_dataframe()
    snapshot = calculate_equity_metrics(equity_df, config=None, srf_column="srf_flag", compliant_column="compliant")

    assert "hei_score" in snapshot.trend_summary
    assert snapshot.trend_summary["hei_score"] == snapshot.hei_score
    assert "srf_population_pct" in snapshot.trend_summary

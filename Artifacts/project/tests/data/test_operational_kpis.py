import pandas as pd
import pytest

from src.data.kpi_engine import calculate_operational_metrics


def _sample_gap_history() -> pd.DataFrame:
    dates = pd.date_range("2025-01-01", periods=8, freq="W")
    return pd.DataFrame(
        {
            "date": dates,
            "gaps_closed": [120, 135, 150, 165, 180, 195, 210, 225],
            "days_to_close": [32, 30, 29, 27, 25, 24, 22, 21],
        }
    )


def _sample_outreach() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "eligible_members": [10000],
            "attempted": [7800],
            "contacted": [5600],
            "scheduled": [4300],
            "completed": [3200],
            "no_show": [450],
            "channel_phone_attempts": [3100],
            "channel_phone_contacts": [2300],
            "channel_phone_completed": [1650],
            "channel_sms_attempts": [2200],
            "channel_sms_contacts": [1600],
            "channel_sms_completed": [930],
            "channel_portal_attempts": [1500],
            "channel_portal_contacts": [1100],
            "channel_portal_completed": [720],
            "channel_inperson_attempts": [1000],
            "channel_inperson_contacts": [900],
            "channel_inperson_completed": [650],
        }
    )


@pytest.fixture()
def operational_snapshot():
    gap_history = _sample_gap_history()
    outreach = _sample_outreach()
    snapshot = calculate_operational_metrics(gap_history, outreach_df=outreach, config=None)
    return snapshot


def test_operational_snapshot_contains_velocity_details(operational_snapshot):
    assert operational_snapshot.velocity_series
    assert operational_snapshot.rolling_velocity
    assert operational_snapshot.forecast_velocity
    assert operational_snapshot.recent_trend in {"up", "down", "flat"}


def test_operational_snapshot_channel_performance(operational_snapshot):
    channels = operational_snapshot.channel_performance
    names = {entry["channel"] for entry in channels}
    assert {"Phone", "Sms", "Portal", "Inperson"}.issubset(names)
    for entry in channels:
        assert "contact_rate" in entry
        assert 0.0 <= entry["contact_rate"] <= 1.0
        assert 0.0 <= entry["completion_rate"] <= 1.0


def test_operational_snapshot_engagement_metrics(operational_snapshot):
    engagement = operational_snapshot.engagement_summary
    assert pytest.approx(engagement["attempts_per_member"], rel=1e-2) == 0.78
    assert "response_rate" in engagement
    assert engagement["completion_rate"] <= 1.0

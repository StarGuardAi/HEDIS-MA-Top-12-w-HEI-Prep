import pandas as pd
from streamlit.testing.v1 import AppTest

from src.data.kpi_engine import calculate_operational_metrics
from streamlit_pages.operations_command import render_operations_command


def _operations_demo_app():
    import pandas as _pd  # local import for AppTest sandbox
    from src.data.kpi_engine import calculate_operational_metrics as _calc_metrics
    from streamlit_pages.operations_command import render_operations_command as _render_operations

    gap_history = _pd.DataFrame(
        {
            "date": _pd.date_range("2025-01-01", periods=6, freq="W"),
            "gaps_closed": [110, 135, 150, 175, 190, 205],
            "days_to_close": [30, 29, 27, 26, 24, 23],
        }
    )

    outreach = _pd.DataFrame(
        {
            "eligible_members": [9500],
            "attempted": [7200],
            "contacted": [5100],
            "scheduled": [3900],
            "completed": [2950],
            "no_show": [410],
            "channel_phone_attempts": [2800],
            "channel_phone_contacts": [2000],
            "channel_phone_completed": [1450],
            "channel_sms_attempts": [2000],
            "channel_sms_contacts": [1450],
            "channel_sms_completed": [840],
            "channel_portal_attempts": [1400],
            "channel_portal_contacts": [900],
            "channel_portal_completed": [620],
            "channel_inperson_attempts": [1000],
            "channel_inperson_contacts": [850],
            "channel_inperson_completed": [640],
        }
    )

    snapshot = _calc_metrics(gap_history, outreach_df=outreach, config=None)
    _render_operations(snapshot, gap_history, outreach)


def test_operations_command_renders_without_errors():
    app = AppTest.from_function(_operations_demo_app)
    app.run(timeout=10)
    assert not app.exception
    assert len(app.metric) >= 3

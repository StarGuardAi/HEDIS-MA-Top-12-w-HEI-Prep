import pandas as pd
from streamlit.testing.v1 import AppTest


def _predictive_demo_app():
    import pandas as _pd
    import numpy as _np
    from src.data.kpi_engine import calculate_equity_metrics
    from streamlit_pages.predictive_priority import render_predictive_priority

    priority_df = _pd.DataFrame(
        {
            "Member ID": [f"M{i:03d}" for i in range(1, 51)],
            "Risk Tier": ["High"] * 20 + ["Medium"] * 15 + ["Low"] * 15,
            "Gap Probability": _np.linspace(0.2, 0.95, 50),
            "Financial Value": _np.linspace(500, 2500, 50),
            "Expected ROI": _np.linspace(1.5, 5.0, 50),
            "Priority Score": _np.linspace(100, 500, 50),
            "Intervention Priority": ["High"] * 20 + ["Medium"] * 15 + ["Low"] * 15,
            "Recommended Actions": ["Outreach"] * 50,
        }
    )

    diagnostics = {
        "auc": 0.89,
        "lift_curve": _pd.DataFrame({"decile": [10, 20, 30, 40, 50], "lift": [2.5, 2.1, 1.8, 1.4, 1.2]}),
    }

    equity_df = _pd.DataFrame(
        {
            "member_id": [f"E{i:03d}" for i in range(1, 121)],
            "srf_flag": [True] * 60 + [False] * 60,
            "compliant": [1] * 45 + [0] * 15 + [1] * 35 + [0] * 25,
            "segment": (['Dual Eligible'] * 30 + ['Limited English'] * 30 + ['Rural'] * 30 + ['Disability'] * 30),
        }
    )

    snapshot = calculate_equity_metrics(equity_df, config=None, srf_column="srf_flag", compliant_column="compliant")
    render_predictive_priority(priority_df, diagnostics, snapshot)


def test_predictive_priority_renders_without_errors():
    app = AppTest.from_function(_predictive_demo_app)
    app.run(timeout=10)
    assert not app.exception
    assert len(app.metric) >= 3

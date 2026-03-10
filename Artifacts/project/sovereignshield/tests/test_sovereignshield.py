"""
SovereignShield Sprint 1 — chart module tests.
6 tests covering heatmap_data, mttr_trend_data, donut_data, kb_growth_data,
compliance_heatmap, mttr_trend.
"""
from __future__ import annotations

import sys
from pathlib import Path

# Ensure sovereignshield package is importable (run from repo root or Artifacts/project/)
_root = Path(__file__).resolve().parents[2]
if str(_root) not in sys.path:
    sys.path.insert(0, str(_root))

import pandas as pd
import pytest

from sovereignshield.core.charts import (
    compliance_heatmap,
    donut_data,
    heatmap_data,
    kb_growth_data,
    mttr_trend,
    mttr_trend_data,
)


def test_heatmap_data_columns():
    """heatmap_data returns DataFrame with resource_id, violation_type, status, run_count."""
    runs = [
        {"resource_id": "s3-x", "violation_type": "data_residency", "is_compliant": True},
        {"resource_id": "ec2-y", "violation_type": "encryption", "is_compliant": False},
    ]
    df = heatmap_data(runs)
    assert isinstance(df, pd.DataFrame)
    assert set(df.columns) >= {"resource_id", "violation_type", "status", "run_count"}
    assert len(df) == 2
    assert df["status"].iloc[0] == "compliant"
    assert df["status"].iloc[1] == "violation"


def test_mttr_trend_data_shape():
    """mttr_trend_data returns DataFrame with run_index, mttr_seconds, timestamp; respects limit."""
    runs = [
        {"timestamp": "2025-03-09T10:00:00", "mttr_seconds": 4.2},
        {"timestamp": "2025-03-09T11:00:00", "mttr_seconds": 3.1},
        {"timestamp": "2025-03-09T12:00:00", "mttr_seconds": 5.0},
    ]
    df = mttr_trend_data(runs, limit=20)
    assert isinstance(df, pd.DataFrame)
    assert set(df.columns) >= {"run_index", "mttr_seconds", "timestamp"}
    assert len(df) == 3
    df2 = mttr_trend_data(runs, limit=2)
    assert len(df2) == 2


def test_donut_data_counts():
    """donut_data returns severity counts for HIGH, MEDIUM, LOW, INFO."""
    runs = [
        {"severity": "HIGH"},
        {"severity": "HIGH"},
        {"severity": "MEDIUM"},
        {"severity": "LOW"},
        {"severity": "INFO"},
    ]
    df = donut_data(runs)
    assert isinstance(df, pd.DataFrame)
    assert set(df.columns) >= {"severity", "count"}
    high_row = df[df["severity"] == "HIGH"]
    assert len(high_row) == 1
    assert high_row["count"].iloc[0] == 2
    assert df["count"].sum() == 5


def test_kb_growth_data_nonnegative():
    """kb_growth_data returns session/kb_added with non-negative counts."""
    runs = [
        {"timestamp": "2025-03-09T10:00:00", "is_compliant": True},
        {"timestamp": "2025-03-09T10:30:00", "is_compliant": True},
        {"timestamp": "2025-03-09T10:45:00", "is_compliant": False},
        {"timestamp": "2025-03-10T09:00:00", "is_compliant": True},
    ]
    df = kb_growth_data(runs)
    assert isinstance(df, pd.DataFrame)
    assert set(df.columns) >= {"session", "kb_added"}
    assert (df["kb_added"] >= 0).all()
    # 2 compliant on 2025-03-09, 1 on 2025-03-10
    assert df["kb_added"].sum() == 3


def test_compliance_heatmap_returns_ggplot():
    """compliance_heatmap returns a plotnine ggplot object."""
    pytest.importorskip("plotnine")
    runs = [
        {"resource_id": "s3-x", "violation_type": "data_residency", "is_compliant": True},
    ]
    p = compliance_heatmap(runs)
    assert p is not None
    assert hasattr(p, "draw") or "ggplot" in type(p).__name__ or "ggplot" in str(type(p))


def test_mttr_trend_returns_ggplot():
    """mttr_trend returns a plotnine ggplot object."""
    pytest.importorskip("plotnine")
    runs = [
        {"timestamp": "2025-03-09T10:00:00", "mttr_seconds": 4.2},
        {"timestamp": "2025-03-09T11:00:00", "mttr_seconds": 3.1},
    ]
    p = mttr_trend(runs, limit=20)
    assert p is not None
    assert hasattr(p, "draw") or "ggplot" in type(p).__name__ or "ggplot" in str(type(p))

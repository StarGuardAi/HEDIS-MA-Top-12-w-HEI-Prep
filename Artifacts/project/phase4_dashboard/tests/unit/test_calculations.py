"""
Unit tests for calculation accuracy
"""
import pytest
import pandas as pd
import numpy as np
from utils.scenario_modeler import ScenarioModeler
from utils.roi_calculator import ROICalculator
from utils.historical_tracking import HistoricalTracker


class TestROICalculations:
    """Test ROI calculation accuracy."""
    
    def test_roi_calculator_initialization(self, roi_calculator):
        """Test ROI calculator initializes with defaults."""
        assert roi_calculator.defaults is not None
        assert "quality_bonus_per_member_per_star" in roi_calculator.defaults
        assert "revenue_per_closure" in roi_calculator.defaults
        assert roi_calculator.defaults["revenue_per_closure"] == 100.0
    
    def test_confidence_interval_calculation(self, roi_calculator):
        """Test confidence interval calculation accuracy."""
        # Test with known values
        successes = 80
        total = 100
        ci_lower, ci_upper = roi_calculator._calculate_confidence_interval(
            successes, total, 0.95
        )
        
        # CI should be within 0-100%
        assert 0 <= ci_lower <= 100
        assert 0 <= ci_upper <= 100
        assert ci_lower <= ci_upper
        
        # Point estimate should be within CI
        point_estimate = (successes / total) * 100
        assert ci_lower <= point_estimate <= ci_upper
    
    def test_confidence_interval_edge_cases(self, roi_calculator):
        """Test confidence interval with edge cases."""
        # All successes
        ci_lower, ci_upper = roi_calculator._calculate_confidence_interval(100, 100, 0.95)
        assert ci_upper <= 100
        
        # No successes
        ci_lower, ci_upper = roi_calculator._calculate_confidence_interval(0, 100, 0.95)
        assert ci_lower >= 0
        
        # Zero total
        ci_lower, ci_upper = roi_calculator._calculate_confidence_interval(0, 0, 0.95)
        assert ci_lower == 0 and ci_upper == 0


class TestScenarioCalculations:
    """Test scenario modeling calculations."""
    
    def test_scenario_calculation_basic(self, scenario_modeler):
        """Test basic scenario calculation."""
        budget = 250000
        fte_count = 5
        
        scenario = scenario_modeler.calculate_scenario(budget, fte_count, "balanced")
        
        assert scenario["budget"] == budget
        assert scenario["fte_count"] == fte_count
        assert scenario["predicted_interventions"] >= 0
        assert scenario["predicted_closures"] >= 0
        assert scenario["predicted_revenue"] >= 0
        assert scenario["total_costs"] >= 0
        assert "predicted_roi_ratio" in scenario
    
    def test_scenario_budget_constraint(self, scenario_modeler):
        """Test scenario respects budget constraints."""
        budget = 100000
        fte_count = 10  # High FTE
        
        scenario = scenario_modeler.calculate_scenario(budget, fte_count, "balanced")
        
        # Actual cost should not exceed budget
        assert scenario["actual_cost"] <= budget
    
    def test_scenario_capacity_constraint(self, scenario_modeler):
        """Test scenario respects capacity constraints."""
        budget = 1000000  # High budget
        fte_count = 1  # Low FTE
        
        scenario = scenario_modeler.calculate_scenario(budget, fte_count, "balanced")
        
        # Interventions should be limited by capacity
        max_capacity = scenario["max_capacity"]
        assert scenario["predicted_interventions"] <= max_capacity
    
    def test_scenario_roi_calculation(self, scenario_modeler):
        """Test ROI ratio calculation accuracy."""
        budget = 250000
        fte_count = 5
        
        scenario = scenario_modeler.calculate_scenario(budget, fte_count, "balanced")
        
        # ROI should be revenue / cost
        if scenario["actual_cost"] > 0:
            expected_roi = scenario["predicted_revenue"] / scenario["actual_cost"]
            assert abs(scenario["predicted_roi_ratio"] - expected_roi) < 0.01


class TestHistoricalCalculations:
    """Test historical tracking calculations."""
    
    def test_status_calculation_on_track(self, historical_tracker):
        """Test status calculation for on-track measure."""
        # Mock status calculation (would need actual data)
        # This tests the logic structure
        status = historical_tracker.calculate_status(
            "HBA1C",
            target_success_rate=85.0,
            lookback_months=3
        )
        
        assert "status" in status
        assert status["status"] in ["on_track", "at_risk", "critical", "unknown"]
        assert "current_rate" in status
        assert "target_rate" in status
        assert status["target_rate"] == 85.0
    
    def test_seasonal_pattern_detection_structure(self, historical_tracker):
        """Test seasonal pattern detection returns correct structure."""
        patterns = historical_tracker.detect_seasonal_patterns(
            measure_id="HBA1C",
            start_date="2024-01-01",
            end_date="2024-12-31"
        )
        
        assert "has_seasonality" in patterns
        assert isinstance(patterns["has_seasonality"], bool)
        assert "peak_month" in patterns
        assert "low_month" in patterns
        assert "seasonal_variance" in patterns


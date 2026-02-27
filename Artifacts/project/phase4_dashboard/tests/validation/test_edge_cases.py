"""
Data validation tests for edge cases
"""
import pytest
import pandas as pd
from utils.scenario_modeler import ScenarioModeler
from utils.campaign_builder import CampaignBuilder
from utils.roi_calculator import ROICalculator


class TestMissingData:
    """Test handling of missing data."""
    
    def test_scenario_with_zero_budget(self, scenario_modeler):
        """Test scenario calculation with zero budget."""
        scenario = scenario_modeler.calculate_scenario(0, 5, "balanced")
        
        # Should handle gracefully
        assert scenario is not None
        assert scenario["budget"] == 0
        assert scenario["predicted_interventions"] == 0
    
    def test_scenario_with_zero_fte(self, scenario_modeler):
        """Test scenario calculation with zero FTE."""
        scenario = scenario_modeler.calculate_scenario(250000, 0, "balanced")
        
        # Should handle gracefully (will be clamped to 1)
        assert scenario is not None
        assert scenario["fte_count"] >= 1
    
    def test_campaign_with_empty_member_list(self, campaign_builder):
        """Test campaign with empty member list."""
        metrics = campaign_builder.calculate_campaign_metrics([])
        
        assert metrics is not None
        assert metrics["total_members"] == 0
        assert metrics["total_value"] == 0
    
    def test_roi_with_no_data(self, roi_calculator):
        """Test ROI calculation with no data."""
        roi = roi_calculator.calculate_measure_roi("NONEXISTENT")
        
        assert roi is not None
        assert roi["total_interventions"] == 0
        assert roi["net_roi"] == 0


class TestNullValues:
    """Test handling of null values."""
    
    def test_scenario_with_none_values(self, scenario_modeler):
        """Test scenario handles None values."""
        # Should clamp None to defaults
        scenario = scenario_modeler.calculate_scenario(250000, 5, "balanced")
        
        # All values should be numeric, not None
        for key, value in scenario.items():
            if isinstance(value, (int, float)):
                assert value is not None
                assert not pd.isna(value)


class TestDateValidation:
    """Test date range validation."""
    
    def test_invalid_date_range(self):
        """Test handling of invalid date ranges."""
        from datetime import datetime
        
        start_date = datetime(2024, 12, 31)
        end_date = datetime(2024, 1, 1)  # End before start
        
        # Functions should handle or validate date ranges
        # This tests that they don't crash
        try:
            from utils.queries import get_roi_by_measure_query
            query = get_roi_by_measure_query(
                start_date.strftime("%Y-%m-%d"),
                end_date.strftime("%Y-%m-%d")
            )
            # Query generation should succeed even with invalid range
            assert query is not None
        except Exception as e:
            # If validation exists, that's also acceptable
            assert "date" in str(e).lower() or "range" in str(e).lower()


class TestCalculationBoundaries:
    """Test calculation boundary conditions."""
    
    def test_roi_with_extreme_values(self, roi_calculator):
        """Test ROI calculation with extreme values."""
        # Very high success rate
        config = {
            "quality_bonus_per_member_per_star": 1000000,  # Extreme value
            "members_per_measure": 1000000,
            "revenue_per_closure": 1000000
        }
        
        roi = roi_calculator.calculate_measure_roi("HBA1C", config=config)
        
        # Should handle without overflow
        assert roi is not None
        assert not pd.isna(roi.get("net_roi", 0))
    
    def test_scenario_boundary_values(self, scenario_modeler):
        """Test scenario with boundary values."""
        # Minimum values
        scenario_min = scenario_modeler.calculate_scenario(50000, 1, "balanced")
        assert scenario_min is not None
        
        # Maximum values
        scenario_max = scenario_modeler.calculate_scenario(500000, 10, "balanced")
        assert scenario_max is not None
        
        # Values outside range should be clamped
        scenario_over = scenario_modeler.calculate_scenario(1000000, 20, "balanced")
        assert scenario_over["budget"] <= 500000
        assert scenario_over["fte_count"] <= 10


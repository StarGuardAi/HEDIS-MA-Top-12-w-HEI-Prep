"""
Unit tests for sensitivity analysis
"""
import pytest
import pandas as pd
from utils.roi_calculator import ROICalculator


class TestSensitivityAnalysis:
    """Test sensitivity analysis functionality."""
    
    def test_sensitivity_analysis_structure(self, roi_calculator):
        """Test sensitivity analysis returns correct structure."""
        # Create base ROI
        base_roi = {
            "measure_id": "HBA1C",
            "total_interventions": 100,
            "successful_closures": 80,
            "success_rate": 80.0,
            "total_revenue": 8000.0,
            "quality_bonus": 200000.0,
            "total_costs": 5000.0,
            "net_roi": 203000.0,
            "roi_ratio": 2.0
        }
        
        scenarios = [
            {"name": "Lower", "success_rate": 75},
            {"name": "Higher", "success_rate": 85}
        ]
        
        sensitivity_df = roi_calculator.sensitivity_analysis(base_roi, scenarios)
        
        assert isinstance(sensitivity_df, pd.DataFrame)
        assert len(sensitivity_df) == 2
        assert "scenario_name" in sensitivity_df.columns
        assert "net_roi" in sensitivity_df.columns
        assert "change_from_base" in sensitivity_df.columns
    
    def test_sensitivity_with_different_rates(self, roi_calculator):
        """Test sensitivity analysis with different success rates."""
        base_roi = {
            "measure_id": "HBA1C",
            "total_interventions": 100,
            "successful_closures": 80,
            "success_rate": 80.0,
            "total_revenue": 8000.0,
            "quality_bonus": 200000.0,
            "total_costs": 5000.0,
            "net_roi": 203000.0,
            "roi_ratio": 2.0
        }
        
        scenarios = [
            {"name": "Low", "success_rate": 70},
            {"name": "Medium", "success_rate": 80},
            {"name": "High", "success_rate": 90}
        ]
        
        sensitivity_df = roi_calculator.sensitivity_analysis(base_roi, scenarios)
        
        # Higher success rate should yield higher ROI
        high_roi = sensitivity_df[sensitivity_df["scenario_name"] == "High"]["net_roi"].iloc[0]
        low_roi = sensitivity_df[sensitivity_df["scenario_name"] == "Low"]["net_roi"].iloc[0]
        
        assert high_roi >= low_roi
    
    def test_sensitivity_with_cost_multiplier(self, roi_calculator):
        """Test sensitivity analysis with cost changes."""
        base_roi = {
            "measure_id": "HBA1C",
            "total_interventions": 100,
            "successful_closures": 80,
            "success_rate": 80.0,
            "total_revenue": 8000.0,
            "quality_bonus": 200000.0,
            "total_costs": 5000.0,
            "net_roi": 203000.0,
            "roi_ratio": 2.0
        }
        
        scenarios = [
            {"name": "Base", "cost_multiplier": 1.0},
            {"name": "Higher Costs", "cost_multiplier": 1.5}
        ]
        
        sensitivity_df = roi_calculator.sensitivity_analysis(base_roi, scenarios)
        
        # Higher costs should yield lower ROI
        base_roi_value = sensitivity_df[sensitivity_df["scenario_name"] == "Base"]["net_roi"].iloc[0]
        high_cost_roi = sensitivity_df[sensitivity_df["scenario_name"] == "Higher Costs"]["net_roi"].iloc[0]
        
        assert base_roi_value >= high_cost_roi


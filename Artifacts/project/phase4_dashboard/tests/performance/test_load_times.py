"""
Performance tests for load times
"""
import pytest
import time
from utils.scenario_modeler import ScenarioModeler
from utils.campaign_builder import CampaignBuilder
from utils.roi_calculator import ROICalculator


class TestLoadTimes:
    """Test load time benchmarks."""
    
    @pytest.mark.performance
    def test_scenario_calculation_speed(self, scenario_modeler):
        """Test scenario calculation completes in reasonable time."""
        start_time = time.time()
        
        scenario = scenario_modeler.calculate_scenario(250000, 5, "balanced")
        
        elapsed = time.time() - start_time
        
        # Should complete in < 1 second
        assert elapsed < 1.0, f"Scenario calculation took {elapsed:.2f}s, target < 1s"
        assert scenario is not None
    
    @pytest.mark.performance
    def test_pareto_frontier_generation_speed(self, scenario_modeler):
        """Test Pareto frontier generation speed."""
        start_time = time.time()
        
        pareto_df = scenario_modeler.generate_pareto_frontier(num_points=50)
        
        elapsed = time.time() - start_time
        
        # Should complete in < 3 seconds
        assert elapsed < 3.0, f"Pareto generation took {elapsed:.2f}s, target < 3s"
        assert pareto_df is not None
    
    @pytest.mark.performance
    def test_campaign_metrics_calculation_speed(self, campaign_builder):
        """Test campaign metrics calculation speed."""
        # Simulate with sample member IDs
        member_ids = [f"MEM{i:04d}" for i in range(100)]
        
        start_time = time.time()
        
        metrics = campaign_builder.calculate_campaign_metrics(member_ids)
        
        elapsed = time.time() - start_time
        
        # Should complete in < 2 seconds
        assert elapsed < 2.0, f"Metrics calculation took {elapsed:.2f}s, target < 2s"
        assert metrics is not None
    
    @pytest.mark.performance
    def test_roi_calculation_speed(self, roi_calculator):
        """Test ROI calculation speed."""
        start_time = time.time()
        
        roi = roi_calculator.calculate_measure_roi("HBA1C")
        
        elapsed = time.time() - start_time
        
        # Should complete in < 2 seconds
        assert elapsed < 2.0, f"ROI calculation took {elapsed:.2f}s, target < 2s"
        assert roi is not None


class TestStressTests:
    """Stress tests with large datasets."""
    
    @pytest.mark.performance
    @pytest.mark.stress
    def test_large_dataset_scenario(self, scenario_modeler):
        """Test scenario calculation with large dataset simulation."""
        # Simulate large dataset by calculating many scenarios
        start_time = time.time()
        
        scenarios = []
        for budget in range(50000, 500001, 50000):
            for fte in range(1, 11):
                scenario = scenario_modeler.calculate_scenario(budget, fte, "balanced")
                scenarios.append(scenario)
        
        elapsed = time.time() - start_time
        
        # Should handle 100 scenarios in reasonable time
        assert len(scenarios) == 100
        assert elapsed < 10.0, f"100 scenarios took {elapsed:.2f}s, target < 10s"
    
    @pytest.mark.performance
    @pytest.mark.stress
    def test_large_member_list_campaign(self, campaign_builder):
        """Test campaign with large member list."""
        # Simulate 10K members
        member_ids = [f"MEM{i:05d}" for i in range(10000)]
        
        start_time = time.time()
        
        metrics = campaign_builder.calculate_campaign_metrics(member_ids)
        
        elapsed = time.time() - start_time
        
        # Should handle 10K members in reasonable time
        assert elapsed < 5.0, f"10K members took {elapsed:.2f}s, target < 5s"
        assert metrics is not None


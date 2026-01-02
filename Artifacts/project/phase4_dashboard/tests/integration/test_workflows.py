"""
Integration tests for end-to-end workflows
"""
import pytest
import pandas as pd
from utils.scenario_modeler import ScenarioModeler
from utils.campaign_builder import CampaignBuilder
from utils.roi_calculator import ROICalculator
from utils.alert_system import AlertSystem


class TestScenarioWorkflow:
    """Test end-to-end scenario modeling workflow."""
    
    def test_scenario_workflow_complete(self, scenario_modeler):
        """Test complete scenario modeling workflow."""
        # Step 1: Calculate scenario
        scenario = scenario_modeler.calculate_scenario(250000, 5, "balanced")
        assert scenario is not None
        
        # Step 2: Generate Pareto frontier
        pareto_df = scenario_modeler.generate_pareto_frontier()
        assert pareto_df is not None
        
        # Step 3: Compare scenarios
        scenarios = [
            {"budget": 150000, "fte_count": 3, "strategy": "balanced"},
            {"budget": 250000, "fte_count": 5, "strategy": "balanced"},
            {"budget": 350000, "fte_count": 7, "strategy": "balanced"}
        ]
        comparison_df = scenario_modeler.compare_scenarios(scenarios)
        assert len(comparison_df) == 3


class TestCampaignWorkflow:
    """Test end-to-end campaign building workflow."""
    
    def test_campaign_workflow_complete(self, campaign_builder):
        """Test complete campaign building workflow."""
        # Step 1: Get available members
        members = campaign_builder.get_available_members()
        assert isinstance(members, pd.DataFrame)
        
        # Skip if no members available (database may not be set up)
        if members.empty:
            pytest.skip("No members available in test database")
        
        if not members.empty:
            # Step 2: Calculate metrics
            member_ids = members['member_id'].head(10).tolist()
            metrics = campaign_builder.calculate_campaign_metrics(member_ids)
            assert metrics is not None
            assert "total_members" in metrics
            
            # Step 3: Create campaign
            campaign = campaign_builder.create_campaign(
                name="Test Campaign",
                member_ids=member_ids,
                coordinator_count=3
            )
            assert campaign is not None
            assert campaign["campaign_id"] is not None
            
            # Step 4: Export CRM CSV
            crm_csv = campaign_builder.export_crm_csv(campaign["campaign_id"])
            assert len(crm_csv) > 0
            assert "Member ID" in crm_csv


class TestROIWorkflow:
    """Test end-to-end ROI calculation workflow."""
    
    def test_roi_workflow_complete(self, roi_calculator):
        """Test complete ROI calculation workflow."""
        # Step 1: Calculate ROI
        roi = roi_calculator.calculate_measure_roi("HBA1C")
        assert roi is not None
        
        # Step 2: Sensitivity analysis
        scenarios = [
            {"name": "Lower", "success_rate": 80},
            {"name": "Higher", "success_rate": 95}
        ]
        sensitivity_df = roi_calculator.sensitivity_analysis(roi, scenarios)
        assert len(sensitivity_df) == 2
        
        # Step 3: Generate CFO report
        report = roi_calculator.generate_cfo_report([roi])
        assert len(report) > 0
        assert "ROI" in report or "roi" in report.lower()


class TestAlertWorkflow:
    """Test end-to-end alert generation workflow."""
    
    def test_alert_workflow_complete(self, alert_system):
        """Test complete alert generation workflow."""
        # Step 1: Generate alerts
        alerts = alert_system.generate_all_alerts()
        assert isinstance(alerts, list)
        
        # Step 2: Get alert stats
        stats = alert_system.get_alert_stats()
        assert "total" in stats
        assert "unread" in stats
        
        # Step 3: Filter alerts
        filtered = alert_system.get_alerts(priority="critical")
        assert isinstance(filtered, list)
        
        # Step 4: Mark as read
        if alerts:
            alert_system.mark_as_read(alerts[0]["alert_id"])
            assert alerts[0]["read"] is True


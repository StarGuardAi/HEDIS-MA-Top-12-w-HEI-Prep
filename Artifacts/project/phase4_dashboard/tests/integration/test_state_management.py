"""
Integration tests for state management
"""
import pytest
from utils.scenario_modeler import ScenarioModeler
from utils.campaign_builder import CampaignBuilder


class TestStateManagement:
    """Test state management across workflows."""
    
    def test_scenario_state_persistence(self, scenario_modeler):
        """Test scenario state is maintained."""
        # Create scenario
        scenario1 = scenario_modeler.calculate_scenario(250000, 5, "balanced")
        
        # Create another scenario
        scenario2 = scenario_modeler.calculate_scenario(350000, 7, "high_roi")
        
        # Both should be independent
        assert scenario1["budget"] == 250000
        assert scenario2["budget"] == 350000
        assert scenario1["fte_count"] == 5
        assert scenario2["fte_count"] == 7
    
    def test_campaign_state_management(self, campaign_builder):
        """Test campaign state management."""
        # Create campaign
        campaign1 = campaign_builder.create_campaign(
            name="Campaign 1",
            member_ids=["MEM001", "MEM002"],
            coordinator_count=2
        )
        
        campaign_id_1 = campaign1["campaign_id"]
        
        # Retrieve campaign
        retrieved = campaign_builder.get_campaign(campaign_id_1)
        assert retrieved is not None
        assert retrieved["name"] == "Campaign 1"
        
        # Create another campaign
        campaign2 = campaign_builder.create_campaign(
            name="Campaign 2",
            member_ids=["MEM003", "MEM004"],
            coordinator_count=3
        )
        
        # Both should exist
        all_campaigns = campaign_builder.get_all_campaigns()
        assert len(all_campaigns) >= 2


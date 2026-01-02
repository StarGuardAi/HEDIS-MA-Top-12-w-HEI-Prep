"""
Unit tests for filter logic
"""
import pytest
import pandas as pd
from utils.campaign_builder import CampaignBuilder
from utils.alert_system import AlertSystem


class TestCampaignFilters:
    """Test campaign builder filter logic."""
    
    def test_get_available_members_filter_by_measure(self, campaign_builder):
        """Test filtering members by measure."""
        # This would need actual database connection
        # Testing the filter logic structure
        members = campaign_builder.get_available_members(
            measure_id="HBA1C",
            status_filter=["pending", "scheduled"]
        )
        
        assert isinstance(members, pd.DataFrame)
    
    def test_get_available_members_filter_by_status(self, campaign_builder):
        """Test filtering members by status."""
        members = campaign_builder.get_available_members(
            status_filter=["pending"]
        )
        
        assert isinstance(members, pd.DataFrame)
    
    def test_get_available_members_date_range(self, campaign_builder):
        """Test filtering members by date range."""
        start_date = "2024-01-01"
        end_date = "2024-12-31"
        
        members = campaign_builder.get_available_members(
            start_date=start_date,
            end_date=end_date
        )
        
        assert isinstance(members, pd.DataFrame)


class TestAlertFilters:
    """Test alert system filter logic."""
    
    def test_get_alerts_filter_by_type(self, alert_system):
        """Test filtering alerts by type."""
        alerts = alert_system.get_alerts(alert_type="star_rating_risk")
        
        assert isinstance(alerts, list)
        # All alerts should be of specified type
        for alert in alerts:
            assert alert.get("type") == "star_rating_risk"
    
    def test_get_alerts_filter_by_priority(self, alert_system):
        """Test filtering alerts by priority."""
        alerts = alert_system.get_alerts(priority="critical")
        
        assert isinstance(alerts, list)
        # All alerts should be of specified priority
        for alert in alerts:
            assert alert.get("priority") == "critical"
    
    def test_get_alerts_unread_only(self, alert_system):
        """Test filtering unread alerts."""
        # Add some test alerts
        alert_system.alert_history = [
            {"alert_id": "1", "read": False, "type": "test"},
            {"alert_id": "2", "read": True, "type": "test"},
            {"alert_id": "3", "read": False, "type": "test"}
        ]
        
        unread = alert_system.get_alerts(unread_only=True)
        
        assert len(unread) == 2
        for alert in unread:
            assert alert.get("read") is False


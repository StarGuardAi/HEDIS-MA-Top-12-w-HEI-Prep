"""
Unit tests for alert generation
"""
import pytest
from utils.alert_system import AlertSystem, AlertType, AlertPriority


class TestAlertGeneration:
    """Test alert generation logic."""
    
    def test_star_rating_risk_detection(self, alert_system):
        """Test star rating risk alert generation."""
        # Configure for low threshold to trigger alert
        alert_system.update_config({
            "star_rating_threshold": 90.0,
            "enabled_alert_types": [AlertType.STAR_RATING_RISK]
        })
        
        alerts = alert_system.check_star_rating_risks()
        
        assert isinstance(alerts, list)
        # Alerts should have correct structure
        for alert in alerts:
            assert alert["type"] == AlertType.STAR_RATING_RISK.value
            assert "priority" in alert
            assert "title" in alert
            assert "message" in alert
    
    def test_opportunity_alert_generation(self, alert_system):
        """Test opportunity alert generation."""
        alert_system.update_config({
            "opportunity_value_threshold": 1000.0,
            "enabled_alert_types": [AlertType.OPPORTUNITY]
        })
        
        alerts = alert_system.check_opportunities()
        
        assert isinstance(alerts, list)
        for alert in alerts:
            assert alert["type"] == AlertType.OPPORTUNITY.value
            assert "potential_revenue" in alert
    
    def test_deadline_alert_generation(self, alert_system):
        """Test deadline alert generation."""
        alert_system.update_config({
            "deadline_days_ahead": 30,
            "enabled_alert_types": [AlertType.DEADLINE]
        })
        
        alerts = alert_system.check_deadlines()
        
        assert isinstance(alerts, list)
        for alert in alerts:
            assert alert["type"] == AlertType.DEADLINE.value
            assert "interventions_due" in alert
            assert "days_until" in alert
    
    def test_performance_anomaly_detection(self, alert_system):
        """Test performance anomaly detection."""
        alert_system.update_config({
            "anomaly_threshold": 0.10,
            "enabled_alert_types": [AlertType.PERFORMANCE_ANOMALY]
        })
        
        alerts = alert_system.check_performance_anomalies()
        
        assert isinstance(alerts, list)
        for alert in alerts:
            assert alert["type"] == AlertType.PERFORMANCE_ANOMALY.value
            assert "change_pct" in alert
    
    def test_alert_priority_assignment(self, alert_system):
        """Test alert priority assignment."""
        alerts = alert_system.generate_all_alerts()
        
        for alert in alerts:
            assert alert["priority"] in ["critical", "high", "medium", "low"]
            assert "priority" in alert
    
    def test_alert_filtering(self, alert_system):
        """Test alert filtering functionality."""
        # Generate alerts
        alerts = alert_system.generate_all_alerts()
        
        # Filter by type
        star_alerts = alert_system.get_alerts(alert_type="star_rating_risk")
        assert all(a["type"] == "star_rating_risk" for a in star_alerts)
        
        # Filter by priority
        critical_alerts = alert_system.get_alerts(priority="critical")
        assert all(a["priority"] == "critical" for a in critical_alerts)
        
        # Filter unread
        unread_alerts = alert_system.get_alerts(unread_only=True)
        assert all(not a.get("read", False) for a in unread_alerts)


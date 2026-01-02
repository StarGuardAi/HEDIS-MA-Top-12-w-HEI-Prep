"""
Gap Workflow Alerts and Reminders
Alert system for gap closure workflow
"""
from typing import Dict, List
from datetime import datetime, timedelta
from utils.gap_workflow import GapWorkflowManager, GapStatus, Urgency


class GapWorkflowAlerts:
    """Alert and reminder system for gap closure workflow."""
    
    def __init__(self, workflow_manager: GapWorkflowManager):
        self.workflow_manager = workflow_manager
    
    def get_upcoming_deadlines(self, days_ahead: int = 30) -> List[Dict]:
        """Get gaps with upcoming deadlines."""
        alerts = []
        cutoff_date = datetime.now() + timedelta(days=days_ahead)
        
        for gap in self.workflow_manager.gaps.values():
            if gap.deadline_date <= cutoff_date and gap.status not in [GapStatus.CLOSED, GapStatus.EXCLUDED]:
                days_until = (gap.deadline_date - datetime.now()).days
                
                alerts.append({
                    "gap_id": gap.gap_id,
                    "member_id": gap.member_id,
                    "measure_id": gap.measure_id,
                    "deadline_date": gap.deadline_date,
                    "days_until": days_until,
                    "urgency": gap.urgency.value,
                    "priority": gap.priority.value,
                    "status": gap.status.value,
                    "alert_type": "upcoming_deadline",
                    "message": f"Gap {gap.gap_id} deadline in {days_until} days"
                })
        
        return sorted(alerts, key=lambda x: x["days_until"])
    
    def get_missed_appointments(self) -> List[Dict]:
        """Get gaps with missed appointments."""
        alerts = []
        
        for gap in self.workflow_manager.gaps.values():
            if gap.gap_reason == "Missed Appointment" and gap.status != GapStatus.CLOSED:
                alerts.append({
                    "gap_id": gap.gap_id,
                    "member_id": gap.member_id,
                    "measure_id": gap.measure_id,
                    "missed_date": gap.metadata.get("appointment_date"),
                    "alert_type": "missed_appointment",
                    "message": f"Member {gap.member_id} missed appointment for {gap.measure_id}",
                    "priority": gap.priority.value
                })
        
        return alerts
    
    def get_lab_results_pending(self, days_threshold: int = 14) -> List[Dict]:
        """Get gaps with lab results pending."""
        alerts = []
        threshold_date = datetime.now() - timedelta(days=days_threshold)
        
        for gap in self.workflow_manager.gaps.values():
            if gap.gap_reason == "Lab Pending":
                # Check if lab was ordered
                lab_order_date = gap.metadata.get("lab_order_date")
                if lab_order_date and lab_order_date <= threshold_date:
                    days_pending = (datetime.now() - lab_order_date).days
                    
                    alerts.append({
                        "gap_id": gap.gap_id,
                        "member_id": gap.member_id,
                        "measure_id": gap.measure_id,
                        "lab_order_date": lab_order_date,
                        "days_pending": days_pending,
                        "alert_type": "lab_pending",
                        "message": f"Lab results pending for {days_pending} days",
                        "priority": gap.priority.value
                    })
        
        return sorted(alerts, key=lambda x: x["days_pending"], reverse=True)
    
    def get_lost_to_followup(self, days_threshold: int = 30) -> List[Dict]:
        """Get members lost to follow-up."""
        alerts = []
        threshold_date = datetime.now() - timedelta(days=days_threshold)
        
        for gap in self.workflow_manager.gaps.values():
            if gap.status == GapStatus.INTERVENTION_IN_PROGRESS:
                # Check last contact
                if gap.gap_id in self.workflow_manager.interventions:
                    interventions = self.workflow_manager.interventions[gap.gap_id]
                    if interventions:
                        last_contact = max(i.contact_date for i in interventions)
                        if last_contact <= threshold_date:
                            days_since = (datetime.now() - last_contact).days
                            
                            alerts.append({
                                "gap_id": gap.gap_id,
                                "member_id": gap.member_id,
                                "measure_id": gap.measure_id,
                                "last_contact": last_contact,
                                "days_since": days_since,
                                "alert_type": "lost_to_followup",
                                "message": f"No contact for {days_since} days",
                                "priority": gap.priority.value
                            })
        
        return sorted(alerts, key=lambda x: x["days_since"], reverse=True)
    
    def get_escalation_alerts(self) -> List[Dict]:
        """Get gaps requiring escalation."""
        alerts = []
        
        for gap in self.workflow_manager.gaps.values():
            if gap.gap_id in self.workflow_manager.interventions:
                interventions = self.workflow_manager.interventions[gap.gap_id]
                
                for intervention in interventions:
                    if intervention.escalation_triggered:
                        alerts.append({
                            "gap_id": gap.gap_id,
                            "member_id": gap.member_id,
                            "measure_id": gap.measure_id,
                            "intervention_id": intervention.intervention_id,
                            "escalation_reason": intervention.escalation_reason,
                            "alert_type": "escalation",
                            "message": f"Escalation required: {intervention.escalation_reason}",
                            "priority": "High"
                        })
        
        return alerts
    
    def get_all_alerts(self) -> Dict[str, List[Dict]]:
        """Get all alerts grouped by type."""
        return {
            "upcoming_deadlines": self.get_upcoming_deadlines(),
            "missed_appointments": self.get_missed_appointments(),
            "lab_pending": self.get_lab_results_pending(),
            "lost_to_followup": self.get_lost_to_followup(),
            "escalations": self.get_escalation_alerts()
        }
    
    def get_alert_summary(self) -> Dict:
        """Get summary of all alerts."""
        all_alerts = self.get_all_alerts()
        
        total_alerts = sum(len(alerts) for alerts in all_alerts.values())
        
        high_priority = sum(
            1 for alerts in all_alerts.values()
            for alert in alerts
            if alert.get("priority") in ["P1", "High", "Critical"]
        )
        
        return {
            "total_alerts": total_alerts,
            "high_priority": high_priority,
            "by_type": {alert_type: len(alerts) for alert_type, alerts in all_alerts.items()}
        }


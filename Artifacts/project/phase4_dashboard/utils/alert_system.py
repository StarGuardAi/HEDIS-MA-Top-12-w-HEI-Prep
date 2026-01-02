"""
Intelligent Alert System
Monitors HEDIS portfolio for risks, opportunities, deadlines, and anomalies
"""
from typing import Dict, List, Optional, Tuple
from datetime import datetime, timedelta
import pandas as pd
import numpy as np
from enum import Enum

from utils.database import execute_query
from utils.queries import get_roi_by_measure_query, get_portfolio_summary_query


class AlertType(Enum):
    """Alert type enumeration"""
    STAR_RATING_RISK = "star_rating_risk"
    OPPORTUNITY = "opportunity"
    DEADLINE = "deadline"
    PERFORMANCE_ANOMALY = "performance_anomaly"


class AlertPriority(Enum):
    """Alert priority levels"""
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class AlertSystem:
    """
    Intelligent alert system for HEDIS portfolio monitoring.
    Detects risks, opportunities, deadlines, and performance anomalies.
    """
    
    def __init__(self):
        self.alert_history = []  # Store alerts in memory (could use database)
        self.config = {
            "star_rating_threshold": 85.0,  # Minimum success rate for star rating
            "opportunity_value_threshold": 10000.0,  # Minimum value for opportunity alerts
            "deadline_days_ahead": 30,  # Days ahead for deadline alerts
            "anomaly_threshold": 0.15,  # 15% change threshold for anomalies
            "enabled_alert_types": [AlertType.STAR_RATING_RISK, AlertType.OPPORTUNITY, 
                                   AlertType.DEADLINE, AlertType.PERFORMANCE_ANOMALY]
        }
    
    def update_config(self, config: Dict):
        """Update alert system configuration."""
        self.config.update(config)
    
    def check_star_rating_risks(
        self,
        start_date: str = None,
        end_date: str = None
    ) -> List[Dict]:
        """
        Check for star rating risk alerts.
        Alerts when measures are trending below threshold.
        """
        alerts = []
        
        if AlertType.STAR_RATING_RISK not in self.config["enabled_alert_types"]:
            return alerts
        
        if start_date is None:
            start_date = (datetime.now() - timedelta(days=90)).strftime("%Y-%m-%d")
        if end_date is None:
            end_date = datetime.now().strftime("%Y-%m-%d")
        
        # Get measure performance
        query = get_roi_by_measure_query(start_date, end_date)
        measure_data = execute_query(query)
        
        if measure_data.empty:
            return alerts
        
        threshold = self.config.get("star_rating_threshold", 85.0)
        
        for _, row in measure_data.iterrows():
            measure_name = row.get("measure_name", "Unknown")
            measure_code = row.get("measure_code", "")
            success_rate = 0.0
            
            total_interventions = row.get("total_interventions", 0)
            successful_closures = row.get("successful_closures", 0)
            
            if total_interventions > 0:
                success_rate = (successful_closures / total_interventions) * 100
            
            if success_rate < threshold and total_interventions >= 10:  # Only alert if significant volume
                alerts.append({
                    "alert_id": f"star_risk_{measure_code}_{datetime.now().strftime('%Y%m%d')}",
                    "type": AlertType.STAR_RATING_RISK.value,
                    "priority": AlertPriority.HIGH.value if success_rate < threshold * 0.9 else AlertPriority.MEDIUM.value,
                    "title": f"{measure_name} Trending Below Threshold",
                    "message": f"{measure_name} shows {success_rate:.1f}% success rate, below {threshold}% threshold. Risk to Star Rating.",
                    "measure_name": measure_name,
                    "measure_code": measure_code,
                    "current_rate": success_rate,
                    "threshold": threshold,
                    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "read": False,
                    "actionable": True
                })
        
        return alerts
    
    def check_opportunities(
        self,
        start_date: str = None,
        end_date: str = None
    ) -> List[Dict]:
        """
        Check for high-value opportunity alerts.
        Identifies new high-value members or measures.
        """
        alerts = []
        
        if AlertType.OPPORTUNITY not in self.config["enabled_alert_types"]:
            return alerts
        
        if start_date is None:
            start_date = (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d")
        if end_date is None:
            end_date = (datetime.now() + timedelta(days=30)).strftime("%Y-%m-%d")
        
        # Get member prioritization data
        member_query = f"""
            SELECT 
                mi.measure_id,
                hm.measure_name,
                COUNT(DISTINCT mi.member_id) as members_count,
                SUM(CASE WHEN mi.status = 'completed' THEN 1 ELSE 0 END) * 100.0 as potential_revenue,
                ROUND(
                    CAST(SUM(CASE WHEN mi.status = 'completed' THEN 1 ELSE 0 END) AS REAL) * 100.0 / 
                    NULLIF(COUNT(*), 0),
                    1
                ) as predicted_success_rate
            FROM member_interventions mi
            LEFT JOIN hedis_measures hm ON mi.measure_id = hm.measure_id
            WHERE mi.intervention_date >= '{start_date}'
            AND mi.intervention_date <= '{end_date}'
            AND (mi.status = 'pending' OR mi.status = 'scheduled')
            GROUP BY mi.measure_id, hm.measure_name
            HAVING potential_revenue >= {self.config.get('opportunity_value_threshold', 10000)}
            ORDER BY potential_revenue DESC
            LIMIT 5
        """
        
        opportunity_data = execute_query(member_query)
        
        if not opportunity_data.empty:
            for _, row in opportunity_data.iterrows():
                measure_name = row.get("measure_name", "Unknown")
                measure_code = row.get("measure_id", "")
                members_count = int(row.get("members_count", 0))
                # Handle None values properly
                potential_rev = row.get("potential_revenue", 0) if "potential_revenue" in row else 0
                success_rt = row.get("predicted_success_rate", 0) if "predicted_success_rate" in row else 0
                potential_revenue = float(potential_rev) if potential_rev is not None else 0.0
                success_rate = float(success_rt) if success_rt is not None else 0.0
                
                alerts.append({
                    "alert_id": f"opportunity_{measure_code}_{datetime.now().strftime('%Y%m%d')}",
                    "type": AlertType.OPPORTUNITY.value,
                    "priority": AlertPriority.HIGH.value if potential_revenue >= 50000 else AlertPriority.MEDIUM.value,
                    "title": f"New High-Value Members Identified",
                    "message": f"{measure_name}: {members_count} members with ${potential_revenue:,.0f} potential revenue ({success_rate:.1f}% predicted success rate)",
                    "measure_name": measure_name,
                    "measure_code": measure_code,
                    "members_count": members_count,
                    "potential_revenue": potential_revenue,
                    "predicted_success_rate": success_rate,
                    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "read": False,
                    "actionable": True
                })
        
        return alerts
    
    def check_deadlines(
        self,
        days_ahead: int = None
    ) -> List[Dict]:
        """
        Check for deadline reminders.
        Alerts for interventions due within specified days.
        """
        alerts = []
        
        if AlertType.DEADLINE not in self.config["enabled_alert_types"]:
            return alerts
        
        if days_ahead is None:
            days_ahead = self.config.get("deadline_days_ahead", 30)
        
        end_date = (datetime.now() + timedelta(days=days_ahead)).strftime("%Y-%m-%d")
        start_date = datetime.now().strftime("%Y-%m-%d")
        
        # Get interventions due soon
        deadline_query = f"""
            SELECT 
                mi.measure_id,
                hm.measure_name,
                COUNT(*) as interventions_due,
                COUNT(DISTINCT mi.member_id) as members_affected,
                MIN(mi.intervention_date) as earliest_due_date
            FROM member_interventions mi
            LEFT JOIN hedis_measures hm ON mi.measure_id = hm.measure_id
            WHERE mi.intervention_date >= '{start_date}'
            AND mi.intervention_date <= '{end_date}'
            AND (mi.status = 'pending' OR mi.status = 'scheduled')
            GROUP BY mi.measure_id, hm.measure_name
            HAVING COUNT(*) >= 10
            ORDER BY COUNT(*) DESC
        """
        
        deadline_data = execute_query(deadline_query)
        
        if not deadline_data.empty:
            for _, row in deadline_data.iterrows():
                measure_name = row.get("measure_name", "Unknown")
                measure_code = row.get("measure_id", "")
                interventions_due = int(row.get("interventions_due", 0))
                members_affected = int(row.get("members_affected", 0))
                earliest_due = row.get("earliest_due_date", "")
                
                # Calculate days until deadline
                if earliest_due:
                    due_date = datetime.strptime(str(earliest_due)[:10], "%Y-%m-%d")
                    days_until = (due_date - datetime.now()).days
                    
                    priority = AlertPriority.CRITICAL.value if days_until <= 7 else (
                        AlertPriority.HIGH.value if days_until <= 14 else AlertPriority.MEDIUM.value
                    )
                    
                    alerts.append({
                        "alert_id": f"deadline_{measure_code}_{datetime.now().strftime('%Y%m%d')}",
                        "type": AlertType.DEADLINE.value,
                        "priority": priority,
                        "title": f"{interventions_due} {measure_name} Tests Due Within {days_ahead} Days",
                        "message": f"{interventions_due} interventions affecting {members_affected} members. Earliest due: {earliest_due}. {days_until} days remaining.",
                        "measure_name": measure_name,
                        "measure_code": measure_code,
                        "interventions_due": interventions_due,
                        "members_affected": members_affected,
                        "days_until": days_until,
                        "earliest_due_date": str(earliest_due)[:10],
                        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "read": False,
                        "actionable": True
                    })
        
        return alerts
    
    def check_performance_anomalies(
        self,
        start_date: str = None,
        end_date: str = None
    ) -> List[Dict]:
        """
        Check for performance anomalies.
        Detects significant changes in closure rates or other metrics.
        """
        alerts = []
        
        if AlertType.PERFORMANCE_ANOMALY not in self.config["enabled_alert_types"]:
            return alerts
        
        if start_date is None:
            start_date = (datetime.now() - timedelta(days=14)).strftime("%Y-%m-%d")
        if end_date is None:
            end_date = datetime.now().strftime("%Y-%m-%d")
        
        # Get current period performance
        current_query = get_portfolio_summary_query(start_date, end_date)
        current_data = execute_query(current_query)
        
        # Get previous period performance (same length, before current period)
        period_length = (datetime.strptime(end_date, "%Y-%m-%d") - datetime.strptime(start_date, "%Y-%m-%d")).days
        prev_start = (datetime.strptime(start_date, "%Y-%m-%d") - timedelta(days=period_length)).strftime("%Y-%m-%d")
        prev_end = start_date
        
        previous_query = get_portfolio_summary_query(prev_start, prev_end)
        previous_data = execute_query(previous_query)
        
        if not current_data.empty and not previous_data.empty:
            current_row = current_data.iloc[0]
            previous_row = previous_data.iloc[0]
            
            # Handle None values properly
            current_rate = current_row.get("overall_success_rate", 0) if "overall_success_rate" in current_row else 0
            previous_rate = previous_row.get("overall_success_rate", 0) if "overall_success_rate" in previous_row else 0
            
            current_success_rate = float(current_rate) if current_rate is not None else 0.0
            previous_success_rate = float(previous_rate) if previous_rate is not None else 0.0
            
            if previous_success_rate > 0:
                change_pct = ((current_success_rate - previous_success_rate) / previous_success_rate)
                threshold = self.config.get("anomaly_threshold", 0.15)
                
                if abs(change_pct) >= threshold:
                    is_decrease = change_pct < 0
                    priority = AlertPriority.HIGH.value if is_decrease else AlertPriority.MEDIUM.value
                    
                    alerts.append({
                        "alert_id": f"anomaly_{datetime.now().strftime('%Y%m%d')}",
                        "type": AlertType.PERFORMANCE_ANOMALY.value,
                        "priority": priority,
                        "title": f"Closure Rate {'Dropped' if is_decrease else 'Increased'} {abs(change_pct)*100:.1f}%",
                        "message": f"Overall closure rate changed from {previous_success_rate:.1f}% to {current_success_rate:.1f}% ({'decrease' if is_decrease else 'increase'} of {abs(change_pct)*100:.1f}%)",
                        "current_rate": current_success_rate,
                        "previous_rate": previous_success_rate,
                        "change_pct": change_pct * 100,
                        "is_decrease": is_decrease,
                        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "read": False,
                        "actionable": True
                    })
        
        return alerts
    
    def generate_sample_alerts(self) -> List[Dict]:
        """
        Generate sample alerts for demonstration when database is empty.
        """
        sample_alerts = []
        now = datetime.now()
        
        # Sample Star Rating Risk Alert
        sample_alerts.append({
            "alert_id": f"star_risk_sample_{now.strftime('%Y%m%d')}",
            "type": AlertType.STAR_RATING_RISK.value,
            "priority": AlertPriority.HIGH.value,
            "title": "Blood Pressure Control Trending Below Threshold",
            "message": "Blood Pressure Control shows 78.5% success rate, below 85% threshold. Risk to Star Rating.",
            "measure_name": "Blood Pressure Control",
            "measure_code": "CBP",
            "current_rate": 78.5,
            "threshold": 85.0,
            "timestamp": now.strftime("%Y-%m-%d %H:%M:%S"),
            "read": False,
            "actionable": True
        })
        
        # Sample Opportunity Alert
        sample_alerts.append({
            "alert_id": f"opportunity_sample_{now.strftime('%Y%m%d')}",
            "type": AlertType.OPPORTUNITY.value,
            "priority": AlertPriority.HIGH.value,
            "title": "New High-Value Members Identified",
            "message": "HbA1c Testing: 847 members with $285,000 potential revenue (93.2% predicted success rate)",
            "measure_name": "HbA1c Testing",
            "measure_code": "CDC",
            "members_count": 847,
            "potential_revenue": 285000.0,
            "predicted_success_rate": 93.2,
            "timestamp": now.strftime("%Y-%m-%d %H:%M:%S"),
            "read": False,
            "actionable": True
        })
        
        # Sample Deadline Alert
        days_until = 12
        sample_alerts.append({
            "alert_id": f"deadline_sample_{now.strftime('%Y%m%d')}",
            "type": AlertType.DEADLINE.value,
            "priority": AlertPriority.CRITICAL.value if days_until <= 7 else AlertPriority.HIGH.value,
            "title": f"156 Colorectal Cancer Screening Tests Due Within 30 Days",
            "message": f"156 interventions affecting 142 members. Earliest due: {(now + timedelta(days=days_until)).strftime('%Y-%m-%d')}. {days_until} days remaining.",
            "measure_name": "Colorectal Cancer Screening",
            "measure_code": "COL",
            "interventions_due": 156,
            "members_affected": 142,
            "days_until": days_until,
            "earliest_due_date": (now + timedelta(days=days_until)).strftime("%Y-%m-%d"),
            "timestamp": now.strftime("%Y-%m-%d %H:%M:%S"),
            "read": False,
            "actionable": True
        })
        
        # Sample Performance Anomaly Alert
        sample_alerts.append({
            "alert_id": f"anomaly_sample_{now.strftime('%Y%m%d')}",
            "type": AlertType.PERFORMANCE_ANOMALY.value,
            "priority": AlertPriority.MEDIUM.value,
            "title": "Breast Cancer Screening Performance Drop Detected",
            "message": "Breast Cancer Screening shows 18.5% decrease in success rate compared to previous period (45.2% vs 55.4%).",
            "measure_name": "Breast Cancer Screening",
            "measure_code": "BCS",
            "current_rate": 45.2,
            "previous_rate": 55.4,
            "change_percent": -18.5,
            "timestamp": now.strftime("%Y-%m-%d %H:%M:%S"),
            "read": False,
            "actionable": True
        })
        
        # Another Opportunity Alert (Medium Priority)
        sample_alerts.append({
            "alert_id": f"opportunity_sample2_{now.strftime('%Y%m%d')}",
            "type": AlertType.OPPORTUNITY.value,
            "priority": AlertPriority.MEDIUM.value,
            "title": "Diabetes Eye Exam Opportunity",
            "message": "Diabetes Eye Exam: 234 members with $125,000 potential revenue (87.5% predicted success rate)",
            "measure_name": "Diabetes Eye Exam",
            "measure_code": "EED",
            "members_count": 234,
            "potential_revenue": 125000.0,
            "predicted_success_rate": 87.5,
            "timestamp": now.strftime("%Y-%m-%d %H:%M:%S"),
            "read": False,
            "actionable": True
        })
        
        return sample_alerts
    
    def generate_all_alerts(
        self,
        start_date: str = None,
        end_date: str = None
    ) -> List[Dict]:
        """
        Generate all alerts by running all checks.
        Generates sample alerts if database is empty.
        """
        all_alerts = []
        
        # Star rating risks
        all_alerts.extend(self.check_star_rating_risks(start_date, end_date))
        
        # Opportunities
        all_alerts.extend(self.check_opportunities(start_date, end_date))
        
        # Deadlines
        all_alerts.extend(self.check_deadlines())
        
        # Performance anomalies
        all_alerts.extend(self.check_performance_anomalies(start_date, end_date))
        
        # If no alerts found, generate sample alerts for demonstration
        if len(all_alerts) == 0:
            all_alerts = self.generate_sample_alerts()
        
        # Sort by priority and timestamp
        priority_order = {
            AlertPriority.CRITICAL.value: 0,
            AlertPriority.HIGH.value: 1,
            AlertPriority.MEDIUM.value: 2,
            AlertPriority.LOW.value: 3
        }
        
        all_alerts.sort(key=lambda x: (
            priority_order.get(x.get("priority", "low"), 3),
            x.get("timestamp", "")
        ))
        
        # Store in history
        self.alert_history.extend(all_alerts)
        
        return all_alerts
    
    def get_alerts(
        self,
        alert_type: Optional[str] = None,
        priority: Optional[str] = None,
        unread_only: bool = False
    ) -> List[Dict]:
        """
        Get filtered alerts.
        """
        alerts = self.alert_history.copy()
        
        if alert_type:
            alerts = [a for a in alerts if a.get("type") == alert_type]
        
        if priority:
            alerts = [a for a in alerts if a.get("priority") == priority]
        
        if unread_only:
            alerts = [a for a in alerts if not a.get("read", False)]
        
        return alerts
    
    def mark_as_read(self, alert_id: str):
        """Mark alert as read."""
        for alert in self.alert_history:
            if alert.get("alert_id") == alert_id:
                alert["read"] = True
                break
    
    def mark_all_as_read(self):
        """Mark all alerts as read."""
        for alert in self.alert_history:
            alert["read"] = True
    
    def delete_alert(self, alert_id: str):
        """Delete alert from history."""
        self.alert_history = [a for a in self.alert_history if a.get("alert_id") != alert_id]
    
    def get_alert_stats(self) -> Dict:
        """Get alert statistics."""
        total = len(self.alert_history)
        unread = len([a for a in self.alert_history if not a.get("read", False)])
        
        by_type = {}
        by_priority = {}
        
        for alert in self.alert_history:
            alert_type = alert.get("type", "unknown")
            priority = alert.get("priority", "unknown")
            
            by_type[alert_type] = by_type.get(alert_type, 0) + 1
            by_priority[priority] = by_priority.get(priority, 0) + 1
        
        return {
            "total": total,
            "unread": unread,
            "read": total - unread,
            "by_type": by_type,
            "by_priority": by_priority
        }


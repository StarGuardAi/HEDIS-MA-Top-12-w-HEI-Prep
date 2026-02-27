"""
Gap Workflow Reporting and Analytics
Performance dashboards and metrics for gap closure workflow
"""
from typing import Dict, List
from datetime import datetime, timedelta
import pandas as pd
from utils.gap_workflow import GapWorkflowManager, GapStatus, Priority


class GapWorkflowReporting:
    """Reporting and analytics for gap closure workflow."""
    
    def __init__(self, workflow_manager: GapWorkflowManager):
        self.workflow_manager = workflow_manager
    
    def get_coordinator_performance(self, coordinator_id: str, start_date: datetime, end_date: datetime) -> Dict:
        """Get coordinator performance metrics."""
        # Filter gaps by coordinator and date
        coordinator_gaps = [
            gap for gap in self.workflow_manager.gaps.values()
            if gap.assigned_coordinator == coordinator_id
            and start_date <= gap.identified_date <= end_date
        ]
        
        if not coordinator_gaps:
            return {
                "coordinator_id": coordinator_id,
                "total_gaps": 0,
                "closed": 0,
                "closure_rate": 0.0,
                "average_time_to_close": 0.0,
                "cost_per_closure": 0.0
            }
        
        closed_gaps = [g for g in coordinator_gaps if g.status == GapStatus.CLOSED]
        
        # Calculate time to close
        times_to_close = []
        for gap in closed_gaps:
            if gap.gap_id in self.workflow_manager.verifications:
                verification = self.workflow_manager.verifications[gap.gap_id]
                time_to_close = (verification.closure_date - gap.identified_date).days
                times_to_close.append(time_to_close)
        
        avg_time_to_close = sum(times_to_close) / len(times_to_close) if times_to_close else 0.0
        
        # Estimate cost per closure (simplified)
        cost_per_closure = avg_time_to_close * 50.0  # $50 per day estimate
        
        return {
            "coordinator_id": coordinator_id,
            "total_gaps": len(coordinator_gaps),
            "closed": len(closed_gaps),
            "closure_rate": len(closed_gaps) / len(coordinator_gaps) if coordinator_gaps else 0.0,
            "average_time_to_close": avg_time_to_close,
            "cost_per_closure": cost_per_closure,
            "in_progress": len([g for g in coordinator_gaps if g.status == GapStatus.INTERVENTION_IN_PROGRESS]),
            "pending": len([g for g in coordinator_gaps if g.status == GapStatus.PENDING_VERIFICATION])
        }
    
    def get_closure_rates_by_measure(self, start_date: datetime, end_date: datetime) -> pd.DataFrame:
        """Get closure rates by measure."""
        gaps_in_period = [
            gap for gap in self.workflow_manager.gaps.values()
            if start_date <= gap.identified_date <= end_date
        ]
        
        measure_stats = {}
        for gap in gaps_in_period:
            measure_id = gap.measure_id
            if measure_id not in measure_stats:
                measure_stats[measure_id] = {
                    "total": 0,
                    "closed": 0,
                    "excluded": 0,
                    "in_progress": 0
                }
            
            measure_stats[measure_id]["total"] += 1
            
            if gap.status == GapStatus.CLOSED:
                measure_stats[measure_id]["closed"] += 1
            elif gap.status == GapStatus.EXCLUDED:
                measure_stats[measure_id]["excluded"] += 1
            elif gap.status == GapStatus.INTERVENTION_IN_PROGRESS:
                measure_stats[measure_id]["in_progress"] += 1
        
        # Convert to DataFrame
        data = []
        for measure_id, stats in measure_stats.items():
            closure_rate = stats["closed"] / stats["total"] if stats["total"] > 0 else 0.0
            data.append({
                "Measure": measure_id,
                "Total Gaps": stats["total"],
                "Closed": stats["closed"],
                "Excluded": stats["excluded"],
                "In Progress": stats["in_progress"],
                "Closure Rate": f"{closure_rate*100:.1f}%"
            })
        
        return pd.DataFrame(data)
    
    def get_closure_rates_by_coordinator(self, start_date: datetime, end_date: datetime) -> pd.DataFrame:
        """Get closure rates by coordinator."""
        coordinators = set(
            gap.assigned_coordinator
            for gap in self.workflow_manager.gaps.values()
            if gap.assigned_coordinator
        )
        
        data = []
        for coordinator_id in coordinators:
            performance = self.get_coordinator_performance(coordinator_id, start_date, end_date)
            data.append({
                "Coordinator": coordinator_id,
                "Total Gaps": performance["total_gaps"],
                "Closed": performance["closed"],
                "Closure Rate": f"{performance['closure_rate']*100:.1f}%",
                "Avg Time to Close": f"{performance['average_time_to_close']:.1f} days",
                "Cost per Closure": f"${performance['cost_per_closure']:.2f}"
            })
        
        return pd.DataFrame(data)
    
    def get_time_to_close_metrics(self, start_date: datetime, end_date: datetime) -> Dict:
        """Get time-to-close metrics."""
        closed_gaps = [
            gap for gap in self.workflow_manager.gaps.values()
            if gap.status == GapStatus.CLOSED
            and start_date <= gap.identified_date <= end_date
        ]
        
        if not closed_gaps:
            return {
                "average": 0.0,
                "median": 0.0,
                "p25": 0.0,
                "p75": 0.0,
                "min": 0.0,
                "max": 0.0
            }
        
        times_to_close = []
        for gap in closed_gaps:
            if gap.gap_id in self.workflow_manager.verifications:
                verification = self.workflow_manager.verifications[gap.gap_id]
                time_to_close = (verification.closure_date - gap.identified_date).days
                times_to_close.append(time_to_close)
        
        if not times_to_close:
            return {"average": 0.0, "median": 0.0, "p25": 0.0, "p75": 0.0, "min": 0.0, "max": 0.0}
        
        times_to_close.sort()
        
        return {
            "average": sum(times_to_close) / len(times_to_close),
            "median": times_to_close[len(times_to_close) // 2],
            "p25": times_to_close[len(times_to_close) // 4],
            "p75": times_to_close[3 * len(times_to_close) // 4],
            "min": min(times_to_close),
            "max": max(times_to_close)
        }
    
    def get_roi_by_intervention_type(self, start_date: datetime, end_date: datetime) -> pd.DataFrame:
        """Get ROI by intervention type."""
        # Get all interventions in period
        interventions = []
        for gap_id, gap_interventions in self.workflow_manager.interventions.items():
            gap = self.workflow_manager.gaps.get(gap_id)
            if not gap or not (start_date <= gap.identified_date <= end_date):
                continue
            
            for intervention in gap_interventions:
                if start_date <= intervention.contact_date <= end_date:
                    interventions.append({
                        "intervention": intervention,
                        "gap": gap
                    })
        
        # Group by intervention type (contact method)
        intervention_stats = {}
        for item in interventions:
            method = item["intervention"].contact_method
            gap = item["gap"]
            
            if method not in intervention_stats:
                intervention_stats[method] = {
                    "count": 0,
                    "closed": 0,
                    "total_cost": 0.0
                }
            
            intervention_stats[method]["count"] += 1
            intervention_stats[method]["total_cost"] += 25.0  # $25 per intervention estimate
            
            if gap.status == GapStatus.CLOSED:
                intervention_stats[method]["closed"] += 1
        
        # Calculate ROI
        data = []
        for method, stats in intervention_stats.items():
            closure_rate = stats["closed"] / stats["count"] if stats["count"] > 0 else 0.0
            avg_cost = stats["total_cost"] / stats["count"] if stats["count"] > 0 else 0.0
            cost_per_closure = stats["total_cost"] / stats["closed"] if stats["closed"] > 0 else 0.0
            
            # Estimate revenue per closure (simplified)
            revenue_per_closure = 100.0
            total_revenue = stats["closed"] * revenue_per_closure
            roi = (total_revenue - stats["total_cost"]) / stats["total_cost"] if stats["total_cost"] > 0 else 0.0
            
            data.append({
                "Intervention Type": method,
                "Count": stats["count"],
                "Closed": stats["closed"],
                "Closure Rate": f"{closure_rate*100:.1f}%",
                "Avg Cost": f"${avg_cost:.2f}",
                "Cost per Closure": f"${cost_per_closure:.2f}",
                "Total Revenue": f"${total_revenue:.2f}",
                "ROI": f"{roi*100:.1f}%"
            })
        
        return pd.DataFrame(data)
    
    def get_geographic_performance(self, start_date: datetime, end_date: datetime) -> pd.DataFrame:
        """Get closure rates by geography."""
        gaps_in_period = [
            gap for gap in self.workflow_manager.gaps.values()
            if start_date <= gap.identified_date <= end_date
        ]
        
        geo_stats = {}
        for gap in gaps_in_period:
            geography = gap.metadata.get("geography", "Unknown")
            
            if geography not in geo_stats:
                geo_stats[geography] = {
                    "total": 0,
                    "closed": 0
                }
            
            geo_stats[geography]["total"] += 1
            if gap.status == GapStatus.CLOSED:
                geo_stats[geography]["closed"] += 1
        
        data = []
        for geography, stats in geo_stats.items():
            closure_rate = stats["closed"] / stats["total"] if stats["total"] > 0 else 0.0
            data.append({
                "Geography": geography,
                "Total Gaps": stats["total"],
                "Closed": stats["closed"],
                "Closure Rate": f"{closure_rate*100:.1f}%"
            })
        
        return pd.DataFrame(data)


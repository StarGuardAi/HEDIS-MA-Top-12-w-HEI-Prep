"""
What-If Scenario Modeler
Calculates predicted ROI and outcomes based on budget and FTE inputs
"""
from typing import Dict, List, Optional, Tuple
import pandas as pd
import numpy as np

from utils.database import execute_query
from utils.queries import get_roi_by_measure_query, get_cost_per_closure_by_activity_query


class ScenarioModeler:
    """
    Models HEDIS portfolio scenarios based on budget and FTE allocations.
    Uses historical data to predict outcomes.
    """
    
    def __init__(self, start_date: str = "2024-10-01", end_date: str = "2024-12-31"):
        self.start_date = start_date
        self.end_date = end_date
        self.baseline_metrics = self._load_baseline_metrics()
        self.activity_metrics = self._load_activity_metrics()
        
    def _load_baseline_metrics(self) -> pd.DataFrame:
        """Load baseline ROI metrics by measure."""
        query = get_roi_by_measure_query(self.start_date, self.end_date)
        return execute_query(query)
    
    def _load_activity_metrics(self) -> pd.DataFrame:
        """Load activity-level cost and success metrics."""
        query = get_cost_per_closure_by_activity_query(self.start_date, self.end_date, min_uses=5)
        return execute_query(query)
    
    def calculate_scenario(
        self,
        budget: float,
        fte_count: int,
        strategy: str = "balanced"
    ) -> Dict:
        """
        Calculate scenario outcomes based on budget and FTE inputs.
        
        Args:
            budget: Total budget allocation ($50K to $500K)
            fte_count: Number of care coordinators (1-10)
            strategy: Allocation strategy - "balanced", "high_roi", "high_volume"
        
        Returns:
            Dictionary with predicted outcomes
        """
        # Validate inputs
        budget = max(50000, min(500000, budget))
        fte_count = max(1, min(10, fte_count))
        
        # Calculate capacity based on FTE
        # Assumption: Each FTE can handle ~200 interventions per quarter
        # (based on industry standards: ~3-4 interventions per day per FTE)
        interventions_per_fte_per_quarter = 200
        max_capacity = fte_count * interventions_per_fte_per_quarter
        
        # Calculate average cost per intervention from baseline
        if not self.baseline_metrics.empty:
            avg_cost = self.baseline_metrics['total_investment'].sum() / max(
                self.baseline_metrics['total_interventions'].sum(), 1
            )
            avg_success_rate = (
                self.baseline_metrics['successful_closures'].sum() / 
                max(self.baseline_metrics['total_interventions'].sum(), 1)
            ) * 100
            avg_roi = self.baseline_metrics['roi_ratio'].mean()
        else:
            # Default values if no data
            avg_cost = 50.0
            avg_success_rate = 75.0
            avg_roi = 2.0
        
        # Budget-constrained interventions
        budget_constrained_interventions = int(budget / avg_cost)
        
        # Capacity-constrained interventions
        capacity_constrained_interventions = max_capacity
        
        # Actual interventions (minimum of budget and capacity)
        actual_interventions = min(budget_constrained_interventions, capacity_constrained_interventions)
        
        # Apply strategy multiplier
        strategy_multipliers = {
            "balanced": 1.0,
            "high_roi": 1.15,  # Focus on high-ROI measures increases success rate
            "high_volume": 0.95  # Volume focus slightly reduces success rate
        }
        adjusted_success_rate = avg_success_rate * strategy_multipliers.get(strategy, 1.0)
        adjusted_success_rate = min(95.0, max(50.0, adjusted_success_rate))  # Cap between 50-95%
        
        # Calculate predicted closures
        predicted_closures = int(actual_interventions * (adjusted_success_rate / 100))
        
        # Revenue calculation: $100 per closure (standard HEDIS revenue)
        revenue_per_closure = 100.0
        predicted_revenue = predicted_closures * revenue_per_closure
        
        # Actual cost (may be less than budget if capacity constrained)
        actual_cost = min(budget, actual_interventions * avg_cost)
        
        # Calculate ROI
        predicted_roi_ratio = (predicted_revenue / actual_cost) if actual_cost > 0 else 0
        predicted_net_benefit = predicted_revenue - actual_cost
        
        # Calculate utilization
        budget_utilization = (actual_cost / budget * 100) if budget > 0 else 0
        capacity_utilization = (actual_interventions / max_capacity * 100) if max_capacity > 0 else 0
        
        # Determine constraint
        if budget_constrained_interventions < capacity_constrained_interventions:
            constraint = "budget"
        else:
            constraint = "capacity"
        
        return {
            "budget": budget,
            "fte_count": fte_count,
            "strategy": strategy,
            "max_capacity": max_capacity,
            "predicted_interventions": actual_interventions,
            "predicted_closures": predicted_closures,
            "predicted_revenue": predicted_revenue,
            "actual_cost": actual_cost,
            "predicted_roi_ratio": predicted_roi_ratio,
            "predicted_net_benefit": predicted_net_benefit,
            "predicted_success_rate": adjusted_success_rate,
            "budget_utilization": budget_utilization,
            "capacity_utilization": capacity_utilization,
            "constraint": constraint,
            "avg_cost_per_intervention": avg_cost,
            "revenue_per_closure": revenue_per_closure
        }
    
    def generate_pareto_frontier(
        self,
        budget_range: Tuple[float, float] = (50000, 500000),
        fte_range: Tuple[int, int] = (1, 10),
        num_points: int = 50
    ) -> pd.DataFrame:
        """
        Generate Pareto frontier points for visualization.
        Shows trade-offs between ROI and volume.
        
        Returns:
            DataFrame with Pareto frontier points
        """
        points = []
        
        # Generate points across budget and FTE ranges
        budget_step = (budget_range[1] - budget_range[0]) / (num_points // 2)
        fte_step = (fte_range[1] - fte_range[0]) / (num_points // 2)
        
        for i in range(num_points):
            if i < num_points // 2:
                # Vary budget, keep FTE constant
                budget = budget_range[0] + (i * budget_step)
                fte = (fte_range[0] + fte_range[1]) / 2
            else:
                # Vary FTE, keep budget constant
                budget = (budget_range[0] + budget_range[1]) / 2
                fte = int(fte_range[0] + ((i - num_points // 2) * fte_step))
            
            scenario = self.calculate_scenario(budget, fte, "balanced")
            points.append({
                "budget": budget,
                "fte_count": fte,
                "predicted_roi_ratio": scenario["predicted_roi_ratio"],
                "predicted_closures": scenario["predicted_closures"],
                "predicted_revenue": scenario["predicted_revenue"],
                "predicted_net_benefit": scenario["predicted_net_benefit"]
            })
        
        df = pd.DataFrame(points)
        
        # Filter to Pareto-optimal points (non-dominated solutions)
        pareto_points = []
        for _, point in df.iterrows():
            is_pareto = True
            for _, other in df.iterrows():
                if (other["predicted_roi_ratio"] >= point["predicted_roi_ratio"] and
                    other["predicted_closures"] >= point["predicted_closures"] and
                    (other["predicted_roi_ratio"] > point["predicted_roi_ratio"] or
                     other["predicted_closures"] > point["predicted_closures"])):
                    is_pareto = False
                    break
            if is_pareto:
                pareto_points.append(point.to_dict())
        
        return pd.DataFrame(pareto_points).sort_values("predicted_roi_ratio", ascending=False)
    
    def compare_scenarios(self, scenarios: List[Dict]) -> pd.DataFrame:
        """
        Compare multiple scenarios side-by-side.
        
        Args:
            scenarios: List of scenario dictionaries with budget, fte_count, strategy
        
        Returns:
            DataFrame with comparison metrics
        """
        results = []
        for i, scenario_input in enumerate(scenarios, 1):
            scenario = self.calculate_scenario(
                scenario_input["budget"],
                scenario_input["fte_count"],
                scenario_input.get("strategy", "balanced")
            )
            scenario["scenario_name"] = scenario_input.get("name", f"Scenario {i}")
            results.append(scenario)
        
        return pd.DataFrame(results)
    
    def get_optimal_scenario(
        self,
        budget_constraint: Optional[float] = None,
        fte_constraint: Optional[int] = None,
        objective: str = "max_roi"
    ) -> Dict:
        """
        Find optimal scenario given constraints.
        
        Args:
            budget_constraint: Maximum budget
            fte_constraint: Maximum FTE count
            objective: "max_roi", "max_closures", "max_net_benefit"
        
        Returns:
            Optimal scenario dictionary
        """
        best_scenario = None
        best_value = -float('inf')
        
        budget_range = (50000, budget_constraint or 500000)
        fte_range = (1, fte_constraint or 10)
        
        # Grid search for optimal
        for budget in range(int(budget_range[0]), int(budget_range[1]), 25000):
            for fte in range(fte_range[0], fte_range[1] + 1):
                scenario = self.calculate_scenario(budget, fte, "balanced")
                
                if objective == "max_roi":
                    value = scenario["predicted_roi_ratio"]
                elif objective == "max_closures":
                    value = scenario["predicted_closures"]
                elif objective == "max_net_benefit":
                    value = scenario["predicted_net_benefit"]
                else:
                    value = scenario["predicted_roi_ratio"]
                
                if value > best_value:
                    best_value = value
                    best_scenario = scenario
        
        return best_scenario or self.calculate_scenario(250000, 5, "balanced")


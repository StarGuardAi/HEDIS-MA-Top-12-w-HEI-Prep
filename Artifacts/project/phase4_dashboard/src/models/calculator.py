"""
Business calculation logic (ROI, Star Rating impact, etc.)
"""
import pandas as pd
from typing import Dict, Any


class ROICalculator:
    """Calculate financial ROI for gap closure interventions"""
    
    def __init__(self, star_rating_bonus: float = 5000):
        """
        Args:
            star_rating_bonus: Bonus per member per star rating point
        """
        self.star_rating_bonus = star_rating_bonus
    
    def calculate_intervention_roi(
        self, 
        members_df: pd.DataFrame,
        intervention_cost_per_member: float = 50
    ) -> Dict[str, Any]:
        """
        Calculate ROI for gap closure interventions
        
        Args:
            members_df: DataFrame with member-level predictions
            intervention_cost_per_member: Cost to intervene per member
        
        Returns:
            Dict with ROI metrics
        """
        total_members = len(members_df)
        predicted_closures = (members_df['predicted_closure_probability'] * 
                             members_df['financial_value']).sum()
        total_cost = total_members * intervention_cost_per_member
        net_value = predicted_closures - total_cost
        roi_percentage = (net_value / total_cost) * 100
        
        return {
            'total_members': total_members,
            'predicted_value': predicted_closures,
            'intervention_cost': total_cost,
            'net_value': net_value,
            'roi_percentage': roi_percentage
        }


class StarRatingCalculator:
    """Calculate Star Rating impacts"""
    
    @staticmethod
    def calculate_measure_impact(
        current_rate: float,
        predicted_rate: float,
        measure_weight: float
    ) -> float:
        """
        Calculate impact on overall Star Rating
        
        Args:
            current_rate: Current compliance rate (0-100)
            predicted_rate: Predicted rate after interventions (0-100)
            measure_weight: CMS weight for this measure
        
        Returns:
            Impact on overall rating (0-1 scale)
        """
        rate_improvement = (predicted_rate - current_rate) / 100
        impact = rate_improvement * measure_weight / 5.0  # Normalize to 5-star scale
        return impact


# Add more calculator classes as needed


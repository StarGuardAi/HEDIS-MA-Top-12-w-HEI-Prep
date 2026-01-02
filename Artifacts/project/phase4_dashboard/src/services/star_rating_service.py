"""
Star Rating Service

Business logic for Medicare Advantage Star Rating calculations.
"""
from typing import Dict, Any, List, Optional
import pandas as pd

from domain.value_objects import StarRating
from src.models.calculator import StarRatingCalculator
from src.services.measure_service import MeasureService
from config.settings import HEDIS_MEASURES


class StarRatingService:
    """Service for Star Rating-related business logic"""
    
    def __init__(self):
        self.calculator = StarRatingCalculator()
        self.measure_service = MeasureService()
    
    def calculate_overall_rating(
        self,
        measure_rates: Optional[Dict[str, float]] = None,
        base_rating: float = 4.0
    ) -> StarRating:
        """
        Calculate overall star rating
        
        Args:
            measure_rates: Dictionary of measure_name -> rate
            base_rating: Base star rating
        
        Returns:
            StarRating value object
        """
        if measure_rates is None:
            # Get from data
            measures_df = self.measure_service.get_all_measures()
            measure_rates = {}
            
            if not measures_df.empty and 'current_rate' in measures_df.columns:
                for _, row in measures_df.iterrows():
                    measure_name = row.get('measure_name', '')
                    current_rate = row.get('current_rate', 0)
                    measure_rates[measure_name] = current_rate
        
        # Calculate impacts
        measure_impacts = {}
        for measure_name, current_rate in measure_rates.items():
            # Get measure weight
            measure_key = measure_name.replace(' ', '_')
            measure_weight = HEDIS_MEASURES.get(measure_key, {}).get('star_weight', 1.0)
            
            # Assume 5% improvement
            predicted_rate = current_rate + 5
            
            impact = self.calculator.calculate_measure_impact(
                current_rate=current_rate,
                predicted_rate=predicted_rate,
                measure_weight=measure_weight
            )
            measure_impacts[measure_name] = impact
        
        # Calculate overall rating
        overall_rating = self.calculator.calculate_overall_rating(
            measure_impacts,
            base_rating
        )
        
        # Create domain scores (simplified)
        return StarRating(
            overall_rating=overall_rating,
            process_domain=4.0,
            outcome_domain=4.0,
            patient_experience_domain=4.0,
            access_domain=4.0
        )
    
    def calculate_measure_impact(
        self,
        measure_name: str,
        current_rate: float,
        predicted_rate: float
    ) -> float:
        """
        Calculate impact of a measure on star rating
        
        Args:
            measure_name: Name of the measure
            current_rate: Current compliance rate
            predicted_rate: Predicted rate after intervention
        
        Returns:
            Impact value (0-1 scale)
        """
        measure_key = measure_name.replace(' ', '_')
        measure_weight = HEDIS_MEASURES.get(measure_key, {}).get('star_weight', 1.0)
        
        return self.calculator.calculate_measure_impact(
            current_rate=current_rate,
            predicted_rate=predicted_rate,
            measure_weight=measure_weight
        )
    
    def get_rating_summary(self) -> Dict[str, Any]:
        """
        Get star rating summary
        
        Returns:
            Dictionary with rating summary
        """
        rating = self.calculate_overall_rating()
        
        return {
            'overall_rating': rating.overall_rating,
            'rounded_rating': rating.rounded_rating(),
            'distance_to_next_tier': rating.distance_to_next_tier(),
            'is_above_threshold': rating.is_above_threshold(4.0)
        }


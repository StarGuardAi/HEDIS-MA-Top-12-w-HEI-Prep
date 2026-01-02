"""
Measure Service

Business logic for HEDIS measure operations.
"""
from typing import List, Dict, Any, Optional
import pandas as pd

from domain.entities import Measure
from domain.value_objects import MeasureRate
from src.data.loaders import load_measures_data
from config.settings import HEDIS_MEASURES
from infrastructure.cache import cached


class MeasureService:
    """Service for measure-related business logic"""
    
    @cached(prefix="measures", ttl=3600)
    def get_all_measures(self) -> pd.DataFrame:
        """
        Get all HEDIS measures data
        
        Returns:
            DataFrame with measure performance data
        """
        return load_measures_data()
    
    def get_measure_definitions(self) -> Dict[str, Dict[str, Any]]:
        """
        Get HEDIS measure definitions
        
        Returns:
            Dictionary of measure definitions
        """
        return HEDIS_MEASURES
    
    def get_measure_by_name(self, measure_name: str) -> Optional[Dict[str, Any]]:
        """
        Get a specific measure definition
        
        Args:
            measure_name: Name of the measure
        
        Returns:
            Measure definition dictionary or None
        """
        # Convert measure name to key format
        measure_key = measure_name.replace(' ', '_')
        return HEDIS_MEASURES.get(measure_key)
    
    def calculate_measure_rate(
        self,
        numerator: int,
        denominator: int
    ) -> MeasureRate:
        """
        Calculate measure rate
        
        Args:
            numerator: Numerator count
            denominator: Denominator count
        
        Returns:
            MeasureRate value object
        """
        return MeasureRate.calculate(numerator, denominator)
    
    def get_measures_by_category(self, category: str) -> List[str]:
        """
        Get measures by category
        
        Args:
            category: Measure category (e.g., 'Diabetes', 'Cardiovascular')
        
        Returns:
            List of measure names
        """
        return [
            measure_info['name']
            for measure_info in HEDIS_MEASURES.values()
            if measure_info.get('category') == category
        ]
    
    def get_measures_summary(self) -> Dict[str, Any]:
        """
        Get summary statistics for all measures
        
        Returns:
            Dictionary with summary statistics
        """
        df = load_measures_data()
        
        if df.empty:
            return {
                'total_measures': len(HEDIS_MEASURES),
                'measures_with_data': 0,
                'avg_rate': 0.0,
                'measures_above_benchmark': 0
            }
        
        return {
            'total_measures': len(HEDIS_MEASURES),
            'measures_with_data': len(df),
            'avg_rate': df['current_rate'].mean() if 'current_rate' in df.columns else 0.0,
            'measures_above_benchmark': len(df[
                (df['current_rate'] > df['benchmark_rate']) if 'benchmark_rate' in df.columns else False
            ]) if 'benchmark_rate' in df.columns else 0
        }


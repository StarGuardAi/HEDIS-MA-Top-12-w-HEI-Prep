"""
ROI Service

Business logic for ROI calculations and financial analysis.
"""
from typing import Dict, Any, List, Optional
import pandas as pd
from decimal import Decimal

from domain.value_objects import ROI
from src.models.calculator import ROICalculator
from src.services.member_service import MemberService


class ROIService:
    """Service for ROI-related business logic"""
    
    def __init__(self):
        self.calculator = ROICalculator()
        self.member_service = MemberService()
    
    def calculate_portfolio_roi(
        self,
        intervention_cost_per_member: float = 50.0,
        date_range: Optional[tuple] = None,
        measures: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Calculate ROI for entire portfolio
        
        Args:
            intervention_cost_per_member: Cost per member intervention
            date_range: Optional date range filter
            measures: Optional measure filter
        
        Returns:
            Dictionary with ROI metrics
        """
        members_df = self.member_service.get_all_members(
            date_range=date_range,
            measures=measures
        )
        
        return self.calculator.calculate_intervention_roi(
            members_df,
            intervention_cost_per_member
        )
    
    def calculate_measure_roi(
        self,
        measure_name: str,
        intervention_cost_per_member: float = 50.0
    ) -> Dict[str, Any]:
        """
        Calculate ROI for a specific measure
        
        Args:
            measure_name: Name of the measure
            intervention_cost_per_member: Cost per member
        
        Returns:
            Dictionary with ROI metrics
        """
        members_df = self.member_service.get_all_members(measures=[measure_name])
        return self.calculator.calculate_intervention_roi(
            members_df,
            intervention_cost_per_member
        )
    
    def calculate_roi_from_values(
        self,
        investment: Decimal,
        return_value: Decimal
    ) -> ROI:
        """
        Calculate ROI from investment and return values
        
        Args:
            investment: Total investment amount
            return_value: Total return value
        
        Returns:
            ROI value object
        """
        return ROI.calculate(investment, return_value)
    
    def get_roi_summary(self) -> Dict[str, Any]:
        """
        Get portfolio ROI summary
        
        Returns:
            Dictionary with ROI summary
        """
        roi_result = self.calculate_portfolio_roi()
        
        return {
            'roi_percentage': roi_result['roi_percentage'],
            'net_value': roi_result['net_value'],
            'total_members': roi_result['total_members'],
            'predicted_value': roi_result['predicted_value'],
            'intervention_cost': roi_result['intervention_cost']
        }


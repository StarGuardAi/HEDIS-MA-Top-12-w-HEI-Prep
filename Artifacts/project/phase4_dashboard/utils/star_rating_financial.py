"""
Star Rating Financial Impact Calculator
Calculates quality bonus, member impact, and brand value
"""
from typing import Dict, Optional
from utils.roi_calculator import ROICalculator


class StarRatingFinancial:
    """Calculate financial impact of Star Rating changes."""
    
    def __init__(self):
        self.roi_calculator = ROICalculator()
        
        # Quality bonus rates (simplified - actual rates vary)
        self.quality_bonus_rates = {
            5.0: 0.05,  # 5% bonus for 5 stars
            4.5: 0.04,  # 4% bonus for 4.5 stars
            4.0: 0.03,  # 3% bonus for 4 stars
            3.5: 0.02,  # 2% bonus for 3.5 stars
            3.0: 0.01,  # 1% bonus for 3 stars
            2.5: 0.0,
            2.0: 0.0,
            1.5: 0.0,
            1.0: 0.0
        }
        
        # Member growth/retention impact (simplified)
        self.member_impact_rates = {
            5.0: 0.10,  # 10% growth for 5 stars
            4.5: 0.08,  # 8% growth for 4.5 stars
            4.0: 0.05,  # 5% growth for 4 stars
            3.5: 0.02,  # 2% growth for 3.5 stars
            3.0: 0.0,
            2.5: -0.02,  # -2% loss for 2.5 stars
            2.0: -0.05,  # -5% loss for 2 stars
            1.5: -0.10,  # -10% loss for 1.5 stars
            1.0: -0.15  # -15% loss for 1 star
        }
    
    def calculate_quality_bonus(
        self,
        star_rating: float,
        total_revenue: float = 100000000  # Default $100M
    ) -> Dict:
        """
        Calculate quality bonus payment.
        
        Args:
            star_rating: Overall Star Rating
            total_revenue: Total plan revenue
        
        Returns:
            Dictionary with bonus calculations
        """
        # Get bonus rate
        bonus_rate = self.quality_bonus_rates.get(star_rating, 0.0)
        
        # Calculate bonus amount
        bonus_amount = total_revenue * bonus_rate
        
        # Calculate per member per month (PMPM)
        # Assuming 10,000 members
        members = 10000
        pmpm = bonus_amount / (members * 12)
        
        return {
            "star_rating": star_rating,
            "bonus_rate": bonus_rate,
            "bonus_amount": bonus_amount,
            "pmpm": pmpm,
            "annual_per_member": bonus_amount / members
        }
    
    def calculate_member_impact(
        self,
        star_rating: float,
        current_members: int = 10000
    ) -> Dict:
        """
        Calculate member growth/retention impact.
        
        Args:
            star_rating: Overall Star Rating
            current_members: Current member count
        
        Returns:
            Dictionary with member impact calculations
        """
        # Get impact rate
        impact_rate = self.member_impact_rates.get(star_rating, 0.0)
        
        # Calculate member change
        member_change = current_members * impact_rate
        
        # Calculate revenue impact (assuming $10,000 per member per year)
        revenue_per_member = 10000
        revenue_impact = member_change * revenue_per_member
        
        return {
            "star_rating": star_rating,
            "impact_rate": impact_rate,
            "member_change": member_change,
            "projected_members": current_members + member_change,
            "revenue_impact": revenue_impact
        }
    
    def calculate_rating_change_impact(
        self,
        current_rating: float,
        projected_rating: float,
        total_revenue: float = 100000000,
        current_members: int = 10000
    ) -> Dict:
        """
        Calculate financial impact of rating change.
        
        Args:
            current_rating: Current Star Rating
            projected_rating: Projected Star Rating
            total_revenue: Total plan revenue
            current_members: Current member count
        
        Returns:
            Dictionary with comprehensive impact analysis
        """
        # Current state
        current_bonus = self.calculate_quality_bonus(current_rating, total_revenue)
        current_members_impact = self.calculate_member_impact(current_rating, current_members)
        
        # Projected state
        projected_bonus = self.calculate_quality_bonus(projected_rating, total_revenue)
        projected_members_impact = self.calculate_member_impact(projected_rating, current_members)
        
        # Calculate changes
        bonus_change = projected_bonus["bonus_amount"] - current_bonus["bonus_amount"]
        member_change = projected_members_impact["member_change"] - current_members_impact["member_change"]
        revenue_change = projected_members_impact["revenue_impact"] - current_members_impact["revenue_impact"]
        
        # Total impact
        total_impact = bonus_change + revenue_change
        
        return {
            "current_rating": current_rating,
            "projected_rating": projected_rating,
            "rating_change": projected_rating - current_rating,
            "bonus_change": bonus_change,
            "member_change": member_change,
            "revenue_change": revenue_change,
            "total_impact": total_impact,
            "current_bonus": current_bonus,
            "projected_bonus": projected_bonus,
            "current_members": current_members_impact,
            "projected_members": projected_members_impact
        }
    
    def estimate_brand_value_impact(
        self,
        star_rating: float
    ) -> Dict:
        """
        Estimate brand reputation value impact.
        
        Args:
            star_rating: Overall Star Rating
        
        Returns:
            Dictionary with brand value estimates
        """
        # Simplified brand value calculation
        brand_value_multipliers = {
            5.0: 1.5,  # 50% premium for 5 stars
            4.5: 1.3,  # 30% premium for 4.5 stars
            4.0: 1.1,  # 10% premium for 4 stars
            3.5: 1.0,  # No premium
            3.0: 0.9,  # -10% discount
            2.5: 0.8,  # -20% discount
            2.0: 0.7,  # -30% discount
            1.5: 0.6,  # -40% discount
            1.0: 0.5   # -50% discount
        }
        
        multiplier = brand_value_multipliers.get(star_rating, 1.0)
        
        # Base brand value (simplified)
        base_brand_value = 5000000  # $5M base
        
        brand_value = base_brand_value * multiplier
        
        return {
            "star_rating": star_rating,
            "multiplier": multiplier,
            "brand_value": brand_value,
            "premium_discount": (multiplier - 1.0) * 100
        }


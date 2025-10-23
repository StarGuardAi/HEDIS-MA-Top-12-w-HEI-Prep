"""
Star Rating Calculator for HEDIS Portfolio Optimizer

This module calculates Medicare Advantage Star Ratings based on HEDIS measure
performance, including triple-weighted measures and Health Equity Index (HEI)
bonus/penalty factors.

CMS Star Rating Methodology: 2025
"""

from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class MeasurePerformance:
    """Performance data for a single HEDIS measure."""
    measure_code: str
    measure_name: str
    tier: int
    weight: float  # 1.0 or 3.0
    
    # Performance metrics
    numerator: int
    denominator: int
    rate: float  # numerator / denominator
    
    # Star rating
    star_rating: float  # 1.0 to 5.0
    points: float  # Based on star rating and weight
    
    # Financial impact
    revenue_estimate: float


@dataclass
class PortfolioPerformance:
    """Overall portfolio performance across all measures."""
    total_points: float
    weighted_average_stars: float
    tier1_stars: float
    tier2_stars: float
    tier3_stars: float
    tier4_hei_factor: float  # -5% to +5%
    
    # Financial impact
    base_star_revenue: float
    hei_adjusted_revenue: float
    total_revenue: float
    
    # Measure details
    measure_performances: List[MeasurePerformance]


class StarRatingCalculator:
    """
    Calculate Medicare Advantage Star Ratings for HEDIS measure portfolio.
    
    Features:
    - Triple-weighted measures (GSD, KED, CBP)
    - Health Equity Index (HEI) bonus/penalty
    - Tier-level analysis
    - Revenue estimation
    """
    
    def __init__(self, 
                 revenue_per_star_point: float = 50000,
                 revenue_per_full_star: float = 500000):
        """
        Initialize Star Rating Calculator.
        
        Args:
            revenue_per_star_point: Revenue per 0.1 Star point ($50K default)
            revenue_per_full_star: Revenue per full Star ($500K default)
        """
        self.revenue_per_star_point = revenue_per_star_point
        self.revenue_per_full_star = revenue_per_full_star
        
        # CMS Star rating thresholds (2025)
        self.star_thresholds = {
            5.0: 90,  # 5 stars = 90th percentile
            4.5: 85,  # 4.5 stars = 85th percentile
            4.0: 75,  # 4 stars = 75th percentile
            3.5: 65,  # 3.5 stars = 65th percentile
            3.0: 50,  # 3 stars = 50th percentile
            2.5: 40,  # 2.5 stars = 40th percentile
            2.0: 25,  # 2 stars = 25th percentile
            1.5: 15,  # 1.5 stars = 15th percentile
            1.0: 0,   # 1 star = 0th percentile
        }
        
        # Triple-weighted measures
        self.triple_weighted = ["GSD", "KED", "CBP"]
        
        logger.info("Initialized Star Rating Calculator")
    
    def calculate_star_rating_from_percentile(self, percentile: float) -> float:
        """
        Calculate star rating from percentile rank.
        
        Args:
            percentile: Percentile rank (0-100)
            
        Returns:
            Star rating (1.0-5.0)
        """
        if percentile >= 90:
            return 5.0
        elif percentile >= 85:
            return 4.5
        elif percentile >= 75:
            return 4.0
        elif percentile >= 65:
            return 3.5
        elif percentile >= 50:
            return 3.0
        elif percentile >= 40:
            return 2.5
        elif percentile >= 25:
            return 2.0
        elif percentile >= 15:
            return 1.5
        else:
            return 1.0
    
    def calculate_star_rating_from_rate(self, rate: float, 
                                       benchmarks: Dict[float, float]) -> float:
        """
        Calculate star rating from measure rate using benchmarks.
        
        Args:
            rate: Measure rate (0.0-1.0)
            benchmarks: Mapping of star ratings to benchmark rates
            
        Returns:
            Star rating (1.0-5.0)
        """
        # Sort benchmarks from highest to lowest
        sorted_benchmarks = sorted(benchmarks.items(), reverse=True)
        
        for star_level, benchmark_rate in sorted_benchmarks:
            if rate >= benchmark_rate:
                return star_level
        
        return 1.0  # Default to 1 star
    
    def calculate_measure_points(self, 
                                measure_code: str,
                                star_rating: float,
                                weight: float = 1.0) -> float:
        """
        Calculate points for a single measure.
        
        Args:
            measure_code: Measure code (e.g., "GSD", "KED")
            star_rating: Star rating (1.0-5.0)
            weight: Measure weight (1.0 or 3.0)
            
        Returns:
            Points earned for this measure
        """
        return star_rating * weight
    
    def calculate_measure_performance(self,
                                     measure_code: str,
                                     measure_name: str,
                                     tier: int,
                                     numerator: int,
                                     denominator: int,
                                     benchmarks: Optional[Dict[float, float]] = None,
                                     percentile: Optional[float] = None) -> MeasurePerformance:
        """
        Calculate performance for a single measure.
        
        Args:
            measure_code: Measure code
            measure_name: Measure name
            tier: Tier (1-4)
            numerator: Numerator (compliant members)
            denominator: Denominator (eligible members)
            benchmarks: Optional benchmark rates
            percentile: Optional percentile rank
            
        Returns:
            MeasurePerformance object
        """
        # Calculate rate
        rate = numerator / denominator if denominator > 0 else 0.0
        
        # Determine weight
        weight = 3.0 if measure_code in self.triple_weighted else 1.0
        
        # Calculate star rating
        if percentile is not None:
            star_rating = self.calculate_star_rating_from_percentile(percentile)
        elif benchmarks is not None:
            star_rating = self.calculate_star_rating_from_rate(rate, benchmarks)
        else:
            # Default: convert rate to percentile estimate
            percentile_estimate = rate * 100
            star_rating = self.calculate_star_rating_from_percentile(percentile_estimate)
        
        # Calculate points
        points = self.calculate_measure_points(measure_code, star_rating, weight)
        
        # Estimate revenue
        revenue_estimate = points * self.revenue_per_star_point
        
        return MeasurePerformance(
            measure_code=measure_code,
            measure_name=measure_name,
            tier=tier,
            weight=weight,
            numerator=numerator,
            denominator=denominator,
            rate=rate,
            star_rating=star_rating,
            points=points,
            revenue_estimate=revenue_estimate
        )
    
    def calculate_portfolio_performance(self,
                                       measure_performances: List[MeasurePerformance],
                                       hei_factor: float = 0.0) -> PortfolioPerformance:
        """
        Calculate overall portfolio performance.
        
        Args:
            measure_performances: List of measure performances
            hei_factor: Health Equity Index factor (-5.0 to +5.0)
            
        Returns:
            PortfolioPerformance object
        """
        if not measure_performances:
            raise ValueError("No measure performances provided")
        
        # Calculate total points
        total_points = sum(mp.points for mp in measure_performances)
        total_weight = sum(mp.weight for mp in measure_performances)
        
        # Calculate weighted average stars
        weighted_average_stars = total_points / total_weight if total_weight > 0 else 0.0
        
        # Calculate tier-level averages
        tier1_measures = [mp for mp in measure_performances if mp.tier == 1]
        tier2_measures = [mp for mp in measure_performances if mp.tier == 2]
        tier3_measures = [mp for mp in measure_performances if mp.tier == 3]
        
        tier1_stars = self._calculate_tier_average(tier1_measures)
        tier2_stars = self._calculate_tier_average(tier2_measures)
        tier3_stars = self._calculate_tier_average(tier3_measures)
        
        # Calculate financial impact
        base_star_revenue = sum(mp.revenue_estimate for mp in measure_performances)
        
        # Apply HEI factor (5% bonus or penalty)
        hei_multiplier = 1.0 + (hei_factor / 100.0)
        hei_adjusted_revenue = base_star_revenue * hei_multiplier
        
        total_revenue = hei_adjusted_revenue
        
        return PortfolioPerformance(
            total_points=total_points,
            weighted_average_stars=weighted_average_stars,
            tier1_stars=tier1_stars,
            tier2_stars=tier2_stars,
            tier3_stars=tier3_stars,
            tier4_hei_factor=hei_factor,
            base_star_revenue=base_star_revenue,
            hei_adjusted_revenue=hei_adjusted_revenue,
            total_revenue=total_revenue,
            measure_performances=measure_performances
        )
    
    def _calculate_tier_average(self, 
                               tier_measures: List[MeasurePerformance]) -> float:
        """Calculate weighted average stars for a tier."""
        if not tier_measures:
            return 0.0
        
        total_points = sum(mp.points for mp in tier_measures)
        total_weight = sum(mp.weight for mp in tier_measures)
        
        return total_points / total_weight if total_weight > 0 else 0.0
    
    def calculate_hei_factor(self,
                            measure_performances_overall: List[MeasurePerformance],
                            measure_performances_underserved: List[MeasurePerformance]) -> float:
        """
        Calculate Health Equity Index (HEI) bonus/penalty factor.
        
        Args:
            measure_performances_overall: Performance for overall population
            measure_performances_underserved: Performance for underserved populations
            
        Returns:
            HEI factor (-5.0 to +5.0)
        """
        # Calculate performance gaps
        gaps = []
        
        for overall, underserved in zip(measure_performances_overall, 
                                       measure_performances_underserved):
            if overall.measure_code == underserved.measure_code:
                gap = overall.rate - underserved.rate
                gaps.append(gap)
        
        if not gaps:
            return 0.0
        
        # Average gap across measures
        avg_gap = sum(gaps) / len(gaps)
        
        # CMS HEI scoring (simplified)
        # - Gap < 3%: +5% bonus
        # - Gap 3-5%: 0% (neutral)
        # - Gap > 5%: -5% penalty
        if avg_gap < 0.03:
            return 5.0  # Excellent equity
        elif avg_gap < 0.05:
            return 0.0  # Acceptable equity
        else:
            penalty = min(-5.0, -1.0 * (avg_gap - 0.05) * 100)
            return penalty  # Poor equity = penalty
    
    def estimate_revenue_impact(self,
                               current_stars: float,
                               projected_stars: float,
                               hei_current: float = 0.0,
                               hei_projected: float = 0.0) -> Dict[str, float]:
        """
        Estimate revenue impact of Star Rating improvement.
        
        Args:
            current_stars: Current weighted average stars
            projected_stars: Projected stars after interventions
            hei_current: Current HEI factor
            hei_projected: Projected HEI factor
            
        Returns:
            Dictionary with revenue impact breakdown
        """
        # Base revenue impact
        star_improvement = projected_stars - current_stars
        base_revenue_impact = star_improvement * self.revenue_per_full_star
        
        # HEI revenue impact
        hei_improvement = hei_projected - hei_current
        # Assuming $40M at risk for HEI
        hei_revenue_impact = (hei_improvement / 10.0) * 40000000
        
        # Total impact
        total_revenue_impact = base_revenue_impact + hei_revenue_impact
        
        return {
            "star_improvement": star_improvement,
            "base_revenue_impact": base_revenue_impact,
            "hei_improvement": hei_improvement,
            "hei_revenue_impact": hei_revenue_impact,
            "total_revenue_impact": total_revenue_impact,
        }
    
    def format_portfolio_report(self, 
                               portfolio: PortfolioPerformance) -> str:
        """
        Generate formatted portfolio performance report.
        
        Args:
            portfolio: PortfolioPerformance object
            
        Returns:
            Formatted report string
        """
        report = []
        report.append("=" * 80)
        report.append("HEDIS STAR RATING PORTFOLIO PERFORMANCE REPORT")
        report.append("=" * 80)
        report.append("")
        
        # Overall performance
        report.append("OVERALL PERFORMANCE")
        report.append("-" * 80)
        report.append(f"Total Points:           {portfolio.total_points:.2f}")
        report.append(f"Weighted Average Stars: {portfolio.weighted_average_stars:.2f} ⭐")
        report.append(f"Base Star Revenue:      ${portfolio.base_star_revenue:,.0f}")
        report.append(f"HEI Factor:             {portfolio.tier4_hei_factor:+.2f}%")
        report.append(f"HEI-Adjusted Revenue:   ${portfolio.hei_adjusted_revenue:,.0f}")
        report.append(f"Total Revenue:          ${portfolio.total_revenue:,.0f}")
        report.append("")
        
        # Tier performance
        report.append("TIER PERFORMANCE")
        report.append("-" * 80)
        report.append(f"Tier 1 (Diabetes):       {portfolio.tier1_stars:.2f} ⭐")
        report.append(f"Tier 2 (Cardiovascular): {portfolio.tier2_stars:.2f} ⭐")
        report.append(f"Tier 3 (Cancer):         {portfolio.tier3_stars:.2f} ⭐")
        report.append("")
        
        # Measure details
        report.append("MEASURE DETAILS")
        report.append("-" * 80)
        report.append(f"{'Code':<10} {'Name':<40} {'Weight':<8} {'Rate':<8} {'Stars':<8} {'Revenue':<15}")
        report.append("-" * 80)
        
        for mp in sorted(portfolio.measure_performances, key=lambda x: (x.tier, x.measure_code)):
            weight_str = "3x" if mp.weight == 3.0 else "1x"
            report.append(
                f"{mp.measure_code:<10} "
                f"{mp.measure_name[:40]:<40} "
                f"{weight_str:<8} "
                f"{mp.rate*100:>6.1f}% "
                f"{mp.star_rating:>6.1f}⭐ "
                f"${mp.revenue_estimate:>13,.0f}"
            )
        
        report.append("=" * 80)
        
        return "\n".join(report)


# Convenience functions
def calculate_simple_star_rating(rate: float) -> float:
    """
    Simple star rating calculation based on rate.
    
    Args:
        rate: Measure rate (0.0-1.0)
        
    Returns:
        Star rating (1.0-5.0)
    """
    percentile = rate * 100
    
    if percentile >= 90:
        return 5.0
    elif percentile >= 85:
        return 4.5
    elif percentile >= 75:
        return 4.0
    elif percentile >= 65:
        return 3.5
    elif percentile >= 50:
        return 3.0
    elif percentile >= 40:
        return 2.5
    elif percentile >= 25:
        return 2.0
    elif percentile >= 15:
        return 1.5
    else:
        return 1.0


def estimate_measure_value(star_rating: float, 
                          weight: float = 1.0,
                          revenue_per_point: float = 50000) -> float:
    """
    Estimate financial value of a measure.
    
    Args:
        star_rating: Star rating (1.0-5.0)
        weight: Measure weight (1.0 or 3.0)
        revenue_per_point: Revenue per 0.1 Star point
        
    Returns:
        Estimated revenue value
    """
    points = star_rating * weight
    return points * revenue_per_point


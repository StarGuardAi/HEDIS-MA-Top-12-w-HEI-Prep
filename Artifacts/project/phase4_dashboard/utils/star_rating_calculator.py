"""
Medicare Advantage Star Rating Calculator
Implements CMS Star Rating calculation methodology
"""
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from enum import Enum
import numpy as np


class Domain(Enum):
    """Star Rating domains."""
    PROCESS = "Process"
    OUTCOME = "Outcome"
    PATIENT_EXPERIENCE = "Patient Experience"
    ACCESS = "Access"


@dataclass
class MeasureWeight:
    """Measure weight configuration."""
    measure_id: str
    domain: Domain
    weight: float
    cut_points: Dict[float, float]  # {star_rating: threshold}
    improvement_bonus: bool = False  # Improvement bonus eligible


@dataclass
class MeasureScore:
    """Current measure score."""
    measure_id: str
    current_rate: float
    domain: Domain
    weight: float
    current_star: float
    cut_points: Dict[float, float]


@dataclass
class DomainScore:
    """Domain score calculation."""
    domain: Domain
    weighted_sum: float
    total_weight: float
    domain_star: float


class StarRatingCalculator:
    """
    Medicare Advantage Star Rating Calculator.
    Implements CMS methodology for calculating Star Ratings.
    """
    
    def __init__(self):
        # CMS Star Rating measure weights (simplified - actual weights vary by year)
        self.measure_weights = {
            "HBA1C": MeasureWeight(
                measure_id="HBA1C",
                domain=Domain.OUTCOME,
                weight=0.15,
                cut_points={5.0: 95.0, 4.0: 90.0, 3.0: 85.0, 2.0: 75.0, 1.0: 0.0},
                improvement_bonus=True
            ),
            "BP": MeasureWeight(
                measure_id="BP",
                domain=Domain.OUTCOME,
                weight=0.12,
                cut_points={5.0: 90.0, 4.0: 85.0, 3.0: 75.0, 2.0: 65.0, 1.0: 0.0},
                improvement_bonus=True
            ),
            "COL": MeasureWeight(
                measure_id="COL",
                domain=Domain.PROCESS,
                weight=0.10,
                cut_points={5.0: 80.0, 4.0: 70.0, 3.0: 60.0, 2.0: 50.0, 1.0: 0.0}
            ),
            "MAM": MeasureWeight(
                measure_id="MAM",
                domain=Domain.PROCESS,
                weight=0.10,
                cut_points={5.0: 85.0, 4.0: 75.0, 3.0: 65.0, 2.0: 55.0, 1.0: 0.0}
            ),
            "CCS": MeasureWeight(
                measure_id="CCS",
                domain=Domain.PROCESS,
                weight=0.08,
                cut_points={5.0: 90.0, 4.0: 80.0, 3.0: 70.0, 2.0: 60.0, 1.0: 0.0}
            ),
            "CAHPS": MeasureWeight(
                measure_id="CAHPS",
                domain=Domain.PATIENT_EXPERIENCE,
                weight=0.20,
                cut_points={5.0: 4.5, 4.0: 4.0, 3.0: 3.5, 2.0: 3.0, 1.0: 0.0}
            ),
            "ACCESS": MeasureWeight(
                measure_id="ACCESS",
                domain=Domain.ACCESS,
                weight=0.15,
                cut_points={5.0: 95.0, 4.0: 90.0, 3.0: 85.0, 2.0: 75.0, 1.0: 0.0}
            )
        }
        
        # Domain weights (simplified)
        self.domain_weights = {
            Domain.PROCESS: 0.25,
            Domain.OUTCOME: 0.30,
            Domain.PATIENT_EXPERIENCE: 0.25,
            Domain.ACCESS: 0.20
        }
    
    def calculate_star_from_rate(self, rate: float, cut_points: Dict[float, float]) -> float:
        """
        Calculate star rating from performance rate.
        
        Args:
            rate: Performance rate (0-100)
            cut_points: Dictionary mapping star ratings to thresholds
        
        Returns:
            Star rating (1.0-5.0)
        """
        # Sort cut points descending
        sorted_cut_points = sorted(cut_points.items(), reverse=True)
        
        for star, threshold in sorted_cut_points:
            if rate >= threshold:
                return star
        
        return 1.0
    
    def calculate_domain_score(self, measure_scores: List[MeasureScore]) -> Dict[Domain, DomainScore]:
        """
        Calculate domain scores from measure scores.
        
        Args:
            measure_scores: List of measure scores
        
        Returns:
            Dictionary mapping domains to domain scores
        """
        domain_scores = {}
        
        for domain in Domain:
            domain_measures = [m for m in measure_scores if m.domain == domain]
            
            if not domain_measures:
                domain_scores[domain] = DomainScore(
                    domain=domain,
                    weighted_sum=0.0,
                    total_weight=0.0,
                    domain_star=0.0
                )
                continue
            
            # Calculate weighted sum
            weighted_sum = sum(m.current_star * m.weight for m in domain_measures)
            total_weight = sum(m.weight for m in domain_measures)
            
            # Calculate domain star (weighted average)
            domain_star = weighted_sum / total_weight if total_weight > 0 else 0.0
            
            domain_scores[domain] = DomainScore(
                domain=domain,
                weighted_sum=weighted_sum,
                total_weight=total_weight,
                domain_star=domain_star
            )
        
        return domain_scores
    
    def calculate_overall_rating(self, domain_scores: Dict[Domain, DomainScore]) -> float:
        """
        Calculate overall Star Rating from domain scores.
        
        Args:
            domain_scores: Dictionary of domain scores
        
        Returns:
            Overall Star Rating (1.0-5.0)
        """
        weighted_sum = 0.0
        total_weight = 0.0
        
        for domain, score in domain_scores.items():
            weight = self.domain_weights.get(domain, 0.0)
            weighted_sum += score.domain_star * weight
            total_weight += weight
        
        overall_rating = weighted_sum / total_weight if total_weight > 0 else 0.0
        
        # Round to nearest 0.5
        return round(overall_rating * 2) / 2
    
    def calculate_current_state(self, current_rates: Dict[str, float]) -> Dict:
        """
        Calculate current Star Rating state.
        
        Args:
            current_rates: Dictionary mapping measure_id to current rate
        
        Returns:
            Dictionary with current state assessment
        """
        # Create measure scores
        measure_scores = []
        for measure_id, rate in current_rates.items():
            if measure_id not in self.measure_weights:
                continue
            
            weight_config = self.measure_weights[measure_id]
            star = self.calculate_star_from_rate(rate, weight_config.cut_points)
            
            measure_scores.append(MeasureScore(
                measure_id=measure_id,
                current_rate=rate,
                domain=weight_config.domain,
                weight=weight_config.weight,
                current_star=star,
                cut_points=weight_config.cut_points
            ))
        
        # Calculate domain scores
        domain_scores = self.calculate_domain_score(measure_scores)
        
        # Calculate overall rating
        overall_rating = self.calculate_overall_rating(domain_scores)
        
        # Calculate distance to next tier
        next_tier = self._get_next_tier(overall_rating)
        distance_to_next = next_tier - overall_rating
        
        return {
            "overall_rating": overall_rating,
            "domain_scores": domain_scores,
            "measure_scores": measure_scores,
            "next_tier": next_tier,
            "distance_to_next": distance_to_next
        }
    
    def simulate_improvement(
        self,
        current_rates: Dict[str, float],
        improvements: Dict[str, float]
    ) -> Dict:
        """
        Simulate impact of measure improvements.
        
        Args:
            current_rates: Current measure rates
            improvements: Dictionary mapping measure_id to improvement (percentage points)
        
        Returns:
            Dictionary with projected state
        """
        # Apply improvements
        projected_rates = current_rates.copy()
        for measure_id, improvement in improvements.items():
            if measure_id in projected_rates:
                projected_rates[measure_id] = min(100.0, projected_rates[measure_id] + improvement)
        
        # Calculate projected state
        projected_state = self.calculate_current_state(projected_rates)
        
        # Calculate change
        current_state = self.calculate_current_state(current_rates)
        
        return {
            "projected_rating": projected_state["overall_rating"],
            "current_rating": current_state["overall_rating"],
            "rating_change": projected_state["overall_rating"] - current_state["overall_rating"],
            "projected_domain_scores": projected_state["domain_scores"],
            "current_domain_scores": current_state["domain_scores"],
            "projected_measure_scores": projected_state["measure_scores"],
            "improvements": improvements
        }
    
    def calculate_required_improvements(
        self,
        current_rates: Dict[str, float],
        target_rating: float
    ) -> Dict[str, float]:
        """
        Calculate required improvements to reach target rating.
        
        Args:
            current_rates: Current measure rates
            target_rating: Target overall Star Rating
        
        Returns:
            Dictionary mapping measure_id to required improvement
        """
        # This is a simplified calculation
        # In practice, this would use optimization algorithms
        
        current_state = self.calculate_current_state(current_rates)
        current_rating = current_state["overall_rating"]
        
        if current_rating >= target_rating:
            return {}
        
        # Calculate gap
        rating_gap = target_rating - current_rating
        
        # Distribute improvement across measures (proportional to weight)
        required_improvements = {}
        
        for measure_score in current_state["measure_scores"]:
            # Calculate potential improvement
            weight = measure_score.weight
            current_star = measure_score.current_star
            
            # Estimate improvement needed (simplified)
            improvement_needed = rating_gap * weight * 10  # Rough estimate
            
            # Get next cut point
            next_cut_point = self._get_next_cut_point(
                measure_score.current_rate,
                measure_score.cut_points
            )
            
            if next_cut_point:
                improvement_to_next = max(0, next_cut_point - measure_score.current_rate)
                required_improvements[measure_score.measure_id] = improvement_to_next
        
        return required_improvements
    
    def _get_next_tier(self, current_rating: float) -> float:
        """Get next star tier."""
        tiers = [1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0]
        for tier in tiers:
            if tier > current_rating:
                return tier
        return 5.0
    
    def _get_next_cut_point(
        self,
        current_rate: float,
        cut_points: Dict[float, float]
    ) -> Optional[float]:
        """Get next cut point threshold."""
        sorted_cut_points = sorted(cut_points.items(), reverse=True)
        
        for star, threshold in sorted_cut_points:
            if current_rate < threshold:
                return threshold
        
        return None
    
    def prioritize_measures(
        self,
        current_rates: Dict[str, float],
        target_rating: float
    ) -> List[Dict]:
        """
        Prioritize measures for improvement.
        
        Returns:
            List of prioritized measures with effort vs impact
        """
        current_state = self.calculate_current_state(current_rates)
        
        priorities = []
        
        for measure_score in current_state["measure_scores"]:
            # Calculate impact (how much improvement needed to next star)
            next_cut_point = self._get_next_cut_point(
                measure_score.current_rate,
                measure_score.cut_points
            )
            
            if next_cut_point:
                improvement_needed = next_cut_point - measure_score.current_rate
                impact = measure_score.weight * (measure_score.current_star + 1 - measure_score.current_star)
                
                # Estimate effort (simplified - based on current rate)
                effort = improvement_needed / 10.0  # Rough estimate
                
                # Calculate efficiency (impact / effort)
                efficiency = impact / effort if effort > 0 else 0
                
                priorities.append({
                    "measure_id": measure_score.measure_id,
                    "current_rate": measure_score.current_rate,
                    "current_star": measure_score.current_star,
                    "improvement_needed": improvement_needed,
                    "impact": impact,
                    "effort": effort,
                    "efficiency": efficiency,
                    "next_cut_point": next_cut_point
                })
        
        # Sort by efficiency (highest first)
        priorities.sort(key=lambda x: x["efficiency"], reverse=True)
        
        return priorities


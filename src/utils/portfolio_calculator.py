"""
Portfolio Calculator for HEDIS Measures

This module integrates multiple HEDIS measures into a unified portfolio calculator
that combines predictions, calculates Star Rating impact, and provides ROI analysis.

Supports:
- Portfolio-level aggregation across measures
- Star Rating impact calculation
- ROI analysis and value projection
- Member segmentation by gap patterns

HEDIS Specification: MY2025 Volume 2
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Tuple
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class PortfolioCalculator:
    """
    Calculate portfolio-level metrics across multiple HEDIS measures.
    
    Integrates 11 measures across 3 tiers:
    
    TIER 1 - Diabetes Portfolio (5 measures):
    - GSD (Glycemic Status Assessment) [3x]
    - KED (Kidney Health Evaluation) [3x] - NEW 2025
    - EED (Eye Exam for Diabetes)
    - PDC-DR (Medication Adherence - Diabetes)
    - BPD (Blood Pressure Control - Diabetes) - NEW 2025
    
    TIER 2 - Cardiovascular Portfolio (4 measures):
    - CBP (Controlling High Blood Pressure) [3x]
    - SUPD (Statin Therapy for Diabetes)
    - PDC-RASA (Medication Adherence - Hypertension)
    - PDC-STA (Medication Adherence - Cholesterol)
    
    TIER 3 - Cancer Screening Portfolio (2 measures):
    - BCS (Breast Cancer Screening)
    - COL (Colorectal Cancer Screening)
    
    TIER 4 - Health Equity Portfolio (1 measure):
    - HEI (Health Equity Index) - NEW 2027 REQUIREMENT
    
    Total Portfolio Value: $13M-$27M/year (100K member plan)
    Star Rating Coverage: 30-35% of total
    HEI Protection: $10M-$20M/year downside risk mitigation
    """
    
    # Measure weights (for Star Rating calculation)
    MEASURE_WEIGHTS = {
        # Tier 1: Diabetes Portfolio
        "GSD": 3.0,  # Triple-weighted
        "KED": 3.0,  # Triple-weighted, NEW 2025
        "EED": 1.0,  # Standard
        "PDC-DR": 1.0,  # Standard
        "BPD": 1.0,  # Standard, NEW 2025
        
        # Tier 2: Cardiovascular Portfolio
        "CBP": 3.0,  # Triple-weighted
        "SUPD": 1.0,  # Standard
        "PDC-RASA": 1.0,  # Standard
        "PDC-STA": 1.0,  # Standard
        
        # Tier 3: Cancer Screening Portfolio
        "BCS": 1.0,  # Standard
        "COL": 1.0,  # Standard
        
        # Tier 4: Health Equity Portfolio
        "HEI": 1.0,  # Equity measure (spans all measures)
    }
    
    # Measure values (annual quality bonus payment range for 100K member plan)
    MEASURE_VALUES = {
        # Tier 1: Diabetes Portfolio ($1.2M-$1.4M total)
        "GSD": (360000, 615000),  # $360K-$615K
        "KED": (360000, 615000),  # $360K-$615K
        "EED": (120000, 205000),  # $120K-$205K
        "PDC-DR": (120000, 205000),  # $120K-$205K
        "BPD": (120000, 205000),  # $120K-$205K
        
        # Tier 2: Cardiovascular Portfolio ($620K-$930K total)
        "CBP": (300000, 450000),  # $300K-$450K (3x weighted!)
        "SUPD": (120000, 180000),  # $120K-$180K
        "PDC-RASA": (100000, 150000),  # $100K-$150K
        "PDC-STA": (100000, 150000),  # $100K-$150K
        
        # Tier 3: Cancer Screening Portfolio ($300K-$450K total)
        "BCS": (150000, 225000),  # $150K-$225K
        "COL": (150000, 225000),  # $150K-$225K
        
        # Tier 4: Health Equity Portfolio ($10M-$20M PROTECTION)
        "HEI": (10000000, 20000000),  # $10M-$20M downside risk protection
    }
    
    # NEW 2025 measures (high priority)
    NEW_2025_MEASURES = {"KED", "BPD"}
    
    # NEW 2027 measures (CRITICAL - mandatory reporting)
    NEW_2027_MEASURES = {"HEI"}
    
    # Tier assignments
    TIER_1_MEASURES = {"GSD", "KED", "EED", "PDC-DR", "BPD"}
    TIER_2_MEASURES = {"CBP", "SUPD", "PDC-RASA", "PDC-STA"}
    TIER_3_MEASURES = {"BCS", "COL"}
    TIER_4_MEASURES = {"HEI"}
    
    # Triple-weighted measures (highest Star Rating impact)
    TRIPLE_WEIGHTED_MEASURES = {"GSD", "KED", "CBP"}
    
    def __init__(self, measurement_year: int = 2023):
        """
        Initialize portfolio calculator.
        
        Args:
            measurement_year: Measurement year for calculations
        """
        self.measurement_year = measurement_year
        logger.info("Portfolio calculator initialized for MY%d", measurement_year)
    
    def load_measure_predictions(
        self,
        measure_results: Dict[str, pd.DataFrame]
    ) -> pd.DataFrame:
        """
        Load and combine predictions from multiple measures.
        
        Args:
            measure_results: Dictionary of measure results DataFrames
                {
                    "GSD": gsd_results_df,
                    "KED": ked_results_df,
                    "EED": eed_results_df,
                    "PDC-DR": pdc_dr_results_df,
                    "BPD": bpd_results_df,
                }
                
        Returns:
            Combined DataFrame with member-level results across all measures
        """
        if not measure_results:
            logger.warning("No measure results provided")
            return pd.DataFrame()
        
        # Start with first measure
        first_measure = list(measure_results.keys())[0]
        combined_df = measure_results[first_measure][["DESYNPUF_ID", "age"]].copy()
        combined_df = combined_df.rename(columns={"DESYNPUF_ID": "member_id"})
        
        # Add each measure's results
        for measure_code, results_df in measure_results.items():
            # Extract key columns
            measure_data = results_df[[
                "DESYNPUF_ID",
                "in_denominator",
                "excluded",
                "has_gap",
                "numerator_compliant"
            ]].copy()
            
            # Rename columns with measure prefix
            measure_data = measure_data.rename(columns={
                "DESYNPUF_ID": "member_id",
                "in_denominator": f"{measure_code}_denominator",
                "excluded": f"{measure_code}_excluded",
                "has_gap": f"{measure_code}_gap",
                "numerator_compliant": f"{measure_code}_compliant",
            })
            
            # Merge with combined data
            combined_df = combined_df.merge(
                measure_data,
                on="member_id",
                how="outer"
            )
        
        # Fill NaN values (member not in measure denominator)
        for measure_code in measure_results.keys():
            combined_df[f"{measure_code}_denominator"] = combined_df[f"{measure_code}_denominator"].fillna(False)
            combined_df[f"{measure_code}_excluded"] = combined_df[f"{measure_code}_excluded"].fillna(False)
            combined_df[f"{measure_code}_gap"] = combined_df[f"{measure_code}_gap"].fillna(False)
            combined_df[f"{measure_code}_compliant"] = combined_df[f"{measure_code}_compliant"].fillna(False)
        
        logger.info("Combined results for %d members across %d measures",
                   len(combined_df), len(measure_results))
        
        return combined_df
    
    def calculate_member_gaps(
        self,
        combined_df: pd.DataFrame,
        measure_codes: Optional[List[str]] = None
    ) -> pd.DataFrame:
        """
        Calculate gap counts and patterns for each member.
        
        Args:
            combined_df: Combined measure results from load_measure_predictions()
            measure_codes: List of measures to include (default: all)
            
        Returns:
            DataFrame with gap analysis columns added
        """
        if measure_codes is None:
            measure_codes = list(self.MEASURE_WEIGHTS.keys())
        
        result_df = combined_df.copy()
        
        # Count total gaps per member
        gap_cols = [f"{measure}_gap" for measure in measure_codes]
        result_df["total_gaps"] = result_df[gap_cols].sum(axis=1)
        
        # Count denominators (measures member is eligible for)
        denom_cols = [f"{measure}_denominator" for measure in measure_codes]
        result_df["total_denominators"] = result_df[denom_cols].sum(axis=1)
        
        # Calculate gap rate (gaps / eligible measures)
        result_df["member_gap_rate"] = np.where(
            result_df["total_denominators"] > 0,
            result_df["total_gaps"] / result_df["total_denominators"],
            0.0
        )
        
        # Multi-measure gap flags
        result_df["has_any_gap"] = result_df["total_gaps"] > 0
        result_df["has_multiple_gaps"] = result_df["total_gaps"] >= 2
        result_df["has_3plus_gaps"] = result_df["total_gaps"] >= 3
        result_df["has_all_gaps"] = result_df["total_gaps"] == result_df["total_denominators"]
        
        # Triple-weighted measure gaps (high priority)
        triple_weighted = list(self.TRIPLE_WEIGHTED_MEASURES.intersection(set(measure_codes)))
        triple_gap_cols = [f"{m}_gap" for m in triple_weighted if m in measure_codes]
        result_df["triple_weighted_gaps"] = result_df[triple_gap_cols].sum(axis=1)
        
        # NEW 2025 measure gaps (high priority)
        new_2025 = [m for m in self.NEW_2025_MEASURES if m in measure_codes]
        new_gap_cols = [f"{m}_gap" for m in new_2025]
        result_df["new_2025_gaps"] = result_df[new_gap_cols].sum(axis=1)
        
        logger.info("Calculated gaps for %d members", len(result_df))
        
        return result_df
    
    def calculate_star_rating_impact(
        self,
        measure_summaries: Dict[str, Dict],
        measure_codes: Optional[List[str]] = None
    ) -> Dict:
        """
        Calculate current Star Rating and potential improvement.
        
        Args:
            measure_summaries: Dictionary of measure summary statistics
                {
                    "GSD": {"compliance_rate": 85.0, ...},
                    "KED": {"compliance_rate": 72.0, ...},
                    ...
                }
            measure_codes: List of measures to include (default: all)
            
        Returns:
            Dictionary with Star Rating analysis
        """
        if measure_codes is None:
            measure_codes = list(self.MEASURE_WEIGHTS.keys())
        
        # Calculate weighted average compliance rate
        total_weight = 0.0
        weighted_compliance = 0.0
        
        for measure in measure_codes:
            if measure in measure_summaries:
                weight = self.MEASURE_WEIGHTS.get(measure, 1.0)
                compliance = measure_summaries[measure].get("compliance_rate", 0.0)
                
                weighted_compliance += compliance * weight
                total_weight += weight
        
        current_rate = weighted_compliance / total_weight if total_weight > 0 else 0.0
        
        # Estimate Star Rating (simplified)
        # Actual Star Ratings use percentile rankings, this is a directional estimate
        if current_rate >= 90:
            current_stars = 5.0
        elif current_rate >= 80:
            current_stars = 4.0
        elif current_rate >= 70:
            current_stars = 3.0
        elif current_rate >= 60:
            current_stars = 2.0
        else:
            current_stars = 1.0
        
        # Calculate potential with 100% gap closure
        potential_rate = 100.0  # Perfect score
        potential_stars = 5.0
        
        # Calculate potential with 50% gap closure
        improvement_50pct = (potential_rate - current_rate) * 0.5
        mid_rate = current_rate + improvement_50pct
        
        if mid_rate >= 90:
            mid_stars = 5.0
        elif mid_rate >= 80:
            mid_stars = 4.0
        elif mid_rate >= 70:
            mid_stars = 3.0
        elif mid_rate >= 60:
            mid_stars = 2.0
        else:
            mid_stars = 1.0
        
        star_impact = {
            "current_weighted_rate": round(current_rate, 2),
            "current_stars": current_stars,
            "with_50pct_closure": {
                "weighted_rate": round(mid_rate, 2),
                "stars": mid_stars,
                "star_improvement": round(mid_stars - current_stars, 1),
            },
            "with_100pct_closure": {
                "weighted_rate": round(potential_rate, 2),
                "stars": potential_stars,
                "star_improvement": round(potential_stars - current_stars, 1),
            },
            "total_weight": total_weight,
        }
        
        logger.info("Star Rating: %.1f stars (%.1f%% weighted rate)",
                   current_stars, current_rate)
        
        return star_impact
    
    def calculate_portfolio_value(
        self,
        measure_summaries: Dict[str, Dict],
        measure_codes: Optional[List[str]] = None
    ) -> Dict:
        """
        Calculate portfolio value and ROI potential.
        
        Args:
            measure_summaries: Dictionary of measure summary statistics
            measure_codes: List of measures to include (default: all)
            
        Returns:
            Dictionary with value analysis
        """
        if measure_codes is None:
            measure_codes = list(self.MEASURE_WEIGHTS.keys())
        
        total_value_min = 0
        total_value_max = 0
        current_value_min = 0
        current_value_max = 0
        potential_value_min = 0
        potential_value_max = 0
        
        measure_values = []
        
        for measure in measure_codes:
            if measure not in measure_summaries:
                continue
            
            summary = measure_summaries[measure]
            compliance_rate = summary.get("compliance_rate", 0.0) / 100.0
            
            # Measure value range
            value_min, value_max = self.MEASURE_VALUES.get(measure, (0, 0))
            
            # Current value (proportional to compliance rate)
            current_min = value_min * compliance_rate
            current_max = value_max * compliance_rate
            
            # Potential value (with 100% compliance)
            potential_min = value_min
            potential_max = value_max
            
            # Opportunity value (gap closure)
            opportunity_min = potential_min - current_min
            opportunity_max = potential_max - current_max
            
            measure_values.append({
                "measure": measure,
                "weight": self.MEASURE_WEIGHTS.get(measure, 1.0),
                "compliance_rate": summary.get("compliance_rate", 0.0),
                "gaps": summary.get("gaps", 0),
                "eligible": summary.get("eligible_population", 0),
                "current_value": f"${int(current_min):,}-${int(current_max):,}",
                "potential_value": f"${int(potential_min):,}-${int(potential_max):,}",
                "opportunity_value": f"${int(opportunity_min):,}-${int(opportunity_max):,}",
            })
            
            total_value_min += potential_min
            total_value_max += potential_max
            current_value_min += current_min
            current_value_max += current_max
            potential_value_min += opportunity_min
            potential_value_max += opportunity_max
        
        portfolio_value = {
            "total_portfolio_value": f"${int(total_value_min):,}-${int(total_value_max):,}",
            "current_value": f"${int(current_value_min):,}-${int(current_value_max):,}",
            "opportunity_value": f"${int(potential_value_min):,}-${int(potential_value_max):,}",
            "opportunity_pct": round((potential_value_min / total_value_min * 100) if total_value_min > 0 else 0, 1),
            "measure_breakdown": measure_values,
        }
        
        logger.info("Portfolio value: $%s-$%s (current), $%s-$%s (opportunity)",
                   f"{int(current_value_min):,}", f"{int(current_value_max):,}",
                   f"{int(potential_value_min):,}", f"{int(potential_value_max):,}")
        
        return portfolio_value
    
    def segment_members(
        self,
        combined_df: pd.DataFrame,
        measure_codes: Optional[List[str]] = None
    ) -> Dict[str, pd.DataFrame]:
        """
        Segment members by gap patterns for targeted interventions.
        
        Args:
            combined_df: Combined measure results with gaps calculated
            measure_codes: List of measures to include (default: all)
            
        Returns:
            Dictionary of member segments
        """
        if measure_codes is None:
            measure_codes = list(self.MEASURE_WEIGHTS.keys())
        
        segments = {}
        
        # High-value members (triple-weighted measure gaps)
        segments["high_value"] = combined_df[
            combined_df["triple_weighted_gaps"] > 0
        ].copy()
        
        # NEW 2025 priority (NEW measures with gaps)
        segments["new_2025_priority"] = combined_df[
            combined_df["new_2025_gaps"] > 0
        ].copy()
        
        # Multi-measure opportunities (2+ gaps)
        segments["multi_measure"] = combined_df[
            combined_df["has_multiple_gaps"]
        ].copy()
        
        # Single-gap opportunities
        segments["single_gap"] = combined_df[
            combined_df["total_gaps"] == 1
        ].copy()
        
        # Compliant members (no gaps)
        segments["compliant"] = combined_df[
            combined_df["total_gaps"] == 0
        ].copy()
        
        # Log segment sizes
        for segment_name, segment_df in segments.items():
            logger.info("Segment '%s': %d members", segment_name, len(segment_df))
        
        return segments
    
    def generate_portfolio_summary(
        self,
        measure_summaries: Dict[str, Dict],
        combined_df: pd.DataFrame,
        measure_codes: Optional[List[str]] = None
    ) -> Dict:
        """
        Generate comprehensive portfolio summary.
        
        Args:
            measure_summaries: Dictionary of measure summary statistics
            combined_df: Combined member-level results
            measure_codes: List of measures to include (default: all)
            
        Returns:
            Complete portfolio summary dictionary
        """
        if measure_codes is None:
            measure_codes = list(self.MEASURE_WEIGHTS.keys())
        
        # Calculate components
        star_impact = self.calculate_star_rating_impact(measure_summaries, measure_codes)
        portfolio_value = self.calculate_portfolio_value(measure_summaries, measure_codes)
        segments = self.segment_members(combined_df, measure_codes)
        
        # Overall statistics
        total_members = len(combined_df)
        members_with_gaps = combined_df["has_any_gap"].sum()
        members_multi_gaps = combined_df["has_multiple_gaps"].sum()
        
        summary = {
            "measurement_year": self.measurement_year,
            "portfolio_name": "Tier 1 Diabetes Portfolio",
            "measures_included": measure_codes,
            "total_measures": len(measure_codes),
            
            # Member statistics
            "total_members": int(total_members),
            "members_with_gaps": int(members_with_gaps),
            "members_multi_gaps": int(members_multi_gaps),
            "gap_rate": round((members_with_gaps / total_members * 100) if total_members > 0 else 0, 1),
            
            # Star Rating impact
            "star_rating": star_impact,
            
            # Portfolio value
            "value": portfolio_value,
            
            # Segments
            "segments": {name: len(df) for name, df in segments.items()},
            
            # Individual measures
            "measures": measure_summaries,
        }
        
        logger.info("Portfolio summary generated for %d measures, %d members",
                   len(measure_codes), total_members)
        
        return summary


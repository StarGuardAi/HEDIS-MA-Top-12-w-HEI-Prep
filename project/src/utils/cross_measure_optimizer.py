"""
Cross-Measure Optimizer for HEDIS Portfolio

This module optimizes interventions across multiple HEDIS measures by identifying
high-value opportunities, prioritizing members, and bundling interventions for
maximum efficiency and ROI.

Features:
- Multi-measure member identification
- Priority scoring and ranking
- Intervention bundling
- ROI optimization
- Resource allocation

HEDIS Specification: MY2025 Volume 2
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Tuple
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class CrossMeasureOptimizer:
    """
    Optimize interventions across multiple HEDIS measures for maximum ROI.
    
    Prioritization factors:
    1. Triple-weighted measures (GSD, KED)
    2. NEW 2025 measures (KED, BPD)
    3. Multiple gaps (efficiency)
    4. Prediction probability (likelihood to close)
    """
    
    # Priority weights for scoring
    PRIORITY_WEIGHTS = {
        "triple_weighted": 3.0,
        "new_2025": 2.0,
        "multi_measure": 1.5,
        "single_measure": 1.0,
    }
    
    # Intervention costs (estimated per member per gap)
    INTERVENTION_COSTS = {
        "GSD": 150,  # HbA1c test + outreach
        "KED": 200,  # eGFR + ACR tests + outreach
        "EED": 180,  # Eye exam + outreach
        "PDC-DR": 100,  # Medication adherence outreach
        "BPD": 120,  # BP monitoring + outreach
    }
    
    # Gap closure probabilities (estimated success rates)
    CLOSURE_RATES = {
        "GSD": 0.60,  # 60% success rate
        "KED": 0.55,  # 55% success rate
        "EED": 0.65,  # 65% success rate
        "PDC-DR": 0.50,  # 50% success rate
        "BPD": 0.58,  # 58% success rate
    }
    
    # Measure values (for ROI calculation)
    MEASURE_VALUES = {
        "GSD": (360000, 615000),
        "KED": (360000, 615000),
        "EED": (120000, 205000),
        "PDC-DR": (120000, 205000),
        "BPD": (120000, 205000),
    }
    
    def __init__(self):
        """Initialize cross-measure optimizer."""
        logger.info("Cross-measure optimizer initialized")
    
    def identify_multi_measure_members(
        self,
        combined_df: pd.DataFrame,
        min_gaps: int = 2
    ) -> pd.DataFrame:
        """
        Identify members with gaps in multiple measures.
        
        Args:
            combined_df: Combined measure results with gaps
            min_gaps: Minimum number of gaps to include (default: 2)
            
        Returns:
            DataFrame of members with multiple gaps, sorted by priority
        """
        # Filter to members with multiple gaps
        multi_gap_members = combined_df[
            combined_df["total_gaps"] >= min_gaps
        ].copy()
        
        if multi_gap_members.empty:
            logger.warning("No members found with %d+ gaps", min_gaps)
            return pd.DataFrame()
        
        logger.info("Found %d members with %d+ gaps",
                   len(multi_gap_members), min_gaps)
        
        return multi_gap_members
    
    def calculate_priority_score(
        self,
        combined_df: pd.DataFrame,
        measure_codes: Optional[List[str]] = None
    ) -> pd.DataFrame:
        """
        Calculate priority score for each member based on multiple factors.
        
        Scoring factors:
        - Triple-weighted measure gaps (×3.0)
        - NEW 2025 measure gaps (×2.0)
        - Multiple gaps (×1.5)
        - Gap count (linear)
        
        Args:
            combined_df: Combined measure results with gaps
            measure_codes: List of measures to include (default: all 5)
            
        Returns:
            DataFrame with priority_score column added
        """
        if measure_codes is None:
            measure_codes = ["GSD", "KED", "EED", "PDC-DR", "BPD"]
        
        result_df = combined_df.copy()
        result_df["priority_score"] = 0.0
        
        # Factor 1: Triple-weighted measure gaps (high priority)
        triple_weighted = ["GSD", "KED"]
        for measure in triple_weighted:
            if measure in measure_codes:
                result_df["priority_score"] += (
                    result_df[f"{measure}_gap"].astype(int) * 
                    self.PRIORITY_WEIGHTS["triple_weighted"]
                )
        
        # Factor 2: NEW 2025 measure gaps (high priority)
        new_2025 = ["KED", "BPD"]
        for measure in new_2025:
            if measure in measure_codes:
                result_df["priority_score"] += (
                    result_df[f"{measure}_gap"].astype(int) * 
                    self.PRIORITY_WEIGHTS["new_2025"]
                )
        
        # Factor 3: Multiple gaps (efficiency bonus)
        result_df["priority_score"] += np.where(
            result_df["has_multiple_gaps"],
            self.PRIORITY_WEIGHTS["multi_measure"],
            0.0
        )
        
        # Factor 4: Total gap count (linear)
        result_df["priority_score"] += result_df["total_gaps"] * 0.5
        
        # Normalize to 0-100 scale
        if result_df["priority_score"].max() > 0:
            result_df["priority_score"] = (
                result_df["priority_score"] / result_df["priority_score"].max() * 100
            )
        
        logger.info("Calculated priority scores for %d members", len(result_df))
        
        return result_df
    
    def rank_members_by_roi(
        self,
        combined_df: pd.DataFrame,
        eligible_denominators: Dict[str, int],
        measure_codes: Optional[List[str]] = None
    ) -> pd.DataFrame:
        """
        Rank members by expected ROI from interventions.
        
        ROI = (Expected value from gap closure) / (Intervention cost)
        
        Args:
            combined_df: Combined measure results with priority scores
            eligible_denominators: Dictionary of eligible population by measure
            measure_codes: List of measures to include (default: all 5)
            
        Returns:
            DataFrame with ROI columns added, sorted by expected ROI
        """
        if measure_codes is None:
            measure_codes = ["GSD", "KED", "EED", "PDC-DR", "BPD"]
        
        result_df = combined_df.copy()
        result_df["total_cost"] = 0.0
        result_df["expected_value_min"] = 0.0
        result_df["expected_value_max"] = 0.0
        
        # Calculate cost and expected value for each measure gap
        for measure in measure_codes:
            # Skip if not in denominator
            if not result_df[f"{measure}_gap"].any():
                continue
            
            # Intervention cost
            cost_per_member = self.INTERVENTION_COSTS.get(measure, 100)
            result_df["total_cost"] += (
                result_df[f"{measure}_gap"].astype(int) * cost_per_member
            )
            
            # Expected value (value per member × closure rate)
            eligible_pop = eligible_denominators.get(measure, 1)
            value_min, value_max = self.MEASURE_VALUES.get(measure, (0, 0))
            value_per_member_min = value_min / eligible_pop if eligible_pop > 0 else 0
            value_per_member_max = value_max / eligible_pop if eligible_pop > 0 else 0
            closure_rate = self.CLOSURE_RATES.get(measure, 0.5)
            
            result_df["expected_value_min"] += (
                result_df[f"{measure}_gap"].astype(int) * 
                value_per_member_min * 
                closure_rate
            )
            result_df["expected_value_max"] += (
                result_df[f"{measure}_gap"].astype(int) * 
                value_per_member_max * 
                closure_rate
            )
        
        # Calculate ROI
        result_df["expected_roi_min"] = np.where(
            result_df["total_cost"] > 0,
            result_df["expected_value_min"] / result_df["total_cost"],
            0.0
        )
        result_df["expected_roi_max"] = np.where(
            result_df["total_cost"] > 0,
            result_df["expected_value_max"] / result_df["total_cost"],
            0.0
        )
        result_df["expected_roi_avg"] = (
            result_df["expected_roi_min"] + result_df["expected_roi_max"]
        ) / 2.0
        
        # Sort by ROI (descending)
        result_df = result_df.sort_values("expected_roi_avg", ascending=False)
        
        logger.info("Ranked %d members by expected ROI", len(result_df))
        
        return result_df
    
    def identify_intervention_bundles(
        self,
        combined_df: pd.DataFrame,
        measure_codes: Optional[List[str]] = None
    ) -> Dict[str, List[Dict]]:
        """
        Identify intervention bundles for members with multiple gaps.
        
        Bundling strategies:
        - Lab bundle: GSD + KED (both need lab tests)
        - PCP bundle: Multiple tests at single visit
        - Specialty bundle: Eye exam + other specialist needs
        
        Args:
            combined_df: Combined measure results
            measure_codes: List of measures to include (default: all 5)
            
        Returns:
            Dictionary of bundling opportunities
        """
        if measure_codes is None:
            measure_codes = ["GSD", "KED", "EED", "PDC-DR", "BPD"]
        
        bundles = {
            "lab_bundle": [],  # GSD + KED
            "pcp_bundle": [],  # Multiple PCP-based interventions
            "specialty_bundle": [],  # Eye exam + other specialist
            "medication_bundle": [],  # PDC-DR + BPD (medication focus)
        }
        
        for _, member in combined_df.iterrows():
            member_id = member["member_id"]
            
            # Lab bundle: GSD + KED (both need lab tests)
            if member.get("GSD_gap", False) and member.get("KED_gap", False):
                bundles["lab_bundle"].append({
                    "member_id": member_id,
                    "measures": ["GSD", "KED"],
                    "intervention": "Combined lab order (HbA1c + eGFR + ACR)",
                    "cost_saving": self.INTERVENTION_COSTS["GSD"] * 0.3,  # 30% savings
                })
            
            # PCP bundle: Multiple measures addressable at PCP visit
            pcp_gaps = []
            if member.get("GSD_gap", False):
                pcp_gaps.append("GSD")
            if member.get("KED_gap", False):
                pcp_gaps.append("KED")
            if member.get("BPD_gap", False):
                pcp_gaps.append("BPD")
            
            if len(pcp_gaps) >= 2:
                bundles["pcp_bundle"].append({
                    "member_id": member_id,
                    "measures": pcp_gaps,
                    "intervention": "Single PCP visit for multiple tests",
                    "cost_saving": 50 * (len(pcp_gaps) - 1),  # $50 savings per additional test
                })
            
            # Specialty bundle: Eye exam + other needs
            if member.get("EED_gap", False):
                specialty_gaps = ["EED"]
                # Could add retinopathy screening for KED
                if member.get("KED_gap", False):
                    specialty_gaps.append("KED")
                
                if len(specialty_gaps) >= 2:
                    bundles["specialty_bundle"].append({
                        "member_id": member_id,
                        "measures": specialty_gaps,
                        "intervention": "Ophthalmology visit with additional screening",
                        "cost_saving": 40,
                    })
            
            # Medication bundle: PDC-DR + BPD
            if member.get("PDC-DR_gap", False) or member.get("BPD_gap", False):
                med_gaps = []
                if member.get("PDC-DR_gap", False):
                    med_gaps.append("PDC-DR")
                if member.get("BPD_gap", False):
                    med_gaps.append("BPD")
                
                if len(med_gaps) >= 2:
                    bundles["medication_bundle"].append({
                        "member_id": member_id,
                        "measures": med_gaps,
                        "intervention": "Pharmacist consultation (med adherence + BP monitoring)",
                        "cost_saving": 30,
                    })
        
        # Log bundle opportunities
        for bundle_type, bundle_list in bundles.items():
            if bundle_list:
                total_savings = sum(b.get("cost_saving", 0) for b in bundle_list)
                logger.info("%s: %d opportunities ($%d potential savings)",
                           bundle_type, len(bundle_list), int(total_savings))
        
        return bundles
    
    def generate_priority_list(
        self,
        combined_df: pd.DataFrame,
        eligible_denominators: Dict[str, int],
        top_n: Optional[int] = None,
        min_priority_score: Optional[float] = None
    ) -> pd.DataFrame:
        """
        Generate prioritized member list for interventions.
        
        Args:
            combined_df: Combined measure results
            eligible_denominators: Dictionary of eligible population by measure
            top_n: Return only top N members (optional)
            min_priority_score: Minimum priority score to include (optional)
            
        Returns:
            Prioritized DataFrame with actionable recommendations
        """
        # Calculate priority scores
        result_df = self.calculate_priority_score(combined_df)
        
        # Calculate ROI
        result_df = self.rank_members_by_roi(
            result_df,
            eligible_denominators
        )
        
        # Filter by minimum priority score
        if min_priority_score is not None:
            result_df = result_df[result_df["priority_score"] >= min_priority_score]
        
        # Select top N
        if top_n is not None:
            result_df = result_df.head(top_n)
        
        # Add intervention recommendations
        result_df = self._add_intervention_recommendations(result_df)
        
        # Select key columns for output
        output_cols = [
            "member_id",
            "age",
            "total_gaps",
            "priority_score",
            "expected_roi_avg",
            "total_cost",
            "expected_value_min",
            "expected_value_max",
            "intervention_priority",
            "recommended_actions",
        ]
        
        # Add gap columns
        gap_cols = [col for col in result_df.columns if col.endswith("_gap")]
        output_cols.extend(gap_cols)
        
        result_df = result_df[[col for col in output_cols if col in result_df.columns]]
        
        logger.info("Generated priority list: %d members", len(result_df))
        
        return result_df
    
    def _add_intervention_recommendations(
        self,
        result_df: pd.DataFrame
    ) -> pd.DataFrame:
        """Add intervention recommendations to priority list."""
        result_df = result_df.copy()
        
        # Determine intervention priority
        result_df["intervention_priority"] = "Standard"
        result_df.loc[result_df["priority_score"] >= 75, "intervention_priority"] = "High"
        result_df.loc[result_df["priority_score"] >= 90, "intervention_priority"] = "Urgent"
        
        # Generate recommended actions
        def generate_actions(row):
            actions = []
            
            # Check each measure gap
            if row.get("GSD_gap", False):
                actions.append("Schedule HbA1c test")
            if row.get("KED_gap", False):
                actions.append("Order eGFR + ACR tests")
            if row.get("EED_gap", False):
                actions.append("Schedule eye exam")
            if row.get("PDC-DR_gap", False):
                actions.append("Medication adherence counseling")
            if row.get("BPD_gap", False):
                actions.append("BP monitoring + medication review")
            
            # Bundle opportunity
            if row.get("GSD_gap", False) and row.get("KED_gap", False):
                actions.append("⭐ Bundle: Combined lab order")
            
            return " | ".join(actions) if actions else "No actions needed"
        
        result_df["recommended_actions"] = result_df.apply(generate_actions, axis=1)
        
        return result_df
    
    def calculate_portfolio_optimization(
        self,
        combined_df: pd.DataFrame,
        eligible_denominators: Dict[str, int],
        budget: Optional[float] = None
    ) -> Dict:
        """
        Calculate optimal intervention strategy within budget constraints.
        
        Args:
            combined_df: Combined measure results
            eligible_denominators: Dictionary of eligible population by measure
            budget: Available budget for interventions (optional)
            
        Returns:
            Dictionary with optimization results
        """
        # Generate full priority list
        priority_list = self.generate_priority_list(
            combined_df,
            eligible_denominators
        )
        
        if priority_list.empty:
            return {
                "total_members": 0,
                "total_interventions": 0,
                "total_cost": 0,
                "expected_value": (0, 0),
                "expected_roi": 0,
            }
        
        # Apply budget constraint if specified
        if budget is not None:
            cumulative_cost = 0
            budget_constrained = []
            
            for _, row in priority_list.iterrows():
                if cumulative_cost + row["total_cost"] <= budget:
                    budget_constrained.append(row)
                    cumulative_cost += row["total_cost"]
                else:
                    break
            
            optimized_df = pd.DataFrame(budget_constrained)
        else:
            optimized_df = priority_list
        
        # Calculate totals
        total_members = len(optimized_df)
        total_gaps = optimized_df["total_gaps"].sum()
        total_cost = optimized_df["total_cost"].sum()
        expected_value_min = optimized_df["expected_value_min"].sum()
        expected_value_max = optimized_df["expected_value_max"].sum()
        expected_roi = (expected_value_min + expected_value_max) / 2 / total_cost if total_cost > 0 else 0
        
        optimization_results = {
            "total_members": int(total_members),
            "total_interventions": int(total_gaps),
            "total_cost": f"${int(total_cost):,}",
            "expected_value": f"${int(expected_value_min):,}-${int(expected_value_max):,}",
            "expected_roi": round(expected_roi, 2),
            "budget_used": f"${int(total_cost):,}" if budget else "No budget constraint",
            "budget_remaining": f"${int(budget - total_cost):,}" if budget else "N/A",
        }
        
        logger.info("Portfolio optimization: %d members, %d interventions, $%d cost, %.1fx ROI",
                   total_members, total_gaps, int(total_cost), expected_roi)
        
        return optimization_results


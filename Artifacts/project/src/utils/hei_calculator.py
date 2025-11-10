"""
Health Equity Index (HEI) Calculator

This module calculates health equity metrics across HEDIS measures and demographic groups
to comply with CMS Health Equity Index requirements (NEW 2027).

Methodology:
1. Stratify measure performance by race/ethnicity, language, SDOH
2. Calculate disparities (gaps between groups)
3. Compute equity score (0-100 scale)
4. Generate actionable equity reports

CMS Requirement: NEW for MY2025, ENFORCED in 2027
Financial Impact: $10M-$20M/year protection

Author: Analytics Team
Date: October 23, 2025
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Tuple
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# CMS HEI Thresholds
HEI_THRESHOLD_NO_PENALTY = 70  # >= 70: No penalty
HEI_THRESHOLD_MODERATE_PENALTY = 50  # 50-69: -0.25 stars
# < 50: -0.5 stars (HIGH penalty)

# Minimum group size for statistical validity
MIN_GROUP_SIZE = 30


class HEICalculator:
    """
    Calculate Health Equity Index (HEI) metrics across HEDIS measures.
    
    Measures disparities in care across demographic groups and calculates
    equity score for CMS Star Rating compliance.
    """
    
    def __init__(
        self,
        measurement_year: int = 2025,
        min_group_size: int = MIN_GROUP_SIZE
    ):
        """
        Initialize HEI calculator.
        
        Args:
            measurement_year: HEDIS measurement year
            min_group_size: Minimum members per group for valid comparison
        """
        self.measurement_year = measurement_year
        self.min_group_size = min_group_size
        logger.info(f"HEI Calculator initialized for MY{measurement_year}")
    
    def calculate_stratified_performance(
        self,
        measure_results_df: pd.DataFrame,
        hei_data_df: pd.DataFrame,
        measure_code: str,
        stratification_var: str = 'race_ethnicity_std',
        member_id_col: str = 'member_id'
    ) -> pd.DataFrame:
        """
        Calculate measure performance stratified by demographic group.
        
        Args:
            measure_results_df: Measure results (denominator, numerator, gaps)
            hei_data_df: HEI data with demographics/SDOH
            measure_code: HEDIS measure code (e.g., 'GSD', 'KED')
            stratification_var: Variable to stratify by
            member_id_col: Member identifier column
            
        Returns:
            DataFrame with stratified performance metrics
        """
        # Merge measure results with HEI data
        merged_df = measure_results_df.merge(
            hei_data_df[[member_id_col, stratification_var]],
            on=member_id_col,
            how='inner'
        )
        
        # Calculate performance by group
        stratified = merged_df.groupby(stratification_var).agg({
            f'{measure_code}_in_denominator': 'sum',
            f'{measure_code}_in_numerator': 'sum',
            f'{measure_code}_gap': 'sum',
            member_id_col: 'count'
        }).reset_index()
        
        stratified.columns = [
            stratification_var,
            'denominator',
            'numerator',
            'gaps',
            'total_members'
        ]
        
        # Calculate rates
        stratified['compliance_rate'] = (
            stratified['numerator'] / stratified['denominator'] * 100
        ).fillna(0)
        
        stratified['gap_rate'] = (
            stratified['gaps'] / stratified['denominator'] * 100
        ).fillna(0)
        
        # Add measure info
        stratified['measure'] = measure_code
        stratified['measurement_year'] = self.measurement_year
        
        # Flag groups too small for valid comparison
        stratified['is_valid_group'] = (
            stratified['denominator'] >= self.min_group_size
        )
        
        return stratified
    
    def identify_disparities(
        self,
        stratified_df: pd.DataFrame,
        stratification_var: str = 'race_ethnicity_std',
        disparity_threshold: float = 10.0
    ) -> Dict:
        """
        Identify disparities (gaps) between demographic groups.
        
        Args:
            stratified_df: Stratified performance data
            stratification_var: Variable stratified by
            disparity_threshold: Minimum gap to flag as disparity (percentage points)
            
        Returns:
            Dictionary with disparity metrics
        """
        # Filter to valid groups only
        valid_df = stratified_df[stratified_df['is_valid_group']].copy()
        
        if len(valid_df) < 2:
            return {
                'has_disparity': False,
                'reason': 'insufficient_groups',
                'disparity_magnitude': 0,
                'highest_performing_group': None,
                'lowest_performing_group': None,
            }
        
        # Find highest and lowest performing groups
        highest_idx = valid_df['compliance_rate'].idxmax()
        lowest_idx = valid_df['compliance_rate'].idxmin()
        
        highest_group = valid_df.loc[highest_idx, stratification_var]
        lowest_group = valid_df.loc[lowest_idx, stratification_var]
        
        highest_rate = valid_df.loc[highest_idx, 'compliance_rate']
        lowest_rate = valid_df.loc[lowest_idx, 'compliance_rate']
        
        # Calculate disparity magnitude
        disparity_magnitude = highest_rate - lowest_rate
        
        # Determine if this is a meaningful disparity
        has_disparity = disparity_magnitude >= disparity_threshold
        
        disparity_info = {
            'has_disparity': has_disparity,
            'disparity_magnitude': disparity_magnitude,
            'highest_performing_group': highest_group,
            'highest_compliance_rate': highest_rate,
            'lowest_performing_group': lowest_group,
            'lowest_compliance_rate': lowest_rate,
            'measure': valid_df['measure'].iloc[0],
            'stratification_var': stratification_var,
            'disparity_category': self._categorize_disparity(disparity_magnitude),
            'groups_compared': len(valid_df),
        }
        
        return disparity_info
    
    def _categorize_disparity(self, magnitude: float) -> str:
        """
        Categorize disparity severity.
        
        Args:
            magnitude: Disparity magnitude (percentage points)
            
        Returns:
            Disparity category
        """
        if magnitude < 5:
            return 'MINIMAL'
        elif magnitude < 10:
            return 'SMALL'
        elif magnitude < 20:
            return 'MODERATE'
        elif magnitude < 30:
            return 'LARGE'
        else:
            return 'SEVERE'
    
    def calculate_equity_score_single_measure(
        self,
        disparity_info: Dict,
        measure_weight: float = 1.0
    ) -> float:
        """
        Calculate equity score for a single measure (0-100 scale).
        
        Higher score = better equity (lower disparities).
        
        Args:
            disparity_info: Disparity information from identify_disparities()
            measure_weight: Measure weight (3x for triple-weighted measures)
            
        Returns:
            Equity score (0-100)
        """
        if not disparity_info['has_disparity']:
            # No significant disparity = perfect equity score
            return 100.0
        
        # Convert disparity magnitude to equity score
        # 0% disparity = 100 score
        # 50% disparity = 0 score
        disparity_pct = disparity_info['disparity_magnitude']
        
        # Linear scale (could be adjusted)
        equity_score = max(0, 100 - (disparity_pct * 2))
        
        return equity_score
    
    def calculate_portfolio_equity_score(
        self,
        measure_results_dict: Dict[str, pd.DataFrame],
        hei_data_df: pd.DataFrame,
        measure_weights: Dict[str, float],
        stratification_vars: List[str] = ['race_ethnicity_std', 'language_std'],
        member_id_col: str = 'member_id'
    ) -> Dict:
        """
        Calculate overall portfolio equity score across all measures.
        
        Args:
            measure_results_dict: Dictionary of measure results DataFrames
            hei_data_df: HEI data with demographics
            measure_weights: Dictionary of measure weights (for weighting)
            stratification_vars: Variables to stratify by
            member_id_col: Member identifier column
            
        Returns:
            Dictionary with portfolio equity score and details
        """
        logger.info("Calculating portfolio equity score across measures")
        
        all_disparities = []
        measure_equity_scores = {}
        
        # Calculate disparities for each measure and stratification variable
        for measure_code, measure_df in measure_results_dict.items():
            measure_weight = measure_weights.get(measure_code, 1.0)
            
            for strat_var in stratification_vars:
                # Stratified performance
                stratified_df = self.calculate_stratified_performance(
                    measure_df,
                    hei_data_df,
                    measure_code,
                    strat_var,
                    member_id_col
                )
                
                # Identify disparities
                disparity_info = self.identify_disparities(
                    stratified_df,
                    strat_var
                )
                
                # Calculate equity score for this measure/stratification
                equity_score = self.calculate_equity_score_single_measure(
                    disparity_info,
                    measure_weight
                )
                
                disparity_info['equity_score'] = equity_score
                disparity_info['measure_weight'] = measure_weight
                
                all_disparities.append(disparity_info)
                
                # Store measure-level equity score
                key = f"{measure_code}_{strat_var}"
                measure_equity_scores[key] = equity_score
        
        # Calculate weighted average equity score
        total_weight = 0
        weighted_sum = 0
        
        for disparity in all_disparities:
            weight = disparity['measure_weight']
            score = disparity['equity_score']
            weighted_sum += score * weight
            total_weight += weight
        
        overall_equity_score = weighted_sum / total_weight if total_weight > 0 else 0
        
        # Determine penalty tier
        if overall_equity_score >= HEI_THRESHOLD_NO_PENALTY:
            penalty = 0.0
            penalty_category = 'NO_PENALTY'
        elif overall_equity_score >= HEI_THRESHOLD_MODERATE_PENALTY:
            penalty = -0.25
            penalty_category = 'MODERATE_PENALTY'
        else:
            penalty = -0.5
            penalty_category = 'HIGH_PENALTY'
        
        # Calculate financial impact (assuming 100K member plan)
        # Star Rating impact translates to bonus payment
        # Rough estimate: -0.5 stars = -$12M/year for typical plan
        if penalty == -0.5:
            financial_impact = -12000000  # -$12M
        elif penalty == -0.25:
            financial_impact = -6000000  # -$6M
        else:
            financial_impact = 0
        
        result = {
            'overall_equity_score': overall_equity_score,
            'penalty_stars': penalty,
            'penalty_category': penalty_category,
            'financial_impact': financial_impact,
            'measures_evaluated': len(measure_results_dict),
            'stratifications_evaluated': len(stratification_vars),
            'total_comparisons': len(all_disparities),
            'measures_with_disparities': sum(1 for d in all_disparities if d['has_disparity']),
            'severe_disparities': sum(1 for d in all_disparities if d.get('disparity_category') == 'SEVERE'),
            'measure_equity_scores': measure_equity_scores,
            'all_disparities': all_disparities,
        }
        
        logger.info(f"Portfolio Equity Score: {overall_equity_score:.1f} ({penalty_category})")
        
        return result
    
    def generate_equity_report(
        self,
        equity_results: Dict,
        output_format: str = 'summary'
    ) -> str:
        """
        Generate human-readable equity report.
        
        Args:
            equity_results: Results from calculate_portfolio_equity_score()
            output_format: 'summary' or 'detailed'
            
        Returns:
            Formatted report string
        """
        report = []
        
        report.append("=" * 80)
        report.append("HEALTH EQUITY INDEX (HEI) REPORT")
        report.append(f"Measurement Year: {self.measurement_year}")
        report.append("=" * 80)
        report.append("")
        
        # Overall score
        score = equity_results['overall_equity_score']
        penalty = equity_results['penalty_stars']
        penalty_cat = equity_results['penalty_category']
        
        report.append("OVERALL EQUITY SCORE")
        report.append(f"  Score: {score:.1f}/100")
        report.append(f"  Penalty: {penalty} stars ({penalty_cat})")
        report.append(f"  Financial Impact: ${equity_results['financial_impact']:,}")
        report.append("")
        
        # Summary statistics
        report.append("DISPARITY ANALYSIS")
        report.append(f"  Measures Evaluated: {equity_results['measures_evaluated']}")
        report.append(f"  Stratifications: {equity_results['stratifications_evaluated']}")
        report.append(f"  Total Comparisons: {equity_results['total_comparisons']}")
        report.append(f"  Measures with Disparities: {equity_results['measures_with_disparities']}")
        report.append(f"  Severe Disparities: {equity_results['severe_disparities']}")
        report.append("")
        
        if output_format == 'detailed':
            report.append("DETAILED DISPARITY BREAKDOWN")
            report.append("-" * 80)
            
            for disp in equity_results['all_disparities']:
                if disp['has_disparity']:
                    report.append(f"\nMeasure: {disp['measure']}")
                    report.append(f"  Stratification: {disp['stratification_var']}")
                    report.append(f"  Disparity Magnitude: {disp['disparity_magnitude']:.1f} percentage points")
                    report.append(f"  Category: {disp['disparity_category']}")
                    report.append(f"  Highest Group: {disp['highest_performing_group']} ({disp['highest_compliance_rate']:.1f}%)")
                    report.append(f"  Lowest Group: {disp['lowest_performing_group']} ({disp['lowest_compliance_rate']:.1f}%)")
                    report.append(f"  Equity Score: {disp['equity_score']:.1f}/100")
        
        report.append("")
        report.append("=" * 80)
        
        return "\n".join(report)
    
    def identify_priority_interventions(
        self,
        equity_results: Dict,
        top_n: int = 10
    ) -> List[Dict]:
        """
        Identify top priority interventions to address disparities.
        
        Args:
            equity_results: Results from calculate_portfolio_equity_score()
            top_n: Number of top priorities to return
            
        Returns:
            List of priority interventions
        """
        all_disparities = equity_results['all_disparities']
        
        # Filter to measures with disparities
        disparities_only = [d for d in all_disparities if d['has_disparity']]
        
        # Sort by disparity magnitude (highest first)
        sorted_disparities = sorted(
            disparities_only,
            key=lambda x: x['disparity_magnitude'] * x['measure_weight'],
            reverse=True
        )
        
        # Generate interventions
        interventions = []
        
        for disp in sorted_disparities[:top_n]:
            intervention = {
                'priority_rank': len(interventions) + 1,
                'measure': disp['measure'],
                'stratification': disp['stratification_var'],
                'target_group': disp['lowest_performing_group'],
                'current_rate': disp['lowest_compliance_rate'],
                'goal_rate': disp['highest_compliance_rate'],
                'gap_to_close': disp['disparity_magnitude'],
                'disparity_category': disp['disparity_category'],
                'measure_weight': disp['measure_weight'],
                'recommended_actions': self._recommend_actions(disp),
            }
            interventions.append(intervention)
        
        return interventions
    
    def _recommend_actions(self, disparity_info: Dict) -> List[str]:
        """
        Recommend specific actions based on disparity characteristics.
        
        Args:
            disparity_info: Disparity information
            
        Returns:
            List of recommended actions
        """
        actions = []
        
        strat_var = disparity_info['stratification_var']
        target_group = disparity_info['lowest_performing_group']
        
        # Language-based recommendations
        if strat_var == 'language_std' and target_group != 'ENGLISH':
            actions.append(f"Develop {target_group} language materials for {disparity_info['measure']}")
            actions.append(f"Hire {target_group}-speaking care managers")
            actions.append("Provide interpreter services for appointments")
        
        # Race/ethnicity-based recommendations
        elif strat_var == 'race_ethnicity_std':
            actions.append(f"Conduct cultural competency training for {target_group} population")
            actions.append(f"Partner with {target_group} community organizations")
            actions.append("Analyze provider network adequacy for this population")
            actions.append("Review barriers to care specific to this group")
        
        # SDOH-based recommendations
        elif 'sdoh' in strat_var.lower():
            actions.append("Provide transportation assistance")
            actions.append("Offer telehealth options")
            actions.append("Connect members to social services")
            actions.append("Waive cost-sharing for preventive services")
        
        # General recommendations
        actions.append(f"Target outreach to {target_group} members with gaps")
        actions.append(f"Monitor progress monthly for {disparity_info['measure']}")
        
        return actions


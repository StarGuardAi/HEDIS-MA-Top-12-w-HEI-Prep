"""
Integration Tests for 9-Measure Portfolio System

Tests the complete portfolio integration including:
- Tier 1: 5 diabetes measures
- Tier 2: 4 cardiovascular measures
- Cross-tier optimization
- Portfolio-level metrics

Author: Analytics Team
Date: October 23, 2025
"""

import unittest
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import sys
import os

# Add src to path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from src.utils.portfolio_calculator import PortfolioCalculator


class Test9MeasurePortfolio(unittest.TestCase):
    """Test suite for integrated 9-measure portfolio system"""
    
    def setUp(self):
        """Set up test data and portfolio calculator"""
        self.calculator = PortfolioCalculator(measurement_year=2025)
        
        # Create synthetic member data (10 members)
        self.members = pd.DataFrame({
            'DESYNPUF_ID': [f'M{i:04d}' for i in range(1, 11)],
            'age': [45, 52, 68, 55, 72, 48, 61, 59, 66, 50],
            'gender': ['M', 'F', 'M', 'F', 'M', 'F', 'M', 'F', 'M', 'F'],
            'has_diabetes': [1, 1, 1, 1, 1, 0, 1, 0, 1, 0],
            'has_htn': [1, 1, 1, 0, 1, 1, 1, 1, 1, 0],
            'has_ascvd': [0, 1, 1, 0, 1, 0, 0, 0, 1, 0]
        })
    
    def test_portfolio_calculator_initialization(self):
        """Test portfolio calculator initializes with all 9 measures"""
        # Check Tier 1 measures
        self.assertEqual(len(self.calculator.TIER_1_MEASURES), 5)
        self.assertIn('GSD', self.calculator.TIER_1_MEASURES)
        self.assertIn('KED', self.calculator.TIER_1_MEASURES)
        self.assertIn('EED', self.calculator.TIER_1_MEASURES)
        self.assertIn('PDC-DR', self.calculator.TIER_1_MEASURES)
        self.assertIn('BPD', self.calculator.TIER_1_MEASURES)
        
        # Check Tier 2 measures
        self.assertEqual(len(self.calculator.TIER_2_MEASURES), 4)
        self.assertIn('CBP', self.calculator.TIER_2_MEASURES)
        self.assertIn('SUPD', self.calculator.TIER_2_MEASURES)
        self.assertIn('PDC-RASA', self.calculator.TIER_2_MEASURES)
        self.assertIn('PDC-STA', self.calculator.TIER_2_MEASURES)
        
        # Check total measures
        total_measures = len(self.calculator.MEASURE_WEIGHTS)
        self.assertEqual(total_measures, 9)
    
    def test_triple_weighted_measures(self):
        """Test triple-weighted measures are correctly identified"""
        triple_weighted = self.calculator.TRIPLE_WEIGHTED_MEASURES
        
        self.assertEqual(len(triple_weighted), 3)
        self.assertIn('GSD', triple_weighted)
        self.assertIn('KED', triple_weighted)
        self.assertIn('CBP', triple_weighted)
        
        # Verify weights
        self.assertEqual(self.calculator.MEASURE_WEIGHTS['GSD'], 3.0)
        self.assertEqual(self.calculator.MEASURE_WEIGHTS['KED'], 3.0)
        self.assertEqual(self.calculator.MEASURE_WEIGHTS['CBP'], 3.0)
    
    def test_measure_values_configured(self):
        """Test all 9 measures have value ranges configured"""
        all_measures = ['GSD', 'KED', 'EED', 'PDC-DR', 'BPD', 
                       'CBP', 'SUPD', 'PDC-RASA', 'PDC-STA']
        
        for measure in all_measures:
            self.assertIn(measure, self.calculator.MEASURE_VALUES)
            value_min, value_max = self.calculator.MEASURE_VALUES[measure]
            self.assertGreater(value_min, 0)
            self.assertGreater(value_max, value_min)
    
    def test_tier_1_portfolio_value(self):
        """Test Tier 1 total value is within expected range ($1.2M-$1.4M)"""
        tier1_min = sum(
            self.calculator.MEASURE_VALUES[m][0] 
            for m in self.calculator.TIER_1_MEASURES
        )
        tier1_max = sum(
            self.calculator.MEASURE_VALUES[m][1] 
            for m in self.calculator.TIER_1_MEASURES
        )
        
        # Expected: $1.2M-$1.4M (with some tolerance)
        self.assertGreater(tier1_min, 1_100_000)  # > $1.1M
        self.assertLess(tier1_min, 1_300_000)     # < $1.3M
        self.assertGreater(tier1_max, 1_300_000)  # > $1.3M
        self.assertLess(tier1_max, 1_500_000)     # < $1.5M
    
    def test_tier_2_portfolio_value(self):
        """Test Tier 2 total value is within expected range ($620K-$930K)"""
        tier2_min = sum(
            self.calculator.MEASURE_VALUES[m][0] 
            for m in self.calculator.TIER_2_MEASURES
        )
        tier2_max = sum(
            self.calculator.MEASURE_VALUES[m][1] 
            for m in self.calculator.TIER_2_MEASURES
        )
        
        # Expected: $620K-$930K
        self.assertGreater(tier2_min, 550_000)   # > $550K
        self.assertLess(tier2_min, 700_000)      # < $700K
        self.assertGreater(tier2_max, 850_000)   # > $850K
        self.assertLess(tier2_max, 1_000_000)    # < $1M
    
    def test_combined_portfolio_value(self):
        """Test combined portfolio value is $1.82M-$2.33M"""
        all_measures = list(self.calculator.MEASURE_WEIGHTS.keys())
        
        total_min = sum(
            self.calculator.MEASURE_VALUES[m][0] 
            for m in all_measures
        )
        total_max = sum(
            self.calculator.MEASURE_VALUES[m][1] 
            for m in all_measures
        )
        
        # Expected: $1.82M-$2.33M
        self.assertGreater(total_min, 1_700_000)  # > $1.7M
        self.assertLess(total_min, 1_900_000)     # < $1.9M
        self.assertGreater(total_max, 2_200_000)  # > $2.2M
        self.assertLess(total_max, 2_400_000)     # < $2.4M
    
    def test_load_measure_predictions_tier1(self):
        """Test loading Tier 1 measure predictions"""
        # Create synthetic Tier 1 results
        tier1_results = {}
        for measure in ['GSD', 'KED', 'EED', 'PDC-DR', 'BPD']:
            tier1_results[measure] = self.members.copy()
            tier1_results[measure][f'{measure}_in_denominator'] = 1
            tier1_results[measure][f'{measure}_in_numerator'] = np.random.choice([0, 1], size=len(self.members))
            tier1_results[measure][f'{measure}_gap'] = 1 - tier1_results[measure][f'{measure}_in_numerator']
        
        # Load into portfolio calculator
        combined = self.calculator.load_measure_predictions(tier1_results)
        
        # Verify structure
        self.assertIsInstance(combined, pd.DataFrame)
        self.assertEqual(len(combined), len(self.members))
        self.assertIn('member_id', combined.columns)
    
    def test_load_measure_predictions_all_9(self):
        """Test loading all 9 measure predictions"""
        # Create synthetic results for all 9 measures
        all_results = {}
        all_measures = ['GSD', 'KED', 'EED', 'PDC-DR', 'BPD',
                       'CBP', 'SUPD', 'PDC-RASA', 'PDC-STA']
        
        for measure in all_measures:
            all_results[measure] = self.members.copy()
            all_results[measure][f'{measure}_in_denominator'] = 1
            all_results[measure][f'{measure}_in_numerator'] = np.random.choice([0, 1], size=len(self.members))
            all_results[measure][f'{measure}_gap'] = 1 - all_results[measure][f'{measure}_in_numerator']
        
        # Load into portfolio calculator
        combined = self.calculator.load_measure_predictions(all_results)
        
        # Verify all measures included
        for measure in all_measures:
            self.assertIn(f'{measure}_in_denominator', combined.columns)
            self.assertIn(f'{measure}_in_numerator', combined.columns)
            self.assertIn(f'{measure}_gap', combined.columns)
    
    def test_calculate_gaps_9_measures(self):
        """Test gap calculation across all 9 measures"""
        # Create synthetic combined data
        combined = self.members.copy()
        combined['member_id'] = combined['DESYNPUF_ID']
        
        # Add measure results (mix of compliant and gaps)
        all_measures = ['GSD', 'KED', 'EED', 'PDC-DR', 'BPD',
                       'CBP', 'SUPD', 'PDC-RASA', 'PDC-STA']
        
        for measure in all_measures:
            combined[f'{measure}_in_denominator'] = 1
            combined[f'{measure}_in_numerator'] = np.random.choice([0, 1], size=len(combined), p=[0.3, 0.7])
            combined[f'{measure}_gap'] = 1 - combined[f'{measure}_in_numerator']
        
        # Calculate gaps
        gap_df = self.calculator.calculate_gaps(combined, all_measures)
        
        # Verify gap summary columns exist
        self.assertIn('total_denominators', gap_df.columns)
        self.assertIn('total_numerators', gap_df.columns)
        self.assertIn('total_gaps', gap_df.columns)
        self.assertIn('gap_rate', gap_df.columns)
        
        # Verify multi-measure gap flags
        self.assertIn('has_any_gap', gap_df.columns)
        self.assertIn('has_multiple_gaps', gap_df.columns)
        self.assertIn('has_3plus_gaps', gap_df.columns)
        
        # Verify triple-weighted gaps tracked
        self.assertIn('triple_weighted_gaps', gap_df.columns)
    
    def test_triple_weighted_gap_priority(self):
        """Test triple-weighted measures are prioritized"""
        # Create member with only triple-weighted gaps
        combined = pd.DataFrame({
            'member_id': ['M0001'],
            'age': [55],
            # Triple-weighted gaps (GSD, KED, CBP)
            'GSD_in_denominator': [1], 'GSD_in_numerator': [0], 'GSD_gap': [1],
            'KED_in_denominator': [1], 'KED_in_numerator': [0], 'KED_gap': [1],
            'CBP_in_denominator': [1], 'CBP_in_numerator': [0], 'CBP_gap': [1],
            # Standard measures - compliant
            'EED_in_denominator': [1], 'EED_in_numerator': [1], 'EED_gap': [0],
            'PDC-DR_in_denominator': [1], 'PDC-DR_in_numerator': [1], 'PDC-DR_gap': [0],
            'BPD_in_denominator': [1], 'BPD_in_numerator': [1], 'BPD_gap': [0],
            'SUPD_in_denominator': [1], 'SUPD_in_numerator': [1], 'SUPD_gap': [0],
            'PDC-RASA_in_denominator': [1], 'PDC-RASA_in_numerator': [1], 'PDC-RASA_gap': [0],
            'PDC-STA_in_denominator': [1], 'PDC-STA_in_numerator': [1], 'PDC-STA_gap': [0],
        })
        
        all_measures = ['GSD', 'KED', 'EED', 'PDC-DR', 'BPD',
                       'CBP', 'SUPD', 'PDC-RASA', 'PDC-STA']
        
        gap_df = self.calculator.calculate_gaps(combined, all_measures)
        
        # Should have 3 triple-weighted gaps
        self.assertEqual(gap_df['triple_weighted_gaps'].iloc[0], 3)
        
        # Should have 3 total gaps
        self.assertEqual(gap_df['total_gaps'].iloc[0], 3)
    
    def test_cross_tier_member_overlap(self):
        """Test identifying members with HTN + Diabetes (cross-tier overlap)"""
        # Members with both conditions apply to both Tier 1 and Tier 2 measures
        overlap_members = self.members[
            (self.members['has_diabetes'] == 1) & 
            (self.members['has_htn'] == 1)
        ]
        
        # Should have overlap members
        self.assertGreater(len(overlap_members), 0)
        
        # These members are eligible for 8-9 measures
        # Tier 1: GSD, KED, EED, PDC-DR, BPD (all 5)
        # Tier 2: CBP, SUPD, PDC-RASA (3 of 4, SUPD requires diabetes)
    
    def test_star_rating_calculation_9_measures(self):
        """Test Star Rating calculation with all 9 measures"""
        # Create synthetic measure summaries
        measure_summaries = {}
        all_measures = ['GSD', 'KED', 'EED', 'PDC-DR', 'BPD',
                       'CBP', 'SUPD', 'PDC-RASA', 'PDC-STA']
        
        for measure in all_measures:
            measure_summaries[measure] = {
                'compliance_rate': 75.0,  # 75% compliant
                'eligible_population': 1000,
                'compliant': 750,
                'gaps': 250
            }
        
        # Calculate Star Rating
        star_impact = self.calculator.calculate_star_rating_impact(
            measure_summaries,
            all_measures
        )
        
        # Verify output structure
        self.assertIn('current_weighted_rate', star_impact)
        self.assertIn('current_stars', star_impact)
        self.assertIn('with_50pct_closure', star_impact)
        self.assertIn('with_100pct_closure', star_impact)
        
        # With 75% compliance, should be around 3-4 stars
        self.assertGreaterEqual(star_impact['current_stars'], 3.0)
        self.assertLessEqual(star_impact['current_stars'], 4.0)
    
    def test_portfolio_value_calculation_9_measures(self):
        """Test portfolio value calculation with all 9 measures"""
        # Create synthetic measure summaries
        measure_summaries = {}
        all_measures = ['GSD', 'KED', 'EED', 'PDC-DR', 'BPD',
                       'CBP', 'SUPD', 'PDC-RASA', 'PDC-STA']
        
        for measure in all_measures:
            measure_summaries[measure] = {
                'compliance_rate': 70.0,  # 70% compliant
                'eligible_population': 1000,
                'compliant': 700,
                'gaps': 300
            }
        
        # Calculate portfolio value
        portfolio_value = self.calculator.calculate_portfolio_value(
            measure_summaries,
            all_measures
        )
        
        # Verify output structure
        self.assertIn('total_portfolio_value', portfolio_value)
        self.assertIn('current_value', portfolio_value)
        self.assertIn('opportunity_value', portfolio_value)
        self.assertIn('measure_breakdown', portfolio_value)
        
        # Should have breakdown for all 9 measures
        self.assertEqual(len(portfolio_value['measure_breakdown']), 9)
    
    def test_member_segmentation_9_measures(self):
        """Test member segmentation across 9 measures"""
        # Create synthetic data with varied gap patterns
        combined = pd.DataFrame({
            'member_id': ['M0001', 'M0002', 'M0003', 'M0004'],
            'age': [55, 62, 48, 71],
            'total_denominators': [9, 8, 7, 9],
            'total_numerators': [9, 6, 4, 2],
            'total_gaps': [0, 2, 3, 7],
            'has_any_gap': [False, True, True, True],
            'has_multiple_gaps': [False, True, True, True],
            'has_3plus_gaps': [False, False, True, True],
            'triple_weighted_gaps': [0, 1, 2, 3],
        })
        
        all_measures = ['GSD', 'KED', 'EED', 'PDC-DR', 'BPD',
                       'CBP', 'SUPD', 'PDC-RASA', 'PDC-STA']
        
        segments = self.calculator.segment_members(combined, all_measures)
        
        # Verify segments exist
        self.assertIn('no_gaps', segments)
        self.assertIn('single_gap', segments)
        self.assertIn('multiple_gaps', segments)
        self.assertIn('high_gap', segments)
        
        # Verify segmentation is correct
        self.assertEqual(len(segments['no_gaps']), 1)  # M0001
        self.assertEqual(len(segments['multiple_gaps']), 2)  # M0002, M0003
        self.assertEqual(len(segments['high_gap']), 1)  # M0004
    
    def test_new_2025_measures_identified(self):
        """Test NEW 2025 measures are properly identified"""
        new_2025 = self.calculator.NEW_2025_MEASURES
        
        self.assertEqual(len(new_2025), 2)
        self.assertIn('KED', new_2025)
        self.assertIn('BPD', new_2025)
    
    def test_tier_assignment_correctness(self):
        """Test measures are correctly assigned to tiers"""
        # No overlap between tiers
        overlap = self.calculator.TIER_1_MEASURES.intersection(
            self.calculator.TIER_2_MEASURES
        )
        self.assertEqual(len(overlap), 0)
        
        # All measures accounted for
        all_tier_measures = self.calculator.TIER_1_MEASURES.union(
            self.calculator.TIER_2_MEASURES
        )
        self.assertEqual(len(all_tier_measures), 9)
    
    def test_portfolio_summary_generation(self):
        """Test complete portfolio summary can be generated"""
        # Create comprehensive test data
        combined = self.members.copy()
        combined['member_id'] = combined['DESYNPUF_ID']
        
        all_measures = ['GSD', 'KED', 'EED', 'PDC-DR', 'BPD',
                       'CBP', 'SUPD', 'PDC-RASA', 'PDC-STA']
        
        # Add all measure results
        for measure in all_measures:
            combined[f'{measure}_in_denominator'] = 1
            combined[f'{measure}_in_numerator'] = np.random.choice([0, 1], size=len(combined), p=[0.3, 0.7])
            combined[f'{measure}_gap'] = 1 - combined[f'{measure}_in_numerator']
        
        # Generate all portfolio metrics
        gap_df = self.calculator.calculate_gaps(combined, all_measures)
        
        # Create measure summaries
        measure_summaries = {}
        for measure in all_measures:
            measure_summaries[measure] = {
                'compliance_rate': 70.0,
                'eligible_population': len(combined),
                'compliant': int(len(combined) * 0.7),
                'gaps': int(len(combined) * 0.3)
            }
        
        star_impact = self.calculator.calculate_star_rating_impact(
            measure_summaries, all_measures
        )
        portfolio_value = self.calculator.calculate_portfolio_value(
            measure_summaries, all_measures
        )
        
        # Verify all components generated successfully
        self.assertIsNotNone(gap_df)
        self.assertIsNotNone(star_impact)
        self.assertIsNotNone(portfolio_value)
    
    def test_performance_with_large_population(self):
        """Test system performance with larger population"""
        # Create 1000 member dataset
        large_members = pd.DataFrame({
            'DESYNPUF_ID': [f'M{i:06d}' for i in range(1000)],
            'age': np.random.randint(40, 85, 1000),
        })
        
        # Add measure results
        combined = large_members.copy()
        combined['member_id'] = combined['DESYNPUF_ID']
        
        all_measures = ['GSD', 'KED', 'EED', 'PDC-DR', 'BPD',
                       'CBP', 'SUPD', 'PDC-RASA', 'PDC-STA']
        
        for measure in all_measures:
            combined[f'{measure}_in_denominator'] = 1
            combined[f'{measure}_in_numerator'] = np.random.choice([0, 1], size=len(combined))
            combined[f'{measure}_gap'] = 1 - combined[f'{measure}_in_numerator']
        
        # Should complete without errors
        gap_df = self.calculator.calculate_gaps(combined, all_measures)
        
        self.assertEqual(len(gap_df), 1000)


if __name__ == '__main__':
    unittest.main()


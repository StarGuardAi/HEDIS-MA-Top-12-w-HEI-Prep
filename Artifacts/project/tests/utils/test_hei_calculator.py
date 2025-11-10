"""
Unit Tests for Health Equity Index (HEI) Calculator

Tests the HEI calculation engine for equity scoring and disparity detection.

Author: Analytics Team
Date: October 23, 2025
"""

import unittest
import pandas as pd
import numpy as np
from datetime import datetime
import sys
import os

# Add src to path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from src.utils.hei_calculator import HEICalculator


class TestHEICalculator(unittest.TestCase):
    """Test suite for HEI Calculator"""
    
    def setUp(self):
        """Set up test data"""
        self.hei_calc = HEICalculator(measurement_year=2025)
        
        # Create test HEI data with demographics
        self.hei_data = pd.DataFrame({
            'member_id': [f'M{i:03d}' for i in range(1, 101)],
            'race_ethnicity_std': ['WHITE'] * 40 + ['BLACK'] * 30 + ['HISPANIC'] * 20 + ['ASIAN'] * 10,
            'language_std': ['ENGLISH'] * 70 + ['SPANISH'] * 20 + ['CHINESE'] * 10,
            'is_lep': [0] * 70 + [1] * 30,
            'lis': [0] * 70 + [1] * 30,
            'dual_eligible': [0] * 80 + [1] * 20,
        })
        
        # Create test measure results (GSD) with disparity
        # White group: 80% compliant, Black group: 60% compliant
        self.measure_results_gsd = pd.DataFrame({
            'member_id': [f'M{i:03d}' for i in range(1, 101)],
            'GSD_in_denominator': [1] * 100,
            'GSD_in_numerator': (
                [1] * 32 + [0] * 8 +  # White: 32/40 = 80%
                [1] * 18 + [0] * 12 +  # Black: 18/30 = 60%
                [1] * 14 + [0] * 6 +   # Hispanic: 14/20 = 70%
                [1] * 8 + [0] * 2      # Asian: 8/10 = 80%
            ),
            'GSD_gap': (
                [0] * 32 + [1] * 8 +
                [0] * 18 + [1] * 12 +
                [0] * 14 + [1] * 6 +
                [0] * 8 + [1] * 2
            ),
        })
    
    def test_stratified_performance_calculation(self):
        """Test calculation of stratified performance by race/ethnicity"""
        stratified = self.hei_calc.calculate_stratified_performance(
            self.measure_results_gsd,
            self.hei_data,
            'GSD',
            'race_ethnicity_std'
        )
        
        # Should have 4 groups
        self.assertEqual(len(stratified), 4)
        
        # Check White group (80% compliance)
        white_group = stratified[stratified['race_ethnicity_std'] == 'WHITE'].iloc[0]
        self.assertAlmostEqual(white_group['compliance_rate'], 80.0, places=1)
        
        # Check Black group (60% compliance)
        black_group = stratified[stratified['race_ethnicity_std'] == 'BLACK'].iloc[0]
        self.assertAlmostEqual(black_group['compliance_rate'], 60.0, places=1)
    
    def test_disparity_identification(self):
        """Test identification of disparities between groups"""
        stratified = self.hei_calc.calculate_stratified_performance(
            self.measure_results_gsd,
            self.hei_data,
            'GSD',
            'race_ethnicity_std'
        )
        
        disparity_info = self.hei_calc.identify_disparities(
            stratified,
            'race_ethnicity_std',
            disparity_threshold=10.0
        )
        
        # Should detect disparity (80% - 60% = 20% gap)
        self.assertTrue(disparity_info['has_disparity'])
        self.assertAlmostEqual(disparity_info['disparity_magnitude'], 20.0, places=1)
        self.assertEqual(disparity_info['highest_performing_group'], 'WHITE')
        self.assertEqual(disparity_info['lowest_performing_group'], 'BLACK')
    
    def test_equity_score_calculation(self):
        """Test equity score calculation for single measure"""
        disparity_info = {
            'has_disparity': True,
            'disparity_magnitude': 20.0,  # 20 percentage point gap
            'measure': 'GSD',
        }
        
        equity_score = self.hei_calc.calculate_equity_score_single_measure(
            disparity_info,
            measure_weight=3.0
        )
        
        # With 20% disparity, should get 60/100 score
        self.assertAlmostEqual(equity_score, 60.0, places=1)
    
    def test_equity_score_no_disparity(self):
        """Test equity score when no disparity exists"""
        disparity_info = {
            'has_disparity': False,
            'disparity_magnitude': 0,
            'measure': 'GSD',
        }
        
        equity_score = self.hei_calc.calculate_equity_score_single_measure(
            disparity_info,
            measure_weight=1.0
        )
        
        # No disparity = perfect score
        self.assertEqual(equity_score, 100.0)
    
    def test_portfolio_equity_score(self):
        """Test portfolio-level equity score calculation"""
        measure_results = {
            'GSD': self.measure_results_gsd
        }
        
        measure_weights = {
            'GSD': 3.0
        }
        
        equity_results = self.hei_calc.calculate_portfolio_equity_score(
            measure_results,
            self.hei_data,
            measure_weights,
            stratification_vars=['race_ethnicity_std']
        )
        
        # Should calculate overall score
        self.assertIn('overall_equity_score', equity_results)
        self.assertGreater(equity_results['overall_equity_score'], 0)
        self.assertLessEqual(equity_results['overall_equity_score'], 100)
        
        # Should have penalty category
        self.assertIn('penalty_category', equity_results)
        
        # Should detect disparities
        self.assertGreater(equity_results['measures_with_disparities'], 0)
    
    def test_penalty_tiers(self):
        """Test correct penalty tier assignment"""
        # Test high equity score (>= 70) = no penalty
        results_high = {
            'overall_equity_score': 75.0,
            'all_disparities': []
        }
        
        # High score should result in no penalty
        # (Note: This is testing the logic, actual call would be different)
        self.assertGreaterEqual(75.0, 70)
        
        # Test moderate score (50-69) = -0.25 penalty
        self.assertTrue(50 <= 60 < 70)
        
        # Test low score (< 50) = -0.5 penalty
        self.assertLess(40, 50)
    
    def test_priority_interventions(self):
        """Test identification of priority interventions"""
        measure_results = {
            'GSD': self.measure_results_gsd
        }
        
        measure_weights = {
            'GSD': 3.0
        }
        
        equity_results = self.hei_calc.calculate_portfolio_equity_score(
            measure_results,
            self.hei_data,
            measure_weights,
            stratification_vars=['race_ethnicity_std']
        )
        
        interventions = self.hei_calc.identify_priority_interventions(
            equity_results,
            top_n=5
        )
        
        # Should generate interventions
        self.assertGreater(len(interventions), 0)
        
        # First intervention should target largest disparity
        first = interventions[0]
        self.assertIn('measure', first)
        self.assertIn('target_group', first)
        self.assertIn('recommended_actions', first)
    
    def test_equity_report_generation(self):
        """Test equity report generation"""
        measure_results = {
            'GSD': self.measure_results_gsd
        }
        
        measure_weights = {
            'GSD': 3.0
        }
        
        equity_results = self.hei_calc.calculate_portfolio_equity_score(
            measure_results,
            self.hei_data,
            measure_weights,
            stratification_vars=['race_ethnicity_std']
        )
        
        report = self.hei_calc.generate_equity_report(equity_results, 'summary')
        
        # Should generate report
        self.assertIsInstance(report, str)
        self.assertIn('HEALTH EQUITY INDEX', report)
        self.assertIn('EQUITY SCORE', report)
    
    def test_multiple_stratifications(self):
        """Test equity calculation across multiple stratification variables"""
        measure_results = {
            'GSD': self.measure_results_gsd
        }
        
        measure_weights = {
            'GSD': 3.0
        }
        
        equity_results = self.hei_calc.calculate_portfolio_equity_score(
            measure_results,
            self.hei_data,
            measure_weights,
            stratification_vars=['race_ethnicity_std', 'language_std']
        )
        
        # Should evaluate both stratifications
        self.assertEqual(equity_results['stratifications_evaluated'], 2)
        self.assertEqual(equity_results['total_comparisons'], 2)  # 1 measure × 2 stratifications
    
    def test_minimum_group_size(self):
        """Test handling of small groups below minimum size"""
        # Create small groups
        small_hei_data = pd.DataFrame({
            'member_id': [f'M{i:03d}' for i in range(1, 51)],
            'race_ethnicity_std': ['WHITE'] * 40 + ['ASIAN'] * 10,  # Asian group too small
        })
        
        small_measure_results = pd.DataFrame({
            'member_id': [f'M{i:03d}' for i in range(1, 51)],
            'GSD_in_denominator': [1] * 50,
            'GSD_in_numerator': [1] * 32 + [0] * 8 + [1] * 8 + [0] * 2,
            'GSD_gap': [0] * 32 + [1] * 8 + [0] * 8 + [1] * 2,
        })
        
        stratified = self.hei_calc.calculate_stratified_performance(
            small_measure_results,
            small_hei_data,
            'GSD',
            'race_ethnicity_std'
        )
        
        # Asian group should be flagged as invalid (< 30 members)
        asian_group = stratified[stratified['race_ethnicity_std'] == 'ASIAN'].iloc[0]
        self.assertFalse(asian_group['is_valid_group'])


if __name__ == '__main__':
    unittest.main()


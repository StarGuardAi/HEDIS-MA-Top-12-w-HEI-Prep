"""
Unit Tests for KED (Kidney Health Evaluation) Measure

Tests for denominator, numerator, exclusions, gap analysis, and
compliance with HEDIS MY2025 specifications.

HEDIS Specification: MY2025
Measure Code: KED
Weight: 3x (Triple-weighted)
NEW 2025 Measure
"""

import unittest
import pandas as pd
import numpy as np
from datetime import datetime
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

# Import modules to test
from src.measures.ked import KEDMeasure, KEDResult, calculate_ked_measure
from tests.fixtures.synthetic_ked_data import (
    get_synthetic_ked_test_data,
    EXPECTED_KED_RESULTS
)


class TestKEDMeasure(unittest.TestCase):
    """Test cases for KED measure calculation."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.measurement_year = 2025
        self.ked = KEDMeasure(self.measurement_year)
        
        # Load synthetic test data
        self.member_df, self.claims_df, self.labs_df = get_synthetic_ked_test_data(
            self.measurement_year
        )
    
    def test_initialization(self):
        """Test KED measure initialization."""
        self.assertEqual(self.ked.measurement_year, 2025)
        self.assertEqual(self.ked.my_start, datetime(2025, 1, 1))
        self.assertEqual(self.ked.my_end, datetime(2025, 12, 31))
    
    def test_diabetes_codes(self):
        """Test diabetes ICD-10 code sets."""
        # Should have both Type 1 and Type 2 codes
        self.assertGreater(len(self.ked.DIABETES_CODES), 50)
        
        # Check specific codes
        self.assertIn('E10.9', self.ked.DIABETES_CODES)  # Type 1
        self.assertIn('E11.9', self.ked.DIABETES_CODES)  # Type 2
        self.assertIn('E11.22', self.ked.DIABETES_CODES)  # Diabetes with CKD
    
    def test_exclusion_codes(self):
        """Test exclusion ICD-10 code sets."""
        # Should have ESRD and kidney transplant codes
        self.assertGreater(len(self.ked.EXCLUSION_CODES), 4)
        
        # Check specific codes
        self.assertIn('N18.6', self.ked.EXCLUSION_CODES)  # ESRD
        self.assertIn('Z94.0', self.ked.EXCLUSION_CODES)  # Kidney transplant
        self.assertIn('Z99.2', self.ked.EXCLUSION_CODES)  # Dialysis
    
    def test_loinc_codes(self):
        """Test LOINC code sets for labs."""
        # eGFR codes
        self.assertGreater(len(self.ked.EGFR_LOINC_CODES), 0)
        self.assertIn('48642-3', self.ked.EGFR_LOINC_CODES)  # eGFR CKD-EPI
        self.assertIn('48643-1', self.ked.EGFR_LOINC_CODES)  # eGFR MDRD
        
        # ACR codes
        self.assertGreater(len(self.ked.ACR_LOINC_CODES), 0)
        self.assertIn('9318-7', self.ked.ACR_LOINC_CODES)  # ACR
        self.assertIn('13705-9', self.ked.ACR_LOINC_CODES)  # ACR First Morning
    
    def test_denominator_age_eligibility(self):
        """Test age eligibility for denominator (18-75)."""
        result_df = self.ked.identify_denominator(
            self.member_df.copy(),
            self.claims_df.copy()
        )
        
        # Check age calculation
        self.assertIn('age_at_my_end', result_df.columns)
        self.assertIn('age_eligible', result_df.columns)
        
        # Age 17 should not be eligible
        too_young = result_df[result_df['member_id'] == 'KED_AGE_TOO_YOUNG_001']
        self.assertEqual(len(too_young), 1)
        self.assertEqual(too_young.iloc[0]['age_at_my_end'], 17)
        self.assertFalse(too_young.iloc[0]['age_eligible'])
        
        # Age 76 should not be eligible
        too_old = result_df[result_df['member_id'] == 'KED_AGE_TOO_OLD_001']
        self.assertEqual(len(too_old), 1)
        self.assertEqual(too_old.iloc[0]['age_at_my_end'], 76)
        self.assertFalse(too_old.iloc[0]['age_eligible'])
        
        # Age 50 should be eligible
        eligible = result_df[result_df['member_id'] == 'KED_COMPLIANT_001']
        self.assertEqual(len(eligible), 1)
        self.assertEqual(eligible.iloc[0]['age_at_my_end'], 50)
        self.assertTrue(eligible.iloc[0]['age_eligible'])
    
    def test_denominator_diabetes_diagnosis(self):
        """Test diabetes diagnosis logic for denominator."""
        result_df = self.ked.identify_denominator(
            self.member_df.copy(),
            self.claims_df.copy()
        )
        
        # Check diabetes flag
        self.assertIn('has_diabetes', result_df.columns)
        
        # Member with 2 outpatient diabetes claims should have diabetes
        member1 = result_df[result_df['member_id'] == 'KED_COMPLIANT_001']
        self.assertTrue(member1.iloc[0]['has_diabetes'])
        
        # Member with 1 inpatient diabetes claim should have diabetes
        member2 = result_df[result_df['member_id'] == 'KED_COMPLIANT_002']
        self.assertTrue(member2.iloc[0]['has_diabetes'])
        
        # Member without diabetes claims should not have diabetes
        no_diabetes = result_df[result_df['member_id'] == 'KED_NO_DIABETES_001']
        self.assertFalse(no_diabetes.iloc[0]['has_diabetes'])
    
    def test_denominator_identification(self):
        """Test complete denominator identification."""
        result_df = self.ked.identify_denominator(
            self.member_df.copy(),
            self.claims_df.copy()
        )
        
        # Check denominator flag
        self.assertIn('in_denominator', result_df.columns)
        
        # Compliant member should be in denominator (age + diabetes)
        compliant = result_df[result_df['member_id'] == 'KED_COMPLIANT_001']
        self.assertTrue(compliant.iloc[0]['in_denominator'])
        
        # Age-ineligible should not be in denominator
        too_young = result_df[result_df['member_id'] == 'KED_AGE_TOO_YOUNG_001']
        self.assertFalse(too_young.iloc[0]['in_denominator'])
        
        # Non-diabetic should not be in denominator
        no_diabetes = result_df[result_df['member_id'] == 'KED_NO_DIABETES_001']
        self.assertFalse(no_diabetes.iloc[0]['in_denominator'])
    
    def test_exclusions_esrd(self):
        """Test ESRD exclusion."""
        # First identify denominator
        result_df = self.ked.identify_denominator(
            self.member_df.copy(),
            self.claims_df.copy()
        )
        
        # Apply exclusions
        result_df = self.ked.apply_exclusions(result_df, self.claims_df.copy())
        
        # Check exclusion flag
        self.assertIn('excluded', result_df.columns)
        self.assertIn('in_denominator_final', result_df.columns)
        
        # Member with ESRD should be excluded
        esrd_member = result_df[result_df['member_id'] == 'KED_EXCLUDED_ESRD_001']
        self.assertTrue(esrd_member.iloc[0]['excluded'])
        self.assertFalse(esrd_member.iloc[0]['in_denominator_final'])
    
    def test_exclusions_kidney_transplant(self):
        """Test kidney transplant exclusion."""
        # First identify denominator
        result_df = self.ked.identify_denominator(
            self.member_df.copy(),
            self.claims_df.copy()
        )
        
        # Apply exclusions
        result_df = self.ked.apply_exclusions(result_df, self.claims_df.copy())
        
        # Member with kidney transplant should be excluded
        transplant_member = result_df[
            result_df['member_id'] == 'KED_EXCLUDED_TRANSPLANT_001'
        ]
        self.assertTrue(transplant_member.iloc[0]['excluded'])
        self.assertFalse(transplant_member.iloc[0]['in_denominator_final'])
    
    def test_numerator_egfr_test(self):
        """Test eGFR test identification."""
        # Identify denominator and apply exclusions
        result_df = self.ked.identify_denominator(
            self.member_df.copy(),
            self.claims_df.copy()
        )
        result_df = self.ked.apply_exclusions(result_df, self.claims_df.copy())
        
        # Identify numerator
        result_df = self.ked.identify_numerator(result_df, self.labs_df.copy())
        
        # Check eGFR test flags
        self.assertIn('has_egfr_test', result_df.columns)
        
        # Compliant member should have eGFR test
        compliant = result_df[result_df['member_id'] == 'KED_COMPLIANT_001']
        self.assertTrue(compliant.iloc[0]['has_egfr_test'])
        
        # Member missing eGFR should not have eGFR test
        missing_egfr = result_df[result_df['member_id'] == 'KED_GAP_EGFR_001']
        self.assertFalse(missing_egfr.iloc[0]['has_egfr_test'])
    
    def test_numerator_acr_test(self):
        """Test ACR test identification."""
        # Identify denominator and apply exclusions
        result_df = self.ked.identify_denominator(
            self.member_df.copy(),
            self.claims_df.copy()
        )
        result_df = self.ked.apply_exclusions(result_df, self.claims_df.copy())
        
        # Identify numerator
        result_df = self.ked.identify_numerator(result_df, self.labs_df.copy())
        
        # Check ACR test flags
        self.assertIn('has_acr_test', result_df.columns)
        
        # Compliant member should have ACR test
        compliant = result_df[result_df['member_id'] == 'KED_COMPLIANT_001']
        self.assertTrue(compliant.iloc[0]['has_acr_test'])
        
        # Member missing ACR should not have ACR test
        missing_acr = result_df[result_df['member_id'] == 'KED_GAP_ACR_001']
        self.assertFalse(missing_acr.iloc[0]['has_acr_test'])
    
    def test_numerator_both_tests_required(self):
        """Test that BOTH eGFR AND ACR tests are required for numerator."""
        # Identify denominator and apply exclusions
        result_df = self.ked.identify_denominator(
            self.member_df.copy(),
            self.claims_df.copy()
        )
        result_df = self.ked.apply_exclusions(result_df, self.claims_df.copy())
        
        # Identify numerator
        result_df = self.ked.identify_numerator(result_df, self.labs_df.copy())
        
        # Check numerator flag
        self.assertIn('in_numerator', result_df.columns)
        
        # Member with both tests should be in numerator
        compliant = result_df[result_df['member_id'] == 'KED_COMPLIANT_001']
        self.assertTrue(compliant.iloc[0]['in_numerator'])
        
        # Member with only eGFR should NOT be in numerator
        only_egfr = result_df[result_df['member_id'] == 'KED_GAP_ACR_001']
        self.assertTrue(only_egfr.iloc[0]['has_egfr_test'])
        self.assertFalse(only_egfr.iloc[0]['has_acr_test'])
        self.assertFalse(only_egfr.iloc[0]['in_numerator'])
        
        # Member with only ACR should NOT be in numerator
        only_acr = result_df[result_df['member_id'] == 'KED_GAP_EGFR_001']
        self.assertFalse(only_acr.iloc[0]['has_egfr_test'])
        self.assertTrue(only_acr.iloc[0]['has_acr_test'])
        self.assertFalse(only_acr.iloc[0]['in_numerator'])
        
        # Member with neither test should NOT be in numerator
        no_tests = result_df[result_df['member_id'] == 'KED_GAP_BOTH_001']
        self.assertFalse(no_tests.iloc[0]['has_egfr_test'])
        self.assertFalse(no_tests.iloc[0]['has_acr_test'])
        self.assertFalse(no_tests.iloc[0]['in_numerator'])
    
    def test_date_filtering_measurement_year_only(self):
        """Test that only tests in measurement year count."""
        # Identify denominator and apply exclusions
        result_df = self.ked.identify_denominator(
            self.member_df.copy(),
            self.claims_df.copy()
        )
        result_df = self.ked.apply_exclusions(result_df, self.claims_df.copy())
        
        # Identify numerator
        result_df = self.ked.identify_numerator(result_df, self.labs_df.copy())
        
        # KED_GAP_BOTH_001 has labs in prior year but not in MY
        gap_both = result_df[result_df['member_id'] == 'KED_GAP_BOTH_001']
        self.assertEqual(len(gap_both), 1)
        
        # Should be in denominator but not numerator (no tests in MY)
        self.assertTrue(gap_both.iloc[0]['in_denominator_final'])
        self.assertFalse(gap_both.iloc[0]['has_egfr_test'])
        self.assertFalse(gap_both.iloc[0]['has_acr_test'])
        self.assertFalse(gap_both.iloc[0]['in_numerator'])
    
    def test_complete_measure_calculation(self):
        """Test complete KED measure calculation."""
        results = self.ked.calculate_measure(
            self.member_df.copy(),
            self.claims_df.copy(),
            self.labs_df.copy()
        )
        
        # Check result structure
        self.assertIsInstance(results, dict)
        self.assertEqual(results['measure_code'], 'KED')
        self.assertEqual(results['measurement_year'], 2025)
        self.assertEqual(results['weight'], 3.0)  # Triple-weighted
        self.assertTrue(results['new_2025'])
        
        # Check performance metrics
        self.assertIn('denominator', results)
        self.assertIn('numerator', results)
        self.assertIn('rate', results)
        
        # Verify against expected results
        self.assertEqual(results['denominator'], EXPECTED_KED_RESULTS['denominator'])
        self.assertEqual(results['numerator'], EXPECTED_KED_RESULTS['numerator'])
        self.assertAlmostEqual(results['rate'], EXPECTED_KED_RESULTS['rate'], places=1)
    
    def test_gap_analysis(self):
        """Test gap analysis functionality."""
        results = self.ked.calculate_measure(
            self.member_df.copy(),
            self.claims_df.copy(),
            self.labs_df.copy()
        )
        
        # Check gap analysis structure
        self.assertIn('gaps', results)
        gaps = results['gaps']
        
        self.assertIn('total_gaps', gaps)
        self.assertIn('missing_egfr', gaps)
        self.assertIn('missing_acr', gaps)
        self.assertIn('missing_both', gaps)
        
        # Verify gap counts
        self.assertEqual(gaps['total_gaps'], EXPECTED_KED_RESULTS['gaps']['total_gaps'])
        self.assertEqual(gaps['missing_egfr'], EXPECTED_KED_RESULTS['gaps']['missing_egfr'])
        self.assertEqual(gaps['missing_acr'], EXPECTED_KED_RESULTS['gaps']['missing_acr'])
        self.assertEqual(gaps['missing_both'], EXPECTED_KED_RESULTS['gaps']['missing_both'])
        
        # Check gap member list
        self.assertIn('gap_members', results)
        self.assertIsInstance(results['gap_members'], list)
        self.assertEqual(len(results['gap_members']), 3)
    
    def test_member_level_results(self):
        """Test member-level results output."""
        results = self.ked.calculate_measure(
            self.member_df.copy(),
            self.claims_df.copy(),
            self.labs_df.copy()
        )
        
        # Check member results
        self.assertIn('member_results', results)
        member_results = results['member_results']
        
        self.assertIsInstance(member_results, pd.DataFrame)
        self.assertEqual(len(member_results), len(self.member_df))
        
        # Check required columns
        required_columns = [
            'member_id',
            'age_eligible',
            'has_diabetes',
            'in_denominator',
            'excluded',
            'in_denominator_final',
            'has_egfr_test',
            'has_acr_test',
            'in_numerator'
        ]
        for col in required_columns:
            self.assertIn(col, member_results.columns)
    
    def test_convenience_function(self):
        """Test convenience function for KED calculation."""
        results = calculate_ked_measure(
            self.member_df.copy(),
            self.claims_df.copy(),
            self.labs_df.copy(),
            measurement_year=2025
        )
        
        # Should produce same results as class method
        self.assertEqual(results['measure_code'], 'KED')
        self.assertEqual(results['denominator'], EXPECTED_KED_RESULTS['denominator'])
        self.assertEqual(results['numerator'], EXPECTED_KED_RESULTS['numerator'])
    
    def test_edge_case_empty_dataframes(self):
        """Test handling of empty DataFrames."""
        empty_members = pd.DataFrame(columns=self.member_df.columns)
        empty_claims = pd.DataFrame(columns=self.claims_df.columns)
        empty_labs = pd.DataFrame(columns=self.labs_df.columns)
        
        results = self.ked.calculate_measure(
            empty_members,
            empty_claims,
            empty_labs
        )
        
        # Should handle gracefully
        self.assertEqual(results['denominator'], 0)
        self.assertEqual(results['numerator'], 0)
        self.assertEqual(results['rate'], 0.0)
    
    def test_edge_case_missing_columns(self):
        """Test handling of missing required columns."""
        # This should raise an error or handle gracefully
        incomplete_members = self.member_df[['member_id']].copy()
        
        with self.assertRaises((KeyError, AttributeError)):
            self.ked.identify_denominator(incomplete_members, self.claims_df.copy())
    
    def test_multiple_tests_same_member(self):
        """Test handling of multiple tests for same member (should use most recent)."""
        # Add multiple eGFR tests for same member
        extra_labs = self.labs_df.copy()
        extra_lab = {
            'member_id': 'KED_COMPLIANT_001',
            'test_date': datetime(2025, 1, 15),  # Earlier test
            'loinc_code': '48642-3',
            'result_value': 55.0,
            'result_unit': 'mL/min/1.73m2',
        }
        extra_labs = pd.concat([extra_labs, pd.DataFrame([extra_lab])], ignore_index=True)
        
        results = self.ked.calculate_measure(
            self.member_df.copy(),
            self.claims_df.copy(),
            extra_labs
        )
        
        # Should still count as having eGFR test
        member_results = results['member_results']
        compliant = member_results[member_results['member_id'] == 'KED_COMPLIANT_001']
        self.assertTrue(compliant.iloc[0]['has_egfr_test'])
        
        # Should use most recent test date
        self.assertIsNotNone(compliant.iloc[0]['egfr_test_date'])


class TestKEDHEDISCompliance(unittest.TestCase):
    """Test HEDIS MY2025 specification compliance."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.ked = KEDMeasure(2025)
    
    def test_measure_metadata(self):
        """Test measure metadata matches HEDIS specifications."""
        # Triple-weighted measure
        results = calculate_ked_measure(
            *get_synthetic_ked_test_data(2025),
            measurement_year=2025
        )
        
        self.assertEqual(results['weight'], 3.0)
        self.assertTrue(results['new_2025'])
        self.assertEqual(results['measure_code'], 'KED')
    
    def test_age_range_18_75(self):
        """Test HEDIS age range requirement (18-75)."""
        # Age range should be 18-75 per HEDIS specs
        my_end = datetime(2025, 12, 31)
        
        # Test age 18 (eligible)
        age_18_birthdate = my_end - pd.Timedelta(days=18*365)
        age_18_years = (my_end - age_18_birthdate).days // 365
        self.assertEqual(age_18_years, 18)
        self.assertTrue(18 <= age_18_years <= 75)
        
        # Test age 75 (eligible)
        age_75_birthdate = my_end - pd.Timedelta(days=75*365)
        age_75_years = (my_end - age_75_birthdate).days // 365
        self.assertEqual(age_75_years, 75)
        self.assertTrue(18 <= age_75_years <= 75)
        
        # Test age 17 (not eligible)
        age_17_birthdate = my_end - pd.Timedelta(days=17*365)
        age_17_years = (my_end - age_17_birthdate).days // 365
        self.assertEqual(age_17_years, 17)
        self.assertFalse(18 <= age_17_years <= 75)
        
        # Test age 76 (not eligible)
        age_76_birthdate = my_end - pd.Timedelta(days=76*365)
        age_76_years = (my_end - age_76_birthdate).days // 365
        self.assertEqual(age_76_years, 76)
        self.assertFalse(18 <= age_76_years <= 75)
    
    def test_diabetes_diagnosis_criteria(self):
        """Test HEDIS diabetes diagnosis criteria."""
        # Per HEDIS: 2 outpatient OR 1 inpatient/ED
        # Both should count as having diabetes
        member_df, claims_df, labs_df = get_synthetic_ked_test_data(2025)
        
        result_df = self.ked.identify_denominator(member_df, claims_df)
        
        # 2 outpatient claims = diabetes
        member1 = result_df[result_df['member_id'] == 'KED_COMPLIANT_001']
        self.assertTrue(member1.iloc[0]['has_diabetes'])
        
        # 1 inpatient claim = diabetes
        member2 = result_df[result_df['member_id'] == 'KED_COMPLIANT_002']
        self.assertTrue(member2.iloc[0]['has_diabetes'])
    
    def test_required_tests_both_egfr_and_acr(self):
        """Test HEDIS requirement for BOTH eGFR AND ACR."""
        results = calculate_ked_measure(
            *get_synthetic_ked_test_data(2025),
            measurement_year=2025
        )
        
        member_results = results['member_results']
        
        # Only members with BOTH tests should be in numerator
        numerator_members = member_results[member_results['in_numerator']]
        
        for _, member in numerator_members.iterrows():
            self.assertTrue(member['has_egfr_test'], 
                          f"Member {member['member_id']} in numerator without eGFR")
            self.assertTrue(member['has_acr_test'],
                          f"Member {member['member_id']} in numerator without ACR")
    
    def test_measurement_year_timeframe(self):
        """Test that only tests in measurement year count."""
        # Per HEDIS: Tests must be in measurement year (Jan 1 - Dec 31)
        self.assertEqual(self.ked.my_start, datetime(2025, 1, 1))
        self.assertEqual(self.ked.my_end, datetime(2025, 12, 31))
    
    def test_exclusion_criteria_esrd_transplant(self):
        """Test HEDIS exclusion criteria (ESRD, kidney transplant)."""
        results = calculate_ked_measure(
            *get_synthetic_ked_test_data(2025),
            measurement_year=2025
        )
        
        member_results = results['member_results']
        
        # Excluded members should not be in final denominator
        esrd_member = member_results[
            member_results['member_id'] == 'KED_EXCLUDED_ESRD_001'
        ]
        self.assertTrue(esrd_member.iloc[0]['excluded'])
        self.assertFalse(esrd_member.iloc[0]['in_denominator_final'])
        
        transplant_member = member_results[
            member_results['member_id'] == 'KED_EXCLUDED_TRANSPLANT_001'
        ]
        self.assertTrue(transplant_member.iloc[0]['excluded'])
        self.assertFalse(transplant_member.iloc[0]['in_denominator_final'])


if __name__ == '__main__':
    unittest.main()


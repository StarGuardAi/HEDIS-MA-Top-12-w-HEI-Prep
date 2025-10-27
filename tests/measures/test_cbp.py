"""
Unit Tests for CBP (Controlling High Blood Pressure) Measure

Tests the CBP measure implementation for HEDIS MY2023-2025 compliance.

Author: Analytics Team
Date: October 25, 2025
"""

import unittest
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from src.measures.cbp import (
    CBPMeasure,
    generate_gap_list,
    HTN_DIAGNOSIS_CODES,
    BP_SYSTOLIC_THRESHOLD,
    BP_DIASTOLIC_THRESHOLD
)


class TestCBPMeasure(unittest.TestCase):
    """Test suite for CBP measure implementation"""
    
    def setUp(self):
        """Set up test data"""
        self.measurement_year = 2025
        self.cbp = CBPMeasure(measurement_year=self.measurement_year)
        
        # Create synthetic test data
        self.test_member_id = '12345'
        self.test_birth_date = '1960-06-15'  # Age 65 in 2025
        
        # Member data
        self.member_data = pd.DataFrame({
            'member_id': [self.test_member_id],
            'birth_date': [self.test_birth_date],
            'enrollment_months': [12]
        })
        
        # Claims data with HTN diagnosis
        self.claims_data_with_htn = pd.DataFrame({
            'member_id': [self.test_member_id, self.test_member_id, self.test_member_id],
            'diagnosis_code': ['I10', 'E11.9', 'I10'],
            'service_date': ['2025-01-15', '2025-02-20', '2025-03-10'],
            'claim_type': ['outpatient', 'outpatient', 'professional']
        })
        
        # Vitals data with controlled BP
        self.vitals_data_controlled = pd.DataFrame({
            'member_id': [self.test_member_id, self.test_member_id],
            'reading_date': ['2025-01-15', '2025-06-20'],
            'systolic_bp': [138, 135],
            'diastolic_bp': [88, 85]
        })
        
        # Vitals data with uncontrolled BP
        self.vitals_data_uncontrolled = pd.DataFrame({
            'member_id': [self.test_member_id],
            'reading_date': ['2025-06-20'],
            'systolic_bp': [155],
            'diastolic_bp': [95]
        })
    
    def test_calculate_age(self):
        """Test age calculation as of December 31"""
        birth_date = datetime(1960, 6, 15)
        age = self.cbp.calculate_age(birth_date)
        self.assertEqual(age, 65)
        
        # Test edge cases
        birth_date_dec31 = datetime(1960, 12, 31)
        age = self.cbp.calculate_age(birth_date_dec31)
        self.assertEqual(age, 65)
        
        birth_date_jan1 = datetime(1960, 1, 1)
        age = self.cbp.calculate_age(birth_date_jan1)
        self.assertEqual(age, 65)
    
    def test_denominator_age_criteria(self):
        """Test age criteria for denominator (18-85)"""
        # Test age within range
        in_denom, reason = self.cbp.is_in_denominator(
            self.member_data,
            self.claims_data_with_htn
        )
        self.assertTrue(in_denom)
        
        # Test age too young (17)
        young_member = self.member_data.copy()
        young_member['birth_date'] = '2008-01-01'  # Age 17 in 2025
        in_denom, reason = self.cbp.is_in_denominator(
            young_member,
            self.claims_data_with_htn
        )
        self.assertFalse(in_denom)
        self.assertIn("Age", reason)
        
        # Test age too old (86)
        old_member = self.member_data.copy()
        old_member['birth_date'] = '1939-01-01'  # Age 86 in 2025
        in_denom, reason = self.cbp.is_in_denominator(
            old_member,
            self.claims_data_with_htn
        )
        self.assertFalse(in_denom)
        self.assertIn("Age", reason)
    
    def test_denominator_htn_diagnosis(self):
        """Test HTN diagnosis requirement"""
        # Test with HTN diagnosis
        in_denom, reason = self.cbp.is_in_denominator(
            self.member_data,
            self.claims_data_with_htn
        )
        self.assertTrue(in_denom)
        
        # Test without HTN diagnosis
        claims_no_htn = pd.DataFrame({
            'member_id': [self.test_member_id],
            'diagnosis_code': ['E11.9'],  # Diabetes, no HTN
            'service_date': ['2025-01-15'],
            'claim_type': ['outpatient']
        })
        in_denom, reason = self.cbp.is_in_denominator(
            self.member_data,
            claims_no_htn
        )
        self.assertFalse(in_denom)
        self.assertIn("No HTN diagnosis", reason)
    
    def test_denominator_outpatient_encounter(self):
        """Test outpatient encounter requirement"""
        # Test with outpatient encounter
        in_denom, reason = self.cbp.is_in_denominator(
            self.member_data,
            self.claims_data_with_htn
        )
        self.assertTrue(in_denom)
        
        # Test without outpatient encounter in measurement year
        claims_no_outpatient = pd.DataFrame({
            'member_id': [self.test_member_id],
            'diagnosis_code': ['I10'],
            'service_date': ['2024-01-15'],  # Prior year
            'claim_type': ['outpatient']
        })
        in_denom, reason = self.cbp.is_in_denominator(
            self.member_data,
            claims_no_outpatient
        )
        self.assertFalse(in_denom)
        self.assertIn("No outpatient encounter", reason)
    
    def test_denominator_exclusions(self):
        """Test exclusion criteria"""
        # Test pregnancy exclusion
        claims_with_pregnancy = self.claims_data_with_htn.copy()
        pregnancy_claim = pd.DataFrame({
            'member_id': [self.test_member_id],
            'diagnosis_code': ['O10'],
            'service_date': ['2025-01-15'],
            'claim_type': ['outpatient']
        })
        claims_with_pregnancy = pd.concat([claims_with_pregnancy, pregnancy_claim], ignore_index=True)
        
        in_denom, reason = self.cbp.is_in_denominator(
            self.member_data,
            claims_with_pregnancy
        )
        self.assertFalse(in_denom)
        self.assertIn("Pregnancy", reason)
        
        # Test ESRD exclusion
        claims_with_esrd = self.claims_data_with_htn.copy()
        esrd_claim = pd.DataFrame({
            'member_id': [self.test_member_id],
            'diagnosis_code': ['N18.6'],
            'service_date': ['2025-01-15'],
            'claim_type': ['outpatient']
        })
        claims_with_esrd = pd.concat([claims_with_esrd, esrd_claim], ignore_index=True)
        
        in_denom, reason = self.cbp.is_in_denominator(
            self.member_data,
            claims_with_esrd
        )
        self.assertFalse(in_denom)
        self.assertIn("ESRD", reason)
    
    def test_numerator_bp_controlled(self):
        """Test BP control criteria (<140/90)"""
        # Test controlled BP
        in_numer, reason = self.cbp.is_in_numerator(self.vitals_data_controlled)
        self.assertTrue(in_numer)
        self.assertIn("controlled", reason.lower())
        
        # Test uncontrolled BP
        in_numer, reason = self.cbp.is_in_numerator(self.vitals_data_uncontrolled)
        self.assertFalse(in_numer)
        self.assertIn("not controlled", reason.lower())
    
    def test_numerator_no_bp_readings(self):
        """Test numerator with no BP readings"""
        empty_vitals = pd.DataFrame()
        in_numer, reason = self.cbp.is_in_numerator(empty_vitals)
        self.assertFalse(in_numer)
        self.assertIn("No BP readings", reason)
    
    def test_numerator_most_recent_reading(self):
        """Test that most recent BP reading is used"""
        # Create multiple readings with most recent uncontrolled
        vitals_multiple = pd.DataFrame({
            'member_id': [self.test_member_id] * 3,
            'reading_date': ['2025-01-15', '2025-03-20', '2025-06-20'],
            'systolic_bp': [135, 138, 155],  # Last one uncontrolled
            'diastolic_bp': [85, 88, 95]
        })
        
        in_numer, reason = self.cbp.is_in_numerator(vitals_multiple)
        self.assertFalse(in_numer)
        self.assertIn("155", reason)
    
    def test_bp_threshold_boundary_cases(self):
        """Test BP threshold boundary cases"""
        # Test systolic exactly 140 (should be uncontrolled)
        vitals_boundary_systolic = pd.DataFrame({
            'member_id': [self.test_member_id],
            'reading_date': ['2025-06-20'],
            'systolic_bp': [140],
            'diastolic_bp': [85]
        })
        in_numer, reason = self.cbp.is_in_numerator(vitals_boundary_systolic)
        self.assertFalse(in_numer)
        
        # Test diastolic exactly 90 (should be uncontrolled)
        vitals_boundary_diastolic = pd.DataFrame({
            'member_id': [self.test_member_id],
            'reading_date': ['2025-06-20'],
            'systolic_bp': [135],
            'diastolic_bp': [90]
        })
        in_numer, reason = self.cbp.is_in_numerator(vitals_boundary_diastolic)
        self.assertFalse(in_numer)
        
        # Test 139/89 (should be controlled)
        vitals_just_controlled = pd.DataFrame({
            'member_id': [self.test_member_id],
            'reading_date': ['2025-06-20'],
            'systolic_bp': [139],
            'diastolic_bp': [89]
        })
        in_numer, reason = self.cbp.is_in_numerator(vitals_just_controlled)
        self.assertTrue(in_numer)
    
    def test_calculate_member_status_compliant(self):
        """Test complete member status calculation - compliant member"""
        result = self.cbp.calculate_member_status(
            self.member_data,
            self.claims_data_with_htn,
            self.vitals_data_controlled
        )
        
        self.assertTrue(result['in_denominator'])
        self.assertTrue(result['in_numerator'])
        self.assertTrue(result['compliant'])
        self.assertFalse(result['has_gap'])
        self.assertEqual(result['age'], 65)
        self.assertIn('/', result['most_recent_bp'])
    
    def test_calculate_member_status_gap(self):
        """Test complete member status calculation - gap member"""
        result = self.cbp.calculate_member_status(
            self.member_data,
            self.claims_data_with_htn,
            self.vitals_data_uncontrolled
        )
        
        self.assertTrue(result['in_denominator'])
        self.assertFalse(result['in_numerator'])
        self.assertFalse(result['compliant'])
        self.assertTrue(result['has_gap'])
        self.assertEqual(result['age'], 65)
    
    def test_calculate_population_rate(self):
        """Test population-level rate calculation"""
        # Create population of 3 members
        members_df = pd.DataFrame({
            'member_id': ['M001', 'M002', 'M003'],
            'birth_date': ['1960-01-01', '1965-01-01', '1970-01-01'],
            'enrollment_months': [12, 12, 12]
        })
        
        claims_df = pd.DataFrame({
            'member_id': ['M001', 'M001', 'M002', 'M002', 'M003', 'M003'],
            'diagnosis_code': ['I10', 'I10', 'I10', 'I10', 'I10', 'I10'],
            'service_date': ['2025-01-15', '2025-02-15', '2025-01-20', '2025-02-20', '2025-01-25', '2025-02-25'],
            'claim_type': ['outpatient', 'outpatient', 'outpatient', 'outpatient', 'outpatient', 'outpatient']
        })
        
        vitals_df = pd.DataFrame({
            'member_id': ['M001', 'M002', 'M003'],
            'reading_date': ['2025-06-15', '2025-06-20', '2025-06-25'],
            'systolic_bp': [135, 155, 138],
            'diastolic_bp': [85, 95, 88]
        })
        
        results = self.cbp.calculate_population_rate(members_df, claims_df, vitals_df)
        
        self.assertEqual(results['total_population'], 3)
        self.assertEqual(results['denominator_count'], 3)
        self.assertEqual(results['numerator_count'], 2)  # M001 and M003 controlled
        self.assertAlmostEqual(results['measure_rate'], 66.67, places=1)
        self.assertEqual(results['gap_count'], 1)  # M002 has gap
    
    def test_generate_gap_list(self):
        """Test gap list generation"""
        # Create test population
        members_df = pd.DataFrame({
            'member_id': ['M001', 'M002'],
            'birth_date': ['1960-01-01', '1945-01-01'],  # M002 is older
            'enrollment_months': [12, 12]
        })
        
        claims_df = pd.DataFrame({
            'member_id': ['M001', 'M001', 'M002', 'M002'],
            'diagnosis_code': ['I10', 'I10', 'I10', 'I10'],
            'service_date': ['2025-01-15', '2025-02-15', '2025-01-20', '2025-02-20'],
            'claim_type': ['outpatient', 'outpatient', 'outpatient', 'outpatient']
        })
        
        vitals_df = pd.DataFrame({
            'member_id': ['M001', 'M002'],
            'reading_date': ['2025-06-15', '2025-06-20'],
            'systolic_bp': [155, 160],
            'diastolic_bp': [95, 100]
        })
        
        gap_list = generate_gap_list(members_df, claims_df, vitals_df, self.measurement_year)
        
        self.assertEqual(len(gap_list), 2)  # Both have gaps
        self.assertIn('member_id', gap_list.columns)
        self.assertIn('priority_score', gap_list.columns)
        
        # M002 should have higher priority (older)
        self.assertGreater(
            gap_list[gap_list['member_id'] == 'M002']['priority_score'].iloc[0],
            gap_list[gap_list['member_id'] == 'M001']['priority_score'].iloc[0]
        )
    
    def test_hedis_code_compliance(self):
        """Test that HTN codes match HEDIS specifications"""
        # Verify essential codes are included
        essential_codes = ['I10', 'I11.0', 'I11.9', 'I12.0', 'I12.9', 
                          'I13.0', 'I13.10', 'I13.11', 'I13.2']
        for code in essential_codes:
            self.assertIn(code, HTN_DIAGNOSIS_CODES)
        
        # Verify secondary HTN codes
        secondary_codes = ['I15.0', 'I15.1', 'I15.2', 'I15.8', 'I15.9']
        for code in secondary_codes:
            self.assertIn(code, HTN_DIAGNOSIS_CODES)
        
        # Verify crisis codes
        crisis_codes = ['I16.0', 'I16.1', 'I16.9']
        for code in crisis_codes:
            self.assertIn(code, HTN_DIAGNOSIS_CODES)
    
    def test_bp_thresholds(self):
        """Test BP thresholds match HEDIS specifications"""
        self.assertEqual(BP_SYSTOLIC_THRESHOLD, 140)
        self.assertEqual(BP_DIASTOLIC_THRESHOLD, 90)


class TestCBPIntegration(unittest.TestCase):
    """Integration tests for CBP measure"""
    
    def test_end_to_end_workflow(self):
        """Test complete CBP workflow from data to gap list"""
        # Create realistic test data
        members_df = pd.DataFrame({
            'member_id': ['M001', 'M002', 'M003', 'M004'],
            'birth_date': ['1960-01-01', '1965-01-01', '1970-01-01', '1975-01-01'],
            'enrollment_months': [12, 12, 12, 12]
        })
        
        claims_df = pd.DataFrame({
            'member_id': ['M001'] * 3 + ['M002'] * 3 + ['M003'] * 3 + ['M004'] * 2,
            'diagnosis_code': ['I10', 'E11.9', 'I10'] + 
                             ['I10', 'I10', 'I10'] + 
                             ['I10', 'I10', 'I10'] +
                             ['I10', 'I10'],
            'service_date': ['2025-01-15', '2025-02-20', '2025-03-10'] + 
                           ['2025-01-20', '2025-02-25', '2025-03-15'] + 
                           ['2025-01-25', '2025-02-28', '2025-03-20'] +
                           ['2025-01-30', '2025-02-28'],
            'claim_type': ['outpatient'] * 11
        })
        
        vitals_df = pd.DataFrame({
            'member_id': ['M001', 'M002', 'M003', 'M004'],
            'reading_date': ['2025-06-15', '2025-06-20', '2025-06-25', '2025-06-30'],
            'systolic_bp': [135, 155, 138, 142],
            'diastolic_bp': [85, 95, 88, 92]
        })
        
        # Run complete workflow
        cbp = CBPMeasure(measurement_year=2025)
        results = cbp.calculate_population_rate(members_df, claims_df, vitals_df)
        gap_list = generate_gap_list(members_df, claims_df, vitals_df, 2025)
        
        # Validate results
        self.assertEqual(results['denominator_count'], 4)
        self.assertEqual(results['numerator_count'], 2)  # M001 and M003
        self.assertEqual(len(gap_list), 2)  # M002 and M004


if __name__ == '__main__':
    unittest.main()


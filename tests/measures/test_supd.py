"""
Unit Tests for SUPD (Statin Therapy for Patients with Diabetes) Measure

Tests the SUPD measure implementation for HEDIS MY2023-2025 compliance.

Author: Analytics Team
Date: October 25, 2025
"""

import unittest
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from src.measures.supd import (
    SUPDMeasure,
    generate_gap_list,
    DIABETES_CODES,
    STATIN_MEDICATIONS,
    HIGH_POTENCY_STATINS
)


class TestSUPDMeasure(unittest.TestCase):
    """Test suite for SUPD measure implementation"""
    
    def setUp(self):
        """Set up test data"""
        self.measurement_year = 2025
        self.supd = SUPDMeasure(measurement_year=self.measurement_year)
        
        # Create synthetic test data
        self.test_member_id = '12345'
        self.test_birth_date = '1970-06-15'  # Age 55 in 2025
        
        # Member data
        self.member_data = pd.DataFrame({
            'member_id': [self.test_member_id],
            'birth_date': [self.test_birth_date],
            'enrollment_months': [12]
        })
        
        # Claims data with diabetes diagnosis
        self.claims_data_with_diabetes = pd.DataFrame({
            'member_id': [self.test_member_id, self.test_member_id, self.test_member_id],
            'diagnosis_code': ['E11.9', 'E11.22', 'I10'],
            'service_date': ['2025-01-15', '2025-02-20', '2025-03-10'],
            'claim_type': ['outpatient', 'outpatient', 'professional']
        })
        
        # Pharmacy data with statin
        self.pharmacy_data_with_statin = pd.DataFrame({
            'member_id': [self.test_member_id, self.test_member_id],
            'medication_name': ['atorvastatin 40mg', 'atorvastatin 40mg'],
            'fill_date': ['2025-01-15', '2025-02-15'],
            'days_supply': [30, 30]
        })
        
        # Pharmacy data without statin
        self.pharmacy_data_no_statin = pd.DataFrame({
            'member_id': [self.test_member_id],
            'medication_name': ['metformin 500mg'],
            'fill_date': ['2025-01-15'],
            'days_supply': [30]
        })
    
    def test_calculate_age(self):
        """Test age calculation as of December 31"""
        birth_date = datetime(1970, 6, 15)
        age = self.supd.calculate_age(birth_date)
        self.assertEqual(age, 55)
        
        # Test boundary cases
        birth_date_40 = datetime(1985, 12, 31)
        age = self.supd.calculate_age(birth_date_40)
        self.assertEqual(age, 40)
        
        birth_date_75 = datetime(1950, 1, 1)
        age = self.supd.calculate_age(birth_date_75)
        self.assertEqual(age, 75)
    
    def test_denominator_age_criteria(self):
        """Test age criteria for denominator (40-75)"""
        # Test age within range
        in_denom, reason = self.supd.is_in_denominator(
            self.member_data,
            self.claims_data_with_diabetes
        )
        self.assertTrue(in_denom)
        
        # Test age too young (39)
        young_member = self.member_data.copy()
        young_member['birth_date'] = '1986-01-01'  # Age 39 in 2025
        in_denom, reason = self.supd.is_in_denominator(
            young_member,
            self.claims_data_with_diabetes
        )
        self.assertFalse(in_denom)
        self.assertIn("Age", reason)
        
        # Test age too old (76)
        old_member = self.member_data.copy()
        old_member['birth_date'] = '1949-01-01'  # Age 76 in 2025
        in_denom, reason = self.supd.is_in_denominator(
            old_member,
            self.claims_data_with_diabetes
        )
        self.assertFalse(in_denom)
        self.assertIn("Age", reason)
    
    def test_denominator_diabetes_diagnosis(self):
        """Test diabetes diagnosis requirement"""
        # Test with diabetes diagnosis
        in_denom, reason = self.supd.is_in_denominator(
            self.member_data,
            self.claims_data_with_diabetes
        )
        self.assertTrue(in_denom)
        
        # Test without diabetes diagnosis
        claims_no_diabetes = pd.DataFrame({
            'member_id': [self.test_member_id],
            'diagnosis_code': ['I10'],  # HTN only, no diabetes
            'service_date': ['2025-01-15'],
            'claim_type': ['outpatient']
        })
        in_denom, reason = self.supd.is_in_denominator(
            self.member_data,
            claims_no_diabetes
        )
        self.assertFalse(in_denom)
        self.assertIn("diabetes", reason.lower())
    
    def test_denominator_outpatient_encounter(self):
        """Test outpatient encounter requirement"""
        # Test with outpatient encounter
        in_denom, reason = self.supd.is_in_denominator(
            self.member_data,
            self.claims_data_with_diabetes
        )
        self.assertTrue(in_denom)
        
        # Test without outpatient encounter in measurement year
        claims_no_outpatient = pd.DataFrame({
            'member_id': [self.test_member_id],
            'diagnosis_code': ['E11.9'],
            'service_date': ['2024-01-15'],  # Prior year
            'claim_type': ['outpatient']
        })
        in_denom, reason = self.supd.is_in_denominator(
            self.member_data,
            claims_no_outpatient
        )
        self.assertFalse(in_denom)
        self.assertIn("outpatient", reason.lower())
    
    def test_denominator_exclusions(self):
        """Test exclusion criteria"""
        # Test pregnancy exclusion
        claims_with_pregnancy = self.claims_data_with_diabetes.copy()
        pregnancy_claim = pd.DataFrame({
            'member_id': [self.test_member_id],
            'diagnosis_code': ['O10'],
            'service_date': ['2025-01-15'],
            'claim_type': ['outpatient']
        })
        claims_with_pregnancy = pd.concat([claims_with_pregnancy, pregnancy_claim], ignore_index=True)
        
        in_denom, reason = self.supd.is_in_denominator(
            self.member_data,
            claims_with_pregnancy
        )
        self.assertFalse(in_denom)
        self.assertIn("Pregnancy", reason)
        
        # Test ESRD exclusion
        claims_with_esrd = self.claims_data_with_diabetes.copy()
        esrd_claim = pd.DataFrame({
            'member_id': [self.test_member_id],
            'diagnosis_code': ['N18.6'],
            'service_date': ['2025-01-15'],
            'claim_type': ['outpatient']
        })
        claims_with_esrd = pd.concat([claims_with_esrd, esrd_claim], ignore_index=True)
        
        in_denom, reason = self.supd.is_in_denominator(
            self.member_data,
            claims_with_esrd
        )
        self.assertFalse(in_denom)
        self.assertIn("ESRD", reason)
        
        # Test cirrhosis exclusion
        claims_with_cirrhosis = self.claims_data_with_diabetes.copy()
        cirrhosis_claim = pd.DataFrame({
            'member_id': [self.test_member_id],
            'diagnosis_code': ['K70.3'],
            'service_date': ['2025-01-15'],
            'claim_type': ['outpatient']
        })
        claims_with_cirrhosis = pd.concat([claims_with_cirrhosis, cirrhosis_claim], ignore_index=True)
        
        in_denom, reason = self.supd.is_in_denominator(
            self.member_data,
            claims_with_cirrhosis
        )
        self.assertFalse(in_denom)
        self.assertIn("Cirrhosis", reason)
    
    def test_numerator_statin_prescription(self):
        """Test statin prescription criteria"""
        # Test with statin prescription
        in_numer, reason = self.supd.is_in_numerator(self.pharmacy_data_with_statin)
        self.assertTrue(in_numer)
        self.assertIn("statin", reason.lower())
        
        # Test without statin prescription
        in_numer, reason = self.supd.is_in_numerator(self.pharmacy_data_no_statin)
        self.assertFalse(in_numer)
        self.assertIn("No statin", reason)
    
    def test_numerator_no_pharmacy_data(self):
        """Test numerator with no pharmacy data"""
        empty_pharmacy = pd.DataFrame()
        in_numer, reason = self.supd.is_in_numerator(empty_pharmacy)
        self.assertFalse(in_numer)
        self.assertIn("No", reason)
    
    def test_statin_potency_detection(self):
        """Test statin potency classification"""
        # High potency statin
        high_potency_pharmacy = pd.DataFrame({
            'member_id': [self.test_member_id],
            'medication_name': ['atorvastatin 40mg'],
            'fill_date': ['2025-01-15'],
            'days_supply': [30]
        })
        in_numer, reason = self.supd.is_in_numerator(high_potency_pharmacy)
        self.assertTrue(in_numer)
        
        # Moderate potency statin
        moderate_potency_pharmacy = pd.DataFrame({
            'member_id': [self.test_member_id],
            'medication_name': ['simvastatin 20mg'],
            'fill_date': ['2025-01-15'],
            'days_supply': [30]
        })
        in_numer, reason = self.supd.is_in_numerator(moderate_potency_pharmacy)
        self.assertTrue(in_numer)
    
    def test_calculate_member_status_compliant(self):
        """Test complete member status calculation - compliant member"""
        result = self.supd.calculate_member_status(
            self.member_data,
            self.claims_data_with_diabetes,
            self.pharmacy_data_with_statin
        )
        
        self.assertTrue(result['in_denominator'])
        self.assertTrue(result['in_numerator'])
        self.assertTrue(result['compliant'])
        self.assertFalse(result['has_gap'])
        self.assertEqual(result['age'], 55)
    
    def test_calculate_member_status_gap(self):
        """Test complete member status calculation - gap member"""
        result = self.supd.calculate_member_status(
            self.member_data,
            self.claims_data_with_diabetes,
            self.pharmacy_data_no_statin
        )
        
        self.assertTrue(result['in_denominator'])
        self.assertFalse(result['in_numerator'])
        self.assertFalse(result['compliant'])
        self.assertTrue(result['has_gap'])
    
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
            'diagnosis_code': ['E11.9', 'E11.9', 'E11.9', 'E11.9', 'E11.9', 'E11.9'],
            'service_date': ['2025-01-15', '2025-02-15', '2025-01-20', '2025-02-20', '2025-01-25', '2025-02-25'],
            'claim_type': ['outpatient', 'outpatient', 'outpatient', 'outpatient', 'outpatient', 'outpatient']
        })
        
        pharmacy_df = pd.DataFrame({
            'member_id': ['M001', 'M002'],
            'medication_name': ['atorvastatin 40mg', 'simvastatin 20mg'],
            'fill_date': ['2025-06-15', '2025-06-20'],
            'days_supply': [30, 30]
        })
        
        results = self.supd.calculate_population_rate(members_df, claims_df, pharmacy_df)
        
        self.assertEqual(results['total_population'], 3)
        self.assertEqual(results['denominator_count'], 3)
        self.assertEqual(results['numerator_count'], 2)  # M001 and M002 have statins
        self.assertAlmostEqual(results['measure_rate'], 66.67, places=1)
        self.assertEqual(results['gap_count'], 1)  # M003 has gap
    
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
            'diagnosis_code': ['E11.9', 'E11.9', 'E11.9', 'E11.9'],
            'service_date': ['2025-01-15', '2025-02-15', '2025-01-20', '2025-02-20'],
            'claim_type': ['outpatient', 'outpatient', 'outpatient', 'outpatient']
        })
        
        pharmacy_df = pd.DataFrame()  # No statins for either
        
        gap_list = generate_gap_list(members_df, claims_df, pharmacy_df, self.measurement_year)
        
        self.assertEqual(len(gap_list), 2)  # Both have gaps
        self.assertIn('member_id', gap_list.columns)
        self.assertIn('priority_score', gap_list.columns)
    
    def test_hedis_code_compliance(self):
        """Test that diabetes codes match HEDIS specifications"""
        # Verify essential diabetes codes are included
        self.assertIn('E10', DIABETES_CODES)
        self.assertIn('E11', DIABETES_CODES)
        self.assertIn('E13', DIABETES_CODES)
    
    def test_statin_medication_list(self):
        """Test statin medication list completeness"""
        expected_statins = ['atorvastatin', 'simvastatin', 'rosuvastatin', 
                           'pravastatin', 'lovastatin', 'fluvastatin', 'pitavastatin']
        for statin in expected_statins:
            self.assertIn(statin, STATIN_MEDICATIONS)


class TestSUPDIntegration(unittest.TestCase):
    """Integration tests for SUPD measure"""
    
    def test_end_to_end_workflow(self):
        """Test complete SUPD workflow from data to gap list"""
        # Create realistic test data
        members_df = pd.DataFrame({
            'member_id': ['M001', 'M002', 'M003', 'M004'],
            'birth_date': ['1960-01-01', '1965-01-01', '1970-01-01', '1975-01-01'],
            'enrollment_months': [12, 12, 12, 12]
        })
        
        claims_df = pd.DataFrame({
            'member_id': ['M001'] * 3 + ['M002'] * 3 + ['M003'] * 3 + ['M004'] * 2,
            'diagnosis_code': ['E11.9', 'E11.22', 'I10'] * 3 + ['E11.9', 'E11.9'],
            'service_date': ['2025-01-15', '2025-02-20', '2025-03-10'] +
                           ['2025-01-20', '2025-02-25', '2025-03-15'] +
                           ['2025-01-25', '2025-02-28', '2025-03-20'] +
                           ['2025-01-30', '2025-02-28'],
            'claim_type': ['outpatient'] * 11
        })
        
        pharmacy_df = pd.DataFrame({
            'member_id': ['M001', 'M002', 'M003'],
            'medication_name': ['atorvastatin 40mg', 'simvastatin 20mg', 'rosuvastatin 20mg'],
            'fill_date': ['2025-06-15', '2025-06-20', '2025-06-25'],
            'days_supply': [30, 30, 30]
        })
        
        # Run complete workflow
        supd = SUPDMeasure(measurement_year=2025)
        results = supd.calculate_population_rate(members_df, claims_df, pharmacy_df)
        gap_list = generate_gap_list(members_df, claims_df, pharmacy_df, 2025)
        
        # Validate results
        self.assertEqual(results['denominator_count'], 4)
        self.assertEqual(results['numerator_count'], 3)  # M001, M002, M003
        self.assertEqual(len(gap_list), 1)  # M004 only


if __name__ == '__main__':
    unittest.main()


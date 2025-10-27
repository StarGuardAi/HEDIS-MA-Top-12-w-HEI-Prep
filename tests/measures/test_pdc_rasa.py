"""
Unit Tests for PDC-RASA (Medication Adherence - Hypertension) Measure

Tests the PDC-RASA measure implementation for HEDIS MY2023-2025 compliance.

Author: Analytics Team
Date: October 25, 2025
"""

import unittest
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from src.measures.pdc_rasa import (
    PDCRASAMeasure,
    generate_gap_list,
    ACE_INHIBITORS,
    ARBS,
    ALL_RAS_ANTAGONISTS,
    PDC_THRESHOLD
)


class TestPDCRASAMeasure(unittest.TestCase):
    """Test suite for PDC-RASA measure implementation"""
    
    def setUp(self):
        """Set up test data"""
        self.measurement_year = 2025
        self.pdc_rasa = PDCRASAMeasure(measurement_year=self.measurement_year)
        
        # Create synthetic test data
        self.test_member_id = '12345'
        self.test_birth_date = '1960-06-15'  # Age 65 in 2025
        
        # Member data
        self.member_data = pd.DataFrame({
            'member_id': [self.test_member_id],
            'birth_date': [self.test_birth_date],
            'enrollment_months': [12]
        })
        
        # Pharmacy data with good adherence (PDC ~0.85)
        fill_dates = pd.date_range('2025-01-15', periods=12, freq='30D')
        self.pharmacy_data_adherent = pd.DataFrame({
            'member_id': [self.test_member_id] * 12,
            'medication_name': ['lisinopril 10mg'] * 12,
            'fill_date': fill_dates.strftime('%Y-%m-%d'),
            'days_supply': [30] * 12
        })
        
        # Pharmacy data with poor adherence (PDC ~0.40)
        fill_dates_poor = pd.date_range('2025-01-15', periods=5, freq='75D')
        self.pharmacy_data_nonadherent = pd.DataFrame({
            'member_id': [self.test_member_id] * 5,
            'medication_name': ['lisinopril 10mg'] * 5,
            'fill_date': fill_dates_poor.strftime('%Y-%m-%d'),
            'days_supply': [30] * 5
        })
        
        # Pharmacy data with only 1 fill (not eligible)
        self.pharmacy_data_one_fill = pd.DataFrame({
            'member_id': [self.test_member_id],
            'medication_name': ['lisinopril 10mg'],
            'fill_date': ['2025-01-15'],
            'days_supply': [30]
        })
    
    def test_calculate_age(self):
        """Test age calculation as of December 31"""
        birth_date = datetime(1960, 6, 15)
        age = self.pdc_rasa.calculate_age(birth_date)
        self.assertEqual(age, 65)
        
        # Test boundary case - age 18
        birth_date_18 = datetime(2007, 12, 31)
        age = self.pdc_rasa.calculate_age(birth_date_18)
        self.assertEqual(age, 18)
    
    def test_calculate_pdc_high_adherence(self):
        """Test PDC calculation with high adherence"""
        pdc, days_covered, total_days = self.pdc_rasa.calculate_pdc(self.pharmacy_data_adherent)
        
        # PDC should be high (close to 1.0)
        self.assertGreater(pdc, 0.80)
        self.assertGreaterEqual(days_covered, 0)
        self.assertEqual(total_days, 365)  # Full year
    
    def test_calculate_pdc_low_adherence(self):
        """Test PDC calculation with low adherence"""
        pdc, days_covered, total_days = self.pdc_rasa.calculate_pdc(self.pharmacy_data_nonadherent)
        
        # PDC should be low
        self.assertLess(pdc, 0.80)
        self.assertGreater(pdc, 0.0)
    
    def test_calculate_pdc_empty_data(self):
        """Test PDC calculation with no pharmacy data"""
        empty_pharmacy = pd.DataFrame()
        pdc, days_covered, total_days = self.pdc_rasa.calculate_pdc(empty_pharmacy)
        
        self.assertEqual(pdc, 0.0)
        self.assertEqual(days_covered, 0)
    
    def test_denominator_minimum_fills(self):
        """Test minimum 2 fills requirement for denominator"""
        # Test with 2+ fills (should be in denominator)
        in_denom, reason = self.pdc_rasa.is_in_denominator(
            self.member_data,
            self.pharmacy_data_adherent
        )
        self.assertTrue(in_denom)
        
        # Test with only 1 fill (should not be in denominator)
        in_denom, reason = self.pdc_rasa.is_in_denominator(
            self.member_data,
            self.pharmacy_data_one_fill
        )
        self.assertFalse(in_denom)
        self.assertIn("2", reason)
    
    def test_denominator_age_criteria(self):
        """Test age criteria for denominator (18+)"""
        # Test age within range (65)
        in_denom, reason = self.pdc_rasa.is_in_denominator(
            self.member_data,
            self.pharmacy_data_adherent
        )
        self.assertTrue(in_denom)
        
        # Test age too young (17)
        young_member = self.member_data.copy()
        young_member['birth_date'] = '2008-01-01'  # Age 17 in 2025
        in_denom, reason = self.pdc_rasa.is_in_denominator(
            young_member,
            self.pharmacy_data_adherent
        )
        self.assertFalse(in_denom)
        self.assertIn("Age", reason)
    
    def test_denominator_enrollment(self):
        """Test continuous enrollment requirement"""
        # Test with continuous enrollment
        in_denom, reason = self.pdc_rasa.is_in_denominator(
            self.member_data,
            self.pharmacy_data_adherent
        )
        self.assertTrue(in_denom)
        
        # Test without continuous enrollment
        partial_enrollment = self.member_data.copy()
        partial_enrollment['enrollment_months'] = 10  # Less than 12 months
        in_denom, reason = self.pdc_rasa.is_in_denominator(
            partial_enrollment,
            self.pharmacy_data_adherent
        )
        self.assertFalse(in_denom)
        self.assertIn("enrolled", reason.lower())
    
    def test_numerator_adherent_member(self):
        """Test numerator with PDC ≥ 80%"""
        pdc, _, _ = self.pdc_rasa.calculate_pdc(self.pharmacy_data_adherent)
        in_numer, reason = self.pdc_rasa.is_in_numerator(self.pharmacy_data_adherent)
        
        if pdc >= PDC_THRESHOLD:
            self.assertTrue(in_numer)
            self.assertIn("0.", reason)  # PDC value in reason
    
    def test_numerator_nonadherent_member(self):
        """Test numerator with PDC < 80%"""
        in_numer, reason = self.pdc_rasa.is_in_numerator(self.pharmacy_data_nonadherent)
        self.assertFalse(in_numer)
        self.assertIn("80%", reason)
    
    def test_pdc_threshold(self):
        """Test PDC threshold is correctly set"""
        self.assertEqual(PDC_THRESHOLD, 0.80)
    
    def test_ace_inhibitor_detection(self):
        """Test ACE inhibitor medications are detected"""
        # Test various ACE inhibitors
        for ace in ['lisinopril', 'enalapril', 'ramipril']:
            pharmacy_data = pd.DataFrame({
                'member_id': [self.test_member_id] * 12,
                'medication_name': [f'{ace} 10mg'] * 12,
                'fill_date': pd.date_range('2025-01-15', periods=12, freq='30D').strftime('%Y-%m-%d'),
                'days_supply': [30] * 12
            })
            in_denom, reason = self.pdc_rasa.is_in_denominator(
                self.member_data,
                pharmacy_data
            )
            self.assertTrue(in_denom, f"{ace} should be detected as RAS antagonist")
    
    def test_arb_detection(self):
        """Test ARB medications are detected"""
        # Test various ARBs
        for arb in ['losartan', 'valsartan', 'irbesartan']:
            pharmacy_data = pd.DataFrame({
                'member_id': [self.test_member_id] * 12,
                'medication_name': [f'{arb} 50mg'] * 12,
                'fill_date': pd.date_range('2025-01-15', periods=12, freq='30D').strftime('%Y-%m-%d'),
                'days_supply': [30] * 12
            })
            in_denom, reason = self.pdc_rasa.is_in_denominator(
                self.member_data,
                pharmacy_data
            )
            self.assertTrue(in_denom, f"{arb} should be detected as RAS antagonist")
    
    def test_calculate_member_status_compliant(self):
        """Test complete member status calculation - adherent member"""
        result = self.pdc_rasa.calculate_member_status(
            self.member_data,
            self.pharmacy_data_adherent
        )
        
        self.assertTrue(result['in_denominator'])
        # Check if PDC is high enough
        if result['pdc'] >= PDC_THRESHOLD:
            self.assertTrue(result['in_numerator'])
            self.assertTrue(result['compliant'])
            self.assertFalse(result['has_gap'])
    
    def test_calculate_member_status_gap(self):
        """Test complete member status calculation - non-adherent member"""
        result = self.pdc_rasa.calculate_member_status(
            self.member_data,
            self.pharmacy_data_nonadherent
        )
        
        self.assertTrue(result['in_denominator'])
        self.assertFalse(result['in_numerator'])
        self.assertFalse(result['compliant'])
        self.assertTrue(result['has_gap'])
        self.assertLess(result['pdc'], PDC_THRESHOLD)
    
    def test_calculate_population_rate(self):
        """Test population-level rate calculation"""
        # Create population of 3 members with varying adherence
        members_df = pd.DataFrame({
            'member_id': ['M001', 'M002', 'M003'],
            'birth_date': ['1960-01-01', '1965-01-01', '1970-01-01'],
            'enrollment_months': [12, 12, 12]
        })
        
        # M001: High adherence, M002: High adherence, M003: Low adherence
        fill_dates_high = pd.date_range('2025-01-15', periods=12, freq='30D')
        fill_dates_low = pd.date_range('2025-01-15', periods=5, freq='75D')
        
        pharmacy_df = pd.DataFrame({
            'member_id': ['M001'] * 12 + ['M002'] * 12 + ['M003'] * 5,
            'medication_name': ['lisinopril 10mg'] * 29,
            'fill_date': list(fill_dates_high.strftime('%Y-%m-%d')) + 
                        list(fill_dates_high.strftime('%Y-%m-%d')) +
                        list(fill_dates_low.strftime('%Y-%m-%d')),
            'days_supply': [30] * 29
        })
        
        results = self.pdc_rasa.calculate_population_rate(members_df, pharmacy_df)
        
        self.assertEqual(results['total_population'], 3)
        self.assertEqual(results['denominator_count'], 3)  # All have 2+ fills
        # Numerator depends on PDC calculation
        self.assertGreaterEqual(results['numerator_count'], 2)  # At least M001 and M002
    
    def test_generate_gap_list(self):
        """Test gap list generation"""
        # Create test population with gaps
        members_df = pd.DataFrame({
            'member_id': ['M001', 'M002'],
            'birth_date': ['1960-01-01', '1965-01-01'],
            'enrollment_months': [12, 12]
        })
        
        # Both have low adherence
        fill_dates_low = pd.date_range('2025-01-15', periods=5, freq='75D')
        pharmacy_df = pd.DataFrame({
            'member_id': ['M001'] * 5 + ['M002'] * 5,
            'medication_name': ['lisinopril 10mg'] * 10,
            'fill_date': list(fill_dates_low.strftime('%Y-%m-%d')) * 2,
            'days_supply': [30] * 10
        })
        
        gap_list = generate_gap_list(members_df, pharmacy_df, self.measurement_year)
        
        self.assertGreater(len(gap_list), 0)  # Should have gaps
        self.assertIn('member_id', gap_list.columns)
        self.assertIn('pdc', gap_list.columns)
        self.assertIn('priority_score', gap_list.columns)
    
    def test_hedis_medication_list(self):
        """Test RAS antagonist medication lists are complete"""
        # Verify ACE inhibitors
        expected_ace = ['lisinopril', 'enalapril', 'ramipril', 'captopril']
        for med in expected_ace:
            self.assertIn(med, ACE_INHIBITORS)
        
        # Verify ARBs
        expected_arbs = ['losartan', 'valsartan', 'irbesartan']
        for med in expected_arbs:
            self.assertIn(med, ARBS)
        
        # Verify all RAS antagonists combined
        self.assertGreater(len(ALL_RAS_ANTAGONISTS), 15)


class TestPDCRASAIntegration(unittest.TestCase):
    """Integration tests for PDC-RASA measure"""
    
    def test_end_to_end_workflow(self):
        """Test complete PDC-RASA workflow from data to gap list"""
        # Create realistic test data
        members_df = pd.DataFrame({
            'member_id': ['M001', 'M002', 'M003'],
            'birth_date': ['1960-01-01', '1965-01-01', '1970-01-01'],
            'enrollment_months': [12, 12, 12]
        })
        
        # Create pharmacy data with varying adherence
        fill_dates_high = pd.date_range('2025-01-15', periods=12, freq='30D')
        fill_dates_medium = pd.date_range('2025-01-15', periods=9, freq='40D')
        fill_dates_low = pd.date_range('2025-01-15', periods=5, freq='75D')
        
        pharmacy_df = pd.DataFrame({
            'member_id': ['M001'] * 12 + ['M002'] * 9 + ['M003'] * 5,
            'medication_name': ['lisinopril 10mg'] * 26,
            'fill_date': list(fill_dates_high.strftime('%Y-%m-%d')) +
                        list(fill_dates_medium.strftime('%Y-%m-%d')) +
                        list(fill_dates_low.strftime('%Y-%m-%d')),
            'days_supply': [30] * 26
        })
        
        # Run complete workflow
        pdc_rasa = PDCRASAMeasure(measurement_year=2025)
        results = pdc_rasa.calculate_population_rate(members_df, pharmacy_df)
        gap_list = generate_gap_list(members_df, pharmacy_df, 2025)
        
        # Validate results
        self.assertEqual(results['total_population'], 3)
        self.assertEqual(results['denominator_count'], 3)  # All have 2+ fills
        self.assertGreater(results['numerator_count'], 0)  # At least some adherent


if __name__ == '__main__':
    unittest.main()


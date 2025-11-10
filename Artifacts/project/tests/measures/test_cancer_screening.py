"""
Unit Tests for Cancer Screening Measures (BCS, COL)

Tests both Tier 3 measures:
- BCS: Breast Cancer Screening
- COL: Colorectal Cancer Screening

Author: Analytics Team
Date: October 23, 2025
"""

import unittest
import pandas as pd
from datetime import datetime, timedelta
import sys
import os

# Add src to path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from src.measures.bcs import BCSMeasure
from src.measures.col import COLMeasure


class TestBCSMeasure(unittest.TestCase):
    """Test suite for BCS (Breast Cancer Screening) measure"""
    
    def setUp(self):
        """Set up test data"""
        self.bcs = BCSMeasure(measurement_year=2025)
        
        # Base member data (eligible female, age 55)
        self.eligible_member = pd.DataFrame({
            'member_id': ['M001'],
            'birth_date': [datetime(1970, 6, 15)],
            'gender': ['F'],
            'enrollment_months': [12]
        })
        
        # Base claims data with outpatient encounter
        self.eligible_claims = pd.DataFrame({
            'member_id': ['M001'],
            'claim_type': ['outpatient'],
            'service_date': [datetime(2025, 3, 15)],
            'diagnosis_code': ['Z00.00'],
            'provider_specialty': ['primary care']
        })
    
    def test_denominator_eligible_female(self):
        """Test eligible female is in denominator"""
        in_denom, reason = self.bcs.is_in_denominator(
            self.eligible_member,
            self.eligible_claims
        )
        self.assertTrue(in_denom)
        self.assertEqual(reason, "eligible")
    
    def test_denominator_excludes_male(self):
        """Test males are excluded from denominator"""
        male_member = self.eligible_member.copy()
        male_member['gender'] = 'M'
        
        in_denom, reason = self.bcs.is_in_denominator(
            male_member,
            self.eligible_claims
        )
        self.assertFalse(in_denom)
        self.assertIn("gender_not_female", reason)
    
    def test_denominator_age_too_young(self):
        """Test age < 50 excluded"""
        young_member = self.eligible_member.copy()
        young_member['birth_date'] = datetime(1980, 1, 1)  # Age 45
        
        in_denom, reason = self.bcs.is_in_denominator(
            young_member,
            self.eligible_claims
        )
        self.assertFalse(in_denom)
        self.assertIn("age_too_young", reason)
    
    def test_denominator_age_too_old(self):
        """Test age > 74 excluded"""
        old_member = self.eligible_member.copy()
        old_member['birth_date'] = datetime(1945, 1, 1)  # Age 80
        
        in_denom, reason = self.bcs.is_in_denominator(
            old_member,
            self.eligible_claims
        )
        self.assertFalse(in_denom)
        self.assertIn("age_too_old", reason)
    
    def test_denominator_bilateral_mastectomy_excluded(self):
        """Test bilateral mastectomy exclusion"""
        mastectomy_claims = self.eligible_claims.copy()
        mastectomy_claims['diagnosis_code'] = 'Z90.13'
        
        in_denom, reason = self.bcs.is_in_denominator(
            self.eligible_member,
            mastectomy_claims
        )
        self.assertFalse(in_denom)
        self.assertEqual(reason, "bilateral_mastectomy_history")
    
    def test_numerator_compliant_with_mammography(self):
        """Test compliant with mammography in 2-year window"""
        procedures = pd.DataFrame({
            'member_id': ['M001'],
            'procedure_code': ['77067'],  # Screening mammography
            'service_date': [datetime(2024, 8, 15)]  # Within 2-year window
        })
        
        in_num, reason = self.bcs.is_in_numerator(procedures)
        self.assertTrue(in_num)
        self.assertIn("compliant_mammography", reason)
    
    def test_numerator_gap_no_mammography(self):
        """Test gap when no mammography"""
        procedures = pd.DataFrame({
            'member_id': ['M001'],
            'procedure_code': ['99213'],  # Office visit, not mammography
            'service_date': [datetime(2025, 3, 15)]
        })
        
        in_num, reason = self.bcs.is_in_numerator(procedures)
        self.assertFalse(in_num)
        self.assertIn("no_mammography", reason)
    
    def test_numerator_gap_old_mammography(self):
        """Test gap when mammography outside 2-year window"""
        procedures = pd.DataFrame({
            'member_id': ['M001'],
            'procedure_code': ['77067'],
            'service_date': [datetime(2022, 1, 15)]  # Too old
        })
        
        in_num, reason = self.bcs.is_in_numerator(procedures)
        self.assertFalse(in_num)
        self.assertIn("no_mammography_in_2yr_window", reason)


class TestCOLMeasure(unittest.TestCase):
    """Test suite for COL (Colorectal Cancer Screening) measure"""
    
    def setUp(self):
        """Set up test data"""
        self.col = COLMeasure(measurement_year=2025)
        
        # Base member data (eligible, age 60)
        self.eligible_member = pd.DataFrame({
            'member_id': ['M002'],
            'birth_date': [datetime(1965, 6, 15)],
            'gender': ['M'],
            'enrollment_months': [12]
        })
        
        # Base claims data with outpatient encounter
        self.eligible_claims = pd.DataFrame({
            'member_id': ['M002'],
            'claim_type': ['outpatient'],
            'service_date': [datetime(2025, 3, 15)],
            'diagnosis_code': ['Z00.00'],
            'provider_specialty': ['primary care']
        })
    
    def test_denominator_eligible_male(self):
        """Test eligible male is in denominator"""
        in_denom, reason = self.col.is_in_denominator(
            self.eligible_member,
            self.eligible_claims
        )
        self.assertTrue(in_denom)
        self.assertEqual(reason, "eligible")
    
    def test_denominator_eligible_female(self):
        """Test eligible female is in denominator"""
        female_member = self.eligible_member.copy()
        female_member['gender'] = 'F'
        
        in_denom, reason = self.col.is_in_denominator(
            female_member,
            self.eligible_claims
        )
        self.assertTrue(in_denom)
        self.assertEqual(reason, "eligible")
    
    def test_denominator_age_too_young(self):
        """Test age < 50 excluded"""
        young_member = self.eligible_member.copy()
        young_member['birth_date'] = datetime(1980, 1, 1)  # Age 45
        
        in_denom, reason = self.col.is_in_denominator(
            young_member,
            self.eligible_claims
        )
        self.assertFalse(in_denom)
        self.assertIn("age_too_young", reason)
    
    def test_denominator_age_too_old(self):
        """Test age > 75 excluded"""
        old_member = self.eligible_member.copy()
        old_member['birth_date'] = datetime(1945, 1, 1)  # Age 80
        
        in_denom, reason = self.col.is_in_denominator(
            old_member,
            self.eligible_claims
        )
        self.assertFalse(in_denom)
        self.assertIn("age_too_old", reason)
    
    def test_denominator_total_colectomy_excluded(self):
        """Test total colectomy exclusion"""
        colectomy_claims = self.eligible_claims.copy()
        colectomy_claims['diagnosis_code'] = 'Z90.49'
        
        in_denom, reason = self.col.is_in_denominator(
            self.eligible_member,
            colectomy_claims
        )
        self.assertFalse(in_denom)
        self.assertEqual(reason, "total_colectomy_history")
    
    def test_numerator_compliant_colonoscopy(self):
        """Test compliant with colonoscopy in 10-year window"""
        procedures = pd.DataFrame({
            'member_id': ['M002'],
            'procedure_code': ['45378'],  # Colonoscopy
            'service_date': [datetime(2020, 5, 15)]  # Within 10-year window
        })
        
        in_num, reason = self.col.is_in_numerator(procedures)
        self.assertTrue(in_num)
        self.assertIn("compliant_colonoscopy", reason)
    
    def test_numerator_compliant_fit_annual(self):
        """Test compliant with FIT in current year"""
        procedures = pd.DataFrame({
            'member_id': ['M002'],
            'procedure_code': ['82274'],  # FIT
            'service_date': [datetime(2025, 6, 15)]  # Current year
        })
        
        in_num, reason = self.col.is_in_numerator(procedures)
        self.assertTrue(in_num)
        self.assertIn("compliant_fit", reason)
    
    def test_numerator_compliant_cologuard(self):
        """Test compliant with Cologuard in 3-year window"""
        procedures = pd.DataFrame({
            'member_id': ['M002'],
            'procedure_code': ['81528'],  # Cologuard
            'service_date': [datetime(2023, 3, 15)]  # Within 3-year window
        })
        
        in_num, reason = self.col.is_in_numerator(procedures)
        self.assertTrue(in_num)
        self.assertIn("compliant_cologuard", reason)
    
    def test_numerator_compliant_flexible_sig(self):
        """Test compliant with flexible sigmoidoscopy in 5-year window"""
        procedures = pd.DataFrame({
            'member_id': ['M002'],
            'procedure_code': ['45330'],  # Flexible sigmoidoscopy
            'service_date': [datetime(2021, 8, 15)]  # Within 5-year window
        })
        
        in_num, reason = self.col.is_in_numerator(procedures)
        self.assertTrue(in_num)
        self.assertIn("compliant_flexible_sig", reason)
    
    def test_numerator_gap_no_screening(self):
        """Test gap when no screening"""
        procedures = pd.DataFrame({
            'member_id': ['M002'],
            'procedure_code': ['99213'],  # Office visit, not screening
            'service_date': [datetime(2025, 3, 15)]
        })
        
        in_num, reason = self.col.is_in_numerator(procedures)
        self.assertFalse(in_num)
        self.assertIn("no_screening", reason)
    
    def test_numerator_gap_colonoscopy_too_old(self):
        """Test gap when colonoscopy outside 10-year window"""
        procedures = pd.DataFrame({
            'member_id': ['M002'],
            'procedure_code': ['45378'],
            'service_date': [datetime(2010, 1, 15)]  # Too old (>10 years)
        })
        
        in_num, reason = self.col.is_in_numerator(procedures)
        self.assertFalse(in_num)
        self.assertIn("no_screening_in_lookback", reason)
    
    def test_numerator_fit_last_year_not_current(self):
        """Test gap when FIT from last year (needs annual)"""
        procedures = pd.DataFrame({
            'member_id': ['M002'],
            'procedure_code': ['82274'],
            'service_date': [datetime(2024, 6, 15)]  # Last year, not current
        })
        
        in_num, reason = self.col.is_in_numerator(procedures)
        self.assertFalse(in_num)
        self.assertIn("no_screening_in_lookback", reason)
    
    def test_colonoscopy_modality_check(self):
        """Test colonoscopy detection specifically"""
        procedures = pd.DataFrame({
            'member_id': ['M002'],
            'procedure_code': ['45378'],
            'service_date': [datetime(2020, 1, 1)]
        })
        
        has_colo, date = self.col.is_in_numerator_colonoscopy(procedures)
        self.assertTrue(has_colo)
        self.assertIsNotNone(date)
    
    def test_fit_modality_check(self):
        """Test FIT detection specifically"""
        procedures = pd.DataFrame({
            'member_id': ['M002'],
            'procedure_code': ['82274'],
            'service_date': [datetime(2025, 1, 1)]
        })
        
        has_fit, date = self.col.is_in_numerator_fit(procedures)
        self.assertTrue(has_fit)
        self.assertIsNotNone(date)
    
    def test_cologuard_modality_check(self):
        """Test Cologuard detection specifically"""
        procedures = pd.DataFrame({
            'member_id': ['M002'],
            'procedure_code': ['81528'],
            'service_date': [datetime(2023, 1, 1)]
        })
        
        has_cologuard, date = self.col.is_in_numerator_cologuard(procedures)
        self.assertTrue(has_cologuard)
        self.assertIsNotNone(date)


class TestCancerScreeningIntegration(unittest.TestCase):
    """Integration tests for cancer screening measures"""
    
    def test_bcs_gap_list_generation(self):
        """Test BCS gap list generation"""
        bcs = BCSMeasure(measurement_year=2025)
        
        # Create test population
        members = pd.DataFrame({
            'member_id': ['F001', 'F002', 'F003'],
            'birth_date': [datetime(1970, 1, 1), datetime(1965, 1, 1), datetime(1960, 1, 1)],
            'gender': ['F', 'F', 'F'],
            'enrollment_months': [12, 12, 12]
        })
        
        claims = pd.DataFrame({
            'member_id': ['F001', 'F001', 'F002', 'F002', 'F003', 'F003'],
            'claim_type': ['outpatient', 'outpatient', 'outpatient', 'outpatient', 'outpatient', 'outpatient'],
            'service_date': [datetime(2025, 1, 1)] * 6,
            'diagnosis_code': ['Z00.00'] * 6,
            'provider_specialty': ['primary care'] * 6
        })
        
        procedures = pd.DataFrame({
            'member_id': ['F001'],  # Only F001 has mammography
            'procedure_code': ['77067'],
            'service_date': [datetime(2024, 6, 1)]
        })
        
        gap_list = bcs.generate_gap_list(members, claims, procedures)
        
        # Should have 2 gaps (F002, F003)
        self.assertEqual(len(gap_list), 2)
        self.assertTrue(gap_list['has_gap'].all())
    
    def test_col_gap_list_generation(self):
        """Test COL gap list generation"""
        col = COLMeasure(measurement_year=2025)
        
        # Create test population
        members = pd.DataFrame({
            'member_id': ['P001', 'P002', 'P003'],
            'birth_date': [datetime(1970, 1, 1), datetime(1965, 1, 1), datetime(1960, 1, 1)],
            'gender': ['M', 'F', 'M'],
            'enrollment_months': [12, 12, 12]
        })
        
        claims = pd.DataFrame({
            'member_id': ['P001', 'P001', 'P002', 'P002', 'P003', 'P003'],
            'claim_type': ['outpatient', 'outpatient', 'outpatient', 'outpatient', 'outpatient', 'outpatient'],
            'service_date': [datetime(2025, 1, 1)] * 6,
            'diagnosis_code': ['Z00.00'] * 6,
            'provider_specialty': ['primary care'] * 6
        })
        
        procedures = pd.DataFrame({
            'member_id': ['P001'],  # Only P001 has colonoscopy
            'procedure_code': ['45378'],
            'service_date': [datetime(2020, 6, 1)]
        })
        
        gap_list = col.generate_gap_list(members, claims, procedures)
        
        # Should have 2 gaps (P002, P003)
        self.assertEqual(len(gap_list), 2)
        self.assertTrue(gap_list['has_gap'].all())


if __name__ == '__main__':
    unittest.main()


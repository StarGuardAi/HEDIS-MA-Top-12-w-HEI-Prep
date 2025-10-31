"""
Unit Tests for Diabetes Feature Engineering

Tests comprehensive feature engineering for diabetes-related HEDIS measures
with HIPAA compliance and HEDIS specification validation.
"""

import unittest
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

# Import modules to test
from src.data.features.diabetes_features import (
    DiabetesFeatureEngineer,
    DiabetesCodeSets,
    create_diabetes_features
)


class TestDiabetesCodeSets(unittest.TestCase):
    """Test diabetes and comorbidity code sets."""
    
    def test_diabetes_code_sets(self):
        """Test diabetes ICD-10 code sets."""
        # Should have Type 1 and Type 2 codes
        self.assertGreater(len(DiabetesCodeSets.TYPE1_DIABETES), 20)
        self.assertGreater(len(DiabetesCodeSets.TYPE2_DIABETES), 20)
        
        # Check specific codes
        self.assertIn('E10.9', DiabetesCodeSets.TYPE1_DIABETES)
        self.assertIn('E11.9', DiabetesCodeSets.TYPE2_DIABETES)
        
        # ALL_DIABETES should combine both
        self.assertEqual(
            DiabetesCodeSets.ALL_DIABETES,
            DiabetesCodeSets.TYPE1_DIABETES | DiabetesCodeSets.TYPE2_DIABETES
        )
    
    def test_comorbidity_code_sets(self):
        """Test comorbidity code sets."""
        # CKD codes
        self.assertIn('N18.3', DiabetesCodeSets.CKD_CODES)
        self.assertIn('N18.6', DiabetesCodeSets.CKD_CODES)  # ESRD
        
        # CVD codes
        self.assertIn('I25.10', DiabetesCodeSets.CVD_CODES)
        self.assertIn('I21.0', DiabetesCodeSets.CVD_CODES)  # MI
        
        # Retinopathy codes
        self.assertIn('E11.311', DiabetesCodeSets.RETINOPATHY_CODES)
        
        # Hypertension codes
        self.assertIn('I10', DiabetesCodeSets.HYPERTENSION_CODES)
        
        # Hyperlipidemia codes
        self.assertIn('E78.5', DiabetesCodeSets.HYPERLIPIDEMIA_CODES)


class TestDiabetesFeatureEngineer(unittest.TestCase):
    """Test diabetes feature engineering."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.measurement_year = 2025
        self.engineer = DiabetesFeatureEngineer(self.measurement_year)
        
        # Create sample data
        self.member_df = self._create_sample_members()
        self.claims_df = self._create_sample_claims()
        self.labs_df = self._create_sample_labs()
    
    def _create_sample_members(self):
        """Create sample member data."""
        my_end = datetime(2025, 12, 31)
        
        members = [
            {
                'member_id': 'M001',
                'birth_date': my_end - timedelta(days=50*365),  # Age 50
                'gender': 'M',
                'race': 'White',
                'state': 'CA',
            },
            {
                'member_id': 'M002',
                'birth_date': my_end - timedelta(days=65*365),  # Age 65
                'gender': 'F',
                'race': 'Black',
                'state': 'NY',
            },
            {
                'member_id': 'M003',
                'birth_date': my_end - timedelta(days=45*365),  # Age 45
                'gender': 'F',
                'race': 'Hispanic',
                'state': 'TX',
            },
        ]
        
        return pd.DataFrame(members)
    
    def _create_sample_claims(self):
        """Create sample claims data."""
        claims = [
            # M001 - Type 2 diabetes with CKD
            {
                'member_id': 'M001',
                'service_date': datetime(2024, 3, 15),
                'claim_type': 'outpatient',
                'diagnosis_code': 'E11.9',
            },
            {
                'member_id': 'M001',
                'service_date': datetime(2024, 6, 20),
                'claim_type': 'outpatient',
                'diagnosis_code': 'E11.22',  # Diabetes with CKD
            },
            {
                'member_id': 'M001',
                'service_date': datetime(2025, 4, 10),
                'claim_type': 'outpatient',
                'diagnosis_code': 'N18.3',  # CKD Stage 3
            },
            {
                'member_id': 'M001',
                'service_date': datetime(2025, 5, 15),
                'claim_type': 'outpatient',
                'diagnosis_code': 'I10',  # Hypertension
            },
            
            # M002 - Type 1 diabetes with retinopathy
            {
                'member_id': 'M002',
                'service_date': datetime(2025, 2, 10),
                'claim_type': 'inpatient',
                'diagnosis_code': 'E10.9',
            },
            {
                'member_id': 'M002',
                'service_date': datetime(2025, 4, 20),
                'claim_type': 'outpatient',
                'diagnosis_code': 'E10.311',  # Type 1 with retinopathy
            },
            {
                'member_id': 'M002',
                'service_date': datetime(2025, 3, 1),
                'claim_type': 'emergency',
                'diagnosis_code': 'E10.9',
            },
            
            # M003 - Type 2 diabetes with CVD and hyperlipidemia
            {
                'member_id': 'M003',
                'service_date': datetime(2024, 8, 5),
                'claim_type': 'outpatient',
                'diagnosis_code': 'E11.9',
            },
            {
                'member_id': 'M003',
                'service_date': datetime(2025, 1, 15),
                'claim_type': 'outpatient',
                'diagnosis_code': 'E11.9',
            },
            {
                'member_id': 'M003',
                'service_date': datetime(2025, 3, 10),
                'claim_type': 'inpatient',
                'diagnosis_code': 'I25.10',  # CAD
            },
            {
                'member_id': 'M003',
                'service_date': datetime(2025, 6, 20),
                'claim_type': 'outpatient',
                'diagnosis_code': 'E78.5',  # Hyperlipidemia
            },
        ]
        
        return pd.DataFrame(claims)
    
    def _create_sample_labs(self):
        """Create sample lab data."""
        labs = [
            # M001 - Has HbA1c and eGFR
            {
                'member_id': 'M001',
                'test_date': datetime(2024, 6, 15),
                'loinc_code': '4548-4',  # HbA1c
                'result_value': 7.5,
            },
            {
                'member_id': 'M001',
                'test_date': datetime(2025, 3, 20),
                'loinc_code': '4548-4',  # HbA1c (more recent)
                'result_value': 7.2,
            },
            {
                'member_id': 'M001',
                'test_date': datetime(2025, 3, 20),
                'loinc_code': '48642-3',  # eGFR
                'result_value': 55.0,
            },
            
            # M002 - Has HbA1c only
            {
                'member_id': 'M002',
                'test_date': datetime(2025, 2, 15),
                'loinc_code': '4548-4',  # HbA1c
                'result_value': 8.5,
            },
            
            # M003 - No labs in prior year, but has older lab
            {
                'member_id': 'M003',
                'test_date': datetime(2023, 5, 10),
                'loinc_code': '4548-4',  # HbA1c (too old)
                'result_value': 9.0,
            },
        ]
        
        return pd.DataFrame(labs)
    
    def test_initialization(self):
        """Test feature engineer initialization."""
        self.assertEqual(self.engineer.measurement_year, 2025)
        self.assertEqual(self.engineer.my_start, datetime(2025, 1, 1))
        self.assertEqual(self.engineer.my_end, datetime(2025, 12, 31))
        self.assertEqual(self.engineer.lookback_start, datetime(2023, 1, 1))
    
    def test_hash_member_id(self):
        """Test PHI-safe member ID hashing."""
        hashed = self.engineer._hash_member_id('TEST123')
        
        # Should return 8-character hash
        self.assertEqual(len(hashed), 8)
        
        # Should be consistent
        hashed2 = self.engineer._hash_member_id('TEST123')
        self.assertEqual(hashed, hashed2)
        
        # Different IDs should hash differently
        hashed3 = self.engineer._hash_member_id('TEST456')
        self.assertNotEqual(hashed, hashed3)
    
    def test_demographic_features(self):
        """Test demographic feature creation."""
        result = self.engineer.create_demographic_features(self.member_df.copy())
        
        # Should have age features
        self.assertIn('age_at_my_end', result.columns)
        self.assertIn('age_group', result.columns)
        
        # Check age calculation
        m001 = result[result['member_id'] == 'M001'].iloc[0]
        self.assertEqual(m001['age_at_my_end'], 50)
        
        # Should have gender features
        self.assertIn('gender_male', result.columns)
        self.assertIn('gender_female', result.columns)
        self.assertEqual(m001['gender_male'], 1)
        self.assertEqual(m001['gender_female'], 0)
        
        # Should have race features
        self.assertTrue(any(col.startswith('race_') for col in result.columns))
        
        # Should have region features
        self.assertIn('region_west', result.columns)  # CA is west
        self.assertEqual(m001['region_west'], 1)
    
    def test_diabetes_diagnosis_features(self):
        """Test diabetes diagnosis feature creation."""
        result = self.engineer.create_diabetes_diagnosis_features(
            self.member_df.copy(),
            self.claims_df.copy()
        )
        
        # Should have diabetes type features
        self.assertIn('diabetes_type1', result.columns)
        self.assertIn('diabetes_type2', result.columns)
        
        # M001 should have Type 2
        m001 = result[result['member_id'] == 'M001'].iloc[0]
        self.assertEqual(m001['diabetes_type2'], 1)
        self.assertEqual(m001['diabetes_type1'], 0)
        
        # M002 should have Type 1
        m002 = result[result['member_id'] == 'M002'].iloc[0]
        self.assertEqual(m002['diabetes_type1'], 1)
        self.assertEqual(m002['diabetes_type2'], 0)
        
        # Should have duration feature
        self.assertIn('diabetes_duration_years', result.columns)
        self.assertGreaterEqual(m001['diabetes_duration_years'], 0)
        
        # Should have diagnosis count
        self.assertIn('diabetes_dx_count', result.columns)
        self.assertGreater(m001['diabetes_dx_count'], 0)
    
    def test_comorbidity_features(self):
        """Test comorbidity feature creation."""
        result = self.engineer.create_comorbidity_features(
            self.member_df.copy(),
            self.claims_df.copy()
        )
        
        # Should have comorbidity flags
        comorbidity_cols = ['has_ckd', 'has_cvd', 'has_retinopathy', 
                           'has_neuropathy', 'has_hypertension', 'has_hyperlipidemia']
        for col in comorbidity_cols:
            self.assertIn(col, result.columns)
        
        # M001 should have CKD and hypertension
        m001 = result[result['member_id'] == 'M001'].iloc[0]
        self.assertEqual(m001['has_ckd'], 1)
        self.assertEqual(m001['has_hypertension'], 1)
        
        # M002 should have retinopathy
        m002 = result[result['member_id'] == 'M002'].iloc[0]
        self.assertEqual(m002['has_retinopathy'], 1)
        
        # M003 should have CVD and hyperlipidemia
        m003 = result[result['member_id'] == 'M003'].iloc[0]
        self.assertEqual(m003['has_cvd'], 1)
        self.assertEqual(m003['has_hyperlipidemia'], 1)
        
        # Should have comorbidity count
        self.assertIn('comorbidity_count', result.columns)
        self.assertEqual(m001['comorbidity_count'], 2)  # CKD + HTN
    
    def test_lab_history_features(self):
        """Test lab history feature creation."""
        result = self.engineer.create_lab_history_features(
            self.member_df.copy(),
            self.labs_df.copy()
        )
        
        # Should have prior year test flags
        self.assertIn('had_hba1c_prior_year', result.columns)
        self.assertIn('had_egfr_prior_year', result.columns)
        self.assertIn('had_acr_prior_year', result.columns)
        
        # Should have most recent values
        self.assertIn('most_recent_hba1c', result.columns)
        self.assertIn('most_recent_egfr', result.columns)
        
        # Should have test count
        self.assertIn('lab_test_count_2yr', result.columns)
        
        # M001 should have recent HbA1c and eGFR
        m001 = result[result['member_id'] == 'M001'].iloc[0]
        self.assertIsNotNone(m001['most_recent_hba1c'])
        self.assertEqual(m001['most_recent_hba1c'], 7.2)  # Most recent
        self.assertIsNotNone(m001['most_recent_egfr'])
        self.assertEqual(m001['most_recent_egfr'], 55.0)
    
    def test_lab_history_features_no_labs(self):
        """Test lab history features when no labs available."""
        result = self.engineer.create_lab_history_features(
            self.member_df.copy(),
            labs_df=None
        )
        
        # Should create default features
        self.assertIn('had_hba1c_prior_year', result.columns)
        self.assertEqual(result['had_hba1c_prior_year'].sum(), 0)
        
        # Should handle gracefully
        self.assertEqual(len(result), len(self.member_df))
    
    def test_utilization_features(self):
        """Test utilization feature creation."""
        result = self.engineer.create_utilization_features(
            self.member_df.copy(),
            self.claims_df.copy()
        )
        
        # Should have utilization counts
        util_cols = ['ed_visits', 'inpatient_admits', 'outpatient_visits', 'total_visits']
        for col in util_cols:
            self.assertIn(col, result.columns)
        
        # Should have high utilizer flags
        self.assertIn('high_ed_user', result.columns)
        self.assertIn('had_inpatient', result.columns)
        
        # M002 should have ED visit
        m002 = result[result['member_id'] == 'M002'].iloc[0]
        self.assertGreater(m002['ed_visits'], 0)
        
        # M003 should have inpatient admission
        m003 = result[result['member_id'] == 'M003'].iloc[0]
        self.assertGreater(m003['inpatient_admits'], 0)
        self.assertEqual(m003['had_inpatient'], 1)
    
    def test_create_all_features(self):
        """Test complete feature engineering pipeline."""
        result = self.engineer.create_all_features(
            self.member_df.copy(),
            self.claims_df.copy(),
            self.labs_df.copy()
        )
        
        # Should have all members
        self.assertEqual(len(result), len(self.member_df))
        
        # Should have many features
        feature_cols = [col for col in result.columns if col != 'member_id']
        self.assertGreater(len(feature_cols), 30)
        
        # Should have no nulls in key features (or handled appropriately)
        self.assertFalse(result['age_at_my_end'].isnull().any())
        self.assertFalse(result['diabetes_type1'].isnull().any())
        self.assertFalse(result['has_ckd'].isnull().any())
        
        # All utilization features should be non-negative
        self.assertTrue((result['ed_visits'] >= 0).all())
        self.assertTrue((result['inpatient_admits'] >= 0).all())
    
    def test_convenience_function(self):
        """Test convenience function for feature creation."""
        result = create_diabetes_features(
            self.member_df.copy(),
            self.claims_df.copy(),
            self.labs_df.copy(),
            measurement_year=2025
        )
        
        # Should work same as class method
        self.assertEqual(len(result), len(self.member_df))
        self.assertIn('age_at_my_end', result.columns)
        self.assertIn('diabetes_type1', result.columns)
    
    def test_missing_data_handling(self):
        """Test handling of missing data."""
        # Create member with no claims
        members_with_no_data = pd.DataFrame([{
            'member_id': 'M999',
            'birth_date': datetime(1975, 6, 15),
            'gender': 'M',
            'race': 'White',
            'state': 'CA',
        }])
        
        result = self.engineer.create_all_features(
            members_with_no_data,
            self.claims_df.copy(),
            self.labs_df.copy()
        )
        
        # Should handle gracefully
        self.assertEqual(len(result), 1)
        
        # Diabetes features should default to 0
        self.assertEqual(result.iloc[0]['diabetes_type1'], 0)
        self.assertEqual(result.iloc[0]['diabetes_type2'], 0)
        
        # Comorbidity features should default to 0
        self.assertEqual(result.iloc[0]['has_ckd'], 0)
    
    def test_phi_protection(self):
        """Test that no raw member IDs appear in feature names."""
        result = self.engineer.create_all_features(
            self.member_df.copy(),
            self.claims_df.copy(),
            self.labs_df.copy()
        )
        
        # Feature columns should not contain actual member IDs
        feature_cols = [col for col in result.columns if col != 'member_id']
        
        for member_id in self.member_df['member_id']:
            for col in feature_cols:
                self.assertNotIn(str(member_id), str(col))


class TestHEDISCompliance(unittest.TestCase):
    """Test HEDIS specification compliance."""
    
    def test_age_calculation_dec_31(self):
        """Test that age is calculated at Dec 31 of measurement year."""
        engineer = DiabetesFeatureEngineer(2025)
        
        # Age should be calculated at Dec 31, 2025
        self.assertEqual(engineer.my_end, datetime(2025, 12, 31))
        
        # Member born Jan 1, 1975 should be 50 on Dec 31, 2025
        member = pd.DataFrame([{
            'member_id': 'TEST',
            'birth_date': datetime(1975, 1, 1),
            'gender': 'M',
            'race': 'White',
            'state': 'CA',
        }])
        
        result = engineer.create_demographic_features(member)
        self.assertEqual(result.iloc[0]['age_at_my_end'], 50)
    
    def test_lookback_period(self):
        """Test 2-year lookback period for features."""
        engineer = DiabetesFeatureEngineer(2025)
        
        # Lookback should start Jan 1, 2023
        self.assertEqual(engineer.lookback_start, datetime(2023, 1, 1))
        
        # Should be 2 years before measurement year
        days_diff = (engineer.my_start - engineer.lookback_start).days
        self.assertAlmostEqual(days_diff, 730, delta=2)  # ~2 years


if __name__ == '__main__':
    unittest.main()


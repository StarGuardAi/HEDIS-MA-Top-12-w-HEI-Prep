"""
Unit Tests for Cardiovascular Feature Engineering

Tests the cardiovascular_features module for Tier 2 measures.

Author: Analytics Team
Date: October 23, 2025
"""

import unittest
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from src.data.features.cardiovascular_features import (
    create_cardiovascular_features,
    validate_cardiovascular_features,
    get_cbp_features,
    get_supd_features,
    get_pdc_rasa_features,
    get_pdc_sta_features
)


class TestCardiovascularFeatures(unittest.TestCase):
    """Test suite for cardiovascular feature engineering"""
    
    def setUp(self):
        """Set up test data"""
        self.measurement_year = 2025
        
        # Create synthetic claims data
        self.claims_data = pd.DataFrame({
            'member_id': [1, 1, 1, 2, 2, 3, 3, 3],
            'diagnosis_code': ['I10', 'E11.9', 'I50.9', 'I10', 'I21.9', 'I63.9', 'N18.3', 'I20.0'],
            'procedure_code': ['99213', '99214', '99215', '92920', '99213', '99214', '99215', '93000'],
            'service_date': [
                '2025-01-15', '2025-02-20', '2025-03-10',
                '2025-01-20', '2024-12-15', '2024-11-10',
                '2025-01-05', '2025-02-15'
            ],
            'claim_type': ['outpatient', 'outpatient', 'outpatient', 'outpatient', 
                          'inpatient', 'emergency', 'outpatient', 'outpatient'],
            'provider_specialty': ['primary_care', 'primary_care', 'cardiology', 
                                  'cardiology', 'cardiology', 'emergency', 'nephrology', 'cardiology']
        })
        
        # Create synthetic pharmacy data
        self.pharmacy_data = pd.DataFrame({
            'member_id': [1, 1, 1, 2, 2, 3],
            'medication_name': ['lisinopril 10mg', 'atorvastatin 40mg', 'metoprolol 50mg',
                              'losartan 50mg', 'rosuvastatin 20mg', 'amlodipine 5mg'],
            'fill_date': ['2025-01-10', '2025-01-15', '2025-02-10',
                         '2025-01-20', '2025-02-15', '2025-03-01'],
            'days_supply': [30, 30, 30, 30, 30, 30]
        })
        
        # Create synthetic vitals data
        self.vitals_data = pd.DataFrame({
            'member_id': [1, 1, 2, 2, 3],
            'reading_date': ['2025-01-15', '2025-03-10', '2025-01-20', '2025-02-25', '2025-01-05'],
            'systolic_bp': [138, 142, 135, 128, 155],
            'diastolic_bp': [88, 92, 85, 80, 95]
        })
    
    def test_create_cardiovascular_features_basic(self):
        """Test basic cardiovascular feature creation"""
        features = create_cardiovascular_features(
            claims_df=self.claims_data,
            pharmacy_df=self.pharmacy_data,
            vitals_df=self.vitals_data,
            measurement_year=self.measurement_year
        )
        
        # Check output structure
        self.assertIsInstance(features, pd.DataFrame)
        self.assertEqual(len(features), 3)  # 3 unique members
        self.assertIn('member_id_hash', features.columns)
        
        # Check that member_id is hashed (PHI protection)
        self.assertTrue(all(features['member_id_hash'].str.len() == 16))
        self.assertNotIn('member_id', features.columns)
    
    def test_htn_features(self):
        """Test HTN-specific features"""
        features = create_cardiovascular_features(
            claims_df=self.claims_data,
            pharmacy_df=self.pharmacy_data,
            vitals_df=self.vitals_data
        )
        
        # Member 1 has HTN diagnosis (I10)
        member1 = features.iloc[0]
        self.assertEqual(member1['has_htn_diagnosis'], 1)
        self.assertGreater(member1['htn_diagnosis_count'], 0)
        
        # Check BP medication features
        self.assertGreater(member1['bp_med_fills_count'], 0)
        self.assertGreater(member1['bp_med_classes_count'], 0)
    
    def test_cvd_features(self):
        """Test CVD/ASCVD features"""
        features = create_cardiovascular_features(
            claims_df=self.claims_data,
            pharmacy_df=self.pharmacy_data,
            vitals_df=self.vitals_data
        )
        
        # Member 2 has MI history (I21.9)
        member2 = features.iloc[1]
        self.assertEqual(member2['has_mi_history'], 1)
        self.assertEqual(member2['has_ascvd'], 1)
        
        # Member 3 has stroke history (I63.9)
        member3 = features.iloc[2]
        self.assertEqual(member3['has_stroke_history'], 1)
        self.assertEqual(member3['has_ascvd'], 1)
    
    def test_medication_features(self):
        """Test medication-related features"""
        features = create_cardiovascular_features(
            claims_df=self.claims_data,
            pharmacy_df=self.pharmacy_data,
            vitals_df=self.vitals_data
        )
        
        # Member 1 has statin (atorvastatin)
        member1 = features.iloc[0]
        self.assertEqual(member1['has_statin_rx'], 1)
        self.assertGreater(member1['statin_fills_count'], 0)
        
        # Member 1 has ACE/ARB (lisinopril)
        self.assertEqual(member1['has_ace_arb_rx'], 1)
        self.assertGreater(member1['ace_arb_fills_count'], 0)
    
    def test_diabetes_overlap_features(self):
        """Test shared diabetes features"""
        features = create_cardiovascular_features(
            claims_df=self.claims_data,
            pharmacy_df=self.pharmacy_data,
            vitals_df=self.vitals_data
        )
        
        # Member 1 has diabetes (E11.9)
        member1 = features.iloc[0]
        self.assertEqual(member1['has_diabetes'], 1)
        self.assertEqual(member1['in_tier1_population'], 1)
    
    def test_bp_vitals_features(self):
        """Test BP vitals features"""
        features = create_cardiovascular_features(
            claims_df=self.claims_data,
            pharmacy_df=self.pharmacy_data,
            vitals_df=self.vitals_data
        )
        
        # Member 1 has BP readings
        member1 = features.iloc[0]
        self.assertGreater(member1['most_recent_systolic'], 0)
        self.assertGreater(member1['most_recent_diastolic'], 0)
        self.assertGreater(member1['avg_systolic_bp_year'], 0)
        
        # Member 3 has uncontrolled BP (155/95)
        member3 = features.iloc[2]
        self.assertGreater(member3['uncontrolled_bp_episodes'], 0)
    
    def test_specialist_visits_features(self):
        """Test cardiology and specialist visit features"""
        features = create_cardiovascular_features(
            claims_df=self.claims_data,
            pharmacy_df=self.pharmacy_data,
            vitals_df=self.vitals_data
        )
        
        # Member 1 has cardiology visit
        member1 = features.iloc[0]
        self.assertGreaterEqual(member1['cardiology_visits_count'], 1)
    
    def test_complication_features(self):
        """Test complication flags"""
        features = create_cardiovascular_features(
            claims_df=self.claims_data,
            pharmacy_df=self.pharmacy_data,
            vitals_df=self.vitals_data
        )
        
        # Member 1 has CHF (I50.9)
        member1 = features.iloc[0]
        self.assertEqual(member1['has_chf'], 1)
        
        # Member 3 has CKD (N18.3)
        member3 = features.iloc[2]
        self.assertEqual(member3['has_ckd'], 1)
    
    def test_missing_pharmacy_data(self):
        """Test handling of missing pharmacy data"""
        features = create_cardiovascular_features(
            claims_df=self.claims_data,
            pharmacy_df=None,  # No pharmacy data
            vitals_df=self.vitals_data
        )
        
        # Should not error, should set medication features to 0
        self.assertEqual(features['has_statin_rx'].sum(), 0)
        self.assertEqual(features['has_ace_arb_rx'].sum(), 0)
        self.assertEqual(features['total_bp_medications'].sum(), 0)
    
    def test_missing_vitals_data(self):
        """Test handling of missing vitals data"""
        features = create_cardiovascular_features(
            claims_df=self.claims_data,
            pharmacy_df=self.pharmacy_data,
            vitals_df=None  # No vitals data
        )
        
        # Should not error, should set BP features to 0
        self.assertEqual(features['most_recent_systolic'].sum(), 0)
        self.assertEqual(features['most_recent_diastolic'].sum(), 0)
        self.assertEqual(features['uncontrolled_bp_episodes'].sum(), 0)
    
    def test_validate_cardiovascular_features(self):
        """Test feature validation function"""
        features = create_cardiovascular_features(
            claims_df=self.claims_data,
            pharmacy_df=self.pharmacy_data,
            vitals_df=self.vitals_data
        )
        
        validation = validate_cardiovascular_features(features)
        
        # Check validation output structure
        self.assertIn('total_members', validation)
        self.assertIn('has_htn_diagnosis', validation)
        self.assertIn('has_ascvd', validation)
        self.assertIn('has_diabetes', validation)
        self.assertIn('htn_diabetes_overlap', validation)
        
        # Check counts
        self.assertEqual(validation['total_members'], 3)
        self.assertGreater(validation['has_htn_diagnosis'], 0)
    
    def test_get_cbp_features(self):
        """Test CBP-specific feature subset"""
        features = create_cardiovascular_features(
            claims_df=self.claims_data,
            pharmacy_df=self.pharmacy_data,
            vitals_df=self.vitals_data
        )
        
        cbp_features = get_cbp_features(features)
        
        # Check that CBP-relevant columns are present
        self.assertIn('has_htn_diagnosis', cbp_features.columns)
        self.assertIn('most_recent_systolic', cbp_features.columns)
        self.assertIn('bp_med_classes_count', cbp_features.columns)
        
        # Check that subset is smaller than full feature set
        self.assertLess(len(cbp_features.columns), len(features.columns))
    
    def test_get_supd_features(self):
        """Test SUPD-specific feature subset"""
        features = create_cardiovascular_features(
            claims_df=self.claims_data,
            pharmacy_df=self.pharmacy_data,
            vitals_df=self.vitals_data
        )
        
        supd_features = get_supd_features(features)
        
        # Check that SUPD-relevant columns are present
        self.assertIn('has_diabetes', supd_features.columns)
        self.assertIn('has_ascvd', supd_features.columns)
        self.assertIn('has_statin_rx', supd_features.columns)
    
    def test_get_pdc_rasa_features(self):
        """Test PDC-RASA-specific feature subset"""
        features = create_cardiovascular_features(
            claims_df=self.claims_data,
            pharmacy_df=self.pharmacy_data,
            vitals_df=self.vitals_data
        )
        
        pdc_rasa_features = get_pdc_rasa_features(features)
        
        # Check that PDC-RASA-relevant columns are present
        self.assertIn('has_ace_arb_rx', pdc_rasa_features.columns)
        self.assertIn('ace_arb_fills_count', pdc_rasa_features.columns)
        self.assertIn('avg_refill_gap_days', pdc_rasa_features.columns)
    
    def test_get_pdc_sta_features(self):
        """Test PDC-STA-specific feature subset"""
        features = create_cardiovascular_features(
            claims_df=self.claims_data,
            pharmacy_df=self.pharmacy_data,
            vitals_df=self.vitals_data
        )
        
        pdc_sta_features = get_pdc_sta_features(features)
        
        # Check that PDC-STA-relevant columns are present
        self.assertIn('has_statin_rx', pdc_sta_features.columns)
        self.assertIn('statin_fills_count', pdc_sta_features.columns)
        self.assertIn('has_high_potency_statin', pdc_sta_features.columns)
    
    def test_phi_protection(self):
        """Test that PHI is properly protected"""
        features = create_cardiovascular_features(
            claims_df=self.claims_data,
            pharmacy_df=self.pharmacy_data,
            vitals_df=self.vitals_data
        )
        
        # Member IDs should be hashed
        self.assertNotIn('member_id', features.columns)
        self.assertIn('member_id_hash', features.columns)
        
        # No raw member IDs in any values
        for col in features.columns:
            if features[col].dtype == 'object':
                self.assertFalse(any(features[col].astype(str).str.isdigit().fillna(False)))
    
    def test_feature_counts(self):
        """Test that we have the expected number of features"""
        features = create_cardiovascular_features(
            claims_df=self.claims_data,
            pharmacy_df=self.pharmacy_data,
            vitals_df=self.vitals_data
        )
        
        # Should have 35+ features plus member_id_hash
        self.assertGreaterEqual(len(features.columns), 36)
    
    def test_empty_claims_handling(self):
        """Test error handling for empty claims data"""
        empty_claims = pd.DataFrame()
        
        with self.assertRaises(ValueError):
            create_cardiovascular_features(
                claims_df=empty_claims,
                pharmacy_df=self.pharmacy_data,
                vitals_df=self.vitals_data
            )
    
    def test_missing_member_id_column(self):
        """Test error handling for missing member_id column"""
        bad_claims = self.claims_data.rename(columns={'member_id': 'patient_id'})
        
        with self.assertRaises(ValueError):
            create_cardiovascular_features(
                claims_df=bad_claims,
                pharmacy_df=self.pharmacy_data,
                vitals_df=self.vitals_data
            )


if __name__ == '__main__':
    unittest.main()


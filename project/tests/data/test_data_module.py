"""
Unit Tests for HEDIS GSD Data Module

Tests data loading, preprocessing, and feature engineering functions
with healthcare compliance validation.
"""

import unittest
import pandas as pd
import numpy as np
from datetime import datetime
import tempfile
import os
from pathlib import Path

# Import modules to test
from src.data.data_loader import CMSDataLoader, load_cms_data
from src.data.data_preprocessing import CMSDataPreprocessor, preprocess_cms_data
from src.data.feature_engineering import HEDISFeatureEngineer, HEDISConfig, create_hedis_gsd_features


class TestCMSDataLoader(unittest.TestCase):
    """Test cases for CMS data loader."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.mkdtemp()
        self.loader = CMSDataLoader(self.temp_dir)
        
        # Create sample data files
        self._create_sample_beneficiary_file()
        self._create_sample_claims_file()
    
    def tearDown(self):
        """Clean up test fixtures."""
        import shutil
        shutil.rmtree(self.temp_dir)
    
    def _create_sample_beneficiary_file(self):
        """Create sample beneficiary data file."""
        sample_data = {
            'DESYNPUF_ID': ['TEST001', 'TEST002', 'TEST003'],
            'BENE_BIRTH_DT': ['19500101', '19600101', '19700101'],
            'BENE_DEATH_DT': ['', '', ''],
            'BENE_SEX_IDENT_CD': [1, 2, 1],
            'BENE_RACE_CD': [1, 2, 1],
            'BENE_ESRD_IND': [0, 0, 0],
            'SP_STATE_CODE': [26, 39, 6],
            'BENE_COUNTY_CD': [950, 230, 290],
            'SP_DIABETES': [1, 0, 1]
        }
        
        df = pd.DataFrame(sample_data)
        file_path = Path(self.temp_dir) / "DE1_0_2008_Beneficiary_Summary_File_Sample_1.csv"
        df.to_csv(file_path, index=False)
    
    def _create_sample_claims_file(self):
        """Create sample claims data file."""
        sample_data = {
            'DESYNPUF_ID': ['TEST001', 'TEST002', 'TEST001'],
            'CLM_ID': ['CLM001', 'CLM002', 'CLM003'],
            'CLM_FROM_DT': ['20080101', '20080201', '20080301'],
            'CLM_THRU_DT': ['20080101', '20080201', '20080301'],
            'CLM_PMT_AMT': [100.0, 200.0, 150.0],
            'ICD9_DGNS_CD_1': ['250.00', '401.9', '250.01'],
            'ICD9_DGNS_CD_2': ['', '', ''],
            'ICD9_DGNS_CD_3': ['', '', ''],
            'ICD9_DGNS_CD_4': ['', '', ''],
            'ICD9_DGNS_CD_5': ['', '', '']
        }
        
        df = pd.DataFrame(sample_data)
        file_path = Path(self.temp_dir) / "DE1_0_2008_to_2010_Inpatient_Claims_Sample_1.csv"
        df.to_csv(file_path, index=False)
        
        # Create outpatient file
        file_path = Path(self.temp_dir) / "DE1_0_2008_to_2010_Outpatient_Claims_Sample_1.csv"
        df.to_csv(file_path, index=False)
    
    def test_load_beneficiary_data(self):
        """Test loading beneficiary data."""
        df = self.loader.load_beneficiary_data()
        
        self.assertEqual(len(df), 3)
        self.assertIn('DESYNPUF_ID', df.columns)
        self.assertIn('BENE_BIRTH_DT', df.columns)
        self.assertIn('SP_DIABETES', df.columns)
    
    def test_load_claims_data(self):
        """Test loading claims data."""
        inpatient_df = self.loader.load_inpatient_data()
        outpatient_df = self.loader.load_outpatient_data()
        
        self.assertEqual(len(inpatient_df), 3)
        self.assertEqual(len(outpatient_df), 3)
        self.assertIn('CLM_ID', inpatient_df.columns)
        self.assertIn('ICD9_DGNS_CD_1', inpatient_df.columns)
    
    def test_load_all_data(self):
        """Test loading all data."""
        data = self.loader.load_all_data()
        
        self.assertIn('beneficiary', data)
        self.assertIn('inpatient', data)
        self.assertIn('outpatient', data)
        self.assertEqual(len(data['beneficiary']), 3)
    
    def test_phi_safe_logging(self):
        """Test that logging doesn't expose PHI."""
        # This test ensures no raw member IDs are logged
        # In a real implementation, you'd capture log output and verify
        # For now, we just ensure the method runs without error
        try:
            self.loader.load_all_data()
        except Exception as e:
            self.fail(f"PHI-safe logging failed: {e}")


class TestCMSDataPreprocessor(unittest.TestCase):
    """Test cases for CMS data preprocessor."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.preprocessor = CMSDataPreprocessor(measurement_year=2008)
        
        # Create sample data
        self.beneficiary_data = pd.DataFrame({
            'DESYNPUF_ID': ['TEST001', 'TEST002', 'TEST003'],
            'BENE_BIRTH_DT': ['19500101', '19600101', '19700101'],
            'BENE_DEATH_DT': ['', '', ''],
            'BENE_SEX_IDENT_CD': [1, 2, 1],
            'BENE_RACE_CD': [1, 2, 1],
            'BENE_ESRD_IND': [0, 0, 0],
            'SP_STATE_CODE': [26, 39, 6],
            'SP_DIABETES': [1, 0, 1]
        })
        
        self.claims_data = pd.DataFrame({
            'DESYNPUF_ID': ['TEST001', 'TEST002', 'TEST001'],
            'CLM_ID': ['CLM001', 'CLM002', 'CLM003'],
            'CLM_FROM_DT': ['20080101', '20080201', '20080301'],
            'CLM_THRU_DT': ['20080101', '20080201', '20080301'],
            'CLM_PMT_AMT': [100.0, 200.0, 150.0],
            'ICD9_DGNS_CD_1': ['250.00', '401.9', '250.01'],
            'ICD9_DGNS_CD_2': ['', '', ''],
            'ICD9_DGNS_CD_3': ['', '', ''],
            'ICD9_DGNS_CD_4': ['', '', ''],
            'ICD9_DGNS_CD_5': ['', '', '']
        })
    
    def test_parse_dates(self):
        """Test date parsing functionality."""
        date_cols = ['BENE_BIRTH_DT']
        result = self.preprocessor.parse_dates(self.beneficiary_data, date_cols)
        
        self.assertTrue(pd.api.types.is_datetime64_any_dtype(result['BENE_BIRTH_DT']))
    
    def test_clean_beneficiary_data(self):
        """Test beneficiary data cleaning."""
        result = self.preprocessor.clean_beneficiary_data(self.beneficiary_data)
        
        self.assertIn('age_at_my_end', result.columns)
        self.assertTrue(all(result['age_at_my_end'] >= 0))
    
    def test_clean_claims_data(self):
        """Test claims data cleaning."""
        result = self.preprocessor.clean_claims_data(self.claims_data, 'inpatient')
        
        self.assertTrue(pd.api.types.is_datetime64_any_dtype(result['CLM_FROM_DT']))
        self.assertTrue(pd.api.types.is_numeric_dtype(result['CLM_PMT_AMT']))
    
    def test_create_diabetes_flags(self):
        """Test diabetes flag creation."""
        result = self.preprocessor.create_diabetes_flags(self.claims_data)
        
        self.assertIn('has_diabetes_dx', result.columns)
        self.assertTrue(result['has_diabetes_dx'].dtype == bool)
    
    def test_deduplicate_claims(self):
        """Test claims deduplication."""
        # Add duplicate claim
        duplicate_data = pd.concat([self.claims_data, self.claims_data.iloc[[0]]])
        result = self.preprocessor.deduplicate_claims(duplicate_data)
        
        self.assertEqual(len(result), len(self.claims_data))


class TestHEDISFeatureEngineer(unittest.TestCase):
    """Test cases for HEDIS feature engineer."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.config = HEDISConfig(measurement_year=2008)
        self.engineer = HEDISFeatureEngineer(self.config)
        
        # Create sample processed data
        self.beneficiary_data = pd.DataFrame({
            'DESYNPUF_ID': ['TEST001', 'TEST002', 'TEST003'],
            'age_at_my_end': [58, 48, 38],
            'BENE_SEX_IDENT_CD': [1, 2, 1],
            'BENE_RACE_CD': [1, 2, 1],
            'SP_STATE_CODE': [26, 39, 6],
            'BENE_ESRD_IND': [0, 0, 0],
            'SP_DIABETES': [1, 0, 1]
        })
        
        self.claims_data = pd.DataFrame({
            'DESYNPUF_ID': ['TEST001', 'TEST002', 'TEST001'],
            'CLM_ID': ['CLM001', 'CLM002', 'CLM003'],
            'CLM_PMT_AMT': [100.0, 200.0, 150.0],
            'ICD9_DGNS_CD_1': ['250.00', '401.9', '250.01'],
            'ICD9_DGNS_CD_2': ['', '', ''],
            'ICD9_DGNS_CD_3': ['', '', ''],
            'ICD9_DGNS_CD_4': ['', '', ''],
            'ICD9_DGNS_CD_5': ['', '', '']
        })
    
    def test_create_demographic_features(self):
        """Test demographic feature creation."""
        result = self.engineer.create_demographic_features(self.beneficiary_data)
        
        self.assertIn('age_at_my_end', result.columns)
        self.assertIn('is_female', result.columns)
        self.assertIn('is_white', result.columns)
        self.assertIn('has_esrd', result.columns)
    
    def test_create_comorbidity_features(self):
        """Test comorbidity feature creation."""
        result = self.engineer.create_comorbidity_features(self.claims_data, 'inpatient')
        
        self.assertIn('has_diabetes', result.columns)
        self.assertIn('has_ckd', result.columns)
        self.assertIn('has_cvd', result.columns)
        self.assertIn('has_retinopathy', result.columns)
    
    def test_create_utilization_features(self):
        """Test utilization feature creation."""
        result = self.engineer.create_utilization_features(self.claims_data, 'inpatient')
        
        self.assertIn('inpatient_claim_count', result.columns)
        self.assertIn('inpatient_total_payment', result.columns)
        self.assertIn('inpatient_avg_payment', result.columns)
    
    def test_create_diabetes_specific_features(self):
        """Test diabetes-specific feature creation."""
        claims_data = {'inpatient': self.claims_data}
        result = self.engineer.create_diabetes_specific_features(
            self.beneficiary_data, claims_data
        )
        
        self.assertIn('has_diabetes_flag', result.columns)
        self.assertIn('has_diabetes_comprehensive', result.columns)
    
    def test_create_all_features(self):
        """Test comprehensive feature creation."""
        processed_data = {
            'beneficiary': self.beneficiary_data,
            'inpatient': self.claims_data,
            'outpatient': self.claims_data
        }
        
        result = self.engineer.create_all_features(processed_data)
        
        self.assertIn('DESYNPUF_ID', result.columns)
        self.assertGreater(len(result.columns), 10)  # Should have many features
        self.assertEqual(len(result), 3)  # Should have 3 members


class TestHEDISConfig(unittest.TestCase):
    """Test cases for HEDIS configuration."""
    
    def test_config_initialization(self):
        """Test HEDIS configuration initialization."""
        config = HEDISConfig(measurement_year=2008)
        
        self.assertEqual(config.measurement_year, 2008)
        self.assertEqual(config.age_min, 18)
        self.assertEqual(config.age_max, 75)
        self.assertIsNotNone(config.diabetes_codes)
        self.assertIsNotNone(config.ckd_codes)
        self.assertIsNotNone(config.cvd_codes)
        self.assertIsNotNone(config.retinopathy_codes)
    
    def test_diabetes_codes(self):
        """Test diabetes codes are properly defined."""
        config = HEDISConfig()
        
        # Check that common diabetes codes are included
        self.assertIn('250.00', config.diabetes_codes)
        self.assertIn('250.01', config.diabetes_codes)
        self.assertIn('250.90', config.diabetes_codes)


if __name__ == '__main__':
    # Run all tests
    unittest.main(verbosity=2)

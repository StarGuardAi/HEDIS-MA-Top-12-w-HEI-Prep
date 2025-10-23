"""
Unit Tests for HEDIS GSD Data Validation Module

Tests data validation and quality checks with HIPAA compliance.
"""

import unittest
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Import modules to test
from src.utils.data_validation import (
    HEDISDataValidator,
    HEDISTestDataGenerator,
    validate_hedis_data,
    generate_test_data
)


class TestHEDISDataValidator(unittest.TestCase):
    """Test cases for HEDIS data validator."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.validator = HEDISDataValidator()
        
        # Create sample beneficiary data
        self.beneficiary_data = pd.DataFrame({
            'DESYNPUF_ID': ['TEST001', 'TEST002', 'TEST003'],
            'BENE_BIRTH_DT': pd.to_datetime(['1950-01-01', '1960-01-01', '1970-01-01']),
            'BENE_DEATH_DT': pd.NaT,
            'BENE_SEX_IDENT_CD': [1, 2, 1],
            'BENE_RACE_CD': [1, 2, 1],
            'BENE_ESRD_IND': [0, 0, 0],
            'SP_STATE_CODE': [26, 39, 6],
            'SP_DIABETES': [1, 0, 1],
            'age_at_my_end': [58, 48, 38]
        })
        
        # Create sample claims data
        self.claims_data = pd.DataFrame({
            'DESYNPUF_ID': ['TEST001', 'TEST002', 'TEST001', 'TEST003'],
            'CLM_ID': ['CLM001', 'CLM002', 'CLM003', 'CLM004'],
            'CLM_FROM_DT': pd.to_datetime(['2008-01-01', '2008-02-01', '2008-03-01', '2008-04-01']),
            'CLM_THRU_DT': pd.to_datetime(['2008-01-01', '2008-02-01', '2008-03-01', '2008-04-01']),
            'CLM_PMT_AMT': [100.0, 200.0, 150.0, 120.0],
            'ICD9_DGNS_CD_1': ['250.00', '401.9', '250.01', '272.4'],
            'ICD9_DGNS_CD_2': ['', '', '', ''],
            'ICD9_DGNS_CD_3': ['', '', '', ''],
            'ICD9_DGNS_CD_4': ['', '', '', ''],
            'ICD9_DGNS_CD_5': ['', '', '', '']
        })
    
    def test_validator_initialization(self):
        """Test validator initialization."""
        validator = HEDISDataValidator()
        
        self.assertIsNotNone(validator.config)
        self.assertIn('age_range', validator.config)
        self.assertIn('required_columns', validator.config)
        self.assertIn('date_columns', validator.config)
        self.assertIn('quality_thresholds', validator.config)
    
    def test_custom_config(self):
        """Test validator with custom configuration."""
        custom_config = {
            'age_range': {'min': 20, 'max': 70},
            'quality_thresholds': {
                'max_missing_percentage': 30.0,
                'min_records': 50,
                'max_duplicate_percentage': 10.0
            }
        }
        
        validator = HEDISDataValidator(config=custom_config)
        
        self.assertEqual(validator.config['age_range']['min'], 20)
        self.assertEqual(validator.config['age_range']['max'], 70)
    
    def test_validate_beneficiary_data(self):
        """Test beneficiary data validation."""
        results = self.validator.validate_beneficiary_data(self.beneficiary_data)
        
        self.assertEqual(results['data_type'], 'beneficiary')
        self.assertEqual(results['total_records'], 3)
        self.assertIn('errors', results)
        self.assertIn('warnings', results)
        self.assertIn('quality_metrics', results)
        self.assertIn('validation_time', results)
    
    def test_validate_beneficiary_missing_columns(self):
        """Test validation with missing required columns."""
        # Remove required column
        invalid_data = self.beneficiary_data.drop(columns=['SP_DIABETES'])
        
        results = self.validator.validate_beneficiary_data(invalid_data)
        
        self.assertGreater(len(results['errors']), 0)
        self.assertIn('SP_DIABETES', str(results['errors']))
    
    def test_validate_beneficiary_duplicates(self):
        """Test validation with duplicate member IDs."""
        # Add duplicate
        duplicate_data = pd.concat([self.beneficiary_data, self.beneficiary_data.iloc[[0]]])
        
        results = self.validator.validate_beneficiary_data(duplicate_data)
        
        self.assertGreater(len(results['errors']), 0)
        self.assertIn('duplicate', str(results['errors']).lower())
    
    def test_validate_beneficiary_age_range(self):
        """Test validation of age ranges."""
        # Add invalid age
        invalid_age_data = self.beneficiary_data.copy()
        invalid_age_data.loc[0, 'age_at_my_end'] = 90  # Outside HEDIS range
        
        results = self.validator.validate_beneficiary_data(invalid_age_data)
        
        self.assertGreater(len(results['warnings']), 0)
        self.assertIn('quality_metrics', results)
        self.assertIn('age_stats', results['quality_metrics'])
    
    def test_validate_claims_data_inpatient(self):
        """Test inpatient claims data validation."""
        results = self.validator.validate_claims_data(self.claims_data, 'inpatient')
        
        self.assertEqual(results['data_type'], 'inpatient')
        self.assertEqual(results['total_records'], 4)
        self.assertIn('errors', results)
        self.assertIn('warnings', results)
        self.assertIn('quality_metrics', results)
    
    def test_validate_claims_data_outpatient(self):
        """Test outpatient claims data validation."""
        results = self.validator.validate_claims_data(self.claims_data, 'outpatient')
        
        self.assertEqual(results['data_type'], 'outpatient')
        self.assertEqual(results['total_records'], 4)
        self.assertIn('unique_members', results['quality_metrics'])
        self.assertEqual(results['quality_metrics']['unique_members'], 3)
    
    def test_validate_claims_negative_payments(self):
        """Test validation with negative payment amounts."""
        # Add negative payment
        invalid_payment_data = self.claims_data.copy()
        invalid_payment_data.loc[0, 'CLM_PMT_AMT'] = -100.0
        
        results = self.validator.validate_claims_data(invalid_payment_data, 'inpatient')
        
        self.assertGreater(len(results['warnings']), 0)
        self.assertIn('negative', str(results['warnings']).lower())
    
    def test_validate_claims_missing_dates(self):
        """Test validation with missing dates."""
        # Add missing date
        invalid_date_data = self.claims_data.copy()
        invalid_date_data.loc[0, 'CLM_FROM_DT'] = pd.NaT
        
        results = self.validator.validate_claims_data(invalid_date_data, 'inpatient')
        
        self.assertGreater(len(results['warnings']), 0)
    
    def test_validate_feature_data(self):
        """Test feature data validation."""
        # Create sample feature data
        feature_data = pd.DataFrame({
            'DESYNPUF_ID': ['TEST001', 'TEST002', 'TEST003'],
            'age_at_my_end': [58, 48, 38],
            'is_female': [0, 1, 0],
            'has_diabetes_comprehensive': [1, 0, 1],
            'has_ckd': [0, 0, 1],
            'has_cvd': [1, 0, 0],
            'inpatient_claim_count': [2, 1, 1],
            'outpatient_claim_count': [5, 3, 4]
        })
        
        results = self.validator.validate_feature_data(feature_data)
        
        self.assertEqual(results['data_type'], 'features')
        self.assertEqual(results['total_records'], 3)
        self.assertEqual(results['total_features'], 7)  # Excluding DESYNPUF_ID
        self.assertIn('quality_metrics', results)
    
    def test_validate_feature_data_missing_id(self):
        """Test feature validation with missing DESYNPUF_ID."""
        # Remove DESYNPUF_ID
        invalid_data = pd.DataFrame({
            'age_at_my_end': [58, 48, 38],
            'is_female': [0, 1, 0]
        })
        
        results = self.validator.validate_feature_data(invalid_data)
        
        self.assertGreater(len(results['errors']), 0)
        self.assertIn('DESYNPUF_ID', str(results['errors']))
    
    def test_validate_feature_data_infinite_values(self):
        """Test feature validation with infinite values."""
        # Add infinite value
        feature_data = pd.DataFrame({
            'DESYNPUF_ID': ['TEST001', 'TEST002'],
            'age_at_my_end': [58, np.inf],
            'is_female': [0, 1]
        })
        
        results = self.validator.validate_feature_data(feature_data)
        
        self.assertGreater(len(results['warnings']), 0)
        self.assertIn('infinite', str(results['warnings']).lower())
    
    def test_validate_feature_data_diabetes_rate(self):
        """Test diabetes rate validation."""
        # Create data with unusual diabetes rate
        feature_data = pd.DataFrame({
            'DESYNPUF_ID': [f'TEST{i:03d}' for i in range(100)],
            'has_diabetes_comprehensive': [1] * 90 + [0] * 10,  # 90% diabetes rate
            'age_at_my_end': np.random.randint(18, 76, 100)
        })
        
        results = self.validator.validate_feature_data(feature_data)
        
        self.assertIn('quality_metrics', results)
        self.assertIn('diabetes_rate', results['quality_metrics'])
        self.assertGreater(results['quality_metrics']['diabetes_rate'], 50)
        self.assertGreater(len(results['warnings']), 0)
    
    def test_validate_data_quality(self):
        """Test comprehensive data quality validation."""
        data = {
            'beneficiary': self.beneficiary_data,
            'inpatient': self.claims_data,
            'outpatient': self.claims_data
        }
        
        results = self.validator.validate_data_quality(data)
        
        self.assertIn('validation_time', results)
        self.assertIn('data_types', results)
        self.assertIn('individual_results', results)
        self.assertIn('overall_status', results)
        self.assertIn('summary', results)
        
        self.assertEqual(len(results['data_types']), 3)
        self.assertIn('beneficiary', results['individual_results'])
        self.assertIn('inpatient', results['individual_results'])
        self.assertIn('outpatient', results['individual_results'])
    
    def test_validate_data_quality_overall_status(self):
        """Test overall status determination."""
        # Create valid data
        data = {
            'beneficiary': self.beneficiary_data,
            'inpatient': self.claims_data
        }
        
        results = self.validator.validate_data_quality(data)
        
        # Should PASS with no major errors
        self.assertIn(results['overall_status'], ['PASS', 'WARNING'])


class TestHEDISTestDataGenerator(unittest.TestCase):
    """Test cases for HEDIS test data generator."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.generator = HEDISTestDataGenerator()
    
    def test_generator_initialization(self):
        """Test generator initialization."""
        generator = HEDISTestDataGenerator()
        
        self.assertIsNotNone(generator.config)
        self.assertIn('sample_sizes', generator.config)
        self.assertIn('age_distribution', generator.config)
        self.assertIn('diabetes_rate', generator.config)
    
    def test_custom_config(self):
        """Test generator with custom configuration."""
        custom_config = {
            'sample_sizes': {
                'beneficiary': 500,
                'inpatient': 2000,
                'outpatient': 5000
            },
            'diabetes_rate': 0.30
        }
        
        generator = HEDISTestDataGenerator(config=custom_config)
        
        self.assertEqual(generator.config['sample_sizes']['beneficiary'], 500)
        self.assertEqual(generator.config['diabetes_rate'], 0.30)
    
    def test_generate_beneficiary_data(self):
        """Test beneficiary data generation."""
        df = self.generator.generate_beneficiary_data(n_members=100)
        
        self.assertEqual(len(df), 100)
        self.assertIn('DESYNPUF_ID', df.columns)
        self.assertIn('BENE_BIRTH_DT', df.columns)
        self.assertIn('BENE_SEX_IDENT_CD', df.columns)
        self.assertIn('SP_DIABETES', df.columns)
        
        # Check member IDs are synthetic
        self.assertTrue(all(df['DESYNPUF_ID'].str.startswith('SYNTH_')))
    
    def test_generate_beneficiary_age_distribution(self):
        """Test age distribution in generated data."""
        df = self.generator.generate_beneficiary_data(n_members=1000)
        
        # Extract years from birth dates
        birth_years = df['BENE_BIRTH_DT'].str[:4].astype(int)
        ages = 2008 - birth_years
        
        # Check age range
        self.assertTrue(all(ages >= 18))
        self.assertTrue(all(ages <= 75))
        
        # Check distribution roughly matches config
        young = (ages < 45).sum() / len(ages)
        middle = ((ages >= 45) & (ages < 65)).sum() / len(ages)
        older = (ages >= 65).sum() / len(ages)
        
        # Allow some variance due to randomness
        self.assertGreater(young, 0.2)
        self.assertGreater(middle, 0.3)
        self.assertGreater(older, 0.2)
    
    def test_generate_beneficiary_diabetes_rate(self):
        """Test diabetes rate in generated data."""
        df = self.generator.generate_beneficiary_data(n_members=1000)
        
        diabetes_rate = df['SP_DIABETES'].sum() / len(df)
        expected_rate = self.generator.config['diabetes_rate']
        
        # Allow 10% variance due to randomness
        self.assertGreater(diabetes_rate, expected_rate * 0.9)
        self.assertLess(diabetes_rate, expected_rate * 1.1)
    
    def test_generate_claims_data_inpatient(self):
        """Test inpatient claims data generation."""
        df = self.generator.generate_claims_data(n_claims=200, claim_type='inpatient')
        
        self.assertEqual(len(df), 200)
        self.assertIn('DESYNPUF_ID', df.columns)
        self.assertIn('CLM_ID', df.columns)
        self.assertIn('CLM_FROM_DT', df.columns)
        self.assertIn('CLM_PMT_AMT', df.columns)
        self.assertIn('ICD9_DGNS_CD_1', df.columns)
        
        # Check claim IDs are correctly formatted
        self.assertTrue(all(df['CLM_ID'].str.startswith('CLM_INPATIENT_')))
    
    def test_generate_claims_data_outpatient(self):
        """Test outpatient claims data generation."""
        df = self.generator.generate_claims_data(n_claims=200, claim_type='outpatient')
        
        self.assertEqual(len(df), 200)
        
        # Check claim IDs are correctly formatted
        self.assertTrue(all(df['CLM_ID'].str.startswith('CLM_OUTPATIENT_')))
    
    def test_generate_claims_payment_amounts(self):
        """Test payment amounts are realistic."""
        inpatient_df = self.generator.generate_claims_data(n_claims=100, claim_type='inpatient')
        outpatient_df = self.generator.generate_claims_data(n_claims=100, claim_type='outpatient')
        
        # Inpatient should have higher average payment
        inpatient_avg = inpatient_df['CLM_PMT_AMT'].mean()
        outpatient_avg = outpatient_df['CLM_PMT_AMT'].mean()
        
        self.assertGreater(inpatient_avg, outpatient_avg)
        
        # All payments should be positive
        self.assertTrue(all(inpatient_df['CLM_PMT_AMT'] > 0))
        self.assertTrue(all(outpatient_df['CLM_PMT_AMT'] > 0))
    
    def test_generate_all_test_data(self):
        """Test comprehensive test data generation."""
        data = self.generator.generate_all_test_data()
        
        self.assertIn('beneficiary', data)
        self.assertIn('inpatient', data)
        self.assertIn('outpatient', data)
        
        self.assertIsInstance(data['beneficiary'], pd.DataFrame)
        self.assertIsInstance(data['inpatient'], pd.DataFrame)
        self.assertIsInstance(data['outpatient'], pd.DataFrame)
        
        self.assertGreater(len(data['beneficiary']), 0)
        self.assertGreater(len(data['inpatient']), 0)
        self.assertGreater(len(data['outpatient']), 0)


class TestConvenienceFunctions(unittest.TestCase):
    """Test convenience functions."""
    
    def test_validate_hedis_data(self):
        """Test validate_hedis_data convenience function."""
        # Generate test data
        data = generate_test_data()
        
        # Validate
        results = validate_hedis_data(data)
        
        self.assertIn('overall_status', results)
        self.assertIn('summary', results)
        self.assertIn('individual_results', results)
    
    def test_generate_test_data(self):
        """Test generate_test_data convenience function."""
        data = generate_test_data()
        
        self.assertIn('beneficiary', data)
        self.assertIn('inpatient', data)
        self.assertIn('outpatient', data)
        
        # Check all are DataFrames
        for key, df in data.items():
            self.assertIsInstance(df, pd.DataFrame)
            self.assertGreater(len(df), 0)
    
    def test_generate_test_data_custom_config(self):
        """Test generate_test_data with custom configuration."""
        custom_config = {
            'sample_sizes': {
                'beneficiary': 50,
                'inpatient': 100,
                'outpatient': 200
            }
        }
        
        data = generate_test_data(config=custom_config)
        
        self.assertEqual(len(data['beneficiary']), 50)
        self.assertEqual(len(data['inpatient']), 100)
        self.assertEqual(len(data['outpatient']), 200)


class TestPHICompliance(unittest.TestCase):
    """Test HIPAA PHI compliance in generated data."""
    
    def test_synthetic_member_ids(self):
        """Test that all member IDs are clearly synthetic."""
        generator = HEDISTestDataGenerator()
        df = generator.generate_beneficiary_data(n_members=100)
        
        # All IDs should start with SYNTH_
        self.assertTrue(all(df['DESYNPUF_ID'].str.startswith('SYNTH_')))
    
    def test_no_real_dates_in_future(self):
        """Test that generated dates are not in the future."""
        generator = HEDISTestDataGenerator()
        df = generator.generate_claims_data(n_claims=100)
        
        # Extract years from claim dates
        claim_years = df['CLM_FROM_DT'].str[:4].astype(int)
        
        # All dates should be 2010 or earlier (historical)
        self.assertTrue(all(claim_years <= 2010))
    
    def test_no_death_dates_in_synthetic_data(self):
        """Test that synthetic data doesn't include death dates."""
        generator = HEDISTestDataGenerator()
        df = generator.generate_beneficiary_data(n_members=100)
        
        # All death dates should be empty
        self.assertTrue(all(df['BENE_DEATH_DT'] == ''))


if __name__ == '__main__':
    # Run all tests
    unittest.main(verbosity=2)


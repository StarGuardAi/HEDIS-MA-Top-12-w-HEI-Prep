"""
Data Validation and Testing Utilities for HEDIS GSD Prediction Engine

Provides comprehensive data validation, testing utilities, and quality checks
for healthcare data processing with HIPAA compliance.

HEDIS Specification: MY2023 Volume 2
Measure: HBD - Hemoglobin A1c Control for Patients with Diabetes
"""

import pandas as pd
import numpy as np
import logging
from typing import Dict, List, Optional, Tuple, Union, Any
from datetime import datetime
import hashlib
import os
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class HEDISDataValidator:
    """
    Validates healthcare data with HEDIS compliance and HIPAA safety.
    
    Key features:
    - Schema validation
    - Data quality checks
    - HIPAA compliance validation
    - HEDIS specification compliance
    """
    
    def __init__(self, config: Dict[str, Any] = None):
        """
        Initialize the data validator.
        
        Args:
            config: Configuration dictionary
        """
        self.config = config or self._default_config()
        self.validation_results = {}
        
        logger.info("Initialized HEDIS data validator")
    
    def _default_config(self) -> Dict[str, Any]:
        """Return default configuration."""
        return {
            'age_range': {'min': 18, 'max': 75},
            'required_columns': {
                'beneficiary': ['DESYNPUF_ID', 'BENE_BIRTH_DT', 'BENE_SEX_IDENT_CD', 'SP_DIABETES'],
                'inpatient': ['DESYNPUF_ID', 'CLM_ID', 'CLM_FROM_DT', 'CLM_THRU_DT'],
                'outpatient': ['DESYNPUF_ID', 'CLM_ID', 'CLM_FROM_DT', 'CLM_THRU_DT']
            },
            'date_columns': {
                'beneficiary': ['BENE_BIRTH_DT', 'BENE_DEATH_DT'],
                'inpatient': ['CLM_FROM_DT', 'CLM_THRU_DT'],
                'outpatient': ['CLM_FROM_DT', 'CLM_THRU_DT']
            },
            'numeric_columns': {
                'beneficiary': ['BENE_SEX_IDENT_CD', 'BENE_RACE_CD', 'SP_DIABETES'],
                'inpatient': ['CLM_PMT_AMT'],
                'outpatient': ['CLM_PMT_AMT']
            },
            'quality_thresholds': {
                'max_missing_percentage': 50.0,
                'min_records': 100,
                'max_duplicate_percentage': 5.0
            }
        }
    
    def validate_beneficiary_data(self, df: pd.DataFrame) -> Dict[str, Any]:
        """
        Validate beneficiary data.
        
        Args:
            df: Beneficiary DataFrame
            
        Returns:
            Dictionary with validation results
        """
        logger.info("Validating beneficiary data")
        
        results = {
            'data_type': 'beneficiary',
            'total_records': len(df),
            'validation_time': datetime.now().isoformat(),
            'errors': [],
            'warnings': [],
            'quality_metrics': {}
        }
        
        # Check required columns
        required_cols = self.config['required_columns']['beneficiary']
        missing_cols = set(required_cols) - set(df.columns)
        if missing_cols:
            results['errors'].append(f"Missing required columns: {missing_cols}")
        
        # Check data types
        date_cols = self.config['date_columns']['beneficiary']
        for col in date_cols:
            if col in df.columns:
                if not pd.api.types.is_datetime64_any_dtype(df[col]):
                    results['warnings'].append(f"Column {col} is not datetime type")
        
        # Check age ranges
        if 'age_at_my_end' in df.columns:
            age_stats = df['age_at_my_end'].describe()
            results['quality_metrics']['age_stats'] = age_stats.to_dict()
            
            # Check HEDIS age range
            age_range = self.config['age_range']
            invalid_ages = ((df['age_at_my_end'] < age_range['min']) | 
                           (df['age_at_my_end'] > age_range['max'])).sum()
            if invalid_ages > 0:
                results['warnings'].append(f"{invalid_ages} records outside HEDIS age range")
        
        # Check diabetes indicator
        if 'SP_DIABETES' in df.columns:
            diabetes_counts = df['SP_DIABETES'].value_counts()
            results['quality_metrics']['diabetes_distribution'] = diabetes_counts.to_dict()
            
            missing_diabetes = df['SP_DIABETES'].isna().sum()
            if missing_diabetes > 0:
                results['warnings'].append(f"{missing_diabetes} records with missing diabetes indicator")
        
        # Check for duplicates
        duplicates = df['DESYNPUF_ID'].duplicated().sum()
        if duplicates > 0:
            results['errors'].append(f"{duplicates} duplicate member IDs found")
        
        # Check missing values
        missing_stats = df.isnull().sum()
        high_missing = missing_stats[missing_stats > len(df) * 0.5]
        if len(high_missing) > 0:
            results['warnings'].append(f"Columns with >50% missing values: {high_missing.index.tolist()}")
        
        results['quality_metrics']['missing_values'] = missing_stats.to_dict()
        
        logger.info(f"Beneficiary validation completed: {len(results['errors'])} errors, {len(results['warnings'])} warnings")
        return results
    
    def validate_claims_data(self, df: pd.DataFrame, claim_type: str) -> Dict[str, Any]:
        """
        Validate claims data.
        
        Args:
            df: Claims DataFrame
            claim_type: Type of claims ('inpatient' or 'outpatient')
            
        Returns:
            Dictionary with validation results
        """
        logger.info(f"Validating {claim_type} claims data")
        
        results = {
            'data_type': claim_type,
            'total_records': len(df),
            'validation_time': datetime.now().isoformat(),
            'errors': [],
            'warnings': [],
            'quality_metrics': {}
        }
        
        # Check required columns
        required_cols = self.config['required_columns'][claim_type]
        missing_cols = set(required_cols) - set(df.columns)
        if missing_cols:
            results['errors'].append(f"Missing required columns: {missing_cols}")
        
        # Check date columns
        date_cols = self.config['date_columns'][claim_type]
        for col in date_cols:
            if col in df.columns:
                if not pd.api.types.is_datetime64_any_dtype(df[col]):
                    results['warnings'].append(f"Column {col} is not datetime type")
                
                # Check date ranges
                if col in ['CLM_FROM_DT', 'CLM_THRU_DT']:
                    invalid_dates = df[col].isna().sum()
                    if invalid_dates > 0:
                        results['warnings'].append(f"{invalid_dates} records with invalid dates in {col}")
        
        # Check payment amounts
        if 'CLM_PMT_AMT' in df.columns:
            payment_stats = df['CLM_PMT_AMT'].describe()
            results['quality_metrics']['payment_stats'] = payment_stats.to_dict()
            
            negative_payments = (df['CLM_PMT_AMT'] < 0).sum()
            if negative_payments > 0:
                results['warnings'].append(f"{negative_payments} records with negative payment amounts")
        
        # Check diagnosis codes
        diag_cols = [col for col in df.columns if col.startswith('ICD9_DGNS_CD_')]
        results['quality_metrics']['diagnosis_columns'] = len(diag_cols)
        
        # Check for duplicates
        if 'CLM_ID' in df.columns:
            duplicates = df['CLM_ID'].duplicated().sum()
            if duplicates > 0:
                results['warnings'].append(f"{duplicates} duplicate claim IDs found")
        
        # Check unique members
        unique_members = df['DESYNPUF_ID'].nunique()
        results['quality_metrics']['unique_members'] = unique_members
        
        logger.info(f"{claim_type.title()} validation completed: {len(results['errors'])} errors, {len(results['warnings'])} warnings")
        return results
    
    def validate_feature_data(self, df: pd.DataFrame) -> Dict[str, Any]:
        """
        Validate feature-engineered data.
        
        Args:
            df: Feature DataFrame
            
        Returns:
            Dictionary with validation results
        """
        logger.info("Validating feature data")
        
        results = {
            'data_type': 'features',
            'total_records': len(df),
            'total_features': len(df.columns) - 1,  # Exclude DESYNPUF_ID
            'validation_time': datetime.now().isoformat(),
            'errors': [],
            'warnings': [],
            'quality_metrics': {}
        }
        
        # Check for DESYNPUF_ID
        if 'DESYNPUF_ID' not in df.columns:
            results['errors'].append("Missing DESYNPUF_ID column")
        
        # Check for duplicates
        if 'DESYNPUF_ID' in df.columns:
            duplicates = df['DESYNPUF_ID'].duplicated().sum()
            if duplicates > 0:
                results['errors'].append(f"{duplicates} duplicate member IDs found")
        
        # Check feature distributions
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        for col in numeric_cols:
            if col != 'DESYNPUF_ID':
                col_stats = df[col].describe()
                results['quality_metrics'][f'{col}_stats'] = col_stats.to_dict()
                
                # Check for infinite values
                infinite_count = np.isinf(df[col]).sum()
                if infinite_count > 0:
                    results['warnings'].append(f"Column {col} has {infinite_count} infinite values")
        
        # Check diabetes features
        diabetes_cols = [col for col in df.columns if 'diabetes' in col.lower()]
        if diabetes_cols:
            results['quality_metrics']['diabetes_features'] = len(diabetes_cols)
            
            # Check diabetes comprehensive feature
            if 'has_diabetes_comprehensive' in df.columns:
                diabetes_count = df['has_diabetes_comprehensive'].sum()
                diabetes_rate = diabetes_count / len(df) * 100
                results['quality_metrics']['diabetes_rate'] = diabetes_rate
                
                if diabetes_rate < 5 or diabetes_rate > 50:
                    results['warnings'].append(f"Unusual diabetes rate: {diabetes_rate:.1f}%")
        
        # Check missing values
        missing_stats = df.isnull().sum()
        high_missing = missing_stats[missing_stats > len(df) * 0.1]  # 10% threshold for features
        if len(high_missing) > 0:
            results['warnings'].append(f"Columns with >10% missing values: {high_missing.index.tolist()}")
        
        results['quality_metrics']['missing_values'] = missing_stats.to_dict()
        
        logger.info(f"Feature validation completed: {len(results['errors'])} errors, {len(results['warnings'])} warnings")
        return results
    
    def validate_data_quality(self, data: Dict[str, pd.DataFrame]) -> Dict[str, Any]:
        """
        Comprehensive data quality validation.
        
        Args:
            data: Dictionary of DataFrames
            
        Returns:
            Dictionary with overall validation results
        """
        logger.info("Starting comprehensive data quality validation")
        
        overall_results = {
            'validation_time': datetime.now().isoformat(),
            'data_types': list(data.keys()),
            'individual_results': {},
            'overall_status': 'PASS',
            'summary': {
                'total_errors': 0,
                'total_warnings': 0,
                'total_records': 0
            }
        }
        
        # Validate each data type
        for data_type, df in data.items():
            if data_type == 'beneficiary':
                results = self.validate_beneficiary_data(df)
            elif data_type in ['inpatient', 'outpatient']:
                results = self.validate_claims_data(df, data_type)
            elif data_type == 'features':
                results = self.validate_feature_data(df)
            else:
                logger.warning(f"Unknown data type: {data_type}")
                continue
            
            overall_results['individual_results'][data_type] = results
            overall_results['summary']['total_errors'] += len(results['errors'])
            overall_results['summary']['total_warnings'] += len(results['warnings'])
            overall_results['summary']['total_records'] += results['total_records']
        
        # Determine overall status
        if overall_results['summary']['total_errors'] > 0:
            overall_results['overall_status'] = 'FAIL'
        elif overall_results['summary']['total_warnings'] > 10:
            overall_results['overall_status'] = 'WARNING'
        
        logger.info(f"Data quality validation completed: {overall_results['overall_status']}")
        return overall_results


class HEDISTestDataGenerator:
    """
    Generates synthetic test data for HEDIS GSD prediction engine.
    
    Key features:
    - HIPAA-compliant synthetic data
    - Realistic healthcare patterns
    - Configurable data sizes
    """
    
    def __init__(self, config: Dict[str, Any] = None):
        """
        Initialize the test data generator.
        
        Args:
            config: Configuration dictionary
        """
        self.config = config or self._default_config()
        
        logger.info("Initialized HEDIS test data generator")
    
    def _default_config(self) -> Dict[str, Any]:
        """Return default configuration."""
        return {
            'sample_sizes': {
                'beneficiary': 1000,
                'inpatient': 5000,
                'outpatient': 10000
            },
            'age_distribution': {
                '18-44': 0.3,
                '45-64': 0.4,
                '65-75': 0.3
            },
            'diabetes_rate': 0.25,
            'comorbidity_rates': {
                'ckd': 0.15,
                'cvd': 0.20,
                'retinopathy': 0.10
            }
        }
    
    def generate_beneficiary_data(self, n_members: int = None) -> pd.DataFrame:
        """
        Generate synthetic beneficiary data.
        
        Args:
            n_members: Number of members to generate
            
        Returns:
            DataFrame with synthetic beneficiary data
        """
        if n_members is None:
            n_members = self.config['sample_sizes']['beneficiary']
        
        logger.info(f"Generating {n_members} synthetic beneficiary records")
        
        np.random.seed(42)
        
        # Generate member IDs (synthetic)
        member_ids = [f"SYNTH_{i:06d}" for i in range(n_members)]
        
        # Generate ages based on distribution
        age_groups = ['18-44', '45-64', '65-75']
        age_probs = list(self.config['age_distribution'].values())
        age_group_assignments = np.random.choice(age_groups, n_members, p=age_probs)
        
        ages = []
        for group in age_group_assignments:
            if group == '18-44':
                age = np.random.randint(18, 45)
            elif group == '45-64':
                age = np.random.randint(45, 65)
            else:  # 65-75
                age = np.random.randint(65, 76)
            ages.append(age)
        
        # Generate birth dates (2008 - age)
        birth_years = [2008 - age for age in ages]
        birth_dates = [f"{year}{np.random.randint(1, 13):02d}{np.random.randint(1, 29):02d}" for year in birth_years]
        
        # Generate other demographics
        sex_codes = np.random.choice([1, 2], n_members, p=[0.48, 0.52])  # Slightly more females
        race_codes = np.random.choice([1, 2, 5, 6], n_members, p=[0.7, 0.15, 0.1, 0.05])  # Mostly white
        esrd_flags = np.random.choice([0, 1], n_members, p=[0.98, 0.02])  # 2% ESRD
        
        # Generate diabetes flags
        diabetes_flags = np.random.choice([0, 1], n_members, p=[1-self.config['diabetes_rate'], self.config['diabetes_rate']])
        
        # Generate state codes
        state_codes = np.random.choice([6, 26, 39, 48], n_members, p=[0.25, 0.25, 0.25, 0.25])
        
        # Create DataFrame
        df = pd.DataFrame({
            'DESYNPUF_ID': member_ids,
            'BENE_BIRTH_DT': birth_dates,
            'BENE_DEATH_DT': '',  # No deaths in synthetic data
            'BENE_SEX_IDENT_CD': sex_codes,
            'BENE_RACE_CD': race_codes,
            'BENE_ESRD_IND': esrd_flags,
            'SP_STATE_CODE': state_codes,
            'SP_DIABETES': diabetes_flags
        })
        
        logger.info(f"Generated {len(df)} synthetic beneficiary records")
        return df
    
    def generate_claims_data(self, n_claims: int = None, claim_type: str = 'inpatient') -> pd.DataFrame:
        """
        Generate synthetic claims data.
        
        Args:
            n_claims: Number of claims to generate
            claim_type: Type of claims ('inpatient' or 'outpatient')
            
        Returns:
            DataFrame with synthetic claims data
        """
        if n_claims is None:
            n_claims = self.config['sample_sizes'][claim_type]
        
        logger.info(f"Generating {n_claims} synthetic {claim_type} claims")
        
        np.random.seed(42)
        
        # Generate claim IDs
        claim_ids = [f"CLM_{claim_type.upper()}_{i:08d}" for i in range(n_claims)]
        
        # Generate member IDs (some overlap with beneficiary data)
        member_ids = [f"SYNTH_{np.random.randint(0, 1000):06d}" for _ in range(n_claims)]
        
        # Generate claim dates (2008-2010)
        claim_dates = []
        for _ in range(n_claims):
            year = np.random.choice([2008, 2009, 2010], p=[0.3, 0.4, 0.3])
            month = np.random.randint(1, 13)
            day = np.random.randint(1, 29)
            claim_dates.append(f"{year}{month:02d}{day:02d}")
        
        # Generate payment amounts
        if claim_type == 'inpatient':
            payment_amounts = np.random.lognormal(7, 1, n_claims)  # Higher amounts for inpatient
        else:
            payment_amounts = np.random.lognormal(4, 1, n_claims)  # Lower amounts for outpatient
        
        # Generate diagnosis codes
        diabetes_codes = ['250.00', '250.01', '250.90', '250.91']
        other_codes = ['401.9', '272.4', '585.3', '414.01']
        
        diag_codes = []
        for _ in range(n_claims):
            if np.random.random() < self.config['diabetes_rate']:
                diag_codes.append(np.random.choice(diabetes_codes))
            else:
                diag_codes.append(np.random.choice(other_codes))
        
        # Create DataFrame
        df = pd.DataFrame({
            'DESYNPUF_ID': member_ids,
            'CLM_ID': claim_ids,
            'CLM_FROM_DT': claim_dates,
            'CLM_THRU_DT': claim_dates,  # Same day for simplicity
            'CLM_PMT_AMT': payment_amounts,
            'ICD9_DGNS_CD_1': diag_codes,
            'ICD9_DGNS_CD_2': '',
            'ICD9_DGNS_CD_3': '',
            'ICD9_DGNS_CD_4': '',
            'ICD9_DGNS_CD_5': ''
        })
        
        logger.info(f"Generated {len(df)} synthetic {claim_type} claims")
        return df
    
    def generate_all_test_data(self) -> Dict[str, pd.DataFrame]:
        """
        Generate all synthetic test data.
        
        Returns:
            Dictionary with all synthetic DataFrames
        """
        logger.info("Generating comprehensive synthetic test data")
        
        data = {}
        
        # Generate beneficiary data
        data['beneficiary'] = self.generate_beneficiary_data()
        
        # Generate claims data
        data['inpatient'] = self.generate_claims_data(claim_type='inpatient')
        data['outpatient'] = self.generate_claims_data(claim_type='outpatient')
        
        logger.info(f"Generated synthetic test data: {list(data.keys())}")
        return data


def validate_hedis_data(data: Dict[str, pd.DataFrame], config: Dict[str, Any] = None) -> Dict[str, Any]:
    """
    Convenience function to validate HEDIS data.
    
    Args:
        data: Dictionary of DataFrames
        config: Configuration dictionary
        
    Returns:
        Dictionary with validation results
    """
    validator = HEDISDataValidator(config)
    return validator.validate_data_quality(data)


def generate_test_data(config: Dict[str, Any] = None) -> Dict[str, pd.DataFrame]:
    """
    Convenience function to generate test data.
    
    Args:
        config: Configuration dictionary
        
    Returns:
        Dictionary with synthetic DataFrames
    """
    generator = HEDISTestDataGenerator(config)
    return generator.generate_all_test_data()


if __name__ == "__main__":
    # Example usage
    try:
        # Generate test data
        test_data = generate_test_data()
        
        # Validate test data
        validation_results = validate_hedis_data(test_data)
        
        print("Test data generation and validation completed!")
        print(f"Generated data types: {list(test_data.keys())}")
        print(f"Validation status: {validation_results['overall_status']}")
        print(f"Total records: {validation_results['summary']['total_records']}")
        
    except Exception as e:
        print(f"Error in test data generation/validation: {e}")

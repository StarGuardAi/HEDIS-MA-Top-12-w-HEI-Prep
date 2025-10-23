"""
Data Preprocessing for HEDIS GSD Prediction Engine

Handles data cleaning, normalization, date parsing, and quality control
for CMS DE-SynPUF data with HEDIS-compliant processing.

HEDIS Specification: MY2023 Volume 2
Measure: HBD - Hemoglobin A1c Control for Patients with Diabetes
"""

import pandas as pd
import numpy as np
import logging
from datetime import datetime, date
from typing import Dict, List, Optional, Tuple, Union
import warnings

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class CMSDataPreprocessor:
    """
    Preprocesses CMS DE-SynPUF data with HEDIS-compliant cleaning and validation.
    
    Key preprocessing steps:
    - Date parsing and normalization
    - Deduplication and null handling
    - Data quality checks
    - HEDIS measurement year calculations
    """
    
    def __init__(self, measurement_year: int = 2008):
        """
        Initialize the data preprocessor.
        
        Args:
            measurement_year: HEDIS measurement year (default: 2008)
        """
        self.measurement_year = measurement_year
        self.index_date = datetime(measurement_year, 12, 31)  # Dec 31 MY
        
        # HEDIS diabetes ICD-9 codes (for 2008 data)
        self.diabetes_codes = {
            '250.00', '250.01', '250.02', '250.03', '250.10', '250.11', '250.12', '250.13',
            '250.20', '250.21', '250.22', '250.23', '250.30', '250.31', '250.32', '250.33',
            '250.40', '250.41', '250.42', '250.43', '250.50', '250.51', '250.52', '250.53',
            '250.60', '250.61', '250.62', '250.63', '250.70', '250.71', '250.72', '250.73',
            '250.80', '250.81', '250.82', '250.83', '250.90', '250.91', '250.92', '250.93'
        }
    
    def parse_dates(self, df: pd.DataFrame, date_columns: List[str]) -> pd.DataFrame:
        """
        Parse date columns from string format to datetime.
        
        Args:
            df: DataFrame with date columns
            date_columns: List of column names containing dates
            
        Returns:
            DataFrame with parsed date columns
        """
        df_parsed = df.copy()
        
        for col in date_columns:
            if col in df_parsed.columns:
                try:
                    # Handle empty/null dates
                    df_parsed[col] = pd.to_datetime(df_parsed[col], errors='coerce', format='%Y%m%d')
                    logger.info(f"Parsed {col}: {df_parsed[col].notna().sum()} valid dates")
                except Exception as e:
                    logger.warning(f"Error parsing {col}: {e}")
                    df_parsed[col] = pd.NaT
        
        return df_parsed
    
    def clean_beneficiary_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Clean and normalize beneficiary data.
        
        Args:
            df: Raw beneficiary DataFrame
            
        Returns:
            Cleaned beneficiary DataFrame
        """
        logger.info("Cleaning beneficiary data")
        
        df_clean = df.copy()
        
        # Parse date columns
        date_cols = ['BENE_BIRTH_DT', 'BENE_DEATH_DT']
        df_clean = self.parse_dates(df_clean, date_cols)
        
        # Calculate age at measurement year end (Dec 31)
        df_clean['age_at_my_end'] = self._calculate_age_at_index_date(
            df_clean['BENE_BIRTH_DT']
        )
        
        # Handle death dates - set to None if not applicable
        df_clean['BENE_DEATH_DT'] = df_clean['BENE_DEATH_DT'].where(
            df_clean['BENE_DEATH_DT'].notna(), None
        )
        
        # Validate age ranges (HEDIS GSD: 18-75 years)
        valid_age_mask = (df_clean['age_at_my_end'] >= 18) & (df_clean['age_at_my_end'] <= 75)
        logger.info(f"Members in HEDIS age range (18-75): {valid_age_mask.sum()}")
        
        # Clean categorical variables
        df_clean['BENE_SEX_IDENT_CD'] = df_clean['BENE_SEX_IDENT_CD'].astype('category')
        df_clean['BENE_RACE_CD'] = df_clean['BENE_RACE_CD'].astype('category')
        df_clean['SP_STATE_CODE'] = df_clean['SP_STATE_CODE'].astype('category')
        
        # Handle missing values
        df_clean = self._handle_missing_values(df_clean, 'beneficiary')
        
        logger.info(f"Beneficiary data cleaned: {len(df_clean)} records")
        return df_clean
    
    def clean_claims_data(self, df: pd.DataFrame, claim_type: str) -> pd.DataFrame:
        """
        Clean and normalize claims data (inpatient/outpatient).
        
        Args:
            df: Raw claims DataFrame
            claim_type: Type of claims ('inpatient' or 'outpatient')
            
        Returns:
            Cleaned claims DataFrame
        """
        logger.info(f"Cleaning {claim_type} claims data")
        
        df_clean = df.copy()
        
        # Parse date columns
        date_cols = ['CLM_FROM_DT', 'CLM_THRU_DT']
        df_clean = self.parse_dates(df_clean, date_cols)
        
        # Validate date ranges
        valid_dates_mask = (
            df_clean['CLM_FROM_DT'].notna() & 
            df_clean['CLM_THRU_DT'].notna() &
            (df_clean['CLM_FROM_DT'] <= df_clean['CLM_THRU_DT'])
        )
        logger.info(f"Claims with valid date ranges: {valid_dates_mask.sum()}")
        
        # Clean payment amounts
        df_clean['CLM_PMT_AMT'] = pd.to_numeric(df_clean['CLM_PMT_AMT'], errors='coerce')
        df_clean['CLM_PMT_AMT'] = df_clean['CLM_PMT_AMT'].fillna(0.0)
        
        # Clean diagnosis codes - remove empty strings and normalize
        diag_cols = [col for col in df_clean.columns if col.startswith('ICD9_DGNS_CD_')]
        for col in diag_cols:
            df_clean[col] = df_clean[col].astype(str).replace('nan', '').replace('', None)
        
        # Handle missing values
        df_clean = self._handle_missing_values(df_clean, claim_type)
        
        logger.info(f"{claim_type.title()} claims data cleaned: {len(df_clean)} records")
        return df_clean
    
    def deduplicate_claims(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Remove duplicate claims based on CLM_ID.
        
        Args:
            df: Claims DataFrame
            
        Returns:
            Deduplicated DataFrame
        """
        initial_count = len(df)
        df_dedup = df.drop_duplicates(subset=['CLM_ID'], keep='first')
        removed_count = initial_count - len(df_dedup)
        
        if removed_count > 0:
            logger.info(f"Removed {removed_count} duplicate claims")
        
        return df_dedup
    
    def create_diabetes_flags(self, claims_df: pd.DataFrame) -> pd.DataFrame:
        """
        Create diabetes diagnosis flags based on ICD-9 codes.
        
        Args:
            claims_df: Claims DataFrame with diagnosis codes
            
        Returns:
            DataFrame with diabetes flags
        """
        logger.info("Creating diabetes diagnosis flags")
        
        df_flags = claims_df.copy()
        
        # Get all diagnosis code columns
        diag_cols = [col for col in df_flags.columns if col.startswith('ICD9_DGNS_CD_')]
        
        # Create diabetes flag for each claim
        df_flags['has_diabetes_dx'] = False
        
        for col in diag_cols:
            if col in df_flags.columns:
                # Check if any diagnosis code matches diabetes codes
                diabetes_mask = df_flags[col].isin(self.diabetes_codes)
                df_flags['has_diabetes_dx'] = df_flags['has_diabetes_dx'] | diabetes_mask
        
        diabetes_claims = df_flags['has_diabetes_dx'].sum()
        logger.info(f"Claims with diabetes diagnosis: {diabetes_claims}")
        
        return df_flags
    
    def _calculate_age_at_index_date(self, birth_dates: pd.Series) -> pd.Series:
        """
        Calculate age at measurement year end (Dec 31).
        
        Args:
            birth_dates: Series of birth dates
            
        Returns:
            Series of ages at index date
        """
        # Calculate age at Dec 31 of measurement year
        ages = []
        
        for birth_date in birth_dates:
            if pd.isna(birth_date):
                ages.append(np.nan)
            else:
                # Calculate age at Dec 31 of measurement year
                age = self.index_date.year - birth_date.year
                
                # Adjust if birthday hasn't occurred yet
                if (self.index_date.month, self.index_date.day) < (birth_date.month, birth_date.day):
                    age -= 1
                
                ages.append(age)
        
        return pd.Series(ages, index=birth_dates.index)
    
    def _handle_missing_values(self, df: pd.DataFrame, data_type: str) -> pd.DataFrame:
        """
        Handle missing values based on data type and HEDIS requirements.
        
        Args:
            df: DataFrame to clean
            data_type: Type of data ('beneficiary', 'inpatient', 'outpatient')
            
        Returns:
            DataFrame with handled missing values
        """
        df_clean = df.copy()
        
        if data_type == 'beneficiary':
            # For beneficiary data, preserve missing values for downstream analysis
            # Only fill critical missing values that would break processing
            pass
            
        elif data_type in ['inpatient', 'outpatient']:
            # For claims data, fill missing payment amounts with 0
            if 'CLM_PMT_AMT' in df_clean.columns:
                df_clean['CLM_PMT_AMT'] = df_clean['CLM_PMT_AMT'].fillna(0.0)
        
        # Log missing value statistics
        missing_stats = df_clean.isnull().sum()
        high_missing = missing_stats[missing_stats > len(df_clean) * 0.5]
        
        if len(high_missing) > 0:
            logger.warning(f"Columns with >50% missing values: {high_missing.index.tolist()}")
        
        return df_clean
    
    def validate_data_quality(self, df: pd.DataFrame, data_type: str) -> Dict[str, any]:
        """
        Perform data quality validation checks.
        
        Args:
            df: DataFrame to validate
            data_type: Type of data being validated
            
        Returns:
            Dictionary with validation results
        """
        validation_results = {
            'total_records': len(df),
            'missing_values': df.isnull().sum().to_dict(),
            'data_types': df.dtypes.to_dict(),
            'warnings': []
        }
        
        # Check for duplicate records
        if 'CLM_ID' in df.columns:
            duplicates = df['CLM_ID'].duplicated().sum()
            if duplicates > 0:
                validation_results['warnings'].append(f"{duplicates} duplicate CLM_IDs found")
        
        # Check date ranges
        date_cols = [col for col in df.columns if 'DT' in col or 'DATE' in col]
        for col in date_cols:
            if col in df.columns and df[col].dtype == 'datetime64[ns]':
                min_date = df[col].min()
                max_date = df[col].max()
                validation_results[f'{col}_range'] = {
                    'min': min_date,
                    'max': max_date
                }
        
        # Check for negative payment amounts
        if 'CLM_PMT_AMT' in df.columns:
            negative_payments = (df['CLM_PMT_AMT'] < 0).sum()
            if negative_payments > 0:
                validation_results['warnings'].append(f"{negative_payments} negative payment amounts")
        
        logger.info(f"Data quality validation completed for {data_type}")
        return validation_results


def preprocess_cms_data(data: Dict[str, pd.DataFrame], measurement_year: int = 2008) -> Dict[str, pd.DataFrame]:
    """
    Convenience function to preprocess all CMS data.
    
    Args:
        data: Dictionary of raw DataFrames from data_loader
        measurement_year: HEDIS measurement year
        
    Returns:
        Dictionary of preprocessed DataFrames
    """
    preprocessor = CMSDataPreprocessor(measurement_year)
    
    processed_data = {}
    
    # Process beneficiary data
    if 'beneficiary' in data:
        processed_data['beneficiary'] = preprocessor.clean_beneficiary_data(data['beneficiary'])
    
    # Process claims data
    for claim_type in ['inpatient', 'outpatient']:
        if claim_type in data:
            df_clean = preprocessor.clean_claims_data(data[claim_type], claim_type)
            df_dedup = preprocessor.deduplicate_claims(df_clean)
            df_flags = preprocessor.create_diabetes_flags(df_dedup)
            processed_data[claim_type] = df_flags
    
    logger.info("CMS data preprocessing completed")
    return processed_data


if __name__ == "__main__":
    # Example usage
    from data_loader import load_cms_data
    
    try:
        # Load raw data
        raw_data = load_cms_data()
        
        # Preprocess data
        processed_data = preprocess_cms_data(raw_data)
        
        print("Data preprocessing completed successfully!")
        for data_type, df in processed_data.items():
            print(f"{data_type.title()}: {len(df)} records")
            
    except Exception as e:
        print(f"Error in preprocessing: {e}")

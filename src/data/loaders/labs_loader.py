"""
Laboratory Data Loader for HEDIS Measures

Loads and processes laboratory test results including:
- HbA1c (Glycemic control)
- eGFR (Kidney function)
- ACR/Urine albumin (Kidney health)
- Lipids (Cardiovascular health)
- Other relevant lab values

HEDIS Specification: MY2025
"""

import pandas as pd
import numpy as np
import logging
from typing import Dict, List, Optional, Tuple, Any
from datetime import datetime, timedelta
from pathlib import Path

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class LabsDataLoader:
    """
    Load and process laboratory test results for HEDIS measures.
    
    Features:
    - LOINC code mapping
    - Result normalization
    - Date-based filtering
    - Quality checks
    """
    
    # LOINC codes for key lab tests
    LOINC_CODES = {
        # HbA1c - Glycemic Status
        'hba1c': [
            '4548-4',   # HbA1c (%)
            '17856-6',  # HbA1c in Blood
            '4549-2',   # HbA1c (IFCC)
        ],
        
        # eGFR - Kidney Function
        'egfr': [
            '48642-3',  # eGFR CKD-EPI
            '48643-1',  # eGFR MDRD
            '62238-1',  # eGFR non-African American
            '88294-4',  # eGFR African American
        ],
        
        # ACR - Urine Albumin/Creatinine Ratio
        'acr': [
            '9318-7',   # ACR
            '13705-9',  # ACR First Morning Urine
            '14958-3',  # ACR Random Urine
        ],
        
        # Urine Albumin
        'urine_albumin': [
            '14957-5',  # Microalbumin (mg/dL)
            '1754-1',   # Albumin in Urine (mg/dL)
            '2888-6',   # Albumin in Urine (mg/24h)
        ],
        
        # LDL Cholesterol
        'ldl': [
            '13457-7',  # LDL Cholesterol (Calculated)
            '18262-6',  # LDL Cholesterol (Direct)
        ],
        
        # Blood Pressure (if stored as lab)
        'systolic_bp': [
            '8480-6',   # Systolic BP
        ],
        'diastolic_bp': [
            '8462-4',   # Diastolic BP
        ],
    }
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize the labs data loader.
        
        Args:
            config: Configuration dictionary
        """
        self.config = config or self._default_config()
        logger.info("Initialized Labs Data Loader")
    
    def _default_config(self) -> Dict[str, Any]:
        """Return default configuration."""
        return {
            'measurement_year': 2025,
            'lookback_months': 24,
            'min_records': 10,
            'result_units': {
                'hba1c': '%',
                'egfr': 'mL/min/1.73m2',
                'acr': 'mg/g',
                'ldl': 'mg/dL',
                'bp': 'mmHg'
            },
            'valid_ranges': {
                'hba1c': (4.0, 20.0),
                'egfr': (0, 200),
                'acr': (0, 10000),
                'ldl': (0, 500),
                'systolic_bp': (60, 250),
                'diastolic_bp': (30, 150),
            }
        }
    
    def load_labs_data(self, 
                       file_path: str,
                       measurement_year: Optional[int] = None) -> pd.DataFrame:
        """
        Load laboratory data from file.
        
        Args:
            file_path: Path to labs data file
            measurement_year: Measurement year for filtering
            
        Returns:
            DataFrame with laboratory data
        """
        logger.info(f"Loading labs data from {file_path}")
        
        my_year = measurement_year or self.config['measurement_year']
        
        # Load data
        if Path(file_path).suffix == '.csv':
            df = pd.read_csv(file_path)
        elif Path(file_path).suffix == '.parquet':
            df = pd.read_parquet(file_path)
        else:
            raise ValueError(f"Unsupported file format: {file_path}")
        
        # Validate required columns
        required_cols = ['member_id', 'test_date', 'loinc_code', 'result_value']
        missing_cols = set(required_cols) - set(df.columns)
        if missing_cols:
            raise ValueError(f"Missing required columns: {missing_cols}")
        
        # Convert date column
        df['test_date'] = pd.to_datetime(df['test_date'])
        
        # Filter to measurement year and lookback period
        my_end = datetime(my_year, 12, 31)
        my_start = datetime(my_year, 1, 1)
        lookback_start = my_start - timedelta(days=365 * 2)  # 2 years lookback
        
        df = df[
            (df['test_date'] >= lookback_start) &
            (df['test_date'] <= my_end)
        ].copy()
        
        logger.info(f"Loaded {len(df)} lab records for {df['member_id'].nunique()} members")
        
        return df
    
    def identify_test_type(self, loinc_code: str) -> Optional[str]:
        """
        Identify test type from LOINC code.
        
        Args:
            loinc_code: LOINC code
            
        Returns:
            Test type name or None
        """
        for test_type, codes in self.LOINC_CODES.items():
            if loinc_code in codes:
                return test_type
        return None
    
    def extract_hba1c_tests(self, 
                           labs_df: pd.DataFrame,
                           measurement_year: Optional[int] = None) -> pd.DataFrame:
        """
        Extract HbA1c test results.
        
        Args:
            labs_df: Laboratory DataFrame
            measurement_year: Measurement year
            
        Returns:
            DataFrame with HbA1c tests
        """
        logger.info("Extracting HbA1c tests")
        
        my_year = measurement_year or self.config['measurement_year']
        
        # Filter to HbA1c LOINC codes
        hba1c_df = labs_df[
            labs_df['loinc_code'].isin(self.LOINC_CODES['hba1c'])
        ].copy()
        
        # Convert result to numeric
        hba1c_df['result_numeric'] = pd.to_numeric(hba1c_df['result_value'], errors='coerce')
        
        # Filter to valid range
        valid_range = self.config['valid_ranges']['hba1c']
        hba1c_df = hba1c_df[
            (hba1c_df['result_numeric'] >= valid_range[0]) &
            (hba1c_df['result_numeric'] <= valid_range[1])
        ]
        
        # Add test type
        hba1c_df['test_type'] = 'hba1c'
        
        # Add measurement year flag
        my_start = datetime(my_year, 1, 1)
        my_end = datetime(my_year, 12, 31)
        hba1c_df['in_measurement_year'] = (
            (hba1c_df['test_date'] >= my_start) &
            (hba1c_df['test_date'] <= my_end)
        )
        
        logger.info(f"Extracted {len(hba1c_df)} HbA1c tests for {hba1c_df['member_id'].nunique()} members")
        
        return hba1c_df
    
    def extract_egfr_tests(self,
                          labs_df: pd.DataFrame,
                          measurement_year: Optional[int] = None) -> pd.DataFrame:
        """
        Extract eGFR test results for KED measure.
        
        Args:
            labs_df: Laboratory DataFrame
            measurement_year: Measurement year
            
        Returns:
            DataFrame with eGFR tests
        """
        logger.info("Extracting eGFR tests")
        
        my_year = measurement_year or self.config['measurement_year']
        
        # Filter to eGFR LOINC codes
        egfr_df = labs_df[
            labs_df['loinc_code'].isin(self.LOINC_CODES['egfr'])
        ].copy()
        
        # Convert result to numeric
        egfr_df['result_numeric'] = pd.to_numeric(egfr_df['result_value'], errors='coerce')
        
        # Filter to valid range
        valid_range = self.config['valid_ranges']['egfr']
        egfr_df = egfr_df[
            (egfr_df['result_numeric'] >= valid_range[0]) &
            (egfr_df['result_numeric'] <= valid_range[1])
        ]
        
        # Add test type
        egfr_df['test_type'] = 'egfr'
        
        # Add measurement year flag
        my_start = datetime(my_year, 1, 1)
        my_end = datetime(my_year, 12, 31)
        egfr_df['in_measurement_year'] = (
            (egfr_df['test_date'] >= my_start) &
            (egfr_df['test_date'] <= my_end)
        )
        
        # Flag CKD stages
        egfr_df['ckd_stage'] = pd.cut(
            egfr_df['result_numeric'],
            bins=[0, 15, 30, 45, 60, 200],
            labels=['Stage_5', 'Stage_4', 'Stage_3b', 'Stage_3a', 'Normal']
        )
        
        logger.info(f"Extracted {len(egfr_df)} eGFR tests for {egfr_df['member_id'].nunique()} members")
        
        return egfr_df
    
    def extract_acr_tests(self,
                         labs_df: pd.DataFrame,
                         measurement_year: Optional[int] = None) -> pd.DataFrame:
        """
        Extract ACR (Albumin/Creatinine Ratio) test results for KED measure.
        
        Args:
            labs_df: Laboratory DataFrame
            measurement_year: Measurement year
            
        Returns:
            DataFrame with ACR tests
        """
        logger.info("Extracting ACR tests")
        
        my_year = measurement_year or self.config['measurement_year']
        
        # Filter to ACR LOINC codes
        acr_df = labs_df[
            labs_df['loinc_code'].isin(self.LOINC_CODES['acr'] + self.LOINC_CODES['urine_albumin'])
        ].copy()
        
        # Convert result to numeric
        acr_df['result_numeric'] = pd.to_numeric(acr_df['result_value'], errors='coerce')
        
        # Filter to valid range
        valid_range = self.config['valid_ranges']['acr']
        acr_df = acr_df[
            (acr_df['result_numeric'] >= valid_range[0]) &
            (acr_df['result_numeric'] <= valid_range[1])
        ]
        
        # Add test type
        acr_df['test_type'] = 'acr'
        
        # Add measurement year flag
        my_start = datetime(my_year, 1, 1)
        my_end = datetime(my_year, 12, 31)
        acr_df['in_measurement_year'] = (
            (acr_df['test_date'] >= my_start) &
            (acr_df['test_date'] <= my_end)
        )
        
        # Flag albuminuria stages
        acr_df['albuminuria_stage'] = pd.cut(
            acr_df['result_numeric'],
            bins=[0, 30, 300, 10000],
            labels=['Normal', 'Microalbuminuria', 'Macroalbuminuria']
        )
        
        logger.info(f"Extracted {len(acr_df)} ACR tests for {acr_df['member_id'].nunique()} members")
        
        return acr_df
    
    def get_most_recent_test(self,
                            labs_df: pd.DataFrame,
                            member_id: str,
                            test_type: str) -> Optional[Dict[str, Any]]:
        """
        Get most recent test result for a member.
        
        Args:
            labs_df: Laboratory DataFrame
            member_id: Member ID
            test_type: Test type (hba1c, egfr, acr)
            
        Returns:
            Dictionary with test details or None
        """
        member_tests = labs_df[
            (labs_df['member_id'] == member_id) &
            (labs_df['test_type'] == test_type)
        ].sort_values('test_date', ascending=False)
        
        if len(member_tests) == 0:
            return None
        
        most_recent = member_tests.iloc[0]
        
        return {
            'test_date': most_recent['test_date'],
            'result_value': most_recent['result_numeric'],
            'loinc_code': most_recent['loinc_code'],
            'in_measurement_year': most_recent['in_measurement_year']
        }
    
    def aggregate_member_labs(self,
                             labs_df: pd.DataFrame,
                             measurement_year: Optional[int] = None) -> pd.DataFrame:
        """
        Aggregate lab results by member.
        
        Args:
            labs_df: Laboratory DataFrame
            measurement_year: Measurement year
            
        Returns:
            DataFrame with member-level lab aggregates
        """
        logger.info("Aggregating lab results by member")
        
        my_year = measurement_year or self.config['measurement_year']
        
        # Extract all test types
        hba1c_df = self.extract_hba1c_tests(labs_df, my_year)
        egfr_df = self.extract_egfr_tests(labs_df, my_year)
        acr_df = self.extract_acr_tests(labs_df, my_year)
        
        # Combine all tests
        all_tests = pd.concat([hba1c_df, egfr_df, acr_df], ignore_index=True)
        
        # Get member list
        members = all_tests['member_id'].unique()
        
        # Aggregate features
        member_features = []
        
        for member_id in members:
            features = {'member_id': member_id}
            
            # HbA1c features
            hba1c_tests = all_tests[
                (all_tests['member_id'] == member_id) &
                (all_tests['test_type'] == 'hba1c')
            ]
            if len(hba1c_tests) > 0:
                recent_hba1c = hba1c_tests.sort_values('test_date', ascending=False).iloc[0]
                features['hba1c_most_recent'] = recent_hba1c['result_numeric']
                features['hba1c_most_recent_date'] = recent_hba1c['test_date']
                features['hba1c_in_my'] = recent_hba1c['in_measurement_year']
                features['hba1c_count_my'] = hba1c_tests['in_measurement_year'].sum()
            
            # eGFR features
            egfr_tests = all_tests[
                (all_tests['member_id'] == member_id) &
                (all_tests['test_type'] == 'egfr')
            ]
            if len(egfr_tests) > 0:
                recent_egfr = egfr_tests.sort_values('test_date', ascending=False).iloc[0]
                features['egfr_most_recent'] = recent_egfr['result_numeric']
                features['egfr_most_recent_date'] = recent_egfr['test_date']
                features['egfr_in_my'] = recent_egfr['in_measurement_year']
                features['egfr_count_my'] = egfr_tests['in_measurement_year'].sum()
            
            # ACR features
            acr_tests = all_tests[
                (all_tests['member_id'] == member_id) &
                (all_tests['test_type'] == 'acr')
            ]
            if len(acr_tests) > 0:
                recent_acr = acr_tests.sort_values('test_date', ascending=False).iloc[0]
                features['acr_most_recent'] = recent_acr['result_numeric']
                features['acr_most_recent_date'] = recent_acr['test_date']
                features['acr_in_my'] = recent_acr['in_measurement_year']
                features['acr_count_my'] = acr_tests['in_measurement_year'].sum()
            
            member_features.append(features)
        
        member_labs_df = pd.DataFrame(member_features)
        
        logger.info(f"Aggregated labs for {len(member_labs_df)} members")
        
        return member_labs_df


def load_and_process_labs(file_path: str, 
                          measurement_year: int = 2025,
                          config: Optional[Dict[str, Any]] = None) -> pd.DataFrame:
    """
    Convenience function to load and process laboratory data.
    
    Args:
        file_path: Path to labs data file
        measurement_year: Measurement year
        config: Configuration dictionary
        
    Returns:
        DataFrame with member-level lab aggregates
    """
    loader = LabsDataLoader(config)
    labs_df = loader.load_labs_data(file_path, measurement_year)
    member_labs = loader.aggregate_member_labs(labs_df, measurement_year)
    
    return member_labs


if __name__ == "__main__":
    # Example usage
    logger.info("Labs Data Loader - Example Usage")
    logger.info("This module loads and processes laboratory test results")
    logger.info("Key tests: HbA1c, eGFR, ACR/Urine Albumin")
    logger.info("Used for: GSD, KED, and other clinical measures")


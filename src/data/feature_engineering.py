"""
Feature Engineering for HEDIS GSD Prediction Engine

Creates HEDIS-compliant features for Glycemic Status Diabetes (GSD) prediction
based on CMS DE-SynPUF data and clinical specifications.

HEDIS Specification: MY2023 Volume 2
Measure: HBD - Hemoglobin A1c Control for Patients with Diabetes
"""

import pandas as pd
import numpy as np
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple, Union
from dataclasses import dataclass

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class HEDISConfig:
    """Configuration for HEDIS GSD measure calculations."""
    measurement_year: int = 2008
    age_min: int = 18
    age_max: int = 75
    index_date: datetime = None
    diabetes_codes: set = None
    ckd_codes: set = None
    cvd_codes: set = None
    retinopathy_codes: set = None
    
    def __post_init__(self):
        if self.index_date is None:
            self.index_date = datetime(self.measurement_year, 12, 31)
        
        if self.diabetes_codes is None:
            # ICD-9 diabetes codes for 2008
            self.diabetes_codes = {
                '250.00', '250.01', '250.02', '250.03', '250.10', '250.11', '250.12', '250.13',
                '250.20', '250.21', '250.22', '250.23', '250.30', '250.31', '250.32', '250.33',
                '250.40', '250.41', '250.42', '250.43', '250.50', '250.51', '250.52', '250.53',
                '250.60', '250.61', '250.62', '250.63', '250.70', '250.71', '250.72', '250.73',
                '250.80', '250.81', '250.82', '250.83', '250.90', '250.91', '250.92', '250.93'
            }
        
        if self.ckd_codes is None:
            # Chronic Kidney Disease codes
            self.ckd_codes = {
                '585.1', '585.2', '585.3', '585.4', '585.5', '585.6', '585.9',
                '586', '587', '588.0', '588.1', '588.81', '588.89', '588.9'
            }
        
        if self.cvd_codes is None:
            # Cardiovascular Disease codes
            self.cvd_codes = {
                '410.00', '410.01', '410.02', '410.10', '410.11', '410.12', '410.20', '410.21',
                '410.22', '410.30', '410.31', '410.32', '410.40', '410.41', '410.42', '410.50',
                '410.51', '410.52', '410.60', '410.61', '410.62', '410.70', '410.71', '410.72',
                '410.80', '410.81', '410.82', '410.90', '410.91', '410.92', '411.0', '411.1',
                '411.8', '411.9', '412', '413.0', '413.1', '413.9', '414.00', '414.01', '414.02',
                '414.03', '414.04', '414.05', '414.06', '414.07', '414.10', '414.11', '414.12',
                '414.19', '414.2', '414.3', '414.4', '414.8', '414.9'
            }
        
        if self.retinopathy_codes is None:
            # Diabetic retinopathy codes
            self.retinopathy_codes = {
                '250.50', '250.51', '250.52', '250.53', '361.00', '361.01', '361.02', '361.03',
                '361.04', '361.05', '361.06', '361.07', '361.10', '361.11', '361.12', '361.13',
                '361.14', '361.15', '361.16', '361.17', '361.2', '361.3', '361.4', '361.5',
                '361.6', '361.7', '361.8', '361.9', '362.01', '362.02', '362.03', '362.04',
                '362.05', '362.06', '362.07', '362.10', '362.11', '362.12', '362.13', '362.14',
                '362.15', '362.16', '362.17', '362.18', '362.20', '362.21', '362.22', '362.23',
                '362.24', '362.25', '362.26', '362.27', '362.28', '362.29', '362.30', '362.31',
                '362.32', '362.33', '362.34', '362.35', '362.36', '362.37', '362.38', '362.39',
                '362.40', '362.41', '362.42', '362.43', '362.44', '362.45', '362.46', '362.47',
                '362.48', '362.49', '362.50', '362.51', '362.52', '362.53', '362.54', '362.55',
                '362.56', '362.57', '362.58', '362.59', '362.60', '362.61', '362.62', '362.63',
                '362.64', '362.65', '362.66', '362.67', '362.68', '362.69', '362.70', '362.71',
                '362.72', '362.73', '362.74', '362.75', '362.76', '362.77', '362.78', '362.79',
                '362.80', '362.81', '362.82', '362.83', '362.84', '362.85', '362.86', '362.87',
                '362.88', '362.89', '362.90', '362.91', '362.92', '362.93', '362.94', '362.95',
                '362.96', '362.97', '362.98', '362.99'
            }


class HEDISFeatureEngineer:
    """
    Creates HEDIS-compliant features for GSD prediction.
    
    Features include:
    - Demographics (age, sex, race, state)
    - Comorbidities (CKD, CVD, retinopathy)
    - Utilization patterns (ED visits, hospitalizations)
    - Diabetes-specific indicators
    """
    
    def __init__(self, config: HEDISConfig = None):
        """
        Initialize the feature engineer.
        
        Args:
            config: HEDIS configuration object
        """
        self.config = config or HEDISConfig()
        logger.info(f"Initialized HEDIS feature engineer for MY{self.config.measurement_year}")
    
    def create_demographic_features(self, beneficiary_df: pd.DataFrame) -> pd.DataFrame:
        """
        Create demographic features from beneficiary data.
        
        Args:
            beneficiary_df: Cleaned beneficiary DataFrame
            
        Returns:
            DataFrame with demographic features
        """
        logger.info("Creating demographic features")
        
        features_df = beneficiary_df[['DESYNPUF_ID']].copy()
        
        # Age features
        features_df['age_at_my_end'] = beneficiary_df['age_at_my_end']
        features_df['age_group_18_44'] = (features_df['age_at_my_end'] >= 18) & (features_df['age_at_my_end'] <= 44)
        features_df['age_group_45_64'] = (features_df['age_at_my_end'] >= 45) & (features_df['age_at_my_end'] <= 64)
        features_df['age_group_65_75'] = (features_df['age_at_my_end'] >= 65) & (features_df['age_at_my_end'] <= 75)
        
        # Sex features
        features_df['is_female'] = (beneficiary_df['BENE_SEX_IDENT_CD'] == 2).astype(int)
        features_df['is_male'] = (beneficiary_df['BENE_SEX_IDENT_CD'] == 1).astype(int)
        
        # Race features
        features_df['is_white'] = (beneficiary_df['BENE_RACE_CD'] == 1).astype(int)
        features_df['is_black'] = (beneficiary_df['BENE_RACE_CD'] == 2).astype(int)
        features_df['is_hispanic'] = (beneficiary_df['BENE_RACE_CD'] == 5).astype(int)
        features_df['is_other_race'] = (~beneficiary_df['BENE_RACE_CD'].isin([1, 2, 5])).astype(int)
        
        # State features (top states by population)
        top_states = beneficiary_df['SP_STATE_CODE'].value_counts().head(5).index
        for state in top_states:
            features_df[f'state_{state}'] = (beneficiary_df['SP_STATE_CODE'] == state).astype(int)
        
        # ESRD indicator
        features_df['has_esrd'] = (beneficiary_df['BENE_ESRD_IND'] == 1).astype(int)
        
        logger.info(f"Created {len(features_df.columns) - 1} demographic features")
        return features_df
    
    def create_comorbidity_features(self, claims_df: pd.DataFrame, claim_type: str) -> pd.DataFrame:
        """
        Create comorbidity features from claims data.
        
        Args:
            claims_df: Claims DataFrame with diagnosis codes
            claim_type: Type of claims ('inpatient' or 'outpatient')
            
        Returns:
            DataFrame with comorbidity features aggregated by member
        """
        logger.info(f"Creating comorbidity features from {claim_type} claims")
        
        # Get diagnosis code columns
        diag_cols = [col for col in claims_df.columns if col.startswith('ICD9_DGNS_CD_')]
        
        # Create comorbidity flags for each claim
        claims_with_flags = claims_df.copy()
        claims_with_flags['has_diabetes'] = False
        claims_with_flags['has_ckd'] = False
        claims_with_flags['has_cvd'] = False
        claims_with_flags['has_retinopathy'] = False
        
        for col in diag_cols:
            if col in claims_with_flags.columns:
                # Diabetes flags
                diabetes_mask = claims_with_flags[col].isin(self.config.diabetes_codes)
                claims_with_flags['has_diabetes'] = claims_with_flags['has_diabetes'] | diabetes_mask
                
                # CKD flags
                ckd_mask = claims_with_flags[col].isin(self.config.ckd_codes)
                claims_with_flags['has_ckd'] = claims_with_flags['has_ckd'] | ckd_mask
                
                # CVD flags
                cvd_mask = claims_with_flags[col].isin(self.config.cvd_codes)
                claims_with_flags['has_cvd'] = claims_with_flags['has_cvd'] | cvd_mask
                
                # Retinopathy flags
                retinopathy_mask = claims_with_flags[col].isin(self.config.retinopathy_codes)
                claims_with_flags['has_retinopathy'] = claims_with_flags['has_retinopathy'] | retinopathy_mask
        
        # Aggregate by member
        comorbidity_features = claims_with_flags.groupby('DESYNPUF_ID').agg({
            'has_diabetes': 'any',
            'has_ckd': 'any',
            'has_cvd': 'any',
            'has_retinopathy': 'any',
            'CLM_PMT_AMT': ['sum', 'mean', 'count']
        }).reset_index()
        
        # Flatten column names
        comorbidity_features.columns = [
            'DESYNPUF_ID', 'has_diabetes', 'has_ckd', 'has_cvd', 'has_retinopathy',
            f'{claim_type}_total_payment', f'{claim_type}_avg_payment', f'{claim_type}_claim_count'
        ]
        
        # Convert boolean flags to integers
        bool_cols = ['has_diabetes', 'has_ckd', 'has_cvd', 'has_retinopathy']
        for col in bool_cols:
            comorbidity_features[col] = comorbidity_features[col].astype(int)
        
        logger.info(f"Created {len(comorbidity_features.columns) - 1} comorbidity features")
        return comorbidity_features
    
    def create_utilization_features(self, claims_df: pd.DataFrame, claim_type: str) -> pd.DataFrame:
        """
        Create utilization features from claims data.
        
        Args:
            claims_df: Claims DataFrame
            claim_type: Type of claims ('inpatient' or 'outpatient')
            
        Returns:
            DataFrame with utilization features aggregated by member
        """
        logger.info(f"Creating utilization features from {claim_type} claims")
        
        # Calculate utilization metrics
        utilization_features = claims_df.groupby('DESYNPUF_ID').agg({
            'CLM_ID': 'count',  # Number of claims
            'CLM_PMT_AMT': ['sum', 'mean', 'std'],  # Payment statistics
            'CLM_FROM_DT': ['min', 'max'],  # Date range
        }).reset_index()
        
        # Flatten column names
        utilization_features.columns = [
            'DESYNPUF_ID', f'{claim_type}_claim_count',
            f'{claim_type}_total_payment', f'{claim_type}_avg_payment', f'{claim_type}_payment_std',
            f'{claim_type}_first_claim_date', f'{claim_type}_last_claim_date'
        ]
        
        # Calculate days between first and last claim
        utilization_features[f'{claim_type}_claim_span_days'] = (
            utilization_features[f'{claim_type}_last_claim_date'] - 
            utilization_features[f'{claim_type}_first_claim_date']
        ).dt.days
        
        # Calculate claims per month (approximate)
        utilization_features[f'{claim_type}_claims_per_month'] = (
            utilization_features[f'{claim_type}_claim_count'] / 
            (utilization_features[f'{claim_type}_claim_span_days'] / 30 + 1)
        )
        
        # Fill NaN values
        utilization_features = utilization_features.fillna(0)
        
        logger.info(f"Created {len(utilization_features.columns) - 1} utilization features")
        return utilization_features
    
    def create_diabetes_specific_features(self, beneficiary_df: pd.DataFrame, claims_data: Dict[str, pd.DataFrame]) -> pd.DataFrame:
        """
        Create diabetes-specific features based on HEDIS specifications.
        
        Args:
            beneficiary_df: Beneficiary DataFrame with SP_DIABETES flag
            claims_data: Dictionary of claims DataFrames
            
        Returns:
            DataFrame with diabetes-specific features
        """
        logger.info("Creating diabetes-specific features")
        
        diabetes_features = beneficiary_df[['DESYNPUF_ID']].copy()
        
        # Use SP_DIABETES flag from beneficiary data
        diabetes_features['has_diabetes_flag'] = (beneficiary_df['SP_DIABETES'] == 1).astype(int)
        
        # Combine diabetes flags from all claims sources
        diabetes_features['has_diabetes_claims'] = 0
        
        for claim_type, claims_df in claims_data.items():
            if 'has_diabetes_dx' in claims_df.columns:
                member_diabetes = claims_df.groupby('DESYNPUF_ID')['has_diabetes_dx'].any()
                diabetes_features[f'has_diabetes_{claim_type}'] = diabetes_features['DESYNPUF_ID'].map(
                    member_diabetes
                ).fillna(False).astype(int)
                
                # Update overall diabetes claims flag
                diabetes_features['has_diabetes_claims'] = (
                    diabetes_features['has_diabetes_claims'] | 
                    diabetes_features[f'has_diabetes_{claim_type}']
                )
        
        # Create comprehensive diabetes indicator
        diabetes_features['has_diabetes_comprehensive'] = (
            diabetes_features['has_diabetes_flag'] | 
            diabetes_features['has_diabetes_claims']
        ).astype(int)
        
        # Diabetes duration estimation (simplified)
        diabetes_features['diabetes_duration_estimated'] = 0  # Placeholder for future enhancement
        
        logger.info(f"Created {len(diabetes_features.columns) - 1} diabetes-specific features")
        return diabetes_features
    
    def create_all_features(self, processed_data: Dict[str, pd.DataFrame]) -> pd.DataFrame:
        """
        Create all HEDIS GSD features from processed data.
        
        Args:
            processed_data: Dictionary of processed DataFrames
            
        Returns:
            Complete feature DataFrame
        """
        logger.info("Creating comprehensive HEDIS GSD feature set")
        
        # Start with demographic features
        features_df = self.create_demographic_features(processed_data['beneficiary'])
        
        # Add comorbidity features from claims
        for claim_type in ['inpatient', 'outpatient']:
            if claim_type in processed_data:
                comorbidity_features = self.create_comorbidity_features(
                    processed_data[claim_type], claim_type
                )
                features_df = features_df.merge(
                    comorbidity_features, on='DESYNPUF_ID', how='left'
                )
                
                utilization_features = self.create_utilization_features(
                    processed_data[claim_type], claim_type
                )
                features_df = features_df.merge(
                    utilization_features, on='DESYNPUF_ID', how='left'
                )
        
        # Add diabetes-specific features
        diabetes_features = self.create_diabetes_specific_features(
            processed_data['beneficiary'], processed_data
        )
        features_df = features_df.merge(
            diabetes_features, on='DESYNPUF_ID', how='left'
        )
        
        # Fill missing values
        features_df = features_df.fillna(0)
        
        # Create summary statistics
        total_features = len(features_df.columns) - 1  # Exclude DESYNPUF_ID
        diabetes_members = features_df['has_diabetes_comprehensive'].sum()
        
        logger.info(f"Feature engineering completed:")
        logger.info(f"  - Total features: {total_features}")
        logger.info(f"  - Total members: {len(features_df)}")
        logger.info(f"  - Members with diabetes: {diabetes_members}")
        
        return features_df


def create_hedis_gsd_features(processed_data: Dict[str, pd.DataFrame], 
                              measurement_year: int = 2008) -> pd.DataFrame:
    """
    Convenience function to create all HEDIS GSD features.
    
    Args:
        processed_data: Dictionary of processed DataFrames
        measurement_year: HEDIS measurement year
        
    Returns:
        Complete feature DataFrame
    """
    config = HEDISConfig(measurement_year=measurement_year)
    engineer = HEDISFeatureEngineer(config)
    return engineer.create_all_features(processed_data)


if __name__ == "__main__":
    # Example usage
    from data_loader import load_cms_data
    from data_preprocessing import preprocess_cms_data
    
    try:
        # Load and preprocess data
        raw_data = load_cms_data()
        processed_data = preprocess_cms_data(raw_data)
        
        # Create features
        features_df = create_hedis_gsd_features(processed_data)
        
        print("Feature engineering completed successfully!")
        print(f"Total features: {len(features_df.columns) - 1}")
        print(f"Total members: {len(features_df)}")
        print(f"Members with diabetes: {features_df['has_diabetes_comprehensive'].sum()}")
        
    except Exception as e:
        print(f"Error in feature engineering: {e}")

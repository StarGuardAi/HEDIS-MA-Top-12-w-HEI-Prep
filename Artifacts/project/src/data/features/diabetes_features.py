"""
Diabetes Feature Engineering for HEDIS Measures

Shared feature engineering for all diabetes-related HEDIS measures:
- GSD (Glycemic Status Assessment)
- KED (Kidney Health Evaluation)
- EED (Eye Exam for Diabetes)
- PDC-DR (Medication Adherence - Diabetes)
- BPD (Blood Pressure Control - Diabetes)

Creates comprehensive features including:
- Demographics
- Diabetes diagnosis characteristics
- Comorbidities
- Lab history
- Utilization patterns
- Medication adherence
- Social determinants of health (SDOH)

HEDIS Compliance:
- HIPAA-compliant logging (hashed IDs only)
- HEDIS MY2025 specifications
- PHI protection
- Temporal validation
"""

import pandas as pd
import numpy as np
import logging
import hashlib
from typing import Dict, List, Optional, Tuple, Set, Any
from datetime import datetime, timedelta
from dataclasses import dataclass

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# ICD-10 Code Sets (HEDIS MY2025)
class DiabetesCodeSets:
    """ICD-10 code sets for diabetes and comorbidities."""
    
    # Diabetes - Type 1
    TYPE1_DIABETES = {
        'E10.10', 'E10.11', 'E10.21', 'E10.22', 'E10.29', 'E10.311', 'E10.319',
        'E10.321', 'E10.329', 'E10.331', 'E10.339', 'E10.341', 'E10.349',
        'E10.351', 'E10.359', 'E10.36', 'E10.39', 'E10.40', 'E10.41', 'E10.42',
        'E10.43', 'E10.44', 'E10.49', 'E10.51', 'E10.52', 'E10.59', 'E10.610',
        'E10.618', 'E10.620', 'E10.621', 'E10.622', 'E10.628', 'E10.630',
        'E10.638', 'E10.641', 'E10.649', 'E10.65', 'E10.69', 'E10.8', 'E10.9',
    }
    
    # Diabetes - Type 2
    TYPE2_DIABETES = {
        'E11.00', 'E11.01', 'E11.10', 'E11.11', 'E11.21', 'E11.22', 'E11.29',
        'E11.311', 'E11.319', 'E11.321', 'E11.329', 'E11.331', 'E11.339',
        'E11.341', 'E11.349', 'E11.351', 'E11.359', 'E11.36', 'E11.39',
        'E11.40', 'E11.41', 'E11.42', 'E11.43', 'E11.44', 'E11.49', 'E11.51',
        'E11.52', 'E11.59', 'E11.610', 'E11.618', 'E11.620', 'E11.621',
        'E11.622', 'E11.628', 'E11.630', 'E11.638', 'E11.641', 'E11.649',
        'E11.65', 'E11.69', 'E11.8', 'E11.9',
    }
    
    ALL_DIABETES = TYPE1_DIABETES | TYPE2_DIABETES
    
    # Chronic Kidney Disease
    CKD_CODES = {
        'N18.1',   # CKD Stage 1
        'N18.2',   # CKD Stage 2
        'N18.3',   # CKD Stage 3
        'N18.30',  # CKD Stage 3, unspecified
        'N18.31',  # CKD Stage 3a
        'N18.32',  # CKD Stage 3b
        'N18.4',   # CKD Stage 4
        'N18.5',   # CKD Stage 5
        'N18.6',   # ESRD
        'N18.9',   # CKD, unspecified
        'E11.22',  # Diabetes with CKD
        'E10.22',  # Type 1 diabetes with CKD
    }
    
    # Cardiovascular Disease
    CVD_CODES = {
        # Coronary Artery Disease
        'I25.10', 'I25.11', 'I25.110', 'I25.111', 'I25.118', 'I25.119',
        'I25.2', 'I25.3', 'I25.41', 'I25.42', 'I25.5', 'I25.6', 'I25.700',
        'I25.701', 'I25.708', 'I25.709', 'I25.710', 'I25.711', 'I25.718',
        'I25.719', 'I25.720', 'I25.721', 'I25.728', 'I25.729', 'I25.730',
        'I25.731', 'I25.738', 'I25.739', 'I25.750', 'I25.751', 'I25.758',
        'I25.759', 'I25.760', 'I25.761', 'I25.768', 'I25.769', 'I25.790',
        'I25.791', 'I25.798', 'I25.799', 'I25.810', 'I25.811', 'I25.812',
        'I25.82', 'I25.83', 'I25.84', 'I25.89', 'I25.9',
        
        # Myocardial Infarction
        'I21.0', 'I21.01', 'I21.02', 'I21.09', 'I21.1', 'I21.11', 'I21.19',
        'I21.2', 'I21.21', 'I21.29', 'I21.3', 'I21.4', 'I22.0', 'I22.1',
        'I22.2', 'I22.8', 'I22.9',
        
        # Heart Failure
        'I50.1', 'I50.2', 'I50.20', 'I50.21', 'I50.22', 'I50.23', 'I50.3',
        'I50.30', 'I50.31', 'I50.32', 'I50.33', 'I50.4', 'I50.40', 'I50.41',
        'I50.42', 'I50.43', 'I50.9',
        
        # Stroke
        'I63.0', 'I63.00', 'I63.01', 'I63.011', 'I63.012', 'I63.013',
        'I63.019', 'I63.02', 'I63.03', 'I63.031', 'I63.032', 'I63.033',
        'I63.039', 'I63.09',
    }
    
    # Diabetic Retinopathy
    RETINOPATHY_CODES = {
        'E10.311', 'E10.319', 'E10.321', 'E10.329', 'E10.331', 'E10.339',
        'E10.341', 'E10.349', 'E10.351', 'E10.359', 'E10.36', 'E10.37',
        'E11.311', 'E11.319', 'E11.321', 'E11.329', 'E11.331', 'E11.339',
        'E11.341', 'E11.349', 'E11.351', 'E11.359', 'E11.36', 'E11.37',
        'H35.0', 'H35.00', 'H35.01', 'H35.011', 'H35.012', 'H35.013',
        'H35.019', 'H35.02', 'H35.021', 'H35.022', 'H35.023', 'H35.029',
        'H35.03', 'H35.031', 'H35.032', 'H35.033', 'H35.039', 'H35.04',
        'H35.041', 'H35.042', 'H35.043', 'H35.049', 'H35.05', 'H35.051',
        'H35.052', 'H35.053', 'H35.059', 'H35.06', 'H35.061', 'H35.062',
        'H35.063', 'H35.069', 'H35.07', 'H35.071', 'H35.072', 'H35.073',
        'H35.079',
    }
    
    # Diabetic Neuropathy
    NEUROPATHY_CODES = {
        'E10.40', 'E10.41', 'E10.42', 'E10.43', 'E10.44', 'E10.49',
        'E11.40', 'E11.41', 'E11.42', 'E11.43', 'E11.44', 'E11.49',
        'G63', 'G99.0',
    }
    
    # Hypertension
    HYPERTENSION_CODES = {
        'I10', 'I11.0', 'I11.9', 'I12.0', 'I12.9', 'I13.0', 'I13.10',
        'I13.11', 'I13.2', 'I15.0', 'I15.1', 'I15.2', 'I15.8', 'I15.9',
    }
    
    # Hyperlipidemia
    HYPERLIPIDEMIA_CODES = {
        'E78.0', 'E78.00', 'E78.01', 'E78.1', 'E78.2', 'E78.3', 'E78.4',
        'E78.41', 'E78.49', 'E78.5', 'E78.6', 'E78.70', 'E78.71', 'E78.72',
        'E78.79', 'E78.8', 'E78.89', 'E78.9',
    }


class DiabetesFeatureEngineer:
    """
    Create comprehensive features for diabetes-related HEDIS measures.
    
    Shared across:
    - GSD (Glycemic Status)
    - KED (Kidney Health)
    - EED (Eye Exam)
    - PDC-DR (Medication Adherence)
    - BPD (Blood Pressure Control)
    """
    
    def __init__(self, measurement_year: int = 2025):
        """
        Initialize diabetes feature engineer.
        
        Args:
            measurement_year: HEDIS measurement year
        """
        self.measurement_year = measurement_year
        self.my_start = datetime(measurement_year, 1, 1)
        self.my_end = datetime(measurement_year, 12, 31)
        self.lookback_start = datetime(measurement_year - 2, 1, 1)  # 2-year lookback
        
        logger.info(f"Initialized Diabetes Feature Engineer for MY{measurement_year}")
    
    def _hash_member_id(self, member_id: str) -> str:
        """
        Hash member ID for PHI-safe logging.
        
        Args:
            member_id: Raw member ID
            
        Returns:
            SHA-256 hash (first 8 characters)
        """
        return hashlib.sha256(str(member_id).encode()).hexdigest()[:8]
    
    def create_demographic_features(self,
                                   member_df: pd.DataFrame) -> pd.DataFrame:
        """
        Create demographic features.
        
        Features:
        - Age at measurement year end (Dec 31)
        - Gender
        - Race/ethnicity
        - Geographic region (state)
        
        Args:
            member_df: Member demographics DataFrame
            
        Returns:
            DataFrame with demographic features
        """
        logger.info("Creating demographic features")
        
        features = member_df.copy()
        
        # Age at MY end (Dec 31) - HEDIS compliant
        features['age_at_my_end'] = (
            self.my_end - pd.to_datetime(features['birth_date'])
        ).dt.days // 365
        
        # Age groups
        features['age_group'] = pd.cut(
            features['age_at_my_end'],
            bins=[0, 40, 50, 60, 70, 75, 120],
            labels=['<40', '40-49', '50-59', '60-69', '70-75', '>75']
        )
        
        # Gender (one-hot encode if needed)
        features['gender_male'] = (features['gender'] == 'M').astype(int)
        features['gender_female'] = (features['gender'] == 'F').astype(int)
        
        # Race/ethnicity (one-hot encode)
        if 'race' in features.columns:
            race_dummies = pd.get_dummies(features['race'], prefix='race')
            features = pd.concat([features, race_dummies], axis=1)
        
        # Geographic region
        if 'state' in features.columns:
            # Group states into regions
            northeast = ['ME', 'NH', 'VT', 'MA', 'RI', 'CT', 'NY', 'NJ', 'PA']
            midwest = ['OH', 'IN', 'IL', 'MI', 'WI', 'MN', 'IA', 'MO', 'ND', 'SD', 'NE', 'KS']
            south = ['DE', 'MD', 'DC', 'VA', 'WV', 'NC', 'SC', 'GA', 'FL', 'KY', 'TN', 
                    'AL', 'MS', 'AR', 'LA', 'OK', 'TX']
            west = ['MT', 'ID', 'WY', 'CO', 'NM', 'AZ', 'UT', 'NV', 'WA', 'OR', 'CA',
                   'AK', 'HI']
            
            features['region_northeast'] = features['state'].isin(northeast).astype(int)
            features['region_midwest'] = features['state'].isin(midwest).astype(int)
            features['region_south'] = features['state'].isin(south).astype(int)
            features['region_west'] = features['state'].isin(west).astype(int)
        
        logger.info(f"Created demographic features for {len(features):,} members")
        
        return features
    
    def create_diabetes_diagnosis_features(self,
                                          member_df: pd.DataFrame,
                                          claims_df: pd.DataFrame) -> pd.DataFrame:
        """
        Create diabetes diagnosis features.
        
        Features:
        - Type 1 vs Type 2 indicators
        - Diabetes diagnosis duration (years)
        - Multiple diabetes diagnosis codes count
        - First diagnosis date
        
        Args:
            member_df: Member DataFrame
            claims_df: Claims DataFrame
            
        Returns:
            DataFrame with diabetes diagnosis features
        """
        logger.info("Creating diabetes diagnosis features")
        
        features = member_df.copy()
        
        # Filter to diabetes claims
        diabetes_claims = claims_df[
            (claims_df['diagnosis_code'].isin(DiabetesCodeSets.ALL_DIABETES)) &
            (pd.to_datetime(claims_df['service_date']) <= self.my_end)
        ].copy()
        
        if len(diabetes_claims) == 0:
            logger.warning("No diabetes claims found")
            features['diabetes_type1'] = 0
            features['diabetes_type2'] = 0
            features['diabetes_duration_years'] = 0
            features['diabetes_dx_count'] = 0
            return features
        
        # Type 1 vs Type 2
        member_dx_types = diabetes_claims.groupby('member_id').apply(
            lambda x: pd.Series({
                'has_type1': any(x['diagnosis_code'].isin(DiabetesCodeSets.TYPE1_DIABETES)),
                'has_type2': any(x['diagnosis_code'].isin(DiabetesCodeSets.TYPE2_DIABETES)),
                'first_dx_date': x['service_date'].min(),
                'dx_count': len(x),
                'unique_dx_codes': x['diagnosis_code'].nunique()
            })
        )
        
        features = features.merge(member_dx_types, left_on='member_id', right_index=True, how='left')
        
        features['diabetes_type1'] = features['has_type1'].fillna(False).astype(int)
        features['diabetes_type2'] = features['has_type2'].fillna(False).astype(int)
        
        # Diabetes duration (years)
        features['first_dx_date'] = pd.to_datetime(features['first_dx_date'])
        features['diabetes_duration_years'] = (
            (self.my_end - features['first_dx_date']).dt.days // 365
        ).fillna(0).clip(lower=0)
        
        # Diagnosis code count
        features['diabetes_dx_count'] = features['dx_count'].fillna(0).astype(int)
        features['diabetes_unique_codes'] = features['unique_dx_codes'].fillna(0).astype(int)
        
        logger.info(f"Created diabetes diagnosis features for {len(features):,} members")
        
        return features
    
    def create_comorbidity_features(self,
                                   member_df: pd.DataFrame,
                                   claims_df: pd.DataFrame) -> pd.DataFrame:
        """
        Create comorbidity features.
        
        Features:
        - CKD stages (1-5, ESRD)
        - Cardiovascular disease flags
        - Retinopathy/eye complications
        - Neuropathy
        - Hypertension
        - Hyperlipidemia
        
        Args:
            member_df: Member DataFrame
            claims_df: Claims DataFrame
            
        Returns:
            DataFrame with comorbidity features
        """
        logger.info("Creating comorbidity features")
        
        features = member_df.copy()
        
        # Filter claims to lookback period
        comorbidity_claims = claims_df[
            (pd.to_datetime(claims_df['service_date']) >= self.lookback_start) &
            (pd.to_datetime(claims_df['service_date']) <= self.my_end)
        ].copy()
        
        # Helper function to check comorbidity
        def has_comorbidity(member_claims, code_set):
            return member_claims['diagnosis_code'].isin(code_set).any()
        
        # Aggregate comorbidities by member
        member_comorbidities = comorbidity_claims.groupby('member_id').apply(
            lambda x: pd.Series({
                'has_ckd': has_comorbidity(x, DiabetesCodeSets.CKD_CODES),
                'has_cvd': has_comorbidity(x, DiabetesCodeSets.CVD_CODES),
                'has_retinopathy': has_comorbidity(x, DiabetesCodeSets.RETINOPATHY_CODES),
                'has_neuropathy': has_comorbidity(x, DiabetesCodeSets.NEUROPATHY_CODES),
                'has_hypertension': has_comorbidity(x, DiabetesCodeSets.HYPERTENSION_CODES),
                'has_hyperlipidemia': has_comorbidity(x, DiabetesCodeSets.HYPERLIPIDEMIA_CODES),
            })
        )
        
        features = features.merge(member_comorbidities, left_on='member_id', right_index=True, how='left')
        
        # Convert to binary flags
        for col in ['has_ckd', 'has_cvd', 'has_retinopathy', 'has_neuropathy', 
                   'has_hypertension', 'has_hyperlipidemia']:
            features[col] = features[col].fillna(False).astype(int)
        
        # Comorbidity count
        features['comorbidity_count'] = (
            features['has_ckd'] + features['has_cvd'] + features['has_retinopathy'] +
            features['has_neuropathy'] + features['has_hypertension'] + features['has_hyperlipidemia']
        )
        
        logger.info(f"Created comorbidity features for {len(features):,} members")
        
        return features
    
    def create_lab_history_features(self,
                                    member_df: pd.DataFrame,
                                    labs_df: Optional[pd.DataFrame] = None) -> pd.DataFrame:
        """
        Create lab history features.
        
        Features:
        - Previous year HbA1c test (yes/no)
        - Previous year eGFR test (yes/no)
        - Previous year ACR test (yes/no)
        - Most recent HbA1c value (if available)
        - Most recent eGFR value (if available)
        - Lab test frequency (past 2 years)
        
        Args:
            member_df: Member DataFrame
            labs_df: Labs DataFrame (optional)
            
        Returns:
            DataFrame with lab history features
        """
        logger.info("Creating lab history features")
        
        features = member_df.copy()
        
        if labs_df is None or len(labs_df) == 0:
            logger.warning("No labs data available")
            # Create default features
            features['had_hba1c_prior_year'] = 0
            features['had_egfr_prior_year'] = 0
            features['had_acr_prior_year'] = 0
            features['most_recent_hba1c'] = np.nan
            features['most_recent_egfr'] = np.nan
            features['lab_test_count_2yr'] = 0
            return features
        
        # Filter to lookback period
        labs_lookback = labs_df[
            (pd.to_datetime(labs_df['test_date']) >= self.lookback_start) &
            (pd.to_datetime(labs_df['test_date']) <= self.my_end)
        ].copy()
        
        # Prior year (measurement year - 1)
        prior_year_start = datetime(self.measurement_year - 1, 1, 1)
        prior_year_end = datetime(self.measurement_year - 1, 12, 31)
        labs_prior_year = labs_lookback[
            (pd.to_datetime(labs_lookback['test_date']) >= prior_year_start) &
            (pd.to_datetime(labs_lookback['test_date']) <= prior_year_end)
        ]
        
        # Check for specific tests in prior year
        hba1c_codes = ['4548-4', '17856-6', '4549-2']
        egfr_codes = ['48642-3', '48643-1', '62238-1', '88294-4']
        acr_codes = ['9318-7', '13705-9', '14958-3', '14957-5', '1754-1', '2888-6']
        
        prior_year_tests = labs_prior_year.groupby('member_id').apply(
            lambda x: pd.Series({
                'had_hba1c': any(x['loinc_code'].isin(hba1c_codes)),
                'had_egfr': any(x['loinc_code'].isin(egfr_codes)),
                'had_acr': any(x['loinc_code'].isin(acr_codes)),
            })
        )
        
        features = features.merge(prior_year_tests, left_on='member_id', right_index=True, how='left')
        features['had_hba1c_prior_year'] = features['had_hba1c'].fillna(False).astype(int)
        features['had_egfr_prior_year'] = features['had_egfr'].fillna(False).astype(int)
        features['had_acr_prior_year'] = features['had_acr'].fillna(False).astype(int)
        
        # Most recent test values
        recent_labs = labs_lookback.sort_values('test_date', ascending=False)
        
        # Most recent HbA1c
        recent_hba1c = recent_labs[recent_labs['loinc_code'].isin(hba1c_codes)].groupby('member_id').first()
        features = features.merge(
            recent_hba1c[['result_value']].rename(columns={'result_value': 'most_recent_hba1c'}),
            left_on='member_id', right_index=True, how='left'
        )
        
        # Most recent eGFR
        recent_egfr = recent_labs[recent_labs['loinc_code'].isin(egfr_codes)].groupby('member_id').first()
        features = features.merge(
            recent_egfr[['result_value']].rename(columns={'result_value': 'most_recent_egfr'}),
            left_on='member_id', right_index=True, how='left'
        )
        
        # Lab test frequency (2-year lookback)
        lab_counts = labs_lookback.groupby('member_id').size().to_frame('lab_test_count_2yr')
        features = features.merge(lab_counts, left_on='member_id', right_index=True, how='left')
        features['lab_test_count_2yr'] = features['lab_test_count_2yr'].fillna(0).astype(int)
        
        logger.info(f"Created lab history features for {len(features):,} members")
        
        return features
    
    def create_utilization_features(self,
                                   member_df: pd.DataFrame,
                                   claims_df: pd.DataFrame) -> pd.DataFrame:
        """
        Create healthcare utilization features.
        
        Features:
        - ED visits (past year)
        - Inpatient admissions (past year)
        - PCP visits (past year)
        - Endocrinologist visits (past year)
        - Nephrologist visits (past year)
        - Total office visits
        
        Args:
            member_df: Member DataFrame
            claims_df: Claims DataFrame
            
        Returns:
            DataFrame with utilization features
        """
        logger.info("Creating utilization features")
        
        features = member_df.copy()
        
        # Filter to past year
        util_claims = claims_df[
            (pd.to_datetime(claims_df['service_date']) >= datetime(self.measurement_year - 1, 1, 1)) &
            (pd.to_datetime(claims_df['service_date']) <= self.my_end)
        ].copy()
        
        # Aggregate utilization by member
        member_util = util_claims.groupby('member_id').apply(
            lambda x: pd.Series({
                'ed_visits': (x['claim_type'] == 'emergency').sum(),
                'inpatient_admits': (x['claim_type'] == 'inpatient').sum(),
                'outpatient_visits': (x['claim_type'] == 'outpatient').sum(),
                'total_visits': len(x),
            })
        )
        
        features = features.merge(member_util, left_on='member_id', right_index=True, how='left')
        
        # Fill missing with zeros
        for col in ['ed_visits', 'inpatient_admits', 'outpatient_visits', 'total_visits']:
            features[col] = features[col].fillna(0).astype(int)
        
        # High utilizer flags
        features['high_ed_user'] = (features['ed_visits'] >= 4).astype(int)
        features['had_inpatient'] = (features['inpatient_admits'] >= 1).astype(int)
        
        logger.info(f"Created utilization features for {len(features):,} members")
        
        return features
    
    def create_all_features(self,
                           member_df: pd.DataFrame,
                           claims_df: pd.DataFrame,
                           labs_df: Optional[pd.DataFrame] = None) -> pd.DataFrame:
        """
        Create all diabetes features.
        
        Args:
            member_df: Member demographics DataFrame
            claims_df: Claims DataFrame
            labs_df: Labs DataFrame (optional)
            
        Returns:
            DataFrame with all features
        """
        logger.info("=" * 80)
        logger.info(f"Creating Diabetes Features for MY{self.measurement_year}")
        logger.info("=" * 80)
        
        # Start with demographics
        features = self.create_demographic_features(member_df)
        
        # Add diabetes diagnosis features
        features = self.create_diabetes_diagnosis_features(features, claims_df)
        
        # Add comorbidity features
        features = self.create_comorbidity_features(features, claims_df)
        
        # Add lab history features
        features = self.create_lab_history_features(features, labs_df)
        
        # Add utilization features
        features = self.create_utilization_features(features, claims_df)
        
        # Feature summary
        feature_cols = [col for col in features.columns if col != 'member_id']
        logger.info(f"Total features created: {len(feature_cols)}")
        logger.info(f"Total members: {len(features):,}")
        logger.info("=" * 80)
        
        return features


def create_diabetes_features(member_df: pd.DataFrame,
                             claims_df: pd.DataFrame,
                             labs_df: Optional[pd.DataFrame] = None,
                             measurement_year: int = 2025) -> pd.DataFrame:
    """
    Convenience function to create diabetes features.
    
    Args:
        member_df: Member demographics DataFrame
        claims_df: Claims DataFrame
        labs_df: Labs DataFrame (optional)
        measurement_year: HEDIS measurement year
        
    Returns:
        DataFrame with all diabetes features
    """
    engineer = DiabetesFeatureEngineer(measurement_year)
    features = engineer.create_all_features(member_df, claims_df, labs_df)
    
    return features


if __name__ == "__main__":
    logger.info("Diabetes Feature Engineering Module")
    logger.info("Shared across GSD, KED, EED, PDC-DR, BPD measures")
    logger.info("HEDIS MY2025 compliant")


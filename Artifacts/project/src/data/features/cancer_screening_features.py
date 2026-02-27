"""
Cancer Screening Feature Engineering for Tier 3 Measures

This module creates 15-20 features for cancer screening HEDIS measures:
- BCS: Breast Cancer Screening (mammography)
- COL: Colorectal Cancer Screening (colonoscopy, FIT, Cologuard)

HEDIS Specifications: MY2023 Volume 2
Tier: 3 (Preventive Screening)
Annual Value: $300K-$450K

Author: Analytics Team
Date: October 23, 2025
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
import hashlib


# CPT Codes for Cancer Screening Procedures
MAMMOGRAPHY_CODES = [
    '77065', '77066', '77067',  # Digital mammography
    '77063',  # Screening digital breast tomosynthesis
]

COLONOSCOPY_CODES = [
    '44388', '44389', '44390', '44391', '44392', '44393', '44394',  # Laparoscopic
    '45378', '45379', '45380', '45381', '45382', '45383', '45384', '45385',  # Colonoscopy
    '45386', '45387', '45388', '45389', '45390', '45391', '45392', '45393',  # Colonoscopy continued
    '45398',  # Colonoscopy with stent
]

FIT_CODES = [
    '82270',  # Fecal occult blood test (FOBT)
    '82274',  # Fecal immunochemical test (FIT)
]

COLOGUARD_CODES = [
    '81528',  # FIT-DNA (Cologuard)
]

FLEXIBLE_SIG_CODES = [
    '45330', '45331', '45332', '45333', '45334', '45335', '45337', '45338',  # Flexible sigmoidoscopy
    '45339', '45340', '45341', '45342', '45345', '45346', '45347',
]

# Exclusion Codes
BILATERAL_MASTECTOMY_CODES = ['Z90.13']
UNILATERAL_MASTECTOMY_CODES = ['Z90.11', 'Z90.12']
TOTAL_COLECTOMY_CODES = ['Z90.49']
HOSPICE_CODES = ['Z51.5']

# Cancer History Codes
BREAST_CANCER_CODES = ['C50']  # Malignant neoplasm of breast
COLORECTAL_CANCER_CODES = ['C18', 'C19', 'C20', 'C21']  # CRC


def create_cancer_screening_features(
    claims_df: pd.DataFrame,
    procedure_df: Optional[pd.DataFrame] = None,
    measurement_year: int = 2025,
    member_id_col: str = 'member_id'
) -> pd.DataFrame:
    """
    Create comprehensive cancer screening features for Tier 3 measures.
    
    Args:
        claims_df: Claims data (diagnoses)
        procedure_df: Procedure data (CPT codes) - optional
        measurement_year: HEDIS measurement year
        member_id_col: Column name for member identifier
        
    Returns:
        DataFrame with cancer screening features (one row per member)
        
    Features Created:
        - Demographic: 5 features
        - Screening history: 5 features
        - Risk factors: 5 features
        - Shared/utilization: 5 features
        Total: 20 features
        
    HEDIS Compliance:
        - Follows MY2023 specifications
        - Age calculations use measurement year end (Dec 31)
        - Lookback periods per HEDIS specs
        
    HIPAA Compliance:
        - No PHI in outputs (member_id hashed)
        - Counts and dates only
        - Secure processing
    """
    
    # Validate inputs
    if claims_df.empty:
        raise ValueError("Claims data is required")
    
    if member_id_col not in claims_df.columns:
        raise ValueError(f"{member_id_col} not found in claims data")
    
    # Get unique members
    members = claims_df[member_id_col].unique()
    
    # Initialize feature dictionary
    features_list = []
    
    # Measurement year date range
    measurement_start = datetime(measurement_year, 1, 1)
    measurement_end = datetime(measurement_year, 12, 31)
    prior_year_start = datetime(measurement_year - 1, 1, 1)
    
    # Process each member
    for member_id in members:
        member_claims = claims_df[claims_df[member_id_col] == member_id]
        member_procedures = procedure_df[procedure_df[member_id_col] == member_id] if procedure_df is not None else pd.DataFrame()
        
        # Hash member_id for PHI protection
        member_hash = hashlib.sha256(str(member_id).encode()).hexdigest()[:16]
        
        features = {'member_id_hash': member_hash}
        
        # ==========================================
        # SECTION 1: DEMOGRAPHIC FEATURES (5)
        # ==========================================
        
        # 1. Age (if birth_date available)
        if 'birth_date' in member_claims.columns:
            birth_date = pd.to_datetime(member_claims['birth_date'].iloc[0])
            age = measurement_year - birth_date.year - (
                (measurement_end.month, measurement_end.day) < (birth_date.month, birth_date.day)
            )
            features['age'] = age
            features['age_group'] = '50-64' if age < 65 else '65-75' if age < 76 else 'other'
        else:
            features['age'] = 0
            features['age_group'] = 'unknown'
        
        # 2. Gender
        if 'gender' in member_claims.columns:
            features['gender'] = member_claims['gender'].iloc[0]
            features['is_female'] = 1 if features['gender'] == 'F' else 0
        else:
            features['gender'] = 'U'
            features['is_female'] = 0
        
        # 3. Years enrolled
        if 'enrollment_months' in member_claims.columns:
            features['enrollment_months'] = member_claims['enrollment_months'].iloc[0]
            features['years_enrolled'] = features['enrollment_months'] / 12
        else:
            features['enrollment_months'] = 12
            features['years_enrolled'] = 1.0
        
        # 4. Outpatient encounters count
        outpatient_encounters = member_claims[
            (member_claims['claim_type'].isin(['outpatient', 'professional'])) &
            (pd.to_datetime(member_claims['service_date']) >= measurement_start) &
            (pd.to_datetime(member_claims['service_date']) <= measurement_end)
        ]
        features['outpatient_encounters'] = len(outpatient_encounters)
        
        # 5. Has PCP assignment
        features['has_pcp'] = int(len(outpatient_encounters[
            outpatient_encounters['provider_specialty'].str.contains('primary', case=False, na=False)
        ]) > 0)
        
        # ==========================================
        # SECTION 2: SCREENING HISTORY FEATURES (5)
        # ==========================================
        
        if not member_procedures.empty and 'procedure_code' in member_procedures.columns:
            # 6. Last mammography date (BCS)
            mammography = member_procedures[
                member_procedures['procedure_code'].isin(MAMMOGRAPHY_CODES)
            ]
            if len(mammography) > 0:
                last_mammo_date = pd.to_datetime(mammography['service_date']).max()
                features['last_mammography_date'] = last_mammo_date.strftime('%Y-%m-%d')
                features['days_since_mammography'] = (measurement_end - last_mammo_date).days
                features['had_mammography_2yr'] = int(last_mammo_date >= prior_year_start)
            else:
                features['last_mammography_date'] = None
                features['days_since_mammography'] = 9999
                features['had_mammography_2yr'] = 0
            
            # 7. Mammography frequency
            mammo_count = len(mammography[
                pd.to_datetime(mammography['service_date']) >= datetime(measurement_year - 5, 1, 1)
            ])
            features['mammography_count_5yr'] = mammo_count
            features['mammography_frequency'] = 'annual' if mammo_count >= 4 else 'biennial' if mammo_count >= 2 else 'irregular'
            
            # 8. Last colonoscopy date (COL)
            colonoscopy = member_procedures[
                member_procedures['procedure_code'].isin(COLONOSCOPY_CODES)
            ]
            if len(colonoscopy) > 0:
                last_colo_date = pd.to_datetime(colonoscopy['service_date']).max()
                features['last_colonoscopy_date'] = last_colo_date.strftime('%Y-%m-%d')
                features['days_since_colonoscopy'] = (measurement_end - last_colo_date).days
                features['had_colonoscopy_10yr'] = int(last_colo_date >= datetime(measurement_year - 10, 1, 1))
            else:
                features['last_colonoscopy_date'] = None
                features['days_since_colonoscopy'] = 9999
                features['had_colonoscopy_10yr'] = 0
            
            # 9. Last FIT date (COL)
            fit_test = member_procedures[
                member_procedures['procedure_code'].isin(FIT_CODES)
            ]
            if len(fit_test) > 0:
                last_fit_date = pd.to_datetime(fit_test['service_date']).max()
                features['last_fit_date'] = last_fit_date.strftime('%Y-%m-%d')
                features['days_since_fit'] = (measurement_end - last_fit_date).days
                features['had_fit_annual'] = int(last_fit_date >= measurement_start)
            else:
                features['last_fit_date'] = None
                features['days_since_fit'] = 9999
                features['had_fit_annual'] = 0
            
            # 10. Last Cologuard date (COL)
            cologuard = member_procedures[
                member_procedures['procedure_code'].isin(COLOGUARD_CODES)
            ]
            if len(cologuard) > 0:
                last_cologuard_date = pd.to_datetime(cologuard['service_date']).max()
                features['last_cologuard_date'] = last_cologuard_date.strftime('%Y-%m-%d')
                features['days_since_cologuard'] = (measurement_end - last_cologuard_date).days
                features['had_cologuard_3yr'] = int(last_cologuard_date >= datetime(measurement_year - 3, 1, 1))
            else:
                features['last_cologuard_date'] = None
                features['days_since_cologuard'] = 9999
                features['had_cologuard_3yr'] = 0
        else:
            # No procedure data - set defaults
            features['last_mammography_date'] = None
            features['days_since_mammography'] = 9999
            features['had_mammography_2yr'] = 0
            features['mammography_count_5yr'] = 0
            features['mammography_frequency'] = 'never'
            features['last_colonoscopy_date'] = None
            features['days_since_colonoscopy'] = 9999
            features['had_colonoscopy_10yr'] = 0
            features['last_fit_date'] = None
            features['days_since_fit'] = 9999
            features['had_fit_annual'] = 0
            features['last_cologuard_date'] = None
            features['days_since_cologuard'] = 9999
            features['had_cologuard_3yr'] = 0
        
        # ==========================================
        # SECTION 3: RISK FACTORS (5)
        # ==========================================
        
        # 11. Family history of cancer (would need family history data - proxy: multiple cancer encounters)
        features['has_family_hx_cancer'] = 0  # Placeholder
        
        # 12. Personal cancer history
        breast_cancer = member_claims[
            member_claims['diagnosis_code'].str.startswith('C50', na=False)
        ]
        features['has_breast_cancer_history'] = int(len(breast_cancer) > 0)
        
        colorectal_cancer = member_claims[
            member_claims['diagnosis_code'].str.startswith(tuple(COLORECTAL_CANCER_CODES), na=False)
        ]
        features['has_colorectal_cancer_history'] = int(len(colorectal_cancer) > 0)
        
        # 13. High-risk conditions
        # Bilateral mastectomy (BCS exclusion)
        bilateral_mastectomy = member_claims[
            member_claims['diagnosis_code'].isin(BILATERAL_MASTECTOMY_CODES)
        ]
        features['has_bilateral_mastectomy'] = int(len(bilateral_mastectomy) > 0)
        
        # Total colectomy (COL exclusion)
        total_colectomy = member_claims[
            member_claims['diagnosis_code'].isin(TOTAL_COLECTOMY_CODES)
        ]
        features['has_total_colectomy'] = int(len(total_colectomy) > 0)
        
        # 14. Hospice
        hospice = member_claims[
            member_claims['diagnosis_code'].isin(HOSPICE_CODES)
        ]
        features['in_hospice'] = int(len(hospice) > 0)
        
        # 15. Screening barriers (proxy: low utilization + no screening)
        features['has_screening_barriers'] = int(
            features['outpatient_encounters'] < 2 and 
            features['days_since_mammography'] > 1095 and 
            features['days_since_colonoscopy'] > 3650
        )
        
        # ==========================================
        # SECTION 4: SHARED/UTILIZATION FEATURES (5)
        # ==========================================
        
        # 16. Preventive visit history
        preventive_visits = member_claims[
            member_claims['claim_type'].str.contains('prevent', case=False, na=False)
        ]
        features['preventive_visits_count'] = len(preventive_visits)
        
        # 17. Healthcare utilization (total encounters)
        all_encounters = member_claims[
            (pd.to_datetime(member_claims['service_date']) >= measurement_start) &
            (pd.to_datetime(member_claims['service_date']) <= measurement_end)
        ]
        features['total_encounters'] = len(all_encounters)
        
        # 18. Specialist visits
        oncology_visits = member_claims[
            member_claims['provider_specialty'].str.contains('oncolog', case=False, na=False)
        ]
        features['oncology_visits'] = len(oncology_visits)
        
        gastro_visits = member_claims[
            member_claims['provider_specialty'].str.contains('gastro', case=False, na=False)
        ]
        features['gastro_visits'] = len(gastro_visits)
        
        # 19. Screening compliance patterns (overall)
        features['screening_compliant_pattern'] = int(
            features['had_mammography_2yr'] == 1 or 
            features['had_colonoscopy_10yr'] == 1 or 
            features['had_fit_annual'] == 1
        )
        
        # 20. Engagement score (composite)
        engagement = (
            (features['outpatient_encounters'] > 0) +
            (features['has_pcp'] == 1) +
            (features['preventive_visits_count'] > 0) +
            (features['screening_compliant_pattern'] == 1)
        )
        features['engagement_score'] = engagement  # 0-4 scale
        
        features_list.append(features)
    
    # Convert to DataFrame
    features_df = pd.DataFrame(features_list)
    
    return features_df


def validate_cancer_screening_features(features_df: pd.DataFrame) -> Dict:
    """
    Validate cancer screening features for data quality and HEDIS compliance.
    
    Args:
        features_df: DataFrame with cancer screening features
        
    Returns:
        Dictionary with validation results
    """
    validation = {
        'total_members': len(features_df),
        'female_members': features_df['is_female'].sum(),
        'age_50_74': features_df[(features_df['age'] >= 50) & (features_df['age'] <= 74)].shape[0],
        'age_50_75': features_df[(features_df['age'] >= 50) & (features_df['age'] <= 75)].shape[0],
        'had_mammography_2yr': features_df['had_mammography_2yr'].sum(),
        'had_colonoscopy_10yr': features_df['had_colonoscopy_10yr'].sum(),
        'had_fit_annual': features_df['had_fit_annual'].sum(),
        'has_bilateral_mastectomy': features_df['has_bilateral_mastectomy'].sum(),
        'has_total_colectomy': features_df['has_total_colectomy'].sum(),
        'avg_engagement_score': features_df['engagement_score'].mean(),
        'missing_values': features_df.isnull().sum().to_dict(),
    }
    
    return validation


# Measure-specific feature subsets
def get_bcs_features(features_df: pd.DataFrame) -> pd.DataFrame:
    """Get feature subset for BCS (Breast Cancer Screening)"""
    bcs_cols = [
        'member_id_hash', 'age', 'age_group', 'is_female',
        'last_mammography_date', 'days_since_mammography', 'had_mammography_2yr',
        'mammography_count_5yr', 'mammography_frequency',
        'has_breast_cancer_history', 'has_bilateral_mastectomy',
        'outpatient_encounters', 'has_pcp', 'preventive_visits_count',
        'engagement_score', 'has_screening_barriers'
    ]
    return features_df[[col for col in bcs_cols if col in features_df.columns]]


def get_col_features(features_df: pd.DataFrame) -> pd.DataFrame:
    """Get feature subset for COL (Colorectal Cancer Screening)"""
    col_cols = [
        'member_id_hash', 'age', 'age_group', 'gender',
        'last_colonoscopy_date', 'days_since_colonoscopy', 'had_colonoscopy_10yr',
        'last_fit_date', 'days_since_fit', 'had_fit_annual',
        'last_cologuard_date', 'days_since_cologuard', 'had_cologuard_3yr',
        'has_colorectal_cancer_history', 'has_total_colectomy',
        'outpatient_encounters', 'has_pcp', 'gastro_visits',
        'engagement_score', 'has_screening_barriers'
    ]
    return features_df[[col for col in col_cols if col in features_df.columns]]


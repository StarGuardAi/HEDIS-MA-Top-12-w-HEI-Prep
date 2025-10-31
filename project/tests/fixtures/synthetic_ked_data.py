"""
Synthetic Test Data for KED (Kidney Health Evaluation) Measure

This module provides PHI-free synthetic test data for KED testing.
All data is generated and does not contain any real patient information.

Test Scenarios:
1. Compliant members (has both eGFR and ACR)
2. Gap members (missing eGFR, ACR, or both)
3. Excluded members (ESRD, kidney transplant)
4. Age-ineligible members
5. Non-diabetic members
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Tuple


def generate_synthetic_ked_members(measurement_year: int = 2025) -> pd.DataFrame:
    """
    Generate synthetic member demographics for KED testing.
    
    Returns:
        DataFrame with member demographics
    """
    my_end = datetime(measurement_year, 12, 31)
    
    members = [
        # Compliant members (in denominator and numerator)
        {
            'member_id': 'KED_COMPLIANT_001',
            'birth_date': my_end - timedelta(days=50*365),  # Age 50
            'gender': 'M',
            'race': 'White',
            'state': 'CA',
        },
        {
            'member_id': 'KED_COMPLIANT_002',
            'birth_date': my_end - timedelta(days=65*365),  # Age 65
            'gender': 'F',
            'race': 'Black',
            'state': 'NY',
        },
        
        # Gap members (in denominator, not in numerator)
        {
            'member_id': 'KED_GAP_EGFR_001',  # Missing eGFR only
            'birth_date': my_end - timedelta(days=55*365),  # Age 55
            'gender': 'F',
            'race': 'Hispanic',
            'state': 'TX',
        },
        {
            'member_id': 'KED_GAP_ACR_001',  # Missing ACR only
            'birth_date': my_end - timedelta(days=60*365),  # Age 60
            'gender': 'M',
            'race': 'Asian',
            'state': 'WA',
        },
        {
            'member_id': 'KED_GAP_BOTH_001',  # Missing both tests
            'birth_date': my_end - timedelta(days=45*365),  # Age 45
            'gender': 'F',
            'race': 'White',
            'state': 'FL',
        },
        
        # Excluded members (ESRD)
        {
            'member_id': 'KED_EXCLUDED_ESRD_001',
            'birth_date': my_end - timedelta(days=70*365),  # Age 70
            'gender': 'M',
            'race': 'White',
            'state': 'OH',
        },
        
        # Excluded members (Kidney Transplant)
        {
            'member_id': 'KED_EXCLUDED_TRANSPLANT_001',
            'birth_date': my_end - timedelta(days=55*365),  # Age 55
            'gender': 'F',
            'race': 'Black',
            'state': 'MI',
        },
        
        # Age-ineligible members
        {
            'member_id': 'KED_AGE_TOO_YOUNG_001',
            'birth_date': my_end - timedelta(days=17*365),  # Age 17
            'gender': 'M',
            'race': 'White',
            'state': 'CA',
        },
        {
            'member_id': 'KED_AGE_TOO_OLD_001',
            'birth_date': my_end - timedelta(days=76*365),  # Age 76
            'gender': 'F',
            'race': 'White',
            'state': 'AZ',
        },
        
        # Non-diabetic member
        {
            'member_id': 'KED_NO_DIABETES_001',
            'birth_date': my_end - timedelta(days=50*365),  # Age 50
            'gender': 'M',
            'race': 'White',
            'state': 'IL',
        },
    ]
    
    return pd.DataFrame(members)


def generate_synthetic_ked_claims(measurement_year: int = 2025) -> pd.DataFrame:
    """
    Generate synthetic claims for KED testing.
    
    Includes:
    - Diabetes diagnosis claims
    - ESRD exclusion claims
    - Kidney transplant exclusion claims
    """
    my_start = datetime(measurement_year, 1, 1)
    my_mid = datetime(measurement_year, 6, 15)
    prior_year = datetime(measurement_year - 1, 6, 15)
    
    claims = [
        # Compliant member 1 - diabetes diagnosis (2 outpatient)
        {
            'member_id': 'KED_COMPLIANT_001',
            'claim_id': 'CLM_001_1',
            'service_date': prior_year,
            'claim_type': 'outpatient',
            'diagnosis_code': 'E11.9',  # Type 2 diabetes
        },
        {
            'member_id': 'KED_COMPLIANT_001',
            'claim_id': 'CLM_001_2',
            'service_date': my_mid,
            'claim_type': 'outpatient',
            'diagnosis_code': 'E11.22',  # Diabetes with CKD
        },
        
        # Compliant member 2 - diabetes diagnosis (1 inpatient)
        {
            'member_id': 'KED_COMPLIANT_002',
            'claim_id': 'CLM_002_1',
            'service_date': my_mid,
            'claim_type': 'inpatient',
            'diagnosis_code': 'E11.9',  # Type 2 diabetes
        },
        
        # Gap member - missing eGFR (has diabetes)
        {
            'member_id': 'KED_GAP_EGFR_001',
            'claim_id': 'CLM_003_1',
            'service_date': prior_year,
            'claim_type': 'outpatient',
            'diagnosis_code': 'E11.9',
        },
        {
            'member_id': 'KED_GAP_EGFR_001',
            'claim_id': 'CLM_003_2',
            'service_date': my_mid,
            'claim_type': 'outpatient',
            'diagnosis_code': 'E11.9',
        },
        
        # Gap member - missing ACR (has diabetes)
        {
            'member_id': 'KED_GAP_ACR_001',
            'claim_id': 'CLM_004_1',
            'service_date': prior_year,
            'claim_type': 'outpatient',
            'diagnosis_code': 'E10.9',  # Type 1 diabetes
        },
        {
            'member_id': 'KED_GAP_ACR_001',
            'claim_id': 'CLM_004_2',
            'service_date': my_mid,
            'claim_type': 'outpatient',
            'diagnosis_code': 'E10.9',
        },
        
        # Gap member - missing both (has diabetes)
        {
            'member_id': 'KED_GAP_BOTH_001',
            'claim_id': 'CLM_005_1',
            'service_date': my_mid,
            'claim_type': 'inpatient',
            'diagnosis_code': 'E11.9',
        },
        
        # Excluded member - ESRD (has diabetes + ESRD)
        {
            'member_id': 'KED_EXCLUDED_ESRD_001',
            'claim_id': 'CLM_006_1',
            'service_date': prior_year,
            'claim_type': 'outpatient',
            'diagnosis_code': 'E11.9',  # Diabetes
        },
        {
            'member_id': 'KED_EXCLUDED_ESRD_001',
            'claim_id': 'CLM_006_2',
            'service_date': my_mid,
            'claim_type': 'outpatient',
            'diagnosis_code': 'E11.9',  # Diabetes
        },
        {
            'member_id': 'KED_EXCLUDED_ESRD_001',
            'claim_id': 'CLM_006_3',
            'service_date': my_mid,
            'claim_type': 'inpatient',
            'diagnosis_code': 'N18.6',  # ESRD (exclusion)
        },
        
        # Excluded member - Kidney Transplant (has diabetes + transplant)
        {
            'member_id': 'KED_EXCLUDED_TRANSPLANT_001',
            'claim_id': 'CLM_007_1',
            'service_date': prior_year,
            'claim_type': 'outpatient',
            'diagnosis_code': 'E11.9',  # Diabetes
        },
        {
            'member_id': 'KED_EXCLUDED_TRANSPLANT_001',
            'claim_id': 'CLM_007_2',
            'service_date': my_mid,
            'claim_type': 'outpatient',
            'diagnosis_code': 'E11.9',  # Diabetes
        },
        {
            'member_id': 'KED_EXCLUDED_TRANSPLANT_001',
            'claim_id': 'CLM_007_3',
            'service_date': my_mid,
            'claim_type': 'outpatient',
            'diagnosis_code': 'Z94.0',  # Kidney transplant (exclusion)
        },
        
        # Age-ineligible members (has diabetes but wrong age)
        {
            'member_id': 'KED_AGE_TOO_YOUNG_001',
            'claim_id': 'CLM_008_1',
            'service_date': prior_year,
            'claim_type': 'outpatient',
            'diagnosis_code': 'E10.9',  # Type 1 diabetes
        },
        {
            'member_id': 'KED_AGE_TOO_YOUNG_001',
            'claim_id': 'CLM_008_2',
            'service_date': my_mid,
            'claim_type': 'outpatient',
            'diagnosis_code': 'E10.9',
        },
        {
            'member_id': 'KED_AGE_TOO_OLD_001',
            'claim_id': 'CLM_009_1',
            'service_date': my_mid,
            'claim_type': 'inpatient',
            'diagnosis_code': 'E11.9',
        },
        
        # Non-diabetic member (no diabetes claims)
        {
            'member_id': 'KED_NO_DIABETES_001',
            'claim_id': 'CLM_010_1',
            'service_date': my_mid,
            'claim_type': 'outpatient',
            'diagnosis_code': 'I10',  # Hypertension (not diabetes)
        },
    ]
    
    return pd.DataFrame(claims)


def generate_synthetic_ked_labs(measurement_year: int = 2025) -> pd.DataFrame:
    """
    Generate synthetic lab results for KED testing.
    
    Includes:
    - eGFR tests (LOINC codes)
    - ACR/Urine albumin tests (LOINC codes)
    """
    my_start = datetime(measurement_year, 1, 1)
    my_q1 = datetime(measurement_year, 3, 15)
    my_q2 = datetime(measurement_year, 6, 15)
    my_q3 = datetime(measurement_year, 9, 15)
    prior_year = datetime(measurement_year - 1, 6, 15)
    
    labs = [
        # Compliant member 1 - has both eGFR and ACR
        {
            'member_id': 'KED_COMPLIANT_001',
            'test_date': my_q2,
            'loinc_code': '48642-3',  # eGFR CKD-EPI
            'result_value': 65.0,
            'result_unit': 'mL/min/1.73m2',
        },
        {
            'member_id': 'KED_COMPLIANT_001',
            'test_date': my_q2,
            'loinc_code': '9318-7',  # ACR
            'result_value': 25.0,
            'result_unit': 'mg/g',
        },
        
        # Compliant member 2 - has both eGFR and ACR (different dates)
        {
            'member_id': 'KED_COMPLIANT_002',
            'test_date': my_q1,
            'loinc_code': '48643-1',  # eGFR MDRD
            'result_value': 55.0,
            'result_unit': 'mL/min/1.73m2',
        },
        {
            'member_id': 'KED_COMPLIANT_002',
            'test_date': my_q3,
            'loinc_code': '13705-9',  # ACR First Morning
            'result_value': 120.0,
            'result_unit': 'mg/g',
        },
        
        # Gap member - missing eGFR (has ACR only)
        {
            'member_id': 'KED_GAP_EGFR_001',
            'test_date': my_q2,
            'loinc_code': '9318-7',  # ACR
            'result_value': 35.0,
            'result_unit': 'mg/g',
        },
        
        # Gap member - missing ACR (has eGFR only)
        {
            'member_id': 'KED_GAP_ACR_001',
            'test_date': my_q2,
            'loinc_code': '48642-3',  # eGFR
            'result_value': 70.0,
            'result_unit': 'mL/min/1.73m2',
        },
        
        # Gap member - missing both (no labs in MY)
        # (no lab records for KED_GAP_BOTH_001)
        
        # Gap member - has labs but from PRIOR year (doesn't count)
        {
            'member_id': 'KED_GAP_BOTH_001',
            'test_date': prior_year,
            'loinc_code': '48642-3',  # eGFR
            'result_value': 60.0,
            'result_unit': 'mL/min/1.73m2',
        },
        
        # Excluded members still have labs (but excluded from denominator)
        {
            'member_id': 'KED_EXCLUDED_ESRD_001',
            'test_date': my_q2,
            'loinc_code': '48642-3',  # eGFR
            'result_value': 12.0,  # Low eGFR (ESRD range)
            'result_unit': 'mL/min/1.73m2',
        },
        {
            'member_id': 'KED_EXCLUDED_ESRD_001',
            'test_date': my_q2,
            'loinc_code': '9318-7',  # ACR
            'result_value': 500.0,  # High ACR
            'result_unit': 'mg/g',
        },
        
        # Age-ineligible members may have labs (but not in denominator)
        {
            'member_id': 'KED_AGE_TOO_YOUNG_001',
            'test_date': my_q2,
            'loinc_code': '48642-3',  # eGFR
            'result_value': 95.0,
            'result_unit': 'mL/min/1.73m2',
        },
    ]
    
    return pd.DataFrame(labs)


def get_synthetic_ked_test_data(measurement_year: int = 2025) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """
    Get complete synthetic test data for KED testing.
    
    Returns:
        Tuple of (member_df, claims_df, labs_df)
    """
    member_df = generate_synthetic_ked_members(measurement_year)
    claims_df = generate_synthetic_ked_claims(measurement_year)
    labs_df = generate_synthetic_ked_labs(measurement_year)
    
    return member_df, claims_df, labs_df


# Expected results for validation
EXPECTED_KED_RESULTS = {
    'measurement_year': 2025,
    'denominator': 5,  # 2 compliant + 3 gap members (excluding ESRD, transplant, age-ineligible, non-diabetic)
    'numerator': 2,    # 2 compliant members
    'rate': 40.0,      # 2/5 = 40%
    'gaps': {
        'total_gaps': 3,
        'missing_egfr': 1,   # KED_GAP_EGFR_001
        'missing_acr': 1,    # KED_GAP_ACR_001
        'missing_both': 1,   # KED_GAP_BOTH_001
    },
}


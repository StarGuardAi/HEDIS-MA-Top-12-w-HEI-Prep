"""
Synthetic Test Data for EED (Eye Exam for Diabetes) Measure

PHI-Free synthetic data for testing EED measure logic.
All member IDs and dates are fabricated for testing purposes.

Test Scenarios:
1. Compliant members (with eye exams)
2. Gap members (no eye exams)
3. Excluded members (hospice)
4. Edge cases (multiple exams, prior year exams)
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta


def generate_synthetic_eed_members():
    """
    Generate synthetic member demographics for EED testing.
    
    Returns 10 members with various scenarios:
    - Ages: 18-75 (eligible) and outside range (ineligible)
    - Birth dates calculated for measurement year 2023
    """
    members = pd.DataFrame({
        "DESYNPUF_ID": [f"M{str(i).zfill(5)}" for i in range(1, 11)],
        "BENE_BIRTH_DT": [
            "1970-06-15",  # M00001: Age 53 (eligible)
            "1955-03-20",  # M00002: Age 68 (eligible)
            "1980-11-10",  # M00003: Age 43 (eligible)
            "1990-01-05",  # M00004: Age 33 (eligible)
            "2010-07-22",  # M00005: Age 13 (too young)
            "1940-12-31",  # M00006: Age 83 (too old)
            "1965-04-18",  # M00007: Age 58 (eligible)
            "1975-09-25",  # M00008: Age 48 (eligible)
            "1968-08-14",  # M00009: Age 55 (eligible, hospice)
            "1972-02-28",  # M00010: Age 51 (eligible)
        ],
        "BENE_SEX_IDENT_CD": [1, 2, 1, 2, 1, 2, 1, 2, 1, 2],  # 1=M, 2=F
    })
    
    return members


def generate_synthetic_eed_claims():
    """
    Generate synthetic claims with diabetes diagnosis and exclusions.
    
    Scenarios:
    - M00001-M00004, M00007-M00010: Diabetes diagnosis
    - M00005-M00006: No diabetes (ineligible)
    - M00009: Hospice exclusion
    """
    # Diabetes claims (E11.9 = Type 2 diabetes without complications)
    diabetes_members = ["M00001", "M00002", "M00003", "M00004", 
                       "M00007", "M00008", "M00009", "M00010"]
    
    claims = []
    for member_id in diabetes_members:
        claims.append({
            "DESYNPUF_ID": member_id,
            "CLM_FROM_DT": "2023-03-15",
            "CLM_THRU_DT": "2023-03-15",
            "ICD9_DGNS_CD_1": "E11.9",  # Type 2 diabetes
            "ICD9_DGNS_CD_2": None,
            "HCPCS_CD_1": "99213",  # Office visit
        })
    
    # Hospice claim for M00009 (exclusion)
    claims.append({
        "DESYNPUF_ID": "M00009",
        "CLM_FROM_DT": "2023-06-01",
        "CLM_THRU_DT": "2023-06-01",
        "ICD9_DGNS_CD_1": "Z51.5",  # Hospice care
        "ICD9_DGNS_CD_2": "E11.9",  # Type 2 diabetes
        "HCPCS_CD_1": "99213",
    })
    
    claims_df = pd.DataFrame(claims)
    return claims_df


def generate_synthetic_eed_procedures():
    """
    Generate synthetic eye exam procedures.
    
    Scenarios:
    - M00001: Compliant (retinal exam in 2023)
    - M00002: Compliant (comprehensive eye exam in 2023)
    - M00003: Gap (no eye exam)
    - M00004: Gap (no eye exam)
    - M00007: Compliant (multiple exams in 2023)
    - M00008: Gap (exam in 2022, not 2023)
    - M00010: Compliant (OCT imaging in 2023)
    """
    procedures = [
        # M00001: Compliant (retinal exam)
        {
            "member_id": "M00001",
            "procedure_code": "92225",  # Ophthalmoscopy, extended
            "service_date": pd.Timestamp("2023-05-10"),
            "claim_type": "outpatient"
        },
        
        # M00002: Compliant (comprehensive eye exam)
        {
            "member_id": "M00002",
            "procedure_code": "92014",  # Comprehensive exam, established patient
            "service_date": pd.Timestamp("2023-07-22"),
            "claim_type": "outpatient"
        },
        
        # M00007: Compliant (multiple exams)
        {
            "member_id": "M00007",
            "procedure_code": "92002",  # Medical exam, new patient
            "service_date": pd.Timestamp("2023-02-15"),
            "claim_type": "outpatient"
        },
        {
            "member_id": "M00007",
            "procedure_code": "92250",  # Fundus photography
            "service_date": pd.Timestamp("2023-08-30"),
            "claim_type": "outpatient"
        },
        
        # M00008: Gap (exam in prior year only)
        {
            "member_id": "M00008",
            "procedure_code": "92014",  # Comprehensive exam
            "service_date": pd.Timestamp("2022-11-10"),
            "claim_type": "outpatient"
        },
        
        # M00010: Compliant (OCT imaging)
        {
            "member_id": "M00010",
            "procedure_code": "92134",  # OCT imaging
            "service_date": pd.Timestamp("2023-09-05"),
            "claim_type": "outpatient"
        },
    ]
    
    procedures_df = pd.DataFrame(procedures)
    return procedures_df


def get_expected_eed_results():
    """
    Expected results for EED measure calculation.
    
    Returns dictionary with expected outcomes for each test member.
    """
    return {
        "M00001": {
            "in_denominator": True,      # Age 53, diabetes
            "excluded": False,
            "has_eye_exam": True,        # Retinal exam in 2023
            "numerator_compliant": True,
            "has_gap": False,
        },
        "M00002": {
            "in_denominator": True,      # Age 68, diabetes
            "excluded": False,
            "has_eye_exam": True,        # Comprehensive exam in 2023
            "numerator_compliant": True,
            "has_gap": False,
        },
        "M00003": {
            "in_denominator": True,      # Age 43, diabetes
            "excluded": False,
            "has_eye_exam": False,       # No eye exam
            "numerator_compliant": False,
            "has_gap": True,             # GAP: No eye exam
        },
        "M00004": {
            "in_denominator": True,      # Age 33, diabetes
            "excluded": False,
            "has_eye_exam": False,       # No eye exam
            "numerator_compliant": False,
            "has_gap": True,             # GAP: No eye exam
        },
        "M00005": {
            "in_denominator": False,     # Age 13 (too young)
            "excluded": False,
            "has_eye_exam": False,
            "numerator_compliant": False,
            "has_gap": False,
        },
        "M00006": {
            "in_denominator": False,     # Age 83 (too old)
            "excluded": False,
            "has_eye_exam": False,
            "numerator_compliant": False,
            "has_gap": False,
        },
        "M00007": {
            "in_denominator": True,      # Age 58, diabetes
            "excluded": False,
            "has_eye_exam": True,        # Multiple exams in 2023
            "numerator_compliant": True,
            "has_gap": False,
        },
        "M00008": {
            "in_denominator": True,      # Age 48, diabetes
            "excluded": False,
            "has_eye_exam": False,       # Exam in 2022, not 2023
            "numerator_compliant": False,
            "has_gap": True,             # GAP: No exam in measurement year
        },
        "M00009": {
            "in_denominator": True,      # Age 55, diabetes
            "excluded": True,            # EXCLUDED: Hospice
            "has_eye_exam": False,
            "numerator_compliant": False,
            "has_gap": False,            # Excluded, not a gap
        },
        "M00010": {
            "in_denominator": True,      # Age 51, diabetes
            "excluded": False,
            "has_eye_exam": True,        # OCT imaging in 2023
            "numerator_compliant": True,
            "has_gap": False,
        },
    }


def get_expected_eed_summary():
    """
    Expected summary statistics for EED measure.
    """
    return {
        "denominator": 8,           # Ages 18-75 with diabetes
        "exclusions": 1,            # M00009 (hospice)
        "eligible_population": 7,   # Denominator - exclusions
        "numerator": 4,             # M00001, M00002, M00007, M00010 (compliant)
        "gaps": 3,                  # M00003, M00004, M00008 (gaps)
        "compliance_rate": 57.14,   # 4/7 = 57.14%
        "gap_rate": 42.86,          # 3/7 = 42.86%
    }


# Test scenarios documentation
TEST_SCENARIOS = {
    "compliant_members": {
        "M00001": "Retinal exam (ophthalmoscopy) in measurement year",
        "M00002": "Comprehensive eye exam in measurement year",
        "M00007": "Multiple eye exams in measurement year",
        "M00010": "OCT imaging in measurement year",
    },
    "gap_members": {
        "M00003": "No eye exam in measurement year",
        "M00004": "No eye exam in measurement year",
        "M00008": "Eye exam in prior year only (2022)",
    },
    "excluded_members": {
        "M00009": "Hospice care (Z51.5 diagnosis)",
    },
    "ineligible_members": {
        "M00005": "Age 13 (below minimum age 18)",
        "M00006": "Age 83 (above maximum age 75)",
    }
}

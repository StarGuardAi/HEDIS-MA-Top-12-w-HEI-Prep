"""
PHI-free synthetic claims data for testing

All data is synthetic and does not contain real patient information.
Complies with HIPAA Safe Harbor de-identification method.
"""

import pandas as pd
from datetime import datetime, timedelta

def get_sample_claims():
    """
    Generate synthetic claims data for testing.
    
    Returns:
        pd.DataFrame: Synthetic claims data
    """
    # Synthetic patient IDs (hashed/anonymized)
    patient_ids = [f"SYNTH_{i:06d}" for i in range(1, 101)]
    
    claims_data = []
    
    for patient_id in patient_ids[:20]:  # 20 sample patients
        # Generate 1-5 claims per patient
        num_claims = 3
        base_date = datetime(2023, 1, 1)
        
        for i in range(num_claims):
            claim = {
                'member_id': patient_id,
                'claim_id': f"CLM_{patient_id}_{i:03d}",
                'service_date': (base_date + timedelta(days=i*30)).strftime('%Y-%m-%d'),
                'diagnosis_code': 'E11.9',  # Type 2 diabetes without complications
                'procedure_code': '99213',   # Office visit
                'provider_id': f"PROV_{(hash(patient_id) % 100):03d}",
                'claim_amount': 150.00 + (i * 25),
                'age': 65 + (hash(patient_id) % 20),
                'gender': 'M' if hash(patient_id) % 2 == 0 else 'F'
            }
            claims_data.append(claim)
    
    return pd.DataFrame(claims_data)


def get_sample_lab_results():
    """
    Generate synthetic lab results for testing.
    
    Returns:
        pd.DataFrame: Synthetic lab results
    """
    patient_ids = [f"SYNTH_{i:06d}" for i in range(1, 21)]
    
    lab_data = []
    
    for patient_id in patient_ids:
        # HbA1c test result
        lab = {
            'member_id': patient_id,
            'test_date': '2023-06-15',
            'test_code': '83036',  # HbA1c CPT code
            'test_name': 'Hemoglobin A1c',
            'result_value': 7.5 + (hash(patient_id) % 3),  # Range: 7.5-10.5
            'result_unit': '%',
            'reference_range': '<7.0',
            'abnormal_flag': 'H'  # High
        }
        lab_data.append(lab)
    
    return pd.DataFrame(lab_data)


def get_sample_members():
    """
    Generate synthetic member demographic data for testing.
    
    Returns:
        pd.DataFrame: Synthetic member data
    """
    patient_ids = [f"SYNTH_{i:06d}" for i in range(1, 21)]
    
    member_data = []
    
    for patient_id in patient_ids:
        member = {
            'member_id': patient_id,
            'birth_year': 1958 + (hash(patient_id) % 20),  # Ages 65-85 in 2023
            'gender': 'M' if hash(patient_id) % 2 == 0 else 'F',
            'zip_code': f"{90000 + (hash(patient_id) % 1000):05d}",  # Synthetic ZIP
            'plan_type': 'HMO' if hash(patient_id) % 2 == 0 else 'PPO',
            'enrollment_months': 12,
            'chronic_conditions': ['diabetes', 'hypertension'] if hash(patient_id) % 3 == 0 else ['diabetes']
        }
        member_data.append(member)
    
    return pd.DataFrame(member_data)


# PHI-free test constants
SAMPLE_ICD10_CODES = {
    'diabetes_type2': ['E11.9', 'E11.65', 'E11.21'],
    'diabetes_complications': ['E11.36', 'E11.42', 'E11.51'],
    'hypertension': ['I10', 'I11.9'],
    'ckd': ['N18.1', 'N18.2', 'N18.3']
}

SAMPLE_CPT_CODES = {
    'office_visit': ['99213', '99214', '99215'],
    'hba1c': ['83036', '83037'],
    'lipid_panel': ['80061']
}


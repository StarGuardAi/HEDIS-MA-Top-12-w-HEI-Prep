"""
SUPD - Statin Therapy for Patients with Diabetes

HEDIS Measure: Statin Therapy for Patients with Diabetes (SUPD)
Specification: MY2023 Volume 2
Star Rating Weight: 1x
Tier: 2 (Cardiovascular Comorbidity)
Annual Value: $120K-$180K (100K member plan)

Description:
The percentage of members 40-75 years of age with diabetes who received a statin
medication during the measurement year.

Population:
- Adults 40-75 years with diabetes diagnosis
- In current or prior measurement year
- Exclude: Pregnancy, end-stage renal disease, cirrhosis, hospice

Numerator:
- At least one statin prescription filled in measurement year

Denominator:
- Members with diabetes aged 40-75
- At least one outpatient encounter in measurement year

Author: Analytics Team
Date: October 23, 2025
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import List, Dict, Tuple, Optional


# ICD-10 Codes for Diabetes
DIABETES_CODES = [
    'E10', 'E11', 'E13',  # Diabetes types
]

# Exclusion Codes
PREGNANCY_CODES = ['O09', 'O10', 'O11', 'O12', 'O13', 'O14', 'O15', 'O16', 'Z33', 'Z34']
ESRD_CODES = ['N18.6', 'Z99.2']  # End-stage renal disease
CIRRHOSIS_CODES = ['K70.3', 'K71.7', 'K74']  # Liver cirrhosis
HOSPICE_CODES = ['Z51.5']

# Statin Medications (NDC code patterns or medication names)
STATIN_MEDICATIONS = [
    'atorvastatin', 'simvastatin', 'rosuvastatin', 'pravastatin',
    'lovastatin', 'fluvastatin', 'pitavastatin'
]

# Statin Potency Classification
HIGH_POTENCY_STATINS = ['atorvastatin 40', 'atorvastatin 80', 'rosuvastatin 20', 'rosuvastatin 40']
MODERATE_POTENCY_STATINS = ['atorvastatin 10', 'atorvastatin 20', 'simvastatin 20', 'simvastatin 40',
                            'pravastatin 40', 'pravastatin 80', 'lovastatin 40', 'fluvastatin 80',
                            'pitavastatin 2', 'pitavastatin 4']
LOW_POTENCY_STATINS = ['simvastatin 10', 'pravastatin 10', 'pravastatin 20', 'lovastatin 20',
                       'fluvastatin 20', 'fluvastatin 40']


class SUPDMeasure:
    """
    SUPD (Statin Therapy for Patients with Diabetes) Measure Calculator
    
    This class implements HEDIS SUPD measure logic for identifying
    diabetic patients who received statin therapy.
    """
    
    def __init__(self, measurement_year: int = 2025):
        """
        Initialize SUPD measure calculator.
        
        Args:
            measurement_year: HEDIS measurement year
        """
        self.measurement_year = measurement_year
        self.measurement_start = datetime(measurement_year, 1, 1)
        self.measurement_end = datetime(measurement_year, 12, 31)
        self.prior_year_start = datetime(measurement_year - 1, 1, 1)
        self.prior_year_end = datetime(measurement_year - 1, 12, 31)
    
    def calculate_age(self, birth_date: datetime) -> int:
        """
        Calculate age as of December 31 of measurement year (HEDIS standard).
        
        Args:
            birth_date: Member's date of birth
            
        Returns:
            Age in years
        """
        return self.measurement_year - birth_date.year - (
            (self.measurement_end.month, self.measurement_end.day) <
            (birth_date.month, birth_date.day)
        )
    
    def is_in_denominator(
        self,
        member_df: pd.DataFrame,
        claims_df: pd.DataFrame
    ) -> Tuple[bool, str]:
        """
        Determine if member is in SUPD denominator.
        
        Denominator Criteria:
        1. Age 40-75 as of December 31 of measurement year
        2. Diabetes diagnosis in current or prior year
        3. At least one outpatient encounter in measurement year
        4. Continuous enrollment in measurement year
        5. No exclusions (pregnancy, ESRD, cirrhosis, hospice)
        
        Args:
            member_df: Member demographic data
            claims_df: Member's claims data
            
        Returns:
            Tuple of (is_in_denominator: bool, reason: str)
        """
        # Check age
        if 'birth_date' not in member_df.columns:
            return False, "Missing birth_date"
        
        birth_date = pd.to_datetime(member_df['birth_date'].iloc[0])
        age = self.calculate_age(birth_date)
        
        if age < 40 or age > 75:
            return False, f"Age {age} outside range 40-75"
        
        # Check for diabetes diagnosis in current or prior year
        diabetes_claims = claims_df[
            (claims_df['diagnosis_code'].str.startswith(tuple(DIABETES_CODES), na=False)) &
            (pd.to_datetime(claims_df['service_date']) >= self.prior_year_start) &
            (pd.to_datetime(claims_df['service_date']) <= self.measurement_end)
        ]
        
        if len(diabetes_claims) == 0:
            return False, "No diabetes diagnosis in measurement or prior year"
        
        # Check for at least one outpatient encounter in measurement year
        outpatient_encounters = claims_df[
            (claims_df['claim_type'].isin(['outpatient', 'professional'])) &
            (pd.to_datetime(claims_df['service_date']) >= self.measurement_start) &
            (pd.to_datetime(claims_df['service_date']) <= self.measurement_end)
        ]
        
        if len(outpatient_encounters) == 0:
            return False, "No outpatient encounter in measurement year"
        
        # Check continuous enrollment (if enrollment data available)
        if 'enrollment_months' in member_df.columns:
            if member_df['enrollment_months'].iloc[0] < 12:
                return False, "Not continuously enrolled"
        
        # Check exclusions
        
        # Pregnancy
        pregnancy_claims = claims_df[
            claims_df['diagnosis_code'].str.startswith(tuple(PREGNANCY_CODES), na=False)
        ]
        if len(pregnancy_claims) > 0:
            return False, "Pregnancy exclusion"
        
        # ESRD
        esrd_claims = claims_df[
            claims_df['diagnosis_code'].isin(ESRD_CODES)
        ]
        if len(esrd_claims) > 0:
            return False, "ESRD exclusion"
        
        # Cirrhosis
        cirrhosis_claims = claims_df[
            claims_df['diagnosis_code'].str.startswith(tuple(CIRRHOSIS_CODES), na=False)
        ]
        if len(cirrhosis_claims) > 0:
            return False, "Cirrhosis exclusion"
        
        # Hospice
        hospice_claims = claims_df[
            claims_df['diagnosis_code'].isin(HOSPICE_CODES)
        ]
        if len(hospice_claims) > 0:
            return False, "Hospice exclusion"
        
        # If all criteria met
        return True, "In denominator"
    
    def is_in_numerator(
        self,
        pharmacy_df: pd.DataFrame
    ) -> Tuple[bool, str, Optional[str]]:
        """
        Determine if member is in SUPD numerator.
        
        Numerator Criteria:
        1. At least one statin prescription filled in measurement year
        
        Args:
            pharmacy_df: Member's pharmacy data
            
        Returns:
            Tuple of (is_in_numerator: bool, reason: str, statin_type: str)
        """
        if pharmacy_df.empty:
            return False, "No pharmacy data", None
        
        # Check for required columns
        if 'medication_name' not in pharmacy_df.columns:
            return False, "Missing medication_name column", None
        
        # Filter to measurement year prescriptions
        measurement_year_rx = pharmacy_df[
            (pd.to_datetime(pharmacy_df['fill_date']) >= self.measurement_start) &
            (pd.to_datetime(pharmacy_df['fill_date']) <= self.measurement_end)
        ]
        
        if measurement_year_rx.empty:
            return False, "No prescriptions in measurement year", None
        
        # Check for statin prescriptions
        statin_rx = measurement_year_rx[
            measurement_year_rx['medication_name'].str.lower().str.contains(
                '|'.join(STATIN_MEDICATIONS), na=False
            )
        ]
        
        if len(statin_rx) == 0:
            return False, "No statin prescription in measurement year", None
        
        # Determine statin type/potency
        statin_name = statin_rx.iloc[0]['medication_name'].lower()
        statin_type = "Unknown potency"
        
        if any(med in statin_name for med in HIGH_POTENCY_STATINS):
            statin_type = "High potency"
        elif any(med in statin_name for med in MODERATE_POTENCY_STATINS):
            statin_type = "Moderate potency"
        elif any(med in statin_name for med in LOW_POTENCY_STATINS):
            statin_type = "Low potency"
        
        return True, f"Statin prescription found ({len(statin_rx)} fills)", statin_type
    
    def calculate_member_status(
        self,
        member_df: pd.DataFrame,
        claims_df: pd.DataFrame,
        pharmacy_df: pd.DataFrame
    ) -> Dict:
        """
        Calculate SUPD measure status for a single member.
        
        Args:
            member_df: Member demographic data
            claims_df: Member's claims data
            pharmacy_df: Member's pharmacy data
            
        Returns:
            Dictionary with member status
        """
        result = {
            'member_id': member_df['member_id'].iloc[0],
            'in_denominator': False,
            'denominator_reason': '',
            'in_numerator': False,
            'numerator_reason': '',
            'compliant': False,
            'has_gap': False,
            'statin_type': '',
            'age': 0,
            'has_ascvd': False
        }
        
        # Calculate age
        if 'birth_date' in member_df.columns:
            birth_date = pd.to_datetime(member_df['birth_date'].iloc[0])
            result['age'] = self.calculate_age(birth_date)
        
        # Check for ASCVD history (for risk stratification)
        ascvd_codes = ['I21', 'I22', 'I63', 'I64']  # MI, stroke
        ascvd_claims = claims_df[
            claims_df['diagnosis_code'].str.startswith(tuple(ascvd_codes), na=False)
        ]
        result['has_ascvd'] = len(ascvd_claims) > 0
        
        # Check denominator
        in_denom, denom_reason = self.is_in_denominator(member_df, claims_df)
        result['in_denominator'] = in_denom
        result['denominator_reason'] = denom_reason
        
        if not in_denom:
            return result
        
        # Check numerator (only if in denominator)
        in_numer, numer_reason, statin_type = self.is_in_numerator(pharmacy_df)
        result['in_numerator'] = in_numer
        result['numerator_reason'] = numer_reason
        result['statin_type'] = statin_type or ''
        
        # Compliant if in both denominator and numerator
        result['compliant'] = in_denom and in_numer
        result['has_gap'] = in_denom and not in_numer
        
        return result
    
    def calculate_population_rate(
        self,
        members_df: pd.DataFrame,
        claims_df: pd.DataFrame,
        pharmacy_df: pd.DataFrame
    ) -> Dict:
        """
        Calculate SUPD measure rate for a population.
        
        Args:
            members_df: All members' demographic data
            claims_df: All claims data
            pharmacy_df: All pharmacy data
            
        Returns:
            Dictionary with population-level metrics
        """
        results = []
        
        # Process each member
        for member_id in members_df['member_id'].unique():
            member_data = members_df[members_df['member_id'] == member_id]
            member_claims = claims_df[claims_df['member_id'] == member_id]
            member_pharmacy = pharmacy_df[pharmacy_df['member_id'] == member_id] if not pharmacy_df.empty else pd.DataFrame()
            
            member_result = self.calculate_member_status(
                member_data,
                member_claims,
                member_pharmacy
            )
            results.append(member_result)
        
        results_df = pd.DataFrame(results)
        
        # Calculate aggregate metrics
        denominator_count = results_df['in_denominator'].sum()
        numerator_count = results_df['in_numerator'].sum()
        measure_rate = (numerator_count / denominator_count * 100) if denominator_count > 0 else 0
        gap_count = results_df['has_gap'].sum()
        gap_rate = (gap_count / denominator_count * 100) if denominator_count > 0 else 0
        
        # Calculate by ASCVD status (important for statin therapy)
        with_ascvd = results_df[
            (results_df['in_denominator'] == True) & 
            (results_df['has_ascvd'] == True)
        ]
        without_ascvd = results_df[
            (results_df['in_denominator'] == True) & 
            (results_df['has_ascvd'] == False)
        ]
        
        by_ascvd_status = {
            'with_ascvd': {
                'denominator': len(with_ascvd),
                'numerator': with_ascvd['in_numerator'].sum(),
                'rate': (with_ascvd['in_numerator'].sum() / len(with_ascvd) * 100) if len(with_ascvd) > 0 else 0,
                'gaps': with_ascvd['has_gap'].sum()
            },
            'without_ascvd': {
                'denominator': len(without_ascvd),
                'numerator': without_ascvd['in_numerator'].sum(),
                'rate': (without_ascvd['in_numerator'].sum() / len(without_ascvd) * 100) if len(without_ascvd) > 0 else 0,
                'gaps': without_ascvd['has_gap'].sum()
            }
        }
        
        return {
            'total_population': len(results_df),
            'denominator_count': int(denominator_count),
            'numerator_count': int(numerator_count),
            'measure_rate': round(measure_rate, 2),
            'gap_count': int(gap_count),
            'gap_rate': round(gap_rate, 2),
            'by_ascvd_status': by_ascvd_status,
            'member_details': results_df
        }


def generate_gap_list(
    members_df: pd.DataFrame,
    claims_df: pd.DataFrame,
    pharmacy_df: pd.DataFrame,
    measurement_year: int = 2025
) -> pd.DataFrame:
    """
    Generate prioritized gap list for SUPD measure.
    
    Args:
        members_df: All members' demographic data
        claims_df: All claims data
        pharmacy_df: All pharmacy data
        measurement_year: HEDIS measurement year
        
    Returns:
        DataFrame with gap members and clinical details
    """
    supd = SUPDMeasure(measurement_year)
    results = supd.calculate_population_rate(members_df, claims_df, pharmacy_df)
    
    # Filter to gap members only
    gap_members = results['member_details'][results['member_details']['has_gap'] == True]
    
    # Add priority scoring
    gap_members = gap_members.copy()
    gap_members['priority_score'] = 100  # Base score
    
    # Higher priority if ASCVD history (clinical urgency)
    gap_members.loc[gap_members['has_ascvd'] == True, 'priority_score'] += 50
    
    # Higher priority if older
    gap_members.loc[gap_members['age'] >= 65, 'priority_score'] += 20
    
    # Sort by priority
    gap_members = gap_members.sort_values('priority_score', ascending=False)
    
    return gap_members[['member_id', 'age', 'has_ascvd', 'priority_score', 
                        'numerator_reason']]


# Example usage and testing
if __name__ == "__main__":
    print("SUPD Measure Implementation")
    print("=" * 60)
    print(f"Measure: Statin Therapy for Patients with Diabetes (SUPD)")
    print(f"Star Rating Weight: 1x")
    print(f"Annual Value: $120K-$180K (100K member plan)")
    print(f"Population: Adults 40-75 with diabetes")
    print(f"Numerator: At least one statin prescription in measurement year")
    print("=" * 60)


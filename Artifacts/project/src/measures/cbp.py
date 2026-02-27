"""
CBP - Controlling High Blood Pressure

HEDIS Measure: Controlling High Blood Pressure (CBP)
Specification: MY2023 Volume 2
Star Rating Weight: 3x (TRIPLE-WEIGHTED)
Tier: 2 (Cardiovascular Comorbidity)
Annual Value: $300K-$450K (100K member plan)

Description:
The percentage of members 18-85 years of age who had a diagnosis of hypertension (HTN)
and whose blood pressure was adequately controlled (<140/90 mmHg) during the measurement year.

Population:
- Adults 18-85 years with HTN diagnosis
- In current or prior measurement year
- Exclude: Pregnancy, end-stage renal disease, hospice, SNP

Numerator:
- Most recent BP reading in measurement year <140/90 mmHg

Denominator:
- Members with HTN diagnosis
- At least one outpatient encounter in measurement year

Author: Analytics Team
Date: October 23, 2025
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import List, Dict, Tuple, Optional


# ICD-10 Codes for Hypertension
HTN_DIAGNOSIS_CODES = [
    # Essential hypertension
    'I10',
    # Hypertensive heart disease
    'I11.0', 'I11.9',
    # Hypertensive chronic kidney disease
    'I12.0', 'I12.9',
    # Hypertensive heart and chronic kidney disease
    'I13.0', 'I13.10', 'I13.11', 'I13.2',
    # Secondary hypertension
    'I15.0', 'I15.1', 'I15.2', 'I15.8', 'I15.9',
    # Hypertensive crisis
    'I16.0', 'I16.1', 'I16.9'
]

# Exclusion Codes
PREGNANCY_CODES = ['O09', 'O10', 'O11', 'O12', 'O13', 'O14', 'O15', 'O16', 'Z33', 'Z34']
ESRD_CODES = ['N18.6', 'Z99.2']  # End-stage renal disease
HOSPICE_CODES = ['Z51.5']
SNP_CODES = []  # Would be pulled from enrollment data

# BP Control Thresholds
BP_SYSTOLIC_THRESHOLD = 140
BP_DIASTOLIC_THRESHOLD = 90


class CBPMeasure:
    """
    CBP (Controlling High Blood Pressure) Measure Calculator
    
    This class implements HEDIS CBP measure logic for identifying
    members with controlled blood pressure.
    """
    
    def __init__(self, measurement_year: int = 2025):
        """
        Initialize CBP measure calculator.
        
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
        Determine if member is in CBP denominator.
        
        Denominator Criteria:
        1. Age 18-85 as of December 31 of measurement year
        2. HTN diagnosis in current or prior year
        3. At least one outpatient encounter in measurement year
        4. Continuous enrollment in measurement year
        5. No exclusions (pregnancy, ESRD, hospice, SNP)
        
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
        
        if age < 18 or age > 85:
            return False, f"Age {age} outside range 18-85"
        
        # Check for HTN diagnosis in current or prior year
        htn_claims = claims_df[
            (claims_df['diagnosis_code'].isin(HTN_DIAGNOSIS_CODES)) &
            (pd.to_datetime(claims_df['service_date']) >= self.prior_year_start) &
            (pd.to_datetime(claims_df['service_date']) <= self.measurement_end)
        ]
        
        if len(htn_claims) == 0:
            return False, "No HTN diagnosis in measurement or prior year"
        
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
        vitals_df: pd.DataFrame
    ) -> Tuple[bool, str]:
        """
        Determine if member is in CBP numerator.
        
        Numerator Criteria:
        1. Most recent BP reading in measurement year
        2. Systolic BP <140 mmHg
        3. Diastolic BP <90 mmHg
        
        Args:
            vitals_df: Member's vitals data with BP readings
            
        Returns:
            Tuple of (is_in_numerator: bool, reason: str)
        """
        if vitals_df.empty:
            return False, "No BP readings"
        
        # Check for required columns
        required_cols = ['reading_date', 'systolic_bp', 'diastolic_bp']
        if not all(col in vitals_df.columns for col in required_cols):
            return False, "Missing required BP columns"
        
        # Filter to measurement year readings
        measurement_year_vitals = vitals_df[
            (pd.to_datetime(vitals_df['reading_date']) >= self.measurement_start) &
            (pd.to_datetime(vitals_df['reading_date']) <= self.measurement_end)
        ]
        
        if measurement_year_vitals.empty:
            return False, "No BP readings in measurement year"
        
        # Get most recent BP reading
        most_recent = measurement_year_vitals.sort_values('reading_date').iloc[-1]
        
        systolic = most_recent['systolic_bp']
        diastolic = most_recent['diastolic_bp']
        
        # Check BP control (<140/90)
        if systolic < BP_SYSTOLIC_THRESHOLD and diastolic < BP_DIASTOLIC_THRESHOLD:
            return True, f"BP controlled ({systolic}/{diastolic} < 140/90)"
        else:
            return False, f"BP not controlled ({systolic}/{diastolic} >= 140/90)"
    
    def calculate_member_status(
        self,
        member_df: pd.DataFrame,
        claims_df: pd.DataFrame,
        vitals_df: pd.DataFrame
    ) -> Dict:
        """
        Calculate CBP measure status for a single member.
        
        Args:
            member_df: Member demographic data
            claims_df: Member's claims data
            vitals_df: Member's vitals data
            
        Returns:
            Dictionary with member status:
            {
                'member_id': str,
                'in_denominator': bool,
                'denominator_reason': str,
                'in_numerator': bool,
                'numerator_reason': str,
                'compliant': bool,
                'has_gap': bool,
                'most_recent_bp': str,
                'age': int
            }
        """
        result = {
            'member_id': member_df['member_id'].iloc[0],
            'in_denominator': False,
            'denominator_reason': '',
            'in_numerator': False,
            'numerator_reason': '',
            'compliant': False,
            'has_gap': False,
            'most_recent_bp': '',
            'age': 0
        }
        
        # Calculate age
        if 'birth_date' in member_df.columns:
            birth_date = pd.to_datetime(member_df['birth_date'].iloc[0])
            result['age'] = self.calculate_age(birth_date)
        
        # Check denominator
        in_denom, denom_reason = self.is_in_denominator(member_df, claims_df)
        result['in_denominator'] = in_denom
        result['denominator_reason'] = denom_reason
        
        if not in_denom:
            return result
        
        # Check numerator (only if in denominator)
        in_numer, numer_reason = self.is_in_numerator(vitals_df)
        result['in_numerator'] = in_numer
        result['numerator_reason'] = numer_reason
        
        # Compliant if in both denominator and numerator
        result['compliant'] = in_denom and in_numer
        result['has_gap'] = in_denom and not in_numer
        
        # Get most recent BP for reporting
        if not vitals_df.empty and 'systolic_bp' in vitals_df.columns:
            measurement_year_vitals = vitals_df[
                (pd.to_datetime(vitals_df['reading_date']) >= self.measurement_start) &
                (pd.to_datetime(vitals_df['reading_date']) <= self.measurement_end)
            ]
            if not measurement_year_vitals.empty:
                most_recent = measurement_year_vitals.sort_values('reading_date').iloc[-1]
                result['most_recent_bp'] = f"{int(most_recent['systolic_bp'])}/{int(most_recent['diastolic_bp'])}"
        
        return result
    
    def calculate_population_rate(
        self,
        members_df: pd.DataFrame,
        claims_df: pd.DataFrame,
        vitals_df: pd.DataFrame
    ) -> Dict:
        """
        Calculate CBP measure rate for a population.
        
        Args:
            members_df: All members' demographic data
            claims_df: All claims data
            vitals_df: All vitals data
            
        Returns:
            Dictionary with population-level metrics:
            {
                'total_population': int,
                'denominator_count': int,
                'numerator_count': int,
                'measure_rate': float,
                'gap_count': int,
                'gap_rate': float,
                'by_age_group': dict
            }
        """
        results = []
        
        # Process each member
        for member_id in members_df['member_id'].unique():
            member_data = members_df[members_df['member_id'] == member_id]
            member_claims = claims_df[claims_df['member_id'] == member_id]
            member_vitals = vitals_df[vitals_df['member_id'] == member_id] if not vitals_df.empty else pd.DataFrame()
            
            member_result = self.calculate_member_status(
                member_data,
                member_claims,
                member_vitals
            )
            results.append(member_result)
        
        results_df = pd.DataFrame(results)
        
        # Calculate aggregate metrics
        denominator_count = results_df['in_denominator'].sum()
        numerator_count = results_df['in_numerator'].sum()
        measure_rate = (numerator_count / denominator_count * 100) if denominator_count > 0 else 0
        gap_count = results_df['has_gap'].sum()
        gap_rate = (gap_count / denominator_count * 100) if denominator_count > 0 else 0
        
        # Calculate by age group
        by_age_group = {}
        age_groups = [('18-44', 18, 44), ('45-64', 45, 64), ('65-85', 65, 85)]
        
        for group_name, min_age, max_age in age_groups:
            group_df = results_df[
                (results_df['age'] >= min_age) & 
                (results_df['age'] <= max_age) &
                (results_df['in_denominator'] == True)
            ]
            if len(group_df) > 0:
                group_rate = (group_df['in_numerator'].sum() / len(group_df) * 100)
                by_age_group[group_name] = {
                    'denominator': len(group_df),
                    'numerator': group_df['in_numerator'].sum(),
                    'rate': group_rate,
                    'gaps': group_df['has_gap'].sum()
                }
        
        return {
            'total_population': len(results_df),
            'denominator_count': int(denominator_count),
            'numerator_count': int(numerator_count),
            'measure_rate': round(measure_rate, 2),
            'gap_count': int(gap_count),
            'gap_rate': round(gap_rate, 2),
            'by_age_group': by_age_group,
            'member_details': results_df
        }


def generate_gap_list(
    members_df: pd.DataFrame,
    claims_df: pd.DataFrame,
    vitals_df: pd.DataFrame,
    measurement_year: int = 2025
) -> pd.DataFrame:
    """
    Generate prioritized gap list for CBP measure.
    
    This function identifies members in the denominator who are not in the numerator
    (have gaps) and provides relevant clinical information for outreach.
    
    Args:
        members_df: All members' demographic data
        claims_df: All claims data
        vitals_df: All vitals data
        measurement_year: HEDIS measurement year
        
    Returns:
        DataFrame with gap members and clinical details
    """
    cbp = CBPMeasure(measurement_year)
    results = cbp.calculate_population_rate(members_df, claims_df, vitals_df)
    
    # Filter to gap members only
    gap_members = results['member_details'][results['member_details']['has_gap'] == True]
    
    # Add priority scoring (simple version)
    gap_members = gap_members.copy()
    gap_members['priority_score'] = 100  # Base score
    
    # Higher priority if older (higher risk)
    gap_members.loc[gap_members['age'] >= 65, 'priority_score'] += 20
    
    # Sort by priority
    gap_members = gap_members.sort_values('priority_score', ascending=False)
    
    return gap_members[['member_id', 'age', 'most_recent_bp', 'priority_score', 
                        'numerator_reason']]


# Example usage and testing
if __name__ == "__main__":
    print("CBP Measure Implementation")
    print("=" * 60)
    print(f"Measure: Controlling High Blood Pressure (CBP)")
    print(f"Star Rating Weight: 3x (TRIPLE-WEIGHTED)")
    print(f"Annual Value: $300K-$450K (100K member plan)")
    print(f"BP Threshold: <140/90 mmHg")
    print(f"Population: Adults 18-85 with HTN")
    print("=" * 60)


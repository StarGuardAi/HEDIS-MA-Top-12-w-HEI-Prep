"""
BCS - Breast Cancer Screening

HEDIS Measure: Breast Cancer Screening (BCS)
Specification: MY2023 Volume 2
Star Rating Weight: 1x
Tier: 3 (Preventive Care)
Annual Value: $80K-$120K (100K member plan)

Description:
The percentage of women 50-74 years of age who had a mammography screening
during the measurement year or the year prior.

Population:
- Women aged 50-74 years
- Continuous enrollment for 27 months (measurement year + prior year)
- No bilateral mastectomy

Numerator:
- Mammography screening in measurement year or prior year

Denominator:
- Women aged 50-74 with continuous enrollment

Author: Analytics Team
Date: October 25, 2025
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import List, Dict, Tuple, Optional


# CPT Codes for Mammography
MAMMOGRAPHY_CPT = [
    '77065', '77066', '77067'  # Digital mammography
]

# ICD-10 Procedure Codes for Mammography
MAMMOGRAPHY_ICD_PCS = [
    'BH00', 'BH01'  # Breast imaging
]

# Exclusion Codes
BILATERAL_MASTECTOMY_CODES = [
    'Z90.13',  # Acquired absence of both breasts
    'C50'      # Malignant neoplasm of breast (history of)
]

# Bilateral mastectomy procedure codes
BILATERAL_MASTECTOMY_PROCEDURES = [
    '19303', '19304', '19305', '19306', '19307'
]


class BCSMeasure:
    """
    BCS (Breast Cancer Screening) Measure Calculator
    
    This class implements HEDIS BCS measure logic for identifying
    women who received appropriate breast cancer screening.
    """
    
    def __init__(self, measurement_year: int = 2025):
        """
        Initialize BCS measure calculator.
        
        Args:
            measurement_year: HEDIS measurement year
        """
        self.measurement_year = measurement_year
        self.measurement_start = datetime(measurement_year, 1, 1)
        self.measurement_end = datetime(measurement_year, 12, 31)
        self.prior_year_start = datetime(measurement_year - 1, 1, 1)
        self.prior_year_end = datetime(measurement_year - 1, 12, 31)
        
        # 27-month continuous enrollment period
        self.enrollment_start = datetime(measurement_year - 2, 10, 1)
        self.enrollment_end = datetime(measurement_year, 12, 31)
    
    def calculate_age(self, birth_date: datetime) -> int:
        """Calculate age as of December 31 of measurement year."""
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
        Determine if member is in BCS denominator.
        
        Denominator Criteria:
        1. Female gender
        2. Age 50-74 as of December 31 of measurement year
        3. Continuous enrollment for 27 months
        4. No bilateral mastectomy
        
        Args:
            member_df: Member demographic data
            claims_df: Member's claims data
            
        Returns:
            Tuple of (is_in_denominator: bool, reason: str)
        """
        # Check gender
        if 'gender' in member_df.columns:
            if member_df['gender'].iloc[0].upper() not in ['F', 'FEMALE']:
                return False, "Not female"
        
        # Check age
        if 'birth_date' not in member_df.columns:
            return False, "Missing birth_date"
        
        birth_date = pd.to_datetime(member_df['birth_date'].iloc[0])
        age = self.calculate_age(birth_date)
        
        if age < 50 or age > 74:
            return False, f"Age {age} outside range 50-74"
        
        # Check continuous enrollment (27 months)
        if 'enrollment_months' in member_df.columns:
            if member_df['enrollment_months'].iloc[0] < 27:
                return False, "Not continuously enrolled for 27 months"
        
        # Check for bilateral mastectomy exclusion
        mastectomy_claims = claims_df[
            claims_df['diagnosis_code'].str.startswith(tuple(BILATERAL_MASTECTOMY_CODES), na=False) |
            claims_df['procedure_code'].isin(BILATERAL_MASTECTOMY_PROCEDURES)
        ]
        if len(mastectomy_claims) > 0:
            return False, "Bilateral mastectomy exclusion"
        
        return True, "In denominator"
    
    def is_in_numerator(
        self,
        claims_df: pd.DataFrame
    ) -> Tuple[bool, str]:
        """
        Determine if member is in BCS numerator.
        
        Numerator Criteria:
        1. Mammography screening in measurement year OR prior year
        
        Args:
            claims_df: Member's claims data
            
        Returns:
            Tuple of (is_in_numerator: bool, reason: str)
        """
        if claims_df.empty:
            return False, "No claims data"
        
        # Check for required columns
        if 'procedure_code' not in claims_df.columns and 'diagnosis_code' not in claims_df.columns:
            return False, "Missing procedure/diagnosis code columns"
        
        # Filter to screening period (measurement year + prior year)
        screening_period_claims = claims_df[
            (pd.to_datetime(claims_df['service_date']) >= self.prior_year_start) &
            (pd.to_datetime(claims_df['service_date']) <= self.measurement_end)
        ]
        
        if screening_period_claims.empty:
            return False, "No claims in screening period"
        
        # Check for mammography codes
        mammography_claims = pd.DataFrame()
        
        if 'procedure_code' in screening_period_claims.columns:
            mammography_claims = screening_period_claims[
                screening_period_claims['procedure_code'].isin(MAMMOGRAPHY_CPT)
            ]
        
        if len(mammography_claims) == 0 and 'diagnosis_code' in screening_period_claims.columns:
            mammography_claims = screening_period_claims[
                screening_period_claims['diagnosis_code'].str.startswith(tuple(MAMMOGRAPHY_ICD_PCS), na=False)
            ]
        
        if len(mammography_claims) > 0:
            most_recent = mammography_claims['service_date'].max()
            return True, f"Mammography screening found (most recent: {most_recent})"
        
        return False, "No mammography screening in measurement or prior year"
    
    def calculate_member_status(
        self,
        member_df: pd.DataFrame,
        claims_df: pd.DataFrame
    ) -> Dict:
        """
        Calculate BCS measure status for a single member.
        
        Args:
            member_df: Member demographic data
            claims_df: Member's claims data
            
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
            'age': 0,
            'most_recent_screening': None
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
        in_numer, numer_reason = self.is_in_numerator(claims_df)
        result['in_numerator'] = in_numer
        result['numerator_reason'] = numer_reason
        
        # Extract most recent screening date if found
        if in_numer and 'procedure_code' in claims_df.columns:
            mammography_claims = claims_df[
                claims_df['procedure_code'].isin(MAMMOGRAPHY_CPT)
            ]
            if not mammography_claims.empty:
                result['most_recent_screening'] = mammography_claims['service_date'].max()
        
        # Compliant if in both denominator and numerator
        result['compliant'] = in_denom and in_numer
        result['has_gap'] = in_denom and not in_numer
        
        return result
    
    def calculate_population_rate(
        self,
        members_df: pd.DataFrame,
        claims_df: pd.DataFrame
    ) -> Dict:
        """
        Calculate BCS measure rate for a population.
        
        Args:
            members_df: All members' demographic data
            claims_df: All claims data
            
        Returns:
            Dictionary with population-level metrics
        """
        results = []
        
        # Process each member
        for member_id in members_df['member_id'].unique():
            member_data = members_df[members_df['member_id'] == member_id]
            member_claims = claims_df[claims_df['member_id'] == member_id]
            
            member_result = self.calculate_member_status(
                member_data,
                member_claims
            )
            results.append(member_result)
        
        results_df = pd.DataFrame(results)
        
        # Calculate aggregate metrics
        denominator_count = results_df['in_denominator'].sum()
        numerator_count = results_df['in_numerator'].sum()
        measure_rate = (numerator_count / denominator_count * 100) if denominator_count > 0 else 0
        gap_count = results_df['has_gap'].sum()
        gap_rate = (gap_count / denominator_count * 100) if denominator_count > 0 else 0
        
        return {
            'total_population': len(results_df),
            'denominator_count': int(denominator_count),
            'numerator_count': int(numerator_count),
            'measure_rate': round(measure_rate, 2),
            'gap_count': int(gap_count),
            'gap_rate': round(gap_rate, 2),
            'member_details': results_df
        }


def generate_gap_list(
    members_df: pd.DataFrame,
    claims_df: pd.DataFrame,
    measurement_year: int = 2025
) -> pd.DataFrame:
    """
    Generate prioritized gap list for BCS measure.
    
    Args:
        members_df: All members' demographic data
        claims_df: All claims data
        measurement_year: HEDIS measurement year
        
    Returns:
        DataFrame with gap members and clinical details
    """
    bcs = BCSMeasure(measurement_year)
    results = bcs.calculate_population_rate(members_df, claims_df)
    
    # Filter to gap members only
    gap_members = results['member_details'][results['member_details']['has_gap'] == True].copy()
    
    # Add priority scoring
    gap_members['priority_score'] = 100  # Base score
    
    # Higher priority if older (higher cancer risk)
    gap_members.loc[gap_members['age'] >= 65, 'priority_score'] += 30
    gap_members.loc[gap_members['age'] >= 70, 'priority_score'] += 20
    
    # Sort by priority
    gap_members = gap_members.sort_values('priority_score', ascending=False)
    
    return gap_members[['member_id', 'age', 'priority_score', 'numerator_reason']]


if __name__ == "__main__":
    print("BCS Measure Implementation (Tier 3 - Preventive Care)")
    print("=" * 60)
    print(f"Measure: Breast Cancer Screening (BCS)")
    print(f"Star Rating Weight: 1x")
    print(f"Annual Value: $80K-$120K (100K member plan)")
    print(f"Population: Women 50-74 years")
    print(f"Numerator: Mammography in measurement or prior year")
    print("=" * 60)


"""
COL - Colorectal Cancer Screening

HEDIS Measure: Colorectal Cancer Screening (COL)
Specification: MY2023 Volume 2
Star Rating Weight: 1x
Tier: 3 (Preventive Care)
Annual Value: $100K-$150K (100K member plan)

Description:
The percentage of adults 50-75 years of age who had appropriate screening
for colorectal cancer.

Screening Modalities (with look-back periods):
- Colonoscopy (10 years)
- Flexible sigmoidoscopy (5 years)
- CT colonography (5 years)
- FIT test (annual)
- FIT-DNA test (3 years)

Population:
- Adults aged 50-75 years
- Continuous enrollment
- No total colectomy
- No colorectal cancer history

Author: Analytics Team
Date: October 25, 2025
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import List, Dict, Tuple, Optional


# Colonoscopy CPT Codes (10-year look-back)
COLONOSCOPY_CPT = [
    '44388', '44389', '44390', '44391', '44392', '44393', '44394', '44397', '44401', '44402', '44403', '44404', '44405', '44406', '44407', '44408',
    '45355', '45378', '45379', '45380', '45381', '45382', '45383', '45384', '45385', '45386', '45387', '45388', '45389', '45390', '45391', '45392', '45393', '45398',
    'G0105', 'G0121'
]

# Flexible Sigmoidoscopy CPT Codes (5-year look-back)
SIGMOIDOSCOPY_CPT = [
    '45330', '45331', '45332', '45333', '45334', '45335', '45337', '45338', '45339', '45340', '45341', '45342', '45345', '45346', '45347', '45349', '45350',
    'G0104'
]

# CT Colonography CPT Codes (5-year look-back)
CT_COLONOGRAPHY_CPT = [
    '74263'
]

# FIT Test CPT Codes (annual - 1 year look-back)
FIT_TEST_CPT = [
    '82270', '82274', 'G0328'
]

# FIT-DNA Test CPT Codes (3-year look-back)
FIT_DNA_CPT = [
    '81528'
]

# Exclusion Codes - Total Colectomy
TOTAL_COLECTOMY_CPT = [
    '44150', '44151', '44152', '44153', '44155', '44156', '44157', '44158', '44210', '44211', '44212'
]

TOTAL_COLECTOMY_ICD = [
    'Z90.49'  # Acquired absence of other parts of digestive tract
]

# Exclusion Codes - Colorectal Cancer
COLORECTAL_CANCER_ICD = [
    'C18', 'C19', 'C20', 'C21'  # Malignant neoplasm of colon, rectum, anus
]

# Hospice
HOSPICE_CODES = ['Z51.5']


class COLMeasure:
    """
    COL (Colorectal Cancer Screening) Measure Calculator
    
    This class implements HEDIS COL measure logic with multiple screening
    modalities and different look-back periods.
    """
    
    def __init__(self, measurement_year: int = 2025):
        """
        Initialize COL measure calculator.
        
        Args:
            measurement_year: HEDIS measurement year
        """
        self.measurement_year = measurement_year
        self.measurement_end = datetime(measurement_year, 12, 31)
        
        # Look-back periods for different screening types
        self.colonoscopy_lookback_start = datetime(measurement_year - 10, 1, 1)
        self.sigmoidoscopy_lookback_start = datetime(measurement_year - 5, 1, 1)
        self.ct_colonography_lookback_start = datetime(measurement_year - 5, 1, 1)
        self.fit_test_lookback_start = datetime(measurement_year, 1, 1)
        self.fit_dna_lookback_start = datetime(measurement_year - 3, 1, 1)
    
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
        Determine if member is in COL denominator.
        
        Denominator Criteria:
        1. Age 50-75 as of December 31 of measurement year
        2. Continuous enrollment in measurement year
        3. No total colectomy
        4. No colorectal cancer history
        5. No hospice
        
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
        
        if age < 50 or age > 75:
            return False, f"Age {age} outside range 50-75"
        
        # Check continuous enrollment
        if 'enrollment_months' in member_df.columns:
            if member_df['enrollment_months'].iloc[0] < 12:
                return False, "Not continuously enrolled"
        
        # Check for total colectomy exclusion
        colectomy_claims = claims_df[
            claims_df['procedure_code'].isin(TOTAL_COLECTOMY_CPT) if 'procedure_code' in claims_df.columns else False
        ]
        if len(colectomy_claims) > 0:
            return False, "Total colectomy exclusion"
        
        colectomy_dx = claims_df[
            claims_df['diagnosis_code'].isin(TOTAL_COLECTOMY_ICD)
        ]
        if len(colectomy_dx) > 0:
            return False, "Total colectomy exclusion"
        
        # Check for colorectal cancer history
        cancer_claims = claims_df[
            claims_df['diagnosis_code'].str.startswith(tuple(COLORECTAL_CANCER_ICD), na=False)
        ]
        if len(cancer_claims) > 0:
            return False, "Colorectal cancer history exclusion"
        
        # Check for hospice
        hospice_claims = claims_df[
            claims_df['diagnosis_code'].isin(HOSPICE_CODES)
        ]
        if len(hospice_claims) > 0:
            return False, "Hospice exclusion"
        
        return True, "In denominator"
    
    def is_in_numerator(
        self,
        claims_df: pd.DataFrame
    ) -> Tuple[bool, str, Optional[str]]:
        """
        Determine if member is in COL numerator.
        
        Numerator Criteria (ANY of the following):
        1. Colonoscopy in last 10 years
        2. Flexible sigmoidoscopy in last 5 years
        3. CT colonography in last 5 years
        4. FIT test in measurement year
        5. FIT-DNA test in last 3 years
        
        Args:
            claims_df: Member's claims data
            
        Returns:
            Tuple of (is_in_numerator: bool, reason: str, screening_type: str)
        """
        if claims_df.empty or 'procedure_code' not in claims_df.columns:
            return False, "No claims data with procedure codes", None
        
        # Check each screening modality (in order of clinical preference)
        
        # 1. Colonoscopy (10-year look-back)
        colonoscopy_claims = claims_df[
            (claims_df['procedure_code'].isin(COLONOSCOPY_CPT)) &
            (pd.to_datetime(claims_df['service_date']) >= self.colonoscopy_lookback_start) &
            (pd.to_datetime(claims_df['service_date']) <= self.measurement_end)
        ]
        if len(colonoscopy_claims) > 0:
            most_recent = colonoscopy_claims['service_date'].max()
            return True, f"Colonoscopy on {most_recent} (10-year screening)", "Colonoscopy"
        
        # 2. Flexible Sigmoidoscopy (5-year look-back)
        sigmoidoscopy_claims = claims_df[
            (claims_df['procedure_code'].isin(SIGMOIDOSCOPY_CPT)) &
            (pd.to_datetime(claims_df['service_date']) >= self.sigmoidoscopy_lookback_start) &
            (pd.to_datetime(claims_df['service_date']) <= self.measurement_end)
        ]
        if len(sigmoidoscopy_claims) > 0:
            most_recent = sigmoidoscopy_claims['service_date'].max()
            return True, f"Flexible sigmoidoscopy on {most_recent} (5-year screening)", "Sigmoidoscopy"
        
        # 3. CT Colonography (5-year look-back)
        ct_claims = claims_df[
            (claims_df['procedure_code'].isin(CT_COLONOGRAPHY_CPT)) &
            (pd.to_datetime(claims_df['service_date']) >= self.ct_colonography_lookback_start) &
            (pd.to_datetime(claims_df['service_date']) <= self.measurement_end)
        ]
        if len(ct_claims) > 0:
            most_recent = ct_claims['service_date'].max()
            return True, f"CT colonography on {most_recent} (5-year screening)", "CT Colonography"
        
        # 4. FIT Test (annual)
        fit_claims = claims_df[
            (claims_df['procedure_code'].isin(FIT_TEST_CPT)) &
            (pd.to_datetime(claims_df['service_date']) >= self.fit_test_lookback_start) &
            (pd.to_datetime(claims_df['service_date']) <= self.measurement_end)
        ]
        if len(fit_claims) > 0:
            most_recent = fit_claims['service_date'].max()
            return True, f"FIT test on {most_recent} (annual screening)", "FIT Test"
        
        # 5. FIT-DNA Test (3-year look-back)
        fit_dna_claims = claims_df[
            (claims_df['procedure_code'].isin(FIT_DNA_CPT)) &
            (pd.to_datetime(claims_df['service_date']) >= self.fit_dna_lookback_start) &
            (pd.to_datetime(claims_df['service_date']) <= self.measurement_end)
        ]
        if len(fit_dna_claims) > 0:
            most_recent = fit_dna_claims['service_date'].max()
            return True, f"FIT-DNA test on {most_recent} (3-year screening)", "FIT-DNA Test"
        
        return False, "No colorectal cancer screening in appropriate timeframe", None
    
    def calculate_member_status(
        self,
        member_df: pd.DataFrame,
        claims_df: pd.DataFrame
    ) -> Dict:
        """
        Calculate COL measure status for a single member.
        
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
            'screening_type': None,
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
        in_numer, numer_reason, screening_type = self.is_in_numerator(claims_df)
        result['in_numerator'] = in_numer
        result['numerator_reason'] = numer_reason
        result['screening_type'] = screening_type
        
        # Extract most recent screening date
        if in_numer and 'on' in numer_reason:
            try:
                date_str = numer_reason.split('on ')[1].split(' (')[0]
                result['most_recent_screening'] = date_str
            except:
                pass
        
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
        Calculate COL measure rate for a population.
        
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
        
        # Calculate by screening type
        compliant_members = results_df[results_df['compliant'] == True]
        by_screening_type = {}
        if len(compliant_members) > 0:
            screening_counts = compliant_members['screening_type'].value_counts()
            for screening_type, count in screening_counts.items():
                if screening_type:
                    by_screening_type[screening_type] = {
                        'count': int(count),
                        'percentage': round((count / len(compliant_members) * 100), 2)
                    }
        
        return {
            'total_population': len(results_df),
            'denominator_count': int(denominator_count),
            'numerator_count': int(numerator_count),
            'measure_rate': round(measure_rate, 2),
            'gap_count': int(gap_count),
            'gap_rate': round(gap_rate, 2),
            'by_screening_type': by_screening_type,
            'member_details': results_df
        }


def generate_gap_list(
    members_df: pd.DataFrame,
    claims_df: pd.DataFrame,
    measurement_year: int = 2025
) -> pd.DataFrame:
    """
    Generate prioritized gap list for COL measure.
    
    Args:
        members_df: All members' demographic data
        claims_df: All claims data
        measurement_year: HEDIS measurement year
        
    Returns:
        DataFrame with gap members and clinical details
    """
    col = COLMeasure(measurement_year)
    results = col.calculate_population_rate(members_df, claims_df)
    
    # Filter to gap members only
    gap_members = results['member_details'][results['member_details']['has_gap'] == True].copy()
    
    # Add priority scoring
    gap_members['priority_score'] = 100  # Base score
    
    # Higher priority if older (approaching age limit of 75)
    gap_members.loc[gap_members['age'] >= 70, 'priority_score'] += 40
    gap_members.loc[(gap_members['age'] >= 65) & (gap_members['age'] < 70), 'priority_score'] += 25
    gap_members.loc[(gap_members['age'] >= 60) & (gap_members['age'] < 65), 'priority_score'] += 15
    
    # Sort by priority
    gap_members = gap_members.sort_values('priority_score', ascending=False)
    
    return gap_members[['member_id', 'age', 'priority_score', 'numerator_reason']]


if __name__ == "__main__":
    print("COL Measure Implementation (Tier 3 - Preventive Care)")
    print("=" * 60)
    print(f"Measure: Colorectal Cancer Screening (COL)")
    print(f"Star Rating Weight: 1x")
    print(f"Annual Value: $100K-$150K (100K member plan)")
    print(f"Population: Adults 50-75 years")
    print(f"Screening Options:")
    print(f"  - Colonoscopy (10-year interval)")
    print(f"  - Flexible sigmoidoscopy (5-year interval)")
    print(f"  - CT colonography (5-year interval)")
    print(f"  - FIT test (annual)")
    print(f"  - FIT-DNA test (3-year interval)")
    print("=" * 60)


"""
FLU - Influenza Immunization

HEDIS Measure: Influenza Immunization (FLU)
Specification: MY2023 Volume 2
Star Rating Weight: 1x
Tier: 3 (Preventive Care)
Annual Value: $80K-$120K (100K member plan)

Description:
The percentage of adults 65 years of age and older who received an influenza
immunization during the flu season (October 1 - March 31).

Population:
- Adults aged 65+ years
- Continuous enrollment during flu season
- No egg allergy (anaphylaxis contraindication)

Numerator:
- Influenza vaccination between October 1 and March 31

Denominator:
- Adults 65+ continuously enrolled during flu season

Author: Analytics Team
Date: October 25, 2025
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import List, Dict, Tuple, Optional


# CPT Codes for Influenza Vaccination
FLU_VACCINE_CPT = [
    '90630',  # Influenza virus vaccine, quadrivalent
    '90653',  # Influenza vaccine, inactivated (IIV), subunit
    '90654',  # Influenza virus vaccine, trivalent (IIV3), split virus
    '90655',  # Influenza virus vaccine, trivalent (IIV3), split virus, preservative free
    '90656',  # Influenza virus vaccine, trivalent (IIV3), split virus, preservative free, 0.25 mL
    '90662',  # Influenza virus vaccine, split virus, preservative free
    '90672',  # Influenza virus vaccine, quadrivalent (ccIIV4), derived from cell cultures
    '90673',  # Influenza virus vaccine, trivalent (RIV3), derived from recombinant DNA
    '90674',  # Influenza virus vaccine, quadrivalent (ccIIV4), derived from cell cultures, preservative free
    '90685',  # Influenza virus vaccine, quadrivalent (IIV4), split virus, preservative free
    '90686',  # Influenza virus vaccine, quadrivalent (IIV4), split virus, preservative free, 0.25 mL
    '90687',  # Influenza virus vaccine, quadrivalent (IIV4), split virus, 0.5 mL
    '90688',  # Influenza virus vaccine, quadrivalent (IIV4), split virus, 0.5 mL, preservative free
    'G0008',  # Administration of influenza virus vaccine
    'Q2034',  # Influenza virus vaccine, split virus
    'Q2035',  # Influenza virus vaccine, split virus, when administered to individuals 3 years of age and older
    'Q2036',  # Influenza virus vaccine, split virus, when administered to individuals 3 years of age and older
    'Q2037',  # Influenza virus vaccine, split virus, when administered to individuals 3 years of age and older
    'Q2038',  # Influenza virus vaccine, split virus, when administered to individuals 3 years of age and older
    'Q2039'   # Influenza virus vaccine, not otherwise specified
]

# CVX Codes (vaccine administered codes)
FLU_VACCINE_CVX = [
    '135', '140', '141', '144', '150', '155', '158', '161', 
    '166', '168', '171', '185', '186', '197', '205'
]

# Exclusion Codes
EGG_ALLERGY_CODES = ['Z91.012']  # Allergy to eggs (anaphylaxis contraindication for some flu vaccines)
HOSPICE_CODES = ['Z51.5']


class FLUMeasure:
    """
    FLU (Influenza Immunization) Measure Calculator
    
    This class implements HEDIS FLU measure logic for identifying
    adults 65+ who received influenza vaccination during flu season.
    """
    
    def __init__(self, measurement_year: int = 2025):
        """
        Initialize FLU measure calculator.
        
        Args:
            measurement_year: HEDIS measurement year
        """
        self.measurement_year = measurement_year
        
        # Flu season: October 1 (prior year) to March 31 (measurement year)
        self.flu_season_start = datetime(measurement_year - 1, 10, 1)
        self.flu_season_end = datetime(measurement_year, 3, 31)
        
        # HEDIS year-end for age calculation
        self.measurement_end = datetime(measurement_year, 12, 31)
    
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
        Determine if member is in FLU denominator.
        
        Denominator Criteria:
        1. Age 65+ as of December 31 of measurement year
        2. Continuous enrollment during flu season (Oct 1 - Mar 31)
        3. No anaphylactic egg allergy (contraindication)
        4. No hospice care
        
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
        
        if age < 65:
            return False, f"Age {age} below 65"
        
        # Check continuous enrollment during flu season (6 months)
        if 'enrollment_months' in member_df.columns:
            # For flu season, need at least 6 months enrollment
            if member_df['enrollment_months'].iloc[0] < 6:
                return False, "Not enrolled during flu season"
        
        # Check for egg allergy exclusion
        egg_allergy_claims = claims_df[
            claims_df['diagnosis_code'].isin(EGG_ALLERGY_CODES)
        ]
        if len(egg_allergy_claims) > 0:
            return False, "Egg allergy (anaphylaxis) contraindication"
        
        # Check for hospice exclusion
        hospice_claims = claims_df[
            claims_df['diagnosis_code'].isin(HOSPICE_CODES)
        ]
        if len(hospice_claims) > 0:
            return False, "Hospice exclusion"
        
        return True, "In denominator"
    
    def is_in_numerator(
        self,
        claims_df: pd.DataFrame,
        pharmacy_df: Optional[pd.DataFrame] = None
    ) -> Tuple[bool, str]:
        """
        Determine if member is in FLU numerator.
        
        Numerator Criteria:
        1. Influenza vaccination between October 1 and March 31
        2. Can be administered in physician office (claims) or pharmacy (pharmacy data)
        
        Args:
            claims_df: Member's claims data
            pharmacy_df: Member's pharmacy data (optional)
            
        Returns:
            Tuple of (is_in_numerator: bool, reason: str)
        """
        vaccination_found = False
        vaccination_date = None
        vaccination_source = None
        
        # Check claims data for flu vaccine administration
        if not claims_df.empty and 'procedure_code' in claims_df.columns:
            flu_season_claims = claims_df[
                (pd.to_datetime(claims_df['service_date']) >= self.flu_season_start) &
                (pd.to_datetime(claims_df['service_date']) <= self.flu_season_end)
            ]
            
            vaccine_claims = flu_season_claims[
                flu_season_claims['procedure_code'].isin(FLU_VACCINE_CPT)
            ]
            
            if len(vaccine_claims) > 0:
                vaccination_found = True
                vaccination_date = vaccine_claims['service_date'].max()
                vaccination_source = "physician office"
        
        # Check pharmacy data for flu vaccine (retail/pharmacy administration)
        if not vaccination_found and pharmacy_df is not None and not pharmacy_df.empty:
            if 'medication_name' in pharmacy_df.columns or 'ndc_code' in pharmacy_df.columns:
                flu_season_pharmacy = pharmacy_df[
                    (pd.to_datetime(pharmacy_df['fill_date']) >= self.flu_season_start) &
                    (pd.to_datetime(pharmacy_df['fill_date']) <= self.flu_season_end)
                ]
                
                # Check for flu vaccine in medication name
                if 'medication_name' in flu_season_pharmacy.columns:
                    vaccine_fills = flu_season_pharmacy[
                        flu_season_pharmacy['medication_name'].str.lower().str.contains(
                            'influenza|flu vaccine|fluzone|flublok|fluad|flucelvax',
                            na=False,
                            regex=True
                        )
                    ]
                    
                    if len(vaccine_fills) > 0:
                        vaccination_found = True
                        vaccination_date = vaccine_fills['fill_date'].max()
                        vaccination_source = "retail pharmacy"
        
        if vaccination_found:
            return True, f"Flu vaccination on {vaccination_date} ({vaccination_source})"
        
        return False, "No flu vaccination during flu season (Oct 1 - Mar 31)"
    
    def calculate_member_status(
        self,
        member_df: pd.DataFrame,
        claims_df: pd.DataFrame,
        pharmacy_df: Optional[pd.DataFrame] = None
    ) -> Dict:
        """
        Calculate FLU measure status for a single member.
        
        Args:
            member_df: Member demographic data
            claims_df: Member's claims data
            pharmacy_df: Member's pharmacy data (optional)
            
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
            'vaccination_date': None,
            'vaccination_source': None
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
        in_numer, numer_reason = self.is_in_numerator(claims_df, pharmacy_df)
        result['in_numerator'] = in_numer
        result['numerator_reason'] = numer_reason
        
        # Extract vaccination details if found
        if in_numer and 'on' in numer_reason:
            try:
                # Parse vaccination date from reason string
                parts = numer_reason.split('on ')[1].split(' (')
                result['vaccination_date'] = parts[0]
                result['vaccination_source'] = parts[1].rstrip(')')
            except:
                pass
        
        # Compliant if in both denominator and numerator
        result['compliant'] = in_denom and in_numer
        result['has_gap'] = in_denom and not in_numer
        
        return result
    
    def calculate_population_rate(
        self,
        members_df: pd.DataFrame,
        claims_df: pd.DataFrame,
        pharmacy_df: Optional[pd.DataFrame] = None
    ) -> Dict:
        """
        Calculate FLU measure rate for a population.
        
        Args:
            members_df: All members' demographic data
            claims_df: All claims data
            pharmacy_df: All pharmacy data (optional)
            
        Returns:
            Dictionary with population-level metrics
        """
        results = []
        
        # Process each member
        for member_id in members_df['member_id'].unique():
            member_data = members_df[members_df['member_id'] == member_id]
            member_claims = claims_df[claims_df['member_id'] == member_id]
            member_pharmacy = pharmacy_df[pharmacy_df['member_id'] == member_id] if pharmacy_df is not None and not pharmacy_df.empty else None
            
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
        
        # Calculate by age group (clinical insight)
        age_groups = {
            '65-74': results_df[(results_df['in_denominator'] == True) & (results_df['age'] >= 65) & (results_df['age'] <= 74)],
            '75-84': results_df[(results_df['in_denominator'] == True) & (results_df['age'] >= 75) & (results_df['age'] <= 84)],
            '85+': results_df[(results_df['in_denominator'] == True) & (results_df['age'] >= 85)]
        }
        
        by_age_group = {}
        for age_group, group_df in age_groups.items():
            if len(group_df) > 0:
                by_age_group[age_group] = {
                    'denominator': len(group_df),
                    'numerator': group_df['in_numerator'].sum(),
                    'rate': (group_df['in_numerator'].sum() / len(group_df) * 100),
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
    pharmacy_df: Optional[pd.DataFrame] = None,
    measurement_year: int = 2025
) -> pd.DataFrame:
    """
    Generate prioritized gap list for FLU measure.
    
    Args:
        members_df: All members' demographic data
        claims_df: All claims data
        pharmacy_df: All pharmacy data (optional)
        measurement_year: HEDIS measurement year
        
    Returns:
        DataFrame with gap members and clinical details
    """
    flu = FLUMeasure(measurement_year)
    results = flu.calculate_population_rate(members_df, claims_df, pharmacy_df)
    
    # Filter to gap members only
    gap_members = results['member_details'][results['member_details']['has_gap'] == True].copy()
    
    # Add priority scoring
    gap_members['priority_score'] = 100  # Base score
    
    # HIGHEST priority if 85+ (highest flu complication risk)
    gap_members.loc[gap_members['age'] >= 85, 'priority_score'] += 50
    
    # Higher priority if 75-84
    gap_members.loc[(gap_members['age'] >= 75) & (gap_members['age'] < 85), 'priority_score'] += 30
    
    # Standard priority if 65-74
    gap_members.loc[(gap_members['age'] >= 65) & (gap_members['age'] < 75), 'priority_score'] += 15
    
    # Sort by priority
    gap_members = gap_members.sort_values('priority_score', ascending=False)
    
    return gap_members[['member_id', 'age', 'priority_score', 'numerator_reason']]


if __name__ == "__main__":
    print("FLU Measure Implementation (Tier 3 - Preventive Care)")
    print("=" * 60)
    print(f"Measure: Influenza Immunization (FLU)")
    print(f"Star Rating Weight: 1x")
    print(f"Annual Value: $80K-$120K (100K member plan)")
    print(f"Population: Adults 65+ years")
    print(f"Flu Season: October 1 - March 31")
    print(f"Numerator: Flu vaccination during flu season")
    print(f"Gap Closure: EASY (single annual vaccine, multiple venues)")
    print("=" * 60)


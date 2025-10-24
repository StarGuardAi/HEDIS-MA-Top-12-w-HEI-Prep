"""
PDC-STA - Medication Adherence for Cholesterol (Statins)

HEDIS Measure: Proportion of Days Covered - Statins (PDC-STA)
Specification: MY2023 Volume 2
Star Rating Weight: 1x
Tier: 2 (Cardiovascular Comorbidity)
Annual Value: $100K-$150K (100K member plan)

Description:
The percentage of members 18+ years who received at least two prescriptions for
statin medications and who had a PDC of at least 80% during the measurement year.

Population:
- Adults 18+ years with ASCVD or diabetes
- At least 2 prescription fills of statins
- Continuous enrollment in measurement year

Numerator:
- PDC ≥ 80% for statin medications

Denominator:
- Members with 2+ fills of statins

Author: Analytics Team
Date: October 23, 2025
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import List, Dict, Tuple, Optional


# Statin Medications
STATINS = [
    'atorvastatin', 'simvastatin', 'rosuvastatin', 'pravastatin',
    'lovastatin', 'fluvastatin', 'pitavastatin'
]

# Statin Potency Classification (for risk stratification)
HIGH_POTENCY_STATINS = ['atorvastatin 40', 'atorvastatin 80', 'rosuvastatin 20', 'rosuvastatin 40']
MODERATE_POTENCY_STATINS = ['atorvastatin 10', 'atorvastatin 20', 'simvastatin 20', 'simvastatin 40',
                            'pravastatin 40', 'pravastatin 80', 'lovastatin 40', 'fluvastatin 80']
LOW_POTENCY_STATINS = ['simvastatin 10', 'pravastatin 10', 'pravastatin 20', 'lovastatin 20',
                       'fluvastatin 20', 'fluvastatin 40']

# Exclusion Codes
ESRD_CODES = ['N18.6', 'Z99.2']  # End-stage renal disease
HOSPICE_CODES = ['Z51.5']
CIRRHOSIS_CODES = ['K70.3', 'K71.7', 'K74']  # Liver cirrhosis

# PDC Threshold (HEDIS standard)
PDC_THRESHOLD = 0.80  # 80%


class PDCSTAMeasure:
    """
    PDC-STA (Medication Adherence - Statins) Measure Calculator
    
    This class implements HEDIS PDC-STA measure logic using the
    Proportion of Days Covered (PDC) methodology.
    """
    
    def __init__(self, measurement_year: int = 2025):
        """
        Initialize PDC-STA measure calculator.
        
        Args:
            measurement_year: HEDIS measurement year
        """
        self.measurement_year = measurement_year
        self.measurement_start = datetime(measurement_year, 1, 1)
        self.measurement_end = datetime(measurement_year, 12, 31)
        self.measurement_days = (self.measurement_end - self.measurement_start).days + 1
    
    def calculate_age(self, birth_date: datetime) -> int:
        """
        Calculate age as of December 31 of measurement year.
        
        Args:
            birth_date: Member's date of birth
            
        Returns:
            Age in years
        """
        return self.measurement_year - birth_date.year - (
            (self.measurement_end.month, self.measurement_end.day) <
            (birth_date.month, birth_date.day)
        )
    
    def calculate_pdc(
        self,
        pharmacy_df: pd.DataFrame
    ) -> Tuple[float, int, int]:
        """
        Calculate Proportion of Days Covered (PDC) for statins.
        
        PDC = (Number of days covered / Total days in period) × 100
        
        Args:
            pharmacy_df: Member's pharmacy data for statins
            
        Returns:
            Tuple of (pdc_rate: float, days_covered: int, total_days: int)
        """
        if pharmacy_df.empty:
            return 0.0, 0, self.measurement_days
        
        # Create a set of covered days
        covered_days = set()
        
        # Process each fill
        for _, fill in pharmacy_df.iterrows():
            fill_date = pd.to_datetime(fill['fill_date'])
            days_supply = fill.get('days_supply', 30)  # Default to 30 if missing
            
            # Calculate coverage period for this fill
            coverage_start = max(fill_date, self.measurement_start)
            coverage_end = min(fill_date + timedelta(days=days_supply), self.measurement_end)
            
            # Add covered days
            current_date = coverage_start
            while current_date <= coverage_end:
                covered_days.add(current_date.date())
                current_date += timedelta(days=1)
        
        # Calculate PDC
        days_covered = len(covered_days)
        pdc_rate = (days_covered / self.measurement_days) * 100
        
        return pdc_rate, days_covered, self.measurement_days
    
    def is_in_denominator(
        self,
        member_df: pd.DataFrame,
        claims_df: pd.DataFrame,
        pharmacy_df: pd.DataFrame
    ) -> Tuple[bool, str]:
        """
        Determine if member is in PDC-STA denominator.
        
        Denominator Criteria:
        1. Age 18+ as of December 31 of measurement year
        2. At least 2 prescription fills of statins in measurement year
        3. Continuous enrollment in measurement year
        4. No exclusions (ESRD, hospice, cirrhosis)
        
        Args:
            member_df: Member demographic data
            claims_df: Member's claims data
            pharmacy_df: Member's pharmacy data
            
        Returns:
            Tuple of (is_in_denominator: bool, reason: str)
        """
        # Check age
        if 'birth_date' not in member_df.columns:
            return False, "Missing birth_date"
        
        birth_date = pd.to_datetime(member_df['birth_date'].iloc[0])
        age = self.calculate_age(birth_date)
        
        if age < 18:
            return False, f"Age {age} below 18"
        
        # Check for at least 2 statin fills
        if pharmacy_df.empty or 'medication_name' not in pharmacy_df.columns:
            return False, "No pharmacy data"
        
        statin_fills = pharmacy_df[
            pharmacy_df['medication_name'].str.lower().str.contains(
                '|'.join(STATINS), na=False
            ) &
            (pd.to_datetime(pharmacy_df['fill_date']) >= self.measurement_start) &
            (pd.to_datetime(pharmacy_df['fill_date']) <= self.measurement_end)
        ]
        
        if len(statin_fills) < 2:
            return False, f"Only {len(statin_fills)} fill(s) (need 2+)"
        
        # Check continuous enrollment
        if 'enrollment_months' in member_df.columns:
            if member_df['enrollment_months'].iloc[0] < 12:
                return False, "Not continuously enrolled"
        
        # Check exclusions
        
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
        
        # Cirrhosis
        cirrhosis_claims = claims_df[
            claims_df['diagnosis_code'].str.startswith(tuple(CIRRHOSIS_CODES), na=False)
        ]
        if len(cirrhosis_claims) > 0:
            return False, "Cirrhosis exclusion"
        
        return True, "In denominator"
    
    def is_in_numerator(
        self,
        pharmacy_df: pd.DataFrame
    ) -> Tuple[bool, str, float, Optional[str]]:
        """
        Determine if member is in PDC-STA numerator.
        
        Numerator Criteria:
        1. PDC ≥ 80% for statin medications
        
        Args:
            pharmacy_df: Member's pharmacy data
            
        Returns:
            Tuple of (is_in_numerator: bool, reason: str, pdc_rate: float, potency: str)
        """
        if pharmacy_df.empty:
            return False, "No pharmacy data", 0.0, None
        
        # Filter to statin medications
        statin_fills = pharmacy_df[
            pharmacy_df['medication_name'].str.lower().str.contains(
                '|'.join(STATINS), na=False
            ) &
            (pd.to_datetime(pharmacy_df['fill_date']) >= self.measurement_start) &
            (pd.to_datetime(pharmacy_df['fill_date']) <= self.measurement_end)
        ]
        
        if len(statin_fills) == 0:
            return False, "No statin fills in measurement year", 0.0, None
        
        # Determine statin potency (most common)
        statin_names = statin_fills['medication_name'].str.lower()
        potency = "Unknown"
        
        high_count = sum(statin_names.str.contains('|'.join(HIGH_POTENCY_STATINS), na=False))
        moderate_count = sum(statin_names.str.contains('|'.join(MODERATE_POTENCY_STATINS), na=False))
        low_count = sum(statin_names.str.contains('|'.join(LOW_POTENCY_STATINS), na=False))
        
        if high_count > moderate_count and high_count > low_count:
            potency = "High"
        elif moderate_count > low_count:
            potency = "Moderate"
        elif low_count > 0:
            potency = "Low"
        
        # Calculate PDC
        pdc_rate, days_covered, total_days = self.calculate_pdc(statin_fills)
        
        # Check if PDC meets threshold
        if pdc_rate >= (PDC_THRESHOLD * 100):
            return True, f"PDC {pdc_rate:.1f}% ≥ 80% ({days_covered}/{total_days} days)", pdc_rate, potency
        else:
            return False, f"PDC {pdc_rate:.1f}% < 80% ({days_covered}/{total_days} days)", pdc_rate, potency
    
    def calculate_member_status(
        self,
        member_df: pd.DataFrame,
        claims_df: pd.DataFrame,
        pharmacy_df: pd.DataFrame
    ) -> Dict:
        """
        Calculate PDC-STA measure status for a single member.
        
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
            'pdc_rate': 0.0,
            'fill_count': 0,
            'statin_potency': '',
            'age': 0,
            'has_ascvd': False,
            'has_diabetes': False
        }
        
        # Calculate age
        if 'birth_date' in member_df.columns:
            birth_date = pd.to_datetime(member_df['birth_date'].iloc[0])
            result['age'] = self.calculate_age(birth_date)
        
        # Check for ASCVD/diabetes (for risk stratification)
        ascvd_codes = ['I21', 'I22', 'I63', 'I64']  # MI, stroke
        ascvd_claims = claims_df[
            claims_df['diagnosis_code'].str.startswith(tuple(ascvd_codes), na=False)
        ]
        result['has_ascvd'] = len(ascvd_claims) > 0
        
        diabetes_codes = ['E10', 'E11', 'E13']
        diabetes_claims = claims_df[
            claims_df['diagnosis_code'].str.startswith(tuple(diabetes_codes), na=False)
        ]
        result['has_diabetes'] = len(diabetes_claims) > 0
        
        # Count fills
        if not pharmacy_df.empty and 'medication_name' in pharmacy_df.columns:
            statin_fills = pharmacy_df[
                pharmacy_df['medication_name'].str.lower().str.contains(
                    '|'.join(STATINS), na=False
                )
            ]
            result['fill_count'] = len(statin_fills)
        
        # Check denominator
        in_denom, denom_reason = self.is_in_denominator(member_df, claims_df, pharmacy_df)
        result['in_denominator'] = in_denom
        result['denominator_reason'] = denom_reason
        
        if not in_denom:
            return result
        
        # Check numerator (only if in denominator)
        in_numer, numer_reason, pdc_rate, potency = self.is_in_numerator(pharmacy_df)
        result['in_numerator'] = in_numer
        result['numerator_reason'] = numer_reason
        result['pdc_rate'] = round(pdc_rate, 2)
        result['statin_potency'] = potency or ''
        
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
        Calculate PDC-STA measure rate for a population.
        
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
        
        # Calculate average PDC for denominator
        denom_members = results_df[results_df['in_denominator'] == True]
        avg_pdc = denom_members['pdc_rate'].mean() if len(denom_members) > 0 else 0
        
        # Calculate by potency
        by_potency = {}
        for potency in ['High', 'Moderate', 'Low']:
            potency_members = denom_members[denom_members['statin_potency'] == potency]
            if len(potency_members) > 0:
                by_potency[potency] = {
                    'denominator': len(potency_members),
                    'numerator': potency_members['in_numerator'].sum(),
                    'rate': (potency_members['in_numerator'].sum() / len(potency_members) * 100),
                    'avg_pdc': potency_members['pdc_rate'].mean()
                }
        
        return {
            'total_population': len(results_df),
            'denominator_count': int(denominator_count),
            'numerator_count': int(numerator_count),
            'measure_rate': round(measure_rate, 2),
            'gap_count': int(gap_count),
            'gap_rate': round(gap_rate, 2),
            'avg_pdc': round(avg_pdc, 2),
            'by_potency': by_potency,
            'member_details': results_df
        }


def generate_gap_list(
    members_df: pd.DataFrame,
    claims_df: pd.DataFrame,
    pharmacy_df: pd.DataFrame,
    measurement_year: int = 2025
) -> pd.DataFrame:
    """
    Generate prioritized gap list for PDC-STA measure.
    
    Args:
        members_df: All members' demographic data
        claims_df: All claims data
        pharmacy_df: All pharmacy data
        measurement_year: HEDIS measurement year
        
    Returns:
        DataFrame with gap members and clinical details
    """
    pdc_sta = PDCSTAMeasure(measurement_year)
    results = pdc_sta.calculate_population_rate(members_df, claims_df, pharmacy_df)
    
    # Filter to gap members only
    gap_members = results['member_details'][results['member_details']['has_gap'] == True]
    
    # Add priority scoring
    gap_members = gap_members.copy()
    gap_members['priority_score'] = 100  # Base score
    
    # Highest priority if ASCVD (clinical urgency)
    gap_members.loc[gap_members['has_ascvd'] == True, 'priority_score'] += 50
    
    # High priority if diabetes (guideline-recommended)
    gap_members.loc[gap_members['has_diabetes'] == True, 'priority_score'] += 30
    
    # Higher priority if PDC is very low (< 50%)
    gap_members.loc[gap_members['pdc_rate'] < 50, 'priority_score'] += 25
    
    # Higher priority if older (higher risk)
    gap_members.loc[gap_members['age'] >= 65, 'priority_score'] += 15
    
    # Higher priority if only 2 fills (just in denominator)
    gap_members.loc[gap_members['fill_count'] == 2, 'priority_score'] += 10
    
    # Sort by priority
    gap_members = gap_members.sort_values('priority_score', ascending=False)
    
    return gap_members[['member_id', 'age', 'has_ascvd', 'has_diabetes', 
                        'pdc_rate', 'statin_potency', 'fill_count', 
                        'priority_score', 'numerator_reason']]


# Example usage and testing
if __name__ == "__main__":
    print("PDC-STA Measure Implementation")
    print("=" * 60)
    print(f"Measure: Medication Adherence - Statins (PDC-STA)")
    print(f"Star Rating Weight: 1x")
    print(f"Annual Value: $100K-$150K (100K member plan)")
    print(f"Population: Adults 18+ with 2+ statin fills")
    print(f"Numerator: PDC ≥ 80%")
    print(f"PDC Calculation: Days covered / Total days in year")
    print("=" * 60)


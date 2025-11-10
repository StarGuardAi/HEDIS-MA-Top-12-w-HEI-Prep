"""
BCS - Breast Cancer Screening HEDIS Measure Implementation

HEDIS Specification: MY2023 Volume 2
Measure Code: BCS
Star Rating Weight: 1x (standard)
Annual Value: $150K-$225K (100K member plan)

Population:
- Women ages 50-74
- Continuous enrollment in measurement year
- At least one outpatient encounter

Numerator:
- At least one mammography in measurement year or year prior (2-year lookback)
- CPT codes: 77065-77067 (digital mammography)

Denominator:
- Women 50-74 as of December 31
- Exclude: Bilateral mastectomy, hospice

Author: Analytics Team
Date: October 23, 2025
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
import hashlib


# CPT Codes for Mammography
MAMMOGRAPHY_CPT_CODES = [
    '77065',  # Diagnostic mammography, including CAD when performed; unilateral
    '77066',  # Diagnostic mammography, including CAD when performed; bilateral
    '77067',  # Screening mammography, bilateral (2-view study of each breast), including CAD when performed
    '77063',  # Screening digital breast tomosynthesis, bilateral
]

# ICD-10 Codes for Exclusions
BILATERAL_MASTECTOMY_ICD10 = ['Z90.13']
UNILATERAL_MASTECTOMY_ICD10 = ['Z90.11', 'Z90.12']
HOSPICE_ICD10 = ['Z51.5']

# CPT Codes for Bilateral Mastectomy
BILATERAL_MASTECTOMY_CPT = ['19180', '19182', '19200', '19220', '19240', '19303', '19304', '19305', '19306', '19307']


class BCSMeasure:
    """
    Implementation of BCS (Breast Cancer Screening) HEDIS measure.
    
    This measure tracks mammography screening for women ages 50-74.
    """
    
    def __init__(self, measurement_year: int = 2025):
        """
        Initialize BCS measure calculator.
        
        Args:
            measurement_year: HEDIS measurement year (default 2025)
        """
        self.measurement_year = measurement_year
        self.measurement_end = datetime(measurement_year, 12, 31)
        self.lookback_start = datetime(measurement_year - 1, 1, 1)  # 2-year lookback
        self.measurement_start = datetime(measurement_year, 1, 1)
        
    def calculate_age(self, birth_date: datetime) -> int:
        """
        Calculate age as of December 31 of measurement year (HEDIS standard).
        
        Args:
            birth_date: Member's date of birth
            
        Returns:
            Age in years
        """
        age = self.measurement_year - birth_date.year
        if (self.measurement_end.month, self.measurement_end.day) < (birth_date.month, birth_date.day):
            age -= 1
        return age
    
    def is_in_denominator(
        self,
        member_df: pd.DataFrame,
        claims_df: pd.DataFrame,
        procedure_df: Optional[pd.DataFrame] = None
    ) -> Tuple[bool, str]:
        """
        Determine if member is in BCS denominator (eligible population).
        
        Criteria:
        1. Female
        2. Age 50-74 as of December 31
        3. Continuous enrollment in measurement year
        4. At least one outpatient encounter
        5. Exclude: Bilateral mastectomy, hospice
        
        Args:
            member_df: Member demographic data
            claims_df: Claims data for the member
            procedure_df: Procedure data (optional, for exclusions)
            
        Returns:
            Tuple of (in_denominator: bool, reason: str)
        """
        # 1. Check gender (must be female)
        if 'gender' in member_df.columns:
            gender = member_df['gender'].iloc[0]
            if gender != 'F':
                return False, f"gender_not_female_{gender}"
        else:
            return False, "gender_unknown"
        
        # 2. Check age (50-74 as of Dec 31)
        if 'birth_date' in member_df.columns:
            birth_date = pd.to_datetime(member_df['birth_date'].iloc[0])
            age = self.calculate_age(birth_date)
            if age < 50:
                return False, f"age_too_young_{age}"
            if age > 74:
                return False, f"age_too_old_{age}"
        else:
            return False, "birth_date_missing"
        
        # 3. Check continuous enrollment (12 months in measurement year)
        if 'enrollment_months' in member_df.columns:
            enrollment_months = member_df['enrollment_months'].iloc[0]
            if enrollment_months < 12:
                return False, f"not_continuously_enrolled_{enrollment_months}mo"
        else:
            # Assume continuous enrollment if not specified
            pass
        
        # 4. Check for at least one outpatient encounter
        outpatient_encounters = claims_df[
            (claims_df['claim_type'].isin(['outpatient', 'professional'])) &
            (pd.to_datetime(claims_df['service_date']) >= self.measurement_start) &
            (pd.to_datetime(claims_df['service_date']) <= self.measurement_end)
        ]
        if len(outpatient_encounters) == 0:
            return False, "no_outpatient_encounters"
        
        # 5. Check exclusions
        
        # Bilateral mastectomy (ICD-10)
        bilateral_mastectomy_dx = claims_df[
            claims_df['diagnosis_code'].isin(BILATERAL_MASTECTOMY_ICD10)
        ]
        if len(bilateral_mastectomy_dx) > 0:
            return False, "bilateral_mastectomy_history"
        
        # Bilateral mastectomy (CPT - two unilateral or one bilateral)
        if procedure_df is not None and not procedure_df.empty:
            bilateral_mastectomy_proc = procedure_df[
                procedure_df['procedure_code'].isin(BILATERAL_MASTECTOMY_CPT)
            ]
            if len(bilateral_mastectomy_proc) >= 2:  # Two unilateral
                return False, "bilateral_mastectomy_procedures"
            
            # Check for unilateral on both sides
            unilateral_mastectomy_dx = claims_df[
                claims_df['diagnosis_code'].isin(UNILATERAL_MASTECTOMY_ICD10)
            ]
            if len(unilateral_mastectomy_dx) >= 2:
                return False, "bilateral_mastectomy_unilateral_both_sides"
        
        # Hospice
        hospice = claims_df[
            claims_df['diagnosis_code'].isin(HOSPICE_ICD10)
        ]
        if len(hospice) > 0:
            return False, "hospice_care"
        
        # All criteria met
        return True, "eligible"
    
    def is_in_numerator(
        self,
        procedure_df: pd.DataFrame
    ) -> Tuple[bool, str]:
        """
        Determine if member is in BCS numerator (compliant).
        
        Criteria:
        - At least one mammography in measurement year or year prior (2-year lookback)
        
        Args:
            procedure_df: Procedure data for the member
            
        Returns:
            Tuple of (in_numerator: bool, reason: str)
        """
        if procedure_df.empty:
            return False, "no_mammography_found"
        
        # Check for mammography CPT codes in 2-year lookback window
        mammography = procedure_df[
            (procedure_df['procedure_code'].isin(MAMMOGRAPHY_CPT_CODES)) &
            (pd.to_datetime(procedure_df['service_date']) >= self.lookback_start) &
            (pd.to_datetime(procedure_df['service_date']) <= self.measurement_end)
        ]
        
        if len(mammography) > 0:
            # Get most recent mammography date
            last_mammo_date = pd.to_datetime(mammography['service_date']).max()
            return True, f"compliant_mammography_{last_mammo_date.strftime('%Y-%m-%d')}"
        
        return False, "no_mammography_in_2yr_window"
    
    def calculate_member_status(
        self,
        member_id: str,
        member_df: pd.DataFrame,
        claims_df: pd.DataFrame,
        procedure_df: Optional[pd.DataFrame] = None
    ) -> Dict:
        """
        Calculate BCS status for a single member.
        
        Args:
            member_id: Unique member identifier
            member_df: Member demographic data
            claims_df: Claims data for the member
            procedure_df: Procedure data for the member
            
        Returns:
            Dictionary with member's BCS status and details
        """
        # Hash member_id for PHI protection
        member_hash = hashlib.sha256(str(member_id).encode()).hexdigest()[:16]
        
        result = {
            'member_id_hash': member_hash,
            'measurement_year': self.measurement_year,
            'measure': 'BCS',
        }
        
        # Check denominator
        in_denominator, denom_reason = self.is_in_denominator(member_df, claims_df, procedure_df)
        result['in_denominator'] = in_denominator
        result['denominator_reason'] = denom_reason
        
        if not in_denominator:
            result['in_numerator'] = False
            result['numerator_reason'] = 'not_in_denominator'
            result['has_gap'] = False
            result['gap_type'] = None
            return result
        
        # Check numerator
        if procedure_df is not None:
            in_numerator, num_reason = self.is_in_numerator(procedure_df)
        else:
            in_numerator, num_reason = False, "no_procedure_data"
        
        result['in_numerator'] = in_numerator
        result['numerator_reason'] = num_reason
        result['has_gap'] = not in_numerator
        
        # Classify gap type
        if in_numerator:
            result['gap_type'] = None
        else:
            if procedure_df is not None and not procedure_df.empty:
                # Check if ever had mammography (beyond 2-year window)
                all_mammography = procedure_df[
                    procedure_df['procedure_code'].isin(MAMMOGRAPHY_CPT_CODES)
                ]
                if len(all_mammography) > 0:
                    result['gap_type'] = 'overdue_screening'
                else:
                    result['gap_type'] = 'never_screened'
            else:
                result['gap_type'] = 'never_screened'
        
        return result
    
    def calculate_population_rate(
        self,
        members_df: pd.DataFrame,
        claims_df: pd.DataFrame,
        procedure_df: Optional[pd.DataFrame] = None,
        member_id_col: str = 'member_id'
    ) -> Dict:
        """
        Calculate BCS measure rate for a population.
        
        Args:
            members_df: Member demographics for population
            claims_df: Claims data for population
            procedure_df: Procedure data for population
            member_id_col: Column name for member identifier
            
        Returns:
            Dictionary with population-level BCS metrics
        """
        results = []
        
        # Process each member
        for member_id in members_df[member_id_col].unique():
            member_data = members_df[members_df[member_id_col] == member_id]
            member_claims = claims_df[claims_df[member_id_col] == member_id]
            member_procedures = procedure_df[procedure_df[member_id_col] == member_id] if procedure_df is not None else pd.DataFrame()
            
            member_result = self.calculate_member_status(
                member_id,
                member_data,
                member_claims,
                member_procedures
            )
            results.append(member_result)
        
        # Convert to DataFrame for analysis
        results_df = pd.DataFrame(results)
        
        # Calculate summary statistics
        total_population = len(results_df)
        denominator = results_df['in_denominator'].sum()
        numerator = results_df['in_numerator'].sum()
        gaps = results_df['has_gap'].sum()
        
        rate = (numerator / denominator * 100) if denominator > 0 else 0
        
        summary = {
            'measure': 'BCS',
            'measurement_year': self.measurement_year,
            'total_population': total_population,
            'denominator': denominator,
            'numerator': numerator,
            'gaps': gaps,
            'rate': rate,
            'compliant_pct': rate,
            'gap_pct': (gaps / denominator * 100) if denominator > 0 else 0,
        }
        
        # Gap breakdown
        gap_types = results_df[results_df['has_gap']]['gap_type'].value_counts().to_dict()
        summary['gap_breakdown'] = gap_types
        
        # Denominator exclusions
        exclusion_reasons = results_df[~results_df['in_denominator']]['denominator_reason'].value_counts().to_dict()
        summary['exclusion_reasons'] = exclusion_reasons
        
        return summary
    
    def generate_gap_list(
        self,
        members_df: pd.DataFrame,
        claims_df: pd.DataFrame,
        procedure_df: Optional[pd.DataFrame] = None,
        member_id_col: str = 'member_id',
        include_compliant: bool = False
    ) -> pd.DataFrame:
        """
        Generate actionable gap list for care management.
        
        Args:
            members_df: Member demographics
            claims_df: Claims data
            procedure_df: Procedure data
            member_id_col: Member identifier column
            include_compliant: Include compliant members in output
            
        Returns:
            DataFrame with gap list and priority flags
        """
        results = []
        
        # Process each member
        for member_id in members_df[member_id_col].unique():
            member_data = members_df[members_df[member_id_col] == member_id]
            member_claims = claims_df[claims_df[member_id_col] == member_id]
            member_procedures = procedure_df[procedure_df[member_id_col] == member_id] if procedure_df is not None else pd.DataFrame()
            
            member_result = self.calculate_member_status(
                member_id,
                member_data,
                member_claims,
                member_procedures
            )
            
            # Add member details for gap list
            if 'birth_date' in member_data.columns:
                member_result['age'] = self.calculate_age(pd.to_datetime(member_data['birth_date'].iloc[0]))
            if 'gender' in member_data.columns:
                member_result['gender'] = member_data['gender'].iloc[0]
            
            # Priority scoring
            if member_result['has_gap']:
                priority_score = 0
                
                # Higher priority for older women (60+)
                if member_result.get('age', 0) >= 60:
                    priority_score += 10
                
                # Higher priority for never screened
                if member_result['gap_type'] == 'never_screened':
                    priority_score += 20
                elif member_result['gap_type'] == 'overdue_screening':
                    priority_score += 10
                
                member_result['priority_score'] = priority_score
                member_result['priority_level'] = 'HIGH' if priority_score >= 20 else 'MEDIUM' if priority_score >= 10 else 'LOW'
            else:
                member_result['priority_score'] = 0
                member_result['priority_level'] = None
            
            results.append(member_result)
        
        # Convert to DataFrame
        gap_list_df = pd.DataFrame(results)
        
        # Filter to gaps only (unless include_compliant=True)
        if not include_compliant:
            gap_list_df = gap_list_df[gap_list_df['has_gap']]
        
        # Sort by priority
        gap_list_df = gap_list_df.sort_values('priority_score', ascending=False)
        
        return gap_list_df


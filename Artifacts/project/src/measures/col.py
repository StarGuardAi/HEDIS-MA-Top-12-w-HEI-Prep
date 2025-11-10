"""
COL - Colorectal Cancer Screening HEDIS Measure Implementation

HEDIS Specification: MY2023 Volume 2
Measure Code: COL
Star Rating Weight: 1x (standard)
Annual Value: $150K-$225K (100K member plan)

Population:
- Adults ages 50-75 (both genders)
- Continuous enrollment in measurement year
- At least one outpatient encounter

Numerator (Multiple Options):
- Colonoscopy in past 10 years, OR
- FIT (fecal immunochemical test) annually, OR
- Cologuard (FIT-DNA) every 3 years, OR
- Flexible sigmoidoscopy every 5 years

Denominator:
- Adults 50-75 as of December 31
- Exclude: Total colectomy, hospice

Author: Analytics Team
Date: October 23, 2025
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
import hashlib


# CPT Codes for Colorectal Cancer Screening
COLONOSCOPY_CPT_CODES = [
    '44388', '44389', '44390', '44391', '44392', '44393', '44394',  # Laparoscopic
    '45378', '45379', '45380', '45381', '45382', '45383', '45384',  # Colonoscopy
    '45385', '45386', '45387', '45388', '45389', '45390', '45391',  # Colonoscopy continued
    '45392', '45393', '45398',  # Colonoscopy with stent
]

FIT_CPT_CODES = [
    '82270',  # Fecal occult blood test (FOBT), 1-3 simultaneous
    '82274',  # Fecal immunochemical test (FIT)
]

COLOGUARD_CPT_CODES = [
    '81528',  # FIT-DNA (Cologuard)
]

FLEXIBLE_SIG_CPT_CODES = [
    '45330', '45331', '45332', '45333', '45334', '45335',  # Flexible sigmoidoscopy
    '45337', '45338', '45339', '45340', '45341', '45342',  # Flexible sigmoidoscopy continued
    '45345', '45346', '45347',  # Flexible sigmoidoscopy with biopsy
]

# ICD-10 Codes for Exclusions
TOTAL_COLECTOMY_ICD10 = ['Z90.49']
HOSPICE_ICD10 = ['Z51.5']
COLORECTAL_CANCER_ICD10 = ['C18', 'C19', 'C20', 'C21']  # Malignant neoplasm


class COLMeasure:
    """
    Implementation of COL (Colorectal Cancer Screening) HEDIS measure.
    
    This measure tracks colorectal cancer screening for adults ages 50-75
    using multiple screening modalities with different lookback periods.
    """
    
    def __init__(self, measurement_year: int = 2025):
        """
        Initialize COL measure calculator.
        
        Args:
            measurement_year: HEDIS measurement year (default 2025)
        """
        self.measurement_year = measurement_year
        self.measurement_end = datetime(measurement_year, 12, 31)
        self.measurement_start = datetime(measurement_year, 1, 1)
        
        # Lookback windows for different screening modalities
        self.colonoscopy_lookback = datetime(measurement_year - 10, 1, 1)  # 10 years
        self.fit_lookback = datetime(measurement_year, 1, 1)  # Annual (current year)
        self.cologuard_lookback = datetime(measurement_year - 3, 1, 1)  # 3 years
        self.flexible_sig_lookback = datetime(measurement_year - 5, 1, 1)  # 5 years
        
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
        Determine if member is in COL denominator (eligible population).
        
        Criteria:
        1. Both genders (M or F)
        2. Age 50-75 as of December 31
        3. Continuous enrollment in measurement year
        4. At least one outpatient encounter
        5. Exclude: Total colectomy, hospice
        
        Args:
            member_df: Member demographic data
            claims_df: Claims data for the member
            procedure_df: Procedure data (optional, for exclusions)
            
        Returns:
            Tuple of (in_denominator: bool, reason: str)
        """
        # 1. Check gender (both M and F eligible)
        if 'gender' in member_df.columns:
            gender = member_df['gender'].iloc[0]
            if gender not in ['M', 'F']:
                return False, f"gender_invalid_{gender}"
        else:
            return False, "gender_unknown"
        
        # 2. Check age (50-75 as of Dec 31)
        if 'birth_date' in member_df.columns:
            birth_date = pd.to_datetime(member_df['birth_date'].iloc[0])
            age = self.calculate_age(birth_date)
            if age < 50:
                return False, f"age_too_young_{age}"
            if age > 75:
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
        
        # Total colectomy
        total_colectomy = claims_df[
            claims_df['diagnosis_code'].isin(TOTAL_COLECTOMY_ICD10)
        ]
        if len(total_colectomy) > 0:
            return False, "total_colectomy_history"
        
        # Hospice
        hospice = claims_df[
            claims_df['diagnosis_code'].isin(HOSPICE_ICD10)
        ]
        if len(hospice) > 0:
            return False, "hospice_care"
        
        # All criteria met
        return True, "eligible"
    
    def is_in_numerator_colonoscopy(
        self,
        procedure_df: pd.DataFrame
    ) -> Tuple[bool, Optional[datetime]]:
        """
        Check for colonoscopy screening (10-year lookback).
        
        Args:
            procedure_df: Procedure data for the member
            
        Returns:
            Tuple of (has_colonoscopy: bool, most_recent_date: Optional[datetime])
        """
        if procedure_df.empty:
            return False, None
        
        colonoscopy = procedure_df[
            (procedure_df['procedure_code'].isin(COLONOSCOPY_CPT_CODES)) &
            (pd.to_datetime(procedure_df['service_date']) >= self.colonoscopy_lookback) &
            (pd.to_datetime(procedure_df['service_date']) <= self.measurement_end)
        ]
        
        if len(colonoscopy) > 0:
            most_recent = pd.to_datetime(colonoscopy['service_date']).max()
            return True, most_recent
        
        return False, None
    
    def is_in_numerator_fit(
        self,
        procedure_df: pd.DataFrame
    ) -> Tuple[bool, Optional[datetime]]:
        """
        Check for FIT screening (annual - current year).
        
        Args:
            procedure_df: Procedure data for the member
            
        Returns:
            Tuple of (has_fit: bool, most_recent_date: Optional[datetime])
        """
        if procedure_df.empty:
            return False, None
        
        fit = procedure_df[
            (procedure_df['procedure_code'].isin(FIT_CPT_CODES)) &
            (pd.to_datetime(procedure_df['service_date']) >= self.fit_lookback) &
            (pd.to_datetime(procedure_df['service_date']) <= self.measurement_end)
        ]
        
        if len(fit) > 0:
            most_recent = pd.to_datetime(fit['service_date']).max()
            return True, most_recent
        
        return False, None
    
    def is_in_numerator_cologuard(
        self,
        procedure_df: pd.DataFrame
    ) -> Tuple[bool, Optional[datetime]]:
        """
        Check for Cologuard screening (3-year lookback).
        
        Args:
            procedure_df: Procedure data for the member
            
        Returns:
            Tuple of (has_cologuard: bool, most_recent_date: Optional[datetime])
        """
        if procedure_df.empty:
            return False, None
        
        cologuard = procedure_df[
            (procedure_df['procedure_code'].isin(COLOGUARD_CPT_CODES)) &
            (pd.to_datetime(procedure_df['service_date']) >= self.cologuard_lookback) &
            (pd.to_datetime(procedure_df['service_date']) <= self.measurement_end)
        ]
        
        if len(cologuard) > 0:
            most_recent = pd.to_datetime(cologuard['service_date']).max()
            return True, most_recent
        
        return False, None
    
    def is_in_numerator_flexible_sig(
        self,
        procedure_df: pd.DataFrame
    ) -> Tuple[bool, Optional[datetime]]:
        """
        Check for flexible sigmoidoscopy screening (5-year lookback).
        
        Args:
            procedure_df: Procedure data for the member
            
        Returns:
            Tuple of (has_flex_sig: bool, most_recent_date: Optional[datetime])
        """
        if procedure_df.empty:
            return False, None
        
        flex_sig = procedure_df[
            (procedure_df['procedure_code'].isin(FLEXIBLE_SIG_CPT_CODES)) &
            (pd.to_datetime(procedure_df['service_date']) >= self.flexible_sig_lookback) &
            (pd.to_datetime(procedure_df['service_date']) <= self.measurement_end)
        ]
        
        if len(flex_sig) > 0:
            most_recent = pd.to_datetime(flex_sig['service_date']).max()
            return True, most_recent
        
        return False, None
    
    def is_in_numerator(
        self,
        procedure_df: pd.DataFrame
    ) -> Tuple[bool, str]:
        """
        Determine if member is in COL numerator (compliant).
        
        Member is compliant if they have ANY of:
        - Colonoscopy in past 10 years
        - FIT in current year
        - Cologuard in past 3 years
        - Flexible sigmoidoscopy in past 5 years
        
        Args:
            procedure_df: Procedure data for the member
            
        Returns:
            Tuple of (in_numerator: bool, reason: str)
        """
        if procedure_df.empty:
            return False, "no_screening_found"
        
        # Check each modality
        has_colonoscopy, colo_date = self.is_in_numerator_colonoscopy(procedure_df)
        has_fit, fit_date = self.is_in_numerator_fit(procedure_df)
        has_cologuard, cologuard_date = self.is_in_numerator_cologuard(procedure_df)
        has_flex_sig, flex_sig_date = self.is_in_numerator_flexible_sig(procedure_df)
        
        # Member is compliant if ANY modality is satisfied
        if has_colonoscopy:
            return True, f"compliant_colonoscopy_{colo_date.strftime('%Y-%m-%d')}"
        elif has_fit:
            return True, f"compliant_fit_{fit_date.strftime('%Y-%m-%d')}"
        elif has_cologuard:
            return True, f"compliant_cologuard_{cologuard_date.strftime('%Y-%m-%d')}"
        elif has_flex_sig:
            return True, f"compliant_flexible_sig_{flex_sig_date.strftime('%Y-%m-%d')}"
        
        return False, "no_screening_in_lookback_windows"
    
    def calculate_member_status(
        self,
        member_id: str,
        member_df: pd.DataFrame,
        claims_df: pd.DataFrame,
        procedure_df: Optional[pd.DataFrame] = None
    ) -> Dict:
        """
        Calculate COL status for a single member.
        
        Args:
            member_id: Unique member identifier
            member_df: Member demographic data
            claims_df: Claims data for the member
            procedure_df: Procedure data for the member
            
        Returns:
            Dictionary with member's COL status and details
        """
        # Hash member_id for PHI protection
        member_hash = hashlib.sha256(str(member_id).encode()).hexdigest()[:16]
        
        result = {
            'member_id_hash': member_hash,
            'measurement_year': self.measurement_year,
            'measure': 'COL',
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
        
        # Classify gap type and recommended screening
        if in_numerator:
            result['gap_type'] = None
            result['recommended_screening'] = None
        else:
            # Determine best screening option based on history
            if procedure_df is not None and not procedure_df.empty:
                # Check if ever had colonoscopy (beyond 10-year window)
                all_colonoscopy = procedure_df[
                    procedure_df['procedure_code'].isin(COLONOSCOPY_CPT_CODES)
                ]
                if len(all_colonoscopy) > 0:
                    result['gap_type'] = 'overdue_colonoscopy'
                    result['recommended_screening'] = 'colonoscopy_due'
                else:
                    result['gap_type'] = 'never_screened'
                    result['recommended_screening'] = 'any_screening_fit_or_colonoscopy'
            else:
                result['gap_type'] = 'never_screened'
                result['recommended_screening'] = 'any_screening_fit_or_colonoscopy'
        
        return result
    
    def calculate_population_rate(
        self,
        members_df: pd.DataFrame,
        claims_df: pd.DataFrame,
        procedure_df: Optional[pd.DataFrame] = None,
        member_id_col: str = 'member_id'
    ) -> Dict:
        """
        Calculate COL measure rate for a population.
        
        Args:
            members_df: Member demographics for population
            claims_df: Claims data for population
            procedure_df: Procedure data for population
            member_id_col: Column name for member identifier
            
        Returns:
            Dictionary with population-level COL metrics
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
            'measure': 'COL',
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
        
        # Screening modality breakdown (from numerator reasons)
        screening_modalities = results_df[results_df['in_numerator']]['numerator_reason'].apply(
            lambda x: x.split('_')[1] if '_' in x else 'unknown'
        ).value_counts().to_dict()
        summary['screening_modality_breakdown'] = screening_modalities
        
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
                
                # Higher priority for older adults (65+)
                if member_result.get('age', 0) >= 65:
                    priority_score += 10
                
                # Highest priority for never screened
                if member_result['gap_type'] == 'never_screened':
                    priority_score += 30
                elif member_result['gap_type'] == 'overdue_colonoscopy':
                    priority_score += 15
                
                member_result['priority_score'] = priority_score
                member_result['priority_level'] = 'HIGH' if priority_score >= 30 else 'MEDIUM' if priority_score >= 15 else 'LOW'
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


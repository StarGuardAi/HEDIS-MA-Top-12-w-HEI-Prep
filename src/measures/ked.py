"""
KED - Kidney Health Evaluation for Patients with Diabetes

NEW 2025 HEDIS Measure - Triple-Weighted
Replaces HBD (Hemoglobin A1c Control) as a triple-weighted measure

HEDIS Specification: MY2025
Value: $360-615K
Weight: 3x (Triple-weighted)

Description:
The percentage of members 18-75 years of age with diabetes (type 1 and type 2)
who had each of the following:
- A kidney health evaluation (eGFR)
- A urine albumin test (ACR or urine albumin)
during the measurement year.
"""

import pandas as pd
import numpy as np
import logging
from typing import Dict, List, Optional, Tuple, Set, Any
from datetime import datetime, timedelta
from dataclasses import dataclass

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class KEDResult:
    """Results for KED measure calculation."""
    member_id: str
    in_denominator: bool
    in_numerator: bool
    exclusion_reason: Optional[str]
    has_diabetes: bool
    age_eligible: bool
    has_egfr_test: bool
    egfr_test_date: Optional[datetime]
    has_acr_test: bool
    acr_test_date: Optional[datetime]
    compliant: bool


class KEDMeasure:
    """
    KED - Kidney Health Evaluation for Patients with Diabetes
    
    NEW 2025 HEDIS Measure - Triple-Weighted
    
    Denominator: Members 18-75 with diabetes diagnosis
    Numerator: Members with both eGFR AND ACR tests in measurement year
    Exclusions: ESRD, kidney transplant, hospice
    
    Data Sources:
    - Claims (diabetes diagnosis, exclusions)
    - Labs (eGFR, ACR/urine albumin)
    """
    
    # ICD-10 Diabetes Codes
    DIABETES_CODES = {
        # Type 1 Diabetes
        'E10.10', 'E10.11', 'E10.21', 'E10.22', 'E10.29', 'E10.311', 'E10.319',
        'E10.321', 'E10.329', 'E10.331', 'E10.339', 'E10.341', 'E10.349',
        'E10.351', 'E10.359', 'E10.36', 'E10.39', 'E10.40', 'E10.41', 'E10.42',
        'E10.43', 'E10.44', 'E10.49', 'E10.51', 'E10.52', 'E10.59', 'E10.610',
        'E10.618', 'E10.620', 'E10.621', 'E10.622', 'E10.628', 'E10.630',
        'E10.638', 'E10.641', 'E10.649', 'E10.65', 'E10.69', 'E10.8', 'E10.9',
        
        # Type 2 Diabetes
        'E11.00', 'E11.01', 'E11.10', 'E11.11', 'E11.21', 'E11.22', 'E11.29',
        'E11.311', 'E11.319', 'E11.321', 'E11.329', 'E11.331', 'E11.339',
        'E11.341', 'E11.349', 'E11.351', 'E11.359', 'E11.36', 'E11.39',
        'E11.40', 'E11.41', 'E11.42', 'E11.43', 'E11.44', 'E11.49', 'E11.51',
        'E11.52', 'E11.59', 'E11.610', 'E11.618', 'E11.620', 'E11.621',
        'E11.622', 'E11.628', 'E11.630', 'E11.638', 'E11.641', 'E11.649',
        'E11.65', 'E11.69', 'E11.8', 'E11.9',
    }
    
    # ESRD/Kidney Transplant Exclusion Codes
    EXCLUSION_CODES = {
        # ESRD
        'N18.6',    # End stage renal disease
        'Z99.2',    # Dependence on renal dialysis
        'Z49.01',   # Encounter for fitting and adjustment of extracorporeal dialysis catheter
        'Z49.02',   # Encounter for fitting and adjustment of peritoneal dialysis catheter
        
        # Kidney Transplant
        'Z94.0',    # Kidney transplant status
        'Z76.82',   # Awaiting organ transplant status
    }
    
    # LOINC Codes (from labs_loader)
    EGFR_LOINC_CODES = [
        '48642-3',  # eGFR CKD-EPI
        '48643-1',  # eGFR MDRD
        '62238-1',  # eGFR non-African American
        '88294-4',  # eGFR African American
    ]
    
    ACR_LOINC_CODES = [
        '9318-7',   # ACR
        '13705-9',  # ACR First Morning Urine
        '14958-3',  # ACR Random Urine
        '14957-5',  # Microalbumin (mg/dL)
        '1754-1',   # Albumin in Urine (mg/dL)
        '2888-6',   # Albumin in Urine (mg/24h)
    ]
    
    def __init__(self, measurement_year: int = 2025):
        """
        Initialize KED measure calculator.
        
        Args:
            measurement_year: Measurement year for evaluation
        """
        self.measurement_year = measurement_year
        self.my_start = datetime(measurement_year, 1, 1)
        self.my_end = datetime(measurement_year, 12, 31)
        
        logger.info(f"Initialized KED measure for MY{measurement_year}")
    
    def identify_denominator(self,
                           member_df: pd.DataFrame,
                           claims_df: pd.DataFrame) -> pd.DataFrame:
        """
        Identify denominator: Members 18-75 with diabetes.
        
        Args:
            member_df: Member demographics DataFrame
            claims_df: Claims DataFrame with diagnosis codes
            
        Returns:
            DataFrame with denominator flags
        """
        logger.info("Identifying KED denominator")
        
        # Age eligibility (18-75 on December 31 of MY)
        member_df['age_at_my_end'] = (
            self.my_end - pd.to_datetime(member_df['birth_date'])
        ).dt.days // 365
        
        member_df['age_eligible'] = (
            (member_df['age_at_my_end'] >= 18) &
            (member_df['age_at_my_end'] <= 75)
        )
        
        # Diabetes diagnosis (2 outpatient or 1 inpatient/ED during MY or year prior)
        lookback_start = self.my_start - timedelta(days=365)
        
        diabetes_claims = claims_df[
            (claims_df['diagnosis_code'].isin(self.DIABETES_CODES)) &
            (pd.to_datetime(claims_df['service_date']) >= lookback_start) &
            (pd.to_datetime(claims_df['service_date']) <= self.my_end)
        ].copy()
        
        # Count claims by member and service type
        diabetes_summary = diabetes_claims.groupby('member_id').agg({
            'claim_type': lambda x: (x == 'outpatient').sum(),  # Outpatient count
            'service_date': 'count'  # Total count
        }).rename(columns={'claim_type': 'outpatient_count', 'service_date': 'total_count'})
        
        # Has diabetes if: 2+ outpatient OR 1+ inpatient/ED
        diabetes_summary['has_diabetes'] = (
            (diabetes_summary['outpatient_count'] >= 2) |
            (diabetes_summary['total_count'] - diabetes_summary['outpatient_count'] >= 1)
        )
        
        # Merge with member data
        member_df = member_df.merge(
            diabetes_summary[['has_diabetes']],
            left_on='member_id',
            right_index=True,
            how='left'
        )
        member_df['has_diabetes'] = member_df['has_diabetes'].fillna(False)
        
        # In denominator = age eligible + has diabetes
        member_df['in_denominator'] = (
            member_df['age_eligible'] &
            member_df['has_diabetes']
        )
        
        denom_count = member_df['in_denominator'].sum()
        logger.info(f"KED Denominator: {denom_count} members")
        
        return member_df
    
    def apply_exclusions(self,
                        member_df: pd.DataFrame,
                        claims_df: pd.DataFrame) -> pd.DataFrame:
        """
        Apply exclusions: ESRD, kidney transplant, hospice.
        
        Args:
            member_df: Member DataFrame with denominator flags
            claims_df: Claims DataFrame
            
        Returns:
            DataFrame with exclusion flags
        """
        logger.info("Applying KED exclusions")
        
        # ESRD/Kidney transplant exclusions
        exclusion_claims = claims_df[
            (claims_df['diagnosis_code'].isin(self.EXCLUSION_CODES)) &
            (pd.to_datetime(claims_df['service_date']) >= self.my_start) &
            (pd.to_datetime(claims_df['service_date']) <= self.my_end)
        ]
        
        excluded_members = exclusion_claims['member_id'].unique()
        
        member_df['excluded'] = member_df['member_id'].isin(excluded_members)
        
        # Update denominator to exclude
        member_df['in_denominator_final'] = (
            member_df['in_denominator'] &
            ~member_df['excluded']
        )
        
        excluded_count = member_df['excluded'].sum()
        final_denom = member_df['in_denominator_final'].sum()
        
        logger.info(f"Excluded {excluded_count} members (ESRD/transplant)")
        logger.info(f"Final KED Denominator: {final_denom} members")
        
        return member_df
    
    def identify_numerator(self,
                          member_df: pd.DataFrame,
                          labs_df: pd.DataFrame) -> pd.DataFrame:
        """
        Identify numerator: Members with both eGFR AND ACR tests in MY.
        
        Args:
            member_df: Member DataFrame with denominator flags
            labs_df: Labs DataFrame with test results
            
        Returns:
            DataFrame with numerator flags
        """
        logger.info("Identifying KED numerator")
        
        # Filter labs to measurement year
        labs_my = labs_df[
            (pd.to_datetime(labs_df['test_date']) >= self.my_start) &
            (pd.to_datetime(labs_df['test_date']) <= self.my_end)
        ].copy()
        
        # eGFR tests
        egfr_tests = labs_my[
            labs_my['loinc_code'].isin(self.EGFR_LOINC_CODES)
        ].groupby('member_id').agg({
            'test_date': 'max',
            'loinc_code': 'count'
        }).rename(columns={'test_date': 'egfr_test_date', 'loinc_code': 'egfr_count'})
        
        egfr_tests['has_egfr_test'] = True
        
        # ACR/Urine albumin tests
        acr_tests = labs_my[
            labs_my['loinc_code'].isin(self.ACR_LOINC_CODES)
        ].groupby('member_id').agg({
            'test_date': 'max',
            'loinc_code': 'count'
        }).rename(columns={'test_date': 'acr_test_date', 'loinc_code': 'acr_count'})
        
        acr_tests['has_acr_test'] = True
        
        # Merge with member data
        member_df = member_df.merge(egfr_tests, left_on='member_id', right_index=True, how='left')
        member_df = member_df.merge(acr_tests, left_on='member_id', right_index=True, how='left')
        
        member_df['has_egfr_test'] = member_df['has_egfr_test'].fillna(False)
        member_df['has_acr_test'] = member_df['has_acr_test'].fillna(False)
        
        # Numerator = BOTH eGFR AND ACR in measurement year
        member_df['in_numerator'] = (
            member_df['in_denominator_final'] &
            member_df['has_egfr_test'] &
            member_df['has_acr_test']
        )
        
        numerator_count = member_df['in_numerator'].sum()
        denominator_count = member_df['in_denominator_final'].sum()
        
        if denominator_count > 0:
            rate = numerator_count / denominator_count * 100
            logger.info(f"KED Numerator: {numerator_count} members")
            logger.info(f"KED Rate: {rate:.2f}%")
        else:
            logger.warning("KED Denominator is 0")
        
        return member_df
    
    def calculate_measure(self,
                         member_df: pd.DataFrame,
                         claims_df: pd.DataFrame,
                         labs_df: pd.DataFrame) -> Dict[str, Any]:
        """
        Calculate complete KED measure.
        
        Args:
            member_df: Member demographics DataFrame
            claims_df: Claims DataFrame
            labs_df: Labs DataFrame
            
        Returns:
            Dictionary with measure results
        """
        logger.info("Calculating KED measure")
        
        # Step 1: Identify denominator
        member_df = self.identify_denominator(member_df, claims_df)
        
        # Step 2: Apply exclusions
        member_df = self.apply_exclusions(member_df, claims_df)
        
        # Step 3: Identify numerator
        member_df = self.identify_numerator(member_df, labs_df)
        
        # Calculate measure results
        denominator = member_df['in_denominator_final'].sum()
        numerator = member_df['in_numerator'].sum()
        rate = (numerator / denominator * 100) if denominator > 0 else 0.0
        
        # Get gap members (in denominator but not numerator)
        gap_members = member_df[
            member_df['in_denominator_final'] &
            ~member_df['in_numerator']
        ].copy()
        
        # Analyze gaps
        gap_analysis = {
            'total_gaps': len(gap_members),
            'missing_egfr': (~gap_members['has_egfr_test']).sum(),
            'missing_acr': (~gap_members['has_acr_test']).sum(),
            'missing_both': (
                ~gap_members['has_egfr_test'] &
                ~gap_members['has_acr_test']
            ).sum(),
        }
        
        results = {
            'measure_code': 'KED',
            'measure_name': 'Kidney Health Evaluation for Patients with Diabetes',
            'measurement_year': self.measurement_year,
            'weight': 3.0,  # Triple-weighted
            'new_2025': True,
            
            # Performance
            'denominator': int(denominator),
            'numerator': int(numerator),
            'rate': float(rate),
            
            # Gap analysis
            'gaps': gap_analysis,
            'gap_members': gap_members['member_id'].tolist(),
            
            # Member-level results
            'member_results': member_df
        }
        
        logger.info("=" * 80)
        logger.info(f"KED MEASURE RESULTS - MY{self.measurement_year}")
        logger.info("=" * 80)
        logger.info(f"Denominator: {denominator:,} members")
        logger.info(f"Numerator: {numerator:,} members")
        logger.info(f"Rate: {rate:.2f}%")
        logger.info(f"Gaps: {gap_analysis['total_gaps']:,} members")
        logger.info(f"  - Missing eGFR: {gap_analysis['missing_egfr']:,}")
        logger.info(f"  - Missing ACR: {gap_analysis['missing_acr']:,}")
        logger.info(f"  - Missing both: {gap_analysis['missing_both']:,}")
        logger.info("=" * 80)
        
        return results


def calculate_ked_measure(member_df: pd.DataFrame,
                          claims_df: pd.DataFrame,
                          labs_df: pd.DataFrame,
                          measurement_year: int = 2025) -> Dict[str, Any]:
    """
    Convenience function to calculate KED measure.
    
    Args:
        member_df: Member demographics DataFrame
        claims_df: Claims DataFrame
        labs_df: Labs DataFrame
        measurement_year: Measurement year
        
    Returns:
        Dictionary with measure results
    """
    ked = KEDMeasure(measurement_year)
    results = ked.calculate_measure(member_df, claims_df, labs_df)
    
    return results


if __name__ == "__main__":
    # Example usage
    logger.info("KED - Kidney Health Evaluation for Patients with Diabetes")
    logger.info("NEW 2025 HEDIS Measure - Triple-Weighted")
    logger.info("Value: $360-615K")
    logger.info("")
    logger.info("Denominator: Members 18-75 with diabetes")
    logger.info("Numerator: eGFR + ACR tests in measurement year")
    logger.info("Exclusions: ESRD, kidney transplant")


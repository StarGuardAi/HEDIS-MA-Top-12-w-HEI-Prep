"""
EED (Eye Exam for Patients with Diabetes) HEDIS Measure

This module implements the Eye Exam for Patients with Diabetes measure
according to HEDIS MY2025 specifications.

HEDIS Measure: EED - Eye Exam for Patients with Diabetes
Tier: 1 (Diabetes Core)
Weight: 1x (standard)
Value: $120-205K
HEDIS Specification: MY2025 Volume 2

Denominator: Members age 18-75 with diabetes diagnosis
Numerator: Retinal or dilated eye exam during measurement year
Exclusions: Hospice, advanced illness and frailty

Clinical Importance:
- Diabetic retinopathy is a leading cause of blindness
- Annual eye exams detect early retinopathy changes
- Early treatment prevents vision loss
- Part of comprehensive diabetes management
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Set, Optional, Tuple
from datetime import datetime
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class EEDMeasure:
    """
    Eye Exam for Patients with Diabetes (EED) measure calculator.
    
    HEDIS Specification: MY2025 Volume 2
    Measure Weight: 1x (standard)
    Portfolio Value: $120-205K
    """
    
    # ============================================================================
    # HEDIS CODE SETS (MY2025)
    # ============================================================================
    
    # Diabetes diagnosis codes (ICD-10: E08-E13)
    DIABETES_ICD10 = {
        # E08: Diabetes due to underlying condition
        "E08.00", "E08.01", "E08.10", "E08.11", "E08.21", "E08.22", "E08.29",
        "E08.311", "E08.319", "E08.321", "E08.329", "E08.331", "E08.339",
        "E08.341", "E08.349", "E08.351", "E08.359", "E08.36", "E08.37X1",
        "E08.37X2", "E08.37X3", "E08.37X9", "E08.39", "E08.40", "E08.41",
        "E08.42", "E08.43", "E08.44", "E08.49", "E08.51", "E08.52", "E08.59",
        "E08.610", "E08.618", "E08.620", "E08.621", "E08.622", "E08.628",
        "E08.630", "E08.638", "E08.641", "E08.649", "E08.65", "E08.69", "E08.8",
        
        # E09: Drug or chemical induced diabetes
        "E09.00", "E09.01", "E09.10", "E09.11", "E09.21", "E09.22", "E09.29",
        "E09.311", "E09.319", "E09.321", "E09.329", "E09.331", "E09.339",
        "E09.341", "E09.349", "E09.351", "E09.359", "E09.36", "E09.37X1",
        "E09.37X2", "E09.37X3", "E09.37X9", "E09.39", "E09.40", "E09.41",
        "E09.42", "E09.43", "E09.44", "E09.49", "E09.51", "E09.52", "E09.59",
        "E09.610", "E09.618", "E09.620", "E09.621", "E09.622", "E09.628",
        "E09.630", "E09.638", "E09.641", "E09.649", "E09.65", "E09.69", "E09.8",
        
        # E10: Type 1 diabetes
        "E10.10", "E10.11", "E10.21", "E10.22", "E10.29", "E10.311", "E10.319",
        "E10.321", "E10.329", "E10.331", "E10.339", "E10.341", "E10.349",
        "E10.351", "E10.359", "E10.36", "E10.37X1", "E10.37X2", "E10.37X3",
        "E10.37X9", "E10.39", "E10.40", "E10.41", "E10.42", "E10.43", "E10.44",
        "E10.49", "E10.51", "E10.52", "E10.59", "E10.610", "E10.618", "E10.620",
        "E10.621", "E10.622", "E10.628", "E10.630", "E10.638", "E10.641",
        "E10.649", "E10.65", "E10.69", "E10.8",
        
        # E11: Type 2 diabetes
        "E11.00", "E11.01", "E11.10", "E11.11", "E11.21", "E11.22", "E11.29",
        "E11.311", "E11.319", "E11.321", "E11.329", "E11.331", "E11.339",
        "E11.341", "E11.349", "E11.351", "E11.359", "E11.36", "E11.37X1",
        "E11.37X2", "E11.37X3", "E11.37X9", "E11.39", "E11.40", "E11.41",
        "E11.42", "E11.43", "E11.44", "E11.49", "E11.51", "E11.52", "E11.59",
        "E11.610", "E11.618", "E11.620", "E11.621", "E11.622", "E11.628",
        "E11.630", "E11.638", "E11.641", "E11.649", "E11.65", "E11.69", "E11.8",
        
        # E13: Other specified diabetes
        "E13.00", "E13.01", "E13.10", "E13.11", "E13.21", "E13.22", "E13.29",
        "E13.311", "E13.319", "E13.321", "E13.329", "E13.331", "E13.339",
        "E13.341", "E13.349", "E13.351", "E13.359", "E13.36", "E13.37X1",
        "E13.37X2", "E13.37X3", "E13.37X9", "E13.39", "E13.40", "E13.41",
        "E13.42", "E13.43", "E13.44", "E13.49", "E13.51", "E13.52", "E13.59",
        "E13.610", "E13.618", "E13.620", "E13.621", "E13.622", "E13.628",
        "E13.630", "E13.638", "E13.641", "E13.649", "E13.65", "E13.69", "E13.8",
    }
    
    # Exclusion codes
    HOSPICE_ICD10 = {"Z51.5"}  # Encounter for hospice care
    ADVANCED_ILLNESS_ICD10 = {
        "Z99.11",  # Dependence on respirator
        "Z99.12",  # Dependence on ventilator
    }
    
    # Eye exam procedure codes (CPT/HCPCS)
    EYE_EXAM_CPT = {
        "67028",   # Injection treatment of eye
        "67210",   # Photocoagulation, 1+ sessions
        "67228",   # Treatment of extensive/progressive retinopathy
        "92002",   # Medical exam, new patient
        "92004",   # Medical exam, new patient (comprehensive)
        "92012",   # Medical exam, established patient
        "92014",   # Medical exam, established patient (comprehensive)
        "92018",   # New patient exam under general anesthesia
        "92019",   # Established patient exam under general anesthesia
        "92134",   # Scanning ophthalmic diagnostic imaging (OCT)
        "92225",   # Ophthalmoscopy, extended (with drawings)
        "92226",   # Ophthalmoscopy, extended (with photos)
        "92227",   # Remote imaging (separate billing)
        "92228",   # Remote imaging (unilateral/bilateral)
        "92230",   # Fluorescein angioscopy
        "92235",   # Fluorescein angiography
        "92240",   # ICG angiography
        "92250",   # Fundus photography
    }
    
    EYE_EXAM_HCPCS = {
        "S0620",   # Routine eye exam (with refraction)
        "S0621",   # Comprehensive eye exam (new patient)
        "S3000",   # Diabetic retinopathy screening (non-physician)
    }
    
    def __init__(self, measurement_year: int = 2023):
        """
        Initialize EED measure calculator.
        
        Args:
            measurement_year: Measurement year for calculations (default: 2023)
        """
        self.measurement_year = measurement_year
        self.measurement_year_end = pd.Timestamp(f"{measurement_year}-12-31")
        self.all_eye_exam_codes = self.EYE_EXAM_CPT | self.EYE_EXAM_HCPCS
        
        logger.info("EED measure initialized for measurement year %d", measurement_year)
    
    def calculate_age_at_year_end(self, birth_date: pd.Series) -> pd.Series:
        """
        Calculate age as of December 31 of measurement year.
        
        HEDIS Specification: Age calculated as of December 31 of measurement year.
        """
        birth_date = pd.to_datetime(birth_date, errors="coerce")
        age = (self.measurement_year_end - birth_date).dt.days / 365.25
        return age.astype(int)
    
    def identify_denominator(
        self,
        members_df: pd.DataFrame,
        claims_df: pd.DataFrame
    ) -> pd.DataFrame:
        """
        Identify denominator: Members age 18-75 with diabetes diagnosis.
        
        HEDIS Specification:
        - Age 18-75 as of December 31 of measurement year
        - Diabetes diagnosis (ICD-10: E08-E13) during measurement year or prior
        - Continuous enrollment during measurement year
        
        Args:
            members_df: Member demographics (member_id, birth_date)
            claims_df: Claims with diagnosis codes
            
        Returns:
            DataFrame with denominator members
        """
        # Calculate age
        members_df = members_df.copy()
        members_df["age"] = self.calculate_age_at_year_end(members_df["BENE_BIRTH_DT"])
        
        # Age filter (18-75)
        age_eligible = members_df[
            (members_df["age"] >= 18) & 
            (members_df["age"] <= 75)
        ].copy()
        
        logger.info("Age eligible members (18-75): %d", len(age_eligible))
        
        # Identify members with diabetes diagnosis
        diabetes_members = self._identify_diabetes_members(claims_df)
        
        # Merge to get denominator
        denominator = age_eligible[
            age_eligible["DESYNPUF_ID"].isin(diabetes_members)
        ].copy()
        
        denominator["in_denominator"] = True
        
        logger.info("Denominator (age + diabetes): %d members", len(denominator))
        
        return denominator
    
    def _identify_diabetes_members(self, claims_df: pd.DataFrame) -> Set[str]:
        """
        Identify members with diabetes diagnosis from claims.
        
        Uses ICD-10 codes E08-E13.
        """
        # Find diagnosis columns
        dx_cols = [col for col in claims_df.columns if col.startswith("ICD9_DGNS_CD")]
        
        if not dx_cols:
            logger.warning("No diagnosis columns found in claims")
            return set()
        
        # Check each diagnosis column
        diabetes_members = set()
        for col in dx_cols:
            # Filter by diabetes codes
            diabetes_claims = claims_df[
                claims_df[col].isin(self.DIABETES_ICD10)
            ]
            diabetes_members.update(diabetes_claims["DESYNPUF_ID"].unique())
        
        logger.info("Members with diabetes diagnosis: %d", len(diabetes_members))
        
        return diabetes_members
    
    def apply_exclusions(
        self,
        denominator_df: pd.DataFrame,
        claims_df: pd.DataFrame
    ) -> pd.DataFrame:
        """
        Apply exclusions (hospice, advanced illness).
        
        HEDIS Specification:
        - Hospice care during measurement year (Z51.5)
        - Advanced illness (ventilator dependence)
        
        Args:
            denominator_df: Members in denominator
            claims_df: Claims with diagnosis codes
            
        Returns:
            DataFrame with exclusion flags
        """
        denominator_df = denominator_df.copy()
        
        # Identify excluded members
        excluded_members = self._identify_excluded_members(claims_df)
        
        # Add exclusion flag
        denominator_df["excluded"] = denominator_df["DESYNPUF_ID"].isin(excluded_members)
        
        excluded_count = denominator_df["excluded"].sum()
        logger.info("Excluded members (hospice/advanced illness): %d", excluded_count)
        
        return denominator_df
    
    def _identify_excluded_members(self, claims_df: pd.DataFrame) -> Set[str]:
        """
        Identify members with exclusion criteria.
        """
        exclusion_codes = self.HOSPICE_ICD10 | self.ADVANCED_ILLNESS_ICD10
        
        # Find diagnosis columns
        dx_cols = [col for col in claims_df.columns if col.startswith("ICD9_DGNS_CD")]
        
        excluded_members = set()
        for col in dx_cols:
            excluded_claims = claims_df[
                claims_df[col].isin(exclusion_codes)
            ]
            excluded_members.update(excluded_claims["DESYNPUF_ID"].unique())
        
        return excluded_members
    
    def calculate_numerator(
        self,
        denominator_df: pd.DataFrame,
        procedures_df: pd.DataFrame
    ) -> pd.DataFrame:
        """
        Calculate numerator: Members with eye exam during measurement year.
        
        HEDIS Specification:
        - Retinal or dilated eye exam by eye care professional
        - During measurement year (Jan 1 - Dec 31)
        - Specific CPT/HCPCS codes required
        
        Args:
            denominator_df: Members in denominator (after exclusions)
            procedures_df: Procedures from procedure_loader
            
        Returns:
            DataFrame with numerator compliance flags
        """
        result_df = denominator_df.copy()
        
        # Filter procedures to measurement year
        year_start = pd.Timestamp(f"{self.measurement_year}-01-01")
        year_end = self.measurement_year_end
        
        procedures_df = procedures_df[
            (procedures_df["service_date"] >= year_start) &
            (procedures_df["service_date"] <= year_end)
        ].copy()
        
        # Identify members with eye exams
        members_with_exams = set(procedures_df["member_id"].unique())
        
        # Add compliance flag
        result_df["has_eye_exam"] = result_df["DESYNPUF_ID"].isin(members_with_exams)
        
        # Calculate numerator compliance (not excluded AND has eye exam)
        result_df["numerator_compliant"] = (
            (~result_df["excluded"]) & 
            result_df["has_eye_exam"]
        )
        
        compliant_count = result_df["numerator_compliant"].sum()
        eligible_count = (~result_df["excluded"]).sum()
        
        if eligible_count > 0:
            compliance_rate = (compliant_count / eligible_count) * 100
        else:
            compliance_rate = 0.0
        
        logger.info("Numerator compliant: %d / %d (%.1f%%)",
                   compliant_count, eligible_count, compliance_rate)
        
        return result_df
    
    def calculate_gaps(self, results_df: pd.DataFrame) -> pd.DataFrame:
        """
        Identify gaps (eligible members without eye exam).
        
        Gap = In denominator AND not excluded AND no eye exam
        
        Args:
            results_df: Results from calculate_numerator
            
        Returns:
            DataFrame with gap flags
        """
        results_df = results_df.copy()
        
        # Gap: eligible but not compliant
        results_df["has_gap"] = (
            results_df["in_denominator"] &
            (~results_df["excluded"]) &
            (~results_df["has_eye_exam"])
        )
        
        gap_count = results_df["has_gap"].sum()
        eligible_count = (results_df["in_denominator"] & ~results_df["excluded"]).sum()
        
        if eligible_count > 0:
            gap_rate = (gap_count / eligible_count) * 100
        else:
            gap_rate = 0.0
        
        logger.info("Members with gaps: %d / %d (%.1f%%)",
                   gap_count, eligible_count, gap_rate)
        
        # Add gap description
        results_df["gap_description"] = results_df.apply(
            lambda row: "No eye exam in measurement year" if row["has_gap"] else None,
            axis=1
        )
        
        return results_df
    
    def calculate_measure(
        self,
        members_df: pd.DataFrame,
        claims_df: pd.DataFrame,
        procedures_df: pd.DataFrame
    ) -> Dict:
        """
        Calculate complete EED measure with denominator, numerator, and gaps.
        
        Args:
            members_df: Member demographics
            claims_df: Claims with diagnosis codes
            procedures_df: Eye exam procedures from procedure_loader
            
        Returns:
            Dictionary with:
            - results_df: Member-level results
            - summary: Measure summary statistics
        """
        # Step 1: Identify denominator
        denominator_df = self.identify_denominator(members_df, claims_df)
        
        # Step 2: Apply exclusions
        denominator_df = self.apply_exclusions(denominator_df, claims_df)
        
        # Step 3: Calculate numerator
        results_df = self.calculate_numerator(denominator_df, procedures_df)
        
        # Step 4: Identify gaps
        results_df = self.calculate_gaps(results_df)
        
        # Step 5: Calculate summary statistics
        summary = self._calculate_summary(results_df)
        
        return {
            "results_df": results_df,
            "summary": summary
        }
    
    def _calculate_summary(self, results_df: pd.DataFrame) -> Dict:
        """
        Calculate summary statistics for EED measure.
        """
        denominator_count = results_df["in_denominator"].sum()
        excluded_count = results_df["excluded"].sum()
        eligible_count = denominator_count - excluded_count
        numerator_count = results_df["numerator_compliant"].sum()
        gap_count = results_df["has_gap"].sum()
        
        if eligible_count > 0:
            compliance_rate = (numerator_count / eligible_count) * 100
            gap_rate = (gap_count / eligible_count) * 100
        else:
            compliance_rate = 0.0
            gap_rate = 0.0
        
        summary = {
            "measure": "EED",
            "measure_name": "Eye Exam for Patients with Diabetes",
            "measurement_year": self.measurement_year,
            "denominator": int(denominator_count),
            "exclusions": int(excluded_count),
            "eligible_population": int(eligible_count),
            "numerator": int(numerator_count),
            "gaps": int(gap_count),
            "compliance_rate": round(compliance_rate, 2),
            "gap_rate": round(gap_rate, 2),
        }
        
        logger.info("EED Measure Summary: %s", summary)
        
        return summary

"""
BPD (Blood Pressure Control for Patients with Diabetes) HEDIS Measure

This module implements the Blood Pressure Control for Patients with Diabetes measure
according to HEDIS MY2025 specifications.

HEDIS Measure: BPD - Blood Pressure Control for Patients with Diabetes
Tier: 1 (Diabetes Core)
Weight: 1x (standard)
Value: $120-205K
HEDIS Specification: MY2025 Volume 2 (NEW 2025 MEASURE)

Denominator: Members age 18-75 with diabetes diagnosis
Numerator: Most recent BP <140/90 mmHg during measurement year
Exclusions: Hospice, advanced illness and frailty

Clinical Importance:
- Hypertension is common in diabetes (60-80% prevalence)
- BP control reduces cardiovascular disease risk
- Target <140/90 associated with better outcomes
- Part of comprehensive diabetes management
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Set, Optional
from datetime import datetime
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class BPDMeasure:
    """
    Blood Pressure Control for Patients with Diabetes (BPD) measure calculator.
    
    HEDIS Specification: MY2025 Volume 2 (NEW 2025 MEASURE)
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
        
        # E09: Drug or chemical induced diabetes
        "E09.00", "E09.01", "E09.10", "E09.11", "E09.21", "E09.22", "E09.29",
        "E09.311", "E09.319", "E09.321", "E09.329", "E09.331", "E09.339",
        
        # E10: Type 1 diabetes
        "E10.10", "E10.11", "E10.21", "E10.22", "E10.29", "E10.311", "E10.319",
        "E10.321", "E10.329", "E10.331", "E10.339", "E10.351", "E10.359",
        
        # E11: Type 2 diabetes
        "E11.00", "E11.01", "E11.10", "E11.11", "E11.21", "E11.22", "E11.29",
        "E11.311", "E11.319", "E11.321", "E11.329", "E11.331", "E11.339",
        
        # E13: Other specified diabetes
        "E13.00", "E13.01", "E13.10", "E13.11", "E13.21", "E13.22", "E13.29",
        "E13.311", "E13.319", "E13.321", "E13.329", "E13.331", "E13.339",
    }
    
    # Exclusion codes
    HOSPICE_ICD10 = {"Z51.5"}  # Encounter for hospice care
    ADVANCED_ILLNESS_ICD10 = {
        "Z99.11",  # Dependence on respirator
        "Z99.12",  # Dependence on ventilator
    }
    
    # BP Control thresholds
    BP_SYSTOLIC_THRESHOLD = 140  # <140 mmHg
    BP_DIASTOLIC_THRESHOLD = 90  # <90 mmHg
    
    def __init__(self, measurement_year: int = 2023):
        """
        Initialize BPD measure calculator.
        
        Args:
            measurement_year: Measurement year for calculations (default: 2023)
        """
        self.measurement_year = measurement_year
        self.measurement_year_end = pd.Timestamp(f"{measurement_year}-12-31")
        
        logger.info("BPD measure initialized for measurement year %d (NEW 2025)", measurement_year)
    
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
        """Identify members with exclusion criteria."""
        exclusion_codes = self.HOSPICE_ICD10 | self.ADVANCED_ILLNESS_ICD10
        
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
        bp_summary_df: pd.DataFrame
    ) -> pd.DataFrame:
        """
        Calculate numerator: Members with most recent BP <140/90 mmHg.
        
        HEDIS Specification:
        - Most recent BP reading in measurement year
        - Systolic <140 mmHg AND diastolic <90 mmHg
        - Both thresholds must be met
        
        Args:
            denominator_df: Members in denominator (after exclusions)
            bp_summary_df: BP summary from vitals_loader
            
        Returns:
            DataFrame with numerator compliance flags
        """
        result_df = denominator_df.copy()
        
        # Create member_id to BP control mapping
        bp_dict = bp_summary_df.set_index("member_id")["most_recent_controlled"].to_dict()
        systolic_dict = bp_summary_df.set_index("member_id")["most_recent_systolic"].to_dict()
        diastolic_dict = bp_summary_df.set_index("member_id")["most_recent_diastolic"].to_dict()
        
        # Add BP values
        result_df["has_bp_reading"] = result_df["DESYNPUF_ID"].isin(bp_summary_df["member_id"])
        result_df["bp_controlled"] = result_df["DESYNPUF_ID"].map(bp_dict).fillna(False)
        result_df["most_recent_systolic"] = result_df["DESYNPUF_ID"].map(systolic_dict)
        result_df["most_recent_diastolic"] = result_df["DESYNPUF_ID"].map(diastolic_dict)
        
        # Calculate numerator compliance (not excluded AND BP controlled)
        result_df["numerator_compliant"] = (
            (~result_df["excluded"]) & 
            result_df["has_bp_reading"] &
            result_df["bp_controlled"]
        )
        
        compliant_count = result_df["numerator_compliant"].sum()
        eligible_count = (~result_df["excluded"]).sum()
        
        if eligible_count > 0:
            compliance_rate = (compliant_count / eligible_count) * 100
        else:
            compliance_rate = 0.0
        
        logger.info("Numerator compliant (BP <140/90): %d / %d (%.1f%%)",
                   compliant_count, eligible_count, compliance_rate)
        
        return result_df
    
    def calculate_gaps(self, results_df: pd.DataFrame) -> pd.DataFrame:
        """
        Identify gaps (eligible members with uncontrolled BP or no BP reading).
        
        Gap = In denominator AND not excluded AND (no BP reading OR BP ≥140/90)
        
        Args:
            results_df: Results from calculate_numerator
            
        Returns:
            DataFrame with gap flags
        """
        results_df = results_df.copy()
        
        # Gap: eligible but not controlled
        results_df["has_gap"] = (
            results_df["in_denominator"] &
            (~results_df["excluded"]) &
            (~results_df["numerator_compliant"])
        )
        
        gap_count = results_df["has_gap"].sum()
        eligible_count = (results_df["in_denominator"] & ~results_df["excluded"]).sum()
        
        if eligible_count > 0:
            gap_rate = (gap_count / eligible_count) * 100
        else:
            gap_rate = 0.0
        
        logger.info("Members with gaps: %d / %d (%.1f%%)",
                   gap_count, eligible_count, gap_rate)
        
        # Add gap description with actual BP values
        def gap_desc(row):
            if not row["has_gap"]:
                return None
            if not row["has_bp_reading"]:
                return "No BP reading in measurement year"
            if pd.notna(row["most_recent_systolic"]) and pd.notna(row["most_recent_diastolic"]):
                return f"BP {int(row['most_recent_systolic'])}/{int(row['most_recent_diastolic'])} (≥140/90)"
            return "Uncontrolled BP"
        
        results_df["gap_description"] = results_df.apply(gap_desc, axis=1)
        
        return results_df
    
    def calculate_measure(
        self,
        members_df: pd.DataFrame,
        claims_df: pd.DataFrame,
        bp_summary_df: pd.DataFrame
    ) -> Dict:
        """
        Calculate complete BPD measure.
        
        Args:
            members_df: Member demographics
            claims_df: Claims with diagnosis codes
            bp_summary_df: BP summary from vitals_loader
            
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
        results_df = self.calculate_numerator(denominator_df, bp_summary_df)
        
        # Step 4: Identify gaps
        results_df = self.calculate_gaps(results_df)
        
        # Step 5: Calculate summary statistics
        summary = self._calculate_summary(results_df)
        
        return {
            "results_df": results_df,
            "summary": summary
        }
    
    def _calculate_summary(self, results_df: pd.DataFrame) -> Dict:
        """Calculate summary statistics for BPD measure."""
        denominator_count = results_df["in_denominator"].sum()
        excluded_count = results_df["excluded"].sum()
        eligible_count = denominator_count - excluded_count
        numerator_count = results_df["numerator_compliant"].sum()
        gap_count = results_df["has_gap"].sum()
        
        # Average BP for eligible members with readings
        eligible_with_bp = results_df[
            (~results_df["excluded"]) & 
            results_df["has_bp_reading"]
        ]
        
        if len(eligible_with_bp) > 0:
            avg_systolic = eligible_with_bp["most_recent_systolic"].mean()
            avg_diastolic = eligible_with_bp["most_recent_diastolic"].mean()
        else:
            avg_systolic = None
            avg_diastolic = None
        
        if eligible_count > 0:
            compliance_rate = (numerator_count / eligible_count) * 100
            gap_rate = (gap_count / eligible_count) * 100
        else:
            compliance_rate = 0.0
            gap_rate = 0.0
        
        summary = {
            "measure": "BPD",
            "measure_name": "Blood Pressure Control for Patients with Diabetes",
            "measurement_year": self.measurement_year,
            "new_2025_measure": True,
            "denominator": int(denominator_count),
            "exclusions": int(excluded_count),
            "eligible_population": int(eligible_count),
            "numerator": int(numerator_count),
            "gaps": int(gap_count),
            "compliance_rate": round(compliance_rate, 2),
            "gap_rate": round(gap_rate, 2),
            "bp_threshold": f"<{self.BP_SYSTOLIC_THRESHOLD}/{self.BP_DIASTOLIC_THRESHOLD}",
            "avg_systolic_bp": round(avg_systolic, 1) if avg_systolic else None,
            "avg_diastolic_bp": round(avg_diastolic, 1) if avg_diastolic else None,
        }
        
        logger.info("BPD Measure Summary: %s", summary)
        
        return summary

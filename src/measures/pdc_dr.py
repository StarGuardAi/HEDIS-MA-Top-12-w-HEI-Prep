"""
PDC-DR (Medication Adherence for Diabetes) HEDIS Measure

This module implements the Medication Adherence for Diabetes Medications measure
according to HEDIS MY2025 specifications.

HEDIS Measure: PDC-DR - Medication Adherence for Diabetes Medications
Tier: 1 (Diabetes Core)
Weight: 1x (standard)
Value: $120-205K
HEDIS Specification: MY2025 Volume 2

Denominator: Members age 18-75 with diabetes on diabetes medications (2+ fills)
Numerator: PDC ≥ 80% (proportion of days covered)
Exclusions: Hospice, advanced illness and frailty

Clinical Importance:
- Medication adherence is critical for diabetes control
- Non-adherence leads to poor outcomes and complications
- 80% PDC threshold associated with better clinical outcomes
- Cost-effective intervention point
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Set, Optional
from datetime import datetime
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class PDCDRMeasure:
    """
    Medication Adherence for Diabetes (PDC-DR) measure calculator.
    
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
    
    # PDC threshold for adherence
    PDC_THRESHOLD = 0.80
    
    def __init__(self, measurement_year: int = 2023):
        """
        Initialize PDC-DR measure calculator.
        
        Args:
            measurement_year: Measurement year for calculations (default: 2023)
        """
        self.measurement_year = measurement_year
        self.measurement_year_end = pd.Timestamp(f"{measurement_year}-12-31")
        
        logger.info("PDC-DR measure initialized for measurement year %d", measurement_year)
    
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
        claims_df: pd.DataFrame,
        pdc_df: pd.DataFrame
    ) -> pd.DataFrame:
        """
        Identify denominator: Members age 18-75 with diabetes on medications (2+ fills).
        
        HEDIS Specification:
        - Age 18-75 as of December 31 of measurement year
        - Diabetes diagnosis (ICD-10: E08-E13)
        - At least 2 fills of diabetes medications during measurement year
        - Continuous enrollment
        
        Args:
            members_df: Member demographics (member_id, birth_date)
            claims_df: Claims with diagnosis codes
            pdc_df: PDC calculations from pharmacy_loader
            
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
        
        # Members with 2+ diabetes medication fills (from PDC calculation)
        on_medications = set(pdc_df["member_id"].unique())
        
        # Denominator = Age eligible + diabetes + on medications
        denominator = age_eligible[
            age_eligible["DESYNPUF_ID"].isin(diabetes_members) &
            age_eligible["DESYNPUF_ID"].isin(on_medications)
        ].copy()
        
        denominator["in_denominator"] = True
        
        logger.info("Denominator (age + diabetes + on meds): %d members", len(denominator))
        
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
        pdc_df: pd.DataFrame
    ) -> pd.DataFrame:
        """
        Calculate numerator: Members with PDC ≥ 80%.
        
        HEDIS Specification:
        - PDC (Proportion of Days Covered) ≥ 0.80
        - Treatment period: First fill to end of measurement year
        - Handle overlapping fills correctly
        
        Args:
            denominator_df: Members in denominator (after exclusions)
            pdc_df: PDC calculations from pharmacy_loader
            
        Returns:
            DataFrame with numerator compliance flags
        """
        result_df = denominator_df.copy()
        
        # Create member_id to PDC mapping
        pdc_dict = pdc_df.set_index("member_id")["pdc"].to_dict()
        adherent_dict = pdc_df.set_index("member_id")["adherent"].to_dict()
        
        # Add PDC values
        result_df["pdc"] = result_df["DESYNPUF_ID"].map(pdc_dict).fillna(0.0)
        result_df["is_adherent"] = result_df["DESYNPUF_ID"].map(adherent_dict).fillna(False)
        
        # Calculate numerator compliance (not excluded AND adherent)
        result_df["numerator_compliant"] = (
            (~result_df["excluded"]) & 
            result_df["is_adherent"]
        )
        
        compliant_count = result_df["numerator_compliant"].sum()
        eligible_count = (~result_df["excluded"]).sum()
        
        if eligible_count > 0:
            compliance_rate = (compliant_count / eligible_count) * 100
        else:
            compliance_rate = 0.0
        
        logger.info("Numerator compliant (PDC ≥80%%): %d / %d (%.1f%%)",
                   compliant_count, eligible_count, compliance_rate)
        
        return result_df
    
    def calculate_gaps(self, results_df: pd.DataFrame) -> pd.DataFrame:
        """
        Identify gaps (eligible members with PDC < 80%).
        
        Gap = In denominator AND not excluded AND PDC < 80%
        
        Args:
            results_df: Results from calculate_numerator
            
        Returns:
            DataFrame with gap flags
        """
        results_df = results_df.copy()
        
        # Gap: eligible but not adherent
        results_df["has_gap"] = (
            results_df["in_denominator"] &
            (~results_df["excluded"]) &
            (~results_df["is_adherent"])
        )
        
        gap_count = results_df["has_gap"].sum()
        eligible_count = (results_df["in_denominator"] & ~results_df["excluded"]).sum()
        
        if eligible_count > 0:
            gap_rate = (gap_count / eligible_count) * 100
        else:
            gap_rate = 0.0
        
        logger.info("Members with gaps: %d / %d (%.1f%%)",
                   gap_count, eligible_count, gap_rate)
        
        # Add gap description with actual PDC value
        def gap_desc(row):
            if row["has_gap"]:
                return f"PDC {row['pdc']:.1%} (below 80% threshold)"
            return None
        
        results_df["gap_description"] = results_df.apply(gap_desc, axis=1)
        
        return results_df
    
    def calculate_measure(
        self,
        members_df: pd.DataFrame,
        claims_df: pd.DataFrame,
        pdc_df: pd.DataFrame
    ) -> Dict:
        """
        Calculate complete PDC-DR measure.
        
        Args:
            members_df: Member demographics
            claims_df: Claims with diagnosis codes
            pdc_df: PDC calculations from pharmacy_loader
            
        Returns:
            Dictionary with:
            - results_df: Member-level results
            - summary: Measure summary statistics
        """
        # Step 1: Identify denominator
        denominator_df = self.identify_denominator(members_df, claims_df, pdc_df)
        
        # Step 2: Apply exclusions
        denominator_df = self.apply_exclusions(denominator_df, claims_df)
        
        # Step 3: Calculate numerator
        results_df = self.calculate_numerator(denominator_df, pdc_df)
        
        # Step 4: Identify gaps
        results_df = self.calculate_gaps(results_df)
        
        # Step 5: Calculate summary statistics
        summary = self._calculate_summary(results_df)
        
        return {
            "results_df": results_df,
            "summary": summary
        }
    
    def _calculate_summary(self, results_df: pd.DataFrame) -> Dict:
        """Calculate summary statistics for PDC-DR measure."""
        denominator_count = results_df["in_denominator"].sum()
        excluded_count = results_df["excluded"].sum()
        eligible_count = denominator_count - excluded_count
        numerator_count = results_df["numerator_compliant"].sum()
        gap_count = results_df["has_gap"].sum()
        
        if eligible_count > 0:
            compliance_rate = (numerator_count / eligible_count) * 100
            gap_rate = (gap_count / eligible_count) * 100
            avg_pdc = results_df[~results_df["excluded"]]["pdc"].mean() * 100
        else:
            compliance_rate = 0.0
            gap_rate = 0.0
            avg_pdc = 0.0
        
        summary = {
            "measure": "PDC-DR",
            "measure_name": "Medication Adherence for Diabetes Medications",
            "measurement_year": self.measurement_year,
            "denominator": int(denominator_count),
            "exclusions": int(excluded_count),
            "eligible_population": int(eligible_count),
            "numerator": int(numerator_count),
            "gaps": int(gap_count),
            "compliance_rate": round(compliance_rate, 2),
            "gap_rate": round(gap_rate, 2),
            "avg_pdc": round(avg_pdc, 2),
            "pdc_threshold": self.PDC_THRESHOLD,
        }
        
        logger.info("PDC-DR Measure Summary: %s", summary)
        
        return summary

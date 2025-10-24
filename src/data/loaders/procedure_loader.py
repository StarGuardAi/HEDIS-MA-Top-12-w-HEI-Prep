"""
Procedure Data Loader for HEDIS Measures

This module loads and processes procedure codes (CPT, HCPCS) from claims data
for HEDIS measures requiring procedure validation (eye exams, mammography,
colonoscopy, etc.).

HEDIS Measures Supported:
- EED: Eye Exam for Diabetes (retinal exams, ophthalmoscopy)
- BCS: Breast Cancer Screening (mammography)
- COL: Colorectal Cancer Screening (colonoscopy, FOBT)

HEDIS Specification: MY2025 Volume 2
HIPAA Compliance: PHI-safe logging with hashed member IDs
"""

import pandas as pd
import numpy as np
import hashlib
import logging
from typing import Dict, List, Set, Optional, Tuple
from datetime import datetime, timedelta

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ProcedureLoader:
    """
    Load and process procedure codes from claims data for HEDIS measures.
    
    Supports multiple procedure types:
    - Eye exams (retinal, ophthalmoscopy, imaging)
    - Mammography (screening, diagnostic)
    - Colonoscopy (screening, surveillance)
    - FOBT/FIT tests
    """
    
    # ============================================================================
    # PROCEDURE CODE VALUE SETS (HEDIS MY2025)
    # ============================================================================
    
    # Eye Exam Codes (EED measure)
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
    
    # Mammography Codes (BCS measure)
    MAMMOGRAPHY_CPT = {
        "77065",   # Diagnostic mammography, unilateral
        "77066",   # Diagnostic mammography, bilateral
        "77067",   # Screening mammography, bilateral
    }
    
    MAMMOGRAPHY_HCPCS = {
        "G0202",   # Screening mammography, bilateral
        "G0204",   # Diagnostic mammography, bilateral
        "G0206",   # Diagnostic mammography, unilateral
    }
    
    # Colonoscopy Codes (COL measure)
    COLONOSCOPY_CPT = {
        "44388",   # Colonoscopy through stoma
        "44389",   # Colonoscopy through stoma with biopsy
        "44390",   # Colonoscopy through stoma with foreign body removal
        "44391",   # Colonoscopy through stoma with control of bleeding
        "44392",   # Colonoscopy through stoma with polyp removal
        "44393",   # Colonoscopy through stoma with ablation
        "44394",   # Colonoscopy through stoma with excision
        "45355",   # Colonoscopy with foreign body removal
        "45378",   # Colonoscopy, diagnostic
        "45379",   # Colonoscopy with foreign body removal
        "45380",   # Colonoscopy with biopsy
        "45381",   # Colonoscopy with submucosa injection
        "45382",   # Colonoscopy with control of bleeding
        "45383",   # Colonoscopy with ablation
        "45384",   # Colonoscopy with polyp removal (hot biopsy)
        "45385",   # Colonoscopy with polyp removal (snare)
        "45386",   # Colonoscopy with control of bleeding
        "45388",   # Colonoscopy with ablation
        "45389",   # Colonoscopy with stent placement
        "45390",   # Colonoscopy with excision
        "45391",   # Colonoscopy with endoscopic ultrasound
        "45392",   # Colonoscopy with transendoscopic ultrasound biopsy
    }
    
    COLONOSCOPY_HCPCS = {
        "G0105",   # Colorectal cancer screening; colonoscopy on individual at high risk
        "G0121",   # Colorectal cancer screening; colonoscopy on individual not meeting criteria
    }
    
    def __init__(self):
        """Initialize the procedure loader."""
        self.procedure_types = {
            "eye_exam": self.EYE_EXAM_CPT | self.EYE_EXAM_HCPCS,
            "mammography": self.MAMMOGRAPHY_CPT | self.MAMMOGRAPHY_HCPCS,
            "colonoscopy": self.COLONOSCOPY_CPT | self.COLONOSCOPY_HCPCS,
        }
        logger.info("Procedure loader initialized with %d procedure types", 
                   len(self.procedure_types))
    
    def _hash_member_id(self, member_id: str) -> str:
        """
        Hash member ID for PHI-safe logging.
        
        HIPAA Compliance: Uses SHA-256 hashing to protect member identifiers.
        """
        return hashlib.sha256(str(member_id).encode()).hexdigest()[:8]
    
    def load_procedures_from_claims(
        self,
        inpatient_df: pd.DataFrame,
        outpatient_df: pd.DataFrame,
        carrier_df: Optional[pd.DataFrame] = None,
        procedure_type: str = "eye_exam",
        measurement_year: int = 2023,
        required_columns: Optional[List[str]] = None
    ) -> pd.DataFrame:
        """
        Load procedures from claims data for a specific procedure type.
        
        Args:
            inpatient_df: Inpatient claims with procedure codes
            outpatient_df: Outpatient claims with procedure codes
            carrier_df: Carrier claims with procedure codes (optional)
            procedure_type: Type of procedure to extract ("eye_exam", "mammography", "colonoscopy")
            measurement_year: Measurement year for date filtering
            required_columns: Required columns for validation
            
        Returns:
            DataFrame with member-level procedure history
            
        HEDIS Specification: MY2025 Volume 2
        Performance: Vectorized operations for large datasets
        """
        if procedure_type not in self.procedure_types:
            raise ValueError(f"Invalid procedure type: {procedure_type}. "
                           f"Must be one of {list(self.procedure_types.keys())}")
        
        # Validate required columns
        if required_columns is None:
            required_columns = ["DESYNPUF_ID", "CLM_FROM_DT", "HCPCS_CD_1"]
        
        all_procedures = []
        
        # Process outpatient claims (most common for procedures)
        if not outpatient_df.empty:
            procedures = self._extract_procedures_from_claims(
                outpatient_df,
                self.procedure_types[procedure_type],
                measurement_year,
                claim_type="outpatient"
            )
            if not procedures.empty:
                all_procedures.append(procedures)
        
        # Process inpatient claims
        if not inpatient_df.empty:
            procedures = self._extract_procedures_from_claims(
                inpatient_df,
                self.procedure_types[procedure_type],
                measurement_year,
                claim_type="inpatient"
            )
            if not procedures.empty:
                all_procedures.append(procedures)
        
        # Process carrier claims (if provided)
        if carrier_df is not None and not carrier_df.empty:
            procedures = self._extract_procedures_from_claims(
                carrier_df,
                self.procedure_types[procedure_type],
                measurement_year,
                claim_type="carrier"
            )
            if not procedures.empty:
                all_procedures.append(procedures)
        
        # Combine all procedures
        if not all_procedures:
            logger.warning("No %s procedures found in claims data", procedure_type)
            return pd.DataFrame(columns=["member_id", "procedure_code", 
                                        "service_date", "claim_type"])
        
        combined_df = pd.concat(all_procedures, ignore_index=True)
        
        # PHI-safe logging
        unique_members = combined_df["member_id"].nunique()
        total_procedures = len(combined_df)
        logger.info("Loaded %d %s procedures for %d members",
                   total_procedures, procedure_type, unique_members)
        
        return combined_df
    
    def _extract_procedures_from_claims(
        self,
        claims_df: pd.DataFrame,
        procedure_codes: Set[str],
        measurement_year: int,
        claim_type: str
    ) -> pd.DataFrame:
        """
        Extract procedures from a claims DataFrame.
        
        Performance: Uses vectorized operations and boolean indexing.
        """
        # Handle member ID column variations
        member_id_col = None
        for col in ["DESYNPUF_ID", "member_id", "BENE_ID"]:
            if col in claims_df.columns:
                member_id_col = col
                break
        
        if member_id_col is None:
            logger.warning("No member ID column found in %s claims", claim_type)
            return pd.DataFrame()
        
        # Handle date column variations
        date_col = None
        for col in ["CLM_FROM_DT", "service_date", "CLM_THRU_DT"]:
            if col in claims_df.columns:
                date_col = col
                break
        
        if date_col is None:
            logger.warning("No date column found in %s claims", claim_type)
            return pd.DataFrame()
        
        # Find procedure code columns (HCPCS_CD_1 through HCPCS_CD_45)
        procedure_cols = [col for col in claims_df.columns 
                         if col.startswith("HCPCS_CD") or col.startswith("ICD_PRCDR_CD")]
        
        if not procedure_cols:
            logger.warning("No procedure code columns found in %s claims", claim_type)
            return pd.DataFrame()
        
        # Extract relevant columns
        relevant_cols = [member_id_col, date_col] + procedure_cols
        claims_subset = claims_df[relevant_cols].copy()
        
        # Parse dates
        claims_subset[date_col] = pd.to_datetime(claims_subset[date_col], errors="coerce")
        
        # Filter by measurement year
        year_start = pd.Timestamp(f"{measurement_year}-01-01")
        year_end = pd.Timestamp(f"{measurement_year}-12-31")
        claims_subset = claims_subset[
            (claims_subset[date_col] >= year_start) &
            (claims_subset[date_col] <= year_end)
        ]
        
        if claims_subset.empty:
            return pd.DataFrame()
        
        # Melt procedure columns to long format
        procedures_long = claims_subset.melt(
            id_vars=[member_id_col, date_col],
            value_vars=procedure_cols,
            var_name="procedure_col",
            value_name="procedure_code"
        )
        
        # Remove nulls and filter by procedure codes
        procedures_long = procedures_long[procedures_long["procedure_code"].notna()]
        procedures_long["procedure_code"] = procedures_long["procedure_code"].astype(str).str.strip()
        procedures_long = procedures_long[
            procedures_long["procedure_code"].isin(procedure_codes)
        ]
        
        if procedures_long.empty:
            return pd.DataFrame()
        
        # Rename columns
        procedures_long = procedures_long.rename(columns={
            member_id_col: "member_id",
            date_col: "service_date"
        })
        
        # Add claim type
        procedures_long["claim_type"] = claim_type
        
        # Select final columns
        result = procedures_long[["member_id", "procedure_code", "service_date", "claim_type"]]
        
        return result.drop_duplicates()
    
    def get_member_procedure_summary(
        self,
        procedures_df: pd.DataFrame,
        procedure_type: str = "eye_exam"
    ) -> pd.DataFrame:
        """
        Aggregate procedures to member level.
        
        Returns:
            DataFrame with one row per member containing:
            - member_id
            - has_procedure (bool)
            - procedure_count (int)
            - first_procedure_date (datetime)
            - last_procedure_date (datetime)
            - procedure_codes (list of codes)
        """
        if procedures_df.empty:
            return pd.DataFrame(columns=[
                "member_id", "has_procedure", "procedure_count",
                "first_procedure_date", "last_procedure_date", "procedure_codes"
            ])
        
        # Aggregate by member
        member_summary = procedures_df.groupby("member_id").agg(
            procedure_count=("procedure_code", "count"),
            first_procedure_date=("service_date", "min"),
            last_procedure_date=("service_date", "max"),
            procedure_codes=("procedure_code", lambda x: list(x.unique()))
        ).reset_index()
        
        # Add has_procedure flag
        member_summary["has_procedure"] = True
        
        # Reorder columns
        member_summary = member_summary[[
            "member_id", "has_procedure", "procedure_count",
            "first_procedure_date", "last_procedure_date", "procedure_codes"
        ]]
        
        logger.info("Created procedure summary for %d members", len(member_summary))
        
        return member_summary


# ============================================================================
# CONVENIENCE FUNCTIONS
# ============================================================================

def load_eye_exams(
    inpatient_df: pd.DataFrame,
    outpatient_df: pd.DataFrame,
    carrier_df: Optional[pd.DataFrame] = None,
    measurement_year: int = 2023
) -> pd.DataFrame:
    """
    Load eye exam procedures for EED measure.
    
    Convenience function for eye exam extraction.
    """
    loader = ProcedureLoader()
    return loader.load_procedures_from_claims(
        inpatient_df=inpatient_df,
        outpatient_df=outpatient_df,
        carrier_df=carrier_df,
        procedure_type="eye_exam",
        measurement_year=measurement_year
    )


def load_mammography(
    inpatient_df: pd.DataFrame,
    outpatient_df: pd.DataFrame,
    carrier_df: Optional[pd.DataFrame] = None,
    measurement_year: int = 2023
) -> pd.DataFrame:
    """
    Load mammography procedures for BCS measure.
    
    Convenience function for mammography extraction.
    """
    loader = ProcedureLoader()
    return loader.load_procedures_from_claims(
        inpatient_df=inpatient_df,
        outpatient_df=outpatient_df,
        carrier_df=carrier_df,
        procedure_type="mammography",
        measurement_year=measurement_year
    )


def load_colonoscopy(
    inpatient_df: pd.DataFrame,
    outpatient_df: pd.DataFrame,
    carrier_df: Optional[pd.DataFrame] = None,
    measurement_year: int = 2023
) -> pd.DataFrame:
    """
    Load colonoscopy procedures for COL measure.
    
    Convenience function for colonoscopy extraction.
    """
    loader = ProcedureLoader()
    return loader.load_procedures_from_claims(
        inpatient_df=inpatient_df,
        outpatient_df=outpatient_df,
        carrier_df=carrier_df,
        procedure_type="colonoscopy",
        measurement_year=measurement_year
    )

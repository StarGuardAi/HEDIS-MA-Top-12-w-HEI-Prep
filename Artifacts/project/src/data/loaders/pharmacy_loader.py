"""
Pharmacy Data Loader for HEDIS Medication Adherence Measures

This module loads and processes pharmacy claims data for HEDIS medication
adherence measures (PDC calculations).

HEDIS Measures Supported:
- PDC-DR: Medication Adherence for Diabetes Medications
- PDC-STA: Medication Adherence for Statins
- PDC-RASA: Medication Adherence for RAS Antagonists

PDC Calculation: Proportion of Days Covered
- Days with medication on hand / Total days in measurement period
- Treatment period: First fill to end of measurement year
- Threshold: ≥80% (0.80) for adherence

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


class PharmacyLoader:
    """
    Load and process pharmacy claims for medication adherence measures.
    
    Calculates Proportion of Days Covered (PDC) for medication classes:
    - Diabetes medications (oral hypoglycemics, insulins)
    - Statins (cholesterol medications)
    - RAS antagonists (ACE inhibitors, ARBs)
    """
    
    # ============================================================================
    # MEDICATION NDC CODE SETS (HEDIS MY2025)
    # ============================================================================
    
    # Diabetes Medications (simplified subset - full list from NCQA value sets)
    DIABETES_MEDICATIONS = {
        # Metformin
        "00093315601", "00093315605", "00378018593", "00378018605",
        
        # Glipizide
        "00093074601", "00093074705", "00378015401", "00378015405",
        
        # Glyburide
        "00093511701", "00093511705", "00378015501", "00378015505",
        
        # Insulin (various types)
        "00002825559", "00002825759", "00002882559", "00002882759",
        "00169183811", "00169183911", "00169760311", "00169760411",
        
        # Newer agents (DPP-4 inhibitors, GLP-1 agonists, SGLT2 inhibitors)
        "00002114501", "00002114502", "00025186514", "00025186515",
    }
    
    # Statin Medications
    STATIN_MEDICATIONS = {
        # Atorvastatin (Lipitor)
        "00071015523", "00071015623", "00071015723", "00071015823",
        
        # Simvastatin (Zocor)
        "00006074028", "00006074128", "00006074228", "00006074328",
        
        # Rosuvastatin (Crestor)
        "00310070503", "00310070603", "00310070703", "00310070803",
    }
    
    # RAS Antagonists (ACE Inhibitors and ARBs)
    RASA_MEDICATIONS = {
        # Lisinopril (ACE inhibitor)
        "00378018793", "00378018893", "00378018993", "00378019093",
        
        # Losartan (ARB)
        "00006096228", "00006096328", "00006096428", "00006096528",
        
        # Valsartan (ARB)
        "00078050515", "00078050615", "00078050715", "00078050815",
    }
    
    def __init__(self):
        """Initialize the pharmacy loader."""
        self.medication_classes = {
            "diabetes": self.DIABETES_MEDICATIONS,
            "statin": self.STATIN_MEDICATIONS,
            "rasa": self.RASA_MEDICATIONS,
        }
        logger.info("Pharmacy loader initialized with %d medication classes", 
                   len(self.medication_classes))
    
    def _hash_member_id(self, member_id: str) -> str:
        """
        Hash member ID for PHI-safe logging.
        
        HIPAA Compliance: Uses SHA-256 hashing to protect member identifiers.
        """
        return hashlib.sha256(str(member_id).encode()).hexdigest()[:8]
    
    def load_pharmacy_claims(
        self,
        pharmacy_df: pd.DataFrame,
        medication_class: str = "diabetes",
        measurement_year: int = 2023
    ) -> pd.DataFrame:
        """
        Load pharmacy claims for a specific medication class.
        
        Args:
            pharmacy_df: Pharmacy claims with NDC codes and fill dates
            medication_class: Type of medication ("diabetes", "statin", "rasa")
            measurement_year: Measurement year for date filtering
            
        Returns:
            DataFrame with pharmacy fills:
            - member_id
            - ndc_code
            - fill_date
            - days_supply
            - quantity
            
        HEDIS Specification: MY2025 Volume 2
        Performance: Vectorized operations for large datasets
        """
        if medication_class not in self.medication_classes:
            raise ValueError(f"Invalid medication class: {medication_class}. "
                           f"Must be one of {list(self.medication_classes.keys())}")
        
        # Get medication codes
        medication_codes = self.medication_classes[medication_class]
        
        # Extract relevant columns
        required_cols = {
            "member_id": ["DESYNPUF_ID", "member_id", "BENE_ID"],
            "ndc_code": ["PROD_SRVC_ID", "ndc_code", "NDC"],
            "fill_date": ["SRVC_DT", "fill_date", "service_date"],
            "days_supply": ["QTY_DSPNSD_NUM", "days_supply", "quantity"],
        }
        
        # Map column names
        col_mapping = {}
        for standard_name, possible_names in required_cols.items():
            for col_name in possible_names:
                if col_name in pharmacy_df.columns:
                    col_mapping[col_name] = standard_name
                    break
        
        if len(col_mapping) < 3:  # Need at least member_id, ndc_code, fill_date
            logger.warning("Missing required pharmacy columns")
            return pd.DataFrame(columns=["member_id", "ndc_code", "fill_date", "days_supply"])
        
        # Select and rename columns
        pharmacy_subset = pharmacy_df[list(col_mapping.keys())].copy()
        pharmacy_subset = pharmacy_subset.rename(columns=col_mapping)
        
        # Add days_supply if missing (default to 30 days)
        if "days_supply" not in pharmacy_subset.columns:
            pharmacy_subset["days_supply"] = 30
            logger.info("days_supply column missing, defaulting to 30 days")
        
        # Clean NDC codes (remove dashes, spaces)
        pharmacy_subset["ndc_code"] = (
            pharmacy_subset["ndc_code"]
            .astype(str)
            .str.replace("-", "", regex=False)
            .str.replace(" ", "", regex=False)
            .str.strip()
        )
        
        # Filter by medication class
        pharmacy_subset = pharmacy_subset[
            pharmacy_subset["ndc_code"].isin(medication_codes)
        ]
        
        if pharmacy_subset.empty:
            logger.warning("No %s medications found in pharmacy claims", medication_class)
            return pd.DataFrame(columns=["member_id", "ndc_code", "fill_date", "days_supply"])
        
        # Parse fill dates
        pharmacy_subset["fill_date"] = pd.to_datetime(
            pharmacy_subset["fill_date"], 
            errors="coerce"
        )
        
        # Filter by measurement year (and prior year for lookback)
        year_start = pd.Timestamp(f"{measurement_year - 1}-01-01")
        year_end = pd.Timestamp(f"{measurement_year}-12-31")
        pharmacy_subset = pharmacy_subset[
            (pharmacy_subset["fill_date"] >= year_start) &
            (pharmacy_subset["fill_date"] <= year_end)
        ]
        
        # Convert days_supply to numeric
        pharmacy_subset["days_supply"] = pd.to_numeric(
            pharmacy_subset["days_supply"], 
            errors="coerce"
        ).fillna(30)
        
        # Remove duplicates
        pharmacy_subset = pharmacy_subset.drop_duplicates()
        
        # Sort by member and fill date
        pharmacy_subset = pharmacy_subset.sort_values(["member_id", "fill_date"])
        
        # PHI-safe logging
        unique_members = pharmacy_subset["member_id"].nunique()
        total_fills = len(pharmacy_subset)
        logger.info("Loaded %d %s fills for %d members",
                   total_fills, medication_class, unique_members)
        
        return pharmacy_subset
    
    def calculate_pdc(
        self,
        fills_df: pd.DataFrame,
        measurement_year: int = 2023,
        min_fills: int = 2
    ) -> pd.DataFrame:
        """
        Calculate Proportion of Days Covered (PDC) for each member.
        
        PDC Methodology:
        1. Treatment period = First fill date to December 31 of measurement year
        2. Calculate days covered (accounting for overlapping fills)
        3. PDC = Days covered / Treatment period days
        4. Adherent if PDC ≥ 0.80
        
        Args:
            fills_df: Pharmacy fills from load_pharmacy_claims()
            measurement_year: Measurement year
            min_fills: Minimum fills required (default: 2)
            
        Returns:
            DataFrame with member-level PDC:
            - member_id
            - fill_count
            - first_fill_date
            - last_fill_date
            - treatment_days
            - days_covered
            - pdc
            - adherent (bool, PDC ≥ 0.80)
            
        HEDIS Specification: MY2025 Volume 2
        """
        if fills_df.empty:
            return pd.DataFrame(columns=[
                "member_id", "fill_count", "first_fill_date", "last_fill_date",
                "treatment_days", "days_covered", "pdc", "adherent"
            ])
        
        measurement_year_end = pd.Timestamp(f"{measurement_year}-12-31")
        
        # Group by member
        member_pdcs = []
        
        for member_id, member_fills in fills_df.groupby("member_id"):
            # Sort by fill date
            member_fills = member_fills.sort_values("fill_date")
            
            # Check minimum fills
            fill_count = len(member_fills)
            if fill_count < min_fills:
                continue
            
            # Treatment period
            first_fill_date = member_fills["fill_date"].min()
            last_fill_date = member_fills["fill_date"].max()
            
            # Treatment days = First fill to end of measurement year
            treatment_end = min(measurement_year_end, measurement_year_end)
            treatment_days = (treatment_end - first_fill_date).days + 1
            
            if treatment_days <= 0:
                continue
            
            # Calculate days covered (handle overlapping fills)
            covered_dates = set()
            
            for _, fill in member_fills.iterrows():
                fill_date = fill["fill_date"]
                days_supply = int(fill["days_supply"])
                
                # Add each day covered by this fill
                for day_offset in range(days_supply):
                    covered_date = fill_date + timedelta(days=day_offset)
                    
                    # Only count days in treatment period
                    if first_fill_date <= covered_date <= treatment_end:
                        covered_dates.add(covered_date)
            
            days_covered = len(covered_dates)
            pdc = days_covered / treatment_days if treatment_days > 0 else 0.0
            adherent = pdc >= 0.80
            
            member_pdcs.append({
                "member_id": member_id,
                "fill_count": fill_count,
                "first_fill_date": first_fill_date,
                "last_fill_date": last_fill_date,
                "treatment_days": treatment_days,
                "days_covered": days_covered,
                "pdc": round(pdc, 4),
                "adherent": adherent,
            })
        
        result_df = pd.DataFrame(member_pdcs)
        
        if not result_df.empty:
            adherent_count = result_df["adherent"].sum()
            total_members = len(result_df)
            adherence_rate = (adherent_count / total_members * 100) if total_members > 0 else 0
            
            logger.info("Calculated PDC for %d members: %d adherent (%.1f%%)",
                       total_members, adherent_count, adherence_rate)
        
        return result_df


# ============================================================================
# CONVENIENCE FUNCTIONS
# ============================================================================

def calculate_diabetes_pdc(
    pharmacy_df: pd.DataFrame,
    measurement_year: int = 2023
) -> pd.DataFrame:
    """
    Calculate PDC for diabetes medications (convenience function).
    
    Args:
        pharmacy_df: Pharmacy claims
        measurement_year: Measurement year
        
    Returns:
        DataFrame with member-level PDC for diabetes medications
    """
    loader = PharmacyLoader()
    fills = loader.load_pharmacy_claims(
        pharmacy_df,
        medication_class="diabetes",
        measurement_year=measurement_year
    )
    pdc = loader.calculate_pdc(fills, measurement_year=measurement_year)
    return pdc


def calculate_statin_pdc(
    pharmacy_df: pd.DataFrame,
    measurement_year: int = 2023
) -> pd.DataFrame:
    """Calculate PDC for statins (convenience function)."""
    loader = PharmacyLoader()
    fills = loader.load_pharmacy_claims(
        pharmacy_df,
        medication_class="statin",
        measurement_year=measurement_year
    )
    pdc = loader.calculate_pdc(fills, measurement_year=measurement_year)
    return pdc


def calculate_rasa_pdc(
    pharmacy_df: pd.DataFrame,
    measurement_year: int = 2023
) -> pd.DataFrame:
    """Calculate PDC for RAS antagonists (convenience function)."""
    loader = PharmacyLoader()
    fills = loader.load_pharmacy_claims(
        pharmacy_df,
        medication_class="rasa",
        measurement_year=measurement_year
    )
    pdc = loader.calculate_pdc(fills, measurement_year=measurement_year)
    return pdc

"""
Vitals Data Loader for HEDIS Blood Pressure Measures

This module loads and processes vital signs data (blood pressure, BMI, weight, etc.)
for HEDIS measures requiring vitals validation.

HEDIS Measures Supported:
- BPD: Blood Pressure Control for Patients with Diabetes (<140/90 mmHg)
- CBP: Controlling High Blood Pressure (<140/90 mmHg)

HEDIS Specification: MY2025 Volume 2
HIPAA Compliance: PHI-safe logging with hashed member IDs
"""

import pandas as pd
import numpy as np
import hashlib
import logging
from typing import Dict, List, Set, Optional, Tuple
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class VitalsLoader:
    """
    Load and process vital signs data for HEDIS measures.
    
    Supports:
    - Blood pressure readings (systolic, diastolic)
    - BMI calculations
    - Weight/height measurements
    """
    
    def __init__(self):
        """Initialize the vitals loader."""
        logger.info("Vitals loader initialized")
    
    def _hash_member_id(self, member_id: str) -> str:
        """
        Hash member ID for PHI-safe logging.
        
        HIPAA Compliance: Uses SHA-256 hashing to protect member identifiers.
        """
        return hashlib.sha256(str(member_id).encode()).hexdigest()[:8]
    
    def load_blood_pressure(
        self,
        vitals_df: pd.DataFrame,
        measurement_year: int = 2023,
        bp_threshold_systolic: int = 140,
        bp_threshold_diastolic: int = 90
    ) -> pd.DataFrame:
        """
        Load blood pressure readings from vitals data.
        
        Args:
            vitals_df: Vitals data with BP readings
            measurement_year: Measurement year for date filtering
            bp_threshold_systolic: Systolic BP threshold (default: 140)
            bp_threshold_diastolic: Diastolic BP threshold (default: 90)
            
        Returns:
            DataFrame with BP readings:
            - member_id
            - reading_date
            - systolic_bp
            - diastolic_bp
            - bp_controlled (bool, <140/90)
            
        HEDIS Specification: MY2025 Volume 2
        BP Control: <140 systolic AND <90 diastolic
        """
        # Handle column name variations
        col_mapping = self._map_vitals_columns(vitals_df)
        
        if not all(k in col_mapping for k in ["member_id", "reading_date", "systolic_bp", "diastolic_bp"]):
            logger.warning("Missing required BP columns")
            return pd.DataFrame(columns=[
                "member_id", "reading_date", "systolic_bp", "diastolic_bp", "bp_controlled"
            ])
        
        # Select and rename columns
        vitals_subset = vitals_df[list(col_mapping.keys())].copy()
        vitals_subset = vitals_subset.rename(columns=col_mapping)
        
        # Parse dates
        vitals_subset["reading_date"] = pd.to_datetime(
            vitals_subset["reading_date"], 
            errors="coerce"
        )
        
        # Filter by measurement year
        year_start = pd.Timestamp(f"{measurement_year}-01-01")
        year_end = pd.Timestamp(f"{measurement_year}-12-31")
        vitals_subset = vitals_subset[
            (vitals_subset["reading_date"] >= year_start) &
            (vitals_subset["reading_date"] <= year_end)
        ]
        
        if vitals_subset.empty:
            logger.warning("No BP readings found in measurement year")
            return pd.DataFrame(columns=[
                "member_id", "reading_date", "systolic_bp", "diastolic_bp", "bp_controlled"
            ])
        
        # Convert BP to numeric
        vitals_subset["systolic_bp"] = pd.to_numeric(
            vitals_subset["systolic_bp"], 
            errors="coerce"
        )
        vitals_subset["diastolic_bp"] = pd.to_numeric(
            vitals_subset["diastolic_bp"], 
            errors="coerce"
        )
        
        # Remove invalid readings
        vitals_subset = vitals_subset[
            (vitals_subset["systolic_bp"].notna()) &
            (vitals_subset["diastolic_bp"].notna()) &
            (vitals_subset["systolic_bp"] > 0) &
            (vitals_subset["systolic_bp"] < 300) &  # Invalid if >300
            (vitals_subset["diastolic_bp"] > 0) &
            (vitals_subset["diastolic_bp"] < 200)   # Invalid if >200
        ]
        
        # Calculate BP control
        vitals_subset["bp_controlled"] = (
            (vitals_subset["systolic_bp"] < bp_threshold_systolic) &
            (vitals_subset["diastolic_bp"] < bp_threshold_diastolic)
        )
        
        # Sort by member and date
        vitals_subset = vitals_subset.sort_values(["member_id", "reading_date"])
        
        # PHI-safe logging
        unique_members = vitals_subset["member_id"].nunique()
        total_readings = len(vitals_subset)
        controlled_readings = vitals_subset["bp_controlled"].sum()
        
        logger.info("Loaded %d BP readings for %d members (%d controlled)",
                   total_readings, unique_members, controlled_readings)
        
        return vitals_subset
    
    def _map_vitals_columns(self, vitals_df: pd.DataFrame) -> Dict[str, str]:
        """
        Map column names from source to standard names.
        
        Handles various column naming conventions.
        """
        col_mapping = {}
        
        # Member ID
        for col in ["DESYNPUF_ID", "member_id", "BENE_ID", "patient_id"]:
            if col in vitals_df.columns:
                col_mapping[col] = "member_id"
                break
        
        # Reading date
        for col in ["reading_date", "measure_date", "encounter_date", "service_date", "SRVC_DT"]:
            if col in vitals_df.columns:
                col_mapping[col] = "reading_date"
                break
        
        # Systolic BP
        for col in ["systolic_bp", "systolic", "sbp", "BP_SYSTOLIC", "SYSTOLIC_BP"]:
            if col in vitals_df.columns:
                col_mapping[col] = "systolic_bp"
                break
        
        # Diastolic BP
        for col in ["diastolic_bp", "diastolic", "dbp", "BP_DIASTOLIC", "DIASTOLIC_BP"]:
            if col in vitals_df.columns:
                col_mapping[col] = "diastolic_bp"
                break
        
        return col_mapping
    
    def get_member_bp_summary(
        self,
        bp_df: pd.DataFrame,
        use_most_recent: bool = True
    ) -> pd.DataFrame:
        """
        Aggregate BP readings to member level.
        
        Args:
            bp_df: BP readings from load_blood_pressure()
            use_most_recent: If True, use most recent reading; if False, use all readings
            
        Returns:
            DataFrame with member-level BP summary:
            - member_id
            - has_bp_reading (bool)
            - reading_count (int)
            - most_recent_date
            - most_recent_systolic
            - most_recent_diastolic
            - most_recent_controlled (bool)
            - any_controlled_reading (bool) - True if ANY reading was controlled
            
        HEDIS Specification: Most recent BP reading used for measure
        """
        if bp_df.empty:
            return pd.DataFrame(columns=[
                "member_id", "has_bp_reading", "reading_count",
                "most_recent_date", "most_recent_systolic", "most_recent_diastolic",
                "most_recent_controlled", "any_controlled_reading"
            ])
        
        # Aggregate by member
        member_summary = []
        
        for member_id, member_bps in bp_df.groupby("member_id"):
            # Sort by date (most recent last)
            member_bps = member_bps.sort_values("reading_date")
            
            # Most recent reading
            most_recent = member_bps.iloc[-1]
            
            # Any controlled reading
            any_controlled = member_bps["bp_controlled"].any()
            
            member_summary.append({
                "member_id": member_id,
                "has_bp_reading": True,
                "reading_count": len(member_bps),
                "most_recent_date": most_recent["reading_date"],
                "most_recent_systolic": most_recent["systolic_bp"],
                "most_recent_diastolic": most_recent["diastolic_bp"],
                "most_recent_controlled": most_recent["bp_controlled"],
                "any_controlled_reading": any_controlled,
            })
        
        result_df = pd.DataFrame(member_summary)
        
        logger.info("Created BP summary for %d members", len(result_df))
        
        return result_df
    
    def create_synthetic_bp_data(
        self,
        member_ids: List[str],
        measurement_year: int = 2023,
        controlled_pct: float = 0.5
    ) -> pd.DataFrame:
        """
        Create synthetic BP data for testing (PHI-free).
        
        Args:
            member_ids: List of member IDs to generate data for
            measurement_year: Measurement year
            controlled_pct: Percentage of members with controlled BP
            
        Returns:
            Synthetic BP data
        """
        np.random.seed(42)
        
        bp_readings = []
        
        for i, member_id in enumerate(member_ids):
            # Decide if this member has controlled BP
            is_controlled = i < int(len(member_ids) * controlled_pct)
            
            # Generate 1-3 readings per member
            num_readings = np.random.randint(1, 4)
            
            for reading_num in range(num_readings):
                # Random date in measurement year
                days_offset = np.random.randint(0, 365)
                reading_date = pd.Timestamp(f"{measurement_year}-01-01") + pd.Timedelta(days=days_offset)
                
                if is_controlled:
                    # Controlled: <140/<90
                    systolic = np.random.randint(110, 139)
                    diastolic = np.random.randint(70, 89)
                else:
                    # Uncontrolled: ≥140 or ≥90
                    if np.random.random() < 0.5:
                        # High systolic
                        systolic = np.random.randint(140, 180)
                        diastolic = np.random.randint(70, 95)
                    else:
                        # High diastolic
                        systolic = np.random.randint(120, 150)
                        diastolic = np.random.randint(90, 110)
                
                bp_readings.append({
                    "member_id": member_id,
                    "reading_date": reading_date,
                    "systolic_bp": systolic,
                    "diastolic_bp": diastolic,
                })
        
        bp_df = pd.DataFrame(bp_readings)
        
        logger.info("Generated %d synthetic BP readings for %d members",
                   len(bp_df), len(member_ids))
        
        return bp_df


# ============================================================================
# CONVENIENCE FUNCTIONS
# ============================================================================

def load_bp_for_bpd(
    vitals_df: pd.DataFrame,
    measurement_year: int = 2023
) -> pd.DataFrame:
    """
    Load BP readings for BPD measure (convenience function).
    
    BP Control threshold: <140/90 mmHg
    """
    loader = VitalsLoader()
    return loader.load_blood_pressure(
        vitals_df,
        measurement_year=measurement_year,
        bp_threshold_systolic=140,
        bp_threshold_diastolic=90
    )


def load_bp_for_cbp(
    vitals_df: pd.DataFrame,
    measurement_year: int = 2023
) -> pd.DataFrame:
    """
    Load BP readings for CBP measure (convenience function).
    
    BP Control threshold: <140/90 mmHg
    """
    loader = VitalsLoader()
    return loader.load_blood_pressure(
        vitals_df,
        measurement_year=measurement_year,
        bp_threshold_systolic=140,
        bp_threshold_diastolic=90
    )

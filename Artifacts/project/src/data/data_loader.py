"""
Data Loader for HEDIS GSD Prediction Engine

Loads and validates CMS DE-SynPUF data files with proper schema validation
and PHI-safe logging practices.

HEDIS Specification: MY2023 Volume 2
Measure: HBD - Hemoglobin A1c Control for Patients with Diabetes
"""

import pandas as pd
import logging
from pathlib import Path
from typing import Dict, List, Optional, Tuple
import hashlib

# Configure logging with PHI-safe practices
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class CMSDataLoader:
    """
    Loads CMS DE-SynPUF data files with schema validation and PHI-safe logging.
    
    Implements HIPAA compliance by:
    - Never logging raw member identifiers
    - Using hashed identifiers for audit logs
    - Logging only aggregate counts and statistics
    """
    
    def __init__(self, data_dir: str = "data/raw"):
        """
        Initialize the CMS data loader.
        
        Args:
            data_dir: Path to directory containing CMS DE-SynPUF files
        """
        self.data_dir = Path(data_dir)
        self.schemas = self._define_schemas()
        
    def _define_schemas(self) -> Dict[str, Dict[str, str]]:
        """
        Define expected schemas for CMS DE-SynPUF files.
        
        Returns:
            Dictionary mapping file types to expected column schemas
        """
        return {
            "beneficiary": {
                "DESYNPUF_ID": "object",
                "BENE_BIRTH_DT": "object",  # Will be parsed as date
                "BENE_DEATH_DT": "object",  # Will be parsed as date
                "BENE_SEX_IDENT_CD": "int64",
                "BENE_RACE_CD": "int64",
                "BENE_ESRD_IND": "int64",
                "SP_STATE_CODE": "int64",
                "BENE_COUNTY_CD": "int64",
                "SP_DIABETES": "int64"  # Key diabetes indicator
            },
            "inpatient": {
                "DESYNPUF_ID": "object",
                "CLM_ID": "object",
                "CLM_FROM_DT": "object",  # Will be parsed as date
                "CLM_THRU_DT": "object",  # Will be parsed as date
                "CLM_PMT_AMT": "float64",
                "ICD9_DGNS_CD_1": "object",
                "ICD9_DGNS_CD_2": "object",
                "ICD9_DGNS_CD_3": "object",
                "ICD9_DGNS_CD_4": "object",
                "ICD9_DGNS_CD_5": "object"
            },
            "outpatient": {
                "DESYNPUF_ID": "object",
                "CLM_ID": "object",
                "CLM_FROM_DT": "object",  # Will be parsed as date
                "CLM_THRU_DT": "object",  # Will be parsed as date
                "CLM_PMT_AMT": "float64",
                "ICD9_DGNS_CD_1": "object",
                "ICD9_DGNS_CD_2": "object",
                "ICD9_DGNS_CD_3": "object",
                "ICD9_DGNS_CD_4": "object",
                "ICD9_DGNS_CD_5": "object"
            }
        }
    
    def _hash_identifier(self, identifier: str) -> str:
        """
        Create a hash of an identifier for audit logging.
        
        Args:
            identifier: Raw identifier to hash
            
        Returns:
            First 8 characters of SHA-256 hash
        """
        return hashlib.sha256(str(identifier).encode()).hexdigest()[:8]
    
    def load_beneficiary_data(self) -> pd.DataFrame:
        """
        Load beneficiary summary file with schema validation.
        
        Returns:
            DataFrame with beneficiary data
            
        Raises:
            FileNotFoundError: If beneficiary file not found
            ValueError: If schema validation fails
        """
        file_path = self.data_dir / "DE1_0_2008_Beneficiary_Summary_File_Sample_1.csv"
        
        if not file_path.exists():
            raise FileNotFoundError(f"Beneficiary file not found: {file_path}")
        
        logger.info(f"Loading beneficiary data from {file_path.name}")
        
        try:
            # Load with proper data types
            df = pd.read_csv(file_path, dtype=self.schemas["beneficiary"])
            
            # Validate schema
            self._validate_schema(df, "beneficiary")
            
            # PHI-safe logging - only counts and hashed identifiers
            logger.info(f"Loaded {len(df)} beneficiary records")
            logger.info(f"Date range: {df['BENE_BIRTH_DT'].min()} to {df['BENE_BIRTH_DT'].max()}")
            
            # Log sample of hashed IDs for audit trail
            sample_ids = df['DESYNPUF_ID'].head(3).apply(self._hash_identifier).tolist()
            logger.info(f"Sample hashed IDs: {sample_ids}")
            
            return df
            
        except Exception as e:
            logger.error(f"Error loading beneficiary data: {str(e)}")
            raise
    
    def load_inpatient_data(self) -> pd.DataFrame:
        """
        Load inpatient claims data with schema validation.
        
        Returns:
            DataFrame with inpatient claims data
            
        Raises:
            FileNotFoundError: If inpatient file not found
            ValueError: If schema validation fails
        """
        file_path = self.data_dir / "DE1_0_2008_to_2010_Inpatient_Claims_Sample_1.csv"
        
        if not file_path.exists():
            raise FileNotFoundError(f"Inpatient file not found: {file_path}")
        
        logger.info(f"Loading inpatient claims data from {file_path.name}")
        
        try:
            # Load with proper data types
            df = pd.read_csv(file_path, dtype=self.schemas["inpatient"])
            
            # Validate schema
            self._validate_schema(df, "inpatient")
            
            # PHI-safe logging
            logger.info(f"Loaded {len(df)} inpatient claim records")
            logger.info(f"Date range: {df['CLM_FROM_DT'].min()} to {df['CLM_THRU_DT'].max()}")
            logger.info(f"Total payment amount: ${df['CLM_PMT_AMT'].sum():,.2f}")
            
            return df
            
        except Exception as e:
            logger.error(f"Error loading inpatient data: {str(e)}")
            raise
    
    def load_outpatient_data(self) -> pd.DataFrame:
        """
        Load outpatient claims data with schema validation.
        
        Returns:
            DataFrame with outpatient claims data
            
        Raises:
            FileNotFoundError: If outpatient file not found
            ValueError: If schema validation fails
        """
        file_path = self.data_dir / "DE1_0_2008_to_2010_Outpatient_Claims_Sample_1.csv"
        
        if not file_path.exists():
            raise FileNotFoundError(f"Outpatient file not found: {file_path}")
        
        logger.info(f"Loading outpatient claims data from {file_path.name}")
        
        try:
            # Load with proper data types
            df = pd.read_csv(file_path, dtype=self.schemas["outpatient"])
            
            # Validate schema
            self._validate_schema(df, "outpatient")
            
            # PHI-safe logging
            logger.info(f"Loaded {len(df)} outpatient claim records")
            logger.info(f"Date range: {df['CLM_FROM_DT'].min()} to {df['CLM_THRU_DT'].max()}")
            logger.info(f"Total payment amount: ${df['CLM_PMT_AMT'].sum():,.2f}")
            
            return df
            
        except Exception as e:
            logger.error(f"Error loading outpatient data: {str(e)}")
            raise
    
    def load_all_data(self) -> Dict[str, pd.DataFrame]:
        """
        Load all CMS DE-SynPUF data files.
        
        Returns:
            Dictionary mapping data types to DataFrames
            
        Raises:
            FileNotFoundError: If any required file not found
            ValueError: If schema validation fails
        """
        logger.info("Starting comprehensive CMS data load")
        
        data = {}
        
        try:
            data['beneficiary'] = self.load_beneficiary_data()
            data['inpatient'] = self.load_inpatient_data()
            data['outpatient'] = self.load_outpatient_data()
            
            # Summary statistics (PHI-safe)
            total_members = len(data['beneficiary'])
            total_inpatient_claims = len(data['inpatient'])
            total_outpatient_claims = len(data['outpatient'])
            
            logger.info(f"Data load complete:")
            logger.info(f"  - {total_members} unique members")
            logger.info(f"  - {total_inpatient_claims} inpatient claims")
            logger.info(f"  - {total_outpatient_claims} outpatient claims")
            
            return data
            
        except Exception as e:
            logger.error(f"Error in comprehensive data load: {str(e)}")
            raise
    
    def _validate_schema(self, df: pd.DataFrame, data_type: str) -> None:
        """
        Validate DataFrame schema against expected schema.
        
        Args:
            df: DataFrame to validate
            data_type: Type of data (beneficiary, inpatient, outpatient)
            
        Raises:
            ValueError: If schema validation fails
        """
        expected_schema = self.schemas[data_type]
        
        # Check required columns exist
        missing_cols = set(expected_schema.keys()) - set(df.columns)
        if missing_cols:
            raise ValueError(f"Missing required columns for {data_type}: {missing_cols}")
        
        # Check data types for key columns
        for col, expected_dtype in expected_schema.items():
            if col in df.columns:
                actual_dtype = str(df[col].dtype)
                if expected_dtype not in actual_dtype:
                    logger.warning(f"Column {col} has dtype {actual_dtype}, expected {expected_dtype}")
        
        logger.info(f"Schema validation passed for {data_type} data")


def load_cms_data(data_dir: str = "data/raw") -> Dict[str, pd.DataFrame]:
    """
    Convenience function to load all CMS DE-SynPUF data.
    
    Args:
        data_dir: Path to directory containing CMS files
        
    Returns:
        Dictionary mapping data types to DataFrames
    """
    loader = CMSDataLoader(data_dir)
    return loader.load_all_data()


if __name__ == "__main__":
    # Example usage
    try:
        data = load_cms_data()
        print("Data loaded successfully!")
        print(f"Beneficiary records: {len(data['beneficiary'])}")
        print(f"Inpatient claims: {len(data['inpatient'])}")
        print(f"Outpatient claims: {len(data['outpatient'])}")
    except Exception as e:
        print(f"Error loading data: {e}")

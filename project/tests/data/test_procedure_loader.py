"""
Unit Tests for Procedure Loader

Tests procedure code extraction and aggregation for HEDIS measures.

Test Coverage:
- Eye exam procedure extraction
- Mammography procedure extraction  
- Colonoscopy procedure extraction
- Member-level aggregation
- Date filtering
- Multiple claim types
"""

import unittest
import pandas as pd
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from src.data.loaders.procedure_loader import (
    ProcedureLoader,
    load_eye_exams,
    load_mammography,
    load_colonoscopy,
)


class TestProcedureLoader(unittest.TestCase):
    """Test suite for procedure loader."""
    
    def setUp(self):
        """Set up test data."""
        self.loader = ProcedureLoader()
        
        # Create synthetic outpatient claims with eye exam codes
        self.outpatient_df = pd.DataFrame({
            "DESYNPUF_ID": ["M001", "M002", "M003", "M001"],
            "CLM_FROM_DT": [
                "2023-05-10",
                "2023-07-22",
                "2022-11-15",  # Prior year
                "2023-09-05",
            ],
            "HCPCS_CD_1": ["92014", "92225", "92014", "92134"],  # Eye exam codes
            "HCPCS_CD_2": [None, None, None, None],
        })
        
        # Create synthetic inpatient claims (empty for eye exams)
        self.inpatient_df = pd.DataFrame({
            "DESYNPUF_ID": [],
            "CLM_FROM_DT": [],
            "HCPCS_CD_1": [],
        })
    
    def test_initialization(self):
        """Test procedure loader initialization."""
        self.assertIn("eye_exam", self.loader.procedure_types)
        self.assertIn("mammography", self.loader.procedure_types)
        self.assertIn("colonoscopy", self.loader.procedure_types)
        
        # Check code sets
        self.assertGreater(len(self.loader.EYE_EXAM_CPT), 0)
        self.assertGreater(len(self.loader.MAMMOGRAPHY_CPT), 0)
        self.assertGreater(len(self.loader.COLONOSCOPY_CPT), 0)
    
    def test_load_eye_exams(self):
        """Test eye exam procedure loading."""
        procedures = self.loader.load_procedures_from_claims(
            inpatient_df=self.inpatient_df,
            outpatient_df=self.outpatient_df,
            procedure_type="eye_exam",
            measurement_year=2023
        )
        
        # Should have 3 procedures in 2023 (M001 x2, M002 x1)
        # M003's procedure is in 2022, should be filtered out
        self.assertEqual(len(procedures), 3)
        
        # Check columns
        self.assertIn("member_id", procedures.columns)
        self.assertIn("procedure_code", procedures.columns)
        self.assertIn("service_date", procedures.columns)
        self.assertIn("claim_type", procedures.columns)
        
        # Check specific procedures
        m001_procedures = procedures[procedures["member_id"] == "M001"]
        self.assertEqual(len(m001_procedures), 2)  # Two exams for M001
        
        m002_procedures = procedures[procedures["member_id"] == "M002"]
        self.assertEqual(len(m002_procedures), 1)  # One exam for M002
        
        # M003 should have 0 procedures (2022 exam filtered out)
        m003_procedures = procedures[procedures["member_id"] == "M003"]
        self.assertEqual(len(m003_procedures), 0)
    
    def test_date_filtering(self):
        """Test date filtering by measurement year."""
        procedures = self.loader.load_procedures_from_claims(
            inpatient_df=self.inpatient_df,
            outpatient_df=self.outpatient_df,
            procedure_type="eye_exam",
            measurement_year=2023
        )
        
        # All procedures should be in 2023
        for _, row in procedures.iterrows():
            self.assertEqual(row["service_date"].year, 2023)
        
        # Test with 2022 measurement year
        procedures_2022 = self.loader.load_procedures_from_claims(
            inpatient_df=self.inpatient_df,
            outpatient_df=self.outpatient_df,
            procedure_type="eye_exam",
            measurement_year=2022
        )
        
        # Should only have M003's 2022 exam
        self.assertEqual(len(procedures_2022), 1)
        self.assertEqual(procedures_2022.iloc[0]["member_id"], "M003")
    
    def test_member_procedure_summary(self):
        """Test member-level procedure aggregation."""
        procedures = self.loader.load_procedures_from_claims(
            inpatient_df=self.inpatient_df,
            outpatient_df=self.outpatient_df,
            procedure_type="eye_exam",
            measurement_year=2023
        )
        
        summary = self.loader.get_member_procedure_summary(
            procedures,
            procedure_type="eye_exam"
        )
        
        # Should have 2 members (M001, M002)
        self.assertEqual(len(summary), 2)
        
        # Check M001 (2 procedures)
        m001_summary = summary[summary["member_id"] == "M001"].iloc[0]
        self.assertTrue(m001_summary["has_procedure"])
        self.assertEqual(m001_summary["procedure_count"], 2)
        self.assertEqual(len(m001_summary["procedure_codes"]), 2)  # 92014, 92134
        
        # Check M002 (1 procedure)
        m002_summary = summary[summary["member_id"] == "M002"].iloc[0]
        self.assertTrue(m002_summary["has_procedure"])
        self.assertEqual(m002_summary["procedure_count"], 1)
        self.assertEqual(m002_summary["procedure_codes"], ["92225"])
    
    def test_empty_procedures(self):
        """Test handling of empty procedure data."""
        empty_df = pd.DataFrame({
            "DESYNPUF_ID": [],
            "CLM_FROM_DT": [],
            "HCPCS_CD_1": [],
        })
        
        procedures = self.loader.load_procedures_from_claims(
            inpatient_df=empty_df,
            outpatient_df=empty_df,
            procedure_type="eye_exam",
            measurement_year=2023
        )
        
        # Should return empty DataFrame with correct columns
        self.assertEqual(len(procedures), 0)
        self.assertIn("member_id", procedures.columns)
        self.assertIn("procedure_code", procedures.columns)
    
    def test_invalid_procedure_type(self):
        """Test error handling for invalid procedure type."""
        with self.assertRaises(ValueError):
            self.loader.load_procedures_from_claims(
                inpatient_df=self.inpatient_df,
                outpatient_df=self.outpatient_df,
                procedure_type="invalid_type",
                measurement_year=2023
            )
    
    def test_convenience_function_eye_exams(self):
        """Test convenience function for eye exams."""
        procedures = load_eye_exams(
            inpatient_df=self.inpatient_df,
            outpatient_df=self.outpatient_df,
            measurement_year=2023
        )
        
        # Should work same as full loader
        self.assertGreater(len(procedures), 0)
        self.assertIn("member_id", procedures.columns)


class TestProcedureTypes(unittest.TestCase):
    """Test different procedure types."""
    
    def setUp(self):
        """Set up test data for different procedure types."""
        self.loader = ProcedureLoader()
    
    def test_eye_exam_codes(self):
        """Test eye exam code sets."""
        eye_exam_codes = self.loader.EYE_EXAM_CPT | self.loader.EYE_EXAM_HCPCS
        
        # Check specific codes
        self.assertIn("92014", eye_exam_codes)  # Comprehensive exam
        self.assertIn("92225", eye_exam_codes)  # Ophthalmoscopy
        self.assertIn("92134", eye_exam_codes)  # OCT imaging
        self.assertIn("S0620", eye_exam_codes)  # Routine exam (HCPCS)
    
    def test_mammography_codes(self):
        """Test mammography code sets."""
        mammo_codes = self.loader.MAMMOGRAPHY_CPT | self.loader.MAMMOGRAPHY_HCPCS
        
        # Check specific codes
        self.assertIn("77067", mammo_codes)  # Screening mammography
        self.assertIn("G0202", mammo_codes)  # Screening (HCPCS)
    
    def test_colonoscopy_codes(self):
        """Test colonoscopy code sets."""
        colo_codes = self.loader.COLONOSCOPY_CPT | self.loader.COLONOSCOPY_HCPCS
        
        # Check specific codes
        self.assertIn("45378", colo_codes)  # Diagnostic colonoscopy
        self.assertIn("G0105", colo_codes)  # Screening colonoscopy (HCPCS)


if __name__ == "__main__":
    unittest.main()


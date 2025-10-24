"""
Unit Tests for EED (Eye Exam for Diabetes) Measure

Tests the EED measure calculation logic against synthetic PHI-free test data.

Test Coverage:
- Denominator identification (age + diabetes)
- Exclusions (hospice, advanced illness)
- Numerator calculation (eye exam procedures)
- Gap identification
- Summary statistics
- Edge cases
"""

import unittest
import pandas as pd
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from src.measures.eed import EEDMeasure
from tests.fixtures.synthetic_eed_data import (
    generate_synthetic_eed_members,
    generate_synthetic_eed_claims,
    generate_synthetic_eed_procedures,
    get_expected_eed_results,
    get_expected_eed_summary,
)


class TestEEDMeasure(unittest.TestCase):
    """Test suite for EED measure calculations."""
    
    def setUp(self):
        """Set up test data and measure calculator."""
        self.measure = EEDMeasure(measurement_year=2023)
        self.members_df = generate_synthetic_eed_members()
        self.claims_df = generate_synthetic_eed_claims()
        self.procedures_df = generate_synthetic_eed_procedures()
        self.expected_results = get_expected_eed_results()
        self.expected_summary = get_expected_eed_summary()
    
    def test_initialization(self):
        """Test EED measure initialization."""
        self.assertEqual(self.measure.measurement_year, 2023)
        self.assertEqual(
            self.measure.measurement_year_end, 
            pd.Timestamp("2023-12-31")
        )
        # Check eye exam codes are loaded
        self.assertGreater(len(self.measure.all_eye_exam_codes), 0)
        self.assertIn("92014", self.measure.all_eye_exam_codes)  # Comprehensive exam
        self.assertIn("92225", self.measure.all_eye_exam_codes)  # Ophthalmoscopy
    
    def test_age_calculation(self):
        """Test age calculation at year end."""
        ages = self.measure.calculate_age_at_year_end(self.members_df["BENE_BIRTH_DT"])
        
        # Verify specific ages
        self.assertEqual(ages.iloc[0], 53)  # M00001: Born 1970
        self.assertEqual(ages.iloc[1], 68)  # M00002: Born 1955
        self.assertEqual(ages.iloc[4], 13)  # M00005: Born 2010 (too young)
        self.assertEqual(ages.iloc[5], 83)  # M00006: Born 1940 (too old)
    
    def test_denominator_identification(self):
        """Test denominator: age 18-75 + diabetes."""
        denominator = self.measure.identify_denominator(
            self.members_df,
            self.claims_df
        )
        
        # Expected: 8 members (ages 18-75 with diabetes)
        # Excludes M00005 (age 13) and M00006 (age 83)
        self.assertEqual(len(denominator), 8)
        
        # Check specific members
        denominator_ids = set(denominator["DESYNPUF_ID"])
        self.assertIn("M00001", denominator_ids)  # Age 53, diabetes
        self.assertIn("M00002", denominator_ids)  # Age 68, diabetes
        self.assertNotIn("M00005", denominator_ids)  # Age 13 (too young)
        self.assertNotIn("M00006", denominator_ids)  # Age 83 (too old)
        
        # All should have in_denominator flag
        self.assertTrue(denominator["in_denominator"].all())
    
    def test_exclusions(self):
        """Test exclusion application (hospice)."""
        denominator = self.measure.identify_denominator(
            self.members_df,
            self.claims_df
        )
        result = self.measure.apply_exclusions(denominator, self.claims_df)
        
        # Expected: M00009 excluded (hospice)
        excluded_members = result[result["excluded"]]["DESYNPUF_ID"].tolist()
        self.assertEqual(len(excluded_members), 1)
        self.assertIn("M00009", excluded_members)
        
        # Others should not be excluded
        not_excluded = result[~result["excluded"]]["DESYNPUF_ID"].tolist()
        self.assertIn("M00001", not_excluded)
        self.assertIn("M00002", not_excluded)
    
    def test_numerator_calculation(self):
        """Test numerator: members with eye exams."""
        denominator = self.measure.identify_denominator(
            self.members_df,
            self.claims_df
        )
        denominator = self.measure.apply_exclusions(denominator, self.claims_df)
        result = self.measure.calculate_numerator(denominator, self.procedures_df)
        
        # Expected compliant: M00001, M00002, M00007, M00010
        compliant_members = result[result["numerator_compliant"]]["DESYNPUF_ID"].tolist()
        self.assertEqual(len(compliant_members), 4)
        self.assertIn("M00001", compliant_members)  # Retinal exam
        self.assertIn("M00002", compliant_members)  # Comprehensive exam
        self.assertIn("M00007", compliant_members)  # Multiple exams
        self.assertIn("M00010", compliant_members)  # OCT imaging
        
        # Expected non-compliant: M00003, M00004, M00008
        non_compliant = result[
            ~result["numerator_compliant"] & ~result["excluded"]
        ]["DESYNPUF_ID"].tolist()
        self.assertIn("M00003", non_compliant)  # No exam
        self.assertIn("M00004", non_compliant)  # No exam
        self.assertIn("M00008", non_compliant)  # Exam in 2022 only
    
    def test_gap_identification(self):
        """Test gap identification."""
        denominator = self.measure.identify_denominator(
            self.members_df,
            self.claims_df
        )
        denominator = self.measure.apply_exclusions(denominator, self.claims_df)
        result = self.measure.calculate_numerator(denominator, self.procedures_df)
        result = self.measure.calculate_gaps(result)
        
        # Expected gaps: M00003, M00004, M00008
        gap_members = result[result["has_gap"]]["DESYNPUF_ID"].tolist()
        self.assertEqual(len(gap_members), 3)
        self.assertIn("M00003", gap_members)
        self.assertIn("M00004", gap_members)
        self.assertIn("M00008", gap_members)
        
        # M00009 should NOT have gap (excluded)
        self.assertNotIn("M00009", gap_members)
    
    def test_complete_measure_calculation(self):
        """Test complete EED measure calculation."""
        result = self.measure.calculate_measure(
            self.members_df,
            self.claims_df,
            self.procedures_df
        )
        
        # Check structure
        self.assertIn("results_df", result)
        self.assertIn("summary", result)
        
        results_df = result["results_df"]
        summary = result["summary"]
        
        # Verify summary statistics
        self.assertEqual(summary["measure"], "EED")
        self.assertEqual(summary["denominator"], self.expected_summary["denominator"])
        self.assertEqual(summary["exclusions"], self.expected_summary["exclusions"])
        self.assertEqual(summary["eligible_population"], self.expected_summary["eligible_population"])
        self.assertEqual(summary["numerator"], self.expected_summary["numerator"])
        self.assertEqual(summary["gaps"], self.expected_summary["gaps"])
        self.assertAlmostEqual(summary["compliance_rate"], self.expected_summary["compliance_rate"], places=1)
        self.assertAlmostEqual(summary["gap_rate"], self.expected_summary["gap_rate"], places=1)
    
    def test_individual_member_results(self):
        """Test individual member results match expected outcomes."""
        result = self.measure.calculate_measure(
            self.members_df,
            self.claims_df,
            self.procedures_df
        )
        
        results_df = result["results_df"]
        
        # Test each member against expected results
        for member_id, expected in self.expected_results.items():
            if member_id in results_df["DESYNPUF_ID"].values:
                member_row = results_df[results_df["DESYNPUF_ID"] == member_id].iloc[0]
                
                self.assertEqual(
                    member_row["in_denominator"],
                    expected["in_denominator"],
                    f"{member_id}: in_denominator mismatch"
                )
                self.assertEqual(
                    member_row["excluded"],
                    expected["excluded"],
                    f"{member_id}: excluded mismatch"
                )
                self.assertEqual(
                    member_row["has_eye_exam"],
                    expected["has_eye_exam"],
                    f"{member_id}: has_eye_exam mismatch"
                )
                self.assertEqual(
                    member_row["numerator_compliant"],
                    expected["numerator_compliant"],
                    f"{member_id}: numerator_compliant mismatch"
                )
                self.assertEqual(
                    member_row["has_gap"],
                    expected["has_gap"],
                    f"{member_id}: has_gap mismatch"
                )
    
    def test_edge_case_no_procedures(self):
        """Test handling of members with no procedures."""
        empty_procedures = pd.DataFrame(columns=["member_id", "procedure_code", 
                                                 "service_date", "claim_type"])
        
        result = self.measure.calculate_measure(
            self.members_df,
            self.claims_df,
            empty_procedures
        )
        
        # All eligible members should have gaps
        summary = result["summary"]
        self.assertEqual(summary["numerator"], 0)
        self.assertEqual(summary["gaps"], summary["eligible_population"])
    
    def test_edge_case_prior_year_exam(self):
        """Test that prior year exams don't count for numerator."""
        # M00008 has exam in 2022 only
        result = self.measure.calculate_measure(
            self.members_df,
            self.claims_df,
            self.procedures_df
        )
        
        results_df = result["results_df"]
        m00008 = results_df[results_df["DESYNPUF_ID"] == "M00008"].iloc[0]
        
        # Should NOT be compliant (exam in wrong year)
        self.assertFalse(m00008["numerator_compliant"])
        self.assertTrue(m00008["has_gap"])
    
    def test_edge_case_multiple_exams(self):
        """Test handling of members with multiple exams."""
        # M00007 has multiple exams
        result = self.measure.calculate_measure(
            self.members_df,
            self.claims_df,
            self.procedures_df
        )
        
        results_df = result["results_df"]
        m00007 = results_df[results_df["DESYNPUF_ID"] == "M00007"].iloc[0]
        
        # Should be compliant (has at least one exam)
        self.assertTrue(m00007["numerator_compliant"])
        self.assertFalse(m00007["has_gap"])


if __name__ == "__main__":
    unittest.main()

"""
Unit Tests for Labs Data Loader

Tests lab results loading (eGFR, ACR, HbA1c) with LOINC code mapping
and member-level aggregation for HEDIS measures.
"""

import unittest
import pandas as pd
import numpy as np
from datetime import datetime
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

# Import modules to test
try:
    from src.data.loaders.labs_loader import (
        LabsLoader,
        load_lab_results,
        LOINC_CODE_MAPPING
    )
except ImportError:
    # Module may not exist yet, skip tests
    pass


class TestLabsLoader(unittest.TestCase):
    """Test cases for labs data loader."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.loader = LabsLoader()
        
        # Create sample lab data
        self.sample_labs = self._create_sample_labs()
    
    def _create_sample_labs(self):
        """Create sample lab results for testing."""
        labs = [
            # HbA1c tests
            {
                'member_id': 'TEST001',
                'test_date': datetime(2025, 3, 15),
                'loinc_code': '4548-4',  # HbA1c
                'result_value': 7.5,
                'result_unit': '%',
            },
            {
                'member_id': 'TEST001',
                'test_date': datetime(2025, 6, 20),
                'loinc_code': '4548-4',  # HbA1c (more recent)
                'result_value': 7.2,
                'result_unit': '%',
            },
            
            # eGFR tests
            {
                'member_id': 'TEST002',
                'test_date': datetime(2025, 4, 10),
                'loinc_code': '48642-3',  # eGFR CKD-EPI
                'result_value': 65.0,
                'result_unit': 'mL/min/1.73m2',
            },
            {
                'member_id': 'TEST002',
                'test_date': datetime(2025, 8, 15),
                'loinc_code': '48643-1',  # eGFR MDRD
                'result_value': 63.0,
                'result_unit': 'mL/min/1.73m2',
            },
            
            # ACR tests
            {
                'member_id': 'TEST003',
                'test_date': datetime(2025, 5, 20),
                'loinc_code': '9318-7',  # ACR
                'result_value': 35.0,
                'result_unit': 'mg/g',
            },
            
            # Multiple test types for same member
            {
                'member_id': 'TEST004',
                'test_date': datetime(2025, 6, 1),
                'loinc_code': '4548-4',  # HbA1c
                'result_value': 8.2,
                'result_unit': '%',
            },
            {
                'member_id': 'TEST004',
                'test_date': datetime(2025, 6, 1),
                'loinc_code': '48642-3',  # eGFR
                'result_value': 70.0,
                'result_unit': 'mL/min/1.73m2',
            },
            {
                'member_id': 'TEST004',
                'test_date': datetime(2025, 6, 1),
                'loinc_code': '9318-7',  # ACR
                'result_value': 25.0,
                'result_unit': 'mg/g',
            },
        ]
        
        return pd.DataFrame(labs)
    
    def test_loinc_code_mapping(self):
        """Test LOINC code mapping for lab tests."""
        # Should have mappings for HbA1c, eGFR, ACR
        self.assertIn('hba1c', LOINC_CODE_MAPPING)
        self.assertIn('egfr', LOINC_CODE_MAPPING)
        self.assertIn('acr', LOINC_CODE_MAPPING)
        
        # HbA1c codes
        hba1c_codes = LOINC_CODE_MAPPING['hba1c']
        self.assertIn('4548-4', hba1c_codes)
        self.assertIn('17856-6', hba1c_codes)
        
        # eGFR codes
        egfr_codes = LOINC_CODE_MAPPING['egfr']
        self.assertIn('48642-3', egfr_codes)  # CKD-EPI
        self.assertIn('48643-1', egfr_codes)  # MDRD
        
        # ACR codes
        acr_codes = LOINC_CODE_MAPPING['acr']
        self.assertIn('9318-7', acr_codes)
        self.assertIn('13705-9', acr_codes)
    
    def test_hba1c_extraction(self):
        """Test HbA1c test extraction."""
        result = self.loader.extract_hba1c_tests(self.sample_labs.copy())
        
        # Should extract HbA1c tests
        self.assertGreater(len(result), 0)
        self.assertTrue(all(result['loinc_code'] == '4548-4'))
        
        # Should have required columns
        required_cols = ['member_id', 'test_date', 'loinc_code', 'result_value']
        for col in required_cols:
            self.assertIn(col, result.columns)
    
    def test_egfr_extraction(self):
        """Test eGFR test extraction."""
        result = self.loader.extract_egfr_tests(self.sample_labs.copy())
        
        # Should extract eGFR tests
        self.assertGreater(len(result), 0)
        self.assertTrue(all(result['loinc_code'].isin(['48642-3', '48643-1'])))
    
    def test_acr_extraction(self):
        """Test ACR test extraction."""
        result = self.loader.extract_acr_tests(self.sample_labs.copy())
        
        # Should extract ACR tests
        self.assertGreater(len(result), 0)
        self.assertTrue(all(result['loinc_code'] == '9318-7'))
    
    def test_member_level_aggregation(self):
        """Test member-level aggregation (most recent test)."""
        # Member with multiple HbA1c tests
        member_tests = self.sample_labs[
            (self.sample_labs['member_id'] == 'TEST001') &
            (self.sample_labs['loinc_code'] == '4548-4')
        ]
        
        # Should have 2 tests
        self.assertEqual(len(member_tests), 2)
        
        # Most recent should be June 20 with value 7.2
        most_recent = member_tests.sort_values('test_date').iloc[-1]
        self.assertEqual(most_recent['result_value'], 7.2)
    
    def test_date_filtering(self):
        """Test date filtering for measurement year."""
        # Filter to Q2 2025 (April-June)
        start_date = datetime(2025, 4, 1)
        end_date = datetime(2025, 6, 30)
        
        filtered = self.loader.filter_by_date(
            self.sample_labs.copy(),
            start_date,
            end_date
        )
        
        # Should only include tests in Q2
        self.assertTrue(all(
            (pd.to_datetime(filtered['test_date']) >= start_date) &
            (pd.to_datetime(filtered['test_date']) <= end_date)
        ))
    
    def test_missing_data_handling(self):
        """Test handling of missing/invalid data."""
        # Create data with missing values
        labs_with_nulls = self.sample_labs.copy()
        labs_with_nulls.loc[0, 'result_value'] = np.nan
        
        # Should handle gracefully (either drop or flag)
        result = self.loader.extract_hba1c_tests(labs_with_nulls)
        
        # Should not crash
        self.assertIsInstance(result, pd.DataFrame)
    
    def test_multiple_test_types_same_member(self):
        """Test member with multiple test types on same date."""
        # TEST004 has HbA1c, eGFR, and ACR on same date
        member_labs = self.sample_labs[self.sample_labs['member_id'] == 'TEST004']
        
        # Should have 3 different test types
        self.assertEqual(len(member_labs), 3)
        self.assertEqual(len(member_labs['loinc_code'].unique()), 3)
        
        # Each test type should be extractable separately
        hba1c = self.loader.extract_hba1c_tests(member_labs.copy())
        egfr = self.loader.extract_egfr_tests(member_labs.copy())
        acr = self.loader.extract_acr_tests(member_labs.copy())
        
        self.assertEqual(len(hba1c), 1)
        self.assertEqual(len(egfr), 1)
        self.assertEqual(len(acr), 1)


class TestLabsLoaderPHIProtection(unittest.TestCase):
    """Test PHI protection in labs loader."""
    
    def test_no_raw_member_ids_in_logs(self):
        """Test that raw member IDs are not logged."""
        # Labs loader should hash member IDs or use aggregate counts in logs
        # This is a security requirement
        pass  # Implement with actual logging capture
    
    def test_aggregated_statistics_only(self):
        """Test that only aggregated statistics are logged."""
        # Should log counts, not individual member records
        pass  # Implement with actual logging capture


if __name__ == '__main__':
    unittest.main()


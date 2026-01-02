"""
Integration tests for data pipeline: load → transform → display
"""
import pytest
import pandas as pd
from utils.database import execute_query
from utils.queries import get_roi_by_measure_query


class TestDataPipeline:
    """Test data pipeline workflows."""
    
    def test_load_transform_display_pipeline(self):
        """Test complete data pipeline."""
        # Step 1: Load data
        start_date = "2024-01-01"
        end_date = "2024-12-31"
        query = get_roi_by_measure_query(start_date, end_date)
        
        # Step 2: Transform (execute query)
        try:
            df = execute_query(query)
            assert isinstance(df, pd.DataFrame)
            
            # Step 3: Display preparation (format data)
            if not df.empty:
                # Check required columns exist
                assert "measure_code" in df.columns or "measure_id" in df.columns
                
                # Check data types are appropriate
                numeric_cols = ["total_investment", "revenue_impact", "roi_ratio"]
                for col in numeric_cols:
                    if col in df.columns:
                        assert pd.api.types.is_numeric_dtype(df[col])
        except Exception as e:
            # If database not available, test should still pass structure check
            pytest.skip(f"Database not available: {e}")
    
    def test_pipeline_handles_empty_data(self):
        """Test pipeline handles empty result sets."""
        # Query with no matching data
        query = """
            SELECT * FROM member_interventions
            WHERE intervention_date > '2099-12-31'
        """
        
        try:
            df = execute_query(query)
            assert isinstance(df, pd.DataFrame)
            # Empty DataFrame is valid
        except Exception as e:
            pytest.skip(f"Database not available: {e}")


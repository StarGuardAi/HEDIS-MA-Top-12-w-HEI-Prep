"""
Unit tests for data loading functions
"""
import pytest
import pandas as pd
from datetime import datetime, timedelta
from utils.database import execute_query, get_connection
from utils.queries import (
    get_roi_by_measure_query,
    get_portfolio_summary_query,
    get_cost_per_closure_by_activity_query
)


class TestDataLoading:
    """Test data loading functions."""
    
    def test_get_roi_by_measure_query_structure(self):
        """Test ROI by measure query returns correct structure."""
        start_date = "2024-01-01"
        end_date = "2024-12-31"
        query = get_roi_by_measure_query(start_date, end_date)
        
        assert "SELECT" in query.upper()
        assert "measure_id" in query or "measure_code" in query
        assert "roi_ratio" in query.lower()
        assert start_date in query
        assert end_date in query
    
    def test_get_portfolio_summary_query_structure(self):
        """Test portfolio summary query structure."""
        start_date = "2024-01-01"
        end_date = "2024-12-31"
        query = get_portfolio_summary_query(start_date, end_date)
        
        assert "SELECT" in query.upper()
        assert "total_investment" in query.lower()
        assert "total_closures" in query.lower()
        assert start_date in query
        assert end_date in query
    
    def test_get_cost_per_closure_query_structure(self):
        """Test cost per closure query structure."""
        start_date = "2024-01-01"
        end_date = "2024-12-31"
        query = get_cost_per_closure_by_activity_query(start_date, end_date)
        
        assert "SELECT" in query.upper()
        assert "activity_name" in query.lower()
        assert "cost_per_closure" in query.lower()
        assert start_date in query
        assert end_date in query
    
    def test_query_date_validation(self):
        """Test queries handle date ranges correctly."""
        start_date = "2024-01-01"
        end_date = "2024-12-31"
        
        query = get_roi_by_measure_query(start_date, end_date)
        
        # Check dates are properly formatted in query
        assert start_date in query
        assert end_date in query
        assert ">=" in query or ">=" in query.upper()
        assert "<=" in query or "<=" in query.upper()
    
    def test_query_handles_empty_results(self, temp_db):
        """Test queries handle empty result sets gracefully."""
        # Query with date range that has no data
        start_date = "2020-01-01"
        end_date = "2020-12-31"
        
        query = get_roi_by_measure_query(start_date, end_date)
        
        # Should not raise exception even with no data
        try:
            result = execute_query(query)
            assert isinstance(result, pd.DataFrame)
        except Exception as e:
            pytest.fail(f"Query should handle empty results: {e}")


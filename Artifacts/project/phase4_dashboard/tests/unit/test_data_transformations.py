"""
Unit tests for data transformations
"""
import pytest
import pandas as pd
from utils.database import convert_query_for_sqlite
from utils.scenario_modeler import ScenarioModeler


class TestSQLiteConversions:
    """Test SQL query conversions for SQLite."""
    
    def test_convert_count_filter(self):
        """Test COUNT(*) FILTER conversion."""
        postgres_query = """
            SELECT COUNT(*) FILTER (WHERE status = 'completed') as completed_count
            FROM member_interventions
        """
        
        sqlite_query = convert_query_for_sqlite(postgres_query)
        
        assert "FILTER" not in sqlite_query
        assert "SUM(CASE WHEN" in sqlite_query or "CASE WHEN" in sqlite_query
    
    def test_convert_date_trunc(self):
        """Test DATE_TRUNC conversion."""
        postgres_query = """
            SELECT DATE_TRUNC('month', intervention_date)::DATE as month_start
            FROM member_interventions
        """
        
        sqlite_query = convert_query_for_sqlite(postgres_query)
        
        assert "DATE_TRUNC" not in sqlite_query
        assert "strftime" in sqlite_query or "date(" in sqlite_query
    
    def test_convert_type_casts(self):
        """Test type cast removal."""
        postgres_query = """
            SELECT cost::DECIMAL, date::DATE
            FROM member_interventions
        """
        
        sqlite_query = convert_query_for_sqlite(postgres_query)
        
        assert "::DECIMAL" not in sqlite_query
        assert "::DATE" not in sqlite_query


class TestDataTransformations:
    """Test data transformation functions."""
    
    def test_scenario_data_formatting(self, scenario_modeler):
        """Test scenario data is properly formatted."""
        scenario = scenario_modeler.calculate_scenario(250000, 5, "balanced")
        
        # Check all values are proper types
        assert isinstance(scenario["budget"], (int, float))
        assert isinstance(scenario["fte_count"], int)
        assert isinstance(scenario["predicted_roi_ratio"], (int, float))
        assert isinstance(scenario["predicted_closures"], int)
        assert isinstance(scenario["predicted_revenue"], (int, float))
    
    def test_pareto_frontier_formatting(self, scenario_modeler):
        """Test Pareto frontier data formatting."""
        pareto_df = scenario_modeler.generate_pareto_frontier(num_points=10)
        
        assert isinstance(pareto_df, pd.DataFrame)
        if not pareto_df.empty:
            assert "budget" in pareto_df.columns
            assert "fte_count" in pareto_df.columns
            assert "predicted_roi_ratio" in pareto_df.columns
            assert "predicted_closures" in pareto_df.columns


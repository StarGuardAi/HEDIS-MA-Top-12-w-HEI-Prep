"""
Unit tests for forecasting functions
"""
import pytest
import pandas as pd
from utils.historical_tracking import HistoricalTracker


class TestForecasting:
    """Test forecasting accuracy."""
    
    def test_forecast_structure(self, historical_tracker):
        """Test forecast returns correct structure."""
        forecast_df = historical_tracker.forecast_next_quarter("HBA1C")
        
        assert isinstance(forecast_df, pd.DataFrame)
        
        if not forecast_df.empty:
            required_cols = ['month', 'forecasted_success_rate', 'forecasted_interventions']
            for col in required_cols:
                assert col in forecast_df.columns
    
    def test_forecast_values_reasonable(self, historical_tracker):
        """Test forecast values are within reasonable bounds."""
        forecast_df = historical_tracker.forecast_next_quarter("HBA1C")
        
        if not forecast_df.empty:
            # Success rate should be 0-100%
            rates = forecast_df['forecasted_success_rate']
            assert (rates >= 0).all()
            assert (rates <= 100).all()
            
            # Interventions should be non-negative
            interventions = forecast_df['forecasted_interventions']
            assert (interventions >= 0).all()
    
    def test_forecast_handles_no_data(self, historical_tracker):
        """Test forecast handles missing data gracefully."""
        forecast_df = historical_tracker.forecast_next_quarter("NONEXISTENT")
        
        # Should return empty DataFrame, not raise exception
        assert isinstance(forecast_df, pd.DataFrame)


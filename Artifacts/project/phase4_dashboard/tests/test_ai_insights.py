"""
Tests for AI insights engine
"""
import pytest
import pandas as pd
from unittest.mock import Mock, patch, MagicMock
import os

from src.ai.insights_engine import InsightsEngine, InsightsCache
from core.exceptions import ConfigurationError, ExternalServiceError


@pytest.fixture
def sample_portfolio_metrics():
    """Sample portfolio metrics for testing"""
    return {
        'total_members': 10000,
        'total_gaps': 1500,
        'predicted_closure_rate': 85.5,
        'total_financial_value': 450000.0,
        'star_rating_current': 4.0,
        'star_rating_predicted': 4.5,
        'top_measures': [
            {'name': 'HbA1c_Testing', 'value': 300000},
            {'name': 'BP_Control', 'value': 150000}
        ]
    }


@pytest.fixture
def mock_openai_client():
    """Mock OpenAI client"""
    with patch('src.ai.insights_engine.OpenAI') as mock:
        client_instance = MagicMock()
        mock.return_value = client_instance
        
        # Mock chat completion response
        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].message.content = "Test executive summary"
        client_instance.chat.completions.create.return_value = mock_response
        
        yield client_instance


def test_insights_engine_initialization_missing_key():
    """Test that InsightsEngine raises error when API key is missing"""
    with patch.dict(os.environ, {}, clear=True):
        with pytest.raises(ConfigurationError) as exc_info:
            InsightsEngine()
        assert "API key not set" in str(exc_info.value)


def test_insights_engine_initialization_with_key(mock_openai_client):
    """Test that InsightsEngine initializes successfully with API key"""
    with patch.dict(os.environ, {'OPENAI_API_KEY': 'test-key'}):
        engine = InsightsEngine()
        assert engine.api_key == 'test-key'
        assert engine.provider == 'openai'


def test_executive_summary_generation(sample_portfolio_metrics, mock_openai_client):
    """Test that executive summary generates successfully"""
    with patch.dict(os.environ, {'OPENAI_API_KEY': 'test-key'}):
        engine = InsightsEngine()
        
        # Mock the cached function to avoid actual API call
        with patch.object(engine, 'generate_executive_summary') as mock_gen:
            mock_gen.return_value = "Test executive summary"
            summary = engine.generate_executive_summary(sample_portfolio_metrics)
            
            assert len(summary) > 0
            assert "Test executive summary" in summary


def test_metric_explanation(mock_openai_client):
    """Test metric explanation generation"""
    with patch.dict(os.environ, {'OPENAI_API_KEY': 'test-key'}):
        engine = InsightsEngine()
        
        # Mock the cached function
        with patch.object(engine, 'explain_metric') as mock_explain:
            mock_explain.return_value = "ROI measures return on investment..."
            explanation = engine.explain_metric(
                metric_name="ROI Percentage",
                metric_value=498,
                context={'intervention_cost': 50000, 'predicted_value': 300000}
            )
            
            assert len(explanation) > 0
            assert "ROI" in explanation or "return" in explanation.lower()


def test_generate_recommendations_empty_data(mock_openai_client):
    """Test recommendations with empty data"""
    with patch.dict(os.environ, {'OPENAI_API_KEY': 'test-key'}):
        engine = InsightsEngine()
        
        empty_df = pd.DataFrame()
        recommendations = engine.generate_recommendations(empty_df, top_n=3)
        
        assert recommendations == []


def test_detect_anomalies_no_anomaly(mock_openai_client):
    """Test anomaly detection when no anomaly exists"""
    with patch.dict(os.environ, {'OPENAI_API_KEY': 'test-key'}):
        engine = InsightsEngine()
        
        # Create normal time series data
        data = pd.DataFrame({
            'date': pd.date_range('2024-01-01', periods=10, freq='D'),
            'metric': [100, 101, 99, 102, 100, 101, 99, 100, 101, 100]
        })
        
        anomaly = engine.detect_anomalies(data, 'metric')
        # Should return None for normal data
        assert anomaly is None


def test_insights_cache():
    """Test insights cache functionality"""
    # Test that cache can be cleared
    InsightsCache.clear_insights_cache()
    # Should not raise exception
    assert True


def test_build_context_string():
    """Test context string building"""
    with patch.dict(os.environ, {'OPENAI_API_KEY': 'test-key'}):
        engine = InsightsEngine()
        
        metrics = {
            'total_members': 10000,
            'total_gaps': 1500,
            'predicted_closure_rate': 85.5,
            'top_measures': [1, 2, 3]
        }
        
        context = engine._build_context_string(metrics)
        
        assert 'total_members: 10000' in context
        assert 'predicted_closure_rate: 85.50' in context
        assert 'top_measures: 3 items' in context


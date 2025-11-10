"""
API Test Fixtures
Pytest fixtures for API testing.
"""

import pytest
from fastapi.testclient import TestClient
from typing import Dict, Any

# Import the FastAPI app
import sys
sys.path.append(".")
from src.api.main import app
from src.api.config import settings
from src.api.auth import api_key_manager


@pytest.fixture
def test_client():
    """
    Create a TestClient for the FastAPI app.
    """
    return TestClient(app)


@pytest.fixture
def valid_api_key():
    """
    Return a valid API key for testing.
    """
    # Return default dev key if in development
    if settings.environment == "development" and settings.default_api_key:
        return settings.default_api_key
    
    # Otherwise generate a test key
    test_key = "test-api-key-12345"
    api_key_manager.add_key(test_key, "Test Key", "test-001")
    return test_key


@pytest.fixture
def invalid_api_key():
    """
    Return an invalid API key for testing.
    """
    return "invalid-key-xyz"


@pytest.fixture
def api_headers(valid_api_key):
    """
    Return headers with valid API key.
    """
    return {"X-API-Key": valid_api_key}


@pytest.fixture
def sample_member_id():
    """
    Return a sample member ID for testing.
    """
    return "M123456"


@pytest.fixture
def sample_prediction_request(sample_member_id):
    """
    Return a sample prediction request payload.
    """
    return {
        "member_id": sample_member_id,
        "measurement_year": 2025,
        "include_shap": True
    }


@pytest.fixture
def sample_batch_request():
    """
    Return a sample batch prediction request payload.
    """
    return {
        "member_ids": ["M123456", "M789012", "M345678"],
        "measurement_year": 2025,
        "include_shap": False
    }


@pytest.fixture
def sample_portfolio_request(sample_member_id):
    """
    Return a sample portfolio prediction request payload.
    """
    return {
        "member_id": sample_member_id,
        "measures": ["GSD", "KED", "EED"],
        "include_shap": True,
        "measurement_year": 2025
    }


@pytest.fixture
def valid_measure_codes():
    """
    Return list of valid HEDIS measure codes.
    """
    return ["GSD", "KED", "EED", "PDC-DR", "BPD", "CBP", "SUPD", "PDC-RASA", "PDC-STA", "BCS", "COL", "HEI"]




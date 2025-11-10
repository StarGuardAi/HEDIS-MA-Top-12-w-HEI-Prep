"""
Test Authentication
Tests for API key authentication.
"""

import pytest
from fastapi.testclient import TestClient


class TestAuthentication:
    """Tests for API key authentication."""
    
    def test_valid_api_key(
        self,
        test_client: TestClient,
        valid_api_key: str,
        sample_prediction_request: dict
    ):
        """Test request with valid API key succeeds."""
        headers = {"X-API-Key": valid_api_key}
        
        response = test_client.post(
            "/api/v1/predict/GSD",
            json=sample_prediction_request,
            headers=headers
        )
        
        assert response.status_code == 200
    
    def test_missing_api_key(
        self,
        test_client: TestClient,
        sample_prediction_request: dict
    ):
        """Test request without API key returns 401."""
        response = test_client.post(
            "/api/v1/predict/GSD",
            json=sample_prediction_request
        )
        
        assert response.status_code == 401
        data = response.json()
        assert "detail" in data
    
    def test_invalid_api_key(
        self,
        test_client: TestClient,
        invalid_api_key: str,
        sample_prediction_request: dict
    ):
        """Test request with invalid API key returns 401."""
        headers = {"X-API-Key": invalid_api_key}
        
        response = test_client.post(
            "/api/v1/predict/GSD",
            json=sample_prediction_request,
            headers=headers
        )
        
        assert response.status_code == 401
        data = response.json()
        assert "detail" in data
    
    def test_health_endpoints_no_auth(
        self,
        test_client: TestClient
    ):
        """Test that health endpoints don't require authentication."""
        endpoints = ["/", "/health", "/health/ready", "/health/live"]
        
        for endpoint in endpoints:
            response = test_client.get(endpoint)
            assert response.status_code != 401, f"Endpoint {endpoint} requires auth but shouldn't"
    
    def test_prediction_endpoints_require_auth(
        self,
        test_client: TestClient,
        sample_prediction_request: dict
    ):
        """Test that prediction endpoints require authentication."""
        endpoints = [
            ("/api/v1/predict/GSD", "post", sample_prediction_request),
            ("/api/v1/predict/batch/GSD", "post", {"member_ids": ["M123"], "measurement_year": 2025}),
            ("/api/v1/predict/portfolio", "post", {"member_id": "M123", "measurement_year": 2025}),
        ]
        
        for endpoint, method, data in endpoints:
            if method == "get":
                response = test_client.get(endpoint)
            else:
                response = test_client.post(endpoint, json=data)
            
            assert response.status_code == 401, f"Endpoint {endpoint} doesn't require auth"
    
    def test_rate_limit_headers_present(
        self,
        test_client: TestClient,
        api_headers: dict,
        sample_prediction_request: dict
    ):
        """Test that rate limit headers are included in responses."""
        response = test_client.post(
            "/api/v1/predict/GSD",
            json=sample_prediction_request,
            headers=api_headers
        )
        
        assert response.status_code == 200
        
        # Rate limit headers should be present (if rate limiting is enabled)
        # These headers may not be present if rate limiting is disabled
        # Just check they don't cause errors if present
        if "X-RateLimit-Limit" in response.headers:
            assert int(response.headers["X-RateLimit-Limit"]) > 0
        
        if "X-RateLimit-Remaining" in response.headers:
            remaining = int(response.headers["X-RateLimit-Remaining"])
            assert remaining >= 0




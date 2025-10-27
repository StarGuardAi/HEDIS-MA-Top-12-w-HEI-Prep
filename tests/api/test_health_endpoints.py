"""
Test Health Check Endpoints
"""

import pytest
from fastapi.testclient import TestClient


def test_root_endpoint(test_client: TestClient):
    """Test root endpoint returns API information."""
    response = test_client.get("/")
    
    assert response.status_code == 200
    data = response.json()
    
    assert "name" in data
    assert "version" in data
    assert "status" in data
    assert data["status"] == "operational"


def test_health_check(test_client: TestClient):
    """Test basic health check endpoint."""
    response = test_client.get("/health")
    
    assert response.status_code == 200
    data = response.json()
    
    assert data["status"] == "healthy"
    assert "version" in data
    assert "environment" in data
    assert "timestamp" in data


def test_readiness_check_ready(test_client: TestClient):
    """Test readiness endpoint when API is ready."""
    response = test_client.get("/health/ready")
    
    # Should return 200 if models are loaded or loading is disabled
    assert response.status_code in [200, 503]
    data = response.json()
    
    assert "status" in data
    assert "timestamp" in data


def test_liveness_check(test_client: TestClient):
    """Test liveness endpoint (always returns alive)."""
    response = test_client.get("/health/live")
    
    assert response.status_code == 200
    data = response.json()
    
    assert data["status"] == "alive"
    assert "timestamp" in data


def test_health_endpoints_no_auth_required(test_client: TestClient):
    """Test that health endpoints don't require authentication."""
    # All health endpoints should work without API key
    endpoints = ["/", "/health", "/health/ready", "/health/live"]
    
    for endpoint in endpoints:
        response = test_client.get(endpoint)
        # Should not return 401 Unauthorized
        assert response.status_code != 401


def test_response_headers(test_client: TestClient):
    """Test that responses include expected headers."""
    response = test_client.get("/health")
    
    # Should have request ID header
    assert "X-Request-ID" in response.headers
    
    # Should have process time header
    assert "X-Process-Time-Ms" in response.headers
    
    # Process time should be reasonable (< 1000ms)
    process_time = float(response.headers["X-Process-Time-Ms"])
    assert process_time < 1000.0



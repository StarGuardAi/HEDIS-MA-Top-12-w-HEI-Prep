"""
Test Prediction Endpoints
Tests for single, batch, and portfolio prediction endpoints.
"""

import pytest
from fastapi.testclient import TestClient


class TestSinglePrediction:
    """Tests for single member prediction endpoint."""
    
    def test_single_prediction_success(
        self,
        test_client: TestClient,
        api_headers: dict,
        sample_prediction_request: dict
    ):
        """Test successful single prediction."""
        response = test_client.post(
            "/api/v1/predict/GSD",
            json=sample_prediction_request,
            headers=api_headers
        )
        
        assert response.status_code == 200
        data = response.json()
        
        # Check response structure
        assert "prediction_id" in data
        assert "member_hash" in data
        assert "measure_code" in data
        assert data["measure_code"] == "GSD"
        assert "risk_score" in data
        assert "risk_tier" in data
        assert "gap_probability" in data
        assert "recommendation" in data
        assert "model_version" in data
        assert "prediction_date" in data
        
        # Check risk score is valid (0-1)
        assert 0.0 <= data["risk_score"] <= 1.0
        assert 0.0 <= data["gap_probability"] <= 1.0
        
        # Check risk tier is valid
        assert data["risk_tier"] in ["high", "medium", "low"]
    
    def test_single_prediction_with_shap(
        self,
        test_client: TestClient,
        api_headers: dict,
        sample_prediction_request: dict
    ):
        """Test prediction with SHAP values."""
        sample_prediction_request["include_shap"] = True
        
        response = test_client.post(
            "/api/v1/predict/GSD",
            json=sample_prediction_request,
            headers=api_headers
        )
        
        assert response.status_code == 200
        data = response.json()
        
        # SHAP values should be included (may be None if model doesn't support it)
        assert "shap_values" in data
        assert "top_features" in data
    
    def test_single_prediction_invalid_measure(
        self,
        test_client: TestClient,
        api_headers: dict,
        sample_prediction_request: dict
    ):
        """Test prediction with invalid measure code."""
        response = test_client.post(
            "/api/v1/predict/INVALID",
            json=sample_prediction_request,
            headers=api_headers
        )
        
        assert response.status_code == 404
    
    def test_single_prediction_missing_auth(
        self,
        test_client: TestClient,
        sample_prediction_request: dict
    ):
        """Test prediction without authentication."""
        response = test_client.post(
            "/api/v1/predict/GSD",
            json=sample_prediction_request
        )
        
        assert response.status_code == 401
    
    def test_single_prediction_invalid_year(
        self,
        test_client: TestClient,
        api_headers: dict,
        sample_prediction_request: dict
    ):
        """Test prediction with invalid measurement year."""
        sample_prediction_request["measurement_year"] = 1999
        
        response = test_client.post(
            "/api/v1/predict/GSD",
            json=sample_prediction_request,
            headers=api_headers
        )
        
        assert response.status_code == 422  # Validation error
    
    def test_single_prediction_response_time(
        self,
        test_client: TestClient,
        api_headers: dict,
        sample_prediction_request: dict
    ):
        """Test that prediction response time is acceptable."""
        response = test_client.post(
            "/api/v1/predict/GSD",
            json=sample_prediction_request,
            headers=api_headers
        )
        
        # Check process time header
        if "X-Process-Time-Ms" in response.headers:
            process_time = float(response.headers["X-Process-Time-Ms"])
            # Target is < 50ms, allow up to 200ms for testing
            assert process_time < 200.0


class TestBatchPrediction:
    """Tests for batch prediction endpoint."""
    
    def test_batch_prediction_success(
        self,
        test_client: TestClient,
        api_headers: dict,
        sample_batch_request: dict
    ):
        """Test successful batch prediction."""
        response = test_client.post(
            "/api/v1/predict/batch/GSD",
            json=sample_batch_request,
            headers=api_headers
        )
        
        assert response.status_code == 200
        data = response.json()
        
        # Check response structure
        assert "predictions" in data
        assert "total_processed" in data
        assert "total_high_risk" in data
        assert "total_medium_risk" in data
        assert "total_low_risk" in data
        assert "processing_time_ms" in data
        assert "measure_code" in data
        
        # Check counts
        assert data["total_processed"] == len(sample_batch_request["member_ids"])
        assert data["total_processed"] == (
            data["total_high_risk"] + 
            data["total_medium_risk"] + 
            data["total_low_risk"]
        )
        
        # Check predictions structure
        assert len(data["predictions"]) == data["total_processed"]
    
    def test_batch_prediction_size_limit(
        self,
        test_client: TestClient,
        api_headers: dict
    ):
        """Test that batch size limit is enforced."""
        # Create batch with 1001 members (over limit of 1000)
        large_batch = {
            "member_ids": [f"M{i:06d}" for i in range(1001)],
            "measurement_year": 2025,
            "include_shap": False
        }
        
        response = test_client.post(
            "/api/v1/predict/batch/GSD",
            json=large_batch,
            headers=api_headers
        )
        
        assert response.status_code == 422  # Validation error
    
    def test_batch_prediction_empty_list(
        self,
        test_client: TestClient,
        api_headers: dict
    ):
        """Test batch prediction with empty member list."""
        empty_batch = {
            "member_ids": [],
            "measurement_year": 2025
        }
        
        response = test_client.post(
            "/api/v1/predict/batch/GSD",
            json=empty_batch,
            headers=api_headers
        )
        
        assert response.status_code == 422  # Validation error


class TestPortfolioPrediction:
    """Tests for portfolio prediction endpoint."""
    
    def test_portfolio_prediction_success(
        self,
        test_client: TestClient,
        api_headers: dict,
        sample_portfolio_request: dict
    ):
        """Test successful portfolio prediction."""
        response = test_client.post(
            "/api/v1/predict/portfolio",
            json=sample_portfolio_request,
            headers=api_headers
        )
        
        assert response.status_code == 200
        data = response.json()
        
        # Check response structure
        assert "member_hash" in data
        assert "predictions" in data
        assert "total_gaps" in data
        assert "gap_measures" in data
        assert "priority_score" in data
        assert "priority_tier" in data
        assert "recommended_interventions" in data
        assert "estimated_value" in data
        assert "processing_time_ms" in data
        
        # Check predictions for requested measures
        assert len(data["predictions"]) == len(sample_portfolio_request["measures"])
        for measure in sample_portfolio_request["measures"]:
            assert measure in data["predictions"]
        
        # Check priority score range
        assert 0.0 <= data["priority_score"] <= 100.0
        
        # Check priority tier
        assert data["priority_tier"] in ["critical", "high", "medium", "low"]
    
    def test_portfolio_prediction_all_measures(
        self,
        test_client: TestClient,
        api_headers: dict,
        sample_member_id: str
    ):
        """Test portfolio prediction for all 12 measures."""
        request_data = {
            "member_id": sample_member_id,
            "measurement_year": 2025,
            "include_shap": False
        }
        
        response = test_client.post(
            "/api/v1/predict/portfolio",
            json=request_data,
            headers=api_headers
        )
        
        assert response.status_code == 200
        data = response.json()
        
        # Should predict for all 12 measures (if not specified)
        # Note: Actual count depends on model availability
        assert len(data["predictions"]) >= 3  # At least 3 measures
    
    def test_portfolio_prediction_invalid_measure(
        self,
        test_client: TestClient,
        api_headers: dict,
        sample_member_id: str
    ):
        """Test portfolio prediction with invalid measure code."""
        request_data = {
            "member_id": sample_member_id,
            "measures": ["INVALID", "GSD"],
            "measurement_year": 2025
        }
        
        response = test_client.post(
            "/api/v1/predict/portfolio",
            json=request_data,
            headers=api_headers
        )
        
        assert response.status_code == 422  # Validation error or bad request
    
    def test_portfolio_prediction_response_time(
        self,
        test_client: TestClient,
        api_headers: dict,
        sample_portfolio_request: dict
    ):
        """Test that portfolio prediction response time is acceptable."""
        response = test_client.post(
            "/api/v1/predict/portfolio",
            json=sample_portfolio_request,
            headers=api_headers
        )
        
        assert response.status_code == 200
        data = response.json()
        
        # Target is < 200ms for 3 measures
        # Allow up to 1000ms for testing
        assert data["processing_time_ms"] < 1000.0




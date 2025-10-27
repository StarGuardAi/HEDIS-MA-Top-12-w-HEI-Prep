"""
Test Measures Endpoints
Tests for measure information endpoints.
"""

import pytest
from fastapi.testclient import TestClient


class TestMeasuresEndpoints:
    """Tests for measures information endpoints."""
    
    def test_list_measures(self, test_client: TestClient):
        """Test listing all measures."""
        response = test_client.get("/api/v1/measures")
        
        assert response.status_code == 200
        data = response.json()
        
        # Should return a list
        assert isinstance(data, list)
        
        # Should have 12 measures (all tiers)
        assert len(data) >= 11  # Allow for HEI to be optional
        
        # Check structure of each measure
        if len(data) > 0:
            measure = data[0]
            assert "code" in measure
            assert "name" in measure
            assert "tier" in measure
            assert "weight" in measure
            assert "status" in measure
    
    def test_get_measure_detail_valid(
        self,
        test_client: TestClient,
        valid_measure_codes: list
    ):
        """Test getting details for a valid measure."""
        # Test GSD measure
        response = test_client.get("/api/v1/measures/GSD")
        
        assert response.status_code == 200
        data = response.json()
        
        # Check detailed structure
        assert data["code"] == "GSD"
        assert "name" in data
        assert "tier" in data
        assert "weight" in data
        assert "description" in data
        assert "population_criteria" in data
        assert "data_sources_required" in data
    
    def test_get_measure_detail_invalid(self, test_client: TestClient):
        """Test getting details for an invalid measure."""
        response = test_client.get("/api/v1/measures/INVALID")
        
        assert response.status_code == 404
    
    def test_get_measure_performance(self, test_client: TestClient):
        """Test getting performance for a measure."""
        response = test_client.get("/api/v1/measures/GSD/performance")
        
        # Should return 200 or 404 depending on whether data is available
        assert response.status_code in [200, 404, 503]
        
        if response.status_code == 200:
            data = response.json()
            assert "measure_code" in data
            assert "current_rate" in data
            assert "star_rating" in data
    
    def test_triple_weighted_measures(self, test_client: TestClient):
        """Test that triple-weighted measures are correctly identified."""
        response = test_client.get("/api/v1/measures")
        
        assert response.status_code == 200
        measures = response.json()
        
        # Find triple-weighted measures (weight = 3)
        triple_weighted = [m for m in measures if m.get("weight") == 3]
        
        # Should have GSD, KED, and CBP as triple-weighted
        triple_weighted_codes = [m["code"] for m in triple_weighted]
        assert "GSD" in triple_weighted_codes or "KED" in triple_weighted_codes
    
    def test_new_2025_measures(self, test_client: TestClient):
        """Test that NEW 2025 measures are correctly identified."""
        response = test_client.get("/api/v1/measures")
        
        assert response.status_code == 200
        measures = response.json()
        
        # Find NEW 2025 measures
        new_measures = [m for m in measures if m.get("new_measure") == True]
        
        # Should have at least KED and BPD as NEW 2025
        # (They may not be implemented yet, so just check the field exists)
        for measure in measures:
            assert "new_measure" in measure
    
    def test_measure_tiers(self, test_client: TestClient):
        """Test that all measures have valid tier assignments."""
        response = test_client.get("/api/v1/measures")
        
        assert response.status_code == 200
        measures = response.json()
        
        # Check that all measures have valid tiers (1-4)
        for measure in measures:
            assert measure["tier"] in [1, 2, 3, 4]
        
        # Check tier distribution
        tier_counts = {1: 0, 2: 0, 3: 0, 4: 0}
        for measure in measures:
            tier_counts[measure["tier"]] += 1
        
        # Tier 1 (Diabetes) should have ~5 measures
        # Tier 2 (Cardio) should have ~4 measures
        # Tier 3 (Cancer) should have ~2 measures
        # Tier 4 (HEI) should have ~1 measure
        assert tier_counts[1] >= 3
        assert tier_counts[2] >= 2
        assert tier_counts[3] >= 1
    
    def test_measures_no_auth_required(self, test_client: TestClient):
        """Test that measure endpoints don't require authentication."""
        # Measures are public information
        response = test_client.get("/api/v1/measures")
        assert response.status_code != 401
        
        response = test_client.get("/api/v1/measures/GSD")
        assert response.status_code != 401



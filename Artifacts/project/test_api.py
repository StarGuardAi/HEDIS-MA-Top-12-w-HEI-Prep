"""
HEDIS API Test Script
Quick verification that the API is working correctly.
"""

import requests
import json
import time
from typing import Dict, Any

# API Configuration
BASE_URL = "http://localhost:8000"
API_KEY = "dev-key-12345"
HEADERS = {"X-API-Key": API_KEY}


def print_test_header(test_name: str):
    """Print a test header."""
    print("\n" + "="*80)
    print(f"TEST: {test_name}")
    print("="*80)


def print_result(success: bool, message: str, response: Dict[str, Any] = None):
    """Print test result."""
    status = "[PASS]" if success else "[FAIL]"
    print(f"{status} - {message}")
    if response and not success:
        print(f"Response: {json.dumps(response, indent=2)}")


def test_health_check():
    """Test health check endpoints."""
    print_test_header("Health Check Endpoints")
    
    try:
        # Test basic health
        response = requests.get(f"{BASE_URL}/health")
        success = response.status_code == 200
        print_result(success, f"GET /health - Status: {response.status_code}", response.json() if not success else None)
        if success:
            data = response.json()
            print(f"   Status: {data.get('status')}")
            print(f"   Version: {data.get('version')}")
        
        # Test readiness
        response = requests.get(f"{BASE_URL}/health/ready")
        success = response.status_code == 200
        print_result(success, f"GET /health/ready - Status: {response.status_code}", response.json() if not success else None)
        
        # Test liveness
        response = requests.get(f"{BASE_URL}/health/live")
        success = response.status_code == 200
        print_result(success, f"GET /health/live - Status: {response.status_code}", response.json() if not success else None)
        
        return True
    except requests.exceptions.ConnectionError:
        print_result(False, "Cannot connect to API. Is it running?")
        print("   Run: python -m uvicorn src.api.main:app --reload")
        return False
    except Exception as e:
        print_result(False, f"Error: {str(e)}")
        return False


def test_root_endpoint():
    """Test root endpoint."""
    print_test_header("Root Endpoint")
    
    try:
        response = requests.get(f"{BASE_URL}/")
        success = response.status_code == 200
        print_result(success, f"GET / - Status: {response.status_code}")
        if success:
            data = response.json()
            print(f"   Name: {data.get('name')}")
            print(f"   Version: {data.get('version')}")
            print(f"   Status: {data.get('status')}")
        return success
    except Exception as e:
        print_result(False, f"Error: {str(e)}")
        return False


def test_measures_endpoints():
    """Test measures endpoints."""
    print_test_header("Measures Endpoints")
    
    try:
        # List all measures
        response = requests.get(f"{BASE_URL}/api/v1/measures", headers=HEADERS)
        success = response.status_code == 200
        print_result(success, f"GET /api/v1/measures - Status: {response.status_code}")
        
        if success:
            measures = response.json()
            print(f"   Total Measures: {len(measures)}")
            print(f"   Measure Codes: {[m['code'] for m in measures]}")
            
            # Test measure details for GSD
            if measures:
                measure_code = "GSD"
                response = requests.get(f"{BASE_URL}/api/v1/measures/{measure_code}", headers=HEADERS)
                success = response.status_code == 200
                print_result(success, f"GET /api/v1/measures/{measure_code} - Status: {response.status_code}")
                if success:
                    data = response.json()
                    print(f"   Measure: {data.get('name')}")
                    print(f"   Tier: {data.get('tier')}")
                    print(f"   Weight: {data.get('weight')}x")
        
        return True
    except Exception as e:
        print_result(False, f"Error: {str(e)}")
        return False


def test_prediction_endpoints():
    """Test prediction endpoints."""
    print_test_header("Prediction Endpoints")
    
    try:
        # Test single prediction
        print("\nTesting Single Member Prediction...")
        response = requests.post(
            f"{BASE_URL}/api/v1/predict/GSD",
            headers=HEADERS,
            json={
                "member_id": "M123456",
                "measurement_year": 2025,
                "include_shap": True
            }
        )
        success = response.status_code == 200
        print_result(success, f"POST /api/v1/predict/GSD - Status: {response.status_code}")
        
        if success:
            data = response.json()
            print(f"   Member Hash: {data.get('member_hash')}")
            print(f"   Risk Score: {data.get('risk_score'):.3f}")
            print(f"   Risk Tier: {data.get('risk_tier')}")
            print(f"   Recommendation: {data.get('recommendation')[:80]}...")
            print(f"   Processing Time: {data.get('prediction_date')}")
        
        # Test batch prediction
        print("\nTesting Batch Prediction...")
        response = requests.post(
            f"{BASE_URL}/api/v1/predict/batch/GSD",
            headers=HEADERS,
            json={
                "member_ids": ["M001", "M002", "M003"],
                "measurement_year": 2025,
                "include_shap": False
            }
        )
        success = response.status_code == 200
        print_result(success, f"POST /api/v1/predict/batch/GSD - Status: {response.status_code}")
        
        if success:
            data = response.json()
            print(f"   Total Processed: {data.get('total_processed')}")
            print(f"   High Risk: {data.get('total_high_risk')}")
            print(f"   Processing Time: {data.get('processing_time_ms'):.2f}ms")
        
        # Test portfolio prediction
        print("\nTesting Portfolio Prediction...")
        response = requests.post(
            f"{BASE_URL}/api/v1/predict/portfolio",
            headers=HEADERS,
            json={
                "member_id": "M123456",
                "measures": ["GSD", "KED", "EED"],
                "include_shap": False
            }
        )
        success = response.status_code == 200
        print_result(success, f"POST /api/v1/predict/portfolio - Status: {response.status_code}")
        
        if success:
            data = response.json()
            print(f"   Total Gaps: {data.get('total_gaps')}")
            print(f"   Gap Measures: {data.get('gap_measures')}")
            print(f"   Priority Score: {data.get('priority_score'):.1f}")
            print(f"   Estimated Value: ${data.get('estimated_value'):,.0f}")
            print(f"   Processing Time: {data.get('processing_time_ms'):.2f}ms")
        
        return True
    except Exception as e:
        print_result(False, f"Error: {str(e)}")
        return False


def test_portfolio_endpoints():
    """Test portfolio endpoints."""
    print_test_header("Portfolio Endpoints")
    
    try:
        # Test portfolio summary
        print("\nTesting Portfolio Summary...")
        response = requests.get(f"{BASE_URL}/api/v1/portfolio/summary", headers=HEADERS)
        success = response.status_code == 200
        print_result(success, f"GET /api/v1/portfolio/summary - Status: {response.status_code}")
        
        if success:
            data = response.json()
            print(f"   Total Members: {data.get('total_members'):,}")
            print(f"   Total Gaps: {data.get('total_gaps'):,}")
            print(f"   Current Stars: {data.get('star_rating_current')}")
            print(f"   Projected Stars: {data.get('star_rating_projected')}")
            print(f"   Estimated Value: ${data.get('estimated_value'):,.0f}")
        
        # Test priority list
        print("\nTesting Priority List...")
        response = requests.get(
            f"{BASE_URL}/api/v1/portfolio/priority-list?limit=10",
            headers=HEADERS
        )
        success = response.status_code == 200
        print_result(success, f"GET /api/v1/portfolio/priority-list - Status: {response.status_code}")
        
        if success:
            data = response.json()
            print(f"   Priority Members: {data.get('total_members')}")
            print(f"   Total Value: ${data.get('total_value'):,.0f}")
            print(f"   Expected Closures: {data.get('expected_closures')}")
        
        return True
    except Exception as e:
        print_result(False, f"Error: {str(e)}")
        return False


def test_analytics_endpoints():
    """Test analytics endpoints."""
    print_test_header("Analytics Endpoints")
    
    try:
        # Test Star Rating calculation
        print("\nTesting Star Rating Calculation...")
        response = requests.post(
            f"{BASE_URL}/api/v1/analytics/star-rating",
            headers=HEADERS,
            json={
                "measure_rates": {
                    "GSD": 0.75,
                    "KED": 0.68,
                    "EED": 0.72,
                    "BPD": 0.70
                },
                "plan_size": 100000
            }
        )
        success = response.status_code == 200
        print_result(success, f"POST /api/v1/analytics/star-rating - Status: {response.status_code}")
        
        if success:
            data = response.json()
            print(f"   Overall Stars: {data.get('overall_stars')}")
            print(f"   Star Tier: {data.get('star_tier')}")
            print(f"   Revenue Estimate: ${data.get('revenue_estimate'):,.0f}")
        
        # Test ROI calculation
        print("\nTesting ROI Calculation...")
        response = requests.get(
            f"{BASE_URL}/api/v1/analytics/roi?plan_size=100000&gap_closure_rate=0.3",
            headers=HEADERS
        )
        success = response.status_code == 200
        print_result(success, f"GET /api/v1/analytics/roi - Status: {response.status_code}")
        
        if success:
            data = response.json()
            print(f"   Current Value: ${data.get('current_portfolio_value'):,.0f}")
            print(f"   Projected Value: ${data.get('projected_value_with_closures'):,.0f}")
            print(f"   Net ROI: {data.get('net_roi'):.1f}%")
            print(f"   5-Year Value: ${data.get('five_year_value'):,.0f}")
        
        return True
    except Exception as e:
        print_result(False, f"Error: {str(e)}")
        return False


def test_authentication():
    """Test authentication and rate limiting."""
    print_test_header("Authentication & Rate Limiting")
    
    try:
        # Test without API key
        print("\nTesting Missing API Key...")
        response = requests.get(f"{BASE_URL}/api/v1/measures")
        success = response.status_code == 401
        print_result(success, f"GET /api/v1/measures (no key) - Status: {response.status_code} (expected 401)")
        
        # Test with valid API key
        print("\nTesting Valid API Key...")
        response = requests.get(f"{BASE_URL}/api/v1/measures", headers=HEADERS)
        success = response.status_code == 200
        print_result(success, f"GET /api/v1/measures (with key) - Status: {response.status_code}")
        
        # Check rate limit headers
        if success:
            print(f"   Rate Limit: {response.headers.get('X-RateLimit-Limit', 'N/A')}")
            print(f"   Remaining: {response.headers.get('X-RateLimit-Remaining', 'N/A')}")
        
        return True
    except Exception as e:
        print_result(False, f"Error: {str(e)}")
        return False


def test_performance():
    """Test API performance."""
    print_test_header("Performance Testing")
    
    try:
        print("\nTesting Response Times...")
        
        # Test single prediction speed
        times = []
        for i in range(5):
            start = time.time()
            response = requests.post(
                f"{BASE_URL}/api/v1/predict/GSD",
                headers=HEADERS,
                json={"member_id": f"M{i:06d}", "include_shap": False}
            )
            elapsed = (time.time() - start) * 1000
            times.append(elapsed)
        
        avg_time = sum(times) / len(times)
        print(f"   Single Prediction Average: {avg_time:.2f}ms")
        print(f"   Min: {min(times):.2f}ms | Max: {max(times):.2f}ms")
        
        success = avg_time < 100  # Target < 100ms
        print_result(success, f"Response time < 100ms: {avg_time:.2f}ms")
        
        return True
    except Exception as e:
        print_result(False, f"Error: {str(e)}")
        return False


def main():
    """Run all API tests."""
    print("\n" + "="*80)
    print("HEDIS API TEST SUITE")
    print("="*80)
    print(f"Base URL: {BASE_URL}")
    print(f"API Key: {API_KEY}")
    print("="*80)
    
    # Run all tests
    results = {
        "Health Checks": test_health_check(),
        "Root Endpoint": test_root_endpoint(),
        "Measures": test_measures_endpoints(),
        "Predictions": test_prediction_endpoints(),
        "Portfolio": test_portfolio_endpoints(),
        "Analytics": test_analytics_endpoints(),
        "Authentication": test_authentication(),
        "Performance": test_performance(),
    }
    
    # Print summary
    print("\n" + "="*80)
    print("TEST SUMMARY")
    print("="*80)
    
    passed = sum(1 for result in results.values() if result)
    total = len(results)
    
    for test_name, result in results.items():
        status = "[PASS]" if result else "[FAIL]"
        print(f"{status} - {test_name}")
    
    print("="*80)
    print(f"Results: {passed}/{total} tests passed ({passed/total*100:.1f}%)")
    print("="*80)
    
    if passed == total:
        print("\nALL TESTS PASSED! API is working perfectly!")
    else:
        print("\nSome tests failed. Check the output above for details.")
    
    return passed == total


if __name__ == "__main__":
    try:
        success = main()
        exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\nTests interrupted by user")
        exit(1)


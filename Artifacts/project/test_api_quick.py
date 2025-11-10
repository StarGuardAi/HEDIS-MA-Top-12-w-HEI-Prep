"""
Quick API Test Script
Test the HEDIS API endpoints to verify functionality.
"""

import requests
import json

API_BASE = "http://localhost:8000"
API_KEY = "dev-key-12345"

def test_health():
    """Test health check endpoint."""
    print("\n" + "=" * 60)
    print("TEST 1: Health Check")
    print("=" * 60)
    
    r = requests.get(f"{API_BASE}/health")
    print(f"Status: {r.status_code}")
    print(f"Response: {json.dumps(r.json(), indent=2)}")
    return r.status_code == 200

def test_measures():
    """Test measures listing endpoint."""
    print("\n" + "=" * 60)
    print("TEST 2: List Measures (No Auth Required)")
    print("=" * 60)
    
    r = requests.get(f"{API_BASE}/api/v1/measures")
    print(f"Status: {r.status_code}")
    
    if r.status_code == 200:
        measures = r.json()
        print(f"\nFound {len(measures)} measures:\n")
        for m in measures[:5]:  # Show first 5
            weight = f"[{m['weight']}x]" if m['weight'] > 1 else ""
            new = "NEW" if m.get('new_measure') else ""
            print(f"  {m['code']}: {m['name']} {weight} {new}")
    
    return r.status_code == 200

def test_measure_detail():
    """Test measure detail endpoint."""
    print("\n" + "=" * 60)
    print("TEST 3: Get Measure Detail (GSD)")
    print("=" * 60)
    
    r = requests.get(f"{API_BASE}/api/v1/measures/GSD")
    print(f"Status: {r.status_code}")
    
    if r.status_code == 200:
        measure = r.json()
        print(f"\nMeasure: {measure['code']}")
        print(f"Name: {measure['name']}")
        print(f"Tier: {measure['tier']}")
        print(f"Weight: {measure['weight']}")
        print(f"Description: {measure['description'][:100]}...")
    
    return r.status_code == 200

def test_prediction_no_auth():
    """Test prediction endpoint without authentication (should fail)."""
    print("\n" + "=" * 60)
    print("TEST 4: Prediction Without Auth (Should Fail)")
    print("=" * 60)
    
    payload = {
        "member_id": "M123456",
        "measurement_year": 2025,
        "include_shap": False
    }
    
    r = requests.post(f"{API_BASE}/api/v1/predict/GSD", json=payload)
    print(f"Status: {r.status_code}")
    print(f"Expected: 401 (Unauthorized)")
    
    if r.status_code == 401:
        print("✅ Authentication is working correctly!")
        return True
    else:
        print("⚠️ Authentication may not be enforcing correctly")
        return False

def test_prediction_with_auth():
    """Test prediction endpoint with authentication."""
    print("\n" + "=" * 60)
    print("TEST 5: Single Member Prediction (With Auth)")
    print("=" * 60)
    
    headers = {"X-API-Key": API_KEY}
    payload = {
        "member_id": "M123456",
        "measurement_year": 2025,
        "include_shap": True
    }
    
    r = requests.post(
        f"{API_BASE}/api/v1/predict/GSD",
        headers=headers,
        json=payload
    )
    
    print(f"Status: {r.status_code}")
    
    if r.status_code == 200:
        pred = r.json()
        print(f"\nPrediction Results:")
        print(f"  Member Hash: {pred['member_hash']}")
        print(f"  Measure: {pred['measure_code']}")
        print(f"  Risk Tier: {pred['risk_tier'].upper()}")
        print(f"  Gap Probability: {pred['gap_probability']:.1%}")
        print(f"  Recommendation: {pred['recommendation'][:80]}...")
        
        if 'X-Process-Time-Ms' in r.headers:
            print(f"  Response Time: {r.headers['X-Process-Time-Ms']}ms")
    else:
        print(f"Error: {r.text}")
    
    return r.status_code == 200

def test_batch_prediction():
    """Test batch prediction endpoint."""
    print("\n" + "=" * 60)
    print("TEST 6: Batch Predictions (10 members)")
    print("=" * 60)
    
    headers = {"X-API-Key": API_KEY}
    payload = {
        "member_ids": [f"M{i:06d}" for i in range(100, 110)],
        "measurement_year": 2025,
        "include_shap": False
    }
    
    r = requests.post(
        f"{API_BASE}/api/v1/predict/batch/GSD",
        headers=headers,
        json=payload
    )
    
    print(f"Status: {r.status_code}")
    
    if r.status_code == 200:
        results = r.json()
        print(f"\nBatch Results:")
        print(f"  Total Processed: {results['total_processed']}")
        print(f"  High Risk: {results['total_high_risk']}")
        print(f"  Medium Risk: {results['total_medium_risk']}")
        print(f"  Low Risk: {results['total_low_risk']}")
        print(f"  Processing Time: {results['processing_time_ms']:.2f}ms")
    else:
        print(f"Error: {r.text}")
    
    return r.status_code == 200

def test_portfolio_prediction():
    """Test portfolio prediction endpoint."""
    print("\n" + "=" * 60)
    print("TEST 7: Portfolio Prediction (All Measures)")
    print("=" * 60)
    
    headers = {"X-API-Key": API_KEY}
    payload = {
        "member_id": "M123456",
        "measurement_year": 2025,
        "include_shap": False
    }
    
    r = requests.post(
        f"{API_BASE}/api/v1/predict/portfolio",
        headers=headers,
        json=payload
    )
    
    print(f"Status: {r.status_code}")
    
    if r.status_code == 200:
        portfolio = r.json()
        print(f"\nPortfolio Results:")
        print(f"  Member Hash: {portfolio['member_hash']}")
        print(f"  Total Gaps: {portfolio['total_gaps']}")
        print(f"  Gap Measures: {', '.join(portfolio['gap_measures'])}")
        print(f"  Priority Score: {portfolio['priority_score']:.1f}/100")
        print(f"  Priority Tier: {portfolio['priority_tier'].upper()}")
        print(f"  Processing Time: {portfolio['processing_time_ms']:.2f}ms")
    else:
        print(f"Error: {r.text}")
    
    return r.status_code == 200

def main():
    """Run all tests."""
    print("\n" + "=" * 60)
    print("  HEDIS API ENDPOINT TESTS")
    print("=" * 60)
    print(f"\nAPI Base URL: {API_BASE}")
    print(f"API Key: {API_KEY}")
    
    results = {}
    
    try:
        results['health'] = test_health()
        results['measures'] = test_measures()
        results['measure_detail'] = test_measure_detail()
        results['auth_check'] = test_prediction_no_auth()
        results['single_prediction'] = test_prediction_with_auth()
        results['batch_prediction'] = test_batch_prediction()
        results['portfolio_prediction'] = test_portfolio_prediction()
        
        # Summary
        print("\n" + "=" * 60)
        print("  TEST SUMMARY")
        print("=" * 60)
        
        passed = sum(1 for v in results.values() if v)
        total = len(results)
        
        for test_name, result in results.items():
            status = "✅ PASSED" if result else "❌ FAILED"
            print(f"{test_name:25s} {status}")
        
        print("\n" + "=" * 60)
        print(f"  TOTAL: {passed}/{total} tests passed")
        print("=" * 60)
        
        if passed == total:
            print("\n🎉 ALL TESTS PASSED! API is working correctly!")
        else:
            print(f"\n⚠️ {total - passed} test(s) failed. Check errors above.")
        
    except requests.exceptions.ConnectionError:
        print("\n❌ ERROR: Could not connect to API")
        print("Make sure the API server is running:")
        print("  uvicorn src.api.main:app --reload")
    except Exception as e:
        print(f"\n❌ ERROR: {e}")

if __name__ == "__main__":
    main()




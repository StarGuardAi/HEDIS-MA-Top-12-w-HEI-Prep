"""
HEDIS API Usage Examples
Practical examples for using the HEDIS Star Rating Portfolio Optimizer API.

Author: Robert Reichert
"""

import requests
import json
from typing import List, Dict, Any


# ===== Configuration =====

API_BASE_URL = "http://localhost:8000"
API_KEY = "dev-key-12345"  # Development API key

HEADERS = {
    "X-API-Key": API_KEY,
    "Content-Type": "application/json"
}


# ===== Helper Functions =====

def print_section(title: str):
    """Print a section header."""
    print("\n" + "=" * 70)
    print(f"  {title}")
    print("=" * 70)


def print_response(response: requests.Response):
    """Pretty print API response."""
    print(f"Status Code: {response.status_code}")
    if response.status_code == 200:
        print(json.dumps(response.json(), indent=2))
    else:
        print(f"Error: {response.text}")


# ===== Example 1: Health Check =====

def example_health_check():
    """Example 1: Check API health status."""
    print_section("Example 1: Health Check")
    
    response = requests.get(f"{API_BASE_URL}/health")
    
    if response.status_code == 200:
        data = response.json()
        print(f"✅ API Status: {data['status']}")
        print(f"Version: {data['version']}")
        print(f"Environment: {data['environment']}")
    else:
        print(f"❌ API is not healthy: {response.status_code}")


# ===== Example 2: List All Measures =====

def example_list_measures():
    """Example 2: Get list of all HEDIS measures."""
    print_section("Example 2: List All Measures")
    
    response = requests.get(f"{API_BASE_URL}/api/v1/measures")
    
    if response.status_code == 200:
        measures = response.json()
        print(f"Found {len(measures)} measures:\n")
        
        # Group by tier
        tiers = {1: [], 2: [], 3: [], 4: []}
        for measure in measures:
            tiers[measure['tier']].append(measure)
        
        for tier_num, tier_measures in tiers.items():
            if tier_measures:
                print(f"Tier {tier_num}:")
                for m in tier_measures:
                    weight_str = f"[{m['weight']}x]" if m['weight'] > 1 else ""
                    new_str = "NEW 2025" if m.get('new_measure') else ""
                    print(f"  {m['code']}: {m['name']} {weight_str} {new_str}")
                print()


# ===== Example 3: Single Member Prediction =====

def example_single_prediction():
    """Example 3: Predict gap probability for single member."""
    print_section("Example 3: Single Member Prediction")
    
    member_id = "M123456"
    measure_code = "GSD"
    
    payload = {
        "member_id": member_id,
        "measurement_year": 2025,
        "include_shap": True
    }
    
    response = requests.post(
        f"{API_BASE_URL}/api/v1/predict/{measure_code}",
        headers=HEADERS,
        json=payload
    )
    
    if response.status_code == 200:
        pred = response.json()
        print(f"Measure: {pred['measure_code']}")
        print(f"Member Hash: {pred['member_hash']}")
        print(f"Risk Tier: {pred['risk_tier'].upper()}")
        print(f"Gap Probability: {pred['gap_probability']:.1%}")
        print(f"\nRecommendation:")
        print(f"  {pred['recommendation']}")
        
        if pred.get('top_features'):
            print(f"\nTop Influential Features:")
            for feat in pred['top_features'][:3]:
                print(f"  - {feat['name']}: {feat.get('value', 'N/A')} (impact: {feat['impact']:.3f})")
    else:
        print(f"Error: {response.status_code}")
        print(response.text)


# ===== Example 4: Batch Predictions =====

def example_batch_prediction():
    """Example 4: Batch predictions for multiple members."""
    print_section("Example 4: Batch Predictions")
    
    # Generate 10 sample member IDs
    member_ids = [f"M{i:06d}" for i in range(100, 110)]
    measure_code = "KED"
    
    payload = {
        "member_ids": member_ids,
        "measurement_year": 2025,
        "include_shap": False  # Faster without SHAP
    }
    
    response = requests.post(
        f"{API_BASE_URL}/api/v1/predict/batch/{measure_code}",
        headers=HEADERS,
        json=payload
    )
    
    if response.status_code == 200:
        results = response.json()
        print(f"Measure: {results['measure_code']}")
        print(f"Total Processed: {results['total_processed']}")
        print(f"High Risk: {results['total_high_risk']}")
        print(f"Medium Risk: {results['total_medium_risk']}")
        print(f"Low Risk: {results['total_low_risk']}")
        print(f"Processing Time: {results['processing_time_ms']:.2f}ms")
        
        # Show high-risk members
        high_risk = [p for p in results['predictions'] if p['risk_tier'] == 'high']
        if high_risk:
            print(f"\nHigh-Risk Members ({len(high_risk)}):")
            for pred in high_risk[:5]:  # Show first 5
                print(f"  - {pred['member_hash']}: {pred['gap_probability']:.1%}")
    else:
        print(f"Error: {response.status_code}")
        print(response.text)


# ===== Example 5: Portfolio Prediction =====

def example_portfolio_prediction():
    """Example 5: Complete risk profile across all measures."""
    print_section("Example 5: Portfolio Prediction")
    
    member_id = "M123456"
    
    payload = {
        "member_id": member_id,
        "measurement_year": 2025,
        "include_shap": False
    }
    
    response = requests.post(
        f"{API_BASE_URL}/api/v1/predict/portfolio",
        headers=HEADERS,
        json=payload
    )
    
    if response.status_code == 200:
        portfolio = response.json()
        print(f"Member Hash: {portfolio['member_hash']}")
        print(f"Total Gaps: {portfolio['total_gaps']}")
        print(f"Gap Measures: {', '.join(portfolio['gap_measures'])}")
        print(f"Priority Score: {portfolio['priority_score']:.1f}/100")
        print(f"Priority Tier: {portfolio['priority_tier'].upper()}")
        print(f"Estimated Value: ${portfolio['estimated_value']:.2f}")
        print(f"Processing Time: {portfolio['processing_time_ms']:.2f}ms")
        
        print(f"\nPredictions by Measure:")
        for measure_code, pred in portfolio['predictions'].items():
            print(f"  {measure_code}: {pred['risk_tier']} ({pred['gap_probability']:.1%})")
        
        if portfolio['recommended_interventions']:
            print(f"\nRecommended Interventions:")
            for intervention in portfolio['recommended_interventions']:
                print(f"  - {intervention}")
    else:
        print(f"Error: {response.status_code}")
        print(response.text)


# ===== Example 6: Portfolio Summary =====

def example_portfolio_summary():
    """Example 6: Get portfolio-level summary statistics."""
    print_section("Example 6: Portfolio Summary")
    
    response = requests.get(
        f"{API_BASE_URL}/api/v1/portfolio/summary",
        headers=HEADERS
    )
    
    if response.status_code == 200:
        summary = response.json()
        print(f"Total Members: {summary['total_members']:,}")
        print(f"Total Gaps: {summary['total_gaps']:,}")
        print(f"Current Star Rating: {summary['star_rating_current']:.1f}")
        print(f"Projected Star Rating: {summary['star_rating_projected']:.1f}")
        print(f"Estimated Value: ${summary['estimated_value']:,.0f}")
        
        print(f"\nGaps by Measure:")
        for measure, count in summary['gaps_by_measure'].items():
            print(f"  {measure}: {count:,}")
        
        print(f"\nGaps by Tier:")
        for tier, count in summary['gaps_by_tier'].items():
            print(f"  Tier {tier}: {count:,}")
    else:
        print(f"Error: {response.status_code}")
        print(response.text)


# ===== Example 7: Star Rating Calculation =====

def example_star_rating():
    """Example 7: Calculate Star Rating from measure rates."""
    print_section("Example 7: Star Rating Calculation")
    
    payload = {
        "measure_rates": {
            "GSD": 0.75,
            "KED": 0.70,
            "EED": 0.65,
            "PDC-DR": 0.80,
            "BPD": 0.78,
            "CBP": 0.82,
            "SUPD": 0.88,
            "PDC-RASA": 0.85,
            "PDC-STA": 0.83,
            "BCS": 0.72,
            "COL": 0.68
        },
        "hei_factor": 1.0  # No HEI adjustment
    }
    
    response = requests.post(
        f"{API_BASE_URL}/api/v1/analytics/star-rating",
        headers=HEADERS,
        json=payload
    )
    
    if response.status_code == 200:
        stars = response.json()
        print(f"Overall Star Rating: {stars['overall_stars']:.1f} ⭐")
        print(f"Total Points: {stars['total_points']:.2f}")
        print(f"Revenue Estimate: ${stars['revenue_estimate']:,.0f}")
        
        print(f"\nMeasure-Level Stars:")
        for measure, rating in stars['measure_stars'].items():
            print(f"  {measure}: {rating:.1f} ⭐")
    else:
        print(f"Error: {response.status_code}")
        print(response.text)


# ===== Example 8: Scenario Simulation =====

def example_simulation():
    """Example 8: Simulate gap closure scenarios."""
    print_section("Example 8: Scenario Simulation")
    
    payload = {
        "baseline_rates": {
            "GSD": 0.75,
            "KED": 0.70,
            "EED": 0.65,
            "CBP": 0.80
        },
        "closure_scenarios": [0.1, 0.2, 0.3],  # 10%, 20%, 30%
        "strategy": "triple_weighted"
    }
    
    response = requests.post(
        f"{API_BASE_URL}/api/v1/analytics/simulate",
        headers=HEADERS,
        json=payload
    )
    
    if response.status_code == 200:
        sim = response.json()
        print(f"Recommended Strategy: {sim['recommended_strategy']}")
        
        print(f"\nScenario Results:")
        for scenario in sim['scenarios']:
            print(f"\n  {scenario['closure_rate']:.0%} Gap Closure:")
            print(f"    Projected Stars: {scenario['projected_stars']:.1f}")
            print(f"    Revenue Impact: ${scenario['revenue_impact']:,.0f}")
            print(f"    Investment: ${scenario['investment_required']:,.0f}")
            print(f"    ROI: {scenario['roi']:.1f}%")
    else:
        print(f"Error: {response.status_code}")
        print(response.text)


# ===== Main Execution =====

def main():
    """Run all examples."""
    print("\n" + "=" * 70)
    print("  HEDIS Star Rating Portfolio Optimizer - API Examples")
    print("=" * 70)
    print(f"\nAPI Base URL: {API_BASE_URL}")
    print(f"API Key: {API_KEY}")
    
    try:
        # Run examples
        example_health_check()
        example_list_measures()
        example_single_prediction()
        example_batch_prediction()
        example_portfolio_prediction()
        example_portfolio_summary()
        example_star_rating()
        example_simulation()
        
        print("\n" + "=" * 70)
        print("  ✅ All Examples Completed Successfully!")
        print("=" * 70)
        
    except requests.exceptions.ConnectionError:
        print("\n❌ ERROR: Could not connect to API")
        print("Make sure the API server is running:")
        print("  uvicorn src.api.main:app --reload")
    except Exception as e:
        print(f"\n❌ ERROR: {e}")


if __name__ == "__main__":
    main()




import requests
import time

print("\n" + "="*60)
print("TESTING HEDIS API AFTER FIX")
print("="*60)

# Wait a moment for auto-reload
print("\nWaiting for API to reload...")
time.sleep(2)

# Test 1: Measures List
print("\n1. Testing Measures List...")
r = requests.get('http://localhost:8000/api/v1/measures')
print(f"Status: {r.status_code}")
if r.status_code == 200:
    measures = r.json()
    print(f"SUCCESS! Found {len(measures)} measures")
    for m in measures[:3]:
        print(f"  - {m['code']}: {m['name']}")
else:
    print(f"FAILED: {r.text}")

# Test 2: Single Measure Detail
print("\n2. Testing Single Measure (GSD)...")
r = requests.get('http://localhost:8000/api/v1/measures/GSD')
print(f"Status: {r.status_code}")
if r.status_code == 200:
    print("SUCCESS! GSD measure details retrieved")
else:
    print(f"FAILED: {r.text}")

# Test 3: Prediction with Auth
print("\n3. Testing Prediction (with API key)...")
headers = {"X-API-Key": "dev-key-12345"}
payload = {"member_id": "M123456", "measurement_year": 2025}
r = requests.post('http://localhost:8000/api/v1/predict/GSD', headers=headers, json=payload)
print(f"Status: {r.status_code}")
if r.status_code == 200:
    pred = r.json()
    print(f"SUCCESS! Risk Tier: {pred['risk_tier']}, Probability: {pred['gap_probability']:.1%}")
else:
    print(f"FAILED: {r.text[:200]}")

print("\n" + "="*60)
print("TESTING COMPLETE!")
print("="*60)



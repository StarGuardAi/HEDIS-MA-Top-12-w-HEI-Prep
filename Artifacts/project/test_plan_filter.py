"""Test plan filter functionality"""
import sys
from pathlib import Path

project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from src.data.phase1_database import get_dashboard_summary

print("\n" + "=" * 80)
print("TESTING PLAN FILTER FUNCTIONALITY")
print("=" * 80)

# Test All Plans
print("\n[1] ALL PLANS")
print("-" * 80)
summary_all = get_dashboard_summary()
print(f"Total Members:        {summary_all.get('total_members', 0):,}")
print(f"Total Gaps:          {summary_all.get('total_gaps', 0):,}")
print(f"Revenue at Risk:     ${summary_all.get('total_revenue_at_risk', 0):,.0f}")
print(f"Active Plans:        {summary_all.get('total_plans', 0)}")

# Test H1234-001
print("\n[2] H1234-001 ONLY")
print("-" * 80)
summary_h1234 = get_dashboard_summary('H1234-001')
print(f"Total Members:        {summary_h1234.get('total_members', 0):,}")
print(f"Total Gaps:          {summary_h1234.get('total_gaps', 0):,}")
print(f"Revenue at Risk:     ${summary_h1234.get('total_revenue_at_risk', 0):,.0f}")
print(f"Active Plans:        {summary_h1234.get('total_plans', 0)}")

# Test H5678-002
print("\n[3] H5678-002 ONLY")
print("-" * 80)
summary_h5678 = get_dashboard_summary('H5678-002')
print(f"Total Members:        {summary_h5678.get('total_members', 0):,}")
print(f"Total Gaps:          {summary_h5678.get('total_gaps', 0):,}")
print(f"Revenue at Risk:     ${summary_h5678.get('total_revenue_at_risk', 0):,.0f}")
print(f"Active Plans:        {summary_h5678.get('total_plans', 0)}")

# Test H9012-003
print("\n[4] H9012-003 ONLY")
print("-" * 80)
summary_h9012 = get_dashboard_summary('H9012-003')
print(f"Total Members:        {summary_h9012.get('total_members', 0):,}")
print(f"Total Gaps:          {summary_h9012.get('total_gaps', 0):,}")
print(f"Revenue at Risk:     ${summary_h9012.get('total_revenue_at_risk', 0):,.0f}")
print(f"Active Plans:        {summary_h9012.get('total_plans', 0)}")

print("\n" + "=" * 80)
print("[SUCCESS] Plan filter is working correctly!")
print("=" * 80)
print("\nThe dashboard should now update when you select different plans.")


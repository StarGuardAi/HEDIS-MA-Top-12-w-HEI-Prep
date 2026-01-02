"""Test Phase 1 Dashboard Data"""
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from src.data.phase1_database import (
    get_revenue_at_risk,
    get_dashboard_summary,
    get_cost_per_closure,
    get_member_segmentation,
    test_connection
)
import pandas as pd

print("\n" + "=" * 80)
print("PHASE 1 DATABASE - DASHBOARD DATA PREVIEW")
print("=" * 80)

# Test connection
print("\n[1] DATABASE CONNECTION TEST")
print("-" * 80)
if test_connection():
    print("[OK] Connection: SUCCESS")
else:
    print("[FAIL] Connection: FAILED")
    sys.exit(1)

# Dashboard Summary
print("\n[2] DASHBOARD SUMMARY METRICS")
print("-" * 80)
summary = get_dashboard_summary()
print(f"Total Members:        {summary.get('total_members', 0):,}")
print(f"Total Care Gaps:      {summary.get('total_gaps', 0):,}")
print(f"Total Revenue at Risk: ${summary.get('total_revenue_at_risk', 0):,.0f}")
print(f"Active Plans:         {summary.get('total_plans', 0)}")
print(f"Measures Tracked:     {summary.get('measure_count', 0)}")

# Top Revenue at Risk
print("\n[3] TOP 5 REVENUE AT RISK MEASURES")
print("-" * 80)
rar = get_revenue_at_risk()
top5 = rar.head(5)[['plan_name', 'measure_name', 'revenue_at_risk', 'members_needed', 'current_rate_pct']]
for idx, row in top5.iterrows():
    print(f"{row['plan_name'][:20]:<20} | {row['measure_name'][:35]:<35} | ${row['revenue_at_risk']:>10,.0f} | {row['members_needed']:>6,} members | {row['current_rate_pct']:>5.1f}%")

# Cost Analysis
print("\n[4] COST PER CLOSURE SUMMARY")
print("-" * 80)
cost = get_cost_per_closure()
if not cost.empty:
    cost_summary = cost.groupby('plan_name').agg({
        'total_gaps_closed': 'sum',
        'total_intervention_cost': 'sum',
        'cost_per_gap_closed': 'mean'
    }).reset_index()
    for idx, row in cost_summary.iterrows():
        print(f"{row['plan_name'][:25]:<25} | {row['total_gaps_closed']:>6,} closures | ${row['total_intervention_cost']:>10,.0f} total | ${row['cost_per_gap_closed']:>6.2f} avg/closure")

# Member Segmentation
print("\n[5] MEMBER SEGMENTATION SAMPLE")
print("-" * 80)
seg = get_member_segmentation()
if not seg.empty:
    top_segments = seg.head(5)[['plan_name', 'risk_category', 'age_band', 'member_count', 'gaps_per_member']]
    for idx, row in top_segments.iterrows():
        print(f"{row['plan_name'][:20]:<20} | {row['risk_category']:<15} | {row['age_band']:<8} | {row['member_count']:>5,} members | {row['gaps_per_member']:>4.2f} gaps/member")

print("\n" + "=" * 80)
print("[SUCCESS] All dashboard data queries successful!")
print("=" * 80)
print("\nIn Streamlit Dashboard, you'll see:")
print("   - Interactive charts for all this data")
print("   - Plan filtering capabilities")
print("   - Real-time data refresh")
print("   - Detailed drill-down views")
print("\nAccess at: http://localhost:8501")
print("Navigate to: Phase 1 Database (in sidebar)")


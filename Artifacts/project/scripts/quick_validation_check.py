#!/usr/bin/env python3
"""
Quick Validation Check - Run key validation tests and report status
"""

import sys
import os
from pathlib import Path

try:
    import psycopg2
    from psycopg2.extras import RealDictCursor
except ImportError:
    print("ERROR: psycopg2 not installed")
    sys.exit(1)


def get_db_config():
    """Get database configuration."""
    return {
        "host": os.getenv("DB_HOST", "localhost"),
        "database": os.getenv("DB_NAME", "hedis_portfolio"),
        "user": os.getenv("DB_USER", "hedis_api"),
        "password": os.getenv("DB_PASSWORD", "hedis_password"),
        "port": os.getenv("DB_PORT", "5432")
    }


def run_validation_checks():
    """Run key validation checks."""
    db_config = get_db_config()
    
    try:
        conn = psycopg2.connect(**db_config)
        cur = conn.cursor(cursor_factory=RealDictCursor)
        
        results = {
            'passed': 0,
            'warnings': 0,
            'failed': 0,
            'tests': []
        }
        
        print("=" * 80)
        print("QUICK VALIDATION CHECK")
        print("=" * 80)
        print()
        
        # Test 1: Database Objects
        print("SECTION 1: SYSTEM HEALTH")
        print("-" * 80)
        
        cur.execute("""
            SELECT COUNT(*) as count FROM information_schema.tables 
            WHERE table_schema = 'public' AND table_type = 'BASE TABLE'
        """)
        table_count = cur.fetchone()['count']
        status = "PASS" if table_count >= 30 else "FAIL"
        print(f"  [{'OK' if status == 'PASS' else 'FAIL'}] Tables: {table_count} (expected: 30+)")
        if status == "PASS":
            results['passed'] += 1
        else:
            results['failed'] += 1
        
        cur.execute("""
            SELECT COUNT(*) as count FROM information_schema.views 
            WHERE table_schema = 'public'
        """)
        view_count = cur.fetchone()['count']
        status = "PASS" if view_count >= 25 else "WARN"
        print(f"  [{'OK' if status == 'PASS' else 'WARN'}] Views: {view_count} (expected: 25+)")
        if status == "PASS":
            results['passed'] += 1
        elif status == "WARN":
            results['warnings'] += 1
        
        # Test 2: Phase 1 Foundation
        print()
        print("SECTION 2: PHASE 1 FOUNDATION")
        print("-" * 80)
        
        cur.execute("SELECT COUNT(*) as count FROM plan_members WHERE member_id LIKE 'M%'")
        member_count = cur.fetchone()['count']
        status = "PASS" if member_count == 10000 else "FAIL"
        print(f"  [{'OK' if status == 'PASS' else 'FAIL'}] Members: {member_count:,} (expected: 10,000)")
        if status == "PASS":
            results['passed'] += 1
        else:
            results['failed'] += 1
        
        cur.execute("SELECT COUNT(*) as count FROM member_gaps WHERE member_id LIKE 'M%'")
        gap_count = cur.fetchone()['count']
        status = "PASS" if 12000 <= gap_count <= 18000 else "WARN"
        print(f"  [{'OK' if status == 'PASS' else 'WARN'}] Care Gaps: {gap_count:,} (expected: 12K-18K)")
        if status == "PASS":
            results['passed'] += 1
        elif status == "WARN":
            results['warnings'] += 1
        
        cur.execute("SELECT COUNT(*) as count FROM hedis_measures")
        measure_count = cur.fetchone()['count']
        status = "PASS" if measure_count == 12 else "FAIL"
        print(f"  [{'OK' if status == 'PASS' else 'FAIL'}] HEDIS Measures: {measure_count} (expected: 12)")
        if status == "PASS":
            results['passed'] += 1
        else:
            results['failed'] += 1
        
        # Test 3: Phase 2 Operations
        print()
        print("SECTION 3: PHASE 2 OPERATIONS")
        print("-" * 80)
        
        cur.execute("SELECT COUNT(*) as count FROM member_engagement_scores")
        engagement_count = cur.fetchone()['count']
        status = "PASS" if engagement_count == 10000 else "FAIL"
        print(f"  [{'OK' if status == 'PASS' else 'FAIL'}] Engagement Scores: {engagement_count:,} (expected: 10,000)")
        if status == "PASS":
            results['passed'] += 1
        else:
            results['failed'] += 1
        
        cur.execute("SELECT COUNT(*) as count FROM provider_directory WHERE network_status = 'Active'")
        provider_count = cur.fetchone()['count']
        status = "PASS" if provider_count >= 500 else "FAIL"
        print(f"  [{'OK' if status == 'PASS' else 'FAIL'}] Active Providers: {provider_count} (expected: 500+)")
        if status == "PASS":
            results['passed'] += 1
        else:
            results['failed'] += 1
        
        cur.execute("SELECT COUNT(*) as count FROM member_risk_stratification")
        risk_count = cur.fetchone()['count']
        status = "PASS" if risk_count == 10000 else "FAIL"
        print(f"  [{'OK' if status == 'PASS' else 'FAIL'}] Risk Stratifications: {risk_count:,} (expected: 10,000)")
        if status == "PASS":
            results['passed'] += 1
        else:
            results['failed'] += 1
        
        cur.execute("SELECT COUNT(*) as count FROM gap_closure_propensity")
        propensity_count = cur.fetchone()['count']
        status = "PASS" if propensity_count >= 8000 else "WARN"
        print(f"  [{'OK' if status == 'PASS' else 'WARN'}] Propensity Scores: {propensity_count:,} (expected: 8,000+)")
        if status == "PASS":
            results['passed'] += 1
        elif status == "WARN":
            results['warnings'] += 1
        
        cur.execute("SELECT COUNT(*) as count FROM member_cost_predictions")
        cost_count = cur.fetchone()['count']
        status = "PASS" if cost_count == 10000 else "FAIL"
        print(f"  [{'OK' if status == 'PASS' else 'FAIL'}] Cost Predictions: {cost_count:,} (expected: 10,000)")
        if status == "PASS":
            results['passed'] += 1
        else:
            results['failed'] += 1
        
        # Test 4: Dashboards
        print()
        print("SECTION 4: DASHBOARDS")
        print("-" * 80)
        
        cur.execute("""
            SELECT COUNT(*) as count FROM pg_views 
            WHERE schemaname = 'public' AND viewname LIKE 'vw_%'
        """)
        dashboard_count = cur.fetchone()['count']
        status = "PASS" if dashboard_count >= 25 else "WARN"
        print(f"  [{'OK' if status == 'PASS' else 'WARN'}] Dashboard Views: {dashboard_count} (expected: 25+)")
        if status == "PASS":
            results['passed'] += 1
        elif status == "WARN":
            results['warnings'] += 1
        
        # Test 5: Data Quality
        print()
        print("SECTION 5: DATA QUALITY")
        print("-" * 80)
        
        cur.execute("""
            SELECT COUNT(*) as count FROM member_gaps mg
            WHERE NOT EXISTS (
                SELECT 1 FROM plan_members pm WHERE pm.member_id = mg.member_id
            )
        """)
        orphan_count = cur.fetchone()['count']
        status = "PASS" if orphan_count == 0 else "FAIL"
        print(f"  [{'OK' if status == 'PASS' else 'FAIL'}] Orphaned Records: {orphan_count} (expected: 0)")
        if status == "PASS":
            results['passed'] += 1
        else:
            results['failed'] += 1
        
        # Summary
        print()
        print("=" * 80)
        print("VALIDATION SUMMARY")
        print("=" * 80)
        total = results['passed'] + results['warnings'] + results['failed']
        print(f"Total Tests: {total}")
        print(f"  [PASS] {results['passed']} ({results['passed']/total*100:.1f}%)")
        print(f"  [WARN] {results['warnings']} ({results['warnings']/total*100:.1f}%)")
        print(f"  [FAIL] {results['failed']} ({results['failed']/total*100:.1f}%)")
        print()
        
        if results['failed'] == 0:
            if results['warnings'] == 0:
                print("[SUCCESS] All tests passed! System is production-ready.")
            else:
                print("[SUCCESS] All critical tests passed. Some warnings to review.")
        else:
            print(f"[WARNING] {results['failed']} test(s) failed. Review above.")
        
        print("=" * 80)
        
        conn.close()
        return results['failed'] == 0
        
    except psycopg2.Error as e:
        print(f"[ERROR] Database connection failed: {e}")
        return False


if __name__ == "__main__":
    success = run_validation_checks()
    sys.exit(0 if success else 1)


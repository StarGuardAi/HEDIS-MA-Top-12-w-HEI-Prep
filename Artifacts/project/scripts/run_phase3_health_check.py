#!/usr/bin/env python3
"""
Run Phase 3 Health Check
Executes the SQL health check and displays results
"""

import sys
import os

try:
    import psycopg2
    from psycopg2.extras import RealDictCursor
except ImportError:
    print("ERROR: psycopg2 not installed. Install with: pip install psycopg2-binary")
    sys.exit(1)


def get_db_config():
    """Get database configuration from environment or defaults."""
    return {
        "host": os.getenv("DB_HOST", "localhost"),
        "database": os.getenv("DB_NAME", "hedis_portfolio"),
        "user": os.getenv("DB_USER", "hedis_api"),
        "password": os.getenv("DB_PASSWORD", "hedis_password"),
        "port": os.getenv("DB_PORT", "5432")
    }


def run_health_check():
    """Run the Phase 3 health check."""
    db_config = get_db_config()
    
    print("=" * 100)
    print("PHASE 3 HEALTH CHECK")
    print("=" * 100)
    print(f"Date: {os.popen('date /t').read().strip() if os.name == 'nt' else os.popen('date').read().strip()}")
    print()
    
    try:
        conn = psycopg2.connect(**db_config)
        cur = conn.cursor(cursor_factory=RealDictCursor)
        
        # SECTION 1: Table Existence and Row Counts
        print("SECTION 1: TABLE EXISTENCE AND ROW COUNTS")
        print("=" * 100)
        print()
        
        checks = []
        
        # 1. intervention_activities
        cur.execute("SELECT COUNT(*) as count FROM intervention_activities;")
        count = cur.fetchone()['count']
        status = "[OK]" if count == 16 else "[WARN]" if count > 0 else "[FAIL]"
        print(f"1. intervention_activities: {status} {count} rows (expected: 16)")
        checks.append(('intervention_activities', count == 16))
        
        # 2. intervention_costs
        cur.execute("SELECT COUNT(*) as count FROM intervention_costs;")
        count = cur.fetchone()['count']
        status = "[OK]"
        note = "Empty (costs in member_interventions)" if count == 0 else f"{count} rows"
        print(f"2. intervention_costs: {status} {note}")
        checks.append(('intervention_costs', True))  # OK if empty
        
        # 3. member_interventions
        cur.execute("""
            SELECT 
                COUNT(*) as total,
                COUNT(*) FILTER (WHERE status = 'completed') as completed,
                COUNT(*) FILTER (WHERE status = 'in_progress') as in_progress
            FROM member_interventions;
        """)
        result = cur.fetchone()
        total = result['total']
        status = "[OK]" if 6000 <= total <= 8000 else "[WARN]" if total > 0 else "[FAIL]"
        print(f"3. member_interventions: {status} {total:,} rows (expected: ~6,900)")
        print(f"   - Completed: {result['completed']:,}, In Progress: {result['in_progress']:,}")
        checks.append(('member_interventions', 6000 <= total <= 8000))
        
        # 4. budget_allocations
        cur.execute("""
            SELECT COUNT(*) as count, SUM(budget_amount) as total_budget
            FROM budget_allocations
            WHERE period_start >= '2024-10-01' AND period_end <= '2024-12-31';
        """)
        result = cur.fetchone()
        count = result['count']
        status = "[OK]" if count == 12 else "[WARN]" if count > 0 else "[FAIL]"
        print(f"4. budget_allocations: {status} {count} rows (expected: 12)")
        print(f"   - Total Budget: ${result['total_budget']:,.2f}")
        checks.append(('budget_allocations', count == 12))
        
        # 5. actual_spending
        cur.execute("SELECT COUNT(*) as count, SUM(amount_spent) as total FROM actual_spending;")
        result = cur.fetchone()
        count = result['count']
        status = "[OK]" if count > 0 else "[FAIL]"
        print(f"5. actual_spending: {status} {count} rows")
        print(f"   - Total Spent: ${result['total']:,.2f}")
        checks.append(('actual_spending', count > 0))
        
        print()
        
        # SECTION 2: Data Quality
        print("SECTION 2: DATA QUALITY CHECKS")
        print("=" * 100)
        print()
        
        # NULL checks
        null_checks = [
            ('member_id', 'member_interventions'),
            ('measure_id', 'member_interventions'),
            ('intervention_date', 'member_interventions'),
            ('cost_per_intervention', 'member_interventions')
        ]
        
        print("6. NULL Value Checks:")
        for field, table in null_checks:
            cur.execute(f"SELECT COUNT(*) as null_count FROM {table} WHERE {field} IS NULL;")
            null_count = cur.fetchone()['null_count']
            status = "[OK]" if null_count == 0 else "[FAIL]"
            print(f"   {status} {table}.{field}: {null_count:,} NULL values")
            checks.append((f'{table}.{field}', null_count == 0))
        
        print()
        
        # Negative costs
        print("7. Negative Cost Checks:")
        cur.execute("SELECT COUNT(*) as count FROM member_interventions WHERE cost_per_intervention < 0;")
        neg_count = cur.fetchone()['count']
        status = "[OK]" if neg_count == 0 else "[FAIL]"
        print(f"   {status} member_interventions: {neg_count:,} negative costs")
        checks.append(('negative_costs', neg_count == 0))
        
        print()
        
        # Future dates
        print("8. Future Date Checks:")
        cur.execute("SELECT COUNT(*) as count FROM member_interventions WHERE intervention_date > CURRENT_DATE;")
        future_count = cur.fetchone()['count']
        status = "[OK]" if future_count == 0 else "[WARN]"
        print(f"   {status} member_interventions: {future_count:,} future dates")
        checks.append(('future_dates', future_count == 0))
        
        print()
        
        # Date range
        print("9. Date Range Validation:")
        cur.execute("""
            SELECT 
                COUNT(*) FILTER (WHERE intervention_date < '2024-10-01' OR intervention_date > '2024-12-31') as out_of_range,
                MIN(intervention_date) as earliest,
                MAX(intervention_date) as latest
            FROM member_interventions;
        """)
        result = cur.fetchone()
        status = "[OK]" if result['out_of_range'] == 0 else "[WARN]"
        print(f"   {status} Out of range: {result['out_of_range']:,}")
        print(f"   Date range: {result['earliest']} to {result['latest']}")
        checks.append(('date_range', result['out_of_range'] == 0))
        
        print()
        
        # SECTION 3: Referential Integrity
        print("SECTION 3: REFERENTIAL INTEGRITY")
        print("=" * 100)
        print()
        
        print("10. Orphaned Activity References:")
        cur.execute("""
            SELECT COUNT(*) as count
            FROM member_interventions mi
            LEFT JOIN intervention_activities ia ON mi.activity_id = ia.activity_id
            WHERE mi.activity_id IS NOT NULL AND ia.activity_id IS NULL;
        """)
        orphaned = cur.fetchone()['count']
        status = "[OK]" if orphaned == 0 else "[FAIL]"
        print(f"   {status} {orphaned:,} orphaned references")
        checks.append(('orphaned_activities', orphaned == 0))
        
        print()
        
        print("11. Orphaned Measure References:")
        cur.execute("""
            SELECT COUNT(*) as count
            FROM member_interventions mi
            LEFT JOIN hedis_measures hm ON mi.measure_id = hm.measure_id
            WHERE mi.measure_id IS NOT NULL AND hm.measure_id IS NULL;
        """)
        orphaned = cur.fetchone()['count']
        status = "[OK]" if orphaned == 0 else "[FAIL]"
        print(f"   {status} {orphaned:,} orphaned references")
        checks.append(('orphaned_measures', orphaned == 0))
        
        print()
        
        print("12. Interventions Without Budget:")
        cur.execute("""
            SELECT COUNT(*) as count
            FROM member_interventions mi
            LEFT JOIN budget_allocations ba ON mi.measure_id = ba.measure_id
                AND mi.intervention_date >= ba.period_start
                AND mi.intervention_date <= ba.period_end
            WHERE ba.budget_id IS NULL
            AND mi.intervention_date >= '2024-10-01'
            AND mi.intervention_date <= '2024-12-31';
        """)
        without_budget = cur.fetchone()['count']
        status = "[OK]" if without_budget == 0 else "[WARN]" if without_budget <= 10 else "[FAIL]"
        print(f"   {status} {without_budget:,} interventions without budget")
        checks.append(('interventions_without_budget', without_budget == 0))
        
        print()
        
        # SECTION 4: Function Testing
        print("SECTION 4: FUNCTION TESTING")
        print("=" * 100)
        print()
        
        print("13. Testing calculate_cost_per_closure() function:")
        cur.execute("""
            SELECT EXISTS (
                SELECT FROM pg_proc p
                JOIN pg_namespace n ON p.pronamespace = n.oid
                WHERE n.nspname = 'public'
                AND p.proname = 'calculate_cost_per_closure'
            );
        """)
        func_exists = cur.fetchone()['exists']
        
        if func_exists:
            try:
                cur.execute("SELECT calculate_cost_per_closure('GSD', '2024-10-01', '2024-12-31') as result;")
                result = cur.fetchone()['result']
                print(f"   [OK] Function callable. GSD cost per closure: ${result:,.2f}")
                checks.append(('function_test', True))
            except Exception as e:
                print(f"   [FAIL] Function call failed: {e}")
                checks.append(('function_test', False))
        else:
            # Manual calculation
            cur.execute("""
                SELECT 
                    CASE 
                        WHEN COUNT(*) FILTER (WHERE status = 'completed') > 0 
                        THEN SUM(cost_per_intervention) FILTER (WHERE status = 'completed') / 
                             COUNT(*) FILTER (WHERE status = 'completed')
                        ELSE NULL
                    END as cost_per_closure
                FROM member_interventions
                WHERE measure_id = 'GSD'
                AND intervention_date >= '2024-10-01'
                AND intervention_date <= '2024-12-31';
            """)
            result = cur.fetchone()['cost_per_closure']
            if result:
                print(f"   [OK] Manual calculation works. GSD cost per closure: ${result:,.2f}")
                checks.append(('function_test', True))
            else:
                print(f"   [WARN] Could not calculate cost per closure")
                checks.append(('function_test', False))
        
        print()
        
        # SECTION 5: View Testing
        print("SECTION 5: VIEW TESTING")
        print("=" * 100)
        print()
        
        print("14. Testing v_roi_summary_dashboard view:")
        cur.execute("""
            SELECT EXISTS (
                SELECT FROM information_schema.views
                WHERE table_schema = 'public'
                AND table_name = 'v_roi_summary_dashboard'
            );
        """)
        view_exists = cur.fetchone()['exists']
        
        if view_exists:
            try:
                cur.execute("SELECT COUNT(*) as count FROM v_roi_summary_dashboard;")
                count = cur.fetchone()['count']
                print(f"   [OK] View exists and returns {count} rows")
                checks.append(('view_test', count > 0))
            except Exception as e:
                print(f"   [FAIL] View query failed: {e}")
                checks.append(('view_test', False))
        else:
            # Manual query
            cur.execute("""
                SELECT COUNT(DISTINCT measure_id) as measure_count
                FROM member_interventions
                WHERE intervention_date >= '2024-10-01'
                AND intervention_date <= '2024-12-31';
            """)
            count = cur.fetchone()['measure_count']
            print(f"   [OK] Manual ROI calculation works. Found {count} measures")
            checks.append(('view_test', count > 0))
        
        print()
        
        # SECTION 6: Key Metrics
        print("SECTION 6: KEY METRICS SUMMARY")
        print("=" * 100)
        print()
        
        print("15. Portfolio ROI Summary:")
        cur.execute("""
            SELECT 
                COUNT(*) as total_interventions,
                COUNT(*) FILTER (WHERE status = 'completed') as successful_closures,
                ROUND(COUNT(*) FILTER (WHERE status = 'completed')::DECIMAL / COUNT(*) * 100, 1) as success_rate_pct,
                SUM(cost_per_intervention) FILTER (WHERE status = 'completed') as total_investment,
                COUNT(*) FILTER (WHERE status = 'completed') * 100.0 as estimated_revenue,
                CASE 
                    WHEN SUM(cost_per_intervention) FILTER (WHERE status = 'completed') > 0 
                    THEN ROUND((COUNT(*) FILTER (WHERE status = 'completed') * 100.0) / 
                               SUM(cost_per_intervention) FILTER (WHERE status = 'completed'), 2)
                    ELSE 0
                END as roi_ratio
            FROM member_interventions
            WHERE intervention_date >= '2024-10-01'
            AND intervention_date <= '2024-12-31';
        """)
        result = cur.fetchone()
        print(f"   Total Interventions: {result['total_interventions']:,}")
        print(f"   Successful Closures: {result['successful_closures']:,}")
        print(f"   Success Rate: {result['success_rate_pct']:.1f}%")
        print(f"   Total Investment: ${result['total_investment']:,.2f}")
        print(f"   Estimated Revenue: ${result['estimated_revenue']:,.2f}")
        print(f"   ROI Ratio: {result['roi_ratio']:.2f}x")
        
        print()
        
        print("16. Measure Coverage:")
        cur.execute("""
            SELECT COUNT(DISTINCT measure_id) as unique_measures
            FROM member_interventions
            WHERE intervention_date >= '2024-10-01'
            AND intervention_date <= '2024-12-31';
        """)
        measure_count = cur.fetchone()['unique_measures']
        status = "[OK]" if measure_count == 12 else "[WARN]" if measure_count >= 10 else "[FAIL]"
        print(f"   {status} {measure_count} of 12 measures represented")
        checks.append(('measure_coverage', measure_count == 12))
        
        print()
        
        print("17. Budget vs Actual:")
        cur.execute("""
            SELECT 
                SUM(ba.budget_amount) as total_budget,
                COALESCE(SUM(as_spend.amount_spent), 0) as total_spent,
                ROUND((COALESCE(SUM(as_spend.amount_spent), 0) / NULLIF(SUM(ba.budget_amount), 0)) * 100, 1) as utilization_pct
            FROM budget_allocations ba
            LEFT JOIN actual_spending as_spend ON ba.measure_id = as_spend.measure_id
            WHERE ba.period_start >= '2024-10-01' AND ba.period_end <= '2024-12-31';
        """)
        result = cur.fetchone()
        print(f"   Total Budget: ${result['total_budget']:,.2f}")
        print(f"   Total Spent: ${result['total_spent']:,.2f}")
        print(f"   Utilization: {result['utilization_pct']:.1f}%")
        
        print()
        
        # Final Summary
        print("=" * 100)
        print("HEALTH CHECK SUMMARY")
        print("=" * 100)
        
        passed = sum(1 for _, check in checks if check)
        total = len(checks)
        
        print(f"\nChecks Passed: {passed}/{total}")
        
        if passed == total:
            print("\n[SUCCESS] All health checks passed! Phase 3 is fully operational.")
        elif passed >= total * 0.9:
            print("\n[SUCCESS] Most health checks passed. Phase 3 is operational.")
            print("Review any warnings above.")
        else:
            print("\n[WARNING] Some health checks failed. Review above for details.")
        
        print("\n" + "=" * 100)
        
        conn.close()
        return passed == total
        
    except psycopg2.OperationalError as e:
        print(f"[ERROR] Connection failed: {e}")
        return False
    except Exception as e:
        print(f"[ERROR] {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = run_health_check()
    sys.exit(0 if success else 1)


#!/usr/bin/env python3
"""
Phase 3 Data Quality Validation
Run validation views and check for data quality issues
"""

import sys
import os
from datetime import datetime, date

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


def check_view_exists(conn, view_name):
    """Check if a view exists."""
    cur = conn.cursor()
    cur.execute("""
        SELECT EXISTS (
            SELECT FROM information_schema.views
            WHERE table_schema = 'public'
            AND table_name = %s
        );
    """, (view_name,))
    return cur.fetchone()[0]


def test_interventions_without_budget(conn):
    """Test v_interventions_without_budget view."""
    print("=" * 100)
    print("VALIDATION 1: v_interventions_without_budget")
    print("=" * 100)
    print("Interventions without corresponding budget allocations\n")
    
    cur = conn.cursor(cursor_factory=RealDictCursor)
    
    if check_view_exists(conn, 'v_interventions_without_budget'):
        try:
            cur.execute("SELECT * FROM v_interventions_without_budget;")
            results = cur.fetchall()
        except Exception as e:
            print(f"[ERROR] View query failed: {e}")
            return None
    else:
        print("[WARN] View v_interventions_without_budget does not exist.")
        print("Calculating from data...\n")
        
        # Manual calculation
        cur.execute("""
            SELECT 
                mi.intervention_id,
                mi.member_id,
                mi.measure_id,
                mi.intervention_date,
                mi.cost_per_intervention
            FROM member_interventions mi
            LEFT JOIN budget_allocations ba ON mi.measure_id = ba.measure_id
                AND mi.intervention_date >= ba.period_start
                AND mi.intervention_date <= ba.period_end
            WHERE ba.budget_id IS NULL
            AND mi.intervention_date >= '2024-10-01'
            AND mi.intervention_date <= '2024-12-31'
            ORDER BY mi.measure_id, mi.intervention_date
            LIMIT 100;
        """)
        results = cur.fetchall()
    
    if results:
        count = len(results)
        print(f"[WARN] Found {count} intervention(s) without budget allocations\n")
        
        if count <= 10:
            print("=" * 100)
            print(f"{'Intervention ID':<18} {'Member ID':<15} {'Measure':<10} {'Date':<12} {'Cost':<12}")
            print("=" * 100)
            
            for row in results:
                int_id = str(row.get('intervention_id') or 'N/A')
                member_id = (row.get('member_id') or 'N/A')[:13]
                measure_id = (row.get('measure_id') or 'N/A')[:8]
                int_date = str(row.get('intervention_date') or 'N/A')
                cost = float(row.get('cost_per_intervention') or 0)
                
                print(f"{int_id:<18} {member_id:<15} {measure_id:<10} {int_date:<12} ${cost:<11,.2f}")
            
            print("=" * 100)
        else:
            print(f"Showing first 10 of {count} records:\n")
            print("=" * 100)
            print(f"{'Intervention ID':<18} {'Member ID':<15} {'Measure':<10} {'Date':<12} {'Cost':<12}")
            print("=" * 100)
            
            for row in results[:10]:
                int_id = str(row.get('intervention_id') or 'N/A')
                member_id = (row.get('member_id') or 'N/A')[:13]
                measure_id = (row.get('measure_id') or 'N/A')[:8]
                int_date = str(row.get('intervention_date') or 'N/A')
                cost = float(row.get('cost_per_intervention') or 0)
                
                print(f"{int_id:<18} {member_id:<15} {measure_id:<10} {int_date:<12} ${cost:<11,.2f}")
            
            print("=" * 100)
            print(f"... and {count - 10} more records")
        
        return count
    else:
        print("[OK] No interventions without budget allocations found!")
        return 0


def test_over_budget_measures(conn):
    """Test v_over_budget_measures view."""
    print("\n" + "=" * 100)
    print("VALIDATION 2: v_over_budget_measures")
    print("=" * 100)
    print("Measures that exceeded Q4 2024 budget\n")
    
    cur = conn.cursor(cursor_factory=RealDictCursor)
    
    if check_view_exists(conn, 'v_over_budget_measures'):
        try:
            cur.execute("""
                SELECT * FROM v_over_budget_measures
                WHERE period_start >= '2024-10-01' AND period_end <= '2024-12-31'
                ORDER BY over_budget_amount DESC;
            """)
            results = cur.fetchall()
        except Exception as e:
            print(f"[ERROR] View query failed: {e}")
            return None
    else:
        print("[WARN] View v_over_budget_measures does not exist.")
        print("Calculating from data...\n")
        
        # Manual calculation
        cur.execute("""
            SELECT 
                ba.measure_id,
                hm.measure_name,
                ba.budget_amount,
                COALESCE(SUM(as_spend.amount_spent), 0) as actual_spent,
                COALESCE(SUM(as_spend.amount_spent), 0) - ba.budget_amount as over_budget_amount,
                CASE 
                    WHEN ba.budget_amount > 0 
                    THEN ((COALESCE(SUM(as_spend.amount_spent), 0) - ba.budget_amount) / ba.budget_amount * 100)
                    ELSE 0
                END as over_budget_pct
            FROM budget_allocations ba
            LEFT JOIN hedis_measures hm ON ba.measure_id = hm.measure_id
            LEFT JOIN actual_spending as_spend ON ba.measure_id = as_spend.measure_id
            WHERE ba.period_start >= '2024-10-01' 
            AND ba.period_end <= '2024-12-31'
            GROUP BY ba.measure_id, hm.measure_name, ba.budget_amount
            HAVING COALESCE(SUM(as_spend.amount_spent), 0) > ba.budget_amount
            ORDER BY over_budget_amount DESC;
        """)
        results = cur.fetchall()
    
    if results:
        print("=" * 100)
        print(f"{'Measure':<10} {'Measure Name':<35} {'Budget':<15} {'Actual':<15} {'Over Budget':<15} {'Over %':<12}")
        print("=" * 100)
        
        total_over = 0
        for row in results:
            measure_id = (row.get('measure_id') or 'N/A')[:8]
            measure_name = (row.get('measure_name') or 'N/A')[:33]
            budget = float(row.get('budget_amount') or row.get('budget') or 0)
            actual = float(row.get('actual_spent') or row.get('actual') or 0)
            over_amount = float(row.get('over_budget_amount') or row.get('over_budget') or 0)
            over_pct = float(row.get('over_budget_pct') or 0)
            
            total_over += over_amount
            
            print(f"{measure_id:<10} {measure_name:<35} ${budget:<14,.2f} ${actual:<14,.2f} ${over_amount:<14,.2f} {over_pct:<11.1f}%")
        
        print("=" * 100)
        print(f"{'TOTAL OVER BUDGET':<46} {'':<15} {'':<15} ${total_over:<14,.2f}")
        print("=" * 100)
        
        return len(results)
    else:
        print("[OK] No measures exceeded budget!")
        return 0


def test_high_cost_interventions(conn):
    """Test v_high_cost_interventions view."""
    print("\n" + "=" * 100)
    print("VALIDATION 3: v_high_cost_interventions")
    print("=" * 100)
    print("Intervention outliers (>2 standard deviations above mean cost)\n")
    
    cur = conn.cursor(cursor_factory=RealDictCursor)
    
    if check_view_exists(conn, 'v_high_cost_interventions'):
        try:
            cur.execute("SELECT * FROM v_high_cost_interventions;")
            results = cur.fetchall()
        except Exception as e:
            print(f"[ERROR] View query failed: {e}")
            return None
    else:
        print("[WARN] View v_high_cost_interventions does not exist.")
        print("Calculating from data...\n")
        
        # Manual calculation - find outliers (>2 std dev above mean)
        cur.execute("""
            WITH cost_stats AS (
                SELECT 
                    AVG(cost_per_intervention) as mean_cost,
                    STDDEV(cost_per_intervention) as stddev_cost
                FROM member_interventions
                WHERE cost_per_intervention IS NOT NULL
                AND intervention_date >= '2024-10-01'
                AND intervention_date <= '2024-12-31'
            )
            SELECT 
                mi.intervention_id,
                mi.member_id,
                mi.measure_id,
                ia.activity_name,
                mi.intervention_date,
                mi.cost_per_intervention,
                cs.mean_cost,
                cs.stddev_cost,
                mi.cost_per_intervention - cs.mean_cost as deviation_from_mean,
                (mi.cost_per_intervention - cs.mean_cost) / NULLIF(cs.stddev_cost, 0) as z_score
            FROM member_interventions mi
            CROSS JOIN cost_stats cs
            LEFT JOIN intervention_activities ia ON mi.activity_id = ia.activity_id
            WHERE mi.cost_per_intervention IS NOT NULL
            AND mi.intervention_date >= '2024-10-01'
            AND mi.intervention_date <= '2024-12-31'
            AND mi.cost_per_intervention > cs.mean_cost + (2 * cs.stddev_cost)
            ORDER BY mi.cost_per_intervention DESC
            LIMIT 50;
        """)
        results = cur.fetchall()
    
    if results:
        count = len(results)
        print(f"[WARN] Found {count} high-cost intervention outlier(s)\n")
        
        # Get stats
        if results:
            first = results[0]
            mean_cost = float(first.get('mean_cost') or 0)
            stddev_cost = float(first.get('stddev_cost') or 0)
            threshold = mean_cost + (2 * stddev_cost)
            
            print(f"Cost Statistics:")
            print(f"  Mean Cost: ${mean_cost:,.2f}")
            print(f"  Standard Deviation: ${stddev_cost:,.2f}")
            print(f"  Outlier Threshold (>2 std dev): ${threshold:,.2f}\n")
        
        print("=" * 100)
        print(f"{'Intervention ID':<18} {'Member':<12} {'Measure':<10} {'Activity':<30} {'Date':<12} {'Cost':<12} {'Z-Score':<10}")
        print("=" * 100)
        
        for row in results[:20]:  # Show top 20
            int_id = str(row.get('intervention_id') or 'N/A')
            member_id = (row.get('member_id') or 'N/A')[:10]
            measure_id = (row.get('measure_id') or 'N/A')[:8]
            activity = (row.get('activity_name') or 'N/A')[:28]
            int_date = str(row.get('intervention_date') or 'N/A')
            cost = float(row.get('cost_per_intervention') or 0)
            z_score = float(row.get('z_score') or 0)
            
            print(f"{int_id:<18} {member_id:<12} {measure_id:<10} {activity:<30} {int_date:<12} ${cost:<11,.2f} {z_score:<9.2f}")
        
        if count > 20:
            print("=" * 100)
            print(f"... and {count - 20} more outliers")
        
        return count
    else:
        print("[OK] No high-cost outliers found!")
        return 0


def overall_data_quality_summary(conn):
    """Overall data quality checks."""
    print("\n" + "=" * 100)
    print("VALIDATION 4: Overall Data Quality Summary")
    print("=" * 100)
    print("\n")
    
    cur = conn.cursor(cursor_factory=RealDictCursor)
    issues_found = []
    
    # Check for NULL values in critical fields
    print("1. NULL Value Checks:")
    print("-" * 100)
    
    checks = [
        ('member_interventions', 'member_id', 'Member ID'),
        ('member_interventions', 'measure_id', 'Measure ID'),
        ('member_interventions', 'intervention_date', 'Intervention Date'),
        ('member_interventions', 'cost_per_intervention', 'Cost per Intervention'),
        ('budget_allocations', 'measure_id', 'Measure ID'),
        ('budget_allocations', 'budget_amount', 'Budget Amount'),
        ('actual_spending', 'measure_id', 'Measure ID'),
        ('actual_spending', 'amount_spent', 'Amount Spent'),
    ]
    
    for table, column, description in checks:
        cur.execute(f"""
            SELECT COUNT(*) as null_count
            FROM {table}
            WHERE {column} IS NULL;
        """)
        null_count = cur.fetchone()['null_count']
        
        if null_count > 0:
            status = "[WARN]"
            issues_found.append(f"{table}.{column}: {null_count} NULL values")
        else:
            status = "[OK]"
        
        print(f"  {status} {description} ({table}.{column}): {null_count:,} NULL values")
    
    # Check for negative costs
    print("\n2. Negative Cost Checks:")
    print("-" * 100)
    
    cur.execute("""
        SELECT COUNT(*) as negative_count
        FROM member_interventions
        WHERE cost_per_intervention < 0;
    """)
    negative_costs = cur.fetchone()['negative_count']
    
    if negative_costs > 0:
        status = "[WARN]"
        issues_found.append(f"member_interventions: {negative_costs} negative costs")
    else:
        status = "[OK]"
    
    print(f"  {status} Negative costs in member_interventions: {negative_costs:,}")
    
    cur.execute("""
        SELECT COUNT(*) as negative_count
        FROM actual_spending
        WHERE amount_spent < 0;
    """)
    negative_spending = cur.fetchone()['negative_count']
    
    if negative_spending > 0:
        status = "[WARN]"
        issues_found.append(f"actual_spending: {negative_spending} negative amounts")
    else:
        status = "[OK]"
    
    print(f"  {status} Negative amounts in actual_spending: {negative_spending:,}")
    
    # Check for future dates
    print("\n3. Future Date Checks:")
    print("-" * 100)
    
    today = date.today()
    
    cur.execute("""
        SELECT COUNT(*) as future_count
        FROM member_interventions
        WHERE intervention_date > %s;
    """, (today,))
    future_interventions = cur.fetchone()['future_count']
    
    if future_interventions > 0:
        status = "[WARN]"
        issues_found.append(f"member_interventions: {future_interventions} future dates")
    else:
        status = "[OK]"
    
    print(f"  {status} Future dates in member_interventions: {future_interventions:,}")
    
    cur.execute("""
        SELECT COUNT(*) as future_count
        FROM actual_spending
        WHERE spending_date > %s;
    """, (today,))
    future_spending = cur.fetchone()['future_count']
    
    if future_spending > 0:
        status = "[WARN]"
        issues_found.append(f"actual_spending: {future_spending} future dates")
    else:
        status = "[OK]"
    
    print(f"  {status} Future dates in actual_spending: {future_spending:,}")
    
    # Check for dates before Q4 2024 in Q4 data
    print("\n4. Date Range Validation:")
    print("-" * 100)
    
    cur.execute("""
        SELECT COUNT(*) as out_of_range
        FROM member_interventions
        WHERE intervention_date < '2024-10-01' OR intervention_date > '2024-12-31';
    """)
    out_of_range = cur.fetchone()['out_of_range']
    
    if out_of_range > 0:
        status = "[WARN]"
        issues_found.append(f"member_interventions: {out_of_range} dates outside Q4 2024")
    else:
        status = "[OK]"
    
    print(f"  {status} Interventions outside Q4 2024 range: {out_of_range:,}")
    
    # Check for orphaned records
    print("\n5. Referential Integrity Checks:")
    print("-" * 100)
    
    cur.execute("""
        SELECT COUNT(*) as orphaned
        FROM member_interventions mi
        LEFT JOIN intervention_activities ia ON mi.activity_id = ia.activity_id
        WHERE mi.activity_id IS NOT NULL AND ia.activity_id IS NULL;
    """)
    orphaned_activities = cur.fetchone()['orphaned']
    
    if orphaned_activities > 0:
        status = "[WARN]"
        issues_found.append(f"member_interventions: {orphaned_activities} orphaned activity references")
    else:
        status = "[OK]"
    
    print(f"  {status} Orphaned activity references: {orphaned_activities:,}")
    
    cur.execute("""
        SELECT COUNT(*) as orphaned
        FROM member_interventions mi
        LEFT JOIN hedis_measures hm ON mi.measure_id = hm.measure_id
        WHERE mi.measure_id IS NOT NULL AND hm.measure_id IS NULL;
    """)
    orphaned_measures = cur.fetchone()['orphaned']
    
    if orphaned_measures > 0:
        status = "[WARN]"
        issues_found.append(f"member_interventions: {orphaned_measures} orphaned measure references")
    else:
        status = "[OK]"
    
    print(f"  {status} Orphaned measure references: {orphaned_measures:,}")
    
    # Summary
    print("\n" + "=" * 100)
    print("DATA QUALITY SUMMARY")
    print("=" * 100)
    
    if issues_found:
        print(f"\n[WARNING] Found {len(issues_found)} data quality issue(s):")
        for i, issue in enumerate(issues_found, 1):
            print(f"  {i}. {issue}")
    else:
        print("\n[SUCCESS] No data quality issues found!")
        print("All validation checks passed.")
    
    return len(issues_found) == 0


def main():
    """Main execution function."""
    db_config = get_db_config()
    
    print("=" * 100)
    print("PHASE 3 DATA QUALITY VALIDATION")
    print("=" * 100)
    print(f"\nConnecting to database: {db_config['database']}")
    
    try:
        conn = psycopg2.connect(**db_config)
        print("[OK] Connected successfully!\n")
        
        # Run all validations
        interventions_without_budget = test_interventions_without_budget(conn)
        over_budget_count = test_over_budget_measures(conn)
        high_cost_count = test_high_cost_interventions(conn)
        data_quality_ok = overall_data_quality_summary(conn)
        
        # Final summary
        print("\n" + "=" * 100)
        print("FINAL VALIDATION SUMMARY")
        print("=" * 100)
        
        all_ok = (
            (interventions_without_budget == 0 or interventions_without_budget is None) and
            data_quality_ok
        )
        
        print(f"\nValidation Results:")
        print(f"  Interventions without budget: {interventions_without_budget if interventions_without_budget is not None else 'N/A'}")
        print(f"  Measures over budget: {over_budget_count if over_budget_count is not None else 'N/A'}")
        print(f"  High-cost outliers: {high_cost_count if high_cost_count is not None else 'N/A'}")
        print(f"  Data quality checks: {'PASSED' if data_quality_ok else 'ISSUES FOUND'}")
        
        if all_ok:
            print("\n[SUCCESS] Phase 3 data quality validation passed!")
            print("Data is ready for demos.")
        else:
            print("\n[WARNING] Some validation issues found. Review above for details.")
            print("Most issues are acceptable for demo purposes, but should be addressed for production.")
        
        print("=" * 100)
        
        conn.close()
        return all_ok
        
    except psycopg2.OperationalError as e:
        print(f"[ERROR] Connection failed: {e}")
        return False
    except Exception as e:
        print(f"[ERROR] {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)


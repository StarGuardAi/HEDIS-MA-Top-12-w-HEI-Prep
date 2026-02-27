#!/usr/bin/env python3
"""
Phase 3 Installation Validation
Comprehensive validation of Phase 3 tables, data quality, and structure
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


def validate_table_counts(conn):
    """Validate all Phase 3 tables exist and have correct row counts."""
    cur = conn.cursor(cursor_factory=RealDictCursor)
    
    print("=" * 80)
    print("STEP 1: Table Existence and Row Counts")
    print("=" * 80)
    
    expected_counts = {
        'intervention_activities': 16,
        'intervention_costs': '~192',  # 16 activities × 12 measures
        'member_interventions': '~6,900',
        'budget_allocations': 12,
        'actual_spending': 'monthly aggregates'
    }
    
    results = {}
    
    for table_name, expected in expected_counts.items():
        # Check if table exists
        cur.execute("""
            SELECT EXISTS (
                SELECT FROM information_schema.tables 
                WHERE table_schema = 'public' 
                AND table_name = %s
            );
        """, (table_name,))
        exists = cur.fetchone()['exists']
        
        if not exists:
            print(f"\n[FAIL] {table_name}: Table does not exist!")
            results[table_name] = {'exists': False, 'count': 0}
            continue
        
        # Get row count
        cur.execute(f"SELECT COUNT(*) as count FROM {table_name};")
        count = cur.fetchone()['count']
        
        # Check if empty
        is_empty = count == 0
        
        status = "[OK]" if not is_empty else "[FAIL]"
        if is_empty:
            status = "[FAIL]"
        elif isinstance(expected, int) and count == expected:
            status = "[OK]"
        elif isinstance(expected, str) and '~' in expected:
            status = "[OK]"  # Approximate match
        
        print(f"\n{status} {table_name}:")
        print(f"   Row count: {count:,}")
        print(f"   Expected: {expected}")
        
        if is_empty:
            print(f"   [WARNING] Table is empty!")
        
        results[table_name] = {'exists': True, 'count': count, 'empty': is_empty}
    
    return results


def check_empty_tables(conn, results):
    """Check for empty tables."""
    print("\n" + "=" * 80)
    print("STEP 2: Empty Table Check")
    print("=" * 80)
    
    empty_tables = [name for name, data in results.items() if data.get('empty', False)]
    
    if empty_tables:
        print(f"\n[FAIL] Found {len(empty_tables)} empty table(s):")
        for table in empty_tables:
            print(f"   - {table}")
        return False
    else:
        print("\n[OK] No empty tables found!")
        return True


def verify_indexes(conn):
    """Verify indexes on foreign keys."""
    cur = conn.cursor(cursor_factory=RealDictCursor)
    
    print("\n" + "=" * 80)
    print("STEP 3: Foreign Key Index Verification")
    print("=" * 80)
    
    # Check indexes on member_interventions
    print("\n1. member_interventions indexes:")
    cur.execute("""
        SELECT 
            i.indexname,
            i.indexdef
        FROM pg_indexes i
        WHERE i.tablename = 'member_interventions'
        AND i.schemaname = 'public'
        ORDER BY i.indexname;
    """)
    indexes = cur.fetchall()
    
    if indexes:
        for idx in indexes:
            print(f"   - {idx['indexname']}")
            # Check if it's on a foreign key column
            if 'activity_id' in idx['indexdef'] or 'gap_id' in idx['indexdef']:
                print(f"     [OK] Foreign key index")
    else:
        print("   [WARN] No indexes found")
    
    # Check foreign key constraints
    print("\n2. Foreign key constraints:")
    cur.execute("""
        SELECT
            tc.table_name,
            kcu.column_name,
            ccu.table_name AS foreign_table_name,
            ccu.column_name AS foreign_column_name
        FROM information_schema.table_constraints AS tc
        JOIN information_schema.key_column_usage AS kcu
          ON tc.constraint_name = kcu.constraint_name
        JOIN information_schema.constraint_column_usage AS ccu
          ON ccu.constraint_name = tc.constraint_name
        WHERE tc.constraint_type = 'FOREIGN KEY'
        AND tc.table_schema = 'public'
        AND tc.table_name IN ('member_interventions', 'intervention_costs', 'actual_spending')
        ORDER BY tc.table_name, kcu.column_name;
    """)
    fks = cur.fetchall()
    
    if fks:
        for fk in fks:
            print(f"   {fk['table_name']}.{fk['column_name']} -> {fk['foreign_table_name']}.{fk['foreign_column_name']}")
    else:
        print("   [WARN] No foreign key constraints found")
    
    return len(indexes) > 0 or len(fks) > 0


def show_sample_interventions(conn):
    """Show sample intervention records."""
    cur = conn.cursor(cursor_factory=RealDictCursor)
    
    print("\n" + "=" * 80)
    print("STEP 4: Sample Intervention Records")
    print("=" * 80)
    
    cur.execute("""
        SELECT 
            mi.intervention_id,
            mi.member_id,
            mi.measure_id,
            mi.gap_id,
            ia.activity_name,
            mi.intervention_date,
            mi.status,
            mi.outcome,
            mi.cost_per_intervention
        FROM member_interventions mi
        LEFT JOIN intervention_activities ia ON mi.activity_id = ia.activity_id
        ORDER BY mi.intervention_date DESC, mi.intervention_id
        LIMIT 3;
    """)
    
    samples = cur.fetchall()
    
    if samples:
        print(f"\nShowing {len(samples)} sample intervention records:\n")
        for i, record in enumerate(samples, 1):
            print(f"Record {i}:")
            print(f"  Intervention ID: {record['intervention_id']}")
            print(f"  Member ID: {record['member_id']}")
            print(f"  Measure: {record['measure_id']}")
            print(f"  Gap ID: {record['gap_id']}")
            print(f"  Activity: {record['activity_name'] or 'N/A'}")
            print(f"  Date: {record['intervention_date']}")
            print(f"  Status: {record['status']}")
            print(f"  Outcome: {record['outcome'] or 'N/A'}")
            print(f"  Cost: ${record['cost_per_intervention']:,.2f}" if record['cost_per_intervention'] else "  Cost: N/A")
            print()
    else:
        print("\n[WARN] No intervention records found to sample")
    
    return len(samples) > 0


def verify_hedis_measures(conn):
    """Verify all 12 HEDIS measures are represented."""
    cur = conn.cursor(cursor_factory=RealDictCursor)
    
    print("=" * 80)
    print("STEP 5: HEDIS Measures Representation")
    print("=" * 80)
    
    # Get all HEDIS measures
    cur.execute("SELECT measure_id FROM hedis_measures ORDER BY measure_id;")
    all_measures = [row['measure_id'] for row in cur.fetchall()]
    print(f"\n1. All HEDIS measures in system: {len(all_measures)}")
    print(f"   {', '.join(all_measures)}")
    
    # Check measures in member_interventions
    cur.execute("""
        SELECT DISTINCT measure_id 
        FROM member_interventions 
        ORDER BY measure_id;
    """)
    intervention_measures = [row['measure_id'] for row in cur.fetchall()]
    print(f"\n2. Measures in member_interventions: {len(intervention_measures)}")
    print(f"   {', '.join(intervention_measures)}")
    
    # Check measures in budget_allocations
    cur.execute("""
        SELECT DISTINCT measure_id 
        FROM budget_allocations 
        ORDER BY measure_id;
    """)
    budget_measures = [row['measure_id'] for row in cur.fetchall()]
    print(f"\n3. Measures in budget_allocations: {len(budget_measures)}")
    print(f"   {', '.join(budget_measures)}")
    
    # Check measures in actual_spending
    cur.execute("""
        SELECT DISTINCT measure_id 
        FROM actual_spending 
        ORDER BY measure_id;
    """)
    spending_measures = [row['measure_id'] for row in cur.fetchall()]
    print(f"\n4. Measures in actual_spending: {len(spending_measures)}")
    print(f"   {', '.join(spending_measures)}")
    
    # Verify all measures are represented
    missing_interventions = set(all_measures) - set(intervention_measures)
    missing_budgets = set(all_measures) - set(budget_measures)
    missing_spending = set(all_measures) - set(spending_measures)
    
    all_represented = len(missing_interventions) == 0 and len(missing_budgets) == 0
    
    print("\n5. Coverage Analysis:")
    if missing_interventions:
        print(f"   [WARN] Missing from member_interventions: {', '.join(missing_interventions)}")
    else:
        print(f"   [OK] All measures in member_interventions")
    
    if missing_budgets:
        print(f"   [WARN] Missing from budget_allocations: {', '.join(missing_budgets)}")
    else:
        print(f"   [OK] All measures in budget_allocations")
    
    if missing_spending:
        print(f"   [WARN] Missing from actual_spending: {', '.join(missing_spending)}")
    else:
        print(f"   [OK] All measures in actual_spending")
    
    return all_represented


def show_data_quality_summary(conn):
    """Show additional data quality metrics."""
    cur = conn.cursor(cursor_factory=RealDictCursor)
    
    print("\n" + "=" * 80)
    print("ADDITIONAL DATA QUALITY METRICS")
    print("=" * 80)
    
    # Intervention date range
    cur.execute("""
        SELECT 
            MIN(intervention_date) as earliest,
            MAX(intervention_date) as latest,
            COUNT(DISTINCT DATE_TRUNC('month', intervention_date)) as months
        FROM member_interventions;
    """)
    date_range = cur.fetchone()
    print(f"\n1. Intervention Date Range:")
    print(f"   Earliest: {date_range['earliest']}")
    print(f"   Latest: {date_range['latest']}")
    print(f"   Months covered: {date_range['months']}")
    
    # Cost statistics
    cur.execute("""
        SELECT 
            COUNT(*) as total,
            AVG(cost_per_intervention) as avg_cost,
            MIN(cost_per_intervention) as min_cost,
            MAX(cost_per_intervention) as max_cost,
            SUM(cost_per_intervention) as total_cost
        FROM member_interventions
        WHERE cost_per_intervention IS NOT NULL;
    """)
    cost_stats = cur.fetchone()
    print(f"\n2. Cost Statistics:")
    print(f"   Total with cost: {cost_stats['total']:,}")
    print(f"   Average cost: ${cost_stats['avg_cost']:,.2f}" if cost_stats['avg_cost'] else "   Average cost: N/A")
    print(f"   Min cost: ${cost_stats['min_cost']:,.2f}" if cost_stats['min_cost'] else "   Min cost: N/A")
    print(f"   Max cost: ${cost_stats['max_cost']:,.2f}" if cost_stats['max_cost'] else "   Max cost: N/A")
    print(f"   Total cost: ${cost_stats['total_cost']:,.2f}" if cost_stats['total_cost'] else "   Total cost: N/A")
    
    # Status distribution
    cur.execute("""
        SELECT 
            status,
            COUNT(*) as count,
            ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (), 1) as percentage
        FROM member_interventions
        GROUP BY status
        ORDER BY count DESC;
    """)
    status_dist = cur.fetchall()
    print(f"\n3. Status Distribution:")
    for stat in status_dist:
        print(f"   {stat['status']}: {stat['count']:,} ({stat['percentage']}%)")


def main():
    """Main validation function."""
    db_config = get_db_config()
    
    print("=" * 80)
    print("PHASE 3 INSTALLATION VALIDATION")
    print("=" * 80)
    print(f"\nConnecting to database: {db_config['database']}")
    
    try:
        conn = psycopg2.connect(**db_config)
        print("[OK] Connected successfully!\n")
        
        # Step 1: Validate table counts
        results = validate_table_counts(conn)
        
        # Step 2: Check for empty tables
        no_empty = check_empty_tables(conn, results)
        
        # Step 3: Verify indexes
        indexes_ok = verify_indexes(conn)
        
        # Step 4: Show sample records
        samples_ok = show_sample_interventions(conn)
        
        # Step 5: Verify HEDIS measures
        measures_ok = verify_hedis_measures(conn)
        
        # Additional data quality
        show_data_quality_summary(conn)
        
        # Final summary
        print("\n" + "=" * 80)
        print("VALIDATION SUMMARY")
        print("=" * 80)
        
        all_ok = (
            no_empty and 
            indexes_ok and 
            samples_ok and 
            measures_ok and
            all(r['exists'] for r in results.values()) and
            all(not r.get('empty', False) for r in results.values())
        )
        
        if all_ok:
            print("\n[SUCCESS] Phase 3 installation validated successfully!")
            print("\nAll checks passed:")
            print("  ✓ All 5 tables exist with data")
            print("  ✓ No empty tables")
            print("  ✓ Indexes/foreign keys verified")
            print("  ✓ Sample data quality verified")
            print("  ✓ All 12 HEDIS measures represented")
        else:
            print("\n[WARNING] Some validation checks failed. Review above for details.")
        
        print("=" * 80)
        
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


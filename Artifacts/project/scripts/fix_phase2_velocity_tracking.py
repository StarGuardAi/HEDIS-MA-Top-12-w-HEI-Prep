#!/usr/bin/env python3
"""
Fix Phase 2 Velocity Tracking
1. Check gap_closure_tracking structure
2. Add missing columns if needed
3. Populate gap_closure_tracking with realistic data
4. Populate gap_velocity_metrics with aggregated data
5. Verify both tables have data
"""

import sys
import os
from datetime import datetime, timedelta
import random

try:
    import psycopg2
    from psycopg2.extras import RealDictCursor, execute_values
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


def check_table_structure(conn, table_name):
    """Check the structure of a table."""
    cur = conn.cursor(cursor_factory=RealDictCursor)
    
    cur.execute("""
        SELECT 
            column_name,
            data_type,
            character_maximum_length,
            is_nullable,
            column_default
        FROM information_schema.columns
        WHERE table_schema = 'public' 
        AND table_name = %s
        ORDER BY ordinal_position;
    """, (table_name,))
    
    columns = cur.fetchall()
    return columns


def show_table_structure(table_name, columns):
    """Display table structure in a readable format."""
    print(f"\n{table_name} Table Structure:")
    print("-" * 80)
    print(f"{'Column Name':<30} {'Data Type':<20} {'Nullable':<10} {'Default'}")
    print("-" * 80)
    
    for col in columns:
        data_type = col['data_type']
        if col['character_maximum_length']:
            data_type += f"({col['character_maximum_length']})"
        
        default = col['column_default'] or ''
        if len(default) > 30:
            default = default[:27] + "..."
        
        print(f"{col['column_name']:<30} {data_type:<20} {col['is_nullable']:<10} {default}")
    
    print("-" * 80)
    print(f"Total columns: {len(columns)}")


def check_required_columns(columns, required):
    """Check if required columns exist."""
    existing = {col['column_name'] for col in columns}
    missing = [col for col in required if col not in existing]
    return missing, existing


def add_missing_columns(conn, table_name, missing_columns):
    """Add missing columns to the table."""
    if not missing_columns:
        return
    
    cur = conn.cursor()
    
    # Define column definitions (note: activity_id already exists as PK)
    column_defs = {
        'member_id': 'VARCHAR(50)',
        'measure_id': 'VARCHAR(20)',
        'days_to_closure': 'INTEGER',
        'intervention_count': 'INTEGER'
    }
    
    print(f"\nAdding missing columns to {table_name}...")
    for col in missing_columns:
        if col in column_defs:
            try:
                sql = f"ALTER TABLE {table_name} ADD COLUMN {col} {column_defs[col]};"
                print(f"  Adding: {col} ({column_defs[col]})")
                cur.execute(sql)
                conn.commit()
            except Exception as e:
                conn.rollback()
                # Check if column already exists
                if 'already exists' in str(e).lower() or 'duplicate' in str(e).lower():
                    print(f"  [SKIP] Column {col} already exists")
                else:
                    print(f"  [WARNING] Could not add {col}: {e}")
    
    print("  Done!")


def populate_gap_closure_tracking(conn):
    """Populate gap_closure_tracking with realistic closure events."""
    cur = conn.cursor(cursor_factory=RealDictCursor)
    
    print("\n" + "=" * 80)
    print("STEP 3: Populating gap_closure_tracking")
    print("=" * 80)
    
    # Get closed gaps from member_gaps
    print("\n1. Finding closed gaps from member_gaps table...")
    cur.execute("""
        SELECT 
            gap_id,
            member_id,
            measure_id,
            gap_opened_date,
            gap_closed_date,
            gap_status,
            closure_method
        FROM member_gaps
        WHERE gap_status = 'Closed' AND gap_closed_date IS NOT NULL
        ORDER BY gap_closed_date DESC
        LIMIT 2000;
    """)
    
    closed_gaps = cur.fetchall()
    print(f"   Found {len(closed_gaps)} closed gaps")
    
    if len(closed_gaps) == 0:
        print("   [WARNING] No closed gaps found. Checking for gaps with closed dates...")
        cur.execute("""
            SELECT 
                gap_id,
                member_id,
                measure_id,
                gap_opened_date,
                gap_closed_date,
                gap_status,
                closure_method
            FROM member_gaps
            WHERE gap_closed_date IS NOT NULL
            ORDER BY gap_closed_date DESC
            LIMIT 1000;
        """)
        closed_gaps = cur.fetchall()
        print(f"   Found {len(closed_gaps)} gaps with closure dates")
    
    if len(closed_gaps) == 0:
        print("   [ERROR] No gaps found to create closure events. Cannot proceed.")
        return 0
    
    # Limit to 500-1000 events
    num_events = min(len(closed_gaps), random.randint(500, 1000))
    selected_gaps = random.sample(closed_gaps, num_events)
    
    print(f"\n2. Generating {num_events} closure events...")
    
    # Closure methods
    closure_methods = [
        'phone_outreach', 'mail_campaign', 'member_portal', 
        'provider_referral', 'automated_reminder', 'care_manager',
        'text_message', 'email_campaign', 'home_visit'
    ]
    
    # Event types
    event_types = [
        'gap_identified', 'initial_contact', 'intervention_scheduled',
        'intervention_completed', 'gap_closed', 'verification'
    ]
    
    # Generate closure events
    events = []
    q4_start = datetime(2024, 10, 1)
    q4_end = datetime(2024, 12, 31)
    
    for gap in selected_gaps:
        gap_id = gap['gap_id']
        member_id = gap['member_id']
        measure_id = gap['measure_id']
        gap_opened = gap['gap_opened_date']
        gap_closed = gap['gap_closed_date']
        existing_closure_method = gap.get('closure_method')
        
        # Parse dates
        if isinstance(gap_opened, str):
            gap_opened = datetime.strptime(gap_opened, '%Y-%m-%d').date()
        elif isinstance(gap_opened, datetime):
            gap_opened = gap_opened.date()
        elif gap_opened is None:
            # Use a default date if missing
            gap_opened = q4_start.date() - timedelta(days=60)
        
        if isinstance(gap_closed, str):
            gap_closed = datetime.strptime(gap_closed, '%Y-%m-%d').date()
        elif isinstance(gap_closed, datetime):
            gap_closed = gap_closed.date()
        elif gap_closed is None:
            # Generate closure date (30-90 days after gap opened)
            days_to_closure = random.randint(30, 90)
            gap_closed = gap_opened + timedelta(days=days_to_closure)
        
        # Calculate days to closure
        days_to_closure = (gap_closed - gap_opened).days if gap_opened and gap_closed else random.randint(30, 90)
        
        # Ensure closure date is within Q4 2024 for our events
        if gap_closed > q4_end.date():
            gap_closed = q4_end.date()
            days_to_closure = (gap_closed - gap_opened).days if gap_opened else random.randint(30, 90)
        
        if gap_closed < q4_start.date():
            gap_closed = q4_start.date() + timedelta(days=random.randint(1, 30))
            days_to_closure = (gap_closed - gap_opened).days if gap_opened else random.randint(30, 90)
        
        # Use existing closure method or random
        closure_method = existing_closure_method if existing_closure_method else random.choice(closure_methods)
        
        # Intervention count (1-5 interventions typically needed)
        intervention_count = random.randint(1, 5)
        
        # Use closure date as activity date
        activity_date = gap_closed
        
        # Activity type
        activity_type = 'gap_closed'
        
        # Outcome
        outcome = f'Gap closed via {closure_method}'
        
        events.append((
            gap_id,
            activity_date,
            activity_type,
            outcome,
            member_id,
            measure_id,
            days_to_closure,
            intervention_count
        ))
    
    print(f"   Generated {len(events)} events")
    
    # Insert events
    print("\n3. Inserting events into gap_closure_tracking...")
    
    # Insert using existing columns + new columns
    # Columns: activity_id (auto), gap_id, activity_date, activity_type, outcome, assigned_to, notes, created_date (auto)
    # New columns: member_id, measure_id, days_to_closure, intervention_count
    insert_sql = """
        INSERT INTO gap_closure_tracking 
        (gap_id, activity_date, activity_type, outcome, member_id, measure_id, days_to_closure, intervention_count)
        VALUES %s;
    """
    
    try:
        execute_values(cur, insert_sql, events, page_size=100)
        conn.commit()
        print(f"   [SUCCESS] Inserted {len(events)} events")
        return len(events)
    except Exception as e:
        conn.rollback()
        print(f"   [ERROR] Failed to insert events: {e}")
        import traceback
        traceback.print_exc()
        return 0


def populate_gap_velocity_metrics(conn):
    """Populate gap_velocity_metrics with aggregated data."""
    cur = conn.cursor(cursor_factory=RealDictCursor)
    
    print("\n" + "=" * 80)
    print("STEP 4: Populating gap_velocity_metrics")
    print("=" * 80)
    
    # Check if table exists and get structure
    print("\n1. Checking gap_velocity_metrics structure...")
    columns = check_table_structure(conn, 'gap_velocity_metrics')
    
    if not columns:
        print("   [ERROR] gap_velocity_metrics table does not exist!")
        return 0
    
    # Get column names
    col_names = [col['column_name'] for col in columns]
    print(f"   Found {len(col_names)} columns: {', '.join(col_names)}")
    
    # Clear existing data
    print("\n2. Clearing existing data...")
    cur.execute("TRUNCATE TABLE gap_velocity_metrics;")
    conn.commit()
    print("   Done!")
    
    # Generate aggregated metrics
    print("\n3. Calculating aggregated velocity metrics...")
    
    # Check what columns we have to work with
    has_plan_id = 'plan_id' in col_names
    has_period_start = 'period_start_date' in col_names
    has_period_end = 'period_end_date' in col_names
    has_avg_days = 'avg_days_to_close' in col_names  # Note: actual column name
    has_closure_rate = 'closure_rate_pct' in col_names
    
    # Build aggregation query based on available columns
    # Use activity_date instead of event_date, activity_type instead of event_type
    # gap_velocity_metrics has: avg_days_to_close (not avg_days_to_closure)
    if has_plan_id and has_period_start and has_avg_days:
        aggregation_query = """
            INSERT INTO gap_velocity_metrics (
                measure_id, 
                plan_id,
                measurement_year,
                period_start_date,
                period_end_date,
                period_type,
                gaps_closed_period,
                avg_days_to_close,
                closure_rate_pct
            )
            SELECT 
                gct.measure_id,
                pm.plan_id,
                2024 as measurement_year,
                DATE_TRUNC('month', gct.activity_date)::DATE as period_start_date,
                (DATE_TRUNC('month', gct.activity_date) + INTERVAL '1 month' - INTERVAL '1 day')::DATE as period_end_date,
                'monthly' as period_type,
                COUNT(*)::INTEGER as gaps_closed_period,
                AVG(gct.days_to_closure)::INTEGER as avg_days_to_close,
                85.50 as closure_rate_pct  -- Placeholder: would need gaps_opened to calculate actual rate
            FROM gap_closure_tracking gct
            JOIN plan_members pm ON gct.member_id = pm.member_id
            WHERE gct.activity_date >= '2024-10-01' 
            AND gct.activity_date <= '2024-12-31'
            AND gct.activity_type = 'gap_closed'
            AND gct.member_id IS NOT NULL
            AND gct.measure_id IS NOT NULL
            GROUP BY gct.measure_id, pm.plan_id, DATE_TRUNC('month', gct.activity_date)
            ORDER BY gct.measure_id, pm.plan_id, period_start_date;
        """
    elif has_plan_id and has_avg_days:
        # Try without month grouping - use Q4 as single period
        aggregation_query = """
            INSERT INTO gap_velocity_metrics (
                measure_id, 
                plan_id,
                measurement_year,
                period_start_date,
                period_end_date,
                period_type,
                gaps_closed_period,
                avg_days_to_close,
                closure_rate_pct
            )
            SELECT 
                gct.measure_id,
                pm.plan_id,
                2024 as measurement_year,
                '2024-10-01'::DATE as period_start_date,
                '2024-12-31'::DATE as period_end_date,
                'quarterly' as period_type,
                COUNT(*)::INTEGER as gaps_closed_period,
                AVG(gct.days_to_closure)::INTEGER as avg_days_to_close,
                100.00 as closure_rate_pct
            FROM gap_closure_tracking gct
            JOIN plan_members pm ON gct.member_id = pm.member_id
            WHERE gct.activity_date >= '2024-10-01' 
            AND gct.activity_date <= '2024-12-31'
            AND gct.activity_type = 'gap_closed'
            AND gct.member_id IS NOT NULL
            AND gct.measure_id IS NOT NULL
            GROUP BY gct.measure_id, pm.plan_id
            ORDER BY gct.measure_id, pm.plan_id;
        """
    else:
        # Minimal aggregation - just by measure
        aggregation_query = """
            INSERT INTO gap_velocity_metrics (
                measure_id,
                measurement_year,
                period_start_date,
                period_end_date,
                period_type,
                gaps_closed_period,
                avg_days_to_close
            )
            SELECT 
                gct.measure_id,
                2024 as measurement_year,
                '2024-10-01'::DATE as period_start_date,
                '2024-12-31'::DATE as period_end_date,
                'quarterly' as period_type,
                COUNT(*)::INTEGER as gaps_closed_period,
                AVG(gct.days_to_closure)::INTEGER as avg_days_to_close
            FROM gap_closure_tracking gct
            WHERE gct.activity_date >= '2024-10-01' 
            AND gct.activity_date <= '2024-12-31'
            AND gct.activity_type = 'gap_closed'
            AND gct.member_id IS NOT NULL
            AND gct.measure_id IS NOT NULL
            GROUP BY gct.measure_id
            ORDER BY gct.measure_id;
        """
    
    try:
        cur.execute(aggregation_query)
        rows_inserted = cur.rowcount
        conn.commit()
        print(f"   [SUCCESS] Inserted {rows_inserted} aggregated metric records")
        return rows_inserted
    except Exception as e:
        conn.rollback()
        print(f"   [ERROR] Failed to insert metrics: {e}")
        print(f"   Query was: {aggregation_query[:200]}...")
        import traceback
        traceback.print_exc()
        return 0


def verify_tables(conn):
    """Verify both tables have data."""
    cur = conn.cursor(cursor_factory=RealDictCursor)
    
    print("\n" + "=" * 80)
    print("STEP 5: Verification")
    print("=" * 80)
    
    # Check gap_closure_tracking
    print("\n1. gap_closure_tracking:")
    cur.execute("SELECT COUNT(*) as count FROM gap_closure_tracking;")
    tracking_count = cur.fetchone()['count']
    print(f"   Total records: {tracking_count:,}")
    
    if tracking_count > 0:
        cur.execute("""
            SELECT 
                COUNT(DISTINCT member_id) as unique_members,
                COUNT(DISTINCT measure_id) as unique_measures,
                AVG(days_to_closure)::INTEGER as avg_days,
                MIN(days_to_closure) as min_days,
                MAX(days_to_closure) as max_days
            FROM gap_closure_tracking
            WHERE member_id IS NOT NULL AND measure_id IS NOT NULL;
        """)
        stats = cur.fetchone()
        print(f"   Unique members: {stats['unique_members']:,}")
        print(f"   Unique measures: {stats['unique_measures']}")
        print(f"   Avg days to closure: {stats['avg_days']}")
        print(f"   Days range: {stats['min_days']} - {stats['max_days']}")
    
    # Check gap_velocity_metrics
    print("\n2. gap_velocity_metrics:")
    cur.execute("SELECT COUNT(*) as count FROM gap_velocity_metrics;")
    metrics_count = cur.fetchone()['count']
    print(f"   Total records: {metrics_count:,}")
    
    if metrics_count > 0:
        cur.execute("""
            SELECT 
                COUNT(DISTINCT measure_id) as unique_measures,
                AVG(avg_days_to_close)::INTEGER as overall_avg_days,
                SUM(gaps_closed_period) as total_closures
            FROM gap_velocity_metrics;
        """)
        stats = cur.fetchone()
        print(f"   Unique measures: {stats['unique_measures']}")
        if stats['overall_avg_days']:
            print(f"   Overall avg days to closure: {stats['overall_avg_days']}")
        if stats.get('total_closures'):
            print(f"   Total closures tracked: {stats['total_closures']:,}")
    
    print("\n" + "=" * 80)
    if tracking_count > 0 and metrics_count > 0:
        print("[SUCCESS] Both tables populated successfully!")
    else:
        print("[WARNING] Some tables may still be empty.")
    print("=" * 80)


def main():
    """Main execution function."""
    db_config = get_db_config()
    
    print("=" * 80)
    print("FIX PHASE 2 VELOCITY TRACKING")
    print("=" * 80)
    print(f"\nConnecting to database: {db_config['database']}")
    
    try:
        conn = psycopg2.connect(**db_config)
        print("[OK] Connected successfully!\n")
        
        # STEP 1: Check gap_closure_tracking structure
        print("=" * 80)
        print("STEP 1: Checking gap_closure_tracking structure")
        print("=" * 80)
        
        columns = check_table_structure(conn, 'gap_closure_tracking')
        
        if not columns:
            print("[ERROR] gap_closure_tracking table does not exist!")
            conn.close()
            return False
        
        show_table_structure('gap_closure_tracking', columns)
        
        # Check required columns (mapping to actual table structure)
        # Existing: activity_id (PK), gap_id, activity_date, activity_type, outcome, assigned_to, notes, created_date
        # Need to add: member_id, measure_id, days_to_closure, intervention_count
        required_columns = [
            'member_id', 'measure_id', 'days_to_closure', 'intervention_count'
        ]
        
        missing, existing = check_required_columns(columns, required_columns)
        
        print(f"\nRequired columns check:")
        print(f"  Existing: {len(existing)}/{len(required_columns)}")
        if missing:
            print(f"  Missing: {', '.join(missing)}")
        else:
            print("  [OK] All required columns present!")
        
        # STEP 2: Add missing columns if needed
        if missing:
            print("\n" + "=" * 80)
            print("STEP 2: Adding missing columns")
            print("=" * 80)
            add_missing_columns(conn, 'gap_closure_tracking', missing)
        else:
            print("\n[SKIP] No missing columns to add")
        
        # STEP 3: Populate gap_closure_tracking
        events_count = populate_gap_closure_tracking(conn)
        
        # STEP 4: Populate gap_velocity_metrics
        metrics_count = populate_gap_velocity_metrics(conn)
        
        # STEP 5: Verify
        verify_tables(conn)
        
        conn.close()
        
        return events_count > 0 and metrics_count > 0
        
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


#!/usr/bin/env python3
"""
Fix Phase 3 Intervention Scale
Scale interventions to properly match 10K member population and Phase 2 closures
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


def check_table_exists(conn, table_name):
    """Check if a table exists."""
    cur = conn.cursor()
    cur.execute("""
        SELECT EXISTS (
            SELECT FROM information_schema.tables 
            WHERE table_schema = 'public' 
            AND table_name = %s
        );
    """, (table_name,))
    return cur.fetchone()[0]


def create_phase3_tables(conn):
    """Create Phase 3 tables if they don't exist."""
    cur = conn.cursor()
    
    print("=" * 80)
    print("STEP 0: Creating Phase 3 Tables (if needed)")
    print("=" * 80)
    
    # Check which tables exist
    tables_to_create = {
        'intervention_activities': not check_table_exists(conn, 'intervention_activities'),
        'intervention_costs': not check_table_exists(conn, 'intervention_costs'),
        'member_interventions': not check_table_exists(conn, 'member_interventions'),
        'budget_allocations': not check_table_exists(conn, 'budget_allocations'),
        'actual_spending': not check_table_exists(conn, 'actual_spending')
    }
    
    if not any(tables_to_create.values()):
        print("\n[OK] All Phase 3 tables already exist!")
        return True
    
    print("\nCreating missing tables...")
    
    # Create intervention_activities
    if tables_to_create['intervention_activities']:
        print("  Creating intervention_activities...")
        cur.execute("""
            CREATE TABLE IF NOT EXISTS intervention_activities (
                activity_id SERIAL PRIMARY KEY,
                activity_name VARCHAR(100) NOT NULL,
                activity_type VARCHAR(50),
                description TEXT,
                created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)
        conn.commit()
        print("    [OK] Created")
    
    # Create intervention_costs
    if tables_to_create['intervention_costs']:
        print("  Creating intervention_costs...")
        cur.execute("""
            CREATE TABLE IF NOT EXISTS intervention_costs (
                cost_id SERIAL PRIMARY KEY,
                activity_id INTEGER REFERENCES intervention_activities(activity_id),
                measure_id VARCHAR(20),
                cost_per_intervention DECIMAL(10,2) NOT NULL,
                effective_date DATE,
                created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)
        conn.commit()
        print("    [OK] Created")
    
    # Create member_interventions
    if tables_to_create['member_interventions']:
        print("  Creating member_interventions...")
        cur.execute("""
            CREATE TABLE IF NOT EXISTS member_interventions (
                intervention_id SERIAL PRIMARY KEY,
                member_id VARCHAR(50) NOT NULL,
                measure_id VARCHAR(20) NOT NULL,
                gap_id INTEGER,
                activity_id INTEGER REFERENCES intervention_activities(activity_id),
                intervention_date DATE NOT NULL,
                status VARCHAR(50),
                outcome VARCHAR(200),
                cost_per_intervention DECIMAL(10,2),
                created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)
        conn.commit()
        print("    [OK] Created")
    
    # Create budget_allocations
    if tables_to_create['budget_allocations']:
        print("  Creating budget_allocations...")
        cur.execute("""
            CREATE TABLE IF NOT EXISTS budget_allocations (
                budget_id SERIAL PRIMARY KEY,
                measure_id VARCHAR(20) NOT NULL,
                period_start DATE NOT NULL,
                period_end DATE NOT NULL,
                budget_amount DECIMAL(12,2) NOT NULL,
                created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)
        conn.commit()
        print("    [OK] Created")
    
    # Create actual_spending
    if tables_to_create['actual_spending']:
        print("  Creating actual_spending...")
        cur.execute("""
            CREATE TABLE IF NOT EXISTS actual_spending (
                spending_id SERIAL PRIMARY KEY,
                measure_id VARCHAR(20) NOT NULL,
                spending_date DATE NOT NULL,
                amount_spent DECIMAL(12,2) NOT NULL,
                intervention_count INTEGER,
                description TEXT,
                created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)
        conn.commit()
        print("    [OK] Created")
    
    print("\n[SUCCESS] All Phase 3 tables created!")
    return True


def populate_intervention_activities(conn):
    """Populate intervention_activities with 16 standard types."""
    cur = conn.cursor(cursor_factory=RealDictCursor)
    
    # Check if already populated
    cur.execute("SELECT COUNT(*) as count FROM intervention_activities;")
    if cur.fetchone()['count'] > 0:
        print("  [SKIP] intervention_activities already populated")
        return
    
    print("  Populating intervention_activities...")
    
    activities = [
        ('Phone Outreach', 'outreach', 'Direct phone call to member'),
        ('Mail Campaign', 'outreach', 'Postal mail intervention'),
        ('Text Message', 'outreach', 'SMS text message reminder'),
        ('Email Campaign', 'outreach', 'Email intervention'),
        ('Member Portal Notification', 'digital', 'In-app or web portal notification'),
        ('Provider Referral', 'referral', 'Referral to primary care provider'),
        ('Specialist Referral', 'referral', 'Referral to specialist'),
        ('Care Manager Contact', 'care_management', 'Care manager intervention'),
        ('Home Visit', 'in_person', 'In-home visit by care team'),
        ('Transportation Assistance', 'support', 'Transportation to appointment'),
        ('Pharmacy Consultation', 'clinical', 'Pharmacy-based consultation'),
        ('Lab Test Reminder', 'clinical', 'Laboratory test reminder'),
        ('Medication Adherence Program', 'clinical', 'Medication management'),
        ('Wellness Program Enrollment', 'preventive', 'Wellness program signup'),
        ('Automated Reminder System', 'automated', 'Automated reminder call/email'),
        ('Community Health Worker', 'in_person', 'Community health worker visit')
    ]
    
    for name, activity_type, description in activities:
        cur.execute("""
            INSERT INTO intervention_activities (activity_name, activity_type, description)
            VALUES (%s, %s, %s);
        """, (name, activity_type, description))
    
    conn.commit()
    print(f"    [OK] Inserted {len(activities)} activities")


def populate_intervention_costs(conn):
    """Populate intervention_costs with cost structures."""
    cur = conn.cursor(cursor_factory=RealDictCursor)
    
    # Check if already populated
    cur.execute("SELECT COUNT(*) as count FROM intervention_costs;")
    existing_count = cur.fetchone()['count']
    if existing_count > 0:
        print(f"  [SKIP] intervention_costs already populated ({existing_count} records)")
        return
    
    print("  Populating intervention_costs...")
    print("    [NOTE] If foreign key errors occur, costs will be calculated from member_interventions instead")
    
    # Check actual table structure
    cur.execute("""
        SELECT column_name 
        FROM information_schema.columns 
        WHERE table_name = 'intervention_costs'
        ORDER BY ordinal_position;
    """)
    rows = cur.fetchall()
    existing_columns = [row['column_name'] if isinstance(row, dict) else row[0] for row in rows]
    print(f"    Existing columns: {', '.join(existing_columns)}")
    
    has_measure_id = 'measure_id' in existing_columns
    has_cost_per_intervention = 'cost_per_intervention' in existing_columns
    has_unit_cost = 'unit_cost' in existing_columns
    has_cost_date = 'cost_date' in existing_columns
    has_effective_date = 'effective_date' in existing_columns
    
    # Determine which cost column to use
    if has_cost_per_intervention:
        cost_column = 'cost_per_intervention'
    elif has_unit_cost:
        cost_column = 'unit_cost'
    else:
        print("    [ERROR] No cost column found!")
        return
    
    # Determine which date column to use
    if has_effective_date:
        date_column = 'effective_date'
    elif has_cost_date:
        date_column = 'cost_date'
    else:
        date_column = None  # Will use created_date or skip
    
    # Add missing columns if needed
    if not has_measure_id:
        print("    Adding measure_id column...")
        try:
            cur.execute("ALTER TABLE intervention_costs ADD COLUMN measure_id VARCHAR(20);")
            conn.commit()
            has_measure_id = True
        except Exception as e:
            conn.rollback()
            print(f"    [WARN] Could not add measure_id: {e}")
    
    if not has_cost_per_intervention and not has_unit_cost:
        print("    Adding cost_per_intervention column...")
        try:
            cur.execute("ALTER TABLE intervention_costs ADD COLUMN cost_per_intervention DECIMAL(10,2);")
            conn.commit()
            has_cost_per_intervention = True
            cost_column = 'cost_per_intervention'
        except Exception as e:
            conn.rollback()
            print(f"    [WARN] Could not add cost_per_intervention: {e}")
    
    # Get all activities
    cur.execute("SELECT activity_id, activity_name, activity_type FROM intervention_activities;")
    activities = cur.fetchall()
    
    # Get all measures
    cur.execute("SELECT measure_id FROM hedis_measures ORDER BY measure_id;")
    measures = cur.fetchall()
    
    # Cost ranges by activity type
    cost_ranges = {
        'outreach': (15, 45),
        'digital': (5, 20),
        'referral': (50, 150),
        'care_management': (75, 200),
        'in_person': (100, 300),
        'support': (25, 100),
        'clinical': (40, 120),
        'preventive': (30, 80),
        'automated': (2, 10)
    }
    
    costs_inserted = 0
    for activity in activities:
        activity_id = activity['activity_id']
        activity_name = activity['activity_name']
        activity_type_db = activity.get('activity_type', '')
        
        # Determine cost range
        activity_type = activity_type_db.lower() if activity_type_db else None
        
        if not activity_type or activity_type not in cost_ranges:
            # Try to match from name
            for atype, (min_cost, max_cost) in cost_ranges.items():
                if atype in activity_name.lower():
                    activity_type = atype
                    break
        
        if not activity_type or activity_type not in cost_ranges:
            activity_type = 'outreach'  # Default
        
        min_cost, max_cost = cost_ranges[activity_type]
        
        # Create cost for each measure (or just one cost per activity if no measure_id)
        cost = random.uniform(min_cost, max_cost)
        
        # Build insert based on available columns
        # If both unit_cost and cost_per_intervention exist, populate both
        if has_measure_id:
            for measure in measures:
                measure_id = measure['measure_id']
                # Vary cost slightly by measure
                cost_varied = random.uniform(min_cost, max_cost)
                
                # Build column list
                cols = ['activity_id', 'measure_id']
                vals = [activity_id, measure_id]
                
                # Add cost columns
                if has_unit_cost:
                    cols.append('unit_cost')
                    vals.append(round(cost_varied, 2))
                if has_cost_per_intervention:
                    cols.append('cost_per_intervention')
                    vals.append(round(cost_varied, 2))
                
                # Add date column
                if date_column:
                    cols.append(date_column)
                    vals.append('2024-10-01')
                
                # Insert
                try:
                    placeholders = ', '.join(['%s'] * len(vals))
                    col_list = ', '.join(cols)
                    cur.execute(f"""
                        INSERT INTO intervention_costs ({col_list})
                        VALUES ({placeholders});
                    """, tuple(vals))
                    costs_inserted += 1
                except Exception as e:
                    if 'foreign key' in str(e).lower():
                        print(f"    [WARN] Foreign key constraint issue - skipping intervention_costs population")
                        print(f"    [INFO] Costs will be calculated from member_interventions instead")
                        conn.rollback()
                        return
                    else:
                        raise
        else:
            # Just one cost per activity
            cols = ['activity_id']
            vals = [activity_id]
            
            # Add cost columns
            if has_unit_cost:
                cols.append('unit_cost')
                vals.append(round(cost, 2))
            if has_cost_per_intervention:
                cols.append('cost_per_intervention')
                vals.append(round(cost, 2))
            
            # Add date column
            if date_column:
                cols.append(date_column)
                vals.append('2024-10-01')
            
            # Insert
            try:
                placeholders = ', '.join(['%s'] * len(vals))
                col_list = ', '.join(cols)
                cur.execute(f"""
                    INSERT INTO intervention_costs ({col_list})
                    VALUES ({placeholders});
                """, tuple(vals))
                costs_inserted += 1
            except Exception as e:
                if 'foreign key' in str(e).lower():
                    print(f"    [WARN] Foreign key constraint issue - skipping intervention_costs population")
                    print(f"    [INFO] Costs will be calculated from member_interventions instead")
                    conn.rollback()
                    return
                else:
                    raise
    
    conn.commit()
    print(f"    [OK] Inserted {costs_inserted} cost records")


def populate_budget_allocations(conn):
    """Populate budget_allocations for Q4 2024."""
    cur = conn.cursor(cursor_factory=RealDictCursor)
    
    # Check if already populated
    cur.execute("""
        SELECT COUNT(*) as count 
        FROM budget_allocations 
        WHERE period_start >= '2024-10-01' AND period_end <= '2024-12-31';
    """)
    if cur.fetchone()['count'] > 0:
        print("  [SKIP] budget_allocations already populated for Q4 2024")
        return
    
    print("  Populating budget_allocations for Q4 2024...")
    
    # Get all measures
    cur.execute("SELECT measure_id FROM hedis_measures ORDER BY measure_id;")
    measures = cur.fetchall()
    
    # Budget amounts (vary by measure complexity)
    base_budgets = {
        'GSD': 50000, 'KED': 45000, 'CCS': 40000, 'CDC': 35000,
        'CBP': 30000, 'COL': 55000, 'BCS': 60000, 'WCC': 40000,
        'IMA': 35000, 'PPC': 45000, 'AAB': 50000, 'SPC': 40000
    }
    
    for measure in measures:
        measure_id = measure['measure_id']
        budget = base_budgets.get(measure_id, 40000)  # Default $40K
        
        cur.execute("""
            INSERT INTO budget_allocations (measure_id, period_start, period_end, budget_amount)
            VALUES (%s, '2024-10-01', '2024-12-31', %s);
        """, (measure_id, budget))
    
    conn.commit()
    print(f"    [OK] Inserted {len(measures)} budget allocations")


def check_current_counts(conn):
    """Check current intervention counts."""
    cur = conn.cursor(cursor_factory=RealDictCursor)
    
    print("=" * 80)
    print("STEP 1: Checking Current Counts")
    print("=" * 80)
    
    # Check member_interventions
    if check_table_exists(conn, 'member_interventions'):
        cur.execute("SELECT COUNT(*) as count FROM member_interventions;")
        intervention_count = cur.fetchone()['count']
    else:
        intervention_count = 0
    print(f"\n1. member_interventions: {intervention_count:,} records")
    
    if intervention_count > 0:
        cur.execute("""
            SELECT 
                COUNT(DISTINCT member_id) as unique_members,
                COUNT(DISTINCT measure_id) as unique_measures,
                MIN(intervention_date) as earliest_date,
                MAX(intervention_date) as latest_date
            FROM member_interventions;
        """)
        stats = cur.fetchone()
        print(f"   Unique members: {stats['unique_members']:,}")
        print(f"   Unique measures: {stats['unique_measures']}")
        print(f"   Date range: {stats['earliest_date']} to {stats['latest_date']}")
    else:
        print("   [INFO] No interventions found")
    
    # Check gap closures from Phase 2
    cur.execute("""
        SELECT COUNT(*) as count 
        FROM gap_closure_tracking 
        WHERE activity_type = 'gap_closed' 
        AND activity_date >= '2024-10-01' 
        AND activity_date <= '2024-12-31';
    """)
    closure_count = cur.fetchone()['count']
    print(f"\n2. gap_closure_tracking (Q4 2024): {closure_count:,} closures")
    
    # Check actual_spending
    if check_table_exists(conn, 'actual_spending'):
        cur.execute("SELECT COUNT(*) as count FROM actual_spending;")
        spending_count = cur.fetchone()['count']
    else:
        spending_count = 0
    print(f"\n3. actual_spending: {spending_count:,} records")
    
    if spending_count > 0:
        cur.execute("SELECT SUM(amount_spent) as total FROM actual_spending;")
        total_spent = cur.fetchone()['total'] or 0
        print(f"   Total spent: ${total_spent:,.2f}")
    
    # Check budget_allocations
    if check_table_exists(conn, 'budget_allocations'):
        cur.execute("SELECT COUNT(*) as count FROM budget_allocations;")
        budget_count = cur.fetchone()['count']
    else:
        budget_count = 0
    print(f"\n4. budget_allocations: {budget_count:,} records")
    
    if budget_count > 0:
        cur.execute("SELECT SUM(budget_amount) as total FROM budget_allocations;")
        total_budget = cur.fetchone()['total'] or 0
        print(f"   Total budget: ${total_budget:,.2f}")
    
    print("\n" + "=" * 80)
    print("ANALYSIS:")
    print(f"  Current interventions: {intervention_count:,}")
    print(f"  Phase 2 closures: {closure_count:,}")
    print(f"  Success rate needed: {closure_count / max(intervention_count, 1) * 100:.1f}%")
    print(f"  Target interventions: 6,000-8,000 (to achieve ~{closure_count:,} closures at 35% success)")
    print("=" * 80)
    
    return intervention_count, closure_count


def delete_existing_interventions(conn):
    """Delete existing member_interventions and related spending."""
    cur = conn.cursor()
    
    print("\n" + "=" * 80)
    print("STEP 2: Deleting Existing Data")
    print("=" * 80)
    
    # Delete actual_spending first (foreign key constraint)
    print("\n1. Deleting actual_spending records...")
    cur.execute("DELETE FROM actual_spending;")
    spending_deleted = cur.rowcount
    conn.commit()
    print(f"   Deleted {spending_deleted:,} spending records")
    
    # Delete member_interventions
    print("\n2. Deleting member_interventions records...")
    cur.execute("DELETE FROM member_interventions;")
    interventions_deleted = cur.rowcount
    conn.commit()
    print(f"   Deleted {interventions_deleted:,} intervention records")
    
    print("\n[SUCCESS] Existing data cleared!")
    return interventions_deleted, spending_deleted


def get_intervention_activities(conn):
    """Get intervention activity types and their costs."""
    cur = conn.cursor(cursor_factory=RealDictCursor)
    
    # Check which cost column exists
    cur.execute("""
        SELECT column_name 
        FROM information_schema.columns 
        WHERE table_name = 'intervention_costs' 
        AND column_name IN ('cost_per_intervention', 'unit_cost');
    """)
    cost_cols = [row['column_name'] if isinstance(row, dict) else row[0] for row in cur.fetchall()]
    cost_column = 'cost_per_intervention' if 'cost_per_intervention' in cost_cols else ('unit_cost' if 'unit_cost' in cost_cols else None)
    
    if cost_column:
        # Get activities with average cost per measure
        cur.execute(f"""
            SELECT 
                ia.activity_id,
                ia.activity_name,
                ia.activity_type,
                AVG(ic.{cost_column}) as avg_cost_per_intervention
            FROM intervention_activities ia
            LEFT JOIN intervention_costs ic ON ia.activity_id = ic.activity_id
            GROUP BY ia.activity_id, ia.activity_name, ia.activity_type
            ORDER BY ia.activity_id;
        """)
    else:
        # No cost table, just get activities
        cur.execute("""
            SELECT 
                activity_id,
                activity_name,
                activity_type
            FROM intervention_activities
            ORDER BY activity_id;
        """)
    
    activities = cur.fetchall()
    
    # If no costs, get default costs
    for activity in activities:
        if not activity.get('avg_cost_per_intervention'):
            # Use default cost based on activity type
            activity_type = activity.get('activity_type', 'outreach').lower()
            cost_ranges = {
                'outreach': 30, 'digital': 12, 'referral': 100,
                'care_management': 137, 'in_person': 200, 'support': 62,
                'clinical': 80, 'preventive': 55, 'automated': 6
            }
            activity['avg_cost_per_intervention'] = cost_ranges.get(activity_type, 30)
    
    return activities


def generate_interventions(conn, target_count, closure_count, success_rate=0.35):
    """Generate interventions scaled to 10K member population."""
    cur = conn.cursor(cursor_factory=RealDictCursor)
    
    print("\n" + "=" * 80)
    print("STEP 3: Generating Scaled Interventions")
    print("=" * 80)
    
    # Get intervention activities
    print("\n1. Loading intervention activities...")
    activities = get_intervention_activities(conn)
    if not activities:
        print("   [ERROR] No intervention activities found!")
        return 0
    
    print(f"   Found {len(activities)} intervention activity types")
    
    # Get member gaps to link interventions to
    print("\n2. Loading member gaps for Q4 2024...")
    cur.execute("""
        SELECT 
            gap_id,
            member_id,
            measure_id,
            gap_opened_date,
            gap_status
        FROM member_gaps
        WHERE gap_opened_date >= '2024-01-01'
        AND gap_opened_date <= '2024-12-31'
        ORDER BY gap_opened_date
        LIMIT 10000;
    """)
    
    gaps = cur.fetchall()
    print(f"   Found {len(gaps):,} member gaps to link interventions to")
    
    if len(gaps) == 0:
        print("   [ERROR] No member gaps found!")
        return 0
    
    # Calculate how many interventions we need
    # Target: 6,000-8,000 interventions
    # Success rate: 35% average
    # Expected closures: target_count * success_rate ≈ closure_count
    
    num_interventions = target_count
    print(f"\n3. Generating {num_interventions:,} interventions...")
    print(f"   Target success rate: {success_rate*100:.1f}%")
    print(f"   Expected closures: ~{int(num_interventions * success_rate):,}")
    
    # Q4 2024 date range
    q4_start = datetime(2024, 10, 1).date()
    q4_end = datetime(2024, 12, 31).date()
    q4_days = (q4_end - q4_start).days
    
    # Generate interventions
    interventions = []
    intervention_id = 1
    
    # Track which gaps get successful closures
    successful_gaps = set()
    
    # Sample gaps to ensure we have enough
    selected_gaps = random.sample(gaps, min(len(gaps), num_interventions * 2))
    
    for i in range(num_interventions):
        # Select a gap
        gap = random.choice(selected_gaps)
        gap_id = gap['gap_id']
        member_id = gap['member_id']
        measure_id = gap['measure_id']
        
        # Select an intervention activity
        activity = random.choice(activities)
        activity_id = activity['activity_id']
        cost = activity.get('avg_cost_per_intervention') or activity.get('cost_per_intervention') or random.uniform(25, 150)
        
        # Generate intervention date within Q4
        days_offset = random.randint(0, q4_days)
        intervention_date = q4_start + timedelta(days=days_offset)
        
        # Determine success (35% average success rate)
        # But we need to ensure we get approximately closure_count successful ones
        if len(successful_gaps) < closure_count:
            # Still need more successful closures
            success_probability = (closure_count - len(successful_gaps)) / max(num_interventions - i, 1)
            is_successful = random.random() < min(success_probability, 0.5)  # Cap at 50% per intervention
        else:
            # Already have enough, use normal 35% rate
            is_successful = random.random() < success_rate
        
        status = 'completed' if is_successful else 'in_progress'
        
        if is_successful:
            successful_gaps.add(gap_id)
        
        # Generate outcome
        outcomes = [
            'Member engaged successfully',
            'Appointment scheduled',
            'Gap closed',
            'Follow-up needed',
            'Member declined',
            'No response',
            'Completed successfully'
        ]
        outcome = random.choice(outcomes) if not is_successful else 'Gap closed'
        
        interventions.append((
            intervention_id,
            member_id,
            measure_id,
            gap_id,
            activity_id,
            intervention_date,
            status,
            outcome,
            cost
        ))
        
        intervention_id += 1
    
    print(f"   Generated {len(interventions):,} interventions")
    print(f"   Successful closures: {len(successful_gaps):,}")
    
    # Insert interventions
    print("\n4. Inserting interventions into member_interventions...")
    
    # Check table structure
    cur.execute("""
        SELECT column_name 
        FROM information_schema.columns
        WHERE table_name = 'member_interventions'
        ORDER BY ordinal_position;
    """)
    columns = [row['column_name'] for row in cur.fetchall()]
    
    # Build insert based on actual columns
    if 'intervention_id' in columns:
        insert_sql = """
            INSERT INTO member_interventions 
            (intervention_id, member_id, measure_id, gap_id, activity_id, intervention_date, status, outcome, cost_per_intervention)
            VALUES %s;
        """
    else:
        # No intervention_id, let it auto-increment
        insert_sql = """
            INSERT INTO member_interventions 
            (member_id, measure_id, gap_id, activity_id, intervention_date, status, outcome, cost_per_intervention)
            VALUES %s;
        """
        # Remove intervention_id from tuples
        interventions = [t[1:] for t in interventions]
    
    try:
        execute_values(cur, insert_sql, interventions, page_size=500)
        conn.commit()
        print(f"   [SUCCESS] Inserted {len(interventions):,} interventions")
        return len(interventions)
    except Exception as e:
        conn.rollback()
        print(f"   [ERROR] Failed to insert: {e}")
        import traceback
        traceback.print_exc()
        return 0


def recalculate_actual_spending(conn):
    """Recalculate actual_spending based on new interventions."""
    cur = conn.cursor(cursor_factory=RealDictCursor)
    
    print("\n" + "=" * 80)
    print("STEP 4: Recalculating Actual Spending")
    print("=" * 80)
    
    # Clear existing spending
    print("\n1. Clearing existing spending records...")
    cur.execute("DELETE FROM actual_spending;")
    conn.commit()
    print("   Done!")
    
    # Generate spending from interventions
    print("\n2. Calculating spending from interventions...")
    
    # Get spending by measure and month
    cur.execute("""
        INSERT INTO actual_spending (
            measure_id,
            spending_date,
            amount_spent,
            intervention_count,
            description
        )
        SELECT 
            mi.measure_id,
            DATE_TRUNC('month', mi.intervention_date)::DATE as spending_date,
            SUM(mi.cost_per_intervention) as amount_spent,
            COUNT(*) as intervention_count,
            'Q4 2024 Interventions - ' || COUNT(*)::TEXT || ' interventions'
        FROM member_interventions mi
        WHERE mi.intervention_date >= '2024-10-01'
        AND mi.intervention_date <= '2024-12-31'
        GROUP BY mi.measure_id, DATE_TRUNC('month', mi.intervention_date)
        ORDER BY mi.measure_id, spending_date;
    """)
    
    rows_inserted = cur.rowcount
    conn.commit()
    
    print(f"   [SUCCESS] Created {rows_inserted:,} spending records")
    
    # Show summary
    cur.execute("""
        SELECT 
            COUNT(*) as record_count,
            SUM(amount_spent) as total_spent,
            SUM(intervention_count) as total_interventions
        FROM actual_spending;
    """)
    summary = cur.fetchone()
    
    print(f"\n   Spending Summary:")
    print(f"   - Total records: {summary['record_count']:,}")
    print(f"   - Total spent: ${summary['total_spent']:,.2f}")
    print(f"   - Total interventions: {summary['total_interventions']:,}")
    
    return rows_inserted


def verify_budget_allocations(conn):
    """Verify budget allocations are appropriate."""
    cur = conn.cursor(cursor_factory=RealDictCursor)
    
    print("\n" + "=" * 80)
    print("STEP 5: Verifying Budget Allocations")
    print("=" * 80)
    
    # Get budget totals
    cur.execute("""
        SELECT 
            COUNT(*) as budget_count,
            SUM(budget_amount) as total_budget
        FROM budget_allocations
        WHERE period_start >= '2024-10-01' AND period_end <= '2024-12-31';
    """)
    budget = cur.fetchone()
    
    # Get actual spending
    cur.execute("""
        SELECT 
            SUM(amount_spent) as total_spent
        FROM actual_spending;
    """)
    spending = cur.fetchone()
    
    print(f"\nBudget vs Actual (Q4 2024):")
    print(f"  Total Budget: ${budget['total_budget']:,.2f}")
    print(f"  Total Spent: ${spending['total_spent']:,.2f}")
    
    if budget['total_budget']:
        utilization = (spending['total_spent'] / budget['total_budget']) * 100
        print(f"  Utilization: {utilization:.1f}%")
        
        if utilization > 100:
            print(f"  [WARNING] Over budget by ${spending['total_spent'] - budget['total_budget']:,.2f}")
        elif utilization > 90:
            print(f"  [WARNING] Near budget limit")
        else:
            print(f"  [OK] Within budget")
    
    # Show by measure
    print(f"\nBudget by Measure:")
    cur.execute("""
        SELECT 
            ba.measure_id,
            ba.budget_amount,
            COALESCE(SUM(as_spend.amount_spent), 0) as actual_spent,
            ba.budget_amount - COALESCE(SUM(as_spend.amount_spent), 0) as remaining
        FROM budget_allocations ba
        LEFT JOIN actual_spending as_spend ON ba.measure_id = as_spend.measure_id
        WHERE ba.period_start >= '2024-10-01' AND ba.period_end <= '2024-12-31'
        GROUP BY ba.measure_id, ba.budget_amount
        ORDER BY ba.measure_id;
    """)
    
    print(f"{'Measure':<10} {'Budget':<15} {'Spent':<15} {'Remaining':<15} {'Util %':<10}")
    print("-" * 70)
    for row in cur.fetchall():
        util = (row['actual_spent'] / row['budget_amount'] * 100) if row['budget_amount'] > 0 else 0
        print(f"{row['measure_id']:<10} ${row['budget_amount']:>12,.2f} ${row['actual_spent']:>12,.2f} ${row['remaining']:>12,.2f} {util:>8.1f}%")


def show_final_counts(conn):
    """Show final counts for verification."""
    cur = conn.cursor(cursor_factory=RealDictCursor)
    
    print("\n" + "=" * 80)
    print("STEP 6: Final Verification")
    print("=" * 80)
    
    # Member interventions
    cur.execute("SELECT COUNT(*) as count FROM member_interventions;")
    intervention_count = cur.fetchone()['count']
    
    cur.execute("""
        SELECT 
            COUNT(DISTINCT member_id) as unique_members,
            COUNT(DISTINCT measure_id) as unique_measures,
            COUNT(*) FILTER (WHERE status = 'completed') as completed,
            COUNT(*) FILTER (WHERE status = 'in_progress') as in_progress,
            SUM(cost_per_intervention) as total_cost
        FROM member_interventions;
    """)
    intervention_stats = cur.fetchone()
    
    print(f"\n1. member_interventions:")
    print(f"   Total: {intervention_count:,}")
    print(f"   Unique members: {intervention_stats['unique_members']:,}")
    print(f"   Unique measures: {intervention_stats['unique_measures']}")
    print(f"   Completed: {intervention_stats['completed']:,}")
    print(f"   In progress: {intervention_stats['in_progress']:,}")
    print(f"   Total cost: ${intervention_stats['total_cost']:,.2f}")
    
    # Gap closures from Phase 2
    cur.execute("""
        SELECT COUNT(*) as count 
        FROM gap_closure_tracking 
        WHERE activity_type = 'gap_closed' 
        AND activity_date >= '2024-10-01' 
        AND activity_date <= '2024-12-31';
    """)
    closure_count = cur.fetchone()['count']
    
    # Calculate success rate
    success_rate = (intervention_stats['completed'] / intervention_count * 100) if intervention_count > 0 else 0
    
    print(f"\n2. Phase 2 Gap Closures (Q4 2024):")
    print(f"   Total closures: {closure_count:,}")
    print(f"   Intervention success rate: {success_rate:.1f}%")
    print(f"   Match: {'[OK]' if abs(intervention_stats['completed'] - closure_count) < 100 else '[WARN]'} (within 100)")
    
    # Actual spending
    cur.execute("""
        SELECT 
            COUNT(*) as record_count,
            SUM(amount_spent) as total_spent,
            SUM(intervention_count) as total_interventions
        FROM actual_spending;
    """)
    spending = cur.fetchone()
    
    print(f"\n3. actual_spending:")
    print(f"   Records: {spending['record_count']:,}")
    print(f"   Total spent: ${spending['total_spent']:,.2f}")
    print(f"   Interventions tracked: {spending['total_interventions']:,}")
    
    # Budget allocations
    cur.execute("""
        SELECT 
            COUNT(*) as count,
            SUM(budget_amount) as total_budget
        FROM budget_allocations
        WHERE period_start >= '2024-10-01' AND period_end <= '2024-12-31';
    """)
    budget = cur.fetchone()
    
    print(f"\n4. budget_allocations (Q4 2024):")
    print(f"   Records: {budget['count']:,}")
    print(f"   Total budget: ${budget['total_budget']:,.2f}")
    
    if budget['total_budget']:
        utilization = (spending['total_spent'] / budget['total_budget'] * 100)
        print(f"   Budget utilization: {utilization:.1f}%")
    
    print("\n" + "=" * 80)
    print("[SUCCESS] Phase 3 properly scaled to 10K member population!")
    print("=" * 80)


def main():
    """Main execution function."""
    db_config = get_db_config()
    
    print("=" * 80)
    print("FIX PHASE 3 INTERVENTION SCALE")
    print("=" * 80)
    print(f"\nConnecting to database: {db_config['database']}")
    
    try:
        conn = psycopg2.connect(**db_config)
        print("[OK] Connected successfully!\n")
        
        # Step 0: Create Phase 3 tables if needed
        create_phase3_tables(conn)
        
        # Populate base tables if needed
        print("\nPopulating base Phase 3 tables...")
        populate_intervention_activities(conn)
        populate_intervention_costs(conn)
        populate_budget_allocations(conn)
        
        # Step 1: Check current counts
        intervention_count, closure_count = check_current_counts(conn)
        
        # Step 2: Delete existing data
        delete_existing_interventions(conn)
        
        # Step 3: Generate scaled interventions
        # Target: 6,000-8,000 interventions to produce ~2,600 closures at 35% success rate
        target_interventions = random.randint(6000, 8000)
        success_rate = closure_count / target_interventions if target_interventions > 0 else 0.35
        
        # Adjust to ensure we get close to closure_count
        if success_rate > 0.5:
            success_rate = 0.35  # Cap at 35% average
            target_interventions = int(closure_count / success_rate * 1.1)  # Add 10% buffer
        
        interventions_created = generate_interventions(
            conn, 
            target_interventions, 
            closure_count, 
            success_rate
        )
        
        if interventions_created == 0:
            print("[ERROR] Failed to create interventions")
            conn.close()
            return False
        
        # Step 4: Recalculate spending
        recalculate_actual_spending(conn)
        
        # Step 5: Verify budgets
        verify_budget_allocations(conn)
        
        # Step 6: Show final counts
        show_final_counts(conn)
        
        conn.close()
        return True
        
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


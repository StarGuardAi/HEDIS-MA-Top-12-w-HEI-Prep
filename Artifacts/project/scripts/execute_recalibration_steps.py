"""
Execute Recalibration Steps
Run this script to execute all recalibration steps in order.
"""
import sys
import os
from pathlib import Path

# Add phase4_dashboard to path
project_root = Path(__file__).parent.parent
dashboard_path = project_root / "phase4_dashboard"
sys.path.insert(0, str(dashboard_path))

from utils.database import execute_query, test_connection, get_connection


def execute_sql_file(file_path: str) -> bool:
    """Execute a SQL file and return True if successful."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            sql_content = f.read()
        
        # Split by semicolon but keep SQL statements together
        # PostgreSQL requires transactions for some operations
        conn = get_connection()
        conn.autocommit = True  # Allow DDL statements
        cursor = conn.cursor()
        
        try:
            # Execute the entire script
            cursor.execute(sql_content)
            
            # If there are results, fetch them
            try:
                results = cursor.fetchall()
                if results:
                    print(f"\nResults from {Path(file_path).name}:")
                    for row in results:
                        print(f"  {row}")
            except:
                pass  # No results to fetch
            
            cursor.close()
            conn.close()
            print(f"[OK] Successfully executed: {Path(file_path).name}")
            return True
        except Exception as e:
            cursor.close()
            conn.close()
            print(f"[ERROR] Error executing {Path(file_path).name}: {e}")
            return False
    except Exception as e:
        print(f"[ERROR] Error reading {file_path}: {e}")
        return False


def check_database_counts():
    """Step 1: Check current database member counts."""
    print("\n" + "="*60)
    print("STEP 1: CHECKING CURRENT DATABASE MEMBER COUNTS")
    print("="*60)
    
    if not test_connection():
        print("[ERROR] Database connection failed!")
        print("Please ensure PostgreSQL is running and credentials are correct.")
        return False
    
    print("[OK] Database connection successful")
    
    queries = {
        "plan_members": "SELECT COUNT(*) as count FROM plan_members",
        "plan_members_active": "SELECT COUNT(*) as count FROM plan_members WHERE is_active = TRUE",
        "member_gaps": "SELECT COUNT(*) as count FROM member_gaps",
        "member_interventions": "SELECT COUNT(*) as count FROM member_interventions",
        "member_interventions_q4": """SELECT COUNT(*) as count FROM member_interventions 
                                      WHERE intervention_date >= '2024-10-01' 
                                      AND intervention_date <= '2024-12-31'""",
        "plan_context_exists": """SELECT EXISTS (
                                    SELECT FROM information_schema.tables 
                                    WHERE table_schema = 'public' 
                                    AND table_name = 'plan_context'
                                  ) as exists"""
    }
    
    results = {}
    for name, query in queries.items():
        try:
            df = execute_query(query)
            if not df.empty:
                count = df.iloc[0].iloc[0]  # Get first value
                results[name] = count
                print(f"  {name}: {count}")
            else:
                results[name] = 0
                print(f"  {name}: 0 (no data)")
        except Exception as e:
            results[name] = None
            print(f"  {name}: ERROR - {e}")
    
    # Check plan info
    try:
        plan_query = "SELECT plan_id, plan_name, total_enrollment, current_star_rating FROM ma_plans LIMIT 5"
        plan_df = execute_query(plan_query)
        if not plan_df.empty:
            print("\n  Plan Info:")
            for _, row in plan_df.iterrows():
                print(f"    Plan: {row.get('plan_name', 'N/A')}, Members: {row.get('total_enrollment', 'N/A')}, Stars: {row.get('current_star_rating', 'N/A')}")
    except Exception as e:
        print(f"  Plan Info: ERROR - {e}")
    
    return results


def create_plan_context_table():
    """Step 2: Create plan_context table."""
    print("\n" + "="*60)
    print("STEP 2: CREATING PLAN_CONTEXT TABLE")
    print("="*60)
    
    script_path = Path(__file__).parent / "create_plan_context_table.sql"
    
    if not script_path.exists():
        print(f"[ERROR] Script not found: {script_path}")
        return False
    
    return execute_sql_file(str(script_path))


def verify_plan_context():
    """Step 3: Verify plan_context table was created."""
    print("\n" + "="*60)
    print("STEP 3: VERIFYING PLAN_CONTEXT TABLE")
    print("="*60)
    
    try:
        query = "SELECT * FROM plan_context ORDER BY context_id DESC LIMIT 1"
        df = execute_query(query)
        
        if df.empty:
            print("[ERROR] plan_context table is empty!")
            return False
        
        row = df.iloc[0]
        print("[OK] plan_context table verified:")
        print(f"  Plan Name: {row.get('plan_name', 'N/A')}")
        print(f"  Total Members: {row.get('total_members', 'N/A'):,}")
        print(f"  Active Members: {row.get('active_members', 'N/A'):,}")
        print(f"  Star Rating 2024: {row.get('star_rating_2024', 'N/A')}")
        print(f"  Star Rating Projected 2025: {row.get('star_rating_projected_2025', 'N/A')}")
        print(f"  Bonus Revenue at Risk: ${row.get('bonus_revenue_at_risk', 0):,.0f}")
        print(f"  Geographic Region: {row.get('geographic_region', 'N/A')}")
        print(f"  Member Growth YoY: {row.get('member_growth_yoy', 'N/A')}%")
        
        return True
    except Exception as e:
        print(f"[ERROR] Error verifying plan_context: {e}")
        return False


def main():
    """Execute all recalibration steps."""
    print("\n" + "="*60)
    print("HEDIS PORTFOLIO OPTIMIZER - RECALIBRATION STEPS")
    print("="*60)
    
    # Step 1: Check current database counts
    counts = check_database_counts()
    if counts is False:
        print("\n[ERROR] Step 1 failed. Cannot proceed.")
        return
    
    # Step 2: Create plan_context table (if it doesn't exist)
    if counts.get('plan_context_exists') is True:
        print("\n[WARNING] plan_context table already exists. Skipping creation.")
        print("   (If you want to recreate it, drop it first or modify the script)")
    else:
        if not create_plan_context_table():
            print("\n[ERROR] Step 2 failed. Cannot proceed.")
            return
    
    # Step 3: Verify plan_context
    if not verify_plan_context():
        print("\n[ERROR] Step 3 failed.")
        return
    
    # Summary
    print("\n" + "="*60)
    print("[OK] ALL STEPS COMPLETED SUCCESSFULLY!")
    print("="*60)
    print("\nNext steps:")
    print("  1. Test the dashboard: cd phase4_dashboard && streamlit run app.py")
    print("  2. Verify the plan profile context box appears on the landing page")
    print("  3. Test the scenario selector")
    print("  4. Check all pages have storytelling context")
    print("\n")


if __name__ == "__main__":
    main()


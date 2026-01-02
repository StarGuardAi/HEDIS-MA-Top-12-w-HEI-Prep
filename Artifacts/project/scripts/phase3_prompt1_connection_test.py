#!/usr/bin/env python3
"""
Phase 3 Prompt 1: Connection Test
Verify PostgreSQL connection and Phase 1 & 2 tables
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


def test_connection_and_tables():
    """Test database connection and verify Phase 1 & 2 tables."""
    db_config = get_db_config()
    
    print("=" * 80)
    print("PHASE 3 PROMPT 1: CONNECTION TEST")
    print("=" * 80)
    print()
    print(f"Connecting to database: {db_config['database']}")
    print(f"Host: {db_config['host']}:{db_config['port']}")
    print(f"User: {db_config['user']}")
    print()
    
    try:
        # Test connection
        print("1. Testing database connection...")
        conn = psycopg2.connect(**db_config)
        print("   [OK] Connection successful!")
        print()
        
        cur = conn.cursor(cursor_factory=RealDictCursor)
        
        # Check PostgreSQL version
        cur.execute("SELECT version();")
        version = cur.fetchone()['version']
        print(f"   PostgreSQL Version: {version.split(',')[0]}")
        print()
        
        # Verify Phase 1 & 2 tables exist
        print("2. Verifying Phase 1 & 2 tables exist...")
        print("-" * 80)
        
        required_tables = [
            "measures",
            "plans", 
            "members",
            "member_gaps",
            "gap_closure_events",
            "velocity_metrics"
        ]
        
        # Check which tables exist
        cur.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public' 
            AND table_type = 'BASE TABLE'
            ORDER BY table_name;
        """)
        existing_tables = [row['table_name'] for row in cur.fetchall()]
        
        # Check for exact matches and similar names
        table_status = {}
        for table in required_tables:
            # Check for exact match
            if table in existing_tables:
                table_status[table] = table
            else:
                # Check for similar names (case-insensitive, with prefixes/suffixes)
                matches = [t for t in existing_tables if table.lower() in t.lower() or t.lower() in table.lower()]
                if matches:
                    table_status[table] = matches[0]  # Use first match
                else:
                    table_status[table] = None
        
        # Show table status
        all_found = True
        for required_table, actual_table in table_status.items():
            if actual_table:
                status = "[OK]"
                all_found = all_found and True
            else:
                status = "[X]"
                all_found = False
                actual_table = "NOT FOUND"
            
            print(f"   {status} {required_table:25s} -> {actual_table}")
        
        if not all_found:
            print()
            print("   [WARN] Some tables not found. Checking for similar table names...")
            print(f"   Found {len(existing_tables)} tables in database:")
            for table in sorted(existing_tables)[:20]:  # Show first 20
                print(f"      - {table}")
            if len(existing_tables) > 20:
                print(f"      ... and {len(existing_tables) - 20} more")
        
        print()
        
        # Count records in each table
        print("3. Counting records in each table...")
        print("-" * 80)
        
        table_counts = {}
        for required_table, actual_table in table_status.items():
            if actual_table:
                try:
                    cur.execute(f"SELECT COUNT(*) as count FROM {actual_table};")
                    count = cur.fetchone()['count']
                    table_counts[required_table] = count
                    print(f"   {required_table:25s}: {count:,} records")
                except Exception as e:
                    print(f"   {required_table:25s}: ERROR - {str(e)}")
                    table_counts[required_table] = None
            else:
                print(f"   {required_table:25s}: N/A (table not found)")
                table_counts[required_table] = None
        
        print()
        print("=" * 80)
        print("SUMMARY")
        print("=" * 80)
        
        if all_found:
            print("[SUCCESS] All Phase 1 & 2 tables found!")
        else:
            print("[WARNING] Some tables missing. Please verify Phase 1 & 2 are complete.")
        
        print()
        print("Table Record Counts:")
        for table, count in table_counts.items():
            if count is not None:
                print(f"  - {table}: {count:,} records")
            else:
                print(f"  - {table}: Not available")
        
        print()
        if all_found and all(c is not None and c > 0 for c in table_counts.values()):
            print("[SUCCESS] Phase 1 & 2 are complete and ready for Phase 3!")
        else:
            print("[WARNING] Please complete Phase 1 & 2 before proceeding with Phase 3.")
        
        print("=" * 80)
        
        conn.close()
        return all_found and all(c is not None and c > 0 for c in table_counts.values())
        
    except psycopg2.OperationalError as e:
        print(f"   [ERROR] Connection failed: {e}")
        print()
        print("Troubleshooting:")
        print("  1. Check if PostgreSQL service is running")
        print("  2. Verify connection settings:")
        print(f"     - Host: {db_config['host']}")
        print(f"     - Port: {db_config['port']}")
        print(f"     - Database: {db_config['database']}")
        print(f"     - User: {db_config['user']}")
        print("  3. Set environment variables if needed:")
        print("     - DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASSWORD")
        return False
        
    except Exception as e:
        print(f"   [ERROR] Error: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = test_connection_and_tables()
    sys.exit(0 if success else 1)


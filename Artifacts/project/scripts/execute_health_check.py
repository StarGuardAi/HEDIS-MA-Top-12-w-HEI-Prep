#!/usr/bin/env python3
"""
Execute Phase 3 Health Check SQL
"""

import sys
import os
import psycopg2
from psycopg2.extras import RealDictCursor

def get_db_config():
    """Get database configuration from environment or defaults."""
    return {
        "host": os.getenv("DB_HOST", "localhost"),
        "database": os.getenv("DB_NAME", "hedis_portfolio"),
        "user": os.getenv("DB_USER", "hedis_api"),
        "password": os.getenv("DB_PASSWORD", "hedis_password"),
        "port": os.getenv("DB_PORT", "5432")
    }

def execute_sql_file(filepath):
    """Execute SQL file and return results."""
    db_config = get_db_config()
    
    try:
        conn = psycopg2.connect(**db_config)
        cur = conn.cursor(cursor_factory=RealDictCursor)
        
        # Read SQL file
        with open(filepath, 'r', encoding='utf-8') as f:
            sql_content = f.read()
        
        # Split by semicolons and execute each statement
        statements = sql_content.split(';')
        
        results = []
        for stmt in statements:
            stmt = stmt.strip()
            if not stmt or stmt.startswith('--') or stmt.startswith('\\echo'):
                # Handle \echo commands
                if stmt.startswith('\\echo'):
                    echo_text = stmt.replace('\\echo', '').strip().strip("'")
                    if echo_text:
                        print(echo_text)
                continue
            
            try:
                cur.execute(stmt)
                if cur.description:
                    # Query returned results
                    rows = cur.fetchall()
                    if rows:
                        results.append((stmt[:50] + '...', rows))
                conn.commit()
            except psycopg2.ProgrammingError as e:
                # Some statements don't return results
                if "no results to fetch" not in str(e).lower():
                    print(f"Warning: {e}")
                conn.rollback()
            except Exception as e:
                print(f"Error executing statement: {e}")
                conn.rollback()
        
        # Print results
        for query, rows in results:
            if rows:
                # Print column headers
                if rows:
                    headers = list(rows[0].keys())
                    print("\n" + " | ".join(headers))
                    print("-" * (sum(len(str(h)) for h in headers) + len(headers) * 3))
                    # Print rows
                    for row in rows:
                        print(" | ".join(str(row[h]) if row[h] is not None else "NULL" for h in headers))
                print()
        
        conn.close()
        return True
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    script_dir = os.path.dirname(os.path.abspath(__file__))
    sql_file = os.path.join(script_dir, "phase3_health_check.sql")
    
    if not os.path.exists(sql_file):
        print(f"Error: {sql_file} not found")
        sys.exit(1)
    
    print("=" * 100)
    print("PHASE 3 HEALTH CHECK - EXECUTING SQL")
    print("=" * 100)
    print()
    
    execute_sql_file(sql_file)
    
    print("=" * 100)
    print("HEALTH CHECK COMPLETE")
    print("=" * 100)


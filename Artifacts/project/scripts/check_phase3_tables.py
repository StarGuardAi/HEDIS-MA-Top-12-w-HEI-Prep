#!/usr/bin/env python3
"""Check what Phase 3 tables exist"""

import os
import psycopg2
from psycopg2.extras import RealDictCursor

def get_db_config():
    return {
        "host": os.getenv("DB_HOST", "localhost"),
        "database": os.getenv("DB_NAME", "hedis_portfolio"),
        "user": os.getenv("DB_USER", "hedis_api"),
        "password": os.getenv("DB_PASSWORD", "hedis_password"),
        "port": os.getenv("DB_PORT", "5432")
    }

conn = psycopg2.connect(**get_db_config())
cur = conn.cursor(cursor_factory=RealDictCursor)

print("Checking Phase 3 tables...")
print("=" * 80)

phase3_tables = [
    'intervention_activities',
    'intervention_costs',
    'member_interventions',
    'budget_allocations',
    'actual_spending'
]

for table in phase3_tables:
    cur.execute("""
        SELECT EXISTS (
            SELECT FROM information_schema.tables 
            WHERE table_schema = 'public' 
            AND table_name = %s
        );
    """, (table,))
    exists = cur.fetchone()['exists']
    
    if exists:
        cur.execute(f"SELECT COUNT(*) as count FROM {table};")
        count = cur.fetchone()['count']
        print(f"[EXISTS] {table}: {count:,} records")
    else:
        print(f"[MISSING] {table}")

conn.close()


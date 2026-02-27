#!/usr/bin/env python3
"""Quick script to check actual table structures"""

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

print("=" * 80)
print("member_gaps structure:")
print("=" * 80)
cur.execute("""
    SELECT column_name, data_type, is_nullable
    FROM information_schema.columns
    WHERE table_name = 'member_gaps'
    ORDER BY ordinal_position;
""")
for col in cur.fetchall():
    print(f"  {col['column_name']:<30} {col['data_type']:<20} nullable={col['is_nullable']}")

print("\n" + "=" * 80)
print("gap_closure_tracking structure:")
print("=" * 80)
cur.execute("""
    SELECT column_name, data_type, is_nullable
    FROM information_schema.columns
    WHERE table_name = 'gap_closure_tracking'
    ORDER BY ordinal_position;
""")
for col in cur.fetchall():
    print(f"  {col['column_name']:<30} {col['data_type']:<20} nullable={col['is_nullable']}")

print("\n" + "=" * 80)
print("Sample from member_gaps:")
print("=" * 80)
cur.execute("SELECT * FROM member_gaps LIMIT 1;")
sample = cur.fetchone()
if sample:
    for key, value in sample.items():
        print(f"  {key}: {value}")

conn.close()


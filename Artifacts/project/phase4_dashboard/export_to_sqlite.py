"""
Export PostgreSQL data to SQLite for Streamlit Cloud deployment
Exports Phase 3 HEDIS Portfolio data to SQLite database
"""
import os
import sys
import sqlite3
from pathlib import Path
from typing import List, Optional

import pandas as pd
import psycopg2
from psycopg2.extras import RealDictCursor

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))


def get_postgres_config():
    """Get PostgreSQL configuration from environment variables."""
    import os
    port = os.getenv("DB_PORT", "5432")
    # Convert to int if it's a string
    if isinstance(port, str):
        port = int(port)
    return {
        "host": os.getenv("DB_HOST", "localhost"),
        "database": os.getenv("DB_NAME", "hedis_portfolio"),
        "user": os.getenv("DB_USER", "hedis_api"),
        "password": os.getenv("DB_PASSWORD", "hedis_password"),
        "port": port,
    }


def get_postgres_connection():
    """Get PostgreSQL connection using environment variables."""
    config = get_postgres_config()
    return psycopg2.connect(**config)


def get_sqlite_connection(db_path: str):
    """Get SQLite connection."""
    # Create data directory if it doesn't exist
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    return sqlite3.connect(db_path)


def export_table(pg_conn, sqlite_conn, table_name: str, schema: Optional[str] = None) -> bool:
    """
    Export a single table from PostgreSQL to SQLite.
    
    Args:
        pg_conn: PostgreSQL connection
        sqlite_conn: SQLite connection
        table_name: Name of the table to export
        schema: Optional schema name (default: public)
        
    Returns:
        True if successful, False otherwise
    """
    try:
        # Get full table name
        full_table_name = f"{schema}.{table_name}" if schema else table_name
        
        # Check if table exists in PostgreSQL
        pg_cursor = pg_conn.cursor()
        pg_cursor.execute("""
            SELECT EXISTS (
                SELECT FROM information_schema.tables 
                WHERE table_schema = %s 
                AND table_name = %s
            );
        """, (schema or 'public', table_name))
        
        if not pg_cursor.fetchone()[0]:
            print(f"  WARNING: Table '{table_name}' does not exist in PostgreSQL, skipping...")
            pg_cursor.close()
            return False
        
        # Get table data
        print(f"  Exporting {table_name}...")
        query = f'SELECT * FROM "{full_table_name}"'
        df = pd.read_sql_query(query, pg_conn)
        
        if df.empty:
            print(f"  WARNING: Table '{table_name}' is empty, skipping...")
            pg_cursor.close()
            return False
        
        # Get column types from PostgreSQL
        pg_cursor.execute("""
            SELECT 
                column_name,
                data_type,
                character_maximum_length
            FROM information_schema.columns
            WHERE table_schema = %s 
            AND table_name = %s
            ORDER BY ordinal_position;
        """, (schema or 'public', table_name))
        
        columns_info = pg_cursor.fetchall()
        pg_cursor.close()
        
        # Create table in SQLite with appropriate types
        sqlite_cursor = sqlite_conn.cursor()
        
        # Build CREATE TABLE statement
        column_defs = []
        for col_name, data_type, max_length in columns_info:
            sqlite_type = map_postgres_to_sqlite_type(data_type, max_length)
            column_defs.append(f'"{col_name}" {sqlite_type}')
        
        create_table_sql = f'''
            CREATE TABLE IF NOT EXISTS "{table_name}" (
                {', '.join(column_defs)}
            );
        '''
        
        sqlite_cursor.execute(create_table_sql)
        
        # Insert data
        df.to_sql(table_name, sqlite_conn, if_exists='replace', index=False)
        
        row_count = len(df)
        print(f"  SUCCESS: Exported {row_count:,} rows from {table_name}")
        
        return True
        
    except Exception as e:
        print(f"  ERROR: Error exporting {table_name}: {e}")
        return False


def map_postgres_to_sqlite_type(pg_type: str, max_length: Optional[int] = None) -> str:
    """Map PostgreSQL data types to SQLite types."""
    pg_type_lower = pg_type.lower()
    
    # Numeric types
    if pg_type_lower in ('integer', 'int', 'int4', 'serial', 'serial4'):
        return 'INTEGER'
    elif pg_type_lower in ('bigint', 'int8', 'bigserial', 'serial8'):
        return 'INTEGER'
    elif pg_type_lower in ('smallint', 'int2', 'smallserial', 'serial2'):
        return 'INTEGER'
    elif pg_type_lower in ('real', 'float4'):
        return 'REAL'
    elif pg_type_lower in ('double precision', 'float8', 'float', 'numeric', 'decimal', 'money'):
        return 'REAL'
    # Text types
    elif pg_type_lower in ('text', 'varchar', 'char', 'character varying', 'character'):
        return 'TEXT'
    # Date/time types
    elif pg_type_lower in ('date', 'time', 'timestamp', 'timestamp without time zone', 
                           'timestamp with time zone', 'timestamptz'):
        return 'TEXT'  # SQLite stores dates as TEXT
    # Boolean
    elif pg_type_lower in ('boolean', 'bool'):
        return 'INTEGER'  # SQLite uses 0/1 for boolean
    # JSON
    elif pg_type_lower in ('json', 'jsonb'):
        return 'TEXT'
    # UUID
    elif pg_type_lower == 'uuid':
        return 'TEXT'
    # Default
    else:
        return 'TEXT'


def export_all_tables():
    """Export all required tables from PostgreSQL to SQLite."""
    
    # Tables to export (mapping: user_requested_name -> actual_table_name)
    tables_to_export = [
        ('hedis_measures', 'measures'),  # Export as 'measures' for compatibility
        ('plan_context', 'plans'),      # Export as 'plans' for compatibility
        ('members', 'members'),
        ('member_gaps', 'member_gaps'),
        ('member_interventions', 'member_interventions'),
        ('intervention_activities', 'intervention_activities'),  # Also needed for joins
        ('budget_allocations', 'budget_allocations'),
        ('actual_spending', 'actual_spending'),
        ('gap_closure_tracking', 'gap_closure_tracking'),
        ('gap_velocity_metrics', 'gap_velocity_metrics'),
    ]
    
    # Output path
    script_dir = Path(__file__).parent
    data_dir = script_dir / 'data'
    db_path = data_dir / 'hedis_portfolio.db'
    
    print("=" * 60)
    print("PostgreSQL to SQLite Export")
    print("=" * 60)
    print(f"\nOutput: {db_path}")
    print(f"Tables to export: {len(tables_to_export)}\n")
    
    # Connect to databases
    try:
        print("Connecting to PostgreSQL...")
        pg_conn = get_postgres_connection()
        print("PostgreSQL connected")
    except Exception as e:
        print(f"Failed to connect to PostgreSQL: {e}")
        print("\nMake sure PostgreSQL is running and credentials are correct.")
        return False
    
    try:
        print(f"\nCreating SQLite database: {db_path}")
        sqlite_conn = get_sqlite_connection(str(db_path))
        print("SQLite database created")
    except Exception as e:
        print(f"Failed to create SQLite database: {e}")
        pg_conn.close()
        return False
    
    # Export tables
    print("\n" + "=" * 60)
    print("Exporting Tables")
    print("=" * 60 + "\n")
    
    success_count = 0
    failed_count = 0
    
    for actual_table_name, export_table_name in tables_to_export:
        # Try exporting with actual table name first
        if export_table(pg_conn, sqlite_conn, actual_table_name):
            success_count += 1
            # If export name is different, create a view or copy
            if actual_table_name != export_table_name:
                try:
                    sqlite_cursor = sqlite_conn.cursor()
                    # Create a view with the alternative name
                    sqlite_cursor.execute(f'''
                        CREATE VIEW IF NOT EXISTS "{export_table_name}" AS 
                        SELECT * FROM "{actual_table_name}";
                    ''')
                    sqlite_conn.commit()
                    print(f"  Created view '{export_table_name}' -> '{actual_table_name}'")
                except Exception as e:
                    print(f"  ⚠️  Could not create view '{export_table_name}': {e}")
        else:
            failed_count += 1
    
    # Create indexes for better performance
    print("\n" + "=" * 60)
    print("Creating Indexes")
    print("=" * 60 + "\n")
    
    indexes = [
        ("member_interventions", "intervention_date"),
        ("member_interventions", "measure_id"),
        ("member_interventions", "activity_id"),
        ("member_interventions", "status"),
        ("budget_allocations", "measure_id"),
        ("actual_spending", "measure_id"),
        ("actual_spending", "spending_date"),
        ("member_gaps", "measure_id"),
        ("gap_closure_tracking", "measure_id"),
    ]
    
    sqlite_cursor = sqlite_conn.cursor()
    for table_name, column_name in indexes:
        try:
            index_name = f"idx_{table_name}_{column_name}"
            sqlite_cursor.execute(f'''
                CREATE INDEX IF NOT EXISTS {index_name} 
                ON "{table_name}" ("{column_name}");
            ''')
            print(f"  Created index: {index_name}")
        except Exception as e:
            # Table might not exist, skip
            pass
    
    sqlite_conn.commit()
    
    # Close connections
    sqlite_conn.close()
    pg_conn.close()
    
    # Summary
    print("\n" + "=" * 60)
    print("Export Summary")
    print("=" * 60)
    print(f"Successfully exported: {success_count} tables")
    if failed_count > 0:
        print(f"Failed/Skipped: {failed_count} tables")
    print(f"\nSQLite database: {db_path}")
    print(f"Size: {db_path.stat().st_size / 1024 / 1024:.2f} MB")
    print("\nExport complete!")
    
    return success_count > 0


if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("HEDIS Portfolio - PostgreSQL to SQLite Export")
    print("=" * 60 + "\n")
    
    success = export_all_tables()
    
    if success:
        print("\nReady for Streamlit Cloud deployment!")
        print("The SQLite database will be used when PostgreSQL secrets are not available.")
        sys.exit(0)
    else:
        print("\nExport failed. Please check the errors above.")
        sys.exit(1)


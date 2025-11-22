"""
Phase 4 Dashboard - Database Connection Utilities
Handles PostgreSQL and SQLite connections for hedis_portfolio database
Auto-detects which database to use based on available configuration
"""
import os
import sqlite3
from pathlib import Path
from typing import Dict, List, Optional, Union

import pandas as pd

# Import streamlit for secrets (with fallback for non-streamlit contexts)
try:
    import streamlit as st
    STREAMLIT_AVAILABLE = True
except ImportError:
    STREAMLIT_AVAILABLE = False
    st = None

# Try importing PostgreSQL driver (optional)
try:
    import psycopg2
    from psycopg2.extras import RealDictCursor
    POSTGRES_AVAILABLE = True
except ImportError:
    POSTGRES_AVAILABLE = False

# Database type detection
_db_type = None  # 'postgres' or 'sqlite'
_db_status_message = None  # Status message about which database is being used


def get_db_type() -> str:
    """
    Detect which database to use.
    Priority: SQLite (if file exists) > PostgreSQL fallback
    This prioritizes SQLite for cloud deployment where SQLite is preferred.
    """
    global _db_type, _db_status_message
    
    if _db_type:
        return _db_type
    
    # FIRST: Check if SQLite database file exists (priority for cloud deployment)
    sqlite_path = get_sqlite_path()
    sqlite_exists = os.path.exists(sqlite_path)
    
    if sqlite_exists:
        # SQLite file exists, try to use it first (preferred for cloud deployment)
        try:
            # Test SQLite connection
            test_conn = sqlite3.connect(sqlite_path)
            test_conn.close()
            _db_type = 'sqlite'
            _db_status_message = f"✅ Using SQLite database ({sqlite_path})"
            return 'sqlite'
        except Exception:
            # SQLite connection failed, will try PostgreSQL as fallback
            pass
    
    # SECOND: Try PostgreSQL if SQLite is not available or failed
    has_postgres_config = False
    
    # Check Streamlit secrets (only if secrets file exists)
    if STREAMLIT_AVAILABLE and hasattr(st, 'secrets'):
        try:
            if 'postgres' in st.secrets:
                has_postgres_config = True
        except (FileNotFoundError, AttributeError, KeyError):
            # Secrets file doesn't exist or postgres key not found
            pass
    # Check environment variables
    elif os.getenv("DB_HOST") or os.getenv("DB_NAME") or os.getenv("DB_USER"):
        has_postgres_config = True
    
    # If PostgreSQL config exists and driver is available, try PostgreSQL
    if has_postgres_config and POSTGRES_AVAILABLE:
        # Try to connect to PostgreSQL, but suppress errors
        try:
            config = get_postgres_config()
            test_conn = psycopg2.connect(**config)
            test_conn.close()
            _db_type = 'postgres'
            _db_status_message = f"✅ Using PostgreSQL database ({config.get('host', 'localhost')}:{config.get('database', 'hedis_portfolio')})"
            return 'postgres'
        except Exception:
            # PostgreSQL connection failed, will fall back to SQLite
            pass
    
    # Fallback to SQLite (will create file if it doesn't exist)
    # This is the default for cloud deployment
    _db_type = 'sqlite'
    _db_status_message = f"✅ Using SQLite database for demo ({sqlite_path})"
    return 'sqlite'


def get_postgres_config() -> Dict[str, Union[str, int]]:
    """
    Get PostgreSQL configuration from Streamlit secrets, environment variables, or defaults.
    Priority: st.secrets > environment variables > defaults
    """
    # Try Streamlit secrets first (for Streamlit Cloud deployment)
    if STREAMLIT_AVAILABLE and hasattr(st, 'secrets'):
        try:
            if 'postgres' in st.secrets:
                port = st.secrets["postgres"].get("port", 5432)
                # Convert to int if it's a string
                if isinstance(port, str):
                    port = int(port)
                return {
                    "host": st.secrets["postgres"]["host"],
                    "database": st.secrets["postgres"]["database"],
                    "user": st.secrets["postgres"]["user"],
                    "password": st.secrets["postgres"]["password"],
                    "port": port,
                }
        except (FileNotFoundError, AttributeError, KeyError):
            # Secrets file doesn't exist or postgres key not found, fall through to env vars
            pass
    
    # Fallback to environment variables (for local development)
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


def get_sqlite_path() -> str:
    """Get path to SQLite database file."""
    # Try to get from Streamlit secrets first (only if secrets file exists)
    if STREAMLIT_AVAILABLE and hasattr(st, 'secrets'):
        try:
            if 'sqlite' in st.secrets:
                return st.secrets["sqlite"]["path"]
        except (FileNotFoundError, AttributeError, KeyError):
            # Secrets file doesn't exist or sqlite key not found, use default path
            pass
    
    # Default path relative to dashboard directory
    script_dir = Path(__file__).parent.parent
    db_path = script_dir / 'data' / 'hedis_portfolio.db'
    return str(db_path)


def get_connection():
    """
    Get database connection.
    Priority: SQLite first (for cloud deployment), PostgreSQL second (for local dev)
    """
    global _db_type, _db_status_message
    
    # First: Try SQLite (default for cloud deployment)
    sqlite_path = Path(__file__).parent.parent / "data" / "hedis_portfolio.db"
    
    if sqlite_path.exists():
        try:
            conn = sqlite3.connect(str(sqlite_path))
            
            # Test connection with a simple query
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM member_interventions")
            count = cursor.fetchone()[0]
            cursor.close()
            
            # Set status message for display in app
            _db_type = 'sqlite'
            _db_status_message = f"✅ Using SQLite Database ({count:,} interventions)"
            
            # Only show message once per session
            if STREAMLIT_AVAILABLE and hasattr(st, 'sidebar') and hasattr(st, 'session_state'):
                try:
                    if 'db_status_shown' not in st.session_state:
                        st.sidebar.success(f"✅ Database Connected ({count:,} interventions)")
                        st.session_state.db_status_shown = True
                except:
                    pass
            return conn
        except Exception as e:
            # SQLite file exists but connection failed, try PostgreSQL
            if STREAMLIT_AVAILABLE and hasattr(st, 'sidebar'):
                try:
                    st.sidebar.error(f"❌ Database Error: {str(e)}")
                except:
                    pass
    
    # Second: Try PostgreSQL (for local development)
    if not POSTGRES_AVAILABLE:
        # PostgreSQL driver not available, create SQLite file if needed
        os.makedirs(sqlite_path.parent, exist_ok=True)
        conn = sqlite3.connect(str(sqlite_path))
        _db_type = 'sqlite'
        _db_status_message = "✅ Using SQLite Database (new file created)"
        if STREAMLIT_AVAILABLE and hasattr(st, 'sidebar') and hasattr(st, 'session_state'):
            try:
                if 'db_status_shown' not in st.session_state:
                    st.sidebar.warning("⚠️ Database file not found - created new empty database")
                    st.session_state.db_status_shown = True
            except:
                pass
        return conn
    
    try:
        # Get PostgreSQL configuration
        config = get_postgres_config()
        conn = psycopg2.connect(**config)
        # Set status message for display in app
        _db_type = 'postgres'
        _db_status_message = "✅ Using PostgreSQL Database"
        if STREAMLIT_AVAILABLE and hasattr(st, 'sidebar') and hasattr(st, 'session_state'):
            try:
                if 'db_status_shown' not in st.session_state:
                    st.sidebar.success("✅ Using PostgreSQL Database")
                    st.session_state.db_status_shown = True
            except:
                pass
        return conn
    except Exception as e:
        # PostgreSQL failed, fall back to SQLite (create if needed)
        os.makedirs(sqlite_path.parent, exist_ok=True)
        try:
            conn = sqlite3.connect(str(sqlite_path))
            _db_type = 'sqlite'
            _db_status_message = "✅ Using SQLite Database"
            
            # Show warning in sidebar if Streamlit is available
            if STREAMLIT_AVAILABLE and hasattr(st, 'sidebar') and hasattr(st, 'session_state'):
                try:
                    if 'db_status_shown' not in st.session_state:
                        st.sidebar.warning("PostgreSQL unavailable, using SQLite")
                        st.sidebar.success("✅ Using SQLite Database")
                        st.session_state.db_status_shown = True
                except:
                    pass
            
            return conn
        except Exception as sqlite_error:
            # Both databases failed - this is a critical error
            error_msg = f"Cannot connect to database. PostgreSQL error: {e}. SQLite error: {sqlite_error}"
            if STREAMLIT_AVAILABLE and hasattr(st, 'sidebar'):
                try:
                    st.sidebar.error("❌ No database connection available")
                except:
                    pass
            raise Exception(error_msg)


def execute_query(query: str, params: Optional[tuple] = None) -> pd.DataFrame:
    """
    Execute a SQL query and return results as a pandas DataFrame.
    Automatically handles PostgreSQL and SQLite syntax differences.
    
    Args:
        query: SQL query string (will be converted for SQLite if needed)
        params: Optional parameters for parameterized queries
        
    Returns:
        DataFrame with query results
    """
    db_type = get_db_type()
    conn = get_connection()
    
    try:
        # Convert query for SQLite if needed
        if db_type == 'sqlite':
            query = convert_query_for_sqlite(query)
        
        if db_type == 'postgres':
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            rows = cursor.fetchall()
            df = pd.DataFrame(rows)
            cursor.close()
        else:
            # SQLite - use pandas directly for better compatibility
            if params:
                df = pd.read_sql_query(query, conn, params=params)
            else:
                df = pd.read_sql_query(query, conn)
        
        return df
    except Exception as e:
        raise Exception(f"Database query error: {e}")
    finally:
        conn.close()


def convert_query_for_sqlite(query: str) -> str:
    """
    Convert PostgreSQL-specific SQL syntax to SQLite-compatible syntax.
    Handles common PostgreSQL functions that SQLite doesn't support.
    """
    import re
    
    # Replace COUNT(*) FILTER (WHERE condition) with SUM(CASE WHEN condition THEN 1 ELSE 0 END)
    def replace_count_filter(match):
        condition = match.group(1)
        return f"SUM(CASE WHEN {condition} THEN 1 ELSE 0 END)"
    
    query = re.sub(
        r"COUNT\s*\(\s*\*\s*\)\s*FILTER\s*\(\s*WHERE\s+([^)]+)\s*\)",
        replace_count_filter,
        query,
        flags=re.IGNORECASE
    )
    
    # Replace SUM(column) FILTER (WHERE condition) with SUM(CASE WHEN condition THEN column ELSE 0 END)
    def replace_sum_filter(match):
        column = match.group(1)
        condition = match.group(2)
        return f"SUM(CASE WHEN {condition} THEN {column} ELSE 0 END)"
    
    query = re.sub(
        r"SUM\s*\(\s*([^)]+)\s*\)\s*FILTER\s*\(\s*WHERE\s+([^)]+)\s*\)",
        replace_sum_filter,
        query,
        flags=re.IGNORECASE
    )
    
    # Replace AVG(column) FILTER (WHERE condition) with AVG(CASE WHEN condition THEN column ELSE NULL END)
    def replace_avg_filter(match):
        column = match.group(1)
        condition = match.group(2)
        return f"AVG(CASE WHEN {condition} THEN {column} ELSE NULL END)"
    
    query = re.sub(
        r"AVG\s*\(\s*([^)]+)\s*\)\s*FILTER\s*\(\s*WHERE\s+([^)]+)\s*\)",
        replace_avg_filter,
        query,
        flags=re.IGNORECASE
    )
    
    # Replace TO_CHAR(date, 'YYYY-MM') with strftime('%Y-%m', date)
    query = re.sub(
        r"TO_CHAR\s*\(\s*([^,]+)\s*,\s*'YYYY-MM'\s*\)",
        r"strftime('%Y-%m', \1)",
        query,
        flags=re.IGNORECASE
    )
    
    # Replace DATE_TRUNC('month', date)::DATE with date(date, 'start of month')
    # Handle both with and without ::DATE cast
    query = re.sub(
        r"DATE_TRUNC\s*\(\s*'month'\s*,\s*([^)]+)\s*\)(?:\s*::\s*DATE)?",
        r"date(\1, 'start of month')",
        query,
        flags=re.IGNORECASE
    )
    
    # Replace ::DECIMAL, ::DATE, ::INTEGER type casts (but keep them for DATE_TRUNC above)
    query = re.sub(r'::\s*\w+', '', query)
    
    # Replace NULLIF(a, b) with CASE WHEN a = b THEN NULL ELSE a END
    query = re.sub(
        r'NULLIF\s*\(\s*([^,]+)\s*,\s*([^)]+)\s*\)',
        r"CASE WHEN \1 = \2 THEN NULL ELSE \1 END",
        query,
        flags=re.IGNORECASE
    )
    
    # Replace ROUND with SQLite-compatible version (SQLite supports ROUND)
    # No change needed, but ensure it's compatible
    
    return query


def get_db_status_message() -> str:
    """Get status message about which database is being used."""
    global _db_status_message
    if _db_status_message:
        return _db_status_message
    
    # Force detection to generate status message
    get_db_type()
    return _db_status_message or "Checking database connection..."


def test_connection() -> bool:
    """
    Test database connection and return True if successful.
    Returns False if connection fails.
    """
    try:
        conn = get_connection()
        db_type = get_db_type()
        
        if db_type == 'postgres':
            cursor = conn.cursor()
            cursor.execute("SELECT 1;")
            cursor.close()
        else:
            # SQLite
            cursor = conn.cursor()
            cursor.execute("SELECT 1;")
            cursor.close()
        
        conn.close()
        return True
    except Exception as e:
        # Suppress error messages - connection failed
        return False


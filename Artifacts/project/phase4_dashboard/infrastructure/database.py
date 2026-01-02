"""
Database Management

Centralized database connection and query management.
"""

from typing import Optional, List, Dict, Any
from contextlib import contextmanager
import pandas as pd

from core.config import get_settings
from core.logging import get_logger
from core.exceptions import DatabaseError

# Import existing database utilities
from utils.database import get_db_connection, execute_query

logger = get_logger(__name__)


class DatabaseManager:
    """Database connection and query manager"""
    
    def __init__(self):
        self.settings = get_settings()
        self._connection = None
    
    @contextmanager
    def get_connection(self):
        """Get database connection context manager"""
        try:
            conn = get_db_connection()
            yield conn
        except Exception as e:
            logger.error(f"Database connection error: {e}")
            raise DatabaseError(f"Failed to connect to database: {e}")
        finally:
            # Connection cleanup handled by utils.database
            pass
    
    def execute_query(
        self,
        query: str,
        params: Optional[Dict[str, Any]] = None,
        return_df: bool = True
    ) -> Optional[pd.DataFrame]:
        """
        Execute a database query
        
        Args:
            query: SQL query string
            params: Query parameters
            return_df: Whether to return DataFrame
        
        Returns:
            Query results as DataFrame or None
        """
        try:
            result = execute_query(query, params)
            if return_df and result is not None:
                return result
            return result
        except Exception as e:
            logger.error(f"Query execution error: {e}")
            raise DatabaseError(f"Query execution failed: {e}")
    
    def execute_many(
        self,
        query: str,
        params_list: List[Dict[str, Any]]
    ) -> None:
        """
        Execute query with multiple parameter sets
        
        Args:
            query: SQL query string
            params_list: List of parameter dictionaries
        """
        try:
            with self.get_connection() as conn:
                # Implementation depends on database type
                # This is a placeholder for batch operations
                for params in params_list:
                    self.execute_query(query, params, return_df=False)
        except Exception as e:
            logger.error(f"Batch execution error: {e}")
            raise DatabaseError(f"Batch execution failed: {e}")
    
    def health_check(self) -> bool:
        """Check database health"""
        try:
            result = self.execute_query("SELECT 1", return_df=False)
            return result is not None
        except Exception:
            return False


# Singleton instance
_db_manager: Optional[DatabaseManager] = None


def get_db_manager() -> DatabaseManager:
    """Get database manager instance (singleton)"""
    global _db_manager
    if _db_manager is None:
        _db_manager = DatabaseManager()
    return _db_manager


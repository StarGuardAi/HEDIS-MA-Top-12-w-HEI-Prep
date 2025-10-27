"""
Database Connection Management

Provides database connection pooling, session management, and health checks
for PostgreSQL database.

HIPAA Compliance:
- Connection strings sanitized (no credentials in logs)
- Connection pooling with timeout
- Health check for monitoring

Author: Robert Reichert
Date: October 2025
"""

import os
import logging
from typing import Generator
from contextlib import contextmanager

from sqlalchemy import create_engine, event, pool
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.exc import OperationalError, DisconnectionError

logger = logging.getLogger(__name__)

# Database URL from environment (never log this - contains credentials)
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://hedis_api:hedis_password@localhost:5432/hedis_portfolio"
)

# Create engine with connection pooling
engine = create_engine(
    DATABASE_URL,
    poolclass=pool.QueuePool,
    pool_size=5,  # Minimum connections
    max_overflow=15,  # Additional connections when needed (total max: 20)
    pool_timeout=30,  # Wait 30s for connection before timeout
    pool_recycle=3600,  # Recycle connections after 1 hour
    pool_pre_ping=True,  # Verify connection health before using
    echo=False,  # Set to True for SQL query logging (dev only)
)

# Session factory
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)


@event.listens_for(pool.Pool, "connect")
def receive_connect(dbapi_conn, connection_record):
    """
    Event listener for new database connections.
    Logs connection creation (PHI-safe).
    """
    logger.debug("New database connection established")


@event.listens_for(pool.Pool, "checkout")
def receive_checkout(dbapi_conn, connection_record, connection_proxy):
    """
    Event listener for connection checkout from pool.
    Monitors connection usage.
    """
    logger.debug("Connection checked out from pool")


def get_db() -> Generator[Session, None, None]:
    """
    FastAPI dependency for database session.
    
    Usage:
        @app.get("/endpoint")
        def endpoint(db: Session = Depends(get_db)):
            # Use db session
            pass
    
    Yields:
        Session: SQLAlchemy database session
        
    Notes:
        - Automatically closes session after request
        - Rolls back transaction on error
        - PHI-safe error logging
    """
    db = SessionLocal()
    try:
        yield db
    except Exception as e:
        logger.error(f"Database session error: {str(e)}")
        db.rollback()
        raise
    finally:
        db.close()


@contextmanager
def get_db_context():
    """
    Context manager for database session (for non-FastAPI use).
    
    Usage:
        with get_db_context() as db:
            # Use db session
            result = db.query(Model).all()
    
    Yields:
        Session: SQLAlchemy database session
    """
    db = SessionLocal()
    try:
        yield db
        db.commit()
    except Exception as e:
        logger.error(f"Database context error: {str(e)}")
        db.rollback()
        raise
    finally:
        db.close()


def check_database_health() -> dict:
    """
    Check database connection health.
    
    Returns:
        dict: Health status
            - status: "healthy" or "unhealthy"
            - message: Description
            - pool_size: Current pool size
            - overflow: Current overflow connections
    
    Notes:
        - Used by health check endpoints
        - PHI-safe (no data queried)
    """
    try:
        # Test connection
        with engine.connect() as conn:
            conn.execute("SELECT 1")
        
        # Get pool stats
        pool_status = engine.pool.status()
        
        return {
            "status": "healthy",
            "message": "Database connection successful",
            "pool_info": pool_status
        }
    
    except (OperationalError, DisconnectionError) as e:
        logger.error(f"Database health check failed: {str(e)}")
        return {
            "status": "unhealthy",
            "message": f"Database connection failed: {str(e)}",
            "pool_info": None
        }
    except Exception as e:
        logger.error(f"Unexpected database error: {str(e)}")
        return {
            "status": "unhealthy",
            "message": f"Unexpected error: {str(e)}",
            "pool_info": None
        }


def close_database_connections():
    """
    Close all database connections.
    
    Notes:
        - Called on application shutdown
        - Ensures clean connection closure
        - PHI-safe logging
    """
    logger.info("Closing all database connections...")
    engine.dispose()
    logger.info("Database connections closed")


def get_connection_info() -> dict:
    """
    Get sanitized connection information (for debugging).
    
    Returns:
        dict: Sanitized connection info
            - pool_size: Configured pool size
            - max_overflow: Max overflow connections
            - pool_timeout: Connection timeout
            - pool_recycle: Connection recycle time
    
    Notes:
        - Does NOT include credentials
        - PHI-safe
    """
    return {
        "pool_size": engine.pool.size(),
        "max_overflow": engine.pool._max_overflow,
        "pool_timeout": engine.pool._timeout,
        "pool_recycle": engine.pool._recycle,
        "current_checked_in": engine.pool.checkedin(),
        "current_checked_out": engine.pool.checkedout(),
        "current_overflow": engine.pool.overflow(),
    }



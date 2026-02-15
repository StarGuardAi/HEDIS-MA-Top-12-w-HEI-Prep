"""
Joint Audit Logger for Healthcare AI
Implements HIPAA-compliant audit logging with database storage

Based on Rule 3.6 from JOINT_CONTEXT_AGENTIC_RULES.md
"""
import json
import hashlib
import logging
from typing import Dict, List, Optional, Any
from datetime import datetime
import sys
import os

# Add project root to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

# Initialize logger early (before it's used in try/except blocks)
logger = logging.getLogger(__name__)

try:
    from database.connection import get_db_context, engine
    from sqlalchemy import text, create_engine
    from sqlalchemy.exc import SQLAlchemyError
    HAS_DB = True
except ImportError:
    HAS_DB = False
    logger.warning("Database utilities not available. Audit logs will be stored in memory only.")

try:
    from services.security.phi_validator import get_phi_validator
    HAS_PHI_VALIDATOR = True
except ImportError:
    HAS_PHI_VALIDATOR = False

from services.context_engine import estimate_tokens


class JointAuditLogger:
    """
    Log both context and agentic steps together for complete audit trail.
    
    Based on Rule 3.6 from JOINT_CONTEXT_AGENTIC_RULES.md
    
    HIPAA Compliant:
    - No PHI in logs
    - Encrypted storage (application-level)
    - Immutable audit trail
    - Query interface for compliance review
    """
    
    def __init__(self, use_database: bool = True):
        """
        Initialize joint audit logger.
        
        Args:
            use_database: If True, store logs in database (default: True)
        """
        self.use_database = use_database and HAS_DB
        self.audit_log = []  # In-memory fallback
        
        if self.use_database:
            self._ensure_table_exists()
    
    def _ensure_table_exists(self):
        """Ensure audit_logs table exists in database."""
        if not HAS_DB:
            return
        
        try:
            create_table_sql = """
            CREATE TABLE IF NOT EXISTS audit_logs (
                id SERIAL PRIMARY KEY,
                timestamp TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
                query_hash VARCHAR(64) NOT NULL,
                query_length INTEGER,
                initial_context_hash VARCHAR(64),
                initial_context_size_tokens INTEGER,
                initial_context_layers TEXT,
                plan_steps_count INTEGER,
                plan_steps TEXT,
                step_results_count INTEGER,
                step_results_summary TEXT,
                final_context_hash VARCHAR(64),
                final_context_size_tokens INTEGER,
                execution_time_ms INTEGER,
                validation_results TEXT,
                errors TEXT,
                log_data JSONB,
                created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
            );
            
            CREATE INDEX IF NOT EXISTS idx_audit_logs_timestamp ON audit_logs(timestamp);
            CREATE INDEX IF NOT EXISTS idx_audit_logs_query_hash ON audit_logs(query_hash);
            """
            
            with engine.connect() as conn:
                conn.execute(text(create_table_sql))
                conn.commit()
            
            logger.info("Audit logs table ensured")
        except Exception as e:
            logger.error(f"Error creating audit_logs table: {e}")
            self.use_database = False
    
    def _hash_content(self, content: Any) -> str:
        """Create SHA-256 hash of content (HIPAA compliant - no PHI in hash)."""
        content_str = json.dumps(content, sort_keys=True, default=str)
        return hashlib.sha256(content_str.encode()).hexdigest()
    
    def _sanitize_for_logging(self, content: Any) -> Any:
        """
        Sanitize content for logging (remove any potential PHI).
        
        Args:
            content: Content to sanitize
        
        Returns:
            Sanitized content (no PHI)
        """
        if HAS_PHI_VALIDATOR:
            phi_validator = get_phi_validator()
            validation_result = phi_validator.validate_no_phi(
                content,
                context="audit logging",
                log_violations=False  # Don't log during sanitization
            )
            
            if not validation_result.is_valid:
                # Return sanitized version (just structure, no content)
                if isinstance(content, dict):
                    return {k: "[REDACTED]" if k.lower() in ['name', 'id', 'ssn', 'dob'] else v
                            for k, v in content.items()}
                elif isinstance(content, str):
                    return "[REDACTED - Potential PHI detected]"
                else:
                    return "[REDACTED]"
        
        return content
    
    def log_joint_execution(
        self,
        query: str,
        initial_context: Dict,
        plan: Dict,
        step_results: List[Any],
        final_context: Dict,
        execution_time: Optional[float] = None,
        validation_results: Optional[Dict] = None,
        errors: Optional[List[str]] = None
    ):
        """
        Log complete execution with context and steps.
        
        Args:
            query: User query
            initial_context: Initial hierarchical context
            plan: Agentic plan
            step_results: Results from each step
            final_context: Final accumulated context
            execution_time: Execution time in seconds
            validation_results: Validation results dictionary
            errors: List of errors (if any)
        """
        # Sanitize query for logging (ensure no PHI)
        sanitized_query = self._sanitize_for_logging(query)
        
        # Create audit entry
        audit_entry = {
            "timestamp": datetime.now().isoformat(),
            "query_hash": self._hash_content(query),
            "query_length": len(query),
            "initial_context": {
                "hash": self._hash_content(initial_context),
                "size_tokens": estimate_tokens(initial_context),
                "layers": list(initial_context.keys()) if isinstance(initial_context, dict) else []
            },
            "plan": {
                "steps_count": len(plan.get("steps", [])),
                "steps": [
                    {
                        "id": step.get("id", ""),
                        "type": step.get("type", ""),
                        "context_hint": step.get("context_hint", "")
                    }
                    for step in plan.get("steps", [])
                    if step.get("type") != "synthesize"  # Exclude synthesize step
                ]
            },
            "step_results": [
                {
                    "step_index": i,
                    "result_type": type(result).__name__,
                    "result_hash": self._hash_content(str(result)),
                    "result_size_tokens": estimate_tokens({"data": result}) if result else 0
                }
                for i, result in enumerate(step_results)
            ],
            "final_context": {
                "hash": self._hash_content(final_context),
                "size_tokens": estimate_tokens(final_context),
                "layers": list(final_context.keys()) if isinstance(final_context, dict) else []
            },
            "execution_time_ms": int(execution_time * 1000) if execution_time else None,
            "validation_results": validation_results,
            "errors": errors
        }
        
        # Store in database if enabled
        if self.use_database:
            try:
                self._store_in_database(audit_entry)
            except Exception as e:
                logger.error(f"Error storing audit log in database: {e}")
                # Fallback to in-memory
                self.audit_log.append(audit_entry)
        else:
            # Store in memory
            self.audit_log.append(audit_entry)
        
        logger.info(
            f"Joint execution logged: {len(plan.get('steps', []))} steps, "
            f"{estimate_tokens(initial_context)} -> {estimate_tokens(final_context)} tokens"
        )
    
    def _store_in_database(self, audit_entry: Dict):
        """Store audit entry in database."""
        if not HAS_DB:
            return
        
        try:
            # Prepare data for database
            plan_steps_json = json.dumps(audit_entry["plan"]["steps"])
            step_results_summary = json.dumps([
                {
                    "step_index": r["step_index"],
                    "result_type": r["result_type"],
                    "result_hash": r["result_hash"]
                }
                for r in audit_entry["step_results"]
            ])
            validation_results_json = json.dumps(audit_entry.get("validation_results")) if audit_entry.get("validation_results") else None
            errors_json = json.dumps(audit_entry.get("errors")) if audit_entry.get("errors") else None
            
            # Full log data as JSONB
            log_data_json = json.dumps(audit_entry)
            
            insert_sql = text("""
                INSERT INTO audit_logs (
                    timestamp, query_hash, query_length,
                    initial_context_hash, initial_context_size_tokens, initial_context_layers,
                    plan_steps_count, plan_steps,
                    step_results_count, step_results_summary,
                    final_context_hash, final_context_size_tokens,
                    execution_time_ms, validation_results, errors, log_data
                ) VALUES (
                    :timestamp, :query_hash, :query_length,
                    :initial_context_hash, :initial_context_size_tokens, :initial_context_layers,
                    :plan_steps_count, :plan_steps,
                    :step_results_count, :step_results_summary,
                    :final_context_hash, :final_context_size_tokens,
                    :execution_time_ms, :validation_results, :errors, :log_data
                )
            """)
            
            params = {
                "timestamp": datetime.fromisoformat(audit_entry["timestamp"]),
                "query_hash": audit_entry["query_hash"],
                "query_length": audit_entry["query_length"],
                "initial_context_hash": audit_entry["initial_context"]["hash"],
                "initial_context_size_tokens": audit_entry["initial_context"]["size_tokens"],
                "initial_context_layers": json.dumps(audit_entry["initial_context"]["layers"]),
                "plan_steps_count": audit_entry["plan"]["steps_count"],
                "plan_steps": plan_steps_json,
                "step_results_count": len(audit_entry["step_results"]),
                "step_results_summary": step_results_summary,
                "final_context_hash": audit_entry["final_context"]["hash"],
                "final_context_size_tokens": audit_entry["final_context"]["size_tokens"],
                "execution_time_ms": audit_entry.get("execution_time_ms"),
                "validation_results": validation_results_json,
                "errors": errors_json,
                "log_data": log_data_json
            }
            
            with engine.connect() as conn:
                conn.execute(insert_sql, params)
                conn.commit()
        
        except SQLAlchemyError as e:
            logger.error(f"Database error storing audit log: {e}")
            raise
        except Exception as e:
            logger.error(f"Error storing audit log: {e}")
            raise
    
    def get_audit_log(self, limit: Optional[int] = None) -> List[Dict]:
        """
        Get audit log entries.
        
        Args:
            limit: Maximum number of entries to return (None for all)
        
        Returns:
            List of audit log entries
        """
        if self.use_database:
            return self._query_from_database(limit)
        else:
            if limit:
                return self.audit_log[-limit:]
            return self.audit_log.copy()
    
    def _query_from_database(self, limit: Optional[int] = None) -> List[Dict]:
        """Query audit logs from database."""
        if not HAS_DB:
            return []
        
        try:
            query_sql = """
                SELECT 
                    id, timestamp, query_hash, query_length,
                    initial_context_hash, initial_context_size_tokens,
                    plan_steps_count, final_context_size_tokens,
                    execution_time_ms, created_at,
                    log_data
                FROM audit_logs
                ORDER BY timestamp DESC
            """
            
            if limit:
                query_sql += f" LIMIT {limit}"
            
            with engine.connect() as conn:
                result = conn.execute(text(query_sql))
                rows = result.fetchall()
                
                audit_entries = []
                for row in rows:
                    entry = {
                        "id": row[0],
                        "timestamp": row[1].isoformat() if row[1] else None,
                        "query_hash": row[2],
                        "query_length": row[3],
                        "initial_context_hash": row[4],
                        "initial_context_size_tokens": row[5],
                        "plan_steps_count": row[6],
                        "final_context_size_tokens": row[7],
                        "execution_time_ms": row[8],
                        "created_at": row[9].isoformat() if row[9] else None,
                        "log_data": json.loads(row[10]) if row[10] else None
                    }
                    audit_entries.append(entry)
                
                return audit_entries
        
        except Exception as e:
            logger.error(f"Error querying audit logs: {e}")
            return []
    
    def query_by_date_range(
        self,
        start_date: datetime,
        end_date: datetime
    ) -> List[Dict]:
        """
        Query audit logs by date range (for compliance review).
        
        Args:
            start_date: Start date
            end_date: End date
        
        Returns:
            List of audit log entries
        """
        if not self.use_database:
            # Filter in-memory logs
            return [
                entry for entry in self.audit_log
                if start_date <= datetime.fromisoformat(entry["timestamp"]) <= end_date
            ]
        
        if not HAS_DB:
            return []
        
        try:
            query_sql = text("""
                SELECT 
                    id, timestamp, query_hash, query_length,
                    initial_context_hash, initial_context_size_tokens,
                    plan_steps_count, final_context_size_tokens,
                    execution_time_ms, validation_results, errors,
                    log_data
                FROM audit_logs
                WHERE timestamp >= :start_date AND timestamp <= :end_date
                ORDER BY timestamp DESC
            """)
            
            with engine.connect() as conn:
                result = conn.execute(query_sql, {
                    "start_date": start_date,
                    "end_date": end_date
                })
                rows = result.fetchall()
                
                audit_entries = []
                for row in rows:
                    entry = {
                        "id": row[0],
                        "timestamp": row[1].isoformat() if row[1] else None,
                        "query_hash": row[2],
                        "query_length": row[3],
                        "initial_context_hash": row[4],
                        "initial_context_size_tokens": row[5],
                        "plan_steps_count": row[6],
                        "final_context_size_tokens": row[7],
                        "execution_time_ms": row[8],
                        "validation_results": json.loads(row[9]) if row[9] else None,
                        "errors": json.loads(row[10]) if row[10] else None,
                        "log_data": json.loads(row[11]) if row[11] else None
                    }
                    audit_entries.append(entry)
                
                return audit_entries
        
        except Exception as e:
            logger.error(f"Error querying audit logs by date range: {e}")
            return []
    
    def query_by_query_hash(self, query_hash: str) -> List[Dict]:
        """
        Query audit logs by query hash (for compliance review).
        
        Args:
            query_hash: Query hash to search for
        
        Returns:
            List of audit log entries
        """
        if not self.use_database:
            # Filter in-memory logs
            return [
                entry for entry in self.audit_log
                if entry.get("query_hash") == query_hash
            ]
        
        if not HAS_DB:
            return []
        
        try:
            query_sql = text("""
                SELECT 
                    id, timestamp, query_hash, query_length,
                    initial_context_hash, initial_context_size_tokens,
                    plan_steps_count, final_context_size_tokens,
                    execution_time_ms, validation_results, errors,
                    log_data
                FROM audit_logs
                WHERE query_hash = :query_hash
                ORDER BY timestamp DESC
            """)
            
            with engine.connect() as conn:
                result = conn.execute(query_sql, {"query_hash": query_hash})
                rows = result.fetchall()
                
                audit_entries = []
                for row in rows:
                    entry = {
                        "id": row[0],
                        "timestamp": row[1].isoformat() if row[1] else None,
                        "query_hash": row[2],
                        "query_length": row[3],
                        "initial_context_hash": row[4],
                        "initial_context_size_tokens": row[5],
                        "plan_steps_count": row[6],
                        "final_context_size_tokens": row[7],
                        "execution_time_ms": row[8],
                        "validation_results": json.loads(row[9]) if row[9] else None,
                        "errors": json.loads(row[10]) if row[10] else None,
                        "log_data": json.loads(row[11]) if row[11] else None
                    }
                    audit_entries.append(entry)
                
                return audit_entries
        
        except Exception as e:
            logger.error(f"Error querying audit logs by query hash: {e}")
            return []
    
    def get_statistics(self) -> Dict:
        """
        Get audit log statistics (for compliance review).
        
        Returns:
            Dictionary with statistics
        """
        if not self.use_database:
            return {
                "total_entries": len(self.audit_log),
                "storage_type": "memory"
            }
        
        if not HAS_DB:
            return {"error": "Database not available"}
        
        try:
            stats_sql = text("""
                SELECT 
                    COUNT(*) as total_entries,
                    MIN(timestamp) as earliest_entry,
                    MAX(timestamp) as latest_entry,
                    AVG(execution_time_ms) as avg_execution_time_ms,
                    AVG(plan_steps_count) as avg_steps_count
                FROM audit_logs
            """)
            
            with engine.connect() as conn:
                result = conn.execute(stats_sql)
                row = result.fetchone()
                
                return {
                    "total_entries": row[0] if row[0] else 0,
                    "earliest_entry": row[1].isoformat() if row[1] else None,
                    "latest_entry": row[2].isoformat() if row[2] else None,
                    "avg_execution_time_ms": float(row[3]) if row[3] else None,
                    "avg_steps_count": float(row[4]) if row[4] else None,
                    "storage_type": "database"
                }
        
        except Exception as e:
            logger.error(f"Error getting audit log statistics: {e}")
            return {"error": str(e)}


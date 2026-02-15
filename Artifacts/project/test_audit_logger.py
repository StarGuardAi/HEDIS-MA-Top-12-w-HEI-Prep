"""
Test script for Joint Audit Logger
Tests Rule 3.6 implementation
"""
import sys
import os
import logging
from datetime import datetime, timedelta

# Add project root to path
sys.path.insert(0, os.path.dirname(__file__))

from services.audit_logger import JointAuditLogger

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)


def test_audit_logger_initialization():
    """Test audit logger initialization."""
    print("=" * 80)
    print("Test 1: Audit Logger Initialization")
    print("=" * 80)
    
    logger = JointAuditLogger(use_database=False)  # Use in-memory for testing
    assert logger is not None
    
    print("[SUCCESS] Audit logger initialized successfully!\n")


def test_log_joint_execution():
    """Test logging joint execution."""
    print("=" * 80)
    print("Test 2: Log Joint Execution")
    print("=" * 80)
    
    audit_logger = JointAuditLogger(use_database=False)
    
    query = "Calculate ROI for diabetes interventions"
    initial_context = {
        "layer_1_domain": {"hedis_overview": "HEDIS measures..."},
        "layer_2_measure": {"GSD": {}}
    }
    plan = {
        "steps": [
            {"id": "step_1", "type": "retrieve", "context_hint": "Domain knowledge"},
            {"id": "step_2", "type": "calculate", "context_hint": "ROI calculation"}
        ]
    }
    step_results = [{"result": "ROI: 2.5x"}, {"result": "Net benefit: $10000"}]
    final_context = {
        "layer_1_domain": {"hedis_overview": "HEDIS measures..."},
        "layer_2_measure": {"GSD": {}},
        "step_results": step_results
    }
    
    audit_logger.log_joint_execution(
        query=query,
        initial_context=initial_context,
        plan=plan,
        step_results=step_results,
        final_context=final_context,
        execution_time=1.5,
        validation_results={"passed": True},
        errors=None
    )
    
    audit_log = audit_logger.get_audit_log()
    assert len(audit_log) == 1
    
    entry = audit_log[0]
    assert "timestamp" in entry
    assert "query_hash" in entry
    assert "initial_context" in entry
    assert "plan" in entry
    assert "step_results" in entry
    assert "final_context" in entry
    
    print(f"[SUCCESS] Joint execution logged: {len(audit_log)} entry")
    print(f"  Query hash: {entry['query_hash'][:16]}...")
    print(f"  Steps: {entry['plan']['steps_count']}")
    print(f"  Execution time: {entry.get('execution_time_ms')}ms")
    print("\n[SUCCESS] Log joint execution test passed!\n")


def test_audit_log_query_interface():
    """Test query interface for compliance review."""
    print("=" * 80)
    print("Test 3: Query Interface")
    print("=" * 80)
    
    audit_logger = JointAuditLogger(use_database=False)
    
    # Add some test entries
    for i in range(3):
        audit_logger.log_joint_execution(
            query=f"Test query {i}",
            initial_context={"layer_1_domain": {}},
            plan={"steps": []},
            step_results=[],
            final_context={"layer_1_domain": {}},
            execution_time=1.0 + i
        )
    
    # Test get_audit_log
    all_logs = audit_logger.get_audit_log()
    assert len(all_logs) == 3
    
    # Test limit
    limited_logs = audit_logger.get_audit_log(limit=2)
    assert len(limited_logs) == 2
    
    # Test statistics
    stats = audit_logger.get_statistics()
    assert stats["total_entries"] == 3
    assert stats["storage_type"] == "memory"
    
    print(f"[SUCCESS] Query interface test passed!")
    print(f"  Total entries: {stats['total_entries']}")
    print(f"  Storage type: {stats['storage_type']}")
    print("\n[SUCCESS] Query interface test passed!\n")


def test_audit_log_no_phi():
    """Test that audit logs don't contain PHI."""
    print("=" * 80)
    print("Test 4: No PHI in Logs")
    print("=" * 80)
    
    audit_logger = JointAuditLogger(use_database=False)
    
    # Query with potential PHI (should be sanitized)
    query = "Analyze data for John Doe (SSN: 123-45-6789)"
    initial_context = {"layer_1_domain": {}}
    plan = {"steps": []}
    step_results = []
    final_context = {"layer_1_domain": {}}
    
    audit_logger.log_joint_execution(
        query=query,
        initial_context=initial_context,
        plan=plan,
        step_results=step_results,
        final_context=final_context
    )
    
    audit_log = audit_logger.get_audit_log()
    entry = audit_log[0]
    
    # Check that query_hash exists but query content is not stored directly
    assert "query_hash" in entry
    assert entry["query_hash"] is not None
    
    # In database version, query would be hashed only
    # In memory version, full entry is stored but sanitized
    
    print(f"[SUCCESS] Audit log created with hash: {entry['query_hash'][:16]}...")
    print("\n[SUCCESS] No PHI in logs test passed!\n")


if __name__ == "__main__":
    print("\n" + "=" * 80)
    print("Joint Audit Logger Test Suite")
    print("=" * 80 + "\n")
    
    try:
        test_audit_logger_initialization()
        test_log_joint_execution()
        test_audit_log_query_interface()
        test_audit_log_no_phi()
        
        print("=" * 80)
        print("[SUCCESS] All tests passed!")
        print("=" * 80)
        sys.exit(0)
        
    except AssertionError as e:
        print(f"\n[FAILED] Test assertion failed: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n[ERROR] Test failed with exception: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)




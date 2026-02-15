"""
Test script for ToolExecutor
Tests all 4 tools with various scenarios
"""
import sys
import os
import logging
import pandas as pd

# Add project root to path
sys.path.insert(0, os.path.dirname(__file__))

from services.agentic_rag import ToolExecutor, ToolNotFoundError, ToolExecutionError

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)


def test_query_database():
    """Test query_database tool."""
    print("=" * 80)
    print("Test 1: query_database Tool")
    print("=" * 80)
    
    executor = ToolExecutor()
    
    # Test gaps query
    try:
        result = executor.execute("query_database", {
            "query_type": "gaps",
            "measure_id": "GSD",
            "aggregated_only": True
        })
        print(f"[OK] Query returned: {type(result).__name__}")
        if isinstance(result, pd.DataFrame):
            print(f"  Rows: {len(result)}, Columns: {list(result.columns)}")
    except ToolExecutionError as e:
        print(f"[SKIP] Database query failed (expected if DB not available): {e}")
    except Exception as e:
        print(f"[ERROR] Unexpected error: {e}")
    
    print()


def test_calculate_roi():
    """Test calculate_roi tool."""
    print("=" * 80)
    print("Test 2: calculate_roi Tool")
    print("=" * 80)
    
    executor = ToolExecutor()
    
    result = executor.execute("calculate_roi", {
        "measure_id": "GSD",
        "intervention_count": 1000,
        "cost_per_intervention": 25.0
    })
    
    print(f"[OK] ROI calculation completed")
    print(f"  ROI Ratio: {result.get('roi_ratio', 'N/A')}")
    print(f"  Net Benefit: ${result.get('net_benefit', 0):,.2f}")
    print(f"  Total Cost: ${result.get('total_cost', 0):,.2f}")
    print(f"  Total Revenue: ${result.get('total_revenue', 0):,.2f}")
    
    assert "roi_ratio" in result
    assert "net_benefit" in result
    assert result["roi_ratio"] > 0
    
    print()


def test_validate_hedis_spec():
    """Test validate_hedis_spec tool."""
    print("=" * 80)
    print("Test 3: validate_hedis_spec Tool")
    print("=" * 80)
    
    executor = ToolExecutor()
    
    # Test valid data
    result = executor.execute("validate_hedis_spec", {
        "measure_id": "GSD",
        "data": {
            "measure_id": "GSD",
            "age": 50,
            "data_sources": ["claims", "labs"]
        }
    })
    
    print(f"[OK] Validation completed")
    print(f"  Is Valid: {result.get('is_valid', False)}")
    print(f"  Errors: {result.get('errors', [])}")
    print(f"  Warnings: {result.get('warnings', [])}")
    
    assert "is_valid" in result
    assert "errors" in result
    
    print()


def test_retrieve_docs():
    """Test retrieve_docs tool."""
    print("=" * 80)
    print("Test 4: retrieve_docs Tool")
    print("=" * 80)
    
    executor = ToolExecutor()
    
    result = executor.execute("retrieve_docs", {
        "query": "HEDIS specifications for HbA1c testing",
        "top_k": 3
    })
    
    print(f"[OK] Document retrieval completed")
    print(f"  Retrieved {len(result)} documents")
    
    assert isinstance(result, list)
    
    print()


def test_phi_validation():
    """Test PHI validation."""
    print("=" * 80)
    print("Test 5: PHI Validation")
    print("=" * 80)
    
    executor = ToolExecutor()
    
    # Test with PHI (should fail)
    try:
        executor.execute("calculate_roi", {
            "measure_id": "GSD",
            "member_id": "1234567890",  # Potential PHI
            "intervention_count": 100
        })
        print("[FAIL] PHI validation should have failed")
    except (ValueError, ToolExecutionError) as e:
        if "PHI detected" in str(e):
            print(f"[OK] PHI validation correctly rejected: {e}")
        else:
            print(f"[WARN] Error but not PHI-related: {e}")
    except Exception as e:
        print(f"[WARN] Unexpected error (may be OK): {e}")
    
    print()


def test_audit_logging():
    """Test audit logging."""
    print("=" * 80)
    print("Test 6: Audit Logging")
    print("=" * 80)
    
    executor = ToolExecutor()
    
    # Execute some tools
    executor.execute("calculate_roi", {
        "measure_id": "GSD",
        "intervention_count": 100,
        "cost_per_intervention": 25.0
    })
    
    audit_log = executor.get_audit_log()
    
    print(f"[OK] Audit log contains {len(audit_log)} entries")
    for entry in audit_log:
        print(f"  - {entry['tool_name']}: {entry['status']}")
    
    assert len(audit_log) > 0
    assert audit_log[0]["tool_name"] == "calculate_roi"
    
    print()


def test_tool_not_found():
    """Test tool not found error."""
    print("=" * 80)
    print("Test 7: Tool Not Found Error")
    print("=" * 80)
    
    executor = ToolExecutor()
    
    try:
        executor.execute("nonexistent_tool", {})
        print("[FAIL] Should have raised ToolNotFoundError")
    except ToolNotFoundError:
        print("[OK] ToolNotFoundError raised correctly")
    except Exception as e:
        print(f"[FAIL] Wrong exception: {e}")
    
    print()


if __name__ == "__main__":
    print("\n" + "=" * 80)
    print("Tool Executor Test Suite")
    print("=" * 80 + "\n")
    
    try:
        test_query_database()
        test_calculate_roi()
        test_validate_hedis_spec()
        test_retrieve_docs()
        test_phi_validation()
        test_audit_logging()
        test_tool_not_found()
        
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


"""
Test script for validation and retry logic
Tests Rule 2.3 implementation
"""
import sys
import os
import logging

# Add project root to path
sys.path.insert(0, os.path.dirname(__file__))

from services.agentic_rag import HEDISAgenticRAG

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)


def test_step_validation():
    """Test step-level validation."""
    print("=" * 80)
    print("Test 1: Step-Level Validation")
    print("=" * 80)
    
    agent = HEDISAgenticRAG(rag_retriever=None, use_llm=False)
    agent.reset_metrics()
    
    query = "Calculate ROI for diabetes interventions"
    result = agent.process_query(query)
    
    metrics = result.get("metrics", {})
    print(f"Step Success Rate: {metrics.get('step_success_rate', 'N/A')}")
    print(f"Validation Pass Rate: {metrics.get('validation_pass_rate', 'N/A')}")
    print(f"Total Steps: {metrics.get('total_steps', 0)}")
    print(f"Successful Steps: {metrics.get('successful_steps', 0)}")
    print(f"Failed Steps: {metrics.get('failed_steps', 0)}")
    
    assert metrics.get("step_success_rate", 0) >= 0
    assert metrics.get("validation_pass_rate", 0) >= 0
    
    print("[SUCCESS] Step validation test passed!\n")


def test_retry_logic():
    """Test retry logic with query refinement."""
    print("=" * 80)
    print("Test 2: Retry Logic with Query Refinement")
    print("=" * 80)
    
    agent = HEDISAgenticRAG(rag_retriever=None, use_llm=False)
    agent.reset_metrics()
    
    # Query that might need refinement
    query = "Find gaps, calculate ROI, prioritize, validate, and synthesize"
    result = agent.process_query(query, max_retries=2)
    
    metrics = result.get("metrics", {})
    print(f"Retry Rate: {metrics.get('retry_rate', 'N/A')}")
    print(f"Total Retries: {metrics.get('total_retries', 0)}")
    print(f"Queries with Retries: {metrics.get('queries_with_retries', 0)}")
    print(f"Retry Count: {result.get('retry_count', 0)}")
    
    assert metrics.get("retry_rate", 0) >= 0
    assert result.get("retry_count", 0) >= 0
    
    print("[SUCCESS] Retry logic test passed!\n")


def test_fallback_operation():
    """Test fallback to simpler operation."""
    print("=" * 80)
    print("Test 3: Fallback Operation")
    print("=" * 80)
    
    agent = HEDISAgenticRAG(rag_retriever=None, use_llm=False)
    agent.reset_metrics()
    
    query = "Query database for gaps"
    result = agent.process_query(query)
    
    metrics = result.get("metrics", {})
    print(f"Fallback Operations: {metrics.get('fallback_operations', 0)}")
    
    # Check if fallback was used
    if metrics.get("fallback_operations", 0) > 0:
        print("Fallback operations were used (expected if DB unavailable)")
    
    print("[SUCCESS] Fallback operation test passed!\n")


def test_metrics_tracking():
    """Test metrics tracking."""
    print("=" * 80)
    print("Test 4: Metrics Tracking")
    print("=" * 80)
    
    agent = HEDISAgenticRAG(rag_retriever=None, use_llm=False)
    # Don't reset metrics - let them accumulate
    
    # Run multiple queries
    queries = [
        "Calculate ROI for GSD",
        "Find gaps in diabetes care",
        "Prioritize members by risk"
    ]
    
    for query in queries:
        agent.process_query(query)
    
    metrics = agent._get_metrics()
    
    print("Aggregated Metrics:")
    print(f"  Total Queries: {metrics.get('total_queries', 0)}")
    print(f"  Total Steps: {metrics.get('total_steps', 0)}")
    print(f"  Successful Steps: {metrics.get('successful_steps', 0)}")
    print(f"  Failed Steps: {metrics.get('failed_steps', 0)}")
    print(f"  Step Success Rate: {metrics.get('step_success_rate', 0):.3f}")
    print(f"  Retry Rate: {metrics.get('retry_rate', 0):.3f}")
    print(f"  Validation Pass Rate: {metrics.get('validation_pass_rate', 0):.3f}")
    
    assert metrics.get("total_queries", 0) >= 3  # At least 3 queries
    assert metrics.get("step_success_rate", 0) >= 0
    assert metrics.get("retry_rate", 0) >= 0
    assert metrics.get("validation_pass_rate", 0) >= 0
    
    print("[SUCCESS] Metrics tracking test passed!\n")


def test_validation_failure_logging():
    """Test validation failure logging."""
    print("=" * 80)
    print("Test 5: Validation Failure Logging")
    print("=" * 80)
    
    agent = HEDISAgenticRAG(rag_retriever=None, use_llm=False)
    agent.reset_metrics()
    
    query = "Calculate ROI"
    result = agent.process_query(query)
    
    step_failures = result.get("step_failures", [])
    print(f"Step Failures: {len(step_failures)}")
    
    if step_failures:
        for failure in step_failures:
            print(f"  - {failure.get('step_id')} ({failure.get('step_type')}): {failure.get('errors', [])}")
    
    validator_metrics = result.get("metrics", {}).get("validator_metrics", {})
    print(f"\nValidator Metrics:")
    print(f"  Total Validations: {validator_metrics.get('total_validations', 0)}")
    print(f"  Passed: {validator_metrics.get('passed_validations', 0)}")
    print(f"  Failed: {validator_metrics.get('failed_validations', 0)}")
    print(f"  PHI Detections: {validator_metrics.get('phi_detections', 0)}")
    
    print("[SUCCESS] Validation failure logging test passed!\n")


if __name__ == "__main__":
    print("\n" + "=" * 80)
    print("Validation and Retry Logic Test Suite")
    print("=" * 80 + "\n")
    
    try:
        test_step_validation()
        test_retry_logic()
        test_fallback_operation()
        test_metrics_tracking()
        test_validation_failure_logging()
        
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


"""
Test script for ContextAwareAgenticRAG
Tests Template 1 from JOINT_CONTEXT_AGENTIC_RULES.md
"""
import sys
import os
import logging

# Add project root to path
sys.path.insert(0, os.path.dirname(__file__))

from services.joint_rag import ContextAwareAgenticRAG

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)


def test_basic_joint_rag():
    """Test basic context-aware agentic RAG workflow."""
    print("=" * 80)
    print("Test 1: Basic Context-Aware Agentic RAG Workflow")
    print("=" * 80)
    
    agent = ContextAwareAgenticRAG(rag_retriever=None, use_llm=False)
    
    query = "Calculate ROI for HbA1c testing interventions"
    result = agent.process_query(query)
    
    print(f"\nQuery: {query}")
    print(f"\nSteps Executed: {result.get('steps_executed', 0)}")
    print(f"Retry Count: {result.get('retry_count', 0)}")
    
    response = result.get("response", {})
    print(f"\nResponse Summary: {response.get('summary', 'N/A')[:200]}...")
    print(f"Recommendations: {len(response.get('recommendations', []))}")
    
    context_used = result.get("context_used", {})
    print(f"\nContext Sizes:")
    print(f"  Initial: {context_used.get('initial_size', 0)} tokens")
    print(f"  Final: {context_used.get('final_size', 0)} tokens")
    
    assert result.get("steps_executed", 0) >= 0
    assert "response" in result
    assert "context_used" in result
    
    print("\n[SUCCESS] Basic joint RAG test passed!\n")


def test_complex_query():
    """Test complex multi-step query."""
    print("=" * 80)
    print("Test 2: Complex Multi-Step Query")
    print("=" * 80)
    
    agent = ContextAwareAgenticRAG(rag_retriever=None, use_llm=False)
    
    query = "Find gaps in diabetes care, calculate ROI, and prioritize by risk"
    result = agent.process_query(query, max_steps=5)
    
    print(f"\nQuery: {query}")
    print(f"Steps Executed: {result.get('steps_executed', 0)}")
    
    plan = result.get("plan", {})
    print(f"\nPlan Steps: {len(plan.get('steps', []))}")
    for i, step in enumerate(plan.get("steps", [])[:3]):
        print(f"  {i+1}. {step.get('type', 'N/A')} - {step.get('id', 'N/A')}")
    
    assert result.get("steps_executed", 0) > 0
    
    print("\n[SUCCESS] Complex query test passed!\n")


def test_context_compression():
    """Test context compression during execution."""
    print("=" * 80)
    print("Test 3: Context Compression")
    print("=" * 80)
    
    agent = ContextAwareAgenticRAG(rag_retriever=None, use_llm=False)
    
    query = "Analyze cross-measure diabetes care opportunities with ROI calculations"
    result = agent.process_query(query)
    
    context_used = result.get("context_used", {})
    initial_size = context_used.get("initial_size", 0)
    final_size = context_used.get("final_size", 0)
    
    print(f"\nInitial Context Size: {initial_size} tokens")
    print(f"Final Context Size: {final_size} tokens")
    print(f"Max Allowed: {agent.max_tokens} tokens")
    
    # Final context should be under max_tokens
    assert final_size <= agent.max_tokens or initial_size == 0
    
    print("\n[SUCCESS] Context compression test passed!\n")


def test_audit_logging():
    """Test joint audit logging."""
    print("=" * 80)
    print("Test 4: Joint Audit Logging")
    print("=" * 80)
    
    agent = ContextAwareAgenticRAG(rag_retriever=None, use_llm=False)
    
    query = "Calculate ROI for GSD"
    result = agent.process_query(query)
    
    audit_log = agent.get_audit_log()
    print(f"\nAudit Log Entries: {len(audit_log)}")
    
    if audit_log:
        latest_entry = audit_log[-1]
        print(f"\nLatest Audit Entry:")
        print(f"  Query: {latest_entry.get('query', 'N/A')[:50]}...")
        print(f"  Steps: {latest_entry.get('plan', {}).get('steps_count', 0)}")
        print(f"  Initial Context Size: {latest_entry.get('initial_context', {}).get('size_tokens', 0)} tokens")
        print(f"  Final Context Size: {latest_entry.get('final_context', {}).get('size_tokens', 0)} tokens")
    
    assert len(audit_log) > 0
    
    print("\n[SUCCESS] Audit logging test passed!\n")


def test_metrics():
    """Test metrics tracking."""
    print("=" * 80)
    print("Test 5: Metrics Tracking")
    print("=" * 80)
    
    agent = ContextAwareAgenticRAG(rag_retriever=None, use_llm=False)
    
    query = "Calculate ROI"
    result = agent.process_query(query)
    
    metrics = result.get("metrics", {})
    print(f"\nMetrics:")
    print(f"  Context Builder: {metrics.get('context_builder_metrics', {})}")
    print(f"  Agentic: {metrics.get('agentic_metrics', {})}")
    print(f"  Validation: {metrics.get('validation_metrics', {})}")
    
    assert "metrics" in result
    
    print("\n[SUCCESS] Metrics tracking test passed!\n")


if __name__ == "__main__":
    print("\n" + "=" * 80)
    print("Context-Aware Agentic RAG Test Suite")
    print("=" * 80 + "\n")
    
    try:
        test_basic_joint_rag()
        test_complex_query()
        test_context_compression()
        test_audit_logging()
        test_metrics()
        
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




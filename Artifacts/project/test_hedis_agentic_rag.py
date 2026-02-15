"""
Test script for HEDISAgenticRAG
Tests full agentic RAG workflow
"""
import sys
import os
import logging
import json

# Add project root to path
sys.path.insert(0, os.path.dirname(__file__))

from services.agentic_rag import HEDISAgenticRAG

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)


def test_full_workflow():
    """Test full agentic RAG workflow."""
    print("=" * 80)
    print("Test: Full Agentic RAG Workflow")
    print("=" * 80)
    
    # Create agentic RAG agent
    agent = HEDISAgenticRAG(rag_retriever=None, use_llm=False)
    
    # Test query
    query = "Find gaps in HbA1c testing, calculate ROI, prioritize by risk"
    
    print(f"Query: {query}")
    print()
    
    try:
        result = agent.process_query(query)
        
        print("Result:")
        print(f"  Steps Executed: {result.get('steps_executed', 0)}")
        print(f"  Retry Count: {result.get('retry_count', 0)}")
        print()
        
        response = result.get("response", {})
        print("Response:")
        print(f"  Summary: {response.get('summary', 'N/A')[:200]}...")
        print(f"  Recommendations: {len(response.get('recommendations', []))}")
        for i, rec in enumerate(response.get('recommendations', [])[:3], 1):
            print(f"    {i}. {rec}")
        print(f"  Metrics: {list(response.get('metrics', {}).keys())}")
        print()
        
        context = result.get("context_used", {})
        print("Context Used:")
        print(f"  Retrieved Docs: {len(context.get('retrieved_docs', []))}")
        print(f"  Query Results: {len(context.get('query_results', []))}")
        print(f"  Calculations: {len(context.get('calculations', []))}")
        print(f"  Validations: {len(context.get('validations', []))}")
        print()
        
        assert result.get("steps_executed", 0) > 0
        assert "response" in result
        assert "summary" in result["response"]
        
        print("[SUCCESS] Full workflow test passed!\n")
        return True
        
    except Exception as e:
        print(f"[ERROR] Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_max_steps_limit():
    """Test max steps limit."""
    print("=" * 80)
    print("Test: Max Steps Limit")
    print("=" * 80)
    
    agent = HEDISAgenticRAG(rag_retriever=None, use_llm=False)
    agent.max_steps = 3  # Set low limit for testing
    
    query = "Find gaps, calculate ROI, prioritize, validate, and synthesize"
    
    try:
        result = agent.process_query(query)
        steps_executed = result.get("steps_executed", 0)
        
        print(f"Steps executed: {steps_executed}")
        print(f"Max steps limit: {agent.max_steps}")
        
        # Should not exceed max_steps (excluding synthesize)
        assert steps_executed <= agent.max_steps
        
        print("[SUCCESS] Max steps limit test passed!\n")
        return True
        
    except Exception as e:
        print(f"[ERROR] Test failed: {e}")
        return False


def test_validation_and_retry():
    """Test validation and retry logic."""
    print("=" * 80)
    print("Test: Validation and Retry")
    print("=" * 80)
    
    agent = HEDISAgenticRAG(rag_retriever=None, use_llm=False)
    
    query = "Calculate ROI for diabetes interventions"
    
    try:
        result = agent.process_query(query, max_retries=2)
        
        print(f"Retry count: {result.get('retry_count', 0)}")
        print(f"Validation warning: {result.get('validation_warning', 'None')}")
        
        assert "response" in result
        assert result.get("retry_count", 0) >= 0
        
        print("[SUCCESS] Validation and retry test passed!\n")
        return True
        
    except Exception as e:
        print(f"[ERROR] Test failed: {e}")
        return False


if __name__ == "__main__":
    print("\n" + "=" * 80)
    print("HEDISAgenticRAG Test Suite")
    print("=" * 80 + "\n")
    
    try:
        success1 = test_full_workflow()
        success2 = test_max_steps_limit()
        success3 = test_validation_and_retry()
        
        if success1 and success2 and success3:
            print("=" * 80)
            print("[SUCCESS] All tests passed!")
            print("=" * 80)
            sys.exit(0)
        else:
            print("=" * 80)
            print("[FAILED] Some tests failed")
            print("=" * 80)
            sys.exit(1)
        
    except Exception as e:
        print(f"\n[ERROR] Test suite failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)




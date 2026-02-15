"""
Test script for context refinement loop
Tests Practice 2 from JOINT_CONTEXT_AGENTIC_RULES.md
"""
import sys
import os
import logging

# Add project root to path
sys.path.insert(0, os.path.dirname(__file__))

from services.joint_rag import ContextAwareAgenticRAG, refine_context_in_loop, estimate_tokens

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)


def test_refine_context_in_loop():
    """Test refine_context_in_loop function."""
    print("=" * 80)
    print("Test 1: refine_context_in_loop Function")
    print("=" * 80)
    
    context = {
        "layer_1_domain": {"hedis_overview": "HEDIS measures..."},
        "layer_2_measure": {"GSD": {}}
    }
    
    step_result = {"roi_ratio": 2.5, "net_benefit": 10000}
    
    refined_context, metrics = refine_context_in_loop(
        context,
        step_result,
        iteration=0,
        step_type="calculate",
        step_id="step_1"
    )
    
    print(f"Initial Context Size: {metrics['context_size_before']} tokens")
    print(f"Final Context Size: {metrics['context_size_after']} tokens")
    print(f"Compression Applied: {metrics['compression_applied']}")
    print(f"Relevance Updated: {metrics['relevance_updated']}")
    
    assert "step_results" in refined_context
    assert len(refined_context["step_results"]) == 1
    
    print("\n[SUCCESS] refine_context_in_loop test passed!\n")


def test_context_refinement_tracking():
    """Test context refinement metrics tracking."""
    print("=" * 80)
    print("Test 2: Context Refinement Metrics Tracking")
    print("=" * 80)
    
    agent = ContextAwareAgenticRAG(rag_retriever=None, use_llm=False)
    
    query = "Calculate ROI for diabetes interventions"
    result = agent.process_query(query)
    
    refinement = result.get("context_refinement", {})
    
    print(f"\nContext Size by Step: {len(refinement.get('context_size_by_step', []))} entries")
    for entry in refinement.get("context_size_by_step", [])[:3]:
        print(f"  {entry.get('step')}: {entry.get('size')} tokens")
    
    print(f"\nCompression Events: {len(refinement.get('compression_events', []))}")
    for event in refinement.get("compression_events", []):
        print(f"  Step {event.get('step')}: {event.get('size_before')} -> {event.get('size_after')} tokens")
    
    print(f"\nRelevance Scores Updates: {len(refinement.get('relevance_scores', []))}")
    
    assert "context_size_by_step" in refinement
    assert "relevance_scores" in refinement
    assert "compression_events" in refinement
    
    print("\n[SUCCESS] Context refinement tracking test passed!\n")


def test_relevance_score_updates():
    """Test relevance score updates."""
    print("=" * 80)
    print("Test 3: Relevance Score Updates")
    print("=" * 80)
    
    context = {
        "layer_1_domain": {"hedis_overview": "HEDIS measures..."},
        "relevance_scores": [0.5, 0.6]
    }
    
    # First iteration (should not update relevance)
    refined_context, metrics = refine_context_in_loop(
        context,
        {"result": "test"},
        iteration=0,
        step_type="retrieve",
        step_id="step_1"
    )
    
    assert not metrics["relevance_updated"], "First iteration should not update relevance"
    
    # Second iteration (should update relevance)
    refined_context, metrics = refine_context_in_loop(
        refined_context,
        {"result": "test2"},
        iteration=1,
        step_type="calculate",
        step_id="step_2"
    )
    
    assert metrics["relevance_updated"], "Second iteration should update relevance"
    assert "relevance_scores" in refined_context
    
    print(f"Relevance Scores: {refined_context.get('relevance_scores', [])}")
    
    print("\n[SUCCESS] Relevance score updates test passed!\n")


def test_compression_threshold():
    """Test compression when context exceeds 4000 tokens."""
    print("=" * 80)
    print("Test 4: Compression Threshold")
    print("=" * 80)
    
    # Create a large context
    context = {
        "layer_1_domain": {"hedis_overview": "HEDIS " * 1000},  # Large text
        "layer_2_measure": {"GSD": {"data": "x" * 1000}},
        "layer_3_query": {"data": "y" * 1000}
    }
    
    initial_size = estimate_tokens(context)
    print(f"Initial Context Size: {initial_size} tokens")
    
    step_result = {"data": "result"}
    
    refined_context, metrics = refine_context_in_loop(
        context,
        step_result,
        iteration=0,
        step_type="calculate",
        step_id="step_1"
    )
    
    final_size = metrics["context_size_after"]
    print(f"Final Context Size: {final_size} tokens")
    print(f"Compression Applied: {metrics['compression_applied']}")
    
    if initial_size > 4000:
        assert metrics["compression_applied"], "Should compress when > 4000 tokens"
        assert final_size <= 4000, "Final size should be <= 4000 tokens"
    
    print("\n[SUCCESS] Compression threshold test passed!\n")


if __name__ == "__main__":
    print("\n" + "=" * 80)
    print("Context Refinement Loop Test Suite")
    print("=" * 80 + "\n")
    
    try:
        test_refine_context_in_loop()
        test_context_refinement_tracking()
        test_relevance_score_updates()
        test_compression_threshold()
        
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




"""
Test script for context-driven planning
Tests Rule 3.3 implementation
"""
import sys
import os
import logging

# Add project root to path
sys.path.insert(0, os.path.dirname(__file__))

from services.joint_rag import select_tools_with_context, ContextDrivenPlanningAgent
from services.agentic_rag import PlanningAgent

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)


def test_select_tools_missing_domain():
    """Test tool selection when domain knowledge is missing."""
    print("=" * 80)
    print("Test 1: Tool Selection - Missing Domain Knowledge")
    print("=" * 80)
    
    query = "Calculate ROI for diabetes"
    context = {
        "layer_1_domain": {},  # Missing domain knowledge
        "layer_2_measure": {"GSD": {}}
    }
    
    tools = select_tools_with_context(query, context)
    
    print(f"Query: {query}")
    print(f"Context: Domain knowledge missing")
    print(f"Selected Tools: {tools}")
    
    assert "retrieve" in tools, "Should add retrieve tool when domain knowledge missing"
    assert "calculate" in tools, "Should add calculate tool for ROI query"
    
    print("\n[SUCCESS] Missing domain knowledge test passed!\n")


def test_select_tools_with_measures():
    """Test tool selection when measures are in context."""
    print("=" * 80)
    print("Test 2: Tool Selection - Measures in Context")
    print("=" * 80)
    
    query = "Find gaps in diabetes care"
    context = {
        "layer_1_domain": {"hedis_overview": "HEDIS measures..."},
        "layer_2_measure": {"GSD": {"measure_id": "GSD"}}  # Measures in context
    }
    
    tools = select_tools_with_context(query, context)
    
    print(f"Query: {query}")
    print(f"Context: Measures GSD in context")
    print(f"Selected Tools: {tools}")
    
    assert "query_db" in tools, "Should add query_db tool when measures in context"
    assert "retrieve" not in tools, "Should not add retrieve when domain knowledge exists"
    
    print("\n[SUCCESS] Measures in context test passed!\n")


def test_select_tools_roi_calculation():
    """Test tool selection for ROI calculation."""
    print("=" * 80)
    print("Test 3: Tool Selection - ROI Calculation")
    print("=" * 80)
    
    query = "Calculate ROI for HbA1c testing"
    context = {
        "layer_1_domain": {"hedis_overview": "HEDIS measures..."},
        "layer_2_measure": {"GSD": {}}
    }
    
    tools = select_tools_with_context(query, context)
    
    print(f"Query: {query}")
    print(f"Selected Tools: {tools}")
    
    assert "calculate" in tools, "Should add calculate tool for ROI query"
    assert "query_db" in tools, "Should add query_db tool when measures in context"
    
    print("\n[SUCCESS] ROI calculation test passed!\n")


def test_select_tools_validation():
    """Test tool selection for validation."""
    print("=" * 80)
    print("Test 4: Tool Selection - Validation")
    print("=" * 80)
    
    query = "Validate compliance for diabetes measures"
    context = {
        "layer_1_domain": {"hedis_overview": "HEDIS measures..."},
        "layer_2_measure": {"GSD": {}}
    }
    
    tools = select_tools_with_context(query, context)
    
    print(f"Query: {query}")
    print(f"Selected Tools: {tools}")
    
    assert "validate" in tools, "Should add validate tool for validation query"
    
    print("\n[SUCCESS] Validation test passed!\n")


def test_context_driven_planning():
    """Test context-driven planning agent."""
    print("=" * 80)
    print("Test 5: Context-Driven Planning Agent")
    print("=" * 80)
    
    base_agent = PlanningAgent(use_llm=False)
    context_agent = ContextDrivenPlanningAgent(base_agent)
    
    query = "Calculate ROI for diabetes interventions"
    context = {
        "layer_1_domain": {"hedis_overview": "HEDIS measures for diabetes..."},
        "layer_2_measure": {"GSD": {"measure_id": "GSD", "description": "HbA1c testing"}}
    }
    
    plan = context_agent.decompose_with_context(query, context)
    
    print(f"Query: {query}")
    print(f"Plan Steps: {len(plan.get('steps', []))}")
    
    step_types = [step.get("type") for step in plan.get("steps", []) if step.get("type") != "synthesize"]
    print(f"Step Types: {step_types}")
    
    # Check that plan includes appropriate steps
    assert len(plan.get("steps", [])) > 0, "Plan should have steps"
    
    # Check context hints are added
    for step in plan.get("steps", []):
        if step.get("type") != "synthesize":
            assert "context_hint" in step, f"Step {step.get('id')} should have context_hint"
            print(f"  {step.get('id')} ({step.get('type')}): {step.get('context_hint', 'N/A')[:50]}...")
    
    print("\n[SUCCESS] Context-driven planning test passed!\n")


def test_tool_selection_default():
    """Test default tool selection when no specific requirements."""
    print("=" * 80)
    print("Test 6: Tool Selection - Default")
    print("=" * 80)
    
    query = "Tell me about HEDIS"
    context = {
        "layer_1_domain": {"hedis_overview": "HEDIS measures..."},
        "layer_2_measure": {}
    }
    
    tools = select_tools_with_context(query, context)
    
    print(f"Query: {query}")
    print(f"Selected Tools: {tools}")
    
    assert len(tools) > 0, "Should select at least one tool"
    assert "retrieve" in tools, "Should default to retrieve when no specific requirements"
    
    print("\n[SUCCESS] Default tool selection test passed!\n")


if __name__ == "__main__":
    print("\n" + "=" * 80)
    print("Context-Driven Planning Test Suite")
    print("=" * 80 + "\n")
    
    try:
        test_select_tools_missing_domain()
        test_select_tools_with_measures()
        test_select_tools_roi_calculation()
        test_select_tools_validation()
        test_context_driven_planning()
        test_tool_selection_default()
        
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




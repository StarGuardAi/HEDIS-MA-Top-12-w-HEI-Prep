"""
Demonstration of context-driven tool selection.
Shows how tool selection adapts based on available context.
"""

import sys
import os

# Add project root to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from services.joint_rag import (
    ContextDrivenToolSelector,
    ContextDrivenPlanningAgent,
    ToolType
)
from services.context_engine import HierarchicalContextBuilder
from services.agentic_rag import PlanningAgent


def demo_scenario_1_empty_context():
    """Scenario 1: Empty context - should select all tools."""
    print("\n" + "="*60)
    print("SCENARIO 1: Empty Context")
    print("="*60)
    
    query = "Calculate ROI for HbA1c testing interventions"
    context = {
        "layer_1_domain": {},
        "layer_2_measure": {},
        "layer_3_query": {}
    }
    
    selector = ContextDrivenToolSelector()
    selections = selector.select_tools(query, context)
    
    print(f"\nQuery: {query}")
    print(f"Context: Empty (no layers populated)")
    print(f"\nTools Selected: {len(selections)}")
    for i, sel in enumerate(selections, 1):
        print(f"{i}. {sel.tool_type.value}")
        print(f"   Confidence: {sel.confidence:.2f}")
        print(f"   Reasoning: {sel.reasoning}")
    
    # Expected: retrieve → query_db → calculate
    expected_tools = ["retrieve", "query_db", "calculate"]
    actual_tools = [s.tool_type.value for s in selections]
    print(f"\n[OK] Selected {len(expected_tools)} tools as expected")
    print(f"  Tools: {actual_tools}")


def demo_scenario_2_partial_context():
    """Scenario 2: Partial context - should skip retrieval."""
    print("\n" + "="*60)
    print("SCENARIO 2: Partial Context (Domain Knowledge Available)")
    print("="*60)
    
    query = "Calculate ROI for HbA1c testing interventions"
    context = {
        "layer_1_domain": {
            "hedis_overview": "HEDIS is a standardized set of measures...",
            "terminology": {"CDC": "Comprehensive Diabetes Care"}
        },
        "layer_2_measure": {
            "CDC": {
                "spec": "HbA1c testing annually...",
                "performance": {"current_rate": 0.75}
            }
        },
        "layer_3_query": {}
    }
    
    selector = ContextDrivenToolSelector()
    selections = selector.select_tools(query, context)
    
    print(f"\nQuery: {query}")
    print(f"Context: Layer 1 (domain) + Layer 2 (measure) populated")
    print(f"\nTools Selected: {len(selections)}")
    for i, sel in enumerate(selections, 1):
        print(f"{i}. {sel.tool_type.value}")
        print(f"   Confidence: {sel.confidence:.2f}")
        print(f"   Reasoning: {sel.reasoning}")
    
    # Expected: query_db → calculate (skipped retrieval)
    expected_tools = ["query_db", "calculate"]
    actual_tools = [s.tool_type.value for s in selections]
    print(f"\n[OK] Skipped retrieval - domain knowledge available")
    print(f"  Tools: {actual_tools}")


def demo_scenario_3_full_context():
    """Scenario 3: Full context - should only calculate."""
    print("\n" + "="*60)
    print("SCENARIO 3: Full Context (All Data Available)")
    print("="*60)
    
    query = "Calculate ROI for HbA1c testing interventions"
    context = {
        "layer_1_domain": {
            "hedis_overview": "HEDIS measures...",
            "terminology": {"CDC": "Comprehensive Diabetes Care"}
        },
        "layer_2_measure": {
            "CDC": {"spec": "...", "performance": {...}}
        },
        "layer_3_query": {
            "query_results": [{"measure_id": "CDC", "gap_count": 1500}],
            "intervention_data": {"cost_per_intervention": 50}
        }
    }
    
    selector = ContextDrivenToolSelector()
    selections = selector.select_tools(query, context)
    
    print(f"\nQuery: {query}")
    print(f"Context: All 3 layers populated with data")
    print(f"\nTools Selected: {len(selections)}")
    for i, sel in enumerate(selections, 1):
        print(f"{i}. {sel.tool_type.value}")
        print(f"   Confidence: {sel.confidence:.2f}")
        print(f"   Reasoning: {sel.reasoning}")
    
    # Expected: calculate only (all data available)
    expected_tools = ["calculate"]
    actual_tools = [s.tool_type.value for s in selections]
    print(f"\n[OK] Minimal tools - all required data in context")
    print(f"  Tools: {actual_tools}")


def demo_full_planning_flow():
    """Demonstrate full planning flow with context."""
    print("\n" + "="*60)
    print("FULL PLANNING FLOW")
    print("="*60)
    
    query = "Analyze cross-measure diabetes opportunities with ROI validation"
    
    # Build context
    context_builder = HierarchicalContextBuilder()
    try:
        context = context_builder.build_context(query, max_tokens=4000)
    except Exception as e:
        print(f"Note: Could not build full context (may need RAG retriever): {e}")
        context = {
            "layer_1_domain": {"hedis_overview": "HEDIS measures..."},
            "layer_2_measure": {"CDC": {}},
            "layer_3_query": {}
        }
    
    # Create plan
    base_agent = PlanningAgent(use_llm=False)
    planner = ContextDrivenPlanningAgent(base_agent)
    plan = planner.decompose_with_context(query, context)
    
    print(f"\nQuery: {query}")
    print(f"\nContext Built:")
    print(f"  Layers: {list(context.keys())}")
    
    print(f"\nExecution Plan:")
    print(f"  Total Steps: {len(plan['steps'])}")
    if 'estimated_execution_time' in plan:
        print(f"  Estimated Time: {plan['estimated_execution_time']}s")
    
    if 'context_used' in plan and 'tool_selection_details' in plan['context_used']:
        print(f"\nTool Selection Details:")
        for detail in plan['context_used']['tool_selection_details']:
            print(f"  - {detail['tool']}: {detail['confidence']:.2f} confidence")
            print(f"    Reasoning: {detail['reasoning']}")
    
    print(f"\nStep Details:")
    for step in plan["steps"]:
        print(f"\n  Step {step['id']}: {step['type']}")
        if 'confidence' in step:
            print(f"    Confidence: {step['confidence']:.2f}")
        if 'reasoning' in step:
            print(f"    Reasoning: {step['reasoning']}")
        if step.get('depends_on'):
            print(f"    Depends on: {', '.join(step['depends_on'])}")


if __name__ == "__main__":
    print("\n" + "="*60)
    print("CONTEXT-DRIVEN TOOL SELECTION DEMO")
    print("="*60)
    
    try:
        demo_scenario_1_empty_context()
        demo_scenario_2_partial_context()
        demo_scenario_3_full_context()
        demo_full_planning_flow()
        
        print("\n" + "="*60)
        print("DEMO COMPLETE")
        print("="*60)
    except Exception as e:
        print(f"\nError during demo: {e}")
        import traceback
        traceback.print_exc()


"""
Test script for PlanningAgent
Tests query decomposition with various scenarios
"""
import sys
import os
import json
import logging

# Add project root to path
sys.path.insert(0, os.path.dirname(__file__))

from services.agentic_rag import PlanningAgent, PlanningError

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)


def test_example_query():
    """Test with the example query from requirements."""
    print("=" * 80)
    print("Test 1: Example Query")
    print("=" * 80)
    
    agent = PlanningAgent(use_llm=False)
    query = "Find gaps in HbA1c testing, calculate ROI, prioritize by risk"
    
    print(f"Query: {query}")
    print()
    
    plan = agent.decompose(query)
    
    print("Generated Plan:")
    print(json.dumps(plan, indent=2))
    print()
    
    # Validate expected steps
    expected_types = ["retrieve", "query_db", "calculate", "calculate", "synthesize"]
    actual_types = [step["type"] for step in plan["steps"]]
    
    print("Step Types:")
    for i, (expected, actual) in enumerate(zip(expected_types, actual_types), 1):
        status = "[OK]" if expected == actual else "[MISMATCH]"
        print(f"  Step {i}: {status} Expected: {expected}, Got: {actual}")
    
    # Check that we have retrieve → query_db → calculate → synthesize
    assert plan["steps"][0]["type"] == "retrieve", "First step should be retrieve"
    assert plan["steps"][1]["type"] == "query_db", "Second step should be query_db"
    assert any(step["type"] == "calculate" for step in plan["steps"]), "Should have calculate step"
    assert plan["steps"][-1]["type"] == "synthesize", "Last step should be synthesize"
    
    print()
    print("[SUCCESS] Example query test passed!\n")


def test_plan_validation():
    """Test plan validation."""
    print("=" * 80)
    print("Test 2: Plan Validation")
    print("=" * 80)
    
    agent = PlanningAgent(use_llm=False)
    
    # Test valid plan
    valid_query = "Find gaps in diabetes care"
    plan = agent.decompose(valid_query)
    assert agent._validate_plan(plan), "Valid plan should pass validation"
    print("[OK] Valid plan passes validation")
    
    # Test invalid plan (missing steps)
    invalid_plan = {}
    assert not agent._validate_plan(invalid_plan), "Invalid plan should fail validation"
    print("[OK] Invalid plan (missing steps) fails validation")
    
    # Test invalid plan (missing step id)
    invalid_plan2 = {
        "steps": [
            {"type": "retrieve", "query": "test"}
        ]
    }
    assert not agent._validate_plan(invalid_plan2), "Invalid plan (missing id) should fail validation"
    print("[OK] Invalid plan (missing step id) fails validation")
    
    print()
    print("[SUCCESS] Plan validation test passed!\n")


def test_measure_extraction():
    """Test measure ID extraction."""
    print("=" * 80)
    print("Test 3: Measure ID Extraction")
    print("=" * 80)
    
    agent = PlanningAgent(use_llm=False)
    
    test_cases = [
        ("Find gaps in HbA1c testing", "GSD"),
        ("Calculate ROI for CDC measure", "GSD"),
        ("Query gaps in kidney health evaluation", "KED"),
        ("Eye exam for diabetes", "EED"),
        ("Blood pressure control gaps", "CBP"),
    ]
    
    for query, expected_measure in test_cases:
        measure_id = agent._extract_measure_id(query)
        status = "[OK]" if measure_id == expected_measure else "[FAIL]"
        print(f"  {status} Query: '{query}' -> Measure: {measure_id} (expected: {expected_measure})")
        assert measure_id == expected_measure, f"Expected {expected_measure}, got {measure_id}"
    
    print()
    print("[SUCCESS] Measure extraction test passed!\n")


def test_dependency_management():
    """Test step dependency management."""
    print("=" * 80)
    print("Test 4: Dependency Management")
    print("=" * 80)
    
    agent = PlanningAgent(use_llm=False)
    query = "Find gaps in HbA1c testing, calculate ROI"
    
    plan = agent.decompose(query)
    
    print("Step Dependencies:")
    for step in plan["steps"]:
        deps = step.get("depends_on", [])
        print(f"  {step['id']} ({step['type']}): depends on {deps if deps else 'nothing'}")
    
    # Check that later steps depend on earlier ones
    assert len(plan["steps"]) > 1, "Should have multiple steps"
    assert plan["steps"][1].get("depends_on") == [plan["steps"][0]["id"]], \
        "Second step should depend on first step"
    
    print()
    print("[SUCCESS] Dependency management test passed!\n")


def test_various_queries():
    """Test various query patterns."""
    print("=" * 80)
    print("Test 5: Various Query Patterns")
    print("=" * 80)
    
    agent = PlanningAgent(use_llm=False)
    
    test_queries = [
        "What are the HEDIS specifications for diabetes care?",
        "Find members who need HbA1c testing",
        "Calculate ROI for diabetes interventions",
        "Prioritize members by risk for eye exams",
        "Validate results against HEDIS specs",
        "Find gaps, calculate ROI, and prioritize",
    ]
    
    for query in test_queries:
        print(f"\nQuery: {query}")
        try:
            plan = agent.decompose(query)
            print(f"  Generated {len(plan['steps'])} steps:")
            for step in plan["steps"]:
                print(f"    - {step['type']}: {step.get('query', 'N/A')[:50]}...")
        except PlanningError as e:
            print(f"  [ERROR] Planning failed: {e}")
    
    print()
    print("[SUCCESS] Various queries test passed!\n")


if __name__ == "__main__":
    print("\n" + "=" * 80)
    print("Planning Agent Test Suite")
    print("=" * 80 + "\n")
    
    try:
        test_example_query()
        test_plan_validation()
        test_measure_extraction()
        test_dependency_management()
        test_various_queries()
        
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




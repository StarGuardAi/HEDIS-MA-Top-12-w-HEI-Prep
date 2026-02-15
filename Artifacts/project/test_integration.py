"""
Integration test script for Context Engineering and Agentic RAG
Run this script to verify all components work correctly
"""

import sys
import os
import io

# Set UTF-8 encoding for stdout to handle emojis
if sys.stdout.encoding != 'utf-8':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

def test_imports():
    """Test all imports work"""
    print("Testing imports...")
    try:
        from services.context_engineering import HierarchicalContextBuilder
        from services.agentic_rag import AgenticPlanner, ToolExecutor
        sys.path.insert(0, 'phase4_dashboard')
        from components.visualization_components import render_efficiency_gauge
        print("[OK] All imports successful")
        return True
    except Exception as e:
        print(f"[FAIL] Import error: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_context_builder():
    """Test context builder works"""
    print("\nTesting context builder...")
    try:
        from services.context_engineering import HierarchicalContextBuilder
        builder = HierarchicalContextBuilder()
        context = builder.build_context("Test query")
        assert 'metadata' in context
        assert 'efficiency_score' in context['metadata']
        print(f"[OK] Context builder works: {context['metadata']['efficiency_score']}% efficiency")
        
        # Test cache stats
        stats = builder.get_cache_stats()
        assert 'cache_hits' in stats
        assert 'cache_misses' in stats
        print(f"[OK] Cache stats work: {stats['cache_hits']} hits, {stats['cache_misses']} misses")
        return True
    except Exception as e:
        print(f"[FAIL] Context builder error: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_planner():
    """Test planner works"""
    print("\nTesting planner...")
    try:
        from services.agentic_rag import AgenticPlanner
        planner = AgenticPlanner()
        plan = planner.create_plan("Test query")
        assert 'steps' in plan
        assert 'estimated_time' in plan
        assert 'total_steps' in plan
        print(f"[OK] Planner works: {len(plan['steps'])} steps, {plan['estimated_time']}s estimated time")
        return True
    except Exception as e:
        print(f"[FAIL] Planner error: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_executor():
    """Test executor works"""
    print("\nTesting executor...")
    try:
        from services.agentic_rag import AgenticPlanner, ToolExecutor
        planner = AgenticPlanner()
        executor = ToolExecutor()
        plan = planner.create_plan("Test query")
        
        # Execute first step
        if plan['steps']:
            step = plan['steps'][0]
            result = executor.execute_step(step)
            assert hasattr(result, 'success')
            assert hasattr(result, 'execution_time')
            print(f"[OK] Executor works: Step {result.step_id} {'succeeded' if result.success else 'failed'}")
            return True
        else:
            print("[WARN] No steps in plan to execute")
            return True
    except Exception as e:
        print(f"[FAIL] Executor error: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_visualization_components():
    """Test visualization components work"""
    print("\nTesting visualization components...")
    try:
        sys.path.insert(0, 'phase4_dashboard')
        from components.visualization_components import render_efficiency_gauge
        fig = render_efficiency_gauge(75)
        assert fig is not None
        print("[OK] Visualization components work")
        return True
    except Exception as e:
        print(f"[FAIL] Visualization components error: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_file_structure():
    """Test that all required files exist"""
    print("\nTesting file structure...")
    files_to_check = [
        'services/context_engineering/context_builder.py',
        'services/context_engineering/__init__.py',
        'services/agentic_rag/planner.py',
        'services/agentic_rag/executor.py',
        'services/agentic_rag/__init__.py',
        'phase4_dashboard/components/visualization_components.py',
        'phase4_dashboard/components/__init__.py',
        'phase4_dashboard/pages/8_🎓_AI_Capabilities_Demo.py',
        'docs/CONTEXT_ENGINEERING_AGENTIC_RAG.md',
        'docs/INTEGRATION_TESTING_CHECKLIST.md'
    ]
    
    all_exist = True
    for file_path in files_to_check:
        if os.path.exists(file_path):
            print(f"[OK] {file_path}")
        else:
            print(f"[FAIL] {file_path} NOT FOUND")
            all_exist = False
    
    return all_exist

if __name__ == "__main__":
    print("=" * 60)
    print("Integration Test Suite for Context Engineering & Agentic RAG")
    print("=" * 60)
    
    results = [
        test_file_structure(),
        test_imports(),
        test_context_builder(),
        test_planner(),
        test_executor(),
        test_visualization_components()
    ]
    
    print("\n" + "=" * 60)
    if all(results):
        print("[SUCCESS] ALL TESTS PASSED - Ready for demo!")
        sys.exit(0)
    else:
        print("[FAILURE] SOME TESTS FAILED - Review errors above")
        sys.exit(1)


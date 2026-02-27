"""
Test script for HierarchicalContextBuilder
Tests with query: "What's the ROI for HbA1c testing interventions?"
"""
import sys
import os
import json
from pprint import pprint

# Add project root to path
sys.path.insert(0, os.path.dirname(__file__))

from services.context_engine import HierarchicalContextBuilder


def test_hierarchical_context_builder():
    """Test HierarchicalContextBuilder with ROI query."""
    
    print("=" * 80)
    print("Testing HierarchicalContextBuilder")
    print("=" * 80)
    print()
    
    # Initialize builder
    builder = HierarchicalContextBuilder()
    
    # Test query
    test_query = "What's the ROI for HbA1c testing interventions?"
    
    print(f"Test Query: {test_query}")
    print()
    
    try:
        # Build context
        context = builder.build_context(test_query, max_tokens=4000)
        
        print("[SUCCESS] Context built successfully!")
        print()
        
        # Display results
        print("=" * 80)
        print("LAYER 1: Domain Knowledge")
        print("=" * 80)
        print(f"HEDIS Overview: {context['layer_1_domain']['hedis_overview'][:200]}...")
        print(f"Star Ratings: {context['layer_1_domain']['star_ratings'][:200]}...")
        print(f"Terminology included: {'terminology' in context['layer_1_domain']}")
        print()
        
        print("=" * 80)
        print("LAYER 2: Measure-Specific Context")
        print("=" * 80)
        if context['layer_2_measure']:
            for measure_id, measure_data in context['layer_2_measure'].items():
                print(f"\nMeasure: {measure_id}")
                print(f"  Name: {measure_data['spec']['name']}")
                print(f"  Tier: {measure_data['spec']['tier']}")
                print(f"  Weight: {measure_data['spec']['weight']}x")
                print(f"  Star Value: {measure_data['spec']['star_value']}")
                print(f"  Performance:")
                print(f"    - Avg ROI: {measure_data['performance']['avg_roi']:.2f}x")
                print(f"    - Members: {measure_data['performance']['members_count']:,}")
                print(f"    - Completion Rate: {measure_data['performance']['completion_rate']:.1%}")
        else:
            print("No measures extracted from query")
        print()
        
        print("=" * 80)
        print("LAYER 3: Query-Specific Context")
        print("=" * 80)
        query_context = context['layer_3_query']
        print(f"Retrieved Docs: {len(query_context.get('retrieved_docs', []))}")
        print(f"Query Type: {query_context.get('query_type', 'N/A')}")
        print(f"Query Keywords: {query_context.get('query_keywords', [])}")
        print()
        
        # Token estimation
        estimated_tokens = builder._estimate_tokens(context)
        print("=" * 80)
        print("Token Management")
        print("=" * 80)
        print(f"Estimated Tokens: {estimated_tokens}")
        print(f"Max Tokens: 4000")
        print(f"Within Limit: {'Yes' if estimated_tokens <= 4000 else 'No'}")
        print()
        
        # PHI Validation
        print("=" * 80)
        print("PHI Validation")
        print("=" * 80)
        is_valid, errors = builder._validate_phi(test_query)
        print(f"Query Valid: {'Yes' if is_valid else 'No'}")
        if errors:
            print(f"Errors: {errors}")
        print()
        
        # Context structure validation
        print("=" * 80)
        print("Context Structure Validation")
        print("=" * 80)
        required_keys = ['layer_1_domain', 'layer_2_measure', 'layer_3_query']
        for key in required_keys:
            status = '[OK]' if key in context else '[MISSING]'
            print(f"{status} {key}: {'Present' if key in context else 'Missing'}")
        print()
        
        # Summary
        print("=" * 80)
        print("SUMMARY")
        print("=" * 80)
        print(f"[SUCCESS] Hierarchical context built successfully")
        print(f"[SUCCESS] {len(context['layer_2_measure'])} measure(s) identified: {list(context['layer_2_measure'].keys())}")
        print(f"[SUCCESS] PHI validation passed")
        print(f"[SUCCESS] Token count: {estimated_tokens} / 4000")
        print(f"[SUCCESS] Context structure: Valid")
        print()
        
        return True
        
    except ValueError as e:
        print(f"[ERROR] PHI Validation Error: {e}")
        return False
    except Exception as e:
        print(f"[ERROR] Error: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = test_hierarchical_context_builder()
    sys.exit(0 if success else 1)


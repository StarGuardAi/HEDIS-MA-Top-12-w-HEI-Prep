"""
Test script for context compression functionality
Tests Template 4 compression with various scenarios
"""
import sys
import os
import logging

# Add project root to path
sys.path.insert(0, os.path.dirname(__file__))

from services.context_engine import compress_context, estimate_tokens, summarize_document

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)


def test_document_summarization():
    """Test document summarization function."""
    print("=" * 80)
    print("Test 1: Document Summarization")
    print("=" * 80)
    
    long_content = (
        "This is a very long document about HEDIS measures and healthcare quality. "
        "HEDIS measures are used to assess healthcare quality across multiple domains. "
        "The measures include diabetes care, cardiovascular health, and cancer screening. "
        "Each measure has specific requirements and impacts CMS Star Ratings. "
        "Star Ratings directly affect Medicare Advantage plan revenue. "
        "Triple-weighted measures have 3x impact on star ratings."
    )
    
    print(f"Original length: {len(long_content)} chars")
    summarized = summarize_document(long_content, max_length=200)
    print(f"Summarized length: {len(summarized)} chars")
    print(f"Summarized content: {summarized}")
    print()
    
    assert len(summarized) <= 203  # 200 + "..."
    print("[SUCCESS] Document summarization works correctly\n")


def test_relevance_filtering():
    """Test relevance score filtering."""
    print("=" * 80)
    print("Test 2: Relevance Score Filtering")
    print("=" * 80)
    
    context = {
        "retrieved_docs": [
            {"content": "High relevance document", "score": 0.8, "metadata": {}},
            {"content": "Medium relevance document", "score": 0.6, "metadata": {}},
            {"content": "Low relevance document", "score": 0.3, "metadata": {}},
            {"content": "Very low relevance document", "score": 0.2, "metadata": {}},
        ],
        "relevance_scores": [0.8, 0.6, 0.3, 0.2]
    }
    
    print(f"Original docs: {len(context['retrieved_docs'])}")
    print(f"Relevance scores: {context['relevance_scores']}")
    
    compressed = compress_context(context, target_tokens=1000)
    
    print(f"Compressed docs: {len(compressed['retrieved_docs'])}")
    print(f"Filtered scores: {compressed['relevance_scores']}")
    
    # Should only keep docs with score >= 0.5
    assert all(score >= 0.5 for score in compressed['relevance_scores'])
    assert len(compressed['retrieved_docs']) == 2  # Only 0.8 and 0.6
    print("[SUCCESS] Relevance filtering works correctly\n")


def test_token_compression():
    """Test token-based compression."""
    print("=" * 80)
    print("Test 3: Token Compression")
    print("=" * 80)
    
    # Create a large context
    large_context = {
        "retrieved_docs": [
            {
                "content": "A" * 500,  # 500 chars = ~125 tokens
                "score": 0.7,
                "metadata": {}
            },
            {
                "content": "B" * 500,
                "score": 0.6,
                "metadata": {}
            },
            {
                "content": "C" * 500,
                "score": 0.8,
                "metadata": {}
            }
        ],
        "relevance_scores": [0.7, 0.6, 0.8],
        "layer_1_domain": {
            "hedis_overview": "X" * 2000,  # 2000 chars = ~500 tokens
            "star_ratings": "Y" * 2000
        }
    }
    
    original_tokens = estimate_tokens(large_context)
    print(f"Original tokens: {original_tokens}")
    
    compressed = compress_context(large_context, target_tokens=3000)
    final_tokens = estimate_tokens(compressed)
    
    print(f"Final tokens: {final_tokens}")
    print(f"Compression ratio: {(1 - final_tokens/original_tokens)*100:.1f}%")
    
    if "_compression_metrics" in compressed:
        metrics = compressed["_compression_metrics"]
        print(f"\nCompression Metrics:")
        print(f"  Docs before: {metrics['docs_before']}")
        print(f"  Docs after: {metrics['docs_after']}")
        print(f"  Docs removed: {metrics['docs_removed']}")
        print(f"  Docs summarized: {metrics['docs_summarized']}")
        print(f"  Tokens removed: {metrics['tokens_removed']}")
    
    # Check that documents were summarized
    for doc in compressed.get("retrieved_docs", []):
        if "compressed" in doc:
            assert len(doc["content"]) <= 203  # 200 + "..."
    
    print("[SUCCESS] Token compression works correctly\n")


def test_hierarchical_context_compression():
    """Test compression with hierarchical context structure."""
    print("=" * 80)
    print("Test 4: Hierarchical Context Compression")
    print("=" * 80)
    
    hierarchical_context = {
        "layer_1_domain": {
            "hedis_overview": "HEDIS measures healthcare quality..." * 50,
            "star_ratings": "CMS Star Ratings impact revenue..." * 50,
            "terminology": "HEDIS: Healthcare Effectiveness..."
        },
        "layer_2_measure": {
            "GSD": {
                "spec": {"name": "Glycemic Status Assessment", "tier": 1},
                "performance": {"avg_roi": 1.35}
            }
        },
        "layer_3_query": {
            "retrieved_docs": [
                {"content": "Document about GSD" * 20, "score": 0.7, "metadata": {}},
                {"content": "Document about ROI" * 20, "score": 0.4, "metadata": {}},  # Should be filtered
                {"content": "Document about Star Ratings" * 20, "score": 0.8, "metadata": {}}
            ],
            "relevance_scores": [0.7, 0.4, 0.8]
        }
    }
    
    original_tokens = estimate_tokens(hierarchical_context)
    print(f"Original tokens: {original_tokens}")
    
    compressed = compress_context(hierarchical_context, target_tokens=3000)
    final_tokens = estimate_tokens(compressed)
    
    print(f"Final tokens: {final_tokens}")
    
    # Check that low-relevance doc was removed
    query_layer = compressed.get("layer_3_query", {})
    assert len(query_layer.get("retrieved_docs", [])) == 2  # Only 0.7 and 0.8
    assert all(score >= 0.5 for score in query_layer.get("relevance_scores", []))
    
    print("[SUCCESS] Hierarchical context compression works correctly\n")


def test_compression_metrics():
    """Test compression metrics logging."""
    print("=" * 80)
    print("Test 5: Compression Metrics")
    print("=" * 80)
    
    context = {
        "retrieved_docs": [
            {"content": "Doc 1" * 100, "score": 0.8, "metadata": {}},
            {"content": "Doc 2" * 100, "score": 0.3, "metadata": {}},  # Below threshold
            {"content": "Doc 3" * 100, "score": 0.6, "metadata": {}}
        ],
        "relevance_scores": [0.8, 0.3, 0.6]
    }
    
    compressed = compress_context(context, target_tokens=1000)
    
    assert "_compression_metrics" in compressed
    metrics = compressed["_compression_metrics"]
    
    print("Compression Metrics:")
    for key, value in metrics.items():
        print(f"  {key}: {value}")
    
    assert metrics["docs_before"] == 3
    assert metrics["docs_after"] == 2  # One removed (score < 0.5)
    assert metrics["docs_removed"] == 1
    assert metrics["relevance_threshold"] == 0.5
    
    print("[SUCCESS] Compression metrics logged correctly\n")


if __name__ == "__main__":
    print("\n" + "=" * 80)
    print("Context Compression Test Suite")
    print("=" * 80 + "\n")
    
    try:
        test_document_summarization()
        test_relevance_filtering()
        test_token_compression()
        test_hierarchical_context_compression()
        test_compression_metrics()
        
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




"""
Hierarchical Context Builder for Healthcare AI Chatbot
Implements HIPAA-compliant context engineering with 3-layer hierarchy

Based on Template 1 from CONTEXT_ENGINEERING_RULES.md
"""
import re
import logging
from typing import Dict, List, Optional, Tuple
from datetime import datetime
import sys
import os
import numpy as np

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

try:
    from utils.hedis_specs import (
        MEASURE_REGISTRY,
        get_measure_spec,
        TIER_1_DIABETES,
        TIER_2_CARDIOVASCULAR,
        TIER_3_CANCER
    )
except ImportError:
    # Fallback if imports fail
    MEASURE_REGISTRY = {}
    get_measure_spec = lambda x: None
    TIER_1_DIABETES = []
    TIER_2_CARDIOVASCULAR = []
    TIER_3_CANCER = []

logger = logging.getLogger(__name__)

# TERMINOLOGY_CONTEXT from Rule 1.4
TERMINOLOGY_CONTEXT = """
HEDIS: Healthcare Effectiveness Data and Information Set
PHI: Protected Health Information
Star Rating: CMS quality rating (1-5 stars)
Gap-in-Care: Member missing required preventive service
ROI: Return on Investment (revenue impact / intervention cost)
CDC: Comprehensive Diabetes Care (legacy measure name, now GSD/KED/EED)
GSD: Glycemic Status Assessment for Patients with Diabetes
KED: Kidney Health Evaluation for Patients with Diabetes (NEW 2025)
EED: Eye Exam for Patients with Diabetes
HbA1c: Hemoglobin A1c test for diabetes monitoring
"""

# Temporal context
TEMPORAL_CONTEXT = f"""
Current Date: {datetime.now().strftime('%Y-%m-%d')}
Measurement Year: 2025
Lookback Period: 365 days
Intervention Window: Next 30 days
"""

# Compliance context
COMPLIANCE_CONTEXT = """
HIPAA: De-identification required for all PHI
CMS: Star Rating methodology (2025)
HEDIS MY2025: Current specification version
HEI: Health Equity Index (2027 requirement)
"""


class HierarchicalContextBuilder:
    """
    Build hierarchical context for healthcare AI queries.
    
    Implements 3-layer hierarchy:
    1. Domain knowledge (HEDIS specs, terminology)
    2. Measure-specific context (CDC/EED/GSD)
    3. Query-specific context (retrieved dynamically)
    """
    
    def __init__(self, rag_retriever=None):
        """
        Initialize the hierarchical context builder.
        
        Args:
            rag_retriever: Optional RAG retriever for query-specific context
        """
        self.rag_retriever = rag_retriever
        
        # Measure name mappings for query extraction
        self.measure_keywords = {
            'cdc': ['cdc', 'comprehensive diabetes care', 'diabetes care'],
            'gsd': ['gsd', 'glycemic', 'hba1c', 'a1c', 'hemoglobin a1c'],
            'ked': ['ked', 'kidney', 'egfr', 'acr', 'kidney health'],
            'eed': ['eed', 'eye exam', 'retinal', 'diabetic retinopathy'],
            'cbp': ['cbp', 'blood pressure', 'hypertension', 'bp control'],
            'bcs': ['bcs', 'breast cancer', 'mammography'],
            'col': ['col', 'colorectal', 'colonoscopy', 'colon cancer']
        }
    
    def build_context(self, query: str, max_tokens: int = 4000) -> Dict:
        """
        Build hierarchical context with token management.
        
        Args:
            query: User query string
            max_tokens: Maximum token limit (default: 4000)
        
        Returns:
            Dictionary with layer_1_domain, layer_2_measure, layer_3_query
        
        Raises:
            ValueError: If PHI is detected in query
        """
        # PHI validation before context assembly (Rule 1.1)
        if HAS_PHI_VALIDATOR:
            phi_validator = get_phi_validator()
            validation_result = phi_validator.validate_before_context_assembly(
                {"query": query},
                log_violations=True
            )
            if not validation_result.is_valid:
                raise ValueError(f"PHI detected in query. Violation types: {validation_result.violation_types}")
        else:
            # Fallback validation
            is_valid, phi_errors = self._validate_phi(query)
            if not is_valid:
                raise ValueError(f"PHI detected in query. Errors: {phi_errors}")
        
        # Build hierarchical context
        context = {
            "layer_1_domain": self._get_domain_knowledge(),
            "layer_2_measure": self._get_measure_context(query),
            "layer_3_query": self._get_query_specific_context(query)
        }
        
        # Validate context before returning (Rule 1.1)
        if HAS_PHI_VALIDATOR:
            phi_validator = get_phi_validator()
            validation_result = phi_validator.validate_before_context_assembly(
                context,
                log_violations=True
            )
            if not validation_result.is_valid:
                raise ValueError(f"PHI detected in assembled context. Violation types: {validation_result.violation_types}")
        
        # Compress if needed
        estimated_tokens = estimate_tokens(context)
        if estimated_tokens > max_tokens:
            logger.warning(
                f"Context exceeds token limit ({estimated_tokens} > {max_tokens}). "
                "Compressing context..."
            )
            context = self._compress_context(context, max_tokens)
        
        logger.info(
            f"Built hierarchical context: {estimated_tokens} tokens, "
            f"{len(context['layer_2_measure'])} measures, "
            f"{len(context['layer_3_query'].get('retrieved_docs', []))} retrieved docs"
        )
        
        return context
    
    def _get_domain_knowledge(self) -> Dict:
        """
        Layer 1: Core domain knowledge (HEDIS specs, terminology).
        
        Returns:
            Dictionary with domain knowledge including TERMINOLOGY_CONTEXT
        """
        return {
            "hedis_overview": (
                "HEDIS (Healthcare Effectiveness Data and Information Set) measures "
                "healthcare quality across multiple domains including diabetes care, "
                "cardiovascular health, and cancer screening. HEDIS measures impact "
                "CMS Star Ratings, which directly affect Medicare Advantage plan revenue."
            ),
            "star_ratings": (
                "CMS Star Ratings (1-5 stars) impact Medicare Advantage plan revenue. "
                "Each star point improvement can generate $45K-$60K per 1,000 members annually. "
                "Triple-weighted measures (GSD, KED, CBP) have 3x impact on star ratings."
            ),
            "terminology": TERMINOLOGY_CONTEXT,
            "temporal": TEMPORAL_CONTEXT,
            "compliance": COMPLIANCE_CONTEXT
        }
    
    def _get_measure_context(self, query: str) -> Dict:
        """
        Layer 2: Measure-specific context (CDC/EED/GSD).
        
        Extracts relevant measures from query and includes their specifications.
        
        Args:
            query: User query string
        
        Returns:
            Dictionary mapping measure IDs to their specs and performance data
        """
        measures = self._extract_measures_from_query(query)
        measure_context = {}
        
        for measure_id in measures:
            spec = get_measure_spec(measure_id)
            if spec:
                measure_context[measure_id] = {
                    "spec": {
                        "code": spec.code,
                        "name": spec.name,
                        "tier": spec.tier,
                        "weight": spec.weight,
                        "target_population": spec.target_population,
                        "data_sources": spec.data_sources,
                        "hedis_spec_version": spec.hedis_spec_version,
                        "star_value": spec.star_value,
                        "age_range": f"{spec.age_min}-{spec.age_max}" if spec.age_min and spec.age_max else None
                    },
                    "performance": self._get_aggregate_stats(measure_id)
                }
            else:
                logger.warning(f"Measure spec not found for: {measure_id}")
        
        return measure_context
    
    def _get_query_specific_context(self, query: str) -> Dict:
        """
        Layer 3: Query-specific retrieved context.
        
        Uses RAG to retrieve relevant documents if available.
        
        Args:
            query: User query string
        
        Returns:
            Dictionary with retrieved documents and relevance scores
        """
        if self.rag_retriever:
            try:
                retrieved = self.rag_retriever.retrieve(query, top_k=5)
                return {
                    "retrieved_docs": [
                        {
                            "content": doc.get("content", str(doc)),
                            "score": doc.get("score", 0.0),
                            "metadata": doc.get("metadata", {})
                        }
                        for doc in retrieved
                    ],
                    "relevance_scores": [
                        doc.get("score", 0.0) for doc in retrieved
                    ]
                }
            except Exception as e:
                logger.warning(f"RAG retrieval failed: {e}")
                return {"retrieved_docs": [], "relevance_scores": []}
        else:
            # Fallback: return query-specific keywords and context
            return {
                "retrieved_docs": [],
                "relevance_scores": [],
                "query_keywords": self._extract_keywords(query),
                "query_type": self._classify_query_type(query)
            }
    
    def _extract_measures_from_query(self, query: str) -> List[str]:
        """
        Extract measure IDs from query text.
        
        Args:
            query: User query string
        
        Returns:
            List of measure IDs (e.g., ['GSD', 'CDC'])
        """
        query_lower = query.lower()
        measures = []
        
        # Check for measure keywords
        for measure_id, keywords in self.measure_keywords.items():
            if any(keyword in query_lower for keyword in keywords):
                # Map to actual measure codes
                measure_code = self._map_keyword_to_measure_code(measure_id)
                if measure_code and measure_code not in measures:
                    measures.append(measure_code)
        
        # Special handling for CDC (legacy name, maps to GSD/KED/EED)
        if 'cdc' in query_lower or 'comprehensive diabetes care' in query_lower:
            # Add all diabetes measures
            for measure in TIER_1_DIABETES:
                if measure not in measures:
                    measures.append(measure)
        
        # If no measures found, check for ROI queries (likely about diabetes measures)
        if not measures and ('roi' in query_lower or 'return on investment' in query_lower):
            if 'hba1c' in query_lower or 'a1c' in query_lower:
                measures.append('GSD')
            elif 'diabetes' in query_lower:
                measures.extend(['GSD', 'KED', 'EED'])
        
        return measures
    
    def _map_keyword_to_measure_code(self, keyword: str) -> Optional[str]:
        """Map keyword to measure code."""
        mapping = {
            'cdc': 'GSD',  # CDC is legacy, map to GSD
            'gsd': 'GSD',
            'ked': 'KED',
            'eed': 'EED',
            'cbp': 'CBP',
            'bcs': 'BCS',
            'col': 'COL'
        }
        return mapping.get(keyword.lower())
    
    def _get_aggregate_stats(self, measure_id: str) -> Dict:
        """
        Get aggregate performance statistics for a measure.
        
        Args:
            measure_id: Measure code (e.g., 'GSD')
        
        Returns:
            Dictionary with aggregate stats (no PHI)
        """
        # Placeholder for aggregate stats - in production, query database
        # This should return aggregated data only, no member-level PHI
        return {
            "avg_roi": 1.35,  # Example ROI ratio
            "members_count": 1500,  # Aggregate count
            "completion_rate": 0.75,  # Example completion rate
            "star_impact": "$360-615K" if measure_id in ['GSD', 'KED', 'CBP'] else "$120-205K"
        }
    
    def _extract_keywords(self, query: str) -> List[str]:
        """Extract important keywords from query."""
        # Simple keyword extraction
        important_words = ['roi', 'roi ratio', 'cost', 'benefit', 'intervention', 
                          'testing', 'screening', 'measure', 'star rating']
        query_lower = query.lower()
        return [word for word in important_words if word in query_lower]
    
    def _classify_query_type(self, query: str) -> str:
        """Classify query type."""
        query_lower = query.lower()
        if 'roi' in query_lower or 'return on investment' in query_lower:
            return "roi_analysis"
        elif 'performance' in query_lower or 'completion' in query_lower:
            return "performance_analysis"
        elif 'spec' in query_lower or 'requirement' in query_lower:
            return "specification_query"
        else:
            return "general_query"
    
    def _validate_phi(self, query: str) -> Tuple[bool, List[str]]:
        """
        Validate query for PHI leakage.
        
        Args:
            query: User query string
        
        Returns:
            Tuple of (is_valid, list_of_errors)
        """
        errors = []
        
        # PHI patterns from Rule 1.8
        phi_patterns = [
            (r'\b\d{3}-\d{2}-\d{4}\b', 'SSN pattern detected'),
            (r'\b\d{3}-\d{2}-\d{4}\b', 'SSN pattern detected'),
            (r'\b[A-Z][a-z]+\s+[A-Z][a-z]+\b', 'Potential name pattern detected'),
            (r'\b\d{1,2}/\d{1,2}/\d{4}\b', 'Potential date of birth pattern detected'),
            (r'\b\d{10,}\b', 'Potential member ID pattern detected'),
        ]
        
        for pattern, error_msg in phi_patterns:
            if re.search(pattern, query):
                errors.append(f"{error_msg}: {pattern}")
        
        return len(errors) == 0, errors
    
    def _estimate_tokens(self, context: Dict) -> int:
        """
        Estimate token count for context.
        Uses standalone estimate_tokens() function.
        
        Args:
            context: Context dictionary
        
        Returns:
            Estimated token count
        """
        return estimate_tokens(context)
    
    def _compress_context(self, context: Dict, target_tokens: int) -> Dict:
        """
        Compress context to fit within token limit.
        Uses compress_context() function internally.
        
        Args:
            context: Context dictionary
            target_tokens: Target token limit
        
        Returns:
            Compressed context dictionary
        """
        return compress_context(context, target_tokens, logger=logger)


def compress_context(context: Dict, target_tokens: int = 3000, logger: Optional[logging.Logger] = None) -> Dict:
    """
    Compress context to fit within token limit (Template 4).
    
    Strategy:
    1. Summarize retrieved documents to max 200 chars each
    2. Remove context with relevance < 0.5
    3. Truncate long text fields to target_tokens
    
    Args:
        context: Context dictionary (hierarchical or flat)
        target_tokens: Target token limit (default: 3000)
        logger: Optional logger for compression metrics
    
    Returns:
        Compressed context dictionary
    """
    if logger is None:
        logger = logging.getLogger(__name__)
    
    # Track compression metrics
    metrics = {
        "original_tokens": estimate_tokens(context),
        "target_tokens": target_tokens,
        "docs_before": 0,
        "docs_after": 0,
        "docs_removed": 0,
        "docs_summarized": 0,
        "relevance_threshold": 0.5
    }
    
    current_tokens = metrics["original_tokens"]
    compressed = context.copy()
    
    # Always apply relevance filtering and summarization (quality control)
    # Handle hierarchical context structure (layer_3_query)
    if "layer_3_query" in compressed:
        query_layer = compressed["layer_3_query"]
        retrieved_docs = query_layer.get("retrieved_docs", [])
        relevance_scores = query_layer.get("relevance_scores", [])
        
        metrics["docs_before"] = len(retrieved_docs)
        
        if retrieved_docs:
            # Step 1: Remove documents with relevance < 0.5 (always apply)
            filtered_docs = []
            filtered_scores = []
            
            for doc, score in zip(retrieved_docs, relevance_scores):
                if score >= 0.5:
                    filtered_docs.append(doc)
                    filtered_scores.append(score)
                else:
                    metrics["docs_removed"] += 1
            
            # Step 2: Summarize documents to max 200 chars each (always apply)
            summarized_docs = []
            for doc in filtered_docs:
                content = doc.get("content", "")
                if isinstance(content, str) and len(content) > 200:
                    summarized_content = summarize_document(content, max_length=200)
                    summarized_docs.append({
                        **doc,
                        "content": summarized_content,
                        "original_length": len(content),
                        "compressed": True
                    })
                    metrics["docs_summarized"] += 1
                else:
                    summarized_docs.append(doc)
            
            query_layer["retrieved_docs"] = summarized_docs
            query_layer["relevance_scores"] = filtered_scores
            metrics["docs_after"] = len(summarized_docs)
    
    # Handle flat context structure (direct retrieved_docs)
    elif "retrieved_docs" in compressed:
        retrieved_docs = compressed.get("retrieved_docs", [])
        relevance_scores = compressed.get("relevance_scores", [])
        
        metrics["docs_before"] = len(retrieved_docs)
        
        if retrieved_docs:
            # Step 1: Remove documents with relevance < 0.5 (always apply)
            filtered_docs = []
            filtered_scores = []
            
            for doc, score in zip(retrieved_docs, relevance_scores):
                if score >= 0.5:
                    filtered_docs.append(doc)
                    filtered_scores.append(score)
                else:
                    metrics["docs_removed"] += 1
            
            # Step 2: Summarize documents to max 200 chars each (always apply)
            summarized_docs = []
            for doc in filtered_docs:
                content = doc.get("content", "")
                if isinstance(content, str) and len(content) > 200:
                    summarized_content = summarize_document(content, max_length=200)
                    summarized_docs.append({
                        **doc,
                        "content": summarized_content,
                        "original_length": len(content),
                        "compressed": True
                    })
                    metrics["docs_summarized"] += 1
                else:
                    summarized_docs.append(doc)
            
            compressed["retrieved_docs"] = summarized_docs
            compressed["relevance_scores"] = filtered_scores
            metrics["docs_after"] = len(summarized_docs)
    
    # Step 3: Truncate long text fields if still over token limit
    current_tokens = estimate_tokens(compressed)
    
    if current_tokens <= target_tokens:
        logger.info(
            f"Context compression complete (within limit): {metrics['original_tokens']} -> "
            f"{current_tokens} tokens. Docs: {metrics['docs_before']} -> {metrics['docs_after']} "
            f"({metrics['docs_removed']} removed, {metrics['docs_summarized']} summarized)"
        )
    else:
        logger.info(
            f"Compressing context: {current_tokens} tokens -> target: {target_tokens} tokens "
            f"({current_tokens - target_tokens} tokens to remove)"
        )
    
    # Step 3: Truncate long text fields if still over limit
    current_tokens = estimate_tokens(compressed)
    if current_tokens > target_tokens:
        # Truncate domain knowledge fields
        if "layer_1_domain" in compressed:
            domain = compressed["layer_1_domain"]
            for field in ["hedis_overview", "star_ratings"]:
                if field in domain and isinstance(domain[field], str):
                    max_field_tokens = (target_tokens - estimate_tokens(compressed)) + len(domain[field]) // 4
                    max_field_chars = max_field_tokens * 4
                    if len(domain[field]) > max_field_chars:
                        domain[field] = domain[field][:max_field_chars] + "..."
        
        # Truncate measure context if needed
        if "layer_2_measure" in compressed:
            measure_context = compressed["layer_2_measure"]
            for measure_id, measure_data in measure_context.items():
                if isinstance(measure_data, dict) and "spec" in measure_data:
                    spec = measure_data["spec"]
                    for field in ["name", "target_population"]:
                        if field in spec and isinstance(spec[field], str) and len(spec[field]) > 100:
                            spec[field] = spec[field][:100] + "..."
    
    # Log compression metrics
    final_tokens = estimate_tokens(compressed)
    compression_ratio = (1 - final_tokens / metrics["original_tokens"]) * 100 if metrics["original_tokens"] > 0 else 0
    
    metrics.update({
        "final_tokens": final_tokens,
        "tokens_removed": metrics["original_tokens"] - final_tokens,
        "compression_ratio": compression_ratio,
        "within_limit": final_tokens <= target_tokens
    })
    
    logger.info(
        f"Context compression complete: "
        f"{metrics['original_tokens']} -> {final_tokens} tokens "
        f"({compression_ratio:.1f}% reduction). "
        f"Docs: {metrics['docs_before']} -> {metrics['docs_after']} "
        f"({metrics['docs_removed']} removed, {metrics['docs_summarized']} summarized)"
    )
    
    # Store metrics in context for audit trail
    compressed["_compression_metrics"] = metrics
    
    return compressed


def summarize_document(content: str, max_length: int = 200) -> str:
    """
    Summarize a document to max_length characters.
    
    Strategy:
    - If content is short, return as-is
    - If content is long, take first max_length chars and add "..."
    - Try to break at sentence boundary if possible
    
    Args:
        content: Document content string
        max_length: Maximum length in characters
    
    Returns:
        Summarized content string
    """
    if not isinstance(content, str):
        content = str(content)
    
    if len(content) <= max_length:
        return content
    
    # Try to break at sentence boundary
    truncated = content[:max_length]
    last_period = truncated.rfind('.')
    last_newline = truncated.rfind('\n')
    
    # Use sentence boundary if within last 50 chars
    if last_period > max_length - 50:
        return truncated[:last_period + 1] + "..."
    elif last_newline > max_length - 50:
        return truncated[:last_newline] + "..."
    else:
        return truncated + "..."


def estimate_tokens(context: Dict) -> int:
    """
    Estimate token count for context.
    
    Uses simple approximation: ~4 characters per token.
    
    Args:
        context: Context dictionary
    
    Returns:
        Estimated token count
    """
    context_str = str(context)
    # Rough approximation: 4 characters per token
    return len(context_str) // 4


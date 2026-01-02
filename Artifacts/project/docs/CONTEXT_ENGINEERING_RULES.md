# Context Engineering Rules & Templates for Healthcare AI

## Core Principle
**Context engineering in healthcare AI must balance information richness with security, compliance, and clinical accuracy.**

---

## 1. Context Engineering Rules

### Rule 1.1: HIPAA-Compliant Context Assembly
**ALWAYS** de-identify PHI before including in context windows.

```python
# ✅ GOOD: De-identified context
context = {
    "measure_spec": hedis_specs.get("CDC"),
    "aggregate_stats": {"avg_roi": 1.35, "members_count": 1500},  # No PHI
    "clinical_guidelines": diabetes_care_guidelines
}

# ❌ BAD: Contains PHI
context = {
    "member_id": "12345",
    "member_name": "John Doe",
    "diagnosis_date": "2024-01-15"
}
```

### Rule 1.2: Hierarchical Context Structure
**ALWAYS** structure context in layers: Domain → Measure → Member (aggregated).

```
Layer 1: Domain Knowledge (HEDIS specs, clinical guidelines)
Layer 2: Measure-Specific Context (CDC measure details, ROI data)
Layer 3: Query-Specific Context (member aggregates, predictions)
```

### Rule 1.3: Context Window Management
**NEVER** exceed token limits. **ALWAYS** prioritize most relevant context.

- **Priority Order**: Regulatory requirements > Clinical guidelines > Measure specs > Aggregate data
- **Compression**: Summarize retrieved documents before LLM call
- **Truncation**: Remove least relevant context if window is full

### Rule 1.4: Domain-Specific Terminology
**ALWAYS** include healthcare terminology definitions in context.

```python
TERMINOLOGY_CONTEXT = """
HEDIS: Healthcare Effectiveness Data and Information Set
PHI: Protected Health Information
Star Rating: CMS quality rating (1-5 stars)
Gap-in-Care: Member missing required preventive service
ROI: Return on Investment (revenue impact / intervention cost)
"""
```

### Rule 1.5: Few-Shot Examples in Context
**INCLUDE** 2-3 successful query examples for complex reasoning tasks.

```python
FEW_SHOT_EXAMPLES = """
Example 1:
Query: "Which measures have declining trends?"
Context: [Retrieved measure performance data]
Response: "HbA1c Testing shows -2.3% trend. Recommend prioritizing 847 members."

Example 2:
Query: "Calculate ROI for diabetes interventions"
Context: [CDC measure data, cost data, revenue impact]
Response: "ROI: 1.35x. Net benefit: $285K for 1,500 interventions."
"""
```

### Rule 1.6: Temporal Context Awareness
**ALWAYS** include temporal context for time-sensitive queries.

```python
TEMPORAL_CONTEXT = """
Current Date: 2024-12-15
Measurement Year: 2025
Lookback Period: 365 days
Intervention Window: Next 30 days
"""
```

### Rule 1.7: Regulatory Compliance Context
**ALWAYS** include compliance requirements in context for regulatory queries.

```python
COMPLIANCE_CONTEXT = """
HIPAA: De-identification required for all PHI
CMS: Star Rating methodology (2025)
HEDIS MY2025: Current specification version
HEI: Health Equity Index (2027 requirement)
"""
```

### Rule 1.8: Context Validation
**ALWAYS** validate context before sending to LLM.

- Check for PHI leakage
- Verify context relevance (semantic similarity > 0.7)
- Ensure completeness (all required fields present)
- Validate format (JSON, structured text)

---

## 2. Context Engineering Templates

### Template 1: Basic Context Assembly

```python
def assemble_basic_context(query: str, measure_id: str = None) -> Dict:
    """
    Assemble basic context for HEDIS queries.
    
    Args:
        query: User query
        measure_id: Optional measure ID for measure-specific context
    
    Returns:
        Dictionary with structured context
    """
    context = {
        "domain": "HEDIS Healthcare Quality",
        "terminology": TERMINOLOGY_CONTEXT,
        "temporal": TEMPORAL_CONTEXT,
        "compliance": COMPLIANCE_CONTEXT,
        "query": query
    }
    
    if measure_id:
        context["measure_spec"] = get_hedis_measure_spec(measure_id)
        context["measure_performance"] = get_aggregate_performance(measure_id)
    
    return context
```

### Template 2: Hierarchical Context Builder

```python
class HierarchicalContextBuilder:
    """Build context in hierarchical layers."""
    
    def build_context(self, query: str, max_tokens: int = 4000) -> Dict:
        """
        Build hierarchical context with token management.
        
        Layers:
        1. Domain knowledge (always included)
        2. Measure-specific (if relevant)
        3. Query-specific (retrieved dynamically)
        """
        context = {
            "layer_1_domain": self._get_domain_knowledge(),
            "layer_2_measure": self._get_measure_context(query),
            "layer_3_query": self._get_query_specific_context(query)
        }
        
        # Compress if needed
        if self._estimate_tokens(context) > max_tokens:
            context = self._compress_context(context, max_tokens)
        
        return context
    
    def _get_domain_knowledge(self) -> Dict:
        """Layer 1: Core domain knowledge."""
        return {
            "hedis_overview": "HEDIS measures healthcare quality...",
            "star_ratings": "CMS Star Ratings impact revenue...",
            "terminology": TERMINOLOGY_CONTEXT
        }
    
    def _get_measure_context(self, query: str) -> Dict:
        """Layer 2: Measure-specific context."""
        measures = self._extract_measures_from_query(query)
        return {
            measure_id: {
                "spec": get_hedis_spec(measure_id),
                "performance": get_aggregate_stats(measure_id)
            }
            for measure_id in measures
        }
    
    def _get_query_specific_context(self, query: str) -> Dict:
        """Layer 3: Query-specific retrieved context."""
        # Use RAG to retrieve relevant documents
        retrieved = self.rag_retriever.retrieve(query, top_k=5)
        return {
            "retrieved_docs": retrieved,
            "relevance_scores": [doc.score for doc in retrieved]
        }
```

### Template 3: Prompt Template with Context

```python
HEDIS_PROMPT_TEMPLATE = """You are an expert healthcare analytics consultant specializing in HEDIS measure optimization and Medicare Advantage Star Ratings.

{domain_context}

{measure_context}

{query_context}

{compliance_context}

{few_shot_examples}

User Query: {user_query}

Instructions:
1. Use the provided context to answer accurately
2. Reference specific measures, metrics, and data from context
3. Provide actionable recommendations with numbers
4. Ensure all responses comply with HIPAA (no PHI)
5. Use healthcare terminology correctly

Response Format: JSON with keys: summary, recommendations, metrics
"""
```

### Template 4: Context Compression

```python
def compress_context(context: Dict, target_tokens: int) -> Dict:
    """
    Compress context to fit within token limit.
    
    Strategy:
    1. Summarize retrieved documents
    2. Remove least relevant context
    3. Truncate long text fields
    """
    current_tokens = estimate_tokens(context)
    
    if current_tokens <= target_tokens:
        return context
    
    # Compress retrieved documents
    if "retrieved_docs" in context:
        context["retrieved_docs"] = [
            summarize_document(doc, max_length=200)
            for doc in context["retrieved_docs"]
        ]
    
    # Remove least relevant context
    relevance_scores = context.get("relevance_scores", [])
    if relevance_scores:
        threshold = np.percentile(relevance_scores, 50)
        context["retrieved_docs"] = [
            doc for doc, score in zip(context["retrieved_docs"], relevance_scores)
            if score >= threshold
        ]
    
    return context
```

### Template 5: Context Validation

```python
def validate_context(context: Dict) -> Tuple[bool, List[str]]:
    """
    Validate context before LLM call.
    
    Returns:
        (is_valid, errors)
    """
    errors = []
    
    # Check for PHI
    phi_patterns = [
        r'\b\d{3}-\d{2}-\d{4}\b',  # SSN
        r'\b[A-Z][a-z]+\s+[A-Z][a-z]+\b',  # Names
        r'\b\d{1,2}/\d{1,2}/\d{4}\b'  # Dates (potential DOB)
    ]
    
    context_str = str(context)
    for pattern in phi_patterns:
        if re.search(pattern, context_str):
            errors.append(f"Potential PHI detected: {pattern}")
    
    # Check relevance
    if "relevance_scores" in context:
        avg_relevance = np.mean(context["relevance_scores"])
        if avg_relevance < 0.5:
            errors.append(f"Low context relevance: {avg_relevance:.2f}")
    
    # Check completeness
    required_fields = ["domain", "query"]
    for field in required_fields:
        if field not in context:
            errors.append(f"Missing required field: {field}")
    
    return len(errors) == 0, errors
```

---

## 3. Context Engineering Best Practices

### Practice 1: Context Caching
Cache domain knowledge and measure specs (changes infrequently).

```python
@lru_cache(maxsize=100)
def get_hedis_measure_spec(measure_id: str) -> Dict:
    """Cache measure specs (rarely change)."""
    return load_measure_spec(measure_id)
```

### Practice 2: Context Versioning
Version context templates for reproducibility.

```python
CONTEXT_VERSION = "1.0.0"
CONTEXT_TEMPLATE_VERSION = {
    "domain": "1.0.0",
    "measure": "1.0.0",
    "compliance": "1.0.0"
}
```

### Practice 3: Context Logging
Log all context sent to LLM for audit trail.

```python
def log_context(context: Dict, query: str, response: str):
    """Log context for audit trail."""
    audit_log = {
        "timestamp": datetime.now().isoformat(),
        "query": query,
        "context_hash": hash(str(context)),
        "context_size": estimate_tokens(context),
        "response": response
    }
    write_audit_log(audit_log)
```

### Practice 4: Context Metrics
Track context effectiveness.

```python
CONTEXT_METRICS = {
    "avg_context_size": 0,
    "avg_relevance_score": 0,
    "compression_rate": 0,
    "validation_failures": 0
}
```

---

## 4. Healthcare-Specific Context Patterns

### Pattern 1: Clinical Context
```python
CLINICAL_CONTEXT_TEMPLATE = """
Measure: {measure_name}
Clinical Rationale: {clinical_rationale}
Evidence Base: {evidence_level}
Guidelines: {clinical_guidelines}
Temporal Requirements: {temporal_logic}
```

### Pattern 2: Financial Context
```python
FINANCIAL_CONTEXT_TEMPLATE = """
Measure: {measure_name}
Revenue per Star Point: ${revenue_per_point:,.0f}
Current Performance: {current_rate:.1f}%
Target Performance: {target_rate:.1f}%
Gap: {gap:.1f}%
Members to Close Gap: {members_needed:,}
ROI Ratio: {roi_ratio:.2f}x
```

### Pattern 3: Compliance Context
```python
COMPLIANCE_CONTEXT_TEMPLATE = """
HIPAA Status: ✅ De-identified data only
CMS Compliance: ✅ HEDIS MY2025 compliant
HEI Ready: ✅ Health Equity Index calculations included
Audit Trail: ✅ All queries logged
```

---

## 5. Context Engineering Checklist

Before sending context to LLM:

- [ ] PHI de-identified
- [ ] Context structured hierarchically
- [ ] Token limit checked
- [ ] Relevance scores > 0.5
- [ ] Required fields present
- [ ] Terminology included
- [ ] Temporal context included
- [ ] Compliance context included
- [ ] Few-shot examples included (if complex query)
- [ ] Context validated
- [ ] Context logged for audit

---

## 6. Implementation Priority

### Phase 1: Foundation
1. Basic context assembly template
2. PHI validation
3. Context logging

### Phase 2: Enhancement
1. Hierarchical context builder
2. Context compression
3. Relevance scoring

### Phase 3: Advanced
1. Dynamic context adaptation
2. Few-shot learning
3. Context effectiveness metrics

---

**Remember**: Context engineering in healthcare must prioritize security, compliance, and clinical accuracy over information richness.



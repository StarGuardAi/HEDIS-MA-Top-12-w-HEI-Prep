# Joint Rules & Templates: Context Engineering + Agentic RAG

## Core Principle
**When combining context engineering with agentic RAG, maintain security, compliance, and clinical accuracy while maximizing reasoning capability.**

---

## 1. Joint Rules

### Rule 3.1: Context-Aware Planning
**ALWAYS** use context to inform agentic planning decisions.

```python
def plan_with_context(query: str, initial_context: Dict) -> Dict:
    """
    Plan agentic steps using initial context.
    
    Context informs:
    - Which tools to use
    - What to retrieve
    - How to structure steps
    """
    # Use context to determine relevant measures
    measures = extract_measures_from_context(initial_context)
    
    # Plan steps based on context
    plan = {
        "steps": [
            {
                "type": "retrieve",
                "query": f"HEDIS specifications for {measures}",
                "context_hint": initial_context.get("domain")
            },
            {
                "type": "query_db",
                "query_type": "performance",
                "measure_id": measures[0],
                "context_filters": initial_context.get("filters", {})
            }
        ]
    }
    
    return plan
```

### Rule 3.2: Context Accumulation Across Steps
**ALWAYS** accumulate and refine context as agentic steps execute.

```python
class ContextAwareAgenticRAG:
    """Agentic RAG with context accumulation."""
    
    def __init__(self):
        self.context_builder = HierarchicalContextBuilder()
        self.context_accumulator = ContextAccumulator()
        self.agentic_agent = HEDISAgenticRAG()
    
    def process_query(self, query: str) -> Dict:
        """Process with context-aware agentic RAG."""
        # Step 1: Build initial context
        initial_context = self.context_builder.build_context(query)
        
        # Step 2: Plan with context
        plan = self.plan_with_context(query, initial_context)
        
        # Step 3: Execute steps, accumulating context
        for step in plan["steps"]:
            result = self.execute_step(step, self.context_accumulator.get_context())
            self.context_accumulator.add_step_result(step["type"], result)
            
            # Refine context based on step result
            refined_context = self.refine_context(
                self.context_accumulator.get_context(),
                result
            )
            self.context_accumulator.update_context(refined_context)
        
        # Step 4: Synthesize with full accumulated context
        final_context = self.context_accumulator.get_full_context()
        response = self.synthesize_with_context(query, final_context)
        
        return response
```

### Rule 3.3: Context-Driven Tool Selection
**ALWAYS** select tools based on available context and query requirements.

```python
def select_tools_with_context(query: str, context: Dict) -> List[str]:
    """
    Select tools based on context and query.
    
    Context indicators:
    - Domain knowledge → retrieve tool
    - Measure-specific → query_db tool
    - Calculation needed → calculate tool
    - Validation needed → validate tool
    """
    tools = []
    
    # Check if domain knowledge needed
    if not context.get("domain_knowledge"):
        tools.append("retrieve")
    
    # Check if database query needed
    if "measure_id" in context or "member_data" in query.lower():
        tools.append("query_db")
    
    # Check if calculation needed
    if any(keyword in query.lower() for keyword in ["roi", "calculate", "compute"]):
        tools.append("calculate")
    
    # Check if validation needed
    if "validate" in query.lower() or "compliance" in query.lower():
        tools.append("validate")
    
    return tools
```

### Rule 3.4: Context Compression for Agentic Steps
**ALWAYS** compress context before each agentic step to stay within token limits.

```python
def execute_step_with_compressed_context(step: Dict, context: Dict) -> Any:
    """Execute step with compressed context."""
    # Compress context for this step
    step_context = compress_context_for_step(context, step["type"])
    
    # Execute step with compressed context
    result = execute_step(step, step_context)
    
    # Expand context with result
    expanded_context = expand_context_with_result(context, result)
    
    return result, expanded_context
```

### Rule 3.5: Context Validation in Agentic Loops
**ALWAYS** validate context at each agentic step to prevent error propagation.

```python
def execute_agentic_step_with_validation(step: Dict, context: Dict) -> Tuple[Any, Dict]:
    """Execute step with context validation."""
    # Validate context before step
    is_valid, errors = validate_context(context)
    if not is_valid:
        raise ContextValidationError(f"Context validation failed: {errors}")
    
    # Execute step
    result = execute_step(step, context)
    
    # Validate result
    if not validate_result(result):
        # Refine context and retry
        refined_context = refine_context_from_error(context, result)
        return execute_agentic_step_with_validation(step, refined_context)
    
    # Update context with result
    updated_context = update_context_with_result(context, result)
    
    return result, updated_context
```

### Rule 3.6: Joint Audit Trail
**ALWAYS** log both context and agentic steps together for complete audit trail.

```python
class JointAuditLogger:
    """Log context and agentic steps together."""
    
    def log_joint_execution(self, query: str, context: Dict, plan: Dict, results: List[Any]):
        """Log complete execution with context and steps."""
        audit_entry = {
            "timestamp": datetime.now().isoformat(),
            "query": query,
            "initial_context": {
                "size": estimate_tokens(context),
                "hash": hash(str(context)),
                "layers": list(context.keys())
            },
            "plan": {
                "steps_count": len(plan["steps"]),
                "steps": [
                    {
                        "type": step["type"],
                        "context_used": step.get("context_hint")
                    }
                    for step in plan["steps"]
                ]
            },
            "results": [
                {
                    "step_type": result["step_type"],
                    "result_hash": hash(str(result)),
                    "execution_time": result.get("execution_time")
                }
                for result in results
            ],
            "final_context": {
                "size": estimate_tokens(context),
                "hash": hash(str(context))
            }
        }
        
        write_audit_log(audit_entry)
```

---

## 2. Joint Templates

### Template 1: Context-Aware Agentic RAG Agent

```python
class ContextAwareAgenticRAG:
    """
    Complete agentic RAG with context engineering.
    
    Combines:
    - Hierarchical context building
    - Agentic planning
    - Context accumulation
    - Tool execution
    - Response synthesis
    """
    
    def __init__(self):
        # Context engineering components
        self.context_builder = HierarchicalContextBuilder()
        self.context_compressor = ContextCompressor()
        self.context_validator = ContextValidator()
        
        # Agentic RAG components
        self.plan_agent = PlanningAgent()
        self.tool_executor = ToolExecutor()
        self.synthesizer = ResponseSynthesizer()
        self.result_validator = ResultValidator()
        
        # Joint components
        self.context_accumulator = ContextAccumulator()
        self.audit_logger = JointAuditLogger()
    
    def process_query(self, query: str, max_steps: int = 10) -> Dict:
        """
        Process query with context-aware agentic RAG.
        
        Flow:
        1. Build initial hierarchical context
        2. Plan agentic steps using context
        3. Execute steps, accumulating context
        4. Compress context as needed
        5. Synthesize final response
        6. Validate and retry if needed
        """
        # Step 1: Build initial context
        initial_context = self.context_builder.build_context(query)
        
        # Step 2: Validate initial context
        is_valid, errors = self.context_validator.validate(initial_context)
        if not is_valid:
            raise ContextValidationError(f"Initial context invalid: {errors}")
        
        # Step 3: Plan with context
        plan = self.plan_agent.decompose_with_context(query, initial_context)
        
        # Step 4: Initialize context accumulator
        self.context_accumulator.initialize(initial_context)
        
        # Step 5: Execute agentic steps
        step_results = []
        for i, step in enumerate(plan["steps"]):
            if i >= max_steps:
                break
            
            # Get current accumulated context
            current_context = self.context_accumulator.get_full_context()
            
            # Compress context if needed
            compressed_context = self.context_compressor.compress(
                current_context,
                target_tokens=2000
            )
            
            # Execute step with compressed context
            try:
                result = self.tool_executor.execute(
                    step["type"],
                    step["params"],
                    context=compressed_context
                )
                
                # Validate result
                if not self.result_validator.validate(result):
                    # Refine context and retry
                    refined_context = self.refine_context_from_result(
                        compressed_context,
                        result
                    )
                    result = self.tool_executor.execute(
                        step["type"],
                        step["params"],
                        context=refined_context
                    )
                
                # Accumulate context
                self.context_accumulator.add_step_result(step["type"], result)
                step_results.append(result)
                
            except Exception as e:
                logger.error(f"Step {i} failed: {e}")
                # Fallback strategy
                result = self.fallback_step_execution(step, compressed_context)
                self.context_accumulator.add_step_result(step["type"], result)
                step_results.append(result)
        
        # Step 6: Synthesize with full accumulated context
        final_context = self.context_accumulator.get_full_context()
        response = self.synthesizer.generate_with_context(query, final_context)
        
        # Step 7: Validate final response
        if not self.result_validator.validate(response):
            # Retry with refined query
            return self.process_query(query, max_steps=max_steps)
        
        # Step 8: Audit log
        self.audit_logger.log_joint_execution(
            query,
            initial_context,
            plan,
            step_results
        )
        
        return {
            "response": response,
            "steps_executed": len(step_results),
            "context_used": {
                "initial_size": estimate_tokens(initial_context),
                "final_size": estimate_tokens(final_context)
            },
            "plan": plan
        }
    
    def refine_context_from_result(self, context: Dict, result: Any) -> Dict:
        """Refine context based on step result."""
        # Add result to context
        context["recent_results"] = context.get("recent_results", [])
        context["recent_results"].append(result)
        
        # Update relevance scores
        if "relevance_scores" in context:
            context["relevance_scores"] = update_relevance_scores(
                context["relevance_scores"],
                result
            )
        
        return context
    
    def fallback_step_execution(self, step: Dict, context: Dict) -> Any:
        """Fallback strategy for failed steps."""
        if step["type"] == "retrieve":
            # Fallback to keyword search
            return keyword_search(step["query"])
        elif step["type"] == "query_db":
            # Fallback to cached query
            return get_cached_query_result(step["params"])
        else:
            raise StepExecutionError(f"No fallback for step type: {step['type']}")
```

### Template 2: Context-Driven Planning Agent

```python
class ContextDrivenPlanningAgent:
    """Planning agent that uses context to inform decisions."""
    
    def decompose_with_context(self, query: str, context: Dict) -> Dict:
        """
        Decompose query using context to inform planning.
        
        Context informs:
        - Available measures
        - Relevant tools
        - Step dependencies
        - Expected results
        """
        # Extract context hints
        measures = context.get("layer_2_measure", {}).keys()
        domain_knowledge = context.get("layer_1_domain", {})
        
        # Build planning prompt with context
        planning_prompt = f"""Decompose this query into executable steps.

Context:
- Available measures: {list(measures)}
- Domain knowledge: {domain_knowledge.get('hedis_overview', '')[:200]}

Query: {query}

Plan steps that:
1. Use context to inform tool selection
2. Respect dependencies between steps
3. Accumulate context across steps

Return JSON plan.
"""
        
        plan_response = self.llm.generate(planning_prompt)
        plan = json.loads(plan_response)
        
        # Enhance plan with context hints
        for step in plan["steps"]:
            step["context_hint"] = self._get_context_hint(step, context)
        
        return plan
    
    def _get_context_hint(self, step: Dict, context: Dict) -> str:
        """Get context hint for step."""
        if step["type"] == "retrieve":
            return context.get("layer_1_domain", {}).get("hedis_overview", "")[:100]
        elif step["type"] == "query_db":
            measures = context.get("layer_2_measure", {}).keys()
            return f"Measures in context: {list(measures)}"
        return ""
```

### Template 3: Context-Accumulating Tool Executor

```python
class ContextAwareToolExecutor:
    """Tool executor that uses and updates context."""
    
    def execute(self, tool_name: str, params: Dict, context: Dict = None) -> Any:
        """
        Execute tool with context awareness.
        
        Context used for:
        - Parameter enrichment
        - Result validation
        - Error recovery
        """
        # Enrich params with context
        enriched_params = self._enrich_params_with_context(params, context)
        
        # Execute tool
        result = self._execute_tool(tool_name, enriched_params)
        
        # Validate result against context
        if context:
            validated_result = self._validate_result_against_context(result, context)
            if not validated_result["is_valid"]:
                # Refine params and retry
                refined_params = self._refine_params_from_validation(
                    enriched_params,
                    validated_result["errors"]
                )
                result = self._execute_tool(tool_name, refined_params)
        
        return result
    
    def _enrich_params_with_context(self, params: Dict, context: Dict) -> Dict:
        """Enrich tool parameters with context."""
        enriched = params.copy()
        
        if context:
            # Add measure context if available
            if "measure_id" in params and "layer_2_measure" in context:
                measure_id = params["measure_id"]
                if measure_id in context["layer_2_measure"]:
                    enriched["measure_context"] = context["layer_2_measure"][measure_id]
            
            # Add domain context
            if "layer_1_domain" in context:
                enriched["domain_context"] = context["layer_1_domain"]
        
        return enriched
    
    def _validate_result_against_context(self, result: Any, context: Dict) -> Dict:
        """Validate result against context expectations."""
        # Check if result aligns with context
        if isinstance(result, dict):
            # Validate measure IDs match context
            if "measure_id" in result:
                measures_in_context = context.get("layer_2_measure", {}).keys()
                if result["measure_id"] not in measures_in_context:
                    return {
                        "is_valid": False,
                        "errors": [f"Measure {result['measure_id']} not in context"]
                    }
        
        return {"is_valid": True, "errors": []}
```

### Template 4: Joint Response Synthesizer

```python
class JointResponseSynthesizer:
    """Synthesize response using both context and agentic results."""
    
    SYNTHESIS_PROMPT = """Synthesize a comprehensive response using accumulated context and agentic step results.

Initial Context:
{initial_context}

Agentic Step Results:
{step_results}

Accumulated Context:
{accumulated_context}

User Query: {query}

Create a response that:
1. Answers the query comprehensively
2. References specific data from context and results
3. Provides actionable recommendations
4. Uses healthcare terminology correctly
5. Includes specific metrics and numbers

Response Format: JSON
{
    "summary": "executive summary",
    "recommendations": ["rec1", "rec2"],
    "metrics": {...},
    "data_sources": ["source1", "source2"],
    "reasoning_steps": ["step1", "step2"]
}
"""
    
    def generate_with_context(self, query: str, context: Dict) -> Dict:
        """Generate response with full context."""
        # Extract components
        initial_context = context.get("initial", {})
        step_results = context.get("step_results", [])
        accumulated_context = context.get("accumulated", {})
        
        # Build synthesis prompt
        prompt = self.SYNTHESIS_PROMPT.format(
            query=query,
            initial_context=json.dumps(initial_context, indent=2),
            step_results=json.dumps(step_results, indent=2),
            accumulated_context=json.dumps(accumulated_context, indent=2)
        )
        
        # Generate response
        response = self.llm.generate(prompt)
        result = json.loads(response)
        
        # Add context metadata
        result["context_metadata"] = {
            "initial_context_size": estimate_tokens(initial_context),
            "steps_count": len(step_results),
            "accumulated_context_size": estimate_tokens(accumulated_context)
        }
        
        return result
```

---

## 3. Joint Best Practices

### Practice 1: Context-Aware Step Selection
```python
def select_steps_with_context(query: str, context: Dict) -> List[Dict]:
    """Select agentic steps based on available context."""
    steps = []
    
    # If domain knowledge missing, add retrieve step
    if not context.get("domain_knowledge"):
        steps.append({"type": "retrieve", "query": "HEDIS domain knowledge"})
    
    # If measure-specific query, add query_db step
    if extract_measures_from_query(query):
        steps.append({"type": "query_db", "query_type": "performance"})
    
    return steps
```

### Practice 2: Context Refinement Loop
```python
def refine_context_in_loop(context: Dict, step_result: Any, iteration: int) -> Dict:
    """Refine context based on step results in agentic loop."""
    # Add result to context
    context["step_results"] = context.get("step_results", [])
    context["step_results"].append(step_result)
    
    # Update relevance scores
    if iteration > 0:
        context["relevance_scores"] = update_relevance_from_results(
            context.get("relevance_scores", []),
            context["step_results"]
        )
    
    # Compress if needed
    if estimate_tokens(context) > 4000:
        context = compress_context(context, target_tokens=3000)
    
    return context
```

### Practice 3: Joint Error Recovery
```python
def recover_from_error_with_context(error: Exception, context: Dict, step: Dict) -> Dict:
    """Recover from error using context."""
    # Use context to determine recovery strategy
    if "domain_knowledge" in context:
        # Try alternative tool
        return execute_alternative_tool(step, context)
    else:
        # Fallback to simpler operation
        return execute_fallback_operation(step, context)
```

---

## 4. Joint Implementation Checklist

Before executing context-aware agentic RAG:

- [ ] Initial context built hierarchically
- [ ] Context validated (no PHI, relevance > 0.5)
- [ ] Plan created using context
- [ ] Context accumulator initialized
- [ ] Tools selected based on context
- [ ] Step dependencies validated
- [ ] Context compression configured
- [ ] Error recovery strategies defined
- [ ] Audit logging enabled
- [ ] Result validation configured
- [ ] Context refinement logic implemented
- [ ] Joint synthesis prompt prepared

---

## 5. Implementation Priority

### Phase 1: Foundation (Weeks 1-2)
1. Basic context-aware agentic RAG agent
2. Context-driven planning
3. Context accumulation
4. Joint audit logging

### Phase 2: Enhancement (Weeks 3-4)
1. Context compression in loops
2. Context-driven tool selection
3. Context refinement from errors
4. Joint error recovery

### Phase 3: Advanced (Weeks 5-6)
1. Dynamic context adaptation
2. Multi-agent coordination
3. Advanced context optimization
4. Performance tuning

---

## 6. Healthcare-Specific Joint Patterns

### Pattern 1: Cross-Measure Analysis with Context
```python
def cross_measure_analysis_with_context(measures: List[str]) -> Dict:
    """Cross-measure analysis using context-aware agentic RAG."""
    # Build context for measures
    context = build_measure_context(measures)
    
    # Plan cross-measure steps
    plan = {
        "steps": [
            {"type": "retrieve", "query": f"HEDIS specs for {measures}"},
            {"type": "query_db", "query_type": "member_overlaps", "measures": measures},
            {"type": "calculate", "operation": "cross_measure_roi", "measures": measures},
            {"type": "validate", "operation": "validate_cross_measure", "measures": measures}
        ]
    }
    
    # Execute with context accumulation
    return execute_plan_with_context(plan, context)
```

### Pattern 2: ROI Calculation with Context
```python
def roi_calculation_with_context(measure_id: str, context: Dict) -> Dict:
    """ROI calculation using context and agentic steps."""
    # Enhance context with measure-specific data
    enhanced_context = enhance_context_with_measure(context, measure_id)
    
    # Plan ROI calculation steps
    plan = {
        "steps": [
            {"type": "retrieve", "query": f"ROI data for {measure_id}"},
            {"type": "query_db", "query_type": "intervention_costs", "measure_id": measure_id},
            {"type": "query_db", "query_type": "revenue_impact", "measure_id": measure_id},
            {"type": "calculate", "operation": "roi", "measure_id": measure_id},
            {"type": "validate", "operation": "validate_roi", "measure_id": measure_id}
        ]
    }
    
    # Execute with context
    return execute_plan_with_context(plan, enhanced_context)
```

---

**Remember**: Joint context engineering and agentic RAG must work together seamlessly while maintaining security, compliance, and clinical accuracy.



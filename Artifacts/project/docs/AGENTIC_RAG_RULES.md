# Agentic RAG Rules & Templates for Healthcare AI

## Core Principle
**Agentic RAG in healthcare AI must demonstrate multi-step reasoning, tool calling, and self-correction while maintaining HIPAA compliance and clinical accuracy.**

---

## 1. Agentic RAG Rules

### Rule 2.1: Multi-Step Planning
**ALWAYS** decompose complex queries into executable steps before execution.

```python
# ✅ GOOD: Planned multi-step execution
plan = {
    "steps": [
        {"type": "retrieve", "query": "HbA1c testing requirements"},
        {"type": "query_db", "sql": "SELECT member_id FROM gaps WHERE measure='CDC'"},
        {"type": "calculate", "operation": "roi", "params": {...}},
        {"type": "synthesize", "context": "all_results"}
    ]
}

# ❌ BAD: Single-step without planning
response = llm.generate(query)  # No planning, no tool calling
```

### Rule 2.2: Tool Calling Pattern
**ALWAYS** use structured tool calling for database queries, calculations, and validations.

```python
TOOLS = {
    "query_database": {
        "description": "Query HEDIS database for member data (aggregated, de-identified)",
        "parameters": {
            "query_type": "gaps|performance|roi",
            "measure_id": "string",
            "filters": "dict"
        },
        "returns": "DataFrame with aggregated results"
    },
    "calculate_roi": {
        "description": "Calculate ROI for interventions",
        "parameters": {
            "measure_id": "string",
            "intervention_count": "int",
            "cost_per_intervention": "float"
        },
        "returns": "dict with roi_ratio, net_benefit"
    },
    "validate_hedis_spec": {
        "description": "Validate against HEDIS specifications",
        "parameters": {
            "measure_id": "string",
            "data": "dict"
        },
        "returns": "validation_result"
    }
}
```

### Rule 2.3: Self-Correction Loop
**ALWAYS** implement validation and retry logic for critical operations.

```python
def agentic_query_with_retry(query: str, max_retries: int = 3):
    """Execute query with self-correction."""
    for attempt in range(max_retries):
        result = execute_agentic_query(query)
        
        # Validate result
        if validate_result(result):
            return result
        
        # Refine query based on validation errors
        query = refine_query(query, result.validation_errors)
    
    raise AgenticRAGError("Max retries exceeded")
```

### Rule 2.4: Context Accumulation
**ALWAYS** accumulate context across steps in multi-step queries.

```python
class ContextAccumulator:
    """Accumulate context across agentic steps."""
    
    def __init__(self):
        self.context = {
            "retrieved_docs": [],
            "query_results": [],
            "calculations": [],
            "validations": []
        }
    
    def add_step_result(self, step_type: str, result: Any):
        """Add result from a step."""
        self.context[step_type].append(result)
    
    def get_full_context(self) -> Dict:
        """Get accumulated context for final synthesis."""
        return self.context
```

### Rule 2.5: Error Handling & Graceful Degradation
**ALWAYS** handle tool failures gracefully with fallback strategies.

```python
def execute_tool_with_fallback(tool_name: str, params: Dict):
    """Execute tool with fallback."""
    try:
        return TOOLS[tool_name].execute(params)
    except ToolError as e:
        logger.warning(f"Tool {tool_name} failed: {e}")
        
        # Fallback to simpler operation
        if tool_name == "query_database":
            return fallback_keyword_search(params)
        elif tool_name == "calculate_roi":
            return estimate_roi(params)
        
        raise
```

### Rule 2.6: Audit Trail for Agentic Steps
**ALWAYS** log all agentic steps for compliance and debugging.

```python
class AgenticAuditLogger:
    """Log all agentic RAG steps."""
    
    def log_step(self, step: Dict, result: Any, context: Dict):
        """Log a single agentic step."""
        audit_entry = {
            "timestamp": datetime.now().isoformat(),
            "step_type": step["type"],
            "step_params": step.get("params", {}),
            "result": sanitize_for_logging(result),
            "context_hash": hash(str(context)),
            "execution_time": step.get("execution_time")
        }
        write_audit_log(audit_entry)
```

### Rule 2.7: HIPAA-Compliant Tool Execution
**NEVER** expose PHI in tool calls or results.

```python
def execute_tool_safely(tool_name: str, params: Dict) -> Dict:
    """Execute tool with PHI protection."""
    # Validate no PHI in params
    validate_no_phi(params)
    
    # Execute tool
    result = TOOLS[tool_name].execute(params)
    
    # De-identify result
    result = de_identify_result(result)
    
    return result
```

### Rule 2.8: Step Dependency Management
**ALWAYS** respect dependencies between agentic steps.

```python
class StepDependencyManager:
    """Manage dependencies between agentic steps."""
    
    def validate_dependencies(self, plan: List[Dict]) -> bool:
        """Validate step dependencies are satisfied."""
        executed_steps = set()
        
        for step in plan:
            dependencies = step.get("depends_on", [])
            for dep in dependencies:
                if dep not in executed_steps:
                    return False
            executed_steps.add(step["id"])
        
        return True
```

---

## 2. Agentic RAG Templates

### Template 1: Basic Agentic RAG Agent

```python
class HEDISAgenticRAG:
    """Agentic RAG agent for HEDIS queries."""
    
    def __init__(self):
        self.rag_retriever = VectorRetriever()
        self.tool_executor = ToolExecutor()
        self.plan_agent = PlanningAgent()
        self.synthesizer = ResponseSynthesizer()
        self.validator = ResultValidator()
        self.context_accumulator = ContextAccumulator()
    
    def process_query(self, query: str) -> Dict:
        """
        Process query using agentic RAG.
        
        Steps:
        1. Plan decomposition
        2. Execute steps with tools
        3. Accumulate context
        4. Synthesize response
        5. Validate and retry if needed
        """
        # Step 1: Plan
        plan = self.plan_agent.decompose(query)
        
        # Step 2: Execute steps
        for step in plan["steps"]:
            if step["type"] == "retrieve":
                result = self.rag_retriever.retrieve(step["query"])
                self.context_accumulator.add_step_result("retrieved_docs", result)
            
            elif step["type"] == "query_db":
                result = self.tool_executor.execute("query_database", step["params"])
                self.context_accumulator.add_step_result("query_results", result)
            
            elif step["type"] == "calculate":
                result = self.tool_executor.execute(step["operation"], step["params"])
                self.context_accumulator.add_step_result("calculations", result)
            
            elif step["type"] == "validate":
                result = self.tool_executor.execute("validate_hedis_spec", step["params"])
                self.context_accumulator.add_step_result("validations", result)
        
        # Step 3: Synthesize
        full_context = self.context_accumulator.get_full_context()
        response = self.synthesizer.generate(query, full_context)
        
        # Step 4: Validate
        if not self.validator.validate(response):
            # Retry with refined context
            return self.process_query(query)
        
        return {
            "response": response,
            "steps_executed": len(plan["steps"]),
            "context_used": full_context
        }
```

### Template 2: Planning Agent

```python
class PlanningAgent:
    """Decompose queries into executable steps."""
    
    PLANNING_PROMPT = """You are a query planning agent for HEDIS healthcare analytics.

Given a user query, decompose it into executable steps.

Available tools:
- retrieve: Retrieve relevant HEDIS documentation
- query_db: Query database (aggregated, de-identified data only)
- calculate: Perform calculations (ROI, metrics)
- validate: Validate against HEDIS specifications

Return JSON with steps array:
{
    "steps": [
        {
            "id": "step_1",
            "type": "retrieve|query_db|calculate|validate",
            "query": "description of what to retrieve/query",
            "params": {...},
            "depends_on": []
        }
    ]
}

User Query: {query}
"""
    
    def decompose(self, query: str) -> Dict:
        """Decompose query into steps."""
        prompt = self.PLANNING_PROMPT.format(query=query)
        
        response = self.llm.generate(prompt)
        plan = json.loads(response)
        
        # Validate plan
        if not self._validate_plan(plan):
            raise PlanningError("Invalid plan structure")
        
        return plan
    
    def _validate_plan(self, plan: Dict) -> bool:
        """Validate plan structure."""
        required_fields = ["steps"]
        if not all(field in plan for field in required_fields):
            return False
        
        for step in plan["steps"]:
            if "type" not in step or "id" not in step:
                return False
        
        return True
```

### Template 3: Tool Executor

```python
class ToolExecutor:
    """Execute tools in agentic RAG workflow."""
    
    def __init__(self):
        self.tools = {
            "query_database": self._query_database,
            "calculate_roi": self._calculate_roi,
            "validate_hedis_spec": self._validate_hedis_spec
        }
    
    def execute(self, tool_name: str, params: Dict) -> Any:
        """Execute a tool."""
        if tool_name not in self.tools:
            raise ToolNotFoundError(f"Tool {tool_name} not found")
        
        # Validate no PHI
        validate_no_phi(params)
        
        # Execute tool
        try:
            result = self.tools[tool_name](params)
            
            # De-identify result
            result = de_identify_result(result)
            
            return result
        except Exception as e:
            logger.error(f"Tool {tool_name} failed: {e}")
            raise ToolExecutionError(f"Tool execution failed: {e}")
    
    def _query_database(self, params: Dict) -> pd.DataFrame:
        """Query database (aggregated data only)."""
        query_type = params.get("query_type")
        measure_id = params.get("measure_id")
        
        if query_type == "gaps":
            return execute_query(f"""
                SELECT 
                    measure_id,
                    COUNT(*) as gap_count,
                    AVG(predicted_success_rate) as avg_success_rate
                FROM member_gaps
                WHERE measure_id = '{measure_id}'
                GROUP BY measure_id
            """)
        # ... other query types
    
    def _calculate_roi(self, params: Dict) -> Dict:
        """Calculate ROI."""
        measure_id = params["measure_id"]
        intervention_count = params["intervention_count"]
        cost_per_intervention = params["cost_per_intervention"]
        
        # Get revenue impact
        revenue_per_point = get_revenue_per_point(measure_id)
        star_impact = calculate_star_impact(measure_id, intervention_count)
        
        total_cost = intervention_count * cost_per_intervention
        total_revenue = star_impact * revenue_per_point
        
        roi_ratio = total_revenue / total_cost if total_cost > 0 else 0
        net_benefit = total_revenue - total_cost
        
        return {
            "roi_ratio": roi_ratio,
            "net_benefit": net_benefit,
            "total_cost": total_cost,
            "total_revenue": total_revenue
        }
    
    def _validate_hedis_spec(self, params: Dict) -> Dict:
        """Validate against HEDIS specifications."""
        measure_id = params["measure_id"]
        data = params["data"]
        
        spec = get_hedis_spec(measure_id)
        validation_result = validate_against_spec(data, spec)
        
        return {
            "is_valid": validation_result.is_valid,
            "errors": validation_result.errors,
            "warnings": validation_result.warnings
        }
```

### Template 4: Response Synthesizer

```python
class ResponseSynthesizer:
    """Synthesize final response from accumulated context."""
    
    SYNTHESIS_PROMPT = """You are synthesizing a response from multiple agentic steps.

Context from steps:
{accumulated_context}

User Query: {query}

Synthesize a comprehensive response that:
1. Answers the user's query
2. References specific data from context
3. Provides actionable recommendations
4. Uses healthcare terminology correctly
5. Includes specific numbers and metrics

Response Format: JSON
{
    "summary": "executive summary",
    "recommendations": ["rec1", "rec2"],
    "metrics": {...},
    "data_sources": ["source1", "source2"]
}
"""
    
    def generate(self, query: str, context: Dict) -> Dict:
        """Generate synthesized response."""
        prompt = self.SYNTHESIS_PROMPT.format(
            query=query,
            accumulated_context=json.dumps(context, indent=2)
        )
        
        response = self.llm.generate(prompt)
        result = json.loads(response)
        
        return result
```

### Template 5: Result Validator

```python
class ResultValidator:
    """Validate agentic RAG results."""
    
    def validate(self, result: Dict) -> bool:
        """Validate result quality."""
        checks = [
            self._check_no_phi(result),
            self._check_completeness(result),
            self._check_accuracy(result),
            self._check_format(result)
        ]
        
        return all(checks)
    
    def _check_no_phi(self, result: Dict) -> bool:
        """Check no PHI in result."""
        result_str = str(result)
        phi_patterns = [
            r'\b\d{3}-\d{2}-\d{4}\b',  # SSN
            r'\b[A-Z][a-z]+\s+[A-Z][a-z]+\b'  # Names
        ]
        
        for pattern in phi_patterns:
            if re.search(pattern, result_str):
                return False
        
        return True
    
    def _check_completeness(self, result: Dict) -> bool:
        """Check result is complete."""
        required_fields = ["summary", "recommendations"]
        return all(field in result for field in required_fields)
    
    def _check_accuracy(self, result: Dict) -> bool:
        """Check result accuracy (basic checks)."""
        # Check metrics are numeric
        if "metrics" in result:
            for key, value in result["metrics"].items():
                if isinstance(value, (int, float)):
                    if value < 0 and key not in ["trend", "variance"]:
                        return False
        
        return True
    
    def _check_format(self, result: Dict) -> bool:
        """Check result format."""
        # Check recommendations is list
        if "recommendations" in result:
            if not isinstance(result["recommendations"], list):
                return False
        
        return True
```

---

## 3. Agentic RAG Best Practices

### Practice 1: Step Retry Logic
```python
def execute_step_with_retry(step: Dict, max_retries: int = 3):
    """Execute step with retry logic."""
    for attempt in range(max_retries):
        try:
            result = execute_step(step)
            if validate_step_result(result):
                return result
        except Exception as e:
            logger.warning(f"Step failed (attempt {attempt+1}): {e}")
            if attempt < max_retries - 1:
                step = refine_step(step, e)
    
    raise StepExecutionError("Max retries exceeded")
```

### Practice 2: Parallel Step Execution
```python
def execute_parallel_steps(steps: List[Dict]) -> List[Any]:
    """Execute independent steps in parallel."""
    independent_steps = [s for s in steps if not s.get("depends_on")]
    
    with ThreadPoolExecutor(max_workers=5) as executor:
        results = executor.map(execute_step, independent_steps)
    
    return list(results)
```

### Practice 3: Step Caching
```python
@lru_cache(maxsize=100)
def cached_query_database(query_hash: str) -> pd.DataFrame:
    """Cache database query results."""
    return execute_query(query_hash)
```

---

## 4. Healthcare-Specific Agentic Patterns

### Pattern 1: Cross-Measure Analysis
```python
CROSS_MEASURE_AGENTIC_PLAN = {
    "steps": [
        {"type": "retrieve", "query": "diabetes measures (CDC, EED, GSD)"},
        {"type": "query_db", "query_type": "member_overlaps", "measures": ["CDC", "EED", "GSD"]},
        {"type": "calculate", "operation": "cross_measure_roi", "measures": ["CDC", "EED", "GSD"]},
        {"type": "synthesize", "context": "all_results"}
    ]
}
```

### Pattern 2: ROI Calculation Workflow
```python
ROI_CALCULATION_PLAN = {
    "steps": [
        {"type": "retrieve", "query": "measure ROI data"},
        {"type": "query_db", "query_type": "intervention_costs", "measure_id": "CDC"},
        {"type": "query_db", "query_type": "revenue_impact", "measure_id": "CDC"},
        {"type": "calculate", "operation": "roi", "params": {...}},
        {"type": "validate", "operation": "validate_roi_calculation"},
        {"type": "synthesize", "context": "all_results"}
    ]
}
```

---

## 5. Agentic RAG Checklist

Before executing agentic query:

- [ ] Query decomposed into steps
- [ ] Step dependencies validated
- [ ] Tools available and validated
- [ ] PHI validation configured
- [ ] Error handling implemented
- [ ] Retry logic configured
- [ ] Audit logging enabled
- [ ] Result validation configured
- [ ] Context accumulation initialized
- [ ] Fallback strategies defined

---

## 6. Implementation Priority

### Phase 1: Foundation
1. Basic agentic RAG agent
2. Planning agent
3. Tool executor
4. PHI validation

### Phase 2: Enhancement
1. Self-correction loops
2. Context accumulation
3. Parallel step execution
4. Result validation

### Phase 3: Advanced
1. Dynamic tool discovery
2. Multi-agent coordination
3. Advanced error recovery
4. Performance optimization

---

**Remember**: Agentic RAG in healthcare must demonstrate reasoning capability while maintaining security, compliance, and clinical accuracy.



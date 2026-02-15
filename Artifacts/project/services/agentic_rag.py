"""
Agentic RAG Planning Agent and Tool Executor for Healthcare AI
Implements multi-step query decomposition and tool execution using Templates 2 & 3 from AGENTIC_RAG_RULES.md
"""
import json
import re
import logging
from typing import Dict, List, Optional, Any, Union, Tuple
from datetime import datetime
import sys
import os
import pandas as pd

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

try:
    from database.connection import get_db_context, engine
    from data.phase1_database import query_to_dataframe
    from utils.hedis_specs import get_measure_spec, MEASURE_REGISTRY
    HAS_DB = True
except ImportError:
    HAS_DB = False
    logger.warning("Database utilities not available. Some tools may not work.")

logger = logging.getLogger(__name__)


class PlanningError(Exception):
    """Exception raised for planning errors."""
    pass


class ToolNotFoundError(Exception):
    """Exception raised when tool is not found."""
    pass


class ToolExecutionError(Exception):
    """Exception raised when tool execution fails."""
    pass


class PlanningAgent:
    """
    Decompose queries into executable steps.
    
    Based on Template 2 from AGENTIC_RAG_RULES.md
    """
    
    PLANNING_PROMPT = """You are a query planning agent for HEDIS healthcare analytics.

Given a user query, decompose it into executable steps.

Available tools:
- retrieve: Retrieve relevant HEDIS documentation and specifications
- query_db: Query database (aggregated, de-identified data only)
- calculate: Perform calculations (ROI, metrics, prioritization)
- validate: Validate against HEDIS specifications
- synthesize: Synthesize final response from accumulated context

Step types and their purposes:
- retrieve: Get HEDIS specs, clinical guidelines, measure definitions
- query_db: Query member gaps, performance data, intervention costs (aggregated only)
- calculate: Calculate ROI, prioritize members, compute metrics
- validate: Validate results against HEDIS specifications
- synthesize: Combine all results into final response

Return JSON with steps array:
{{
    "steps": [
        {{
            "id": "step_1",
            "type": "retrieve|query_db|calculate|validate|synthesize",
            "query": "description of what to retrieve/query/calculate",
            "params": {{}},
            "depends_on": []
        }}
    ]
}}

Rules:
1. Always start with retrieve step for HEDIS specs if query mentions measures
2. Use query_db for member data, gaps, performance (aggregated only)
3. Use calculate for ROI, prioritization, metrics
4. Use validate to check against HEDIS specs
5. Always end with synthesize step
6. Set depends_on to indicate step dependencies (e.g., ["step_1"])

User Query: {query}
"""
    
    def __init__(self, use_llm: bool = False, llm_client=None):
        """
        Initialize PlanningAgent.
        
        Args:
            use_llm: If True, use LLM for planning. If False, use rule-based parsing.
            llm_client: Optional LLM client for planning (if use_llm=True)
        """
        self.use_llm = use_llm
        self.llm_client = llm_client
    
    def decompose(self, query: str) -> Dict:
        """
        Decompose query into executable steps.
        
        Args:
            query: User query string
        
        Returns:
            Dictionary with steps array:
            {
                "steps": [
                    {
                        "id": "step_1",
                        "type": "retrieve|query_db|calculate|validate|synthesize",
                        "query": "description",
                        "params": {},
                        "depends_on": []
                    }
                ]
            }
        
        Raises:
            PlanningError: If plan structure is invalid
        """
        logger.info(f"Decomposing query: {query}")
        
        if self.use_llm and self.llm_client:
            plan = self._decompose_with_llm(query)
        else:
            plan = self._decompose_rule_based(query)
        
        # Validate plan structure
        if not self._validate_plan(plan):
            raise PlanningError("Invalid plan structure after decomposition")
        
        logger.info(f"Generated plan with {len(plan['steps'])} steps")
        for i, step in enumerate(plan['steps'], 1):
            logger.debug(f"  Step {i}: {step['type']} - {step.get('query', 'N/A')}")
        
        return plan
    
    def _decompose_with_llm(self, query: str) -> Dict:
        """Decompose query using LLM."""
        prompt = self.PLANNING_PROMPT.format(query=query)
        
        try:
            response = self.llm_client.generate(prompt)
            plan = json.loads(response)
            return plan
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse LLM response as JSON: {e}")
            # Fallback to rule-based
            return self._decompose_rule_based(query)
        except Exception as e:
            logger.error(f"LLM planning failed: {e}")
            # Fallback to rule-based
            return self._decompose_rule_based(query)
    
    def _decompose_rule_based(self, query: str) -> Dict:
        """
        Decompose query using rule-based parsing.
        
        Parses common patterns:
        - "Find gaps" → query_db gaps
        - "Calculate ROI" → calculate ROI
        - "Prioritize" → calculate prioritization
        - Measure mentions → retrieve specs
        """
        query_lower = query.lower()
        steps = []
        step_counter = 1
        
        # Step 1: Retrieve HEDIS specs if measure mentioned
        measure_keywords = ['hba1c', 'a1c', 'cdc', 'gsd', 'ked', 'eed', 'cbp', 
                           'diabetes', 'measure', 'hedis']
        if any(keyword in query_lower for keyword in measure_keywords):
            measure_id = self._extract_measure_id(query)
            steps.append({
                "id": f"step_{step_counter}",
                "type": "retrieve",
                "query": f"Retrieve HEDIS specifications for {measure_id or 'mentioned measures'}",
                "params": {
                    "measure_id": measure_id,
                    "content_type": "specifications"
                },
                "depends_on": []
            })
            step_counter += 1
        
        # Step 2: Query database for gaps/performance data
        if 'gap' in query_lower or 'missing' in query_lower or 'need' in query_lower:
            measure_id = self._extract_measure_id(query)
            steps.append({
                "id": f"step_{step_counter}",
                "type": "query_db",
                "query": f"Query database for gaps in {measure_id or 'HbA1c testing'}",
                "params": {
                    "query_type": "gaps",
                    "measure_id": measure_id or "GSD",
                    "aggregated_only": True
                },
                "depends_on": [f"step_{step_counter - 1}"] if step_counter > 1 else []
            })
            step_counter += 1
        
        # Step 3: Calculate ROI if mentioned
        if 'roi' in query_lower or 'return on investment' in query_lower or 'calculate' in query_lower:
            measure_id = self._extract_measure_id(query)
            steps.append({
                "id": f"step_{step_counter}",
                "type": "calculate",
                "query": f"Calculate ROI for {measure_id or 'HbA1c testing'} interventions",
                "params": {
                    "operation": "roi",
                    "measure_id": measure_id or "GSD",
                    "intervention_count": "from_step_data",
                    "cost_per_intervention": "from_step_data"
                },
                "depends_on": [f"step_{step_counter - 1}"] if step_counter > 1 else []
            })
            step_counter += 1
        
        # Step 4: Prioritize if mentioned
        if 'prioritize' in query_lower or 'priority' in query_lower or 'risk' in query_lower:
            measure_id = self._extract_measure_id(query)
            steps.append({
                "id": f"step_{step_counter}",
                "type": "calculate",
                "query": f"Prioritize members by risk for {measure_id or 'HbA1c testing'}",
                "params": {
                    "operation": "prioritize",
                    "measure_id": measure_id or "GSD",
                    "prioritization_method": "risk_score",
                    "member_data": "from_step_data"
                },
                "depends_on": [f"step_{step_counter - 1}"] if step_counter > 1 else []
            })
            step_counter += 1
        
        # Step 5: Validate if validation mentioned
        if 'validate' in query_lower or 'check' in query_lower or 'verify' in query_lower:
            measure_id = self._extract_measure_id(query)
            steps.append({
                "id": f"step_{step_counter}",
                "type": "validate",
                "query": f"Validate results against HEDIS specifications for {measure_id or 'mentioned measures'}",
                "params": {
                    "measure_id": measure_id or "GSD",
                    "data": "from_step_data"
                },
                "depends_on": [f"step_{step_counter - 1}"] if step_counter > 1 else []
            })
            step_counter += 1
        
        # Final step: Always synthesize
        steps.append({
            "id": f"step_{step_counter}",
            "type": "synthesize",
            "query": "Synthesize final response from all accumulated context",
            "params": {
                "context": "all_results",
                "format": "structured"
            },
            "depends_on": [step["id"] for step in steps] if steps else []
        })
        
        return {"steps": steps}
    
    def _extract_measure_id(self, query: str) -> Optional[str]:
        """Extract measure ID from query."""
        query_lower = query.lower()
        
        # Measure mappings
        measure_map = {
            'hba1c': 'GSD',
            'a1c': 'GSD',
            'glycemic': 'GSD',
            'cdc': 'GSD',  # Legacy name
            'gsd': 'GSD',
            'ked': 'KED',
            'kidney': 'KED',
            'egfr': 'KED',
            'eed': 'EED',
            'eye exam': 'EED',
            'retinal': 'EED',
            'cbp': 'CBP',
            'blood pressure': 'CBP',
            'hypertension': 'CBP',
            'bcs': 'BCS',
            'breast cancer': 'BCS',
            'mammography': 'BCS',
            'col': 'COL',
            'colorectal': 'COL',
            'colonoscopy': 'COL'
        }
        
        for keyword, measure_id in measure_map.items():
            if keyword in query_lower:
                return measure_id
        
        return None
    
    def _validate_plan(self, plan: Dict) -> bool:
        """
        Validate plan structure.
        
        Checks:
        - Required fields present
        - Step structure valid
        - Step types valid
        - Dependencies valid
        
        Args:
            plan: Plan dictionary
        
        Returns:
            True if valid, False otherwise
        """
        # Check required fields
        if "steps" not in plan:
            logger.error("Plan missing 'steps' field")
            return False
        
        if not isinstance(plan["steps"], list):
            logger.error("Plan 'steps' must be a list")
            return False
        
        if len(plan["steps"]) == 0:
            logger.error("Plan must have at least one step")
            return False
        
        # Validate each step
        valid_step_types = {"retrieve", "query_db", "calculate", "validate", "synthesize"}
        step_ids = set()
        
        for i, step in enumerate(plan["steps"]):
            # Check required fields
            if "id" not in step:
                logger.error(f"Step {i+1} missing 'id' field")
                return False
            
            if "type" not in step:
                logger.error(f"Step {step.get('id', i+1)} missing 'type' field")
                return False
            
            # Check step type is valid
            if step["type"] not in valid_step_types:
                logger.error(f"Step {step['id']} has invalid type: {step['type']}")
                return False
            
            # Check for duplicate IDs
            if step["id"] in step_ids:
                logger.error(f"Duplicate step ID: {step['id']}")
                return False
            step_ids.add(step["id"])
            
            # Check depends_on is a list
            if "depends_on" in step:
                if not isinstance(step["depends_on"], list):
                    logger.error(f"Step {step['id']} 'depends_on' must be a list")
                    return False
                
                # Check dependencies reference valid step IDs
                for dep_id in step["depends_on"]:
                    if dep_id not in step_ids:
                        logger.warning(f"Step {step['id']} depends on {dep_id} which doesn't exist yet (may be forward reference)")
        
        # Check that last step is synthesize
        if plan["steps"][-1]["type"] != "synthesize":
            logger.warning("Last step should be 'synthesize' type")
            # Not a hard error, just a warning
        
        logger.debug(f"Plan validation passed: {len(plan['steps'])} steps")
        return True


class ToolExecutor:
    """
    Execute tools in agentic RAG workflow.
    
    Based on Template 3 from AGENTIC_RAG_RULES.md
    
    Tools:
    1. query_database: Query aggregated HEDIS data (no PHI)
    2. calculate_roi: Calculate ROI for interventions
    3. validate_hedis_spec: Validate against HEDIS specifications
    4. retrieve_docs: RAG retrieval for documentation
    """
    
    def __init__(self, rag_retriever=None):
        """
        Initialize ToolExecutor.
        
        Args:
            rag_retriever: Optional RAG retriever for retrieve_docs tool
        """
        self.rag_retriever = rag_retriever
        self.tools = {
            "query_database": self._query_database,
            "calculate_roi": self._calculate_roi,
            "validate_hedis_spec": self._validate_hedis_spec,
            "retrieve_docs": self._retrieve_docs
        }
        
        # Audit log for all tool calls
        self.audit_log = []
    
    def execute(self, tool_name: str, params: Dict) -> Any:
        """
        Execute a tool with PHI validation and de-identification.
        
        Args:
            tool_name: Name of tool to execute
            params: Tool parameters
        
        Returns:
            Tool execution result (de-identified)
        
        Raises:
            ToolNotFoundError: If tool doesn't exist
            ToolExecutionError: If tool execution fails
        """
        # Validate tool exists
        if tool_name not in self.tools:
            raise ToolNotFoundError(f"Tool {tool_name} not found. Available: {list(self.tools.keys())}")
        
        # Log tool call start
        audit_entry = {
            "timestamp": datetime.now().isoformat(),
            "tool_name": tool_name,
            "params": self._sanitize_for_logging(params),
            "status": "started"
        }
        
        try:
            # Validate no PHI in params (Rule 1.1)
            if HAS_PHI_VALIDATOR:
                phi_validator = get_phi_validator()
                validation_result = phi_validator.validate_before_tool_call(
                    params,
                    tool_name,
                    log_violations=True
                )
                if not validation_result.is_valid:
                    raise ValueError(f"PHI detected in tool parameters. Violation types: {validation_result.violation_types}")
            else:
                # Fallback validation
                is_valid, phi_errors = self._validate_no_phi(params)
                if not is_valid:
                    raise ValueError(f"PHI detected in tool parameters: {phi_errors}")
            
            # Execute tool
            logger.info(f"Executing tool: {tool_name} with params: {self._sanitize_for_logging(params)}")
            result = self.tools[tool_name](params)
            
            # Validate result before de-identification (Rule 1.1)
            if HAS_PHI_VALIDATOR:
                phi_validator = get_phi_validator()
                validation_result = phi_validator.validate_before_result_return(
                    result,
                    log_violations=True
                )
                if not validation_result.is_valid:
                    logger.error(f"PHI detected in tool result. Violation types: {validation_result.violation_types}")
                    # De-identify and re-validate
                    result = self._de_identify_result(result)
                    validation_result = phi_validator.validate_before_result_return(
                        result,
                        log_violations=True
                    )
                    if not validation_result.is_valid:
                        raise ValueError(f"PHI detected in tool result after de-identification. Violation types: {validation_result.violation_types}")
            
            # De-identify result
            result = self._de_identify_result(result)
            
            # Final validation before return (Rule 1.1)
            if HAS_PHI_VALIDATOR:
                phi_validator = get_phi_validator()
                validation_result = phi_validator.validate_before_result_return(
                    result,
                    log_violations=True
                )
                if not validation_result.is_valid:
                    raise ValueError(f"PHI detected in result after de-identification. Violation types: {validation_result.violation_types}")
            
            # Log successful execution
            audit_entry.update({
                "status": "completed",
                "result_type": type(result).__name__,
                "result_size": self._get_result_size(result)
            })
            
            self.audit_log.append(audit_entry)
            logger.info(f"Tool {tool_name} executed successfully")
            
            return result
            
        except Exception as e:
            # Log failed execution
            audit_entry.update({
                "status": "failed",
                "error": str(e)
            })
            self.audit_log.append(audit_entry)
            
            logger.error(f"Tool {tool_name} failed: {e}")
            raise ToolExecutionError(f"Tool execution failed: {e}")
    
    def _query_database(self, params: Dict) -> pd.DataFrame:
        """
        Query database (aggregated data only, no PHI).
        
        Query types:
        - gaps: Member gaps aggregated by measure
        - performance: Measure performance metrics
        - intervention_costs: Intervention cost data
        - revenue_impact: Revenue impact calculations
        
        Args:
            params: Dictionary with:
                - query_type: "gaps" | "performance" | "intervention_costs" | "revenue_impact"
                - measure_id: Measure code (e.g., "GSD")
                - plan_id: Optional plan ID filter
                - aggregated_only: Must be True (enforced)
        
        Returns:
            DataFrame with aggregated results (no member-level data)
        """
        if not HAS_DB:
            raise ToolExecutionError("Database utilities not available")
        
        query_type = params.get("query_type", "gaps")
        measure_id = params.get("measure_id")
        plan_id = params.get("plan_id")
        
        # Enforce aggregated_only
        if not params.get("aggregated_only", False):
            logger.warning("query_database requires aggregated_only=True. Setting automatically.")
            params["aggregated_only"] = True
        
        # Build query based on type
        if query_type == "gaps":
            query = """
                SELECT 
                    measure_id,
                    COUNT(*) as gap_count,
                    AVG(predicted_success_rate) as avg_success_rate,
                    SUM(CASE WHEN risk_score > 0.7 THEN 1 ELSE 0 END) as high_risk_count
                FROM member_gaps
                WHERE measure_id = %(measure_id)s
            """
            query_params = {"measure_id": measure_id}
            
            if plan_id:
                query += " AND plan_id = %(plan_id)s"
                query_params["plan_id"] = plan_id
            
            query += " GROUP BY measure_id"
            
        elif query_type == "performance":
            query = """
                SELECT 
                    measure_id,
                    COUNT(DISTINCT member_id) as eligible_members,
                    COUNT(DISTINCT CASE WHEN is_compliant THEN member_id END) as compliant_members,
                    AVG(CASE WHEN is_compliant THEN 1.0 ELSE 0.0 END) * 100 as compliance_rate_pct
                FROM member_gaps
                WHERE measure_id = %(measure_id)s
            """
            query_params = {"measure_id": measure_id}
            
            if plan_id:
                query += " AND plan_id = %(plan_id)s"
                query_params["plan_id"] = plan_id
            
            query += " GROUP BY measure_id"
            
        elif query_type == "intervention_costs":
            query = """
                SELECT 
                    measure_id,
                    activity_type,
                    AVG(unit_cost) as avg_cost,
                    COUNT(*) as activity_count,
                    SUM(unit_cost) as total_cost
                FROM intervention_activities
                WHERE measure_id = %(measure_id)s
            """
            query_params = {"measure_id": measure_id}
            
            if plan_id:
                query += " AND plan_id = %(plan_id)s"
                query_params["plan_id"] = plan_id
            
            query += " GROUP BY measure_id, activity_type"
            
        elif query_type == "revenue_impact":
            query = """
                SELECT 
                    measure_id,
                    star_weight,
                    revenue_per_star_point,
                    COUNT(DISTINCT member_id) as members_impacted,
                    revenue_per_star_point * star_weight as potential_revenue_impact
                FROM measure_revenue_impact
                WHERE measure_id = %(measure_id)s
            """
            query_params = {"measure_id": measure_id}
            
            if plan_id:
                query += " AND plan_id = %(plan_id)s"
                query_params["plan_id"] = plan_id
            
            query += " GROUP BY measure_id, star_weight, revenue_per_star_point"
            
        else:
            raise ToolExecutionError(f"Unknown query_type: {query_type}")
        
        try:
            result = query_to_dataframe(query, query_params)
            logger.info(f"Database query returned {len(result)} rows")
            return result
        except Exception as e:
            logger.error(f"Database query failed: {e}")
            raise ToolExecutionError(f"Database query failed: {e}")
    
    def _calculate_roi(self, params: Dict) -> Dict:
        """
        Calculate ROI for interventions.
        
        Args:
            params: Dictionary with:
                - measure_id: Measure code (e.g., "GSD")
                - intervention_count: Number of interventions (or "from_step_data")
                - cost_per_intervention: Cost per intervention (or "from_step_data")
                - plan_id: Optional plan ID
        
        Returns:
            Dictionary with:
                - roi_ratio: ROI ratio (revenue / cost)
                - net_benefit: Net benefit (revenue - cost)
                - total_cost: Total intervention cost
                - total_revenue: Total revenue impact
        """
        measure_id = params.get("measure_id")
        
        # Get intervention count and cost
        intervention_count = params.get("intervention_count")
        cost_per_intervention = params.get("cost_per_intervention")
        
        # Handle "from_step_data" placeholder
        if intervention_count == "from_step_data" or intervention_count is None:
            # Try to get from previous step data or use defaults
            intervention_count = params.get("default_intervention_count", 1000)
        
        if cost_per_intervention == "from_step_data" or cost_per_intervention is None:
            # Default cost per intervention (from activity_cost_standards)
            cost_per_intervention = params.get("default_cost_per_intervention", 25.0)
        
        # Get revenue impact per star point
        # Triple-weighted measures: $360-615K, others: $120-205K
        spec = get_measure_spec(measure_id) if HAS_DB else None
        if spec and spec.weight >= 3.0:
            revenue_per_point = 500000  # Average of $360-615K
        else:
            revenue_per_point = 162500  # Average of $120-205K
        
        # Calculate star impact (simplified: assume 0.1 star improvement per 1000 interventions)
        star_impact = (intervention_count / 1000) * 0.1
        
        # Calculate costs and revenue
        total_cost = intervention_count * cost_per_intervention
        total_revenue = star_impact * revenue_per_point
        
        # Calculate ROI
        roi_ratio = total_revenue / total_cost if total_cost > 0 else 0
        net_benefit = total_revenue - total_cost
        
        return {
            "roi_ratio": round(roi_ratio, 2),
            "net_benefit": round(net_benefit, 2),
            "total_cost": round(total_cost, 2),
            "total_revenue": round(total_revenue, 2),
            "intervention_count": intervention_count,
            "cost_per_intervention": cost_per_intervention,
            "star_impact": round(star_impact, 3),
            "revenue_per_point": revenue_per_point
        }
    
    def _validate_hedis_spec(self, params: Dict) -> Dict:
        """
        Validate against HEDIS specifications.
        
        Args:
            params: Dictionary with:
                - measure_id: Measure code (e.g., "GSD")
                - data: Data to validate (dict or DataFrame)
        
        Returns:
            Dictionary with:
                - is_valid: Whether data is valid
                - errors: List of validation errors
                - warnings: List of validation warnings
        """
        measure_id = params.get("measure_id")
        data = params.get("data", {})
        
        if not HAS_DB:
            return {
                "is_valid": False,
                "errors": ["HEDIS spec validation not available"],
                "warnings": []
            }
        
        spec = get_measure_spec(measure_id)
        if not spec:
            return {
                "is_valid": False,
                "errors": [f"Measure spec not found: {measure_id}"],
                "warnings": []
            }
        
        errors = []
        warnings = []
        
        # Validate measure_id matches
        if isinstance(data, dict) and "measure_id" in data:
            if data["measure_id"] != measure_id:
                errors.append(f"Measure ID mismatch: expected {measure_id}, got {data['measure_id']}")
        
        # Validate age range if applicable
        if spec.age_min and spec.age_max:
            if isinstance(data, dict) and "age" in data:
                age = data["age"]
                if age < spec.age_min or age > spec.age_max:
                    errors.append(f"Age {age} outside valid range: {spec.age_min}-{spec.age_max}")
        
        # Validate data sources
        if isinstance(data, dict) and "data_sources" in data:
            required_sources = set(spec.data_sources)
            provided_sources = set(data["data_sources"])
            missing_sources = required_sources - provided_sources
            if missing_sources:
                warnings.append(f"Missing data sources: {missing_sources}")
        
        return {
            "is_valid": len(errors) == 0,
            "errors": errors,
            "warnings": warnings,
            "measure_id": measure_id,
            "spec_version": spec.hedis_spec_version
        }
    
    def _retrieve_docs(self, params: Dict) -> List[Dict]:
        """
        Retrieve documents using RAG retrieval.
        
        Args:
            params: Dictionary with:
                - query: Search query string
                - top_k: Number of results to return (default: 5)
                - content_type: Optional content type filter
        
        Returns:
            List of dictionaries with:
                - content: Document content
                - score: Relevance score
                - metadata: Document metadata
        """
        query = params.get("query", "")
        top_k = params.get("top_k", 5)
        content_type = params.get("content_type")
        
        if not self.rag_retriever:
            # Fallback: return empty results
            logger.warning("RAG retriever not available. Returning empty results.")
            return []
        
        try:
            results = self.rag_retriever.retrieve(query, top_k=top_k)
            
            # Format results
            formatted_results = []
            for result in results:
                formatted_results.append({
                    "content": result.get("content", str(result)),
                    "score": result.get("score", 0.0),
                    "metadata": result.get("metadata", {})
                })
            
            logger.info(f"Retrieved {len(formatted_results)} documents for query: {query[:50]}...")
            return formatted_results
            
        except Exception as e:
            logger.error(f"RAG retrieval failed: {e}")
            return []
    
    def _validate_no_phi(self, params: Dict) -> Tuple[bool, List[str]]:
        """
        Validate no PHI in parameters.
        
        Args:
            params: Parameters dictionary
        
        Returns:
            Tuple of (is_valid, list_of_errors)
        """
        errors = []
        params_str = str(params)
        
        # PHI patterns
        phi_patterns = [
            (r'\b\d{3}-\d{2}-\d{4}\b', 'SSN pattern detected'),
            (r'\b[A-Z][a-z]+\s+[A-Z][a-z]+\b', 'Potential name pattern detected'),
            (r'\b\d{1,2}/\d{1,2}/\d{4}\b', 'Potential date of birth pattern detected'),
            (r'\b\d{10,}\b', 'Potential member ID pattern detected'),
        ]
        
        for pattern, error_msg in phi_patterns:
            if re.search(pattern, params_str):
                errors.append(f"{error_msg}: {pattern}")
        
        return len(errors) == 0, errors
    
    def _de_identify_result(self, result: Any) -> Any:
        """
        De-identify result by removing any PHI.
        
        Args:
            result: Tool execution result
        
        Returns:
            De-identified result
        """
        if isinstance(result, pd.DataFrame):
            # Remove any columns that might contain PHI
            phi_columns = ['member_id', 'member_name', 'ssn', 'date_of_birth', 'phone', 'email']
            columns_to_drop = [col for col in phi_columns if col in result.columns]
            if columns_to_drop:
                logger.warning(f"Dropping potential PHI columns: {columns_to_drop}")
                result = result.drop(columns=columns_to_drop)
        
        elif isinstance(result, dict):
            # Remove PHI keys
            phi_keys = ['member_id', 'member_name', 'ssn', 'date_of_birth', 'phone', 'email']
            result = {k: v for k, v in result.items() if k not in phi_keys}
        
        return result
    
    def _sanitize_for_logging(self, data: Any) -> Any:
        """Sanitize data for audit logging (remove sensitive info)."""
        if isinstance(data, dict):
            sanitized = {}
            for key, value in data.items():
                if key.lower() in ['password', 'secret', 'token', 'api_key']:
                    sanitized[key] = "***REDACTED***"
                else:
                    sanitized[key] = self._sanitize_for_logging(value)
            return sanitized
        elif isinstance(data, list):
            return [self._sanitize_for_logging(item) for item in data]
        else:
            return data
    
    def _get_result_size(self, result: Any) -> str:
        """Get size description of result for logging."""
        if isinstance(result, pd.DataFrame):
            return f"{len(result)} rows x {len(result.columns)} columns"
        elif isinstance(result, dict):
            return f"{len(result)} keys"
        elif isinstance(result, list):
            return f"{len(result)} items"
        else:
            return "unknown"
    
    def get_audit_log(self) -> List[Dict]:
        """Get audit log of all tool calls."""
        return self.audit_log.copy()


class ContextAccumulator:
    """
    Accumulate context across agentic steps.
    
    Based on Rule 2.4 from AGENTIC_RAG_RULES.md
    """
    
    def __init__(self):
        """Initialize context accumulator."""
        self.context = {
            "retrieved_docs": [],
            "query_results": [],
            "calculations": [],
            "validations": []
        }
    
    def add_step_result(self, step_type: str, result: Any):
        """
        Add result from a step.
        
        Args:
            step_type: Type of step result ("retrieved_docs", "query_results", "calculations", "validations")
            result: Result to add
        """
        if step_type in self.context:
            self.context[step_type].append(result)
        else:
            logger.warning(f"Unknown step type: {step_type}. Adding to context anyway.")
            if step_type not in self.context:
                self.context[step_type] = []
            self.context[step_type].append(result)
    
    def get_full_context(self) -> Dict:
        """
        Get accumulated context for final synthesis.
        
        Returns:
            Dictionary with all accumulated context
        """
        return self.context.copy()
    
    def reset(self):
        """Reset accumulator for new query."""
        self.context = {
            "retrieved_docs": [],
            "query_results": [],
            "calculations": [],
            "validations": []
        }


class ResponseSynthesizer:
    """
    Synthesize final response from accumulated context.
    
    Based on Template 4 from AGENTIC_RAG_RULES.md
    """
    
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
{{
    "summary": "executive summary",
    "recommendations": ["rec1", "rec2"],
    "metrics": {{}},
    "data_sources": ["source1", "source2"]
}}
"""
    
    def __init__(self, use_llm: bool = False, llm_client=None):
        """
        Initialize ResponseSynthesizer.
        
        Args:
            use_llm: If True, use LLM for synthesis. If False, use rule-based.
            llm_client: Optional LLM client for synthesis
        """
        self.use_llm = use_llm
        self.llm_client = llm_client
    
    def generate(self, query: str, context: Dict) -> Dict:
        """
        Generate synthesized response.
        
        Args:
            query: Original user query
            context: Accumulated context from steps
        
        Returns:
            Dictionary with synthesized response
        """
        if self.use_llm and self.llm_client:
            return self._generate_with_llm(query, context)
        else:
            return self._generate_rule_based(query, context)
    
    def _generate_with_llm(self, query: str, context: Dict) -> Dict:
        """Generate response using LLM."""
        prompt = self.SYNTHESIS_PROMPT.format(
            query=query,
            accumulated_context=json.dumps(context, indent=2, default=str)
        )
        
        try:
            response = self.llm_client.generate(prompt)
            result = json.loads(response)
            return result
        except json.JSONDecodeError:
            logger.warning("LLM response not valid JSON. Using rule-based synthesis.")
            return self._generate_rule_based(query, context)
        except Exception as e:
            logger.error(f"LLM synthesis failed: {e}. Using rule-based synthesis.")
            return self._generate_rule_based(query, context)
    
    def _generate_rule_based(self, query: str, context: Dict) -> Dict:
        """Generate response using rule-based synthesis."""
        summary_parts = []
        recommendations = []
        metrics = {}
        data_sources = []
        
        # Extract information from context
        if context.get("retrieved_docs"):
            summary_parts.append(f"Retrieved {len(context['retrieved_docs'])} relevant documents")
            data_sources.append("HEDIS documentation")
        
        if context.get("query_results"):
            query_results = context["query_results"]
            for result in query_results:
                if isinstance(result, pd.DataFrame) and len(result) > 0:
                    summary_parts.append(f"Found {len(result)} aggregated results")
                    # Extract key metrics
                    for col in result.columns:
                        if 'count' in col.lower() or 'rate' in col.lower():
                            metrics[col] = result[col].iloc[0] if len(result) > 0 else None
            data_sources.append("Database queries")
        
        if context.get("calculations"):
            calculations = context["calculations"]
            for calc in calculations:
                if isinstance(calc, dict):
                    if "roi_ratio" in calc:
                        metrics["roi_ratio"] = calc["roi_ratio"]
                        metrics["net_benefit"] = calc.get("net_benefit", 0)
                        summary_parts.append(f"ROI: {calc['roi_ratio']:.2f}x, Net Benefit: ${calc.get('net_benefit', 0):,.2f}")
                    if "total_cost" in calc:
                        metrics["total_cost"] = calc["total_cost"]
                        metrics["total_revenue"] = calc.get("total_revenue", 0)
        
        if context.get("validations"):
            validations = context["validations"]
            for val in validations:
                if isinstance(val, dict) and val.get("is_valid"):
                    summary_parts.append("Validation passed against HEDIS specifications")
                elif isinstance(val, dict):
                    recommendations.append("Review validation errors and correct data")
        
        # Generate recommendations based on context
        if metrics.get("roi_ratio", 0) > 1.5:
            recommendations.append("High ROI detected. Consider scaling interventions.")
        elif metrics.get("roi_ratio", 0) < 1.0:
            recommendations.append("ROI below break-even. Review intervention costs.")
        
        if not recommendations:
            recommendations.append("Continue monitoring measure performance")
        
        summary = ". ".join(summary_parts) if summary_parts else "Query processed successfully."
        
        return {
            "summary": summary,
            "recommendations": recommendations,
            "metrics": metrics,
            "data_sources": data_sources if data_sources else ["Agentic RAG processing"]
        }


class ResultValidator:
    """
    Validate agentic RAG results and step results.
    
    Based on Template 5 and Rule 2.3 from AGENTIC_RAG_RULES.md
    """
    
    def __init__(self):
        """Initialize validator with metrics tracking."""
        self.validation_metrics = {
            "total_validations": 0,
            "passed_validations": 0,
            "failed_validations": 0,
            "phi_detections": 0,
            "completeness_failures": 0,
            "accuracy_failures": 0,
            "format_failures": 0
        }
    
    def validate(self, result: Dict) -> bool:
        """
        Validate result quality.
        
        Args:
            result: Result dictionary to validate
        
        Returns:
            True if valid, False otherwise
        """
        self.validation_metrics["total_validations"] += 1
        
        checks = {
            "no_phi": self._check_no_phi(result),
            "completeness": self._check_completeness(result),
            "accuracy": self._check_accuracy(result),
            "format": self._check_format(result)
        }
        
        # Track failures
        if not checks["no_phi"]:
            self.validation_metrics["phi_detections"] += 1
        if not checks["completeness"]:
            self.validation_metrics["completeness_failures"] += 1
        if not checks["accuracy"]:
            self.validation_metrics["accuracy_failures"] += 1
        if not checks["format"]:
            self.validation_metrics["format_failures"] += 1
        
        is_valid = all(checks.values())
        
        if is_valid:
            self.validation_metrics["passed_validations"] += 1
        else:
            self.validation_metrics["failed_validations"] += 1
            logger.warning(f"Validation failed. Checks: {checks}")
        
        return is_valid
    
    def validate_step_result(self, step_type: str, step_id: str, result: Any) -> Tuple[bool, List[str]]:
        """
        Validate individual step result.
        
        Args:
            step_type: Type of step (retrieve, query_db, calculate, validate)
            step_id: Step identifier
            result: Step result to validate
        
        Returns:
            Tuple of (is_valid, list_of_errors)
        """
        errors = []
        
        # Check for PHI
        if isinstance(result, (dict, list, pd.DataFrame)):
            result_str = str(result)
            if not self._check_no_phi({"data": result_str}):
                errors.append("PHI detected in step result")
        
        # Type-specific validation
        if step_type == "query_db":
            if isinstance(result, pd.DataFrame):
                if len(result) == 0:
                    errors.append("Query returned no results")
                # Check for PHI columns
                phi_columns = ['member_id', 'member_name', 'ssn', 'date_of_birth']
                found_phi_cols = [col for col in phi_columns if col in result.columns]
                if found_phi_cols:
                    errors.append(f"PHI columns found: {found_phi_cols}")
        
        elif step_type == "calculate":
            if isinstance(result, dict):
                if "roi_ratio" in result:
                    if result["roi_ratio"] < 0:
                        errors.append("Negative ROI ratio")
                    if result["roi_ratio"] > 1000:  # Unrealistic ROI
                        errors.append(f"Unrealistic ROI ratio: {result['roi_ratio']}")
        
        elif step_type == "retrieve":
            if isinstance(result, list):
                if len(result) == 0:
                    errors.append("No documents retrieved")
                # Check relevance scores
                for doc in result:
                    if isinstance(doc, dict) and "score" in doc:
                        if doc["score"] < 0.3:  # Low relevance
                            errors.append(f"Low relevance score: {doc['score']}")
                            break
        
        is_valid = len(errors) == 0
        
        if not is_valid:
            logger.warning(f"Step {step_id} ({step_type}) validation failed: {errors}")
        
        return is_valid, errors
    
    def get_validation_pass_rate(self) -> float:
        """Get validation pass rate."""
        if self.validation_metrics["total_validations"] == 0:
            return 1.0
        return self.validation_metrics["passed_validations"] / self.validation_metrics["total_validations"]
    
    def get_metrics(self) -> Dict:
        """Get validation metrics."""
        return {
            **self.validation_metrics,
            "validation_pass_rate": self.get_validation_pass_rate()
        }
    
    def _check_no_phi(self, result: Dict) -> bool:
        """Check no PHI in result."""
        result_str = str(result)
        phi_patterns = [
            (r'\b\d{3}-\d{2}-\d{4}\b', 'SSN pattern'),  # SSN
            (r'\b[A-Z][a-z]+\s+[A-Z][a-z]+\s+[A-Z][a-z]+\b', 'Full name pattern'),  # Full names (3+ words)
            (r'\b\d{1,2}/\d{1,2}/\d{4}\b', 'DOB pattern'),  # Date of birth
        ]
        
        # Common false positives to ignore
        false_positives = [
            'Retrieved Docs', 'Query Results', 'Calculations', 'Validations',
            'Net Benefit', 'Total Cost', 'Total Revenue', 'Star Impact'
        ]
        
        for pattern, description in phi_patterns:
            matches = re.findall(pattern, result_str)
            # Filter out false positives
            real_matches = [m for m in matches if not any(fp.lower() in str(m).lower() for fp in false_positives)]
            if real_matches:
                logger.warning(f"PHI pattern detected in result: {description} - {real_matches[:3]}")
                return False
        
        return True
    
    def _check_completeness(self, result: Dict) -> bool:
        """Check result is complete."""
        required_fields = ["summary", "recommendations"]
        missing_fields = [field for field in required_fields if field not in result]
        
        if missing_fields:
            logger.warning(f"Result missing required fields: {missing_fields}")
            return False
        
        return True
    
    def _check_accuracy(self, result: Dict) -> bool:
        """Check result accuracy (basic checks)."""
        # Check metrics are numeric
        if "metrics" in result:
            for key, value in result["metrics"].items():
                if isinstance(value, (int, float)):
                    if value < 0 and key not in ["trend", "variance"]:
                        logger.warning(f"Negative metric value: {key} = {value}")
                        return False
        
        return True
    
    def _check_format(self, result: Dict) -> bool:
        """Check result format."""
        # Check recommendations is list
        if "recommendations" in result:
            if not isinstance(result["recommendations"], list):
                logger.warning("Recommendations must be a list")
                return False
        
        return True


class HEDISAgenticRAG:
    """
    Agentic RAG agent for HEDIS queries.
    
    Based on Template 1 and Rule 2.3 from AGENTIC_RAG_RULES.md
    
    Orchestrates:
    1. Planning with PlanningAgent
    2. Tool execution with ToolExecutor
    3. Context accumulation
    4. Response synthesis
    5. Validation and retry with self-correction
    """
    
    def __init__(self, rag_retriever=None, use_llm: bool = False, llm_client=None):
        """
        Initialize HEDISAgenticRAG.
        
        Args:
            rag_retriever: Optional RAG retriever for document retrieval
            use_llm: If True, use LLM for planning/synthesis
            llm_client: Optional LLM client
        """
        self.rag_retriever = rag_retriever
        self.tool_executor = ToolExecutor(rag_retriever=rag_retriever)
        self.plan_agent = PlanningAgent(use_llm=use_llm, llm_client=llm_client)
        self.synthesizer = ResponseSynthesizer(use_llm=use_llm, llm_client=llm_client)
        self.validator = ResultValidator()
        self.context_accumulator = ContextAccumulator()
        self.max_steps = 10
        self.max_retries = 3
        
        # Metrics tracking
        self.metrics = {
            "total_queries": 0,
            "total_steps": 0,
            "successful_steps": 0,
            "failed_steps": 0,
            "total_retries": 0,
            "queries_with_retries": 0,
            "fallback_operations": 0
        }
    
    def process_query(self, query: str, max_retries: Optional[int] = None) -> Dict:
        """
        Process query using agentic RAG.
        
        Steps:
        1. Plan decomposition
        2. Execute steps with tools
        3. Accumulate context
        4. Synthesize response
        5. Validate and retry if needed
        
        Args:
            query: User query string
            max_retries: Maximum retry attempts (default: 3)
        
        Returns:
            Dictionary with:
                - response: Synthesized response
                - steps_executed: Number of steps executed
                - context_used: Accumulated context
        """
        if max_retries is None:
            max_retries = self.max_retries
        
        # Track query (only increment once, not on retries)
        original_query = query
        is_first_attempt = True
        
        retry_count = 0
        
        while retry_count <= max_retries:
            # Increment query counter only on first attempt
            if is_first_attempt:
                self.metrics["total_queries"] += 1
                is_first_attempt = False
            try:
                # Reset context accumulator
                self.context_accumulator.reset()
                
                # Step 1: Plan
                logger.info(f"Planning query: {query}")
                plan = self.plan_agent.decompose(query)
                
                # Check step limit
                if len(plan["steps"]) > self.max_steps:
                    logger.warning(
                        f"Plan has {len(plan['steps'])} steps, exceeding limit of {self.max_steps}. "
                        f"Truncating to first {self.max_steps} steps."
                    )
                    plan["steps"] = plan["steps"][:self.max_steps]
                
                # Step 2: Execute steps with validation
                executed_steps = []
                step_failures = []
                
                for step in plan["steps"]:
                    # Skip synthesize step (handled separately)
                    if step["type"] == "synthesize":
                        continue
                    
                    self.metrics["total_steps"] += 1
                    logger.info(f"Executing step: {step['id']} ({step['type']})")
                    
                    try:
                        result = None
                        
                        if step["type"] == "retrieve":
                            result = self.tool_executor.execute("retrieve_docs", {
                                "query": step.get("query", ""),
                                "top_k": step.get("params", {}).get("top_k", 5),
                                "content_type": step.get("params", {}).get("content_type")
                            })
                            self.context_accumulator.add_step_result("retrieved_docs", result)
                        
                        elif step["type"] == "query_db":
                            result = self.tool_executor.execute("query_database", step.get("params", {}))
                            self.context_accumulator.add_step_result("query_results", result)
                        
                        elif step["type"] == "calculate":
                            operation = step.get("params", {}).get("operation", "roi")
                            if operation == "roi":
                                result = self.tool_executor.execute("calculate_roi", step.get("params", {}))
                            else:
                                # Generic calculation
                                result = self.tool_executor.execute("calculate_roi", step.get("params", {}))
                            self.context_accumulator.add_step_result("calculations", result)
                        
                        elif step["type"] == "validate":
                            result = self.tool_executor.execute("validate_hedis_spec", step.get("params", {}))
                            self.context_accumulator.add_step_result("validations", result)
                        
                        # Validate step result
                        is_valid, errors = self.validator.validate_step_result(
                            step["type"], 
                            step["id"], 
                            result
                        )
                        
                        if is_valid:
                            self.metrics["successful_steps"] += 1
                            executed_steps.append(step["id"])
                        else:
                            self.metrics["failed_steps"] += 1
                            step_failures.append({
                                "step_id": step["id"],
                                "step_type": step["type"],
                                "errors": errors
                            })
                            logger.warning(
                                f"Step {step['id']} validation failed: {errors}. "
                                "Continuing with other steps."
                            )
                            # Still add result to context (may be useful)
                            executed_steps.append(step["id"])
                        
                    except (ToolExecutionError, ToolNotFoundError) as e:
                        self.metrics["failed_steps"] += 1
                        step_failures.append({
                            "step_id": step["id"],
                            "step_type": step["type"],
                            "errors": [str(e)]
                        })
                        logger.error(f"Step {step['id']} execution failed: {e}")
                        # Try fallback operation
                        fallback_result = self._fallback_operation(step)
                        if fallback_result:
                            self.metrics["fallback_operations"] += 1
                            logger.info(f"Fallback operation succeeded for step {step['id']}")
                            executed_steps.append(step["id"])
                        else:
                            logger.warning(f"No fallback available for step {step['id']}. Skipping.")
                            continue
                
                # Step 3: Synthesize
                full_context = self.context_accumulator.get_full_context()
                logger.info("Synthesizing response from accumulated context")
                response = self.synthesizer.generate(query, full_context)
                
                # Step 4: Validate final response
                if self.validator.validate(response):
                    logger.info("Response validation passed")
                    
                    # Update metrics
                    if retry_count > 0:
                        self.metrics["queries_with_retries"] += 1
                    self.metrics["total_retries"] += retry_count
                    
                    return {
                        "response": response,
                        "steps_executed": len(executed_steps),
                        "context_used": full_context,
                        "retry_count": retry_count,
                        "step_failures": step_failures,
                        "metrics": self._get_metrics()
                    }
                else:
                    logger.warning("Response validation failed. Refining query and retrying...")
                    retry_count += 1
                    self.metrics["total_retries"] += 1
                    
                    if retry_count <= max_retries:
                        # Refine query based on validation errors
                        query = self._refine_query(query, response, step_failures)
                        logger.info(f"Refined query (attempt {retry_count + 1}): {query[:100]}...")
                        continue
                    else:
                        logger.error("Max retries exceeded. Using fallback response.")
                        self.metrics["fallback_operations"] += 1
                        fallback_response = self._fallback_response(original_query, full_context)
                        return {
                            "response": fallback_response,
                            "steps_executed": len(executed_steps),
                            "context_used": full_context,
                            "retry_count": retry_count,
                            "step_failures": step_failures,
                            "validation_warning": "Response did not pass validation, using fallback",
                            "metrics": self._get_metrics()
                        }
            
            except PlanningError as e:
                logger.error(f"Planning failed: {e}")
                if retry_count < max_retries:
                    retry_count += 1
                    query = self._refine_query(query, {}, [])
                    continue
                else:
                    raise
            except Exception as e:
                logger.error(f"Unexpected error in process_query: {e}")
                if retry_count < max_retries:
                    retry_count += 1
                    query = self._refine_query(query, {}, [])
                    logger.info(f"Retrying (attempt {retry_count}/{max_retries})...")
                    continue
                else:
                    # Fallback to simple response
                    fallback_response = self._fallback_response(original_query, {})
                    return {
                        "response": fallback_response,
                        "steps_executed": 0,
                        "context_used": {},
                        "retry_count": retry_count,
                        "error": str(e),
                        "metrics": self._get_metrics()
                    }
    
    def _refine_query(self, query: str, response: Dict, step_failures: List[Dict]) -> str:
        """
        Refine query based on validation errors and step failures.
        
        Based on Rule 2.3: refine query on failure.
        
        Args:
            query: Original query
            response: Failed response (if any)
            step_failures: List of step failures
        
        Returns:
            Refined query string
        """
        refined = query
        
        # Simplify query if too complex
        if len(step_failures) > 2:
            # Remove complex operations
            refined = refined.replace("prioritize by risk", "")
            refined = refined.replace("validate", "")
            refined = refined.replace("and", ",")
            logger.info("Simplified query due to multiple step failures")
        
        # Add error context if available
        if step_failures:
            error_types = [f["step_type"] for f in step_failures]
            if "query_db" in error_types:
                refined = refined.replace("query database", "retrieve information")
                logger.info("Replaced database query with retrieval due to failures")
        
        # Clean up query
        refined = " ".join(refined.split())  # Remove extra whitespace
        
        return refined if refined.strip() else query
    
    def _fallback_operation(self, step: Dict) -> Optional[Any]:
        """
        Fallback to simpler operation if step fails.
        
        Args:
            step: Failed step
        
        Returns:
            Fallback result or None
        """
        step_type = step.get("type")
        
        if step_type == "query_db":
            # Fallback: Use retrieve instead of query_db
            logger.info(f"Falling back to retrieve_docs for step {step['id']}")
            try:
                return self.tool_executor.execute("retrieve_docs", {
                    "query": step.get("query", ""),
                    "top_k": 3
                })
            except Exception:
                return None
        
        elif step_type == "calculate":
            # Fallback: Return default values
            logger.info(f"Falling back to default calculation for step {step['id']}")
            return {
                "roi_ratio": 1.0,
                "net_benefit": 0,
                "total_cost": 0,
                "total_revenue": 0,
                "fallback": True
            }
        
        return None
    
    def _fallback_response(self, query: str, context: Dict) -> Dict:
        """
        Generate fallback response when max retries exceeded.
        
        Args:
            query: Original query
            context: Accumulated context
        
        Returns:
            Fallback response dictionary
        """
        return {
            "summary": f"Unable to fully process query: {query}. Please try simplifying your request.",
            "recommendations": [
                "Try breaking down complex queries into simpler parts",
                "Ensure database is available for data queries",
                "Check that measure IDs are valid"
            ],
            "metrics": {},
            "data_sources": ["Fallback response"],
            "fallback": True
        }
    
    def _get_metrics(self) -> Dict:
        """Get performance metrics."""
        total_steps = self.metrics["total_steps"]
        step_success_rate = (
            self.metrics["successful_steps"] / total_steps 
            if total_steps > 0 else 1.0
        )
        
        total_queries = self.metrics["total_queries"]
        retry_rate = (
            self.metrics["queries_with_retries"] / total_queries 
            if total_queries > 0 else 0.0
        )
        
        validation_pass_rate = self.validator.get_validation_pass_rate()
        
        return {
            "step_success_rate": round(step_success_rate, 3),
            "retry_rate": round(retry_rate, 3),
            "validation_pass_rate": round(validation_pass_rate, 3),
            "total_queries": self.metrics["total_queries"],
            "total_steps": self.metrics["total_steps"],
            "successful_steps": self.metrics["successful_steps"],
            "failed_steps": self.metrics["failed_steps"],
            "total_retries": self.metrics["total_retries"],
            "queries_with_retries": self.metrics["queries_with_retries"],
            "fallback_operations": self.metrics["fallback_operations"],
            "validator_metrics": self.validator.get_metrics()
        }
    
    def reset_metrics(self):
        """Reset metrics (useful for testing)."""
        self.metrics = {
            "total_queries": 0,
            "total_steps": 0,
            "successful_steps": 0,
            "failed_steps": 0,
            "total_retries": 0,
            "queries_with_retries": 0,
            "fallback_operations": 0
        }
        self.validator.validation_metrics = {
            "total_validations": 0,
            "passed_validations": 0,
            "failed_validations": 0,
            "phi_detections": 0,
            "completeness_failures": 0,
            "accuracy_failures": 0,
            "format_failures": 0
        }


# Example usage and testing
if __name__ == "__main__":
    # Set up logging
    logging.basicConfig(level=logging.INFO)
    
    # Create planning agent
    agent = PlanningAgent(use_llm=False)
    
    # Test query
    test_query = "Find gaps in HbA1c testing, calculate ROI, prioritize by risk"
    
    print("=" * 80)
    print("Planning Agent Test")
    print("=" * 80)
    print(f"Query: {test_query}")
    print()
    
    try:
        plan = agent.decompose(test_query)
        
        print("Generated Plan:")
        print(json.dumps(plan, indent=2))
        print()
        
        print("Plan Summary:")
        for i, step in enumerate(plan["steps"], 1):
            print(f"  {i}. {step['type']}: {step.get('query', 'N/A')}")
            if step.get('depends_on'):
                print(f"     Depends on: {', '.join(step['depends_on'])}")
        
        print()
        print("[SUCCESS] Plan generated and validated successfully!")
        
    except PlanningError as e:
        print(f"[ERROR] Planning failed: {e}")
    except Exception as e:
        print(f"[ERROR] Unexpected error: {e}")
        import traceback
        traceback.print_exc()


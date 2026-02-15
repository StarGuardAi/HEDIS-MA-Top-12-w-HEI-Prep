"""
Joint Context Engineering + Agentic RAG
Combines hierarchical context building with agentic RAG for maximum capability

Based on Template 1 from JOINT_CONTEXT_AGENTIC_RULES.md
"""
import json
import logging
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime
from dataclasses import dataclass, field
from enum import Enum
import sys
import os

# Add project root to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from services.context_engine import (
    HierarchicalContextBuilder,
    compress_context,
    estimate_tokens
)

try:
    from services.security.phi_validator import get_phi_validator
    HAS_PHI_VALIDATOR = True
except ImportError:
    HAS_PHI_VALIDATOR = False
    logger.warning("PHI validator not available. Using fallback validation.")
from services.agentic_rag import (
    HEDISAgenticRAG,
    PlanningAgent,
    ToolExecutor,
    ContextAccumulator,
    ResponseSynthesizer,
    ResultValidator,
    PlanningError,
    ToolExecutionError
)

try:
    from services.audit_logger import JointAuditLogger
    HAS_AUDIT_LOGGER = True
except ImportError:
    # Fallback to in-memory version
    HAS_AUDIT_LOGGER = False

logger = logging.getLogger(__name__)


class ToolType(Enum):
    """Available tools for agentic execution"""
    RETRIEVE = "retrieve"
    QUERY_DB = "query_db"
    CALCULATE = "calculate"
    VALIDATE = "validate"
    SYNTHESIZE = "synthesize"


@dataclass
class ToolSelection:
    """Result of tool selection process with confidence scoring"""
    tool_type: ToolType
    confidence: float
    reasoning: str
    context_indicators: List[str] = field(default_factory=list)
    params: Dict[str, Any] = field(default_factory=dict)


class QueryParser:
    """Parse query to extract intent and requirements."""
    
    def parse_intent(self, query: str) -> Dict[str, Any]:
        """
        Parse query intent.
        
        Returns:
            Dict with:
            - keywords: List of important keywords
            - measures: List of measure IDs mentioned
            - needs_calculation: bool
            - needs_data: bool
            - measure_specific: bool
            - high_stakes: bool
        """
        query_lower = query.lower()
        
        # Extract measure IDs
        measures = self._extract_measures(query)
        
        # Check for calculation needs
        calc_keywords = ["roi", "calculate", "compute", "impact", "revenue", "cost", "savings", "benefit"]
        needs_calculation = any(kw in query_lower for kw in calc_keywords)
        
        # Check for data needs
        data_keywords = ["member", "gap", "performance", "rate", "score", "count"]
        needs_data = any(kw in query_lower for kw in data_keywords)
        
        # Check if measure-specific
        measure_specific = len(measures) > 0
        
        # Check if high-stakes
        high_stakes = "roi" in query_lower or "compliance" in query_lower or "validate" in query_lower
        
        # Check if clinical guidelines needed
        needs_clinical_guidelines = "guideline" in query_lower or "clinical" in query_lower
        
        return {
            "keywords": query_lower.split(),
            "measures": measures,
            "needs_calculation": needs_calculation,
            "needs_data": needs_data,
            "measure_specific": measure_specific,
            "high_stakes": high_stakes,
            "needs_clinical_guidelines": needs_clinical_guidelines
        }
    
    def _extract_measures(self, query: str) -> List[str]:
        """Extract HEDIS measure IDs from query."""
        measure_patterns = [
            "CDC", "EED", "GSD", "HBD", "KED",  # Diabetes measures
            "CBP", "BPD",  # Blood pressure
            "COL", "SPC",  # Colorectal, statin
            "BCS", "CCS"   # Breast cancer, cervical cancer
        ]
        
        query_upper = query.upper()
        measures = [m for m in measure_patterns if m in query_upper]
        
        # Also check for explicit mentions
        if "diabetes" in query.lower() or "hba1c" in query.lower() or "a1c" in query.lower():
            measures.extend(["CDC", "EED", "GSD"])
        if "blood pressure" in query.lower() or "hypertension" in query.lower() or "bp" in query.lower():
            measures.extend(["CBP", "BPD"])
        if "eye" in query.lower() or "retinal" in query.lower():
            measures.append("EED")
        if "kidney" in query.lower() or "egfr" in query.lower() or "acr" in query.lower():
            measures.append("KED")
        
        # Remove duplicates
        return list(set(measures))


class ContextAnalyzer:
    """Analyze context to identify information gaps."""
    
    def identify_gaps(self, context: Dict, intent: Dict) -> List[str]:
        """
        Identify what's missing from context.
        
        Returns:
            List of gap types (e.g., "domain_knowledge", "measure_data")
        """
        gaps = []
        
        # Check domain knowledge
        if not context.get("layer_1_domain") or not context.get("layer_1_domain", {}).get("hedis_overview"):
            gaps.append("domain_knowledge")
        
        # Check measure context
        if intent.get("measure_specific", False):
            measures = intent.get("measures", [])
            measure_context = context.get("layer_2_measure", {})
            
            for measure in measures:
                if measure not in measure_context:
                    gaps.append(f"measure_specs_{measure}")
        
        # Check query results
        if intent.get("needs_data", False):
            query_results = context.get("layer_3_query", {}).get("query_results", [])
            if not query_results:
                gaps.append("member_data")
        
        return gaps


class ContextDrivenToolSelector:
    """
    Intelligently select tools based on context analysis.
    
    Selection Logic:
    - Analyze query intent and requirements
    - Check what's already available in context
    - Determine minimal tool set needed
    - Prioritize tools by confidence score
    """
    
    def __init__(self):
        self.context_analyzer = ContextAnalyzer()
        self.query_parser = QueryParser()
        self.selection_history = []
    
    def select_tools(
        self, 
        query: str, 
        context: Dict[str, Any]
    ) -> List[ToolSelection]:
        """
        Select tools based on query and available context.
        
        Args:
            query: User query
            context: Current context (hierarchical layers)
            
        Returns:
            List of ToolSelection objects with confidence scores
        """
        logger.info(f"Selecting tools for query: {query[:100]}...")
        
        # Step 1: Analyze query intent
        intent = self.query_parser.parse_intent(query)
        logger.debug(f"Query intent: {intent}")
        
        # Step 2: Analyze context gaps
        context_gaps = self.context_analyzer.identify_gaps(context, intent)
        logger.debug(f"Context gaps: {context_gaps}")
        
        # Step 3: Select tools to fill gaps
        tool_selections = []
        
        # Check for retrieval need
        if self._needs_retrieval(context, intent):
            tool_selections.append(
                self._create_retrieval_selection(query, context, intent)
            )
        
        # Check for database query need
        if self._needs_database_query(context, intent):
            tool_selections.append(
                self._create_database_selection(query, context, intent)
            )
        
        # Check for calculation need
        if self._needs_calculation(query, context, intent):
            tool_selections.append(
                self._create_calculation_selection(query, context, intent)
            )
        
        # Check for validation need
        if self._needs_validation(query, context, intent):
            tool_selections.append(
                self._create_validation_selection(query, context, intent)
            )
        
        # Step 4: Sort by confidence and dependencies
        tool_selections = self._sort_and_validate_selections(tool_selections)
        
        # Step 5: Log selection
        self._log_selection(query, context, tool_selections)
        
        logger.info(f"Selected {len(tool_selections)} tools: {[s.tool_type.value for s in tool_selections]}")
        return tool_selections
    
    def _needs_retrieval(self, context: Dict, intent: Dict) -> bool:
        """Determine if retrieval is needed."""
        domain_knowledge = context.get("layer_1_domain", {})
        
        if not domain_knowledge or not domain_knowledge.get("hedis_overview"):
            logger.debug("Domain knowledge missing - retrieval needed")
            return True
        
        # Check if measure specifications needed
        if intent.get("measure_specific", False):
            measures = intent.get("measures", [])
            measure_context = context.get("layer_2_measure", {})
            
            for measure in measures:
                if measure not in measure_context:
                    logger.debug(f"Measure {measure} specs missing - retrieval needed")
                    return True
        
        # Check if clinical guidelines needed
        if intent.get("needs_clinical_guidelines", False):
            if "clinical_guidelines" not in domain_knowledge:
                logger.debug("Clinical guidelines missing - retrieval needed")
                return True
        
        return False
    
    def _needs_database_query(self, context: Dict, intent: Dict) -> bool:
        """Determine if database query is needed."""
        member_keywords = ["member", "gap", "performance", "rate", "score", "count"]
        if any(kw in intent.get("keywords", []) for kw in member_keywords):
            logger.debug("Member data keywords detected - database query needed")
            return True
        
        # Check if measure data needed
        if intent.get("measure_specific", False):
            query_results = context.get("layer_3_query", {}).get("query_results", [])
            if not query_results:
                logger.debug("Measure data needed - database query needed")
                return True
        
        # Check if calculations require data
        if intent.get("needs_calculation", False):
            if not context.get("layer_3_query", {}).get("intervention_data"):
                logger.debug("Calculation requires data - database query needed")
                return True
        
        return False
    
    def _needs_calculation(self, query: str, context: Dict, intent: Dict) -> bool:
        """Determine if calculation is needed."""
        calculation_keywords = [
            "roi", "return", "benefit", "cost", "savings",
            "calculate", "compute", "determine", "estimate",
            "impact", "revenue", "value"
        ]
        
        query_lower = query.lower()
        has_calc_keyword = any(kw in query_lower for kw in calculation_keywords)
        
        if has_calc_keyword:
            logger.debug("Calculation keywords detected - calculation needed")
            return True
        
        if intent.get("needs_calculation", False):
            logger.debug("Intent suggests calculation - calculation needed")
            return True
        
        return False
    
    def _needs_validation(self, query: str, context: Dict, intent: Dict) -> bool:
        """Determine if validation is needed."""
        validation_keywords = [
            "validate", "verify", "check", "compliance", "compliant",
            "hedis", "specification", "spec", "cms", "ncqa", "regulation"
        ]
        
        query_lower = query.lower()
        has_validation_keyword = any(kw in query_lower for kw in validation_keywords)
        
        if has_validation_keyword:
            logger.debug("Validation keywords detected - validation needed")
            return True
        
        # Check if high-stakes calculation
        if intent.get("needs_calculation", False) and intent.get("high_stakes", False):
            logger.debug("High-stakes calculation - validation recommended")
            return True
        
        return False
    
    def _create_retrieval_selection(
        self, 
        query: str, 
        context: Dict, 
        intent: Dict
    ) -> ToolSelection:
        """Create retrieval tool selection with parameters."""
        retrieval_targets = []
        
        if not context.get("layer_1_domain", {}):
            retrieval_targets.append("HEDIS domain knowledge")
        
        if intent.get("measure_specific", False):
            measures = intent.get("measures", [])
            for measure in measures:
                if measure not in context.get("layer_2_measure", {}):
                    retrieval_targets.append(f"HEDIS {measure} specifications")
        
        if intent.get("needs_clinical_guidelines", False):
            retrieval_targets.append("clinical guidelines")
        
        retrieval_query = " AND ".join(retrieval_targets) if retrieval_targets else query
        
        return ToolSelection(
            tool_type=ToolType.RETRIEVE,
            confidence=0.90,
            reasoning=f"Need to retrieve: {', '.join(retrieval_targets) if retrieval_targets else 'domain knowledge'}",
            context_indicators=["missing_domain_knowledge", "measure_specs_needed"],
            params={
                "query": retrieval_query,
                "top_k": 5,
                "min_relevance": 0.7
            }
        )
    
    def _create_database_selection(
        self,
        query: str,
        context: Dict,
        intent: Dict
    ) -> ToolSelection:
        """Create database query tool selection with parameters."""
        query_type = "gaps"  # default
        
        query_lower = query.lower()
        if "performance" in query_lower or "rate" in query_lower:
            query_type = "performance"
        elif "member" in query_lower or "gap" in query_lower:
            query_type = "gaps"
        elif "roi" in query_lower or "cost" in query_lower:
            query_type = "intervention_costs"
        
        # Get measure IDs from intent
        measure_ids = intent.get("measures", [])
        
        return ToolSelection(
            tool_type=ToolType.QUERY_DB,
            confidence=0.85,
            reasoning=f"Need {query_type} data for {measure_ids if measure_ids else 'measures'}",
            context_indicators=["member_data_needed", "measure_specific"],
            params={
                "query_type": query_type,
                "measure_ids": measure_ids,
                "aggregation": "summary"  # Always aggregated for HIPAA
            }
        )
    
    def _create_calculation_selection(
        self,
        query: str,
        context: Dict,
        intent: Dict
    ) -> ToolSelection:
        """Create calculation tool selection with parameters."""
        calc_type = "roi"  # default
        
        query_lower = query.lower()
        if "roi" in query_lower or "return" in query_lower:
            calc_type = "roi"
        elif "impact" in query_lower or "revenue" in query_lower:
            calc_type = "revenue_impact"
        elif "cost" in query_lower or "savings" in query_lower:
            calc_type = "cost_analysis"
        
        # Get measure IDs
        measure_ids = intent.get("measures", [])
        
        return ToolSelection(
            tool_type=ToolType.CALCULATE,
            confidence=0.95,
            reasoning=f"Need to calculate {calc_type} for {measure_ids if measure_ids else 'measures'}",
            context_indicators=["calculation_required", "roi_keywords"],
            params={
                "operation": calc_type,
                "measure_ids": measure_ids,
                "include_confidence_intervals": True
            }
        )
    
    def _create_validation_selection(
        self,
        query: str,
        context: Dict,
        intent: Dict
    ) -> ToolSelection:
        """Create validation tool selection with parameters."""
        validation_targets = []
        
        if intent.get("needs_calculation", False):
            validation_targets.append("calculation_results")
        
        if intent.get("measure_specific", False):
            validation_targets.append("hedis_compliance")
        
        measure_ids = intent.get("measures", [])
        
        return ToolSelection(
            tool_type=ToolType.VALIDATE,
            confidence=0.80,
            reasoning=f"Validate {', '.join(validation_targets) if validation_targets else 'results'}",
            context_indicators=["compliance_check", "high_stakes"],
            params={
                "validation_type": "hedis_spec",
                "measure_ids": measure_ids,
                "strict_mode": True
            }
        )
    
    def _sort_and_validate_selections(
        self,
        selections: List[ToolSelection]
    ) -> List[ToolSelection]:
        """
        Sort tools by dependencies and confidence.
        
        Order:
        1. retrieve (provides context)
        2. query_db (provides data)
        3. calculate (uses data)
        4. validate (validates results)
        """
        tool_order = {
            ToolType.RETRIEVE: 1,
            ToolType.QUERY_DB: 2,
            ToolType.CALCULATE: 3,
            ToolType.VALIDATE: 4
        }
        
        # Sort by tool order, then confidence
        sorted_selections = sorted(
            selections,
            key=lambda x: (tool_order.get(x.tool_type, 99), -x.confidence)
        )
        
        return sorted_selections
    
    def _log_selection(
        self,
        query: str,
        context: Dict,
        selections: List[ToolSelection]
    ):
        """Log tool selection for audit trail."""
        selection_log = {
            "timestamp": datetime.now().isoformat(),
            "query": query[:200],  # Truncate for logging
            "context_layers": list(context.keys()),
            "tools_selected": [
                {
                    "tool": s.tool_type.value,
                    "confidence": s.confidence,
                    "reasoning": s.reasoning
                }
                for s in selections
            ]
        }
        
        logger.info(f"Tool selection: {json.dumps(selection_log, indent=2)}")
        self.selection_history.append(selection_log)


def select_tools_with_context(query: str, context: Dict) -> List[str]:
    """
    Select tools based on context and query requirements.
    
    Based on Rule 3.3 from JOINT_CONTEXT_AGENTIC_RULES.md
    
    Context indicators:
    - Domain knowledge missing → retrieve tool
    - Measure-specific → query_db tool
    - Calculation needed → calculate tool
    - Validation needed → validate tool
    
    Args:
        query: User query string
        context: Hierarchical context dictionary
    
    Returns:
        List of tool names to use
    """
    tools = []
    query_lower = query.lower()
    
    # Check if domain knowledge needed
    # Domain knowledge is in layer_1_domain
    domain_knowledge = context.get("layer_1_domain", {})
    if not domain_knowledge or not domain_knowledge.get("hedis_overview"):
        tools.append("retrieve")
        logger.info("Domain knowledge missing, adding retrieve tool")
    
    # Check if database query needed
    # Check for measure_id in context (layer_2_measure) or query mentions member data
    measures_in_context = list(context.get("layer_2_measure", {}).keys())
    if measures_in_context or "member_data" in query_lower or "gaps" in query_lower:
        tools.append("query_db")
        logger.info(f"Measure-specific query detected (measures: {measures_in_context}), adding query_db tool")
    
    # Check if calculation needed
    if any(keyword in query_lower for keyword in ["roi", "calculate", "compute", "roi ratio"]):
        tools.append("calculate")
        logger.info("Calculation keywords detected, adding calculate tool")
    
    # Check if validation needed
    if "validate" in query_lower or "compliance" in query_lower or "verify" in query_lower:
        tools.append("validate")
        logger.info("Validation keywords detected, adding validate tool")
    
    # If no tools selected, default to retrieve
    if not tools:
        tools.append("retrieve")
        logger.info("No specific tools detected, defaulting to retrieve")
    
    return tools


def refine_context_in_loop(
    context: Dict,
    step_result: Any,
    iteration: int,
    step_type: str,
    step_id: str
) -> Tuple[Dict, Dict]:
    """
    Refine context based on step results in agentic loop.
    
    Based on Practice 2 from JOINT_CONTEXT_AGENTIC_RULES.md
    
    Args:
        context: Current context dictionary
        step_result: Result from current step
        iteration: Current iteration number (0-indexed)
        step_type: Type of step (retrieve, query_db, calculate, validate)
        step_id: Step identifier
    
    Returns:
        Tuple of (refined_context, metrics_dict)
    """
    metrics = {
        "context_size_before": estimate_tokens(context),
        "compression_applied": False,
        "relevance_updated": False
    }
    
    # Add result to context
    if "step_results" not in context:
        context["step_results"] = []
    
    context["step_results"].append({
        "iteration": iteration,
        "step_id": step_id,
        "step_type": step_type,
        "result": step_result,
        "timestamp": datetime.now().isoformat()
    })
    
    # Update relevance scores after first step
    if iteration > 0:
        context["relevance_scores"] = _update_relevance_from_results(
            context.get("relevance_scores", []),
            context["step_results"]
        )
        metrics["relevance_updated"] = True
        logger.info(f"Iteration {iteration}: Updated relevance scores based on step results")
    
    # Compress if needed (stay under 4000 tokens)
    current_tokens = estimate_tokens(context)
    if current_tokens > 4000:
        logger.info(
            f"Iteration {iteration}: Context size {current_tokens} tokens exceeds 4000, compressing..."
        )
        context = compress_context(
            context,
            target_tokens=3000,  # Compress to 3000 to leave room
            logger=logger
        )
        metrics["compression_applied"] = True
        metrics["context_size_after"] = estimate_tokens(context)
        logger.info(
            f"Iteration {iteration}: Compressed context to {metrics['context_size_after']} tokens"
        )
    else:
        metrics["context_size_after"] = current_tokens
    
    return context, metrics


def _update_relevance_from_results(
    current_scores: List[float],
    step_results: List[Dict]
) -> List[float]:
    """
    Update relevance scores based on step results.
    
    Args:
        current_scores: Current relevance scores
        step_results: List of step results
    
    Returns:
        Updated relevance scores
    """
    # If no current scores, initialize based on step results
    if not current_scores:
        # Initialize scores based on number of step results
        return [0.7] * len(step_results) if step_results else []
    
    # Update scores based on step success
    # Successful steps increase relevance, failed steps decrease
    updated_scores = current_scores.copy()
    
    # Ensure scores list matches step_results length
    while len(updated_scores) < len(step_results):
        updated_scores.append(0.5)  # Default relevance for new results
    
    # Update scores based on recent results
    for i, result in enumerate(step_results[-3:]):  # Look at last 3 results
        step_type = result.get("step_type", "")
        result_data = result.get("result", {})
        
        # Increase relevance for successful retrievals
        if step_type == "retrieve":
            if isinstance(result_data, list) and len(result_data) > 0:
                updated_scores[i] = min(updated_scores[i] + 0.1, 1.0)
        
        # Increase relevance for successful calculations
        elif step_type == "calculate":
            if isinstance(result_data, dict) and result_data.get("roi_ratio", 0) > 0:
                updated_scores[i] = min(updated_scores[i] + 0.1, 1.0)
        
        # Increase relevance for successful queries
        elif step_type == "query_db":
            if isinstance(result_data, (dict, list)) and len(result_data) > 0:
                updated_scores[i] = min(updated_scores[i] + 0.1, 1.0)
    
    return updated_scores


class JointAuditLogger:
    """
    Log both context and agentic steps together for complete audit trail.
    
    Based on Rule 3.6 from JOINT_CONTEXT_AGENTIC_RULES.md
    """
    
    def __init__(self):
        """Initialize joint audit logger."""
        self.audit_log = []
    
    def log_joint_execution(
        self,
        query: str,
        initial_context: Dict,
        plan: Dict,
        step_results: List[Any],
        final_context: Dict
    ):
        """
        Log complete execution with context and steps.
        
        Args:
            query: User query
            initial_context: Initial hierarchical context
            plan: Agentic plan
            step_results: Results from each step
            final_context: Final accumulated context
        """
        audit_entry = {
            "timestamp": datetime.now().isoformat(),
            "query": query,
            "initial_context": {
                "size_tokens": estimate_tokens(initial_context),
                "hash": hash(str(initial_context)),
                "layers": list(initial_context.keys()) if isinstance(initial_context, dict) else []
            },
            "plan": {
                "steps_count": len(plan.get("steps", [])),
                "steps": [
                    {
                        "id": step.get("id", ""),
                        "type": step.get("type", ""),
                        "context_hint": step.get("context_hint", "")
                    }
                    for step in plan.get("steps", [])
                ]
            },
            "step_results": [
                {
                    "step_index": i,
                    "result_type": type(result).__name__,
                    "result_hash": hash(str(result)),
                    "result_size": estimate_tokens({"data": result}) if result else 0
                }
                for i, result in enumerate(step_results)
            ],
            "final_context": {
                "size_tokens": estimate_tokens(final_context),
                "hash": hash(str(final_context)),
                "layers": list(final_context.keys()) if isinstance(final_context, dict) else []
            }
        }
        
        self.audit_log.append(audit_entry)
        logger.info(
            f"Joint execution logged: {len(plan.get('steps', []))} steps, "
            f"{estimate_tokens(initial_context)} -> {estimate_tokens(final_context)} tokens"
        )
    
    def get_audit_log(self) -> List[Dict]:
        """Get audit log."""
        return self.audit_log.copy()


class ContextDrivenPlanningAgent:
    """
    Planning agent that uses context to inform decisions.
    
    Based on Template 2 from JOINT_CONTEXT_AGENTIC_RULES.md
    
    Enhanced with ContextDrivenToolSelector for intelligent tool selection.
    """
    
    def __init__(self, base_planning_agent: PlanningAgent):
        """
        Initialize context-driven planning agent.
        
        Args:
            base_planning_agent: Base PlanningAgent instance
        """
        self.base_planning_agent = base_planning_agent
        self.tool_selector = ContextDrivenToolSelector()
    
    def decompose_with_context(self, query: str, context: Dict) -> Dict:
        """
        Decompose query using context to inform planning.
        
        Context informs:
        - Available measures
        - Relevant tools
        - Step dependencies
        - Expected results
        
        Args:
            query: User query string
            context: Hierarchical context dictionary
        
        Returns:
            Plan dictionary with steps
        """
        # Select tools based on context (using enhanced selector)
        tool_selections = self.tool_selector.select_tools(query, context)
        selected_tools = [s.tool_type.value for s in tool_selections]
        logger.info(f"Selected tools based on context: {selected_tools}")
        
        # Store tool selections for later use
        self._last_tool_selections = tool_selections
        
        # Extract context hints
        measures = list(context.get("layer_2_measure", {}).keys())
        domain_knowledge = context.get("layer_1_domain", {})
        
        # Get base plan from planning agent
        base_plan = self.base_planning_agent.decompose(query)
        
        # Filter and enhance steps based on selected tools
        enhanced_steps = []
        step_counter = 1
        
        # Add retrieve step if selected and not already present
        if "retrieve" in selected_tools:
            has_retrieve = any(step.get("type") == "retrieve" for step in base_plan.get("steps", []))
            if not has_retrieve:
                enhanced_steps.append({
                    "id": f"step_{step_counter}",
                    "type": "retrieve",
                    "query": f"Retrieve HEDIS specifications for {', '.join(measures) if measures else 'mentioned measures'}",
                    "params": {
                        "top_k": 5,
                        "content_type": "specifications"
                    },
                    "context_hint": f"Domain knowledge available: {bool(domain_knowledge)}",
                    "depends_on": []
                })
                step_counter += 1
        
        # Process base plan steps, filtering by selected tools
        for step in base_plan.get("steps", []):
            step_type = step.get("type")
            
            # Skip synthesize step (will add at end)
            if step_type == "synthesize":
                continue
            
            # Only include steps for selected tools
            if step_type in selected_tools or step_type == "retrieve":
                # Enhance step with context hints
                enhanced_step = step.copy()
                
                # Add context hints
                if step_type == "retrieve":
                    enhanced_step["context_hint"] = (
                        f"Domain knowledge available: {bool(domain_knowledge)}"
                    )
                elif step_type == "query_db":
                    enhanced_step["context_hint"] = (
                        f"Measures in context: {measures}"
                    )
                    # Use measure from context if available
                    if measures and "measure_id" not in enhanced_step.get("params", {}):
                        enhanced_step["params"] = enhanced_step.get("params", {})
                        enhanced_step["params"]["measure_id"] = measures[0]
                elif step_type == "calculate":
                    enhanced_step["context_hint"] = (
                        f"Using measures from context: {measures}"
                    )
                    if measures and "measure_id" not in enhanced_step.get("params", {}):
                        enhanced_step["params"] = enhanced_step.get("params", {})
                        enhanced_step["params"]["measure_id"] = measures[0]
                elif step_type == "validate":
                    enhanced_step["context_hint"] = (
                        f"Validating against measures in context: {measures}"
                    )
                    if measures and "measure_id" not in enhanced_step.get("params", {}):
                        enhanced_step["params"] = enhanced_step.get("params", {})
                        enhanced_step["params"]["measure_id"] = measures[0]
                
                enhanced_step["id"] = f"step_{step_counter}"
                enhanced_steps.append(enhanced_step)
                step_counter += 1
        
        # Add synthesize step at the end
        enhanced_steps.append({
            "id": f"step_{step_counter}",
            "type": "synthesize",
            "query": "Synthesize final response from all accumulated context",
            "params": {
                "context": "all_results",
                "format": "structured"
            },
            "depends_on": [step["id"] for step in enhanced_steps],
            "context_hint": f"Using context from {len(enhanced_steps) - 1} steps"
        })
        
        # Build plan with tool selection details
        plan = {
            "steps": enhanced_steps,
            "query": query,
            "estimated_execution_time": len(enhanced_steps) * 5,  # 5 sec per step estimate
            "context_used": {
                "layers": list(context.keys()),
                "tool_selections": len(tool_selections),
                "tool_selection_details": [
                    {
                        "tool": s.tool_type.value,
                        "confidence": s.confidence,
                        "reasoning": s.reasoning
                    }
                    for s in tool_selections
                ]
            }
        }
        
        logger.info(f"Created plan with {len(enhanced_steps)} steps")
        return plan


class ContextAwareAgenticRAG:
    """
    Complete agentic RAG with context engineering.
    
    Combines:
    - Hierarchical context building
    - Agentic planning
    - Context accumulation
    - Tool execution
    - Response synthesis
    
    Based on Template 1 from JOINT_CONTEXT_AGENTIC_RULES.md
    """
    
    def __init__(self, rag_retriever=None, use_llm: bool = False, llm_client=None):
        """
        Initialize ContextAwareAgenticRAG.
        
        Args:
            rag_retriever: Optional RAG retriever
            use_llm: If True, use LLM for planning/synthesis
            llm_client: Optional LLM client
        """
        # Context engineering components
        self.context_builder = HierarchicalContextBuilder(rag_retriever=rag_retriever)
        
        # Agentic RAG components
        base_planning_agent = PlanningAgent(use_llm=use_llm, llm_client=llm_client)
        self.plan_agent = ContextDrivenPlanningAgent(base_planning_agent)
        self.tool_executor = ToolExecutor(rag_retriever=rag_retriever)
        self.synthesizer = ResponseSynthesizer(use_llm=use_llm, llm_client=llm_client)
        self.result_validator = ResultValidator()
        
        # Joint components
        self.context_accumulator = ContextAccumulator()
        if HAS_AUDIT_LOGGER:
            self.audit_logger = JointAuditLogger(use_database=True)
        else:
            # Fallback to in-memory version
            self.audit_logger = _InMemoryAuditLogger()
            logger.warning("Using in-memory audit logger. Install audit_logger module for database storage.")
        
        # Configuration
        self.max_steps = 10
        self.max_tokens = 4000
        self.max_retries = 3
    
    def process_query(self, query: str, max_steps: Optional[int] = None) -> Dict:
        """
        Process query with context-aware agentic RAG.
        
        Flow:
        1. Build initial hierarchical context
        2. Plan agentic steps using context
        3. Execute steps, accumulating context
        4. Compress context as needed (stay under 4000 tokens)
        5. Synthesize final response
        6. Validate and retry if needed
        7. Joint audit logging
        
        Args:
            query: User query string
            max_steps: Maximum steps to execute (default: 10)
        
        Returns:
            Dictionary with response, steps, context, and metrics
        """
        if max_steps is None:
            max_steps = self.max_steps
        
        retry_count = 0
        original_query = query
        
        # Track query start time for execution time calculation
        import time
        self._query_start_time = time.time()
        
        while retry_count <= self.max_retries:
            try:
                # Step 1: Build initial hierarchical context
                logger.info(f"Building initial hierarchical context for query: {query}")
                initial_context = self.context_builder.build_context(query, max_tokens=self.max_tokens)
                
                # Validate initial context
                initial_tokens = estimate_tokens(initial_context)
                logger.info(f"Initial context built: {initial_tokens} tokens")
                
                # Step 2: Plan with context (context-driven tool selection)
                logger.info("Planning agentic steps with context")
                plan = self._plan_with_context(query, initial_context)
                
                # Check step limit
                if len(plan["steps"]) > max_steps:
                    logger.warning(
                        f"Plan has {len(plan['steps'])} steps, truncating to {max_steps}"
                    )
                    plan["steps"] = plan["steps"][:max_steps]
                
                # Step 3: Initialize context accumulator with initial context
                self.context_accumulator.reset()
                self.context_accumulator.add_step_result("initial_context", initial_context)
                
                # Step 4: Execute agentic steps, accumulating context with refinement loop
                step_results = []
                current_context = initial_context.copy()
                
                # Reset refinement metrics for this query
                self.context_refinement_metrics = {
                    "context_size_by_step": [],
                    "relevance_scores": [],
                    "compression_events": []
                }
                
                # Track initial context size
                self.context_refinement_metrics["context_size_by_step"].append({
                    "step": "initial",
                    "size": estimate_tokens(current_context)
                })
                
                for i, step in enumerate(plan["steps"]):
                    # Skip synthesize step (handled separately)
                    if step["type"] == "synthesize":
                        continue
                    
                    logger.info(f"Executing step {i+1}/{len(plan['steps'])}: {step['id']} ({step['type']})")
                    
                    # Execute step with context
                    try:
                        result = self._execute_step_with_context(step, current_context)
                        
                        # Validate step result
                        is_valid, errors = self.result_validator.validate_step_result(
                            step["type"],
                            step["id"],
                            result
                        )
                        
                        if is_valid:
                            # Accumulate context
                            self._accumulate_step_result(step["type"], result)
                            step_results.append(result)
                        else:
                            logger.warning(
                                f"Step {step['id']} validation failed: {errors}. "
                                "Continuing with other steps."
                            )
                            step_results.append(result)  # Still add for context
                        
                        # Refine context in loop (Practice 2)
                        current_context, refinement_metrics = refine_context_in_loop(
                            current_context,
                            result,
                            iteration=i,
                            step_type=step["type"],
                            step_id=step["id"]
                        )
                        
                        # Track context size after refinement
                        self.context_refinement_metrics["context_size_by_step"].append({
                            "step": step["id"],
                            "step_type": step["type"],
                            "size": refinement_metrics["context_size_after"],
                            "iteration": i
                        })
                        
                        # Track compression events
                        if refinement_metrics["compression_applied"]:
                            self.context_refinement_metrics["compression_events"].append({
                                "step": step["id"],
                                "iteration": i,
                                "size_before": refinement_metrics["context_size_before"],
                                "size_after": refinement_metrics["context_size_after"]
                            })
                        
                        # Track relevance scores
                        if refinement_metrics["relevance_updated"]:
                            # Get current relevance scores from context
                            relevance_scores = current_context.get("relevance_scores", [])
                            self.context_refinement_metrics["relevance_scores"].append({
                                "step": step["id"],
                                "iteration": i,
                                "scores": relevance_scores.copy() if relevance_scores else []
                            })
                    
                    except (ToolExecutionError, Exception) as e:
                        logger.error(f"Step {step['id']} failed: {e}")
                        # Try fallback
                        fallback_result = self._fallback_step_execution(step, current_context)
                        if fallback_result:
                            self._accumulate_step_result(step["type"], fallback_result)
                            step_results.append(fallback_result)
                            
                            # Refine context with fallback result
                            current_context, refinement_metrics = refine_context_in_loop(
                                current_context,
                                fallback_result,
                                iteration=i,
                                step_type=step["type"],
                                step_id=step["id"]
                            )
                            
                            # Track metrics for fallback
                            self.context_refinement_metrics["context_size_by_step"].append({
                                "step": step["id"],
                                "step_type": step["type"],
                                "size": refinement_metrics["context_size_after"],
                                "iteration": i,
                                "fallback": True
                            })
                
                # Step 5: Get final accumulated context
                final_context = self.context_accumulator.get_full_context()
                
                # Compress final context if needed
                final_tokens = estimate_tokens(final_context)
                if final_tokens > self.max_tokens:
                    logger.info(f"Compressing final context: {final_tokens} tokens")
                    final_context = compress_context(
                        final_context,
                        target_tokens=self.max_tokens,
                        logger=logger
                    )
                
                # Step 6: Synthesize with full accumulated context
                logger.info("Synthesizing response with accumulated context")
                import time
                synthesis_start = time.time()
                response = self.synthesizer.generate(query, final_context)
                synthesis_time = time.time() - synthesis_start
                
                # Calculate total execution time
                total_execution_time = time.time() - getattr(self, '_query_start_time', time.time())
                
                # Step 7: Validate final response
                validation_passed = False
                validation_result_data = None
                if self.result_validator.validate(response):
                    logger.info("Response validation passed")
                    validation_passed = True
                    validation_result_data = {
                        "passed": True,
                        "validation_metrics": self.result_validator.get_metrics()
                    }
                    
                    # Step 8: Joint audit logging (Rule 3.6)
                    self.audit_logger.log_joint_execution(
                        query=original_query,
                        initial_context=initial_context,
                        plan=plan,
                        step_results=step_results,
                        final_context=final_context,
                        execution_time=total_execution_time,
                        validation_results=validation_result_data,
                        errors=None  # Can be populated if errors occurred
                    )
                    
                    return {
                        "response": response,
                        "steps_executed": len(step_results),
                        "context_used": {
                            "initial_size": estimate_tokens(initial_context),
                            "final_size": estimate_tokens(final_context),
                            "initial_context": initial_context,
                            "final_context": final_context
                        },
                        "plan": plan,
                        "retry_count": retry_count,
                        "metrics": self._get_metrics(),
                        "context_refinement": self.context_refinement_metrics,
                        "execution_time": total_execution_time,
                        "validation_passed": validation_passed
                    }
                else:
                    validation_result_data = {
                        "passed": False,
                        "validation_metrics": self.result_validator.get_metrics()
                    }
                    logger.warning("Response validation failed. Refining query and retrying...")
                    retry_count += 1
                    if retry_count <= self.max_retries:
                        query = self._refine_query(query, response, step_results)
                        continue
                    else:
                        logger.error("Max retries exceeded. Using fallback response.")
                        fallback_response = self._fallback_response(original_query, final_context)
                        return {
                            "response": fallback_response,
                            "steps_executed": len(step_results),
                            "context_used": {
                                "initial_size": estimate_tokens(initial_context),
                                "final_size": estimate_tokens(final_context),
                                "initial_context": initial_context,
                                "final_context": final_context
                            },
                            "plan": plan,
                            "retry_count": retry_count,
                            "validation_warning": "Response did not pass validation",
                            "metrics": self._get_metrics()
                        }
            
            except PlanningError as e:
                logger.error(f"Planning failed: {e}")
                if retry_count < self.max_retries:
                    retry_count += 1
                    query = self._refine_query(query, {}, [])
                    continue
                else:
                    raise
            except Exception as e:
                logger.error(f"Unexpected error: {e}")
                if retry_count < self.max_retries:
                    retry_count += 1
                    query = self._refine_query(query, {}, [])
                    continue
                else:
                    fallback_response = self._fallback_response(original_query, {})
                    return {
                        "response": fallback_response,
                        "steps_executed": 0,
                        "context_used": {},
                        "error": str(e),
                        "metrics": self._get_metrics()
                    }
    
    def _plan_with_context(self, query: str, context: Dict) -> Dict:
        """
        Plan agentic steps using context (context-driven tool selection).
        
        Based on Rule 3.1, Rule 3.3, and Template 2 from JOINT_CONTEXT_AGENTIC_RULES.md
        
        Args:
            query: User query
            context: Initial hierarchical context
        
        Returns:
            Plan dictionary with steps
        """
        # Use context-driven planning agent
        plan = self.plan_agent.decompose_with_context(query, context)
        
        logger.info(
            f"Context-driven plan created: {len(plan['steps'])} steps, "
            f"tools: {[step['type'] for step in plan['steps'] if step['type'] != 'synthesize']}"
        )
        
        return plan
    
    def _execute_step_with_context(self, step: Dict, context: Dict) -> Any:
        """
        Execute step with context awareness.
        
        Args:
            step: Step dictionary
            context: Current accumulated context
        
        Returns:
            Step execution result
        """
        step_type = step.get("type")
        params = step.get("params", {})
        
        # Enrich params with context
        enriched_params = self._enrich_params_with_context(params, context)
        
        # Execute tool
        if step_type == "retrieve":
            return self.tool_executor.execute("retrieve_docs", enriched_params)
        elif step_type == "query_db":
            return self.tool_executor.execute("query_database", enriched_params)
        elif step_type == "calculate":
            operation = enriched_params.get("operation", "roi")
            if operation == "roi":
                return self.tool_executor.execute("calculate_roi", enriched_params)
            else:
                return self.tool_executor.execute("calculate_roi", enriched_params)
        elif step_type == "validate":
            return self.tool_executor.execute("validate_hedis_spec", enriched_params)
        else:
            raise ToolExecutionError(f"Unknown step type: {step_type}")
    
    def _enrich_params_with_context(self, params: Dict, context: Dict) -> Dict:
        """
        Enrich tool parameters with context.
        
        Based on Template 3 from JOINT_CONTEXT_AGENTIC_RULES.md
        
        Args:
            params: Tool parameters
            context: Current context
        
        Returns:
            Enriched parameters
        """
        enriched = params.copy()
        
        # Add measure context if available
        if "measure_id" in params and "layer_2_measure" in context:
            measure_id = params["measure_id"]
            if measure_id in context["layer_2_measure"]:
                enriched["measure_context"] = context["layer_2_measure"][measure_id]
        
        # Add domain context
        if "layer_1_domain" in context:
            enriched["domain_context"] = context["layer_1_domain"]
        
        return enriched
    
    def _accumulate_step_result(self, step_type: str, result: Any):
        """Accumulate step result in context accumulator."""
        if step_type == "retrieve":
            self.context_accumulator.add_step_result("retrieved_docs", result)
        elif step_type == "query_db":
            self.context_accumulator.add_step_result("query_results", result)
        elif step_type == "calculate":
            self.context_accumulator.add_step_result("calculations", result)
        elif step_type == "validate":
            self.context_accumulator.add_step_result("validations", result)
    
    def _update_context_with_result(self, context: Dict, result: Any, step_type: str) -> Dict:
        """
        Update context with step result.
        
        Args:
            context: Current context
            result: Step result
            step_type: Type of step
        
        Returns:
            Updated context
        """
        updated = context.copy()
        
        # Add result to appropriate layer
        if step_type == "query_db" and isinstance(result, dict):
            # Add query results to layer_3_query
            if "layer_3_query" not in updated:
                updated["layer_3_query"] = {}
            if "query_results" not in updated["layer_3_query"]:
                updated["layer_3_query"]["query_results"] = []
            updated["layer_3_query"]["query_results"].append(result)
        
        elif step_type == "calculate" and isinstance(result, dict):
            # Add calculations to layer_3_query
            if "layer_3_query" not in updated:
                updated["layer_3_query"] = {}
            if "calculations" not in updated["layer_3_query"]:
                updated["layer_3_query"]["calculations"] = []
            updated["layer_3_query"]["calculations"].append(result)
        
        return updated
    
    def _refine_query(self, query: str, response: Dict, step_results: List[Any]) -> str:
        """Refine query based on failures."""
        # Simplify query
        refined = query
        
        # Remove complex operations if many failures
        if len(step_results) == 0:
            refined = refined.replace("prioritize", "")
            refined = refined.replace("validate", "")
        
        return " ".join(refined.split())
    
    def _fallback_step_execution(self, step: Dict, context: Dict) -> Optional[Any]:
        """Fallback strategy for failed steps."""
        step_type = step.get("type")
        
        if step_type == "query_db":
            # Fallback to retrieve
            logger.info(f"Falling back to retrieve_docs for step {step['id']}")
            return self.tool_executor.execute("retrieve_docs", {
                "query": step.get("query", ""),
                "top_k": 3
            })
        elif step_type == "calculate":
            # Return default values
            return {
                "roi_ratio": 1.0,
                "net_benefit": 0,
                "fallback": True
            }
        
        return None
    
    def _fallback_response(self, query: str, context: Dict) -> Dict:
        """Generate fallback response."""
        return {
            "summary": f"Unable to fully process query: {query}. Please try simplifying your request.",
            "recommendations": [
                "Try breaking down complex queries into simpler parts",
                "Ensure database is available for data queries"
            ],
            "metrics": {},
            "data_sources": ["Fallback response"],
            "fallback": True
        }
    
    def _get_metrics(self) -> Dict:
        """Get performance metrics."""
        return {
            "context_builder_metrics": {
                "initial_context_built": True
            },
            "agentic_metrics": {
                "steps_executed": len(self.context_accumulator.get_full_context().get("query_results", []))
            },
            "validation_metrics": self.result_validator.get_metrics()
        }
    
    def get_audit_log(self) -> List[Dict]:
        """Get joint audit log."""
        return self.audit_logger.get_audit_log()


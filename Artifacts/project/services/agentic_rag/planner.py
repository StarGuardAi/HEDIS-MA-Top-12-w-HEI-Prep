"""
Agentic Planning: Decompose queries into executable steps
"""

from typing import Dict, List, Any
from dataclasses import dataclass
from enum import Enum
import json

class ToolType(Enum):
    RETRIEVE = "retrieve"
    QUERY_DB = "query_db"
    CALCULATE = "calculate"
    VALIDATE = "validate"
    SYNTHESIZE = "synthesize"

@dataclass
class ExecutionStep:
    """Single step in execution plan"""
    id: str
    type: ToolType
    params: Dict[str, Any]
    depends_on: List[str]
    confidence: float
    reasoning: str

class AgenticPlanner:
    """
    Decompose complex queries into executable steps.
    Uses context to inform planning decisions.
    """
    
    def __init__(self):
        self.planning_history = []
    
    def create_plan(
        self, 
        query: str, 
        context: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """
        Create execution plan for query.
        
        Returns:
            {
                "query": str,
                "steps": List[ExecutionStep],
                "estimated_time": float,
                "estimated_cost": float,
                "optimization_applied": List[str]
            }
        """
        # Parse query intent
        intent = self._parse_intent(query)
        
        # Determine required steps
        steps = []
        step_counter = 1
        optimizations = []
        
        # Step 1: Check if retrieval needed
        if not self._has_domain_knowledge(context):
            steps.append(ExecutionStep(
                id=f"step_{step_counter}",
                type=ToolType.RETRIEVE,
                params={"query": "HEDIS specifications", "top_k": 5},
                depends_on=[],
                confidence=0.90,
                reasoning="Domain knowledge missing from context"
            ))
            step_counter += 1
        else:
            optimizations.append("Skipped retrieval - context cached")
        
        # Step 2: Database query if needed
        if intent["needs_data"]:
            depends = [steps[-1].id] if steps else []
            steps.append(ExecutionStep(
                id=f"step_{step_counter}",
                type=ToolType.QUERY_DB,
                params={
                    "query_type": "member_gaps",
                    "measure_id": intent["measures"][0] if intent["measures"] else "CDC"
                },
                depends_on=depends,
                confidence=0.85,
                reasoning="Member data required for calculation"
            ))
            step_counter += 1
        
        # Step 3: Calculation if needed
        if intent["needs_calculation"]:
            depends = [steps[-1].id] if steps else []
            steps.append(ExecutionStep(
                id=f"step_{step_counter}",
                type=ToolType.CALCULATE,
                params={
                    "operation": "roi",
                    "measure_id": intent["measures"][0] if intent["measures"] else "CDC"
                },
                depends_on=depends,
                confidence=0.95,
                reasoning="ROI calculation requested"
            ))
            step_counter += 1
        
        # Step 4: Validation if needed
        if intent["needs_validation"] or intent["needs_calculation"]:
            depends = [steps[-1].id] if steps else []
            steps.append(ExecutionStep(
                id=f"step_{step_counter}",
                type=ToolType.VALIDATE,
                params={
                    "validation_type": "hedis_compliance",
                    "strict_mode": True
                },
                depends_on=depends,
                confidence=0.88,
                reasoning="Validation required for compliance/accuracy"
            ))
            step_counter += 1
        
        # Final step: Synthesis
        steps.append(ExecutionStep(
            id=f"step_{step_counter}",
            type=ToolType.SYNTHESIZE,
            params={"use_all_context": True},
            depends_on=[s.id for s in steps] if steps else [],
            confidence=1.0,
            reasoning="Synthesize final response"
        ))
        
        # Calculate estimates
        estimated_time = sum(self._estimate_step_time(s) for s in steps)
        estimated_cost = sum(self._estimate_step_cost(s) for s in steps)
        
        plan = {
            "query": query,
            "steps": steps,
            "total_steps": len(steps),
            "estimated_time": round(estimated_time, 1),
            "estimated_cost": round(estimated_cost, 4),
            "optimizations_applied": optimizations,
            "avg_confidence": round(sum(s.confidence for s in steps) / len(steps), 2)
        }
        
        self.planning_history.append(plan)
        return plan
    
    def _parse_intent(self, query: str) -> Dict[str, Any]:
        """Parse query to understand intent"""
        query_lower = query.lower()
        
        # Extract measures
        measures = []
        measure_patterns = ["CDC", "EED", "GSD", "HBD", "KED", "CBP", "BPD"]
        for measure in measure_patterns:
            if measure.lower() in query_lower:
                measures.append(measure)
        
        return {
            "needs_calculation": any(kw in query_lower for kw in ["roi", "calculate", "compute", "impact"]),
            "needs_data": any(kw in query_lower for kw in ["member", "gap", "performance", "rate"]),
            "needs_validation": any(kw in query_lower for kw in ["validate", "compliance", "hedis", "verify"]),
            "measures": measures,
            "complexity": self._assess_complexity(query_lower)
        }
    
    def _assess_complexity(self, query: str) -> str:
        """Assess query complexity"""
        word_count = len(query.split())
        
        if word_count < 10:
            return "simple"
        elif word_count < 25:
            return "medium"
        else:
            return "complex"
    
    def _has_domain_knowledge(self, context: Dict[str, Any]) -> bool:
        """Check if domain knowledge exists in context"""
        if not context:
            return False
        return bool(context.get("layer_1_domain", {}).get("hedis_overview"))
    
    def _estimate_step_time(self, step: ExecutionStep) -> float:
        """Estimate execution time for step (seconds)"""
        time_estimates = {
            ToolType.RETRIEVE: 3.5,
            ToolType.QUERY_DB: 2.8,
            ToolType.CALCULATE: 1.2,
            ToolType.VALIDATE: 0.9,
            ToolType.SYNTHESIZE: 1.5
        }
        return time_estimates.get(step.type, 2.0)
    
    def _estimate_step_cost(self, step: ExecutionStep) -> float:
        """Estimate cost for step (USD)"""
        cost_estimates = {
            ToolType.RETRIEVE: 0.003,
            ToolType.QUERY_DB: 0.002,
            ToolType.CALCULATE: 0.001,
            ToolType.VALIDATE: 0.001,
            ToolType.SYNTHESIZE: 0.002
        }
        return cost_estimates.get(step.type, 0.002)




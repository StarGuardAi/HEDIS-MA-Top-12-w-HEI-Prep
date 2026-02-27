"""
Services module for healthcare AI chatbot.
"""
from .context_engine import (
    HierarchicalContextBuilder,
    TERMINOLOGY_CONTEXT,
    compress_context,
    summarize_document,
    estimate_tokens
)
# Try to import from agentic_rag module (new structure)
try:
    from .agentic_rag import (
        AgenticPlanner,
        ToolExecutor,
        ExecutionStep,
        ToolType,
        ExecutionResult
    )
    HAS_AGENTIC_RAG_NEW = True
except ImportError:
    HAS_AGENTIC_RAG_NEW = False
    AgenticPlanner = None
    ToolExecutor = None
    ExecutionStep = None
    ToolType = None
    ExecutionResult = None

# Try to import from old agentic_rag.py (if it exists)
try:
    from .agentic_rag_old import (
        PlanningAgent,
        PlanningError,
        ToolNotFoundError,
        ToolExecutionError,
        ContextAccumulator,
        ResponseSynthesizer,
        ResultValidator,
        HEDISAgenticRAG
    )
    HAS_AGENTIC_RAG_OLD = True
except ImportError:
    HAS_AGENTIC_RAG_OLD = False
    PlanningAgent = None
    PlanningError = None
    ToolNotFoundError = None
    ToolExecutionError = None
    ContextAccumulator = None
    ResponseSynthesizer = None
    ResultValidator = None
    HEDISAgenticRAG = None

try:
    from .joint_rag import (
        ContextAwareAgenticRAG,
        ContextDrivenPlanningAgent,
        select_tools_with_context
    )
    HAS_JOINT_RAG = True
except ImportError:
    HAS_JOINT_RAG = False
    ContextAwareAgenticRAG = None
    ContextDrivenPlanningAgent = None
    select_tools_with_context = None

try:
    from .audit_logger import JointAuditLogger
    HAS_AUDIT_LOGGER = True
except ImportError:
    HAS_AUDIT_LOGGER = False
    JointAuditLogger = None

__all__ = [
    'HierarchicalContextBuilder',
    'TERMINOLOGY_CONTEXT',
    'compress_context',
    'summarize_document',
    'estimate_tokens',
    # New agentic RAG classes
    'AgenticPlanner',
    'ToolExecutor',
    'ExecutionStep',
    'ToolType',
    'ExecutionResult',
    # Old agentic RAG classes (if available)
    'PlanningAgent',
    'PlanningError',
    'ToolNotFoundError',
    'ToolExecutionError',
    'ContextAccumulator',
    'ResponseSynthesizer',
    'ResultValidator',
    'HEDISAgenticRAG',
    # Joint RAG classes
    'ContextAwareAgenticRAG',
    'ContextDrivenPlanningAgent',
    'ContextDrivenToolSelector',
    'ToolSelection',
    'QueryParser',
    'ContextAnalyzer',
    'select_tools_with_context',
    'HAS_JOINT_RAG',
    # Audit logger
    'JointAuditLogger',
    'HAS_AUDIT_LOGGER',
    # Flags
    'HAS_AGENTIC_RAG_NEW',
    'HAS_AGENTIC_RAG_OLD'
]


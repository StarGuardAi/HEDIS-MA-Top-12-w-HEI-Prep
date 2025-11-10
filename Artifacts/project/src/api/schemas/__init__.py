"""
API Schema Definitions
Pydantic models for request/response validation.
"""

from .common import ErrorResponse, HealthResponse
from .prediction import (
    PredictionRequest,
    PredictionResponse,
    BatchPredictionRequest,
    BatchPredictionResponse,
    PortfolioPredictionRequest,
    PortfolioPredictionResponse,
)
from .portfolio import (
    PortfolioSummaryResponse,
    GapListRequest,
    GapListResponse,
    GapRecord,
    PriorityListResponse,
    MemberPriority,
)
from .analytics import (
    StarRatingRequest,
    StarRatingResponse,
    SimulationRequest,
    SimulationResponse,
    ScenarioResult,
    ROIResponse,
)

__all__ = [
    # Common
    "ErrorResponse",
    "HealthResponse",
    # Prediction
    "PredictionRequest",
    "PredictionResponse",
    "BatchPredictionRequest",
    "BatchPredictionResponse",
    "PortfolioPredictionRequest",
    "PortfolioPredictionResponse",
    # Portfolio
    "PortfolioSummaryResponse",
    "GapListRequest",
    "GapListResponse",
    "GapRecord",
    "PriorityListResponse",
    "MemberPriority",
    # Analytics
    "StarRatingRequest",
    "StarRatingResponse",
    "SimulationRequest",
    "SimulationResponse",
    "ScenarioResult",
    "ROIResponse",
]


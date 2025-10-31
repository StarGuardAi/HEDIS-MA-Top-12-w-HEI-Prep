"""
Measures Router
Endpoints for HEDIS measure information and specifications.
"""

import logging
from typing import Dict, List, Any

from fastapi import APIRouter, HTTPException, status, Request
from pydantic import BaseModel, Field

# Import HEDIS specifications
import sys
sys.path.append(".")
from src.utils.hedis_specs import MEASURE_REGISTRY, get_measure_spec, MeasureSpec

logger = logging.getLogger(__name__)

router = APIRouter()


# ===== Response Schemas =====

class MeasureListItem(BaseModel):
    """Brief measure information for list view."""
    code: str = Field(..., description="Measure code (e.g., GSD)")
    name: str = Field(..., description="Full measure name")
    tier: int = Field(..., description="Portfolio tier (1-4)")
    weight: int = Field(..., description="Star Rating weight (1 or 3)")
    status: str = Field(..., description="Status: production, development, planned")
    new_measure: bool = Field(default=False, description="NEW 2025 measure")
    star_value_estimate: str = Field(..., description="Estimated annual value")


class MeasureDetailResponse(BaseModel):
    """Detailed measure information."""
    code: str
    name: str
    tier: int
    weight: int
    status: str
    new_measure: bool
    description: str
    population_criteria: Dict[str, Any]
    data_sources_required: List[str]
    hedis_version: str
    star_value_estimate: str
    model_target_auc: float
    required_features: List[str]


class MeasurePerformanceResponse(BaseModel):
    """Current performance for a measure."""
    measure_code: str
    current_rate: float = Field(..., description="Current rate (0-1)")
    numerator: int = Field(..., description="Members meeting criteria")
    denominator: int = Field(..., description="Eligible members")
    star_rating: float = Field(..., description="Star Rating for this measure")
    estimated_value: float = Field(..., description="Estimated value ($)")
    gap_count: int = Field(..., description="Number of predicted gaps")
    high_risk_count: int = Field(..., description="High-risk gaps")


# ===== Measures Endpoints =====

@router.get("/measures", tags=["Measures"])
async def list_measures(request: Request) -> List[MeasureListItem]:
    """
    Get list of all 12 HEDIS measures in the portfolio.
    
    **12 Measures Across 4 Tiers:**
    
    **Tier 1 (Diabetes):** GSD*, KED*, EED, PDC-DR, BPD*
    - *Triple-weighted (3x Star Rating impact)
    - GSD, BPD = NEW 2025 measures
    
    **Tier 2 (Cardiovascular):** CBP*, SUPD, PDC-RASA, PDC-STA
    - *Triple-weighted
    
    **Tier 3 (Cancer Screening):** BCS, COL
    
    **Tier 4 (Health Equity):** HEI
    - 5% bonus/penalty on overall Star Rating
    """
    request_id = getattr(request.state, 'request_id', 'unknown')
    
    logger.info(f"List Measures Request | Request-ID: {request_id}")
    
    measures_list = []
    
    for code, spec in MEASURE_REGISTRY.items():
        item = MeasureListItem(
            code=code,
            name=spec.name,
            tier=spec.tier,
            weight=spec.weight,
            status=spec.status,
            new_measure=spec.new_measure,
            star_value_estimate=spec.star_value_estimate
        )
        measures_list.append(item)
    
    # Sort by tier, then by weight (desc), then by code
    measures_list.sort(key=lambda x: (x.tier, -x.weight, x.code))
    
    logger.info(f"Returned {len(measures_list)} measures")
    
    return measures_list


@router.get("/measures/{measure_code}", response_model=MeasureDetailResponse, tags=["Measures"])
async def get_measure_details(measure_code: str, request: Request) -> MeasureDetailResponse:
    """
    Get detailed information for a specific HEDIS measure.
    
    **Includes:**
    - Full measure specifications
    - Population criteria (age, gender, diagnosis)
    - Required data sources
    - Value sets (ICD-10, CPT, LOINC codes)
    - Model metadata
    - Star Rating value estimate
    """
    request_id = getattr(request.state, 'request_id', 'unknown')
    measure_code = measure_code.upper()
    
    logger.info(f"Measure Details Request | Code: {measure_code} | Request-ID: {request_id}")
    
    # Get measure spec
    spec = get_measure_spec(measure_code)
    
    if not spec:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Measure code '{measure_code}' not found. Available: {list(MEASURE_REGISTRY.keys())}"
        )
    
    # Build response
    response = MeasureDetailResponse(
        code=measure_code,
        name=spec.name,
        tier=spec.tier,
        weight=spec.weight,
        status=spec.status,
        new_measure=spec.new_measure,
        description=spec.description,
        population_criteria={
            "age_range": spec.age_range,
            "gender": spec.gender,
            "diagnosis_required": spec.diagnosis_required
        },
        data_sources_required=spec.data_sources_required,
        hedis_version=spec.hedis_version,
        star_value_estimate=spec.star_value_estimate,
        model_target_auc=spec.model_target_auc,
        required_features=spec.required_features
    )
    
    logger.info(f"Returned details for {measure_code}")
    
    return response


@router.get("/measures/{measure_code}/performance", response_model=MeasurePerformanceResponse, tags=["Measures"])
async def get_measure_performance(measure_code: str, request: Request) -> MeasurePerformanceResponse:
    """
    Get current performance metrics for a specific measure.
    
    **Metrics:**
    - Current rate (numerator/denominator)
    - Star Rating
    - Gap count (predicted gaps)
    - High-risk gap count
    - Estimated value of improvement
    
    **Note:** Performance data comes from predictions and actual claims data.
    """
    request_id = getattr(request.state, 'request_id', 'unknown')
    measure_code = measure_code.upper()
    
    logger.info(f"Measure Performance Request | Code: {measure_code} | Request-ID: {request_id}")
    
    # Validate measure
    if measure_code not in MEASURE_REGISTRY:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Measure code '{measure_code}' not found"
        )
    
    # TODO: Load actual performance data from database
    # For now, return demo data
    
    # Demo performance data
    current_rate = 0.75
    denominator = 1000
    numerator = int(denominator * current_rate)
    
    # Calculate star rating (simplified)
    if current_rate >= 0.90:
        star_rating = 5.0
    elif current_rate >= 0.80:
        star_rating = 4.5
    elif current_rate >= 0.70:
        star_rating = 4.0
    else:
        star_rating = 3.5
    
    # Gap metrics
    gap_count = denominator - numerator
    high_risk_count = int(gap_count * 0.6)  # 60% high-risk
    
    # Estimated value
    measure_spec = MEASURE_REGISTRY[measure_code]
    estimated_value = gap_count * 200.0 * measure_spec.weight
    
    response = MeasurePerformanceResponse(
        measure_code=measure_code,
        current_rate=current_rate,
        numerator=numerator,
        denominator=denominator,
        star_rating=star_rating,
        estimated_value=estimated_value,
        gap_count=gap_count,
        high_risk_count=high_risk_count
    )
    
    logger.info(
        f"Performance for {measure_code} | Rate: {current_rate:.1%} | "
        f"Gaps: {gap_count} | Stars: {star_rating}"
    )
    
    return response


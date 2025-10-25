"""
Portfolio Router
Endpoints for portfolio-level analytics, gap analysis, and optimization.
"""

import time
import logging
from typing import Dict, List, Optional
from datetime import datetime

from fastapi import APIRouter, HTTPException, status, Depends, Request, Query

from ..schemas.portfolio import (
    PortfolioSummaryResponse,
    GapListRequest,
    GapListResponse,
    GapRecord,
    PriorityListResponse,
    MemberPriority,
    OptimizationRequest,
    OptimizationResponse,
)
from ..config import get_settings, APISettings

# Import portfolio utilities
import sys
sys.path.append(".")
from src.utils.hedis_specs import MEASURE_REGISTRY, get_measure_spec

logger = logging.getLogger(__name__)

router = APIRouter()


# ===== Helper Functions =====

def calculate_priority_score(gap_probability: float, measure_weight: int, is_new_2025: bool) -> float:
    """
    Calculate priority score for a gap.
    Higher for triple-weighted measures and NEW 2025 measures.
    """
    base_score = gap_probability * 100
    weighted_score = base_score * measure_weight
    
    # Bonus for NEW 2025 measures
    if is_new_2025:
        weighted_score *= 1.2
    
    return min(weighted_score, 100.0)


# ===== Portfolio Endpoints =====

@router.get("/portfolio/summary", response_model=PortfolioSummaryResponse, tags=["Portfolio"])
async def get_portfolio_summary(
    request: Request,
    settings: APISettings = Depends(get_settings)
) -> PortfolioSummaryResponse:
    """
    Get comprehensive portfolio summary with gap analysis and Star Rating projections.
    
    **Includes:**
    - Total member count and gap counts
    - Gaps by measure and tier
    - Current vs. projected Star Rating
    - Estimated portfolio value
    - ROI projections
    
    **Cache:** Results cached for 5 minutes
    
    **Response Time Target:** < 1 second
    """
    start_time = time.time()
    request_id = getattr(request.state, 'request_id', 'unknown')
    
    try:
        # TODO: Load actual predictions from database
        # For now, return demo data
        logger.info("Generating portfolio summary | Request-ID: {request_id}")
        
        # Demo data
        total_members = 10000
        total_gaps = 2500
        
        gaps_by_measure = {
            "GSD": 450,
            "KED": 380,
            "EED": 320,
            "PDC-DR": 280,
            "BPD": 270,
            "CBP": 350,
            "SUPD": 180,
            "PDC-RASA": 120,
            "PDC-STA": 100,
            "BCS": 30,
            "COL": 20,
        }
        
        gaps_by_tier = {
            1: 1200,  # Tier 1: Diabetes
            2: 750,   # Tier 2: Cardiovascular
            3: 50,    # Tier 3: Cancer Screening
            4: 500,   # Tier 4: HEI-related
        }
        
        high_risk_count = 1200
        star_rating_current = 3.8
        star_rating_projected = 4.3
        estimated_value = 1500000.0
        gap_closure_target = 1250
        expected_closures = 875
        roi_estimate = 320.5
        
        processing_time = (time.time() - start_time) * 1000
        
        logger.info(
            f"Portfolio Summary Generated | Members: {total_members} | "
            f"Gaps: {total_gaps} | Time: {processing_time:.2f}ms"
        )
        
        response = PortfolioSummaryResponse(
            total_members=total_members,
            total_gaps=total_gaps,
            gaps_by_measure=gaps_by_measure,
            gaps_by_tier=gaps_by_tier,
            high_risk_count=high_risk_count,
            star_rating_current=star_rating_current,
            star_rating_projected=star_rating_projected,
            star_improvement=star_rating_projected - star_rating_current,
            estimated_value=estimated_value,
            gap_closure_target=gap_closure_target,
            expected_closures=expected_closures,
            roi_estimate=roi_estimate,
        )
        
        return response
        
    except Exception as e:
        logger.error(f"Portfolio summary failed | Error: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to generate portfolio summary: {str(e)}"
        )


@router.post("/portfolio/gaps", response_model=GapListResponse, tags=["Portfolio"])
async def get_gap_list(
    request_data: GapListRequest,
    request: Request,
    settings: APISettings = Depends(get_settings)
) -> GapListResponse:
    """
    Get filtered and sorted list of quality gaps.
    
    **Filters:**
    - Measure codes (e.g., GSD, KED)
    - Risk tiers (high, medium, low)
    - Minimum gap probability
    - Minimum priority score
    
    **Sorting:** By priority_score (default), gap_probability, or estimated_value
    
    **Pagination:** Use limit and offset for large result sets
    """
    start_time = time.time()
    request_id = getattr(request.state, 'request_id', 'unknown')
    
    try:
        # TODO: Load actual gaps from database with filters
        # For now, return demo data
        
        logger.info(
            f"Gap List Request | Filters: {request_data.dict(exclude_none=True)} | "
            f"Request-ID: {request_id}"
        )
        
        # Demo gaps
        demo_gaps = []
        gap_count = 0
        
        # Generate demo gap records
        measures = request_data.measure_codes or ["GSD", "KED", "EED", "CBP"]
        risk_tiers = request_data.risk_tiers or ["high", "medium"]
        
        for measure_code in measures:
            measure_spec = get_measure_spec(measure_code)
            if not measure_spec:
                continue
            
            for tier in risk_tiers:
                if gap_count >= request_data.limit:
                    break
                
                gap_prob = 0.85 if tier == "high" else 0.55
                
                if request_data.min_probability and gap_prob < request_data.min_probability:
                    continue
                
                priority = calculate_priority_score(
                    gap_prob,
                    measure_spec.weight,
                    measure_spec.new_measure
                )
                
                if request_data.min_priority_score and priority < request_data.min_priority_score:
                    continue
                
                gap = GapRecord(
                    member_hash=f"member_{gap_count:04d}",
                    measure_code=measure_code,
                    measure_name=measure_spec.name,
                    gap_probability=gap_prob,
                    risk_tier=tier,
                    priority_score=priority,
                    intervention_type="lab_test" if measure_code in ["GSD", "KED"] else "pcp_visit",
                    estimated_value=200.0 * measure_spec.weight
                )
                demo_gaps.append(gap)
                gap_count += 1
        
        # Sort gaps
        reverse = request_data.sort_order == "desc"
        demo_gaps.sort(key=lambda x: getattr(x, request_data.sort_by), reverse=reverse)
        
        # Apply offset
        demo_gaps = demo_gaps[request_data.offset:]
        
        # Check if more results
        has_more = len(demo_gaps) > request_data.limit
        demo_gaps = demo_gaps[:request_data.limit]
        
        processing_time = (time.time() - start_time) * 1000
        
        logger.info(
            f"Gap List Generated | Gaps: {len(demo_gaps)} | "
            f"Time: {processing_time:.2f}ms"
        )
        
        response = GapListResponse(
            gaps=demo_gaps,
            total_gaps=gap_count,
            filters_applied=request_data.dict(exclude_none=True),
            limit=request_data.limit,
            offset=request_data.offset,
            has_more=has_more
        )
        
        return response
        
    except Exception as e:
        logger.error(f"Gap list failed | Error: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to generate gap list: {str(e)}"
        )


@router.get("/portfolio/priority-list", response_model=PriorityListResponse, tags=["Portfolio"])
async def get_priority_list(
    request: Request,
    limit: int = Query(default=100, ge=1, le=1000, description="Maximum members to return"),
    min_gaps: int = Query(default=2, ge=1, description="Minimum number of gaps"),
    settings: APISettings = Depends(get_settings)
) -> PriorityListResponse:
    """
    Get list of high-priority members for targeted interventions.
    
    **Prioritization:**
    1. Members with multiple gaps (2+)
    2. Triple-weighted measures (GSD, KED, CBP)
    3. NEW 2025 measures (KED, BPD)
    4. High gap probabilities
    
    **Intervention Bundling:** Identifies opportunities to address multiple gaps with single intervention
    """
    start_time = time.time()
    request_id = getattr(request.state, 'request_id', 'unknown')
    
    try:
        # TODO: Load actual member data from database
        # For now, return demo data
        
        logger.info(
            f"Priority List Request | Limit: {limit} | Min Gaps: {min_gaps} | "
            f"Request-ID: {request_id}"
        )
        
        # Demo priority members
        priority_members = []
        
        for i in range(min(limit, 50)):
            member = MemberPriority(
                member_hash=f"priority_member_{i:04d}",
                total_gaps=min_gaps + (i % 3),
                gap_measures=["GSD", "KED", "EED"][:min_gaps + (i % 3)],
                gap_details=[],
                priority_score=95.0 - (i * 1.5),
                priority_tier="critical" if i < 10 else "high" if i < 30 else "medium",
                estimated_value=600.0 * (min_gaps + (i % 3)),
                interventions=[
                    "Schedule PCP visit",
                    "Order lab tests (HbA1c, eGFR, ACR)",
                    "Refer to ophthalmology"
                ][:min_gaps + (i % 3)],
                intervention_bundle="diabetes_comprehensive"
            )
            priority_members.append(member)
        
        # Calculate stats
        total_value = sum(m.estimated_value for m in priority_members)
        expected_closures = int(len(priority_members) * 0.7)  # 70% success rate
        avg_priority = sum(m.priority_score for m in priority_members) / len(priority_members)
        
        tier_dist = {
            "critical": sum(1 for m in priority_members if m.priority_tier == "critical"),
            "high": sum(1 for m in priority_members if m.priority_tier == "high"),
            "medium": sum(1 for m in priority_members if m.priority_tier == "medium"),
            "low": 0
        }
        
        bundle_dist = {
            "diabetes_comprehensive": sum(1 for m in priority_members if m.intervention_bundle == "diabetes_comprehensive"),
            "lab_only": 0,
            "pcp_visit": 0
        }
        
        processing_time = (time.time() - start_time) * 1000
        
        logger.info(
            f"Priority List Generated | Members: {len(priority_members)} | "
            f"Value: ${total_value:,.0f} | Time: {processing_time:.2f}ms"
        )
        
        response = PriorityListResponse(
            high_priority_members=priority_members,
            total_members=len(priority_members),
            total_value=total_value,
            expected_closures=expected_closures,
            average_priority_score=avg_priority,
            tier_distribution=tier_dist,
            intervention_bundles=bundle_dist
        )
        
        return response
        
    except Exception as e:
        logger.error(f"Priority list failed | Error: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to generate priority list: {str(e)}"
        )


@router.post("/portfolio/optimize", response_model=OptimizationResponse, tags=["Portfolio"])
async def optimize_portfolio(
    request_data: OptimizationRequest,
    request: Request,
    settings: APISettings = Depends(get_settings)
) -> OptimizationResponse:
    """
    Optimize intervention strategy based on budget and constraints.
    
    **Strategies:**
    - **triple_weighted:** Focus on GSD, KED, CBP (3x impact)
    - **new_2025:** Prioritize NEW 2025 measures (KED, BPD)
    - **multi_measure:** Target members with 3+ gaps
    - **balanced:** Optimize across all measures
    
    **Intervention Bundling:** Achieves 20-40% cost savings by combining interventions
    
    **Returns:** Optimized intervention list with ROI projections
    """
    start_time = time.time()
    request_id = getattr(request.state, 'request_id', 'unknown')
    
    try:
        # TODO: Implement actual optimization algorithm
        # For now, return demo optimization
        
        logger.info(
            f"Portfolio Optimization | Strategy: {request_data.strategy} | "
            f"Budget: ${request_data.budget or 'unlimited'} | "
            f"Request-ID: {request_id}"
        )
        
        # Demo optimization results
        selected_interventions = []
        
        # Generate optimized list
        num_interventions = min(
            request_data.max_interventions or 500,
            int((request_data.budget or 100000) / 150) if request_data.budget else 500
        )
        
        for i in range(min(num_interventions, 50)):  # Demo limit
            intervention = MemberPriority(
                member_hash=f"optimized_member_{i:04d}",
                total_gaps=3,
                gap_measures=["GSD", "KED", "EED"],
                priority_score=90.0 - (i * 0.5),
                priority_tier="high",
                estimated_value=600.0,
                interventions=["PCP visit", "Lab tests", "Ophthalmology referral"],
                intervention_bundle="diabetes_comprehensive"
            )
            selected_interventions.append(intervention)
        
        # Calculate optimization metrics
        total_cost = num_interventions * 150.0
        if request_data.include_intervention_bundles:
            total_cost *= 0.75  # 25% savings from bundling
            efficiency_gain = 25.0
        else:
            efficiency_gain = 0.0
        
        total_value = num_interventions * 500.0  # Average value per closure
        net_value = total_value - total_cost
        roi = (net_value / total_cost) * 100 if total_cost > 0 else 0
        expected_closures = int(num_interventions * 0.7)  # 70% success rate
        star_improvement = 0.5  # Estimated improvement
        
        processing_time = (time.time() - start_time) * 1000
        
        logger.info(
            f"Optimization Complete | Interventions: {num_interventions} | "
            f"ROI: {roi:.1f}% | Time: {processing_time:.2f}ms"
        )
        
        response = OptimizationResponse(
            selected_interventions=selected_interventions,
            total_interventions=num_interventions,
            total_cost=total_cost,
            total_value=total_value,
            net_value=net_value,
            roi=roi,
            expected_closures=expected_closures,
            star_improvement=star_improvement,
            efficiency_gain=efficiency_gain,
            optimization_strategy=request_data.strategy
        )
        
        return response
        
    except Exception as e:
        logger.error(f"Portfolio optimization failed | Error: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Portfolio optimization failed: {str(e)}"
        )


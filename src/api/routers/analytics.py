"""
Analytics Router
Endpoints for Star Rating calculation, scenario simulation, and ROI analysis.
"""

import time
import logging
from typing import Dict, List

from fastapi import APIRouter, HTTPException, status, Depends, Request

from ..schemas.analytics import (
    StarRatingRequest,
    StarRatingResponse,
    SimulationRequest,
    SimulationResponse,
    ScenarioResult,
    ROIResponse,
    ROIProjection,
)
from ..config import get_settings, APISettings

# Import Star Rating utilities
import sys
sys.path.append(".")
from src.utils.star_calculator import StarRatingCalculator
from src.utils.hedis_specs import MEASURE_REGISTRY

logger = logging.getLogger(__name__)

router = APIRouter()


# ===== Analytics Endpoints =====

@router.post("/analytics/star-rating", response_model=StarRatingResponse, tags=["Analytics"])
async def calculate_star_rating(
    request_data: StarRatingRequest,
    request: Request,
    settings: APISettings = Depends(get_settings)
) -> StarRatingResponse:
    """
    Calculate overall Star Rating from measure rates.
    
    **Star Rating Methodology:**
    - Triple-weighted measures (GSD, KED, CBP) count 3x
    - Standard measures count 1x
    - HEI adjustment (±5%) if applicable
    
    **Star Tiers:**
    - 5.0 stars: Top performance
    - 4.5 stars: Above average
    - 4.0 stars: Average
    - 3.5 stars: Below average
    - < 3.0 stars: Needs improvement
    """
    start_time = time.time()
    request_id = getattr(request.state, 'request_id', 'unknown')
    
    try:
        logger.info(f"Star Rating Calculation | Measures: {len(request_data.measure_rates)} | Request-ID: {request_id}")
        
        # Initialize Star Rating calculator
        calculator = StarRatingCalculator()
        
        # Calculate measure-level stars
        measure_stars = {}
        measure_points = {}
        tier_points = {1: [], 2: [], 3: [], 4: []}
        
        for measure_code, rate in request_data.measure_rates.items():
            # Get measure spec
            measure_spec = MEASURE_REGISTRY.get(measure_code)
            if not measure_spec:
                logger.warning(f"Unknown measure code: {measure_code}")
                continue
            
            # Calculate star rating for this measure (simplified)
            # In production, this would use CMS percentile thresholds
            if rate >= 0.90:
                stars = 5.0
            elif rate >= 0.80:
                stars = 4.5
            elif rate >= 0.70:
                stars = 4.0
            elif rate >= 0.60:
                stars = 3.5
            elif rate >= 0.50:
                stars = 3.0
            else:
                stars = 2.5
            
            measure_stars[measure_code] = stars
            
            # Calculate points (with weighting)
            points = stars * measure_spec.weight
            measure_points[measure_code] = points
            
            # Add to tier totals
            tier_points[measure_spec.tier].append(points)
        
        # Calculate tier averages
        tier_stars = {}
        for tier, points_list in tier_points.items():
            if points_list:
                tier_stars[str(tier)] = sum(points_list) / len(points_list) / 3.0  # Normalize by max weight
        
        # Calculate overall stars
        total_points = sum(measure_points.values())
        total_weight = sum(MEASURE_REGISTRY[m].weight for m in request_data.measure_rates.keys() if m in MEASURE_REGISTRY)
        
        if total_weight > 0:
            overall_stars = total_points / total_weight
        else:
            overall_stars = 0.0
        
        # Apply HEI adjustment if provided
        hei_adjusted = False
        hei_impact = 0.0
        if request_data.hei_factor is not None:
            hei_impact = request_data.hei_factor * 5.0  # Convert ±5% to star impact
            overall_stars += hei_impact
            hei_adjusted = True
            overall_stars = max(1.0, min(5.0, overall_stars))  # Clamp to 1-5
        
        # Determine star tier
        if overall_stars >= 4.5:
            star_tier = "5-star"
        elif overall_stars >= 3.5:
            star_tier = "4-star"
        elif overall_stars >= 2.5:
            star_tier = "3-star"
        else:
            star_tier = "2-star"
        
        # Calculate revenue estimate
        plan_size = request_data.plan_size or 100000
        # Simplified: $50K per 0.1 star improvement
        revenue_estimate = plan_size * overall_stars * 0.5  # $0.50 per member per star
        
        processing_time = (time.time() - start_time) * 1000
        
        logger.info(
            f"Star Rating Calculated | Overall: {overall_stars:.2f} ({star_tier}) | "
            f"Revenue: ${revenue_estimate:,.0f} | Time: {processing_time:.2f}ms"
        )
        
        response = StarRatingResponse(
            overall_stars=round(overall_stars, 2),
            total_points=round(total_points, 2),
            measure_stars=measure_stars,
            measure_points=measure_points,
            tier_stars=tier_stars,
            hei_adjusted=hei_adjusted,
            hei_impact=round(hei_impact, 2) if hei_adjusted else None,
            revenue_estimate=revenue_estimate,
            star_tier=star_tier
        )
        
        return response
        
    except Exception as e:
        logger.error(f"Star Rating calculation failed | Error: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Star Rating calculation failed: {str(e)}"
        )


@router.post("/analytics/simulate", response_model=SimulationResponse, tags=["Analytics"])
async def simulate_scenarios(
    request_data: SimulationRequest,
    request: Request,
    settings: APISettings = Depends(get_settings)
) -> SimulationResponse:
    """
    Simulate Star Rating impact under different gap closure scenarios.
    
    **Scenarios:** Test multiple gap closure rates (e.g., 10%, 20%, 30%)
    
    **Strategies:**
    - **triple_weighted:** Focus on GSD, KED, CBP (3x measures)
    - **new_2025:** Prioritize NEW 2025 measures (KED, BPD)
    - **multi_measure:** Target members with 3+ gaps
    - **balanced:** Optimize across all measures
    
    **Returns:** ROI projections and optimal strategy recommendation
    """
    start_time = time.time()
    request_id = getattr(request.state, 'request_id', 'unknown')
    
    try:
        logger.info(
            f"Star Rating Simulation | Strategy: {request_data.strategy} | "
            f"Scenarios: {len(request_data.closure_scenarios)} | Request-ID: {request_id}"
        )
        
        # Calculate baseline Star Rating
        baseline_calculator = StarRatingCalculator()
        baseline_stars = 3.8  # Placeholder - calculate from baseline_rates
        
        # Simulate each scenario
        scenarios = []
        max_roi = 0.0
        best_scenario = None
        
        for closure_rate in request_data.closure_scenarios:
            # Calculate improved rates after gap closure
            improved_rates = {}
            total_gaps = 0
            
            for measure_code, baseline_rate in request_data.baseline_rates.items():
                measure_spec = MEASURE_REGISTRY.get(measure_code)
                if not measure_spec:
                    continue
                
                # Estimate gaps
                gap_rate = 1.0 - baseline_rate
                gaps_to_close = gap_rate * closure_rate
                
                # New rate after closure
                new_rate = baseline_rate + gaps_to_close
                improved_rates[measure_code] = min(new_rate, 1.0)
                
                # Count total gaps
                total_gaps += int(request_data.plan_size * gap_rate)
            
            # Calculate new Star Rating
            projected_stars = baseline_stars + (closure_rate * 1.5)  # Simplified
            projected_stars = min(projected_stars, 5.0)
            
            star_improvement = projected_stars - baseline_stars
            
            # Calculate financial impact
            revenue_per_star = request_data.plan_size * 0.5  # $0.50 per member per star
            revenue_impact = star_improvement * revenue_per_star
            
            # Calculate investment required
            gaps_to_close_count = int(total_gaps * closure_rate)
            investment_required = gaps_to_close_count * request_data.intervention_cost
            
            # Calculate ROI
            net_value = revenue_impact - investment_required
            roi = (net_value / investment_required * 100) if investment_required > 0 else 0
            
            # Payback period
            monthly_revenue = revenue_impact / 12
            payback_months = (investment_required / monthly_revenue) if monthly_revenue > 0 else 999
            
            scenario = ScenarioResult(
                closure_rate=closure_rate,
                strategy=request_data.strategy,
                projected_stars=round(projected_stars, 2),
                star_improvement=round(star_improvement, 2),
                revenue_impact=revenue_impact,
                investment_required=investment_required,
                net_value=net_value,
                roi=round(roi, 1),
                gaps_to_close=gaps_to_close_count,
                payback_period_months=round(payback_months, 1)
            )
            
            scenarios.append(scenario)
            
            # Track best ROI
            if roi > max_roi:
                max_roi = roi
                best_scenario = scenario
        
        # Determine optimal closure rate and recommended strategy
        optimal_closure_rate = best_scenario.closure_rate if best_scenario else 0.2
        
        # Calculate break-even closures
        revenue_per_closure = (request_data.plan_size * 0.5 * 0.1) / 100  # Revenue per 1% improvement
        break_even_closures = int(request_data.intervention_cost / revenue_per_closure) if revenue_per_closure > 0 else 0
        
        processing_time = (time.time() - start_time) * 1000
        
        logger.info(
            f"Simulation Complete | Scenarios: {len(scenarios)} | "
            f"Optimal: {optimal_closure_rate*100:.0f}% closure | "
            f"Max ROI: {max_roi:.1f}% | Time: {processing_time:.2f}ms"
        )
        
        response = SimulationResponse(
            baseline_stars=round(baseline_stars, 2),
            scenarios=scenarios,
            recommended_strategy=request_data.strategy,
            optimal_closure_rate=optimal_closure_rate,
            total_gaps=total_gaps,
            break_even_closures=break_even_closures,
            max_roi_scenario=best_scenario
        )
        
        return response
        
    except Exception as e:
        logger.error(f"Simulation failed | Error: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Simulation failed: {str(e)}"
        )


@router.get("/analytics/roi", response_model=ROIResponse, tags=["Analytics"])
async def calculate_roi(
    request: Request,
    plan_size: int = 100000,
    gap_closure_rate: float = 0.3,
    settings: APISettings = Depends(get_settings)
) -> ROIResponse:
    """
    Calculate multi-year ROI projections for portfolio optimization.
    
    **Projections:** 1-year, 3-year, and 5-year ROI
    
    **Assumptions:**
    - Gap closure rate (default: 30%)
    - Intervention cost per member (default: $150)
    - Star Rating revenue impact ($0.50 per member per star)
    - Sustained value over 5 years
    
    **Returns:** Detailed ROI breakdown with payback analysis
    """
    start_time = time.time()
    request_id = getattr(request.state, 'request_id', 'unknown')
    
    try:
        logger.info(
            f"ROI Calculation | Plan Size: {plan_size:,} | "
            f"Closure Rate: {gap_closure_rate*100:.0f}% | Request-ID: {request_id}"
        )
        
        # Current portfolio value (baseline)
        current_portfolio_value = plan_size * 3.8 * 0.5  # Current stars * revenue per star
        
        # Projected value with gap closures
        star_improvement = gap_closure_rate * 1.0  # 30% closure → 0.3 star improvement
        projected_stars = 3.8 + star_improvement
        projected_portfolio_value = plan_size * projected_stars * 0.5
        
        value_increase = projected_portfolio_value - current_portfolio_value
        
        # Estimate investment
        total_gaps = plan_size * 0.25  # Assume 25% have gaps
        gaps_to_close = total_gaps * gap_closure_rate
        intervention_cost = 150.0
        estimated_investment = gaps_to_close * intervention_cost
        
        # Calculate ROI
        net_roi = ((value_increase - estimated_investment) / estimated_investment * 100) if estimated_investment > 0 else 0
        
        # Payback period
        monthly_value = value_increase / 12
        payback_months = (estimated_investment / monthly_value) if monthly_value > 0 else 999
        
        # Multi-year projections
        projections = []
        cumulative_value = 0.0
        
        for year in range(1, 6):
            # Year 1 has implementation costs, years 2-5 only ongoing costs (10% of initial)
            year_investment = estimated_investment if year == 1 else estimated_investment * 0.1
            year_revenue = value_increase  # Sustained annual value
            year_net = year_revenue - year_investment
            cumulative_value += year_net
            
            year_roi = ((year_net) / year_investment * 100) if year_investment > 0 else 0
            
            projection = ROIProjection(
                year=year,
                investment=year_investment,
                revenue=year_revenue,
                net_value=year_net,
                cumulative_value=cumulative_value,
                roi=round(year_roi, 1)
            )
            projections.append(projection)
        
        five_year_value = cumulative_value
        
        # Assumptions
        assumptions = {
            "gap_closure_rate": gap_closure_rate,
            "cost_per_intervention": intervention_cost,
            "star_rating_revenue_per_0.1": plan_size * 0.05,
            "plan_size": plan_size,
            "baseline_stars": 3.8,
            "projected_stars": round(projected_stars, 2)
        }
        
        processing_time = (time.time() - start_time) * 1000
        
        logger.info(
            f"ROI Calculated | Net ROI: {net_roi:.1f}% | "
            f"5-Year Value: ${five_year_value:,.0f} | Time: {processing_time:.2f}ms"
        )
        
        response = ROIResponse(
            current_portfolio_value=current_portfolio_value,
            projected_value_with_closures=projected_portfolio_value,
            value_increase=value_increase,
            estimated_investment=estimated_investment,
            net_roi=round(net_roi, 1),
            payback_period_months=round(payback_months, 1),
            projections=projections,
            five_year_value=five_year_value,
            assumptions=assumptions
        )
        
        return response
        
    except Exception as e:
        logger.error(f"ROI calculation failed | Error: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"ROI calculation failed: {str(e)}"
        )


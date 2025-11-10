"""
Analytics Schema Definitions
Request/response models for analytics and Star Rating endpoints.
"""

from typing import Dict, List, Optional, Any
from pydantic import BaseModel, Field, validator


class StarRatingRequest(BaseModel):
    """
    Request schema for Star Rating calculation.
    """
    measure_rates: Dict[str, float] = Field(
        ...,
        description="Current rates by measure code (e.g., {'GSD': 0.75, 'KED': 0.68})"
    )
    hei_factor: Optional[float] = Field(
        None,
        description="Health Equity Index factor (±5%), if known",
        ge=-0.05,
        le=0.05
    )
    plan_size: Optional[int] = Field(
        None,
        description="Plan size for revenue calculation",
        ge=1000
    )
    
    @validator('measure_rates')
    def validate_rates(cls, v):
        for measure, rate in v.items():
            if not 0.0 <= rate <= 1.0:
                raise ValueError(f"Rate for {measure} must be between 0 and 1")
        return v
    
    class Config:
        json_schema_extra = {
            "example": {
                "measure_rates": {
                    "GSD": 0.75,
                    "KED": 0.68,
                    "EED": 0.72,
                    "CBP": 0.78
                },
                "hei_factor": 0.02,
                "plan_size": 100000
            }
        }


class StarRatingResponse(BaseModel):
    """
    Response schema for Star Rating calculation.
    """
    overall_stars: float = Field(..., description="Overall Star Rating (1.0-5.0)", ge=1.0, le=5.0)
    total_points: float = Field(..., description="Total points across all measures")
    measure_stars: Dict[str, float] = Field(..., description="Star Rating by measure")
    measure_points: Dict[str, float] = Field(..., description="Points by measure (with weighting)")
    tier_stars: Dict[str, float] = Field(..., description="Average stars by tier")
    hei_adjusted: bool = Field(default=False, description="Whether HEI adjustment was applied")
    hei_impact: Optional[float] = Field(None, description="HEI impact on Star Rating")
    revenue_estimate: float = Field(..., description="Estimated revenue impact ($)")
    star_tier: str = Field(..., description="Star tier: 5-star, 4-star, 3-star, etc.")
    
    class Config:
        json_schema_extra = {
            "example": {
                "overall_stars": 4.2,
                "total_points": 420.5,
                "measure_stars": {
                    "GSD": 4.5,
                    "KED": 4.0,
                    "EED": 4.5
                },
                "measure_points": {
                    "GSD": 13.5,
                    "KED": 12.0,
                    "EED": 4.5
                },
                "tier_stars": {
                    "1": 4.3,
                    "2": 4.1,
                    "3": 4.0,
                    "4": 4.5
                },
                "hei_adjusted": True,
                "hei_impact": 0.1,
                "revenue_estimate": 2100000.0,
                "star_tier": "4-star"
            }
        }


class ScenarioResult(BaseModel):
    """
    Result for a single Star Rating scenario.
    """
    closure_rate: float = Field(..., description="Gap closure rate assumed (0-1)", ge=0.0, le=1.0)
    strategy: str = Field(..., description="Strategy used")
    projected_stars: float = Field(..., description="Projected Star Rating", ge=1.0, le=5.0)
    star_improvement: float = Field(..., description="Star Rating improvement from baseline")
    revenue_impact: float = Field(..., description="Revenue impact ($)")
    investment_required: float = Field(..., description="Estimated investment required ($)")
    net_value: float = Field(..., description="Net value (revenue - investment) ($)")
    roi: float = Field(..., description="ROI (%)")
    gaps_to_close: int = Field(..., description="Number of gaps to close")
    payback_period_months: float = Field(..., description="Payback period in months")
    
    class Config:
        json_schema_extra = {
            "example": {
                "closure_rate": 0.2,
                "strategy": "triple_weighted",
                "projected_stars": 4.3,
                "star_improvement": 0.5,
                "revenue_impact": 250000.0,
                "investment_required": 75000.0,
                "net_value": 175000.0,
                "roi": 233.3,
                "gaps_to_close": 500,
                "payback_period_months": 3.6
            }
        }


class SimulationRequest(BaseModel):
    """
    Request schema for Star Rating simulation.
    """
    baseline_rates: Dict[str, float] = Field(..., description="Current baseline rates by measure")
    closure_scenarios: List[float] = Field(
        ...,
        description="Gap closure rates to simulate (e.g., [0.1, 0.2, 0.3])"
    )
    strategy: str = Field(
        default="balanced",
        description="Intervention strategy: triple_weighted, new_2025, multi_measure, balanced"
    )
    plan_size: int = Field(default=100000, description="Plan size", ge=1000)
    intervention_cost: float = Field(default=150.0, description="Average cost per intervention ($)")
    
    @validator('baseline_rates')
    def validate_baseline_rates(cls, v):
        for measure, rate in v.items():
            if not 0.0 <= rate <= 1.0:
                raise ValueError(f"Rate for {measure} must be between 0 and 1")
        return v
    
    @validator('closure_scenarios')
    def validate_scenarios(cls, v):
        for rate in v:
            if not 0.0 <= rate <= 1.0:
                raise ValueError("Closure rates must be between 0 and 1")
        if len(v) == 0:
            raise ValueError("At least one scenario is required")
        return sorted(v)  # Sort scenarios
    
    @validator('strategy')
    def validate_strategy(cls, v):
        allowed = ["triple_weighted", "new_2025", "multi_measure", "balanced"]
        if v not in allowed:
            raise ValueError(f"strategy must be one of: {allowed}")
        return v
    
    class Config:
        json_schema_extra = {
            "example": {
                "baseline_rates": {
                    "GSD": 0.70,
                    "KED": 0.65,
                    "EED": 0.68
                },
                "closure_scenarios": [0.1, 0.2, 0.3, 0.5],
                "strategy": "balanced",
                "plan_size": 100000,
                "intervention_cost": 150.0
            }
        }


class SimulationResponse(BaseModel):
    """
    Response schema for Star Rating simulation.
    """
    baseline_stars: float = Field(..., description="Baseline Star Rating", ge=1.0, le=5.0)
    scenarios: List[ScenarioResult] = Field(..., description="Results for each scenario")
    recommended_strategy: str = Field(..., description="Recommended strategy based on ROI")
    optimal_closure_rate: float = Field(..., description="Optimal gap closure rate (best ROI)")
    total_gaps: int = Field(..., description="Total gaps in portfolio")
    break_even_closures: int = Field(..., description="Closures needed to break even")
    max_roi_scenario: ScenarioResult = Field(..., description="Scenario with maximum ROI")
    
    class Config:
        json_schema_extra = {
            "example": {
                "baseline_stars": 3.8,
                "scenarios": [],  # Truncated
                "recommended_strategy": "balanced",
                "optimal_closure_rate": 0.25,
                "total_gaps": 2500,
                "break_even_closures": 200,
                "max_roi_scenario": {}  # Truncated
            }
        }


class ROIProjection(BaseModel):
    """
    ROI projection for a specific time period.
    """
    year: int = Field(..., description="Year of projection")
    investment: float = Field(..., description="Investment ($)")
    revenue: float = Field(..., description="Revenue ($)")
    net_value: float = Field(..., description="Net value ($)")
    cumulative_value: float = Field(..., description="Cumulative net value ($)")
    roi: float = Field(..., description="ROI (%)")
    
    class Config:
        json_schema_extra = {
            "example": {
                "year": 1,
                "investment": 150000.0,
                "revenue": 500000.0,
                "net_value": 350000.0,
                "cumulative_value": 350000.0,
                "roi": 233.3
            }
        }


class ROIResponse(BaseModel):
    """
    Response schema for ROI analysis.
    """
    current_portfolio_value: float = Field(..., description="Current portfolio value ($)")
    projected_value_with_closures: float = Field(..., description="Projected value with gap closures ($)")
    value_increase: float = Field(..., description="Value increase ($)")
    estimated_investment: float = Field(..., description="Estimated investment required ($)")
    net_roi: float = Field(..., description="Net ROI (%)")
    payback_period_months: float = Field(..., description="Payback period in months")
    projections: List[ROIProjection] = Field(..., description="Multi-year projections")
    five_year_value: float = Field(..., description="5-year cumulative value ($)")
    assumptions: Dict[str, Any] = Field(..., description="Assumptions used in calculation")
    
    class Config:
        json_schema_extra = {
            "example": {
                "current_portfolio_value": 1500000.0,
                "projected_value_with_closures": 2800000.0,
                "value_increase": 1300000.0,
                "estimated_investment": 375000.0,
                "net_roi": 246.7,
                "payback_period_months": 4.6,
                "projections": [],  # Truncated
                "five_year_value": 5765000.0,
                "assumptions": {
                    "gap_closure_rate": 0.3,
                    "cost_per_intervention": 150.0,
                    "star_rating_revenue_per_0.1": 50000.0
                }
            }
        }


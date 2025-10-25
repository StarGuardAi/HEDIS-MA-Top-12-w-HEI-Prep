"""
Portfolio Schema Definitions
Request/response models for portfolio management endpoints.
"""

from datetime import datetime
from typing import Dict, List, Optional
from pydantic import BaseModel, Field, validator


class GapRecord(BaseModel):
    """
    Individual gap record for a member.
    """
    member_hash: str = Field(..., description="Hashed member ID (PHI-protected)")
    measure_code: str = Field(..., description="HEDIS measure code")
    measure_name: str = Field(..., description="Full measure name")
    gap_probability: float = Field(..., description="Probability of gap (0-1)", ge=0.0, le=1.0)
    risk_tier: str = Field(..., description="Risk tier: high, medium, low")
    priority_score: float = Field(..., description="Priority score (0-100)", ge=0.0, le=100.0)
    intervention_type: str = Field(..., description="Type of intervention needed")
    estimated_value: float = Field(..., description="Estimated value of closing gap ($)")
    
    class Config:
        json_schema_extra = {
            "example": {
                "member_hash": "a1b2c3d4e5f6g7h8",
                "measure_code": "GSD",
                "measure_name": "Glycemic Status Assessment",
                "gap_probability": 0.85,
                "risk_tier": "high",
                "priority_score": 90.5,
                "intervention_type": "lab_test",
                "estimated_value": 200.0
            }
        }


class GapListRequest(BaseModel):
    """
    Request schema for gap list with filters.
    """
    measure_codes: Optional[List[str]] = Field(None, description="Filter by measure codes")
    risk_tiers: Optional[List[str]] = Field(None, description="Filter by risk tiers (high, medium, low)")
    min_probability: Optional[float] = Field(None, description="Minimum gap probability (0-1)", ge=0.0, le=1.0)
    min_priority_score: Optional[float] = Field(None, description="Minimum priority score (0-100)", ge=0.0, le=100.0)
    limit: int = Field(default=100, description="Maximum results to return", ge=1, le=10000)
    offset: int = Field(default=0, description="Offset for pagination", ge=0)
    sort_by: str = Field(default="priority_score", description="Sort field: priority_score, gap_probability")
    sort_order: str = Field(default="desc", description="Sort order: asc, desc")
    
    @validator('sort_by')
    def validate_sort_by(cls, v):
        allowed = ["priority_score", "gap_probability", "estimated_value"]
        if v not in allowed:
            raise ValueError(f"sort_by must be one of: {allowed}")
        return v
    
    @validator('sort_order')
    def validate_sort_order(cls, v):
        if v not in ["asc", "desc"]:
            raise ValueError("sort_order must be 'asc' or 'desc'")
        return v
    
    class Config:
        json_schema_extra = {
            "example": {
                "measure_codes": ["GSD", "KED"],
                "risk_tiers": ["high"],
                "min_probability": 0.7,
                "limit": 100,
                "sort_by": "priority_score"
            }
        }


class GapListResponse(BaseModel):
    """
    Response schema for gap list.
    """
    gaps: List[GapRecord] = Field(..., description="List of gap records")
    total_gaps: int = Field(..., description="Total gaps matching filters")
    filters_applied: Dict = Field(..., description="Filters that were applied")
    limit: int = Field(..., description="Results limit")
    offset: int = Field(..., description="Results offset")
    has_more: bool = Field(..., description="Whether more results are available")
    
    class Config:
        json_schema_extra = {
            "example": {
                "gaps": [],  # Truncated
                "total_gaps": 450,
                "filters_applied": {
                    "risk_tiers": ["high"],
                    "min_probability": 0.7
                },
                "limit": 100,
                "offset": 0,
                "has_more": True
            }
        }


class MemberPriority(BaseModel):
    """
    Priority member record for intervention targeting.
    """
    member_hash: str = Field(..., description="Hashed member ID")
    total_gaps: int = Field(..., description="Total predicted gaps")
    gap_measures: List[str] = Field(..., description="List of measure codes with gaps")
    gap_details: List[Dict] = Field(default_factory=list, description="Details for each gap")
    priority_score: float = Field(..., description="Overall priority score (0-100)", ge=0.0, le=100.0)
    priority_tier: str = Field(..., description="Priority tier: critical, high, medium, low")
    estimated_value: float = Field(..., description="Total estimated value ($)")
    interventions: List[str] = Field(..., description="Recommended interventions")
    intervention_bundle: Optional[str] = Field(None, description="Bundled intervention type")
    
    class Config:
        json_schema_extra = {
            "example": {
                "member_hash": "a1b2c3d4e5f6g7h8",
                "total_gaps": 3,
                "gap_measures": ["GSD", "KED", "EED"],
                "priority_score": 88.5,
                "priority_tier": "high",
                "estimated_value": 600.0,
                "interventions": [
                    "Schedule PCP visit",
                    "Order lab tests (HbA1c, eGFR, ACR)",
                    "Refer to ophthalmology"
                ],
                "intervention_bundle": "diabetes_comprehensive"
            }
        }


class PriorityListResponse(BaseModel):
    """
    Response schema for priority member list.
    """
    high_priority_members: List[MemberPriority] = Field(..., description="List of priority members")
    total_members: int = Field(..., description="Total members in priority list")
    total_value: float = Field(..., description="Total estimated value of all gaps ($)")
    expected_closures: int = Field(..., description="Expected number of closures")
    average_priority_score: float = Field(..., description="Average priority score")
    tier_distribution: Dict[str, int] = Field(..., description="Distribution by priority tier")
    intervention_bundles: Dict[str, int] = Field(..., description="Count by intervention bundle type")
    
    class Config:
        json_schema_extra = {
            "example": {
                "high_priority_members": [],  # Truncated
                "total_members": 250,
                "total_value": 125000.0,
                "expected_closures": 175,
                "average_priority_score": 78.5,
                "tier_distribution": {
                    "critical": 50,
                    "high": 100,
                    "medium": 75,
                    "low": 25
                },
                "intervention_bundles": {
                    "diabetes_comprehensive": 80,
                    "lab_only": 60,
                    "pcp_visit": 110
                }
            }
        }


class PortfolioSummaryResponse(BaseModel):
    """
    Response schema for portfolio summary.
    """
    total_members: int = Field(..., description="Total members in portfolio")
    total_gaps: int = Field(..., description="Total predicted gaps")
    gaps_by_measure: Dict[str, int] = Field(..., description="Gap counts by measure code")
    gaps_by_tier: Dict[int, int] = Field(..., description="Gap counts by tier (1-4)")
    high_risk_count: int = Field(..., description="Count of high-risk gaps")
    star_rating_current: float = Field(..., description="Current Star Rating", ge=1.0, le=5.0)
    star_rating_projected: float = Field(..., description="Projected Star Rating with gap closure", ge=1.0, le=5.0)
    star_improvement: float = Field(..., description="Potential Star Rating improvement")
    estimated_value: float = Field(..., description="Total portfolio value ($)")
    gap_closure_target: int = Field(..., description="Target number of gaps to close")
    expected_closures: int = Field(..., description="Expected closures with interventions")
    roi_estimate: float = Field(..., description="Estimated ROI (%)")
    generation_date: datetime = Field(default_factory=datetime.now, description="Summary generation timestamp")
    
    class Config:
        json_schema_extra = {
            "example": {
                "total_members": 10000,
                "total_gaps": 2500,
                "gaps_by_measure": {
                    "GSD": 450,
                    "KED": 380,
                    "EED": 320
                },
                "gaps_by_tier": {
                    "1": 1200,
                    "2": 800,
                    "3": 350,
                    "4": 150
                },
                "high_risk_count": 1200,
                "star_rating_current": 3.5,
                "star_rating_projected": 4.2,
                "star_improvement": 0.7,
                "estimated_value": 1500000.0,
                "gap_closure_target": 1250,
                "expected_closures": 875,
                "roi_estimate": 320.5,
                "generation_date": "2025-10-24T10:30:00"
            }
        }


class OptimizationRequest(BaseModel):
    """
    Request schema for portfolio optimization.
    """
    budget: Optional[float] = Field(None, description="Budget constraint ($)")
    max_interventions: Optional[int] = Field(None, description="Maximum number of interventions")
    strategy: str = Field(
        default="balanced",
        description="Optimization strategy: triple_weighted, new_2025, multi_measure, balanced"
    )
    include_intervention_bundles: bool = Field(default=True, description="Use intervention bundling")
    
    @validator('strategy')
    def validate_strategy(cls, v):
        allowed = ["triple_weighted", "new_2025", "multi_measure", "balanced"]
        if v not in allowed:
            raise ValueError(f"strategy must be one of: {allowed}")
        return v
    
    class Config:
        json_schema_extra = {
            "example": {
                "budget": 50000.0,
                "max_interventions": 500,
                "strategy": "balanced",
                "include_intervention_bundles": True
            }
        }


class OptimizationResponse(BaseModel):
    """
    Response schema for portfolio optimization.
    """
    selected_interventions: List[MemberPriority] = Field(..., description="Optimized intervention list")
    total_interventions: int = Field(..., description="Total interventions selected")
    total_cost: float = Field(..., description="Total estimated cost ($)")
    total_value: float = Field(..., description="Total estimated value ($)")
    net_value: float = Field(..., description="Net value (value - cost) ($)")
    roi: float = Field(..., description="ROI (%)")
    expected_closures: int = Field(..., description="Expected gap closures")
    star_improvement: float = Field(..., description="Projected Star Rating improvement")
    efficiency_gain: float = Field(..., description="Efficiency gain from bundling (%)")
    optimization_strategy: str = Field(..., description="Strategy used")
    
    class Config:
        json_schema_extra = {
            "example": {
                "selected_interventions": [],  # Truncated
                "total_interventions": 450,
                "total_cost": 67500.0,
                "total_value": 270000.0,
                "net_value": 202500.0,
                "roi": 300.0,
                "expected_closures": 315,
                "star_improvement": 0.5,
                "efficiency_gain": 25.0,
                "optimization_strategy": "balanced"
            }
        }


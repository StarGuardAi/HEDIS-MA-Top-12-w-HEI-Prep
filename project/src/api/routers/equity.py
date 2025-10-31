"""
HEI (Health Equity Index) Router
API endpoints for equity analysis, disparity detection, and intervention recommendations.

This router implements the CMS Health Equity Index (HEI) requirements for MY2027.
First-mover advantage: Implementing 2+ years before mandate.

Author: Robert Reichert
Date: October 25, 2025
"""

import logging
from typing import Dict, List, Any, Optional
from datetime import datetime

from fastapi import APIRouter, HTTPException, status, Request, Body
from pydantic import BaseModel, Field
import pandas as pd

# Import HEI calculator
import sys
sys.path.append(".")
from src.utils.hei_calculator import HEICalculator
from src.utils.hedis_specs import MEASURE_REGISTRY

logger = logging.getLogger(__name__)

router = APIRouter()


# ===== Request/Response Schemas =====

class EquityAnalysisRequest(BaseModel):
    """Request for stratified equity analysis."""
    measure_code: str = Field(..., description="HEDIS measure code (e.g., 'GSD')")
    measure_results: List[Dict[str, Any]] = Field(..., description="Member-level measure results")
    hei_data: List[Dict[str, Any]] = Field(..., description="HEI demographic data (race, ethnicity, language, SDOH)")
    stratification_var: str = Field(default="race_ethnicity_std", description="Variable to stratify by")
    disparity_threshold: float = Field(default=10.0, description="Minimum disparity magnitude (percentage points)")
    measurement_year: int = Field(default=2025, description="HEDIS measurement year")
    
    class Config:
        json_schema_extra = {
            "example": {
                "measure_code": "GSD",
                "measure_results": [
                    {
                        "member_id": "M001",
                        "GSD_in_denominator": 1,
                        "GSD_in_numerator": 1,
                        "GSD_gap": 0
                    }
                ],
                "hei_data": [
                    {
                        "member_id": "M001",
                        "race_ethnicity_std": "WHITE",
                        "language_std": "ENGLISH",
                        "is_lep": 0,
                        "lis": 0,
                        "dual_eligible": 0
                    }
                ],
                "stratification_var": "race_ethnicity_std",
                "disparity_threshold": 10.0,
                "measurement_year": 2025
            }
        }


class StratifiedPerformance(BaseModel):
    """Stratified performance for a demographic group."""
    group: str = Field(..., description="Demographic group name")
    denominator: int = Field(..., description="Members in denominator")
    numerator: int = Field(..., description="Members in numerator")
    gaps: int = Field(..., description="Members with gaps")
    compliance_rate: float = Field(..., description="Compliance rate (%)")
    gap_rate: float = Field(..., description="Gap rate (%)")
    is_valid_group: bool = Field(..., description="Meets minimum size requirement")


class DisparityInfo(BaseModel):
    """Disparity information between groups."""
    has_disparity: bool = Field(..., description="Disparity detected")
    disparity_magnitude: float = Field(..., description="Percentage point difference")
    disparity_category: str = Field(..., description="LOW/MODERATE/HIGH")
    highest_performing_group: str = Field(..., description="Best performing group")
    lowest_performing_group: str = Field(..., description="Worst performing group")
    highest_compliance_rate: float = Field(..., description="Best group rate (%)")
    lowest_compliance_rate: float = Field(..., description="Worst group rate (%)")
    equity_score: float = Field(..., description="Equity score (0-100)")


class EquityAnalysisResponse(BaseModel):
    """Response for equity analysis."""
    request_id: str
    measure_code: str
    stratification_var: str
    stratified_performance: List[StratifiedPerformance]
    disparity_info: DisparityInfo
    analysis_timestamp: str
    measurement_year: int


class PortfolioEquityScoreRequest(BaseModel):
    """Request for portfolio-level equity score."""
    measure_results: Dict[str, List[Dict[str, Any]]] = Field(..., description="Results by measure code")
    hei_data: List[Dict[str, Any]] = Field(..., description="HEI demographic data")
    measure_weights: Dict[str, float] = Field(..., description="Measure weights (1.0 or 3.0)")
    stratification_vars: List[str] = Field(default=["race_ethnicity_std"], description="Variables to stratify by")
    measurement_year: int = Field(default=2025, description="HEDIS measurement year")
    
    class Config:
        json_schema_extra = {
            "example": {
                "measure_results": {
                    "GSD": [{"member_id": "M001", "GSD_in_denominator": 1, "GSD_in_numerator": 1, "GSD_gap": 0}],
                    "KED": [{"member_id": "M001", "KED_in_denominator": 1, "KED_in_numerator": 1, "KED_gap": 0}]
                },
                "hei_data": [{"member_id": "M001", "race_ethnicity_std": "WHITE", "language_std": "ENGLISH"}],
                "measure_weights": {"GSD": 3.0, "KED": 3.0},
                "stratification_vars": ["race_ethnicity_std", "language_std"],
                "measurement_year": 2025
            }
        }


class PortfolioEquityScoreResponse(BaseModel):
    """Response for portfolio equity score."""
    request_id: str
    overall_equity_score: float = Field(..., description="Portfolio equity score (0-100)")
    penalty_category: str = Field(..., description="NO_PENALTY / MODERATE / HIGH")
    penalty_amount: float = Field(..., description="Star rating penalty (0, -0.25, -0.5)")
    measures_analyzed: int
    measures_with_disparities: int
    stratifications_evaluated: int
    total_comparisons: int
    equity_score_by_measure: Dict[str, float]
    analysis_timestamp: str
    financial_impact: Dict[str, Any] = Field(..., description="Financial impact of equity score")


class InterventionPriority(BaseModel):
    """Priority intervention recommendation."""
    priority_rank: int
    measure: str
    stratification: str
    target_group: str
    current_rate: float
    goal_rate: float
    gap_to_close: float
    disparity_category: str
    measure_weight: float
    recommended_actions: List[str]


class InterventionsResponse(BaseModel):
    """Response for priority interventions."""
    request_id: str
    interventions: List[InterventionPriority]
    total_interventions: int
    high_priority_count: int
    financial_impact_potential: str
    analysis_timestamp: str


class EquityReportRequest(BaseModel):
    """Request for detailed equity report."""
    measure_results: Dict[str, List[Dict[str, Any]]]
    hei_data: List[Dict[str, Any]]
    measure_weights: Dict[str, float]
    stratification_vars: List[str] = Field(default=["race_ethnicity_std"])
    report_format: str = Field(default="summary", description="summary or detailed")
    measurement_year: int = Field(default=2025)


class EquityReportResponse(BaseModel):
    """Response for equity report."""
    request_id: str
    report_format: str
    report_content: str = Field(..., description="Formatted equity report")
    overall_equity_score: float
    penalty_category: str
    key_findings: List[str]
    top_priorities: List[str]
    analysis_timestamp: str
    

# ===== HEI Equity Endpoints =====

@router.post("/equity/analyze", response_model=EquityAnalysisResponse, tags=["Health Equity Index (HEI)"])
async def analyze_equity_single_measure(
    request: Request,
    analysis_request: EquityAnalysisRequest = Body(...)
) -> EquityAnalysisResponse:
    """
    **Analyze health equity for a single HEDIS measure.**
    
    Performs stratified analysis by demographic group to identify disparities
    in measure performance. This is a core component of the CMS Health Equity
    Index (HEI) requirement starting in MY2027.
    
    **Key Features:**
    - Stratifies performance by race, ethnicity, language, or SDOH
    - Calculates disparity magnitude between groups
    - Assigns equity score (0-100 scale)
    - Identifies highest and lowest performing groups
    - Validates minimum group sizes
    
    **Use Case:** Detect if certain demographic groups have lower compliance
    rates for a specific measure (e.g., diabetic eye exams lower in Hispanic population).
    
    **Returns:** Stratified performance metrics and disparity information.
    """
    request_id = getattr(request.state, 'request_id', 'unknown')
    
    logger.info(f"Equity Analysis Request | Measure: {analysis_request.measure_code} | "
                f"Stratification: {analysis_request.stratification_var} | Request-ID: {request_id}")
    
    try:
        # Initialize HEI calculator
        hei_calc = HEICalculator(measurement_year=analysis_request.measurement_year)
        
        # Convert to DataFrames
        measure_results_df = pd.DataFrame(analysis_request.measure_results)
        hei_data_df = pd.DataFrame(analysis_request.hei_data)
        
        # Calculate stratified performance
        stratified = hei_calc.calculate_stratified_performance(
            measure_results_df,
            hei_data_df,
            analysis_request.measure_code,
            analysis_request.stratification_var
        )
        
        # Identify disparities
        disparity_info = hei_calc.identify_disparities(
            stratified,
            analysis_request.stratification_var,
            disparity_threshold=analysis_request.disparity_threshold
        )
        
        # Get measure weight for equity scoring
        measure_spec = MEASURE_REGISTRY.get(analysis_request.measure_code)
        measure_weight = measure_spec.weight if measure_spec else 1.0
        
        # Calculate equity score
        equity_score = hei_calc.calculate_equity_score_single_measure(
            disparity_info,
            measure_weight=measure_weight
        )
        disparity_info['equity_score'] = equity_score
        
        # Format stratified performance
        stratified_performance = []
        for _, row in stratified.iterrows():
            perf = StratifiedPerformance(
                group=row[analysis_request.stratification_var],
                denominator=int(row['denominator']),
                numerator=int(row['numerator']),
                gaps=int(row['gaps']),
                compliance_rate=float(row['compliance_rate']),
                gap_rate=float(row['gap_rate']),
                is_valid_group=bool(row['is_valid_group'])
            )
            stratified_performance.append(perf)
        
        # Format disparity info
        disparity = DisparityInfo(
            has_disparity=disparity_info['has_disparity'],
            disparity_magnitude=float(disparity_info['disparity_magnitude']),
            disparity_category=disparity_info['disparity_category'],
            highest_performing_group=disparity_info['highest_performing_group'],
            lowest_performing_group=disparity_info['lowest_performing_group'],
            highest_compliance_rate=float(disparity_info['highest_compliance_rate']),
            lowest_compliance_rate=float(disparity_info['lowest_compliance_rate']),
            equity_score=float(equity_score)
        )
        
        logger.info(f"Equity Analysis Complete | Measure: {analysis_request.measure_code} | "
                    f"Disparity: {disparity.has_disparity} | Score: {equity_score:.1f} | "
                    f"Request-ID: {request_id}")
        
        return EquityAnalysisResponse(
            request_id=request_id,
            measure_code=analysis_request.measure_code,
            stratification_var=analysis_request.stratification_var,
            stratified_performance=stratified_performance,
            disparity_info=disparity,
            analysis_timestamp=datetime.utcnow().isoformat(),
            measurement_year=analysis_request.measurement_year
        )
        
    except Exception as e:
        logger.error(f"Equity Analysis Failed | Error: {str(e)} | Request-ID: {request_id}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Equity analysis failed: {str(e)}"
        )


@router.post("/equity/score", response_model=PortfolioEquityScoreResponse, tags=["Health Equity Index (HEI)"])
async def calculate_portfolio_equity_score(
    request: Request,
    score_request: PortfolioEquityScoreRequest = Body(...)
) -> PortfolioEquityScoreResponse:
    """
    **Calculate portfolio-level Health Equity Index (HEI) score.**
    
    Evaluates equity across all measures in the portfolio and calculates
    an overall equity score (0-100 scale). The score determines CMS penalty tier:
    - **Score ≥ 70:** No penalty
    - **Score 50-69:** -0.25 stars ($10M penalty for 100K members)
    - **Score < 50:** -0.5 stars ($20M penalty for 100K members)
    
    **Key Features:**
    - Portfolio-level equity scoring
    - CMS penalty tier determination
    - Financial impact calculation
    - Multi-stratification support (race, language, SDOH)
    - Weighted by measure importance (triple-weighted measures have 3x impact)
    
    **Use Case:** Determine if your health plan meets CMS equity requirements
    and avoid catastrophic star rating penalties.
    
    **Returns:** Overall equity score, penalty category, and financial impact.
    """
    request_id = getattr(request.state, 'request_id', 'unknown')
    
    logger.info(f"Portfolio Equity Score Request | Measures: {len(score_request.measure_results)} | "
                f"Stratifications: {len(score_request.stratification_vars)} | Request-ID: {request_id}")
    
    try:
        # Initialize HEI calculator
        hei_calc = HEICalculator(measurement_year=score_request.measurement_year)
        
        # Convert measure results to DataFrames
        measure_results_dfs = {}
        for measure_code, results in score_request.measure_results.items():
            measure_results_dfs[measure_code] = pd.DataFrame(results)
        
        # Convert HEI data
        hei_data_df = pd.DataFrame(score_request.hei_data)
        
        # Calculate portfolio equity score
        equity_results = hei_calc.calculate_portfolio_equity_score(
            measure_results_dfs,
            hei_data_df,
            score_request.measure_weights,
            stratification_vars=score_request.stratification_vars
        )
        
        # Determine penalty category
        overall_score = equity_results['overall_equity_score']
        if overall_score >= 70:
            penalty_category = "NO_PENALTY"
            penalty_amount = 0.0
            financial_impact_desc = "No penalty - excellent equity performance"
            financial_impact_value = 0
        elif overall_score >= 50:
            penalty_category = "MODERATE"
            penalty_amount = -0.25
            financial_impact_desc = "Moderate penalty - equity improvement needed"
            financial_impact_value = -10_000_000  # $10M for 100K members
        else:
            penalty_category = "HIGH"
            penalty_amount = -0.5
            financial_impact_desc = "HIGH penalty - urgent equity action required"
            financial_impact_value = -20_000_000  # $20M for 100K members
        
        # Get equity scores by measure
        equity_score_by_measure = {}
        for disp in equity_results['all_disparities']:
            if 'measure' in disp and 'equity_score' in disp:
                equity_score_by_measure[disp['measure']] = disp['equity_score']
        
        logger.info(f"Portfolio Equity Score Complete | Score: {overall_score:.1f} | "
                    f"Penalty: {penalty_category} ({penalty_amount}) | Request-ID: {request_id}")
        
        return PortfolioEquityScoreResponse(
            request_id=request_id,
            overall_equity_score=overall_score,
            penalty_category=penalty_category,
            penalty_amount=penalty_amount,
            measures_analyzed=equity_results['measures_analyzed'],
            measures_with_disparities=equity_results['measures_with_disparities'],
            stratifications_evaluated=equity_results['stratifications_evaluated'],
            total_comparisons=equity_results['total_comparisons'],
            equity_score_by_measure=equity_score_by_measure,
            analysis_timestamp=datetime.utcnow().isoformat(),
            financial_impact={
                "description": financial_impact_desc,
                "estimated_value": financial_impact_value,
                "penalty_stars": penalty_amount,
                "basis": "100K member MA plan"
            }
        )
        
    except Exception as e:
        logger.error(f"Portfolio Equity Score Failed | Error: {str(e)} | Request-ID: {request_id}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Portfolio equity score calculation failed: {str(e)}"
        )


@router.post("/equity/interventions", response_model=InterventionsResponse, tags=["Health Equity Index (HEI)"])
async def get_priority_interventions(
    request: Request,
    score_request: PortfolioEquityScoreRequest = Body(...),
    top_n: int = 10
) -> InterventionsResponse:
    """
    **Get priority intervention recommendations to address health equity disparities.**
    
    Identifies the top opportunities to improve equity and provides actionable
    recommendations for closing gaps. Prioritizes by:
    - Disparity magnitude (larger gaps = higher priority)
    - Measure weight (triple-weighted measures = 3x priority)
    - Group size (larger populations = more impact)
    
    **Key Features:**
    - Ranked intervention priorities
    - Specific action recommendations per group
    - Cultural competency guidance
    - Resource allocation suggestions
    - Financial impact potential
    
    **Use Case:** Create an actionable equity improvement plan to avoid CMS penalties
    and improve care for underserved populations.
    
    **Returns:** Top N priority interventions with recommended actions.
    """
    request_id = getattr(request.state, 'request_id', 'unknown')
    
    logger.info(f"Priority Interventions Request | Top N: {top_n} | Request-ID: {request_id}")
    
    try:
        # Initialize HEI calculator
        hei_calc = HEICalculator(measurement_year=score_request.measurement_year)
        
        # Convert data
        measure_results_dfs = {}
        for measure_code, results in score_request.measure_results.items():
            measure_results_dfs[measure_code] = pd.DataFrame(results)
        hei_data_df = pd.DataFrame(score_request.hei_data)
        
        # Calculate equity results
        equity_results = hei_calc.calculate_portfolio_equity_score(
            measure_results_dfs,
            hei_data_df,
            score_request.measure_weights,
            stratification_vars=score_request.stratification_vars
        )
        
        # Get priority interventions
        interventions = hei_calc.identify_priority_interventions(equity_results, top_n=top_n)
        
        # Format interventions
        formatted_interventions = []
        high_priority_count = 0
        
        for intervention in interventions:
            if intervention['disparity_category'] == 'HIGH':
                high_priority_count += 1
            
            priority = InterventionPriority(
                priority_rank=intervention['priority_rank'],
                measure=intervention['measure'],
                stratification=intervention['stratification'],
                target_group=intervention['target_group'],
                current_rate=intervention['current_rate'],
                goal_rate=intervention['goal_rate'],
                gap_to_close=intervention['gap_to_close'],
                disparity_category=intervention['disparity_category'],
                measure_weight=intervention['measure_weight'],
                recommended_actions=intervention['recommended_actions']
            )
            formatted_interventions.append(priority)
        
        # Calculate financial impact potential
        if equity_results['overall_equity_score'] < 70:
            # Could move to no penalty tier
            financial_impact_potential = "$10M-$20M penalty avoidance"
        else:
            financial_impact_potential = "Maintain no-penalty status"
        
        logger.info(f"Priority Interventions Complete | Total: {len(formatted_interventions)} | "
                    f"High Priority: {high_priority_count} | Request-ID: {request_id}")
        
        return InterventionsResponse(
            request_id=request_id,
            interventions=formatted_interventions,
            total_interventions=len(formatted_interventions),
            high_priority_count=high_priority_count,
            financial_impact_potential=financial_impact_potential,
            analysis_timestamp=datetime.utcnow().isoformat()
        )
        
    except Exception as e:
        logger.error(f"Priority Interventions Failed | Error: {str(e)} | Request-ID: {request_id}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Priority interventions generation failed: {str(e)}"
        )


@router.post("/equity/report", response_model=EquityReportResponse, tags=["Health Equity Index (HEI)"])
async def generate_equity_report(
    request: Request,
    report_request: EquityReportRequest = Body(...)
) -> EquityReportResponse:
    """
    **Generate comprehensive Health Equity Index (HEI) report.**
    
    Creates a formatted report with equity analysis, disparities, and recommendations.
    Available in summary (1-2 pages) or detailed (5-10 pages) formats.
    
    **Report Includes:**
    - Overall equity score and penalty tier
    - Stratified performance by measure
    - Disparity analysis by demographic group
    - Top priority interventions
    - Recommended actions
    - Financial impact summary
    
    **Use Case:** Executive reporting, board presentations, CMS compliance documentation.
    
    **Returns:** Formatted equity report as plain text (convertible to PDF/Word).
    """
    request_id = getattr(request.state, 'request_id', 'unknown')
    
    logger.info(f"Equity Report Request | Format: {report_request.report_format} | Request-ID: {request_id}")
    
    try:
        # Initialize HEI calculator
        hei_calc = HEICalculator(measurement_year=report_request.measurement_year)
        
        # Convert data
        measure_results_dfs = {}
        for measure_code, results in report_request.measure_results.items():
            measure_results_dfs[measure_code] = pd.DataFrame(results)
        hei_data_df = pd.DataFrame(report_request.hei_data)
        
        # Calculate equity results
        equity_results = hei_calc.calculate_portfolio_equity_score(
            measure_results_dfs,
            hei_data_df,
            report_request.measure_weights,
            stratification_vars=report_request.stratification_vars
        )
        
        # Generate report
        report_content = hei_calc.generate_equity_report(
            equity_results,
            report_format=report_request.report_format
        )
        
        # Determine penalty category
        overall_score = equity_results['overall_equity_score']
        if overall_score >= 70:
            penalty_category = "NO_PENALTY"
        elif overall_score >= 50:
            penalty_category = "MODERATE"
        else:
            penalty_category = "HIGH"
        
        # Extract key findings
        key_findings = []
        if equity_results['measures_with_disparities'] > 0:
            key_findings.append(f"{equity_results['measures_with_disparities']} measures have significant disparities")
        if overall_score < 70:
            key_findings.append(f"Equity score {overall_score:.1f} requires improvement")
        else:
            key_findings.append(f"Excellent equity performance (score: {overall_score:.1f})")
        
        # Get top priorities
        interventions = hei_calc.identify_priority_interventions(equity_results, top_n=3)
        top_priorities = [f"{i['measure']} - {i['target_group']}" for i in interventions[:3]]
        
        logger.info(f"Equity Report Complete | Format: {report_request.report_format} | "
                    f"Score: {overall_score:.1f} | Request-ID: {request_id}")
        
        return EquityReportResponse(
            request_id=request_id,
            report_format=report_request.report_format,
            report_content=report_content,
            overall_equity_score=overall_score,
            penalty_category=penalty_category,
            key_findings=key_findings,
            top_priorities=top_priorities,
            analysis_timestamp=datetime.utcnow().isoformat()
        )
        
    except Exception as e:
        logger.error(f"Equity Report Failed | Error: {str(e)} | Request-ID: {request_id}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Equity report generation failed: {str(e)}"
        )


"""
Phase 1 Database Integration
Query functions for Phase 1 HEDIS Portfolio Optimizer database views

Provides easy access to:
- Revenue at Risk calculations
- Gap Closure Velocity metrics
- ROI Analysis & Cost-per-Closure
- Member Segmentation
- Geographic Performance
"""

import os
import logging
from typing import Optional, Dict, List
import pandas as pd
import psycopg2
from psycopg2.extras import RealDictCursor

logger = logging.getLogger(__name__)

# Database configuration
DB_CONFIG = {
    "host": os.getenv("DB_HOST", "localhost"),
    "database": os.getenv("DB_NAME", "hedis_portfolio"),
    "user": os.getenv("DB_USER", "hedis_api"),
    "password": os.getenv("DB_PASSWORD", "hedis_password"),
    "port": os.getenv("DB_PORT", "5432")
}


def get_connection():
    """Get database connection."""
    try:
        return psycopg2.connect(**DB_CONFIG)
    except psycopg2.Error as e:
        logger.error(f"Database connection failed: {e}")
        raise


def query_to_dataframe(query: str, params: Optional[Dict] = None) -> pd.DataFrame:
    """
    Execute SQL query and return as DataFrame.
    
    Args:
        query: SQL query string
        params: Optional query parameters
        
    Returns:
        DataFrame with query results
    """
    conn = get_connection()
    try:
        df = pd.read_sql(query, conn, params=params)
        return df
    except Exception as e:
        logger.error(f"Query execution failed: {e}")
        raise
    finally:
        conn.close()


# ============================================================================
# Revenue at Risk Functions
# ============================================================================

def get_revenue_at_risk(plan_id: Optional[str] = None) -> pd.DataFrame:
    """
    Get revenue at risk data.
    
    Args:
        plan_id: Optional plan ID filter
        
    Returns:
        DataFrame with revenue at risk metrics
    """
    query = """
        SELECT 
            plan_id,
            plan_name,
            parent_organization,
            state,
            measure_id,
            measure_name,
            domain,
            star_weight,
            eligible_members,
            compliant_members,
            current_rate_pct,
            measure_current_stars,
            measure_target_stars,
            star_rating_gap,
            members_needed,
            target_threshold_pct,
            revenue_per_star_point,
            revenue_at_risk,
            weighted_revenue_impact,
            revenue_per_member_closed,
            measurement_year
        FROM vw_revenue_at_risk
    """
    
    if plan_id:
        query += f" WHERE plan_id = '{plan_id}'"
    
    query += " ORDER BY revenue_at_risk DESC"
    
    return query_to_dataframe(query)


def get_revenue_at_risk_summary(plan_id: Optional[str] = None) -> Dict:
    """
    Get summary of revenue at risk across all plans or for a specific plan.
    
    Args:
        plan_id: Optional plan ID filter
        
    Returns:
        Dictionary with summary metrics
    """
    query = """
        SELECT 
            COUNT(DISTINCT plan_id) as plan_count,
            COUNT(DISTINCT measure_id) as measure_count,
            SUM(revenue_at_risk) as total_revenue_at_risk,
            SUM(weighted_revenue_impact) as total_weighted_impact,
            SUM(members_needed) as total_members_needed,
            AVG(revenue_per_member_closed) as avg_revenue_per_member
        FROM vw_revenue_at_risk
    """
    
    if plan_id:
        query += f" WHERE plan_id = '{plan_id}'"
    
    df = query_to_dataframe(query)
    if df.empty:
        return {}
    
    return df.iloc[0].to_dict()


# ============================================================================
# Cost & ROI Functions
# ============================================================================

def get_cost_per_closure(plan_id: Optional[str] = None) -> pd.DataFrame:
    """
    Get cost per closure analysis.
    
    Args:
        plan_id: Optional plan ID filter
        
    Returns:
        DataFrame with cost metrics
    """
    query = """
        SELECT 
            plan_id,
            plan_name,
            measure_id,
            measure_name,
            domain,
            total_gaps_closed,
            total_intervention_cost,
            cost_per_gap_closed,
            revenue_per_star_point,
            roi_ratio,
            labor_costs,
            vendor_costs,
            admin_costs,
            tech_costs
        FROM vw_cost_per_closure
    """
    
    if plan_id:
        query += f" WHERE plan_id = '{plan_id}'"
    
    query += " ORDER BY cost_per_gap_closed"
    
    return query_to_dataframe(query)


def get_portfolio_roi(plan_id: Optional[str] = None) -> pd.DataFrame:
    """
    Get portfolio ROI analysis.
    
    Args:
        plan_id: Optional plan ID filter
        
    Returns:
        DataFrame with ROI metrics
    """
    query = """
        SELECT 
            plan_id,
            plan_name,
            measure_id,
            measure_name,
            potential_revenue,
            gaps_remaining,
            revenue_per_gap_remaining,
            gaps_closed,
            cost_to_date,
            cost_per_closure,
            projected_remaining_cost,
            total_projected_cost,
            projected_roi_ratio,
            net_revenue_impact
        FROM vw_portfolio_roi
    """
    
    if plan_id:
        query += f" WHERE plan_id = '{plan_id}'"
    
    query += " ORDER BY projected_roi_ratio DESC"
    
    return query_to_dataframe(query)


def get_budget_performance(plan_id: Optional[str] = None) -> pd.DataFrame:
    """
    Get budget performance metrics.
    
    Args:
        plan_id: Optional plan ID filter
        
    Returns:
        DataFrame with budget metrics
    """
    query = """
        SELECT 
            plan_id,
            plan_name,
            fiscal_year,
            budget_category,
            allocated_budget,
            spent_to_date,
            budget_remaining,
            burn_rate_monthly,
            projected_year_end,
            pct_budget_used,
            pct_projected_utilization,
            budget_status,
            months_runway_remaining
        FROM vw_budget_performance
    """
    
    if plan_id:
        query += f" WHERE plan_id = '{plan_id}'"
    
    query += " ORDER BY plan_id, budget_category"
    
    return query_to_dataframe(query)


# ============================================================================
# Velocity & Performance Functions
# ============================================================================

def get_current_velocity(plan_id: Optional[str] = None) -> pd.DataFrame:
    """
    Get current gap closure velocity metrics.
    
    Args:
        plan_id: Optional plan ID filter
        
    Returns:
        DataFrame with velocity metrics
    """
    query = """
        SELECT 
            plan_id,
            plan_name,
            measure_id,
            measure_name,
            domain,
            period_start_date,
            period_end_date,
            gaps_open_start,
            gaps_open_end,
            gaps_closed_period,
            net_gap_change,
            closure_rate_pct,
            avg_days_to_close,
            gaps_per_week,
            velocity_rating,
            closure_status,
            projected_gaps_year_end
        FROM vw_current_velocity
    """
    
    if plan_id:
        query += f" WHERE plan_id = '{plan_id}'"
    
    query += " ORDER BY plan_id, measure_id"
    
    return query_to_dataframe(query)


def get_velocity_trends(plan_id: Optional[str] = None) -> pd.DataFrame:
    """
    Get velocity trends (month-over-month).
    
    Args:
        plan_id: Optional plan ID filter
        
    Returns:
        DataFrame with trend data
    """
    query = """
        SELECT 
            plan_id,
            measure_id,
            current_period,
            current_velocity,
            prior_velocity,
            velocity_change,
            velocity_change_pct,
            current_closure_rate,
            prior_closure_rate,
            trend_direction
        FROM vw_velocity_trends
    """
    
    if plan_id:
        query += f" WHERE plan_id = '{plan_id}'"
    
    query += " ORDER BY plan_id, measure_id, current_period DESC"
    
    return query_to_dataframe(query)


# ============================================================================
# Member Segmentation Functions
# ============================================================================

def get_member_segmentation(plan_id: Optional[str] = None) -> pd.DataFrame:
    """
    Get member segmentation analysis.
    
    Args:
        plan_id: Optional plan ID filter
        
    Returns:
        DataFrame with segmentation data
    """
    query = """
        SELECT 
            plan_id,
            plan_name,
            region_type,
            risk_category,
            age_band,
            gender,
            member_count,
            avg_risk_score,
            avg_conditions_per_member,
            total_care_gaps,
            gaps_per_member
        FROM vw_member_segmentation
    """
    
    if plan_id:
        query += f" WHERE plan_id = '{plan_id}'"
    
    query += " ORDER BY member_count DESC"
    
    return query_to_dataframe(query)


def get_geographic_performance() -> pd.DataFrame:
    """
    Get geographic performance heat map data.
    
    Returns:
        DataFrame with geographic metrics
    """
    query = """
        SELECT 
            zip_code,
            city,
            region_type,
            population_density,
            member_count,
            avg_risk_score,
            total_gaps,
            open_gaps,
            closed_gaps,
            closure_rate_pct
        FROM vw_geographic_performance
        WHERE member_count > 0
        ORDER BY member_count DESC
    """
    
    return query_to_dataframe(query)


def get_condition_impact() -> pd.DataFrame:
    """
    Get chronic condition impact analysis.
    
    Returns:
        DataFrame with condition metrics
    """
    query = """
        SELECT 
            condition_code,
            condition_name,
            comorbidity_group,
            affected_members,
            prevalence_pct_actual,
            avg_risk_score,
            total_gaps,
            gaps_per_affected_member
        FROM vw_condition_impact
        ORDER BY affected_members DESC
    """
    
    return query_to_dataframe(query)


# ============================================================================
# Plan & Measure Reference Data
# ============================================================================

def get_plans() -> pd.DataFrame:
    """Get all MA plans."""
    query = """
        SELECT 
            plan_id,
            plan_name,
            parent_organization,
            state,
            total_enrollment,
            current_star_rating,
            prior_year_star_rating,
            quality_bonus_pct,
            monthly_premium_avg,
            is_active
        FROM ma_plans
        WHERE is_active = TRUE
        ORDER BY plan_id
    """
    
    return query_to_dataframe(query)


def get_measures() -> pd.DataFrame:
    """Get all HEDIS measures."""
    query = """
        SELECT 
            measure_id,
            measure_name,
            measure_description,
            domain,
            measure_type,
            star_weight,
            revenue_per_point,
            data_collection
        FROM hedis_measures
        ORDER BY measure_id
    """
    
    return query_to_dataframe(query)


def get_plan_performance(plan_id: Optional[str] = None, measure_id: Optional[str] = None) -> pd.DataFrame:
    """
    Get plan performance by measure.
    
    Args:
        plan_id: Optional plan ID filter
        measure_id: Optional measure ID filter
        
    Returns:
        DataFrame with performance data
    """
    query = """
        SELECT 
            pp.performance_id,
            pp.plan_id,
            mp.plan_name,
            pp.measure_id,
            hm.measure_name,
            pp.measurement_year,
            pp.denominator,
            pp.numerator,
            pp.performance_rate,
            pp.current_star_rating,
            pp.target_star_rating,
            pp.gap_to_target
        FROM plan_performance pp
        JOIN ma_plans mp ON pp.plan_id = mp.plan_id
        JOIN hedis_measures hm ON pp.measure_id = hm.measure_id
        WHERE pp.measurement_year = 2024
    """
    
    conditions = []
    if plan_id:
        conditions.append(f"pp.plan_id = '{plan_id}'")
    if measure_id:
        conditions.append(f"pp.measure_id = '{measure_id}'")
    
    if conditions:
        query += " AND " + " AND ".join(conditions)
    
    query += " ORDER BY pp.plan_id, pp.measure_id"
    
    return query_to_dataframe(query)


# ============================================================================
# Dashboard Summary Functions
# ============================================================================

def get_dashboard_summary(plan_id: Optional[str] = None) -> Dict:
    """
    Get comprehensive dashboard summary.
    
    Args:
        plan_id: Optional plan ID filter
        
    Returns:
        Dictionary with summary metrics
    """
    summary = {}
    
    # Revenue at Risk Summary (respects plan filter)
    rar_summary = get_revenue_at_risk_summary(plan_id)
    summary.update(rar_summary)
    
    # Member counts
    member_query = "SELECT COUNT(*) as count FROM plan_members WHERE member_id LIKE 'M%'"
    if plan_id:
        member_query += f" AND plan_id = '{plan_id}'"
    member_df = query_to_dataframe(member_query)
    summary['total_members'] = member_df.iloc[0]['count'] if not member_df.empty else 0
    
    # Gap counts
    gap_query = "SELECT COUNT(*) as count FROM member_gaps WHERE member_id LIKE 'M%'"
    if plan_id:
        gap_query += f" AND member_id IN (SELECT member_id FROM plan_members WHERE plan_id = '{plan_id}')"
    gap_df = query_to_dataframe(gap_query)
    summary['total_gaps'] = gap_df.iloc[0]['count'] if not gap_df.empty else 0
    
    # Plan count - show 1 if specific plan selected, otherwise total
    if plan_id:
        summary['total_plans'] = 1
    else:
        plan_query = "SELECT COUNT(*) as count FROM ma_plans WHERE is_active = TRUE"
        plan_df = query_to_dataframe(plan_query)
        summary['total_plans'] = plan_df.iloc[0]['count'] if not plan_df.empty else 0
    
    return summary


def test_connection() -> bool:
    """
    Test database connection.
    
    Returns:
        True if connection successful, False otherwise
    """
    try:
        conn = get_connection()
        conn.close()
        return True
    except Exception as e:
        logger.error(f"Connection test failed: {e}")
        return False


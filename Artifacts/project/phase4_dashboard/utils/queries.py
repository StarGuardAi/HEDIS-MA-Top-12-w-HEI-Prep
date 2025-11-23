"""
Phase 4 Dashboard - Phase 3 Demo Queries
SQL queries for Phase 3 ROI analysis visualizations
"""
from datetime import datetime


def get_roi_by_measure_query(start_date: str = "2024-10-01", end_date: str = "2024-12-31") -> str:
    """
    Query 1: ROI by Measure (Bar Chart)
    Returns: measure_code, measure_name, total_investment, revenue_impact, roi_ratio, successful_closures, total_interventions
    """
    return f"""
        SELECT 
            mi.measure_id as measure_code,
            hm.measure_name,
            ROUND(SUM(mi.cost_per_intervention) FILTER (WHERE mi.status = 'completed'), 2) as total_investment,
            COUNT(*) FILTER (WHERE mi.status = 'completed') * 100.0 as revenue_impact,
            CASE 
                WHEN SUM(mi.cost_per_intervention) FILTER (WHERE mi.status = 'completed') > 0 
                THEN ROUND((COUNT(*) FILTER (WHERE mi.status = 'completed') * 100.0) / 
                           SUM(mi.cost_per_intervention) FILTER (WHERE mi.status = 'completed'), 2)
                ELSE 0
            END as roi_ratio,
            COUNT(*) FILTER (WHERE mi.status = 'completed') as successful_closures,
            COUNT(*) as total_interventions
        FROM member_interventions mi
        LEFT JOIN hedis_measures hm ON mi.measure_id = hm.measure_id
        WHERE mi.intervention_date >= '{start_date}'
        AND mi.intervention_date <= '{end_date}'
        GROUP BY mi.measure_id, hm.measure_name
        ORDER BY roi_ratio DESC;
    """


def get_cost_per_closure_by_activity_query(start_date: str = "2024-10-01", end_date: str = "2024-12-31", min_uses: int = 10) -> str:
    """
    Query 2: Cost per Closure by Activity (Scatter Plot)
    Returns: activity_name, avg_cost, success_rate, times_used, successful_closures, cost_per_closure
    """
    return f"""
        SELECT 
            ia.activity_name,
            ROUND(AVG(mi.cost_per_intervention) FILTER (WHERE mi.status = 'completed'), 2) as avg_cost,
            ROUND(CAST(COUNT(*) FILTER (WHERE mi.status = 'completed') AS FLOAT) / NULLIF(COUNT(*), 0) * 100.0, 1) as success_rate,
            COUNT(*) as times_used,
            COUNT(*) FILTER (WHERE mi.status = 'completed') as successful_closures,
            ROUND(SUM(mi.cost_per_intervention) FILTER (WHERE mi.status = 'completed') / 
                  NULLIF(COUNT(*) FILTER (WHERE mi.status = 'completed'), 0), 2) as cost_per_closure
        FROM member_interventions mi
        INNER JOIN intervention_activities ia ON mi.activity_id = ia.activity_id
        WHERE mi.intervention_date >= '{start_date}'
        AND mi.intervention_date <= '{end_date}'
        GROUP BY ia.activity_id, ia.activity_name
        HAVING COUNT(*) >= {min_uses}
        ORDER BY avg_cost ASC;
    """


def get_monthly_intervention_trend_query(start_date: str = "2024-10-01", end_date: str = "2024-12-31") -> str:
    """
    Query 3: Monthly Intervention Trend (Line Chart)
    Returns: month, month_start, total_interventions, successful_closures, avg_cost, success_rate, total_investment
    """
    return f"""
        SELECT 
            TO_CHAR(mi.intervention_date, 'YYYY-MM') as month,
            DATE_TRUNC('month', mi.intervention_date)::DATE as month_start,
            COUNT(*) as total_interventions,
            COUNT(*) FILTER (WHERE mi.status = 'completed') as successful_closures,
            ROUND(AVG(mi.cost_per_intervention), 2) as avg_cost,
            ROUND(CAST(COUNT(*) FILTER (WHERE mi.status = 'completed') AS FLOAT) / NULLIF(COUNT(*), 0) * 100.0, 1) as success_rate,
            ROUND(SUM(mi.cost_per_intervention) FILTER (WHERE mi.status = 'completed'), 2) as total_investment
        FROM member_interventions mi
        WHERE mi.intervention_date >= '{start_date}'
        AND mi.intervention_date <= '{end_date}'
        GROUP BY DATE_TRUNC('month', mi.intervention_date), TO_CHAR(mi.intervention_date, 'YYYY-MM')
        ORDER BY month_start ASC;
    """


def get_budget_variance_by_measure_query(start_date: str = "2024-10-01", end_date: str = "2024-12-31") -> str:
    """
    Query 4: Budget Variance by Measure (Variance Chart)
    Returns: measure_code, measure_name, budget_allocated, actual_spent, variance, variance_pct, budget_status
    """
    return f"""
        SELECT 
            measure_code,
            measure_name,
            budget_allocated,
            actual_spent,
            variance,
            variance_pct,
            budget_status
        FROM (
            SELECT 
                ba.measure_id as measure_code,
                hm.measure_name,
                ba.budget_amount as budget_allocated,
                COALESCE(SUM(as_spend.amount_spent), 0) as actual_spent,
                COALESCE(SUM(as_spend.amount_spent), 0) - ba.budget_amount as variance,
                ROUND(((COALESCE(SUM(as_spend.amount_spent), 0) - ba.budget_amount) / NULLIF(ba.budget_amount, 0)) * 100, 1) as variance_pct,
                CASE 
                    WHEN COALESCE(SUM(as_spend.amount_spent), 0) > ba.budget_amount THEN 'Over Budget'
                    WHEN COALESCE(SUM(as_spend.amount_spent), 0) < ba.budget_amount THEN 'Under Budget'
                    ELSE 'On Budget'
                END as budget_status
            FROM budget_allocations ba
            LEFT JOIN hedis_measures hm ON ba.measure_id = hm.measure_id
            LEFT JOIN actual_spending as_spend ON ba.measure_id = as_spend.measure_id
                AND as_spend.spending_date >= ba.period_start
                AND as_spend.spending_date <= ba.period_end
            WHERE ba.period_start >= '{start_date}' 
            AND ba.period_end <= '{end_date}'
            GROUP BY ba.measure_id, hm.measure_name, ba.budget_amount, ba.period_start, ba.period_end
        ) subquery
        ORDER BY ABS(variance_pct) DESC;
    """


def get_cost_tier_comparison_query(start_date: str = "2024-10-01", end_date: str = "2024-12-31") -> str:
    """
    Query 5: Cost Tier Comparison (Grouped Bar Chart)
    Returns: cost_tier, avg_cost, success_rate, interventions_count, successful_closures, total_investment, cost_per_closure
    """
    return f"""
        WITH tiered_interventions AS (
            SELECT 
                mi.*,
                CASE 
                    WHEN mi.cost_per_intervention < 20 THEN 'Low Touch'
                    WHEN mi.cost_per_intervention < 90 THEN 'Medium Touch'
                    ELSE 'High Touch'
                END as cost_tier
            FROM member_interventions mi
            WHERE mi.intervention_date >= '{start_date}'
            AND mi.intervention_date <= '{end_date}'
        )
        SELECT 
            cost_tier,
            COUNT(intervention_id) as interventions_count,
            COUNT(CASE WHEN status = 'completed' THEN 1 END) as successful_closures,
            ROUND(AVG(cost_per_intervention), 2) as avg_cost,
            ROUND(
                CAST(COUNT(CASE WHEN status = 'completed' THEN 1 END) AS FLOAT) / 
                NULLIF(COUNT(intervention_id), 0) * 100,
                1
            ) as success_rate,
            ROUND(SUM(cost_per_intervention) FILTER (WHERE status = 'completed'), 2) as total_investment,
            ROUND(
                SUM(cost_per_intervention) FILTER (WHERE status = 'completed') / 
                NULLIF(COUNT(CASE WHEN status = 'completed' THEN 1 END), 0),
                2
            ) as cost_per_closure
        FROM tiered_interventions
        GROUP BY cost_tier
        ORDER BY 
            CASE cost_tier
                WHEN 'Low Touch' THEN 1
                WHEN 'Medium Touch' THEN 2
                WHEN 'High Touch' THEN 3
            END;
    """


def get_portfolio_summary_query(start_date: str = "2024-10-01", end_date: str = "2024-12-31") -> str:
    """
    Get overall portfolio KPIs for home page
    Returns: total_investment, total_closures, avg_roi, net_benefit
    """
    return f"""
        SELECT 
            ROUND(SUM(mi.cost_per_intervention) FILTER (WHERE mi.status = 'completed'), 2) as total_investment,
            COUNT(*) FILTER (WHERE mi.status = 'completed') as total_closures,
            COUNT(*) FILTER (WHERE mi.status = 'completed') * 100.0 as revenue_impact,
            CASE 
                WHEN SUM(mi.cost_per_intervention) FILTER (WHERE mi.status = 'completed') > 0 
                THEN ROUND((COUNT(*) FILTER (WHERE mi.status = 'completed') * 100.0) / 
                           SUM(mi.cost_per_intervention) FILTER (WHERE mi.status = 'completed'), 2)
                ELSE 0
            END as roi_ratio,
            (COUNT(*) FILTER (WHERE mi.status = 'completed') * 100.0) - 
            SUM(mi.cost_per_intervention) FILTER (WHERE mi.status = 'completed') as net_benefit,
            COUNT(*) as total_interventions,
            ROUND(COUNT(*) FILTER (WHERE mi.status = 'completed')::DECIMAL / COUNT(*) * 100, 1) as overall_success_rate
        FROM member_interventions mi
        WHERE mi.intervention_date >= '{start_date}'
        AND mi.intervention_date <= '{end_date}';
    """


-- ============================================================================
-- PHASE 3 DEMO VISUALIZATION QUERIES
-- Export-ready queries for Excel, Tableau, or other visualization tools
-- ============================================================================

-- ============================================================================
-- QUERY 1: ROI BY MEASURE (Bar Chart)
-- ============================================================================
-- Columns: measure_code, measure_name, total_investment, revenue_impact, roi_ratio
-- Sort by ROI ratio descending
-- ============================================================================

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
WHERE mi.intervention_date >= '2024-10-01'
AND mi.intervention_date <= '2024-12-31'
GROUP BY mi.measure_id, hm.measure_name
ORDER BY roi_ratio DESC;

-- ============================================================================
-- QUERY 2: COST PER CLOSURE BY ACTIVITY (Scatter Plot)
-- ============================================================================
-- Columns: activity_name, avg_cost (x-axis), success_rate (y-axis), times_used (bubble size)
-- Include only activities with 10+ uses
-- ============================================================================

SELECT 
    ia.activity_name,
    ROUND(AVG(mi.cost_per_intervention) FILTER (WHERE mi.status = 'completed'), 2) as avg_cost,
    ROUND(COUNT(*) FILTER (WHERE mi.status = 'completed')::DECIMAL / COUNT(*) * 100, 1) as success_rate,
    COUNT(*) as times_used,
    COUNT(*) FILTER (WHERE mi.status = 'completed') as successful_closures,
    ROUND(SUM(mi.cost_per_intervention) FILTER (WHERE mi.status = 'completed') / 
          NULLIF(COUNT(*) FILTER (WHERE mi.status = 'completed'), 0), 2) as cost_per_closure
FROM member_interventions mi
INNER JOIN intervention_activities ia ON mi.activity_id = ia.activity_id
WHERE mi.intervention_date >= '2024-10-01'
AND mi.intervention_date <= '2024-12-31'
GROUP BY ia.activity_id, ia.activity_name
HAVING COUNT(*) >= 10
ORDER BY avg_cost ASC;

-- ============================================================================
-- QUERY 3: MONTHLY INTERVENTION TREND (Line Chart)
-- ============================================================================
-- Columns: month, total_interventions, successful_closures, avg_cost, success_rate
-- Group by month in Q4 2024
-- ============================================================================

SELECT 
    TO_CHAR(mi.intervention_date, 'YYYY-MM') as month,
    DATE_TRUNC('month', mi.intervention_date)::DATE as month_start,
    COUNT(*) as total_interventions,
    COUNT(*) FILTER (WHERE mi.status = 'completed') as successful_closures,
    ROUND(AVG(mi.cost_per_intervention), 2) as avg_cost,
    ROUND(COUNT(*) FILTER (WHERE mi.status = 'completed')::DECIMAL / COUNT(*) * 100, 1) as success_rate,
    ROUND(SUM(mi.cost_per_intervention) FILTER (WHERE mi.status = 'completed'), 2) as total_investment
FROM member_interventions mi
WHERE mi.intervention_date >= '2024-10-01'
AND mi.intervention_date <= '2024-12-31'
GROUP BY DATE_TRUNC('month', mi.intervention_date), TO_CHAR(mi.intervention_date, 'YYYY-MM')
ORDER BY month_start ASC;

-- ============================================================================
-- QUERY 4: BUDGET VARIANCE BY MEASURE (Variance Chart)
-- ============================================================================
-- Columns: measure_code, budget_allocated, actual_spent, variance, variance_pct
-- Sort by variance percentage
-- ============================================================================

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
    WHERE ba.period_start >= '2024-10-01' 
    AND ba.period_end <= '2024-12-31'
    GROUP BY ba.measure_id, hm.measure_name, ba.budget_amount, ba.period_start, ba.period_end
) subquery
ORDER BY ABS(variance_pct) DESC;

-- ============================================================================
-- QUERY 5: COST TIER COMPARISON (Grouped Bar Chart)
-- ============================================================================
-- Columns: cost_tier, avg_cost, success_rate, interventions_count
-- Compare low/medium/high touch
-- ============================================================================

WITH intervention_tiers AS (
    SELECT 
        mi.*,
        ia.activity_name,
        CASE 
            WHEN mi.cost_per_intervention <= 25 THEN 'Low Touch'
            WHEN mi.cost_per_intervention <= 75 THEN 'Medium Touch'
            ELSE 'High Touch'
        END as cost_tier
    FROM member_interventions mi
    INNER JOIN intervention_activities ia ON mi.activity_id = ia.activity_id
    WHERE mi.intervention_date >= '2024-10-01'
    AND mi.intervention_date <= '2024-12-31'
)
SELECT 
    cost_tier,
    ROUND(AVG(cost_per_intervention), 2) as avg_cost,
    ROUND(COUNT(*) FILTER (WHERE status = 'completed')::DECIMAL / COUNT(*) * 100, 1) as success_rate,
    COUNT(*) as interventions_count,
    COUNT(*) FILTER (WHERE status = 'completed') as successful_closures,
    ROUND(SUM(cost_per_intervention) FILTER (WHERE status = 'completed'), 2) as total_investment,
    ROUND(SUM(cost_per_intervention) FILTER (WHERE status = 'completed') / 
          NULLIF(COUNT(*) FILTER (WHERE status = 'completed'), 0), 2) as cost_per_closure
FROM intervention_tiers
GROUP BY cost_tier
ORDER BY 
    CASE cost_tier
        WHEN 'Low Touch' THEN 1
        WHEN 'Medium Touch' THEN 2
        WHEN 'High Touch' THEN 3
    END;


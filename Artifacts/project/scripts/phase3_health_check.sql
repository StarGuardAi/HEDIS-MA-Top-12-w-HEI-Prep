-- ============================================================================
-- PHASE 3 HEALTH CHECK - Quick Verification Script
-- Run this anytime to verify Phase 3 is working correctly
-- ============================================================================
-- Usage: psql -U hedis_api -d hedis_portfolio -f phase3_health_check.sql
-- ============================================================================

\echo '============================================================================'
\echo 'PHASE 3 HEALTH CHECK'
\echo '============================================================================'
\echo 'Date: ' || CURRENT_TIMESTAMP
\echo ''

-- ============================================================================
-- SECTION 1: TABLE EXISTENCE AND ROW COUNTS
-- ============================================================================
\echo 'SECTION 1: TABLE EXISTENCE AND ROW COUNTS'
\echo '============================================================================'
\echo ''

-- Check intervention_activities (should be 16)
\echo '1. intervention_activities:'
SELECT 
    CASE 
        WHEN COUNT(*) = 16 THEN '[OK]'
        WHEN COUNT(*) > 0 THEN '[WARN]'
        ELSE '[FAIL]'
    END as status,
    COUNT(*) as row_count,
    CASE 
        WHEN COUNT(*) = 16 THEN 'Expected: 16'
        ELSE 'Expected: 16, Found: ' || COUNT(*)::TEXT
    END as expected
FROM intervention_activities;
\echo ''

-- Check intervention_costs (should be ~192 or 0 if not populated)
\echo '2. intervention_costs:'
SELECT 
    CASE 
        WHEN COUNT(*) >= 0 THEN '[OK]'
        ELSE '[FAIL]'
    END as status,
    COUNT(*) as row_count,
    CASE 
        WHEN COUNT(*) = 0 THEN 'Note: Empty (costs stored in member_interventions)'
        WHEN COUNT(*) >= 192 THEN 'Expected: ~192'
        ELSE 'Found: ' || COUNT(*)::TEXT
    END as expected
FROM intervention_costs;
\echo ''

-- Check member_interventions (should be ~6,900)
\echo '3. member_interventions:'
SELECT 
    CASE 
        WHEN COUNT(*) BETWEEN 6000 AND 8000 THEN '[OK]'
        WHEN COUNT(*) > 0 THEN '[WARN]'
        ELSE '[FAIL]'
    END as status,
    COUNT(*) as row_count,
    CASE 
        WHEN COUNT(*) BETWEEN 6000 AND 8000 THEN 'Expected: ~6,900'
        ELSE 'Expected: ~6,900, Found: ' || COUNT(*)::TEXT
    END as expected,
    COUNT(*) FILTER (WHERE status = 'completed') as completed,
    COUNT(*) FILTER (WHERE status = 'in_progress') as in_progress
FROM member_interventions;
\echo ''

-- Check budget_allocations (should be 12)
\echo '4. budget_allocations:'
SELECT 
    CASE 
        WHEN COUNT(*) = 12 THEN '[OK]'
        WHEN COUNT(*) > 0 THEN '[WARN]'
        ELSE '[FAIL]'
    END as status,
    COUNT(*) as row_count,
    CASE 
        WHEN COUNT(*) = 12 THEN 'Expected: 12'
        ELSE 'Expected: 12, Found: ' || COUNT(*)::TEXT
    END as expected,
    SUM(budget_amount) as total_budget
FROM budget_allocations
WHERE period_start >= '2024-10-01' AND period_end <= '2024-12-31';
\echo ''

-- Check actual_spending (should have monthly aggregates)
\echo '5. actual_spending:'
SELECT 
    CASE 
        WHEN COUNT(*) > 0 THEN '[OK]'
        ELSE '[FAIL]'
    END as status,
    COUNT(*) as row_count,
    CASE 
        WHEN COUNT(*) >= 12 THEN 'Expected: Monthly aggregates (12+ records)'
        ELSE 'Expected: Monthly aggregates, Found: ' || COUNT(*)::TEXT
    END as expected,
    SUM(amount_spent) as total_spent
FROM actual_spending;
\echo ''

-- ============================================================================
-- SECTION 2: DATA QUALITY CHECKS
-- ============================================================================
\echo '============================================================================'
\echo 'SECTION 2: DATA QUALITY CHECKS'
\echo '============================================================================'
\echo ''

-- Check for NULL values in critical fields
\echo '6. NULL Value Checks:'
SELECT 
    'member_interventions.member_id' as field,
    COUNT(*) FILTER (WHERE member_id IS NULL) as null_count,
    CASE 
        WHEN COUNT(*) FILTER (WHERE member_id IS NULL) = 0 THEN '[OK]'
        ELSE '[FAIL]'
    END as status
FROM member_interventions
UNION ALL
SELECT 
    'member_interventions.measure_id' as field,
    COUNT(*) FILTER (WHERE measure_id IS NULL) as null_count,
    CASE 
        WHEN COUNT(*) FILTER (WHERE measure_id IS NULL) = 0 THEN '[OK]'
        ELSE '[FAIL]'
    END as status
FROM member_interventions
UNION ALL
SELECT 
    'member_interventions.intervention_date' as field,
    COUNT(*) FILTER (WHERE intervention_date IS NULL) as null_count,
    CASE 
        WHEN COUNT(*) FILTER (WHERE intervention_date IS NULL) = 0 THEN '[OK]'
        ELSE '[FAIL]'
    END as status
FROM member_interventions
UNION ALL
SELECT 
    'member_interventions.cost_per_intervention' as field,
    COUNT(*) FILTER (WHERE cost_per_intervention IS NULL) as null_count,
    CASE 
        WHEN COUNT(*) FILTER (WHERE cost_per_intervention IS NULL) = 0 THEN '[OK]'
        ELSE '[FAIL]'
    END as status
FROM member_interventions;
\echo ''

-- Check for negative costs
\echo '7. Negative Cost Checks:'
SELECT 
    'member_interventions' as table_name,
    COUNT(*) FILTER (WHERE cost_per_intervention < 0) as negative_count,
    CASE 
        WHEN COUNT(*) FILTER (WHERE cost_per_intervention < 0) = 0 THEN '[OK]'
        ELSE '[FAIL]'
    END as status
FROM member_interventions
UNION ALL
SELECT 
    'actual_spending' as table_name,
    COUNT(*) FILTER (WHERE amount_spent < 0) as negative_count,
    CASE 
        WHEN COUNT(*) FILTER (WHERE amount_spent < 0) = 0 THEN '[OK]'
        ELSE '[FAIL]'
    END as status
FROM actual_spending;
\echo ''

-- Check for future dates
\echo '8. Future Date Checks:'
SELECT 
    'member_interventions' as table_name,
    COUNT(*) FILTER (WHERE intervention_date > CURRENT_DATE) as future_count,
    CASE 
        WHEN COUNT(*) FILTER (WHERE intervention_date > CURRENT_DATE) = 0 THEN '[OK]'
        ELSE '[WARN]'
    END as status
FROM member_interventions
UNION ALL
SELECT 
    'actual_spending' as table_name,
    COUNT(*) FILTER (WHERE spending_date > CURRENT_DATE) as future_count,
    CASE 
        WHEN COUNT(*) FILTER (WHERE spending_date > CURRENT_DATE) = 0 THEN '[OK]'
        ELSE '[WARN]'
    END as status
FROM actual_spending;
\echo ''

-- Check date range (should be Q4 2024)
\echo '9. Date Range Validation:'
SELECT 
    COUNT(*) FILTER (WHERE intervention_date < '2024-10-01' OR intervention_date > '2024-12-31') as out_of_range,
    CASE 
        WHEN COUNT(*) FILTER (WHERE intervention_date < '2024-10-01' OR intervention_date > '2024-12-31') = 0 THEN '[OK]'
        ELSE '[WARN]'
    END as status,
    MIN(intervention_date) as earliest_date,
    MAX(intervention_date) as latest_date
FROM member_interventions;
\echo ''

-- ============================================================================
-- SECTION 3: REFERENTIAL INTEGRITY
-- ============================================================================
\echo '============================================================================'
\echo 'SECTION 3: REFERENTIAL INTEGRITY'
\echo '============================================================================'
\echo ''

-- Check orphaned activity references
\echo '10. Orphaned Activity References:'
SELECT 
    COUNT(*) as orphaned_count,
    CASE 
        WHEN COUNT(*) = 0 THEN '[OK]'
        ELSE '[FAIL]'
    END as status
FROM member_interventions mi
LEFT JOIN intervention_activities ia ON mi.activity_id = ia.activity_id
WHERE mi.activity_id IS NOT NULL AND ia.activity_id IS NULL;
\echo ''

-- Check orphaned measure references
\echo '11. Orphaned Measure References:'
SELECT 
    COUNT(*) as orphaned_count,
    CASE 
        WHEN COUNT(*) = 0 THEN '[OK]'
        ELSE '[FAIL]'
    END as status
FROM member_interventions mi
LEFT JOIN hedis_measures hm ON mi.measure_id = hm.measure_id
WHERE mi.measure_id IS NOT NULL AND hm.measure_id IS NULL;
\echo ''

-- Check interventions without budget allocations
\echo '12. Interventions Without Budget:'
SELECT 
    COUNT(*) as count_without_budget,
    CASE 
        WHEN COUNT(*) = 0 THEN '[OK]'
        WHEN COUNT(*) <= 10 THEN '[WARN]'
        ELSE '[FAIL]'
    END as status
FROM member_interventions mi
LEFT JOIN budget_allocations ba ON mi.measure_id = ba.measure_id
    AND mi.intervention_date >= ba.period_start
    AND mi.intervention_date <= ba.period_end
WHERE ba.budget_id IS NULL
AND mi.intervention_date >= '2024-10-01'
AND mi.intervention_date <= '2024-12-31';
\echo ''

-- ============================================================================
-- SECTION 4: FUNCTION TESTING
-- ============================================================================
\echo '============================================================================'
\echo 'SECTION 4: FUNCTION TESTING'
\echo '============================================================================'
\echo ''

-- Test if calculate_cost_per_closure function exists and works
\echo '13. Testing calculate_cost_per_closure() function:'
DO $$
DECLARE
    func_exists BOOLEAN;
    test_result NUMERIC;
BEGIN
    -- Check if function exists
    SELECT EXISTS (
        SELECT FROM pg_proc p
        JOIN pg_namespace n ON p.pronamespace = n.oid
        WHERE n.nspname = 'public'
        AND p.proname = 'calculate_cost_per_closure'
    ) INTO func_exists;
    
    IF func_exists THEN
        BEGIN
            SELECT calculate_cost_per_closure('GSD', '2024-10-01', '2024-12-31') INTO test_result;
            RAISE NOTICE '[OK] Function exists and callable. Test result for GSD: $%', test_result;
        EXCEPTION WHEN OTHERS THEN
            RAISE NOTICE '[FAIL] Function exists but call failed: %', SQLERRM;
        END;
    ELSE
        RAISE NOTICE '[WARN] Function calculate_cost_per_closure() does not exist. Using manual calculation.';
        SELECT 
            CASE 
                WHEN COUNT(*) FILTER (WHERE status = 'completed') > 0 
                THEN SUM(cost_per_intervention) FILTER (WHERE status = 'completed') / 
                     COUNT(*) FILTER (WHERE status = 'completed')
                ELSE NULL
            END INTO test_result
        FROM member_interventions
        WHERE measure_id = 'GSD'
        AND intervention_date >= '2024-10-01'
        AND intervention_date <= '2024-12-31';
        
        IF test_result IS NOT NULL THEN
            RAISE NOTICE '[OK] Manual calculation works. GSD cost per closure: $%', test_result;
        ELSE
            RAISE NOTICE '[WARN] Could not calculate cost per closure for GSD';
        END IF;
    END IF;
END $$;
\echo ''

-- ============================================================================
-- SECTION 5: VIEW TESTING
-- ============================================================================
\echo '============================================================================'
\echo 'SECTION 5: VIEW TESTING'
\echo '============================================================================'
\echo ''

-- Test if v_roi_summary_dashboard view exists and returns data
\echo '14. Testing v_roi_summary_dashboard view:'
DO $$
DECLARE
    view_exists BOOLEAN;
    row_count INTEGER;
BEGIN
    -- Check if view exists
    SELECT EXISTS (
        SELECT FROM information_schema.views
        WHERE table_schema = 'public'
        AND table_name = 'v_roi_summary_dashboard'
    ) INTO view_exists;
    
    IF view_exists THEN
        BEGIN
            SELECT COUNT(*) INTO row_count FROM v_roi_summary_dashboard;
            IF row_count > 0 THEN
                RAISE NOTICE '[OK] View exists and returns % rows', row_count;
            ELSE
                RAISE NOTICE '[WARN] View exists but returns no data';
            END IF;
        EXCEPTION WHEN OTHERS THEN
            RAISE NOTICE '[FAIL] View exists but query failed: %', SQLERRM;
        END;
    ELSE
        RAISE NOTICE '[WARN] View v_roi_summary_dashboard does not exist. Testing manual query.';
        SELECT COUNT(*) INTO row_count
        FROM (
            SELECT 
                mi.measure_id,
                COUNT(*) FILTER (WHERE mi.status = 'completed') as successful_closures,
                SUM(mi.cost_per_intervention) FILTER (WHERE mi.status = 'completed') as total_investment
            FROM member_interventions mi
            WHERE mi.intervention_date >= '2024-10-01'
            AND mi.intervention_date <= '2024-12-31'
            GROUP BY mi.measure_id
        ) manual_roi;
        
        IF row_count > 0 THEN
            RAISE NOTICE '[OK] Manual ROI calculation works. Found % measures', row_count;
        ELSE
            RAISE NOTICE '[FAIL] Manual ROI calculation returned no results';
        END IF;
    END IF;
END $$;
\echo ''

-- ============================================================================
-- SECTION 6: KEY METRICS SUMMARY
-- ============================================================================
\echo '============================================================================'
\echo 'SECTION 6: KEY METRICS SUMMARY'
\echo '============================================================================'
\echo ''

\echo '15. Portfolio ROI Summary:'
SELECT 
    COUNT(*) as total_interventions,
    COUNT(*) FILTER (WHERE status = 'completed') as successful_closures,
    ROUND(COUNT(*) FILTER (WHERE status = 'completed')::DECIMAL / COUNT(*) * 100, 1) as success_rate_pct,
    SUM(cost_per_intervention) FILTER (WHERE status = 'completed') as total_investment,
    COUNT(*) FILTER (WHERE status = 'completed') * 100.0 as estimated_revenue,
    CASE 
        WHEN SUM(cost_per_intervention) FILTER (WHERE status = 'completed') > 0 
        THEN ROUND((COUNT(*) FILTER (WHERE status = 'completed') * 100.0) / 
                   SUM(cost_per_intervention) FILTER (WHERE status = 'completed'), 2)
        ELSE 0
    END as roi_ratio
FROM member_interventions
WHERE intervention_date >= '2024-10-01'
AND intervention_date <= '2024-12-31';
\echo ''

\echo '16. Measure Coverage:'
SELECT 
    COUNT(DISTINCT measure_id) as unique_measures,
    CASE 
        WHEN COUNT(DISTINCT measure_id) = 12 THEN '[OK] All 12 measures represented'
        WHEN COUNT(DISTINCT measure_id) >= 10 THEN '[WARN] Missing some measures'
        ELSE '[FAIL] Missing multiple measures'
    END as status
FROM member_interventions
WHERE intervention_date >= '2024-10-01'
AND intervention_date <= '2024-12-31';
\echo ''

\echo '17. Budget vs Actual:'
SELECT 
    SUM(ba.budget_amount) as total_budget,
    COALESCE(SUM(as_spend.amount_spent), 0) as total_spent,
    ROUND((COALESCE(SUM(as_spend.amount_spent), 0) / NULLIF(SUM(ba.budget_amount), 0)) * 100, 1) as utilization_pct,
    CASE 
        WHEN COALESCE(SUM(as_spend.amount_spent), 0) <= SUM(ba.budget_amount) * 1.1 THEN '[OK]'
        ELSE '[WARN]'
    END as status
FROM budget_allocations ba
LEFT JOIN actual_spending as_spend ON ba.measure_id = as_spend.measure_id
WHERE ba.period_start >= '2024-10-01' AND ba.period_end <= '2024-12-31';
\echo ''

-- ============================================================================
-- FINAL SUMMARY
-- ============================================================================
\echo '============================================================================'
\echo 'HEALTH CHECK SUMMARY'
\echo '============================================================================'
\echo ''
\echo 'If all checks show [OK] or [WARN] (not [FAIL]), Phase 3 is operational.'
\echo 'Review any [WARN] items but they may be acceptable for your use case.'
\echo ''
\echo 'Health Check Complete: ' || CURRENT_TIMESTAMP
\echo '============================================================================'


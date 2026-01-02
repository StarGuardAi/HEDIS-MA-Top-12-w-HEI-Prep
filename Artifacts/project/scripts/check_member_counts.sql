-- ============================================================================
-- CHECK CURRENT DATABASE MEMBER COUNTS
-- Use this to verify current data scale before recalibration
-- ============================================================================

-- Check members count
SELECT 'plan_members' as table_name, COUNT(*) as record_count 
FROM plan_members
UNION ALL
SELECT 'plan_members (active only)' as table_name, COUNT(*) as record_count 
FROM plan_members 
WHERE is_active = TRUE
UNION ALL
SELECT 'member_gaps' as table_name, COUNT(*) as record_count 
FROM member_gaps
UNION ALL
SELECT 'member_interventions' as table_name, COUNT(*) as record_count 
FROM member_interventions
UNION ALL
SELECT 'member_interventions (Q4 2024)' as table_name, COUNT(*) as record_count 
FROM member_interventions
WHERE intervention_date >= '2024-10-01' 
AND intervention_date <= '2024-12-31';

-- Additional context queries
SELECT 
    'Plan Info' as info_type,
    plan_id,
    plan_name,
    total_enrollment,
    current_star_rating,
    prior_year_star_rating
FROM ma_plans
ORDER BY plan_id
LIMIT 5;

-- Check if plan_context table exists
SELECT 
    EXISTS (
        SELECT FROM information_schema.tables 
        WHERE table_schema = 'public' 
        AND table_name = 'plan_context'
    ) as plan_context_exists;



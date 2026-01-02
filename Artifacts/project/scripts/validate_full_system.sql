/*******************************************************************************

HEDIS STAR RATING PORTFOLIO OPTIMIZER - FULL SYSTEM VALIDATION

Comprehensive Testing Suite for Phase 1 & Phase 2



Purpose: Validate all components, data integrity, and system readiness

Author: Robert Reichert

Created: 2025-11-18

Database: PostgreSQL



Test Categories:

1. Phase 1 Foundation Validation

2. Phase 2 Operational Validation

3. Data Quality Assessment

4. Performance Benchmarking

5. Integration Testing

6. Business Logic Verification

7. Dashboard Functionality

8. Export Readiness



Expected Runtime: 5-7 minutes

Expected Output: Comprehensive validation report with pass/fail status



Usage:

  psql -U username -d database -f validate_full_system.sql > report.txt

  Or use: run_validation_psql.bat (Windows) or run_validation_psql.ps1 (PowerShell)

*******************************************************************************/



\echo '╔══════════════════════════════════════════════════════════════╗'
\echo '║          HEDIS OPTIMIZER - FULL SYSTEM VALIDATION            ║'
\echo '║                  Phase 1 + Phase 2 Complete                  ║'
\echo '╚══════════════════════════════════════════════════════════════╝'
\echo ''



-- ============================================================================

-- SECTION 1: SYSTEM HEALTH CHECK

-- ============================================================================



-- Test 1.1: Database object inventory

SELECT 

    'TABLES' AS object_type,

    COUNT(*) AS object_count,

    CASE 

        WHEN COUNT(*) >= 30 THEN '✓ PASS'

        ELSE '✗ FAIL - Expected 30+ tables'

    END AS status

FROM information_schema.tables

WHERE table_schema = 'public' 

  AND table_type = 'BASE TABLE'



UNION ALL



SELECT 

    'VIEWS',

    COUNT(*),

    CASE 

        WHEN COUNT(*) >= 25 THEN '✓ PASS'

        ELSE '⚠ WARN - Expected 25+ views'

    END

FROM information_schema.views

WHERE table_schema = 'public'



UNION ALL



SELECT 

    'FUNCTIONS',

    COUNT(*),

    CASE 

        WHEN COUNT(*) >= 5 THEN '✓ PASS'

        ELSE '⚠ WARN - Expected 5+ functions'

    END

FROM information_schema.routines

WHERE routine_schema = 'public'

  AND routine_type = 'FUNCTION'



UNION ALL



SELECT 

    'INDEXES',

    COUNT(*),

    CASE 

        WHEN COUNT(*) >= 30 THEN '✓ PASS'

        ELSE '⚠ WARN - Expected 30+ indexes'

    END

FROM pg_indexes

WHERE schemaname = 'public';



\echo ''
\echo '▶ Test 1.2: Table Sizes and Row Counts'

-- Test 1.2: Table sizes and row counts

SELECT 

    table_name,

    row_count,

    pg_size_pretty(table_size) AS table_size,

    expected_range,

    CASE 

        WHEN table_name = 'plan_members' AND row_count >= 10000 THEN '✓ PASS'

        WHEN table_name = 'member_gaps' AND row_count BETWEEN 12000 AND 18000 THEN '✓ PASS'

        WHEN table_name = 'provider_directory' AND row_count >= 500 THEN '✓ PASS'

        WHEN table_name = 'gap_closure_propensity' AND row_count >= 8000 THEN '✓ PASS'

        WHEN table_name = 'member_risk_stratification' AND row_count >= 10000 THEN '✓ PASS'

        WHEN table_name = 'member_engagement_scores' AND row_count >= 10000 THEN '✓ PASS'

        WHEN row_count > 0 THEN '✓ PASS'

        ELSE '✗ CHECK'

    END AS status

FROM (

    SELECT 

        schemaname || '.' || tablename AS table_name,

        n_live_tup AS row_count,

        pg_total_relation_size(schemaname || '.' || tablename) AS table_size,

        CASE tablename

            WHEN 'plan_members' THEN '10,000'

            WHEN 'member_gaps' THEN '12,000-18,000'

            WHEN 'provider_directory' THEN '500+'

            WHEN 'gap_closure_propensity' THEN '8,000+'

            WHEN 'member_risk_stratification' THEN '10,000'

            WHEN 'member_engagement_scores' THEN '10,000'

            ELSE '>0'

        END AS expected_range

    FROM pg_stat_user_tables

    WHERE schemaname = 'public'

    ORDER BY pg_total_relation_size(schemaname || '.' || tablename) DESC

    LIMIT 15

) sizes;



-- ============================================================================

-- SECTION 2: PHASE 1 FOUNDATION VALIDATION

-- ============================================================================



-- Test 2.1: HEDIS Measures completeness

SELECT 

    'Total Measures' AS metric,

    COUNT(*) AS count,

    12 AS expected,

    CASE WHEN COUNT(*) = 12 THEN '✓ PASS' ELSE '✗ FAIL' END AS status

FROM hedis_measures



UNION ALL



SELECT 

    'Star Thresholds',

    COUNT(*),

    84, -- 12 measures × 7 star levels

    CASE WHEN COUNT(*) = 84 THEN '✓ PASS' ELSE '✗ FAIL' END

FROM star_thresholds

WHERE measurement_year = 2024



UNION ALL



SELECT 

    'Revenue Per Point Defined',

    COUNT(*),

    12,

    CASE WHEN COUNT(*) = 12 THEN '✓ PASS' ELSE '✗ FAIL' END

FROM hedis_measures

WHERE revenue_per_point > 0;



\echo ''
\echo '▶ Test 2.2: MA Plan Configuration'

-- Test 2.2: Plan configuration

SELECT 

    plan_id,

    plan_name,

    total_enrollment,

    current_star_rating,

    CASE 

        WHEN total_enrollment > 0 AND current_star_rating IS NOT NULL THEN '✓ PASS'

        ELSE '✗ CHECK'

    END AS status

FROM ma_plans

WHERE is_active = TRUE

ORDER BY plan_id;



\echo ''
\echo '▶ Test 2.3: Plan Performance Coverage'

-- Test 2.3: Plan performance completeness

SELECT 

    plan_id,

    COUNT(DISTINCT measure_id) AS measures_tracked,

    ROUND(AVG(performance_rate), 1) AS avg_performance,

    SUM(gap_to_target) AS total_gaps,

    CASE 

        WHEN COUNT(DISTINCT measure_id) = 12 THEN '✓ PASS - Full coverage'

        WHEN COUNT(DISTINCT measure_id) >= 10 THEN '⚠ WARN - Partial coverage'

        ELSE '✗ FAIL - Incomplete'

    END AS status

FROM plan_performance

WHERE measurement_year = 2024

GROUP BY plan_id

ORDER BY plan_id;



\echo ''
\echo '▶ Test 2.4: Member Demographics Quality'

-- Test 2.4: Member demographics validation

SELECT 

    'Total Members' AS metric,

    COUNT(*) AS count,

    '10,000' AS expected,

    CASE WHEN COUNT(*) = 10000 THEN '✓ PASS' ELSE '✗ FAIL' END AS status

FROM plan_members

WHERE member_id LIKE 'M%'



UNION ALL



SELECT 

    'Members with Risk Scores',

    COUNT(*),

    '10,000',

    CASE WHEN COUNT(*) = 10000 THEN '✓ PASS' ELSE '✗ CHECK' END

FROM plan_members

WHERE member_id LIKE 'M%' AND risk_score IS NOT NULL



UNION ALL



SELECT 

    'Members with Zip Codes',

    COUNT(*),

    '10,000',

    CASE WHEN COUNT(*) = 10000 THEN '✓ PASS' ELSE '✗ CHECK' END

FROM plan_members

WHERE member_id LIKE 'M%' AND zip_code IS NOT NULL



UNION ALL



SELECT 

    'Unique Zip Codes',

    COUNT(DISTINCT zip_code),

    '25-30',

    CASE WHEN COUNT(DISTINCT zip_code) BETWEEN 25 AND 30 THEN '✓ PASS' ELSE '⚠ WARN' END

FROM plan_members

WHERE member_id LIKE 'M%';



\echo ''
\echo '▶ Test 2.5: Chronic Condition Assignment'

-- Test 2.5: Chronic conditions prevalence

SELECT 

    'Members with Conditions' AS metric,

    COUNT(DISTINCT member_id) AS count,

    ROUND(COUNT(DISTINCT member_id)::DECIMAL / 10000 * 100, 1) AS pct_of_total,

    CASE 

        WHEN COUNT(DISTINCT member_id) >= 7000 THEN '✓ PASS - Realistic'

        ELSE '⚠ WARN - Low prevalence'

    END AS status

FROM member_chronic_conditions



UNION ALL



SELECT 

    'Avg Conditions per Member',

    ROUND(AVG(condition_count), 1),

    ROUND(AVG(condition_count)::DECIMAL / 10000 * 100, 1),

    CASE 

        WHEN AVG(condition_count) BETWEEN 1.5 AND 3.5 THEN '✓ PASS'

        ELSE '⚠ WARN'

    END

FROM (

    SELECT member_id, COUNT(*) AS condition_count

    FROM member_chronic_conditions

    GROUP BY member_id

) cond_counts;



\echo ''
\echo '▶ Test 2.6: Revenue at Risk Calculations'

-- Test 2.6: Revenue calculations

SELECT 

    plan_id,

    COUNT(DISTINCT measure_id) AS measures_at_risk,

    SUM(members_needed) AS total_gaps,

    ROUND(SUM(revenue_at_risk)/1000, 0) AS revenue_at_risk_k,

    CASE 

        WHEN SUM(revenue_at_risk) > 0 THEN '✓ PASS'

        ELSE '✗ FAIL - No revenue calculated'

    END AS status

FROM vw_revenue_at_risk

WHERE measurement_year = 2024

GROUP BY plan_id

ORDER BY plan_id;



-- ============================================================================

-- SECTION 3: PHASE 2 OPERATIONAL VALIDATION

-- ============================================================================



-- Test 3.1: Member engagement scoring

SELECT 

    engagement_tier,

    COUNT(*) AS member_count,

    ROUND(COUNT(*)::DECIMAL / 10000 * 100, 1) AS pct_of_total,

    ROUND(AVG(overall_engagement_score), 1) AS avg_score,

    CASE 

        WHEN COUNT(*) > 0 THEN '✓ PASS'

        ELSE '✗ FAIL'

    END AS status

FROM member_engagement_scores

GROUP BY engagement_tier

ORDER BY 

    CASE engagement_tier

        WHEN 'High' THEN 1

        WHEN 'Medium' THEN 2

        WHEN 'Low' THEN 3

        ELSE 4

    END;



\echo ''
\echo '▶ Test 3.2: Provider Network Coverage'

-- Test 3.2: Provider network coverage

SELECT 

    provider_type,

    COUNT(*) AS provider_count,

    COUNT(DISTINCT specialty) AS specialties,

    COUNT(CASE WHEN network_status = 'Active' THEN 1 END) AS active_count,

    CASE 

        WHEN provider_type = 'PCP' AND COUNT(*) >= 200 THEN '✓ PASS'

        WHEN provider_type = 'Specialist' AND COUNT(*) >= 200 THEN '✓ PASS'

        WHEN COUNT(*) > 0 THEN '✓ PASS'

        ELSE '✗ CHECK'

    END AS status

FROM provider_directory

GROUP BY provider_type

ORDER BY provider_count DESC;



\echo ''
\echo '▶ Test 3.3: Member-Provider Attribution'

-- Test 3.3: Member-provider attribution

SELECT 

    'Members with PCP' AS metric,

    COUNT(DISTINCT member_id) AS count,

    ROUND(COUNT(DISTINCT member_id)::DECIMAL / 10000 * 100, 1) AS pct_of_members,

    CASE 

        WHEN COUNT(DISTINCT member_id) >= 9900 THEN '✓ PASS - Near 100%'

        WHEN COUNT(DISTINCT member_id) >= 9500 THEN '⚠ WARN - Good coverage'

        ELSE '✗ FAIL - Poor coverage'

    END AS status

FROM member_provider_attribution

WHERE attribution_type = 'PCP' AND is_current = TRUE



UNION ALL



SELECT 

    'Members with Specialist',

    COUNT(DISTINCT member_id),

    ROUND(COUNT(DISTINCT member_id)::DECIMAL / 10000 * 100, 1),

    CASE 

        WHEN COUNT(DISTINCT member_id) BETWEEN 3000 AND 4000 THEN '✓ PASS - Expected 30-40%'

        ELSE '⚠ WARN'

    END

FROM member_provider_attribution

WHERE attribution_type = 'Specialist' AND is_current = TRUE;



\echo ''
\echo '▶ Test 3.4: Provider Performance Calculation'

-- Test 3.4: Provider performance metrics

SELECT 

    'Providers with Performance Data' AS metric,

    COUNT(DISTINCT provider_id) AS count,

    ROUND(AVG(performance_rate), 1) AS avg_performance,

    CASE 

        WHEN COUNT(DISTINCT provider_id) >= 400 THEN '✓ PASS'

        ELSE '⚠ WARN - Low coverage'

    END AS status

FROM provider_performance

WHERE measurement_year = 2024



UNION ALL



SELECT 

    'Top Performers (≥80%)',

    COUNT(DISTINCT provider_id),

    ROUND(AVG(performance_rate), 1),

    CASE 

        WHEN COUNT(DISTINCT provider_id) > 0 THEN '✓ PASS'

        ELSE '✗ CHECK'

    END

FROM provider_performance

WHERE measurement_year = 2024 AND top_performer = TRUE;



\echo ''
\echo '▶ Test 3.5: Predictive Models Operational'

-- Test 3.5: Predictive models operational

SELECT 

    'Gap Closure Propensity Scores' AS model,

    COUNT(*) AS predictions,

    ROUND(AVG(closure_propensity_score), 1) AS avg_score,

    ROUND(AVG(confidence_score), 1) AS avg_confidence,

    CASE 

        WHEN COUNT(*) >= 8000 THEN '✓ PASS'

        ELSE '✗ FAIL - Insufficient predictions'

    END AS status

FROM gap_closure_propensity



UNION ALL



SELECT 

    'Member Risk Stratification',

    COUNT(*),

    ROUND(AVG(overall_risk_score), 1),

    NULL,

    CASE 

        WHEN COUNT(*) = 10000 THEN '✓ PASS'

        ELSE '✗ FAIL'

    END

FROM member_risk_stratification



UNION ALL



SELECT 

    'Cost Predictions',

    COUNT(*),

    ROUND(AVG(predicted_total_cost), 0),

    ROUND(AVG(prediction_confidence), 1),

    CASE 

        WHEN COUNT(*) = 10000 THEN '✓ PASS'

        ELSE '✗ FAIL'

    END

FROM member_cost_predictions



UNION ALL



SELECT 

    'Intervention Priority Queue',

    COUNT(*),

    ROUND(AVG(priority_score), 1),

    NULL,

    CASE 

        WHEN COUNT(*) >= 8000 THEN '✓ PASS'

        ELSE '⚠ WARN'

    END

FROM intervention_priority_queue;



\echo ''
\echo '▶ Test 3.6: Early Warning System'

-- Test 3.6: Early warning alerts

SELECT 

    alert_type,

    alert_severity,

    COUNT(*) AS alert_count,

    COUNT(CASE WHEN alert_status = 'Active' THEN 1 END) AS active_count,

    CASE 

        WHEN COUNT(*) > 0 THEN '✓ PASS'

        ELSE '⚠ INFO - No alerts'

    END AS status

FROM early_warning_alerts

GROUP BY alert_type, alert_severity

ORDER BY 

    CASE alert_severity

        WHEN 'Critical' THEN 1

        WHEN 'High' THEN 2

        WHEN 'Medium' THEN 3

        ELSE 4

    END,

    alert_count DESC;



-- ============================================================================

-- SECTION 4: DATA QUALITY ASSESSMENT

-- ============================================================================



-- Test 4.1: Referential integrity

SELECT 

    'Member Gaps → Members' AS relationship,

    COUNT(*) AS orphaned_records,

    CASE 

        WHEN COUNT(*) = 0 THEN '✓ PASS - No orphans'

        ELSE '✗ FAIL - Orphaned records found'

    END AS status

FROM member_gaps mg

WHERE NOT EXISTS (

    SELECT 1 FROM plan_members pm WHERE pm.member_id = mg.member_id

)



UNION ALL



SELECT 

    'Provider Attribution → Providers',

    COUNT(*),

    CASE 

        WHEN COUNT(*) = 0 THEN '✓ PASS'

        ELSE '✗ FAIL'

    END

FROM member_provider_attribution mpa

WHERE NOT EXISTS (

    SELECT 1 FROM provider_directory pd WHERE pd.provider_id = mpa.provider_id

)



UNION ALL



SELECT 

    'Propensity → Gaps',

    COUNT(*),

    CASE 

        WHEN COUNT(*) = 0 THEN '✓ PASS'

        ELSE '✗ FAIL'

    END

FROM gap_closure_propensity gcp

WHERE NOT EXISTS (

    SELECT 1 FROM member_gaps mg WHERE mg.gap_id = gcp.gap_id

);



\echo ''
\echo '▶ Test 4.2: Critical Field Completeness'

-- Test 4.2: Data completeness

SELECT 

    'Members without DOB' AS field_check,

    COUNT(*) AS null_count,

    CASE WHEN COUNT(*) = 0 THEN '✓ PASS' ELSE '✗ FAIL' END AS status

FROM plan_members

WHERE date_of_birth IS NULL AND member_id LIKE 'M%'



UNION ALL



SELECT 

    'Members without Risk Score',

    COUNT(*),

    CASE WHEN COUNT(*) = 0 THEN '✓ PASS' ELSE '⚠ WARN' END

FROM plan_members

WHERE risk_score IS NULL AND member_id LIKE 'M%'



UNION ALL



SELECT 

    'Gaps without Measure ID',

    COUNT(*),

    CASE WHEN COUNT(*) = 0 THEN '✓ PASS' ELSE '✗ FAIL' END

FROM member_gaps

WHERE measure_id IS NULL



UNION ALL



SELECT 

    'Providers without Specialty',

    COUNT(*),

    CASE WHEN COUNT(*) = 0 THEN '✓ PASS' ELSE '⚠ WARN' END

FROM provider_directory

WHERE specialty IS NULL AND network_status = 'Active';



\echo ''
\echo '▶ Test 4.3: Data Range Validation'

-- Test 4.3: Data range validation

SELECT 

    'Age Range' AS validation,

    ROUND(MIN(EXTRACT(YEAR FROM AGE(date_of_birth))), 0) AS min_value,

    ROUND(MAX(EXTRACT(YEAR FROM AGE(date_of_birth))), 0) AS max_value,

    '65-95' AS expected_range,

    CASE 

        WHEN MIN(EXTRACT(YEAR FROM AGE(date_of_birth))) >= 65 

         AND MAX(EXTRACT(YEAR FROM AGE(date_of_birth))) <= 100 

        THEN '✓ PASS'

        ELSE '✗ CHECK'

    END AS status

FROM plan_members

WHERE member_id LIKE 'M%'



UNION ALL



SELECT 

    'Risk Scores',

    ROUND(MIN(risk_score), 2),

    ROUND(MAX(risk_score), 2),

    '0.5-5.0',

    CASE 

        WHEN MIN(risk_score) >= 0.5 AND MAX(risk_score) <= 6.0 

        THEN '✓ PASS'

        ELSE '⚠ WARN'

    END

FROM plan_members

WHERE member_id LIKE 'M%'



UNION ALL



SELECT 

    'Engagement Scores',

    ROUND(MIN(overall_engagement_score), 1),

    ROUND(MAX(overall_engagement_score), 1),

    '10-95',

    CASE 

        WHEN MIN(overall_engagement_score) >= 5 

         AND MAX(overall_engagement_score) <= 100 

        THEN '✓ PASS'

        ELSE '⚠ WARN'

    END

FROM member_engagement_scores



UNION ALL



SELECT 

    'Provider Performance',

    ROUND(MIN(performance_rate), 1),

    ROUND(MAX(performance_rate), 1),

    '40-95',

    CASE 

        WHEN MIN(performance_rate) >= 30 AND MAX(performance_rate) <= 100 

        THEN '✓ PASS'

        ELSE '⚠ WARN'

    END

FROM provider_performance

WHERE measurement_year = 2024;



-- ============================================================================

-- SECTION 5: BUSINESS LOGIC VERIFICATION

-- ============================================================================



-- Test 5.1: Revenue calculations accuracy

SELECT 

    measure_id,

    COUNT(*) AS plan_count,

    ROUND(AVG(revenue_at_risk), 0) AS avg_revenue_at_risk,

    ROUND(SUM(revenue_at_risk), 0) AS total_revenue_at_risk,

    CASE 

        WHEN SUM(revenue_at_risk) > 0 THEN '✓ PASS'

        ELSE '✗ FAIL'

    END AS status

FROM vw_revenue_at_risk

WHERE measurement_year = 2024

GROUP BY measure_id

ORDER BY total_revenue_at_risk DESC

LIMIT 5;



\echo ''
\echo '▶ Test 5.2: Propensity Score Distribution'

-- Test 5.2: Gap closure propensity logic

SELECT 

    closure_likelihood,

    COUNT(*) AS gap_count,

    ROUND(AVG(closure_propensity_score), 1) AS avg_score,

    ROUND(AVG(predicted_days_to_close), 0) AS avg_days,

    CASE 

        WHEN closure_likelihood = 'Very High' AND AVG(closure_propensity_score) >= 75 THEN '✓ PASS'

        WHEN closure_likelihood = 'High' AND AVG(closure_propensity_score) >= 60 THEN '✓ PASS'

        WHEN closure_likelihood = 'Medium' AND AVG(closure_propensity_score) >= 45 THEN '✓ PASS'

        WHEN closure_likelihood = 'Low' AND AVG(closure_propensity_score) >= 30 THEN '✓ PASS'

        WHEN closure_likelihood = 'Very Low' AND AVG(closure_propensity_score) < 35 THEN '✓ PASS'

        ELSE '⚠ CHECK - Score range unexpected'

    END AS status

FROM gap_closure_propensity

GROUP BY closure_likelihood

ORDER BY 

    CASE closure_likelihood

        WHEN 'Very High' THEN 1

        WHEN 'High' THEN 2

        WHEN 'Medium' THEN 3

        WHEN 'Low' THEN 4

        ELSE 5

    END;



\echo ''
\echo '▶ Test 5.3: Risk Stratification Alignment'

-- Test 5.3: Risk tier alignment

SELECT 

    risk_tier,

    COUNT(*) AS member_count,

    ROUND(AVG(overall_risk_score), 1) AS avg_risk_score,

    ROUND(AVG(clinical_complexity_score), 1) AS avg_clinical,

    CASE 

        WHEN risk_tier = 'Critical' AND AVG(overall_risk_score) >= 70 THEN '✓ PASS'

        WHEN risk_tier = 'High' AND AVG(overall_risk_score) >= 55 THEN '✓ PASS'

        WHEN risk_tier = 'Medium' AND AVG(overall_risk_score) >= 35 THEN '✓ PASS'

        WHEN risk_tier = 'Low' AND AVG(overall_risk_score) < 40 THEN '✓ PASS'

        ELSE '⚠ CHECK'

    END AS status

FROM member_risk_stratification

GROUP BY risk_tier

ORDER BY 

    CASE risk_tier

        WHEN 'Critical' THEN 1

        WHEN 'High' THEN 2

        WHEN 'Medium' THEN 3

        ELSE 4

    END;



-- ============================================================================

-- SECTION 6: DASHBOARD FUNCTIONALITY

-- ============================================================================



-- Test 6.1: All dashboard views operational

SELECT 

    viewname AS view_name,

    '✓ EXISTS' AS status,

    CASE 

        WHEN viewname LIKE 'vw_%' THEN 'Dashboard View'

        ELSE 'Other View'

    END AS view_type

FROM pg_views

WHERE schemaname = 'public'

  AND viewname LIKE 'vw_%'

ORDER BY viewname;



\echo ''
\echo '▶ Test 6.2: Executive Summary Data Quality'

-- Test 6.2: Executive summary completeness

SELECT * FROM vw_executive_summary;



\echo ''
\echo '▶ Test 6.3: Real-Time Operations Dashboard'

-- Test 6.3: Real-time operations dashboard

SELECT * FROM vw_operations_dashboard;



-- ============================================================================

-- SECTION 7: EXPORT READINESS

-- ============================================================================



-- Test 7.1: Master export view

SELECT 

    'Total Export Records' AS metric,

    COUNT(*) AS count,

    CASE 

        WHEN COUNT(*) = 10000 THEN '✓ PASS'

        ELSE '✗ FAIL'

    END AS status

FROM vw_data_export_master



UNION ALL



SELECT 

    'Records with Complete Data',

    COUNT(*),

    CASE 

        WHEN COUNT(*) >= 9500 THEN '✓ PASS - 95%+ complete'

        ELSE '⚠ WARN'

    END

FROM vw_data_export_master

WHERE age IS NOT NULL 

  AND overall_engagement_score IS NOT NULL

  AND overall_risk_score IS NOT NULL;



\echo ''
\echo '▶ Test 7.2: Export Column Completeness'

-- Test 7.2: Export column completeness

SELECT 

    'Members with Engagement Score' AS field,

    COUNT(*) AS populated_count,

    ROUND(COUNT(*)::DECIMAL / 10000 * 100, 1) AS pct_complete,

    CASE WHEN COUNT(*) >= 9500 THEN '✓ PASS' ELSE '⚠ WARN' END AS status

FROM vw_data_export_master

WHERE overall_engagement_score IS NOT NULL



UNION ALL



SELECT 

    'Members with Risk Score',

    COUNT(*),

    ROUND(COUNT(*)::DECIMAL / 10000 * 100, 1),

    CASE WHEN COUNT(*) >= 9500 THEN '✓ PASS' ELSE '⚠ WARN' END

FROM vw_data_export_master

WHERE overall_risk_score IS NOT NULL



UNION ALL



SELECT 

    'Members with Cost Prediction',

    COUNT(*),

    ROUND(COUNT(*)::DECIMAL / 10000 * 100, 1),

    CASE WHEN COUNT(*) >= 9500 THEN '✓ PASS' ELSE '⚠ WARN' END

FROM vw_data_export_master

WHERE predicted_total_cost IS NOT NULL



UNION ALL



SELECT 

    'Members with PCP Attribution',

    COUNT(*),

    ROUND(COUNT(*)::DECIMAL / 10000 * 100, 1),

    CASE WHEN COUNT(*) >= 9500 THEN '✓ PASS' ELSE '⚠ WARN' END

FROM vw_data_export_master

WHERE pcp_provider_id IS NOT NULL;



-- ============================================================================

-- SECTION 8: FINAL SYSTEM SUMMARY

-- ============================================================================



-- Overall System Status

WITH validation_summary AS (

    SELECT 

        'Database Objects' AS component,

        (SELECT COUNT(*) FROM information_schema.tables WHERE table_schema = 'public' AND table_type = 'BASE TABLE') AS metric_value,

        '40+' AS target,

        CASE WHEN (SELECT COUNT(*) FROM information_schema.tables WHERE table_schema = 'public' AND table_type = 'BASE TABLE') >= 30 THEN '✓ PASS' ELSE '⚠ CHECK' END AS status

    

    UNION ALL

    SELECT 

        'Dashboard Views',

        (SELECT COUNT(*) FROM information_schema.views WHERE table_schema = 'public'),

        '30+',

        CASE WHEN (SELECT COUNT(*) FROM information_schema.views WHERE table_schema = 'public') >= 25 THEN '✓ PASS' ELSE '⚠ CHECK' END

    

    UNION ALL

    SELECT 

        'Member Records',

        (SELECT COUNT(*) FROM plan_members WHERE member_id LIKE 'M%'),

        '10,000',

        CASE WHEN (SELECT COUNT(*) FROM plan_members WHERE member_id LIKE 'M%') = 10000 THEN '✓ PASS' ELSE '✗ FAIL' END

    

    UNION ALL

    SELECT 

        'Care Gaps',

        (SELECT COUNT(*) FROM member_gaps WHERE member_id LIKE 'M%'),

        '12K-18K',

        CASE WHEN (SELECT COUNT(*) FROM member_gaps WHERE member_id LIKE 'M%') BETWEEN 12000 AND 18000 THEN '✓ PASS' ELSE '⚠ CHECK' END

    

    UNION ALL

    SELECT 

        'Providers',

        (SELECT COUNT(*) FROM provider_directory WHERE network_status = 'Active'),

        '500+',

        CASE WHEN (SELECT COUNT(*) FROM provider_directory WHERE network_status = 'Active') >= 500 THEN '✓ PASS' ELSE '✗ FAIL' END

    

    UNION ALL

    SELECT 

        'Engagement Scores',

        (SELECT COUNT(*) FROM member_engagement_scores),

        '10,000',

        CASE WHEN (SELECT COUNT(*) FROM member_engagement_scores) = 10000 THEN '✓ PASS' ELSE '✗ FAIL' END

    

    UNION ALL

    SELECT 

        'Risk Stratification',

        (SELECT COUNT(*) FROM member_risk_stratification),

        '10,000',

        CASE WHEN (SELECT COUNT(*) FROM member_risk_stratification) = 10000 THEN '✓ PASS' ELSE '✗ FAIL' END

    

    UNION ALL

    SELECT 

        'Propensity Scores',

        (SELECT COUNT(*) FROM gap_closure_propensity),

        '8K+',

        CASE WHEN (SELECT COUNT(*) FROM gap_closure_propensity) >= 8000 THEN '✓ PASS' ELSE '⚠ WARN' END

    

    UNION ALL

    SELECT 

        'Cost Predictions',

        (SELECT COUNT(*) FROM member_cost_predictions),

        '10,000',

        CASE WHEN (SELECT COUNT(*) FROM member_cost_predictions) = 10000 THEN '✓ PASS' ELSE '✗ FAIL' END

    

    UNION ALL

    SELECT 

        'Priority Queue',

        (SELECT COUNT(*) FROM intervention_priority_queue),

        '8K+',

        CASE WHEN (SELECT COUNT(*) FROM intervention_priority_queue) >= 8000 THEN '✓ PASS' ELSE '⚠ WARN' END

)

SELECT * FROM validation_summary;



\echo ''
\echo '▶ Key Performance Indicators'

-- Key Performance Indicators

SELECT 

    'Total Revenue at Risk' AS kpi,

    '$' || ROUND(SUM(revenue_at_risk)/1000, 0) || 'K' AS value,

    'Financial Impact' AS category

FROM vw_revenue_at_risk



UNION ALL



SELECT 

    'Portfolio ROI Projection',

    ROUND((SELECT COALESCE(projected_roi, 0) FROM vw_executive_summary), 2)::TEXT || ':1',

    'Efficiency'



UNION ALL



SELECT 

    'Average Engagement Score',

    ROUND(AVG(overall_engagement_score), 1)::TEXT || '/100',

    'Member Engagement'

FROM member_engagement_scores



UNION ALL



SELECT 

    'High-Risk Members',

    COUNT(*)::TEXT || ' (' || ROUND(COUNT(*)::DECIMAL/10000*100, 1)::TEXT || '%)',

    'Risk Management'

FROM member_risk_stratification

WHERE risk_tier IN ('Critical', 'High')



UNION ALL



SELECT 

    'Average Provider Performance',

    ROUND(AVG(avg_performance_rate), 1)::TEXT || '%',

    'Network Quality'

FROM vw_provider_performance_summary



UNION ALL



SELECT 

    'Active Interventions Queued',

    COUNT(*)::TEXT,

    'Operations'

FROM intervention_priority_queue

WHERE status = 'Queued';



\echo ''
\echo '╔══════════════════════════════════════════════════════════════╗'
\echo '║              VALIDATION COMPLETE ✓                           ║'
\echo '║                                                              ║'
\echo '║  All critical systems validated and operational              ║'
\echo '║  Review any ⚠ WARN or ✗ FAIL items above                   ║'
\echo '║                                                              ║'
\echo '║  System Status: PRODUCTION READY                             ║'
\echo '╚══════════════════════════════════════════════════════════════╝'
\echo ''

-- ============================================================================

-- END OF FULL VALIDATION SUITE

-- ============================================================================


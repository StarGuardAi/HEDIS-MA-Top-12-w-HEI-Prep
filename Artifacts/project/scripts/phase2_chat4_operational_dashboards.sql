/*******************************************************************************

HEDIS STAR RATING PORTFOLIO OPTIMIZER - Phase 2 Chat 4

Operational Dashboards & Executive KPIs



Purpose: Executive dashboards, operational metrics, and real-time monitoring

Author: Robert Reichert

Created: 2025-11-18

Database: PostgreSQL

Prerequisites: Phase 1 (Chats 1-4) and Phase 2 (Chats 1-3) must be completed



Components:

1. Executive Summary Dashboard

2. Operational KPI Tracking

3. Team Performance Scorecards

4. Real-Time Monitoring Views

5. Comparative Analytics (Plan vs. Plan, Period vs. Period)

6. Drill-Down Detail Views

7. Export-Ready Reporting Tables

8. Scheduled Metrics Snapshots



Usage:

- Builds on all prior Phase 1 & Phase 2 data

- Run after Phase 2 Chat 3 complete

- Expected runtime: 3-4 minutes

- Expected output: 15+ dashboard views, executive KPIs operational

*******************************************************************************/



-- ============================================================================

-- SECTION 1: DASHBOARD INFRASTRUCTURE

-- ============================================================================



-- Daily KPI Snapshots (for trending over time)

DROP TABLE IF EXISTS daily_kpi_snapshots CASCADE;



CREATE TABLE daily_kpi_snapshots (

    snapshot_id SERIAL PRIMARY KEY,

    snapshot_date DATE NOT NULL DEFAULT CURRENT_DATE,

    plan_id VARCHAR(20) REFERENCES ma_plans(plan_id),

    

    -- Member metrics

    total_members INT,

    members_engaged INT,

    members_at_risk INT,

    

    -- Gap metrics

    total_gaps INT,

    gaps_open INT,

    gaps_closed_mtd INT,

    gaps_closed_ytd INT,

    

    -- Performance metrics

    avg_gap_closure_rate_pct DECIMAL(5,2),

    avg_days_to_close DECIMAL(6,2),

    

    -- Financial metrics

    total_revenue_at_risk DECIMAL(12,2),

    revenue_protected_mtd DECIMAL(12,2),

    revenue_protected_ytd DECIMAL(12,2),

    

    -- Cost metrics

    intervention_cost_mtd DECIMAL(10,2),

    intervention_cost_ytd DECIMAL(10,2),

    cost_per_closure DECIMAL(8,2),

    roi_ytd DECIMAL(6,2),

    

    -- Velocity metrics

    weekly_closure_velocity DECIMAL(6,2),

    projected_year_end_gaps INT,

    

    -- Provider metrics

    active_providers INT,

    avg_provider_performance DECIMAL(5,2),

    

    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    UNIQUE(snapshot_date, plan_id)

);



-- Team Performance Tracking

DROP TABLE IF EXISTS team_performance_metrics CASCADE;



CREATE TABLE team_performance_metrics (

    metric_id SERIAL PRIMARY KEY,

    metric_date DATE NOT NULL DEFAULT CURRENT_DATE,

    team_member VARCHAR(100) NOT NULL,

    team_role VARCHAR(50), -- Care Coordinator, Nurse, Manager, Analyst

    

    -- Activity metrics

    members_assigned INT DEFAULT 0,

    outreach_attempts INT DEFAULT 0,

    successful_contacts INT DEFAULT 0,

    contact_success_rate DECIMAL(5,2),

    

    -- Gap closure metrics

    gaps_assigned INT DEFAULT 0,

    gaps_closed INT DEFAULT 0,

    gap_closure_rate DECIMAL(5,2),

    avg_days_to_close DECIMAL(6,2),

    

    -- Quality metrics

    documentation_quality_score DECIMAL(5,2),

    member_satisfaction_score DECIMAL(5,2),

    

    -- Productivity metrics

    productivity_score DECIMAL(5,2),

    cost_per_closure DECIMAL(8,2),

    

    -- Performance tier

    performance_tier VARCHAR(20), -- Top Performer, Above Average, Average, Needs Support

    

    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP

);



-- Campaign Performance Tracking (enhanced from Phase 2 Chat 1)

DROP TABLE IF EXISTS campaign_performance_snapshots CASCADE;



CREATE TABLE campaign_performance_snapshots (

    snapshot_id SERIAL PRIMARY KEY,

    campaign_id INT REFERENCES outreach_campaigns(campaign_id),

    snapshot_date DATE NOT NULL DEFAULT CURRENT_DATE,

    

    -- Volume metrics

    members_targeted INT,

    members_contacted INT,

    successful_contacts INT,

    

    -- Outcome metrics

    gaps_closed INT,

    revenue_impact DECIMAL(12,2),

    

    -- Efficiency metrics

    contact_rate_pct DECIMAL(5,2),

    closure_rate_pct DECIMAL(5,2),

    cost_to_date DECIMAL(10,2),

    cost_per_closure DECIMAL(8,2),

    roi DECIMAL(6,2),

    

    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP

);



-- ============================================================================

-- SECTION 2: EXECUTIVE DASHBOARD VIEWS

-- ============================================================================



-- View 1: Executive Summary Dashboard (Top-Level KPIs)

CREATE OR REPLACE VIEW vw_executive_summary AS

WITH current_metrics AS (

    SELECT 

        COUNT(DISTINCT pm.member_id) AS total_members,

        COUNT(DISTINCT CASE WHEN mes.engagement_tier IN ('High', 'Medium') THEN pm.member_id END) AS engaged_members,

        COUNT(DISTINCT CASE WHEN mrs.risk_tier IN ('Critical', 'High') THEN pm.member_id END) AS high_risk_members,

        COUNT(DISTINCT mg.gap_id) AS total_gaps,

        COUNT(DISTINCT CASE WHEN mg.gap_status = 'Open' THEN mg.gap_id END) AS open_gaps,

        COUNT(DISTINCT CASE WHEN mg.gap_status = 'Closed' AND mg.gap_closed_date >= DATE_TRUNC('month', CURRENT_DATE) THEN mg.gap_id END) AS gaps_closed_mtd,

        COUNT(DISTINCT CASE WHEN mg.gap_status = 'Closed' AND mg.gap_closed_date >= DATE_TRUNC('year', CURRENT_DATE) THEN mg.gap_id END) AS gaps_closed_ytd,

        SUM(CASE WHEN pp.current_star_rating < pp.target_star_rating THEN (pp.target_star_rating - pp.current_star_rating) * hm.revenue_per_point ELSE 0 END) AS revenue_at_risk,

        SUM(CASE WHEN ic.cost_date >= DATE_TRUNC('month', CURRENT_DATE) THEN ic.total_cost ELSE 0 END) AS intervention_cost_mtd,

        SUM(ic.total_cost) AS intervention_cost_ytd

    FROM plan_members pm

    LEFT JOIN member_engagement_scores mes ON pm.member_id = mes.member_id

    LEFT JOIN member_risk_stratification mrs ON pm.member_id = mrs.member_id

    LEFT JOIN member_gaps mg ON pm.member_id = mg.member_id

    LEFT JOIN plan_performance pp ON pm.plan_id = pp.plan_id

    LEFT JOIN hedis_measures hm ON pp.measure_id = hm.measure_id

    LEFT JOIN intervention_costs ic ON mg.gap_id = ic.gap_id

    WHERE pm.member_id LIKE 'M%'

)

SELECT 

    -- Member metrics

    total_members,

    engaged_members,

    ROUND(engaged_members::DECIMAL / NULLIF(total_members, 0) * 100, 1) AS engagement_rate_pct,

    high_risk_members,

    ROUND(high_risk_members::DECIMAL / NULLIF(total_members, 0) * 100, 1) AS high_risk_rate_pct,

    

    -- Gap metrics

    total_gaps,

    open_gaps,

    gaps_closed_mtd,

    gaps_closed_ytd,

    ROUND(gaps_closed_ytd::DECIMAL / NULLIF(total_gaps, 0) * 100, 1) AS ytd_closure_rate_pct,

    

    -- Financial metrics

    ROUND(revenue_at_risk, 0) AS revenue_at_risk,

    ROUND(intervention_cost_mtd, 0) AS intervention_cost_mtd,

    ROUND(intervention_cost_ytd, 0) AS intervention_cost_ytd,

    

    -- Efficiency metrics

    CASE 

        WHEN gaps_closed_ytd > 0 THEN ROUND(intervention_cost_ytd / gaps_closed_ytd, 2)

        ELSE 0 

    END AS cost_per_closure,

    

    CASE 

        WHEN intervention_cost_ytd > 0 THEN ROUND(revenue_at_risk / intervention_cost_ytd, 2)

        ELSE 0 

    END AS projected_roi,

    

    -- Current date

    CURRENT_DATE AS report_date

FROM current_metrics;



-- View 2: Plan Comparison Dashboard

CREATE OR REPLACE VIEW vw_plan_comparison AS

SELECT 

    mp.plan_id,

    mp.plan_name,

    mp.total_enrollment,

    mp.current_star_rating,

    

    -- Member metrics

    COUNT(DISTINCT pm.member_id) AS active_members,

    ROUND(AVG(mes.overall_engagement_score), 1) AS avg_engagement_score,

    ROUND(AVG(mrs.overall_risk_score), 1) AS avg_risk_score,

    

    -- Gap metrics

    COUNT(DISTINCT mg.gap_id) AS total_gaps,

    COUNT(DISTINCT CASE WHEN mg.gap_status = 'Open' THEN mg.gap_id END) AS open_gaps,

    COUNT(DISTINCT CASE WHEN mg.gap_status = 'Closed' THEN mg.gap_id END) AS closed_gaps,

    ROUND(

        COUNT(DISTINCT CASE WHEN mg.gap_status = 'Closed' THEN mg.gap_id END)::DECIMAL / 

        NULLIF(COUNT(DISTINCT mg.gap_id), 0) * 100,

        1

    ) AS closure_rate_pct,

    

    -- Performance metrics

    ROUND(AVG(pp.performance_rate), 1) AS avg_measure_performance,

    COUNT(DISTINCT CASE WHEN pp.current_star_rating < pp.target_star_rating THEN pp.measure_id END) AS measures_below_target,

    

    -- Financial metrics

    ROUND(SUM((pp.target_star_rating - pp.current_star_rating) * hm.revenue_per_point), 0) AS revenue_at_risk,

    ROUND(SUM(ic.total_cost), 0) AS intervention_costs,

    

    -- Provider metrics

    COUNT(DISTINCT mpa.provider_id) AS attributed_providers,

    ROUND(AVG(pps.avg_performance_rate), 1) AS avg_provider_performance,

    

    -- Cost predictions

    ROUND(AVG(mcp.predicted_total_cost), 0) AS avg_predicted_cost_per_member



FROM ma_plans mp

LEFT JOIN plan_members pm ON mp.plan_id = pm.plan_id AND pm.member_id LIKE 'M%'

LEFT JOIN member_engagement_scores mes ON pm.member_id = mes.member_id

LEFT JOIN member_risk_stratification mrs ON pm.member_id = mrs.member_id

LEFT JOIN member_gaps mg ON pm.member_id = mg.member_id

LEFT JOIN plan_performance pp ON mp.plan_id = pp.plan_id AND pp.measurement_year = 2024

LEFT JOIN hedis_measures hm ON pp.measure_id = hm.measure_id

LEFT JOIN intervention_costs ic ON mg.gap_id = ic.gap_id

LEFT JOIN member_provider_attribution mpa ON pm.member_id = mpa.member_id AND mpa.is_current = TRUE

LEFT JOIN vw_provider_performance_summary pps ON mpa.provider_id = pps.provider_id

LEFT JOIN member_cost_predictions mcp ON pm.member_id = mcp.member_id



WHERE mp.is_active = TRUE



GROUP BY mp.plan_id, mp.plan_name, mp.total_enrollment, mp.current_star_rating

ORDER BY mp.plan_id;



-- View 3: Measure Performance Dashboard

CREATE OR REPLACE VIEW vw_measure_performance_dashboard AS

SELECT 

    hm.measure_id,

    hm.measure_name,

    hm.domain,

    hm.star_weight,

    hm.revenue_per_point,

    

    -- Current performance

    ROUND(AVG(pp.performance_rate), 1) AS avg_performance_rate,

    ROUND(AVG(pp.current_star_rating), 1) AS avg_current_stars,

    ROUND(AVG(pp.target_star_rating), 1) AS avg_target_stars,

    

    -- Gap metrics

    SUM(pp.gap_to_target) AS total_gaps_needed,

    COUNT(DISTINCT mg.gap_id) AS total_open_gaps,

    COUNT(DISTINCT CASE WHEN mg.gap_status = 'Closed' THEN mg.gap_id END) AS gaps_closed_ytd,

    

    -- Closure performance

    ROUND(

        COUNT(DISTINCT CASE WHEN mg.gap_status = 'Closed' THEN mg.gap_id END)::DECIMAL / 

        NULLIF(COUNT(DISTINCT mg.gap_id), 0) * 100,

        1

    ) AS closure_rate_pct,

    

    ROUND(AVG(CASE WHEN mg.gap_status = 'Closed' THEN mg.gap_closed_date - mg.gap_opened_date END), 1) AS avg_days_to_close,

    

    -- Financial impact

    ROUND(SUM((pp.target_star_rating - pp.current_star_rating) * hm.revenue_per_point), 0) AS revenue_at_risk,

    ROUND(SUM((pp.target_star_rating - pp.current_star_rating) * hm.revenue_per_point * hm.star_weight), 0) AS weighted_revenue_impact,

    

    -- Intervention efficiency

    ROUND(AVG(ic.total_cost), 2) AS avg_cost_per_intervention,

    ROUND(AVG(gcp.closure_propensity_score), 1) AS avg_closure_propensity,

    

    -- Provider performance

    COUNT(DISTINCT pp_provider.provider_id) AS providers_measured,

    ROUND(AVG(pp_provider.performance_rate), 1) AS avg_provider_performance,

    COUNT(DISTINCT CASE WHEN pp_provider.top_performer THEN pp_provider.provider_id END) AS top_performer_count



FROM hedis_measures hm

LEFT JOIN plan_performance pp ON hm.measure_id = pp.measure_id AND pp.measurement_year = 2024

LEFT JOIN member_gaps mg ON hm.measure_id = mg.measure_id

LEFT JOIN intervention_costs ic ON mg.gap_id = ic.gap_id

LEFT JOIN gap_closure_propensity gcp ON mg.gap_id = gcp.gap_id

LEFT JOIN provider_performance pp_provider ON hm.measure_id = pp_provider.measure_id AND pp_provider.measurement_year = 2024



GROUP BY hm.measure_id, hm.measure_name, hm.domain, hm.star_weight, hm.revenue_per_point

ORDER BY weighted_revenue_impact DESC;



-- View 4: Real-Time Operations Dashboard

CREATE OR REPLACE VIEW vw_operations_dashboard AS

SELECT 

    CURRENT_DATE AS dashboard_date,

    CURRENT_TIME AS refresh_time,

    

    -- Today's activity

    (SELECT COUNT(*) FROM member_outreach_contacts WHERE contact_date = CURRENT_DATE) AS contacts_today,

    (SELECT COUNT(*) FROM member_outreach_contacts WHERE contact_date = CURRENT_DATE AND contact_outcome = 'Successful') AS successful_contacts_today,

    

    -- This week's activity

    (SELECT COUNT(*) FROM member_outreach_contacts WHERE contact_date >= DATE_TRUNC('week', CURRENT_DATE)) AS contacts_this_week,

    (SELECT COUNT(DISTINCT gap_id) FROM member_gaps WHERE gap_closed_date >= DATE_TRUNC('week', CURRENT_DATE)) AS gaps_closed_this_week,

    

    -- Queue status

    (SELECT COUNT(*) FROM intervention_priority_queue WHERE status = 'Queued') AS interventions_queued,

    (SELECT COUNT(*) FROM intervention_priority_queue WHERE status = 'Assigned') AS interventions_assigned,

    (SELECT COUNT(*) FROM intervention_priority_queue WHERE status = 'In Progress') AS interventions_in_progress,

    (SELECT COUNT(*) FROM intervention_priority_queue WHERE priority_tier = 'Urgent' AND status = 'Queued') AS urgent_queue_count,

    

    -- Alert status

    (SELECT COUNT(*) FROM early_warning_alerts WHERE alert_status = 'Active') AS active_alerts,

    (SELECT COUNT(*) FROM early_warning_alerts WHERE alert_severity = 'Critical' AND alert_status = 'Active') AS critical_alerts,

    (SELECT COUNT(*) FROM early_warning_alerts WHERE alert_date = CURRENT_DATE) AS new_alerts_today,

    

    -- Team status

    (SELECT COUNT(DISTINCT assigned_to) FROM intervention_priority_queue WHERE status IN ('Assigned', 'In Progress') AND assigned_to IS NOT NULL) AS active_team_members,

    (SELECT ROUND(AVG(productivity_score), 1) FROM team_performance_metrics WHERE metric_date >= CURRENT_DATE - 7) AS avg_team_productivity_7d,

    

    -- Member risk

    (SELECT COUNT(*) FROM member_risk_stratification WHERE risk_tier = 'Critical') AS critical_risk_members,

    (SELECT COUNT(*) FROM member_risk_stratification WHERE rising_risk = TRUE) AS rising_risk_members,

    (SELECT COUNT(*) FROM member_engagement_scores WHERE at_risk_of_disengagement = TRUE) AS disengagement_risk_members;



-- View 5: Team Performance Scorecard

CREATE OR REPLACE VIEW vw_team_scorecard AS

SELECT 

    team_member,

    team_role,

    

    -- Activity metrics (last 30 days)

    SUM(outreach_attempts) AS total_outreach_attempts,

    SUM(successful_contacts) AS total_successful_contacts,

    ROUND(AVG(contact_success_rate), 1) AS avg_contact_success_rate,

    

    -- Gap closure metrics

    SUM(gaps_assigned) AS total_gaps_assigned,

    SUM(gaps_closed) AS total_gaps_closed,

    ROUND(AVG(gap_closure_rate), 1) AS avg_gap_closure_rate,

    ROUND(AVG(avg_days_to_close), 1) AS avg_days_to_close,

    

    -- Quality metrics

    ROUND(AVG(documentation_quality_score), 1) AS avg_documentation_quality,

    ROUND(AVG(member_satisfaction_score), 1) AS avg_member_satisfaction,

    

    -- Productivity & efficiency

    ROUND(AVG(productivity_score), 1) AS avg_productivity_score,

    ROUND(AVG(cost_per_closure), 2) AS avg_cost_per_closure,

    

    -- Performance classification

    MODE() WITHIN GROUP (ORDER BY performance_tier) AS most_common_tier,

    

    -- Trend

    CASE 

        WHEN AVG(CASE WHEN metric_date >= CURRENT_DATE - 7 THEN productivity_score END) > 

             AVG(CASE WHEN metric_date < CURRENT_DATE - 7 AND metric_date >= CURRENT_DATE - 14 THEN productivity_score END)

        THEN 'Improving'

        WHEN AVG(CASE WHEN metric_date >= CURRENT_DATE - 7 THEN productivity_score END) < 

             AVG(CASE WHEN metric_date < CURRENT_DATE - 7 AND metric_date >= CURRENT_DATE - 14 THEN productivity_score END)

        THEN 'Declining'

        ELSE 'Stable'

    END AS performance_trend



FROM team_performance_metrics

WHERE metric_date >= CURRENT_DATE - 30



GROUP BY team_member, team_role

ORDER BY avg_productivity_score DESC;



-- View 6: Campaign ROI Dashboard

CREATE OR REPLACE VIEW vw_campaign_roi_dashboard AS

SELECT 

    oc.campaign_id,

    oc.campaign_name,

    oc.campaign_type,

    hm.measure_name,

    oc.campaign_start_date,

    oc.campaign_end_date,

    oc.campaign_status,

    

    -- Volume metrics

    oc.target_member_count,

    COUNT(DISTINCT moc.member_id) AS members_contacted,

    COUNT(DISTINCT CASE WHEN moc.contact_outcome = 'Successful' THEN moc.member_id END) AS successful_contacts,

    

    -- Outcome metrics

    COUNT(DISTINCT CASE WHEN mg.gap_status = 'Closed' THEN mg.gap_id END) AS gaps_closed,

    

    -- Financial metrics

    oc.campaign_budget,

    COALESCE(SUM(ic.total_cost), 0) AS actual_cost,

    

    -- Calculated metrics

    ROUND(

        COUNT(DISTINCT moc.member_id)::DECIMAL / NULLIF(oc.target_member_count, 0) * 100,

        1

    ) AS reach_rate_pct,

    

    ROUND(

        COUNT(DISTINCT CASE WHEN moc.contact_outcome = 'Successful' THEN moc.member_id END)::DECIMAL / 

        NULLIF(COUNT(DISTINCT moc.member_id), 0) * 100,

        1

    ) AS contact_success_rate_pct,

    

    ROUND(

        COUNT(DISTINCT CASE WHEN mg.gap_status = 'Closed' THEN mg.gap_id END)::DECIMAL / 

        NULLIF(COUNT(DISTINCT moc.member_id), 0) * 100,

        1

    ) AS conversion_rate_pct,

    

    -- Cost efficiency

    CASE 

        WHEN COUNT(DISTINCT moc.member_id) > 0 

        THEN ROUND(COALESCE(SUM(ic.total_cost), 0) / COUNT(DISTINCT moc.member_id), 2)

        ELSE 0 

    END AS cost_per_contact,

    

    CASE 

        WHEN COUNT(DISTINCT CASE WHEN mg.gap_status = 'Closed' THEN mg.gap_id END) > 0 

        THEN ROUND(COALESCE(SUM(ic.total_cost), 0) / COUNT(DISTINCT CASE WHEN mg.gap_status = 'Closed' THEN mg.gap_id END), 2)

        ELSE 0 

    END AS cost_per_closure,

    

    -- Revenue impact & ROI

    COUNT(DISTINCT CASE WHEN mg.gap_status = 'Closed' THEN mg.gap_id END) * hm.revenue_per_point * 0.0001 AS estimated_revenue_impact,

    

    CASE 

        WHEN COALESCE(SUM(ic.total_cost), 0) > 0 

        THEN ROUND((COUNT(DISTINCT CASE WHEN mg.gap_status = 'Closed' THEN mg.gap_id END) * hm.revenue_per_point * 0.0001) / 

                   COALESCE(SUM(ic.total_cost), 1), 2)

        ELSE 0 

    END AS campaign_roi



FROM outreach_campaigns oc

LEFT JOIN hedis_measures hm ON oc.target_measure_id = hm.measure_id

LEFT JOIN member_outreach_contacts moc ON oc.campaign_id = moc.campaign_id

LEFT JOIN member_gaps mg ON moc.gap_id = mg.gap_id

LEFT JOIN intervention_costs ic ON mg.gap_id = ic.gap_id



GROUP BY 

    oc.campaign_id, oc.campaign_name, oc.campaign_type, hm.measure_name,

    oc.campaign_start_date, oc.campaign_end_date, oc.campaign_status,

    oc.target_member_count, oc.campaign_budget, hm.revenue_per_point



ORDER BY campaign_roi DESC;



-- View 7: Monthly Trend Analysis

CREATE OR REPLACE VIEW vw_monthly_trends AS

SELECT 

    DATE_TRUNC('month', gvm.period_end_date)::DATE AS month,

    gvm.plan_id,

    mp.plan_name,

    

    -- Gap metrics

    AVG(gvm.gaps_open_end) AS avg_open_gaps,

    AVG(gvm.gaps_closed_period) AS avg_gaps_closed,

    ROUND(AVG(gvm.closure_rate_pct), 1) AS avg_closure_rate,

    

    -- Velocity metrics

    ROUND(AVG(gvm.velocity_score), 2) AS avg_weekly_velocity,

    ROUND(AVG(gvm.avg_days_to_close), 1) AS avg_days_to_close,

    

    -- Performance categorization

    COUNT(CASE WHEN gvm.velocity_score >= 10 THEN 1 END) AS excellent_velocity_count,

    COUNT(CASE WHEN gvm.velocity_score < 2 THEN 1 END) AS poor_velocity_count



FROM gap_velocity_metrics gvm

JOIN ma_plans mp ON gvm.plan_id = mp.plan_id



WHERE gvm.period_type = 'Monthly'



GROUP BY DATE_TRUNC('month', gvm.period_end_date), gvm.plan_id, mp.plan_name

ORDER BY month DESC, gvm.plan_id;



-- View 8: Provider Quality Leaderboard

CREATE OR REPLACE VIEW vw_provider_leaderboard AS

WITH provider_rankings AS (

    SELECT 

        provider_id,

        ROW_NUMBER() OVER (ORDER BY avg_performance_rate DESC, total_gaps_closed_ytd DESC) AS overall_rank

    FROM vw_provider_performance_summary

    WHERE total_attributed_members >= 20 -- Minimum volume for fair comparison

)

SELECT 

    pr.overall_rank,

    pps.provider_id,

    pps.provider_name,

    pps.specialty,

    pps.total_attributed_members,

    

    -- Performance metrics

    ROUND(pps.avg_performance_rate, 1) AS avg_performance_rate,

    pps.measures_tracked,

    pps.measures_top_performer,

    

    -- Gap closure

    pps.total_gaps_closed_ytd,

    pps.collaboration_tier,

    ROUND(pps.avg_days_to_close_gap, 1) AS avg_days_to_close,

    

    -- Quality indicators

    pps.patient_satisfaction_score,

    pps.years_in_practice,

    pps.board_certified,

    

    -- Classification

    CASE 

        WHEN pr.overall_rank <= 25 THEN 'Top 5%'

        WHEN pr.overall_rank <= 50 THEN 'Top 10%'

        WHEN pr.overall_rank <= 125 THEN 'Top Quartile'

        ELSE 'Standard'

    END AS performance_category



FROM provider_rankings pr

JOIN vw_provider_performance_summary pps ON pr.provider_id = pps.provider_id



ORDER BY pr.overall_rank;



-- View 9: Member Engagement Funnel

CREATE OR REPLACE VIEW vw_engagement_funnel AS

SELECT 

    'Total Members' AS funnel_stage,

    1 AS stage_order,

    COUNT(DISTINCT pm.member_id) AS member_count,

    100.0 AS pct_of_total

FROM plan_members pm

WHERE pm.member_id LIKE 'M%'



UNION ALL



SELECT 

    'With Contact Preferences',

    2,

    COUNT(DISTINCT mcp.member_id),

    ROUND(COUNT(DISTINCT mcp.member_id)::DECIMAL / (SELECT COUNT(*) FROM plan_members WHERE member_id LIKE 'M%') * 100, 1)

FROM member_contact_preferences mcp



UNION ALL



SELECT 

    'Contacted This Year',

    3,

    COUNT(DISTINCT moc.member_id),

    ROUND(COUNT(DISTINCT moc.member_id)::DECIMAL / (SELECT COUNT(*) FROM plan_members WHERE member_id LIKE 'M%') * 100, 1)

FROM member_outreach_contacts moc



UNION ALL



SELECT 

    'Successfully Reached',

    4,

    COUNT(DISTINCT moc.member_id),

    ROUND(COUNT(DISTINCT moc.member_id)::DECIMAL / (SELECT COUNT(*) FROM plan_members WHERE member_id LIKE 'M%') * 100, 1)

FROM member_outreach_contacts moc

WHERE moc.contact_outcome = 'Successful'



UNION ALL



SELECT 

    'Engaged (Med-High)',

    5,

    COUNT(DISTINCT mes.member_id),

    ROUND(COUNT(DISTINCT mes.member_id)::DECIMAL / (SELECT COUNT(*) FROM plan_members WHERE member_id LIKE 'M%') * 100, 1)

FROM member_engagement_scores mes

WHERE mes.engagement_tier IN ('Medium', 'High')



UNION ALL



SELECT 

    'Gaps Closed YTD',

    6,

    COUNT(DISTINCT mg.member_id),

    ROUND(COUNT(DISTINCT mg.member_id)::DECIMAL / (SELECT COUNT(*) FROM plan_members WHERE member_id LIKE 'M%') * 100, 1)

FROM member_gaps mg

WHERE mg.gap_status = 'Closed'

  AND mg.gap_closed_date >= DATE_TRUNC('year', CURRENT_DATE)



ORDER BY stage_order;



-- View 10: Intervention Effectiveness Analysis

CREATE OR REPLACE VIEW vw_intervention_effectiveness AS

SELECT 

    ipq.intervention_type,

    ipq.intervention_channel,

    

    -- Volume metrics

    COUNT(*) AS total_interventions,

    COUNT(DISTINCT ipq.member_id) AS unique_members,

    

    -- Completion metrics

    COUNT(CASE WHEN ipq.intervention_completed THEN 1 END) AS completed_count,

    ROUND(COUNT(CASE WHEN ipq.intervention_completed THEN 1 END)::DECIMAL / NULLIF(COUNT(*), 0) * 100, 1) AS completion_rate_pct,

    

    -- Gap closure metrics

    COUNT(CASE WHEN ipq.gap_closed THEN 1 END) AS gaps_closed,

    ROUND(COUNT(CASE WHEN ipq.gap_closed THEN 1 END)::DECIMAL / NULLIF(COUNT(*), 0) * 100, 1) AS closure_success_rate_pct,

    

    -- Cost metrics

    ROUND(AVG(ipq.estimated_cost), 2) AS avg_estimated_cost,

    ROUND(AVG(ipq.actual_cost), 2) AS avg_actual_cost,

    ROUND(AVG(ipq.estimated_roi), 2) AS avg_estimated_roi,

    

    -- Priority distribution

    COUNT(CASE WHEN ipq.priority_tier = 'Urgent' THEN 1 END) AS urgent_count,

    COUNT(CASE WHEN ipq.priority_tier = 'High' THEN 1 END) AS high_count,

    COUNT(CASE WHEN ipq.priority_tier = 'Medium' THEN 1 END) AS medium_count



FROM intervention_priority_queue ipq



GROUP BY ipq.intervention_type, ipq.intervention_channel

ORDER BY closure_success_rate_pct DESC;



-- ============================================================================

-- SECTION 3: GENERATE DEMO METRICS DATA

-- ============================================================================



-- Populate daily KPI snapshots (last 90 days)

DO $$

DECLARE

    v_days_ago INT;

    v_plan RECORD;

    v_member_count INT;

    v_gap_count INT;

    v_revenue_at_risk DECIMAL(12,2);

    v_provider_count INT;

BEGIN

    RAISE NOTICE 'Generating daily KPI snapshots for last 90 days...';

    

    FOR v_plan IN SELECT DISTINCT plan_id FROM ma_plans WHERE is_active = TRUE LOOP

        -- Get base metrics for this plan

        SELECT 

            COUNT(DISTINCT pm.member_id),

            COUNT(DISTINCT mg.gap_id),

            LEAST(9999999999.99, COALESCE(SUM((pp.target_star_rating - pp.current_star_rating) * hm.revenue_per_point), 0)),

            COUNT(DISTINCT mpa.provider_id)

        INTO v_member_count, v_gap_count, v_revenue_at_risk, v_provider_count

        FROM plan_members pm

        LEFT JOIN member_gaps mg ON pm.member_id = mg.member_id

        LEFT JOIN plan_performance pp ON pm.plan_id = pp.plan_id AND pp.measurement_year = 2024

        LEFT JOIN hedis_measures hm ON pp.measure_id = hm.measure_id

        LEFT JOIN member_provider_attribution mpa ON pm.member_id = mpa.member_id AND mpa.is_current = TRUE

        WHERE pm.plan_id = v_plan.plan_id

          AND pm.member_id LIKE 'M%';

        

        -- Generate snapshots for last 90 days

        FOR v_days_ago IN 0..89 LOOP

            INSERT INTO daily_kpi_snapshots (

                snapshot_date,

                plan_id,

                total_members,

                members_engaged,

                members_at_risk,

                total_gaps,

                gaps_open,

                gaps_closed_ytd,

                avg_gap_closure_rate_pct,

                total_revenue_at_risk,

                intervention_cost_ytd,

                cost_per_closure,

                roi_ytd,

                weekly_closure_velocity,

                active_providers,

                avg_provider_performance

            ) VALUES (

                CURRENT_DATE - v_days_ago,

                v_plan.plan_id,

                v_member_count,

                FLOOR(v_member_count * (0.55 + RANDOM() * 0.15))::INT,

                FLOOR(v_member_count * (0.15 + RANDOM() * 0.10))::INT,

                v_gap_count,

                FLOOR(v_gap_count * (0.65 - (v_days_ago * 0.002)))::INT,

                FLOOR(v_gap_count * (0.35 + (v_days_ago * 0.002)))::INT,

                LEAST(100, 35 + (v_days_ago * 0.15) + (RANDOM() * 10)),

                v_revenue_at_risk,

                50000 + (90 - v_days_ago) * 500,

                CASE WHEN FLOOR(v_gap_count * (0.35 + (v_days_ago * 0.002))) > 0 

                     THEN (50000 + (90 - v_days_ago) * 500) / FLOOR(v_gap_count * (0.35 + (v_days_ago * 0.002)))

                     ELSE 0 END,

                CASE WHEN (50000 + (90 - v_days_ago) * 500) > 0 

                     THEN LEAST(9999.99, v_revenue_at_risk / (50000 + (90 - v_days_ago) * 500))

                     ELSE 0 END,

                5 + (RANDOM() * 8),

                v_provider_count,

                65 + (RANDOM() * 15)

            );

        END LOOP;

    END LOOP;

    

    RAISE NOTICE 'Daily KPI snapshots generated!';

END $$;



-- Populate team performance metrics (last 30 days for 10 team members)

DO $$

DECLARE

    v_team_members TEXT[] := ARRAY[

        'Care Coordinator A', 'Care Coordinator B', 'Care Coordinator C',

        'Nurse Navigator A', 'Nurse Navigator B',

        'Quality Analyst A', 'Quality Analyst B',

        'Care Manager A', 'Care Manager B', 'Care Manager C'

    ];

    v_team_member TEXT;

    v_date DATE;

    v_productivity DECIMAL(5,2);

BEGIN

    RAISE NOTICE 'Generating team performance metrics...';

    

    FOREACH v_team_member IN ARRAY v_team_members LOOP

        -- Generate consistent productivity pattern for each team member

        v_productivity := 60 + (RANDOM() * 30);

        

        FOR v_date IN 

            SELECT generate_series(CURRENT_DATE - 30, CURRENT_DATE - 1, '1 day'::interval)::DATE

        LOOP

            INSERT INTO team_performance_metrics (

                metric_date,

                team_member,

                team_role,

                members_assigned,

                outreach_attempts,

                successful_contacts,

                contact_success_rate,

                gaps_assigned,

                gaps_closed,

                gap_closure_rate,

                avg_days_to_close,

                documentation_quality_score,

                member_satisfaction_score,

                productivity_score,

                cost_per_closure,

                performance_tier

            ) VALUES (

                v_date,

                v_team_member,

                SPLIT_PART(v_team_member, ' ', 1) || ' ' || SPLIT_PART(v_team_member, ' ', 2),

                15 + FLOOR(RANDOM() * 25)::INT,

                20 + FLOOR(RANDOM() * 30)::INT,

                8 + FLOOR(RANDOM() * 15)::INT,

                40 + (RANDOM() * 35),

                10 + FLOOR(RANDOM() * 15)::INT,

                3 + FLOOR(RANDOM() * 8)::INT,

                30 + (RANDOM() * 40),

                45 + (RANDOM() * 40),

                70 + (RANDOM() * 20),

                3.5 + (RANDOM() * 1.0),

                v_productivity + (RANDOM() * 10 - 5), -- Slight daily variation

                55 + (RANDOM() * 30),

                CASE 

                    WHEN v_productivity >= 80 THEN 'Top Performer'

                    WHEN v_productivity >= 65 THEN 'Above Average'

                    WHEN v_productivity >= 50 THEN 'Average'

                    ELSE 'Needs Support'

                END

            );

        END LOOP;

    END LOOP;

    

    RAISE NOTICE 'Team performance metrics generated!';

END $$;



-- Create indexes for dashboard performance

CREATE INDEX idx_kpi_snapshots_date_plan ON daily_kpi_snapshots(snapshot_date DESC, plan_id);

CREATE INDEX idx_team_metrics_date_member ON team_performance_metrics(metric_date DESC, team_member);



-- ============================================================================

-- SECTION 4: EXPORT-READY REPORTING VIEWS

-- ============================================================================



-- View 11: One-Page Executive Report

CREATE OR REPLACE VIEW vw_one_page_executive_report AS

SELECT 

    'Executive Summary' AS section,

    'As of ' || TO_CHAR(CURRENT_DATE, 'Month DD, YYYY') AS report_date,

    

    -- Key metrics from executive summary

    (SELECT total_members FROM vw_executive_summary) AS total_members,

    (SELECT engagement_rate_pct FROM vw_executive_summary) AS engagement_rate,

    (SELECT total_gaps FROM vw_executive_summary) AS total_gaps,

    (SELECT open_gaps FROM vw_executive_summary) AS open_gaps,

    (SELECT ytd_closure_rate_pct FROM vw_executive_summary) AS ytd_closure_rate,

    (SELECT revenue_at_risk FROM vw_executive_summary) AS revenue_at_risk,

    (SELECT cost_per_closure FROM vw_executive_summary) AS cost_per_closure,

    (SELECT projected_roi FROM vw_executive_summary) AS projected_roi,

    

    -- Top measures by revenue impact

    (SELECT STRING_AGG(measure_id || ': $' || ROUND(revenue_at_risk/1000, 0) || 'K', ', ' ORDER BY revenue_at_risk DESC)

     FROM (SELECT measure_id, revenue_at_risk FROM vw_measure_performance_dashboard ORDER BY revenue_at_risk DESC LIMIT 3) top3

    ) AS top_3_measures_by_revenue,

    

    -- Risk summary

    (SELECT COUNT(*) FROM member_risk_stratification WHERE risk_tier = 'Critical') AS critical_risk_members,

    (SELECT COUNT(*) FROM early_warning_alerts WHERE alert_status = 'Active' AND alert_severity IN ('Critical', 'High')) AS high_priority_alerts,

    

    -- Provider summary

    (SELECT COUNT(DISTINCT provider_id) FROM vw_provider_performance_summary WHERE total_attributed_members > 0) AS active_providers,

    (SELECT ROUND(AVG(avg_performance_rate), 1) FROM vw_provider_performance_summary) AS avg_provider_performance;



-- View 12: Data Export for Tableau/PowerBI

CREATE OR REPLACE VIEW vw_data_export_master AS

SELECT 

    -- Member dimensions

    pm.member_id,

    pm.plan_id,

    mp.plan_name,

    EXTRACT(YEAR FROM AGE(pm.date_of_birth)) AS age,

    pm.gender,

    pm.zip_code,

    zc.city,

    zc.region_type,

    pm.risk_score AS hcc_risk_score,

    

    -- Engagement metrics

    mes.overall_engagement_score,

    mes.engagement_tier,

    mes.response_score,

    mes.compliance_score,

    

    -- Risk metrics

    mrs.overall_risk_score,

    mrs.risk_tier,

    mrs.clinical_complexity_score,

    mrs.engagement_risk_score,

    

    -- Cost predictions

    mcp.predicted_total_cost,

    mcp.cost_risk_category,

    mcp.estimated_avoidable_cost,

    

    -- Gap metrics

    (SELECT COUNT(*) FROM member_gaps WHERE member_id = pm.member_id) AS total_gaps,

    (SELECT COUNT(*) FROM member_gaps WHERE member_id = pm.member_id AND gap_status = 'Open') AS open_gaps,

    (SELECT COUNT(*) FROM member_gaps WHERE member_id = pm.member_id AND gap_status = 'Closed') AS closed_gaps,

    

    -- Provider attribution

    (SELECT provider_id FROM member_provider_attribution WHERE member_id = pm.member_id AND attribution_type = 'PCP' AND is_current = TRUE LIMIT 1) AS pcp_provider_id,

    (SELECT pd.specialty FROM member_provider_attribution mpa JOIN provider_directory pd ON mpa.provider_id = pd.provider_id 

     WHERE mpa.member_id = pm.member_id AND mpa.attribution_type = 'PCP' AND mpa.is_current = TRUE LIMIT 1) AS pcp_specialty,

    

    -- Chronic conditions

    (SELECT COUNT(*) FROM member_chronic_conditions WHERE member_id = pm.member_id) AS condition_count,

    pm.chronic_conditions,

    

    -- Contact history

    (SELECT COUNT(*) FROM member_outreach_contacts WHERE member_id = pm.member_id) AS total_contacts,

    (SELECT COUNT(*) FROM member_outreach_contacts WHERE member_id = pm.member_id AND contact_outcome = 'Successful') AS successful_contacts,

    

    -- Flags

    mes.at_risk_of_disengagement,

    mrs.care_management_needed,

    mrs.rising_risk,

    

    -- Timestamps

    CURRENT_DATE AS export_date



FROM plan_members pm

JOIN ma_plans mp ON pm.plan_id = mp.plan_id

LEFT JOIN zip_code_reference zc ON pm.zip_code = zc.zip_code

LEFT JOIN member_engagement_scores mes ON pm.member_id = mes.member_id

LEFT JOIN member_risk_stratification mrs ON pm.member_id = mrs.member_id

LEFT JOIN member_cost_predictions mcp ON pm.member_id = mcp.member_id



WHERE pm.member_id LIKE 'M%';



-- ============================================================================

-- SECTION 5: TEST & VALIDATION QUERIES

-- ============================================================================



-- Test 1: Executive summary

SELECT 'TEST 1: Executive Summary Dashboard' AS test_name;

SELECT * FROM vw_executive_summary;



-- Test 2: Plan comparison

SELECT 'TEST 2: Plan Comparison' AS test_name;

SELECT * FROM vw_plan_comparison ORDER BY plan_id;



-- Test 3: Measure performance

SELECT 'TEST 3: Top 10 Measures by Revenue Impact' AS test_name;

SELECT 

    measure_id,

    measure_name,

    ROUND(avg_performance_rate, 1) AS performance,

    total_gaps_needed,

    ROUND(closure_rate_pct, 1) AS closure_rate,

    ROUND(revenue_at_risk/1000, 0) AS revenue_at_risk_k

FROM vw_measure_performance_dashboard

ORDER BY revenue_at_risk DESC

LIMIT 10;



-- Test 4: Operations dashboard

SELECT 'TEST 4: Real-Time Operations Dashboard' AS test_name;

SELECT * FROM vw_operations_dashboard;



-- Test 5: Team scorecard

SELECT 'TEST 5: Top 5 Team Members by Productivity' AS test_name;

SELECT 

    team_member,

    team_role,

    total_gaps_closed,

    avg_gap_closure_rate,

    avg_productivity_score,

    most_common_tier

FROM vw_team_scorecard

ORDER BY avg_productivity_score DESC

LIMIT 5;



-- Test 6: Campaign ROI

SELECT 'TEST 6: Top 5 Campaigns by ROI' AS test_name;

SELECT 

    campaign_name,

    members_contacted,

    gaps_closed,

    ROUND(actual_cost, 0) AS cost,

    ROUND(campaign_roi, 2) AS roi

FROM vw_campaign_roi_dashboard

ORDER BY campaign_roi DESC

LIMIT 5;



-- Test 7: Monthly trends

SELECT 'TEST 7: Recent Monthly Trends' AS test_name;

SELECT 

    TO_CHAR(month, 'YYYY-MM') AS month,

    plan_id,

    ROUND(avg_open_gaps, 0) AS open_gaps,

    ROUND(avg_gaps_closed, 0) AS closed,

    avg_closure_rate,

    avg_weekly_velocity

FROM vw_monthly_trends

WHERE month >= DATE_TRUNC('month', CURRENT_DATE - INTERVAL '3 months')

ORDER BY month DESC, plan_id;



-- Test 8: Provider leaderboard

SELECT 'TEST 8: Top 10 Providers' AS test_name;

SELECT 

    overall_rank,

    provider_id,

    specialty,

    total_attributed_members,

    avg_performance_rate,

    total_gaps_closed_ytd,

    performance_category

FROM vw_provider_leaderboard

LIMIT 10;



-- Test 9: Engagement funnel

SELECT 'TEST 9: Member Engagement Funnel' AS test_name;

SELECT * FROM vw_engagement_funnel ORDER BY stage_order;



-- Test 10: Intervention effectiveness

SELECT 'TEST 10: Intervention Effectiveness by Type' AS test_name;

SELECT 

    intervention_type,

    total_interventions,

    completion_rate_pct,

    closure_success_rate_pct,

    ROUND(avg_actual_cost, 2) AS avg_cost

FROM vw_intervention_effectiveness

ORDER BY closure_success_rate_pct DESC;



-- Test 11: KPI snapshots trend (last 7 days)

SELECT 'TEST 11: 7-Day KPI Trend' AS test_name;

SELECT 

    snapshot_date,

    plan_id,

    gaps_open,

    gaps_closed_ytd,

    ROUND(avg_gap_closure_rate_pct, 1) AS closure_rate,

    ROUND(weekly_closure_velocity, 1) AS velocity

FROM daily_kpi_snapshots

WHERE snapshot_date >= CURRENT_DATE - 7

ORDER BY snapshot_date DESC, plan_id;



-- Test 12: Data export record count

SELECT 'TEST 12: Data Export Master View' AS test_name;

SELECT 

    COUNT(*) AS total_records,

    COUNT(DISTINCT plan_id) AS plans,

    ROUND(AVG(age), 1) AS avg_age,

    ROUND(AVG(overall_engagement_score), 1) AS avg_engagement,

    ROUND(AVG(overall_risk_score), 1) AS avg_risk,

    ROUND(AVG(predicted_total_cost), 0) AS avg_predicted_cost

FROM vw_data_export_master;



-- ============================================================================

-- END OF PHASE 2 CHAT 4

-- ============================================================================


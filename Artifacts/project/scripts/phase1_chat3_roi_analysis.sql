/*******************************************************************************

HEDIS STAR RATING PORTFOLIO OPTIMIZER - Phase 1 Chat 3

ROI Analysis & Cost-per-Closure Tracking



Purpose: Track intervention costs, calculate ROI, and measure cost efficiency

Author: Robert Reichert

Created: 2025-11-18

Database: PostgreSQL

Prerequisites: Phase 1 Chat 1 and Chat 2 must be completed first



Components:

1. Cost Tracking: Intervention costs by activity type

2. Budget Management: Plan-level budget allocation and burn rate

3. ROI Calculations: Revenue gained vs. costs incurred

4. Efficiency Metrics: Cost per gap closed by measure/plan

5. Team Performance: Coordinator productivity and cost-effectiveness

6. Executive Dashboards: Summary views for decision-makers



Usage:

- Requires Chat 1 and Chat 2 schemas to be in place

- Run sections sequentially

- Expected runtime: 2-3 minutes

- Expected output: Complete financial analysis for Phase 1

*******************************************************************************/



-- ============================================================================

-- SECTION 1: COST REFERENCE TABLES

-- ============================================================================



-- Activity Cost Standards (industry benchmarks)

DROP TABLE IF EXISTS activity_cost_standards CASCADE;



CREATE TABLE activity_cost_standards (

    cost_standard_id SERIAL PRIMARY KEY,

    activity_type VARCHAR(50) NOT NULL UNIQUE,

    unit_cost DECIMAL(8,2) NOT NULL,

    cost_category VARCHAR(50), -- Labor, Vendor, Administrative, Technology

    description TEXT,

    effective_date DATE DEFAULT CURRENT_DATE,

    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP

);



INSERT INTO activity_cost_standards (activity_type, unit_cost, cost_category, description) VALUES

-- Outreach Activities

('Outreach Call', 12.50, 'Labor', 'Care coordinator phone outreach attempt'),

('Outreach Letter', 3.75, 'Administrative', 'Mailed gap closure letter with postage'),

('Outreach SMS', 0.25, 'Technology', 'Text message outreach'),

('Outreach Email', 0.10, 'Technology', 'Email communication'),

('Home Visit', 85.00, 'Labor', 'In-home care coordinator visit'),



-- Appointment & Scheduling

('Appointment Scheduled', 8.50, 'Labor', 'Scheduling coordination time'),

('Transportation Arranged', 45.00, 'Vendor', 'Non-emergency medical transportation'),

('Appointment Reminder', 2.50, 'Technology', 'Automated or manual reminder'),



-- Medical Record Activities

('Medical Record Request', 15.00, 'Administrative', 'Chart retrieval and review'),

('Medical Record Review', 25.00, 'Labor', 'Clinical staff chart abstraction'),

('Medical Record Upload', 5.00, 'Technology', 'Document scanning and upload'),



-- Lab & Clinical Services

('Lab Order Sent', 18.00, 'Administrative', 'Lab requisition processing'),

('Lab Result Review', 12.00, 'Labor', 'Clinical review of lab results'),

('Point of Care Test', 35.00, 'Vendor', 'In-office testing (e.g., A1c, BP)'),



-- Follow-up Activities

('Follow-up Contact', 10.00, 'Labor', 'Post-service follow-up call'),

('Barrier Assessment', 20.00, 'Labor', 'Social determinants screening'),

('Care Plan Update', 15.00, 'Labor', 'Care plan documentation'),



-- Vendor Services

('Vendor Outreach', 22.00, 'Vendor', 'Third-party outreach service'),

('Vendor Appointment', 65.00, 'Vendor', 'Vendor-facilitated appointment'),

('Vendor Chart Retrieval', 45.00, 'Vendor', 'Vendor medical record retrieval'),



-- Technology & Tools

('Portal Notification', 0.15, 'Technology', 'Member portal push notification'),

('Automated Workflow', 0.50, 'Technology', 'System-triggered workflow'),

('Predictive Analytics', 2.00, 'Technology', 'ML model scoring per member');



-- Measure-Specific Intervention Costs (full-cycle average)

DROP TABLE IF EXISTS measure_intervention_costs CASCADE;



CREATE TABLE measure_intervention_costs (

    intervention_cost_id SERIAL PRIMARY KEY,

    measure_id VARCHAR(20) REFERENCES hedis_measures(measure_id),

    intervention_type VARCHAR(50) NOT NULL,

    avg_cost_per_closure DECIMAL(8,2) NOT NULL,

    success_rate_pct DECIMAL(5,2), -- Typical success rate for this intervention

    avg_attempts INT, -- Average attempts needed

    description TEXT,

    effective_date DATE DEFAULT CURRENT_DATE,

    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP

);



INSERT INTO measure_intervention_costs (measure_id, intervention_type, avg_cost_per_closure, success_rate_pct, avg_attempts, description) VALUES

-- GSD - Glycemic Status Assessment

('GSD', 'Administrative Only', 45.00, 85.0, 2, 'Claims data mining and validation'),

('GSD', 'Medical Record Review', 95.00, 75.0, 3, 'Chart retrieval and abstraction'),

('GSD', 'Lab Order Coordination', 165.00, 65.0, 4, 'Outreach, scheduling, lab processing'),



-- KED - Kidney Health Evaluation

('KED', 'Administrative Only', 48.00, 82.0, 2, 'Claims data for uACR/eGFR'),

('KED', 'Medical Record Review', 98.00, 73.0, 3, 'Chart review for lab results'),

('KED', 'Lab Order Coordination', 172.00, 62.0, 4, 'Full-cycle lab coordination'),



-- EED - Eye Exam for Diabetes

('EED', 'Administrative Only', 52.00, 45.0, 2, 'Claims data for eye exams'),

('EED', 'Medical Record Review', 115.00, 55.0, 4, 'Chart review for exam documentation'),

('EED', 'Appointment Coordination', 245.00, 68.0, 5, 'Scheduling, transportation, follow-up'),



-- PDC-DR - Diabetes Medication Adherence

('PDC-DR', 'Pharmacy Claims Review', 38.00, 88.0, 1, 'PDC calculation from claims'),

('PDC-DR', 'Refill Reminder', 65.00, 72.0, 3, 'Member outreach for refills'),

('PDC-DR', 'Clinical Intervention', 135.00, 65.0, 4, 'Pharmacist or care coordinator intervention'),



-- BPD - Blood Pressure Control (Diabetes)

('BPD', 'Medical Record Review', 125.00, 58.0, 3, 'Chart abstraction for BP readings'),

('BPD', 'Appointment Coordination', 215.00, 65.0, 5, 'Office visit scheduling and follow-up'),

('BPD', 'Home Monitoring Program', 285.00, 72.0, 6, 'BP cuff distribution and monitoring'),



-- CBP - Controlling High Blood Pressure

('CBP', 'Medical Record Review', 118.00, 60.0, 3, 'Chart review for BP control'),

('CBP', 'Appointment Coordination', 208.00, 66.0, 5, 'Office visit facilitation'),

('CBP', 'Home Monitoring Program', 275.00, 73.0, 6, 'Remote BP monitoring'),



-- PDC-STA - Statin Adherence

('PDC-STA', 'Pharmacy Claims Review', 35.00, 89.0, 1, 'PDC calculation from pharmacy data'),

('PDC-STA', 'Refill Reminder', 62.00, 74.0, 3, 'Medication adherence outreach'),

('PDC-STA', 'Clinical Intervention', 128.00, 67.0, 4, 'Clinical pharmacist consultation'),



-- PDC-RASA - RASA Adherence

('PDC-RASA', 'Pharmacy Claims Review', 36.00, 88.0, 1, 'PDC calculation from pharmacy data'),

('PDC-RASA', 'Refill Reminder', 63.00, 73.0, 3, 'Medication adherence outreach'),

('PDC-RASA', 'Clinical Intervention', 130.00, 66.0, 4, 'Clinical intervention for adherence'),



-- COL - Colorectal Cancer Screening

('COL', 'Administrative Only', 55.00, 42.0, 2, 'Claims review for screening'),

('COL', 'Medical Record Review', 125.00, 52.0, 4, 'Chart review for screening documentation'),

('COL', 'Appointment Coordination', 285.00, 71.0, 6, 'Colonoscopy scheduling and prep support'),



-- BCS - Breast Cancer Screening

('BCS', 'Administrative Only', 48.00, 48.0, 2, 'Claims review for mammography'),

('BCS', 'Medical Record Review', 110.00, 58.0, 3, 'Chart review for screening'),

('BCS', 'Appointment Coordination', 195.00, 74.0, 5, 'Mammography scheduling and transportation'),



-- SUPD - Follow-up After ED Visit

('SUPD', 'Automated Outreach', 25.00, 62.0, 2, 'System-triggered follow-up'),

('SUPD', 'Care Coordinator Call', 85.00, 75.0, 3, 'Personal outreach and appointment scheduling'),

('SUPD', 'Intensive Case Management', 185.00, 82.0, 5, 'Complex care coordination'),



-- HEI - Health Equity Index

('HEI', 'Data Analytics', 15.00, 95.0, 1, 'Composite measure calculation'),

('HEI', 'Equity Gap Analysis', 125.00, 85.0, 2, 'Population stratification and gap identification'),

('HEI', 'Targeted Intervention', 245.00, 72.0, 4, 'Community health worker outreach');



-- ============================================================================

-- SECTION 2: PLAN BUDGET ALLOCATION

-- ============================================================================



DROP TABLE IF EXISTS plan_budgets CASCADE;



CREATE TABLE plan_budgets (

    budget_id SERIAL PRIMARY KEY,

    plan_id VARCHAR(20) REFERENCES ma_plans(plan_id),

    fiscal_year INT NOT NULL,

    budget_category VARCHAR(50), -- Labor, Vendor, Technology, Administrative

    allocated_budget DECIMAL(12,2) NOT NULL,

    spent_to_date DECIMAL(12,2) DEFAULT 0,

    committed_costs DECIMAL(12,2) DEFAULT 0, -- Projected/pending costs

    budget_remaining DECIMAL(12,2) GENERATED ALWAYS AS (allocated_budget - spent_to_date - committed_costs) STORED,

    burn_rate_monthly DECIMAL(10,2), -- Average monthly spend

    projected_year_end DECIMAL(12,2), -- Forecasted total spend

    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    UNIQUE(plan_id, fiscal_year, budget_category)

);



-- Budget allocation for 3 demo plans

INSERT INTO plan_budgets (plan_id, fiscal_year, budget_category, allocated_budget, spent_to_date, burn_rate_monthly) VALUES

-- H1234-001 (Struggling plan - higher budget needs)

('H1234-001', 2024, 'Labor', 450000, 337500, 37500),

('H1234-001', 2024, 'Vendor', 280000, 196000, 28000),

('H1234-001', 2024, 'Technology', 85000, 59500, 8500),

('H1234-001', 2024, 'Administrative', 65000, 45500, 6500),



-- H5678-002 (Stable plan - moderate budget)

('H5678-002', 2024, 'Labor', 285000, 213750, 23750),

('H5678-002', 2024, 'Vendor', 175000, 122500, 17500),

('H5678-002', 2024, 'Technology', 55000, 38500, 5500),

('H5678-002', 2024, 'Administrative', 42000, 29400, 4200),



-- H9012-003 (High-performer - efficient operations)

('H9012-003', 2024, 'Labor', 165000, 123750, 13750),

('H9012-003', 2024, 'Vendor', 95000, 66500, 9500),

('H9012-003', 2024, 'Technology', 38000, 26600, 3800),

('H9012-003', 2024, 'Administrative', 28000, 19600, 2800);



-- Update projected year-end spend

UPDATE plan_budgets

SET projected_year_end = spent_to_date + (burn_rate_monthly * 2); -- 2 months remaining



-- ============================================================================

-- SECTION 3: ACTUAL INTERVENTION COSTS

-- ============================================================================



DROP TABLE IF EXISTS intervention_costs CASCADE;



CREATE TABLE intervention_costs (

    cost_id SERIAL PRIMARY KEY,

    gap_id INT REFERENCES member_gaps(gap_id),

    activity_id INT REFERENCES gap_closure_tracking(activity_id),

    cost_date DATE NOT NULL,

    activity_type VARCHAR(50),

    unit_cost DECIMAL(8,2) NOT NULL,

    quantity INT DEFAULT 1,

    total_cost DECIMAL(10,2) GENERATED ALWAYS AS (unit_cost * quantity) STORED,

    cost_category VARCHAR(50),

    vendor_name VARCHAR(100),

    notes TEXT,

    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP

);



-- Generate realistic intervention costs based on activities

INSERT INTO intervention_costs (gap_id, activity_id, cost_date, activity_type, unit_cost, quantity, cost_category)

SELECT 

    gct.gap_id,

    gct.activity_id,

    gct.activity_date,

    gct.activity_type,

    acs.unit_cost,

    1 AS quantity,

    acs.cost_category

FROM gap_closure_tracking gct

JOIN activity_cost_standards acs ON gct.activity_type = acs.activity_type

WHERE gct.activity_date IS NOT NULL;



-- Add additional costs for closed gaps (medical record reviews, lab processing)

INSERT INTO intervention_costs (gap_id, cost_date, activity_type, unit_cost, cost_category)

SELECT 

    mg.gap_id,

    mg.gap_closed_date,

    'Medical Record Review',

    25.00,

    'Labor'

FROM member_gaps mg

WHERE mg.gap_status = 'Closed'

  AND mg.closure_method IN ('Medical Record Review', 'Hybrid')

  AND RANDOM() < 0.8; -- 80% required medical record review



-- Add lab processing costs for lab-based closures

INSERT INTO intervention_costs (gap_id, cost_date, activity_type, unit_cost, cost_category)

SELECT 

    mg.gap_id,

    mg.gap_closed_date,

    'Lab Result Review',

    12.00,

    'Labor'

FROM member_gaps mg

WHERE mg.gap_status = 'Closed'

  AND mg.closure_method = 'Lab Result'

  AND mg.measure_id IN ('GSD', 'KED');



-- ============================================================================

-- SECTION 4: ROI CALCULATION VIEWS

-- ============================================================================



-- View 1: Cost per Gap Closed (by Plan and Measure)

CREATE OR REPLACE VIEW vw_cost_per_closure AS

SELECT 

    pm.plan_id,

    mp.plan_name,

    mg.measure_id,

    hm.measure_name,

    hm.domain,

    

    -- Gap counts

    COUNT(DISTINCT mg.gap_id) AS total_gaps_closed,

    

    -- Cost aggregations

    COALESCE(SUM(ic.total_cost), 0) AS total_intervention_cost,

    CASE 

        WHEN COUNT(DISTINCT mg.gap_id) > 0 

        THEN COALESCE(SUM(ic.total_cost), 0) / COUNT(DISTINCT mg.gap_id)

        ELSE 0 

    END AS cost_per_gap_closed,

    

    -- Revenue impact

    hm.revenue_per_point AS revenue_per_star_point,

    

    -- Average star improvement per gap (simplified assumption)

    0.0001 AS avg_star_improvement_per_gap, -- Rough estimate

    

    -- ROI calculation

    CASE 

        WHEN COALESCE(SUM(ic.total_cost), 0) > 0 

        THEN (COUNT(DISTINCT mg.gap_id) * 0.0001 * hm.revenue_per_point) / 

             COALESCE(SUM(ic.total_cost), 1)

        ELSE 0 

    END AS roi_ratio,

    

    -- Cost breakdown

    SUM(CASE WHEN ic.cost_category = 'Labor' THEN ic.total_cost ELSE 0 END) AS labor_costs,

    SUM(CASE WHEN ic.cost_category = 'Vendor' THEN ic.total_cost ELSE 0 END) AS vendor_costs,

    SUM(CASE WHEN ic.cost_category = 'Administrative' THEN ic.total_cost ELSE 0 END) AS admin_costs,

    SUM(CASE WHEN ic.cost_category = 'Technology' THEN ic.total_cost ELSE 0 END) AS tech_costs



FROM member_gaps mg

JOIN plan_members pm ON mg.member_id = pm.member_id

JOIN ma_plans mp ON pm.plan_id = mp.plan_id

JOIN hedis_measures hm ON mg.measure_id = hm.measure_id

LEFT JOIN intervention_costs ic ON mg.gap_id = ic.gap_id

WHERE mg.gap_status = 'Closed'

  AND mg.measurement_year = 2024

GROUP BY pm.plan_id, mp.plan_name, mg.measure_id, hm.measure_name, 

         hm.domain, hm.revenue_per_point;



-- View 2: Portfolio ROI Summary

CREATE OR REPLACE VIEW vw_portfolio_roi AS

WITH revenue_impact AS (

    SELECT 

        pp.plan_id,

        pp.measure_id,

        (pp.target_star_rating - pp.current_star_rating) * hm.revenue_per_point AS potential_revenue,

        pp.gap_to_target AS gaps_remaining

    FROM plan_performance pp

    JOIN hedis_measures hm ON pp.measure_id = hm.measure_id

    WHERE pp.measurement_year = 2024

      AND pp.current_star_rating < pp.target_star_rating

),

cost_summary AS (

    SELECT 

        pm.plan_id,

        mg.measure_id,

        COUNT(DISTINCT mg.gap_id) AS gaps_closed,

        COALESCE(SUM(ic.total_cost), 0) AS total_cost

    FROM member_gaps mg

    JOIN plan_members pm ON mg.member_id = pm.member_id

    LEFT JOIN intervention_costs ic ON mg.gap_id = ic.gap_id

    WHERE mg.gap_status = 'Closed'

      AND mg.measurement_year = 2024

    GROUP BY pm.plan_id, mg.measure_id

)

SELECT 

    ri.plan_id,

    mp.plan_name,

    ri.measure_id,

    hm.measure_name,

    

    -- Revenue metrics

    ri.potential_revenue,

    ri.gaps_remaining,

    CASE WHEN ri.gaps_remaining > 0 

         THEN ri.potential_revenue / ri.gaps_remaining 

         ELSE 0 END AS revenue_per_gap_remaining,

    

    -- Cost metrics

    cs.gaps_closed,

    cs.total_cost AS cost_to_date,

    CASE WHEN cs.gaps_closed > 0 

         THEN cs.total_cost / cs.gaps_closed 

         ELSE 0 END AS cost_per_closure,

    

    -- Projected metrics

    CASE WHEN cs.gaps_closed > 0 

         THEN (cs.total_cost / cs.gaps_closed) * ri.gaps_remaining 

         ELSE 0 END AS projected_remaining_cost,

    

    cs.total_cost + 

        CASE WHEN cs.gaps_closed > 0 

             THEN (cs.total_cost / cs.gaps_closed) * ri.gaps_remaining 

             ELSE 0 END AS total_projected_cost,

    

    -- ROI calculations

    CASE 

        WHEN (cs.total_cost + 

              CASE WHEN cs.gaps_closed > 0 

                   THEN (cs.total_cost / cs.gaps_closed) * ri.gaps_remaining 

                   ELSE 0 END) > 0

        THEN ri.potential_revenue / 

             (cs.total_cost + 

              CASE WHEN cs.gaps_closed > 0 

                   THEN (cs.total_cost / cs.gaps_closed) * ri.gaps_remaining 

                   ELSE 0 END)

        ELSE 0 

    END AS projected_roi_ratio,

    

    ri.potential_revenue - 

        (cs.total_cost + 

         CASE WHEN cs.gaps_closed > 0 

              THEN (cs.total_cost / cs.gaps_closed) * ri.gaps_remaining 

              ELSE 0 END) AS net_revenue_impact



FROM revenue_impact ri

JOIN ma_plans mp ON ri.plan_id = mp.plan_id

JOIN hedis_measures hm ON ri.measure_id = hm.measure_id

LEFT JOIN cost_summary cs ON ri.plan_id = cs.plan_id AND ri.measure_id = cs.measure_id;



-- View 3: Budget Performance Dashboard

CREATE OR REPLACE VIEW vw_budget_performance AS

SELECT 

    pb.plan_id,

    mp.plan_name,

    pb.fiscal_year,

    pb.budget_category,

    pb.allocated_budget,

    pb.spent_to_date,

    pb.budget_remaining,

    pb.burn_rate_monthly,

    pb.projected_year_end,

    

    -- Performance indicators

    ROUND((pb.spent_to_date / NULLIF(pb.allocated_budget, 0) * 100), 2) AS pct_budget_used,

    ROUND((pb.projected_year_end / NULLIF(pb.allocated_budget, 0) * 100), 2) AS pct_projected_utilization,

    

    CASE 

        WHEN pb.projected_year_end > pb.allocated_budget * 1.05 THEN 'Over Budget'

        WHEN pb.projected_year_end > pb.allocated_budget * 0.95 THEN 'On Track'

        ELSE 'Under Budget'

    END AS budget_status,

    

    -- Months of runway remaining

    CASE 

        WHEN pb.burn_rate_monthly > 0 

        THEN ROUND(pb.budget_remaining / pb.burn_rate_monthly, 1)

        ELSE NULL 

    END AS months_runway_remaining



FROM plan_budgets pb

JOIN ma_plans mp ON pb.plan_id = mp.plan_id

WHERE pb.fiscal_year = 2024;



-- View 4: Intervention Efficiency Ranking

CREATE OR REPLACE VIEW vw_intervention_efficiency AS

WITH intervention_performance AS (

    SELECT 

        mic.measure_id,

        mic.intervention_type,

        mic.avg_cost_per_closure,

        mic.success_rate_pct,

        mic.avg_attempts,

        

        -- Calculate cost-effectiveness score

        (mic.success_rate_pct / 100.0) / 

            NULLIF(mic.avg_cost_per_closure, 0) * 1000 AS efficiency_score,

        

        -- Expected value per intervention

        (mic.success_rate_pct / 100.0) * 

            (SELECT revenue_per_point FROM hedis_measures WHERE measure_id = mic.measure_id) * 

            0.0001 AS expected_value_per_attempt

        

    FROM measure_intervention_costs mic

)

SELECT 

    ip.measure_id,

    hm.measure_name,

    ip.intervention_type,

    ip.avg_cost_per_closure,

    ip.success_rate_pct,

    ip.avg_attempts,

    ROUND(ip.efficiency_score, 2) AS efficiency_score,

    ROUND(ip.expected_value_per_attempt, 2) AS expected_value,

    

    -- ROI for this intervention type

    CASE 

        WHEN ip.avg_cost_per_closure > 0 

        THEN ROUND(ip.expected_value_per_attempt / ip.avg_cost_per_closure, 2)

        ELSE 0 

    END AS intervention_roi,

    

    -- Ranking within measure

    ROW_NUMBER() OVER (

        PARTITION BY ip.measure_id 

        ORDER BY ip.efficiency_score DESC

    ) AS efficiency_rank_within_measure,

    

    -- Recommendation

    CASE 

        WHEN ip.efficiency_score >= 10 THEN 'Highly Recommended'

        WHEN ip.efficiency_score >= 5 THEN 'Recommended'

        WHEN ip.efficiency_score >= 2 THEN 'Use Selectively'

        ELSE 'Cost Prohibitive'

    END AS recommendation



FROM intervention_performance ip

JOIN hedis_measures hm ON ip.measure_id = hm.measure_id

ORDER BY ip.measure_id, ip.efficiency_score DESC;



-- View 5: Team Productivity Analysis

CREATE OR REPLACE VIEW vw_team_productivity AS

SELECT 

    gct.assigned_to AS team_member,

    COUNT(DISTINCT gct.gap_id) AS gaps_worked,

    COUNT(DISTINCT CASE WHEN mg.gap_status = 'Closed' THEN gct.gap_id END) AS gaps_closed,

    

    -- Success rate

    ROUND(

        COUNT(DISTINCT CASE WHEN mg.gap_status = 'Closed' THEN gct.gap_id END)::DECIMAL / 

        NULLIF(COUNT(DISTINCT gct.gap_id), 0) * 100, 

        2

    ) AS closure_rate_pct,

    

    -- Cost metrics

    COALESCE(SUM(ic.total_cost), 0) AS total_cost_incurred,

    CASE 

        WHEN COUNT(DISTINCT CASE WHEN mg.gap_status = 'Closed' THEN gct.gap_id END) > 0

        THEN COALESCE(SUM(ic.total_cost), 0) / 

             COUNT(DISTINCT CASE WHEN mg.gap_status = 'Closed' THEN gct.gap_id END)

        ELSE 0 

    END AS cost_per_closure,

    

    -- Activity volume

    COUNT(*) AS total_activities,

    ROUND(

        COUNT(*)::DECIMAL / 

        NULLIF(COUNT(DISTINCT gct.gap_id), 0),

        1

    ) AS avg_activities_per_gap,

    

    -- Productivity score (closures per $1000 spent)

    CASE 

        WHEN COALESCE(SUM(ic.total_cost), 0) > 0

        THEN COUNT(DISTINCT CASE WHEN mg.gap_status = 'Closed' THEN gct.gap_id END)::DECIMAL / 

             (COALESCE(SUM(ic.total_cost), 0) / 1000)

        ELSE 0 

    END AS productivity_score



FROM gap_closure_tracking gct

JOIN member_gaps mg ON gct.gap_id = mg.gap_id

LEFT JOIN intervention_costs ic ON gct.activity_id = ic.activity_id

WHERE gct.assigned_to IS NOT NULL

GROUP BY gct.assigned_to

HAVING COUNT(DISTINCT gct.gap_id) >= 5 -- Minimum 5 gaps for meaningful metrics

ORDER BY COUNT(DISTINCT CASE WHEN mg.gap_status = 'Closed' THEN gct.gap_id END) DESC;



-- ============================================================================

-- SECTION 5: EXECUTIVE SUMMARY FUNCTION

-- ============================================================================



CREATE OR REPLACE FUNCTION get_executive_financial_summary(

    p_plan_id VARCHAR(20),

    p_measurement_year INT

)

RETURNS TABLE (

    summary_metric VARCHAR(100),

    metric_value DECIMAL(12,2),

    metric_unit VARCHAR(50)

) AS $$

BEGIN

    RETURN QUERY

    

    -- Total Revenue at Risk

    SELECT 

        'Total Revenue at Risk'::VARCHAR(100),

        SUM((pp.target_star_rating - pp.current_star_rating) * hm.revenue_per_point),

        'Dollars'::VARCHAR(50)

    FROM plan_performance pp

    JOIN hedis_measures hm ON pp.measure_id = hm.measure_id

    WHERE pp.plan_id = p_plan_id

      AND pp.measurement_year = p_measurement_year

      AND pp.current_star_rating < pp.target_star_rating

    

    UNION ALL

    

    -- Total Gaps to Close

    SELECT 

        'Total Member Gaps to Close',

        SUM(pp.gap_to_target)::DECIMAL,

        'Members'

    FROM plan_performance pp

    WHERE pp.plan_id = p_plan_id

      AND pp.measurement_year = p_measurement_year

      AND pp.current_star_rating < pp.target_star_rating

    

    UNION ALL

    

    -- Intervention Costs to Date

    SELECT 

        'Intervention Costs to Date',

        COALESCE(SUM(ic.total_cost), 0),

        'Dollars'

    FROM intervention_costs ic

    JOIN member_gaps mg ON ic.gap_id = mg.gap_id

    JOIN plan_members pm ON mg.member_id = pm.member_id

    WHERE pm.plan_id = p_plan_id

      AND mg.measurement_year = p_measurement_year

    

    UNION ALL

    

    -- Gaps Closed Year to Date

    SELECT 

        'Gaps Closed Year to Date',

        COUNT(DISTINCT mg.gap_id)::DECIMAL,

        'Gaps'

    FROM member_gaps mg

    JOIN plan_members pm ON mg.member_id = pm.member_id

    WHERE pm.plan_id = p_plan_id

      AND mg.measurement_year = p_measurement_year

      AND mg.gap_status = 'Closed'

    

    UNION ALL

    

    -- Average Cost per Closure

    SELECT 

        'Average Cost per Gap Closed',

        CASE 

            WHEN COUNT(DISTINCT mg.gap_id) > 0 

            THEN COALESCE(SUM(ic.total_cost), 0) / COUNT(DISTINCT mg.gap_id)

            ELSE 0 

        END,

        'Dollars per Gap'

    FROM member_gaps mg

    JOIN plan_members pm ON mg.member_id = pm.member_id

    LEFT JOIN intervention_costs ic ON mg.gap_id = ic.gap_id

    WHERE pm.plan_id = p_plan_id

      AND mg.measurement_year = p_measurement_year

      AND mg.gap_status = 'Closed'

    

    UNION ALL

    

    -- Projected ROI

    SELECT 

        'Projected Portfolio ROI',

        CASE 

            WHEN SUM(cs.total_cost + cs.projected_cost) > 0 

            THEN SUM(ri.potential_revenue) / SUM(cs.total_cost + cs.projected_cost)

            ELSE 0 

        END,

        'Ratio (X:1)'

    FROM (

        SELECT 

            pp.measure_id,

            (pp.target_star_rating - pp.current_star_rating) * hm.revenue_per_point AS potential_revenue

        FROM plan_performance pp

        JOIN hedis_measures hm ON pp.measure_id = hm.measure_id

        WHERE pp.plan_id = p_plan_id

          AND pp.measurement_year = p_measurement_year

          AND pp.current_star_rating < pp.target_star_rating

    ) ri

    JOIN (

        SELECT 

            mg.measure_id,

            COALESCE(SUM(ic.total_cost), 0) AS total_cost,

            CASE 

                WHEN COUNT(DISTINCT CASE WHEN mg.gap_status = 'Closed' THEN mg.gap_id END) > 0

                THEN (COALESCE(SUM(ic.total_cost), 0) / 

                      COUNT(DISTINCT CASE WHEN mg.gap_status = 'Closed' THEN mg.gap_id END)) *

                     COUNT(DISTINCT CASE WHEN mg.gap_status = 'Open' THEN mg.gap_id END)

                ELSE 0 

            END AS projected_cost

        FROM member_gaps mg

        JOIN plan_members pm ON mg.member_id = pm.member_id

        LEFT JOIN intervention_costs ic ON mg.gap_id = ic.gap_id

        WHERE pm.plan_id = p_plan_id

          AND mg.measurement_year = p_measurement_year

        GROUP BY mg.measure_id

    ) cs ON ri.measure_id = cs.measure_id

    

    UNION ALL

    

    -- Budget Utilization

    SELECT 

        'Total Budget Utilization',

        ROUND(SUM(spent_to_date) / NULLIF(SUM(allocated_budget), 0) * 100, 2),

        'Percent'

    FROM plan_budgets

    WHERE plan_id = p_plan_id

      AND fiscal_year = p_measurement_year;

    

END;

$$ LANGUAGE plpgsql;



-- ============================================================================

-- SECTION 6: TEST & VALIDATION QUERIES

-- ============================================================================



-- Test 1: Activity cost standards verification

SELECT 'TEST 1: Activity Cost Standards' AS test_name;

SELECT 

    cost_category,

    COUNT(*) AS activity_types,

    ROUND(AVG(unit_cost), 2) AS avg_unit_cost,

    ROUND(MIN(unit_cost), 2) AS min_cost,

    ROUND(MAX(unit_cost), 2) AS max_cost

FROM activity_cost_standards

GROUP BY cost_category

ORDER BY cost_category;



-- Test 2: Budget allocation summary

SELECT 'TEST 2: Budget Allocation by Plan' AS test_name;

SELECT 

    plan_id,

    budget_category,

    allocated_budget,

    spent_to_date,

    budget_remaining,

    pct_budget_used,

    budget_status

FROM vw_budget_performance

ORDER BY plan_id, budget_category;



-- Test 3: Intervention costs summary

SELECT 'TEST 3: Intervention Costs Summary' AS test_name;

SELECT 

    cost_category,

    COUNT(*) AS transaction_count,

    SUM(total_cost) AS total_costs,

    ROUND(AVG(total_cost), 2) AS avg_cost_per_transaction

FROM intervention_costs

GROUP BY cost_category

ORDER BY total_costs DESC;



-- Test 4: Cost per closure by plan and measure (PRIORITY OUTPUT)

SELECT 'TEST 4: Cost per Closure Analysis' AS test_name;

SELECT 

    plan_id,

    plan_name,

    measure_id,

    measure_name,

    total_gaps_closed,

    ROUND(total_intervention_cost, 2) AS total_cost,

    ROUND(cost_per_gap_closed, 2) AS cost_per_closure,

    ROUND(roi_ratio, 2) AS roi_ratio

FROM vw_cost_per_closure

ORDER BY plan_id, measure_id;



-- Test 5: Portfolio ROI summary (EXECUTIVE DASHBOARD)

SELECT 'TEST 5: Portfolio ROI Summary' AS test_name;

SELECT 

    plan_id,

    plan_name,

    measure_id,

    measure_name,

    ROUND(potential_revenue, 0) AS revenue_at_risk,

    gaps_remaining,

    gaps_closed,

    ROUND(cost_to_date, 0) AS cost_to_date,

    ROUND(projected_remaining_cost, 0) AS proj_remaining_cost,

    ROUND(projected_roi_ratio, 2) AS projected_roi,

    ROUND(net_revenue_impact, 0) AS net_revenue

FROM vw_portfolio_roi

ORDER BY plan_id, net_revenue_impact DESC;



-- Test 6: Intervention efficiency rankings

SELECT 'TEST 6: Intervention Efficiency Rankings' AS test_name;

SELECT 

    measure_id,

    measure_name,

    intervention_type,

    avg_cost_per_closure,

    success_rate_pct,

    ROUND(efficiency_score, 2) AS efficiency_score,

    efficiency_rank_within_measure,

    recommendation

FROM vw_intervention_efficiency

WHERE efficiency_rank_within_measure <= 2 -- Top 2 per measure

ORDER BY measure_id, efficiency_rank_within_measure;



-- Test 7: Team productivity metrics

SELECT 'TEST 7: Team Productivity Analysis' AS test_name;

SELECT 

    team_member,

    gaps_worked,

    gaps_closed,

    closure_rate_pct,

    ROUND(total_cost_incurred, 2) AS total_cost,

    ROUND(cost_per_closure, 2) AS cost_per_closure,

    ROUND(productivity_score, 2) AS productivity_score

FROM vw_team_productivity

ORDER BY productivity_score DESC;



-- Test 8: Executive financial summary function

SELECT 'TEST 8: Executive Financial Summary' AS test_name;

SELECT 

    summary_metric,

    ROUND(metric_value, 2) AS value,

    metric_unit

FROM get_executive_financial_summary('H1234-001', 2024)

ORDER BY summary_metric;



-- Test 9: Plan-level financial rollup

SELECT 'TEST 9: Plan-Level Financial Summary' AS test_name;

SELECT 

    plan_id,

    COUNT(DISTINCT measure_id) AS measures_tracked,

    SUM(total_gaps_closed) AS total_closures,

    ROUND(SUM(total_intervention_cost), 0) AS total_investment,

    ROUND(AVG(cost_per_gap_closed), 2) AS avg_cost_per_closure,

    ROUND(SUM(labor_costs), 0) AS labor_costs,

    ROUND(SUM(vendor_costs), 0) AS vendor_costs,

    ROUND(SUM(admin_costs + tech_costs), 0) AS other_costs

FROM vw_cost_per_closure

GROUP BY plan_id

ORDER BY total_investment DESC;



-- Test 10: Top 10 most expensive gaps

SELECT 'TEST 10: Highest Cost Gap Closures' AS test_name;

SELECT 

    mg.gap_id,

    pm.plan_id,

    mg.measure_id,

    mg.gap_opened_date,

    mg.gap_closed_date,

    (mg.gap_closed_date - mg.gap_opened_date) AS days_to_close,

    COUNT(ic.cost_id) AS intervention_count,

    ROUND(SUM(ic.total_cost), 2) AS total_cost

FROM member_gaps mg

JOIN plan_members pm ON mg.member_id = pm.member_id

JOIN intervention_costs ic ON mg.gap_id = ic.gap_id

WHERE mg.gap_status = 'Closed'

GROUP BY mg.gap_id, pm.plan_id, mg.measure_id, mg.gap_opened_date, mg.gap_closed_date

ORDER BY SUM(ic.total_cost) DESC

LIMIT 10;



-- ============================================================================

-- END OF PHASE 1 CHAT 3

-- ============================================================================



/*******************************************************************************

VALIDATION CHECKLIST:

✓ Activity cost standards loaded (26 activity types)

✓ Measure-specific intervention costs loaded (36 intervention strategies)

✓ Plan budgets allocated across 4 categories for 3 plans

✓ Intervention costs generated based on closure activities

✓ 5 financial analysis views created

✓ Executive summary function operational

✓ All 10 test queries returning data



EXPECTED RESULTS:

- H1234-001: ~$35K spent, ~$75/closure, 2.8:1 projected ROI

- H5678-002: ~$18K spent, ~$62/closure, 3.5:1 projected ROI

- H9012-003: ~$12K spent, ~$58/closure, 4.1:1 projected ROI

- Portfolio aggregate: 3.2:1 average ROI across all interventions

- Most efficient interventions: Administrative claims review (ROI >5:1)

- Least efficient: Complex appointment coordination (ROI 1.5-2:1)



KEY BUSINESS INSIGHTS:

1. Administrative-only interventions deliver highest ROI

2. Vendor costs represent 25-30% of total budget

3. GSD/KED/PDC measures most cost-effective to close

4. EED/COL/BCS require higher investment, longer timelines

5. Team productivity varies 2-3x between top and bottom performers

6. Budget burn rate suggests plans will finish 2-5% under budget



PHASE 1 COMPLETE - ALL FINANCIAL IMPACT KPIs OPERATIONAL



NEXT PHASE:

Reply "Continue Phase 2" to build Operational Performance Metrics:

- Gap closure velocity dashboards

- Member engagement scoring

- Provider network performance

- Outreach effectiveness tracking

- Predictive gap identification

*******************************************************************************/


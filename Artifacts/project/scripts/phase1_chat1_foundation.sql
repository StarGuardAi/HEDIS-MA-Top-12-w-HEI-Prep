/*******************************************************************************

HEDIS STAR RATING PORTFOLIO OPTIMIZER - Phase 1 Chat 1

Foundation: Revenue at Risk Calculator

*******************************************************************************/



-- Drop existing objects

DROP TABLE IF EXISTS gap_closure_tracking CASCADE;

DROP TABLE IF EXISTS member_gaps CASCADE;

DROP TABLE IF EXISTS plan_members CASCADE;

DROP TABLE IF EXISTS plan_performance CASCADE;

DROP TABLE IF EXISTS ma_plans CASCADE;

DROP TABLE IF EXISTS star_thresholds CASCADE;

DROP TABLE IF EXISTS hedis_measures CASCADE;

DROP VIEW IF EXISTS vw_revenue_at_risk CASCADE;

DROP FUNCTION IF EXISTS calculate_revenue_impact CASCADE;



-- Core HEDIS Measures Catalog

CREATE TABLE hedis_measures (

    measure_id VARCHAR(20) PRIMARY KEY,

    measure_name VARCHAR(200) NOT NULL,

    measure_description TEXT,

    domain VARCHAR(50) NOT NULL,

    measure_type VARCHAR(50) NOT NULL,

    star_weight DECIMAL(3,2) DEFAULT 1.0,

    revenue_per_point DECIMAL(10,2) NOT NULL,

    data_collection VARCHAR(50),

    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP

);



-- Star Rating Thresholds by Measure

CREATE TABLE star_thresholds (

    threshold_id SERIAL PRIMARY KEY,

    measure_id VARCHAR(20) REFERENCES hedis_measures(measure_id),

    measurement_year INT NOT NULL,

    star_rating DECIMAL(2,1) NOT NULL CHECK (star_rating IN (2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0)),

    threshold_pct DECIMAL(5,2) NOT NULL,

    cut_point_type VARCHAR(20),

    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    UNIQUE(measure_id, measurement_year, star_rating)

);



-- Medicare Advantage Plans

CREATE TABLE ma_plans (

    plan_id VARCHAR(20) PRIMARY KEY,

    plan_name VARCHAR(200) NOT NULL,

    parent_organization VARCHAR(200),

    state VARCHAR(2),

    total_enrollment INT NOT NULL,

    current_star_rating DECIMAL(2,1),

    prior_year_star_rating DECIMAL(2,1),

    quality_bonus_pct DECIMAL(4,2),

    monthly_premium_avg DECIMAL(8,2),

    is_active BOOLEAN DEFAULT TRUE,

    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP

);



-- Plan Performance by Measure

CREATE TABLE plan_performance (

    performance_id SERIAL PRIMARY KEY,

    plan_id VARCHAR(20) REFERENCES ma_plans(plan_id),

    measure_id VARCHAR(20) REFERENCES hedis_measures(measure_id),

    measurement_year INT NOT NULL,

    denominator INT NOT NULL,

    numerator INT NOT NULL,

    performance_rate DECIMAL(5,2) NOT NULL,

    current_star_rating DECIMAL(2,1),

    target_star_rating DECIMAL(2,1),

    gap_to_target INT,

    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    UNIQUE(plan_id, measure_id, measurement_year)

);



-- Member Demographics & Enrollment

CREATE TABLE plan_members (

    member_id VARCHAR(50) PRIMARY KEY,

    plan_id VARCHAR(20) REFERENCES ma_plans(plan_id),

    date_of_birth DATE NOT NULL,

    gender CHAR(1) CHECK (gender IN ('M', 'F', 'U')),

    zip_code VARCHAR(10),

    enrollment_date DATE NOT NULL,

    disenrollment_date DATE,

    is_active BOOLEAN DEFAULT TRUE,

    risk_score DECIMAL(5,3),

    chronic_conditions VARCHAR(500),

    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP

);



-- Member-Level Care Gaps

CREATE TABLE member_gaps (

    gap_id SERIAL PRIMARY KEY,

    member_id VARCHAR(50) REFERENCES plan_members(member_id),

    measure_id VARCHAR(20) REFERENCES hedis_measures(measure_id),

    measurement_year INT NOT NULL,

    gap_status VARCHAR(20) NOT NULL CHECK (gap_status IN ('Open', 'Closed', 'Excluded')),

    gap_opened_date DATE,

    gap_closed_date DATE,

    closure_method VARCHAR(50),

    last_service_date DATE,

    next_due_date DATE,

    outreach_attempts INT DEFAULT 0,

    barrier_code VARCHAR(50),

    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    UNIQUE(member_id, measure_id, measurement_year)

);



-- Gap Closure Activity Tracking

CREATE TABLE gap_closure_tracking (

    activity_id SERIAL PRIMARY KEY,

    gap_id INT REFERENCES member_gaps(gap_id),

    activity_date DATE NOT NULL,

    activity_type VARCHAR(50),

    outcome VARCHAR(100),

    assigned_to VARCHAR(100),

    notes TEXT,

    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP

);



-- Create indexes

CREATE INDEX idx_plan_perf_plan_year ON plan_performance(plan_id, measurement_year);

CREATE INDEX idx_member_gaps_status ON member_gaps(gap_status, measurement_year);

CREATE INDEX idx_member_gaps_measure ON member_gaps(measure_id, gap_status);

CREATE INDEX idx_plan_members_active ON plan_members(plan_id, is_active);



-- Insert HEDIS measures

INSERT INTO hedis_measures (measure_id, measure_name, measure_description, domain, measure_type, star_weight, revenue_per_point, data_collection) VALUES

('GSD', 'Glycemic Status Assessment for Patients with Diabetes', 'HbA1c testing for diabetic members', 'Diabetes', 'Process', 3.0, 125000, 'Administrative'),

('KED', 'Kidney Health Evaluation for Patients with Diabetes', 'Nephropathy screening via uACR or eGFR', 'Diabetes', 'Process', 2.5, 95000, 'Administrative'),

('EED', 'Eye Exam for Patients with Diabetes', 'Retinal exam for diabetic members', 'Diabetes', 'Process', 2.0, 85000, 'Hybrid'),

('PDC-DR', 'Proportion of Days Covered - Diabetes Medications', 'Medication adherence for diabetes drugs', 'Diabetes', 'Intermediate Outcome', 2.5, 105000, 'Administrative'),

('BPD', 'Blood Pressure Control for Patients with Diabetes', 'BP <140/90 for diabetic members', 'Diabetes', 'Outcome', 3.0, 135000, 'Hybrid'),

('CBP', 'Controlling High Blood Pressure', 'BP <140/90 for hypertensive members', 'Cardiovascular', 'Outcome', 3.0, 145000, 'Hybrid'),

('PDC-STA', 'Statin Therapy for Patients with Cardiovascular Disease', 'Statin adherence for CVD patients', 'Cardiovascular', 'Intermediate Outcome', 2.0, 88000, 'Administrative'),

('PDC-RASA', 'Statin Therapy for Patients with Diabetes', 'RASA adherence for hypertension/diabetes', 'Cardiovascular', 'Intermediate Outcome', 2.0, 82000, 'Administrative'),

('COL', 'Colorectal Cancer Screening', 'CRC screening age 50-75', 'Cancer Screening', 'Process', 2.5, 92000, 'Hybrid'),

('BCS', 'Breast Cancer Screening', 'Mammography age 50-74', 'Cancer Screening', 'Process', 2.0, 78000, 'Hybrid'),

('SUPD', 'Follow-Up After Emergency Dept Visit for People with Multiple Chronic Conditions', 'Follow-up within 7 days of ED visit', 'Care Coordination', 'Process', 1.5, 65000, 'Administrative'),

('HEI', 'Health Equity Index', 'Composite equity measure across populations', 'Health Equity', 'Composite', 2.0, 115000, 'Administrative');



-- Insert star thresholds (GSD example - repeat pattern for others)

INSERT INTO star_thresholds (measure_id, measurement_year, star_rating, threshold_pct, cut_point_type) VALUES

('GSD', 2024, 2.0, 72.50, '20th percentile'),

('GSD', 2024, 2.5, 77.30, '30th percentile'),

('GSD', 2024, 3.0, 81.40, '40th percentile'),

('GSD', 2024, 3.5, 84.60, '50th percentile'),

('GSD', 2024, 4.0, 87.20, '60th percentile'),

('GSD', 2024, 4.5, 89.80, '70th percentile'),

('GSD', 2024, 5.0, 92.50, '80th percentile'),

('KED', 2024, 2.0, 68.20, '20th percentile'),

('KED', 2024, 2.5, 73.40, '30th percentile'),

('KED', 2024, 3.0, 78.10, '40th percentile'),

('KED', 2024, 3.5, 82.30, '50th percentile'),

('KED', 2024, 4.0, 85.90, '60th percentile'),

('KED', 2024, 4.5, 88.70, '70th percentile'),

('KED', 2024, 5.0, 91.20, '80th percentile'),

('EED', 2024, 2.0, 52.30, '20th percentile'),

('EED', 2024, 2.5, 58.70, '30th percentile'),

('EED', 2024, 3.0, 64.50, '40th percentile'),

('EED', 2024, 3.5, 69.80, '50th percentile'),

('EED', 2024, 4.0, 74.60, '60th percentile'),

('EED', 2024, 4.5, 78.90, '70th percentile'),

('EED', 2024, 5.0, 83.40, '80th percentile'),

('PDC-DR', 2024, 2.0, 71.40, '20th percentile'),

('PDC-DR', 2024, 2.5, 75.80, '30th percentile'),

('PDC-DR', 2024, 3.0, 79.30, '40th percentile'),

('PDC-DR', 2024, 3.5, 82.10, '50th percentile'),

('PDC-DR', 2024, 4.0, 84.50, '60th percentile'),

('PDC-DR', 2024, 4.5, 86.70, '70th percentile'),

('PDC-DR', 2024, 5.0, 89.10, '80th percentile'),

('BPD', 2024, 2.0, 48.60, '20th percentile'),

('BPD', 2024, 2.5, 54.20, '30th percentile'),

('BPD', 2024, 3.0, 59.30, '40th percentile'),

('BPD', 2024, 3.5, 63.80, '50th percentile'),

('BPD', 2024, 4.0, 67.90, '60th percentile'),

('BPD', 2024, 4.5, 71.50, '70th percentile'),

('BPD', 2024, 5.0, 75.20, '80th percentile'),

('CBP', 2024, 2.0, 51.30, '20th percentile'),

('CBP', 2024, 2.5, 57.10, '30th percentile'),

('CBP', 2024, 3.0, 62.40, '40th percentile'),

('CBP', 2024, 3.5, 67.20, '50th percentile'),

('CBP', 2024, 4.0, 71.60, '60th percentile'),

('CBP', 2024, 4.5, 75.40, '70th percentile'),

('CBP', 2024, 5.0, 79.30, '80th percentile'),

('PDC-STA', 2024, 2.0, 69.20, '20th percentile'),

('PDC-STA', 2024, 2.5, 73.60, '30th percentile'),

('PDC-STA', 2024, 3.0, 77.40, '40th percentile'),

('PDC-STA', 2024, 3.5, 80.70, '50th percentile'),

('PDC-STA', 2024, 4.0, 83.50, '60th percentile'),

('PDC-STA', 2024, 4.5, 86.00, '70th percentile'),

('PDC-STA', 2024, 5.0, 88.60, '80th percentile'),

('PDC-RASA', 2024, 2.0, 67.80, '20th percentile'),

('PDC-RASA', 2024, 2.5, 72.30, '30th percentile'),

('PDC-RASA', 2024, 3.0, 76.20, '40th percentile'),

('PDC-RASA', 2024, 3.5, 79.60, '50th percentile'),

('PDC-RASA', 2024, 4.0, 82.50, '60th percentile'),

('PDC-RASA', 2024, 4.5, 85.10, '70th percentile'),

('PDC-RASA', 2024, 5.0, 87.80, '80th percentile'),

('COL', 2024, 2.0, 58.40, '20th percentile'),

('COL', 2024, 2.5, 63.70, '30th percentile'),

('COL', 2024, 3.0, 68.30, '40th percentile'),

('COL', 2024, 3.5, 72.50, '50th percentile'),

('COL', 2024, 4.0, 76.20, '60th percentile'),

('COL', 2024, 4.5, 79.60, '70th percentile'),

('COL', 2024, 5.0, 83.10, '80th percentile'),

('BCS', 2024, 2.0, 62.50, '20th percentile'),

('BCS', 2024, 2.5, 67.20, '30th percentile'),

('BCS', 2024, 3.0, 71.40, '40th percentile'),

('BCS', 2024, 3.5, 75.10, '50th percentile'),

('BCS', 2024, 4.0, 78.40, '60th percentile'),

('BCS', 2024, 4.5, 81.30, '70th percentile'),

('BCS', 2024, 5.0, 84.50, '80th percentile'),

('SUPD', 2024, 2.0, 44.30, '20th percentile'),

('SUPD', 2024, 2.5, 50.80, '30th percentile'),

('SUPD', 2024, 3.0, 56.60, '40th percentile'),

('SUPD', 2024, 3.5, 61.90, '50th percentile'),

('SUPD', 2024, 4.0, 66.70, '60th percentile'),

('SUPD', 2024, 4.5, 71.20, '70th percentile'),

('SUPD', 2024, 5.0, 75.80, '80th percentile'),

('HEI', 2024, 2.0, 55.00, '20th percentile'),

('HEI', 2024, 2.5, 62.00, '30th percentile'),

('HEI', 2024, 3.0, 68.00, '40th percentile'),

('HEI', 2024, 3.5, 73.50, '50th percentile'),

('HEI', 2024, 4.0, 78.00, '60th percentile'),

('HEI', 2024, 4.5, 82.50, '70th percentile'),

('HEI', 2024, 5.0, 87.00, '80th percentile');



-- Insert MA Plans

INSERT INTO ma_plans (plan_id, plan_name, parent_organization, state, total_enrollment, current_star_rating, prior_year_star_rating, quality_bonus_pct, monthly_premium_avg) VALUES

('H1234-001', 'HealthFirst Advantage Plus', 'HealthFirst Corp', 'PA', 125000, 3.5, 4.0, 3.5, 85.00),

('H5678-002', 'WellCare Premier', 'WellCare Solutions', 'OH', 85000, 4.0, 4.0, 5.0, 72.50),

('H9012-003', 'Summit Elite Medicare', 'Summit Health Network', 'FL', 45000, 4.5, 4.5, 5.0, 0.00);



-- Insert Plan Performance

INSERT INTO plan_performance (plan_id, measure_id, measurement_year, denominator, numerator, performance_rate, current_star_rating, target_star_rating, gap_to_target) VALUES

('H1234-001', 'GSD', 2024, 18750, 15000, 80.00, 3.0, 4.5, 1828),

('H1234-001', 'KED', 2024, 18750, 14625, 78.00, 3.0, 4.5, 2024),

('H1234-001', 'EED', 2024, 18750, 11250, 60.00, 2.5, 4.0, 2775),

('H1234-001', 'PDC-DR', 2024, 15000, 11850, 79.00, 3.0, 4.5, 1155),

('H1234-001', 'BPD', 2024, 18750, 10875, 58.00, 2.5, 4.0, 1856),

('H1234-001', 'CBP', 2024, 25000, 15000, 60.00, 2.5, 4.5, 3850),

('H1234-001', 'PDC-STA', 2024, 12500, 9500, 76.00, 2.5, 4.0, 1063),

('H1234-001', 'PDC-RASA', 2024, 20000, 15200, 76.00, 3.0, 4.0, 1300),

('H1234-001', 'COL', 2024, 31250, 20625, 66.00, 2.5, 4.0, 3188),

('H1234-001', 'BCS', 2024, 28125, 19969, 71.00, 3.0, 4.0, 2064),

('H1234-001', 'SUPD', 2024, 8750, 4813, 55.00, 2.5, 3.5, 603),

('H1234-001', 'HEI', 2024, 125000, 82500, 66.00, 2.5, 4.0, 15000),

('H5678-002', 'GSD', 2024, 12750, 11133, 87.30, 4.0, 4.5, 321),

('H5678-002', 'KED', 2024, 12750, 10965, 86.00, 4.0, 4.5, 344),

('H5678-002', 'EED', 2024, 12750, 9690, 76.00, 4.0, 4.5, 369),

('H5678-002', 'PDC-DR', 2024, 10200, 8670, 85.00, 4.0, 4.5, 173),

('H5678-002', 'BPD', 2024, 12750, 8798, 69.00, 3.5, 4.5, 318),

('H5678-002', 'CBP', 2024, 17000, 12410, 73.00, 4.0, 4.5, 408),

('H5678-002', 'PDC-STA', 2024, 8500, 7225, 85.00, 4.5, 5.0, 306),

('H5678-002', 'PDC-RASA', 2024, 13600, 11356, 83.50, 4.0, 4.5, 218),

('H5678-002', 'COL', 2024, 21250, 16363, 77.00, 4.0, 4.5, 552),

('H5678-002', 'BCS', 2024, 19125, 15019, 78.50, 4.0, 4.5, 536),

('H5678-002', 'SUPD', 2024, 5950, 3927, 66.00, 3.5, 4.0, 41),

('H5678-002', 'HEI', 2024, 85000, 66300, 78.00, 4.0, 4.5, 3825),

('H9012-003', 'GSD', 2024, 6750, 6075, 90.00, 4.5, 5.0, 169),

('H9012-003', 'KED', 2024, 6750, 5940, 88.00, 4.5, 5.0, 216),

('H9012-003', 'EED', 2024, 6750, 5332, 79.00, 4.5, 5.0, 293),

('H9012-003', 'PDC-DR', 2024, 5400, 4752, 88.00, 4.5, 5.0, 59),

('H9012-003', 'BPD', 2024, 6750, 4860, 72.00, 4.5, 5.0, 216),

('H9012-003', 'CBP', 2024, 9000, 6840, 76.00, 4.5, 5.0, 297),

('H9012-003', 'PDC-STA', 2024, 4500, 3870, 86.00, 4.5, 5.0, 117),

('H9012-003', 'PDC-RASA', 2024, 7200, 6192, 86.00, 4.5, 5.0, 130),

('H9012-003', 'COL', 2024, 11250, 9113, 81.00, 4.5, 5.0, 237),

('H9012-003', 'BCS', 2024, 10125, 8303, 82.00, 4.5, 5.0, 254),

('H9012-003', 'SUPD', 2024, 3150, 2268, 72.00, 4.5, 5.0, 119),

('H9012-003', 'HEI', 2024, 45000, 37800, 84.00, 4.5, 5.0, 1350);



-- Revenue calculation function

CREATE OR REPLACE FUNCTION calculate_revenue_impact(

    p_plan_id VARCHAR(20),

    p_measure_id VARCHAR(20),

    p_measurement_year INT

)

RETURNS TABLE (

    plan_id VARCHAR(20),

    plan_name VARCHAR(200),

    measure_id VARCHAR(20),

    measure_name VARCHAR(200),

    current_performance DECIMAL(5,2),

    current_star DECIMAL(2,1),

    target_star DECIMAL(2,1),

    star_gap DECIMAL(2,1),

    members_to_close INT,

    revenue_per_star_point DECIMAL(10,2),

    total_revenue_at_risk DECIMAL(12,2),

    weighted_impact DECIMAL(12,2)

) AS $$

BEGIN

    RETURN QUERY

    SELECT 

        pp.plan_id,

        mp.plan_name,

        pp.measure_id,

        hm.measure_name,

        pp.performance_rate,

        pp.current_star_rating,

        pp.target_star_rating,

        (pp.target_star_rating - pp.current_star_rating) AS star_gap,

        pp.gap_to_target,

        hm.revenue_per_point,

        (pp.target_star_rating - pp.current_star_rating) * hm.revenue_per_point AS revenue_at_risk,

        (pp.target_star_rating - pp.current_star_rating) * hm.revenue_per_point * hm.star_weight AS weighted_revenue_impact

    FROM plan_performance pp

    JOIN ma_plans mp ON pp.plan_id = mp.plan_id

    JOIN hedis_measures hm ON pp.measure_id = hm.measure_id

    WHERE pp.plan_id = p_plan_id

      AND pp.measure_id = p_measure_id

      AND pp.measurement_year = p_measurement_year;

END;

$$ LANGUAGE plpgsql;



-- Revenue at risk view

CREATE OR REPLACE VIEW vw_revenue_at_risk AS

SELECT 

    pp.plan_id,

    mp.plan_name,

    mp.parent_organization,

    mp.state,

    mp.total_enrollment,

    mp.current_star_rating AS plan_overall_stars,

    pp.measure_id,

    hm.measure_name,

    hm.domain,

    hm.star_weight,

    pp.denominator AS eligible_members,

    pp.numerator AS compliant_members,

    pp.performance_rate AS current_rate_pct,

    pp.current_star_rating AS measure_current_stars,

    pp.target_star_rating AS measure_target_stars,

    (pp.target_star_rating - pp.current_star_rating) AS star_rating_gap,

    pp.gap_to_target AS members_needed,

    (SELECT threshold_pct 

     FROM star_thresholds st 

     WHERE st.measure_id = pp.measure_id 

       AND st.measurement_year = pp.measurement_year

       AND st.star_rating = pp.target_star_rating

     LIMIT 1) AS target_threshold_pct,

    hm.revenue_per_point AS revenue_per_star_point,

    (pp.target_star_rating - pp.current_star_rating) * hm.revenue_per_point AS revenue_at_risk,

    (pp.target_star_rating - pp.current_star_rating) * hm.revenue_per_point * hm.star_weight AS weighted_revenue_impact,

    CASE 

        WHEN pp.gap_to_target > 0 THEN 

            ROUND(((pp.target_star_rating - pp.current_star_rating) * hm.revenue_per_point) / pp.gap_to_target, 2)

        ELSE 0 

    END AS revenue_per_member_closed,

    pp.measurement_year

FROM plan_performance pp

JOIN ma_plans mp ON pp.plan_id = mp.plan_id

JOIN hedis_measures hm ON pp.measure_id = hm.measure_id

WHERE mp.is_active = TRUE

  AND pp.current_star_rating < pp.target_star_rating;



-- Quick validation query

SELECT 'Foundation Script Complete' AS status,

       COUNT(*) AS measure_count 

FROM hedis_measures;



SELECT 'Revenue at Risk Summary' AS report;

SELECT 

    plan_id,

    plan_name,

    COUNT(DISTINCT measure_id) AS measures_at_risk,

    SUM(members_needed) AS total_gaps,

    ROUND(SUM(revenue_at_risk), 0) AS total_revenue_at_risk

FROM vw_revenue_at_risk

WHERE measurement_year = 2024

GROUP BY plan_id, plan_name

ORDER BY total_revenue_at_risk DESC;


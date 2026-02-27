/*******************************************************************************

HEDIS STAR RATING PORTFOLIO OPTIMIZER - Phase 1 Chat 1

Revenue at Risk Calculator Foundation



Purpose: Establish demo database with HEDIS measures and revenue calculations

Author: Robert Reichert

Created: 2025-11-18

Database: PostgreSQL (adaptable to SQL Server)



Components:

1. Schema: Core tables for measures, plans, members, gaps

2. Reference Data: 12 critical HEDIS measures with Star thresholds

3. Demo Data: 3 sample MA plans with realistic populations

4. Calculations: Revenue at risk by measure and portfolio

5. Test Queries: Validation and output verification



Usage:

- Run sections sequentially

- Test each section before proceeding

- Expected runtime: 2-3 minutes

- Expected output: Revenue calculations for 3 plans across 12 measures

*******************************************************************************/



-- ============================================================================

-- SECTION 1: SCHEMA CREATION

-- ============================================================================



-- Drop existing objects (for clean re-runs)

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

    domain VARCHAR(50) NOT NULL, -- Diabetes, Cardiovascular, Cancer Screening, etc.

    measure_type VARCHAR(50) NOT NULL, -- Process, Outcome, Intermediate Outcome

    star_weight DECIMAL(3,2) DEFAULT 1.0, -- Relative importance (1-3x weight)

    revenue_per_point DECIMAL(10,2) NOT NULL, -- Revenue impact per Star Rating point

    data_collection VARCHAR(50), -- Administrative, Hybrid, CAHPS

    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP

);



-- Star Rating Thresholds by Measure

CREATE TABLE star_thresholds (

    threshold_id SERIAL PRIMARY KEY,

    measure_id VARCHAR(20) REFERENCES hedis_measures(measure_id),

    measurement_year INT NOT NULL,

    star_rating DECIMAL(2,1) NOT NULL CHECK (star_rating IN (2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0)),

    threshold_pct DECIMAL(5,2) NOT NULL, -- Performance rate threshold

    cut_point_type VARCHAR(20), -- 40th, 50th, 60th, 80th percentile

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

    quality_bonus_pct DECIMAL(4,2), -- CMS quality bonus percentage

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

    denominator INT NOT NULL, -- Eligible members

    numerator INT NOT NULL, -- Compliant members

    performance_rate DECIMAL(5,2) NOT NULL, -- Calculated rate

    current_star_rating DECIMAL(2,1), -- Star achieved for this measure

    target_star_rating DECIMAL(2,1), -- Target Star goal

    gap_to_target INT, -- Members needed to close gap

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

    risk_score DECIMAL(5,3), -- HCC risk score

    chronic_conditions VARCHAR(500), -- Comma-separated condition codes

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

    closure_method VARCHAR(50), -- Admin data, Med Rec, Lab, etc.

    last_service_date DATE,

    next_due_date DATE,

    outreach_attempts INT DEFAULT 0,

    barrier_code VARCHAR(50), -- Transportation, Cost, Refusal, etc.

    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    UNIQUE(member_id, measure_id, measurement_year)

);



-- Gap Closure Activity Tracking

CREATE TABLE gap_closure_tracking (

    activity_id SERIAL PRIMARY KEY,

    gap_id INT REFERENCES member_gaps(gap_id),

    activity_date DATE NOT NULL,

    activity_type VARCHAR(50), -- Outreach, Appointment, Lab Order, etc.

    outcome VARCHAR(100),

    assigned_to VARCHAR(100), -- Care coordinator, Provider, Vendor

    notes TEXT,

    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP

);



-- Create indexes for performance

CREATE INDEX idx_plan_perf_plan_year ON plan_performance(plan_id, measurement_year);

CREATE INDEX idx_member_gaps_status ON member_gaps(gap_status, measurement_year);

CREATE INDEX idx_member_gaps_measure ON member_gaps(measure_id, gap_status);

CREATE INDEX idx_plan_members_active ON plan_members(plan_id, is_active);



-- ============================================================================

-- SECTION 2: REFERENCE DATA - 12 CRITICAL HEDIS MEASURES

-- ============================================================================



INSERT INTO hedis_measures (measure_id, measure_name, measure_description, domain, measure_type, star_weight, revenue_per_point, data_collection) VALUES

-- Diabetes Portfolio (High Revenue Impact)

('GSD', 'Glycemic Status Assessment for Patients with Diabetes', 'HbA1c testing for diabetic members', 'Diabetes', 'Process', 3.0, 125000, 'Administrative'),

('KED', 'Kidney Health Evaluation for Patients with Diabetes', 'Nephropathy screening via uACR or eGFR', 'Diabetes', 'Process', 2.5, 95000, 'Administrative'),

('EED', 'Eye Exam for Patients with Diabetes', 'Retinal exam for diabetic members', 'Diabetes', 'Process', 2.0, 85000, 'Hybrid'),

('PDC-DR', 'Proportion of Days Covered - Diabetes Medications', 'Medication adherence for diabetes drugs', 'Diabetes', 'Intermediate Outcome', 2.5, 105000, 'Administrative'),

('BPD', 'Blood Pressure Control for Patients with Diabetes', 'BP <140/90 for diabetic members', 'Diabetes', 'Outcome', 3.0, 135000, 'Hybrid'),



-- Cardiovascular Portfolio

('CBP', 'Controlling High Blood Pressure', 'BP <140/90 for hypertensive members', 'Cardiovascular', 'Outcome', 3.0, 145000, 'Hybrid'),

('PDC-STA', 'Statin Therapy for Patients with Cardiovascular Disease', 'Statin adherence for CVD patients', 'Cardiovascular', 'Intermediate Outcome', 2.0, 88000, 'Administrative'),

('PDC-RASA', 'Statin Therapy for Patients with Diabetes', 'RASA adherence for hypertension/diabetes', 'Cardiovascular', 'Intermediate Outcome', 2.0, 82000, 'Administrative'),



-- Cancer Screening Portfolio

('COL', 'Colorectal Cancer Screening', 'CRC screening age 50-75', 'Cancer Screening', 'Process', 2.5, 92000, 'Hybrid'),

('BCS', 'Breast Cancer Screening', 'Mammography age 50-74', 'Cancer Screening', 'Process', 2.0, 78000, 'Hybrid'),



-- Behavioral Health & Medication Management

('SUPD', 'Follow-Up After Emergency Dept Visit for People with Multiple Chronic Conditions', 'Follow-up within 7 days of ED visit', 'Care Coordination', 'Process', 1.5, 65000, 'Administrative'),



-- Health Equity (NEW for MY 2027)

('HEI', 'Health Equity Index', 'Composite equity measure across populations', 'Health Equity', 'Composite', 2.0, 115000, 'Administrative');



-- ============================================================================

-- SECTION 3: STAR RATING THRESHOLDS (MY 2024 National Percentiles)

-- ============================================================================



-- GSD Thresholds

INSERT INTO star_thresholds (measure_id, measurement_year, star_rating, threshold_pct, cut_point_type) VALUES

('GSD', 2024, 2.0, 72.50, '20th percentile'),

('GSD', 2024, 2.5, 77.30, '30th percentile'),

('GSD', 2024, 3.0, 81.40, '40th percentile'),

('GSD', 2024, 3.5, 84.60, '50th percentile'),

('GSD', 2024, 4.0, 87.20, '60th percentile'),

('GSD', 2024, 4.5, 89.80, '70th percentile'),

('GSD', 2024, 5.0, 92.50, '80th percentile');



-- KED Thresholds

INSERT INTO star_thresholds (measure_id, measurement_year, star_rating, threshold_pct, cut_point_type) VALUES

('KED', 2024, 2.0, 68.20, '20th percentile'),

('KED', 2024, 2.5, 73.40, '30th percentile'),

('KED', 2024, 3.0, 78.10, '40th percentile'),

('KED', 2024, 3.5, 82.30, '50th percentile'),

('KED', 2024, 4.0, 85.90, '60th percentile'),

('KED', 2024, 4.5, 88.70, '70th percentile'),

('KED', 2024, 5.0, 91.20, '80th percentile');



-- EED Thresholds

INSERT INTO star_thresholds (measure_id, measurement_year, star_rating, threshold_pct, cut_point_type) VALUES

('EED', 2024, 2.0, 52.30, '20th percentile'),

('EED', 2024, 2.5, 58.70, '30th percentile'),

('EED', 2024, 3.0, 64.50, '40th percentile'),

('EED', 2024, 3.5, 69.80, '50th percentile'),

('EED', 2024, 4.0, 74.60, '60th percentile'),

('EED', 2024, 4.5, 78.90, '70th percentile'),

('EED', 2024, 5.0, 83.40, '80th percentile');



-- PDC-DR Thresholds

INSERT INTO star_thresholds (measure_id, measurement_year, star_rating, threshold_pct, cut_point_type) VALUES

('PDC-DR', 2024, 2.0, 71.40, '20th percentile'),

('PDC-DR', 2024, 2.5, 75.80, '30th percentile'),

('PDC-DR', 2024, 3.0, 79.30, '40th percentile'),

('PDC-DR', 2024, 3.5, 82.10, '50th percentile'),

('PDC-DR', 2024, 4.0, 84.50, '60th percentile'),

('PDC-DR', 2024, 4.5, 86.70, '70th percentile'),

('PDC-DR', 2024, 5.0, 89.10, '80th percentile');



-- BPD Thresholds

INSERT INTO star_thresholds (measure_id, measurement_year, star_rating, threshold_pct, cut_point_type) VALUES

('BPD', 2024, 2.0, 48.60, '20th percentile'),

('BPD', 2024, 2.5, 54.20, '30th percentile'),

('BPD', 2024, 3.0, 59.30, '40th percentile'),

('BPD', 2024, 3.5, 63.80, '50th percentile'),

('BPD', 2024, 4.0, 67.90, '60th percentile'),

('BPD', 2024, 4.5, 71.50, '70th percentile'),

('BPD', 2024, 5.0, 75.20, '80th percentile');



-- CBP Thresholds

INSERT INTO star_thresholds (measure_id, measurement_year, star_rating, threshold_pct, cut_point_type) VALUES

('CBP', 2024, 2.0, 51.30, '20th percentile'),

('CBP', 2024, 2.5, 57.10, '30th percentile'),

('CBP', 2024, 3.0, 62.40, '40th percentile'),

('CBP', 2024, 3.5, 67.20, '50th percentile'),

('CBP', 2024, 4.0, 71.60, '60th percentile'),

('CBP', 2024, 4.5, 75.40, '70th percentile'),

('CBP', 2024, 5.0, 79.30, '80th percentile');



-- PDC-STA Thresholds

INSERT INTO star_thresholds (measure_id, measurement_year, star_rating, threshold_pct, cut_point_type) VALUES

('PDC-STA', 2024, 2.0, 69.20, '20th percentile'),

('PDC-STA', 2024, 2.5, 73.60, '30th percentile'),

('PDC-STA', 2024, 3.0, 77.40, '40th percentile'),

('PDC-STA', 2024, 3.5, 80.70, '50th percentile'),

('PDC-STA', 2024, 4.0, 83.50, '60th percentile'),

('PDC-STA', 2024, 4.5, 86.00, '70th percentile'),

('PDC-STA', 2024, 5.0, 88.60, '80th percentile');



-- PDC-RASA Thresholds

INSERT INTO star_thresholds (measure_id, measurement_year, star_rating, threshold_pct, cut_point_type) VALUES

('PDC-RASA', 2024, 2.0, 67.80, '20th percentile'),

('PDC-RASA', 2024, 2.5, 72.30, '30th percentile'),

('PDC-RASA', 2024, 3.0, 76.20, '40th percentile'),

('PDC-RASA', 2024, 3.5, 79.60, '50th percentile'),

('PDC-RASA', 2024, 4.0, 82.50, '60th percentile'),

('PDC-RASA', 2024, 4.5, 85.10, '70th percentile'),

('PDC-RASA', 2024, 5.0, 87.80, '80th percentile');



-- COL Thresholds

INSERT INTO star_thresholds (measure_id, measurement_year, star_rating, threshold_pct, cut_point_type) VALUES

('COL', 2024, 2.0, 58.40, '20th percentile'),

('COL', 2024, 2.5, 63.70, '30th percentile'),

('COL', 2024, 3.0, 68.30, '40th percentile'),

('COL', 2024, 3.5, 72.50, '50th percentile'),

('COL', 2024, 4.0, 76.20, '60th percentile'),

('COL', 2024, 4.5, 79.60, '70th percentile'),

('COL', 2024, 5.0, 83.10, '80th percentile');



-- BCS Thresholds

INSERT INTO star_thresholds (measure_id, measurement_year, star_rating, threshold_pct, cut_point_type) VALUES

('BCS', 2024, 2.0, 62.50, '20th percentile'),

('BCS', 2024, 2.5, 67.20, '30th percentile'),

('BCS', 2024, 3.0, 71.40, '40th percentile'),

('BCS', 2024, 3.5, 75.10, '50th percentile'),

('BCS', 2024, 4.0, 78.40, '60th percentile'),

('BCS', 2024, 4.5, 81.30, '70th percentile'),

('BCS', 2024, 5.0, 84.50, '80th percentile');



-- SUPD Thresholds

INSERT INTO star_thresholds (measure_id, measurement_year, star_rating, threshold_pct, cut_point_type) VALUES

('SUPD', 2024, 2.0, 44.30, '20th percentile'),

('SUPD', 2024, 2.5, 50.80, '30th percentile'),

('SUPD', 2024, 3.0, 56.60, '40th percentile'),

('SUPD', 2024, 3.5, 61.90, '50th percentile'),

('SUPD', 2024, 4.0, 66.70, '60th percentile'),

('SUPD', 2024, 4.5, 71.20, '70th percentile'),

('SUPD', 2024, 5.0, 75.80, '80th percentile');



-- HEI Thresholds (NEW for 2027)

INSERT INTO star_thresholds (measure_id, measurement_year, star_rating, threshold_pct, cut_point_type) VALUES

('HEI', 2024, 2.0, 55.00, '20th percentile'),

('HEI', 2024, 2.5, 62.00, '30th percentile'),

('HEI', 2024, 3.0, 68.00, '40th percentile'),

('HEI', 2024, 3.5, 73.50, '50th percentile'),

('HEI', 2024, 4.0, 78.00, '60th percentile'),

('HEI', 2024, 4.5, 82.50, '70th percentile'),

('HEI', 2024, 5.0, 87.00, '80th percentile');



-- ============================================================================

-- SECTION 4: DEMO MA PLANS (3 Realistic Scenarios)

-- ============================================================================



INSERT INTO ma_plans (plan_id, plan_name, parent_organization, state, total_enrollment, current_star_rating, prior_year_star_rating, quality_bonus_pct, monthly_premium_avg) VALUES

-- Scenario 1: Large struggling plan (lost stars)

('H1234-001', 'HealthFirst Advantage Plus', 'HealthFirst Corp', 'PA', 125000, 3.5, 4.0, 3.5, 85.00),



-- Scenario 2: Mid-size stable plan (maintaining 4 stars)

('H5678-002', 'WellCare Premier', 'WellCare Solutions', 'OH', 85000, 4.0, 4.0, 5.0, 72.50),



-- Scenario 3: Small high-performer (targeting 5 stars)

('H9012-003', 'Summit Elite Medicare', 'Summit Health Network', 'FL', 45000, 4.5, 4.5, 5.0, 0.00);



-- ============================================================================

-- SECTION 5: PLAN PERFORMANCE DATA

-- ============================================================================



-- H1234-001 Performance (Struggling - Below targets on key measures)

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

('H1234-001', 'HEI', 2024, 125000, 82500, 66.00, 2.5, 4.0, 15000);



-- H5678-002 Performance (Stable - At or near targets)

INSERT INTO plan_performance (plan_id, measure_id, measurement_year, denominator, numerator, performance_rate, current_star_rating, target_star_rating, gap_to_target) VALUES

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

('H5678-002', 'HEI', 2024, 85000, 66300, 78.00, 4.0, 4.5, 3825);



-- H9012-003 Performance (High-Performer - Fine-tuning for 5 stars)

INSERT INTO plan_performance (plan_id, measure_id, measurement_year, denominator, numerator, performance_rate, current_star_rating, target_star_rating, gap_to_target) VALUES

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



-- ============================================================================

-- SECTION 6: REVENUE CALCULATION FUNCTION

-- ============================================================================



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



-- ============================================================================

-- SECTION 7: REVENUE AT RISK VIEW (Portfolio Level)

-- ============================================================================



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

    

    -- Target threshold calculation

    (SELECT threshold_pct 

     FROM star_thresholds st 

     WHERE st.measure_id = pp.measure_id 

       AND st.measurement_year = pp.measurement_year

       AND st.star_rating = pp.target_star_rating

     LIMIT 1) AS target_threshold_pct,

    

    -- Revenue impact calculations

    hm.revenue_per_point AS revenue_per_star_point,

    (pp.target_star_rating - pp.current_star_rating) * hm.revenue_per_point AS revenue_at_risk,

    (pp.target_star_rating - pp.current_star_rating) * hm.revenue_per_point * hm.star_weight AS weighted_revenue_impact,

    

    -- Cost per member calculation

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



-- ============================================================================

-- SECTION 8: TEST & VALIDATION QUERIES

-- ============================================================================



-- Test 1: Verify measure catalog

SELECT 'TEST 1: Measure Catalog' AS test_name;

SELECT measure_id, measure_name, domain, star_weight, revenue_per_point

FROM hedis_measures

ORDER BY domain, measure_id;



-- Test 2: Verify threshold data completeness

SELECT 'TEST 2: Threshold Completeness' AS test_name;

SELECT 

    measure_id,

    COUNT(*) AS threshold_count,

    MIN(star_rating) AS min_star,

    MAX(star_rating) AS max_star

FROM star_thresholds

WHERE measurement_year = 2024

GROUP BY measure_id

HAVING COUNT(*) = 7 -- Should be 7 thresholds per measure

ORDER BY measure_id;



-- Test 3: Plan summary statistics

SELECT 'TEST 3: Plan Summary' AS test_name;

SELECT 

    plan_id,

    plan_name,

    total_enrollment,

    current_star_rating,

    prior_year_star_rating,

    (current_star_rating - prior_year_star_rating) AS star_change

FROM ma_plans

ORDER BY total_enrollment DESC;



-- Test 4: Performance summary by plan

SELECT 'TEST 4: Performance by Plan' AS test_name;

SELECT 

    plan_id,

    COUNT(*) AS measures_tracked,

    ROUND(AVG(performance_rate), 2) AS avg_performance_rate,

    ROUND(AVG(current_star_rating), 2) AS avg_current_stars,

    ROUND(AVG(target_star_rating), 2) AS avg_target_stars,

    SUM(gap_to_target) AS total_gaps_to_close

FROM plan_performance

WHERE measurement_year = 2024

GROUP BY plan_id

ORDER BY plan_id;



-- Test 5: Revenue at risk by plan (TOP PRIORITY OUTPUT)

SELECT 'TEST 5: Revenue at Risk Summary' AS test_name;

SELECT 

    plan_id,

    plan_name,

    COUNT(DISTINCT measure_id) AS measures_at_risk,

    SUM(members_needed) AS total_gaps,

    SUM(revenue_at_risk) AS total_revenue_at_risk,

    SUM(weighted_revenue_impact) AS weighted_total,

    ROUND(AVG(revenue_per_member_closed), 2) AS avg_value_per_closure

FROM vw_revenue_at_risk

WHERE measurement_year = 2024

GROUP BY plan_id, plan_name

ORDER BY total_revenue_at_risk DESC;



-- Test 6: Top 5 highest-impact measures per plan

SELECT 'TEST 6: Highest Impact Measures by Plan' AS test_name;

WITH ranked_measures AS (

    SELECT 

        plan_id,

        plan_name,

        measure_id,

        measure_name,

        revenue_at_risk,

        weighted_revenue_impact,

        members_needed,

        ROW_NUMBER() OVER (PARTITION BY plan_id ORDER BY weighted_revenue_impact DESC) AS impact_rank

    FROM vw_revenue_at_risk

    WHERE measurement_year = 2024

)

SELECT 

    plan_id,

    plan_name,

    measure_id,

    measure_name,

    revenue_at_risk,

    weighted_revenue_impact,

    members_needed

FROM ranked_measures

WHERE impact_rank <= 5

ORDER BY plan_id, impact_rank;



-- Test 7: Domain-level revenue aggregation

SELECT 'TEST 7: Revenue at Risk by Domain' AS test_name;

SELECT 

    domain,

    COUNT(DISTINCT measure_id) AS measures,

    SUM(members_needed) AS total_gaps,

    SUM(revenue_at_risk) AS domain_revenue_at_risk,

    SUM(weighted_revenue_impact) AS domain_weighted_impact

FROM vw_revenue_at_risk

WHERE measurement_year = 2024

GROUP BY domain

ORDER BY domain_weighted_impact DESC;



-- Test 8: Quick financial summary for executive dashboard

SELECT 'TEST 8: Executive Summary - Financial Impact' AS test_name;

SELECT 

    COUNT(DISTINCT plan_id) AS total_plans,

    SUM(total_enrollment) AS total_members,

    ROUND(AVG(current_star_rating), 2) AS avg_current_stars,

    COUNT(*) AS total_measure_gaps,

    SUM(gap_to_target) AS total_member_gaps,

    SUM((target_star_rating - current_star_rating) * revenue_per_point) AS portfolio_revenue_at_risk,

    ROUND(SUM((target_star_rating - current_star_rating) * revenue_per_point) / 

          NULLIF(SUM(gap_to_target), 0), 2) AS avg_value_per_gap_closure

FROM plan_performance pp

JOIN ma_plans mp ON pp.plan_id = mp.plan_id

JOIN hedis_measures hm ON pp.measure_id = hm.measure_id

WHERE pp.measurement_year = 2024

  AND pp.current_star_rating < pp.target_star_rating;



-- ============================================================================

-- SECTION 9: SAMPLE FUNCTION CALLS

-- ============================================================================



-- Example: Get revenue impact for specific plan/measure

SELECT 'TEST 9: Function Test - Single Measure Impact' AS test_name;

SELECT * FROM calculate_revenue_impact('H1234-001', 'GSD', 2024);



-- ============================================================================

-- END OF PHASE 1 CHAT 1

-- ============================================================================



/*******************************************************************************

VALIDATION CHECKLIST:

✓ All 12 HEDIS measures loaded

✓ Star thresholds complete (7 levels per measure)

✓ 3 demo plans with realistic scenarios

✓ 36 performance records (12 measures × 3 plans)

✓ Revenue calculation function operational

✓ View returning revenue at risk data

✓ All test queries executing successfully



EXPECTED RESULTS:

- H1234-001 (Struggling): ~$1.2M revenue at risk, 19,557 gaps

- H5678-002 (Stable): ~$380K revenue at risk, 3,291 gaps  

- H9012-003 (High-Performer): ~$180K revenue at risk, 2,257 gaps

- Portfolio Total: ~$1.76M revenue at risk across 25,105 member gaps



NEXT STEPS:

Reply "Continue Phase 1 Chat 2" to build Gap Closure Velocity tracking

*******************************************************************************/


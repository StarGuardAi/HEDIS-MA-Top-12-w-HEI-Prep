/*******************************************************************************

HEDIS STAR RATING PORTFOLIO OPTIMIZER - Phase 2 Chat 2

Provider Network Performance & Attribution Analytics



Purpose: Track provider network performance, attribution, and referral patterns

Author: Robert Reichert

Created: 2025-11-18

Database: PostgreSQL

Prerequisites: Phase 1 (Chats 1-4) and Phase 2 Chat 1 must be completed



Components:

1. Provider Directory & Roster Management

2. Member-Provider Attribution Logic

3. Provider Performance Metrics by HEDIS Measure

4. Referral Pattern Analysis

5. Network Adequacy Scoring

6. Provider Engagement & Collaboration Metrics

7. Quality Score Rankings



Usage:

- Builds on Phase 1 member/gap data and Phase 2 engagement data

- Run after Phase 2 Chat 1 complete

- Expected runtime: 4-5 minutes

- Expected output: 500+ providers, attribution for 10K members, performance analytics

*******************************************************************************/



-- ============================================================================

-- SECTION 1: PROVIDER INFRASTRUCTURE

-- ============================================================================



-- Provider Directory

DROP TABLE IF EXISTS provider_directory CASCADE;



CREATE TABLE provider_directory (

    provider_id VARCHAR(20) PRIMARY KEY,

    npi VARCHAR(10) UNIQUE NOT NULL,

    

    -- Provider details

    provider_type VARCHAR(50) NOT NULL, -- PCP, Specialist, Facility

    specialty VARCHAR(100),

    sub_specialty VARCHAR(100),

    

    -- Name information

    first_name VARCHAR(100),

    last_name VARCHAR(100),

    practice_name VARCHAR(200),

    

    -- Network status

    network_status VARCHAR(20) DEFAULT 'Active', -- Active, Inactive, Termed

    tier_level VARCHAR(20), -- Tier 1, Tier 2, Out of Network

    accepting_new_patients BOOLEAN DEFAULT TRUE,

    

    -- Location

    practice_address VARCHAR(200),

    practice_city VARCHAR(100),

    practice_state CHAR(2),

    practice_zip VARCHAR(10),

    

    -- Contact

    phone VARCHAR(20),

    fax VARCHAR(20),

    email VARCHAR(100),

    

    -- Quality indicators

    board_certified BOOLEAN DEFAULT TRUE,

    years_in_practice INT,

    patient_satisfaction_score DECIMAL(3,1), -- 1-5 scale

    

    -- Network participation

    contracted_plans TEXT, -- Comma-separated plan IDs

    effective_date DATE,

    term_date DATE,

    

    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    updated_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP

);



-- Provider Performance Metrics

DROP TABLE IF EXISTS provider_performance CASCADE;



CREATE TABLE provider_performance (

    performance_id SERIAL PRIMARY KEY,

    provider_id VARCHAR(20) REFERENCES provider_directory(provider_id),

    measure_id VARCHAR(20) REFERENCES hedis_measures(measure_id),

    measurement_year INT NOT NULL,

    

    -- Volume metrics

    attributed_members INT NOT NULL DEFAULT 0,

    eligible_for_measure INT NOT NULL DEFAULT 0,

    numerator_compliant INT NOT NULL DEFAULT 0,

    

    -- Performance rate

    performance_rate DECIMAL(5,2),

    

    -- Benchmarking

    network_avg_rate DECIMAL(5,2),

    percentile_rank INT, -- 1-100 percentile

    

    -- Star rating alignment

    star_rating_achieved DECIMAL(2,1),

    

    -- Gap metrics

    open_gaps INT DEFAULT 0,

    closed_gaps_ytd INT DEFAULT 0,

    

    -- Quality flags

    top_performer BOOLEAN DEFAULT FALSE,

    needs_improvement BOOLEAN DEFAULT FALSE,

    outlier_low BOOLEAN DEFAULT FALSE,

    outlier_high BOOLEAN DEFAULT FALSE,

    

    last_updated DATE DEFAULT CURRENT_DATE,

    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    

    UNIQUE(provider_id, measure_id, measurement_year)

);



-- Member-Provider Attribution

DROP TABLE IF EXISTS member_provider_attribution CASCADE;



CREATE TABLE member_provider_attribution (

    attribution_id SERIAL PRIMARY KEY,

    member_id VARCHAR(50) REFERENCES plan_members(member_id),

    provider_id VARCHAR(20) REFERENCES provider_directory(provider_id),

    

    -- Attribution details

    attribution_type VARCHAR(50) NOT NULL, -- PCP, Specialist, Facility

    attribution_method VARCHAR(50), -- Claims-based, Roster, Member Selection

    attribution_start_date DATE NOT NULL,

    attribution_end_date DATE,

    is_current BOOLEAN DEFAULT TRUE,

    

    -- Visit history

    visit_count_ytd INT DEFAULT 0,

    last_visit_date DATE,

    

    -- Quality measures eligible

    measures_attributed TEXT, -- Comma-separated measure IDs

    

    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP

);



-- Provider Referral Network

DROP TABLE IF EXISTS provider_referrals CASCADE;



CREATE TABLE provider_referrals (

    referral_id SERIAL PRIMARY KEY,

    referring_provider_id VARCHAR(20) REFERENCES provider_directory(provider_id),

    referred_to_provider_id VARCHAR(20) REFERENCES provider_directory(provider_id),

    member_id VARCHAR(50) REFERENCES plan_members(member_id),

    

    -- Referral details

    referral_date DATE NOT NULL,

    referral_reason TEXT,

    referral_type VARCHAR(50), -- Routine, Urgent, Consultation

    

    -- HEDIS measure related

    related_measure_id VARCHAR(20) REFERENCES hedis_measures(measure_id),

    gap_closure_referral BOOLEAN DEFAULT FALSE,

    

    -- Outcome tracking

    appointment_completed BOOLEAN,

    appointment_date DATE,

    days_to_appointment INT,

    

    resulted_in_gap_closure BOOLEAN DEFAULT FALSE,

    

    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP

);



-- Provider Collaboration Scores

DROP TABLE IF EXISTS provider_collaboration_scores CASCADE;



CREATE TABLE provider_collaboration_scores (

    score_id SERIAL PRIMARY KEY,

    provider_id VARCHAR(20) REFERENCES provider_directory(provider_id),

    score_date DATE NOT NULL DEFAULT CURRENT_DATE,

    

    -- Component scores (0-100 scale)

    responsiveness_score DECIMAL(5,2), -- Speed of gap closure

    documentation_score DECIMAL(5,2), -- Quality of documentation

    referral_score DECIMAL(5,2), -- Appropriate referral patterns

    engagement_score DECIMAL(5,2), -- Participation in quality programs

    

    -- Composite collaboration score

    overall_collaboration_score DECIMAL(5,2),

    collaboration_tier VARCHAR(20), -- Excellent, Good, Fair, Poor

    

    -- Performance indicators

    avg_days_to_close_gap DECIMAL(6,2),

    gap_closure_rate_pct DECIMAL(5,2),

    med_rec_submission_rate_pct DECIMAL(5,2),

    

    -- Engagement metrics

    quality_program_participant BOOLEAN DEFAULT FALSE,

    accepts_quality_reports BOOLEAN DEFAULT TRUE,

    responsive_to_outreach BOOLEAN DEFAULT TRUE,

    

    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP

);



-- Network Adequacy Tracking

DROP TABLE IF EXISTS network_adequacy_metrics CASCADE;



CREATE TABLE network_adequacy_metrics (

    adequacy_id SERIAL PRIMARY KEY,

    plan_id VARCHAR(20) REFERENCES ma_plans(plan_id),

    specialty VARCHAR(100) NOT NULL,

    geographic_area VARCHAR(10), -- Zip code or county

    measurement_date DATE NOT NULL DEFAULT CURRENT_DATE,

    

    -- Supply metrics

    total_providers INT NOT NULL,

    accepting_new_patients INT NOT NULL,

    

    -- Demand metrics

    total_members INT NOT NULL,

    member_to_provider_ratio DECIMAL(8,2),

    

    -- Access metrics

    avg_distance_to_provider_miles DECIMAL(6,2),

    pct_members_within_15_miles DECIMAL(5,2),

    

    -- Adequacy assessment

    meets_cms_standards BOOLEAN,

    adequacy_rating VARCHAR(20), -- Excellent, Adequate, Insufficient, Critical

    

    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP

);



-- ============================================================================

-- SECTION 2: GENERATE PROVIDER DEMO DATA

-- ============================================================================



-- Generate Provider Directory (500+ providers across specialties)

DO $$

DECLARE

    v_provider_count INT := 0;

    v_provider_id VARCHAR(20);

    v_npi VARCHAR(10);

    v_specialty VARCHAR(100);

    v_provider_type VARCHAR(50);

    v_zip_codes VARCHAR(10)[];

    v_selected_zip VARCHAR(10);

    v_counter INT;

    

    -- Specialty distribution for Medicare Advantage

    v_specialties TEXT[] := ARRAY[

        'Internal Medicine', 'Family Medicine', 'Cardiology', 

        'Endocrinology', 'Nephrology', 'Ophthalmology',

        'Podiatry', 'Oncology', 'Gastroenterology',

        'Orthopedics', 'Pulmonology', 'Neurology',

        'Urology', 'General Surgery', 'Dermatology',

        'Rheumatology', 'Psychiatry', 'Physical Medicine'

    ];

BEGIN

    RAISE NOTICE 'Generating provider directory...';

    

    -- Load zip codes for distribution

    SELECT ARRAY_AGG(zip_code) INTO v_zip_codes FROM zip_code_reference;

    

    -- Generate Primary Care Providers (250 PCPs)

    FOR v_counter IN 1..250 LOOP

        v_provider_id := 'PCP' || LPAD(v_counter::TEXT, 6, '0');

        v_npi := LPAD((1000000000 + v_counter)::TEXT, 10, '0');

        

        v_specialty := CASE 

            WHEN RANDOM() < 0.60 THEN 'Internal Medicine'

            ELSE 'Family Medicine'

        END;

        

        v_selected_zip := v_zip_codes[1 + FLOOR(RANDOM() * ARRAY_LENGTH(v_zip_codes, 1))::INT];

        

        INSERT INTO provider_directory (

            provider_id, npi, provider_type, specialty,

            first_name, last_name, practice_name,

            network_status, tier_level, accepting_new_patients,

            practice_zip, practice_state,

            board_certified, years_in_practice, patient_satisfaction_score,

            contracted_plans

        ) VALUES (

            v_provider_id,

            v_npi,

            'PCP',

            v_specialty,

            'Dr. ' || CHR(65 + FLOOR(RANDOM() * 26)::INT),

            'Provider-' || v_counter,

            v_specialty || ' Associates',

            'Active',

            CASE WHEN RANDOM() < 0.75 THEN 'Tier 1' ELSE 'Tier 2' END,

            RANDOM() < 0.85,

            v_selected_zip,

            'PA',

            RANDOM() < 0.92,

            10 + FLOOR(RANDOM() * 25)::INT,

            3.5 + (RANDOM() * 1.5),

            'H1234-001,H5678-002,H9012-003'

        );

        

        v_provider_count := v_provider_count + 1;

    END LOOP;

    

    RAISE NOTICE '  Generated % PCPs', v_provider_count;

    

    -- Generate Specialists (250 specialists across various specialties)

    FOR v_counter IN 1..250 LOOP

        v_provider_id := 'SPC' || LPAD(v_counter::TEXT, 6, '0');

        v_npi := LPAD((2000000000 + v_counter)::TEXT, 10, '0');

        

        v_specialty := v_specialties[1 + FLOOR(RANDOM() * ARRAY_LENGTH(v_specialties, 1))::INT];

        v_selected_zip := v_zip_codes[1 + FLOOR(RANDOM() * ARRAY_LENGTH(v_zip_codes, 1))::INT];

        

        INSERT INTO provider_directory (

            provider_id, npi, provider_type, specialty,

            first_name, last_name, practice_name,

            network_status, tier_level, accepting_new_patients,

            practice_zip, practice_state,

            board_certified, years_in_practice, patient_satisfaction_score,

            contracted_plans

        ) VALUES (

            v_provider_id,

            v_npi,

            'Specialist',

            v_specialty,

            'Dr. ' || CHR(65 + FLOOR(RANDOM() * 26)::INT),

            'Specialist-' || v_counter,

            v_specialty || ' Center',

            'Active',

            CASE WHEN RANDOM() < 0.70 THEN 'Tier 1' ELSE 'Tier 2' END,

            RANDOM() < 0.75,

            v_selected_zip,

            'PA',

            RANDOM() < 0.95,

            5 + FLOOR(RANDOM() * 30)::INT,

            3.8 + (RANDOM() * 1.2),

            CASE 

                WHEN RANDOM() < 0.80 THEN 'H1234-001,H5678-002,H9012-003'

                WHEN RANDOM() < 0.90 THEN 'H1234-001,H5678-002'

                ELSE 'H5678-002,H9012-003'

            END

        );

        

        v_provider_count := v_provider_count + 1;

    END LOOP;

    

    RAISE NOTICE '  Generated % Specialists', 250;

    RAISE NOTICE 'Provider directory generation complete! Total: %', v_provider_count;

END $$;



-- Attribute members to PCPs (every member gets a PCP)

DO $$

DECLARE

    v_member RECORD;

    v_pcp_provider_id VARCHAR(20);

    v_pcp_pool VARCHAR(20)[];

BEGIN

    RAISE NOTICE 'Attributing members to PCPs...';

    

    -- Get pool of active PCPs

    SELECT ARRAY_AGG(provider_id) INTO v_pcp_pool

    FROM provider_directory

    WHERE provider_type = 'PCP'

      AND network_status = 'Active';

    

    FOR v_member IN 

        SELECT member_id, zip_code, plan_id

        FROM plan_members

        WHERE member_id LIKE 'M%'

    LOOP

        -- Randomly assign PCP (in production, would use geographic proximity)

        v_pcp_provider_id := v_pcp_pool[1 + FLOOR(RANDOM() * ARRAY_LENGTH(v_pcp_pool, 1))::INT];

        

        INSERT INTO member_provider_attribution (

            member_id,

            provider_id,

            attribution_type,

            attribution_method,

            attribution_start_date,

            is_current,

            visit_count_ytd,

            last_visit_date,

            measures_attributed

        ) VALUES (

            v_member.member_id,

            v_pcp_provider_id,

            'PCP',

            'Claims-based',

            DATE '2024-01-01',

            TRUE,

            1 + FLOOR(RANDOM() * 8)::INT,

            DATE '2024-01-01' + (RANDOM() * 300)::INT,

            'GSD,KED,EED,PDC-DR,BPD,CBP,PDC-STA,PDC-RASA,COL,BCS,SUPD'

        );

    END LOOP;

    

    RAISE NOTICE 'PCP attribution complete for all members!';

END $$;



-- Attribute members to specialists (30-40% have specialist attribution)

INSERT INTO member_provider_attribution (

    member_id,

    provider_id,

    attribution_type,

    attribution_method,

    attribution_start_date,

    is_current,

    visit_count_ytd,

    last_visit_date,

    measures_attributed

)

SELECT 

    pm.member_id,

    (SELECT provider_id 

     FROM provider_directory 

     WHERE provider_type = 'Specialist'

       AND specialty IN ('Cardiology', 'Endocrinology', 'Nephrology', 'Ophthalmology')

       AND network_status = 'Active'

     ORDER BY RANDOM() 

     LIMIT 1

    ),

    'Specialist',

    'Claims-based',

    DATE '2024-01-01' + (RANDOM() * 100)::INT,

    TRUE,

    1 + FLOOR(RANDOM() * 4)::INT,

    DATE '2024-01-01' + (RANDOM() * 300)::INT,

    CASE 

        WHEN mcc.condition_code LIKE '%E1%' THEN 'GSD,KED,EED'

        WHEN mcc.condition_code LIKE '%I%' THEN 'CBP,BPD'

        ELSE 'COL,BCS'

    END

FROM plan_members pm

JOIN member_chronic_conditions mcc ON pm.member_id = mcc.member_id

WHERE pm.member_id LIKE 'M%'

  AND RANDOM() < 0.35

LIMIT 3500; -- ~35% of 10K members



-- Calculate provider performance metrics

DO $$

DECLARE

    v_provider RECORD;

    v_measure RECORD;

    v_attributed_count INT;

    v_eligible_count INT;

    v_numerator_count INT;

    v_performance_rate DECIMAL(5,2);

    v_open_gaps INT;

    v_closed_gaps INT;

BEGIN

    RAISE NOTICE 'Calculating provider performance metrics...';

    

    FOR v_provider IN 

        SELECT provider_id, specialty

        FROM provider_directory

        WHERE network_status = 'Active'

    LOOP

        -- Count attributed members

        SELECT COUNT(DISTINCT member_id) INTO v_attributed_count

        FROM member_provider_attribution

        WHERE provider_id = v_provider.provider_id

          AND is_current = TRUE;

        

        -- Only calculate for providers with attributed members

        IF v_attributed_count > 0 THEN

            FOR v_measure IN 

                SELECT measure_id, domain

                FROM hedis_measures

            LOOP

                -- Determine eligibility based on specialty

                -- PCPs get all measures, specialists get domain-specific

                IF v_provider.specialty IN ('Internal Medicine', 'Family Medicine') OR

                   (v_provider.specialty = 'Endocrinology' AND v_measure.domain = 'Diabetes') OR

                   (v_provider.specialty = 'Cardiology' AND v_measure.domain = 'Cardiovascular') OR

                   (v_provider.specialty = 'Ophthalmology' AND v_measure.measure_id = 'EED') OR

                   (v_provider.specialty = 'Nephrology' AND v_measure.measure_id = 'KED') THEN

                    

                    -- Calculate performance

                    v_eligible_count := FLOOR(v_attributed_count * (0.30 + RANDOM() * 0.40))::INT;

                    

                    IF v_eligible_count > 0 THEN

                        -- Performance varies by provider quality

                        v_performance_rate := 55 + (RANDOM() * 35);

                        v_numerator_count := FLOOR(v_eligible_count * (v_performance_rate / 100.0))::INT;

                        

                        v_open_gaps := v_eligible_count - v_numerator_count;

                        v_closed_gaps := FLOOR(v_numerator_count * 0.70)::INT;

                        

                        INSERT INTO provider_performance (

                            provider_id,

                            measure_id,

                            measurement_year,

                            attributed_members,

                            eligible_for_measure,

                            numerator_compliant,

                            performance_rate,

                            open_gaps,

                            closed_gaps_ytd,

                            top_performer,

                            needs_improvement

                        ) VALUES (

                            v_provider.provider_id,

                            v_measure.measure_id,

                            2024,

                            v_attributed_count,

                            v_eligible_count,

                            v_numerator_count,

                            ROUND(v_performance_rate, 2),

                            v_open_gaps,

                            v_closed_gaps,

                            v_performance_rate >= 80,

                            v_performance_rate < 60

                        );

                    END IF;

                END IF;

            END LOOP;

        END IF;

    END LOOP;

    

    RAISE NOTICE 'Provider performance calculation complete!';

END $$;



-- Calculate network average for benchmarking

UPDATE provider_performance pp

SET network_avg_rate = (

    SELECT AVG(performance_rate)

    FROM provider_performance pp2

    WHERE pp2.measure_id = pp.measure_id

      AND pp2.measurement_year = pp.measurement_year

);



-- Calculate percentile ranks

WITH ranked_providers AS (

    SELECT 

        performance_id,

        measure_id,

        performance_rate,

        PERCENT_RANK() OVER (

            PARTITION BY measure_id 

            ORDER BY performance_rate

        ) * 100 AS percentile

    FROM provider_performance

    WHERE measurement_year = 2024

)

UPDATE provider_performance pp

SET percentile_rank = ROUND(rp.percentile)::INT

FROM ranked_providers rp

WHERE pp.performance_id = rp.performance_id;



-- Generate provider collaboration scores

INSERT INTO provider_collaboration_scores (

    provider_id,

    responsiveness_score,

    documentation_score,

    referral_score,

    engagement_score,

    overall_collaboration_score,

    collaboration_tier,

    avg_days_to_close_gap,

    gap_closure_rate_pct,

    quality_program_participant,

    responsive_to_outreach

)

SELECT 

    pd.provider_id,

    50 + (RANDOM() * 40) AS responsiveness,

    60 + (RANDOM() * 35) AS documentation,

    55 + (RANDOM() * 35) AS referral,

    45 + (RANDOM() * 45) AS engagement,

    (50 + RANDOM() * 40 + 60 + RANDOM() * 35 + 55 + RANDOM() * 35 + 45 + RANDOM() * 45) / 4 AS overall_score,

    CASE 

        WHEN RANDOM() < 0.25 THEN 'Excellent'

        WHEN RANDOM() < 0.65 THEN 'Good'

        WHEN RANDOM() < 0.90 THEN 'Fair'

        ELSE 'Poor'

    END,

    30 + (RANDOM() * 60),

    55 + (RANDOM() * 35),

    RANDOM() < 0.60,

    RANDOM() < 0.75

FROM provider_directory pd

WHERE pd.network_status = 'Active';



-- Update collaboration tier based on overall score

UPDATE provider_collaboration_scores

SET collaboration_tier = CASE 

    WHEN overall_collaboration_score >= 80 THEN 'Excellent'

    WHEN overall_collaboration_score >= 65 THEN 'Good'

    WHEN overall_collaboration_score >= 50 THEN 'Fair'

    ELSE 'Poor'

END;



-- Generate sample referrals (specialists referring back to PCPs for follow-up)

INSERT INTO provider_referrals (

    referring_provider_id,

    referred_to_provider_id,

    member_id,

    referral_date,

    referral_type,

    related_measure_id,

    gap_closure_referral,

    appointment_completed,

    appointment_date,

    resulted_in_gap_closure

)

SELECT 

    mpa_spec.provider_id AS referring_provider,

    mpa_pcp.provider_id AS referred_to_provider,

    mpa_spec.member_id,

    DATE '2024-01-01' + (RANDOM() * 270)::INT,

    CASE FLOOR(RANDOM() * 3)

        WHEN 0 THEN 'Routine'

        WHEN 1 THEN 'Consultation'

        ELSE 'Follow-up'

    END,

    (SELECT measure_id FROM hedis_measures ORDER BY RANDOM() LIMIT 1),

    RANDOM() < 0.40,

    RANDOM() < 0.75,

    DATE '2024-01-01' + (RANDOM() * 280)::INT,

    RANDOM() < 0.35

FROM member_provider_attribution mpa_spec

JOIN member_provider_attribution mpa_pcp 

    ON mpa_spec.member_id = mpa_pcp.member_id

WHERE mpa_spec.attribution_type = 'Specialist'

  AND mpa_pcp.attribution_type = 'PCP'

  AND RANDOM() < 0.15 -- 15% of specialist attributions result in referrals

LIMIT 1500;



-- Create indexes for performance

CREATE INDEX idx_provider_specialty ON provider_directory(specialty, network_status);

CREATE INDEX idx_provider_zip ON provider_directory(practice_zip);

CREATE INDEX idx_provider_performance_provider ON provider_performance(provider_id, measurement_year);

CREATE INDEX idx_provider_performance_measure ON provider_performance(measure_id, performance_rate);

CREATE INDEX idx_attribution_member ON member_provider_attribution(member_id, is_current);

CREATE INDEX idx_attribution_provider ON member_provider_attribution(provider_id, is_current);

CREATE INDEX idx_referrals_referring ON provider_referrals(referring_provider_id);

CREATE INDEX idx_referrals_referred ON provider_referrals(referred_to_provider_id);



-- ============================================================================

-- SECTION 3: PROVIDER ANALYTICS VIEWS

-- ============================================================================



-- View 1: Provider Performance Summary

CREATE OR REPLACE VIEW vw_provider_performance_summary AS

SELECT 

    pd.provider_id,

    pd.npi,

    pd.first_name || ' ' || pd.last_name AS provider_name,

    pd.provider_type,

    pd.specialty,

    pd.practice_zip,

    pd.tier_level,

    pd.patient_satisfaction_score,

    

    -- Attribution metrics

    COUNT(DISTINCT mpa.member_id) AS total_attributed_members,

    

    -- Performance across all measures

    COUNT(DISTINCT pp.measure_id) AS measures_tracked,

    ROUND(AVG(pp.performance_rate), 2) AS avg_performance_rate,

    SUM(pp.open_gaps) AS total_open_gaps,

    SUM(pp.closed_gaps_ytd) AS total_gaps_closed_ytd,

    

    -- Quality indicators

    COUNT(CASE WHEN pp.top_performer THEN 1 END) AS measures_top_performer,

    COUNT(CASE WHEN pp.needs_improvement THEN 1 END) AS measures_need_improvement,

    

    -- Collaboration

    pcs.overall_collaboration_score,

    pcs.collaboration_tier,

    pcs.avg_days_to_close_gap,

    pcs.gap_closure_rate_pct,

    

    -- Network participation

    pd.accepting_new_patients,

    pd.years_in_practice,

    pd.board_certified



FROM provider_directory pd

LEFT JOIN member_provider_attribution mpa 

    ON pd.provider_id = mpa.provider_id 

    AND mpa.is_current = TRUE

LEFT JOIN provider_performance pp 

    ON pd.provider_id = pp.provider_id 

    AND pp.measurement_year = 2024

LEFT JOIN provider_collaboration_scores pcs 

    ON pd.provider_id = pcs.provider_id



WHERE pd.network_status = 'Active'



GROUP BY 

    pd.provider_id, pd.npi, pd.first_name, pd.last_name,

    pd.provider_type, pd.specialty, pd.practice_zip, pd.tier_level,

    pd.patient_satisfaction_score, pd.accepting_new_patients,

    pd.years_in_practice, pd.board_certified,

    pcs.overall_collaboration_score, pcs.collaboration_tier,

    pcs.avg_days_to_close_gap, pcs.gap_closure_rate_pct;



-- View 2: Provider Performance by Measure

CREATE OR REPLACE VIEW vw_provider_measure_performance AS

SELECT 

    pp.provider_id,

    pd.provider_type,

    pd.specialty,

    pp.measure_id,

    hm.measure_name,

    hm.domain,

    

    -- Performance metrics

    pp.attributed_members,

    pp.eligible_for_measure,

    pp.numerator_compliant,

    pp.performance_rate,

    pp.network_avg_rate,

    pp.performance_rate - pp.network_avg_rate AS variance_from_network_avg,

    pp.percentile_rank,

    

    -- Gap metrics

    pp.open_gaps,

    pp.closed_gaps_ytd,

    CASE 

        WHEN pp.eligible_for_measure > 0 

        THEN ROUND(pp.closed_gaps_ytd::DECIMAL / pp.eligible_for_measure * 100, 1)

        ELSE 0 

    END AS gap_closure_rate_pct,

    

    -- Quality flags

    pp.top_performer,

    pp.needs_improvement,

    

    -- Categorization

    CASE 

        WHEN pp.percentile_rank >= 90 THEN 'Top 10%'

        WHEN pp.percentile_rank >= 75 THEN 'Top Quartile'

        WHEN pp.percentile_rank >= 50 THEN 'Above Average'

        WHEN pp.percentile_rank >= 25 THEN 'Below Average'

        ELSE 'Bottom Quartile'

    END AS performance_category



FROM provider_performance pp

JOIN provider_directory pd ON pp.provider_id = pd.provider_id

JOIN hedis_measures hm ON pp.measure_id = hm.measure_id



WHERE pp.measurement_year = 2024

  AND pd.network_status = 'Active';



-- View 3: Network Adequacy Dashboard

CREATE OR REPLACE VIEW vw_network_adequacy_dashboard AS

SELECT 

    pd.specialty,

    COUNT(DISTINCT pd.provider_id) AS total_providers,

    COUNT(DISTINCT CASE WHEN pd.accepting_new_patients THEN pd.provider_id END) AS accepting_new,

    COUNT(DISTINCT CASE WHEN pd.tier_level = 'Tier 1' THEN pd.provider_id END) AS tier_1_providers,

    

    -- Member attribution

    COUNT(DISTINCT mpa.member_id) AS total_members_attributed,

    

    -- Ratios

    ROUND(

        COUNT(DISTINCT mpa.member_id)::DECIMAL / 

        NULLIF(COUNT(DISTINCT pd.provider_id), 0),

        1

    ) AS members_per_provider,

    

    ROUND(

        COUNT(DISTINCT pd.provider_id)::DECIMAL / 

        NULLIF(COUNT(DISTINCT mpa.member_id), 0) * 1000,

        2

    ) AS providers_per_1000_members,

    

    -- Performance

    ROUND(AVG(pp.performance_rate), 1) AS avg_performance_rate,

    ROUND(AVG(pcs.overall_collaboration_score), 1) AS avg_collaboration_score,

    

    -- Adequacy assessment

    CASE 

        WHEN COUNT(DISTINCT pd.provider_id)::DECIMAL / NULLIF(COUNT(DISTINCT mpa.member_id), 0) * 1000 >= 2.0 

        THEN 'Excellent'

        WHEN COUNT(DISTINCT pd.provider_id)::DECIMAL / NULLIF(COUNT(DISTINCT mpa.member_id), 0) * 1000 >= 1.0 

        THEN 'Adequate'

        WHEN COUNT(DISTINCT pd.provider_id)::DECIMAL / NULLIF(COUNT(DISTINCT mpa.member_id), 0) * 1000 >= 0.5 

        THEN 'Marginal'

        ELSE 'Insufficient'

    END AS adequacy_rating



FROM provider_directory pd

LEFT JOIN member_provider_attribution mpa 

    ON pd.provider_id = mpa.provider_id 

    AND mpa.is_current = TRUE

LEFT JOIN provider_performance pp 

    ON pd.provider_id = pp.provider_id 

    AND pp.measurement_year = 2024

LEFT JOIN provider_collaboration_scores pcs 

    ON pd.provider_id = pcs.provider_id



WHERE pd.network_status = 'Active'

  AND pd.provider_type IN ('PCP', 'Specialist')



GROUP BY pd.specialty

ORDER BY total_members_attributed DESC;



-- View 4: Referral Network Analysis

CREATE OR REPLACE VIEW vw_referral_network_analysis AS

SELECT 

    pd_ref.provider_id AS referring_provider_id,

    pd_ref.specialty AS referring_specialty,

    pd_to.specialty AS referred_to_specialty,

    

    -- Referral volume

    COUNT(*) AS total_referrals,

    COUNT(DISTINCT pr.member_id) AS unique_members_referred,

    

    -- Completion metrics

    COUNT(CASE WHEN pr.appointment_completed THEN 1 END) AS appointments_completed,

    ROUND(

        COUNT(CASE WHEN pr.appointment_completed THEN 1 END)::DECIMAL / 

        NULLIF(COUNT(*), 0) * 100,

        1

    ) AS completion_rate_pct,

    

    -- Gap closure impact

    COUNT(CASE WHEN pr.gap_closure_referral THEN 1 END) AS gap_closure_referrals,

    COUNT(CASE WHEN pr.resulted_in_gap_closure THEN 1 END) AS resulted_in_closure,

    ROUND(

        COUNT(CASE WHEN pr.resulted_in_gap_closure THEN 1 END)::DECIMAL / 

        NULLIF(COUNT(CASE WHEN pr.gap_closure_referral THEN 1 END), 0) * 100,

        1

    ) AS gap_closure_success_rate_pct,

    

    -- Timing

    ROUND(AVG(pr.days_to_appointment), 1) AS avg_days_to_appointment



FROM provider_referrals pr

JOIN provider_directory pd_ref ON pr.referring_provider_id = pd_ref.provider_id

JOIN provider_directory pd_to ON pr.referred_to_provider_id = pd_to.provider_id



WHERE pd_ref.network_status = 'Active'

  AND pd_to.network_status = 'Active'



GROUP BY 

    pd_ref.provider_id, pd_ref.specialty,

    pd_to.specialty



HAVING COUNT(*) >= 5 -- Minimum 5 referrals for meaningful analysis



ORDER BY total_referrals DESC;



-- View 5: Top and Bottom Performers by Measure

CREATE OR REPLACE VIEW vw_provider_performance_rankings AS

WITH ranked_providers AS (

    SELECT 

        pp.provider_id,

        pd.specialty,

        pp.measure_id,

        hm.measure_name,

        pp.performance_rate,

        pp.attributed_members,

        pp.eligible_for_measure,

        ROW_NUMBER() OVER (

            PARTITION BY pp.measure_id 

            ORDER BY pp.performance_rate DESC

        ) AS rank_high,

        ROW_NUMBER() OVER (

            PARTITION BY pp.measure_id 

            ORDER BY pp.performance_rate ASC

        ) AS rank_low

    FROM provider_performance pp

    JOIN provider_directory pd ON pp.provider_id = pd.provider_id

    JOIN hedis_measures hm ON pp.measure_id = hm.measure_id

    WHERE pp.measurement_year = 2024

      AND pd.network_status = 'Active'

      AND pp.eligible_for_measure >= 10 -- Minimum volume for valid comparison

)

SELECT 

    measure_id,

    measure_name,

    provider_id,

    specialty,

    performance_rate,

    attributed_members,

    eligible_for_measure,

    CASE 

        WHEN rank_high <= 10 THEN 'Top 10'

        WHEN rank_low <= 10 THEN 'Bottom 10'

    END AS performance_group,

    rank_high,

    rank_low

FROM ranked_providers

WHERE rank_high <= 10 OR rank_low <= 10

ORDER BY measure_id, rank_high;



-- ============================================================================

-- SECTION 4: TEST & VALIDATION QUERIES

-- ============================================================================



-- Test 1: Provider directory summary

SELECT 'TEST 1: Provider Directory Summary' AS test_name;

SELECT 

    provider_type,

    COUNT(*) AS provider_count,

    COUNT(CASE WHEN network_status = 'Active' THEN 1 END) AS active_count,

    COUNT(CASE WHEN accepting_new_patients THEN 1 END) AS accepting_new,

    ROUND(AVG(patient_satisfaction_score), 2) AS avg_satisfaction,

    ROUND(AVG(years_in_practice), 1) AS avg_years_practice

FROM provider_directory

GROUP BY provider_type

ORDER BY provider_count DESC;



-- Test 2: Provider specialty distribution

SELECT 'TEST 2: Top 10 Specialties by Provider Count' AS test_name;

SELECT 

    specialty,

    COUNT(*) AS provider_count,

    COUNT(DISTINCT mpa.member_id) AS members_attributed,

    ROUND(

        COUNT(DISTINCT mpa.member_id)::DECIMAL / 

        NULLIF(COUNT(*), 0),

        1

    ) AS members_per_provider

FROM provider_directory pd

LEFT JOIN member_provider_attribution mpa 

    ON pd.provider_id = mpa.provider_id 

    AND mpa.is_current = TRUE

WHERE pd.network_status = 'Active'

GROUP BY specialty

ORDER BY provider_count DESC

LIMIT 10;



-- Test 3: Member attribution coverage

SELECT 'TEST 3: Member Attribution Coverage' AS test_name;

SELECT 

    'Total Members' AS metric,

    COUNT(*) AS count

FROM plan_members

WHERE member_id LIKE 'M%'

UNION ALL

SELECT 

    'Members with PCP',

    COUNT(DISTINCT member_id)

FROM member_provider_attribution

WHERE attribution_type = 'PCP'

  AND is_current = TRUE

UNION ALL

SELECT 

    'Members with Specialist',

    COUNT(DISTINCT member_id)

FROM member_provider_attribution

WHERE attribution_type = 'Specialist'

  AND is_current = TRUE;



-- Test 4: Provider performance distribution

SELECT 'TEST 4: Provider Performance Distribution by Measure' AS test_name;

SELECT 

    pp.measure_id,

    hm.measure_name,

    COUNT(DISTINCT pp.provider_id) AS providers_tracked,

    ROUND(AVG(pp.performance_rate), 1) AS avg_performance,

    ROUND(MIN(pp.performance_rate), 1) AS min_performance,

    ROUND(MAX(pp.performance_rate), 1) AS max_performance,

    COUNT(CASE WHEN pp.top_performer THEN 1 END) AS top_performers,

    COUNT(CASE WHEN pp.needs_improvement THEN 1 END) AS need_improvement

FROM provider_performance pp

JOIN hedis_measures hm ON pp.measure_id = hm.measure_id

WHERE pp.measurement_year = 2024

GROUP BY pp.measure_id, hm.measure_name

ORDER BY providers_tracked DESC

LIMIT 10;



-- Test 5: Network adequacy summary

SELECT 'TEST 5: Network Adequacy by Specialty' AS test_name;

SELECT 

    specialty,

    total_providers,

    total_members_attributed,

    members_per_provider,

    providers_per_1000_members,

    adequacy_rating

FROM vw_network_adequacy_dashboard

ORDER BY total_members_attributed DESC

LIMIT 10;



-- Test 6: Collaboration scores distribution

SELECT 'TEST 6: Provider Collaboration Score Distribution' AS test_name;

SELECT 

    collaboration_tier,

    COUNT(*) AS provider_count,

    ROUND(AVG(overall_collaboration_score), 1) AS avg_score,

    ROUND(AVG(gap_closure_rate_pct), 1) AS avg_closure_rate,

    ROUND(AVG(avg_days_to_close_gap), 1) AS avg_days_to_close

FROM provider_collaboration_scores

GROUP BY collaboration_tier

ORDER BY 

    CASE collaboration_tier

        WHEN 'Excellent' THEN 1

        WHEN 'Good' THEN 2

        WHEN 'Fair' THEN 3

        ELSE 4

    END;



-- Test 7: Referral patterns summary

SELECT 'TEST 7: Referral Network Summary' AS test_name;

SELECT 

    referring_specialty,

    referred_to_specialty,

    total_referrals,

    unique_members_referred,

    completion_rate_pct,

    gap_closure_success_rate_pct

FROM vw_referral_network_analysis

ORDER BY total_referrals DESC

LIMIT 10;



-- Test 8: Top performers sample

SELECT 'TEST 8: Top 10 Providers Overall' AS test_name;

SELECT 

    provider_id,

    provider_name,

    provider_type,

    specialty,

    total_attributed_members,

    avg_performance_rate,

    total_gaps_closed_ytd,

    collaboration_tier

FROM vw_provider_performance_summary

WHERE total_attributed_members >= 10

ORDER BY avg_performance_rate DESC

LIMIT 10;



-- ============================================================================

-- END OF PHASE 2 CHAT 2

-- ============================================================================


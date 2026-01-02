/*******************************************************************************

HEDIS STAR RATING PORTFOLIO OPTIMIZER - Phase 2 Chat 1

Member Engagement & Outreach Effectiveness Tracking



Purpose: Track member engagement patterns, outreach effectiveness, and barriers

Author: Robert Reichert  

Created: 2025-11-18

Database: PostgreSQL

Prerequisites: Phase 1 (Chats 1-4) must be completed first



Components:

1. Member Engagement Scoring Model

2. Outreach Campaign Tracking

3. Contact Attempt Analysis

4. Response Rate Metrics by Channel

5. Barrier Resolution Tracking

6. Member Preference Management

7. Engagement Trend Analysis



Usage:

- Builds on Phase 1 member and gap data

- Run after Phase 1 Chat 4 complete

- Expected runtime: 3-4 minutes

- Expected output: Engagement scores for 10K members, outreach analytics

*******************************************************************************/



-- ============================================================================

-- SECTION 1: MEMBER ENGAGEMENT INFRASTRUCTURE

-- ============================================================================



-- Member Engagement Scores

DROP TABLE IF EXISTS member_engagement_scores CASCADE;



CREATE TABLE member_engagement_scores (

    engagement_score_id SERIAL PRIMARY KEY,

    member_id VARCHAR(50) REFERENCES plan_members(member_id),

    score_date DATE NOT NULL DEFAULT CURRENT_DATE,

    

    -- Component scores (0-100 scale)

    response_score DECIMAL(5,2), -- How responsive to outreach

    compliance_score DECIMAL(5,2), -- Historical gap closure rate

    technology_score DECIMAL(5,2), -- Digital engagement level

    preventive_score DECIMAL(5,2), -- Preventive care utilization

    

    -- Composite engagement score

    overall_engagement_score DECIMAL(5,2),

    engagement_tier VARCHAR(20), -- High, Medium, Low, Very Low

    

    -- Engagement indicators

    total_contacts_ytd INT DEFAULT 0,

    successful_contacts_ytd INT DEFAULT 0,

    gaps_closed_ytd INT DEFAULT 0,

    gaps_opened_ytd INT DEFAULT 0,

    last_successful_contact DATE,

    days_since_contact INT,

    

    -- Predictive flags

    at_risk_of_disengagement BOOLEAN DEFAULT FALSE,

    requires_intensive_outreach BOOLEAN DEFAULT FALSE,

    

    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    updated_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP

);



-- Member Contact Preferences

DROP TABLE IF EXISTS member_contact_preferences CASCADE;



CREATE TABLE member_contact_preferences (

    preference_id SERIAL PRIMARY KEY,

    member_id VARCHAR(50) REFERENCES plan_members(member_id),

    

    -- Preferred contact methods (ranked 1-5)

    preferred_method_1 VARCHAR(50), -- Phone, Email, SMS, Mail, Portal

    preferred_method_2 VARCHAR(50),

    preferred_method_3 VARCHAR(50),

    

    -- Contact restrictions

    do_not_call BOOLEAN DEFAULT FALSE,

    do_not_email BOOLEAN DEFAULT FALSE,

    do_not_text BOOLEAN DEFAULT FALSE,

    

    -- Timing preferences

    best_contact_time VARCHAR(50), -- Morning, Afternoon, Evening

    best_contact_day VARCHAR(50), -- Weekday, Weekend, Any

    

    -- Language preference

    preferred_language VARCHAR(50) DEFAULT 'English',

    interpreter_needed BOOLEAN DEFAULT FALSE,

    

    -- Communication style

    prefers_detailed_info BOOLEAN DEFAULT FALSE,

    prefers_brief_contact BOOLEAN DEFAULT TRUE,

    

    last_updated DATE DEFAULT CURRENT_DATE,

    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP

);



-- Outreach Campaigns

DROP TABLE IF EXISTS outreach_campaigns CASCADE;



CREATE TABLE outreach_campaigns (

    campaign_id SERIAL PRIMARY KEY,

    campaign_name VARCHAR(200) NOT NULL,

    campaign_type VARCHAR(50), -- Gap Closure, Wellness, Preventive, Education

    

    -- Campaign details

    target_measure_id VARCHAR(20) REFERENCES hedis_measures(measure_id),

    target_population TEXT, -- Description of target criteria

    campaign_start_date DATE NOT NULL,

    campaign_end_date DATE,

    

    -- Campaign metrics

    target_member_count INT,

    members_contacted INT DEFAULT 0,

    successful_contacts INT DEFAULT 0,

    gaps_closed INT DEFAULT 0,

    

    -- Cost tracking

    campaign_budget DECIMAL(10,2),

    cost_to_date DECIMAL(10,2) DEFAULT 0,

    cost_per_contact DECIMAL(8,2),

    cost_per_closure DECIMAL(8,2),

    

    -- Performance

    contact_rate_pct DECIMAL(5,2),

    closure_rate_pct DECIMAL(5,2),

    roi_ratio DECIMAL(6,2),

    

    campaign_status VARCHAR(20) DEFAULT 'Active', -- Active, Completed, Paused

    created_by VARCHAR(100),

    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP

);



-- Member Outreach Contacts

DROP TABLE IF EXISTS member_outreach_contacts CASCADE;



CREATE TABLE member_outreach_contacts (

    contact_id SERIAL PRIMARY KEY,

    member_id VARCHAR(50) REFERENCES plan_members(member_id),

    campaign_id INT REFERENCES outreach_campaigns(campaign_id),

    gap_id INT REFERENCES member_gaps(gap_id),

    

    -- Contact details

    contact_date DATE NOT NULL,

    contact_method VARCHAR(50) NOT NULL, -- Phone, Email, SMS, Mail, Portal, Home Visit

    contact_attempt_number INT DEFAULT 1,

    

    -- Outcome

    contact_outcome VARCHAR(50), -- Successful, Left Message, No Answer, Wrong Number, Declined, Completed

    contact_duration_minutes INT,

    

    -- Follow-up

    follow_up_needed BOOLEAN DEFAULT FALSE,

    follow_up_date DATE,

    follow_up_reason TEXT,

    

    -- Barriers identified

    barrier_identified VARCHAR(100),

    barrier_category VARCHAR(50), -- Transportation, Financial, Health, Behavioral, System

    barrier_resolved BOOLEAN DEFAULT FALSE,

    

    -- Assignment

    assigned_to VARCHAR(100), -- Care coordinator name

    contact_notes TEXT,

    

    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP

);



-- Barrier Resolution Tracking

DROP TABLE IF EXISTS barrier_resolutions CASCADE;



CREATE TABLE barrier_resolutions (

    resolution_id SERIAL PRIMARY KEY,

    contact_id INT REFERENCES member_outreach_contacts(contact_id),

    member_id VARCHAR(50) REFERENCES plan_members(member_id),

    

    -- Barrier details

    barrier_type VARCHAR(100) NOT NULL,

    barrier_description TEXT,

    barrier_identified_date DATE NOT NULL,

    barrier_severity VARCHAR(20), -- Low, Medium, High, Critical

    

    -- Resolution

    resolution_strategy TEXT,

    resolution_date DATE,

    resolution_successful BOOLEAN,

    days_to_resolve INT,

    

    -- Resources used

    resources_provided TEXT, -- Transportation voucher, Financial assistance, etc.

    referrals_made TEXT, -- Social services, community resources

    

    -- Impact

    led_to_gap_closure BOOLEAN DEFAULT FALSE,

    estimated_cost DECIMAL(8,2),

    

    assigned_to VARCHAR(100),

    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP

);



-- ============================================================================

-- SECTION 2: GENERATE DEMO ENGAGEMENT DATA

-- ============================================================================



-- Generate member engagement scores for all 10K members

DO $$

DECLARE

    v_member RECORD;

    v_response_score DECIMAL(5,2);

    v_compliance_score DECIMAL(5,2);

    v_tech_score DECIMAL(5,2);

    v_preventive_score DECIMAL(5,2);

    v_overall_score DECIMAL(5,2);

    v_engagement_tier VARCHAR(20);

    v_total_contacts INT;

    v_successful_contacts INT;

BEGIN

    RAISE NOTICE 'Generating engagement scores for 10K members...';

    

    FOR v_member IN 

        SELECT member_id, risk_score, plan_id

        FROM plan_members 

        WHERE member_id LIKE 'M%'

    LOOP

        -- Generate realistic engagement scores based on risk profile

        -- Higher risk = typically lower engagement

        

        -- Response score (willingness to engage)

        v_response_score := 50 + (RANDOM() * 40) - (v_member.risk_score * 5);

        v_response_score := GREATEST(10, LEAST(95, v_response_score));

        

        -- Compliance score (gap closure history)

        v_compliance_score := 60 + (RANDOM() * 30) - (v_member.risk_score * 3);

        v_compliance_score := GREATEST(15, LEAST(98, v_compliance_score));

        

        -- Technology score (digital engagement)

        v_tech_score := 40 + (RANDOM() * 50);

        v_tech_score := GREATEST(5, LEAST(95, v_tech_score));

        

        -- Preventive care score

        v_preventive_score := 55 + (RANDOM() * 35) - (v_member.risk_score * 2);

        v_preventive_score := GREATEST(20, LEAST(97, v_preventive_score));

        

        -- Calculate weighted overall score

        v_overall_score := (v_response_score * 0.30 + 

                           v_compliance_score * 0.35 + 

                           v_tech_score * 0.15 + 

                           v_preventive_score * 0.20);

        

        -- Determine engagement tier

        CASE 

            WHEN v_overall_score >= 75 THEN v_engagement_tier := 'High';

            WHEN v_overall_score >= 55 THEN v_engagement_tier := 'Medium';

            WHEN v_overall_score >= 35 THEN v_engagement_tier := 'Low';

            ELSE v_engagement_tier := 'Very Low';

        END CASE;

        

        -- Generate contact history

        v_total_contacts := FLOOR(RANDOM() * 8)::INT;

        v_successful_contacts := FLOOR(v_total_contacts * (v_response_score / 100.0))::INT;

        

        INSERT INTO member_engagement_scores (

            member_id,

            response_score,

            compliance_score,

            technology_score,

            preventive_score,

            overall_engagement_score,

            engagement_tier,

            total_contacts_ytd,

            successful_contacts_ytd,

            gaps_closed_ytd,

            gaps_opened_ytd,

            last_successful_contact,

            days_since_contact,

            at_risk_of_disengagement,

            requires_intensive_outreach

        ) VALUES (

            v_member.member_id,

            ROUND(v_response_score, 2),

            ROUND(v_compliance_score, 2),

            ROUND(v_tech_score, 2),

            ROUND(v_preventive_score, 2),

            ROUND(v_overall_score, 2),

            v_engagement_tier,

            v_total_contacts,

            v_successful_contacts,

            (SELECT COUNT(*) FROM member_gaps WHERE member_id = v_member.member_id AND gap_status = 'Closed'),

            (SELECT COUNT(*) FROM member_gaps WHERE member_id = v_member.member_id),

            CASE WHEN v_successful_contacts > 0 THEN CURRENT_DATE - (RANDOM() * 90)::INT ELSE NULL END,

            CASE WHEN v_successful_contacts > 0 THEN (RANDOM() * 90)::INT ELSE NULL END,

            v_overall_score < 40,

            v_overall_score < 30

        );

        

    END LOOP;

    

    RAISE NOTICE 'Engagement scores generated for all members!';

END $$;



-- Generate contact preferences (80% of members have preferences on file)

INSERT INTO member_contact_preferences (

    member_id,

    preferred_method_1,

    preferred_method_2,

    preferred_method_3,

    best_contact_time,

    best_contact_day,

    preferred_language,

    prefers_detailed_info

)

SELECT 

    member_id,

    CASE FLOOR(RANDOM() * 5)

        WHEN 0 THEN 'Phone'

        WHEN 1 THEN 'Email'

        WHEN 2 THEN 'SMS'

        WHEN 3 THEN 'Mail'

        ELSE 'Portal'

    END,

    CASE FLOOR(RANDOM() * 4)

        WHEN 0 THEN 'Email'

        WHEN 1 THEN 'Phone'

        WHEN 2 THEN 'SMS'

        ELSE 'Mail'

    END,

    CASE FLOOR(RANDOM() * 3)

        WHEN 0 THEN 'Portal'

        WHEN 1 THEN 'Mail'

        ELSE 'SMS'

    END,

    CASE FLOOR(RANDOM() * 3)

        WHEN 0 THEN 'Morning (8am-12pm)'

        WHEN 1 THEN 'Afternoon (12pm-5pm)'

        ELSE 'Evening (5pm-8pm)'

    END,

    CASE FLOOR(RANDOM() * 3)

        WHEN 0 THEN 'Weekday'

        WHEN 1 THEN 'Weekend'

        ELSE 'Any'

    END,

    CASE 

        WHEN RANDOM() < 0.92 THEN 'English'

        WHEN RANDOM() < 0.97 THEN 'Spanish'

        ELSE 'Other'

    END,

    RANDOM() < 0.35

FROM plan_members

WHERE member_id LIKE 'M%'

  AND RANDOM() < 0.80; -- 80% have preferences



-- Create outreach campaigns for each measure

INSERT INTO outreach_campaigns (

    campaign_name,

    campaign_type,

    target_measure_id,

    target_population,

    campaign_start_date,

    campaign_end_date,

    target_member_count,

    campaign_budget,

    campaign_status,

    created_by

)

SELECT 

    'Q3 2024 ' || measure_name || ' Gap Closure',

    'Gap Closure',

    measure_id,

    'Members with open gaps for ' || measure_name,

    DATE '2024-07-01',

    DATE '2024-09-30',

    (SELECT COUNT(DISTINCT mg.member_id) 

     FROM member_gaps mg 

     WHERE mg.measure_id = hm.measure_id 

       AND mg.gap_status = 'Open'),

    (SELECT COUNT(DISTINCT mg.member_id) 

     FROM member_gaps mg 

     WHERE mg.measure_id = hm.measure_id 

       AND mg.gap_status = 'Open') * 45.00, -- $45 avg per member

    'Completed',

    'System Generated'

FROM hedis_measures hm;



-- Generate outreach contact attempts (sample for members with gaps)

INSERT INTO member_outreach_contacts (

    member_id,

    campaign_id,

    gap_id,

    contact_date,

    contact_method,

    contact_attempt_number,

    contact_outcome,

    contact_duration_minutes,

    barrier_identified,

    barrier_category,

    assigned_to

)

SELECT 

    mg.member_id,

    oc.campaign_id,

    mg.gap_id,

    mg.gap_opened_date + (RANDOM() * 60)::INT,

    CASE FLOOR(RANDOM() * 5)

        WHEN 0 THEN 'Phone'

        WHEN 1 THEN 'Email'

        WHEN 2 THEN 'SMS'

        WHEN 3 THEN 'Mail'

        ELSE 'Phone'

    END,

    1,

    CASE 

        WHEN RANDOM() < 0.45 THEN 'Successful'

        WHEN RANDOM() < 0.70 THEN 'Left Message'

        WHEN RANDOM() < 0.85 THEN 'No Answer'

        ELSE 'Wrong Number'

    END,

    CASE WHEN RANDOM() < 0.45 THEN 5 + FLOOR(RANDOM() * 15)::INT ELSE NULL END,

    CASE 

        WHEN RANDOM() < 0.25 THEN 

            CASE FLOOR(RANDOM() * 5)

                WHEN 0 THEN 'Transportation'

                WHEN 1 THEN 'Cost Concern'

                WHEN 2 THEN 'No Symptoms'

                WHEN 3 THEN 'Already Completed'

                ELSE 'Scheduling Conflict'

            END

        ELSE NULL

    END,

    CASE 

        WHEN RANDOM() < 0.25 THEN

            CASE FLOOR(RANDOM() * 5)

                WHEN 0 THEN 'Transportation'

                WHEN 1 THEN 'Financial'

                WHEN 2 THEN 'Behavioral'

                WHEN 3 THEN 'System'

                ELSE 'Health'

            END

        ELSE NULL

    END,

    CASE FLOOR(RANDOM() * 4)

        WHEN 0 THEN 'Care Coordinator A'

        WHEN 1 THEN 'Care Coordinator B'

        WHEN 2 THEN 'Care Coordinator C'

        ELSE 'Vendor Team'

    END

FROM member_gaps mg

JOIN outreach_campaigns oc ON mg.measure_id = oc.target_measure_id

WHERE mg.gap_status IN ('Open', 'Closed')

  AND RANDOM() < 0.40; -- 40% of gaps get outreach contacts



-- Create indexes for performance

CREATE INDEX idx_engagement_member ON member_engagement_scores(member_id);

CREATE INDEX idx_engagement_tier ON member_engagement_scores(engagement_tier);

CREATE INDEX idx_engagement_score ON member_engagement_scores(overall_engagement_score);

CREATE INDEX idx_outreach_member_campaign ON member_outreach_contacts(member_id, campaign_id);

CREATE INDEX idx_outreach_date ON member_outreach_contacts(contact_date);

CREATE INDEX idx_outreach_outcome ON member_outreach_contacts(contact_outcome);



-- ============================================================================

-- SECTION 3: ENGAGEMENT ANALYTICS VIEWS

-- ============================================================================



-- View 1: Member Engagement Summary

CREATE OR REPLACE VIEW vw_member_engagement_summary AS

SELECT 

    mes.member_id,

    pm.plan_id,

    mp.plan_name,

    mes.overall_engagement_score,

    mes.engagement_tier,

    mes.response_score,

    mes.compliance_score,

    mes.technology_score,

    mes.preventive_score,

    

    -- Contact metrics

    mes.total_contacts_ytd,

    mes.successful_contacts_ytd,

    CASE 

        WHEN mes.total_contacts_ytd > 0 

        THEN ROUND(mes.successful_contacts_ytd::DECIMAL / mes.total_contacts_ytd * 100, 1)

        ELSE 0 

    END AS contact_success_rate_pct,

    

    -- Gap metrics

    mes.gaps_closed_ytd,

    mes.gaps_opened_ytd,

    CASE 

        WHEN mes.gaps_opened_ytd > 0 

        THEN ROUND(mes.gaps_closed_ytd::DECIMAL / mes.gaps_opened_ytd * 100, 1)

        ELSE 0 

    END AS gap_closure_rate_pct,

    

    -- Recency

    mes.last_successful_contact,

    mes.days_since_contact,

    

    -- Risk flags

    mes.at_risk_of_disengagement,

    mes.requires_intensive_outreach,

    

    -- Demographics

    EXTRACT(YEAR FROM AGE(pm.date_of_birth)) AS age,

    pm.gender,

    pm.risk_score,

    pm.zip_code



FROM member_engagement_scores mes

JOIN plan_members pm ON mes.member_id = pm.member_id

JOIN ma_plans mp ON pm.plan_id = mp.plan_id

WHERE pm.member_id LIKE 'M%';



-- View 2: Outreach Campaign Performance

CREATE OR REPLACE VIEW vw_campaign_performance AS

SELECT 

    oc.campaign_id,

    oc.campaign_name,

    oc.campaign_type,

    oc.target_measure_id,

    hm.measure_name,

    oc.campaign_start_date,

    oc.campaign_end_date,

    

    -- Volume metrics

    oc.target_member_count,

    COUNT(DISTINCT moc.member_id) AS members_contacted,

    COUNT(DISTINCT CASE WHEN moc.contact_outcome = 'Successful' THEN moc.member_id END) AS successful_contacts,

    COUNT(DISTINCT moc.contact_id) AS total_contact_attempts,

    

    -- Outcome metrics

    COUNT(DISTINCT CASE WHEN mg.gap_status = 'Closed' AND mg.gap_closed_date >= oc.campaign_start_date THEN mg.gap_id END) AS gaps_closed,

    

    -- Effectiveness rates

    ROUND(

        COUNT(DISTINCT moc.member_id)::DECIMAL / 

        NULLIF(oc.target_member_count, 0) * 100, 

        1

    ) AS contact_rate_pct,

    

    ROUND(

        COUNT(DISTINCT CASE WHEN moc.contact_outcome = 'Successful' THEN moc.member_id END)::DECIMAL / 

        NULLIF(COUNT(DISTINCT moc.member_id), 0) * 100,

        1

    ) AS success_rate_pct,

    

    ROUND(

        COUNT(DISTINCT CASE WHEN mg.gap_status = 'Closed' AND mg.gap_closed_date >= oc.campaign_start_date THEN mg.gap_id END)::DECIMAL / 

        NULLIF(COUNT(DISTINCT moc.member_id), 0) * 100,

        1

    ) AS closure_rate_pct,

    

    -- Cost metrics

    oc.campaign_budget,

    oc.cost_to_date,

    CASE 

        WHEN COUNT(DISTINCT moc.member_id) > 0 

        THEN ROUND(oc.cost_to_date / COUNT(DISTINCT moc.member_id), 2)

        ELSE 0 

    END AS actual_cost_per_contact,

    

    CASE 

        WHEN COUNT(DISTINCT CASE WHEN mg.gap_status = 'Closed' THEN mg.gap_id END) > 0 

        THEN ROUND(oc.cost_to_date / COUNT(DISTINCT CASE WHEN mg.gap_status = 'Closed' THEN mg.gap_id END), 2)

        ELSE 0 

    END AS actual_cost_per_closure,

    

    oc.campaign_status



FROM outreach_campaigns oc

LEFT JOIN hedis_measures hm ON oc.target_measure_id = hm.measure_id

LEFT JOIN member_outreach_contacts moc ON oc.campaign_id = moc.campaign_id

LEFT JOIN member_gaps mg ON moc.gap_id = mg.gap_id

GROUP BY 

    oc.campaign_id, oc.campaign_name, oc.campaign_type, 

    oc.target_measure_id, hm.measure_name,

    oc.campaign_start_date, oc.campaign_end_date,

    oc.target_member_count, oc.campaign_budget, oc.cost_to_date, oc.campaign_status;



-- View 3: Contact Method Effectiveness

CREATE OR REPLACE VIEW vw_contact_method_effectiveness AS

SELECT 

    contact_method,

    COUNT(*) AS total_attempts,

    COUNT(CASE WHEN contact_outcome = 'Successful' THEN 1 END) AS successful_attempts,

    ROUND(

        COUNT(CASE WHEN contact_outcome = 'Successful' THEN 1 END)::DECIMAL / 

        NULLIF(COUNT(*), 0) * 100,

        1

    ) AS success_rate_pct,

    

    AVG(contact_duration_minutes) AS avg_duration_minutes,

    

    COUNT(DISTINCT moc.member_id) AS unique_members_contacted,

    

    COUNT(CASE WHEN barrier_identified IS NOT NULL THEN 1 END) AS barriers_identified,

    

    -- Gap closure linkage

    COUNT(DISTINCT CASE 

        WHEN mg.gap_status = 'Closed' 

        AND mg.gap_closed_date BETWEEN moc.contact_date AND moc.contact_date + 30 

        THEN moc.gap_id 

    END) AS gaps_closed_within_30_days,

    

    ROUND(

        COUNT(DISTINCT CASE 

            WHEN mg.gap_status = 'Closed' 

            AND mg.gap_closed_date BETWEEN moc.contact_date AND moc.contact_date + 30 

            THEN moc.gap_id 

        END)::DECIMAL / 

        NULLIF(COUNT(CASE WHEN contact_outcome = 'Successful' THEN 1 END), 0) * 100,

        1

    ) AS closure_conversion_rate_pct



FROM member_outreach_contacts moc

LEFT JOIN member_gaps mg ON moc.gap_id = mg.gap_id

GROUP BY contact_method

ORDER BY success_rate_pct DESC;



-- View 4: Barrier Analysis

CREATE OR REPLACE VIEW vw_barrier_analysis AS

SELECT 

    barrier_category,

    barrier_identified AS barrier_type,

    COUNT(*) AS occurrence_count,

    COUNT(DISTINCT moc.member_id) AS unique_members_affected,

    

    ROUND(

        COUNT(*)::DECIMAL / 

        (SELECT COUNT(*) FROM member_outreach_contacts WHERE barrier_identified IS NOT NULL) * 100,

        1

    ) AS pct_of_all_barriers,

    

    -- Resolution tracking

    COUNT(CASE WHEN barrier_resolved THEN 1 END) AS resolved_count,

    ROUND(

        COUNT(CASE WHEN barrier_resolved THEN 1 END)::DECIMAL / 

        NULLIF(COUNT(*), 0) * 100,

        1

    ) AS resolution_rate_pct,

    

    -- Impact on gaps

    COUNT(DISTINCT CASE WHEN mg.gap_status = 'Closed' THEN moc.gap_id END) AS associated_closures



FROM member_outreach_contacts moc

LEFT JOIN member_gaps mg ON moc.gap_id = mg.gap_id

WHERE barrier_identified IS NOT NULL

GROUP BY barrier_category, barrier_identified

ORDER BY occurrence_count DESC;



-- ============================================================================

-- SECTION 4: TEST & VALIDATION QUERIES

-- ============================================================================



-- Test 1: Engagement score distribution

SELECT 'TEST 1: Engagement Score Distribution' AS test_name;

SELECT 

    engagement_tier,

    COUNT(*) AS member_count,

    ROUND(COUNT(*)::DECIMAL / 10000 * 100, 1) AS pct_of_total,

    ROUND(AVG(overall_engagement_score), 1) AS avg_score,

    ROUND(MIN(overall_engagement_score), 1) AS min_score,

    ROUND(MAX(overall_engagement_score), 1) AS max_score

FROM member_engagement_scores

GROUP BY engagement_tier

ORDER BY 

    CASE engagement_tier

        WHEN 'High' THEN 1

        WHEN 'Medium' THEN 2

        WHEN 'Low' THEN 3

        ELSE 4

    END;



-- Test 2: Campaign performance summary

SELECT 'TEST 2: Campaign Performance Summary' AS test_name;

SELECT 

    campaign_name,

    target_member_count,

    members_contacted,

    successful_contacts,

    gaps_closed,

    ROUND(contact_rate_pct, 1) AS contact_rate,

    ROUND(success_rate_pct, 1) AS success_rate,

    ROUND(closure_rate_pct, 1) AS closure_rate

FROM vw_campaign_performance

ORDER BY gaps_closed DESC

LIMIT 10;



-- Test 3: Contact method effectiveness

SELECT 'TEST 3: Contact Method Effectiveness' AS test_name;

SELECT * FROM vw_contact_method_effectiveness

ORDER BY success_rate_pct DESC;



-- Test 4: Top barriers

SELECT 'TEST 4: Top 10 Barriers to Care' AS test_name;

SELECT 

    barrier_category,

    barrier_type,

    occurrence_count,

    unique_members_affected,

    resolution_rate_pct

FROM vw_barrier_analysis

ORDER BY occurrence_count DESC

LIMIT 10;



-- Test 5: Engagement by plan

SELECT 'TEST 5: Engagement Scores by Plan' AS test_name;

SELECT 

    plan_id,

    plan_name,

    COUNT(*) AS member_count,

    ROUND(AVG(overall_engagement_score), 1) AS avg_engagement,

    COUNT(CASE WHEN engagement_tier = 'High' THEN 1 END) AS high_engagement,

    COUNT(CASE WHEN engagement_tier = 'Very Low' THEN 1 END) AS very_low_engagement,

    COUNT(CASE WHEN at_risk_of_disengagement THEN 1 END) AS at_risk_count

FROM vw_member_engagement_summary

GROUP BY plan_id, plan_name

ORDER BY plan_id;



-- Test 6: Contact preferences coverage

SELECT 'TEST 6: Contact Preferences Coverage' AS test_name;

SELECT 

    'Total Members' AS metric,

    COUNT(DISTINCT pm.member_id) AS count

FROM plan_members pm

WHERE pm.member_id LIKE 'M%'

UNION ALL

SELECT 

    'With Preferences on File',

    COUNT(DISTINCT mcp.member_id)

FROM member_contact_preferences mcp

UNION ALL

SELECT 

    'Coverage Percentage',

    ROUND(

        COUNT(DISTINCT mcp.member_id)::DECIMAL / 

        (SELECT COUNT(*) FROM plan_members WHERE member_id LIKE 'M%') * 100,

        1

    )

FROM member_contact_preferences mcp;



-- ============================================================================

-- END OF PHASE 2 CHAT 1

-- ============================================================================


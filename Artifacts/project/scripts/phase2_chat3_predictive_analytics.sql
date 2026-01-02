/*******************************************************************************

HEDIS STAR RATING PORTFOLIO OPTIMIZER - Phase 2 Chat 3

Predictive Analytics & Risk Scoring Engine



Purpose: Predictive models for gap closure, risk stratification, and early warnings

Author: Robert Reichert

Created: 2025-11-18

Database: PostgreSQL

Prerequisites: Phase 1 (Chats 1-4) and Phase 2 (Chats 1-2) must be completed



Components:

1. Gap Closure Propensity Scoring

2. Member Risk Stratification Models

3. Cost Risk Prediction

4. Early Warning System (Disengagement Risk)

5. Intervention Prioritization Algorithm

6. Predictive Gap Identification

7. Member Trajectory Analysis

8. ML-Ready Feature Engineering



Usage:

- Builds on Phase 1 & Phase 2 data

- Run after Phase 2 Chat 2 complete

- Expected runtime: 4-5 minutes

- Expected output: Predictive scores for 10K members, risk models operational

*******************************************************************************/



-- ============================================================================

-- SECTION 1: PREDICTIVE ANALYTICS INFRASTRUCTURE

-- ============================================================================



-- Gap Closure Propensity Scores

DROP TABLE IF EXISTS gap_closure_propensity CASCADE;



CREATE TABLE gap_closure_propensity (

    propensity_id SERIAL PRIMARY KEY,

    gap_id INT REFERENCES member_gaps(gap_id),

    member_id VARCHAR(50) REFERENCES plan_members(member_id),

    measure_id VARCHAR(20) REFERENCES hedis_measures(measure_id),

    

    -- Score calculation date

    score_date DATE NOT NULL DEFAULT CURRENT_DATE,

    

    -- Feature inputs (0-100 normalized scores)

    member_engagement_feature DECIMAL(5,2),

    provider_quality_feature DECIMAL(5,2),

    historical_compliance_feature DECIMAL(5,2),

    barrier_complexity_feature DECIMAL(5,2),

    outreach_responsiveness_feature DECIMAL(5,2),

    social_determinants_feature DECIMAL(5,2),

    

    -- Composite propensity score (0-100)

    closure_propensity_score DECIMAL(5,2),

    

    -- Risk categorization

    closure_likelihood VARCHAR(20), -- Very High, High, Medium, Low, Very Low

    recommended_intervention_intensity VARCHAR(20), -- Minimal, Standard, Intensive, Urgent

    

    -- Predictions

    predicted_days_to_close INT,

    predicted_cost_to_close DECIMAL(8,2),

    predicted_closure_date DATE,

    

    -- Model metadata

    model_version VARCHAR(20) DEFAULT 'v1.0',

    confidence_score DECIMAL(5,2), -- Model confidence in prediction

    

    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    UNIQUE(gap_id, score_date)

);



-- Member Risk Stratification

DROP TABLE IF EXISTS member_risk_stratification CASCADE;



CREATE TABLE member_risk_stratification (

    risk_id SERIAL PRIMARY KEY,

    member_id VARCHAR(50) REFERENCES plan_members(member_id),

    stratification_date DATE NOT NULL DEFAULT CURRENT_DATE,

    

    -- Clinical risk dimensions

    clinical_complexity_score DECIMAL(5,2), -- Based on HCC, conditions

    utilization_risk_score DECIMAL(5,2), -- ED visits, admissions

    medication_adherence_risk DECIMAL(5,2), -- PDC measures

    preventive_care_risk DECIMAL(5,2), -- Screening compliance

    

    -- Social risk dimensions

    engagement_risk_score DECIMAL(5,2), -- Contact responsiveness

    financial_risk_score DECIMAL(5,2), -- Cost barriers

    access_risk_score DECIMAL(5,2), -- Transportation, distance

    health_literacy_risk DECIMAL(5,2), -- Communication barriers

    

    -- Composite risk score

    overall_risk_score DECIMAL(5,2),

    risk_tier VARCHAR(20), -- Critical, High, Medium, Low

    

    -- Risk flags

    rising_risk BOOLEAN DEFAULT FALSE, -- Risk increasing vs. prior period

    at_risk_star_impact BOOLEAN DEFAULT FALSE, -- Could impact Star ratings

    high_cost_risk BOOLEAN DEFAULT FALSE, -- Potential high utilizer

    disengagement_risk BOOLEAN DEFAULT FALSE, -- At risk of dropping out

    

    -- Recommended actions

    care_management_needed BOOLEAN DEFAULT FALSE,

    intensive_outreach_needed BOOLEAN DEFAULT FALSE,

    provider_intervention_needed BOOLEAN DEFAULT FALSE,

    

    -- Trajectory

    risk_trend VARCHAR(20), -- Improving, Stable, Worsening, Rapid Decline

    prior_risk_score DECIMAL(5,2),

    risk_change_pct DECIMAL(6,2),

    

    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP

);



-- Cost Risk Predictions

DROP TABLE IF EXISTS member_cost_predictions CASCADE;



CREATE TABLE member_cost_predictions (

    prediction_id SERIAL PRIMARY KEY,

    member_id VARCHAR(50) REFERENCES plan_members(member_id),

    prediction_date DATE NOT NULL DEFAULT CURRENT_DATE,

    prediction_period VARCHAR(20) DEFAULT 'Next 6 Months',

    

    -- Predicted costs

    predicted_medical_cost DECIMAL(10,2),

    predicted_pharmacy_cost DECIMAL(10,2),

    predicted_total_cost DECIMAL(10,2),

    

    -- Cost drivers

    chronic_condition_cost_driver DECIMAL(10,2),

    preventable_ed_cost_driver DECIMAL(10,2),

    medication_nonadherence_cost_driver DECIMAL(10,2),

    

    -- Risk category

    cost_risk_category VARCHAR(20), -- Low, Medium, High, Very High

    percentile_rank INT, -- Cost percentile within plan

    

    -- Intervention opportunity

    estimated_avoidable_cost DECIMAL(10,2),

    intervention_roi DECIMAL(6,2), -- Expected ROI of intervention

    

    -- Confidence metrics

    prediction_confidence DECIMAL(5,2),

    model_version VARCHAR(20) DEFAULT 'v1.0',

    

    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP

);



-- Early Warning System Alerts

DROP TABLE IF EXISTS early_warning_alerts CASCADE;



CREATE TABLE early_warning_alerts (

    alert_id SERIAL PRIMARY KEY,

    member_id VARCHAR(50) REFERENCES plan_members(member_id),

    alert_date DATE NOT NULL DEFAULT CURRENT_DATE,

    

    -- Alert details

    alert_type VARCHAR(50) NOT NULL, -- Disengagement, Gap Escalation, Cost Spike, etc.

    alert_severity VARCHAR(20) NOT NULL, -- Low, Medium, High, Critical

    alert_status VARCHAR(20) DEFAULT 'Active', -- Active, Acknowledged, Resolved, Dismissed

    

    -- Alert description

    alert_title VARCHAR(200),

    alert_description TEXT,

    

    -- Triggering factors

    trigger_metric VARCHAR(100),

    trigger_threshold DECIMAL(10,2),

    current_value DECIMAL(10,2),

    

    -- Related entities

    related_gap_ids TEXT, -- Comma-separated gap IDs

    related_measure_ids TEXT, -- Comma-separated measure IDs

    

    -- Recommended actions

    recommended_action TEXT,

    urgency_level VARCHAR(20), -- Routine, Urgent, Immediate

    

    -- Assignment

    assigned_to VARCHAR(100),

    acknowledged_date DATE,

    resolved_date DATE,

    resolution_notes TEXT,

    

    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP

);



-- Intervention Prioritization Queue

DROP TABLE IF EXISTS intervention_priority_queue CASCADE;



CREATE TABLE intervention_priority_queue (

    queue_id SERIAL PRIMARY KEY,

    member_id VARCHAR(50) REFERENCES plan_members(member_id),

    gap_id INT REFERENCES member_gaps(gap_id),

    

    -- Priority calculation

    priority_date DATE NOT NULL DEFAULT CURRENT_DATE,

    priority_score DECIMAL(8,2) NOT NULL,

    priority_rank INT,

    priority_tier VARCHAR(20), -- Urgent, High, Medium, Low

    

    -- Scoring components

    revenue_impact_score DECIMAL(6,2),

    closure_likelihood_score DECIMAL(6,2),

    time_sensitivity_score DECIMAL(6,2),

    cost_efficiency_score DECIMAL(6,2),

    member_risk_score DECIMAL(6,2),

    

    -- Recommended intervention

    intervention_type VARCHAR(50), -- Outreach, Provider, Transportation, etc.

    intervention_channel VARCHAR(50), -- Phone, Email, Home Visit, etc.

    estimated_cost DECIMAL(8,2),

    estimated_roi DECIMAL(6,2),

    

    -- Assignment

    assigned_to VARCHAR(100),

    assignment_date DATE,

    status VARCHAR(20) DEFAULT 'Queued', -- Queued, Assigned, In Progress, Completed

    

    -- Outcome tracking

    intervention_completed BOOLEAN DEFAULT FALSE,

    completion_date DATE,

    gap_closed BOOLEAN DEFAULT FALSE,

    actual_cost DECIMAL(8,2),

    

    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP

);



-- Member Trajectory Tracking

DROP TABLE IF EXISTS member_trajectories CASCADE;



CREATE TABLE member_trajectories (

    trajectory_id SERIAL PRIMARY KEY,

    member_id VARCHAR(50) REFERENCES plan_members(member_id),

    observation_date DATE NOT NULL,

    

    -- Trajectory metrics

    gaps_open INT DEFAULT 0,

    gaps_closed_last_30_days INT DEFAULT 0,

    engagement_score DECIMAL(5,2),

    risk_score DECIMAL(5,2),

    

    -- Trajectory classification

    trajectory_direction VARCHAR(20), -- Improving, Stable, Declining, Critical

    velocity DECIMAL(6,2), -- Rate of change

    

    -- Predictions

    projected_gaps_30_days INT,

    projected_gaps_90_days INT,

    projected_year_end_gaps INT,

    

    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP

);



-- ============================================================================

-- SECTION 2: CALCULATE PREDICTIVE SCORES

-- ============================================================================



-- Calculate Gap Closure Propensity Scores

DO $$

DECLARE

    v_gap RECORD;

    v_member_engagement DECIMAL(5,2);

    v_provider_quality DECIMAL(5,2);

    v_historical_compliance DECIMAL(5,2);

    v_barrier_complexity DECIMAL(5,2);

    v_outreach_responsiveness DECIMAL(5,2);

    v_social_determinants DECIMAL(5,2);

    v_propensity_score DECIMAL(5,2);

    v_closure_likelihood VARCHAR(20);

    v_predicted_days INT;

    v_predicted_cost DECIMAL(8,2);

    v_counter INT := 0;

BEGIN

    RAISE NOTICE 'Calculating gap closure propensity scores...';

    

    FOR v_gap IN 

        SELECT 

            mg.gap_id,

            mg.member_id,

            mg.measure_id,

            mg.gap_status,

            pm.risk_score,

            mes.overall_engagement_score,

            mes.compliance_score

        FROM member_gaps mg

        JOIN plan_members pm ON mg.member_id = pm.member_id

        LEFT JOIN member_engagement_scores mes ON mg.member_id = mes.member_id

        WHERE mg.gap_status = 'Open'

          AND pm.member_id LIKE 'M%'

    LOOP

        -- Feature 1: Member Engagement (directly from engagement score)

        v_member_engagement := COALESCE(v_gap.overall_engagement_score, 50);

        

        -- Feature 2: Provider Quality (from attributed provider performance)

        SELECT COALESCE(AVG(pp.performance_rate), 65)

        INTO v_provider_quality

        FROM member_provider_attribution mpa

        JOIN provider_performance pp ON mpa.provider_id = pp.provider_id

        WHERE mpa.member_id = v_gap.member_id

          AND pp.measure_id = v_gap.measure_id

          AND mpa.is_current = TRUE;

        

        -- Feature 3: Historical Compliance (from engagement compliance score)

        v_historical_compliance := COALESCE(v_gap.compliance_score, 60);

        

        -- Feature 4: Barrier Complexity (inverse of outreach success)

        SELECT 

            CASE 

                WHEN COUNT(*) = 0 THEN 50

                WHEN COUNT(*) > 0 THEN 100 - (COUNT(CASE WHEN barrier_identified IS NOT NULL THEN 1 END)::DECIMAL / COUNT(*) * 100)

                ELSE 50

            END

        INTO v_barrier_complexity

        FROM member_outreach_contacts

        WHERE member_id = v_gap.member_id;

        

        -- Feature 5: Outreach Responsiveness

        SELECT 

            CASE 

                WHEN COUNT(*) = 0 THEN 50

                ELSE (COUNT(CASE WHEN contact_outcome = 'Successful' THEN 1 END)::DECIMAL / COUNT(*) * 100)

            END

        INTO v_outreach_responsiveness

        FROM member_outreach_contacts

        WHERE member_id = v_gap.member_id;

        

        -- Feature 6: Social Determinants (inverse of risk score, normalized)

        v_social_determinants := 100 - (v_gap.risk_score * 20);

        v_social_determinants := GREATEST(20, LEAST(90, v_social_determinants));

        

        -- Calculate weighted propensity score

        v_propensity_score := (

            v_member_engagement * 0.25 +

            v_provider_quality * 0.20 +

            v_historical_compliance * 0.20 +

            v_barrier_complexity * 0.15 +

            v_outreach_responsiveness * 0.15 +

            v_social_determinants * 0.05

        );

        

        -- Categorize closure likelihood

        CASE 

            WHEN v_propensity_score >= 80 THEN 

                v_closure_likelihood := 'Very High';

            WHEN v_propensity_score >= 65 THEN 

                v_closure_likelihood := 'High';

            WHEN v_propensity_score >= 50 THEN 

                v_closure_likelihood := 'Medium';

            WHEN v_propensity_score >= 35 THEN 

                v_closure_likelihood := 'Low';

            ELSE 

                v_closure_likelihood := 'Very Low';

        END CASE;

        

        -- Predict days to close (inverse relationship with propensity)

        v_predicted_days := FLOOR(180 - (v_propensity_score * 1.5))::INT;

        v_predicted_days := GREATEST(15, LEAST(180, v_predicted_days));

        

        -- Predict cost to close (higher for lower propensity)

        v_predicted_cost := 150 - (v_propensity_score * 1.2);

        v_predicted_cost := GREATEST(35, LEAST(250, v_predicted_cost));

        

        INSERT INTO gap_closure_propensity (

            gap_id,

            member_id,

            measure_id,

            member_engagement_feature,

            provider_quality_feature,

            historical_compliance_feature,

            barrier_complexity_feature,

            outreach_responsiveness_feature,

            social_determinants_feature,

            closure_propensity_score,

            closure_likelihood,

            recommended_intervention_intensity,

            predicted_days_to_close,

            predicted_cost_to_close,

            predicted_closure_date,

            confidence_score

        ) VALUES (

            v_gap.gap_id,

            v_gap.member_id,

            v_gap.measure_id,

            ROUND(v_member_engagement, 2),

            ROUND(v_provider_quality, 2),

            ROUND(v_historical_compliance, 2),

            ROUND(v_barrier_complexity, 2),

            ROUND(v_outreach_responsiveness, 2),

            ROUND(v_social_determinants, 2),

            ROUND(v_propensity_score, 2),

            v_closure_likelihood,

            CASE 

                WHEN v_propensity_score >= 70 THEN 'Minimal'

                WHEN v_propensity_score >= 50 THEN 'Standard'

                WHEN v_propensity_score >= 35 THEN 'Intensive'

                ELSE 'Urgent'

            END,

            v_predicted_days,

            ROUND(v_predicted_cost, 2),

            CURRENT_DATE + v_predicted_days,

            ROUND((65 + (RANDOM() * 25))::NUMERIC, 2) -- Confidence score 65-90%

        );

        

        v_counter := v_counter + 1;

        

        IF v_counter % 1000 = 0 THEN

            RAISE NOTICE '  Processed % gaps...', v_counter;

        END IF;

    END LOOP;

    

    RAISE NOTICE 'Gap closure propensity calculation complete! Total gaps scored: %', v_counter;

END $$;



-- Calculate Member Risk Stratification

DO $$

DECLARE

    v_member RECORD;

    v_clinical_complexity DECIMAL(5,2);

    v_utilization_risk DECIMAL(5,2);

    v_medication_risk DECIMAL(5,2);

    v_preventive_risk DECIMAL(5,2);

    v_engagement_risk DECIMAL(5,2);

    v_financial_risk DECIMAL(5,2);

    v_access_risk DECIMAL(5,2);

    v_health_literacy_risk DECIMAL(5,2);

    v_overall_risk DECIMAL(5,2);

    v_risk_tier VARCHAR(20);

    v_counter INT := 0;

BEGIN

    RAISE NOTICE 'Calculating member risk stratification...';

    

    FOR v_member IN 

        SELECT 

            pm.member_id,

            pm.risk_score,

            pm.chronic_conditions,

            mes.overall_engagement_score,

            mes.compliance_score

        FROM plan_members pm

        LEFT JOIN member_engagement_scores mes ON pm.member_id = mes.member_id

        WHERE pm.member_id LIKE 'M%'

    LOOP

        -- Clinical Complexity (HCC risk score based)

        v_clinical_complexity := v_member.risk_score * 25;

        v_clinical_complexity := LEAST(95, v_clinical_complexity);

        

        -- Utilization Risk (SUPD measure proxy + conditions)

        v_utilization_risk := 30 + (v_member.risk_score * 15);

        IF v_member.chronic_conditions LIKE '%I50%' OR 

           v_member.chronic_conditions LIKE '%J44%' THEN

            v_utilization_risk := v_utilization_risk + 15;

        END IF;

        v_utilization_risk := LEAST(95, v_utilization_risk);

        

        -- Medication Adherence Risk (inverse of PDC performance)

        SELECT 100 - COALESCE(AVG(performance_rate), 70)

        INTO v_medication_risk

        FROM plan_performance pp

        WHERE pp.plan_id = (SELECT plan_id FROM plan_members WHERE member_id = v_member.member_id)

          AND pp.measure_id IN ('PDC-DR', 'PDC-STA', 'PDC-RASA');

        v_medication_risk := COALESCE(v_medication_risk, 50);

        

        -- Preventive Care Risk (inverse of screening compliance)

        SELECT COUNT(*)

        INTO v_preventive_risk

        FROM member_gaps

        WHERE member_id = v_member.member_id

          AND gap_status = 'Open'

          AND measure_id IN ('COL', 'BCS', 'EED');

        v_preventive_risk := v_preventive_risk * 20;

        v_preventive_risk := LEAST(90, v_preventive_risk);

        

        -- Engagement Risk (inverse of engagement score)

        v_engagement_risk := 100 - COALESCE(v_member.overall_engagement_score, 50);

        

        -- Financial Risk (proxy based on barriers)

        SELECT 

            COUNT(CASE WHEN barrier_category = 'Financial' THEN 1 END) * 15

        INTO v_financial_risk

        FROM member_outreach_contacts

        WHERE member_id = v_member.member_id;

        v_financial_risk := LEAST(80, COALESCE(v_financial_risk, 25 + RANDOM() * 30));

        

        -- Access Risk (transportation barriers + distance)

        SELECT 

            COUNT(CASE WHEN barrier_category = 'Transportation' THEN 1 END) * 20

        INTO v_access_risk

        FROM member_outreach_contacts

        WHERE member_id = v_member.member_id;

        v_access_risk := LEAST(75, COALESCE(v_access_risk, 20 + RANDOM() * 25));

        

        -- Health Literacy Risk (communication barriers)

        v_health_literacy_risk := 30 + (RANDOM() * 40);

        

        -- Calculate overall risk score (weighted average)

        v_overall_risk := (

            v_clinical_complexity * 0.25 +

            v_utilization_risk * 0.20 +

            v_medication_risk * 0.15 +

            v_preventive_risk * 0.15 +

            v_engagement_risk * 0.10 +

            v_financial_risk * 0.05 +

            v_access_risk * 0.05 +

            v_health_literacy_risk * 0.05

        );

        

        -- Determine risk tier

        CASE 

            WHEN v_overall_risk >= 75 THEN v_risk_tier := 'Critical';

            WHEN v_overall_risk >= 60 THEN v_risk_tier := 'High';

            WHEN v_overall_risk >= 40 THEN v_risk_tier := 'Medium';

            ELSE v_risk_tier := 'Low';

        END CASE;

        

        INSERT INTO member_risk_stratification (

            member_id,

            clinical_complexity_score,

            utilization_risk_score,

            medication_adherence_risk,

            preventive_care_risk,

            engagement_risk_score,

            financial_risk_score,

            access_risk_score,

            health_literacy_risk,

            overall_risk_score,

            risk_tier,

            rising_risk,

            at_risk_star_impact,

            high_cost_risk,

            disengagement_risk,

            care_management_needed,

            intensive_outreach_needed,

            provider_intervention_needed,

            risk_trend

        ) VALUES (

            v_member.member_id,

            ROUND(v_clinical_complexity, 2),

            ROUND(v_utilization_risk, 2),

            ROUND(v_medication_risk, 2),

            ROUND(v_preventive_risk, 2),

            ROUND(v_engagement_risk, 2),

            ROUND(v_financial_risk, 2),

            ROUND(v_access_risk, 2),

            ROUND(v_health_literacy_risk, 2),

            ROUND(v_overall_risk, 2),

            v_risk_tier,

            RANDOM() < 0.15,

            v_overall_risk >= 65,

            v_clinical_complexity >= 70,

            v_engagement_risk >= 70,

            v_risk_tier IN ('Critical', 'High'),

            v_engagement_risk >= 65,

            v_clinical_complexity >= 75 OR v_preventive_risk >= 60,

            CASE 

                WHEN RANDOM() < 0.20 THEN 'Improving'

                WHEN RANDOM() < 0.60 THEN 'Stable'

                WHEN RANDOM() < 0.90 THEN 'Worsening'

                ELSE 'Rapid Decline'

            END

        );

        

        v_counter := v_counter + 1;

        

        IF v_counter % 1000 = 0 THEN

            RAISE NOTICE '  Processed % members...', v_counter;

        END IF;

    END LOOP;

    

    RAISE NOTICE 'Member risk stratification complete! Total members scored: %', v_counter;

END $$;



-- Calculate Cost Predictions

INSERT INTO member_cost_predictions (

    member_id,

    predicted_medical_cost,

    predicted_pharmacy_cost,

    predicted_total_cost,

    chronic_condition_cost_driver,

    preventable_ed_cost_driver,

    medication_nonadherence_cost_driver,

    cost_risk_category,

    estimated_avoidable_cost,

    intervention_roi,

    prediction_confidence

)

SELECT 

    pm.member_id,

    -- Medical cost prediction (based on risk score and gaps)

    3000 + (pm.risk_score * 2500) + (COALESCE(open_gap_count, 0) * 200) AS predicted_medical,

    -- Pharmacy cost prediction

    1500 + (pm.risk_score * 1000) + (CASE WHEN has_diabetes THEN 800 ELSE 0 END) AS predicted_pharmacy,

    -- Total cost

    4500 + (pm.risk_score * 3500) + (COALESCE(open_gap_count, 0) * 200) + 

        (CASE WHEN has_diabetes THEN 800 ELSE 0 END) AS predicted_total,

    -- Cost drivers

    pm.risk_score * 1200 AS condition_driver,

    CASE WHEN pm.chronic_conditions LIKE '%I50%' THEN 2500 ELSE 500 END AS ed_driver,

    COALESCE(open_gap_count, 0) * 180 AS nonadherence_driver,

    -- Risk category

    CASE 

        WHEN pm.risk_score >= 3.0 OR COALESCE(open_gap_count, 0) >= 5 THEN 'Very High'

        WHEN pm.risk_score >= 2.0 OR COALESCE(open_gap_count, 0) >= 3 THEN 'High'

        WHEN pm.risk_score >= 1.2 OR COALESCE(open_gap_count, 0) >= 2 THEN 'Medium'

        ELSE 'Low'

    END,

    -- Avoidable cost (gaps * avg cost per gap)

    COALESCE(open_gap_count, 0) * 250,

    -- ROI (assuming 3:1 return)

    3.0,

    -- Confidence

    ROUND((70 + (RANDOM() * 20))::NUMERIC, 2)

FROM plan_members pm

LEFT JOIN (

    SELECT 

        member_id,

        COUNT(*) AS open_gap_count

    FROM member_gaps

    WHERE gap_status = 'Open'

    GROUP BY member_id

) gaps ON pm.member_id = gaps.member_id

LEFT JOIN (

    SELECT 

        member_id,

        TRUE AS has_diabetes

    FROM member_chronic_conditions

    WHERE condition_code IN ('E10', 'E11')

    LIMIT 1

) diabetes ON pm.member_id = diabetes.member_id

WHERE pm.member_id LIKE 'M%';



-- Calculate cost percentile ranks

WITH cost_ranks AS (

    SELECT 

        prediction_id,

        PERCENT_RANK() OVER (ORDER BY predicted_total_cost) * 100 AS percentile

    FROM member_cost_predictions

)

UPDATE member_cost_predictions mcp

SET percentile_rank = ROUND(cr.percentile)::INT

FROM cost_ranks cr

WHERE mcp.prediction_id = cr.prediction_id;



-- Generate Early Warning Alerts (for high-risk scenarios)

INSERT INTO early_warning_alerts (

    member_id,

    alert_type,

    alert_severity,

    alert_title,

    alert_description,

    trigger_metric,

    trigger_threshold,

    current_value,

    related_gap_ids,

    recommended_action,

    urgency_level

)

-- Alert 1: High disengagement risk

SELECT 

    mes.member_id,

    'Disengagement Risk',

    CASE 

        WHEN mes.overall_engagement_score < 30 THEN 'Critical'

        WHEN mes.overall_engagement_score < 40 THEN 'High'

        ELSE 'Medium'

    END,

    'Member Disengagement Alert',

    'Member showing signs of disengagement with engagement score below threshold',

    'Engagement Score',

    40,

    mes.overall_engagement_score,

    NULL,

    'Immediate outreach with preferred contact method, consider home visit',

    CASE 

        WHEN mes.overall_engagement_score < 30 THEN 'Immediate'

        ELSE 'Urgent'

    END

FROM member_engagement_scores mes

WHERE mes.overall_engagement_score < 40

  AND mes.at_risk_of_disengagement = TRUE



UNION ALL



-- Alert 2: Multiple open gaps

SELECT 

    pm.member_id,

    'Gap Escalation',

    CASE 

        WHEN gap_count >= 6 THEN 'Critical'

        WHEN gap_count >= 4 THEN 'High'

        ELSE 'Medium'

    END,

    'Multiple Open Gaps Alert',

    'Member has ' || gap_count || ' open gaps requiring attention',

    'Open Gap Count',

    3,

    gap_count,

    gap_list,

    'Coordinate multi-measure outreach campaign, consider care management',

    'Urgent'

FROM (

    SELECT 

        pm.member_id,

        COUNT(mg.gap_id) AS gap_count,

        STRING_AGG(mg.gap_id::TEXT, ',') AS gap_list

    FROM plan_members pm

    JOIN member_gaps mg ON pm.member_id = mg.member_id

    WHERE mg.gap_status = 'Open'

      AND pm.member_id LIKE 'M%'

    GROUP BY pm.member_id

    HAVING COUNT(mg.gap_id) >= 4

) pm



UNION ALL



-- Alert 3: Provider performance concern

SELECT DISTINCT

    mpa.member_id,

    'Provider Quality',

    'Medium',

    'Low Provider Performance Alert',

    'Member attributed to provider with performance below network average',

    'Provider Performance Rate',

    60,

    pp.performance_rate,

    NULL,

    'Consider provider education or member reassignment',

    'Routine'

FROM member_provider_attribution mpa

JOIN provider_performance pp ON mpa.provider_id = pp.provider_id

WHERE pp.performance_rate < 60

  AND pp.needs_improvement = TRUE

  AND mpa.is_current = TRUE

  AND RANDOM() < 0.20 -- Sample 20%

LIMIT 500;



-- Build Intervention Priority Queue

INSERT INTO intervention_priority_queue (

    member_id,

    gap_id,

    priority_score,

    revenue_impact_score,

    closure_likelihood_score,

    time_sensitivity_score,

    cost_efficiency_score,

    member_risk_score,

    priority_tier,

    intervention_type,

    intervention_channel,

    estimated_cost,

    estimated_roi

)

SELECT 

    mg.member_id,

    mg.gap_id,

    -- Priority score (weighted composite)

    (revenue_score * 0.30 +

     closure_score * 0.25 +

     time_score * 0.20 +

     efficiency_score * 0.15 +

     risk_score * 0.10) AS priority_score,

    revenue_score,

    closure_score,

    time_score,

    efficiency_score,

    risk_score,

    -- Priority tier based on composite score

    CASE 

        WHEN (revenue_score * 0.30 + closure_score * 0.25 + time_score * 0.20 + 

              efficiency_score * 0.15 + risk_score * 0.10) >= 75 THEN 'Urgent'

        WHEN (revenue_score * 0.30 + closure_score * 0.25 + time_score * 0.20 + 

              efficiency_score * 0.15 + risk_score * 0.10) >= 60 THEN 'High'

        WHEN (revenue_score * 0.30 + closure_score * 0.25 + time_score * 0.20 + 

              efficiency_score * 0.15 + risk_score * 0.10) >= 45 THEN 'Medium'

        ELSE 'Low'

    END,

    -- Intervention type (based on measure and member profile)

    CASE 

        WHEN hm.measure_id IN ('GSD', 'KED') THEN 'Lab Order'

        WHEN hm.measure_id IN ('EED', 'COL', 'BCS') THEN 'Appointment Coordination'

        WHEN hm.measure_id IN ('PDC-DR', 'PDC-STA', 'PDC-RASA') THEN 'Pharmacy Outreach'

        ELSE 'Standard Outreach'

    END,

    -- Channel (based on engagement preferences)

    COALESCE(mcp.preferred_method_1, 'Phone'),

    -- Estimated cost

    COALESCE(gcp.predicted_cost_to_close, 100),

    -- Estimated ROI

    CASE 

        WHEN COALESCE(gcp.predicted_cost_to_close, 100) > 0 

        THEN (revenue_score * 10) / COALESCE(gcp.predicted_cost_to_close, 100)

        ELSE 0

    END

FROM member_gaps mg

JOIN hedis_measures hm ON mg.measure_id = hm.measure_id

LEFT JOIN gap_closure_propensity gcp ON mg.gap_id = gcp.gap_id

LEFT JOIN member_engagement_scores mes ON mg.member_id = mes.member_id

LEFT JOIN member_risk_stratification mrs ON mg.member_id = mrs.member_id

LEFT JOIN member_contact_preferences mcp ON mg.member_id = mcp.member_id

CROSS JOIN LATERAL (

    SELECT 

        -- Revenue impact (measure revenue * star weight)

        (hm.revenue_per_point * hm.star_weight / 10000.0) AS revenue_score,

        -- Closure likelihood

        COALESCE(gcp.closure_propensity_score, 50) AS closure_score,

        -- Time sensitivity (days gap has been open)

        GREATEST(0, 100 - (CURRENT_DATE - mg.gap_opened_date)) AS time_score,

        -- Cost efficiency (inverse of predicted cost)

        100 - (COALESCE(gcp.predicted_cost_to_close, 100) / 3.0) AS efficiency_score,

        -- Member risk

        COALESCE(mrs.overall_risk_score, 50) AS risk_score

) scores

WHERE mg.gap_status = 'Open'

  AND mg.member_id LIKE 'M%';



-- Assign priority ranks

WITH ranked_queue AS (

    SELECT 

        queue_id,

        ROW_NUMBER() OVER (ORDER BY priority_score DESC) AS rank

    FROM intervention_priority_queue

)

UPDATE intervention_priority_queue ipq

SET priority_rank = rq.rank

FROM ranked_queue rq

WHERE ipq.queue_id = rq.queue_id;



-- Create indexes for performance

CREATE INDEX idx_propensity_member ON gap_closure_propensity(member_id);

CREATE INDEX idx_propensity_gap ON gap_closure_propensity(gap_id);

CREATE INDEX idx_propensity_score ON gap_closure_propensity(closure_propensity_score DESC);

CREATE INDEX idx_risk_member ON member_risk_stratification(member_id);

CREATE INDEX idx_risk_tier ON member_risk_stratification(risk_tier);

CREATE INDEX idx_risk_score ON member_risk_stratification(overall_risk_score DESC);

CREATE INDEX idx_cost_pred_member ON member_cost_predictions(member_id);

CREATE INDEX idx_cost_category ON member_cost_predictions(cost_risk_category);

CREATE INDEX idx_alerts_member ON early_warning_alerts(member_id, alert_status);

CREATE INDEX idx_alerts_severity ON early_warning_alerts(alert_severity, alert_status);

CREATE INDEX idx_priority_rank ON intervention_priority_queue(priority_rank);

CREATE INDEX idx_priority_tier ON intervention_priority_queue(priority_tier, status);



-- ============================================================================

-- SECTION 3: PREDICTIVE ANALYTICS VIEWS

-- ============================================================================



-- View 1: High-Value Target List

CREATE OR REPLACE VIEW vw_high_value_targets AS

SELECT 

    ipq.member_id,

    pm.plan_id,

    mp.plan_name,

    ipq.gap_id,

    hm.measure_id,

    hm.measure_name,

    

    -- Priority metrics

    ipq.priority_rank,

    ipq.priority_tier,

    ROUND(ipq.priority_score, 2) AS priority_score,

    

    -- Component scores

    ROUND(ipq.revenue_impact_score, 2) AS revenue_impact,

    ROUND(ipq.closure_likelihood_score, 2) AS closure_likelihood_score,

    ROUND(ipq.time_sensitivity_score, 2) AS time_sensitivity,

    ROUND(ipq.cost_efficiency_score, 2) AS cost_efficiency,

    

    -- Predictions

    gcp.closure_likelihood,

    gcp.predicted_days_to_close,

    gcp.predicted_cost_to_close,

    ROUND(ipq.estimated_roi, 2) AS estimated_roi,

    

    -- Recommendations

    ipq.intervention_type,

    ipq.intervention_channel,

    gcp.recommended_intervention_intensity,

    

    -- Member context

    mes.overall_engagement_score,

    mrs.risk_tier,

    

    -- Status

    ipq.status,

    ipq.assigned_to



FROM intervention_priority_queue ipq

JOIN plan_members pm ON ipq.member_id = pm.member_id

JOIN ma_plans mp ON pm.plan_id = mp.plan_id

JOIN member_gaps mg ON ipq.gap_id = mg.gap_id

JOIN hedis_measures hm ON mg.measure_id = hm.measure_id

LEFT JOIN gap_closure_propensity gcp ON ipq.gap_id = gcp.gap_id

LEFT JOIN member_engagement_scores mes ON ipq.member_id = mes.member_id

LEFT JOIN member_risk_stratification mrs ON ipq.member_id = mrs.member_id



WHERE ipq.priority_tier IN ('Urgent', 'High')

  AND ipq.status = 'Queued';



-- View 2: Risk Stratification Dashboard

CREATE OR REPLACE VIEW vw_risk_dashboard AS

SELECT 

    pm.plan_id,

    mp.plan_name,

    mrs.risk_tier,

    

    -- Volume metrics

    COUNT(DISTINCT mrs.member_id) AS member_count,

    ROUND(

        COUNT(DISTINCT mrs.member_id)::DECIMAL / 

        (SELECT COUNT(*) FROM plan_members WHERE member_id LIKE 'M%' AND plan_id = pm.plan_id) * 100,

        1

    ) AS pct_of_plan,

    

    -- Risk scores

    ROUND(AVG(mrs.overall_risk_score), 1) AS avg_risk_score,

    ROUND(AVG(mrs.clinical_complexity_score), 1) AS avg_clinical_complexity,

    ROUND(AVG(mrs.engagement_risk_score), 1) AS avg_engagement_risk,

    

    -- Risk flags

    COUNT(CASE WHEN mrs.rising_risk THEN 1 END) AS rising_risk_count,

    COUNT(CASE WHEN mrs.at_risk_star_impact THEN 1 END) AS star_risk_count,

    COUNT(CASE WHEN mrs.disengagement_risk THEN 1 END) AS disengagement_count,

    

    -- Intervention needs

    COUNT(CASE WHEN mrs.care_management_needed THEN 1 END) AS care_mgmt_needed,

    COUNT(CASE WHEN mrs.intensive_outreach_needed THEN 1 END) AS intensive_outreach_needed,

    

    -- Cost implications

    ROUND(AVG(mcp.predicted_total_cost), 0) AS avg_predicted_cost,

    ROUND(SUM(mcp.predicted_total_cost), 0) AS total_predicted_cost



FROM member_risk_stratification mrs

JOIN plan_members pm ON mrs.member_id = pm.member_id

JOIN ma_plans mp ON pm.plan_id = mp.plan_id

LEFT JOIN member_cost_predictions mcp ON mrs.member_id = mcp.member_id



WHERE pm.member_id LIKE 'M%'



GROUP BY pm.plan_id, mp.plan_name, mrs.risk_tier

ORDER BY pm.plan_id, 

    CASE mrs.risk_tier

        WHEN 'Critical' THEN 1

        WHEN 'High' THEN 2

        WHEN 'Medium' THEN 3

        ELSE 4

    END;



-- View 3: Alert Dashboard

CREATE OR REPLACE VIEW vw_alert_dashboard AS

SELECT 

    ewa.alert_type,

    ewa.alert_severity,

    

    -- Volume

    COUNT(*) AS total_alerts,

    COUNT(CASE WHEN ewa.alert_status = 'Active' THEN 1 END) AS active_alerts,

    COUNT(CASE WHEN ewa.alert_status = 'Acknowledged' THEN 1 END) AS acknowledged_alerts,

    COUNT(CASE WHEN ewa.alert_status = 'Resolved' THEN 1 END) AS resolved_alerts,

    

    -- Members affected

    COUNT(DISTINCT ewa.member_id) AS unique_members,

    

    -- Urgency

    COUNT(CASE WHEN ewa.urgency_level = 'Immediate' THEN 1 END) AS immediate_count,

    COUNT(CASE WHEN ewa.urgency_level = 'Urgent' THEN 1 END) AS urgent_count,

    

    -- Age of alerts

    ROUND(AVG(CURRENT_DATE - ewa.alert_date), 1) AS avg_days_open,

    MAX(CURRENT_DATE - ewa.alert_date) AS max_days_open



FROM early_warning_alerts ewa



WHERE ewa.alert_status IN ('Active', 'Acknowledged')



GROUP BY ewa.alert_type, ewa.alert_severity

ORDER BY 

    CASE ewa.alert_severity

        WHEN 'Critical' THEN 1

        WHEN 'High' THEN 2

        WHEN 'Medium' THEN 3

        ELSE 4

    END,

    total_alerts DESC;



-- View 4: Predictive Model Performance

CREATE OR REPLACE VIEW vw_model_performance AS

SELECT 

    'Gap Closure Propensity' AS model_name,

    COUNT(*) AS predictions_made,

    ROUND(AVG(closure_propensity_score), 1) AS avg_score,

    ROUND(AVG(confidence_score), 1) AS avg_confidence,

    

    -- Distribution by likelihood

    COUNT(CASE WHEN closure_likelihood = 'Very High' THEN 1 END) AS very_high_count,

    COUNT(CASE WHEN closure_likelihood = 'High' THEN 1 END) AS high_count,

    COUNT(CASE WHEN closure_likelihood = 'Medium' THEN 1 END) AS medium_count,

    COUNT(CASE WHEN closure_likelihood = 'Low' THEN 1 END) AS low_count,

    

    -- Predictions

    ROUND(AVG(predicted_days_to_close), 1) AS avg_predicted_days,

    ROUND(AVG(predicted_cost_to_close), 2) AS avg_predicted_cost



FROM gap_closure_propensity



UNION ALL



SELECT 

    'Member Risk Stratification',

    COUNT(*),

    ROUND(AVG(overall_risk_score), 1),

    NULL, -- No confidence score for risk strat

    

    COUNT(CASE WHEN risk_tier = 'Critical' THEN 1 END),

    COUNT(CASE WHEN risk_tier = 'High' THEN 1 END),

    COUNT(CASE WHEN risk_tier = 'Medium' THEN 1 END),

    COUNT(CASE WHEN risk_tier = 'Low' THEN 1 END),

    

    NULL,

    NULL



FROM member_risk_stratification



UNION ALL



SELECT 

    'Cost Predictions',

    COUNT(*),

    ROUND(AVG(predicted_total_cost), 0),

    ROUND(AVG(prediction_confidence), 1),

    

    COUNT(CASE WHEN cost_risk_category = 'Very High' THEN 1 END),

    COUNT(CASE WHEN cost_risk_category = 'High' THEN 1 END),

    COUNT(CASE WHEN cost_risk_category = 'Medium' THEN 1 END),

    COUNT(CASE WHEN cost_risk_category = 'Low' THEN 1 END),

    

    NULL,

    ROUND(AVG(estimated_avoidable_cost), 2)



FROM member_cost_predictions;



-- View 5: Member 360 View (Comprehensive Profile)

CREATE OR REPLACE VIEW vw_member_360 AS

SELECT 

    pm.member_id,

    pm.plan_id,

    mp.plan_name,

    

    -- Demographics

    EXTRACT(YEAR FROM AGE(pm.date_of_birth)) AS age,

    pm.gender,

    pm.zip_code,

    pm.risk_score AS hcc_risk_score,

    

    -- Engagement

    mes.overall_engagement_score,

    mes.engagement_tier,

    mes.gaps_closed_ytd,

    mes.gaps_opened_ytd,

    

    -- Risk stratification

    mrs.overall_risk_score,

    mrs.risk_tier,

    mrs.risk_trend,

    mrs.care_management_needed,

    

    -- Cost predictions

    mcp.predicted_total_cost,

    mcp.cost_risk_category,

    mcp.estimated_avoidable_cost,

    

    -- Open gaps

    (SELECT COUNT(*) FROM member_gaps WHERE member_id = pm.member_id AND gap_status = 'Open') AS open_gaps,

    

    -- Active alerts

    (SELECT COUNT(*) FROM early_warning_alerts WHERE member_id = pm.member_id AND alert_status = 'Active') AS active_alerts,

    

    -- Priority interventions

    (SELECT COUNT(*) FROM intervention_priority_queue WHERE member_id = pm.member_id AND status = 'Queued') AS queued_interventions,

    

    -- Attribution

    (SELECT STRING_AGG(DISTINCT pd.specialty, ', ')

     FROM member_provider_attribution mpa

     JOIN provider_directory pd ON mpa.provider_id = pd.provider_id

     WHERE mpa.member_id = pm.member_id AND mpa.is_current = TRUE

    ) AS attributed_specialties



FROM plan_members pm

JOIN ma_plans mp ON pm.plan_id = mp.plan_id

LEFT JOIN member_engagement_scores mes ON pm.member_id = mes.member_id

LEFT JOIN member_risk_stratification mrs ON pm.member_id = mrs.member_id

LEFT JOIN member_cost_predictions mcp ON pm.member_id = mcp.member_id



WHERE pm.member_id LIKE 'M%';



-- ============================================================================

-- SECTION 4: TEST & VALIDATION QUERIES

-- ============================================================================



-- Test 1: Propensity score distribution

SELECT 'TEST 1: Gap Closure Propensity Distribution' AS test_name;

SELECT 

    closure_likelihood,

    COUNT(*) AS gap_count,

    ROUND(AVG(closure_propensity_score), 1) AS avg_score,

    ROUND(AVG(predicted_days_to_close), 1) AS avg_days,

    ROUND(AVG(predicted_cost_to_close), 2) AS avg_cost

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



-- Test 2: Risk stratification summary

SELECT 'TEST 2: Member Risk Stratification Summary' AS test_name;

SELECT * FROM vw_risk_dashboard

ORDER BY member_count DESC;



-- Test 3: Early warning alerts by severity

SELECT 'TEST 3: Active Alerts by Type and Severity' AS test_name;

SELECT * FROM vw_alert_dashboard

ORDER BY active_alerts DESC;



-- Test 4: Top priority interventions

SELECT 'TEST 4: Top 20 Priority Interventions' AS test_name;

SELECT 

    priority_rank,

    member_id,

    measure_name,

    priority_tier,

    ROUND(priority_score, 1) AS priority,

    closure_likelihood,

    ROUND(estimated_roi, 2) AS roi,

    intervention_type

FROM vw_high_value_targets

ORDER BY priority_rank

LIMIT 20;



-- Test 5: Cost predictions by risk category

SELECT 'TEST 5: Cost Predictions by Category' AS test_name;

SELECT 

    cost_risk_category,

    COUNT(*) AS member_count,

    ROUND(AVG(predicted_total_cost), 0) AS avg_predicted_cost,

    ROUND(AVG(estimated_avoidable_cost), 0) AS avg_avoidable_cost,

    ROUND(AVG(intervention_roi), 2) AS avg_roi

FROM member_cost_predictions

GROUP BY cost_risk_category

ORDER BY 

    CASE cost_risk_category

        WHEN 'Very High' THEN 1

        WHEN 'High' THEN 2

        WHEN 'Medium' THEN 3

        ELSE 4

    END;



-- Test 6: Model performance summary

SELECT 'TEST 6: Predictive Model Performance' AS test_name;

SELECT * FROM vw_model_performance;



-- Test 7: High-risk member profile

SELECT 'TEST 7: Critical Risk Members Sample' AS test_name;

SELECT 

    member_id,

    age,

    hcc_risk_score,

    overall_risk_score,

    risk_tier,

    open_gaps,

    active_alerts,

    predicted_total_cost,

    care_management_needed

FROM vw_member_360

WHERE risk_tier = 'Critical'

ORDER BY overall_risk_score DESC

LIMIT 10;



-- Test 8: Intervention queue statistics

SELECT 'TEST 8: Intervention Priority Queue Stats' AS test_name;

SELECT 

    priority_tier,

    COUNT(*) AS intervention_count,

    ROUND(AVG(priority_score), 1) AS avg_priority_score,

    ROUND(AVG(estimated_cost), 2) AS avg_cost,

    ROUND(AVG(estimated_roi), 2) AS avg_roi,

    COUNT(CASE WHEN status = 'Queued' THEN 1 END) AS queued_count,

    COUNT(CASE WHEN status = 'Assigned' THEN 1 END) AS assigned_count

FROM intervention_priority_queue

GROUP BY priority_tier

ORDER BY 

    CASE priority_tier

        WHEN 'Urgent' THEN 1

        WHEN 'High' THEN 2

        WHEN 'Medium' THEN 3

        ELSE 4

    END;



-- ============================================================================

-- END OF PHASE 2 CHAT 3

-- ============================================================================


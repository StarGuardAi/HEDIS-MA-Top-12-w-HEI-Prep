-- ============================================================================
-- CREATE PLAN_CONTEXT TABLE
-- Provides consistent narrative context for "MA plan in trouble" story
-- ============================================================================

-- Drop table if exists (for re-running)
DROP TABLE IF EXISTS plan_context CASCADE;

-- Create plan_context table
CREATE TABLE plan_context (
    context_id SERIAL PRIMARY KEY,
    plan_name VARCHAR(200) NOT NULL DEFAULT 'Mid-Atlantic Medicare Advantage',
    total_members INT NOT NULL DEFAULT 10000,
    active_members INT NOT NULL DEFAULT 10000,
    star_rating_2023 DECIMAL(2,1) NOT NULL DEFAULT 4.0 CHECK (star_rating_2023 >= 1.0 AND star_rating_2023 <= 5.0),
    star_rating_2024 DECIMAL(2,1) NOT NULL DEFAULT 4.0 CHECK (star_rating_2024 >= 1.0 AND star_rating_2024 <= 5.0),
    star_rating_projected_2025 DECIMAL(2,1) NOT NULL DEFAULT 4.5 CHECK (star_rating_projected_2025 >= 1.0 AND star_rating_projected_2025 <= 5.0),
    bonus_revenue_at_risk DECIMAL(12,2) NOT NULL DEFAULT 2500000.00,
    geographic_region VARCHAR(100) NOT NULL DEFAULT 'Pittsburgh Metro Area',
    plan_type VARCHAR(100) NOT NULL DEFAULT 'Regional Medicare Advantage',
    year_established INT NOT NULL DEFAULT 2015,
    member_growth_yoy DECIMAL(5,2) NOT NULL DEFAULT -5.2,
    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(plan_name)
);

-- Create index for quick lookups
CREATE INDEX idx_plan_context_name ON plan_context(plan_name);

-- Insert default plan context
INSERT INTO plan_context (
    plan_name,
    total_members,
    active_members,
    star_rating_2023,
    star_rating_2024,
    star_rating_projected_2025,
    bonus_revenue_at_risk,
    geographic_region,
    plan_type,
    year_established,
    member_growth_yoy
) VALUES (
    'Mid-Atlantic Medicare Advantage',
    10000,
    10000,
    4.0,
    4.0,
    4.5,
    2500000.00,
    'Pittsburgh Metro Area',
    'Regional Medicare Advantage',
    2015,
    -5.2
);

-- Grant permissions
GRANT ALL ON plan_context TO hedis_api;
GRANT USAGE, SELECT ON SEQUENCE plan_context_context_id_seq TO hedis_api;

-- Display success message
SELECT 
    'Plan context table created successfully!' as message,
    plan_name,
    total_members,
    active_members,
    star_rating_2023,
    star_rating_2024,
    star_rating_projected_2025,
    bonus_revenue_at_risk,
    geographic_region
FROM plan_context;



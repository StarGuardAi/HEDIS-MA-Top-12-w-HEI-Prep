-- HEDIS Star Rating Portfolio Optimizer - Database Initialization
-- PostgreSQL Database Setup Script
--
-- This script creates the database, user, and required extensions.
-- Run this as postgres superuser before running Alembic migrations.
--
-- Usage:
--   psql -U postgres -f scripts/init_database.sql
--
-- Author: Robert Reichert
-- Date: October 2025

-- Create database (if not exists)
SELECT 'CREATE DATABASE hedis_portfolio'
WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'hedis_portfolio')\gexec

-- Connect to the database
\c hedis_portfolio

-- Create user (if not exists)
DO
$$
BEGIN
  IF NOT EXISTS (SELECT FROM pg_user WHERE usename = 'hedis_api') THEN
    CREATE USER hedis_api WITH PASSWORD 'hedis_password';
  END IF;
END
$$;

-- Grant privileges
GRANT ALL PRIVILEGES ON DATABASE hedis_portfolio TO hedis_api;
GRANT ALL ON SCHEMA public TO hedis_api;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON TABLES TO hedis_api;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON SEQUENCES TO hedis_api;

-- Create required extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";  -- For UUID generation
CREATE EXTENSION IF NOT EXISTS "pgcrypto";    -- For cryptographic functions

-- Create schemas if needed (currently using public)
-- CREATE SCHEMA IF NOT EXISTS hedis AUTHORIZATION hedis_api;

-- Display success message
SELECT 
    'Database initialization complete!' as message,
    current_database() as database,
    current_user as current_user,
    version() as postgresql_version;

-- Display installed extensions
SELECT 
    extname as extension_name,
    extversion as version
FROM pg_extension
WHERE extname IN ('uuid-ossp', 'pgcrypto');



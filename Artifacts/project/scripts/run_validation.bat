@echo off
REM 10K Dataset Validation Suite Runner (Windows)
REM Executes comprehensive validation tests

echo ================================================================================
echo HEDIS STAR RATING PORTFOLIO OPTIMIZER
echo 10K Dataset Validation Suite
echo ================================================================================
echo.

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python not found. Please install Python 3.8+ and add to PATH.
    pause
    exit /b 1
)

REM Check if psycopg2 is installed
python -c "import psycopg2" >nul 2>&1
if errorlevel 1 (
    echo Installing psycopg2-binary...
    pip install psycopg2-binary
    if errorlevel 1 (
        echo ERROR: Failed to install psycopg2-binary
        pause
        exit /b 1
    )
)

REM Set default database configuration
if "%DB_HOST%"=="" set DB_HOST=localhost
if "%DB_NAME%"=="" set DB_NAME=hedis_portfolio
if "%DB_USER%"=="" set DB_USER=hedis_api
if "%DB_PASSWORD%"=="" set DB_PASSWORD=hedis_password
if "%DB_PORT%"=="" set DB_PORT=5432

echo Database Configuration:
echo   Host: %DB_HOST%
echo   Database: %DB_NAME%
echo   User: %DB_USER%
echo   Port: %DB_PORT%
echo.
echo NOTE: Phase 1 Chat 4 must be completed first (10K members)!
echo.
echo This will take 2-3 minutes to complete...
echo.

REM Run the Python script
python "%~dp0run_validation.py"

if errorlevel 1 (
    echo.
    echo ERROR: Validation failed. Check error messages above.
    echo Make sure Phase 1 Chat 4 has been completed.
    pause
    exit /b 1
) else (
    echo.
    echo Validation completed successfully!
    echo Review validation_report.txt for detailed results.
)

pause


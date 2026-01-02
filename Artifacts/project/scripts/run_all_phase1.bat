@echo off
REM Phase 1 Complete Setup Runner (Windows)
REM Executes all Phase 1 scripts in sequence (Chats 1-4)

echo ================================================================================
echo HEDIS STAR RATING PORTFOLIO OPTIMIZER
echo Phase 1 Complete Setup - All Scripts (1-4)
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
echo WARNING: This will take approximately 15-20 minutes to complete!
echo.
echo Scripts to run:
echo   1. Phase 1 Chat 1: Foundation (~30 seconds)
echo   2. Phase 1 Chat 2: Velocity Tracking (~3 minutes)
echo   3. Phase 1 Chat 3: ROI Analysis (~3 minutes)
echo   4. Phase 1 Chat 4: 10K Scale Enhancement (~7 minutes)
echo.
pause

REM Run the Python script
python "%~dp0run_all_phase1.py"

if errorlevel 1 (
    echo.
    echo ERROR: Setup failed. Check error messages above.
    pause
    exit /b 1
) else (
    echo.
    echo Phase 1 setup completed successfully!
    echo.
    echo Next: Run validation suite with: run_validation.bat
)

pause


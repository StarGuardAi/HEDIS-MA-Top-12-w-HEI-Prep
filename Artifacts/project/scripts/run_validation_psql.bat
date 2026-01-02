@echo off
REM Batch script to run full system validation via psql
REM Usage: run_validation_psql.bat

setlocal

REM Database configuration
if "%DB_HOST%"=="" set DB_HOST=localhost
if "%DB_NAME%"=="" set DB_NAME=hedis_portfolio
if "%DB_USER%"=="" set DB_USER=hedis_api
if "%DB_PASSWORD%"=="" set DB_PASSWORD=hedis_password
if "%DB_PORT%"=="" set DB_PORT=5432

REM Paths
set SCRIPT_DIR=%~dp0
set VALIDATION_SCRIPT=%SCRIPT_DIR%validate_full_system.sql
set OUTPUT_FILE=%SCRIPT_DIR%validation_report.txt

echo ================================================================================
echo HEDIS STAR RATING PORTFOLIO OPTIMIZER
echo FULL SYSTEM VALIDATION SUITE
echo ================================================================================
echo.

if not exist "%VALIDATION_SCRIPT%" (
    echo [ERROR] Validation script not found: %VALIDATION_SCRIPT%
    exit /b 1
)

echo [INFO] Running validation via psql...
echo [INFO] Output will be saved to: %OUTPUT_FILE%
echo.

REM Set PGPASSWORD environment variable
set PGPASSWORD=%DB_PASSWORD%

REM Run psql with the validation script
psql -h %DB_HOST% -p %DB_PORT% -U %DB_USER% -d %DB_NAME% -f "%VALIDATION_SCRIPT%" > "%OUTPUT_FILE%" 2>&1

if %ERRORLEVEL% EQU 0 (
    echo.
    echo [OK] Validation complete! Report saved to: %OUTPUT_FILE%
    type "%OUTPUT_FILE%"
) else (
    echo [ERROR] Validation failed. Check %OUTPUT_FILE% for details.
    type "%OUTPUT_FILE%"
    exit /b 1
)

REM Clear password from environment
set PGPASSWORD=

endlocal


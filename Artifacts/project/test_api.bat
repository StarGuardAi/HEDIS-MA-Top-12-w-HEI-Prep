@echo off
REM Test the HEDIS API
REM Run this after starting the API server with start_api.bat

echo ========================================
echo  HEDIS API Test Suite
echo  Testing all endpoints...
echo ========================================
echo.

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    pause
    exit /b 1
)

REM Check if API is running
echo Checking if API is running on http://localhost:8000...
curl -s http://localhost:8000/health >nul 2>&1
if errorlevel 1 (
    echo.
    echo ERROR: API is not running!
    echo.
    echo Please start the API first:
    echo   1. Run start_api.bat in another terminal
    echo   2. Wait for the server to start
    echo   3. Run this script again
    echo.
    pause
    exit /b 1
)

echo API is running! Starting tests...
echo.
echo ========================================
echo.

REM Run the test script
python test_api.py

echo.
echo ========================================
echo Tests complete!
echo ========================================
pause


@echo off
REM Phase 4 Dashboard - Quick Start Script
REM Run the Streamlit dashboard

echo ============================================
echo HEDIS Portfolio Optimizer - Phase 4 Dashboard
echo ============================================
echo.

REM Change to dashboard directory
cd /d "%~dp0"

REM Check if Streamlit is installed
python -c "import streamlit" 2>nul
if errorlevel 1 (
    echo ERROR: Streamlit not installed!
    echo Please run: pip install streamlit
    pause
    exit /b 1
)

REM Test database connection
echo Testing database connection...
python -c "from utils.database import test_connection; exit(0 if test_connection() else 1)" 2>nul
if errorlevel 1 (
    echo WARNING: Database connection test failed!
    echo Please check your database configuration.
    echo.
    pause
)

REM Launch Streamlit
echo.
echo Starting Streamlit dashboard...
echo Dashboard will open at: http://localhost:8501
echo.
echo Press Ctrl+C to stop the dashboard
echo.

streamlit run app.py

pause


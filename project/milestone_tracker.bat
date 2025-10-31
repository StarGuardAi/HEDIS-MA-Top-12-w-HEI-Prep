@echo off
REM HEDIS GSD Prediction Engine - Milestone Tracker Launcher

echo ========================================
echo HEDIS GSD Milestone Tracker
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please run setup_project.bat first
    echo.
    pause
    exit /b 1
)

REM Run the milestone tracker
echo Starting milestone tracker...
echo.
python milestone_tracker.py

if errorlevel 1 (
    echo.
    echo ERROR: Milestone tracker failed to run
    echo Check for missing dependencies
    echo.
    pause
    exit /b 1
)

echo.
echo Milestone tracker session ended
pause


@echo off
REM HEDIS GSD Prediction Engine - Project Verification

echo ========================================
echo HEDIS GSD Project Verification
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

echo Running comprehensive project verification...
echo.

echo [1/3] Success Criteria Verification...
python scripts/verify-success-criteria.py
echo.

echo [2/3] Testing Verification...
python scripts/verify-testing.py
echo.

echo [3/3] Iteration Verification...
python scripts/verify-iteration.py
echo.

echo ========================================
echo Verification Complete!
echo ========================================
echo.
echo Check the reports directory for detailed results
echo.
pause


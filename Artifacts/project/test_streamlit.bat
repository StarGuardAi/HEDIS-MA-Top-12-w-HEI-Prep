@echo off
REM ============================================================================
REM HEDIS Portfolio Optimizer - Streamlit App Testing Script
REM Author: Robert Reichert
REM Last Updated: October 24, 2025
REM ============================================================================

echo.
echo ========================================
echo  Streamlit App Testing Launcher
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python not found. Please install Python 3.9+
    pause
    exit /b 1
)

echo [INFO] Python found: 
python --version
echo.

REM Check if required packages are installed
echo [INFO] Checking dependencies...
python -c "import streamlit" 2>nul
if errorlevel 1 (
    echo [WARN] Streamlit not installed. Installing...
    pip install streamlit pytest
)

python -c "import pytest" 2>nul
if errorlevel 1 (
    echo [WARN] pytest not installed. Installing...
    pip install pytest
)

echo [OK] Dependencies installed
echo.

REM Show menu
:menu
echo ========================================
echo  Select Testing Option:
echo ========================================
echo.
echo  1. Run Streamlit App (Manual Testing)
echo  2. Run Automated Tests (pytest)
echo  3. Run Tests with Coverage Report
echo  4. Run Specific Test Class
echo  5. Run App in Debug Mode
echo  6. View Testing Documentation
echo  7. Exit
echo.
set /p choice="Enter your choice (1-7): "

if "%choice%"=="1" goto run_app
if "%choice%"=="2" goto run_tests
if "%choice%"=="3" goto run_coverage
if "%choice%"=="4" goto run_specific
if "%choice%"=="5" goto run_debug
if "%choice%"=="6" goto view_docs
if "%choice%"=="7" goto end

echo [ERROR] Invalid choice. Please enter 1-7.
echo.
goto menu

:run_app
echo.
echo ========================================
echo  Starting Streamlit App...
echo ========================================
echo.
echo [INFO] App will open at: http://localhost:8501
echo [INFO] Press Ctrl+C to stop the app
echo.
streamlit run streamlit_app.py
goto end

:run_tests
echo.
echo ========================================
echo  Running Automated Tests...
echo ========================================
echo.
pytest tests/test_streamlit_app.py -v --tb=short
echo.
echo ========================================
echo  Tests Complete!
echo ========================================
echo.
pause
goto menu

:run_coverage
echo.
echo ========================================
echo  Running Tests with Coverage...
echo ========================================
echo.
pytest tests/test_streamlit_app.py -v --cov=streamlit_app --cov-report=html --cov-report=term
echo.
echo [INFO] Opening coverage report in browser...
start htmlcov\index.html
echo.
pause
goto menu

:run_specific
echo.
echo ========================================
echo  Available Test Classes:
echo ========================================
echo.
echo  1. TestAppInitialization
echo  2. TestNavigation
echo  3. TestInteractiveWidgets
echo  4. TestEdgeCases
echo  5. TestDataVisualization
echo  6. TestContactInformation
echo  7. TestPerformance
echo  8. Back to main menu
echo.
set /p test_choice="Enter test class number (1-8): "

if "%test_choice%"=="1" set test_class=TestAppInitialization
if "%test_choice%"=="2" set test_class=TestNavigation
if "%test_choice%"=="3" set test_class=TestInteractiveWidgets
if "%test_choice%"=="4" set test_class=TestEdgeCases
if "%test_choice%"=="5" set test_class=TestDataVisualization
if "%test_choice%"=="6" set test_class=TestContactInformation
if "%test_choice%"=="7" set test_class=TestPerformance
if "%test_choice%"=="8" goto menu

echo.
echo Running %test_class%...
echo.
pytest tests/test_streamlit_app.py::"%test_class%" -v
echo.
pause
goto menu

:run_debug
echo.
echo ========================================
echo  Starting App in Debug Mode...
echo ========================================
echo.
echo [INFO] Debug logs will be shown in console
echo [INFO] App URL: http://localhost:8501
echo.
streamlit run streamlit_app.py --logger.level=debug
goto end

:view_docs
echo.
echo ========================================
echo  Opening Testing Documentation...
echo ========================================
echo.
if exist "docs\STREAMLIT_TESTING_GUIDE.md" (
    start docs\STREAMLIT_TESTING_GUIDE.md
    echo [OK] Documentation opened
) else (
    echo [ERROR] Documentation file not found: docs\STREAMLIT_TESTING_GUIDE.md
)
echo.
pause
goto menu

:end
echo.
echo Goodbye!
echo.


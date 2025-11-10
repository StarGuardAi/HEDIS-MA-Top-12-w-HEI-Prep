@echo off
REM Quick test runner for HEDIS Project (Windows)
REM Author: Robert Reichert

echo ======================================================================
echo   HEDIS Project - Quick Test Runner
echo ======================================================================
echo.

REM Check if pytest is available
python -m pytest --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: pytest not found!
    echo Please install dependencies: pip install -r requirements-full.txt
    pause
    exit /b 1
)

echo Running comprehensive test suite...
echo Expected time: 2-5 minutes
echo.

REM Run tests with coverage
python -m pytest tests/ -v --cov=src --cov-report=html --cov-report=term

if errorlevel 1 (
    echo.
    echo ======================================================================
    echo   Some tests failed. Check output above for details.
    echo ======================================================================
    pause
    exit /b 1
) else (
    echo.
    echo ======================================================================
    echo   All tests passed! Project is production-ready.
    echo ======================================================================
    echo.
    echo Coverage report generated in: htmlcov\index.html
    echo Open it in your browser to see detailed coverage.
    echo.
    pause
)



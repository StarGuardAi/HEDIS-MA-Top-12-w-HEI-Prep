@echo off
REM Start the HEDIS API server
REM This script starts the FastAPI server on localhost:8000

echo ========================================
echo  HEDIS API Server
echo  Starting FastAPI with uvicorn...
echo ========================================
echo.

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    pause
    exit /b 1
)

echo Starting API server on http://localhost:8000
echo.
echo Interactive docs will be available at:
echo   - Swagger UI: http://localhost:8000/docs
echo   - ReDoc:      http://localhost:8000/redoc
echo.
echo Press Ctrl+C to stop the server
echo.
echo ========================================
echo.

REM Start the API server
python -m uvicorn src.api.main:app --reload --host 0.0.0.0 --port 8000

pause


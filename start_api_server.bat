@echo off
REM Start HEDIS API Server
REM This will start the FastAPI server on http://localhost:8000

echo ========================================
echo  Starting HEDIS API Server
echo ========================================
echo.
echo API will be available at:
echo   - Swagger UI:  http://localhost:8000/docs
echo   - ReDoc:       http://localhost:8000/redoc
echo   - Health:      http://localhost:8000/health
echo.
echo Press Ctrl+C to stop the server
echo ========================================
echo.

uvicorn src.api.main:app --reload --host 0.0.0.0 --port 8000



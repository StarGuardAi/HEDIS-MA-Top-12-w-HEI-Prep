@echo off
REM Phase 4 Dashboard - Start Script
REM This starts the Phase 4 ROI Dashboard on port 8502

echo ============================================
echo Phase 4 Dashboard - ROI Analytics
echo ============================================
echo.

cd /d "%~dp0"

echo Starting Phase 4 Dashboard...
echo.
echo Dashboard URL: http://localhost:8502
echo.
echo Press Ctrl+C to stop
echo.

streamlit run app.py --server.port 8502


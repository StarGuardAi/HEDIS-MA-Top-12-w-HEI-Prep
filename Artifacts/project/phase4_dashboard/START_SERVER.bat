@echo off
REM Quick Start Script for HEDIS Portfolio Optimizer
REM This starts the Streamlit server

echo ============================================
echo Starting HEDIS Portfolio Optimizer
echo ============================================
echo.

REM Change to script directory
cd /d "%~dp0"

REM Check if Streamlit is installed
python -c "import streamlit" 2>nul
if errorlevel 1 (
    echo [ERROR] Streamlit is not installed!
    echo.
    echo Please install it first:
    echo   pip install streamlit
    echo.
    pause
    exit /b 1
)

echo [OK] Streamlit is installed
echo.
echo Starting server...
echo.
echo ============================================
echo IMPORTANT: Keep this window open!
echo ============================================
echo.
echo The dashboard will open at: http://localhost:8501
echo.
echo To stop the server, press Ctrl+C
echo.
echo ============================================
echo.

REM Start Streamlit
streamlit run app.py

REM If we get here, server stopped
echo.
echo Server stopped.
pause


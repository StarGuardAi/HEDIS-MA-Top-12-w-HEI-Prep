@echo off
setlocal enabledelayedexpansion
REM Restart Streamlit on Port 8502
REM This script stops any running Streamlit and starts fresh on port 8502

echo ============================================
echo Restarting HEDIS Portfolio Optimizer
echo Port: 8502
echo ============================================
echo.

REM Stop any running Streamlit processes
echo [1/3] Stopping any running Streamlit processes...
echo    Checking for Streamlit processes...

REM Stop streamlit.exe processes
taskkill /F /IM streamlit.exe 2>nul
if %errorlevel% == 0 (
    echo    ✓ Stopped streamlit.exe processes
) else (
    echo    - No streamlit.exe found
)

REM Kill any process using port 8502 (most reliable method)
echo    Checking port 8502...
for /f "tokens=5" %%a in ('netstat -ano 2^>nul ^| findstr ":8502" ^| findstr "LISTENING"') do (
    set "pid=%%a"
    taskkill /F /PID !pid! 2>nul >nul
    if !errorlevel! == 0 (
        echo    ✓ Stopped process on port 8502 (PID: !pid!)
    )
)

REM Wait for processes to fully terminate
timeout /t 2 /nobreak >nul
echo    Done.
echo.

REM Change to dashboard directory
cd /d "%~dp0"
echo [2/3] Changed to dashboard directory: %CD%
echo.

REM Check if Streamlit is installed
python -c "import streamlit" 2>nul
if errorlevel 1 (
    echo ERROR: Streamlit not installed!
    echo Please run: pip install streamlit
    pause
    exit /b 1
)

REM Start Streamlit on port 8502
echo [3/3] Starting Streamlit on port 8502...
echo.
echo ============================================
echo SUCCESS! Streamlit is starting...
echo ============================================
echo.
echo Your dashboard will be available at:
echo    http://localhost:8502
echo.
echo To view the new HEI page:
echo    1. Look in the sidebar for "⚖️ Health Equity Index"
echo    2. Click on it to load the page
echo.
echo Press Ctrl+C to stop the server
echo ============================================
echo.

streamlit run app.py --server.port 8502 --server.address 0.0.0.0

pause


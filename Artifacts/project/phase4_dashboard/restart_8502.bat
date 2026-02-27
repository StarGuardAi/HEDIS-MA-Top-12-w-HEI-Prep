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
set "port_found=0"
netstat -ano | findstr ":8502" | findstr "LISTENING" > "%TEMP%\port_8502_check.txt"
if exist "%TEMP%\port_8502_check.txt" (
    for /f "usebackq tokens=5" %%a in ("%TEMP%\port_8502_check.txt") do (
        set "pid=%%a"
        if not "!pid!"=="" (
            set "port_found=1"
            taskkill /F /PID !pid! >nul 2>&1
            if !errorlevel! == 0 (
                echo    ✓ Stopped process on port 8502 (PID: !pid!)
            )
        )
    )
    del "%TEMP%\port_8502_check.txt" >nul 2>&1
)
if !port_found! == 0 (
    echo    - No process found on port 8502
)

REM Wait for processes to fully terminate
ping 127.0.0.1 -n 3 >nul
echo    Done.
echo.

REM Change to dashboard directory
cd /d "%~dp0"
echo [2/3] Changed to dashboard directory: %CD%
echo.

REM Verify port 8502 is free
echo    Verifying port 8502 is free...
set "port_free=0"
for /l %%i in (1,1,5) do (
    netstat -ano | findstr ":8502" | findstr "LISTENING" >nul 2>&1
    if errorlevel 1 (
        set "port_free=1"
        goto :port_verified
    )
    ping 127.0.0.1 -n 2 >nul
)
:port_verified
if !port_free! == 0 (
    echo    WARNING: Port 8502 may still be in use!
    echo    Attempting to start anyway...
    echo.
)

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


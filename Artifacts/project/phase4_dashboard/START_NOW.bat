@echo off
REM ============================================
REM HEDIS Portfolio Optimizer - START SERVER
REM ============================================
REM This script starts the Streamlit server
REM DO NOT CLOSE THIS WINDOW while using the app!

title HEDIS Portfolio Optimizer - Server

echo.
echo ============================================
echo   HEDIS Portfolio Optimizer
echo   Starting Server...
echo ============================================
echo.

REM Change to script directory
cd /d "%~dp0"

REM Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python not found!
    echo Please install Python 3.8 or higher
    pause
    exit /b 1
)

REM Check Streamlit
echo Checking Streamlit installation...
python -c "import streamlit" 2>nul
if errorlevel 1 (
    echo [ERROR] Streamlit not installed!
    echo.
    echo Installing Streamlit...
    pip install streamlit
    if errorlevel 1 (
        echo [ERROR] Failed to install Streamlit
        pause
        exit /b 1
    )
)

echo [OK] Streamlit is ready
echo.

REM Check if port is in use
netstat -ano | findstr :8501 >nul 2>&1
if not errorlevel 1 (
    echo [WARNING] Port 8501 is already in use!
    echo.
    echo Options:
    echo   1. Close the other application using port 8501
    echo   2. Use a different port (will use 8502)
    echo.
    set /p choice="Use port 8502? (Y/N): "
    if /i "%choice%"=="Y" (
        set PORT=8502
    ) else (
        echo Please close the application using port 8501 and try again
        pause
        exit /b 1
    )
) else (
    set PORT=8501
)

echo.
echo ============================================
echo   IMPORTANT INSTRUCTIONS
echo ============================================
echo.
echo 1. DO NOT CLOSE THIS WINDOW
echo 2. Wait for "Local URL: http://localhost:%PORT%"
echo 3. Browser will open automatically
echo 4. If not, go to: http://localhost:%PORT%
echo.
echo To stop server: Press Ctrl+C
echo.
echo ============================================
echo.

REM Start Streamlit
if "%PORT%"=="8502" (
    streamlit run app.py --server.port 8502
) else (
    streamlit run app.py
)

echo.
echo Server stopped.
pause


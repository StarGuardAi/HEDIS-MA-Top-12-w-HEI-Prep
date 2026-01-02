@echo off
echo ============================================
echo Clearing Streamlit Cache and Restarting
echo ============================================
echo.

REM Stop any running Streamlit processes
echo [1/4] Stopping Streamlit processes...
taskkill /F /IM streamlit.exe 2>nul
taskkill /F /FI "WINDOWTITLE eq *streamlit*" 2>nul
timeout /t 2 /nobreak >nul
echo    Done.
echo.

REM Clear Streamlit cache
echo [2/4] Clearing Streamlit cache...
cd /d "%~dp0"
if exist ".streamlit\cache" (
    rmdir /s /q ".streamlit\cache" 2>nul
    echo    Cache directory cleared.
) else (
    echo    No cache directory found.
)

REM Clear Python cache
echo [3/4] Clearing Python cache...
if exist "pages\__pycache__" (
    rmdir /s /q "pages\__pycache__" 2>nul
    echo    Python cache cleared.
) else (
    echo    No Python cache found.
)

REM Start Streamlit
echo [4/4] Starting Streamlit on port 8502...
echo.
echo ============================================
echo Streamlit will start in a new window
echo ============================================
echo.
echo After it starts:
echo   1. Open: http://localhost:8502
echo   2. Check sidebar - mobile pages should be gone
echo.
echo Press any key to start Streamlit...
pause >nul

cd /d "%~dp0"
start "Streamlit Dashboard" cmd /k "streamlit run app.py --server.port 8502"

echo.
echo Streamlit is starting in a new window...
echo Close this window when done.
timeout /t 3 /nobreak >nul










@echo off
echo ============================================
echo Stop and Restart Streamlit
echo ============================================
echo.

REM Stop Streamlit
echo [1/2] Stopping Streamlit...
taskkill /F /IM streamlit.exe 2>nul
taskkill /F /FI "WINDOWTITLE eq *streamlit*" 2>nul
timeout /t 2 /nobreak >nul
echo    Done.
echo.

REM Restart Streamlit
echo [2/2] Starting Streamlit on port 8502...
echo.
cd /d "%~dp0"
echo Dashboard will be at: http://localhost:8502
echo.
echo Press Ctrl+C in this window to stop Streamlit
echo.
streamlit run app.py --server.port 8502

pause










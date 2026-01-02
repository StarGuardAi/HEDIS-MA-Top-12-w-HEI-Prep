@echo off
REM Auto-restart Streamlit watcher
REM Watches for file changes and automatically restarts Streamlit

echo ========================================
echo 🚀 Starting Streamlit Auto-Restart Watcher
echo ========================================
echo.
echo This will:
echo   - Watch for file changes
echo   - Auto-restart Streamlit on save
echo   - Run on port 8502
echo.
echo Press Ctrl+C to stop
echo ========================================
echo.

cd /d "%~dp0"
python watch_and_restart.py

pause










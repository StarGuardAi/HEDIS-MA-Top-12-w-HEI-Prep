@echo off
echo ============================================
echo Starting Streamlit on Port 8502
echo ============================================
echo.
echo Please keep this window open while using Streamlit.
echo Press Ctrl+C to stop the server.
echo.
echo Your dashboard will be at: http://localhost:8502
echo.
echo ============================================
echo.

cd /d "%~dp0"
streamlit run app.py --server.port 8502

pause










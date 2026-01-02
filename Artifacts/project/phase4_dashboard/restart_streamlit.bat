@echo off
echo Stopping any running Streamlit processes...
taskkill /F /IM streamlit.exe 2>nul
taskkill /F /FI "WINDOWTITLE eq *streamlit*" 2>nul
timeout /t 2 /nobreak >nul

echo.
echo Starting Streamlit with mobile access enabled...
echo.
echo Your local IP: 192.168.1.161
echo.
echo Access from Android:
echo http://192.168.1.161:8501/_mobile_view
echo http://192.168.1.161:8501/_mobile_test
echo.
echo Press Ctrl+C to stop the server
echo.
cd /d "%~dp0"
streamlit run app.py --server.address=0.0.0.0 --server.port=8501 --server.enableCORS=false --server.enableXsrfProtection=false










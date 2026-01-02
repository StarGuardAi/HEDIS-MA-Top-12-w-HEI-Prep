@echo off
echo Starting Streamlit with network access for mobile devices...
echo.
echo Your local IP: 192.168.1.161
echo.
echo Access from Android using:
echo http://192.168.1.161:8501/_mobile_view
echo http://192.168.1.161:8501/_mobile_test
echo.
echo IMPORTANT: If page shows grey placeholders:
echo 1. Check Windows Firewall allows port 8501
echo 2. Ensure Android and PC are on same Wi-Fi network
echo 3. Try the test page first: /_mobile_test
echo.
echo Press Ctrl+C to stop the server
echo.
cd /d "%~dp0"
streamlit run app.py --server.address=0.0.0.0 --server.port=8501 --server.enableCORS=false --server.enableXsrfProtection=false


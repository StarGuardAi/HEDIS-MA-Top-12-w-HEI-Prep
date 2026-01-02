@echo off
echo ========================================
echo Mobile Testing Server
echo ========================================
echo.
echo Activating Python 3.11 environment...

call C:\Users\reich\anaconda3\Scripts\activate.bat hedis_py311

echo.
echo Starting Streamlit app for mobile testing...
echo.
echo Your local IP address: 192.168.1.161
echo.
echo To access on your Android phone:
echo   1. Make sure phone is on same WiFi network
echo   2. Open browser and go to:
echo      http://192.168.1.161:8501
echo.
echo For mobile-optimized view:
echo      http://192.168.1.161:8501/mobile_view
echo.
echo Press Ctrl+C to stop the server
echo ========================================
echo.

streamlit run pages/mobile_view.py --server.address=0.0.0.0 --server.port=8501

pause


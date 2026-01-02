@echo off
echo Stopping Streamlit processes...
taskkill /F /IM streamlit.exe 2>nul
taskkill /F /FI "WINDOWTITLE eq *streamlit*" 2>nul
taskkill /F /FI "IMAGENAME eq python.exe" /FI "WINDOWTITLE eq *streamlit*" 2>nul
echo.
echo Streamlit processes stopped.
echo.
pause










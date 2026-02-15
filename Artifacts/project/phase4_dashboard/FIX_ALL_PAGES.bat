@echo off
echo ========================================
echo Updating ALL pages with aggressive JS fix
echo ========================================
echo.
echo This will update all 22 pages with the
echo most aggressive JavaScript fix possible.
echo.
pause

cd /d "%~dp0"
python fix_all_pages_simple.py

echo.
echo Done! Restart Streamlit to test.
pause


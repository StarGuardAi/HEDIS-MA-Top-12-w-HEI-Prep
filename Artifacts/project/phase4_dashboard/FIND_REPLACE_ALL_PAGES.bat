@echo off
REM Find and Replace Tool for All Dashboard Pages
REM This batch file runs the Python script for bulk find/replace operations

echo ============================================================
echo Find ^& Replace Tool for HEDIS Portfolio Optimizer
echo ============================================================
echo.

cd /d "%~dp0"
python find_replace_all_pages.py

echo.
echo Press any key to exit...
pause >nul


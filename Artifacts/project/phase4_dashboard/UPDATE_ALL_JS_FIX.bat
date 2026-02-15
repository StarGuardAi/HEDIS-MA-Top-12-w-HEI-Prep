@echo off
REM Batch script to update all pages with improved JavaScript fix
REM This uses Python with proper encoding handling

cd /d "%~dp0"
python -c "import sys; sys.stdout.reconfigure(encoding='utf-8'); exec(open('update_js_fix_simple.py', encoding='utf-8').read())" 2>nul

if errorlevel 1 (
    echo.
    echo Running manual updates...
    echo Please wait...
    python update_js_fix_simple.py
)

pause


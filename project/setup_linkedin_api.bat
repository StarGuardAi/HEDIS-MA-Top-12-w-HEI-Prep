@echo off
REM LinkedIn API Setup Script
REM Helps you configure automatic LinkedIn posting

echo ========================================
echo LinkedIn API Setup Wizard
echo ========================================
echo.
echo This script will help you set up automatic LinkedIn posting.
echo.
echo You will need:
echo   1. LinkedIn Developer App credentials
echo   2. About 10 minutes for setup
echo.
echo Don't have a LinkedIn app yet?
echo   Visit: https://www.linkedin.com/developers/apps
echo   See guide: docs\LINKEDIN_API_SETUP_GUIDE.md
echo.
pause

REM Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python not installed
    echo Install Python 3.11+ from python.org
    pause
    exit /b 1
)

REM Check requests library
python -c "import requests" >nul 2>&1
if errorlevel 1 (
    echo Installing requests library...
    pip install requests
)

echo.
echo ========================================
echo Running LinkedIn OAuth Setup
echo ========================================
echo.

REM Run OAuth setup script
python scripts/linkedin_oauth_setup.py

echo.
echo ========================================
echo Setup Complete!
echo ========================================
echo.
echo Next steps:
echo   1. Run: call set_linkedin_token.bat
echo   2. Test: python scripts/publish_to_linkedin.py --milestone 1 --dry-run
echo   3. Real post: python scripts/publish_to_linkedin.py --milestone 1
echo.
echo For help, see: docs\LINKEDIN_API_SETUP_GUIDE.md
echo.

pause


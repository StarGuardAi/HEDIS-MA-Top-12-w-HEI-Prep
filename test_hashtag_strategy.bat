@echo off
REM Test LinkedIn Hashtag Strategy

echo ========================================
echo LinkedIn Hashtag Strategy Test
echo ========================================
echo.

REM Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python not installed
    pause
    exit /b 1
)

echo Testing hashtag selection for all post types...
echo.

python scripts/update_profile.py --test-hashtags

echo.
echo ========================================
echo Test Complete!
echo ========================================
echo.
echo Next steps:
echo 1. Review hashtag recommendations above
echo 2. Generate your first post: publish_linkedin.bat
echo 3. After posting, update engagement metrics in:
echo    reports\linkedin_engagement_tracker.json
echo 4. Generate engagement report:
echo    python scripts\update_profile.py --engagement-report
echo.

pause


@echo off
REM Publish milestone to LinkedIn

echo ========================================
echo LinkedIn Publishing Automation
echo ========================================
echo.

REM Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python not installed
    pause
    exit /b 1
)

REM Get milestone number
set /p milestone="Enter milestone number (1-6): "

REM Get post type
echo.
echo Select post type:
echo 1. Technical (detailed, for data science audience)
echo 2. Impact (business-focused)
echo 3. Storytelling (engaging narrative)
echo.
set /p posttype="Enter choice (1-3): "

if "%posttype%"=="1" set posttypestr=technical
if "%posttype%"=="2" set posttypestr=impact
if "%posttype%"=="3" set posttypestr=storytelling

echo.
echo Generating %posttypestr% LinkedIn post for Milestone %milestone%...
echo.

REM Check if LinkedIn access token is set
if defined LINKEDIN_ACCESS_TOKEN (
    echo ✅ LinkedIn API token detected
    echo.
    echo Choose posting mode:
    echo 1. Post automatically to LinkedIn
    echo 2. Save content for manual posting
    echo.
    set /p autopost="Enter choice (1-2): "
    
    if "!autopost!"=="1" (
        echo.
        echo Posting to LinkedIn automatically...
        python scripts/publish_to_linkedin.py --milestone %milestone% --post-type %posttypestr%
        echo.
        echo ========================================
        echo Check output above for success/failure
        echo ========================================
    ) else (
        echo.
        echo Saving content for manual posting...
        python scripts/publish_to_linkedin.py --milestone %milestone% --post-type %posttypestr% --save-only
        echo.
        echo ========================================
        echo Post content generated!
        echo ========================================
        echo.
        echo Next steps:
        echo 1. Review the generated post content
        echo 2. Copy and paste to LinkedIn
        echo 3. Add your images (from reports/figures/)
        echo 4. Post during optimal time (Tue-Thu, 8-10 AM)
    )
) else (
    echo ⚠️ LinkedIn API token not set - using manual mode
    echo.
    echo To enable automatic posting:
    echo 1. Run: setup_linkedin_api.bat
    echo 2. Or call: set_linkedin_token.bat
    echo.
    
    REM Run Python script (save-only for manual posting)
    python scripts/publish_to_linkedin.py --milestone %milestone% --post-type %posttypestr% --save-only
    
    echo.
    echo ========================================
    echo Post content generated!
    echo ========================================
    echo.
    echo Next steps:
    echo 1. Review the generated post content
    echo 2. Copy and paste to LinkedIn
    echo 3. Add your images (from reports/figures/)
    echo 4. Post during optimal time (Tue-Thu, 8-10 AM)
)

echo.
pause



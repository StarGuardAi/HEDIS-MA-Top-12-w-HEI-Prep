@echo off
REM Publish milestone to GitHub

echo ========================================
echo GitHub Publishing Automation
echo ========================================
echo.

REM Add GitHub CLI to PATH
set PATH=%PATH%;C:\Program Files\GitHub CLI

REM Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python not installed
    pause
    exit /b 1
)

REM Check GitHub CLI authentication
gh auth status >nul 2>&1
if errorlevel 1 (
    echo.
    echo WARNING: Not authenticated with GitHub CLI
    echo Run: authenticate_github.bat
    echo.
    echo You can still update README and badges, but releases require authentication.
    echo.
)

REM Get milestone number (optional)
set /p milestone="Enter milestone number for release (1-6) or press Enter to skip: "

echo.
echo What would you like to do?
echo 1. Update README with milestone status
echo 2. Add/update badges
echo 3. Create GitHub release (requires milestone)
echo 4. Commit changes
echo 5. Do everything (recommended)
echo.
set /p choice="Enter choice (1-5): "

echo.

if "%choice%"=="1" (
    python scripts/publish_to_github.py --update-readme
) else if "%choice%"=="2" (
    python scripts/publish_to_github.py --add-badges
) else if "%choice%"=="3" (
    if "%milestone%"=="" (
        echo ERROR: Milestone number required for release
        pause
        exit /b 1
    )
    python scripts/publish_to_github.py --milestone %milestone% --create-release
) else if "%choice%"=="4" (
    python scripts/publish_to_github.py --commit
) else if "%choice%"=="5" (
    if "%milestone%"=="" (
        python scripts/publish_to_github.py --all
    ) else (
        python scripts/publish_to_github.py --milestone %milestone% --all
    )
) else (
    echo Invalid choice
    pause
    exit /b 1
)

echo.
echo ========================================
echo GitHub publishing complete!
echo ========================================
echo.
echo Next steps:
echo 1. Review the changes
echo 2. Push to GitHub: git push origin main
echo.

pause



@echo off
REM Master Publishing Automation - Publish to All Platforms

echo ========================================
echo HEDIS GSD - Master Publishing Automation
echo ========================================
echo.
echo This will publish your milestone to:
echo   - LinkedIn (content generation)
echo   - GitHub (README, badges, release)
echo   - Resume (Word document)
echo.
echo Note: Canva updates remain manual.
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
    echo GitHub releases will not be created.
    echo Run: authenticate_github.bat
    echo.
)

REM Get milestone number
set /p milestone="Enter milestone number to publish (1-6): "

echo.
echo Publishing Milestone %milestone% to all platforms...
echo.

REM ========================================
REM 1. GitHub Publishing
REM ========================================
echo.
echo [1/3] Publishing to GitHub...
echo ========================================
echo.

python scripts/publish_to_github.py --milestone %milestone% --all

if errorlevel 1 (
    echo.
    echo WARNING: GitHub publishing had issues
    echo.
)

REM ========================================
REM 2. LinkedIn Content Generation
REM ========================================
echo.
echo [2/3] Generating LinkedIn Post...
echo ========================================
echo.

REM Generate technical post by default
python scripts/publish_to_linkedin.py --milestone %milestone% --post-type technical --save-only

if errorlevel 1 (
    echo.
    echo WARNING: LinkedIn content generation had issues
    echo.
)

REM ========================================
REM 3. Resume Generation
REM ========================================
echo.
echo [3/3] Generating Word Resume...
echo ========================================
echo.

REM Install python-docx if needed
python -c "import docx" 2>nul
if errorlevel 1 (
    echo Installing python-docx...
    pip install python-docx
)

python scripts/generate_resume_word.py --milestone %milestone%

if errorlevel 1 (
    echo.
    echo WARNING: Resume generation had issues
    echo.
)

REM ========================================
REM Summary
REM ========================================
echo.
echo ========================================
echo Publishing Complete!
echo ========================================
echo.
echo ✅ GitHub: Updated (README, badges, release notes)
echo ✅ LinkedIn: Content generated (see reports/)
echo ✅ Resume: Word document created (see reports/)
echo ⏳ Canva: Manual update required
echo.
echo ========================================
echo Next Steps:
echo ========================================
echo.
echo 1. GITHUB:
echo    - Review changes
echo    - Run: git push origin main
echo.
echo 2. LINKEDIN:
echo    - Open generated post content
echo    - Copy to LinkedIn
echo    - Add images from reports/figures/
echo    - Post on Tue-Thu, 8-10 AM
echo.
echo 3. RESUME:
echo    - Review Word document
echo    - Update contact info
echo    - Save as PDF
echo.
echo 4. CANVA:
echo    - Run: optimize_portfolio.bat
echo    - Manual update to portfolio
echo.

pause



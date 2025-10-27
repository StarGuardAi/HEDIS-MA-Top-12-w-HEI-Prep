@echo off
REM ================================================================
REM Portfolio Materials Generator - Master Automation Script
REM ================================================================
REM
REM Generates:
REM - One-page resume (PDF and DOCX)
REM - LinkedIn post content
REM - Canva portfolio content
REM
REM Usage:
REM   generate_portfolio_materials.bat
REM   generate_portfolio_materials.bat --resume-only
REM   generate_portfolio_materials.bat --linkedin-only
REM   generate_portfolio_materials.bat --canva-only
REM
REM ================================================================

setlocal enabledelayedexpansion

echo.
echo ================================================================
echo  PORTFOLIO MATERIALS GENERATOR
echo ================================================================
echo.
echo This script will generate:
echo   - One-page resume (PDF and DOCX formats)
echo   - LinkedIn post content
echo   - Canva portfolio content
echo.
echo ================================================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8+ from https://www.python.org/
    pause
    exit /b 1
)

REM Check for required packages
echo Checking dependencies...
python -c "import docx" >nul 2>&1
if errorlevel 1 (
    echo.
    echo Installing python-docx for Word document generation...
    pip install python-docx
)

python -c "import reportlab" >nul 2>&1
if errorlevel 1 (
    echo.
    echo Installing reportlab for PDF generation...
    pip install reportlab
)

echo.
echo Dependencies OK!
echo.
echo ================================================================
echo  GENERATING CONTENT...
echo ================================================================
echo.

REM Run the generator
if "%1"=="" (
    REM Default: generate all
    python scripts/generate_portfolio_content.py --all
) else (
    REM Pass through arguments
    python scripts/generate_portfolio_content.py %*
)

if errorlevel 1 (
    echo.
    echo ================================================================
    echo  ERROR: Content generation failed
    echo ================================================================
    pause
    exit /b 1
)

echo.
echo ================================================================
echo  SUCCESS! All materials generated
echo ================================================================
echo.
echo Files saved in: reports\
echo.
echo Next steps:
echo   1. Review generated resume (PDF and DOCX)
echo   2. Copy LinkedIn content and post
echo   3. Import Canva content to your portfolio
echo   4. Update GitHub profile and pages
echo.
echo Quick actions:
echo   - Open reports folder:  explorer reports
echo   - View LinkedIn post:   notepad reports\LinkedIn_Portfolio_Post_*.txt
echo   - View Canva content:   notepad reports\Canva_Portfolio_Content_*.txt
echo.

REM Ask if user wants to open reports folder
set /p OPEN_FOLDER="Open reports folder now? (Y/N): "
if /i "%OPEN_FOLDER%"=="Y" (
    start explorer reports
)

echo.
echo ================================================================
echo  AUTOMATION COMPLETE
echo ================================================================
echo.
pause


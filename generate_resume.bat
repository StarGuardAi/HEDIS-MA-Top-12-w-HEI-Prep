@echo off
REM Generate one-page Word resume

echo ========================================
echo Word Resume Generation
echo ========================================
echo.

REM Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python not installed
    pause
    exit /b 1
)

REM Check for python-docx
python -c "import docx" 2>nul
if errorlevel 1 (
    echo Installing python-docx...
    pip install python-docx
)

REM Get milestone number (optional)
set /p milestone="Enter milestone number to mark as published (1-6) or press Enter to skip: "

echo.
echo Generating professional one-page resume...
echo.

REM Run Python script
if "%milestone%"=="" (
    python scripts/generate_resume_word.py
) else (
    python scripts/generate_resume_word.py --milestone %milestone%
)

echo.
echo ========================================
echo Resume generated!
echo ========================================
echo.
echo The resume will open in Microsoft Word.
echo.
echo Next steps:
echo 1. Review and customize the resume
echo 2. Update contact information
echo 3. Save as PDF for job applications
echo 4. Keep Word version for easy updates
echo.

pause



@echo off
REM HEDIS GSD Prediction Engine - Update Milestone and Portfolio

echo ========================================
echo Update Milestone and Portfolio
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please run setup_project.bat first
    echo.
    pause
    exit /b 1
)

REM Get milestone number from user
set /p milestone_id="Enter milestone number (1-6): "

REM Validate input
if "%milestone_id%"=="" (
    echo ERROR: No milestone number provided
    pause
    exit /b 1
)

REM Get status from user
echo.
echo Select status:
echo 1. Completed
echo 2. In Progress
echo 3. Pending
echo.
set /p status_choice="Enter status (1-3): "

REM Map choice to status
if "%status_choice%"=="1" set status=completed
if "%status_choice%"=="2" set status=in_progress
if "%status_choice%"=="3" set status=pending

if "%status%"=="" (
    echo ERROR: Invalid status choice
    pause
    exit /b 1
)

echo.
echo Updating Milestone %milestone_id% to status: %status%
echo.

REM Update milestone portfolio
python scripts/milestone_portfolio_updater.py %milestone_id% %status%

if errorlevel 1 (
    echo.
    echo ERROR: Milestone update failed
    echo.
    pause
    exit /b 1
)

echo.
echo ========================================
echo Milestone Updated Successfully!
echo ========================================
echo.
echo The updated portfolio content has been saved.
echo Copy it to your Canva portfolio:
echo https://www.canva.com/design/DAGpa3zpXTw/Y7ycEdZ2_vnKjlFWGdcQwg/edit
echo.
pause


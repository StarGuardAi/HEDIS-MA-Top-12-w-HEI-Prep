@echo off
REM HEDIS GSD Prediction Engine - Quick Start Menu

:menu
cls
echo ========================================
echo HEDIS GSD Prediction Engine
echo Quick Start Menu
echo ========================================
echo.
echo 1. Setup Project (First Time Only)
echo 2. Track Milestones
echo 3. Optimize Canva Portfolio
echo 4. Update Milestone Progress
echo 5. Verify Project Status
echo 6. View Milestone Data
echo 7. Exit
echo.
set /p choice="Enter your choice (1-7): "

if "%choice%"=="1" goto setup
if "%choice%"=="2" goto tracker
if "%choice%"=="3" goto optimize
if "%choice%"=="4" goto update
if "%choice%"=="5" goto verify
if "%choice%"=="6" goto view
if "%choice%"=="7" goto end

echo Invalid choice. Please try again.
pause
goto menu

:setup
cls
echo Running project setup...
call setup_project.bat
goto menu

:tracker
cls
echo Starting milestone tracker...
call milestone_tracker.bat
goto menu

:optimize
cls
echo Optimizing Canva portfolio...
call optimize_portfolio.bat
goto menu

:update
cls
echo Updating milestone progress...
call update_milestone.bat
goto menu

:verify
cls
echo Verifying project status...
call verify_project.bat
goto menu

:view
cls
echo ========================================
echo Current Milestone Data
echo ========================================
echo.
if exist milestones.json (
    type milestones.json
) else (
    echo No milestone data found
    echo Run milestone tracker first
)
echo.
pause
goto menu

:end
echo.
echo Thank you for using HEDIS GSD Prediction Engine!
echo.
exit /b 0


@echo off
REM HEDIS GSD Prediction Engine - Automated Project Setup
REM Run this after installing Python

echo ========================================
echo HEDIS GSD Prediction Engine Setup
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo.
    echo Please install Python from https://www.python.org/downloads/
    echo Make sure to check "Add Python to PATH" during installation
    echo.
    pause
    exit /b 1
)

echo [1/5] Python found:
python --version
echo.

REM Check if pip is available
echo [2/5] Checking pip...
pip --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: pip is not installed
    echo Installing pip...
    python -m ensurepip --upgrade
)
pip --version
echo.

REM Upgrade pip
echo [3/5] Upgrading pip...
python -m pip install --upgrade pip
echo.

REM Install project dependencies
echo [4/5] Installing project dependencies...
if exist requirements.txt (
    pip install -r requirements.txt
    echo Dependencies installed successfully
) else (
    echo WARNING: requirements.txt not found
)
echo.

REM Create necessary directories
echo [5/5] Creating project directories...
if not exist "reports" mkdir reports
if not exist "models" mkdir models
if not exist "data\raw" mkdir data\raw
if not exist "data\processed" mkdir data\processed
if not exist "tasks\completed" mkdir tasks\completed
echo Directories created
echo.

echo ========================================
echo Setup Complete!
echo ========================================
echo.
echo Next steps:
echo 1. Run milestone_tracker.bat to start milestone tracking
echo 2. Run optimize_portfolio.bat to update your Canva portfolio
echo 3. Run verify_project.bat to check project status
echo.
pause


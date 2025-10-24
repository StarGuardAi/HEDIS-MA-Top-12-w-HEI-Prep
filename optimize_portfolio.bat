@echo off
REM HEDIS GSD Prediction Engine - Canva Portfolio Optimizer

echo ========================================
echo Canva Portfolio Optimizer
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

REM Run the portfolio optimizer
echo Generating optimized Canva portfolio content...
echo.
python scripts/canva_portfolio_optimizer.py

if errorlevel 1 (
    echo.
    echo ERROR: Portfolio optimizer failed to run
    echo.
    pause
    exit /b 1
)

echo.
echo ========================================
echo Portfolio Content Generated!
echo ========================================
echo.
echo The optimized content has been saved to:
echo canva_portfolio_optimized.txt
echo.
echo Next steps:
echo 1. Open the file to view the content
echo 2. Copy the content to your Canva portfolio
echo 3. Update design elements as needed
echo.
echo Canva Portfolio URL:
echo https://www.canva.com/design/DAGpa3zpXTw/Y7ycEdZ2_vnKjlFWGdcQwg/edit
echo.

REM Open the generated file
if exist canva_portfolio_optimized.txt (
    notepad canva_portfolio_optimized.txt
)

pause


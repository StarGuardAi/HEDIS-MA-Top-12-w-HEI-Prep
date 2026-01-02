@echo off
REM Docker-based PostgreSQL Setup and Phase 1 Runner (Windows)
REM Automatically starts PostgreSQL in Docker and runs all Phase 1 scripts

echo ================================================================================
echo HEDIS STAR RATING PORTFOLIO OPTIMIZER
echo Docker-based PostgreSQL Setup
echo ================================================================================
echo.

REM Check if Docker is available
docker --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Docker not found!
    echo.
    echo Please install Docker Desktop:
    echo   https://www.docker.com/products/docker-desktop
    echo.
    echo After installing Docker Desktop, restart this script.
    pause
    exit /b 1
)

echo Docker found!
echo.

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python not found. Please install Python 3.8+ and add to PATH.
    pause
    exit /b 1
)

REM Check if psycopg2 is installed
python -c "import psycopg2" >nul 2>&1
if errorlevel 1 (
    echo Installing psycopg2-binary...
    pip install psycopg2-binary
    if errorlevel 1 (
        echo ERROR: Failed to install psycopg2-binary
        pause
        exit /b 1
    )
)

echo Starting PostgreSQL in Docker and running Phase 1 setup...
echo This will take approximately 15-20 minutes.
echo.
pause

REM Run the Python setup script
python "%~dp0setup_with_docker.py"

if errorlevel 1 (
    echo.
    echo ERROR: Setup failed. Check error messages above.
    pause
    exit /b 1
) else (
    echo.
    echo Setup completed successfully!
    echo.
    echo PostgreSQL is running in Docker container 'hedis_postgres'
    echo To stop it: docker-compose -f docker-compose-hedis.yml down
)

pause


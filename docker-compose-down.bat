@echo off
REM HEDIS Portfolio Optimizer - Docker Compose Down (Windows)

echo.
echo Stopping HEDIS Portfolio Optimizer...
echo.

REM Check for --volumes flag
set REMOVE_VOLUMES=0
if "%1"=="--volumes" set REMOVE_VOLUMES=1

if %REMOVE_VOLUMES%==1 (
    echo Removing containers, networks, and volumes...
    docker-compose down -v
) else (
    echo Stopping containers and removing networks...
    docker-compose down
)

if errorlevel 1 (
    echo ERROR: Failed to stop services!
    exit /b 1
)

echo.
echo Services stopped successfully!
echo.

if %REMOVE_VOLUMES%==0 (
    echo Note: Data volumes were preserved.
    echo To remove volumes as well, run:
    echo   docker-compose-down.bat --volumes
    echo.
)



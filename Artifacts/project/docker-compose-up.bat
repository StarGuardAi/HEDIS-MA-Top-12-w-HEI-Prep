@echo off
REM HEDIS Portfolio Optimizer - Docker Compose Up (Windows)

echo.
echo Starting HEDIS Portfolio Optimizer with Docker Compose...
echo.

REM Check if docker-compose is installed
docker-compose --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: docker-compose not found!
    echo Please install Docker Desktop for Windows
    exit /b 1
)

REM Start services
echo Building and starting services...
echo.

docker-compose up --build -d

if errorlevel 1 (
    echo.
    echo ERROR: Failed to start services!
    exit /b 1
)

echo.
echo Services started successfully!
echo.

REM Show running containers
echo Running Services:
docker-compose ps
echo.

REM Wait for API to be healthy
echo Waiting for API to be healthy...
timeout /t 5 /nobreak >nul

for /l %%i in (1,1,30) do (
    curl -f -s http://localhost:8000/api/v1/health >nul 2>&1
    if not errorlevel 1 (
        echo API is healthy!
        goto :healthy
    )
    timeout /t 2 /nobreak >nul
)

echo WARNING: API health check timed out
echo Check logs with: docker-compose logs api
goto :show_info

:healthy
echo.
echo Available Services:
echo   - API: http://localhost:8000
echo   - API Docs: http://localhost:8000/docs
echo   - Database: localhost:5432
echo   - Redis: localhost:6379
echo.

:show_info
echo Useful Commands:
echo   - View logs: docker-compose logs -f
echo   - Stop services: docker-compose down
echo   - Restart API: docker-compose restart api
echo.

echo HEDIS Portfolio Optimizer is running!




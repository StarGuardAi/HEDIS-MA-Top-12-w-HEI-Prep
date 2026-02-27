@echo off
REM HEDIS Portfolio Optimizer - Docker Build Script (Windows)

echo.
echo Building HEDIS Portfolio Optimizer Docker Image...
echo.

REM Get git commit (if available)
for /f "tokens=*" %%i in ('git rev-parse --short HEAD 2^>nul') do set VCS_REF=%%i
if "%VCS_REF%"=="" set VCS_REF=unknown

REM Get current date/time
for /f "tokens=*" %%i in ('powershell -Command "Get-Date -Format 'yyyy-MM-ddTHH:mm:ssZ'"') do set BUILD_DATE=%%i

set IMAGE_NAME=hedis-portfolio-api
set IMAGE_TAG=latest

echo Build Configuration:
echo   - Image: %IMAGE_NAME%:%IMAGE_TAG%
echo   - Build Date: %BUILD_DATE%
echo   - Git Commit: %VCS_REF%
echo.

echo Building Docker image...
docker build ^
  --build-arg BUILD_DATE="%BUILD_DATE%" ^
  --build-arg VCS_REF="%VCS_REF%" ^
  --tag %IMAGE_NAME%:%IMAGE_TAG% ^
  --tag %IMAGE_NAME%:%VCS_REF% ^
  --file Dockerfile ^
  .

if errorlevel 1 (
    echo.
    echo ERROR: Docker build failed!
    exit /b 1
)

echo.
echo Docker image built successfully!
echo.
echo Image Details:
docker images %IMAGE_NAME% --format "table {{.Repository}}\t{{.Tag}}\t{{.Size}}\t{{.CreatedAt}}"
echo.

echo To run the container:
echo   docker run -p 8000:8000 %IMAGE_NAME%:%IMAGE_TAG%
echo.
echo Or use docker-compose:
echo   docker-compose up
echo.


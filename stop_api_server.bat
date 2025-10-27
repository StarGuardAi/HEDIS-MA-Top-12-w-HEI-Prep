@echo off
REM Stop HEDIS API Server
REM This will stop all running uvicorn processes

echo ========================================
echo  Stopping HEDIS API Server
echo ========================================
echo.

powershell -Command "Get-Process | Where-Object {$_.ProcessName -eq 'python' -and $_.CommandLine -like '*uvicorn*'} | Stop-Process -Force"

echo.
echo API server stopped!
echo ========================================



@echo off
echo.
echo ========================================
echo Testing Portfolio Locally
echo ========================================
echo.

echo Opening landing page in browser...
start "" "http://localhost:8000/"

echo.
echo Starting local server on port 8000...
echo Press Ctrl+C to stop the server
echo.

python -m http.server 8000


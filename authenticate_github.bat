@echo off
REM Authenticate with GitHub CLI

echo.
echo ========================================
echo   GitHub Authentication
echo ========================================
echo.

REM Add GitHub CLI to PATH for this session
set PATH=%PATH%;C:\Program Files\GitHub CLI

REM Check if already authenticated
gh auth status >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    echo [OK] Already authenticated with GitHub!
    echo.
    gh auth status
    echo.
    pause
    exit /b 0
)

echo Starting GitHub authentication...
echo.
echo Please follow these steps:
echo 1. Select: GitHub.com
echo 2. Select: HTTPS
echo 3. Select: Login with a web browser
echo 4. Copy the code shown
echo 5. Press Enter to open browser
echo 6. Paste code and authorize
echo.

REM Start authentication
gh auth login

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ========================================
    echo   Authentication Successful!
    echo ========================================
    echo.
    gh auth status
    echo.
    echo You're now ready to publish your milestones!
    echo.
    echo Next steps:
    echo   1. Run: publish_github.bat
    echo   2. Enter milestone number: 1
    echo   3. Then run again for milestone: 2
    echo   4. Finally: git push origin main
    echo.
) else (
    echo.
    echo [!] Authentication failed. Please try again.
    echo.
)

pause


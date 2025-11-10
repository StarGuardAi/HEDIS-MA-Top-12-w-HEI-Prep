@echo off
REM Authenticate with GitHub CLI using Personal Access Token
REM This is an alternative to the interactive web authentication

echo.
echo ========================================
echo   GitHub Authentication (Token Method)
echo ========================================
echo.

REM Add GitHub CLI to PATH
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

echo This method uses a Personal Access Token for authentication.
echo It's simpler than the web browser method.
echo.
echo ========================================
echo   Step 1: Create a Personal Access Token
echo ========================================
echo.
echo 1. Open: https://github.com/settings/tokens?type=beta
echo 2. Click: "Generate new token" (Fine-grained token)
echo 3. Token name: "HEDIS GSD Project"
echo 4. Expiration: 90 days (or your preference)
echo 5. Repository access: Select "Only select repositories"
echo 6. Choose: hedis-gsd-prediction-engine
echo 7. Permissions needed:
echo    - Contents: Read and write
echo    - Metadata: Read-only (auto-selected)
echo 8. Click: "Generate token"
echo 9. COPY the token (you won't see it again!)
echo.

pause

echo.
echo Opening GitHub token creation page in browser...
start https://github.com/settings/tokens?type=beta

echo.
echo ========================================
echo   Step 2: Authenticate with Token
echo ========================================
echo.
echo Once you have your token, paste it below.
echo.

REM Authenticate with token
echo YOUR_TOKEN_HERE | gh auth login --with-token

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
    echo   1. Run: publish_all.bat
    echo   2. Enter milestone number: 1
    echo   3. Then run again for milestone: 2
    echo   4. Finally: git push origin main
    echo.
) else (
    echo.
    echo [!] Authentication failed.
    echo.
    echo Please try the manual method:
    echo 1. Get your token from: https://github.com/settings/tokens
    echo 2. Run this command:
    echo    echo YOUR_TOKEN_HERE | gh auth login --with-token
    echo.
    echo Replace YOUR_TOKEN_HERE with your actual token.
    echo.
)

pause


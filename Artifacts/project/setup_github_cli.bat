@echo off
REM Setup GitHub CLI for Milestone Automation
REM This script helps locate or install GitHub CLI

echo.
echo ========================================
echo   GitHub CLI Setup for Milestone Automation
echo ========================================
echo.

REM Check if gh is already in PATH
where gh >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    echo [OK] GitHub CLI is already installed and in PATH!
    echo.
    gh --version
    echo.
    goto :authenticate
)

echo [!] GitHub CLI not found in PATH
echo.

REM Search common installation locations
echo Searching for GitHub CLI installation...
echo.

set "GH_PATH="

if exist "C:\Program Files\GitHub CLI\gh.exe" (
    set "GH_PATH=C:\Program Files\GitHub CLI"
    goto :found
)

if exist "C:\Program Files (x86)\GitHub CLI\gh.exe" (
    set "GH_PATH=C:\Program Files (x86)\GitHub CLI"
    goto :found
)

if exist "%LOCALAPPDATA%\Programs\GitHub CLI\gh.exe" (
    set "GH_PATH=%LOCALAPPDATA%\Programs\GitHub CLI"
    goto :found
)

REM Not found - offer installation options
echo [!] GitHub CLI not found in standard locations
echo.
echo INSTALLATION OPTIONS:
echo.
echo Option 1: Install via winget (Windows Package Manager)
echo    winget install --id GitHub.cli
echo.
echo Option 2: Download installer from:
echo    https://cli.github.com/
echo.
echo Option 3: Install via Chocolatey
echo    choco install gh
echo.

choice /C 12Q /N /M "Choose option (1, 2, or Q to quit): "
set CHOICE=%ERRORLEVEL%

if %CHOICE% EQU 1 (
    echo.
    echo Installing GitHub CLI via winget...
    winget install --id GitHub.cli
    if %ERRORLEVEL% EQU 0 (
        echo.
        echo [OK] Installation complete!
        echo Please close and reopen this terminal, then run this script again.
        pause
        exit /b 0
    ) else (
        echo.
        echo [!] Installation failed. Try Option 2 (manual download).
        pause
        exit /b 1
    )
)

if %CHOICE% EQU 2 (
    echo.
    echo Opening browser to download page...
    start https://cli.github.com/
    echo.
    echo Please download and install GitHub CLI, then run this script again.
    pause
    exit /b 0
)

echo.
echo Exiting...
exit /b 0

:found
echo [OK] Found GitHub CLI at: %GH_PATH%
echo.

REM Add to PATH for current session
set "PATH=%PATH%;%GH_PATH%"

REM Verify it works
gh --version
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo [!] GitHub CLI found but cannot run. Try reinstalling.
    pause
    exit /b 1
)

echo.
echo [OK] GitHub CLI is working!
echo.

REM Ask about permanent PATH addition
echo Do you want to add GitHub CLI to your system PATH permanently?
echo (This will make 'gh' command available in all terminals)
echo.
choice /C YN /M "Add to PATH permanently? (Y/N)"

if %ERRORLEVEL% EQU 1 (
    echo.
    echo Adding to user PATH...
    
    REM Use PowerShell to modify user PATH
    powershell -Command "[Environment]::SetEnvironmentVariable('Path', [Environment]::GetEnvironmentVariable('Path', 'User') + ';%GH_PATH%', 'User')"
    
    echo [OK] Added to PATH. Changes will take effect in new terminals.
    echo.
)

:authenticate
echo.
echo ========================================
echo   Step 2: Authenticate with GitHub
echo ========================================
echo.

REM Check authentication status
gh auth status >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    echo [OK] Already authenticated with GitHub!
    echo.
    gh auth status
    echo.
    goto :ready
)

echo Not authenticated yet. Let's authenticate now.
echo.
echo This will open a browser window for authentication.
echo.
pause

gh auth login

if %ERRORLEVEL% EQU 0 (
    echo.
    echo [OK] Authentication successful!
    echo.
    goto :ready
) else (
    echo.
    echo [!] Authentication failed. Please try again.
    echo.
    pause
    exit /b 1
)

:ready
echo.
echo ========================================
echo   Setup Complete! You're Ready to Go!
echo ========================================
echo.
echo Next steps to publish your milestones:
echo.
echo 1. Publish Milestone 1:
echo    publish_github.bat
echo    Enter milestone number: 1
echo.
echo 2. Publish Milestone 2:
echo    publish_github.bat  
echo    Enter milestone number: 2
echo.
echo 3. Push changes to GitHub:
echo    git push origin main
echo.
echo 4. Check releases on GitHub:
echo    https://github.com/YOUR_USERNAME/hedis-gsd-prediction-engine/releases
echo.
echo Or use the master script to publish everything at once:
echo    publish_all.bat
echo.

pause


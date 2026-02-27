@echo off
REM organize-repo-files.bat
REM Move all files to a folder except README.md

set TARGET_FOLDER=project

echo Organizing repository files...
echo Target folder: %TARGET_FOLDER%
echo.

REM Create target folder
if not exist "%TARGET_FOLDER%" mkdir "%TARGET_FOLDER%"

echo Moving files and folders...
echo.

REM Move all files/folders except README.md, .git, and target folder
for /f "delims=" %%i in ('dir /b /a ^| findstr /v "^README.md$ ^.git$ ^%TARGET_FOLDER%$"') do (
    if not exist "%TARGET_FOLDER%\%%i" (
        move "%%i" "%TARGET_FOLDER%\" >nul 2>&1
        if errorlevel 1 (
            echo [WARN] Could not move: %%i
        ) else (
            echo [OK] Moved: %%i
        )
    )
)

echo.
echo Repository organized!
echo Root directory now contains:
echo   - README.md (visible at root)
echo   - %TARGET_FOLDER%\ (contains all other files)
echo.
echo Next steps:
echo   1. Review changes: git status
echo   2. Stage changes: git add .
echo   3. Commit: git commit -m "Organize files: move all to %TARGET_FOLDER%/"
echo   4. Push: git push origin main
echo.

pause


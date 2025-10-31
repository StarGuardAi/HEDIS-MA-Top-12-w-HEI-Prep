@echo off
echo Transferring repository to StarGuardAi...
echo.
echo This will transfer: reichert-science-intelligence/HEDIS-MA-Top-12-w-HEI-Prep
echo To organization: StarGuardAi
echo.
pause

gh repo transfer reichert-science-intelligence/HEDIS-MA-Top-12-w-HEI-Prep StarGuardAi --yes

if %errorlevel% equ 0 (
    echo.
    echo Transfer successful!
    echo New URL: https://github.com/StarGuardAi/HEDIS-MA-Top-12-w-HEI-Prep
    echo.
    echo Updating local remote...
    git remote set-url origin https://github.com/StarGuardAi/HEDIS-MA-Top-12-w-HEI-Prep.git
    echo Done!
) else (
    echo.
    echo Transfer failed. Check error above.
)

pause


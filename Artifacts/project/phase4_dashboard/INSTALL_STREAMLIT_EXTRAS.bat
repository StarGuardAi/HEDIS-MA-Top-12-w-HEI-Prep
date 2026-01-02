@echo off
REM ============================================
REM Install streamlit-extras Package
REM ============================================

echo.
echo Installing streamlit-extras package...
echo.

cd /d "%~dp0"

REM Try multiple installation methods
echo Method 1: pip install...
python -m pip install streamlit-extras

echo.
echo Method 2: pip install with upgrade...
python -m pip install --upgrade --force-reinstall streamlit-extras

echo.
echo Verifying installation...
python -c "import streamlit_extras.metric_cards; print('[SUCCESS] streamlit-extras installed!')" 2>nul
if errorlevel 1 (
    echo [ERROR] Installation failed!
    echo.
    echo Trying alternative installation...
    python -m pip install git+https://github.com/arnaudmiribel/streamlit-extras.git
)

echo.
echo ============================================
echo Installation attempt complete
echo ============================================
echo.
echo Please verify with:
echo   python -c "import streamlit_extras.metric_cards; print('OK')"
echo.
pause


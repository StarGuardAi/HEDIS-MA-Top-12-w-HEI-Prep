@echo off
REM ============================================
REM Fix Missing Dependencies
REM ============================================

echo.
echo Installing all required packages...
echo.

cd /d "%~dp0"

REM Install all requirements
pip install -r requirements.txt

echo.
echo ============================================
echo Verifying key packages...
echo ============================================

python -c "import streamlit; print('[OK] streamlit')" 2>nul || echo [FAIL] streamlit
python -c "import pandas; print('[OK] pandas')" 2>nul || echo [FAIL] pandas
python -c "import plotly; print('[OK] plotly')" 2>nul || echo [FAIL] plotly
python -c "import streamlit_extras.metric_cards; print('[OK] streamlit-extras')" 2>nul || echo [FAIL] streamlit-extras
python -c "import streamlit_aggrid; print('[OK] streamlit-aggrid')" 2>nul || echo [FAIL] streamlit-aggrid

echo.
echo ============================================
echo Installation complete!
echo ============================================
echo.
echo Now you can run: streamlit run app.py
echo.
pause


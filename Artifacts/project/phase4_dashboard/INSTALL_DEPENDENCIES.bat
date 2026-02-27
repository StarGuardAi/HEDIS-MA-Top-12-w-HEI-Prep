@echo off
REM ============================================
REM Install All Required Dependencies
REM ============================================

echo.
echo ============================================
echo Installing HEDIS Portfolio Optimizer Dependencies
echo ============================================
echo.

cd /d "%~dp0"

echo Installing core packages...
python -m pip install --upgrade pip
python -m pip install streamlit>=1.39.0
python -m pip install pandas>=2.2.3
python -m pip install plotly>=5.18.0
python -m pip install streamlit-extras>=0.3.0
python -m pip install streamlit-aggrid>=0.3.4

echo.
echo Installing database packages...
python -m pip install psycopg2-binary>=2.9.11
python -m pip install sqlalchemy

echo.
echo Installing AI packages...
python -m pip install openai>=1.0.0
python -m pip install anthropic>=0.18.0

echo.
echo Installing utility packages...
python -m pip install openpyxl>=3.1.0
python -m pip install scipy>=1.11.0

echo.
echo Installing ML packages...
python -m pip install xgboost>=2.0.0
python -m pip install scikit-learn>=1.3.0
python -m pip install imbalanced-learn>=0.11.0

echo.
echo Installing architecture packages...
python -m pip install pydantic>=2.0.0
python -m pip install pydantic-settings>=2.0.0

echo.
echo ============================================
echo Verifying installations...
echo ============================================

python -c "import streamlit; print('[OK] streamlit')" 2>nul || echo [FAIL] streamlit
python -c "import pandas; print('[OK] pandas')" 2>nul || echo [FAIL] pandas
python -c "import plotly; print('[OK] plotly')" 2>nul || echo [FAIL] plotly
python -c "import streamlit_extras.metric_cards; print('[OK] streamlit-extras')" 2>nul || echo [FAIL] streamlit-extras
python -c "import streamlit_aggrid; print('[OK] streamlit-aggrid')" 2>nul || echo [FAIL] streamlit-aggrid

echo.
echo ============================================
echo Installation Complete!
echo ============================================
echo.
echo You can now run: streamlit run app.py
echo.
pause


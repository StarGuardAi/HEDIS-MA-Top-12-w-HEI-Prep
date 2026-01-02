@echo off
echo Activating Python 3.11 environment...

call C:\Users\reich\anaconda3\Scripts\activate.bat hedis_py311

echo Starting Streamlit app...

streamlit run app.py

pause


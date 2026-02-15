@echo off
chcp 65001 >nul
cd /d "%~dp0"
python FINAL_FIX_SCRIPT.py
pause


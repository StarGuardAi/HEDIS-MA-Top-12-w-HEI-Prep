@echo off
REM Quick Python Installation Test

echo ========================================
echo Python Installation Test
echo ========================================
echo.

echo Testing Python installation...
echo.

REM Test 1: Check if python command works
echo [Test 1] Checking python command...
python --version 2>nul
if errorlevel 1 (
    echo FAILED: Python not found in PATH
    echo.
    echo Solutions:
    echo 1. Reinstall Python from python.org
    echo 2. Make sure to CHECK "Add python.exe to PATH"
    echo 3. Close and reopen PowerShell after installation
    echo.
    goto :search_python
) else (
    echo PASSED: Python is installed and in PATH
    python --version
)
echo.

REM Test 2: Check pip
echo [Test 2] Checking pip...
pip --version 2>nul
if errorlevel 1 (
    echo FAILED: pip not found
) else (
    echo PASSED: pip is installed
    pip --version
)
echo.

REM Test 3: Check Python location
echo [Test 3] Python installation location...
python -c "import sys; print(sys.executable)" 2>nul
echo.

echo ========================================
echo All tests passed! Ready for setup.
echo Run: setup_project.bat
echo ========================================
echo.
pause
exit /b 0

:search_python
echo.
echo Searching for Python installations...
echo.

REM Check common Python installation locations
if exist "C:\Program Files\Python311\python.exe" (
    echo Found: C:\Program Files\Python311\python.exe
    echo Add this to PATH manually
)
if exist "C:\Program Files\Python312\python.exe" (
    echo Found: C:\Program Files\Python312\python.exe
    echo Add this to PATH manually
)
if exist "C:\Users\%USERNAME%\AppData\Local\Programs\Python\Python311\python.exe" (
    echo Found: C:\Users\%USERNAME%\AppData\Local\Programs\Python\Python311\python.exe
    echo Add this to PATH manually
)
if exist "C:\Users\%USERNAME%\AppData\Local\Programs\Python\Python312\python.exe" (
    echo Found: C:\Users\%USERNAME%\AppData\Local\Programs\Python\Python312\python.exe
    echo Add this to PATH manually
)

echo.
echo See setup_python.md for manual PATH setup instructions
echo.
pause


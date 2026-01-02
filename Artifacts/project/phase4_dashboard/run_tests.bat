@echo off
REM Test runner for Windows
REM Usage: run_tests.bat [test_type]

set TEST_TYPE=%1
if "%TEST_TYPE%"=="" set TEST_TYPE=all

if "%TEST_TYPE%"=="all" (
    pytest tests/ --cov=utils --cov=pages --cov-report=html --cov-report=term-missing --cov-fail-under=80
) else if "%TEST_TYPE%"=="coverage" (
    pytest tests/ --cov=utils --cov=pages --cov-report=html --cov-report=term-missing --cov-fail-under=80
) else (
    pytest tests/ -m %TEST_TYPE% --cov=utils --cov=pages --cov-report=html --cov-report=term-missing
)

pause


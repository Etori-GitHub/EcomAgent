@echo off
cd /d %~dp0
echo Step 1: Script started
echo Current directory: %CD%
echo.

REM Check python exists
if exist "python\python.exe" (
    echo Step 2: Python found at python\python.exe
) else (
    echo Step 2: ERROR - Python not found!
    pause
    exit /b 1
)

echo Step 3: Checking Chrome...
set "CHROME_PATH=C:\Program Files\Google\Chrome\Application\chrome.exe"
if exist "%CHROME_PATH%" (
    echo Chrome found: %CHROME_PATH%
) else (
    echo Chrome not found
)

echo Step 4: About to start server...
echo.
python\python.exe run_viewer.py
echo.
echo Step 5: Server stopped or script ended
pause
@echo off
cd /d %~dp0
echo ============================================================
echo EcomAgent Data Viewer
echo ============================================================
echo.

set CHROME_PATH=
if exist "C:\Program Files\Google\Chrome\Application\chrome.exe" set CHROME_PATH=C:\Program Files\Google\Chrome\Application\chrome.exe
if exist "C:\Program Files (x86)\Google\Chrome\Application\chrome.exe" if not defined CHROME_PATH set CHROME_PATH=C:\Program Files (x86)\Google\Chrome\Application\chrome.exe
if exist "%LOCALAPPDATA%\Google\Chrome\Application\chrome.exe" if not defined CHROME_PATH set CHROME_PATH=%LOCALAPPDATA%\Google\Chrome\Application\chrome.exe

set TIKTOK_CHROME_DIR=C:\chrome-tiktok
if not exist "%TIKTOK_CHROME_DIR%" mkdir "%TIKTOK_CHROME_DIR%"

if defined CHROME_PATH (
    echo [STARTING] Chrome with WebUI...
    start "" "%CHROME_PATH%" --remote-debugging-port=9222 --user-data-dir="%TIKTOK_CHROME_DIR%" http://127.0.0.1:8000
)

echo [STARTING] EcomAgent server...
echo.
python\python.exe run_viewer.py
pause

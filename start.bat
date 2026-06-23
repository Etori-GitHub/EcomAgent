@echo off
chcp 65001 >nul
cd /d %~dp0
echo ============================================================
echo EcomAgent Data Viewer
echo ============================================================
echo.

set OPENCLAW_PATH=
if exist "%USERPROFILE%\.openclaw" (
    set "OPENCLAW_PATH=%USERPROFILE%\.openclaw"
    echo [OK] OpenClaw detected: %OPENCLAW_PATH%
) else (
    echo [INFO] OpenClaw not installed
)
echo.

echo [CHECKING] Database initialization...
set NEED_INIT=0

if not exist "data\amazon.db" set NEED_INIT=1
if not exist "data\tiktok.db" set NEED_INIT=1
if not exist "data\product_master.db" set NEED_INIT=1
if not exist "data\categories.db" set NEED_INIT=1

if "%NEED_INIT%"=="1" (
    echo [INIT] Initializing databases...
    python\python.exe scripts\init_all_tables.py
    python\python.exe scripts\init_category_tables.py
    echo [OK] Databases initialized
) else (
    echo [OK] All databases exist
)
echo.

set CHROME_PATH=
if exist "C:\Program Files\Google\Chrome\Application\chrome.exe" set CHROME_PATH=C:\Program Files\Google\Chrome\Application\chrome.exe
if exist "C:\Program Files (x86)\Google\Chrome\Application\chrome.exe" if not defined CHROME_PATH set CHROME_PATH=C:\Program Files (x86)\Google\Chrome\Application\chrome.exe
if exist "%LOCALAPPDATA%\Google\Chrome\Application\chrome.exe" if not defined CHROME_PATH set CHROME_PATH=%LOCALAPPDATA%\Google\Chrome\Application\chrome.exe

set TIKTOK_CHROME_DIR=C:\chrome-tiktok
if not exist "%TIKTOK_CHROME_DIR%" mkdir "%TIKTOK_CHROME_DIR%"

echo [STARTING] EcomAgent server...
start /B python\python.exe run_viewer.py

timeout /t 3 /nobreak >nul

if defined CHROME_PATH (
    echo [STARTING] Chrome with WebUI...
    start "" "%CHROME_PATH%" --remote-debugging-port=9222 --user-data-dir="%TIKTOK_CHROME_DIR%" http://127.0.0.1:8000
)

pause

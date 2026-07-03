@echo off
cd /d %~dp0
echo ============================================================
echo EcomAgent Setup
echo ============================================================
echo.

REM Check if python directory exists
if exist "python\python.exe" (
    echo [OK] Python environment already exists.
    goto :start_server
)

echo [INSTALLING] Setting up Python environment...
echo.

REM Download Python embeddable package (3.11.9)
set PYTHON_VERSION=3.11.9
set PYTHON_URL=https://www.python.org/ftp/python/%PYTHON_VERSION%/python-%PYTHON_VERSION%-embed-amd64.zip
set PYTHON_ZIP=python-embed.zip

echo Downloading Python %PYTHON_VERSION%...
powershell -Command "Invoke-WebRequest -Uri '%PYTHON_URL%' -OutFile '%PYTHON_ZIP%' -UseBasicParsing"

if not exist "%PYTHON_ZIP%" (
    echo [ERROR] Failed to download Python.
    pause
    exit /b 1
)

echo Extracting Python...
powershell -Command "Expand-Archive -Path '%PYTHON_ZIP%' -DestinationPath 'python' -Force"

REM Enable pip by modifying _pth file
echo Enabling pip...
echo Lib>> python\python311._pth
echo Lib\site-packages>> python\python311._pth
echo.>> python\python311._pth

REM Download get-pip.py
echo Installing pip...
powershell -Command "Invoke-WebRequest -Uri 'https://bootstrap.pypa.io/get-pip.py' -OutFile 'python\get-pip.py' -UseBasicParsing"
python\python.exe python\get-pip.py --no-warn-script-location

REM Install dependencies
echo Installing dependencies...
python\python.exe -m pip install --no-warn-script-location -r requirements.txt

REM Install Playwright Chromium
echo Installing Playwright Chromium...
python\python.exe -m playwright install chromium

REM Clean up
del %PYTHON_ZIP%
del python\get-pip.py

echo.
echo [OK] Python environment setup complete.
echo.

:start_server
echo ============================================================
echo Starting EcomAgent...
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
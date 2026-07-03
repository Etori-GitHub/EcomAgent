@echo off
cd /d %~dp0
echo ============================================================
echo EcomAgent Setup
echo ============================================================
echo.

REM Step 1: Check if Python exists
if not exist "python\python.exe" (
    echo [INSTALLING] Setting up Python environment...
    echo.
    goto :install_python
)

REM Step 2: Check if pip exists
python\python.exe -c "import pip" 2>nul
if %errorlevel% neq 0 (
    echo [INFO] pip not found, installing pip...
    echo.
    goto :install_pip
)

REM Step 3: Check if dependencies are installed
python\python.exe -c "import fastapi" 2>nul
if %errorlevel%==0 (
    echo [OK] Dependencies already installed.
    goto :install_playwright
)

REM Dependencies missing, install them
echo [INFO] Dependencies not found, installing...
echo.
goto :install_deps

:install_python
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

del %PYTHON_ZIP%

echo.
echo [OK] Python installed.
echo.
goto :install_pip

:install_pip
REM Ensure _pth is configured
if exist "python\python311._pth" (
    findstr "Lib\\site-packages" python\python311._pth >nul
    if %errorlevel% neq 0 (
        echo Configuring python311._pth...
        echo Lib>> python\python311._pth
        echo Lib\site-packages>> python\python311._pth
        echo.>> python\python311._pth
    )
)

REM Download and install pip
echo Installing pip...
powershell -Command "Invoke-WebRequest -Uri 'https://bootstrap.pypa.io/get-pip.py' -OutFile 'python\get-pip.py' -UseBasicParsing"
python\python.exe python\get-pip.py --no-warn-script-location
del python\get-pip.py

echo.
echo [OK] pip installed.
echo.
goto :install_deps

:install_deps
REM Install dependencies
echo [INSTALLING] Dependencies...
python\python.exe -m pip install --no-warn-script-location -r requirements.txt
echo.

:install_playwright
REM Install/Update Playwright Chromium
echo [CHECKING] Playwright Chromium...
python\python.exe -m playwright install chromium
echo.

:init_database
REM Initialize databases if not exist
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

REM Create images directories
if not exist "data\images\amazon" mkdir "data\images\amazon"
if not exist "data\images\tiktok" mkdir "data\images\tiktok"
echo [OK] Images directories created
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
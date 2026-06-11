#!/bin/bash
cd "$(dirname "$0")"
echo "============================================================"
echo "EcomAgent Setup"
echo "============================================================"
echo ""

# Check if python directory exists
if [ -f "python/bin/python3" ]; then
    echo "[OK] Python environment already exists."
    source python/bin/activate
    goto start_server
fi

echo "[INSTALLING] Setting up Python environment..."
echo ""

# Check Python 3.11+
if command -v python3.11 &> /dev/null; then
    PYTHON_CMD=python3.11
elif command -v python3 &> /dev/null; then
    PYTHON_CMD=python3
else
    echo "[ERROR] Python 3.11+ not found. Please install Python first."
    exit 1
fi

# Create virtual environment
echo Creating virtual environment...
$PYTHON_CMD -m venv python
source python/bin/activate

# Install dependencies
echo Installing dependencies...
pip install -r requirements.txt

echo ""
echo "[OK] Python environment setup complete."
echo ""

:start_server
echo "============================================================"
echo "Starting EcomAgent..."
echo "============================================================"
echo ""

# Find Chrome
CHROME_PATH="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
if [ ! -f "$CHROME_PATH" ]; then
    CHROME_PATH=$(which google-chrome || which chromium-browser)
fi

TIKTOK_CHROME_DIR="$HOME/.chrome-tiktok"
mkdir -p "$TIKTOK_CHROME_DIR"

if [ -f "$CHROME_PATH" ]; then
    echo "[STARTING] Chrome with WebUI..."
    "$CHROME_PATH" --remote-debugging-port=9222 --user-data-dir="$TIKTOK_CHROME_DIR" http://127.0.0.1:8000 &
fi

echo "[STARTING] EcomAgent server..."
echo ""
python/bin/python run_viewer.py
#!/bin/bash
cd "$(dirname "$0")"
echo "============================================================"
echo "EcomAgent Data Viewer"
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
python3 run_viewer.py
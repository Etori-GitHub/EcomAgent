#!/bin/bash
cd "$(dirname "$0")"

echo "============================================================"
echo "EcomAgent Data Viewer"
echo "============================================================"
echo ""

# 激活虚拟环境
if [ -f "python/bin/activate" ]; then
    source python/bin/activate
elif [ -f "python/bin/python3" ]; then
    # 虚拟环境存在但没有 activate 脚本
    PYTHON_CMD="./python/bin/python3"
fi

# 确定 Python 命令
if [ -z "$PYTHON_CMD" ]; then
    PYTHON_CMD="python3"
fi

# 检查数据库初始化
echo "[CHECKING] Database initialization..."
NEED_INIT=0

if [ ! -f "data/amazon.db" ]; then
    echo "[MISSING] amazon.db"
    NEED_INIT=1
fi
if [ ! -f "data/tiktok.db" ]; then
    echo "[MISSING] tiktok.db"
    NEED_INIT=1
fi
if [ ! -f "data/product_master.db" ]; then
    echo "[MISSING] product_master.db"
    NEED_INIT=1
fi
if [ ! -f "data/categories.db" ]; then
    echo "[MISSING] categories.db"
    NEED_INIT=1
fi

if [ "$NEED_INIT" -eq 1 ]; then
    echo ""
    echo "[INIT] Initializing databases..."
    $PYTHON_CMD scripts/init_all_tables.py
    $PYTHON_CMD scripts/init_category_tables.py
    echo "[OK] Databases initialized"
else
    echo "[OK] All databases exist"
fi
echo ""

# 查找 Chrome
CHROME_PATH=""
if [ -f "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" ]; then
    CHROME_PATH="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
elif [ -f "/Applications/Chromium.app/Contents/MacOS/Chromium" ]; then
    CHROME_PATH="/Applications/Chromium.app/Contents/MacOS/Chromium"
elif command -v google-chrome &> /dev/null; then
    CHROME_PATH=$(which google-chrome)
elif command -v chromium-browser &> /dev/null; then
    CHROME_PATH=$(which chromium-browser)
fi

# 创建 TikTok Chrome 数据目录
TIKTOK_CHROME_DIR="$HOME/.chrome-tiktok"
mkdir -p "$TIKTOK_CHROME_DIR"

# 启动 Chrome（如果找到）
if [ -n "$CHROME_PATH" ]; then
    echo "[STARTING] Chrome (调试端口 9222)..."
    "$CHROME_PATH" --remote-debugging-port=9222 --user-data-dir="$TIKTOK_CHROME_DIR" http://127.0.0.1:8000 &
    sleep 2
else
    echo "[INFO] 未找到 Chrome，请手动打开浏览器访问 http://127.0.0.1:8000"
fi

echo "[STARTING] EcomAgent 服务..."
echo ""
$PYTHON_CMD run_viewer.py
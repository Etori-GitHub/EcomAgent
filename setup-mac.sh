#!/bin/bash
cd "$(dirname "$0")"

echo "=== EcomAgent macOS Setup ==="

# 1. 解压 Python
if [ -f "python-mac/python-macos.tar.gz" ]; then
    echo "Extracting Python..."
    mkdir -p python
    tar -xzf python-mac/python-macos.tar.gz -C python --strip-components=1
    rm -rf python-mac
else
    echo "Python archive not found. Please download it first."
    exit 1
fi

# 2. 安装依赖
echo "Installing dependencies..."
./python/bin/pip3 install fastapi uvicorn sqlalchemy click pydantic playwright

# 3. 设置权限
chmod +x start.sh

echo ""
echo "=== Setup Complete ==="
echo "Double-click 'start.sh' or run: ./start.sh"

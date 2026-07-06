#!/bin/bash
cd "$(dirname "$0")"

echo "============================================================"
echo "EcomAgent macOS Setup"
echo "============================================================"
echo ""

# 检查系统 Python
if ! command -v python3 &> /dev/null; then
    echo "[ERROR] 未找到 Python 3，请先安装"
    echo "推荐使用 Homebrew: brew install python@3.11"
    exit 1
fi

PYTHON_VERSION=$(python3 --version 2>&1)
echo "检测到: $PYTHON_VERSION"

# 删除旧的损坏的 Python 目录
if [ -d "python" ]; then
    echo "清理旧的 Python 环境..."
    rm -rf python
fi

# 创建新的虚拟环境
echo "创建虚拟环境..."
python3 -m venv python

# 激活虚拟环境
source python/bin/activate

# 安装依赖
echo "安装依赖..."
pip install --trusted-host pypi.org --trusted-host files.pythonhosted.org -r requirements.txt

# 安装 Playwright 浏览器
echo ""
echo "安装 Playwright 浏览器..."
playwright install chromium

# 检查配置文件
echo ""
echo "检查配置文件..."
if [ ! -f "config/api_keys.json" ]; then
    if [ -f "config/api_keys.template.json" ]; then
        echo "[CONFIG] 从模板创建 api_keys.json..."
        cp config/api_keys.template.json config/api_keys.json
        echo "[CONFIG] Created api_keys.json"
    else
        echo "[WARN] api_keys.template.json 不存在"
    fi
else
    echo "[OK] api_keys.json 已存在"
fi

# 设置权限
chmod +x start.sh

echo ""
echo "============================================================"
echo "[OK] 设置完成！"
echo "============================================================"
echo ""
echo "运行方式："
echo "  ./start.sh"
echo ""
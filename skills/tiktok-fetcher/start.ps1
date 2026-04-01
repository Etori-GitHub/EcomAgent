#!/usr/bin/env powershell
# -*- coding: utf-8 -*-
"""
TikTok Shop 抓取启动脚本
"""

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  TikTok Shop 数据抓取工具" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# 获取脚本所在目录
$scriptPath = Split-Path -Parent $MyInvocation.MyCommand.Path
$projectRoot = Split-Path -Parent $scriptPath

Write-Host "[INFO] 项目根目录: $projectRoot" -ForegroundColor Yellow
Write-Host "[INFO] 抓取脚本: $scriptPath\src\fetch_tiktok_categories.py" -ForegroundColor Yellow
Write-Host ""

# 检查 Python 是否可用
try {
    python --version | Out-Null
    Write-Host "[OK] Python 可用" -ForegroundColor Green
} catch {
    Write-Host "[ERR] Python 不可用，请安装 Python 3.11+" -ForegroundColor Red
    exit 1
}

# 检查 Playwright 是否安装
Write-Host "[INFO] 检查 Playwright 安装..." -ForegroundColor Yellow
try {
    python -c "from playwright.sync_api import sync_playwright" | Out-Null
    Write-Host "[OK] Playwright 已安装" -ForegroundColor Green
} catch {
    Write-Host "[WARN] Playwright 未安装，正在安装..." -ForegroundColor Yellow
    python -m pip install playwright
    python -m playwright install chromium
}

# 运行抓取脚本
Write-Host ""
Write-Host "[INFO] 开始抓取 TikTok Shop 数据..." -ForegroundColor Yellow
Write-Host "[INFO] 请耐心等待，脚本会自动抓取多个分类的数据" -ForegroundColor Yellow
Write-Host ""

python "$scriptPath\src\fetch_tiktok_categories.py"

Write-Host ""
Write-Host "[OK] 抓取完成！" -ForegroundColor Green
Write-Host "[INFO] 数据保存位置: $projectRoot\output\scraping\" -ForegroundColor Yellow
Write-Host ""

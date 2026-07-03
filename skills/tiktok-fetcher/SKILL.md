---
name: tiktok
description: 抓取 TikTok Shop 热销榜单数据。使用浏览器自动化抓取数据并保存到本地 JSON 文件。
---
# TikTok Shop 热销榜单抓取

**当前版本支持抓取 28 个分类的热销商品数据。**

专门用于抓取 TikTok Shop 热销榜单数据，使用浏览器自动化抓取并提取各分类的商品信息。**数据保存到 JSON 文件**！

## 技术特点

- ✅ **复用登录状态**：使用 persistent context 复用 Chrome 登录状态，避免反机器人验证
- ✅ **智能选择器**：自动定位类目列表，提取 28 个分类
- ✅ **数据输出**：每个分类保存为独立 JSON 文件
- ✅ **反爬策略**：随机等待、模拟真实用户行为

## 数据输出位置

```bash
# 数据输出目录
code/EcomAgent/output/scraping/

# JSON 文件命名格式
tiktok_分类英文名_YYYYMMDD_HHMMSS.json

# 示例
tiktok_beauty_personal_care_20260509_104700.json
tiktok_electronics_20260509_104730.json
tiktok_womenswear_underwear_20260509_104800.json
```

## 数据格式

```json
{
  "metadata": {
    "platform": "tiktok",
    "category": "美妆个护",
    "category_slug": "beauty_personal_care",
    "category_url": "https://www.tiktok.com/shop/c/beauty-personal-care/601450",
    "scraped_at": "2026-05-09T10:47:00.123456",
    "scraped_date": "2026-05-09",
    "scraped_time": "10:47:00",
    "total_items": 150
  },
  "products": [
    {
      "tag": "DIV",
      "className": "product-card-classname...",
      "text": "商品名称 $19.99",
      "price": "19.99",
      "rating": "4.8"
    }
  ]
}
```

**字段说明**：
- `metadata.platform`: 平台标识（"tiktok"）
- `metadata.category`: 分类中文名
- `metadata.category_slug`: 分类英文名（用于文件名）
- `metadata.category_url`: 分类页面 URL
- `metadata.scraped_at`: 抓取时间（ISO 8601 格式）
- `metadata.scraped_date`: 抓取日期（用于数据库分组）
- `metadata.scraped_time`: 抓取时间（用于数据库分组）
- `metadata.total_items`: 商品总数
- `products`: 商品列表数组

## 反爬对策（重要）

TikTok Shop 有严格的反爬机制，如果遇到 `code:100000` 封禁响应，请使用以下方案：

### 方案 1：Playwright Stealth（推荐先试）

```bash
# 安装依赖
pip install playwright-stealth

# 运行脚本
python code/EcomAgent/skills/tiktok-fetcher/src/fetch_tiktok_stealth.py
```

**特点**：
- 使用 playwright-stealth 插件隐藏自动化特征
- 强化反检测参数
- 模拟真实用户行为

### 方案 2：undetected-chromedriver（效果最强）

```bash
# 安装依赖
pip install undetected-chromedriver

# 运行脚本
python code/EcomAgent/skills/tiktok-fetcher/src/fetch_tiktok_uc.py
```

**特点**：
- 专门绑过反爬检测
- 效果最强，但需要换用 Selenium 语法

### 方案 3：Android App 抓包（终极方案）

如果以上方案都失败，可以考虑通过 TikTok Shop Android App 抓包分析 API。

---

## 使用步骤

### 快速抓取（推荐）

使用项目根目录的 `daily_fetch.py` 统一入口：

```bash
# 完整流程（抓取 + 导入 + 图片下载）
python scripts/daily_fetch.py tiktok
```

### 手动抓取（开发调试）

需先启动 Chrome 调试端口：

```bash
# Windows
chrome.exe --remote-debugging-port=9222 --user-data-dir="C:\chrome-tiktok"

# macOS
/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --remote-debugging-port=9222 --user-data-dir="/tmp/chrome-tiktok"
```

然后运行：

```bash
python skills/tiktok-fetcher/src/fetch_tiktok_categories.py
```

**注意**：手动模式需要单独导入数据：

```bash
python scripts/daily_fetch.py import
```

### 1. 安装依赖

```bash
cd code/EcomAgent/skills/tiktok-fetcher
pip install -r requirements.txt
playwright install chromium

# 可选：安装反爬增强
pip install playwright-stealth undetected-chromedriver
```

### 2. 运行抓取脚本

```bash
# 标准版（可能被封）
python code/EcomAgent/skills/tiktok-fetcher/src/fetch_tiktok_categories.py

# Stealth 版（推荐）
python code/EcomAgent/skills/tiktok-fetcher/src/fetch_tiktok_stealth.py

# UC 版（效果最强）
python code/EcomAgent/skills/tiktok-fetcher/src/fetch_tiktok_uc.py
```

### 3. 数据自动保存

脚本会自动：
1. 访问 TikTok Shop 首页
2. 提取 28 个分类 URL
3. 逐个抓取分类页面数据
4. 保存到 `output/scraping/` 目录

---

## 类目列表

脚本会自动提取以下 28 个分类：

1. 美妆个护
2. 女装与女士内衣
3. 男装与男士内衣
4. 手机与数码
5. 时尚配件
6. 收藏品
7. 家居用品
8. 厨房用品
9. 鞋靴
10. 运动与户外
...（共 28 个）

类目列表会保存到：`skills/tiktok-fetcher/screenshots/categories.json`

---

## 注意事项

- **首次运行需要手动登录**：确保 Chrome Profile 1 已登录 TikTok 账号
- **页面加载时间**：每个分类页面需要 10-30 秒加载时间
- **反爬机制**：已添加随机等待和模拟真实用户行为
- **数据格式**：当前版本提取基础信息，后续可优化选择器提取更详细数据

## 文件结构

```
tiktok-fetcher/
├── SKILL.md                    # 技能说明文档
├── docs/                       # 开发文档
├── src/
│   ├── fetch_tiktok_categories.py  # 主抓取脚本（重构版）
│   └── old/                    # 旧代码参考
├── screenshots/                # 截图和类目列表
└── requirements.txt
```

---

## 开发文档

详细的技术方案、开发经验和扩展说明请参考：
- [开发文档](docs/TikTok-SHOP-SCRAPER.md)

---

_Good luck out there. Make it count._

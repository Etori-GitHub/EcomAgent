---
name: tiktok
description: 抓取TikTok Shop热销榜单数据。使用浏览器自动化抓取数据并保存到本地JSON文件。
---
# TikTok Shop 热销榜单抓取

**当前版本支持抓取多个分类的热销商品数据。**

专门用于抓取 TikTok Shop 热销榜单数据，使用浏览器自动化抓取并提取各分类的商品信息。**数据保存到 JSON 文件**！

## 数据输出位置

```bash
# 数据输出目录
code/EcomAgent/output/scraping/

# JSON 文件命名格式
tiktok_分类名_YYYYMMDD_HHMMSS.json
```

## 数据格式

```json
[
  {
    "rank": 1,
    "name": "商品名称",
    "price": 19.99,
    "rating": 4.8,
    "rating_count": 1234,
    "sold_count": 5678,
    "category": "Electronics",
    "subcategory": "Best Sellers in Electronics"
  }
]
```

## 使用步骤

### 1. 安装依赖

```bash
cd code/EcomAgent/skills/tiktok-fetcher
pip install -r requirements.txt
playwright install chromium
```

### 2. 运行抓取脚本

```bash
# 抓取多个分类的热销数据
python code/EcomAgent/skills/tiktok-fetcher/src/fetch_tiktok_categories.py
```

### 3. 数据自动保存

脚本会自动将数据保存到 `code/EcomAgent/output/scraping/` 目录，按分类和时间戳命名！

---

## 注意事项

- 脚本使用浏览器自动化（Playwright）模拟真实用户操作
- 已添加随机等待机制，避免触发反爬
- 建议在非高峰时段运行
- TikTok Shop 的页面结构可能随时间变化，如抓取失败请检查页面选择器

## 文件结构

```
tiktok-fetcher/
├── SKILL.md                    # 技能说明文档
├── docs/                       # 开发文档
├── src/
│   └── fetch_tiktok_categories.py  # 抓取脚本
└── requirements.txt
```

---

_Good luck out there. Make it count._

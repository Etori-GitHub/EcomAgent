---
name: amazon
description: 抓取亚马逊热销榜单数据。使用 Python 脚本抓取数据并保存到 output 目录的 JSON 文件。
---
# 亚马逊热销榜单抓取

**当前版本支持抓取 6 个主要分类的前 2 页数据，共 600 个商品。**

专门用于抓取亚马逊热销榜单数据，使用 Python 脚本抓取并提取各分类的商品信息。**数据保存到 JSON 文件**！

## 数据输出位置

```bash
# 数据输出目录
code/EcomAgent/output/scraping/

# JSON 文件命名格式
amazon_分类名_YYYYMMDD_HHMMSS.json
```

## 数据格式

```json
[
  {
    "rank": 1,
    "name": "商品名称",
    "asin": "B08JHCVHTY",
    "price": 11.99,
    "rating": 4.4,
    "rating_count": 273537,
    "category": "Electronics",
    "subcategory": "Best Sellers in Electronics"
  }
]
```

## 使用步骤

### 1. 安装依赖

```bash
cd code/EcomAgent/skills/amazon-fetcher
pip install -r requirements.txt
playwright install chromium
```

### 2. 运行抓取脚本

```bash
# 抓取 6 个主要分类的前2页（共600个商品）
python code/EcomAgent/skills/amazon-fetcher/src/fetch_amazon_main_categories.py
```

### 3. 数据自动保存

脚本会自动将数据保存到 `code/EcomAgent/output/scraping/` 目录，按分类和时间戳命名！

---

## 注意事项

- 脚本使用浏览器自动化（Playwright）模拟真实用户操作
- 已添加随机等待机制，避免触发反爬
- 建议在非高峰时段运行
- 当前版本支持 6 个主要分类，每分类 2 页（100 个商品）
- 数据保存在 `output/scraping/` 目录，便于统一管理

## 开发文档

详细的技术方案、开发经验和扩展说明请参考：
- [开发文档](docs/AMAZON-BESTSELLER-SCRAPER.md)

## 文件结构

```
amazon-fetcher/
├── SKILL.md                    # 技能说明文档
├── docs/
│   └── AMAZON-BESTSELLER-SCRAPER.md  # 开发文档
├── src/
│   └── fetch_amazon_main_categories.py  # 抓取 6 个主要分类（推荐使用）
└── requirements.txt
```

---

_Good luck out there. Make it count._

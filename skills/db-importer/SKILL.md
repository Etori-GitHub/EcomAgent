# EcomAgent Database Importer Skill

_定时将抓取数据导入数据库_

## 功能描述

扫描 `output/scraping` 目录，读取 JSON 文件，将数据导入对应的 SQLite 数据库。

## 触发方式

**开发阶段**: 手动触发
```python
python src/import_to_db.py
```

**生产阶段**: 定时任务（后续配置 cron）

## 数据流向

```
JSON files (output/scraping/) 
    ↓
Parser (Amazon/TikTok)
    ↓
Database (data/amazon.db / data/tiktok.db)
```

## 字段映射

### Amazon

**products 表**:
- `asin` (UNIQUE) → `product_id`
- `name` → `name`
- `category` → `category`
- `subcategory` → `subcategory`
- `platform` → `'amazon'` (default)

**daily_sales 表**:
- `rank` → `rank`
- `price` → `price`
- `rating` → `rating`
- `rating_count` → `rating_count`
- `date` → `date` (from filename)
- `product_id` → FK to products

### TikTok

**tiktok_products 表**:
- `name` → `name`
- `category` → `category` (from metadata)
- `shop_name` → (not available in current format)
- `platform` → `'tiktok'` (default)

**tiktok_daily_sales 表**:
- `price` → `price`
- `original_price` → `original_price`
- `rating` → `rating`
- `rating_count` → (not available)
- `sales_count` → `sold` (parsed from "X.XK 已售出")
- `date` → `date` (from filename)
- `category` → `category`

## 注意事项

1. **去重**: 使用 UNIQUE 约束防止重复插入
2. **日期**: 从文件名提取日期（格式：`YYYYMMDD`）
3. **错误处理**: 单个文件失败不影响其他文件
4. **日志**: 输出导入统计信息

## 文件结构

```
skills/db-importer/
├── SKILL.md
├── src/
│   └── import_to_db.py
└── docs/
    └── DB-IMPORTER.md
```

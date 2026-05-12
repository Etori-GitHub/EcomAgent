# Database Importer Documentation

_详细的技术文档_

## 架构设计

### 目录结构

```
EcomAgent/
├── data/
│   ├── amazon.db          # Amazon 数据库
│   └── tiktok.db          # TikTok 数据库
├── output/
│   └── scraping/          # JSON 数据文件
│       ├── amazon_*.json
│       └── tiktok_*.json
└── skills/
    └── db-importer/
        ├── SKILL.md
        ├── src/
        │   └── import_to_db.py
        └── docs/
            └── DB-IMPORTER.md
```

### 数据流程

```
1. 爬虫抓取 → JSON 文件 (output/scraping/)
2. Importer 扫描 → 解析 JSON
3. 去重检查 → 插入数据库 (data/*.db)
```

## 数据库 Schema

### Amazon (amazon.db)

**products 表**:
```sql
CREATE TABLE products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    asin TEXT UNIQUE,
    name TEXT NOT NULL,
    platform TEXT DEFAULT 'amazon',
    category TEXT,
    subcategory TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

**daily_sales 表**:
```sql
CREATE TABLE daily_sales (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    product_id INTEGER NOT NULL,
    date DATE NOT NULL,
    timestamp DATETIME NOT NULL,
    price REAL,
    rank INTEGER,
    rating REAL,
    rating_count INTEGER,
    category TEXT,
    subcategory TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (product_id) REFERENCES products(id)
);
```

### TikTok (tiktok.db)

**tiktok_products 表**:
```sql
CREATE TABLE tiktok_products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    product_id TEXT UNIQUE,
    name TEXT NOT NULL,
    platform TEXT DEFAULT 'tiktok',
    shop_name TEXT,
    category TEXT,
    subcategory TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

**tiktok_daily_sales 表**:
```sql
CREATE TABLE tiktok_daily_sales (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    product_id INTEGER NOT NULL,
    date DATE NOT NULL,
    timestamp DATETIME NOT NULL,
    price REAL,
    original_price REAL,
    discount TEXT,
    rating REAL,
    rating_count INTEGER,
    sales_count TEXT,
    category TEXT,
    subcategory TEXT,
    shop_name TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (product_id) REFERENCES tiktok_products(id)
);
```

## 使用方法

### 手动运行

```bash
cd C:\Users\Etroi\.openclaw\workspace\code\EcomAgent
python skills/db-importer/src/import_to_db.py
```

### 预期输出

```
############################################################
# EcomAgent Database Importer
# Started at: 2026-05-09 15:59:00
############################################################

Found 25 JSON files to process

Amazon files: 9
TikTok files: 16

============================================================
Importing Amazon data from: amazon_Electronics_20260410_160750.json
============================================================
✅ Amazon import complete!
   Total products in DB: 1234
   Total sales records: 5678
   New sales inserted: 100
   Skipped (duplicates): 0

...

############################################################
# Import complete at: 2026-05-09 16:00:00
############################################################
```

## 去重策略

### Amazon
- 使用 `asin` 作为唯一标识
- `INSERT OR IGNORE` 防止重复插入 products
- 每次运行都会插入新的 daily_sales 记录（按日期）

### TikTok
- 使用 `name` 作为唯一标识（因为 API 不提供 product_id）
- 同一文件内去重（seen_names set）
- 跨文件不去重（允许同名产品多次出现）

## 错误处理

1. **文件解析失败**: 跳过该文件，继续处理其他文件
2. **数据库连接失败**: 抛出异常，终止程序
3. **字段类型错误**: 使用 try-except 转换，失败则设为 None

## 扩展性

### 添加新平台

1. 在 `scan_and_import()` 中添加平台检测逻辑
2. 创建 `import_<platform>()` 方法
3. 更新数据库 schema（如果需要）

### 添加定时任务

后续可以配置 cron job:

```python
schedule.every().day.at("09:00").do(importer.scan_and_import)
```

## 注意事项

1. **日期格式**: 从文件名提取，格式 `YYYYMMDD`
2. **销售数量**: TikTok 的 "57.8K 已售出" 需要解析
3. **价格精度**: 使用 REAL 类型，注意浮点数精度
4. **性能**: 大量数据时考虑批量插入

# DB Importer Skill

_将抓取数据导入数据库_

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
# Started at: 2026-05-09 16:04:50
############################################################

Found 28 JSON files to process

Amazon files: 9
TikTok files: 19

============================================================
Importing Amazon data from: amazon_Electronics_20260410_160750.json
============================================================
✅ Amazon import complete!
   Total products in DB: 165
   Total sales records: 500
   New sales inserted: 100
   Skipped (duplicates): 0

...

############################################################
# Import complete at: 2026-05-09 16:04:50
############################################################
```

## 功能说明

1. **自动扫描**: 扫描 `output/scraping` 目录下的所有 JSON 文件
2. **平台识别**: 根据文件名前缀 (`amazon_` 或 `tiktok_`) 自动识别平台
3. **去重处理**: 
   - Amazon: 使用 `asin` 去重
   - TikTok: 使用 `name` 去重（同一文件内）
4. **错误容错**: 单个文件失败不影响其他文件

## 数据库位置

- Amazon: `data/amazon.db`
- TikTok: `data/tiktok.db`

## 下一步

后续可以配置定时任务（cron）自动运行：

```python
# 每天 9:00 自动运行
schedule.every().day.at("09:00").do(importer.scan_and_import)
```

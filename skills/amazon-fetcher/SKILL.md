---
name: amazon
description: 抓取亚马逊热销数据。使用浏览器自动化打开亚马逊热销榜并提取商品信息。自动保存到EcomAgent/data/amazon.db数据库。使用命令：/amazon
---
# 亚马逊热销数据抓取

专门用于抓取亚马逊热销榜数据，使用浏览器自动化打开网页并提取热销商品信息。**自动保存到SQLite数据库**！

## 数据库位置

```bash
# 数据库路径（相对路径，跨平台兼容）
code/EcomAgent/data/amazon.db

# 数据库表结构
products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    asin TEXT UNIQUE,
    name TEXT NOT NULL,
    platform TEXT DEFAULT 'amazon',
    category TEXT,
    subcategory TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
)
daily_sales (
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
)
```

## 使用示例

### 1. 打开亚马逊热销榜

```bash
browser action:navigate targetUrl:"https://www.amazon.com/gp/bestsellers"
```

### 2. 提取数据

```bash
# 获取网页快照
browser action:snapshot

# 从快照中提取商品信息：
# - 商品排名 (rank)
# - ASIN (商品唯一标识)
# - 商品名称
# - 评分 (rating)
# - 评论数 (rating_count)
# - 价格 (price)
```

### 3. 自动保存到SQLite

**抓取数据后会自动保存到 `code/EcomAgent/data/amazon.db` 数据库！**

```bash
# 数据库路径（相对路径，跨平台兼容）
code/EcomAgent/data/amazon.db

# 查询热销商品
sqlite3 code/EcomAgent/data/amazon.db "SELECT p.name, ds.price, ds.rating, ds.rating_count, ds.rank FROM daily_sales ds JOIN products p ON ds.product_id = p.id ORDER BY ds.rank LIMIT 10"
```

### 4. 完整流程示例

```bash
# 1. 打开亚马逊热销榜
browser action:navigate targetUrl:"https://www.amazon.com/gp/bestsellers"

# 2. 等待页面加载
browser action:snapshot

# 3. 提取热销商品列表
# 从快照中提取前10个商品的信息

# 4. 自动保存到SQLite数据库
# 使用 save_data.py 脚本保存数据
python code/EcomAgent/save_data.py

# 5. 查询结果
sqlite3 code/EcomAgent/data/amazon.db "SELECT p.name, ds.price, ds.rating, ds.rating_count, ds.rank FROM daily_sales ds JOIN products p ON ds.product_id = p.id ORDER BY ds.rank LIMIT 10"
```

---

## 数据保存策略

### SQLite数据库（自动保存）

**抓取数据后自动保存到 `data/amazon.db`！**

```bash
# 数据库路径（相对路径，跨平台兼容）
code/EcomAgent/data/amazon.db

# 查询热销商品
sqlite3 code/EcomAgent/data/amazon.db "SELECT p.name, ds.price, ds.rating, ds.rating_count, ds.rank FROM daily_sales ds JOIN products p ON ds.product_id = p.id ORDER BY ds.rank LIMIT 10"
```

### 本地文件保存（可选）

```bash
# JSON格式（结构化数据）
write content:"{...}" file_path:"code/EcomAgent/output/amazon_bestsellers.json"

# CSV格式（Excel兼容）
# 商品名称,销量,价格,链接
# "Owala水瓶",10000,$29.99,https://amazon.com/...
```

---

## 自动化脚本

### fetch_amazon_bestsellers.py（主脚本）

```python
# 抓取亚马逊热销榜前100条数据
python code/EcomAgent/src/skills/fetch_amazon_bestsellers.py

# 脚本功能：
# 1. 初始化数据库表
# 2. 打开亚马逊热销榜网页
# 3. 获取网页快照
# 4. 提取热销商品信息
# 5. 批量保存到SQLite数据库
# 6. 返回 Top 100 热销商品
```

**脚本特点：**
- ✓ 静默模式运行，只输出关键信息
- ✓ 自动去重（同名商品更新销量和价格）
- ✓ 支持扩展到100条商品数据
- ✓ 简洁的输出，减少冗余过程回复

### save_data.py（数据保存脚本）

```python
# 保存到SQLite数据库
python code/EcomAgent/save_data.py

# 脚本功能：
# 1. 初始化数据库表
# 2. 批量保存商品数据
# 3. 查询热销商品
```

### view_db.py（查看数据库脚本）

```python
# 查看数据库内容
python code/EcomAgent/view_db.py

# 脚本功能：
# 1. 显示商品表
# 2. 显示快照表
```

---

## 关键技术点（重要！）

### 1. **浏览器自动化（非爬虫）**
- **必须使用 OpenClaw 的 `browser` 工具**
- **禁止使用 Python 爬虫库**（如 `requests`、`BeautifulSoup`）
- **原因**：避免反爬机制，模拟真实用户操作

### 2. **翻页方式**
- **错误方式**：`browser(action="act", kind="click", ref="e507")` → 返回 `request required` 错误
- **正确方式**：`browser(action="navigate", targetUrl="https://...?pg=2")` → 直接导航

### 3. **商品唯一标识**
- **使用 `asin`**（亚马逊商品ID）作为唯一标识
- **原因**：商品名称可能变化，但 ASIN 不变

### 4. **同一天多次抓取**
- **策略**：删除旧数据，保留最新的一条
- **SQL**：`DELETE FROM daily_sales WHERE product_id = ? AND date = ?`

### 5. **数据库表结构**
- **products 表**：存储商品基础信息（使用 `asin` 唯一约束）
- **daily_sales 表**：存储每日快照（包含 rank、rating、rating_count）

### 6. **翻页限制**
- **Electronics 分类只有 2 页**
- **必须先检查分页导航**，确认总页数
- **如果 "Next page" 是纯文本（不是链接），说明没有下一页**

---

## 注意事项

- 需要浏览器控制权限
- 亚马逊可能有反爬机制
- 建议在非高峰时段抓取
- 提取数据时注意网页结构变化
- SQLite自动保存无需额外配置
- 数据库保存在 `code/EcomAgent/data/amazon.db`（相对路径，跨平台兼容）
- 使用 `code/EcomAgent/src/skills/fetch_amazon_bestsellers.py` 脚本自动保存
- 当前为模拟数据，需完善网页解析逻辑才能抓取真实数据

---

## 数据库查询示例

```sql
-- 查询 Top 10 热销商品
SELECT p.name, ds.price, ds.rating, ds.rating_count, ds.rank 
FROM daily_sales ds 
JOIN products p ON ds.product_id = p.id 
ORDER BY ds.rank 
LIMIT 10;

-- 查询某商品的历史快照
SELECT ds.date, ds.price, ds.rank, ds.rating, ds.rating_count 
FROM daily_sales ds 
JOIN products p ON ds.product_id = p.id 
WHERE p.asin = 'B08JHCVHTY' 
ORDER BY ds.date DESC;

-- 查询某天的所有商品
SELECT p.name, ds.price, ds.rank, ds.rating, ds.rating_count 
FROM daily_sales ds 
JOIN products p ON ds.product_id = p.id 
WHERE ds.date = '2026-03-24' 
ORDER BY ds.rank;
```

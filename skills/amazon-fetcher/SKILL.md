---
name: amazon-fetcher
description: 抓取亚马逊热销数据。使用浏览器自动化打开亚马逊热销榜并提取商品信息。自动保存到EcomAgent/data/amazon.db数据库。使用命令：/fetch_amazon_bestsellers
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
    name TEXT NOT NULL UNIQUE,
    sales INTEGER,
    price REAL,
    platform TEXT DEFAULT 'amazon',
    url TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
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
# - 商品名称
# - 销量/点赞数
# - 价格
# - 商品链接
```

### 3. 自动保存到SQLite

**抓取数据后会自动保存到 `code/EcomAgent/data/amazon.db` 数据库！**

```bash
# 数据库路径（相对路径，跨平台兼容）
code/EcomAgent/data/amazon.db

# 数据库表结构
products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,
    sales INTEGER,
    price REAL,
    platform TEXT DEFAULT 'amazon',
    url TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
)

# 查询热销商品
sqlite3 code/EcomAgent/data/amazon.db "SELECT * FROM products ORDER BY sales DESC LIMIT 10"
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
# 使用 save_to_sqlite.py 脚本保存数据
python code/EcomAgent/src/skills/save_to_sqlite.py

# 5. 查询结果
sqlite3 code/EcomAgent/data/amazon.db "SELECT * FROM products ORDER BY sales DESC LIMIT 10"
```

---

## 数据保存策略

### SQLite数据库（自动保存）

**抓取数据后自动保存到 `data/amazon.db`！**

```bash
# 数据库路径（相对路径，跨平台兼容）
code/EcomAgent/data/amazon.db

# 数据库表结构
products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,
    sales INTEGER,
    price REAL,
    platform TEXT DEFAULT 'amazon',
    url TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
)

# 查询热销商品
sqlite3 code/EcomAgent/data/amazon.db "SELECT * FROM products ORDER BY sales DESC LIMIT 10"
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

### save_to_sqlite.py（备用脚本）

```python
# 保存到SQLite数据库
python code/EcomAgent/src/skills/save_to_sqlite.py

# 脚本功能：
# 1. 初始化数据库表
# 2. 批量保存商品数据
# 3. 查询热销商品
```

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

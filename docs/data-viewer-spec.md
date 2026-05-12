# Data Viewer 详细设计

_Web UI 数据展示功能的技术规格_

## 概述

Data Viewer 是一个基于 Web 的数据展示工具，用于查看 Amazon 和 TikTok Shop 的抓取数据。

## 技术架构

### 后端

- **框架**: FastAPI
- **数据库**: SQLite (直接使用 `data/amazon.db` 和 `data/tiktok.db`)
- **端口**: 8000 (可配置)
- **异步**: 支持异步请求

### 前端

- **技术**: 原生 HTML + CSS + JavaScript
- **框架**: 无 (轻量级)
- **样式**: Tailwind CSS (CDN)
- **图表**: Chart.js (可选，未来扩展)

### CLI 工具

- **命令**: `ecomagent serve`
- **实现**: Python 脚本 + `setuptools` entry points
- **平台**: Windows (`.bat` + `.exe`), Linux/Mac (shell script)

## 功能需求

### 1. 首页 (Dashboard)

**内容**:
- 数据概览统计
  - Amazon: 产品数、销售记录数、最后更新时间
  - TikTok: 产品数、销售记录数、最后更新时间
- 快速导航链接

**API**:
```python
GET /api/stats
```

**响应**:
```json
{
  "amazon": {
    "products": 328,
    "sales": 1800,
    "last_updated": "2026-05-09T16:05:47"
  },
  "tiktok": {
    "products": 570,
    "sales": 570,
    "last_updated": "2026-05-09T16:05:47"
  }
}
```

### 2. Amazon 产品列表

**内容**:
- 产品表格 (分页)
- 搜索/过滤功能
  - 按名称搜索
  - 按分类过滤
  - 按价格范围过滤

**API**:
```python
GET /api/amazon/products?page=1&limit=50&search=&category=&min_price=&max_price=
```

**响应**:
```json
{
  "data": [...],
  "pagination": {
    "page": 1,
    "limit": 50,
    "total": 328,
    "pages": 7
  }
}
```

### 3. TikTok 产品列表

**内容**:
- 产品表格 (分页)
- 搜索/过滤功能
  - 按名称搜索
  - 按分类过滤
  - 按价格范围过滤

**API**:
```python
GET /api/tiktok/products?page=1&limit=50&search=&category=&min_price=&max_price=
```

### 4. 销售记录列表

**内容**:
- 销售记录表格 (分页)
- 按日期筛选
- 按产品筛选

**API**:
```python
GET /api/amazon/sales?page=1&limit=50&date=&product_id=
GET /api/tiktok/sales?page=1&limit=50&date=&product_id=
```

## 页面结构

```
/ (首页)
├── /amazon (Amazon 数据)
│   ├── /products (产品列表)
│   └── /sales (销售记录)
└── /tiktok (TikTok 数据)
    ├── /products (产品列表)
    └── /sales (销售记录)
```

## 数据库 Schema 参考

### Amazon

**products 表**:
```sql
id, asin, name, platform, category, subcategory, created_at, updated_at
```

**daily_sales 表**:
```sql
id, product_id, date, timestamp, price, rank, rating, rating_count, category, subcategory, created_at
```

### TikTok

**tiktok_products 表**:
```sql
id, product_id, name, platform, shop_name, category, subcategory, created_at, updated_at
```

**tiktok_daily_sales 表**:
```sql
id, product_id, date, timestamp, price, original_price, discount, rating, rating_count, sales_count, category, subcategory, shop_name, created_at
```

## API 端点设计

### 基础路径

- `/api/amazon/products`
- `/api/amazon/sales`
- `/api/tiktok/products`
- `/api/tiktok/sales`
- `/api/stats`

### 查询参数

- `page`: 页码 (默认 1)
- `limit`: 每页数量 (默认 50, 最大 200)
- `search`: 搜索关键词
- `category`: 分类过滤
- `min_price`: 最低价格
- `max_price`: 最高价格
- `date`: 日期过滤 (YYYY-MM-DD)
- `product_id`: 产品 ID 过滤

## 前端实现

### HTML 结构

```html
<!DOCTYPE html>
<html>
<head>
    <title>EcomAgent - Data Viewer</title>
    <script src="https://cdn.tailwindcss.com"></script>
</head>
<body>
    <nav>...</nav>
    <main>
        <!-- 动态内容 -->
    </main>
    <script src="/static/js/app.js"></script>
</body>
</html>
```

### JavaScript 模块

- `app.js`: 主应用逻辑
- `api.js`: API 调用封装
- `utils.js`: 工具函数

## CLI 工具实现

### `ecomagent` 脚本

**Windows (ecomagent.bat)**:
```batch
@echo off
python -m src.data_viewer.cli %*
```

**Python CLI (`src/data_viewer/cli.py`)**:
```python
import click

@click.group()
def cli():
    pass

@cli.command()
@click.option('--host', default='0.0.0.0')
@click.option('--port', default=8000)
def serve(host, port):
    """启动 Web UI 服务"""
    from main import run_server
    run_server(host, port)

if __name__ == '__main__':
    cli()
```

## 开发计划

### Phase 3.1: 基础框架 (当前)

- [ ] 创建 `src/data_viewer/` 模块
- [ ] 实现 FastAPI 服务
- [ ] 创建基础 HTML 页面
- [ ] 实现 `/api/stats` 端点
- [ ] 创建 CLI 工具

### Phase 3.2: 数据展示

- [ ] Amazon 产品列表页
- [ ] TikTok 产品列表页
- [ ] 搜索/过滤功能
- [ ] 分页功能

### Phase 3.3: 优化完善

- [ ] 数据导出功能
- [ ] 响应式设计
- [ ] 性能优化
- [ ] 错误处理

## 部署说明

### 本地开发

```bash
# 安装依赖
pip install fastapi uvicorn sqlalchemy

# 启动服务
ecomagent serve
```

### 访问地址

- **本地**: http://localhost:8000
- **局域网**: http://<服务器 IP>:8000

## 注意事项

1. **数据库锁**: SQLite 是文件锁，并发写入可能有问题
   - 解决方案：只读模式，或使用 WAL 模式

2. **性能**: 大数据量时需要分页和索引
   - 解决方案：已实现分页，确保索引正确

3. **安全性**: 本地服务，无需认证
   - 未来扩展：添加基本认证

4. **跨平台**: CLI 工具需要支持 Windows/Linux/Mac
   - 解决方案：使用 `click` 库 + 多平台脚本

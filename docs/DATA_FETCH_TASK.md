# 数据抓取任务系统设计

## 概述

将数据抓取改造为「任务模式」，支持断点续抓、前端交互、类目管理。

## 数据库设计

### 1. categories.db（类目基础信息）

```sql
CREATE TABLE categories (
    id INTEGER PRIMARY KEY,
    platform TEXT NOT NULL,           -- 'amazon' / 'tiktok'
    name TEXT NOT NULL,
    url TEXT NOT NULL,
    enabled BOOLEAN DEFAULT 1,        -- 用户是否启用抓取
    added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_scraped_at TIMESTAMP,        -- 最后抓取时间
    last_products_count INTEGER,      -- 最后一次抓取商品数
    total_scrapes INTEGER DEFAULT 0,  -- 累计抓取次数
    total_products INTEGER DEFAULT 0, -- 累计抓取商品数
    UNIQUE(platform, name)
);

CREATE INDEX idx_categories_platform ON categories(platform);
CREATE INDEX idx_categories_enabled ON categories(enabled);
```

### 2. category_daily.db（每日抓取记录）

```sql
CREATE TABLE category_daily (
    id INTEGER PRIMARY KEY,
    category_id INTEGER NOT NULL,
    date TEXT NOT NULL,               -- 'YYYY-MM-DD'
    products_count INTEGER,           -- 当日抓取商品数
    task_id TEXT,                     -- 关联的任务ID
    scraped_at TIMESTAMP,
    FOREIGN KEY (category_id) REFERENCES categories(id),
    UNIQUE(category_id, date)
);

CREATE INDEX idx_daily_date ON category_daily(date);
CREATE INDEX idx_daily_category ON category_daily(category_id);
```

### 3. tasks.db（任务记录）

```sql
CREATE TABLE tasks (
    id INTEGER PRIMARY KEY,
    task_id TEXT UNIQUE NOT NULL,
    platform TEXT NOT NULL,
    status TEXT DEFAULT 'running',    -- running/completed/failed/cancelled
    started_at TIMESTAMP,
    finished_at TIMESTAMP,
    total_categories INTEGER,
    completed_categories INTEGER,
    total_products INTEGER,
    error_message TEXT
);

CREATE INDEX idx_tasks_platform ON tasks(platform);
CREATE INDEX idx_tasks_status ON tasks(status);
```

## 任务状态文件

路径：`output/tasks/{task_id}.json`

```json
{
  "task_id": "amazon_20260530_132100",
  "platform": "amazon",
  "status": "running",
  "started_at": "2026-05-30T13:21:00",
  "total_categories": 28,
  "completed_categories": 5,
  "current_category": "Electronics",
  "categories": [
    { "name": "Electronics", "url": "...", "status": "done", "products_count": 20 },
    { "name": "Books", "url": "...", "status": "running", "products_count": null },
    { "name": "Toys", "url": "...", "status": "pending", "products_count": null }
  ]
}
```

## 后端 API

| 接口 | 说明 |
|------|------|
| `GET /api/categories/{platform}` | 获取类目列表（含抓取状态） |
| `POST /api/categories/{platform}/refresh` | 刷新类目列表（从平台重新获取） |
| `PUT /api/categories/{id}/enabled` | 启用/禁用类目 |
| `POST /api/tasks/{platform}/fetch` | 开始抓取任务 |
| `GET /api/tasks/{platform}/status` | 获取当前任务进度 |
| `GET /api/tasks/{task_id}` | 获取历史任务详情 |
| `POST /api/tasks/{task_id}/cancel` | 取消任务 |
| `POST /api/tasks/{task_id}/resume` | 续抓失败的任务 |

## 前端交互

### 数据抓取卡片（可展开）

1. 点击「数据抓取」展开
2. 调用 API 获取类目列表
3. 如果类目表为空或超过 24h 未更新 → 提示用户「刷新类目」
4. 展示类目列表，每行显示：
   - 复选框（启用/禁用）
   - 类目名称
   - 抓取状态：`今日已抓 X 个` / `上次抓取：MM-DD HH:mm`
5. 点击「开始抓取」→ 创建任务，只抓取启用的类目

### 展开逻辑

- 每次展开时检查 `categories` 表是否有数据
- 如果空或 `last_scraped_at` > 24h，提示用户「刷新类目」
- 新类目自动加入，`enabled=1` 默认抓取

## 抓取逻辑

### 优先级规则

1. 用户禁用的类目（`enabled=0`）不抓
2. 每天只抓一次（当天已抓的类目跳过）
3. 任务中途失败，下次续抓未完成的类目

### 断点续抓

1. 启动任务 → 检查是否有未完成任务
2. 有则加载任务文件，继续未完成的类目
3. 每个类目完成后立即更新任务文件
4. 全部完成 → 任务标记 `completed`，触发数据导入

### 数据导入时机

- 每个类目抓完立即导入（而不是等全部完成）
- 避免大量数据丢失风险

## 文件结构

```
EcomAgent/
├── data/
│   ├── categories.db          # 类目基础信息
│   ├── category_daily.db      # 每日抓取记录
│   └── tasks.db               # 任务记录
├── output/
│   ├── tasks/                 # 任务状态文件
│   │   └── {task_id}.json
│   ├── scraping/              # 待导入数据
│   └── imported/              # 已导入数据
└── skills/
    ├── amazon-fetcher/
    │   └── src/fetch_amazon_task.py  # 新：任务模式脚本
    └── tiktok-fetcher/
        └── src/fetch_tiktok_task.py  # 新：任务模式脚本
```

## 实现步骤

1. [ ] 创建数据库表
2. [ ] 实现类目管理 API
3. [ ] 改造抓取脚本为任务模式
4. [ ] 实现断点续抓逻辑
5. [ ] 前端添加数据抓取卡片
6. [ ] 实现进度展示

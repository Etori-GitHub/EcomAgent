# EcomAgent 开发文档

本文档面向开发者，介绍项目架构设计、数据库设计、API 设计和功能规划。

---

## 架构设计

### 整体架构

```
┌─────────────────────────────────────────────────────────────┐
│                        Web UI (8000)                         │
│  ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐           │
│  │ 商品总库 │ │ 商品追踪 │ │ 今日TOP │ │ 商品趋势 │           │
│  └────┬────┘ └────┬────┘ └────┬────┘ └────┬────┘           │
│       └───────────┴───────────┴───────────┘                │
│                           │                                  │
│                    FastAPI Backend                          │
│                           │                                  │
└───────────────────────────┼─────────────────────────────────┘
                            │
        ┌───────────────────┼───────────────────┐
        │                   │                   │
   ┌────┴────┐        ┌─────┴─────┐       ┌─────┴─────┐
   │ Amazon  │        │  TikTok   │       │  Product  │
   │   DB    │        │    DB     │       │  Master   │
   └─────────┘        └───────────┘       └───────────┘
        │                   │                   │
        └───────────────────┴───────────────────┘
                            │
                    ┌───────┴───────┐
                    │  DB Importer  │
                    └───────┬───────┘
                            │
                    ┌───────┴───────┐
                    │  JSON Files   │
                    └───────┬───────┘
                            │
        ┌───────────────────┼───────────────────┐
        │                   │                   │
   ┌────┴────┐        ┌─────┴─────┐
   │ Amazon  │        │  TikTok   │
   │ Fetcher │        │  Fetcher  │
   └─────────┘        └───────────┘
```

### 数据流向

```
抓取脚本 → JSON 文件 → DB Importer → SQLite 数据库 → FastAPI → Web UI
```

---

## 数据库设计

### 商品主库 (product_master.db)

统一管理所有平台商品，通过 `ecom_code` 唯一标识。

**product_master 表**

| 字段 | 类型 | 说明 |
|------|------|------|
| id | INTEGER | 主键 |
| ecom_code | TEXT | 唯一标识（ECAMxxx / ETKxxx） |
| platform | TEXT | 平台（amazon/tiktok） |
| name | TEXT | 商品名称 |
| short_name | TEXT | 中文简称 |
| category | TEXT | 分类 |
| price | REAL | 价格 |
| rating | REAL | 评分 |
| sales_count | INTEGER | 销量 |
| product_url | TEXT | 商品链接 |
| image_url | TEXT | 图片 URL |
| local_image_path | TEXT | 本地图片路径 |
| first_seen_at | DATETIME | 首次发现时间 |
| last_updated_at | DATETIME | 最后更新时间 |

### Amazon 数据库 (amazon.db)

**products 表**

| 字段 | 类型 | 说明 |
|------|------|------|
| id | INTEGER | 主键 |
| master_id | INTEGER | 关联主库 ID |
| asin | TEXT | Amazon ASIN |
| name | TEXT | 商品名称 |
| search_keyword | TEXT | 搜索关键词 |
| category | TEXT | 分类 |
| url | TEXT | 商品链接 |

**daily_sales 表**

| 字段 | 类型 | 说明 |
|------|------|------|
| id | INTEGER | 主键 |
| product_id | INTEGER | 关联商品 ID |
| date | DATE | 日期 |
| timestamp | DATETIME | 时间戳 |
| price | REAL | 价格 |
| rating | REAL | 评分 |
| rank | INTEGER | 排名 |
| sales_count | INTEGER | 销量 |

### TikTok 数据库 (tiktok.db)

**tiktok_products 表**

| 字段 | 类型 | 说明 |
|------|------|------|
| id | INTEGER | 主键 |
| master_id | INTEGER | 关联主库 ID |
| tiktokshop_id | TEXT | TikTok Shop ID |
| name | TEXT | 商品名称 |
| search_keyword | TEXT | 搜索关键词 |
| category | TEXT | 分类 |
| url | TEXT | 商品链接 |

**tiktok_daily_sales 表**

| 字段 | 类型 | 说明 |
|------|------|------|
| id | INTEGER | 主键 |
| product_id | INTEGER | 关联商品 ID |
| date | DATE | 日期 |
| timestamp | DATETIME | 时间戳 |
| price | REAL | 价格 |
| rating | REAL | 评分 |
| sales_count | INTEGER | 销量 |

> 注意：TikTok 没有 `rank` 字段

---

## API 设计

### 商品相关

| 端点 | 方法 | 说明 |
|------|------|------|
| `/api/product-master` | GET | 商品列表（支持搜索、过滤、排序、分页） |
| `/api/categories` | GET | 分类列表（按平台分组） |
| `/api/tracked-products` | GET | 追踪商品列表 |
| `/api/product-trend/{ecom_code}` | GET | 商品趋势数据 |
| `/api/sales-trend/{ecom_code}` | GET | 销量趋势小图数据 |

### 统计相关

| 端点 | 方法 | 说明 |
|------|------|------|
| `/api/stats` | GET | 数据概览统计 |
| `/api/amazon/top-by-category` | GET | Amazon TOP 榜 |
| `/api/tiktok/top-by-category` | GET | TikTok TOP 榜 |

### 配置相关

| 端点 | 方法 | 说明 |
|------|------|------|
| `/api/config/list` | GET | 配置文件列表 |
| `/api/config/{name}` | GET | 配置文件内容 |

### OpenClaw 辅助相关

| 端点 | 方法 | 说明 |
|------|------|------|
| `/api/openclaw/settings` | GET | 获取 OpenClaw 辅助配置 |
| `/api/openclaw/settings` | PUT | 更新配置 |
| `/api/openclaw/setup` | POST | 检查 OpenClaw 安装状态 |
| `/api/openclaw/toggle` | POST | 启用/禁用定时任务 |

---

## OpenClaw 集成规范

### 任务命名规范

**所有 EcomAgent 相关的定时任务必须遵循以下命名规范：**

- **前缀**：`ecomagent-`
- **格式**：`ecomagent-<功能名>`
- **示例**：
  - `ecomagent-amazon-fetch` - Amazon 数据抓取
  - `ecomagent-translation` - 商品名称翻译
  - `ecomagent-image-download` - 图片下载

### 命名规范的原因

1. **便于识别**：所有 EcomAgent 任务一目了然
2. **便于管理**：可以通过 `WHERE name LIKE 'ecomagent-%'` 查询所有任务
3. **避免冲突**：与其他定时任务不会混淆
4. **便于清理**：批量删除或禁用时方便操作

### 添加新任务的流程

1. **定义任务名称**：使用 `ecomagent-` 前缀
2. **更新 `scripts/openclaw_config.py`**：
   - 在 `TASKS` 字典中添加新任务定义
   - 在 `DEFAULT_SETTINGS` 中添加默认配置
3. **更新 `src/data_viewer/main.py`**：
   - 在 `TASK_NAME_MAP` 中添加任务映射
4. **重启 EcomAgent**：启动脚本会自动检查并同步配置

### 配置文件

| 文件 | 说明 |
|------|------|
| `config/openclaw_settings.json` | EcomAgent 本地配置 |
| `~/.openclaw/state/openclaw.sqlite` | OpenClaw 定时任务数据库 |

### 手动命令

```bash
# 检查配置状态
python scripts/openclaw_config.py check

# 同步配置（启动时自动执行）
python scripts/openclaw_config.py setup

# 从 OpenClaw 同步状态到本地
python scripts/openclaw_config.py sync
```

---

## 前端架构

### 技术栈

- **框架**: Lit (Web Components)
- **语言**: TypeScript
- **构建**: Vite
- **样式**: CSS 变量系统（OpenClaw 风格）

### 目录结构

```
ui/
├── src/
│   ├── app.ts                 # 主应用（路由、全局状态）
│   ├── components/            # 组件
│   │   ├── sidebar.ts         # 侧边栏
│   │   ├── layout.ts          # 布局
│   │   └── header.ts          # 头部
│   ├── pages/                 # 页面
│   │   ├── dashboard.ts       # 数据概览
│   │   ├── product-master.ts  # 商品总库
│   │   ├── tracking.ts        # 商品追踪
│   │   ├── today-top.ts       # 今日TOP榜
│   │   ├── product-trend-page.ts  # 商品趋势
│   │   └── settings.ts        # 系统设置
│   ├── services/
│   │   └── api.ts             # API 函数
│   ├── types/
│   │   └── index.ts           # 类型定义
│   └── styles/
│       └── base.css           # 基础样式
├── package.json
├── tsconfig.json
└── vite.config.ts
```

### 全局状态管理

```typescript
// 页面导航
window.ecomagentNavigate(page: PageName)

// 获取当前页面
window.ecomagentGetCurrentPage(): PageName

// 监听页面变化
window.ecomagentOnPageChange(callback)

// 打开趋势页面
window.ecomagentOpenTrend(ecomCode: string, fromPage?: string)
```

---

## 功能规划

### 已完成

- [x] Amazon 数据抓取
- [x] TikTok 数据抓取
- [x] 数据库存储
- [x] Web UI 基础功能
- [x] 商品追踪
- [x] 商品趋势分析
- [x] 图片管理

### 进行中

- [ ] 事件追踪（图片变更、标题变更）
- [ ] 定时任务自动化

### 待开发

- [ ] 跨平台分析
- [ ] 数据导出
- [ ] 原始数据查看
- [ ] 1688 货源对接
- [ ] 妙手 ERP 对接
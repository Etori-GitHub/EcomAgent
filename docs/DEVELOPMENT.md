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
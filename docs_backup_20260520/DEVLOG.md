# EcomAgent Web UI 开发日志

## 2026-05-13 开发进度

### 完成功能

#### 1. UI 模块化重构 ✅
- 从单文件 `index.html` 重构为 Lit + TypeScript + Vite 架构
- 组件化：sidebar、layout、card
- 页面化：dashboard、product-master、tracking、today-top、settings、cross-platform、raw-data、export、product-trend
- 构建输出到 `src/data_viewer/static/`

#### 2. 核心问题修复 ✅
| 问题 | 原因 | 解决方案 |
|------|------|----------|
| 侧边栏折叠不生效 | Lit Boolean 属性反射不及时 | `requestUpdate('collapsed')` |
| 导航切换不生效 | Lit 事件不穿透 Shadow DOM | 全局函数 `window.ecomagentNavigate` |
| 侧边栏高亮不跟随 | 属性传递多层失效 | 全局状态管理 |
| 异步数据后视图不更新 | Lit 更新检测不及时 | 显式 `requestUpdate()` |

#### 3. 商品总库页面 ✅
- 统计卡片：总数、Amazon、TikTok、今日新增
- 搜索过滤：关键词、平台、分类
- 商品列表 + 分页
- 追踪按钮（☆/★）
- 趋势按钮（模态框）

#### 4. 商品追踪页面 ✅
- 追踪列表展示
- 删除按钮取消追踪
- 后端 API `/api/tracked-products?ids=xxx`

#### 5. 今日TOP榜页面 ✅
- Amazon/TikTok 分类切换
- 排名变化状态：
  - ↑数字（绿色）- 排名上升
  - ↓数字（红色）- 排名下降
  - 新（绿色标签）- 新入榜
- 分类置顶功能（★按钮，localStorage 保存）
- 后端 API 计算昨日排名对比

#### 6. 商品趋势页面 ✅
- 模态框方式展示（不跳转页面）
- 指标切换：评分、价格、排名
- 时间区间：7天、15天、30天
- 柱状图 + 数据表格
- 后端 API `/api/product-trend/{ecom_code}`

#### 7. 设置页面重构 ✅
- 每个配置一个大卡片
- 友好名称显示
- 分组区域布局
- 字段样式统一（标题160px + 输入框flex:1）

#### 8. 数据概览页面 ✅
- "销售记录"改为"抓取记录"
- Amazon/TikTok 卡片添加"更新数据"按钮
- 按钮与统计数据同行显示

---

### 文件结构

```
EcomAgent/
├── ui/                              # Lit + TypeScript 前端
│   ├── src/
│   │   ├── app.ts                   # 主应用
│   │   ├── components/              # 组件
│   │   │   ├── sidebar.ts           # 侧边栏
│   │   │   ├── layout.ts            # 布局
│   │   │   └── card.ts              # 卡片
│   │   ├── pages/                   # 页面
│   │   │   ├── dashboard.ts          # 数据概览
│   │   │   ├── product-master.ts     # 商品总库
│   │   │   ├── tracking.ts           # 商品追踪
│   │   │   ├── today-top.ts          # 今日TOP榜
│   │   │   ├── settings.ts           # 系统设置
│   │   │   ├── cross-platform.ts     # 跨平台分析
│   │   │   ├── raw-data.ts           # 原始数据
│   │   │   ├── export.ts             # 数据导出
│   │   │   └── product-trend.ts      # 商品趋势
│   │   ├── services/
│   │   │   └── api.ts                # API 函数
│   │   ├── types/                    # 类型定义
│   │   └── styles/                   # CSS
│   ├── package.json
│   ├── tsconfig.json
│   └── vite.config.ts
├── src/data_viewer/
│   ├── main.py                      # FastAPI 后端
│   └── static/                      # 构建输出
├── docs/
│   ├── TROUBLESHOOTING.md           # 踩坑文档
│   └── DEVLOG.md                    # 开发日志（本文件）
└── data/                            # 数据库
```

---

### 后端 API

| 端点 | 说明 |
|------|------|
| `GET /api/stats` | 数据概览统计 |
| `GET /api/product-master` | 商品总库列表 |
| `GET /api/tracked-products?ids=xxx` | 追踪商品列表 |
| `GET /api/amazon/top-by-category` | Amazon TOP 榜 |
| `GET /api/tiktok/top-by-category` | TikTok TOP 榜 |
| `GET /api/product-trend/{ecom_code}` | 商品趋势数据 |
| `GET /api/config/list` | 配置文件列表 |
| `GET /api/config/{name}` | 配置文件内容 |

---

### 待办事项

**Phase 3.4: 功能完善**
- [ ] 更新按钮对接实际抓取 API
- [ ] 跨平台分析页面实现
- [ ] 原始数据页面实现
- [ ] 数据导出页面实现
- [ ] 自定义日期选择（趋势页面）

---

### 技术要点

1. **全局状态管理**
   ```typescript
   window.ecomagentNavigate = (page) => { ... };
   window.ecomagentGetCurrentPage = () => _currentPage;
   window.ecomagentOnPageChange = (callback) => { ... };
   ```

2. **Lit Boolean 属性**
   ```typescript
   @property({ type: Boolean, reflect: true }) collapsed = false;
   // 修改后需调用
   this.requestUpdate('collapsed');
   ```

3. **模态框实现**
   ```typescript
   // 父组件管理状态
   @state() private showTrend = false;
   @state() private trendCode = '';
   
   // 子组件接收属性
   @property({ type: String }) ecomCode = '';
   
   // 监听属性变化
   updated(changedProperties) {
     if (changedProperties.has('ecomCode') && this.ecomCode) {
       this.loadTrendData();
     }
   }
   ```

4. **localStorage 使用**
   - `tracked-products` - 追踪商品列表
   - `pinned-categories` - 置顶分类列表
   - `theme` - 主题偏好

5. **TikTok 数据库差异**
   - 没有 `rank` 列，查询时需手动处理

---

### 启动方式

```bash
# 前端构建
cd ui && npm run build

# 后端启动
cd .. && python -m src.data_viewer.main

# 访问
http://localhost:8000
```

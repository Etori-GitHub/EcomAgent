# Web UI 技术方案

_前端架构和实现细节_

## 技术栈

### 前端
- **HTML5**: 语义化标签
- **CSS3**: CSS 变量 + Flexbox + Grid
- **JavaScript**: 原生 ES6+
- **字体**: Inter (Google Fonts)
- **图标**: SVG 内联

### 后端
- **FastAPI**: Python Web 框架
- **SQLite**: 数据库
- **Python 3.10+**: 运行环境

## 架构设计

### 文件结构
```
src/data_viewer/
├── __init__.py
├── main.py              # FastAPI 应用
├── cli.py               # CLI 工具
└── static/
    └── index.html       # 单页应用
```

### 单页应用 (SPA)
- 所有页面内容在 `index.html` 中定义
- 使用 `display: none/block` 切换页面
- JavaScript 动态加载数据

## CSS 变量系统

### 深色主题 (默认)
```css
:root {
  --bg: #0e1015;
  --bg-accent: #13151b;
  --bg-elevated: #191c24;
  --bg-hover: #1f2330;
  --text: #d4d4d8;
  --text-strong: #f4f4f5;
  --muted: #838387;
  --border: #1e2028;
  --accent: #ff5c5c;
  --card: #161920;
  --panel: #0e1015;
}
```

### 浅色主题
```css
body[data-theme-mode="light"] {
  --bg: #f8f9fa;
  --bg-accent: #f1f3f5;
  --bg-elevated: #ffffff;
  --text: #3c3c43;
  --text-strong: #1a1a1e;
  --muted: #6e6e73;
  --border: #e5e5ea;
  --accent: #dc2626;
  --card: #ffffff;
  --panel: #f8f9fa;
}
```

## 布局结构

### 整体布局
```
┌─────────────────────────────────────────┐
│                                         │
│  ┌──────────┐  ┌─────────────────────┐  │
│  │          │  │  状态栏             │  │
│  │  左侧    │  ├─────────────────────┤  │
│  │  导航栏  │  │                     │  │
│  │          │  │  内容区域           │  │
│  │          │  │                     │  │
│  └──────────┘  └─────────────────────┘  │
│                                         │
└─────────────────────────────────────────┘
```

### 导航栏结构
```
┌──────────────────┐
│ E EcomAgent      │  ← 品牌标识 + 折叠按钮
│ 数据可视化平台    │
├──────────────────┤
│ 📊 数据概览      │  ← 导航菜单
│ 📦 Amazon 数据   │
│ 🏆 Amazon 排名   │
│ 🎵 TikTok 数据   │
│ 🏆 TikTok 排名   │
│ 🔄 跨平台分析    │
│ 📈 销量趋势      │
│ 📥 数据导出      │
└──────────────────┘
```

### 折叠状态
```
┌──────┐
│  ◀   │  ← 展开按钮
├──────┤
│  📊  │
│  📦  │
│  🏆  │
│  🎵  │
│  🏆  │
│  🔄  │
│  📈  │
│  📥  │
└──────┘
```

## 交互设计

### 主题切换
```javascript
function toggleTheme() {
    const body = document.body;
    const currentMode = body.getAttribute('data-theme-mode');
    const newMode = currentMode === 'dark' ? 'light' : 'dark';
    body.setAttribute('data-theme-mode', newMode);
    localStorage.setItem('theme', newMode);
}
```

### 导航折叠
```javascript
function toggleSidebar() {
    const sidebar = document.getElementById('sidebar');
    sidebar.classList.toggle('collapsed');
}
```

### 页面切换
```javascript
function showPage(page) {
    // 隐藏所有页面
    document.querySelectorAll('.page').forEach(p => p.classList.add('hidden'));
    // 显示目标页面
    document.getElementById(page + '-page').classList.remove('hidden');
    // 更新导航高亮
    document.querySelectorAll('.sidebar-menu-item').forEach(item => {
        item.classList.remove('active');
    });
    document.getElementById('nav-' + page).classList.add('active');
}
```

## API 端点

### 已实现
- `GET /api/stats` - 数据概览统计
- `GET /api/amazon/products` - Amazon 产品列表
- `GET /api/tiktok/products` - TikTok 产品列表

### 待实现
- `GET /api/amazon/ranking` - Amazon 销量排名
- `GET /api/tiktok/ranking` - TikTok 销量排名
- `GET /api/cross-platform` - 跨平台分析
- `GET /api/trends` - 销量趋势
- `GET /api/export/{platform}/{format}` - 数据导出

## 性能优化

### 已实现
- CSS 变量减少重复代码
- SVG 内联减少 HTTP 请求
- 分页加载减少数据量

### 待实现
- 虚拟滚动 (大数据量)
- 图片懒加载
- 缓存策略
- CDN 加速

## 响应式设计

### 断点
- 桌面: > 1024px
- 平板: 768px - 1024px
- 手机: < 768px

### 适配策略
- 平板: 导航栏水平排列
- 手机: 导航栏收起，表格横向滚动

## 安全考虑

### 已实现
- XSS 防护: 数据转义
- CSRF 防护: SameSite Cookie

### 待实现
- 认证授权
- API 限流
- 日志审计

## 扩展计划

### 图表组件
- ECharts 或 Chart.js
- 销量趋势图
- 品类分布图
- 跨平台对比图

### 高级功能
- 数据筛选器
- 自定义报表
- 数据预警
- 导出模板

---

_本文档随项目进展持续更新_

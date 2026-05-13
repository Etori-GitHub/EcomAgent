# 开发踩坑记录

本文档记录 EcomAgent 开发过程中遇到的问题和解决方案。

---

## 2026-05-13 - 商品趋势模态框组件

### 需求
点击商品列表的"趋势"按钮，在当前页面弹出模态框显示商品趋势数据，而不是跳转到新页面。

### 实现方案

**1. 父组件管理模态框状态**
```typescript
// product-master.ts
@state() private showTrend = false;
@state() private trendCode = '';

private _showTrendModal(ecomCode: string) {
  this.trendCode = ecomCode;
  this.showTrend = true;
}

private _closeTrendModal() {
  this.showTrend = false;
  this.trendCode = '';
}
```

**2. 模态框 HTML 结构**
```typescript
render() {
  return html`
    <!-- 正常内容 -->
    
    <!-- 模态框 -->
    ${this.showTrend ? html`
      <div class="modal-overlay" @click=${this._closeTrendModal}>
        <div class="modal-content" @click=${(e) => e.stopPropagation()}>
          <button class="modal-close" @click=${this._closeTrendModal}>✕</button>
          <ea-product-trend ecomCode=${this.trendCode}></ea-product-trend>
        </div>
      </div>
    ` : ''}
  `;
}
```

**3. 子组件接收属性**
```typescript
// product-trend.ts
@property({ type: String }) ecomCode = '';

updated(changedProperties: Map<string, unknown>) {
  if (changedProperties.has('ecomCode') && this.ecomCode) {
    this.loadTrendData();
  }
}
```

### 注意事项
- 点击遮罩层关闭模态框，点击内容区阻止冒泡
- 子组件用 `@property` 接收参数，`updated` 监听变化
- 不要在 `connectedCallback` 里依赖 `ecomCode`，此时属性可能还未传入

---

## 2026-05-13 - TikTok 数据库字段差异

### 问题现象
查询 TikTok 趋势数据时报错：`sqlite3.OperationalError: no such column: rank`

### 问题原因
TikTok 和 Amazon 的数据库表结构不同：
- Amazon `daily_sales` 表有 `rank` 列
- TikTok `tiktok_daily_sales` 表没有 `rank` 列

### 解决方案
查询 TikTok 数据时，手动构造返回数据，`rank` 设为 `None`：
```python
elif platform == 'tiktok':
    tcursor.execute("""
        SELECT date, price, rating
        FROM tiktok_daily_sales
        WHERE product_id = ? AND date >= ? AND date <= ?
        ORDER BY date DESC
    """, (product_id, start_date, end_date))
    for r in tcursor.fetchall():
        trend.append({
            'date': r['date'],
            'price': r['price'],
            'rating': r['rating'],
            'rank': None  # TikTok 没有排名数据
        })
```

---

## 2026-05-13 - 今日TOP榜排名变化功能

### 需求
在今日TOP榜页面添加：
1. 排名变化状态（上升/下降/新入榜）
2. 分类置顶功能

### 实现方案

**1. 后端 API 返回排名变化**
```python
# 查询昨天的排名
cursor.execute("""
    SELECT rank FROM daily_sales 
    WHERE product_id = ? AND date = ?
""", (product['id'], yesterday))
yesterday_rank = cursor.fetchone()

if yesterday_rank:
    product['rank_change'] = yesterday_rank['rank'] - product['rank']  # 正数=上升
    product['is_new'] = False
else:
    product['is_new'] = True
    product['rank_change'] = None
```

**2. 前端显示排名变化**
```typescript
private _renderRankChange(change?: number, isNew?: boolean) {
  if (isNew) return html`<span class="new-badge">新</span>`;
  if (change === null) return null;
  if (change > 0) return html`<span class="rank-change up">↑${change}</span>`;
  if (change < 0) return html`<span class="rank-change down">↓${Math.abs(change)}</span>`;
  return null;
}
```

**3. 置顶功能（localStorage）**
```typescript
@state() private pinnedCategories: Set<string> = new Set();

private _togglePin(category: string) {
  if (this.pinnedCategories.has(category)) {
    this.pinnedCategories.delete(category);
  } else {
    this.pinnedCategories.add(category);
  }
  localStorage.setItem('pinned-categories', JSON.stringify([...this.pinnedCategories]));
  this.requestUpdate();
}
```

---

## 2026-05-13 - Lit Boolean 属性反射问题

### 问题现象
侧边栏折叠按钮点击后，`collapsed` 状态在切换，但 CSS `:host([collapsed])` 样式不生效。

### 问题原因
Lit 的 `@property({ type: Boolean, reflect: true })` 在修改 Boolean 属性时，属性反射可能不及时或不完整：
- `collapsed = true` → 属性值是空字符串 `""`（HTML Boolean 属性的标准行为）
- `collapsed = false` → 属性被移除

但直接赋值 `this.collapsed = !this.collapsed` 后，Lit 可能没有立即触发属性反射。

### 解决方案
修改 Boolean 属性后，手动调用 `requestUpdate('propertyName')` 强制触发属性反射和重新渲染。

```typescript
@property({ type: Boolean, reflect: true }) collapsed = false;

private _onToggle() {
  this.collapsed = !this.collapsed;
  this.requestUpdate('collapsed'); // 关键！
}
```

### 调试方法
```typescript
console.log('collapsed attribute:', this.getAttribute('collapsed'));
// true → "" (空字符串)
// false → null (属性被移除)
```

### CSS 选择器写法
```css
/* 属性存在时生效，无论值是什么 */
:host([collapsed]) {
  width: 60px;
}
```

### 参考资料
- [Lit Properties - Boolean attributes](https://lit.dev/docs/components/properties/#boolean-attributes)
- Boolean attributes in HTML: 存在即为 true，值通常为空字符串

---

## 2026-05-13 - Lit 事件冒泡问题

### 问题现象
sidebar 组件点击导航项后，父组件 app.ts 没有收到事件，页面不切换。

### 问题原因
Lit 的自定义事件默认不会穿透 Shadow DOM 边界，需要设置 `composed: true` 和 `bubbles: true`。

### 解决方案
**方案一：事件穿透 Shadow DOM**
```typescript
this.dispatchEvent(new CustomEvent('nav', {
  detail: page,
  bubbles: true,
  composed: true  // 关键！
}));
```

**方案二：全局函数（最终采用）**
```typescript
// app.ts
window.ecomagentNavigate = (page: PageName) => {
  this._page = page;
};

// sidebar.ts
private _onNavClick(page: PageName) {
  if (window.ecomagentNavigate) {
    window.ecomagentNavigate(page);
  }
}
```

方案二更简单直接，适合简单状态管理，不依赖 Lit 事件系统。

---

## 2026-05-13 - Playwright 复用已有浏览器

### 需求
抓取数据时复用已打开的 Chrome 浏览器，保留登录状态，避免重复启动。

### 解决方案

**1. 启动 Chrome（带远程调试端口）**
```bash
chrome.exe --remote-debugging-port=9222 --user-data-dir="C:\Users\Etroi\chrome-debug-profile"
```

**2. Playwright 连接到已有浏览器**
```python
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    # 连接到已有浏览器
    browser = p.chromium.connect_over_cdp("http://localhost:9222")
    
    # 使用已有上下文（保留登录状态）
    context = browser.contexts[0] if browser.contexts else browser.new_context()
    
    # 新建标签页
    page = context.new_page()
    
    # ... 抓取逻辑 ...
    
    # 不要关闭 browser，只关闭页面
    page.close()
```

### 注意事项
- Chrome 必须用 `--remote-debugging-port=9222` 启动
- 建议用独立的 `--user-data-dir` 避免影响日常浏览
- 脚本结束时只 `page.close()`，不要 `browser.close()`

---

## 2026-05-13 - Lit 属性传递 vs 全局状态管理

### 问题现象
点击导航项后，页面内容切换了，但侧边栏的高亮状态没有跟着变化，始终停留在第一个项上。

### 问题原因
Lit 的属性传递机制在多层组件嵌套时容易出问题：
1. `app.ts` → `layout.ts` → `sidebar.ts` 三层传递
2. 属性更新后，子组件可能不会重新渲染
3. `.currentPage=${value}` 和 `currentPage=${value}` 的区别容易混淆

### 解决方案
**放弃属性传递，改用全局状态管理**：

```typescript
// app.ts - 定义全局函数
const _listeners: Set<(page: PageName) => void> = new Set();
let _currentPage: PageName = 'dashboard';

window.ecomagentNavigate = (page: PageName) => {
  _currentPage = page;
  _listeners.forEach(fn => fn(page));
};

window.ecomagentGetCurrentPage = () => _currentPage;

window.ecomagentOnPageChange = (callback) => {
  _listeners.add(callback);
};
```

```typescript
// sidebar.ts - 直接监听全局状态
constructor() {
  super();
  window.ecomagentOnPageChange((page) => {
    this._currentPage = page;
    this.requestUpdate();
  });
  this._currentPage = window.ecomagentGetCurrentPage();
}
```

### 优势
1. **简单直接**：不依赖 Lit 的属性传递机制
2. **实时同步**：所有组件都监听同一个全局状态
3. **易于调试**：可以在控制台直接调用 `window.ecomagentNavigate('xxx')` 测试

### 适用场景
- 简单应用的状态管理
- 跨多层组件的状态同步
- 不想引入复杂状态管理库（如 Redux、MobX）时

### 注意事项
- 全局函数需要在组件加载前定义
- 监听器需要在组件销毁时清理（可选）
- 不要滥用全局状态，复杂应用还是用正规状态管理

---

## 2026-05-13 - Lit 异步数据加载后视图不更新

### 问题现象
页面加载时一直显示转圈圈（loading 状态），数据加载完成后视图没有更新。

### 问题原因
Lit 的 `@state` 装饰器会自动触发更新，但在复杂的异步流程中（特别是循环里的多个 `await`），Lit 的更新检测可能不够及时。

### 解决方案
异步数据加载完成后，显式调用 `requestUpdate()` 确保视图更新：

```typescript
async loadData() {
  this.loading = true;
  try {
    // 多个异步操作...
    const result = await api.getData();
    this.data = result;
  } catch (e) {
    console.error(e);
  } finally {
    this.loading = false;
    this.requestUpdate();  // 关键！
  }
}
```

### 经验教训
- 异步数据加载完成后，最好显式调用 `requestUpdate()`
- 尤其是在 `Promise.all` + 循环 `await` 的复杂场景
- 加调试日志有助于定位问题

---

```markdown
## YYYY-MM-DD - 问题标题

### 问题现象
描述遇到的具体问题。

### 问题原因
分析问题的根本原因。

### 解决方案
给出具体的代码或配置修改。

### 注意事项
列出需要注意的细节。

### 参考资料
相关文档或链接。
```

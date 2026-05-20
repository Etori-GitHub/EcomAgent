# EcomAgent 开发笔记

记录开发过程中遇到的技术难点和解决方案，积累经验。

---

## SVG 图表开发

### 问题：XY 轴标签不显示

**现象**：SVG 折线图渲染成功，但 XY 轴的文字标签不显示。

**原因**：
1. Lit 的 `html` 模板在处理 SVG 内部动态内容时存在问题
2. SVG 是 XML 命名空间，而 Lit 的 `html` 模板默认使用 HTML 命名空间
3. 使用 `html` 模板的 `${map(...)}` 语法生成的 SVG 元素可能无法正确渲染

**解决方案**：使用 `unsafeSVG` 指令，将 SVG 内容作为字符串构建后插入。

```typescript
import { unsafeSVG } from 'lit/directives/unsafe-svg.js';

private _renderChart(): unknown {
  // 构建 SVG 内容字符串
  let svgContent = '';
  
  // Y 轴标签
  yTicks.forEach(t => {
    svgContent += `<text x="${padding.left - 12}" y="${yScale(t) + 4}" fill="#aaa">${label}</text>`;
  });
  
  // X 轴标签
  processedData.forEach((d, i) => {
    svgContent += `<text x="${xScale(i)}" y="${height - 20}" fill="#aaa">${d.date}</text>`;
  });
  
  return html`
    <svg viewBox="0 0 ${width} ${height}">
      ${unsafeSVG(svgContent)}
    </svg>
  `;
}
```

**经验**：
- Lit 的 `html` 模板适合 HTML 元素，SVG 内部动态内容用 `unsafeSVG`
- 使用 `preserveAspectRatio="none"` 让 SVG 填充容器，避免缩放导致标签被裁剪
- SVG 容器高度要大于 viewBox 高度，预留空间给标签

### 问题：CSS 变量在 SVG 中不生效

**现象**：`fill="var(--muted)"` 在 SVG text 元素中不显示颜色。

**原因**：SVG 元素不支持 CSS 变量作为属性值。

**解决方案**：使用固定颜色值。
```typescript
// 错误
fill="var(--muted)"

// 正确
fill="#888"
```

### Tooltip 交互设计方案（参考 B站创作者中心）

**交互逻辑**：
- 鼠标在图表区域内移动时，根据鼠标 X 坐标计算最近的数据点索引
- 使用 `Math.round()` 找到最近的日期点
- 实时更新虚线位置、高亮点和浮框内容

**视觉效果**：
1. **虚线竖线**：
   - 从图表顶部到底部贯穿
   - 红色虚线 `stroke="#ff5c5c" stroke-dasharray="4,4"`
   - 半透明 `opacity="0.6"`

2. **数据点高亮**：
   - 指向的点放大（半径 8px，普通点 4px）
   - 白色描边 3px
   - 红色填充

3. **浮框**：
   - 半透明深色背景 + 毛玻璃效果
   - 红色边框淡化
   - 显示日期 + 指标值
   - 位置在数据点上方

**技术要点**：
- Tooltip SVG 元素需要单独渲染，不能放在 `unsafeSVG(svgContent)` 中
- 因为 `svgContent` 是在函数开始时构建的，`tooltipData` 更新不会触发重新构建
- 使用两个 `unsafeSVG()` 调用：一个用于静态图表，一个用于动态 Tooltip

**待解决问题**：
- 当前 Tooltip 不显示，可能是鼠标事件处理或坐标计算有问题
- 需要检查 `handleMouseMove` 函数的坐标计算逻辑
- 需要验证 `tooltipData` 状态更新是否触发视图更新

---

## Lit 框架开发

### 问题：Boolean 属性反射不及时

**现象**：修改 `@property({ type: Boolean })` 后，CSS `:host([collapsed])` 样式不生效。

**原因**：Lit 的 Boolean 属性反射可能不及时。

**解决方案**：
```typescript
this.collapsed = !this.collapsed;
this.requestUpdate('collapsed');  // 强制触发更新
```

### 问题：事件不穿透 Shadow DOM

**现象**：子组件 dispatchEvent 后，父组件收不到事件。

**原因**：Lit 自定义事件默认不穿透 Shadow DOM。

**解决方案**：
```typescript
// 方案一：设置 composed: true
this.dispatchEvent(new CustomEvent('change', {
  bubbles: true,
  composed: true  // 穿透 Shadow DOM
}));

// 方案二：全局函数（更简单）
window.ecomagentNavigate = (page) => { ... };
```

### 问题：异步数据加载后视图不更新

**现象**：数据加载完成，但页面一直显示 loading。

**解决方案**：
```typescript
async loadData() {
  this.loading = true;
  try {
    this.data = await api.getData();
  } finally {
    this.loading = false;
    this.requestUpdate();  // 强制更新
  }
}
```

---

## Playwright 爬虫开发

### 复用已有浏览器

**需求**：抓取时复用已打开的 Chrome，保留登录状态。

**方案**：
```python
# 1. 启动 Chrome（带调试端口）
# chrome.exe --remote-debugging-port=9222 --user-data-dir="..."

# 2. Playwright 连接
browser = p.chromium.connect_over_cdp("http://localhost:9222")
context = browser.contexts[0]  # 使用已有上下文
page = context.new_page()

# 3. 不要关闭 browser，只关闭页面
page.close()
# 不要调用 browser.close()
```

---

## SQLite 数据库

### TikTok 表缺少 UNIQUE 约束

**问题**：`tiktokshop_id` 字段没有 UNIQUE 约束，导致导入时产生重复记录。

**解决**：
```sql
-- 创建唯一索引
CREATE UNIQUE INDEX idx_tiktokshop_unique ON tiktok_products(tiktokshop_id);

-- 删除重复记录
DELETE FROM tiktok_products WHERE id NOT IN (
  SELECT MIN(id) FROM tiktok_products GROUP BY tiktokshop_id
);
```

---

## 后端 API 设计

### 排序 + 分页顺序

**问题**：先分页再排序，导致排序只对当前页生效。

**错误代码**：
```python
cursor.execute("SELECT * FROM products LIMIT ? OFFSET ?", (limit, offset))
products = cursor.fetchall()
products.sort(key=lambda x: x['sales'], reverse=True)  # 只排序当前页
```

**正确代码**：
```python
cursor.execute("SELECT * FROM products")
products = cursor.fetchall()
products.sort(key=lambda x: x['sales'], reverse=True)  # 先排序
products = products[offset:offset + limit]  # 再分页
```
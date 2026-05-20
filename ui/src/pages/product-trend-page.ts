import { LitElement, html, css } from 'lit';
import { unsafeSVG } from 'lit/directives/unsafe-svg.js';
import { customElement, state, property } from 'lit/decorators.js';
import type { PageName } from '../types';

interface TrendRecord {
  date: string;
  price: number | null;
  rating: number | null;
  rank: number | null;
  sales_count: number | null;
}

interface DetailRecord {
  date: string;
  timestamp: string;
  short_name: string | null;
  search_keyword: string | null;
  price: number | null;
  rating: number | null;
  rank: number | null;
  sales_count: number | null;
  events: string;
}

@customElement('ea-product-trend-page')
export class EaProductTrendPage extends LitElement {
  static styles = css`
    :host { display: block; }
    
    /* 头部 */
    .header {
      display: flex;
      align-items: center;
      gap: 16px;
      margin-bottom: 24px;
    }
    .back-btn {
      display: flex;
      align-items: center;
      gap: 6px;
      padding: 8px 16px;
      background: var(--card);
      border: 1px solid var(--border);
      border-radius: var(--radius-sm);
      color: var(--text);
      font-size: 13px;
      cursor: pointer;
      transition: var(--duration-fast) ease;
    }
    .back-btn:hover {
      background: var(--bg-hover);
      border-color: var(--accent);
    }
    .product-title {
      font-size: 18px;
      font-weight: 600;
      color: var(--text-strong);
    }
    .product-code {
      font-size: 12px;
      color: var(--muted);
      margin-left: 8px;
    }
    
    /* 时间选择 */
    .time-selector {
      background: var(--card);
      border-radius: var(--radius-lg);
      border: 1px solid var(--border);
      padding: 16px;
      margin-bottom: 24px;
      display: flex;
      align-items: center;
      gap: 16px;
      flex-wrap: wrap;
    }
    .time-label {
      font-size: 13px;
      font-weight: 500;
      color: var(--text);
    }
    .time-tabs {
      display: flex;
      gap: 4px;
      background: var(--bg-elevated);
      padding: 4px;
      border-radius: var(--radius-sm);
    }
    .time-tab {
      padding: 6px 12px;
      border-radius: 4px;
      font-size: 12px;
      font-weight: 500;
      border: none;
      cursor: pointer;
      transition: var(--duration-fast) ease;
      background: transparent;
      color: var(--muted);
    }
    .time-tab.active {
      background: var(--accent);
      color: var(--accent-foreground);
    }
    .time-tab:hover:not(.active) {
      color: var(--text);
    }
    .date-inputs {
      display: flex;
      align-items: center;
      gap: 8px;
    }
    .date-input {
      padding: 6px 10px;
      border: 1px solid var(--border);
      border-radius: var(--radius-sm);
      font-size: 13px;
      background: var(--bg-elevated);
      color: var(--text);
    }
    .date-input:focus {
      outline: none;
      border-color: var(--accent);
    }
    .apply-btn {
      padding: 6px 12px;
      background: var(--accent);
      color: var(--accent-foreground);
      border: none;
      border-radius: var(--radius-sm);
      font-size: 12px;
      cursor: pointer;
    }
    .apply-btn:hover {
      background: var(--accent-hover);
    }
    
    /* 图表区域 */
    .chart-section {
      background: var(--card);
      border-radius: var(--radius-lg);
      border: 1px solid var(--border);
      padding: 20px;
      margin-bottom: 24px;
    }
    .chart-header {
      display: flex;
      align-items: center;
      justify-content: space-between;
      margin-bottom: 16px;
    }
    .chart-title {
      font-size: 14px;
      font-weight: 600;
      color: var(--text-strong);
    }
    .metric-tabs {
      display: flex;
      gap: 4px;
      background: var(--bg-elevated);
      padding: 4px;
      border-radius: var(--radius-sm);
    }
    .metric-tab {
      padding: 6px 14px;
      border-radius: 4px;
      font-size: 12px;
      font-weight: 500;
      border: none;
      cursor: pointer;
      transition: all 0.3s ease;
      background: transparent;
      color: var(--muted);
    }
    .metric-tab.active {
      background: var(--accent);
      color: var(--accent-foreground);
      transform: scale(1.02);
    }
    .metric-tab:hover:not(.active) {
      color: var(--text);
      background: var(--bg-hover);
    }
    .metric-hint {
      font-size: 11px;
      color: var(--muted);
      margin-left: 8px;
    }
    
    .chart-container {
      width: 100%;
      aspect-ratio: 800 / 320;
      position: relative;
      background: var(--bg-elevated);
      border-radius: var(--radius-sm);
    }
    .chart-svg {
      width: 100%;
      height: 100%;
      display: block;
    }
    
    /* Tooltip 浮框 */
    .tooltip {
      position: absolute;
      transform: translate(-50%, -100%);
      background: rgba(26, 26, 30, 0.95);
      backdrop-filter: blur(8px);
      border: 1px solid rgba(255, 92, 92, 0.2);
      border-radius: 8px;
      padding: 8px 12px;
      font-size: 12px;
      pointer-events: none;
      white-space: nowrap;
      z-index: 10;
      box-shadow: 0 4px 16px rgba(0, 0, 0, 0.3);
    }
    .tooltip-date {
      color: #888;
      font-size: 11px;
      margin-bottom: 4px;
    }
    .tooltip-value {
      color: #fff;
      font-weight: 500;
      font-size: 13px;
    }
    .tooltip-label {
      color: #ff5c5c;
      font-size: 11px;
      margin-right: 4px;
    }
    
    /* Tooltip 点动效 */
    .tooltip-point {
      transition: r 0.15s ease, stroke-width 0.15s ease;
    }
    .chart-empty {
      display: flex;
      align-items: center;
      justify-content: center;
      height: 100%;
      color: var(--muted);
      font-size: 14px;
    }
    
    /* 详细表格 */
    .table-section {
      background: var(--card);
      border-radius: var(--radius-lg);
      border: 1px solid var(--border);
      overflow: hidden;
    }
    .table-header {
      padding: 16px 20px;
      border-bottom: 1px solid var(--border);
      font-size: 14px;
      font-weight: 600;
      color: var(--text-strong);
    }
    table { width: 100%; border-collapse: collapse; }
    th {
      background: var(--bg-accent);
      padding: 10px 12px;
      font-size: 11px;
      font-weight: 600;
      color: var(--muted);
      text-align: left;
      border-bottom: 1px solid var(--border);
      white-space: nowrap;
    }
    td {
      padding: 10px 12px;
      font-size: 13px;
      color: var(--text);
      border-bottom: 1px solid var(--border);
    }
    tr:last-child td { border-bottom: none; }
    tr:hover td { background: var(--card-highlight); }
    
    .event-tag {
      display: inline-block;
      padding: 2px 6px;
      background: var(--accent-subtle);
      color: var(--accent);
      border-radius: 4px;
      font-size: 11px;
      margin-right: 4px;
    }
    
    /* 分页 */
    .pagination {
      display: flex;
      justify-content: center;
      gap: 8px;
      padding: 16px;
    }
    .page-btn {
      padding: 6px 12px;
      border: 1px solid var(--border);
      border-radius: 6px;
      background: var(--bg-elevated);
      color: var(--text);
      cursor: pointer;
      font-size: 13px;
    }
    .page-btn:hover { background: var(--bg-hover); }
    .page-btn.active {
      background: var(--accent);
      color: white;
      border-color: var(--accent);
    }
    
    .loading {
      text-align: center;
      padding: 48px;
      color: var(--muted);
    }
    .spinner {
      width: 32px;
      height: 32px;
      border: 2px solid var(--accent);
      border-top-color: transparent;
      border-radius: 50%;
      animation: spin 1s linear infinite;
      margin: 0 auto 12px;
    }
    @keyframes spin { to { transform: rotate(360deg); } }
  `;

  @property({ type: String }) ecomCode = '';
  
  @state() private loading = true;
  @state() private product: Record<string, any> = {};
  @state() private trend: TrendRecord[] = [];
  @state() private details: DetailRecord[] = [];
  @state() private pagination = { page: 1, limit: 20, total: 0, pages: 1 };
  @state() private timePreset = '7';
  @state() private customStart = '';
  @state() private customEnd = '';
  @state() private metric = 'sales_count';
  @state() private currentPage = 1;
  @state() private tooltipData: { show: boolean; x: number; y: number; date: string; value: number | null; index: number } = { show: false, x: 0, y: 0, date: '', value: null, index: 0 };

  connectedCallback() {
    super.connectedCallback();
    this.loadData();
  }

  async loadData() {
    this.loading = true;
    try {
      const params = new URLSearchParams();
      if (this.timePreset === 'custom' && this.customStart && this.customEnd) {
        params.set('start_date', this.customStart);
        params.set('end_date', this.customEnd);
      } else {
        params.set('days', this.timePreset);
      }
      params.set('page', String(this.currentPage));
      
      const response = await fetch(`/api/product-trend/${this.ecomCode}?${params}`);
      if (!response.ok) throw new Error('Failed to load');
      const data = await response.json();
      
      this.product = data.product;
      this.trend = data.trend;
      this.details = data.details;
      this.pagination = data.pagination;
    } catch (e) {
      console.error('Load trend error:', e);
    } finally {
      this.loading = false;
      this.requestUpdate();
    }
  }

  private _goBack() {
    // 从 sessionStorage 获取来源页面
    const sourcePage = sessionStorage.getItem('trend-source-page') || 'product-master';
    // 跳转回来源页面
    window.ecomagentNavigate(sourcePage as PageName);
    // 恢复状态
    const sourceState = sessionStorage.getItem('trend-source-state');
    if (sourceState) {
      sessionStorage.setItem('restore-state', sourceState);
    }
  }

  private _onTimePreset(preset: string) {
    this.timePreset = preset;
    this.currentPage = 1;
    this.loadData();
  }

  private _onCustomDateChange() {
    if (this.customStart && this.customEnd) {
      this.timePreset = 'custom';
      this.currentPage = 1;
      this.loadData();
    }
  }

  private _onMetricChange(metric: string) {
    this.metric = metric;
    this.requestUpdate();
  }

  private _onPageChange(newPage: number) {
    this.currentPage = newPage;
    this.loadData();
  }

  private _formatValue(value: number | null, metric: string): string {
    if (value == null) return '-';
    if (metric === 'sales_count') {
      if (value >= 10000) return `${(value / 1000).toFixed(1)}K`;
      if (value >= 1000) return `${(value / 1000).toFixed(1)}K`;
    }
    if (metric === 'rating') return value.toFixed(1);
    if (metric === 'price') return `$${value.toFixed(2)}`;
    return String(value);
  }

  private _renderChart(): unknown {
    const data = this.trend;
    if (!data || data.length < 1) {
      return html`<div class="chart-empty">暂无数据</div>`;
    }

    // 空值当作 0 处理
    const processedData = data.map(d => {
      const val = d[this.metric as keyof TrendRecord] as number | null;
      return { ...d, value: val ?? 0, rawValue: val };
    });

    const width = 800;
    const height = 320;
    const padding = { top: 20, right: 40, bottom: 50, left: 70 };
    const chartWidth = width - padding.left - padding.right;
    const chartHeight = height - padding.top - padding.bottom;

    const values = processedData.map(d => d.value);
    const minVal = Math.min(...values);
    const maxVal = Math.max(...values);
    const range = maxVal - minVal || 1;

    // X 轴（日期）
    const xScale = (i: number) => padding.left + (i / (data.length - 1 || 1)) * chartWidth;
    
    // Y 轴（数值）
    const yScale = (v: number) => padding.top + chartHeight - ((v - minVal) / range) * chartHeight;

    // 生成路径
    const pathPoints = processedData.map((d, i) => `${xScale(i)},${yScale(d.value)}`).join(' L ');
    const linePath = `M ${pathPoints}`;
    const areaPath = `M ${padding.left},${padding.top + chartHeight} L ${pathPoints} L ${xScale(data.length - 1)},${padding.top + chartHeight} Z`;

    // Y 轴刻度
    const yTicks: number[] = [];
    const tickCount = 5;
    for (let i = 0; i <= tickCount; i++) {
      yTicks.push(minVal + (range * i) / tickCount);
    }

    // X 轴刻度（每隔几个显示一个）
    const xTickInterval = Math.ceil(data.length / 7);

    // 构建 SVG 内容字符串
    let svgContent = '';
    
    // 渐变定义
    svgContent += `<defs>
      <linearGradient id="areaGradient" x1="0" x2="0" y1="0" y2="1">
        <stop offset="0%" stop-color="#ff5c5c" stop-opacity="0.3" />
        <stop offset="100%" stop-color="#ff5c5c" stop-opacity="0.05" />
      </linearGradient>
    </defs>`;
    
    // 网格线
    yTicks.forEach(t => {
      svgContent += `<line x1="${padding.left}" y1="${yScale(t)}" x2="${width - padding.right}" y2="${yScale(t)}" stroke="#444" stroke-width="1" stroke-dasharray="4,4"/>`;
    });
    
    // 面积
    svgContent += `<path d="${areaPath}" fill="url(#areaGradient)"/>`;
    
    // 折线
    svgContent += `<path d="${linePath}" fill="none" stroke="#ff5c5c" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/>`;
    
    // 数据点
    processedData.forEach((d, i) => {
      svgContent += `<circle cx="${xScale(i)}" cy="${yScale(d.value)}" r="4" fill="#ff5c5c" stroke="#1a1a1a" stroke-width="1"/>`;
    });
    
    // Y 轴标签
    yTicks.forEach(t => {
      const label = this._formatValue(t, this.metric);
      svgContent += `<text x="${padding.left - 6}" y="${yScale(t) + 2}" text-anchor="end" fill="#888" font-size="8" font-family="system-ui, -apple-system, sans-serif" font-weight="400">${label}</text>`;
    });
    
    // X 轴标签
    processedData.forEach((d, i) => {
      if (i % xTickInterval !== 0 && i !== data.length - 1) return;
      const label = d.date.slice(5);
      svgContent += `<text x="${xScale(i)}" y="${height - 8}" text-anchor="middle" fill="#888" font-size="8" font-family="system-ui, -apple-system, sans-serif" font-weight="400">${label}</text>`;
    });

    // 鼠标移动处理
    const handleMouseMove = (e: MouseEvent) => {
      const rect = (e.currentTarget as SVGSVGElement).getBoundingClientRect();
      const mouseX = e.clientX - rect.left;
      const svgWidth = rect.width;
      const scale = svgWidth / width;
      
      // 计算对应的数据索引
      const relX = mouseX / scale - padding.left;
      const index = Math.round((relX / chartWidth) * (data.length - 1));
      
      if (index >= 0 && index < data.length) {
        const d = processedData[index];
        this.tooltipData = {
          show: true,
          x: xScale(index),
          y: yScale(d.value),
          date: d.date,
          value: d.rawValue,
          index
        };
      }
    };

    const handleMouseLeave = () => {
      this.tooltipData = { ...this.tooltipData, show: false };
    };

    return html`
      <svg class="chart-svg" viewBox="0 0 ${width} ${height}" preserveAspectRatio="xMidYMid meet"
        @mousemove=${handleMouseMove} @mouseleave=${handleMouseLeave}>
        ${unsafeSVG(svgContent)}
        ${this.tooltipData.show ? unsafeSVG(`<line class="tooltip-line" x1="${this.tooltipData.x}" y1="0" x2="${this.tooltipData.x}" y2="${height}" stroke="#ff5c5c" stroke-width="1" stroke-dasharray="4,4" opacity="0.6"/><circle class="tooltip-point" cx="${this.tooltipData.x}" cy="${this.tooltipData.y}" r="8" fill="#ff5c5c" stroke="#fff" stroke-width="3"/>`) : null}
      </svg>
      
      <!-- Tooltip 浮框 -->
      ${this.tooltipData.show ? html`
        <div class="tooltip" style="left:calc(${(this.tooltipData.x / 800) * 100}%);top:calc(${(this.tooltipData.y / 320) * 100}%)">
          <div class="tooltip-date">${this.tooltipData.date}</div>
          <div class="tooltip-value">
            <span class="tooltip-label">${this._getMetricLabel()}</span>
            ${this._formatValue(this.tooltipData.value, this.metric)}
          </div>
        </div>
      ` : ''}
    `;
  }

  private _getMetricLabel(): string {
    switch (this.metric) {
      case 'sales_count': return '销量';
      case 'rating': return '评分';
      case 'price': return '价格';
      default: return '';
    }
  }

  private _getMetricHint(): string {
    switch (this.metric) {
      case 'sales_count': return '显示商品每日销量变化趋势';
      case 'rating': return '显示商品评分变化趋势';
      case 'price': return '显示商品价格变化趋势';
      default: return '';
    }
  }

  private _renderPagination(): unknown {
    const buttons = [];
    const maxVisible = 5;
    let start = Math.max(1, this.pagination.page - Math.floor(maxVisible / 2));
    let end = Math.min(this.pagination.pages, start + maxVisible - 1);
    if (end - start < maxVisible - 1) {
      start = Math.max(1, end - maxVisible + 1);
    }

    if (start > 1) {
      buttons.push(html`<button class="page-btn" @click=${() => this._onPageChange(1)}>1</button>`);
      if (start > 2) buttons.push(html`<span style="color:var(--muted)">...</span>`);
    }
    for (let i = start; i <= end; i++) {
      buttons.push(html`
        <button class="page-btn ${i === this.pagination.page ? 'active' : ''}" @click=${() => this._onPageChange(i)}>${i}</button>
      `);
    }
    if (end < this.pagination.pages) {
      if (end < this.pagination.pages - 1) buttons.push(html`<span style="color:var(--muted)">...</span>`);
      buttons.push(html`<button class="page-btn" @click=${() => this._onPageChange(this.pagination.pages)}>${this.pagination.pages}</button>`);
    }
    return html`<div class="pagination">${buttons}</div>`;
  }

  render() {
    if (this.loading) {
      return html`<div class="loading"><div class="spinner"></div><p>加载中...</p></div>`;
    }

    const metricTabs = [
      { key: 'sales_count', label: '销量' },
      { key: 'rating', label: '评分' },
      { key: 'price', label: '价格' },
    ];

    const timePresets = [
      { key: '7', label: '近7天' },
      { key: '15', label: '近15天' },
      { key: '30', label: '近1月' },
      { key: '90', label: '近3月' },
    ];

    return html`
      <!-- 头部 -->
      <div class="header">
        <button class="back-btn" @click=${this._goBack}>
          <span>←</span>
          <span>返回</span>
        </button>
        <div>
          <span class="product-title">${this.product.short_name || this.product.name || '商品趋势'}</span>
        </div>
      </div>

      <!-- 时间选择 -->
      <div class="time-selector">
        <span class="time-label">时间范围：</span>
        <div class="time-tabs">
          ${timePresets.map(t => html`
            <button class="time-tab ${this.timePreset === t.key ? 'active' : ''}" @click=${() => this._onTimePreset(t.key)}>${t.label}</button>
          `)}
        </div>
        <div class="date-inputs">
          <input type="date" class="date-input" .value=${this.customStart} @input=${(e: Event) => { this.customStart = (e.target as HTMLInputElement).value; }} @change=${this._onCustomDateChange}>
          <span style="color:var(--muted)">至</span>
          <input type="date" class="date-input" .value=${this.customEnd} @input=${(e: Event) => { this.customEnd = (e.target as HTMLInputElement).value; }} @change=${this._onCustomDateChange}>
          <button class="apply-btn" @click=${this._onCustomDateChange}>应用</button>
        </div>
      </div>

      <!-- 图表 -->
      <div class="chart-section">
        <div class="chart-header">
          <span class="chart-title">趋势图表</span>
          <div style="display:flex;align-items:center">
            <div class="metric-tabs">
              ${metricTabs.map(t => html`
                <button class="metric-tab ${this.metric === t.key ? 'active' : ''}" @click=${() => this._onMetricChange(t.key)}>${t.label}</button>
              `)}
            </div>
            <span class="metric-hint">${this._getMetricHint()}</span>
          </div>
        </div>
        <div class="chart-container">
          ${this._renderChart()}
        </div>
      </div>

      <!-- 详细表格 -->
      <div class="table-section">
        <div class="table-header">每日数据详情</div>
        <table>
          <thead>
            <tr>
              <th>日期</th>
              <th>简称</th>
              <th>关键词</th>
              <th>评分</th>
              <th>价格</th>
              <th>销量</th>
              <th>事件</th>
            </tr>
          </thead>
          <tbody>
            ${this.details.map(d => html`
              <tr>
                <td>${d.date}</td>
                <td style="max-width:150px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap" title=${d.short_name || ''}>${d.short_name || '-'}</td>
                <td style="max-width:200px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap" title=${d.search_keyword || ''}>${d.search_keyword || '-'}</td>
                <td>${d.rating != null ? d.rating.toFixed(1) : '-'}</td>
                <td>${d.price != null ? `$${d.price.toFixed(2)}` : '-'}</td>
                <td>${d.sales_count != null ? this._formatValue(d.sales_count, 'sales_count') : '-'}</td>
                <td>${d.events ? d.events.split(', ').map(e => html`<span class="event-tag">${e}</span>`) : '-'}</td>
              </tr>
            `)}
          </tbody>
        </table>
        ${this.pagination.pages > 1 ? this._renderPagination() : ''}
      </div>
    `;
  }
}

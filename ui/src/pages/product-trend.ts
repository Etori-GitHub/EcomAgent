import { LitElement, html, css } from 'lit';
import { customElement, state, property } from 'lit/decorators.js';
import type { Product } from '../types';
import { getProductTrend } from '../services/api';

interface TrendData {
  date: string;
  price: number | null;
  rating: number | null;
  rank: number | null;
}

@customElement('ea-product-trend')
export class EaProductTrend extends LitElement {
  static styles = css`
    :host { display: block; padding: 24px; }
    
    .header {
      display: flex;
      align-items: center;
      gap: 12px;
      margin-bottom: 24px;
    }
    
    .back-link {
      color: var(--accent);
      text-decoration: none;
      font-size: 13px;
    }
    
    .back-link:hover { text-decoration: underline; }
    
    h2 {
      font-size: 20px;
      font-weight: 700;
      color: var(--text-strong);
      margin: 0;
    }
    
    .product-info {
      background: var(--card);
      border-radius: var(--radius-lg);
      border: 1px solid var(--border);
      padding: 16px;
      margin-bottom: 24px;
    }
    
    .product-name {
      font-size: 16px;
      font-weight: 600;
      color: var(--text-strong);
      margin-bottom: 8px;
    }
    
    .product-meta {
      font-size: 13px;
      color: var(--muted);
    }
    
    .controls {
      display: flex;
      gap: 12px;
      margin-bottom: 24px;
      flex-wrap: wrap;
      align-items: center;
    }
    
    .control-group {
      display: flex;
      align-items: center;
      gap: 8px;
    }
    
    .control-label {
      font-size: 13px;
      color: var(--muted);
    }
    
    .select {
      padding: 6px 12px;
      border: 1px solid var(--border);
      border-radius: var(--radius-sm);
      font-size: 13px;
      background: var(--bg-elevated);
      color: var(--text);
      cursor: pointer;
    }
    
    .select:focus {
      outline: none;
      border-color: var(--accent);
    }
    
    .chart-container {
      background: var(--card);
      border-radius: var(--radius-lg);
      border: 1px solid var(--border);
      padding: 20px;
      margin-bottom: 24px;
    }
    
    .chart-title {
      font-size: 14px;
      font-weight: 600;
      color: var(--text-strong);
      margin-bottom: 16px;
    }
    
    .chart {
      height: 300px;
      display: flex;
      align-items: flex-end;
      gap: 4px;
      padding: 20px 0;
      border-bottom: 1px solid var(--border);
      position: relative;
    }
    
    .chart-bar {
      flex: 1;
      background: var(--accent);
      border-radius: 4px 4px 0 0;
      min-width: 20px;
      max-width: 60px;
      position: relative;
      transition: height 0.3s ease;
    }
    
    .chart-bar:hover {
      background: var(--accent-hover);
    }
    
    .chart-bar-label {
      position: absolute;
      bottom: -24px;
      left: 50%;
      transform: translateX(-50%);
      font-size: 10px;
      color: var(--muted);
      white-space: nowrap;
    }
    
    .chart-bar-value {
      position: absolute;
      top: -20px;
      left: 50%;
      transform: translateX(-50%);
      font-size: 10px;
      color: var(--text);
      white-space: nowrap;
    }
    
    .chart-empty {
      height: 300px;
      display: flex;
      align-items: center;
      justify-content: center;
      color: var(--muted);
    }
    
    .table-container {
      background: var(--card);
      border-radius: var(--radius-lg);
      border: 1px solid var(--border);
      overflow: hidden;
    }
    
    table {
      width: 100%;
      border-collapse: collapse;
    }
    
    th {
      background: var(--bg-accent);
      padding: 12px;
      font-size: 11px;
      font-weight: 600;
      color: var(--muted);
      text-align: left;
      border-bottom: 1px solid var(--border);
    }
    
    td {
      padding: 12px;
      font-size: 13px;
      color: var(--text);
      border-bottom: 1px solid var(--border);
    }
    
    tr:last-child td { border-bottom: none; }
    tr:hover td { background: var(--card-highlight); }
    
    .trend-up { color: var(--ok); }
    .trend-down { color: var(--danger); }
    
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
  @state() private product: Product | null = null;
  @state() private trendData: TrendData[] = [];
  @state() private loading = true;
  @state() private metric: 'price' | 'rating' | 'rank' = 'rating';
  @state() private days = 7;

  connectedCallback() {
    super.connectedCallback();
    if (this.ecomCode) {
      this.loadTrendData();
    }
  }

  updated(changedProperties: Map<string, unknown>) {
    if (changedProperties.has('ecomCode') && this.ecomCode) {
      this.loadTrendData();
    }
  }

  async loadTrendData() {
    if (!this.ecomCode) return;
    this.loading = true;
    try {
      const result = await getProductTrend(this.ecomCode, this.days);
      this.product = result.product;
      this.trendData = result.trend || [];
    } catch (e) {
      console.error('Load trend error:', e);
    } finally {
      this.loading = false;
      this.requestUpdate();
    }
  }

  private _onMetricChange(e: Event) {
    this.metric = (e.target as HTMLSelectElement).value as any;
    this.requestUpdate();
  }

  private _onDaysChange(e: Event) {
    const value = (e.target as HTMLSelectElement).value;
    if (value === 'custom') {
      // TODO: 自定义日期选择
      return;
    }
    this.days = parseInt(value);
    this.loadTrendData();
  }

  private _getMetricLabel(): string {
    switch (this.metric) {
      case 'price': return '价格';
      case 'rating': return '评分';
      case 'rank': return '排名';
    }
  }

  private _renderChart() {
    if (this.trendData.length === 0) {
      return html`<div class="chart-empty">暂无数据</div>`;
    }

    const values = this.trendData
      .map(d => d[this.metric])
      .filter(v => v !== null && v !== undefined) as number[];

    if (values.length === 0) {
      return html`<div class="chart-empty">暂无${this._getMetricLabel()}数据</div>`;
    }

    const max = Math.max(...values);
    const min = Math.min(...values);
    const range = max - min || 1;

    return html`
      <div class="chart">
        ${this.trendData.map(d => {
          const value = d[this.metric];
          if (value === null || value === undefined) {
            return html`<div class="chart-bar" style="height:0"></div>`;
          }
          const height = ((value - min) / range) * 250 + 20;
          return html`
            <div class="chart-bar" style="height:${height}px">
              <span class="chart-bar-value">${this.metric === 'rating' ? value.toFixed(1) : value}</span>
              <span class="chart-bar-label">${d.date.slice(5)}</span>
            </div>
          `;
        })}
      </div>
    `;
  }

  private _renderTrend(current: number | null, previous: number | null): unknown {
    if (current === null || previous === null) return '-';
    const diff = current - previous;
    if (Math.abs(diff) < 0.01) return '-';
    if (this.metric === 'rank') {
      // 排名越小越好
      return diff < 0 
        ? html`<span class="trend-up">↑${Math.abs(diff).toFixed(0)}</span>`
        : html`<span class="trend-down">↓${Math.abs(diff).toFixed(0)}</span>`;
    }
    return diff > 0
      ? html`<span class="trend-up">↑${diff.toFixed(2)}</span>`
      : html`<span class="trend-down">↓${Math.abs(diff).toFixed(2)}</span>`;
  }

  render() {
    if (this.loading) {
      return html`<div class="loading"><div class="spinner"></div><p>加载中...</p></div>`;
    }

    if (!this.product) {
      return html`
        <div class="header">
          <a class="back-link" href="javascript:history.back()">← 返回</a>
        </div>
        <div style="text-align:center;padding:48px;color:var(--muted)">商品不存在</div>
      `;
    }

    return html`
      <div class="header">
        <a class="back-link" href="javascript:history.back()">← 返回</a>
        <h2>趋势分析</h2>
      </div>

      <div class="product-info">
        <div class="product-name">${this.product.name || this.product.short_name || '未知商品'}</div>
        <div class="product-meta">
          编码: ${this.product.ecom_code} | 平台: ${this.product.platform} | 
          分类: ${this.product.category || '-'}
        </div>
      </div>

      <div class="controls">
        <div class="control-group">
          <span class="control-label">指标:</span>
          <select class="select" .value=${this.metric} @change=${this._onMetricChange}>
            <option value="rating">评分</option>
            <option value="price">价格</option>
            <option value="rank">排名</option>
          </select>
        </div>
        <div class="control-group">
          <span class="control-label">时间区间:</span>
          <select class="select" .value=${String(this.days)} @change=${this._onDaysChange}>
            <option value="7">7天</option>
            <option value="15">15天</option>
            <option value="30">30天</option>
          </select>
        </div>
      </div>

      <div class="chart-container">
        <div class="chart-title">${this._getMetricLabel()}变化趋势</div>
        ${this._renderChart()}
      </div>

      <div class="table-container">
        <table>
          <thead>
            <tr>
              <th>日期</th>
              <th>价格</th>
              <th>评分</th>
              <th>排名</th>
              <th>变化</th>
            </tr>
          </thead>
          <tbody>
            ${this.trendData.map((d, idx) => {
              const prev = idx < this.trendData.length - 1 ? this.trendData[idx + 1] : null;
              return html`
                <tr>
                  <td>${d.date}</td>
                  <td>${d.price !== null ? `$${d.price.toFixed(2)}` : '-'}</td>
                  <td>${d.rating !== null ? d.rating.toFixed(1) : '-'}</td>
                  <td>${d.rank !== null ? d.rank : '-'}</td>
                  <td>${prev ? this._renderTrend(d[this.metric], prev[this.metric]) : '-'}</td>
                </tr>
              `;
            })}
          </tbody>
        </table>
      </div>
    `;
  }
}
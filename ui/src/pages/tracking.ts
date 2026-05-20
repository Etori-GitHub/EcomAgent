import { LitElement, html, css } from 'lit';
import { customElement, state } from 'lit/decorators.js';
import type { Product } from '../types';
import { getTrackedProducts, getSalesTrend } from '../services/api';
import './product-trend';

@customElement('ea-tracking')
export class EaTracking extends LitElement {
  static styles = css`
    :host { display: block; }
    
    /* 模态框 */
    .modal-overlay {
      position: fixed;
      top: 0; left: 0; right: 0; bottom: 0;
      background: rgba(0, 0, 0, 0.7);
      display: flex;
      align-items: center;
      justify-content: center;
      z-index: 1000;
    }
    .modal-content {
      background: var(--bg);
      border-radius: var(--radius-lg);
      width: 90%; max-width: 900px; max-height: 90vh;
      overflow-y: auto; position: relative;
    }
    .modal-close {
      position: absolute; top: 12px; right: 12px;
      background: var(--bg-elevated); border: 1px solid var(--border);
      border-radius: var(--radius-sm); width: 28px; height: 28px;
      cursor: pointer; font-size: 16px; color: var(--muted);
      display: flex; align-items: center; justify-content: center; z-index: 10;
    }
    .modal-close:hover { color: var(--text); }
    
    /* 空状态 */
    .empty-state {
      text-align: center;
      padding: 64px;
      color: var(--muted);
    }
    .empty-icon { font-size: 48px; margin-bottom: 16px; }
    
    /* 表格 */
    .table-container {
      background: var(--card);
      border-radius: var(--radius-lg);
      border: 1px solid var(--border);
      overflow: hidden;
    }
    table { width: 100%; border-collapse: collapse; }
    th {
      background: var(--bg-accent); padding: 10px 12px;
      font-size: 11px; font-weight: 600; color: var(--muted);
      text-align: left; border-bottom: 1px solid var(--border);
      white-space: nowrap;
    }
    td {
      padding: 10px 12px; font-size: 13px; color: var(--text);
      border-bottom: 1px solid var(--border);
      vertical-align: middle;
    }
    tr:last-child td { border-bottom: none; }
    tr:hover td { background: var(--card-highlight); }
    
    /* 商品行 */
    .product-row td { padding: 12px; }
    .product-img {
      width: 56px; height: 56px;
      object-fit: cover; border-radius: 6px;
      flex-shrink: 0;
      background: var(--bg-elevated);
    }
    .product-img-placeholder {
      width: 56px; height: 56px;
      background: var(--bg-elevated); border-radius: 6px;
      display: flex; align-items: center; justify-content: center;
      color: var(--muted); font-size: 18px; flex-shrink: 0;
    }
    .product-info { min-width: 0; }
    .product-name {
      font-size: 13px; font-weight: 500; color: var(--text);
      overflow: hidden; text-overflow: ellipsis; white-space: nowrap;
      max-width: 200px; display: block;
    }
    .product-name:hover { color: var(--accent); }
    
    .platform-badge {
      display: inline-block; padding: 2px 8px;
      border-radius: 4px; font-size: 11px; font-weight: 600;
    }
    .platform-amazon { background: var(--accent-subtle); color: var(--accent); }
    .platform-tiktok { background: rgba(0, 242, 234, 0.1); color: #00f2ea; }
    
    .product-link {
      color: var(--text); text-decoration: none;
    }
    .product-link:hover { text-decoration: underline; color: var(--accent); }
    
    .sales-count {
      font-weight: 600; font-variant-numeric: tabular-nums;
    }
    
    /* 迷你趋势图 */
    .sparkline-cell { width: 120px; }
    .sparkline-container {
      width: 100px; height: 32px; position: relative;
    }
    .sparkline-container svg { width: 100%; height: 100%; }
    
    /* 追踪按钮 */
    .track-btn {
      background: transparent; border: none;
      font-size: 14px; cursor: pointer;
      padding: 2px; line-height: 1;
      color: #fbbf24; transition: color 0.15s;
    }
    .track-btn:hover { color: var(--muted); }
    
    /* 操作按钮 */
    .action-btn {
      padding: 4px 8px; border-radius: var(--radius-sm);
      font-size: 11px; cursor: pointer;
      transition: var(--duration-fast) ease;
      border: 1px solid var(--border);
      background: var(--bg-elevated); color: var(--muted);
      margin-right: 4px;
    }
    .action-btn:hover {
      background: var(--bg-hover); color: var(--text);
    }
    
    .loading {
      text-align: center; padding: 48px; color: var(--muted);
    }
    .spinner {
      width: 32px; height: 32px;
      border: 2px solid var(--accent); border-top-color: transparent;
      border-radius: 50%; animation: spin 1s linear infinite;
      margin: 0 auto 12px;
    }
    @keyframes spin { to { transform: rotate(360deg); } }
  `;

  @state() private products: Product[] = [];
  @state() private loading = true;
  @state() private trackedIds: Set<string> = new Set();
  @state() private showTrend = false;
  @state() private trendCode = '';
  @state() private sparklines: Map<string, Array<{ date: string; value: number | null }>> = new Map();

  connectedCallback() {
    super.connectedCallback();
    this.loadTracked();
  }

  loadTracked() {
    const saved = localStorage.getItem('tracked-products');
    if (saved) {
      this.trackedIds = new Set(JSON.parse(saved));
    }
    this.loadData();
  }

  saveTracked() {
    localStorage.setItem('tracked-products', JSON.stringify([...this.trackedIds]));
  }

  async loadData() {
    this.loading = true;
    
    if (this.trackedIds.size === 0) {
      this.products = [];
      this.loading = false;
      this.requestUpdate();
      return;
    }

    try {
      const result = await getTrackedProducts([...this.trackedIds]);
      this.products = result.products || [];
      this.loadSparklines(this.products);
    } catch (e) {
      console.error('Load tracking error:', e);
      this.products = [];
    } finally {
      this.loading = false;
      this.requestUpdate();
    }
  }

  async loadSparklines(products: Product[]) {
    const promises = products.map(async (p) => {
      try {
        const result = await getSalesTrend(p.ecom_code, 7);
        this.sparklines.set(p.ecom_code, result.trend);
      } catch {
        this.sparklines.set(p.ecom_code, []);
      }
    });
    await Promise.all(promises);
    this.requestUpdate();
  }

  private _untrack(ecomCode: string) {
    this.trackedIds.delete(ecomCode);
    this.saveTracked();
    this.products = this.products.filter(p => p.ecom_code !== ecomCode);
    this.requestUpdate();
  }

  private _showTrendPage(ecomCode: string) {
    // 保存当前页面状态
    const currentState = {
      scrollY: window.scrollY
    };
    sessionStorage.setItem('tracking-state', JSON.stringify(currentState));
    // 跳转到趋势页面
    window.ecomagentOpenTrend(ecomCode, 'tracking');
  }

  private _closeTrendModal() {
    this.showTrend = false;
    this.trendCode = '';
  }

  private _formatSales(n: number | null | undefined): string {
    if (n == null) return '-';
    if (n >= 10000) return `${(n / 1000).toFixed(1)}K`;
    if (n >= 1000) return `${(n / 1000).toFixed(1)}K`;
    return String(n);
  }

  private _renderSparkline(ecomCode: string): unknown {
    const data = this.sparklines.get(ecomCode);
    if (!data || data.length < 2) {
      return html`<div class="sparkline-container" style="display:flex;align-items:center;justify-content:center;color:var(--muted);font-size:10px;">暂无数据</div>`;
    }

    const values = data.map(d => d.value).filter(v => v != null) as number[];
    if (values.length < 2) {
      return html`<div class="sparkline-container" style="display:flex;align-items:center;justify-content:center;color:var(--muted);font-size:10px;">暂无数据</div>`;
    }

    const min = Math.min(...values);
    const max = Math.max(...values);
    const range = max - min || 1;
    const w = 100;
    const h = 32;
    const padding = 2;

    const points = values.map((v, i) => {
      const x = padding + (i / (values.length - 1)) * (w - padding * 2);
      const y = h - padding - ((v - min) / range) * (h - padding * 2);
      return `${x},${y}`;
    }).join(' ');

    const fillPoints = points + ` ${padding + ((values.length - 1) / (values.length - 1)) * (w - padding * 2)},${h - padding} ${padding},${h - padding}`;

    return html`
      <div class="sparkline-container">
        <svg viewBox="0 0 ${w} ${h}" preserveAspectRatio="none">
          <defs>
            <linearGradient id="grad-track-${ecomCode}" x1="0" x2="0" y1="0" y2="1">
              <stop offset="0%" stop-color="var(--accent)" stop-opacity="0.15" />
              <stop offset="100%" stop-color="var(--accent)" stop-opacity="0" />
            </linearGradient>
          </defs>
          <polygon points="${fillPoints}" fill="url(#grad-track-${ecomCode})" />
          <polyline points="${points}" fill="none" stroke="var(--accent)" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" />
        </svg>
      </div>
    `;
  }

  render() {
    if (this.loading) {
      return html`<div class="loading"><div class="spinner"></div><p>加载中...</p></div>`;
    }

    if (this.products.length === 0) {
      return html`
        <div class="empty-state">
          <div class="empty-icon">🎯</div>
          <p>暂无追踪商品</p>
          <p style="font-size: 12px; margin-top: 8px;">请在商品总库中点击 ☆ 按钮添加</p>
        </div>
      `;
    }

    return html`
      <div class="table-container">
        <table>
          <thead>
            <tr>
              <th style="width:50px">排名</th>
              <th style="width:64px">图片</th>
              <th style="width:20%">商品简称</th>
              <th>分类</th>
              <th>价格</th>
              <th>评分</th>
              <th>销量</th>
              <th style="width:100px">7日趋势</th>
              <th style="width:90px">操作</th>
            </tr>
          </thead>
          <tbody>
            ${this.products.map((p, i) => html`
              <tr class="product-row">
                <td style="text-align:center;font-weight:600;color:var(--muted)">${i + 1}</td>
                <td>
                  ${p.local_image_path 
                    ? html`<img class="product-img" src="/images/${p.local_image_path}" loading="lazy" />`
                    : html`<div class="product-img-placeholder">📦</div>`}
                </td>
                <td>
                  <div class="product-info">
                    ${p.product_url 
                      ? html`<a class="product-name product-link" href=${p.product_url} target="_blank" title=${p.name}>${p.short_name || p.name || '无名称'}</a>`
                      : html`<span class="product-name" title=${p.name}>${p.short_name || p.name || '无名称'}</span>`}
                  </div>
                </td>
                <td title=${p.category}>${p.category || '-'}</td>
                <td>${p.price ? `$${p.price.toFixed(2)}` : '-'}</td>
                <td>${p.rating ? html`${p.rating.toFixed(1)} ⭐` : '-'}</td>
                <td><span class="sales-count">${this._formatSales(p.sales_count)}</span></td>
                <td class="sparkline-cell">${this._renderSparkline(p.ecom_code)}</td>
                <td>
                  <button class="action-btn" @click=${() => this._showTrendPage(p.ecom_code)} title="查看趋势">趋势</button>
                  <button class="action-btn" @click=${() => window.open(p.product_url || '#', '_blank')} title="查看详情">查看</button>
                  <button class="action-btn" style="color:var(--danger)" @click=${() => this._untrack(p.ecom_code)} title="取消追踪">移除</button>
                </td>
              </tr>
            `)}
          </tbody>
        </table>
      </div>
      
      <!-- 趋势模态框 -->
      ${this.showTrend ? html`
        <div class="modal-overlay" @click=${this._closeTrendModal}>
          <div class="modal-content" @click=${(e: Event) => e.stopPropagation()}>
            <button class="modal-close" @click=${this._closeTrendModal}>✕</button>
            <ea-product-trend ecomCode=${this.trendCode}></ea-product-trend>
          </div>
        </div>
      ` : ''}
    `;
  }
}
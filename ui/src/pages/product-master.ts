import { LitElement, html, css } from 'lit';
import { customElement, state } from 'lit/decorators.js';
import type { Product } from '../types';
import { getProducts } from '../services/api';
import './product-trend';

@customElement('ea-product-master')
export class EaProductMaster extends LitElement {
  static styles = css`
    :host { display: block; }
    
    /* 模态框 */
    .modal-overlay {
      position: fixed;
      top: 0;
      left: 0;
      right: 0;
      bottom: 0;
      background: rgba(0, 0, 0, 0.7);
      display: flex;
      align-items: center;
      justify-content: center;
      z-index: 1000;
    }
    
    .modal-content {
      background: var(--bg);
      border-radius: var(--radius-lg);
      width: 90%;
      max-width: 900px;
      max-height: 90vh;
      overflow-y: auto;
      position: relative;
    }
    
    .modal-close {
      position: absolute;
      top: 12px;
      right: 12px;
      background: var(--bg-elevated);
      border: 1px solid var(--border);
      border-radius: var(--radius-sm);
      width: 28px;
      height: 28px;
      cursor: pointer;
      font-size: 16px;
      color: var(--muted);
      display: flex;
      align-items: center;
      justify-content: center;
      z-index: 10;
    }
    
    .modal-close:hover {
      color: var(--text);
    }
    
    /* 统计卡片 */
    .stats-grid {
      display: grid;
      grid-template-columns: repeat(4, 1fr);
      gap: 16px;
      margin-bottom: 24px;
    }
    
    .stat-card {
      background: var(--card);
      border-radius: var(--radius-lg);
      border: 1px solid var(--border);
      padding: 16px;
      text-align: center;
    }
    
    .stat-value {
      font-size: 32px;
      font-weight: 700;
    }
    
    .stat-value.accent { color: var(--accent); }
    .stat-value.tiktok { color: #00f2ea; }
    .stat-value.ok { color: var(--ok); }
    .stat-value.text { color: var(--text-strong); }
    
    .stat-label {
      font-size: 12px;
      color: var(--muted);
      margin-top: 4px;
    }
    
    /* 工具栏 */
    .toolbar {
      background: var(--card);
      border-radius: var(--radius-lg);
      border: 1px solid var(--border);
      padding: 16px;
      margin-bottom: 24px;
    }
    
    .toolbar-grid {
      display: grid;
      grid-template-columns: 1fr 1fr 1fr auto;
      gap: 12px;
      align-items: end;
    }
    
    .field-label {
      font-size: 11px;
      font-weight: 600;
      color: var(--muted);
      display: block;
      margin-bottom: 6px;
    }
    
    .input, .select {
      width: 100%;
      padding: 6px 10px;
      border: 1px solid var(--border);
      border-radius: var(--radius-sm);
      font-size: 13px;
      background: var(--bg-elevated);
      color: var(--text);
      transition: var(--duration-fast) ease;
    }
    
    .input:focus, .select:focus {
      outline: none;
      border-color: var(--accent);
    }
    
    .search-btn {
      background: var(--accent);
      color: var(--accent-foreground);
      padding: 6px 16px;
      border-radius: var(--radius-sm);
      font-size: 13px;
      font-weight: 500;
      border: none;
      cursor: pointer;
      transition: var(--duration-fast) ease;
    }
    
    .search-btn:hover {
      background: var(--accent-hover);
    }
    
    /* 表格 */
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
    
    .platform-badge {
      display: inline-block;
      padding: 2px 8px;
      border-radius: 4px;
      font-size: 11px;
      font-weight: 600;
    }
    
    .platform-amazon {
      background: var(--accent-subtle);
      color: var(--accent);
    }
    
    .platform-tiktok {
      background: rgba(0, 242, 234, 0.1);
      color: #00f2ea;
    }
    
    .product-link {
      color: var(--accent);
      text-decoration: none;
    }
    
    .product-link:hover { text-decoration: underline; }
    
    .truncate {
      max-width: 150px;
      overflow: hidden;
      text-overflow: ellipsis;
      white-space: nowrap;
    }
    
    /* 操作按钮 */
    .action-btn {
      padding: 4px 8px;
      border-radius: var(--radius-sm);
      font-size: 11px;
      cursor: pointer;
      transition: var(--duration-fast) ease;
      border: 1px solid var(--border);
      background: var(--bg-elevated);
      color: var(--muted);
      margin-right: 4px;
    }
    
    .action-btn:hover {
      background: var(--bg-hover);
      color: var(--text);
    }
    
    .action-btn.track {
      background: transparent;
      border: none;
      font-size: 14px;
    }
    
    .action-btn.track.active {
      color: #fbbf24;
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
    
    @media (max-width: 768px) {
      .stats-grid { grid-template-columns: repeat(2, 1fr); }
      .toolbar-grid { grid-template-columns: 1fr; }
    }
  `;

  @state() private products: Product[] = [];
  @state() private loading = true;
  @state() private page = 1;
  @state() private total = 0;
  @state() private pages = 0;
  @state() private stats: Record<string, number> = {};
  @state() private search = '';
  @state() private platform = '';
  @state() private category = '';
  @state() private trackedIds: Set<string> = new Set();
  @state() private showTrend = false;
  @state() private trendCode = '';

  connectedCallback() {
    super.connectedCallback();
    this.loadTracked();
    this.loadData();
  }

  loadTracked() {
    const saved = localStorage.getItem('tracked-products');
    if (saved) {
      this.trackedIds = new Set(JSON.parse(saved));
    }
  }

  saveTracked() {
    localStorage.setItem('tracked-products', JSON.stringify([...this.trackedIds]));
  }

  async loadData() {
    this.loading = true;
    console.log('=== ProductMaster: Loading data ===');
    try {
      const result = await getProducts({
        page: this.page,
        limit: 20,
        search: this.search,
        platform: this.platform,
        category: this.category,
      });
      console.log('=== ProductMaster: Data loaded ===', result);
      this.products = result.data;
      this.total = result.pagination.total;
      this.pages = result.pagination.pages;
      this.stats = result.stats;
    } catch (e) {
      console.error('=== ProductMaster: Error ===', e);
    } finally {
      this.loading = false;
      this.requestUpdate();
    }
  }

  private _onSearch() {
    this.page = 1;
    this.loadData();
  }

  private _onInputChange(e: Event, field: 'search' | 'platform' | 'category') {
    (this as any)[field] = (e.target as HTMLInputElement | HTMLSelectElement).value;
  }

  private _onPageChange(newPage: number) {
    this.page = newPage;
    this.loadData();
  }

  private _toggleTrack(ecomCode: string) {
    if (this.trackedIds.has(ecomCode)) {
      this.trackedIds.delete(ecomCode);
    } else {
      this.trackedIds.add(ecomCode);
    }
    this.saveTracked();
    this.requestUpdate();
  }

  private _showTrendModal(ecomCode: string) {
    this.trendCode = ecomCode;
    this.showTrend = true;
  }

  private _closeTrendModal() {
    this.showTrend = false;
    this.trendCode = '';
  }

  private _renderPagination() {
    const buttons = [];
    const maxVisible = 5;
    let start = Math.max(1, this.page - Math.floor(maxVisible / 2));
    let end = Math.min(this.pages, start + maxVisible - 1);
    
    if (end - start < maxVisible - 1) {
      start = Math.max(1, end - maxVisible + 1);
    }

    if (start > 1) {
      buttons.push(html`<button class="page-btn" @click=${() => this._onPageChange(1)}>1</button>`);
      if (start > 2) buttons.push(html`<span style="color:var(--muted)">...</span>`);
    }

    for (let i = start; i <= end; i++) {
      buttons.push(html`
        <button class="page-btn ${i === this.page ? 'active' : ''}" @click=${() => this._onPageChange(i)}>${i}</button>
      `);
    }

    if (end < this.pages) {
      if (end < this.pages - 1) buttons.push(html`<span style="color:var(--muted)">...</span>`);
      buttons.push(html`<button class="page-btn" @click=${() => this._onPageChange(this.pages)}>${this.pages}</button>`);
    }

    return html`<div class="pagination">${buttons}</div>`;
  }

  render() {
    if (this.loading) {
      return html`<div class="loading"><div class="spinner"></div><p>加载中...</p></div>`;
    }

    return html`
      <!-- 统计卡片 -->
      <div class="stats-grid">
        <div class="stat-card">
          <div class="stat-value text">${this.stats.total || this.total}</div>
          <div class="stat-label">总商品数</div>
        </div>
        <div class="stat-card">
          <div class="stat-value accent">${this.stats.amazon || 0}</div>
          <div class="stat-label">Amazon</div>
        </div>
        <div class="stat-card">
          <div class="stat-value tiktok">${this.stats.tiktok || 0}</div>
          <div class="stat-label">TikTok</div>
        </div>
        <div class="stat-card">
          <div class="stat-value ok">${this.stats.today || 0}</div>
          <div class="stat-label">今日新增</div>
        </div>
      </div>

      <!-- 搜索过滤 -->
      <div class="toolbar">
        <div class="toolbar-grid">
          <div>
            <label class="field-label">搜索关键词</label>
            <input type="text" class="input" placeholder="商品名称..." 
              .value=${this.search}
              @input=${(e: Event) => this._onInputChange(e, 'search')}
              @keyup=${(e: KeyboardEvent) => e.key === 'Enter' && this._onSearch()}>
          </div>
          <div>
            <label class="field-label">平台</label>
            <select class="select" .value=${this.platform} @change=${(e: Event) => { this._onInputChange(e, 'platform'); this._onSearch(); }}>
              <option value="">全部平台</option>
              <option value="amazon">Amazon</option>
              <option value="tiktok">TikTok</option>
            </select>
          </div>
          <div>
            <label class="field-label">分类</label>
            <input type="text" class="input" placeholder="分类..." 
              .value=${this.category}
              @input=${(e: Event) => this._onInputChange(e, 'category')}
              @keyup=${(e: KeyboardEvent) => e.key === 'Enter' && this._onSearch()}>
          </div>
          <button class="search-btn" @click=${this._onSearch}>🔍 搜索</button>
        </div>
      </div>

      <!-- 商品列表 -->
      <div class="table-container">
        <table>
          <thead>
            <tr>
              <th>编码</th>
              <th>平台</th>
              <th>产品简称</th>
              <th>分类</th>
              <th>价格</th>
              <th>评分</th>
              <th>更新时间</th>
              <th>操作</th>
            </tr>
          </thead>
          <tbody>
            ${this.products.map(p => html`
              <tr>
                <td style="font-size:11px;color:var(--muted)">${p.ecom_code}</td>
                <td>
                  <span class="platform-badge ${p.platform === 'amazon' ? 'platform-amazon' : 'platform-tiktok'}">
                    ${p.platform}
                  </span>
                </td>
                <td>
                  <span style="display:flex;align-items:center;gap:8px">
                    ${p.product_url 
                      ? html`<a class="product-link" href=${p.product_url} target="_blank" title=${p.name}>${p.short_name || p.name || '无名称'}</a>`
                      : html`<span title=${p.name}>${p.short_name || p.name || '无名称'}</span>`}
                    <button 
                      class="action-btn track ${this.trackedIds.has(p.ecom_code) ? 'active' : ''}"
                      @click=${() => this._toggleTrack(p.ecom_code)}
                      title=${this.trackedIds.has(p.ecom_code) ? '取消追踪' : '添加追踪'}
                    >${this.trackedIds.has(p.ecom_code) ? '★' : '☆'}</button>
                  </span>
                </td>
                <td>${p.category || '-'}</td>
                <td>${p.price ? `$${p.price.toFixed(2)}` : '-'}</td>
                <td>${p.rating ? html`${p.rating.toFixed(1)} ⭐` : '-'}</td>
                <td>${p.last_updated_at || '-'}</td>
                <td>
                  <button class="action-btn" @click=${() => this._showTrendModal(p.ecom_code)} title="查看趋势">趋势</button>
                  <button class="action-btn" @click=${() => window.open(p.product_url || '#', '_blank')} title="查看详情">查看</button>
                </td>
              </tr>
            `)}
          </tbody>
        </table>
        ${this.pages > 1 ? this._renderPagination() : ''}
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
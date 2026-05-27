import { LitElement, html, css } from 'lit';
import { customElement, state } from 'lit/decorators.js';
import type { Product } from '../types';
import { getProducts, getCategories, getSalesTrend } from '../services/api';
import './product-trend';

@customElement('ea-product-master')
export class EaProductMaster extends LitElement {
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
    
    /* 平台切换 */
    .tabs {
      background: var(--card);
      border-radius: var(--radius-lg);
      border: 1px solid var(--border);
      padding: 4px;
      display: inline-flex;
      gap: 4px;
      margin-bottom: 16px;
    }
    .tab-btn {
      padding: 8px 16px;
      border-radius: var(--radius-sm);
      font-size: 13px; font-weight: 500;
      border: none; cursor: pointer;
      transition: var(--duration-fast) ease;
      background: transparent; color: var(--muted);
    }
    .tab-btn.active {
      background: var(--accent);
      color: var(--accent-foreground);
    }
    .tab-btn:hover:not(.active) { color: var(--text); }
    
    /* 统计卡片 */
    .stats-row {
      display: flex;
      gap: 16px;
      margin-bottom: 16px;
    }
    .stat-item {
      background: var(--card);
      border-radius: var(--radius-lg);
      border: 1px solid var(--border);
      padding: 12px 20px;
      display: flex;
      align-items: center;
      gap: 12px;
    }
    .stat-value {
      font-size: 24px;
      font-weight: 700;
      color: var(--text-strong);
    }
    .stat-value.accent { color: var(--accent); }
    .stat-value.tiktok { color: #00f2ea; }
    .stat-value.ok { color: var(--ok); }
    .stat-label {
      font-size: 13px;
      color: var(--muted);
    }
    
    /* 工具栏 */
    .toolbar {
      background: var(--card);
      border-radius: var(--radius-lg);
      border: 1px solid var(--border);
      padding: 12px 16px;
      margin-bottom: 24px;
      display: flex;
      gap: 12px;
      align-items: center;
    }
    .field-group {
      display: flex;
      flex-direction: column;
      gap: 4px;
    }
    .field-label {
      font-size: 11px; font-weight: 600; color: var(--muted);
    }
    .input, .select {
      padding: 6px 10px;
      border: 1px solid var(--border);
      border-radius: var(--radius-sm);
      font-size: 13px; background: var(--bg-elevated);
      color: var(--text); transition: var(--duration-fast) ease;
    }
    .input:focus, .select:focus {
      outline: none; border-color: var(--accent);
    }
    .input.search-input { width: 180px; }
    .select { width: 230px; }
    .search-btn {
      background: var(--accent); color: var(--accent-foreground);
      padding: 6px 16px; border-radius: var(--radius-sm);
      font-size: 13px; font-weight: 500; border: none;
      cursor: pointer; transition: var(--duration-fast) ease;
    }
    .search-btn:hover { background: var(--accent-hover); }
    
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
      white-space: nowrap; user-select: none;
    }
    th.sortable { cursor: pointer; }
    th.sortable:hover { color: var(--text); }
    th .sort-icon { margin-left: 4px; font-size: 10px; opacity: 0.5; }
    th.sorted .sort-icon { opacity: 1; color: var(--accent); }
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
    .product-code {
      font-size: 11px; color: var(--muted);
      margin-top: 2px;
    }
    
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
    .sparkline-container svg {
      width: 100%; height: 100%;
    }
    
    /* 追踪按钮 */
    .track-btn {
      background: transparent; border: none;
      font-size: 14px; cursor: pointer;
      padding: 2px; line-height: 1;
      color: var(--muted); transition: color 0.15s;
    }
    .track-btn.active { color: #fbbf24; }
    .track-btn:hover { color: #fbbf24; }
    
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
    
    /* 图片预览浮框 */
    .img-preview {
      position: fixed;
      z-index: 2000;
      max-width: 400px;
      max-height: 400px;
      border-radius: 8px;
      box-shadow: 0 8px 32px rgba(0, 0, 0, 0.5);
      pointer-events: none;
      border: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    /* 分页 */
    .pagination {
      display: flex; justify-content: center;
      gap: 8px; padding: 16px;
    }
    .page-btn {
      padding: 6px 12px; border: 1px solid var(--border);
      border-radius: 6px; background: var(--bg-elevated);
      color: var(--text); cursor: pointer; font-size: 13px;
    }
    .page-btn:hover { background: var(--bg-hover); }
    .page-btn.active {
      background: var(--accent); color: white;
      border-color: var(--accent);
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
  @state() private page = 1;
  @state() private pages = 0;
  @state() private search = '';
  @state() private platform = 'amazon';
  @state() private category = '';
  @state() private categories: { amazon: string[]; tiktok: string[]; all: Array<{ platform: string; category: string }> } = { amazon: [], tiktok: [], all: [] };
  @state() private sortBy = 'sales_count';
  @state() private sortOrder: 'asc' | 'desc' = 'desc';
  @state() private trackedIds: Set<string> = new Set();
  @state() private showTrend = false;
  @state() private trendCode = '';
  @state() private sparklines: Map<string, Array<{ date: string; value: number | null }>> = new Map();
  @state() private previewImg: { show: boolean; src: string; x: number; y: number } = { show: false, src: '', x: 0, y: 0 };

  async connectedCallback() {
    super.connectedCallback();
    this.loadTracked();
    await this.loadCategories();
    // 分类加载完成后再加载数据，这样默认分类才能生效
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

  async loadCategories() {
    try {
      this.categories = await getCategories();
      // 默认选中第一个分类（跳过"全部分类"选项）
      if (!this.category) {
        const cats = this.platform === 'amazon' ? this.categories.amazon : this.categories.tiktok;
        if (cats.length > 0) {
          this.category = cats[0];
        }
      }
    } catch (e) {
      console.error('Failed to load categories', e);
    }
  }

  async loadData() {
    this.loading = true;
    try {
      const result = await getProducts({
        page: this.page,
        limit: 20,
        search: this.search,
        platform: this.platform,
        category: this.category,
        sort_by: this.sortBy || undefined,
        sort_order: this.sortOrder,
      });
      this.products = result.data;
      this.pages = result.pagination.pages;
      
      this.loadSparklines(result.data);
    } catch (e) {
      console.error('Failed to load products', e);
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

  private _onPlatformChange(platform: string) {
    this.platform = platform;
    // 切换平台时选中第一个分类（跳过"全部分类"选项）
    const cats = platform === 'amazon' ? this.categories.amazon : this.categories.tiktok;
    this.category = cats.length > 0 ? cats[0] : '';
    this.page = 1;
    this.loadData();
  }

  private _onSearch() {
    this.page = 1;
    this.loadData();
  }

  private _onInputChange(e: Event, field: 'search' | 'category') {
    (this as any)[field] = (e.target as HTMLInputElement | HTMLSelectElement).value;
  }

  private _onCategoryChange(e: Event) {
    this.category = (e.target as HTMLSelectElement).value;
    this.page = 1;
    this.loadData();
  }

  private _onSort(field: string) {
    if (this.sortBy === field) {
      this.sortOrder = this.sortOrder === 'desc' ? 'asc' : 'desc';
    } else {
      this.sortBy = field;
      this.sortOrder = 'desc';
    }
    this.page = 1;
    this.loadData();
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

  private _showTrendPage(ecomCode: string) {
    // 保存当前页面状态
    const currentState = {
      platform: this.platform,
      category: this.category,
      search: this.search,
      sortBy: this.sortBy,
      sortOrder: this.sortOrder,
      page: this.page,
      scrollY: window.scrollY
    };
    sessionStorage.setItem('product-master-state', JSON.stringify(currentState));
    // 跳转到趋势页面
    window.ecomagentOpenTrend(ecomCode, 'product-master');
  }

  private _closeTrendModal() {
    this.showTrend = false;
    this.trendCode = '';
  }

  private _showSourcingModal(ecomCode: string) {
    // 跳转到货源页面，带 ecom_code 参数
    window.ecomagentNavigateToSourcing(ecomCode);
  }

  private async _open1688(name: string | undefined, ecomCode: string) {
    if (!name) return;
    // 带 ecom_code 参数跳转，让插件能识别来源
    const url = `https://s.1688.com/selloffer/offer_search.htm?keywords=${encodeURIComponent(name)}&ecom_code=${encodeURIComponent(ecomCode)}`;
    window.open(url, '_blank');
  }

  private _showImgPreview(e: MouseEvent, src: string) {
    this.previewImg = {
      show: true,
      src,
      x: e.clientX + 16,
      y: e.clientY + 16
    };
    this._updatePreviewElement();
  }

  private _hideImgPreview() {
    this.previewImg = { ...this.previewImg, show: false };
    this._updatePreviewElement();
  }

  private _moveImgPreview(e: MouseEvent) {
    if (!this.previewImg.show) return;
    this.previewImg = {
      ...this.previewImg,
      x: e.clientX + 16,
      y: e.clientY + 16
    };
    this._updatePreviewElement();
  }

  private _updatePreviewElement() {
    let el = document.getElementById('global-img-preview') as HTMLImageElement | null;
    if (!el) {
      el = document.createElement('img');
      el.id = 'global-img-preview';
      el.style.cssText = 'position:fixed;z-index:9999;max-width:400px;max-height:400px;border-radius:8px;box-shadow:0 8px 32px rgba(0,0,0,0.5);pointer-events:none;border:1px solid rgba(255,255,255,0.1);';
      document.body.appendChild(el);
    }
    if (this.previewImg.show) {
      el.src = this.previewImg.src;
      el.style.left = this.previewImg.x + 'px';
      el.style.top = this.previewImg.y + 'px';
      el.style.display = 'block';
    } else {
      el.style.display = 'none';
    }
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
            <linearGradient id="grad-${ecomCode}" x1="0" x2="0" y1="0" y2="1">
              <stop offset="0%" stop-color="var(--accent)" stop-opacity="0.15" />
              <stop offset="100%" stop-color="var(--accent)" stop-opacity="0" />
            </linearGradient>
          </defs>
          <polygon points="${fillPoints}" fill="url(#grad-${ecomCode})" />
          <polyline points="${points}" fill="none" stroke="var(--accent)" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" />
        </svg>
      </div>
    `;
  }

  private _renderSortHeader(label: string, field: string) {
    const isActive = this.sortBy === field;
    const icon = isActive
      ? (this.sortOrder === 'desc' ? '▼' : '▲')
      : '⇅';
    return html`
      <th class="sortable ${isActive ? 'sorted' : ''}" @click=${() => this._onSort(field)}>
        ${label} <span class="sort-icon">${icon}</span>
      </th>
    `;
  }

  private _getCategoryOptions(): string[] {
    if (this.platform === 'amazon') return this.categories.amazon;
    if (this.platform === 'tiktok') return this.categories.tiktok;
    return [];
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

    const categoryOptions = this._getCategoryOptions();

    return html`
      <!-- 平台切换 -->
      <div class="tabs">
        <button class="tab-btn ${this.platform === 'amazon' ? 'active' : ''}" @click=${() => this._onPlatformChange('amazon')}>Amazon</button>
        <button class="tab-btn ${this.platform === 'tiktok' ? 'active' : ''}" @click=${() => this._onPlatformChange('tiktok')}>TikTok</button>
      </div>

      <!-- 搜索过滤 -->
      <div class="toolbar">
        <div class="field-group">
          <label class="field-label">分类</label>
          <select class="select" @change=${this._onCategoryChange}>
            <option value="" ?selected=${!this.category}>全部分类</option>
            ${categoryOptions.map(c => html`<option value=${c} ?selected=${this.category === c}>${c}</option>`)}
          </select>
        </div>
        <div class="field-group">
          <label class="field-label">搜索</label>
          <input type="text" class="input search-input" placeholder="商品名称..." 
            .value=${this.search}
            @input=${(e: Event) => this._onInputChange(e, 'search')}
            @keyup=${(e: KeyboardEvent) => e.key === 'Enter' && this._onSearch()}>
        </div>
        <button class="search-btn" @click=${this._onSearch}>🔍 搜索</button>
      </div>

      <!-- 商品列表 -->
      <div class="table-container">
        <table>
          <thead>
            <tr>
              <th style="width:50px">排名</th>
              <th style="width:64px">图片</th>
              <th style="width:20%">商品简称</th>
              <th>分类</th>
              ${this._renderSortHeader('价格', 'price')}
              ${this._renderSortHeader('评分', 'rating')}
              ${this._renderSortHeader('销量', 'sales_count')}
              <th style="width:100px">7日趋势</th>
              <th style="width:90px">操作</th>
            </tr>
          </thead>
          <tbody>
            ${this.products.map((p, i) => html`
              <tr class="product-row">
                <td style="text-align:center;font-weight:600;color:var(--muted)">${(this.page - 1) * 20 + i + 1}</td>
                <td>
                  ${p.local_image_path 
                    ? html`<img class="product-img" src="/images/${p.local_image_path}" loading="lazy" 
                        @mouseenter=${(e: MouseEvent) => this._showImgPreview(e, `/images/${p.local_image_path}`)}
                        @mouseleave=${this._hideImgPreview}
                        @mousemove=${this._moveImgPreview} />`
                    : html`<div class="product-img-placeholder">📦</div>`}
                </td>
                <td>
                  <div class="product-info">
                    ${p.product_url 
                      ? html`<a class="product-name product-link" href=${p.product_url} target="_blank" title=${p.name}>${p.short_name || p.name || '无名称'}</a>`
                      : html`<span class="product-name" title=${p.name}>${p.short_name || p.name || '无名称'}</span>`}
                    <div class="product-code">
                      <button class="track-btn ${this.trackedIds.has(p.ecom_code) ? 'active' : ''}"
                        @click=${() => this._toggleTrack(p.ecom_code)}
                        title=${this.trackedIds.has(p.ecom_code) ? '取消追踪' : '添加追踪'}
                      >${this.trackedIds.has(p.ecom_code) ? '★' : '☆'}</button>
                    </div>
                  </div>
                </td>
                <td title=${p.category}>${p.category || '-'}</td>
                <td>${p.price ? `$${p.price.toFixed(2)}` : '-'}</td>
                <td>${p.rating ? html`${p.rating.toFixed(1)} ⭐` : '-'}</td>
                <td><span class="sales-count">${this._formatSales(p.sales_count)}</span></td>
                <td class="sparkline-cell">${this._renderSparkline(p.ecom_code)}</td>
                <td>
                  <button class="action-btn" @click=${() => this._showTrendPage(p.ecom_code)} title="查看趋势">趋势</button>
                  <button class="action-btn" @click=${() => this._showSourcingModal(p.ecom_code)} title="查看货源">货源</button>
                  <button class="action-btn" @click=${() => window.open(p.product_url || '#', '_blank')} title="查看详情">查看</button>
                  <button class="action-btn" @click=${() => this._open1688(p.short_name || p.name, p.ecom_code)} title="1688搜索">1688</button>
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
      
      <!-- 图片预览浮框 -->
    `;
  }
}
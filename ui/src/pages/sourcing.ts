import { LitElement, html, css } from 'lit';
import { customElement, property, state } from 'lit/decorators.js';

@customElement('ea-sourcing')
export class EcomAgentSourcing extends LitElement {
  @property({ type: String }) ecomCode = '';
  @state() private sourcingList: any[] = [];
  @state() private loading = true;
  @state() private search = '';
  @state() private page = 1;
  @state() private pages = 0;
  @state() private total = 0;
  @state() private stats = { total: 0, products_linked: 0, today_count: 0, last_updated: null };

  // 素材管理
  @state() private showAssetManager = false;
  @state() private assetManagerItem: any = null;

  static styles = css`
    :host {
      display: block;
    }

    /* 弹窗样式 */
    .modal-overlay {
      position: fixed;
      top: 0;
      left: 0;
      right: 0;
      bottom: 0;
      background: rgba(0, 0, 0, 0.5);
      display: flex;
      align-items: center;
      justify-content: center;
      z-index: 1000;
      animation: fadeIn 0.2s ease;
    }

    @keyframes fadeIn {
      from { opacity: 0; }
      to { opacity: 1; }
    }

    .modal-content {
      background: var(--card);
      border: 1px solid var(--border);
      border-radius: var(--radius-lg);
      padding: 32px;
      max-width: 400px;
      width: 90%;
      text-align: center;
      animation: slideIn 0.3s ease;
      box-shadow: 0 20px 40px rgba(0, 0, 0, 0.15);
    }

    @keyframes slideIn {
      from { transform: translateY(-20px); opacity: 0; }
      to { transform: translateY(0); opacity: 1; }
    }

    .modal-icon {
      font-size: 48px;
      margin-bottom: 16px;
    }

    .modal-title {
      font-size: 18px;
      font-weight: 600;
      color: var(--text);
      margin-bottom: 8px;
    }

    .modal-desc {
      font-size: 14px;
      color: var(--muted);
      margin-bottom: 24px;
      line-height: 1.6;
    }

    .modal-product {
      background: var(--bg);
      border-radius: var(--radius-md);
      padding: 12px;
      margin-bottom: 24px;
      display: flex;
      align-items: center;
      gap: 12px;
    }

    .modal-product-thumb {
      width: 40px;
      height: 40px;
      object-fit: cover;
      border-radius: var(--radius-sm);
    }

    .modal-product-title {
      font-size: 13px;
      color: var(--text);
      overflow: hidden;
      text-overflow: ellipsis;
      white-space: nowrap;
    }

    .modal-buttons {
      display: flex;
      gap: 12px;
      justify-content: center;
    }

    .modal-btn {
      padding: 12px 24px;
      border-radius: var(--radius-md);
      font-size: 14px;
      cursor: pointer;
      transition: all 0.2s;
    }

    .modal-btn-confirm {
      background: var(--primary);
      color: white;
      border: none;
    }

    .modal-btn-confirm:hover {
      opacity: 0.9;
      transform: translateY(-1px);
    }

    .modal-btn-cancel {
      background: var(--bg);
      color: var(--text);
      border: 1px solid var(--border);
    }

    .modal-btn-cancel:hover {
      background: var(--bg-elevated);
    }

    /* 头部统计 */
    .stats-row {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
      gap: 16px;
      margin-bottom: 24px;
    }

    .stat-card {
      background: var(--card);
      border: 1px solid var(--border);
      border-radius: var(--radius-lg);
      padding: 20px;
    }

    .stat-value {
      font-size: 28px;
      font-weight: 600;
      color: var(--text);
      margin-bottom: 4px;
    }

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
      align-items: flex-end;
    }

    .field-group {
      display: flex;
      flex-direction: column;
      gap: 4px;
    }

    .field-label {
      font-size: 11px; font-weight: 600; color: var(--muted);
    }

    .search-input {
      padding: 6px 10px;
      border: 1px solid var(--border);
      border-radius: var(--radius-sm);
      font-size: 13px; background: var(--bg-elevated);
      color: var(--text); transition: var(--duration-fast) ease;
      width: 240px;
    }

    .search-input:focus {
      outline: none; border-color: var(--accent);
    }

    .search-btn {
      padding: 6px 16px; border-radius: var(--radius-sm);
      font-size: 13px; font-weight: 500; border: none;
      cursor: pointer; transition: var(--duration-fast) ease;
      background: var(--accent); color: var(--accent-foreground);
    }

    .search-btn:hover { background: var(--accent-hover); }

    /* 筛选标签 */
    .filter-tag {
      display: inline-flex;
      align-items: center;
      gap: 8px;
      padding: 6px 12px;
      background: var(--accent);
      color: white;
      border-radius: var(--radius-sm);
      font-size: 13px;
    }

    .filter-clear {
      background: transparent;
      border: none;
      color: white;
      cursor: pointer;
      padding: 0;
      font-size: 14px;
      line-height: 1;
      opacity: 0.8;
    }

    .filter-clear:hover {
      opacity: 1;
    }

    /* 货源列表 */
    .sourcing-table {
      background: var(--card);
      border: 1px solid var(--border);
      border-radius: var(--radius-lg);
      overflow: hidden;
    }

    .sourcing-table table {
      width: 100%;
      border-collapse: collapse;
    }

    .sourcing-table th {
      text-align: left;
      padding: 12px 16px;
      background: var(--bg-elevated);
      font-weight: 500;
      font-size: 12px;
      text-transform: uppercase;
      color: var(--muted);
      border-bottom: 1px solid var(--border);
    }

    .sourcing-table td {
      padding: 12px 16px;
      border-bottom: 1px solid var(--border);
      font-size: 13px;
    }

    .sourcing-table tr:last-child td {
      border-bottom: none;
    }

    .sourcing-table tr:hover td {
      background: var(--bg);
    }

    .product-cell {
      display: flex;
      align-items: center;
      gap: 12px;
      min-width: 300px;
    }

    .product-thumb {
      width: 50px;
      height: 50px;
      object-fit: cover;
      border-radius: var(--radius-sm);
      background: var(--bg-elevated);
      flex-shrink: 0;
    }

    .product-info {
      flex: 1;
      min-width: 0;
    }

    .product-title {
      font-size: 13px;
      color: var(--text);
      line-height: 1.4;
      overflow: hidden;
      text-overflow: ellipsis;
      display: -webkit-box;
      -webkit-line-clamp: 2;
      -webkit-box-orient: vertical;
    }

    .product-shop {
      font-size: 11px;
      color: var(--muted);
      margin-top: 2px;
    }

    .price-cell {
      color: #f5222d;
      font-weight: 600;
    }

    .ecom-code-cell {
      font-family: monospace;
      font-size: 12px;
      color: var(--primary);
    }

    .action-btn {
      padding: 6px 12px;
      border-radius: var(--radius-sm);
      font-size: 12px;
      cursor: pointer;
      transition: all 0.2s;
      margin-right: 8px;
    }

    .action-btn-view {
      background: var(--primary);
      color: white;
      border: none;
    }

    .action-btn-view:hover {
      opacity: 0.9;
    }

    .action-btn-video, .action-btn-detail {
      background: transparent;
      color: var(--text);
      border: 1px solid var(--border);
    }

    .action-btn-video:hover, .action-btn-detail:hover {
      background: var(--bg);
      border-color: var(--primary);
    }

    .action-btn-asset {
      background: #722ed1;
      color: white;
      border: none;
    }

    .action-btn-asset:hover {
      opacity: 0.9;
    }

    .action-btn-tiktok {
      background: #ff0050;
      color: white;
      border: none;
    }

    .action-btn-tiktok:hover {
      opacity: 0.9;
    }

    .action-btn-delete {
      background: transparent;
      color: #f5222d;
      border: 1px solid #f5222d;
    }

    .action-btn-delete:hover {
      background: #fff1f0;
    }

    /* 分页 */
    .pagination {
      display: flex;
      justify-content: center;
      align-items: center;
      gap: 8px;
      margin-top: 24px;
    }

    .page-btn {
      padding: 8px 12px;
      border: 1px solid var(--border);
      border-radius: var(--radius-sm);
      background: var(--card);
      color: var(--text);
      font-size: 13px;
      cursor: pointer;
    }

    .page-btn:hover:not(:disabled) {
      border-color: var(--primary);
    }

    .page-btn:disabled {
      opacity: 0.5;
      cursor: not-allowed;
    }

    .page-btn.active {
      background: var(--primary);
      border-color: var(--primary);
      color: white;
    }

    .page-info {
      font-size: 13px;
      color: var(--muted);
    }

    /* 空状态 */
    .empty-state {
      text-align: center;
      padding: 60px 20px;
      color: var(--muted);
    }

    .empty-icon {
      font-size: 64px;
      margin-bottom: 16px;
    }

    .empty-title {
      font-size: 18px;
      color: var(--text);
      margin-bottom: 8px;
    }

    .empty-desc {
      font-size: 14px;
    }

    /* 加载状态 */
    .loading-state {
      text-align: center;
      padding: 60px;
      color: var(--muted);
    }
  `;

  connectedCallback() {
    super.connectedCallback();
    // 不用 await,让渲染先进行
    this.loadStats();
    this.loadSourcing();
  }

  async loadStats() {
    try {
      const response = await fetch('/api/sourcing/stats');
      this.stats = await response.json();
      console.log('[Sourcing] stats:', this.stats);
    } catch (e) {
      console.error('加载统计失败:', e);
    }
  }

  async loadSourcing() {
    try {
      const params = new URLSearchParams();
      params.set('page', String(this.page));
      params.set('limit', '20');
      if (this.search) params.set('search', this.search);
      if (this.ecomCode) params.set('ecom_code', this.ecomCode);

      console.log('[Sourcing] 请求:', `/api/sourcing/list?${params}`);
      const response = await fetch(`/api/sourcing/list?${params}`);
      const data = await response.json();
      console.log('[Sourcing] 响应:', data);

      this.sourcingList = data.data || [];
      this.total = data.pagination?.total || 0;
      this.pages = data.pagination?.pages || 0;
      this.loading = false;
      console.log('[Sourcing] loading 设为 false, 触发 requestUpdate');
      this.requestUpdate();
    } catch (e) {
      console.error('加载货源失败:', e);
      this.sourcingList = [];
      this.loading = false;
      this.requestUpdate();
    }
  }

  private _onSearch(e: KeyboardEvent) {
    if (e.key === 'Enter') {
      this.page = 1;
      this.loadSourcing();
    }
  }

  private _onPageChange(newPage: number) {
    this.page = newPage;
    this.loadSourcing();
    window.scrollTo({ top: 0, behavior: 'smooth' });
  }

  private _formatPrice(price: number) {
    return price ? `¥${price.toFixed(2)}` : '-';
  }

  private _formatDate(dateStr: string) {
    if (!dateStr) return '-';
    const date = new Date(dateStr);
    return `${date.getMonth() + 1}/${date.getDate()} ${date.getHours()}:${String(date.getMinutes()).padStart(2, '0')}`;
  }

  private async _deleteSourcing(ecomCode: string, offerId: string) {
    if (!confirm('确定删除此货源记录?')) return;

    try {
      await fetch(`/api/sourcing/${ecomCode}/${offerId}`, { method: 'DELETE' });
      await Promise.all([this.loadStats(), this.loadSourcing()]);
    } catch (e) {
      console.error('删除失败:', e);
    }
  }

  private _openProduct(url: string) {
    if (url) window.open(url, '_blank');
  }

  // 旧的生成弹窗(已弃用,保留兼容)
  // private _showModal(type: 'video' | 'detail', item: any) { ... }

  private _showAssetManager(item: any) {
    console.log('[Sourcing] _showAssetManager called:', item);
    this.assetManagerItem = item;
    this.showAssetManager = true;
    this.requestUpdate();
  }

  private _closeAssetManager() {
    this.showAssetManager = false;
    this.assetManagerItem = null;
    this.requestUpdate();
  }

  // tiktokUploading and tiktokResult used for future UI enhancement
  // @state() private tiktokUploading = false;
  // @state() private tiktokResult: any = null;

  private async _uploadToTikTok(item: any) {
    console.log('[Sourcing] _uploadToTikTok called, item:', item);

    // 检查并自动启动 Chrome
    try {
      console.log('[Sourcing] Checking TikTok connection...');
      const statusRes = await fetch('/api/tiktok/status');
      const status = await statusRes.json();
      console.log('[Sourcing] TikTok status:', status);

      if (!status.connected) {
        // 尝试启动 Chrome
        console.log('[Sourcing] Chrome not running, starting...');
        const ensureRes = await fetch('/api/tiktok/ensure-chrome', { method: 'POST' });
        const ensureData = await ensureRes.json();
        console.log('[Sourcing] Ensure Chrome result:', ensureData);

        if (!ensureRes.ok) {
          alert('Failed to start Chrome. Please start manually.');
          return;
        }

        // 等待 Chrome 启动
        await new Promise(r => setTimeout(r, 2000));

        // 打开登录页面
        const loginRes = await fetch('/api/tiktok/open-login', { method: 'POST' });
        if (loginRes.ok) {
          alert('Chrome started!\nPlease login to TikTok Shop, then click TikTok button again.');
          return;
        }
      }
    } catch (e) {
      console.error('[Sourcing] Status check failed:', e);
      alert('Server connection failed');
      return;
    }

    // 直接上传,不使用 confirm
    console.log('[Sourcing] 开始上传到 TikTok:', item.ecom_code);
    // this.tiktokUploading = true;
    // this.requestUpdate();

    try {
      const response = await fetch(`/api/tiktok/upload/${item.ecom_code}`, { method: 'POST' });
      const result = await response.json();
      console.log('[Sourcing] 上传结果:', result);

      // this.tiktokUploading = false;
      // this.requestUpdate();

      if (result.success) {
        alert(`上传成功!\n请在 TikTok Shop 后台检查草稿商品`);
      } else {
        alert(`上传失败: ${result.message}`);
      }
    } catch (e) {
      console.error('[Sourcing] 上传失败:', e);
      // this.tiktokUploading = false;
      // this.requestUpdate();
      alert('上传失败,请检查服务器连接');
    }
  }

  private _renderModal() {
    // 旧的生成弹窗已弃用,返回空
    return null;
  }

  private _renderAssetManager() {
    if (!this.showAssetManager) return null;

    return html`
      <div class="modal-overlay" @click=${(e: Event) => {
        if (e.target === e.currentTarget) this._closeAssetManager();
      }}>
        <div class="modal-content" style="max-width: 500px;">
          <asset-generator
            .ecomCode=${this.assetManagerItem?.ecom_code}
            .item=${this.assetManagerItem}
            @close=${this._closeAssetManager}
          ></asset-generator>
        </div>
      </div>
    `;
  }

  private _renderPagination() {
    if (this.pages <= 1) return null;

    const buttons = [];
    const maxVisible = 5;
    let start = Math.max(1, this.page - Math.floor(maxVisible / 2));
    let end = Math.min(this.pages, start + maxVisible - 1);

    if (end - start < maxVisible - 1) {
      start = Math.max(1, end - maxVisible + 1);
    }

    // 上一页
    buttons.push(html`
      <button class="page-btn" ?disabled=${this.page === 1} @click=${() => this._onPageChange(this.page - 1)}>
        ‹
      </button>
    `);

    // 页码
    for (let i = start; i <= end; i++) {
      buttons.push(html`
        <button class="page-btn ${i === this.page ? 'active' : ''}" @click=${() => this._onPageChange(i)}>
          ${i}
        </button>
      `);
    }

    // 下一页
    buttons.push(html`
      <button class="page-btn" ?disabled=${this.page === this.pages} @click=${() => this._onPageChange(this.page + 1)}>
        ›
      </button>
    `);

    return html`
      <div class="pagination">
        <span class="page-info">共 ${this.total} 条</span>
        ${buttons}
      </div>
    `;
  }

  render() {
    console.log('[Sourcing] render called, loading=', this.loading, 'list=', this.sourcingList.length);

    if (this.loading) {
      return html`<div class="loading-state">加载中...</div>`;
    }

    return html`
      <!-- 统计卡片 -->
      <div class="stats-row">
        <div class="stat-card">
          <div class="stat-value">${this.stats.total}</div>
          <div class="stat-label">货源总数</div>
        </div>
        <div class="stat-card">
          <div class="stat-value">${this.stats.products_linked}</div>
          <div class="stat-label">关联商品数</div>
        </div>
        <div class="stat-card">
          <div class="stat-value">${this.stats.today_count}</div>
          <div class="stat-label">今日采集</div>
        </div>
      </div>

      <!-- 搜索栏 -->
      <div class="toolbar">
        <div class="field-group">
          <label class="field-label">搜索</label>
          <input type="text" class="search-input" placeholder="商品名称、店铺、offer ID..."
            .value=${this.search}
            @keydown=${this._onSearch}
            @change=${(e: Event) => this.search = (e.target as HTMLInputElement).value}
          >
        </div>
        <button class="search-btn" @click=${() => { this.page = 1; this.loadSourcing(); }}>🔍 搜索</button>
        ${this.ecomCode ? html`
          <div class="field-group">
            <label class="field-label">筛选</label>
            <div class="filter-tag">
              <span>${this.ecomCode}</span>
              <button class="filter-clear" @click=${() => { this.ecomCode = ''; this.page = 1; this.loadSourcing(); }}>✕</button>
            </div>
          </div>
        ` : ''}
      </div>

      <!-- 货源列表 -->
      ${this.sourcingList.length === 0 ? html`
        <div class="empty-state">
          <div class="empty-icon">📦</div>
          <div class="empty-title">暂无货源记录</div>
          <div class="empty-desc">点击商品库的「1688」按钮开始采集货源</div>
        </div>
      ` : html`
        <div class="sourcing-table">
          <table>
            <thead>
              <tr>
                <th>商品</th>
                <th>价格</th>
                <th>起订量</th>
                <th>关联商品</th>
                <th>采集时间</th>
                <th>操作</th>
              </tr>
            </thead>
            <tbody>
              ${this.sourcingList.map((item: any) => html`
                <tr>
                  <td>
                    <div class="product-cell">
                      <img
                        class="product-thumb"
                        src=${item.local_image_path ? `/images/${item.local_image_path}` : (item.image_url || 'data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" width="50" height="50"><rect fill="%23ddd" width="50" height="50"/></svg>')}
                        onerror="this.src='data:image/svg+xml,<svg xmlns=%22http://www.w3.org/2000/svg%22 width=%2250%22 height=%2250%22><rect fill=%22%23ddd%22 width=%2250%22 height=%2250%22/></svg>'"
                      >
                      <div class="product-info">
                        <div class="product-title">${item.title || '无标题'}</div>
                        <div class="product-shop">${item.shop_name || '未知店铺'} · ${item.offer_id}</div>
                      </div>
                    </div>
                  </td>
                  <td class="price-cell">${this._formatPrice(item.price)}</td>
                  <td>${item.min_order || 1}</td>
                  <td class="ecom-code-cell">${item.ecom_code}</td>
                  <td>${this._formatDate(item.collected_at)}</td>
                  <td>
                    <button class="action-btn action-btn-tiktok" @click=${() => { console.log('[Sourcing] TikTok button clicked!'); this._uploadToTikTok(item); }}>
                      TikTok
                    </button>
                    <button class="action-btn action-btn-asset" @click=${() => this._showAssetManager(item)}>
                      素材
                    </button>
                    <button class="action-btn action-btn-view" @click=${() => this._openProduct(item.product_url)}>
                      查看
                    </button>
                    <button class="action-btn action-btn-delete" @click=${() => this._deleteSourcing(item.ecom_code, item.offer_id)}>
                      删除
                    </button>
                  </td>
                </tr>
              `)}
            </tbody>
          </table>
        </div>

        ${this._renderPagination()}
      `}

      ${this._renderModal()}

      ${this._renderAssetManager()}
    `;
  }
}

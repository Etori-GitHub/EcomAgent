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

  @state() private showModal = false;
  @state() private modalType = ''; // 'video' | 'detail'
  @state() private modalItem: any = null;

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
      display: flex;
      gap: 12px;
      margin-bottom: 16px;
      flex-wrap: wrap;
      align-items: center;
    }
    
    .search-box {
      flex: 1;
      min-width: 200px;
      max-width: 400px;
      position: relative;
    }
    
    .search-input {
      width: 100%;
      padding: 10px 16px 10px 40px;
      border: 1px solid var(--border);
      border-radius: var(--radius-md);
      background: var(--bg);
      color: var(--text);
      font-size: 14px;
    }
    
    .search-input:focus {
      outline: none;
      border-color: var(--primary);
    }
    
    .search-icon {
      position: absolute;
      left: 14px;
      top: 50%;
      transform: translateY(-50%);
      color: var(--muted);
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
    // 不用 await，让渲染先进行
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
    if (!confirm('确定删除此货源记录？')) return;
    
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

  private _showModal(type: 'video' | 'detail', item: any) {
    console.log('[Sourcing] _showModal called:', type, item);
    this.modalType = type;
    this.modalItem = item;
    this.showModal = true;
    this.requestUpdate();
  }

  private _closeModal() {
    console.log('[Sourcing] _closeModal called');
    this.showModal = false;
    this.modalType = '';
    this.modalItem = null;
    this.requestUpdate();
  }

  private _confirmModal() {
    // TODO: 实际功能待开发
    console.log(`[Sourcing] 确认生成: ${this.modalType}`, this.modalItem);
    this._closeModal();
    // 显示提示
    alert(this.modalType === 'video' ? '视频生成功能开发中...' : '详情图生成功能开发中...');
  }

  private _renderModal() {
    if (!this.showModal) return null;
    
    const icon = this.modalType === 'video' ? '🎬' : '🖼️';
    const title = this.modalType === 'video' ? '生成宣传视频' : '生成详情图';
    const desc = this.modalType === 'video' 
      ? '将使用货源商品信息自动生成宣传视频，用于社交平台推广'
      : '将使用货源商品详情自动生成电商详情图，用于商品上架';
    
    return html`
      <div class="modal-overlay" @click=${(e: Event) => {
        if (e.target === e.currentTarget) this._closeModal();
      }}>
        <div class="modal-content">
          <div class="modal-icon">${icon}</div>
          <div class="modal-title">${title}</div>
          <div class="modal-desc">${desc}</div>
          <div class="modal-product">
            <img 
              class="modal-product-thumb" 
              src=${this.modalItem?.image_url || 'data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" width="40" height="40"><rect fill="%23ddd" width="40" height="40"/></svg>'}
              onerror="this.src='data:image/svg+xml,<svg xmlns=%22http://www.w3.org/2000/svg%22 width=%2240%22 height=%2240%22><rect fill=%22%23ddd%22 width=%2240%22 height=%2240%22/></svg>'"
            >
            <div class="modal-product-title">${this.modalItem?.title || '未知商品'}</div>
          </div>
          <div class="modal-buttons">
            <button class="modal-btn modal-btn-cancel" @click=${this._closeModal}>取消</button>
            <button class="modal-btn modal-btn-confirm" @click=${this._confirmModal}>确认生成</button>
          </div>
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
        <div class="search-box">
          <span class="search-icon">🔍</span>
          <input 
            type="text" 
            class="search-input" 
            placeholder="搜索商品名称、店铺、offer ID..."
            .value=${this.search}
            @keydown=${this._onSearch}
            @change=${(e: Event) => this.search = (e.target as HTMLInputElement).value}
          >
        </div>
        ${this.ecomCode ? html`
          <span style="color: var(--primary); font-size: 13px;">
            筛选商品: ${this.ecomCode}
            <button 
              style="margin-left: 8px; padding: 4px 8px; border: 1px solid var(--border); border-radius: var(--radius-sm); cursor: pointer;"
              @click=${() => { this.ecomCode = ''; this.page = 1; this.loadSourcing(); }}
            >清除</button>
          </span>
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
                    <button class="action-btn action-btn-video" @click=${() => this._showModal('video', item)}>
                      视频
                    </button>
                    <button class="action-btn action-btn-detail" @click=${() => this._showModal('detail', item)}>
                      详情图
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
    `;
  }
}

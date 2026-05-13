import { LitElement, html, css } from 'lit';
import { customElement, state } from 'lit/decorators.js';
import type { Product } from '../types';
import { getAmazonProducts, getTiktokProducts } from '../services/api';

@customElement('ea-raw-data')
export class EaRawData extends LitElement {
  static styles = css`
    :host { display: block; }
    
    .tabs {
      background: var(--card);
      border-radius: var(--radius-lg);
      border: 1px solid var(--border);
      padding: 4px;
      display: inline-flex;
      gap: 4px;
      margin-bottom: 24px;
    }
    
    .tab-btn {
      padding: 8px 16px;
      border-radius: var(--radius-sm);
      font-size: 13px;
      font-weight: 500;
      border: none;
      cursor: pointer;
      transition: var(--duration-fast) ease;
      background: transparent;
      color: var(--muted);
    }
    
    .tab-btn.active {
      background: var(--accent);
      color: var(--accent-foreground);
    }
    
    .toolbar {
      background: var(--card);
      border-radius: var(--radius-lg);
      border: 1px solid var(--border);
      padding: 16px;
      margin-bottom: 24px;
    }
    
    .toolbar-grid {
      display: grid;
      grid-template-columns: 1fr 1fr auto;
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
    
    .input {
      width: 100%;
      padding: 6px 10px;
      border: 1px solid var(--border);
      border-radius: var(--radius-sm);
      font-size: 13px;
      background: var(--bg-elevated);
      color: var(--text);
    }
    
    .input:focus {
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
    
    .truncate {
      max-width: 150px;
      overflow: hidden;
      text-overflow: ellipsis;
      white-space: nowrap;
    }
    
    .action-btn {
      padding: 4px 8px;
      border-radius: var(--radius-sm);
      font-size: 11px;
      cursor: pointer;
      border: 1px solid var(--border);
      background: var(--bg-elevated);
      color: var(--muted);
    }
    
    .action-btn:hover {
      background: var(--bg-hover);
      color: var(--text);
    }
    
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

  @state() private platform: 'amazon' | 'tiktok' = 'amazon';
  @state() private products: Product[] = [];
  @state() private loading = false;
  @state() private page = 1;
  @state() private pages = 0;
  @state() private search = '';
  @state() private category = '';

  connectedCallback() {
    super.connectedCallback();
    this.loadData();
  }

  async loadData() {
    this.loading = true;
    console.log('=== RawData: Loading, platform:', this.platform);
    try {
      const params = {
        page: this.page,
        limit: 20,
        search: this.search,
        category: this.category,
      };
      
      const result = this.platform === 'amazon' 
        ? await getAmazonProducts(params)
        : await getTiktokProducts(params);
      
      console.log('=== RawData: Result:', result);
      this.products = result.data || [];
      this.pages = result.pagination?.pages || 0;
    } catch (e) {
      console.error('=== RawData: Error:', e);
      this.products = [];
    } finally {
      this.loading = false;
      this.requestUpdate();
    }
  }

  private _switchPlatform(p: 'amazon' | 'tiktok') {
    this.platform = p;
    this.page = 1;
    this.loadData();
  }

  private _onSearch() {
    this.page = 1;
    this.loadData();
  }

  private _onPageChange(newPage: number) {
    this.page = newPage;
    this.loadData();
  }

  private _renderPagination() {
    const buttons = [];
    const maxVisible = 5;
    let start = Math.max(1, this.page - Math.floor(maxVisible / 2));
    let end = Math.min(this.pages, start + maxVisible - 1);
    
    if (end - start < maxVisible - 1) {
      start = Math.max(1, end - maxVisible + 1);
    }

    for (let i = start; i <= end; i++) {
      buttons.push(html`
        <button class="page-btn ${i === this.page ? 'active' : ''}" @click=${() => this._onPageChange(i)}>${i}</button>
      `);
    }

    return html`<div class="pagination">${buttons}</div>`;
  }

  render() {
    return html`
      <div class="tabs">
        <button class="tab-btn ${this.platform === 'amazon' ? 'active' : ''}" @click=${() => this._switchPlatform('amazon')}>Amazon</button>
        <button class="tab-btn ${this.platform === 'tiktok' ? 'active' : ''}" @click=${() => this._switchPlatform('tiktok')}>TikTok</button>
      </div>

      <div class="toolbar">
        <div class="toolbar-grid">
          <div>
            <label class="field-label">搜索关键词</label>
            <input type="text" class="input" placeholder="产品名称..." 
              .value=${this.search}
              @input=${(e: Event) => this.search = (e.target as HTMLInputElement).value}
              @keyup=${(e: KeyboardEvent) => e.key === 'Enter' && this._onSearch()}>
          </div>
          <div>
            <label class="field-label">分类</label>
            <input type="text" class="input" placeholder="分类..." 
              .value=${this.category}
              @input=${(e: Event) => this.category = (e.target as HTMLInputElement).value}
              @keyup=${(e: KeyboardEvent) => e.key === 'Enter' && this._onSearch()}>
          </div>
          <button class="search-btn" @click=${this._onSearch}>搜索</button>
        </div>
      </div>

      ${this.loading 
        ? html`<div class="loading"><div class="spinner"></div><p>加载中...</p></div>`
        : html`
          <div class="table-container">
            <table>
              <thead>
                <tr>
                  <th>ID</th>
                  <th>产品简称</th>
                  <th>搜索关键词</th>
                  <th>${this.platform === 'tiktok' ? 'TikTokShop ID' : '分类'}</th>
                  ${this.platform === 'tiktok' ? html`<th>分类</th>` : ''}
                  <th>价格</th>
                  <th>评分</th>
                  <th>操作</th>
                </tr>
              </thead>
              <tbody>
                ${this.products.map(p => html`
                  <tr>
                    <td style="font-size:11px;color:var(--muted)">${p.id}</td>
                    <td class="truncate" title=${p.name}>${p.short_name || p.name || '-'}</td>
                    <td class="truncate" title=${p.search_keyword}>${p.search_keyword || '-'}</td>
                    ${this.platform === 'tiktok' 
                      ? html`<td style="font-size:11px;font-family:monospace">${p.tiktokshop_id || '-'}</td>`
                      : ''}
                    <td>${p.category || '-'}</td>
                    <td>${p.price ? `$${p.price.toFixed(2)}` : '-'}</td>
                    <td>${p.rating ? `${p.rating.toFixed(1)} ⭐` : '-'}</td>
                    <td>
                      <button class="action-btn" @click=${() => window.open(p.product_url || '#', '_blank')}>查看</button>
                    </td>
                  </tr>
                `)}
              </tbody>
            </table>
            ${this.pages > 1 ? this._renderPagination() : ''}
          </div>
        `}
    `;
  }
}
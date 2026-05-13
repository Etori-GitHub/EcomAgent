import { LitElement, html, css } from 'lit';
import { customElement, state } from 'lit/decorators.js';
import type { Product } from '../types';
import { getAmazonTop, getTiktokTop } from '../services/api';

// 扩展 Product 类型，添加排名变化
interface TopProduct extends Product {
  rank_change?: number; // 正数=上升，负数=下降，null=新入榜或无数据
  is_new?: boolean;
}

@customElement('ea-today-top')
export class EaTodayTop extends LitElement {
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
    
    .categories-grid {
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(400px, 1fr));
      gap: 16px;
    }
    
    .category-card {
      background: var(--card);
      border-radius: var(--radius-lg);
      border: 1px solid var(--border);
      overflow: hidden;
    }
    
    .category-card.pinned {
      border-color: var(--accent);
      box-shadow: 0 0 0 1px var(--accent);
    }
    
    .category-header {
      padding: 12px 16px;
      background: var(--bg-accent);
      font-size: 14px;
      font-weight: 600;
      color: var(--text-strong);
      border-bottom: 1px solid var(--border);
      display: flex;
      justify-content: space-between;
      align-items: center;
    }
    
    .pin-btn {
      background: transparent;
      border: none;
      cursor: pointer;
      font-size: 16px;
      color: var(--muted);
      padding: 4px;
      transition: var(--duration-fast) ease;
    }
    
    .pin-btn:hover { color: var(--text); }
    .pin-btn.pinned { color: #fbbf24; }
    
    table {
      width: 100%;
      border-collapse: collapse;
    }
    
    td {
      padding: 8px 12px;
      font-size: 12px;
      color: var(--text);
      border-bottom: 1px solid var(--border);
    }
    
    tr:last-child td { border-bottom: none; }
    tr:hover td { background: var(--card-highlight); }
    
    .rank-cell {
      display: flex;
      align-items: center;
      gap: 6px;
    }
    
    .rank {
      color: #00f2ea;
      font-weight: 600;
    }
    
    .rank-change {
      font-size: 10px;
      font-weight: 500;
      display: inline-flex;
      align-items: center;
      gap: 2px;
    }
    
    .rank-change.up { color: var(--ok); }
    .rank-change.down { color: var(--danger); }
    
    .new-badge {
      padding: 1px 4px;
      background: var(--ok);
      color: white;
      font-size: 9px;
      border-radius: 2px;
      font-weight: 500;
    }
    
    .product-link {
      color: var(--text-strong);
      text-decoration: none;
    }
    
    .product-link:hover { text-decoration: underline; }
    
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
      .categories-grid { grid-template-columns: 1fr; }
    }
  `;

  @state() private platform: 'amazon' | 'tiktok' = 'amazon';
  @state() private amazonData: Record<string, TopProduct[]> = {};
  @state() private tiktokData: Record<string, TopProduct[]> = {};
  @state() private loading = false;
  @state() private pinnedCategories: Set<string> = new Set();

  connectedCallback() {
    super.connectedCallback();
    this._loadPinned();
    this.loadData();
  }

  private _loadPinned() {
    const saved = localStorage.getItem('pinned-categories');
    if (saved) {
      this.pinnedCategories = new Set(JSON.parse(saved));
    }
  }

  private _savePinned() {
    localStorage.setItem('pinned-categories', JSON.stringify([...this.pinnedCategories]));
  }

  private _togglePin(category: string) {
    if (this.pinnedCategories.has(category)) {
      this.pinnedCategories.delete(category);
    } else {
      this.pinnedCategories.add(category);
    }
    this._savePinned();
    this.requestUpdate();
  }

  async loadData() {
    this.loading = true;
    try {
      if (this.platform === 'amazon' && Object.keys(this.amazonData).length === 0) {
        this.amazonData = await getAmazonTop();
      } else if (this.platform === 'tiktok' && Object.keys(this.tiktokData).length === 0) {
        this.tiktokData = await getTiktokTop();
      }
    } catch (e) {
      console.error('Load top error:', e);
    } finally {
      this.loading = false;
      this.requestUpdate();
    }
  }

  private _switchPlatform(p: 'amazon' | 'tiktok') {
    this.platform = p;
    this.loadData();
  }

  private _truncate(text: string, maxLen: number = 20): string {
    if (!text) return '-';
    return text.length > maxLen ? text.substring(0, maxLen) + '...' : text;
  }

  private _renderRankChange(change?: number, isNew?: boolean) {
    if (isNew) {
      return html`<span class="new-badge">新</span>`;
    }
    if (change === undefined || change === null) {
      return null;
    }
    if (change > 0) {
      return html`<span class="rank-change up">↑${change}</span>`;
    }
    if (change < 0) {
      return html`<span class="rank-change down">↓${Math.abs(change)}</span>`;
    }
    return null;
  }

  private _sortCategories(categories: string[]): string[] {
    const pinned = categories.filter(c => this.pinnedCategories.has(c));
    const unpinned = categories.filter(c => !this.pinnedCategories.has(c));
    return [...pinned, ...unpinned];
  }

  render() {
    const data = this.platform === 'amazon' ? this.amazonData : this.tiktokData;
    const categories = this._sortCategories(Object.keys(data));

    return html`
      <div class="tabs">
        <button class="tab-btn ${this.platform === 'amazon' ? 'active' : ''}" @click=${() => this._switchPlatform('amazon')}>Amazon</button>
        <button class="tab-btn ${this.platform === 'tiktok' ? 'active' : ''}" @click=${() => this._switchPlatform('tiktok')}>TikTok</button>
      </div>

      ${this.loading 
        ? html`<div class="loading"><div class="spinner"></div><p>加载中...</p></div>`
        : categories.length === 0
          ? html`<div style="text-align:center;padding:48px;color:var(--muted)">暂无数据</div>`
          : html`
            <div class="categories-grid">
              ${categories.map(cat => {
                const isPinned = this.pinnedCategories.has(cat);
                return html`
                  <div class="category-card ${isPinned ? 'pinned' : ''}">
                    <div class="category-header">
                      <span>${cat}</span>
                      <button 
                        class="pin-btn ${isPinned ? 'pinned' : ''}" 
                        @click=${() => this._togglePin(cat)}
                        title=${isPinned ? '取消置顶' : '置顶'}
                      >${isPinned ? '★' : '☆'}</button>
                    </div>
                    <table>
                      <tbody>
                        ${(data[cat] || []).slice(0, 15).map((p, idx) => html`
                          <tr style="cursor:pointer" @click=${() => window.open(p.product_url || '#', '_blank')}>
                            <td>
                              <div class="rank-cell">
                                <span class="rank">#${idx + 1}</span>
                                ${this._renderRankChange(p.rank_change, p.is_new)}
                              </div>
                            </td>
                            <td>
                              <a class="product-link" href=${p.product_url || '#'} target="_blank" title=${p.name}>
                                ${this._truncate(p.short_name || p.name)}
                              </a>
                            </td>
                            <td>${p.price ? `$${p.price.toFixed(2)}` : '-'}</td>
                            <td>${p.rating ? `${p.rating.toFixed(1)} ⭐` : '-'}</td>
                          </tr>
                        `)}
                      </tbody>
                    </table>
                  </div>
                `;
              })}
            </div>
          `}
    `;
  }
}
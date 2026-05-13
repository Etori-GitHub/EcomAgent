import { LitElement, html, css } from 'lit';
import { customElement, state } from 'lit/decorators.js';
import type { Product } from '../types';
import { getTrackedProducts } from '../services/api';

@customElement('ea-tracking')
export class EaTracking extends LitElement {
  static styles = css`
    :host { display: block; }
    
    .empty-state {
      text-align: center;
      padding: 48px;
      color: var(--muted);
    }
    
    .empty-icon {
      font-size: 48px;
      margin-bottom: 16px;
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
    
    .action-btn.untrack {
      background: transparent;
      border: none;
      font-size: 14px;
      color: #fbbf24;
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

  @state() private products: Product[] = [];
  @state() private loading = true;
  @state() private trackedIds: Set<string> = new Set();

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
    } catch (e) {
      console.error('Load tracking error:', e);
      this.products = [];
    } finally {
      this.loading = false;
      this.requestUpdate();
    }
  }

  private _untrack(ecomCode: string) {
    this.trackedIds.delete(ecomCode);
    this.saveTracked();
    this.products = this.products.filter(p => p.ecom_code !== ecomCode);
    this.requestUpdate();
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
                  ${p.product_url 
                    ? html`<a class="product-link" href=${p.product_url} target="_blank" title=${p.name}>${p.short_name || p.name || '无名称'}</a>`
                    : html`<span title=${p.name}>${p.short_name || p.name || '无名称'}</span>`}
                </td>
                <td>${p.category || '-'}</td>
                <td>${p.price ? `$${p.price.toFixed(2)}` : '-'}</td>
                <td>${p.rating ? html`${p.rating.toFixed(1)} ⭐` : '-'}</td>
                <td>${p.last_updated_at || '-'}</td>
                <td>
                  <button class="action-btn" @click=${() => console.log('趋势:', p.ecom_code)}>趋势</button>
                  <button class="action-btn" @click=${() => window.open(p.product_url || '#', '_blank')}>查看</button>
                  <button class="action-btn" style="color:var(--danger)" @click=${() => this._untrack(p.ecom_code)} title="取消追踪">删除</button>
                </td>
              </tr>
            `)}
          </tbody>
        </table>
      </div>
    `;
  }
}
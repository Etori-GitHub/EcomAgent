import { LitElement, html, css } from 'lit';
import { customElement, state } from 'lit/decorators.js';
import type { StatsResponse } from '../types';
import { getStats } from '../services/api';
import '../components/card';

@customElement('ea-dashboard')
export class EaDashboard extends LitElement {
  static styles = css`
    :host { display: block; }
    h2 { font-size: 20px; font-weight: 700; color: var(--text-strong); margin-bottom: 24px; }
    h3 { font-size: 16px; font-weight: 600; color: var(--text-strong); margin-bottom: 16px; }
    .stats-grid { display: grid; grid-template-columns: repeat(2, 1fr); gap: 16px; margin-bottom: 32px; }
    .master-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 16px; margin-bottom: 32px; }
    .loading { text-align: center; padding: 48px; color: var(--muted); }
    .spinner { width: 40px; height: 40px; border: 2px solid var(--accent); border-top-color: transparent; border-radius: 50%; animation: spin 1s linear infinite; margin: 0 auto 16px; }
    .error-box { background: var(--danger-subtle); border: 1px solid var(--danger); border-radius: 8px; padding: 16px; color: var(--danger); margin-bottom: 24px; }
    .retry-btn { margin-top: 12px; padding: 8px 16px; background: var(--accent); color: white; border: none; border-radius: 6px; cursor: pointer; }
    .retry-btn:hover { background: var(--accent-hover); }
    .update-btn {
      padding: 8px 16px;
      border-radius: var(--radius-sm);
      font-size: 13px;
      font-weight: 500;
      cursor: pointer;
      transition: var(--duration-fast) ease;
      border: none;
    }
    .update-btn.amazon {
      background: var(--accent-subtle);
      color: var(--accent);
      border: 1px solid var(--accent);
    }
    .update-btn.amazon:hover { background: var(--accent); color: white; }
    .update-btn.tiktok {
      background: rgba(0, 242, 234, 0.1);
      color: #00f2ea;
      border: 1px solid #00f2ea;
    }
    .update-btn.tiktok:hover { background: #00f2ea; color: black; }
    .update-btn:disabled { opacity: 0.5; cursor: not-allowed; }
    @keyframes spin { to { transform: rotate(360deg); } }
    @media (max-width: 768px) { .stats-grid, .master-grid { grid-template-columns: 1fr; } }
  `;

  @state() private stats: StatsResponse | null = null;
  @state() private loading = true;
  @state() private error = '';
  @state() private updating: 'amazon' | 'tiktok' | null = null;

  connectedCallback() {
    super.connectedCallback();
    this.loadStats();
  }

  async loadStats() {
    this.loading = true;
    this.error = '';
    
    try {
      this.stats = await getStats();
    } catch (e) {
      this.error = e instanceof Error ? e.message : String(e);
    } finally {
      this.loading = false;
      this.requestUpdate();
    }
  }

  private async _updatePlatform(platform: 'amazon' | 'tiktok') {
    this.updating = platform;
    try {
      const endpoint = platform === 'amazon' ? '/api/tasks/amazon-fetch' : '/api/tasks/tiktok-fetch';
      const response = await fetch(endpoint, { method: 'POST' });
      const data = await response.json();
      
      if (data.success) {
        alert(`${platform} 抓取任务已启动，请稍后刷新查看结果`);
      } else {
        alert(data.message || '启动失败');
      }
    } catch (e) {
      alert(`抓取失败: ${e}`);
    } finally {
      this.updating = null;
    }
  }

  render() {
    if (this.loading) {
      return html`<div class="loading"><div class="spinner"></div><p>加载中...</p></div>`;
    }

    if (this.error) {
      return html`
        <div class="error-box">
          <p>加载失败: ${this.error}</p>
          <button class="retry-btn" @click=${this.loadStats}>重试</button>
        </div>
      `;
    }

    if (!this.stats) {
      return html`<div class="error-box"><p>无数据</p></div>`;
    }

    const { amazon, tiktok, product_master } = this.stats;

    return html`
      <h2>数据概览</h2>

      <h3>平台数据</h3>
      <div class="stats-grid">
        <ea-stat-card
          label="Amazon"
          .value=${amazon.products.toLocaleString()}
          icon="📦"
          desc="商品总数"
          color="accent"
        >
          <div style="display:flex;justify-content:space-between;align-items:flex-end;">
            <div style="font-size: 13px; color: var(--muted);">
              抓取记录: ${amazon.sales.toLocaleString()}<br>
              今日新增: ${amazon.today.toLocaleString()}
            </div>
            <button 
              class="update-btn amazon"
              ?disabled=${this.updating === 'amazon'}
              @click=${() => this._updatePlatform('amazon')}
            >${this.updating === 'amazon' ? '更新中...' : '更新数据'}</button>
          </div>
        </ea-stat-card>

        <ea-stat-card
          label="TikTok"
          .value=${tiktok.products.toLocaleString()}
          icon="🎵"
          desc="商品总数"
          color="info"
        >
          <div style="display:flex;justify-content:space-between;align-items:flex-end;">
            <div style="font-size: 13px; color: var(--muted);">
              抓取记录: ${tiktok.sales.toLocaleString()}<br>
              今日新增: ${tiktok.today.toLocaleString()}
            </div>
            <button 
              class="update-btn tiktok"
              ?disabled=${this.updating === 'tiktok'}
              @click=${() => this._updatePlatform('tiktok')}
            >${this.updating === 'tiktok' ? '更新中...' : '更新数据'}</button>
          </div>
        </ea-stat-card>
      </div>

      <h3>商品总库</h3>
      <div class="master-grid">
        <ea-stat-card label="总商品数" .value=${product_master.total.toLocaleString()} color="accent"></ea-stat-card>
        <ea-stat-card label="Amazon" .value=${product_master.amazon.toLocaleString()} color="accent"></ea-stat-card>
        <ea-stat-card label="TikTok" .value=${product_master.tiktok.toLocaleString()} color="info"></ea-stat-card>
        <ea-stat-card label="今日新增" .value=${product_master.today.toLocaleString()} color="ok"></ea-stat-card>
      </div>
    `;
  }
}
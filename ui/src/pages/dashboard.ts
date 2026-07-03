import { LitElement, html, css } from 'lit';
import { customElement, state } from 'lit/decorators.js';
import type { StatsResponse } from '../types';
import { getStats } from '../services/api';
import '../components/card';

interface Category {
  id: number;
  name: string;
  url: string;
  enabled: number;
  last_scraped_at: string | null;
  last_products_count: number | null;
  today_status: 'done' | 'pending' | 'skipped';
  today_count: number | null;
  today_time: string | null;
}

@customElement('ea-dashboard')
export class EaDashboard extends LitElement {
  static styles = css`
    :host { display: block; }
    h2 { font-size: 20px; font-weight: 700; color: var(--text-strong); margin-bottom: 24px; }
    .stats-grid { display: grid; grid-template-columns: repeat(2, 1fr); gap: 16px; margin-bottom: 24px; }
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
    .update-btn.amazon { background: var(--accent-subtle); color: var(--accent); border: 1px solid var(--accent); }
    .update-btn.amazon:hover { background: var(--accent); color: white; }
    .update-btn.tiktok { background: rgba(0, 242, 234, 0.1); color: #00f2ea; border: 1px solid #00f2ea; }
    .update-btn.tiktok:hover { background: #00f2ea; color: black; }
    .update-btn:disabled { opacity: 0.5; cursor: not-allowed; }

    /* 数据抓取卡片 */
    .fetch-panel { background: var(--card); border: 1px solid var(--border); border-radius: var(--radius-lg); margin-top: 8px; overflow: hidden; }
    .fetch-header { display: flex; align-items: center; justify-content: space-between; padding: 12px 16px; cursor: pointer; transition: background 0.15s ease; }
    .fetch-header:hover { background: var(--bg-hover); }
    .fetch-header-left { display: flex; align-items: center; gap: 8px; }
    .fetch-header-left svg { width: 16px; height: 16px; stroke: var(--muted); fill: none; stroke-width: 2; transition: transform 0.2s ease; }
    .fetch-panel.expanded .fetch-header-left svg { transform: rotate(90deg); }
    .fetch-header-title { font-size: 14px; font-weight: 500; color: var(--text); }
    .fetch-header-badge { font-size: 12px; color: var(--muted); }
    .fetch-header-right { display: flex; align-items: center; gap: 6px; }
    .fetch-header-btn { padding: 4px 10px; border-radius: 4px; font-size: 12px; cursor: pointer; border: 1px solid var(--border); background: var(--bg-elevated); color: var(--text); }
    .fetch-header-btn:hover { background: var(--bg-hover); }
    .fetch-header-btn:disabled { opacity: 0.5; cursor: not-allowed; }
    .fetch-content { display: none; padding: 16px; border-top: 1px solid var(--border); }
    .fetch-panel.expanded .fetch-content { display: block; }

    .category-list { max-height: 300px; overflow-y: auto; }
    .category-item { display: flex; align-items: center; padding: 8px 0; border-bottom: 1px solid var(--border); }
    .category-item:last-child { border-bottom: none; }
    .category-checkbox { width: 16px; height: 16px; margin-right: 12px; accent-color: var(--accent); cursor: pointer; }
    .category-name { flex: 1; font-size: 13px; color: var(--text); }
    .category-status { font-size: 12px; color: var(--muted); }
    .category-status.done, .category-status.skipped { color: var(--ok); }
    .category-status.pending { color: var(--muted); }

    .fetch-actions { display: flex; gap: 8px; margin-top: 16px; padding-top: 16px; border-top: 1px solid var(--border); }
    .fetch-actions button { padding: 8px 16px; border-radius: 6px; font-size: 13px; cursor: pointer; border: 1px solid var(--border); background: var(--bg-elevated); color: var(--text); }
    .fetch-actions button:hover { background: var(--bg-hover); }
    .fetch-actions button.primary { background: var(--accent); color: white; border-color: var(--accent); }
    .fetch-actions button.primary:hover { background: var(--accent-hover); }
    .fetch-actions button:disabled { opacity: 0.5; cursor: not-allowed; }
    .empty-text { text-align: center; color: var(--muted); padding: 24px; font-size: 13px; }

    @keyframes spin { to { transform: rotate(360deg); } }
    @media (max-width: 768px) { .stats-grid { grid-template-columns: 1fr; } }
  `;

  @state() private stats: StatsResponse | null = null;
  @state() private loading = true;
  @state() private error = '';

  @state() private expandedPanel: 'amazon' | 'tiktok' | null = null;
  @state() private categories: { amazon: Category[]; tiktok: Category[] } = { amazon: [], tiktok: [] };
  @state() private categoriesLoading = false;
  @state() private fetchTaskStatus: { amazon: string; tiktok: string } = { amazon: '', tiktok: '' };
  @state() private importStatus: { amazon: string; tiktok: string } = { amazon: '', tiktok: '' };

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

  private async _togglePanel(platform: 'amazon' | 'tiktok') {
    // 如果点击的是当前已展开的面板，则关闭
    if (this.expandedPanel === platform) {
      this.expandedPanel = null;
      this.requestUpdate();
      return;
    }
    
    this.expandedPanel = platform;
    this.requestUpdate();
    
    // 加载类目列表
    if (!this.categories[platform] || this.categories[platform].length === 0) {
      await this._loadCategories(platform);
    }
  }

  private async _loadCategories(platform: 'amazon' | 'tiktok') {
    this.categoriesLoading = true;
    this.requestUpdate();
    try {
      const response = await fetch(`/api/categories/${platform}`);
      const data = await response.json();
      this.categories = { ...this.categories, [platform]: data.categories || [] };
      this.requestUpdate();
    } catch (e) {
      console.error('加载类目失败:', e);
    } finally {
      this.categoriesLoading = false;
      this.requestUpdate();
    }
  }

  private async _refreshCategories(platform: 'amazon' | 'tiktok') {
    this.categoriesLoading = true;
    try {
      const response = await fetch(`/api/categories/${platform}/refresh`, { method: 'POST' });
      const data = await response.json();
      if (data.success) {
        await this._loadCategories(platform);
      } else {
        alert(data.message || '刷新失败');
      }
    } catch (e) {
      alert(`刷新失败: ${e}`);
    } finally {
      this.categoriesLoading = false;
    }
  }

  private async _toggleCategory(platform: 'amazon' | 'tiktok', categoryId: number, enabled: boolean) {
    try {
      await fetch(`/api/categories/${categoryId}/enabled?enabled=${enabled}`, { method: 'PUT' });
      // 更新本地状态
      this.categories = {
        ...this.categories,
        [platform]: this.categories[platform].map(c =>
          c.id === categoryId ? { ...c, enabled: enabled ? 1 : 0 } : c
        )
      };
    } catch (e) {
      alert(`更新失败: ${e}`);
    }
  }

  private async _selectAllCategories(platform: 'amazon' | 'tiktok') {
    const cats = this.categories[platform];
    try {
      // 批量更新
      await Promise.all(
        cats.map(cat =>
          fetch(`/api/categories/${cat.id}/enabled?enabled=true`, { method: 'PUT' })
        )
      );
      // 更新本地状态
      this.categories = {
        ...this.categories,
        [platform]: cats.map(c => ({ ...c, enabled: 1 }))
      };
      this.requestUpdate();
    } catch (e) {
      alert(`全选失败: ${e}`);
    }
  }

  private async _deselectAllCategories(platform: 'amazon' | 'tiktok') {
    const cats = this.categories[platform];
    try {
      // 批量更新
      await Promise.all(
        cats.map(cat =>
          fetch(`/api/categories/${cat.id}/enabled?enabled=false`, { method: 'PUT' })
        )
      );
      // 更新本地状态
      this.categories = {
        ...this.categories,
        [platform]: cats.map(c => ({ ...c, enabled: 0 }))
      };
      this.requestUpdate();
    } catch (e) {
      alert(`取消全选失败: ${e}`);
    }
  }

  private async _startFetch(platform: 'amazon' | 'tiktok') {
    this.fetchTaskStatus = { ...this.fetchTaskStatus, [platform]: 'running' };
    try {
      const response = await fetch(`/api/tasks/${platform}/fetch`, { method: 'POST' });
      const data = await response.json();
      if (data.success) {
        alert(`${platform} 抓取任务已启动`);
      } else {
        alert(data.message || '启动失败');
        this.fetchTaskStatus = { ...this.fetchTaskStatus, [platform]: '' };
      }
    } catch (e) {
      alert(`启动失败: ${e}`);
      this.fetchTaskStatus = { ...this.fetchTaskStatus, [platform]: '' };
    }
  }

  private async _importData(platform: 'amazon' | 'tiktok') {
    this.importStatus = { ...this.importStatus, [platform]: 'running' };
    this.requestUpdate();
    try {
      const response = await fetch('/api/tasks/data-import', { method: 'POST' });
      const data = await response.json();
      if (data.success) {
        // 导入成功后刷新统计数据
        await this.loadStats();
      } else {
        alert(data.message || '导入失败');
      }
    } catch (e) {
      alert(`导入失败: ${e}`);
    } finally {
      this.importStatus = { ...this.importStatus, [platform]: '' };
      this.requestUpdate();
    }
  }

  private _renderFetchPanel(platform: 'amazon' | 'tiktok') {
    const isExpanded = this.expandedPanel === platform;
    const cats = this.categories[platform];
    const isLoading = this.categoriesLoading;
    const taskRunning = this.fetchTaskStatus[platform] === 'running';

    const doneCount = cats.filter(c => c.today_status === 'done').length;
    const pendingCount = cats.filter(c => c.today_status === 'pending').length;

    return html`
      <div class="fetch-panel ${isExpanded ? 'expanded' : ''}">
        <div class="fetch-header">
          <div class="fetch-header-left" @click=${() => this._togglePanel(platform)}>
            <svg viewBox="0 0 24 24"><path d="M9 18l6-6-6-6"/></svg>
            <span class="fetch-header-title">数据抓取</span>
            ${cats.length > 0 ? html`
              <span class="fetch-header-badge">${cats.length} 个类目 · 今日已抓 ${doneCount} / 待抓 ${pendingCount}</span>
            ` : ''}
          </div>
          <div class="fetch-header-right">
            <button class="fetch-header-btn" @click=${(e: Event) => { e.stopPropagation(); this._selectAllCategories(platform); }} ?disabled=${isLoading || cats.length === 0}>
              全选
            </button>
            <button class="fetch-header-btn" @click=${(e: Event) => { e.stopPropagation(); this._deselectAllCategories(platform); }} ?disabled=${isLoading || cats.length === 0}>
              取消全选
            </button>
          </div>
        </div>

        <div class="fetch-content">
          ${isLoading ? html`<div class="empty-text">加载中...</div>` : ''}

          ${!isLoading && cats.length === 0 ? html`
            <div class="empty-text">暂无类目数据,请点击「刷新类目」获取</div>
          ` : ''}

          ${!isLoading && cats.length > 0 ? html`
            <div class="category-list">
              ${cats.map(cat => html`
                <div class="category-item">
                  <input
                    type="checkbox"
                    class="category-checkbox"
                    .checked=${cat.enabled === 1}
                    @change=${(e: Event) => { e.stopPropagation(); this._toggleCategory(platform, cat.id, (e.target as HTMLInputElement).checked); }}
                  >
                  <span class="category-name">${cat.name}</span>
                  <span class="category-status ${cat.today_status}">
                    ${cat.today_status === 'done' || cat.today_status === 'skipped'
                      ? `已抓 ${cat.today_count || cat.last_products_count || 0} 个`
                      : cat.last_scraped_at
                        ? `上次: ${new Date(cat.last_scraped_at).toLocaleDateString()}`
                        : '未抓取'}
                  </span>
                </div>
              `)}
            </div>
          ` : ''}

          <div class="fetch-actions">
            <button @click=${(e: Event) => { e.stopPropagation(); this._refreshCategories(platform); }} ?disabled=${isLoading}>
              刷新类目
            </button>
            <button
              class="primary"
              @click=${(e: Event) => { e.stopPropagation(); this._startFetch(platform); }}
              ?disabled=${taskRunning || cats.filter(c => c.enabled && c.today_status === 'pending').length === 0}
            >
              ${taskRunning ? '抓取中...' : '开始抓取'}
            </button>
          </div>
        </div>
      </div>
    `;
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

    const { amazon, tiktok } = this.stats;

    return html`
      <h2>数据概览</h2>

      <div class="stats-grid">
        <div>
          <ea-stat-card
            label="Amazon"
            .value=${amazon.products.toLocaleString()}
            icon="📦"
            desc="商品总数"
            color="accent"
          >
            <div style="display: flex; justify-content: space-between; align-items: center; margin-top: 12px;">
              <span style="font-size: 13px; color: var(--muted);">今日新增: ${amazon.today.toLocaleString()}</span>
              <button class="update-btn amazon" @click=${() => this._importData('amazon')} ?disabled=${this.importStatus.amazon === 'running'}>
                ${this.importStatus.amazon === 'running' ? '导入中...' : '更新数据'}
              </button>
            </div>
          </ea-stat-card>
          ${this._renderFetchPanel('amazon')}
        </div>

        <div>
          <ea-stat-card
            label="TikTok"
            .value=${tiktok.products.toLocaleString()}
            icon="🎵"
            desc="商品总数"
            color="info"
          >
            <div style="display: flex; justify-content: space-between; align-items: center; margin-top: 12px;">
              <span style="font-size: 13px; color: var(--muted);">今日新增: ${tiktok.today.toLocaleString()}</span>
              <button class="update-btn tiktok" @click=${() => this._importData('tiktok')} ?disabled=${this.importStatus.tiktok === 'running'}>
                ${this.importStatus.tiktok === 'running' ? '导入中...' : '更新数据'}
              </button>
            </div>
          </ea-stat-card>
          ${this._renderFetchPanel('tiktok')}
        </div>
      </div>
    `;
  }
}

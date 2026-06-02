import { LitElement, html, css } from 'lit';
import { customElement, state } from 'lit/decorators.js';

interface TranslationLog {
  id: number;
  batch_id: string;
  status: 'pending' | 'running' | 'completed' | 'failed';
  total_count: number;
  success_count: number;
  failed_count: number;
  started_at: string | null;
  completed_at: string | null;
  error_message: string | null;
  created_at: string;
}

interface TranslationStats {
  total_tasks: number;
  status_counts: Record<string, number>;
  total_count: number;
  success_count: number;
  failed_count: number;
  last_run: TranslationLog | null;
}

const API_BASE = '/api';

async function request<T>(url: string, options?: RequestInit): Promise<T> {
  const response = await fetch(url, options);
  if (!response.ok) {
    const error = await response.json().catch(() => ({ detail: 'Request failed' }));
    throw new Error(error.detail || `HTTP ${response.status}`);
  }
  return response.json();
}

async function getTranslationLogs(params: { page?: number; limit?: number; status?: string }): Promise<{
  data: TranslationLog[];
  pagination: { page: number; limit: number; total: number; pages: number };
}> {
  const query = new URLSearchParams(
    Object.entries(params)
      .filter(([, v]) => v !== undefined && v !== '')
      .map(([k, v]) => [k, String(v)])
  );
  return request(`${API_BASE}/translation-logs?${query}`);
}

async function getTranslationStats(): Promise<TranslationStats> {
  return request(`${API_BASE}/translation-logs/stats`);
}

@customElement('ea-translation-logs')
export class EaTranslationLogs extends LitElement {
  static styles = css`
    :host { display: block; }
    
    h2 {
      font-size: 20px;
      font-weight: 700;
      color: var(--text-strong);
      margin-bottom: 24px;
    }
    
    /* 统计卡片 */
    .stats-row {
      display: flex;
      gap: 16px;
      margin-bottom: 24px;
    }
    
    .stat-card {
      background: var(--card);
      border-radius: var(--radius-lg);
      border: 1px solid var(--border);
      padding: 16px 20px;
      flex: 1;
      display: flex;
      align-items: center;
      gap: 16px;
    }
    
    .stat-icon {
      width: 48px;
      height: 48px;
      border-radius: 12px;
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 24px;
    }
    
    .stat-icon.total { background: var(--accent-subtle); color: var(--accent); }
    .stat-icon.success { background: var(--ok-subtle); color: var(--ok); }
    .stat-icon.failed { background: var(--danger-subtle); color: var(--danger); }
    .stat-icon.pending { background: var(--warning-subtle); color: var(--warning); }
    
    .stat-content { flex: 1; }
    
    .stat-value {
      font-size: 28px;
      font-weight: 700;
      color: var(--text-strong);
    }
    
    .stat-label {
      font-size: 13px;
      color: var(--muted);
      margin-top: 2px;
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
    
    .select {
      padding: 8px 12px;
      border: 1px solid var(--border);
      border-radius: var(--radius-sm);
      font-size: 13px;
      background: var(--bg-elevated);
      color: var(--text);
    }
    
    .select:focus {
      outline: none;
      border-color: var(--accent);
    }
    
    .btn {
      padding: 8px 16px;
      border-radius: var(--radius-sm);
      font-size: 13px;
      font-weight: 500;
      cursor: pointer;
      transition: var(--duration-fast) ease;
      border: none;
    }
    
    .btn-secondary {
      background: var(--bg-elevated);
      color: var(--text);
      border: 1px solid var(--border);
    }
    
    .btn-secondary:hover { background: var(--bg-hover); }
    
    /* 表格 */
    .table-container {
      background: var(--card);
      border-radius: var(--radius-lg);
      border: 1px solid var(--border);
      overflow: hidden;
    }
    
    table { width: 100%; border-collapse: collapse; }
    
    th {
      background: var(--bg-accent);
      padding: 12px 16px;
      font-size: 12px;
      font-weight: 600;
      color: var(--muted);
      text-align: left;
      border-bottom: 1px solid var(--border);
      white-space: nowrap;
    }
    
    td {
      padding: 12px 16px;
      font-size: 13px;
      color: var(--text);
      border-bottom: 1px solid var(--border);
      vertical-align: middle;
    }
    
    tr:last-child td { border-bottom: none; }
    tr:hover td { background: var(--card-highlight); }
    
    /* 状态标签 */
    .status-badge {
      display: inline-flex;
      align-items: center;
      gap: 4px;
      padding: 4px 10px;
      border-radius: 20px;
      font-size: 12px;
      font-weight: 500;
    }
    
    .status-badge.pending {
      background: var(--warning-subtle);
      color: var(--warning);
    }
    
    .status-badge.running {
      background: var(--accent-subtle);
      color: var(--accent);
    }
    
    .status-badge.completed {
      background: var(--ok-subtle);
      color: var(--ok);
    }
    
    .status-badge.failed {
      background: var(--danger-subtle);
      color: var(--danger);
    }
    
    .status-dot {
      width: 6px;
      height: 6px;
      border-radius: 50%;
      background: currentColor;
    }
    
    .status-badge.running .status-dot {
      animation: pulse 1.5s infinite;
    }
    
    @keyframes pulse {
      0%, 100% { opacity: 1; }
      50% { opacity: 0.4; }
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
    
    /* 空状态 */
    .empty-state {
      text-align: center;
      padding: 48px;
      color: var(--muted);
    }
    
    .empty-icon {
      font-size: 48px;
      margin-bottom: 16px;
      opacity: 0.5;
    }
    
    /* 加载状态 */
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

  @state() private logs: TranslationLog[] = [];
  @state() private stats: TranslationStats | null = null;
  @state() private loading = true;
  @state() private page = 1;
  @state() private pages = 0;
  @state() private statusFilter = '';

  async connectedCallback() {
    super.connectedCallback();
    await this.loadData();
  }

  async loadData() {
    this.loading = true;
    try {
      const [logsRes, statsRes] = await Promise.all([
        getTranslationLogs({
          page: this.page,
          limit: 20,
          status: this.statusFilter || undefined,
        }),
        getTranslationStats(),
      ]);
      this.logs = logsRes.data;
      this.pages = logsRes.pagination.pages;
      this.stats = statsRes;
    } catch (e) {
      console.error('Failed to load translation logs:', e);
    } finally {
      this.loading = false;
      this.requestUpdate();
    }
  }

  private _onStatusFilter(e: Event) {
    this.statusFilter = (e.target as HTMLSelectElement).value;
    this.page = 1;
    this.loadData();
  }

  private _onPageChange(newPage: number) {
    this.page = newPage;
    this.loadData();
  }

  private _formatDateTime(dateStr: string | null): string {
    if (!dateStr) return '-';
    const date = new Date(dateStr);
    return date.toLocaleString('zh-CN', {
      year: 'numeric',
      month: '2-digit',
      day: '2-digit',
      hour: '2-digit',
      minute: '2-digit',
      second: '2-digit',
    });
  }

  private _renderStatusBadge(status: string) {
    const labels: Record<string, string> = {
      pending: '等待中',
      running: '运行中',
      completed: '已完成',
      failed: '失败',
    };
    return html`
      <span class="status-badge ${status}">
        <span class="status-dot"></span>
        ${labels[status] || status}
      </span>
    `;
  }

  private _renderPagination() {
    const pages = [];
    const maxVisible = 5;
    let start = Math.max(1, this.page - Math.floor(maxVisible / 2));
    let end = Math.min(this.pages, start + maxVisible - 1);
    
    if (end - start < maxVisible - 1) {
      start = Math.max(1, end - maxVisible + 1);
    }
    
    if (start > 1) {
      pages.push(html`
        <button class="page-btn" @click=${() => this._onPageChange(1)}>1</button>
        ${start > 2 ? html`<span style="color:var(--muted)">...</span>` : ''}
      `);
    }
    
    for (let i = start; i <= end; i++) {
      pages.push(html`
        <button class="page-btn ${i === this.page ? 'active' : ''}" @click=${() => this._onPageChange(i)}>${i}</button>
      `);
    }
    
    if (end < this.pages) {
      pages.push(html`
        ${end < this.pages - 1 ? html`<span style="color:var(--muted)">...</span>` : ''}
        <button class="page-btn" @click=${() => this._onPageChange(this.pages)}>${this.pages}</button>
      `);
    }
    
    return html`<div class="pagination">${pages}</div>`;
  }

  render() {
    return html`
      <h2>翻译日志</h2>
      
      ${this.stats ? html`
        <div class="stats-row">
          <div class="stat-card">
            <div class="stat-icon total">📋</div>
            <div class="stat-content">
              <div class="stat-value">${this.stats.total_tasks}</div>
              <div class="stat-label">总任务数</div>
            </div>
          </div>
          <div class="stat-card">
            <div class="stat-icon success">✅</div>
            <div class="stat-content">
              <div class="stat-value">${this.stats.success_count}</div>
              <div class="stat-label">翻译成功</div>
            </div>
          </div>
          <div class="stat-card">
            <div class="stat-icon failed">❌</div>
            <div class="stat-content">
              <div class="stat-value">${this.stats.failed_count}</div>
              <div class="stat-label">翻译失败</div>
            </div>
          </div>
          <div class="stat-card">
            <div class="stat-icon pending">⏳</div>
            <div class="stat-content">
              <div class="stat-value">${this.stats.status_counts.pending || 0}</div>
              <div class="stat-label">等待中</div>
            </div>
          </div>
        </div>
      ` : ''}
      
      <div class="toolbar">
        <select class="select" @change=${this._onStatusFilter}>
          <option value="">全部状态</option>
          <option value="pending" ?selected=${this.statusFilter === 'pending'}>等待中</option>
          <option value="running" ?selected=${this.statusFilter === 'running'}>运行中</option>
          <option value="completed" ?selected=${this.statusFilter === 'completed'}>已完成</option>
          <option value="failed" ?selected=${this.statusFilter === 'failed'}>失败</option>
        </select>
        <button class="btn btn-secondary" @click=${() => this.loadData()}>刷新</button>
      </div>
      
      ${this.loading ? html`
        <div class="loading">
          <div class="spinner"></div>
          <p>加载中...</p>
        </div>
      ` : this.logs.length === 0 ? html`
        <div class="table-container">
          <div class="empty-state">
            <div class="empty-icon">📝</div>
            <p>暂无翻译日志</p>
          </div>
        </div>
      ` : html`
        <div class="table-container">
          <table>
            <thead>
              <tr>
                <th>批次ID</th>
                <th>状态</th>
                <th>总数</th>
                <th>成功</th>
                <th>失败</th>
                <th>开始时间</th>
                <th>完成时间</th>
                <th>错误信息</th>
              </tr>
            </thead>
            <tbody>
              ${this.logs.map(log => html`
                <tr>
                  <td style="font-family:var(--mono);font-size:12px">${log.batch_id}</td>
                  <td>${this._renderStatusBadge(log.status)}</td>
                  <td>${log.total_count}</td>
                  <td style="color:var(--ok)">${log.success_count}</td>
                  <td style="color:var(--danger)">${log.failed_count}</td>
                  <td>${this._formatDateTime(log.started_at)}</td>
                  <td>${this._formatDateTime(log.completed_at)}</td>
                  <td style="color:var(--danger);font-size:12px">${log.error_message || '-'}</td>
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
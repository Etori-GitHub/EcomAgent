import { LitElement, html, css } from 'lit';
import { customElement, state } from 'lit/decorators.js';

@customElement('ea-export')
export class EaExport extends LitElement {
  static styles = css`
    :host { display: block; }
    
    .export-grid {
      display: grid;
      grid-template-columns: repeat(2, 1fr);
      gap: 16px;
      margin-bottom: 24px;
    }
    
    .export-card {
      background: var(--card);
      border-radius: var(--radius-lg);
      border: 1px solid var(--border);
      padding: 20px;
    }
    
    .export-header {
      display: flex;
      align-items: center;
      gap: 12px;
      margin-bottom: 12px;
    }
    
    .export-icon {
      font-size: 24px;
    }
    
    .export-title {
      font-size: 16px;
      font-weight: 600;
      color: var(--text-strong);
    }
    
    .export-desc {
      font-size: 11px;
      color: var(--muted);
    }
    
    .export-stats {
      display: flex;
      gap: 16px;
      margin-bottom: 16px;
      padding: 12px;
      background: var(--bg-elevated);
      border-radius: var(--radius-sm);
    }
    
    .stat-item {
      text-align: center;
    }
    
    .stat-value {
      font-size: 18px;
      font-weight: 600;
      color: var(--text-strong);
    }
    
    .stat-label {
      font-size: 10px;
      color: var(--muted);
    }
    
    .export-btn {
      width: 100%;
      padding: 8px 16px;
      border-radius: var(--radius-sm);
      font-size: 13px;
      font-weight: 500;
      border: 1px solid var(--border);
      cursor: pointer;
      transition: var(--duration-fast) ease;
      background: var(--bg-elevated);
      color: var(--text);
    }
    
    .export-btn:hover {
      background: var(--bg-hover);
      border-color: var(--accent);
    }
    
    .export-btn.primary {
      background: var(--accent);
      color: var(--accent-foreground);
      border-color: var(--accent);
    }
    
    .export-btn.primary:hover {
      background: var(--accent-hover);
    }
    
    .options-card {
      background: var(--card);
      border-radius: var(--radius-lg);
      border: 1px solid var(--border);
      padding: 20px;
    }
    
    .options-title {
      font-size: 14px;
      font-weight: 600;
      color: var(--text-strong);
      margin-bottom: 16px;
    }
    
    .option-row {
      display: flex;
      justify-content: space-between;
      align-items: center;
      padding: 8px 0;
      border-bottom: 1px solid var(--border);
    }
    
    .option-row:last-child {
      border-bottom: none;
    }
    
    .option-label {
      font-size: 13px;
      color: var(--text);
    }
    
    .select {
      padding: 6px 12px;
      border: 1px solid var(--border);
      border-radius: var(--radius-sm);
      font-size: 13px;
      background: var(--bg-elevated);
      color: var(--text);
    }
    
    @media (max-width: 768px) {
      .export-grid { grid-template-columns: 1fr; }
    }
  `;

  @state() private format: 'csv' | 'excel' = 'csv';
  @state() private dateRange: 'all' | '7d' | '30d' = 'all';

  private _export(platform: 'amazon' | 'tiktok' | 'all') {
    console.log('Export:', { platform, format: this.format, dateRange: this.dateRange });
    alert(`导出功能开发中...\n平台: ${platform}\n格式: ${this.format}\n时间范围: ${this.dateRange}`);
  }

  render() {
    return html`
      <h2 style="font-size:20px;font-weight:700;color:var(--text-strong);margin-bottom:24px">数据导出</h2>

      <div class="export-grid">
        <div class="export-card">
          <div class="export-header">
            <span class="export-icon">📊</span>
            <div>
              <div class="export-title">Amazon 数据</div>
              <div class="export-desc">导出 Amazon 所有产品数据</div>
            </div>
          </div>
          <div class="export-stats">
            <div class="stat-item">
              <div class="stat-value">327</div>
              <div class="stat-label">产品数</div>
            </div>
            <div class="stat-item">
              <div class="stat-value">1800</div>
              <div class="stat-label">销售记录</div>
            </div>
          </div>
          <button class="export-btn primary" @click=${() => this._export('amazon')}>导出 Amazon 数据</button>
        </div>

        <div class="export-card">
          <div class="export-header">
            <span class="export-icon">🎵</span>
            <div>
              <div class="export-title">TikTok 数据</div>
              <div class="export-desc">导出 TikTok Shop 所有产品数据</div>
            </div>
          </div>
          <div class="export-stats">
            <div class="stat-item">
              <div class="stat-value">950</div>
              <div class="stat-label">产品数</div>
            </div>
            <div class="stat-item">
              <div class="stat-value">950</div>
              <div class="stat-label">销售记录</div>
            </div>
          </div>
          <button class="export-btn primary" @click=${() => this._export('tiktok')}>导出 TikTok 数据</button>
        </div>
      </div>

      <div class="options-card">
        <div class="options-title">导出选项</div>
        
        <div class="option-row">
          <span class="option-label">导出格式</span>
          <select class="select" .value=${this.format} @change=${(e: Event) => this.format = (e.target as HTMLSelectElement).value as any}>
            <option value="csv">CSV</option>
            <option value="excel">Excel</option>
          </select>
        </div>
        
        <div class="option-row">
          <span class="option-label">时间范围</span>
          <select class="select" .value=${this.dateRange} @change=${(e: Event) => this.dateRange = (e.target as HTMLSelectElement).value as any}>
            <option value="all">全部</option>
            <option value="7d">近7天</option>
            <option value="30d">近30天</option>
          </select>
        </div>
      </div>

      <div style="margin-top:24px">
        <button class="export-btn" style="width:100%" @click=${() => this._export('all')}>导出全部数据</button>
      </div>
    `;
  }
}
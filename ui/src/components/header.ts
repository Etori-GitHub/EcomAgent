import { LitElement, html, css } from 'lit';
import { customElement, property } from 'lit/decorators.js';
import type { PageName } from '../types';

const PAGE_TITLES: Record<PageName, { title: string; subtitle: string }> = {
  'dashboard': { title: '数据概览', subtitle: '查看数据统计和概览' },
  'product-master': { title: '商品总库', subtitle: '统一管理所有平台商品' },
  'sourcing': { title: '货源库', subtitle: '1688货源采集与管理' },
  'assets': { title: '素材管理', subtitle: '生成和管理商品素材' },
  'tracking': { title: '商品追踪', subtitle: '追踪特定商品的价格、销量变化' },
  'cross-platform': { title: '跨平台分析', subtitle: '对比分析不同平台数据' },
  'today-top': { title: '今日TOP榜', subtitle: '各平台热销产品排行' },
  'raw-data': { title: '原始数据', subtitle: '查看和搜索原始数据' },
  'export': { title: '数据导出', subtitle: '导出数据为 CSV 或 Excel' },
  'translation-logs': { title: '翻译日志', subtitle: '翻译任务执行记录' },
  'settings': { title: '系统设置', subtitle: '配置数据源和其他选项' },
  'product-trend': { title: '商品趋势', subtitle: '查看商品各维度数据随时间变化' },
};

@customElement('ea-header')
export class EaHeader extends LitElement {
  static styles = css`
    :host {
      display: flex;
      align-items: center;
      justify-content: space-between;
      margin-bottom: 24px;
      padding-bottom: 16px;
      border-bottom: 1px solid var(--border);
    }

    .title {
      font-size: 20px;
      font-weight: 700;
      color: var(--text-strong);
    }

    .subtitle {
      font-size: 13px;
      color: var(--muted);
      margin-top: 2px;
    }

    .actions {
      display: flex;
      align-items: center;
      gap: 8px;
    }

    .icon-btn {
      width: 30px;
      height: 30px;
      display: flex;
      align-items: center;
      justify-content: center;
      border: 1px solid var(--border);
      border-radius: var(--radius-full);
      background: var(--bg-elevated);
      color: var(--muted);
      cursor: pointer;
      transition: var(--duration-fast) ease;
    }

    .icon-btn:hover {
      color: var(--text);
      background: var(--bg-hover);
    }

    .icon-btn svg {
      width: 14px;
      height: 14px;
      stroke: currentColor;
      fill: none;
      stroke-width: 1.75px;
    }
  `;

  @property({ type: String }) currentPage: PageName = 'dashboard';

  private toggleTheme() {
    const body = document.body;
    const current = body.getAttribute('data-theme-mode');
    const next = current === 'dark' ? 'light' : 'dark';
    body.setAttribute('data-theme-mode', next);
    localStorage.setItem('theme', next);
    this.requestUpdate();
  }

  render() {
    const { title, subtitle } = PAGE_TITLES[this.currentPage];
    const isDark = document.body.getAttribute('data-theme-mode') !== 'light';

    return html`
      <div>
        <div class="title">${title}</div>
        <div class="subtitle">${subtitle}</div>
      </div>
      
      <div class="actions">
        <button class="icon-btn" @click=${this.toggleTheme} title="切换主题">
          ${isDark ? html`
            <svg viewBox="0 0 24 24">
              <path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"></path>
            </svg>
          ` : html`
            <svg viewBox="0 0 24 24">
              <circle cx="12" cy="12" r="4"></circle>
              <path d="M12 2v2M12 20v2M4.93 4.93l1.41 1.41M17.66 17.66l1.41 1.41M2 12h2M20 12h2M6.34 17.66l-1.41 1.41M19.07 4.93l-1.41 1.41"></path>
            </svg>
          `}
        </button>
        
        <button class="icon-btn" @click=${() => this.dispatchEvent(new Event('refresh'))} title="刷新数据">
          <svg viewBox="0 0 24 24">
            <path d="M23 4v6h-6M1 20v-6h6M3.51 9a9 9 0 0 1 14.85-3.36L23 10M1 14l5.64 5.64A9 9 0 0 0 20.49 15"></path>
          </svg>
        </button>
      </div>
    `;
  }
}

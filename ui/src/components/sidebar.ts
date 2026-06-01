import { LitElement, html, css } from 'lit';
import { customElement, property, state } from 'lit/decorators.js';
import { unsafeSVG } from 'lit/directives/unsafe-svg.js';
import type { PageName } from '../types';
import * as api from '../services/api';

const NAV_ITEMS: { group: string; items: { id: PageName; icon: string; label: string }[] }[] = [
  { group: 'Main', items: [
    { id: 'dashboard', icon: 'grid', label: '数据概览' },
    { id: 'product-master', icon: 'box', label: '商品总库' },
    { id: 'sourcing', icon: 'package', label: '货源库' },
    { id: 'tracking', icon: 'target', label: '商品追踪' },
    { id: 'cross-platform', icon: 'sync', label: '跨平台分析' },
  ]},
  { group: '平台数据', items: [
    { id: 'today-top', icon: 'star', label: '今日TOP榜' },
    { id: 'raw-data', icon: 'database', label: '原始数据' },
  ]},
  { group: '配置', items: [
    { id: 'export', icon: 'download', label: '数据导出' },
    { id: 'settings', icon: 'settings', label: '系统设置' },
  ]},
];

const ICONS: Record<string, string> = {
  grid: '<rect x="3" y="3" width="7" height="7" rx="1"/><rect x="14" y="3" width="7" height="7" rx="1"/><rect x="3" y="14" width="7" height="7" rx="1"/><rect x="14" y="14" width="7" height="7" rx="1"/>',
  box: '<path d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z"/><polyline points="3.27 6.96 12 12.01 20.73 6.96"/><line x1="12" y1="22.08" x2="12" y2="12"/>',
  package: '<line x1="16.5" y1="9.4" x2="7.5" y1="4.21"/><path d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z"/><polyline points="3.27 6.96 12 12.01 20.73 6.96"/><line x1="12" y1="22.08" x2="12" y2="12"/><line x1="12" y1="12" x2="7.5" y1="9.4"/>',
  target: '<circle cx="12" cy="12" r="3"/><path d="M12 2v4M12 18v4M2 12h4M18 12h4"/>',
  sync: '<path d="M16 3h5v5M8 21H3v-5M21 3l-7 7M3 21l7-7"/>',
  star: '<path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/>',
  database: '<ellipse cx="12" cy="5" rx="9" ry="3"/><path d="M21 12c0 1.66-4 3-9 3s-9-1.34-9-3"/><path d="M3 5v14c0 1.66 4 3 9 3s9-1.34 9-3V5"/>',
  download: '<path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="7 10 12 15 17 10"/><line x1="12" y1="15" x2="12" y2="3"/>',
  settings: '<circle cx="12" cy="12" r="3"/><path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1 0 2.83 2 2 0 0 1-2.83 0l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-2 2 2 2 0 0 1-2-2v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83 0 2 2 0 0 1 0-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1-2-2 2 2 0 0 1 2-2h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 0-2.83 2 2 0 0 1 2.83 0l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 2-2 2 2 0 0 1 2 2v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 0 2 2 0 0 1 0 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 2 2 2 2 0 0 1-2 2h-.09a1.65 1.65 0 0 0-1.51 1z"/>',
};

declare global {
  interface Window {
    ecomagentNavigate: (page: PageName) => void;
    ecomagentGetCurrentPage: () => PageName;
    ecomagentOnPageChange: (callback: (page: PageName) => void) => void;
    ecomagentAppName?: string;
  }
}

@customElement('ea-sidebar')
export class EaSidebar extends LitElement {
  static styles = css`
    :host { width: 258px; background: var(--panel); color: var(--text); padding: 14px 10px 12px; flex-shrink: 0; border-right: 1px solid var(--border); transition: width 0.2s ease; overflow: hidden; display: flex; flex-direction: column; }
    :host([collapsed]) { width: 60px; padding: 14px 6px 12px; }
    .header { display: flex; align-items: center; justify-content: space-between; padding: 14px 10px; border-bottom: 1px solid var(--border); margin-bottom: 12px; flex-shrink: 0; }
    :host([collapsed]) .header { justify-content: center; border-bottom: none; padding: 14px 0; }
    .brand { display: flex; align-items: center; gap: 10px; }
    :host([collapsed]) .brand { display: none; }
    .logo { width: 32px; height: 32px; background: var(--accent); border-radius: 8px; display: flex; align-items: center; justify-content: center; color: white; font-weight: bold; font-size: 16px; }
    .brand-text { display: flex; flex-direction: column; gap: 2px; }
    .brand-title { font-size: 15px; font-weight: 700; color: var(--text-strong); }
    .brand-subtitle { font-size: 10px; color: var(--muted); }
    .toggle-btn { width: 28px; height: 28px; display: flex; align-items: center; justify-content: center; background: transparent; border: none; border-radius: 6px; cursor: pointer; color: var(--muted); transition: 0.15s ease; }
    .toggle-btn:hover { color: var(--text); background: var(--bg-hover); }
    .toggle-btn svg { width: 16px; height: 16px; stroke: currentColor; fill: none; stroke-width: 1.5; transition: transform 0.15s ease; }
    :host([collapsed]) .toggle-btn svg { transform: rotate(180deg); }
    .nav-content { flex: 1; overflow-y: auto; }
    .nav-group { margin-bottom: 8px; }
    .nav-group-header { padding: 8px 10px; margin-bottom: 4px; }
    :host([collapsed]) .nav-group-header { display: none; }
    .nav-group-title { font-size: 11px; font-weight: 600; color: var(--muted); text-transform: uppercase; letter-spacing: 0.05em; }
    .nav-items { list-style: none; padding: 0; margin: 0; display: flex; flex-direction: column; gap: 4px; }
    .nav-item { padding: 8px 10px; cursor: pointer; border-radius: 8px; font-size: 13px; font-weight: 500; display: flex; align-items: center; gap: 8px; color: var(--muted); border: 1px solid transparent; background: transparent; user-select: none; transition: 0.15s ease; }
    .nav-item:hover { background: var(--bg-hover); border-color: var(--border-hover); color: var(--text); }
    .nav-item.active { background: var(--accent-subtle); border-color: color-mix(in srgb, var(--accent) 25%, transparent); color: var(--accent); }
    :host([collapsed]) .nav-item { justify-content: center; padding: 8px 0; }
    .nav-icon { width: 18px; height: 18px; stroke: currentColor; fill: none; stroke-width: 1.5; stroke-linecap: round; stroke-linejoin: round; flex-shrink: 0; }
    :host([collapsed]) .nav-icon { display: block; }
    :host([collapsed]) .nav-label { display: none; }
  `;

  @property({ type: Boolean, reflect: true }) collapsed = false;
  
  // 应用名称（从配置读取）
  @state() private appName: string = window.ecomagentAppName || 'EcomAgent';
  
  // 内部状态，不通过属性传递
  private _currentPage: PageName = 'dashboard';

  constructor() {
    super();
    // 加载应用名称配置
    this._loadAppName();
    // 监听全局页面变化
    if (window.ecomagentOnPageChange) {
      window.ecomagentOnPageChange((page) => {
        this._currentPage = page;
        this.requestUpdate();
      });
    }
    // 获取初始页面
    if (window.ecomagentGetCurrentPage) {
      this._currentPage = window.ecomagentGetCurrentPage();
    }
  }

  private async _loadAppName() {
    // 如果全局已有缓存，直接使用
    if (window.ecomagentAppName) {
      this.appName = window.ecomagentAppName;
      return;
    }
    try {
      const result = await api.getAppName();
      this.appName = result.app_name;
      window.ecomagentAppName = result.app_name; // 缓存到全局
    } catch (e) {
      console.error('Failed to load app name:', e);
    }
  }

  private _onNavClick(page: PageName) {
    // 货源库直接导航时清除筛选
    if (page === 'sourcing' && window.ecomagentNavigateDirectToSourcing) {
      window.ecomagentNavigateDirectToSourcing();
      return;
    }
    if (window.ecomagentNavigate) {
      window.ecomagentNavigate(page);
    }
  }

  private _onToggle() {
    this.collapsed = !this.collapsed;
    this.requestUpdate('collapsed');
  }

  render() {
    const currentPage = this._currentPage;
    const firstChar = this.appName.charAt(0);
    return html`
      <div class="header">
        <div class="brand">
          <div class="logo">${firstChar}</div>
          <div class="brand-text">
            <span class="brand-title">${this.appName}</span>
            <span class="brand-subtitle">数据可视化平台</span>
          </div>
        </div>
        <button class="toggle-btn" @click=${this._onToggle}>
          <svg viewBox="0 0 24 24"><path d="M15 18l-6-6 6-6"/></svg>
        </button>
      </div>
      <div class="nav-content">
        ${NAV_ITEMS.map(group => html`
          <div class="nav-group">
            <div class="nav-group-header"><span class="nav-group-title">${group.group}</span></div>
            <ul class="nav-items">
              ${group.items.map(item => html`
                <li class="nav-item ${currentPage === item.id ? 'active' : ''}" @click=${() => this._onNavClick(item.id)}>
                  <svg class="nav-icon" viewBox="0 0 24 24">${unsafeSVG(ICONS[item.icon])}</svg>
                  <span class="nav-label">${item.label}</span>
                </li>
              `)}
            </ul>
          </div>
        `)}
      </div>
    `;
  }
}
import { LitElement, html, css } from 'lit';
import { customElement, state } from 'lit/decorators.js';
import type { PageName } from './types';
import './components/layout';
import './pages/dashboard';
import './pages/product-master';
import './pages/tracking';
import './pages/settings';
import './pages/today-top';
import './pages/raw-data';
import './pages/cross-platform';
import './pages/export';
import './pages/product-trend';
import './pages/product-trend-page';
import './pages/sourcing';

// 全局状态
const _listeners: Set<(page: PageName) => void> = new Set();
let _currentPage: PageName = 'dashboard';

// 暴露给全局
window.ecomagentNavigate = (page: PageName) => {
  _currentPage = page;
  _listeners.forEach(fn => fn(page));
};

window.ecomagentGetCurrentPage = () => _currentPage;

window.ecomagentOnPageChange = (callback: (page: PageName) => void) => {
  _listeners.add(callback);
};

// 趋势页面跳转（保存来源状态）
window.ecomagentOpenTrend = (ecomCode: string, fromPage: string = 'product-master') => {
  // 保存来源信息
  sessionStorage.setItem('trend-source-page', fromPage);
  sessionStorage.setItem('trend-source-state', JSON.stringify({
    page: _currentPage,
    scrollY: window.scrollY
  }));
  // 跳转到趋势页面
  _currentPage = 'product-trend' as PageName;
  // 存储商品编码
  sessionStorage.setItem('trend-ecom-code', ecomCode);
  _listeners.forEach(fn => fn('product-trend' as PageName));
};

// 货源页面跳转
window.ecomagentNavigateToSourcing = (ecomCode?: string) => {
  _currentPage = 'sourcing' as PageName;
  if (ecomCode) {
    sessionStorage.setItem('sourcing-ecom-code', ecomCode);
  } else {
    sessionStorage.removeItem('sourcing-ecom-code');
  }
  _listeners.forEach(fn => fn('sourcing' as PageName));
};

@customElement('ecomagent-app')
export class EcomagentApp extends LitElement {
  static styles = css`:host { display: block; min-height: 100vh; }`;

  @state() private _page: PageName = _currentPage;
  @state() private _trendCode = '';
  @state() private _sourcingCode = '';

  constructor() {
    super();
    _listeners.add((page) => {
      this._page = page;
      if (page === 'product-trend') {
        this._trendCode = sessionStorage.getItem('trend-ecom-code') || '';
      }
      if (page === 'sourcing') {
        this._sourcingCode = sessionStorage.getItem('sourcing-ecom-code') || '';
      }
      this.requestUpdate();
    });
  }

  connectedCallback() {
    super.connectedCallback();
    const theme = localStorage.getItem('theme') || 'dark';
    document.body.setAttribute('data-theme-mode', theme);
  }

  private _renderPage() {
    switch (this._page) {
      case 'dashboard': return html`<ea-dashboard></ea-dashboard>`;
      case 'settings': return html`<ea-settings></ea-settings>`;
      case 'product-master': return html`<ea-product-master></ea-product-master>`;
      case 'tracking': return html`<ea-tracking></ea-tracking>`;
      case 'cross-platform': return html`<ea-cross-platform></ea-cross-platform>`;
      case 'today-top': return html`<ea-today-top></ea-today-top>`;
      case 'raw-data': return html`<ea-raw-data></ea-raw-data>`;
      case 'export': return html`<ea-export></ea-export>`;
      case 'product-trend': return html`<ea-product-trend-page ecomCode=${this._trendCode}></ea-product-trend-page>`;
      case 'sourcing': return html`<ea-sourcing ecomCode=${this._sourcingCode}></ea-sourcing>`;
      default: return html`<div style="padding:24px;color:var(--muted)">未知页面</div>`;
    }
  }

  render() {
    // 趋势页面和货源页面需要特殊处理
    if (this._page === 'product-trend') {
      return html`
        <ea-layout currentPage=${this._page}>
          <div style="padding:24px">${this._renderPage()}</div>
        </ea-layout>
      `;
    }

    // 所有其他页面在布局内
    return html`
      <ea-layout currentPage=${this._page}>
        ${this._renderPage()}
      </ea-layout>
    `;
  }
}

// 扩展 window 类型
declare global {
  interface Window {
    ecomagentNavigate: (page: PageName) => void;
    ecomagentGetCurrentPage: () => PageName;
    ecomagentOnPageChange: (callback: (page: PageName) => void) => void;
    ecomagentOpenTrend: (ecomCode: string, fromPage?: string) => void;
    ecomagentNavigateToSourcing: (ecomCode?: string) => void;
  }
}

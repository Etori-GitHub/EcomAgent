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

@customElement('ecomagent-app')
export class EcomagentApp extends LitElement {
  static styles = css`:host { display: block; min-height: 100vh; }`;

  @state() private _page: PageName = _currentPage;

  constructor() {
    super();
    _listeners.add((page) => {
      this._page = page;
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
      default: return html`<div style="padding:24px;color:var(--muted)">未知页面</div>`;
    }
  }

  render() {
    return html`
      <ea-layout currentPage=${this._page}>
        ${this._renderPage()}
      </ea-layout>
    `;
  }
}
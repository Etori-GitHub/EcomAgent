import { LitElement, html, css } from 'lit';
import { customElement, property, state } from 'lit/decorators.js';
import type { PageName } from '../types';
import './sidebar';
import './header';

@customElement('ea-layout')
export class EaLayout extends LitElement {
  static styles = css`
    :host { display: flex; min-height: 100vh; }
    .main-content { flex: 1; padding: 24px; overflow-y: auto; background: var(--bg); }
    .content-body { animation: fadeIn 0.3s ease; }
    @media (max-width: 1024px) { :host { flex-direction: column; } .main-content { padding: 16px; } }
  `;

  @property({ type: String }) currentPage: PageName = 'dashboard';
  @state() sidebarCollapsed = false;

  render() {
    return html`
      <ea-sidebar ?collapsed=${this.sidebarCollapsed}></ea-sidebar>
      <main class="main-content">
        <ea-header .currentPage=${this.currentPage}></ea-header>
        <div class="content-body"><slot></slot></div>
      </main>
    `;
  }
}
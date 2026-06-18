import { LitElement, html, css } from 'lit';
import { customElement, state } from 'lit/decorators.js';

/**
 * 系统设置页面
 * 简化版本：只保留 API 密钥、软件名称、国家/语言配置
 */
@customElement('ea-settings')
export class EaSettings extends LitElement {
  @state() private loading = true;
  @state() private saving = false;
  
  // 配置数据
  @state() private appName = '';
  @state() private country = '马来西亚';
  @state() private language = '马来语';
  @state() private apiKeys: { google: string; volcano: string; xai: string } = { google: '', volcano: '', xai: '' };
  
  // 编辑状态
  @state() private editingField = '';
  @state() private editValue = '';

  static styles = css`
    :host { display: block; padding: 24px; max-width: 800px; }
    
    h2 {
      font-size: 20px;
      font-weight: 700;
      color: var(--text);
      margin-bottom: 24px;
    }
    
    .section {
      background: var(--card);
      border: 1px solid var(--border);
      border-radius: var(--radius-lg);
      margin-bottom: 20px;
      overflow: hidden;
    }
    
    .section-header {
      display: flex;
      align-items: center;
      gap: 12px;
      padding: 16px 20px;
      background: var(--bg);
      border-bottom: 1px solid var(--border);
    }
    
    .section-icon {
      font-size: 20px;
    }
    
    .section-title {
      font-size: 15px;
      font-weight: 600;
      color: var(--text);
    }
    
    .section-body {
      padding: 20px;
    }
    
    .field-row {
      display: flex;
      align-items: center;
      justify-content: space-between;
      padding: 12px 0;
      border-bottom: 1px solid var(--border);
    }
    
    .field-row:last-child {
      border-bottom: none;
    }
    
    .field-label {
      font-size: 14px;
      color: var(--text);
    }
    
    .field-value {
      display: flex;
      align-items: center;
      gap: 8px;
    }
    
    .field-text {
      font-size: 14px;
      color: var(--muted);
      max-width: 300px;
      overflow: hidden;
      text-overflow: ellipsis;
      white-space: nowrap;
    }
    
    .field-input {
      padding: 6px 12px;
      border: 1px solid var(--border);
      border-radius: var(--radius-sm);
      background: var(--bg);
      color: var(--text);
      font-size: 14px;
      min-width: 200px;
    }
    
    .field-input:focus {
      outline: none;
      border-color: var(--primary);
    }
    
    .btn {
      padding: 6px 12px;
      border-radius: var(--radius-sm);
      font-size: 13px;
      cursor: pointer;
      border: 1px solid var(--border);
      background: var(--bg);
      color: var(--text);
    }
    
    .btn:hover {
      background: var(--bg-hover);
    }
    
    .btn-primary {
      background: var(--primary);
      color: white;
      border-color: var(--primary);
    }
    
    .btn-primary:hover {
      opacity: 0.9;
    }
    
    .btn-primary:disabled {
      opacity: 0.5;
      cursor: not-allowed;
    }
    
    .api-key-masked {
      font-family: monospace;
      letter-spacing: 2px;
    }
    
    .hint {
      font-size: 12px;
      color: var(--muted);
      margin-top: 8px;
    }
  `;

  async connectedCallback() {
    super.connectedCallback();
    console.log('[Settings] connectedCallback called');
    await this.loadConfig();
    console.log('[Settings] loadConfig done, loading:', this.loading);
  }

  async loadConfig() {
    try {
      // 加载 settings
      const settingsRes = await fetch('/api/config/settings');
      if (settingsRes.ok) {
        const settingsData = await settingsRes.json();
        const settings = settingsData.data || {};
        this.appName = settings.app_name || '';
        this.country = settings.country || '马来西亚';
        this.language = settings.language || '马来语';
      }
      
      // 加载 api_keys
      const keysRes = await fetch('/api/config/api_keys');
      if (keysRes.ok) {
        const keysData = await keysRes.json();
        const keys = keysData.data || {};
        this.apiKeys = {
          google: keys.google || '',
          volcano: keys.volcano || '',
          xai: keys.xai || ''
        };
      }
    } catch (e) {
      console.error('加载配置失败:', e);
    }
    this.loading = false;
    this.requestUpdate();
  }

  private _editField(field: string, value: string) {
    this.editingField = field;
    this.editValue = value;
  }

  private _cancelEdit() {
    this.editingField = '';
    this.editValue = '';
  }

  private async _saveField(field: string) {
    this.saving = true;
    
    try {
      if (field === 'app_name' || field === 'country' || field === 'language') {
        // 保存到 settings.json
        const res = await fetch('/api/config/settings', {
          method: 'PUT',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            app_name: this.appName,
            country: this.country,
            language: this.language,
            [field]: this.editValue
          })
        });
        
        if (res.ok) {
          if (field === 'app_name') this.appName = this.editValue;
          if (field === 'country') this.country = this.editValue;
          if (field === 'language') this.language = this.editValue;
        }
      } else {
        // 保存到 api_keys.json
        const res = await fetch('/api/config/api_keys', {
          method: 'PUT',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            ...this.apiKeys,
            [field]: this.editValue
          })
        });
        
        if (res.ok) {
          this.apiKeys = { ...this.apiKeys, [field]: this.editValue };
        }
      }
    } catch (e) {
      console.error('保存失败:', e);
      alert('保存失败');
    }
    
    this.saving = false;
    this.editingField = '';
    this.editValue = '';
  }

  private _maskKey(key: string): string {
    if (!key || key.length < 10) return key || '未配置';
    return key.substring(0, 6) + '****' + key.substring(key.length - 4);
  }

  render() {
    console.log('[Settings] render, loading:', this.loading, 'appName:', this.appName);
    
    if (this.loading) {
      return html`<div style="text-align:center;padding:40px;color:var(--muted)">加载中...</div>`;
    }

    return html`
      <h2>⚙️ 系统设置</h2>
      
      <!-- 基础设置 -->
      <div class="section">
        <div class="section-header">
          <span class="section-icon">📱</span>
          <span class="section-title">基础设置</span>
        </div>
        <div class="section-body">
          <div class="field-row">
            <span class="field-label">软件名称</span>
            <div class="field-value">
              ${this.editingField === 'app_name' 
                ? html`
                    <input class="field-input" .value=${this.editValue} @input=${(e: Event) => this.editValue = (e.target as HTMLInputElement).value} />
                    <button class="btn btn-primary" @click=${() => this._saveField('app_name')} ?disabled=${this.saving}>保存</button>
                    <button class="btn" @click=${this._cancelEdit}>取消</button>
                  `
                : html`
                    <span class="field-text">${this.appName || '未设置'}</span>
                    <button class="btn" @click=${() => this._editField('app_name', this.appName)}>编辑</button>
                  `
              }
            </div>
          </div>
          
          <div class="field-row">
            <span class="field-label">国家/地区</span>
            <div class="field-value">
              ${this.editingField === 'country' 
                ? html`
                    <input class="field-input" .value=${this.editValue} @input=${(e: Event) => this.editValue = (e.target as HTMLInputElement).value} placeholder="如：马来西亚、印尼、泰国..." />
                    <button class="btn btn-primary" @click=${() => this._saveField('country')} ?disabled=${this.saving}>保存</button>
                    <button class="btn" @click=${this._cancelEdit}>取消</button>
                  `
                : html`
                    <span class="field-text">${this.country || '未设置'}</span>
                    <button class="btn" @click=${() => this._editField('country', this.country)}>编辑</button>
                  `
              }
            </div>
          </div>
          
          <div class="field-row">
            <span class="field-label">语言</span>
            <div class="field-value">
              ${this.editingField === 'language' 
                ? html`
                    <input class="field-input" .value=${this.editValue} @input=${(e: Event) => this.editValue = (e.target as HTMLInputElement).value} placeholder="如：马来语、印尼语、泰语..." />
                    <button class="btn btn-primary" @click=${() => this._saveField('language')} ?disabled=${this.saving}>保存</button>
                    <button class="btn" @click=${this._cancelEdit}>取消</button>
                  `
                : html`
                    <span class="field-text">${this.language || '未设置'}</span>
                    <button class="btn" @click=${() => this._editField('language', this.language)}>编辑</button>
                  `
              }
            </div>
          </div>
        </div>
        <div class="hint" style="padding: 0 20px 16px;">
          💡 国家和语言配置用于生成素材时的文案语言选择
        </div>
      </div>
      
      <!-- API 密钥 -->
      <div class="section">
        <div class="section-header">
          <span class="section-icon">🔑</span>
          <span class="section-title">API 密钥</span>
        </div>
        <div class="section-body">
          <div class="field-row">
            <span class="field-label">Google API Key</span>
            <div class="field-value">
              ${this.editingField === 'google' 
                ? html`
                    <input class="field-input" type="password" .value=${this.editValue} @input=${(e: Event) => this.editValue = (e.target as HTMLInputElement).value} />
                    <button class="btn btn-primary" @click=${() => this._saveField('google')} ?disabled=${this.saving}>保存</button>
                    <button class="btn" @click=${this._cancelEdit}>取消</button>
                  `
                : html`
                    <span class="field-text api-key-masked">${this._maskKey(this.apiKeys.google)}</span>
                    <button class="btn" @click=${() => this._editField('google', this.apiKeys.google)}>编辑</button>
                  `
              }
            </div>
          </div>
          
          <div class="field-row">
            <span class="field-label">火山引擎 API Key</span>
            <div class="field-value">
              ${this.editingField === 'volcano' 
                ? html`
                    <input class="field-input" type="password" .value=${this.editValue} @input=${(e: Event) => this.editValue = (e.target as HTMLInputElement).value} />
                    <button class="btn btn-primary" @click=${() => this._saveField('volcano')} ?disabled=${this.saving}>保存</button>
                    <button class="btn" @click=${this._cancelEdit}>取消</button>
                  `
                : html`
                    <span class="field-text api-key-masked">${this._maskKey(this.apiKeys.volcano)}</span>
                    <button class="btn" @click=${() => this._editField('volcano', this.apiKeys.volcano)}>编辑</button>
                  `
              }
            </div>
          </div>
          
          <div class="field-row">
            <span class="field-label">xAI API Key</span>
            <div class="field-value">
              ${this.editingField === 'xai' 
                ? html`
                    <input class="field-input" type="password" .value=${this.editValue} @input=${(e: Event) => this.editValue = (e.target as HTMLInputElement).value} />
                    <button class="btn btn-primary" @click=${() => this._saveField('xai')} ?disabled=${this.saving}>保存</button>
                    <button class="btn" @click=${this._cancelEdit}>取消</button>
                  `
                : html`
                    <span class="field-text api-key-masked">${this._maskKey(this.apiKeys.xai)}</span>
                    <button class="btn" @click=${() => this._editField('xai', this.apiKeys.xai)}>编辑</button>
                  `
              }
            </div>
          </div>
        </div>
        <div class="hint" style="padding: 0 20px 16px;">
          💡 API 密钥用于调用各类 AI 模型生成素材
        </div>
      </div>
    `;
  }
}

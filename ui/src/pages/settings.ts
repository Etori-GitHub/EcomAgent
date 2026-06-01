import { LitElement, html, css } from 'lit';
import { customElement, state } from 'lit/decorators.js';
import type { BackupFile } from '../types';
import * as api from '../services/api';

interface ConfigData {
  name: string;
  filename: string;
  data: Record<string, unknown>;
  modified: string;
}

// 配置字段的友好名称映射
const FIELD_LABELS: Record<string, string> = {
  // settings
  'app_name': '软件名称',
  
  // api_keys
  'google': 'Google API Key',
  'volcano': '火山引擎 API Key',
  'xai': 'xAI API Key',
  
  // models - image_providers
  'image_providers': '图片生成模型',
  'default': '默认模型',
  'available': '可用模型',
  'flash_image': 'Flash Image',
  'model': '模型名称',
  'aspect_ratios': '支持比例',
  'resolutions': '支持分辨率',
  
  // models - video_providers
  'video_providers': '视频生成模型',
  'grok': 'Grok',
  'max_duration': '最大时长(秒)',
  
  // models - gemini
  'gemini': 'Gemini 配置',
  'temperature': '温度参数',
  'max_output_tokens': '最大输出Token',
  
  // triggers
  'triggers': '触发器列表',
  'image': '生成图片',
  'video': '生成视频',
  'amazon': '亚马逊抓取',
  'tiktok': 'TikTok抓取',
  'test': '测试模式',
  'name': '名称',
  'script': '脚本路径',
  'keywords': '触发关键词',
  'description': '描述',
  
  // settings
  'settings': '设置',
  'cache_expire_minutes': '缓存过期时间(分钟)',
  'case_sensitive': '区分大小写',
};

// 配置卡片的标题和描述
const CONFIG_INFO: Record<string, { title: string; desc: string; icon: string }> = {
  'settings': {
    title: '系统设置',
    desc: '应用名称等基础配置',
    icon: '⚙️',
  },
  'api_keys': {
    title: 'API 密钥',
    desc: '各平台 API 访问密钥',
    icon: '🔑',
  },
  'models': {
    title: '模型配置',
    desc: '图片、视频生成模型参数',
    icon: '🤖',
  },
  'triggers': {
    title: '触发器',
    desc: '命令关键词触发配置',
    icon: '⚡',
  },
};

@customElement('ea-settings')
export class EaSettings extends LitElement {
  static styles = css`
    :host { display: block; }
    
    h2 {
      font-size: 20px;
      font-weight: 700;
      color: var(--text-strong);
      margin-bottom: 24px;
    }
    
    .actions {
      display: flex;
      gap: 12px;
      margin-bottom: 24px;
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
    
    .btn-primary {
      background: var(--accent);
      color: var(--accent-foreground);
    }
    
    .btn-primary:hover { background: var(--accent-hover); }
    .btn-primary:disabled { opacity: 0.5; cursor: not-allowed; }
    
    .btn-secondary {
      background: var(--bg-elevated);
      color: var(--text);
      border: 1px solid var(--border);
    }
    
    .btn-secondary:hover { background: var(--bg-hover); }
    
    .config-card {
      background: var(--card);
      border-radius: var(--radius-lg);
      border: 1px solid var(--border);
      margin-bottom: 20px;
      overflow: hidden;
    }
    
    .config-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      padding: 16px 20px;
      background: linear-gradient(135deg, var(--bg-accent) 0%, var(--card) 100%);
      border-bottom: 1px solid var(--border);
    }
    
    .config-title-group {
      display: flex;
      align-items: center;
      gap: 12px;
    }
    
    .config-icon {
      width: 40px;
      height: 40px;
      border-radius: 10px;
      background: var(--accent-subtle);
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 20px;
    }
    
    .config-title-text h3 {
      margin: 0;
      font-size: 16px;
      font-weight: 600;
      color: var(--text-strong);
    }
    
    .config-title-text p {
      margin: 2px 0 0;
      font-size: 12px;
      color: var(--muted);
    }
    
    .config-actions {
      display: flex;
      gap: 8px;
    }
    
    .config-body {
      padding: 20px;
    }
    
    /* 简单字段列表 */
    .field-list {
      display: flex;
      flex-direction: column;
      gap: 16px;
    }
    
    .field-item {
      display: grid;
      grid-template-columns: 160px 1fr;
      gap: 16px;
      align-items: center;
    }
    
    .field-label {
      font-size: 13px;
      font-weight: 500;
      color: var(--text);
    }
    
    .field-input {
      min-width: 0; /* 防止溢出 */
    }
    
    .input {
      width: 100%;
      padding: 10px 14px;
      border: 1px solid var(--border);
      border-radius: var(--radius-sm);
      font-size: 13px;
      background: var(--bg-elevated);
      color: var(--text);
      transition: var(--duration-fast) ease;
    }
    
    .input:focus {
      outline: none;
      border-color: var(--accent);
      box-shadow: 0 0 0 3px var(--accent-subtle);
    }
    
    .input.mono {
      font-family: var(--mono);
      font-size: 12px;
    }
    
    .checkbox {
      width: 20px;
      height: 20px;
      cursor: pointer;
      accent-color: var(--accent);
    }
    
    /* 分组区域 */
    .section {
      background: var(--bg-elevated);
      border-radius: var(--radius-md);
      padding: 16px;
      margin-bottom: 16px;
    }
    
    .section:last-child { margin-bottom: 0; }
    
    .section-title {
      font-size: 14px;
      font-weight: 600;
      color: var(--text-strong);
      margin-bottom: 12px;
      padding-bottom: 8px;
      border-bottom: 1px solid var(--border);
    }
    
    .section-field {
      display: grid;
      grid-template-columns: 160px 1fr;
      gap: 16px;
      align-items: center;
    }
    
    .section-field-label {
      font-size: 13px;
      font-weight: 500;
      color: var(--text);
    }
    
    .section-field-input {
      min-width: 0;
    }
    
    .section-grid {
      display: flex;
      flex-direction: column;
      gap: 16px;
    }
    
    .config-meta {
      font-size: 11px;
      color: var(--muted);
      padding: 12px 20px;
      border-top: 1px solid var(--border);
      background: var(--bg-accent);
      display: flex;
      justify-content: space-between;
    }
    
    /* Modal */
    .modal-overlay {
      position: fixed;
      top: 0;
      left: 0;
      right: 0;
      bottom: 0;
      background: rgba(0, 0, 0, 0.7);
      display: flex;
      align-items: center;
      justify-content: center;
      z-index: 1000;
    }
    
    .modal {
      background: var(--card);
      border-radius: var(--radius-lg);
      width: 600px;
      max-height: 80vh;
      overflow: hidden;
      display: flex;
      flex-direction: column;
    }
    
    .modal-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      padding: 16px 20px;
      border-bottom: 1px solid var(--border);
    }
    
    .modal-title {
      font-size: 16px;
      font-weight: 600;
      color: var(--text-strong);
    }
    
    .modal-close {
      background: none;
      border: none;
      color: var(--muted);
      cursor: pointer;
      font-size: 20px;
    }
    
    .modal-body {
      padding: 16px;
      overflow-y: auto;
      flex: 1;
    }
    
    .backup-item {
      background: var(--bg-elevated);
      border-radius: var(--radius-md);
      padding: 12px;
      margin-bottom: 8px;
      display: flex;
      justify-content: space-between;
      align-items: center;
    }
    
    .backup-info { font-size: 13px; }
    
    .backup-name {
      font-weight: 500;
      color: var(--text-strong);
    }
    
    .backup-meta {
      font-size: 11px;
      color: var(--muted);
    }
    
    .backup-actions {
      display: flex;
      gap: 8px;
    }
    
    .action-btn {
      padding: 6px 12px;
      border-radius: var(--radius-sm);
      font-size: 12px;
      cursor: pointer;
      border: none;
      transition: var(--duration-fast) ease;
    }
    
    .action-btn.restore {
      background: var(--ok-subtle);
      color: var(--ok);
    }
    
    .action-btn.restore:hover { background: var(--ok); color: white; }
    
    .action-btn.delete {
      background: var(--danger-subtle);
      color: var(--danger);
    }
    
    .action-btn.delete:hover { background: var(--danger); color: white; }
    
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

  @state() private configs: ConfigData[] = [];
  @state() private backups: BackupFile[] = [];
  @state() private showBackups = false;
  @state() private loading = true;
  @state() private saving: string | null = null;

  connectedCallback() {
    super.connectedCallback();
    this.loadConfigs();
  }

  async loadConfigs() {
    this.loading = true;
    try {
      const configRes = await api.getConfigs();
      const backupRes = await api.getBackups();
      
      const configData: ConfigData[] = [];
      for (const cfg of configRes.configs) {
        if (cfg.name.includes('template')) continue;
        try {
          const detail = await api.getConfig(cfg.name);
          configData.push({
            name: cfg.name,
            filename: cfg.filename,
            data: detail.data,
            modified: detail.modified,
          });
        } catch (e) {
          console.error('Load config error:', cfg.name, e);
        }
      }
      
      this.configs = configData;
      this.backups = backupRes.backups;
    } catch (e) {
      console.error('Failed to load configs:', e);
    } finally {
      this.loading = false;
      this.requestUpdate();
    }
  }

  private _getLabel(key: string): string {
    return FIELD_LABELS[key] || key;
  }

  private _getConfigInfo(name: string): { title: string; desc: string; icon: string } {
    return CONFIG_INFO[name] || { title: name, desc: '', icon: '📄' };
  }

  private _onFieldChange(configName: string, key: string, value: unknown) {
    const config = this.configs.find(c => c.name === configName);
    if (config) {
      const keys = key.split('.');
      let obj: Record<string, unknown> = config.data;
      for (let i = 0; i < keys.length - 1; i++) {
        obj = obj[keys[i]] as Record<string, unknown>;
      }
      obj[keys[keys.length - 1]] = value;
      this.requestUpdate();
    }
  }

  private async _saveConfig(configName: string) {
    const config = this.configs.find(c => c.name === configName);
    if (!config) return;

    this.saving = configName;
    try {
      const content = JSON.stringify(config.data, null, 2);
      const result = await api.updateConfig(configName, content);
      alert('✅ 配置已保存\n备份文件: ' + result.backup);
      this.loadConfigs();
    } catch (e) {
      alert('保存失败: ' + (e instanceof Error ? e.message : String(e)));
    } finally {
      this.saving = null;
    }
  }

  private async _restoreBackup(filename: string) {
    if (!confirm(`确定要还原备份 ${filename} 吗？`)) return;
    try {
      const result = await api.restoreBackup(filename);
      alert(`✅ 已还原备份\n原配置已备份为: ${result.pre_restore_backup}`);
      this.showBackups = false;
      this.loadConfigs();
    } catch (e) {
      alert('还原失败: ' + (e instanceof Error ? e.message : String(e)));
    }
  }

  private async _deleteBackup(filename: string) {
    if (!confirm(`确定要删除备份 ${filename} 吗？`)) return;
    try {
      await api.deleteBackup(filename);
      const backupRes = await api.getBackups();
      this.backups = backupRes.backups;
    } catch (e) {
      alert('删除失败: ' + (e instanceof Error ? e.message : String(e)));
    }
  }

  // 渲染简单字段（api_keys）
  private _renderSimpleFields(config: ConfigData) {
    return html`
      <div class="field-list">
        ${Object.entries(config.data).map(([key, value]) => html`
          <div class="field-item">
            <div class="field-label">${this._getLabel(key)}</div>
            <div class="field-input">
              <input 
                type="text" 
                class="input mono"
                .value=${String(value)}
                @change=${(e: Event) => this._onFieldChange(config.name, key, (e.target as HTMLInputElement).value)}
              >
            </div>
          </div>
        `)}
      </div>
    `;
  }

  // 渲染分组字段（models, triggers）
  private _renderSectionFields(config: ConfigData) {
    return Object.entries(config.data).map(([sectionKey, sectionValue]) => {
      if (typeof sectionValue !== 'object' || sectionValue === null) {
        // 简单字段
        return html`
          <div class="field-item">
            <div class="field-label">${this._getLabel(sectionKey)}</div>
            <div class="field-input">
              <input 
                type="text" 
                class="input"
                .value=${String(sectionValue)}
                @change=${(e: Event) => this._onFieldChange(config.name, sectionKey, (e.target as HTMLInputElement).value)}
              >
            </div>
          </div>
        `;
      }

      // 分组区域
      return html`
        <div class="section">
          <div class="section-title">${this._getLabel(sectionKey)}</div>
          <div class="section-grid">
            ${this._renderSectionFieldsRecursive(config.name, sectionKey, sectionValue as Record<string, unknown>)}
          </div>
        </div>
      `;
    });
  }

  private _renderSectionFieldsRecursive(configName: string, prefix: string, data: Record<string, unknown>): unknown {
    return Object.entries(data).map(([key, value]) => {
      const fullKey = `${prefix}.${key}`;
      
      if (typeof value === 'object' && value !== null && !Array.isArray(value)) {
        // 嵌套对象，递归
        return html`
          <div class="section">
            <div class="section-title">${this._getLabel(key)}</div>
            ${this._renderSectionFieldsRecursive(configName, fullKey, value as Record<string, unknown>)}
          </div>
        `;
      }

      // 简单字段 - 和第一个卡片一样的样式
      return html`
        <div class="field-item">
          <div class="field-label">${this._getLabel(key)}</div>
          <div class="field-input">
            ${this._renderInput(configName, fullKey, value)}
          </div>
        </div>
      `;
    });
  }

  private _renderInput(configName: string, fullKey: string, value: unknown): unknown {
    if (typeof value === 'boolean') {
      return html`
        <input 
          type="checkbox" 
          class="checkbox"
          .checked=${value}
          @change=${(e: Event) => this._onFieldChange(configName, fullKey, (e.target as HTMLInputElement).checked)}
        >
      `;
    }

    if (Array.isArray(value)) {
      return html`
        <input 
          type="text" 
          class="input mono"
          .value=${JSON.stringify(value)}
          @change=${(e: Event) => {
            try {
              const arr = JSON.parse((e.target as HTMLInputElement).value);
              this._onFieldChange(configName, fullKey, arr);
            } catch { /* ignore */ }
          }}
        >
      `;
    }

    return html`
      <input 
        type="text" 
        class="input"
        .value=${String(value ?? '')}
        @change=${(e: Event) => this._onFieldChange(configName, fullKey, (e.target as HTMLInputElement).value)}
      >
    `;
  }

  private _renderConfigCard(config: ConfigData) {
    const info = this._getConfigInfo(config.name);
    const isSaving = this.saving === config.name;
    const isSimple = config.name === 'api_keys' || config.name === 'settings';

    return html`
      <div class="config-card">
        <div class="config-header">
          <div class="config-title-group">
            <div class="config-icon">${info.icon}</div>
            <div class="config-title-text">
              <h3>${info.title}</h3>
              <p>${info.desc}</p>
            </div>
          </div>
          <div class="config-actions">
            <button 
              class="btn btn-primary" 
              ?disabled=${isSaving}
              @click=${() => this._saveConfig(config.name)}
            >${isSaving ? '保存中...' : '保存'}</button>
          </div>
        </div>
        
        <div class="config-body">
          ${isSimple 
            ? this._renderSimpleFields(config)
            : this._renderSectionFields(config)
          }
        </div>
        
        <div class="config-meta">
          <span>文件: ${config.filename}</span>
          <span>修改时间: ${config.modified ? new Date(config.modified).toLocaleString('zh-CN') : '-'}</span>
        </div>
      </div>
    `;
  }

  render() {
    return html`
      <h2>系统设置</h2>

      <div class="actions">
        <button class="btn btn-secondary" @click=${() => this.loadConfigs()}>刷新配置</button>
        <button class="btn btn-secondary" @click=${() => this.showBackups = true}>查看备份</button>
      </div>

      ${this.loading 
        ? html`<div class="loading"><div class="spinner"></div><p>加载中...</p></div>`
        : this.configs.map(cfg => this._renderConfigCard(cfg))
      }

      ${this.showBackups ? html`
        <div class="modal-overlay" @click=${() => this.showBackups = false}>
          <div class="modal" @click=${(e: Event) => e.stopPropagation()}>
            <div class="modal-header">
              <span class="modal-title">备份管理</span>
              <button class="modal-close" @click=${() => this.showBackups = false}>✕</button>
            </div>
            <div class="modal-body">
              ${this.backups.length === 0 
                ? html`<div style="text-align:center;padding:24px;color:var(--muted)">暂无备份文件</div>`
                : this.backups.map(backup => html`
                  <div class="backup-item">
                    <div class="backup-info">
                      <div class="backup-name">${backup.filename}</div>
                      <div class="backup-meta">
                        ${backup.config_name} | ${new Date(backup.created).toLocaleString('zh-CN')} | ${backup.size} bytes
                      </div>
                    </div>
                    <div class="backup-actions">
                      <button class="action-btn restore" @click=${() => this._restoreBackup(backup.filename)}>还原</button>
                      <button class="action-btn delete" @click=${() => this._deleteBackup(backup.filename)}>删除</button>
                    </div>
                  </div>
                `)
              }
            </div>
          </div>
        </div>
      ` : ''}
    `;
  }
}
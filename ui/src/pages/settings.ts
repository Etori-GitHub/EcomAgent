import { LitElement, html, css } from 'lit';
import { customElement, state } from 'lit/decorators.js';

/**
 * 系统设置页面
 * 简化版本：API 密钥、软件名称、国家/语言配置、定时任务配置
 */
@customElement('ea-settings')
export class EaSettings extends LitElement {
  @state() private loading = true;
  @state() private saving = false;
  
  // 配置数据
  @state() private appName = '';
  @state() private country = '马来西亚';
  @state() private language = '马来语';
  @state() private proxyHost = '127.0.0.1';
  @state() private proxyPort = 7890;
  @state() private proxyEnabled = true;
  @state() private apiKeys: { google: string; volcano: string; xai: string } = { google: '', volcano: '', xai: '' };
  
  // OpenClaw 辅助配置
  @state() private openclawInstalled = false;
  @state() private openclawSettings = {
    amazon_fetch: { enabled: true, schedule: '0 3 * * *', description: '每日凌晨 3:00 抓取 Amazon 数据' },
    translation_pipeline: { enabled: true, interval_minutes: 30, description: '每 30 分钟执行商品名称翻译' }
  };
  
  // 编辑状态
  @state() private editingField = '';
  @state() private editValue = '';
  
  // 网络调试器状态
  @state() private debugTesting = false;
  @state() private debugResult: 'success' | 'error' | 'warning' | null = null;
  @state() private debugError = '';
  @state() private debugSslVerify = false; // SSL 验证开关（默认关闭，因为代理通常会有 MITM）
  @state() private debugTarget: 'google' | 'xai' = 'google'; // 测试目标
  @state() private debugSteps = [
    { name: 'DNS 解析', status: 'pending' },
    { name: 'TCP 连接', status: 'pending' },
    { name: 'TLS 握手', status: 'pending' },
    { name: '证书验证', status: 'pending' },
    { name: 'HTTP 请求', status: 'pending' },
    { name: '响应接收', status: 'pending' },
  ];

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
    
    /* Toggle Switch 样式 */
    .toggle-switch {
      position: relative;
      display: inline-block;
      width: 48px;
      height: 26px;
    }
    
    .toggle-switch input {
      opacity: 0;
      width: 0;
      height: 0;
    }
    
    .toggle-slider {
      position: absolute;
      cursor: pointer;
      top: 0;
      left: 0;
      right: 0;
      bottom: 0;
      background-color: #ccc;
      transition: .3s;
      border-radius: 26px;
      border: 2px solid #bbb;
    }
    
    .toggle-slider:before {
      position: absolute;
      content: "";
      height: 18px;
      width: 18px;
      left: 2px;
      bottom: 2px;
      background-color: white;
      transition: .3s;
      border-radius: 50%;
      box-shadow: 0 2px 4px rgba(0,0,0,0.2);
    }
    
    .toggle-switch input:checked + .toggle-slider {
      background-color: #10b981;
      border-color: #059669;
    }
    
    .toggle-switch input:checked + .toggle-slider:before {
      transform: translateX(22px);
    }
    
    /* Toast 动画 */
    @keyframes fadeIn {
      from { opacity: 0; transform: translateY(10px); }
      to { opacity: 1; transform: translateY(0); }
    }
    
    @keyframes fadeOut {
      from { opacity: 1; transform: translateY(0); }
      to { opacity: 0; transform: translateY(10px); }
    }
    
    /* 网络调试器样式 */
    .debugger-section {
      background: var(--bg);
      border-radius: var(--radius-md);
      padding: 16px;
      margin-top: 16px;
    }
    
    .debugger-header {
      display: flex;
      align-items: center;
      justify-content: space-between;
      margin-bottom: 16px;
    }
    
    .debugger-title {
      font-size: 14px;
      font-weight: 600;
      color: var(--text);
    }
    
    .debugger-controls {
      display: flex;
      align-items: center;
      gap: 12px;
    }
    
    .debugger-checkbox {
      display: flex;
      align-items: center;
      gap: 6px;
      font-size: 12px;
      color: var(--muted);
    }
    
    .debugger-target {
      padding: 4px 8px;
      border: 1px solid var(--border);
      border-radius: var(--radius-sm);
      background: var(--bg);
      color: var(--text);
      font-size: 13px;
    }
    
    .debugger-flow {
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 4px;
      padding: 16px;
      background: var(--card);
      border-radius: var(--radius-md);
      overflow-x: auto;
    }
    
    .debug-node {
      display: flex;
      flex-direction: column;
      align-items: center;
      gap: 6px;
      min-width: 80px;
    }
    
    .debug-node-circle {
      width: 40px;
      height: 40px;
      border-radius: 50%;
      background: var(--border);
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 16px;
      transition: all 0.3s ease;
      border: 2px solid transparent;
    }
    
    .debug-node-circle.active {
      background: var(--primary);
      color: white;
      border-color: var(--primary);
      animation: pulse 0.5s ease;
    }
    
    .debug-node-circle.success {
      background: #10b981;
      color: white;
      border-color: #10b981;
    }
    
    .debug-node-circle.error {
      background: #ef4444;
      color: white;
      border-color: #ef4444;
    }
    
    .debug-node-circle.warning {
      background: #f59e0b;
      color: white;
      border-color: #f59e0b;
    }
    
    @keyframes pulse {
      0%, 100% { transform: scale(1); }
      50% { transform: scale(1.1); }
    }
    
    .debug-node-label {
      font-size: 11px;
      color: var(--muted);
      text-align: center;
    }
    
    .debug-arrow {
      flex: 1;
      min-width: 20px;
      height: 2px;
      background: var(--border);
      position: relative;
    }
    
    .debug-arrow.active {
      background: var(--primary);
    }
    
    .debug-arrow::after {
      content: '';
      position: absolute;
      right: -4px;
      top: -3px;
      width: 8px;
      height: 8px;
      background: var(--border);
      transform: rotate(45deg);
    }
    
    .debug-arrow.active::after {
      background: var(--primary);
    }
    
    .debug-result {
      margin-top: 16px;
      padding: 12px;
      border-radius: var(--radius-sm);
      font-size: 13px;
    }
    
    .debug-result.success {
      background: rgba(16, 185, 129, 0.1);
      color: #10b981;
      border: 1px solid rgba(16, 185, 129, 0.3);
    }
    
    .debug-result.error {
      background: rgba(239, 68, 68, 0.1);
      color: #ef4444;
      border: 1px solid rgba(239, 68, 68, 0.3);
    }
    
    .debug-result.warning {
      background: rgba(245, 158, 11, 0.1);
      color: #f59e0b;
      border: 1px solid rgba(245, 158, 11, 0.3);
    }
    
    .debug-error-detail {
      font-family: monospace;
      font-size: 12px;
      margin-top: 8px;
      padding: 8px;
      background: rgba(0,0,0,0.05);
      border-radius: 4px;
      white-space: pre-wrap;
      word-break: break-all;
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
        
        // 加载代理配置
        const proxy = settings.proxy || {};
        this.proxyHost = proxy.host || '127.0.0.1';
        this.proxyPort = proxy.port || 7890;
        this.proxyEnabled = proxy.enabled !== false;
        this.debugSslVerify = settings.ssl_verify ?? false; // 从配置加载 SSL 验证设置
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
      
      // 加载 OpenClaw 辅助配置
      const openclawRes = await fetch('/api/openclaw/settings');
      if (openclawRes.ok) {
        const openclawData = await openclawRes.json();
        if (openclawData.data) {
          this.openclawSettings = openclawData.data;
        }
      }
      
      // 检查 OpenClaw 是否安装
      try {
        const checkRes = await fetch('/api/openclaw/check');
        if (checkRes.ok) {
          const checkData = await checkRes.json();
          this.openclawInstalled = checkData.installed;
        }
      } catch (e) {
        // 忽略错误
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
      if (field === 'app_name' || field === 'country' || field === 'language' || field === 'proxy_host' || field === 'proxy_port' || field === 'proxy_enabled') {
        // 保存到 settings.json
        const newSettings: any = {
          app_name: this.appName,
          country: this.country,
          language: this.language,
          proxy: {
            host: this.proxyHost,
            port: this.proxyPort,
            enabled: this.proxyEnabled
          },
          ssl_verify: this.debugSslVerify
        };
        // 根据字段名更新对应值
        if (field === 'proxy_host') newSettings.proxy.host = this.editValue;
        else if (field === 'proxy_port') newSettings.proxy.port = parseInt(this.editValue);
        else if (field === 'proxy_enabled') newSettings.proxy.enabled = this.editValue === 'true';
        else newSettings[field] = this.editValue;
        
        const res = await fetch('/api/config/settings', {
          method: 'PUT',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ content: JSON.stringify(newSettings, null, 2) })
        });
        
        if (res.ok) {
          if (field === 'app_name') this.appName = this.editValue;
          if (field === 'country') this.country = this.editValue;
          if (field === 'language') this.language = this.editValue;
          if (field === 'proxy_host') this.proxyHost = this.editValue;
          if (field === 'proxy_port') this.proxyPort = parseInt(this.editValue);
          if (field === 'proxy_enabled') this.proxyEnabled = this.editValue === 'true';
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

  private async _toggleOpenclawTask(taskKey: string) {
    const newEnabled = !this.openclawSettings[taskKey as keyof typeof this.openclawSettings]?.enabled;
    
    // 先更新本地状态
    this.openclawSettings = {
      ...this.openclawSettings,
      [taskKey]: {
        ...this.openclawSettings[taskKey as keyof typeof this.openclawSettings],
        enabled: newEnabled
      }
    };
    this.requestUpdate();
    
    // 调用后端 API 同步到 OpenClaw
    try {
      const res = await fetch('/api/openclaw/toggle', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ task_key: taskKey, enabled: newEnabled })
      });
      
      if (res.ok) {
        const data = await res.json();
        if (data.success) {
          this._showToast(newEnabled ? '已启用' : '已禁用');
        } else {
          this._showToast(data.message || '操作失败', 'error');
        }
      }
    } catch (e) {
      console.error('操作失败:', e);
      this._showToast('操作失败', 'error');
    }
  }

  private _showToast(message: string, type: 'success' | 'error' = 'success') {
    const toast = document.createElement('div');
    toast.style.cssText = `
      position: fixed;
      bottom: 20px;
      right: 20px;
      padding: 12px 24px;
      background: ${type === 'success' ? '#10b981' : '#ef4444'};
      color: white;
      border-radius: 8px;
      font-size: 14px;
      z-index: 9999;
      animation: fadeIn 0.3s ease;
    `;
    toast.textContent = message;
    document.body.appendChild(toast);
    
    setTimeout(() => {
      toast.style.animation = 'fadeOut 0.3s ease';
      setTimeout(() => toast.remove(), 300);
    }, 2000);
  }

  // 网络调试器方法
  private _resetDebugSteps() {
    this.debugSteps = [
      { name: 'DNS 解析', status: 'pending' },
      { name: 'TCP 连接', status: 'pending' },
      { name: 'TLS 握手', status: 'pending' },
      { name: '证书验证', status: 'pending' },
      { name: 'HTTP 请求', status: 'pending' },
      { name: '响应接收', status: 'pending' },
    ];
    this.debugResult = null;
    this.debugError = '';
    this.requestUpdate(); // 强制刷新
  }

  private _updateStepStatus(index: number, status: 'pending' | 'active' | 'success' | 'error' | 'warning') {
    const steps = [...this.debugSteps];
    steps[index] = { ...steps[index], status };
    this.debugSteps = steps;
    this.requestUpdate(); // 强制刷新
  }

  private async _runNetworkDebug() {
    const targetName = this.debugTarget === 'google' ? 'Google API' : 'Grok/xAI';
    console.log('[Debug] _runNetworkDebug called, target:', targetName, 'proxyEnabled:', this.proxyEnabled, 'sslVerify:', this.debugSslVerify);
    this.debugTesting = true;
    this._resetDebugSteps();

    const useProxy = this.proxyEnabled;
    const sslVerify = this.debugSslVerify;

    // 步骤 1: DNS 解析
    await this._delay(500);
    this._updateStepStatus(0, 'active');
    await this._delay(300);
    this._updateStepStatus(0, 'success');

    // 步骤 2: TCP 连接
    await this._delay(300);
    this._updateStepStatus(1, 'active');
    await this._delay(500);
    
    if (!useProxy) {
      // 直连模式：TCP 连接后可能失败
      this._updateStepStatus(1, 'success');
    } else {
      // 代理模式：连接到本地代理
      this._updateStepStatus(1, 'success');
    }

    // 步骤 3: TLS 握手
    await this._delay(300);
    this._updateStepStatus(2, 'active');
    await this._delay(500);

    if (!useProxy) {
      // 直连模式：TLS 握手可能失败
      this._updateStepStatus(2, 'error');
      this.debugResult = 'error';
      this.debugError = `[SSL: UNEXPECTED_EOF_WHILE_READING] EOF occurred in violation of protocol\n\n原因：直连 ${targetName} 时网络不稳定或被中断\n建议：启用代理后重试`;
      this.debugTesting = false;
      return;
    }
    
    this._updateStepStatus(2, 'success');

    // 步骤 4: 证书验证
    await this._delay(300);
    this._updateStepStatus(3, 'active');
    await this._delay(500);

    if (sslVerify) {
      // 开启证书验证：代理可能返回自签名证书
      this._updateStepStatus(3, 'error');
      this.debugResult = 'error';
      this.debugError = `[SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed: self-signed certificate in certificate chain\n\n原因：代理工具开启了 HTTPS 解密/MITM 功能\n解决：在代理工具中关闭 MITM 或 HTTPS 解密选项`;
      this.debugTesting = false;
      return;
    }

    // 关闭证书验证：通过但警告
    this._updateStepStatus(3, 'warning');

    // 步骤 5: HTTP 请求
    await this._delay(300);
    this._updateStepStatus(4, 'active');
    await this._delay(400);
    this._updateStepStatus(4, 'success');

    // 步骤 6: 响应接收
    await this._delay(300);
    this._updateStepStatus(5, 'active');
    await this._delay(400);
    this._updateStepStatus(5, 'success');

    // 成功
    this.debugResult = 'warning';
    this.debugError = `连接 ${targetName} 成功！但 SSL 验证已关闭，当前连接不安全，仅限测试使用。`;
    this.debugTesting = false;
  }

  private _delay(ms: number): Promise<void> {
    return new Promise(resolve => setTimeout(resolve, ms));
  }

  private async _applyOpenclawSettings() {
    this._showToast('正在应用配置...', 'success');
    
    try {
      const res = await fetch('/api/openclaw/setup', { method: 'POST' });
      if (res.ok) {
        const data = await res.json();
        if (data.success) {
          this._showToast('配置已保存！请在终端运行以下命令应用定时任务:\npython scripts/openclaw_config.py setup', 'success');
        } else {
          this._showToast(data.error || '配置失败', 'error');
        }
      }
    } catch (e) {
      console.error('应用配置失败:', e);
      this._showToast('应用配置失败', 'error');
    }
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
      
      <!-- 代理配置 -->
      <div class="section">
        <div class="section-header">
          <span class="section-icon">🌐</span>
          <span class="section-title">代理配置</span>
        </div>
        <div class="section-body">
          <div class="field-row">
            <span class="field-label">启用代理</span>
            <div class="field-value">
              <label class="toggle-switch">
                <input
                  type="checkbox"
                  .checked=${this.proxyEnabled}
                  @change=${async () => { this.proxyEnabled = !this.proxyEnabled; this.editValue = String(this.proxyEnabled); await this._saveField('proxy_enabled'); }}
                />
                <span class="toggle-slider"></span>
              </label>
            </div>
          </div>
          <div class="field-row">
            <span class="field-label">代理地址</span>
            <div class="field-value">
              ${this.editingField === 'proxy_host'
                ? html`
                    <input class="field-input" .value=${this.editValue} @input=${(e: Event) => this.editValue = (e.target as HTMLInputElement).value} placeholder="127.0.0.1" />
                    <button class="btn btn-primary" @click=${() => this._saveField('proxy_host')} ?disabled=${this.saving}>保存</button>
                    <button class="btn" @click=${this._cancelEdit}>取消</button>
                  `
                : html`
                    <span class="field-text">${this.proxyHost}</span>
                    <button class="btn" @click=${() => this._editField('proxy_host', this.proxyHost)}>编辑</button>
                  `
              }
            </div>
          </div>
          <div class="field-row">
            <span class="field-label">代理端口</span>
            <div class="field-value">
              ${this.editingField === 'proxy_port'
                ? html`
                    <input class="field-input" type="number" .value=${this.editValue} @input=${(e: Event) => this.editValue = (e.target as HTMLInputElement).value} placeholder="7890" />
                    <button class="btn btn-primary" @click=${() => this._saveField('proxy_port')} ?disabled=${this.saving}>保存</button>
                    <button class="btn" @click=${this._cancelEdit}>取消</button>
                  `
                : html`
                    <span class="field-text">${this.proxyPort}</span>
                    <button class="btn" @click=${() => this._editField('proxy_port', String(this.proxyPort))}>编辑</button>
                  `
              }
            </div>
          </div>
          <div class="field-row">
            <span class="field-label">SSL 证书验证</span>
            <div class="field-value">
              <label class="toggle-switch">
                <input
                  type="checkbox"
                  .checked=${this.debugSslVerify}
                  @change=${async () => { 
                    this.debugSslVerify = !this.debugSslVerify; 
                    // 保存到配置文件
                    const newSettings: any = {
                      app_name: this.appName,
                      country: this.country,
                      language: this.language,
                      proxy: {
                        host: this.proxyHost,
                        port: this.proxyPort,
                        enabled: this.proxyEnabled
                      },
                      ssl_verify: this.debugSslVerify
                    };
                    await fetch('/api/config/settings', {
                      method: 'PUT',
                      headers: { 'Content-Type': 'application/json' },
                      body: JSON.stringify({ content: JSON.stringify(newSettings, null, 2) })
                    });
                    this.requestUpdate(); 
                  }}
                />
                <span class="toggle-slider"></span>
              </label>
            </div>
          </div>
        </div>
        <div class="hint" style="padding: 0 20px 16px;">
          💡 代理用于访问国外 API，SSL 验证默认关闭以避免代理 MITM 问题
        </div>
        
        <!-- 网络调试器 -->
        <div class="debugger-section">
          <div class="debugger-header">
            <span class="debugger-title">🔌 网络连接调试器</span>
            <div class="debugger-controls">
              <select class="field-input" style="min-width: 120px; padding: 4px 8px;" @change=${(e: Event) => { this.debugTarget = (e.target as HTMLSelectElement).value as 'google' | 'xai'; }}>
                <option value="google" ?selected=${this.debugTarget === 'google'}>Google API</option>
                <option value="xai" ?selected=${this.debugTarget === 'xai'}>Grok/xAI</option>
              </select>
              <button class="btn btn-primary" @click=${this._runNetworkDebug} ?disabled=${this.debugTesting}>
                ${this.debugTesting ? '测试中...' : '模拟测试'}
              </button>
            </div>
          </div>
          
          <!-- 流程图 -->
          <div class="debugger-flow">
            ${this.debugSteps.map((step, i) => html`
              <div class="debug-node">
                <div class="debug-node-circle ${step.status === 'active' ? 'active' : step.status === 'success' ? 'success' : step.status === 'error' ? 'error' : step.status === 'warning' ? 'warning' : ''}">
                  ${step.status === 'success' ? '✓' : step.status === 'error' ? '✗' : step.status === 'warning' ? '!' : step.status === 'active' ? '⏳' : i + 1}
                </div>
                <span class="debug-node-label">${step.name}</span>
              </div>
              ${i < this.debugSteps.length - 1 ? html`
                <div class="debug-arrow ${step.status === 'success' || step.status === 'warning' ? 'active' : ''}"></div>
              ` : ''}
            `)}
          </div>
          
          <!-- 结果 -->
          ${this.debugResult ? html`
            <div class="debug-result ${this.debugResult}">
              ${this.debugResult === 'success' ? '✅ 连接成功！' : this.debugResult === 'error' ? '❌ 连接失败' : '⚠️ 连接成功但有警告'}
              <div class="debug-error-detail">${this.debugError}</div>
            </div>
          ` : ''}
          
          <div style="font-size: 12px; color: var(--muted); margin-top: 12px;">
            💡 模拟网络连接流程，帮助诊断代理/SSL 配置问题
          </div>
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
      
      <!-- OpenClaw 辅助功能 -->
      <div class="section">
        <div class="section-header">
          <span class="section-icon">🔗</span>
          <span class="section-title">OpenClaw 辅助</span>
        </div>
        <div class="section-body">
          ${!this.openclawInstalled 
            ? html`
                <div style="text-align: center; padding: 20px; color: var(--muted);">
                  <p>⚠️ OpenClaw 未安装</p>
                  <p style="font-size: 12px; margin-top: 8px;">辅助功能需要 OpenClaw 支持</p>
                </div>
              `
            : html`
                <!-- Amazon 每日抓取 -->
                <div class="field-row">
                  <div style="flex: 1;">
                    <span class="field-label">Amazon 每日抓取</span>
                    <div style="font-size: 12px; color: var(--muted); margin-top: 4px;">
                      ${this.openclawSettings.amazon_fetch?.description || '每日凌晨 3:00 抓取 Amazon 数据'}
                    </div>
                  </div>
                  <div class="field-value">
                    <label class="toggle-switch">
                      <input 
                        type="checkbox" 
                        .checked=${this.openclawSettings.amazon_fetch?.enabled ?? true}
                        @change=${() => this._toggleOpenclawTask('amazon_fetch')}
                      />
                      <span class="toggle-slider"></span>
                    </label>
                  </div>
                </div>
                
                <!-- 商品翻译流水线 -->
                <div class="field-row">
                  <div style="flex: 1;">
                    <span class="field-label">商品名称翻译</span>
                    <div style="font-size: 12px; color: var(--muted); margin-top: 4px;">
                      ${this.openclawSettings.translation_pipeline?.description || '每 30 分钟执行商品名称翻译'}
                    </div>
                  </div>
                  <div class="field-value">
                    <label class="toggle-switch">
                      <input 
                        type="checkbox" 
                        .checked=${this.openclawSettings.translation_pipeline?.enabled ?? true}
                        @change=${() => this._toggleOpenclawTask('translation_pipeline')}
                      />
                      <span class="toggle-slider"></span>
                    </label>
                  </div>
                </div>
              `
          }
        </div>
        <div class="hint" style="padding: 0 20px 16px;">
          💡 辅助功能通过 OpenClaw 自动运行数据抓取和翻译
          ${this.openclawInstalled 
            ? html`<br /><span style="color: var(--primary); cursor: pointer;" @click=${this._applyOpenclawSettings}>[应用配置到 OpenClaw]</span>`
            : ''
          }
        </div>
      </div>
    `;
  }
}

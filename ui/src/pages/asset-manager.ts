import { LitElement, html, css } from 'lit';
import { customElement, property, state } from 'lit/decorators.js';

@customElement('asset-manager')
export class AssetManager extends LitElement {
  @property({ type: String }) ecomCode = '';
  @property({ type: Object }) item: any = null;
  @state() private assets: any = { showcase: [], video: [], detail: [] };
  @state() private loading = true;
  @state() private generating = false;
  @state() private generateType = ''; // 'showcase' | 'video' | 'detail'
  @state() private showGenerateModal = false;
  @state() private taskInfo: any = null;
  @state() private pollingTask = false;

  static styles = css`
    :host {
      display: block;
    }
    
    .asset-manager {
      padding: 20px;
      max-width: 600px;
    }
    
    .asset-header {
      display: flex;
      align-items: center;
      justify-content: space-between;
      margin-bottom: 20px;
    }
    
    .asset-title {
      font-size: 18px;
      font-weight: 600;
      color: var(--text);
    }
    
    .asset-close {
      background: none;
      border: none;
      font-size: 24px;
      cursor: pointer;
      color: var(--muted);
    }
    
    .asset-section {
      margin-bottom: 24px;
    }
    
    .section-header {
      display: flex;
      align-items: center;
      justify-content: space-between;
      margin-bottom: 12px;
    }
    
    .section-title {
      font-size: 14px;
      font-weight: 500;
      color: var(--text);
    }
    
    .section-count {
      font-size: 12px;
      color: var(--muted);
    }
    
    .add-btn {
      padding: 6px 12px;
      font-size: 12px;
      border: 1px solid var(--primary);
      border-radius: var(--radius-sm);
      background: transparent;
      color: var(--primary);
      cursor: pointer;
    }
    
    .add-btn:hover {
      background: var(--primary);
      color: white;
    }
    
    .asset-group {
      background: var(--bg);
      border-radius: var(--radius-md);
      padding: 12px;
      margin-bottom: 8px;
      display: flex;
      align-items: center;
      gap: 12px;
    }
    
    .group-index {
      font-size: 12px;
      color: var(--muted);
      min-width: 50px;
    }
    
    .group-files {
      font-size: 13px;
      color: var(--text);
      flex: 1;
    }
    
    .group-actions {
      display: flex;
      gap: 8px;
    }
    
    .preview-btn, .delete-btn {
      padding: 4px 8px;
      font-size: 12px;
      border-radius: var(--radius-sm);
      cursor: pointer;
    }
    
    .preview-btn {
      background: var(--primary);
      color: white;
      border: none;
    }
    
    .delete-btn {
      background: transparent;
      border: 1px solid #f5222d;
      color: #f5222d;
    }
    
    .empty-section {
      text-align: center;
      padding: 20px;
      color: var(--muted);
      font-size: 13px;
    }
    
    /* 生成弹窗 */
    .gen-modal-overlay {
      position: fixed;
      top: 0;
      left: 0;
      right: 0;
      bottom: 0;
      background: rgba(0, 0, 0, 0.5);
      display: flex;
      align-items: center;
      justify-content: center;
      z-index: 1100;
    }
    
    .gen-modal {
      background: var(--card);
      border-radius: var(--radius-lg);
      padding: 24px;
      max-width: 400px;
      width: 90%;
    }
    
    .gen-modal-title {
      font-size: 16px;
      font-weight: 600;
      margin-bottom: 20px;
    }
    
    .gen-option {
      margin-bottom: 16px;
    }
    
    .gen-label {
      font-size: 13px;
      color: var(--text);
      margin-bottom: 8px;
    }
    
    .gen-radio-group {
      display: flex;
      gap: 16px;
    }
    
    .gen-radio {
      display: flex;
      align-items: center;
      gap: 8px;
      font-size: 13px;
    }
    
    .gen-select {
      width: 100%;
      padding: 8px 12px;
      border: 1px solid var(--border);
      border-radius: var(--radius-sm);
      font-size: 13px;
    }
    
    .gen-buttons {
      display: flex;
      justify-content: flex-end;
      gap: 12px;
      margin-top: 24px;
    }
    
    .gen-cancel, .gen-confirm {
      padding: 8px 16px;
      border-radius: var(--radius-sm);
      font-size: 13px;
      cursor: pointer;
    }
    
    .gen-cancel {
      background: var(--bg);
      border: 1px solid var(--border);
      color: var(--text);
    }
    
    .gen-confirm {
      background: var(--primary);
      border: none;
      color: white;
    }
    
    .gen-confirm:disabled {
      opacity: 0.5;
      cursor: not-allowed;
    }
    
    /* 任务进度 */
    .task-progress {
      padding: 16px;
      background: var(--bg);
      border-radius: var(--radius-md);
      margin-top: 16px;
    }
    
    .task-status {
      font-size: 13px;
      color: var(--text);
      margin-bottom: 8px;
    }
    
    .task-bar {
      height: 4px;
      background: var(--border);
      border-radius: 2px;
      overflow: hidden;
    }
    
    .task-bar-fill {
      height: 100%;
      background: var(--primary);
      transition: width 0.3s;
    }
    
    .task-message {
      font-size: 12px;
      color: var(--muted);
      margin-top: 8px;
    }
  `;

  connectedCallback() {
    super.connectedCallback();
    // 延迟加载，等待属性传递
    setTimeout(() => this.loadAssets(), 0);
  }

  // 属性变化时重新加载
  protected updated(changedProperties: Map<string, any>) {
    if (changedProperties.has('ecomCode') && this.ecomCode) {
      this.loadAssets();
    }
  }

  async loadAssets() {
    if (!this.ecomCode) {
      this.loading = false;
      this.assets = { showcase: [], video: [], detail: [] };
      this.requestUpdate();
      return;
    }
    
    this.loading = true;
    try {
      const response = await fetch(`/api/assets/${this.ecomCode}`);
      const data = await response.json();
      this.assets = data.assets || { showcase: [], video: [], detail: [] };
      console.log('[AssetManager] API response:', data);
    } catch (e) {
      console.error('[AssetManager] 加载素材失败:', e);
    }
    this.loading = false;
    this.requestUpdate();
  }

  private _close() {
    this.dispatchEvent(new CustomEvent('close', { bubbles: true, composed: true }));
  }

  private _showGenerateModal(type: string) {
    console.log('[AssetManager] _showGenerateModal:', type);
    this.generateType = type;
    this.showGenerateModal = true;
    this.taskInfo = null;
    this.requestUpdate();
  }

  private _closeGenerateModal() {
    console.log('[AssetManager] _closeGenerateModal');
    this.showGenerateModal = false;
    this.generateType = '';
    this.pollingTask = false;
    this.requestUpdate();
  }

  private async _startGenerate() {
    console.log('[AssetManager] _startGenerate called, generateType:', this.generateType);
    this.generating = true;
    this.requestUpdate();
    
    try {
      let endpoint = '/api/assets/generate/image';
      let body: any = {
        ecom_code: this.ecomCode,
        asset_type: this.generateType
      };
      
      if (this.generateType === 'video') {
        endpoint = '/api/assets/generate/video';
        body = {
          ecom_code: this.ecomCode,
          duration: 5,
          resolution: '480p'
        };
      }
      
      const response = await fetch(endpoint, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(body)
      });
      
      const result = await response.json();
      
      if (result.success) {
        this.taskInfo = {
          task_id: result.task_id,
          status: 'pending',
          progress: 0,
          message: '任务已提交...'
        };
        this.pollingTask = true;
        this._pollTaskStatus(result.task_id);
      } else {
        alert('生成任务提交失败: ' + result.message);
        this.generating = false;
      }
    } catch (e) {
      console.error('生成失败:', e);
      alert('生成失败，请检查服务器连接');
      this.generating = false;
    }
  }

  private async _pollTaskStatus(taskId: string) {
    while (this.pollingTask) {
      try {
        const response = await fetch(`/api/tasks/${taskId}`);
        const task = await response.json();
        this.taskInfo = task;
        
        if (task.status === 'success' || task.status === 'failed') {
          this.pollingTask = false;
          this.generating = false;
          
          if (task.status === 'success') {
            // 刷新素材列表
            await this.loadAssets();
            this.showGenerateModal = false;
          } else {
            alert('生成失败: ' + task.error);
          }
          break;
        }
        
        // 等待 2 秒后继续轮询
        await new Promise(r => setTimeout(r, 2000));
      } catch (e) {
        console.error('轮询任务状态失败:', e);
        this.pollingTask = false;
        this.generating = false;
      }
    }
  }

  private async _deleteAsset(type: string, groupIndex: number) {
    if (!confirm(`确定删除 ${type} 组 ${groupIndex}？`)) return;
    
    try {
      const response = await fetch(`/api/assets/${this.ecomCode}/${type}/${groupIndex}`, {
        method: 'DELETE'
      });
      
      if (response.ok) {
        await this.loadAssets();
      } else {
        alert('删除失败');
      }
    } catch (e) {
      console.error('删除失败:', e);
    }
  }

  private _previewAsset(type: string, group: any) {
    // 打开预览窗口或下载
    const files: string[] = group.files || [];
    if (files.length === 0) return;
    
    // 播放视频或显示图片
    if (type === 'video') {
      const merged = files.find((f: string) => f.includes('merged'));
      if (merged) {
        window.open('/assets/' + merged, '_blank');
      }
    } else {
      // 图片类型，显示第一张
      window.open('/assets/' + files[0], '_blank');
    }
  }

  render() {
    console.log('[AssetManager] render called, ecomCode:', this.ecomCode, 'loading:', this.loading, 'assets:', this.assets);
    
    if (this.loading) {
      return html`
        <div class="asset-manager">
          <div style="text-align: center; padding: 40px; color: var(--muted);">
            加载中...
          </div>
        </div>
      `;
    }

    const typeNames: Record<string, string> = {
      showcase: '展示图',
      video: '宣传视频',
      detail: '详情图'
    };

    return html`
      <div class="asset-manager">
        <div class="asset-header">
          <div class="asset-title">📁 素材管理</div>
          <button class="asset-close" @click=${this._close}>×</button>
        </div>
        
        <div style="font-size: 12px; color: var(--muted); margin-bottom: 16px;">
          商品: ${this.item?.title || this.ecomCode}
        </div>
        
        ${['showcase', 'video', 'detail'].map(type => html`
          <div class="asset-section">
            <div class="section-header">
              <div>
                <span class="section-title">${typeNames[type]}</span>
                <span class="section-count">(${this.assets[type]?.length || 0}组)</span>
              </div>
              <button class="add-btn" @click=${() => this._showGenerateModal(type)}>
                + 生成
              </button>
            </div>
            
            ${this.assets[type]?.length > 0 
              ? this.assets[type].map((group: any) => html`
                <div class="asset-group">
                  <div class="group-index">组 ${group.group_index}</div>
                  <div class="group-files">${group.files?.length || 0} 个文件</div>
                  <div class="group-actions">
                    <button class="preview-btn" @click=${() => this._previewAsset(type, group)}>
                      预览
                    </button>
                    <button class="delete-btn" @click=${() => this._deleteAsset(type, group.group_index)}>
                      删除
                    </button>
                  </div>
                </div>
              `)
              : html`<div class="empty-section">暂无素材</div>`
            }
          </div>
        `)}
      </div>
      
      ${this.showGenerateModal ? html`
        <div class="gen-modal-overlay" @click=${(e: Event) => {
          if (e.target === e.currentTarget) this._closeGenerateModal();
        }}>
          <div class="gen-modal">
            <div class="gen-modal-title">
              ${this.generateType === 'video' ? '🎬 生成宣传视频' : 
                this.generateType === 'showcase' ? '🖼️ 生成展示图' : '📋 生成详情图'}
            </div>
            
            <div class="gen-option">
              <div class="gen-label">图片来源：</div>
              <div class="gen-radio-group">
                <label class="gen-radio">
                  <input type="radio" name="imageSource" value="sourcing" checked>
                  使用货源图片
                </label>
                <label class="gen-radio">
                  <input type="radio" name="imageSource" value="custom">
                  上传自定义图片
                </label>
              </div>
            </div>
            
            ${this.generateType === 'video' ? html`
              <div class="gen-option">
                <div class="gen-label">视频时长：</div>
                <select class="gen-select">
                  <option value="5">5 秒/段（共15秒）</option>
                  <option value="8">8 秒/段（共24秒）</option>
                </select>
              </div>
              
              <div class="gen-option">
                <div class="gen-label">分辨率：</div>
                <select class="gen-select">
                  <option value="480p">480p（更快）</option>
                  <option value="720p">720p（更清晰）</option>
                </select>
              </div>
            ` : ''}
            
            ${this.taskInfo ? html`
              <div class="task-progress">
                <div class="task-status">
                  状态: ${this.taskInfo.status === 'pending' ? '等待中' :
                    this.taskInfo.status === 'running' ? '生成中...' :
                    this.taskInfo.status === 'success' ? '完成' : '失败'}
                </div>
                <div class="task-bar">
                  <div class="task-bar-fill" style="width: ${this.taskInfo.progress}%"></div>
                </div>
                <div class="task-message">${this.taskInfo.message || ''}</div>
              </div>
            ` : ''}
            
            <div class="gen-buttons">
              <button class="gen-cancel" @click=${this._closeGenerateModal} 
                ?disabled=${this.pollingTask}>
                取消
              </button>
              <button class="gen-confirm" @click=${this._startGenerate}
                ?disabled=${this.generating || this.pollingTask}>
                ${this.generating ? '生成中...' : '开始生成'}
              </button>
            </div>
          </div>
        </div>
      ` : ''}
    `;
  }
}
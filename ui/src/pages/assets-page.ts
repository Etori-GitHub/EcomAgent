import { LitElement, html, css } from 'lit';
import { customElement, state, property } from 'lit/decorators.js';
import './upload-generator';

@customElement('ea-assets-page')
export class EaAssetsPage extends LitElement {
  @property({ type: String }) ecomCode = '';  // 从货源库跳转时传入
  
  @state() private searchQuery = '';
  @state() private assets: any[] = [];
  @state() private loading = true;
  @state() private showUploadModal = false;  // 上传弹框

  // 保留原有状态变量，暂不删除
  // @state() private showGenerateModal = false;
  // @state() private generating = false;
  // @state() private generateType = 'showcase';
  // @state() private selectedEcomCode = '';
  // @state() private sourcingList: any[] = [];
  // @state() private taskInfo: any = null;
  // @state() private pollingTask = false;

  static styles = css`
    :host {
      display: block;
    }
    
    .assets-page {
      padding: 24px;
    }
    
    .page-header {
      display: flex;
      align-items: center;
      justify-content: space-between;
      margin-bottom: 24px;
    }
    
    .page-title {
      font-size: 24px;
      font-weight: 600;
      color: var(--text);
    }
    
    .header-actions {
      display: flex;
      gap: 12px;
      align-items: center;
    }
    
    .search-box {
      display: flex;
      align-items: center;
      background: var(--bg);
      border: 1px solid var(--border);
      border-radius: var(--radius-md);
      padding: 8px 12px;
      gap: 8px;
      min-width: 300px;
    }
    
    .search-box input {
      border: none;
      background: transparent;
      color: var(--text);
      font-size: 14px;
      outline: none;
      flex: 1;
    }
    
    .search-box input::placeholder {
      color: var(--muted);
    }
    
    .generate-btn {
      padding: 8px 16px;
      background: var(--primary);
      color: white;
      border: none;
      border-radius: var(--radius-md);
      font-size: 14px;
      cursor: pointer;
      display: flex;
      align-items: center;
      gap: 6px;
    }
    
    .generate-btn:hover {
      opacity: 0.9;
    }
    
    .assets-table {
      width: 100%;
      border-collapse: collapse;
      background: var(--bg);
      border-radius: var(--radius-md);
      overflow: hidden;
    }
    
    .assets-table th {
      text-align: left;
      padding: 12px 16px;
      font-size: 12px;
      font-weight: 500;
      color: var(--muted);
      text-transform: uppercase;
      letter-spacing: 0.5px;
      border-bottom: 1px solid var(--border);
    }
    
    .assets-table td {
      padding: 16px;
      border-bottom: 1px solid var(--border);
      vertical-align: middle;
    }
    
    .assets-table tr:last-child td {
      border-bottom: none;
    }
    
    .product-name {
      max-width: 200px;
      overflow: hidden;
      text-overflow: ellipsis;
      white-space: nowrap;
      font-size: 14px;
      color: var(--text);
    }
    
    .product-code {
      font-size: 12px;
      color: var(--muted);
      margin-top: 4px;
    }
    
    .asset-type {
      display: inline-flex;
      align-items: center;
      gap: 6px;
      padding: 4px 10px;
      border-radius: var(--radius-sm);
      font-size: 12px;
      font-weight: 500;
    }
    
    .asset-type.showcase {
      background: rgba(59, 130, 246, 0.1);
      color: #3b82f6;
    }
    
    .asset-type.video {
      background: rgba(239, 68, 68, 0.1);
      color: #ef4444;
    }
    
    .asset-type.detail {
      background: rgba(16, 185, 129, 0.1);
      color: #10b981;
    }
    
    .thumbnails {
      display: flex;
      gap: 4px;
      flex-wrap: wrap;
      max-width: 180px;
    }
    
    .thumb {
      width: 48px;
      height: 48px;
      border-radius: var(--radius-sm);
      object-fit: cover;
      cursor: pointer;
      border: 1px solid var(--border);
    }
    
    .thumb:hover {
      border-color: var(--primary);
    }
    
    .thumb-more {
      width: 48px;
      height: 48px;
      border-radius: var(--radius-sm);
      background: var(--border);
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 12px;
      color: var(--muted);
    }
    
    .time {
      font-size: 13px;
      color: var(--text);
    }
    
    .actions {
      display: flex;
      gap: 8px;
    }
    
    .action-btn {
      padding: 6px 12px;
      border-radius: var(--radius-sm);
      font-size: 12px;
      cursor: pointer;
      border: 1px solid var(--border);
      background: transparent;
      color: var(--text);
    }
    
    .action-btn:hover {
      background: var(--border);
    }
    
    .action-btn.delete {
      color: #ef4444;
      border-color: rgba(239, 68, 68, 0.3);
    }
    
    .action-btn.delete:hover {
      background: rgba(239, 68, 68, 0.1);
    }
    
    .empty-state {
      text-align: center;
      padding: 60px 20px;
      color: var(--muted);
    }
    
    .empty-state-icon {
      font-size: 48px;
      margin-bottom: 16px;
    }
    
    .empty-state-text {
      font-size: 14px;
    }
    
    /* 生成弹窗 */
    .modal-overlay {
      position: fixed;
      top: 0;
      left: 0;
      right: 0;
      bottom: 0;
      background: rgba(0, 0, 0, 0.5);
      display: flex;
      align-items: center;
      justify-content: center;
      z-index: 1000;
    }
    
    .modal-content {
      background: var(--bg);
      border-radius: var(--radius-lg);
      padding: 24px;
      width: 100%;
      max-width: 500px;
      max-height: 80vh;
      overflow-y: auto;
    }
    
    .modal-title {
      font-size: 18px;
      font-weight: 600;
      color: var(--text);
      margin-bottom: 20px;
    }
    
    .form-group {
      margin-bottom: 16px;
    }
    
    .form-label {
      display: block;
      font-size: 13px;
      color: var(--muted);
      margin-bottom: 6px;
    }
    
    .form-select {
      width: 100%;
      padding: 10px 12px;
      border: 1px solid var(--border);
      border-radius: var(--radius-md);
      background: var(--bg);
      color: var(--text);
      font-size: 14px;
      outline: none;
    }
    
    .form-select:focus {
      border-color: var(--primary);
    }
    
    .type-options {
      display: flex;
      gap: 12px;
    }
    
    .type-option {
      flex: 1;
      padding: 12px;
      border: 2px solid var(--border);
      border-radius: var(--radius-md);
      background: transparent;
      cursor: pointer;
      text-align: center;
    }
    
    .type-option.active {
      border-color: var(--primary);
      background: rgba(var(--primary-rgb), 0.1);
    }
    
    .type-option-label {
      font-size: 14px;
      font-weight: 500;
      color: var(--text);
    }
    
    .type-option-desc {
      font-size: 12px;
      color: var(--muted);
      margin-top: 4px;
    }
    
    .modal-actions {
      display: flex;
      gap: 12px;
      justify-content: flex-end;
      margin-top: 24px;
    }
    
    .modal-btn {
      padding: 10px 20px;
      border-radius: var(--radius-md);
      font-size: 14px;
      cursor: pointer;
    }
    
    .modal-btn.cancel {
      background: transparent;
      border: 1px solid var(--border);
      color: var(--text);
    }
    
    .modal-btn.confirm {
      background: var(--primary);
      border: none;
      color: white;
    }
    
    .modal-btn.confirm:disabled {
      opacity: 0.5;
      cursor: not-allowed;
    }
    
    /* 任务进度 */
    .task-progress {
      padding: 16px;
      background: var(--border);
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
      background: var(--muted);
      border-radius: 2px;
      overflow: hidden;
    }
    
    .task-bar-fill {
      height: 100%;
      background: var(--primary);
      transition: width 0.3s;
    }
    
    /* 图片预览 */
    .preview-overlay {
      position: fixed;
      top: 0;
      left: 0;
      right: 0;
      bottom: 0;
      background: rgba(0, 0, 0, 0.9);
      display: flex;
      align-items: center;
      justify-content: center;
      z-index: 2000;
    }
    
    .preview-image {
      max-width: 90%;
      max-height: 90%;
      object-fit: contain;
    }
    
    .preview-close {
      position: absolute;
      top: 20px;
      right: 20px;
      background: white;
      border: none;
      width: 40px;
      height: 40px;
      border-radius: 50%;
      font-size: 20px;
      cursor: pointer;
    }
  `;

  connectedCallback() {
    super.connectedCallback();
    console.log('[AssetsPage] connectedCallback called');
    // 如果有传入 ecomCode，设置为搜索词
    if (this.ecomCode) {
      this.searchQuery = this.ecomCode;
    }
    this.loadAssets();
  }

  protected updated(changedProperties: Map<string, any>) {
    if (changedProperties.has('ecomCode') && this.ecomCode) {
      this.searchQuery = this.ecomCode;
      this.loadAssets();
    }
  }

  async loadAssets() {
    console.log('[AssetsPage] loadAssets called');
    this.loading = true;
    this.requestUpdate();
    try {
      const url = this.searchQuery 
        ? `/api/assets/list?search=${encodeURIComponent(this.searchQuery)}`
        : '/api/assets/list';
      console.log('[AssetsPage] fetching:', url);
      const response = await fetch(url);
      const data = await response.json();
      console.log('[AssetsPage] response:', data);
      this.assets = data.assets || [];
    } catch (e) {
      console.error('[AssetsPage] 加载素材失败:', e);
      this.assets = [];
    }
    this.loading = false;
    console.log('[AssetsPage] loadAssets done, loading:', this.loading, 'assets:', this.assets.length);
    this.requestUpdate();
  }

  // 保留 loadSourcingList 方法，暂不删除
  // async loadSourcingList() {
  //   try {
  //     const response = await fetch('/api/sourcing/list?limit=100');
  //     const data = await response.json();
  //     this.sourcingList = data.items || [];
  //   } catch (e) {
  //     console.error('[AssetsPage] 加载货源列表失败:', e);
  //   }
  // }

  private _onSearch(e: KeyboardEvent) {
    if (e.key === 'Enter') {
      this.loadAssets();
    }
  }

  private _onSearchInput(e: Event) {
    const input = e.target as HTMLInputElement;
    this.searchQuery = input.value;
  }

  private _openUploadModal() {
    this.showUploadModal = true;
    this.requestUpdate();
    console.log('[AssetsPage] _openUploadModal called, showUploadModal:', this.showUploadModal);
  }

  private _closeUploadModal() {
    this.showUploadModal = false;
    this.requestUpdate();
    console.log('[AssetsPage] _closeUploadModal called, showUploadModal:', this.showUploadModal);
  }

  // 保留原有方法，暂不删除
  // private _openGenerateModal() {
  //   this.showGenerateModal = true;
  //   this.selectedEcomCode = this.ecomCode || '';
  //   this.generateType = 'showcase';
  //   this.taskInfo = null;
  //   this.generating = false;
  // }

  // private _closeGenerateModal() {
  //   this.showGenerateModal = false;
  //   this.pollingTask = false;
  // }

  // private async _startGenerate() {
  //   if (!this.selectedEcomCode) {
  //     alert('请选择货源');
  //     return;
  //   }
  //
  //   this.generating = true;
  //   
  //   try {
  //     let endpoint = '/api/assets/generate/image';
  //     let body: any = {
  //       ecom_code: this.selectedEcomCode,
  //       asset_type: this.generateType
  //     };
  //
  //     if (this.generateType === 'video') {
  //       endpoint = '/api/assets/generate/video';
  //       body = {
  //         ecom_code: this.selectedEcomCode,
  //         duration: 5,
  //         resolution: '480p'
  //       };
  //     }
  //
  //     const response = await fetch(endpoint, {
  //       method: 'POST',
  //       headers: { 'Content-Type': 'application/json' },
  //       body: JSON.stringify(body)
  //     });
  //
  //     const result = await response.json();
  //
  //     if (result.success) {
  //       this.taskInfo = {
  //         task_id: result.task_id,
  //         status: 'pending',
  //         progress: 0,
  //         message: '任务已提交...'
  //       };
  //       this.pollingTask = true;
  //       this._pollTaskStatus(result.task_id);
  //     } else {
  //       alert('生成任务提交失败: ' + result.message);
  //       this.generating = false;
  //     }
  //   } catch (e) {
  //     console.error('生成失败:', e);
  //     alert('生成失败，请检查服务器连接');
  //     this.generating = false;
  //   }
  // }
  //
  // private async _pollTaskStatus(taskId: string) {
  //   while (this.pollingTask) {
  //     try {
  //       const response = await fetch(`/api/tasks/${taskId}`);
  //       const task = await response.json();
  //       this.taskInfo = task;
  //
  //       if (task.status === 'success' || task.status === 'failed') {
  //         this.pollingTask = false;
  //         this.generating = false;
  //
  //         if (task.status === 'success') {
  //           await this.loadAssets();
  //           this.showGenerateModal = false;
  //         } else {
  //           alert('生成失败: ' + task.error);
  //         }
  //         break;
  //       }
  //
  //       await new Promise(r => setTimeout(r, 2000));
  //     } catch (e) {
  //       console.error('轮询任务状态失败:', e);
  //       this.pollingTask = false;
  //       this.generating = false;
  //     }
  //   }
  // }

  private _openFolder(ecomCode: string, assetType: string, groupIndex: number) {
    // 调用后端 API 打开文件夹
    fetch(`/api/assets/open-folder/${ecomCode}/${assetType}/${groupIndex}`, { method: 'POST' });
  }

  private async _deleteAsset(ecomCode: string, assetType: string, groupIndex: number) {
    if (!confirm('确定删除该素材？')) return;
    
    try {
      const response = await fetch(`/api/assets/${ecomCode}/${assetType}/${groupIndex}`, {
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

  private _previewImage(src: string) {
    // 简单的图片预览
    const overlay = document.createElement('div');
    overlay.className = 'preview-overlay';
    overlay.innerHTML = `
      <img class="preview-image" src="${src}" />
      <button class="preview-close">×</button>
    `;
    overlay.addEventListener('click', (e) => {
      if (e.target === overlay || (e.target as HTMLElement).classList.contains('preview-close')) {
        overlay.remove();
      }
    });
    document.body.appendChild(overlay);
  }

  private _formatTime(dateStr: string) {
    if (!dateStr) return '-';
    const date = new Date(dateStr);
    return date.toLocaleString('zh-CN', {
      year: 'numeric',
      month: '2-digit',
      day: '2-digit',
      hour: '2-digit',
      minute: '2-digit'
    });
  }

  private _getTypeName(type: string) {
    const names: Record<string, string> = {
      showcase: '展示图',
      video: '视频',
      detail: '详情图'
    };
    return names[type] || type;
  }

  private _getTypeIcon(type: string) {
    const icons: Record<string, string> = {
      showcase: '🖼️',
      video: '🎬',
      detail: '📋'
    };
    return icons[type] || '📄';
  }

  render() {
    return html`
      <div class="assets-page">
        <div class="page-header">
          <h1 class="page-title">📁 素材管理</h1>
          <div class="header-actions">
            <div class="search-box">
              <span>🔍</span>
              <input 
                type="text" 
                placeholder="搜索货源名称或编码..." 
                .value=${this.searchQuery}
                @input=${this._onSearchInput}
                @keydown=${this._onSearch}
              />
            </div>
            <button class="generate-btn" @click=${() => { console.log('[AssetsPage] 按钮被点击'); this._openUploadModal(); }}>
              + 上传生成
            </button>
          </div>
        </div>

        ${this.loading ? html`
          <div class="empty-state">
            <div class="empty-state-text">加载中...</div>
          </div>
        ` : this.assets.length === 0 ? html`
          <div class="empty-state">
            <div class="empty-state-icon">📁</div>
            <div class="empty-state-text">暂无素材，点击"生成素材"开始创建</div>
          </div>
        ` : html`
          <table class="assets-table">
            <thead>
              <tr>
                <th style="width: 200px;">货源名称</th>
                <th style="width: 100px;">资源类型</th>
                <th style="width: 200px;">缩略图</th>
                <th>简介</th>
                <th style="width: 140px;">生成时间</th>
                <th style="width: 160px;">操作</th>
              </tr>
            </thead>
            <tbody>
              ${this.assets.map((asset: any) => html`
                <tr>
                  <td>
                    <div class="product-name">${asset.title || '-'}</div>
                    <div class="product-code">${asset.ecom_code}</div>
                  </td>
                  <td>
                    <span class="asset-type ${asset.asset_type}">
                      ${this._getTypeIcon(asset.asset_type)} ${this._getTypeName(asset.asset_type)}
                    </span>
                  </td>
                  <td>
                    <div class="thumbnails">
                      ${(asset.thumbnails || []).slice(0, 3).map((thumb: string) => html`
                        <img 
                          class="thumb" 
                          src="${thumb}" 
                          @click=${() => this._previewImage(thumb)}
                        />
                      `)}
                      ${(asset.thumbnails?.length || 0) > 3 ? html`
                        <div class="thumb-more">+${(asset.thumbnails?.length || 0) - 3}</div>
                      ` : ''}
                    </div>
                  </td>
                  <td>-</td>
                  <td>
                    <div class="time">${this._formatTime(asset.created_at)}</div>
                  </td>
                  <td>
                    <div class="actions">
                      <button 
                        class="action-btn" 
                        @click=${() => this._openFolder(asset.ecom_code, asset.asset_type, asset.group_index)}
                      >
                        文件
                      </button>
                      <button 
                        class="action-btn delete" 
                        @click=${() => this._deleteAsset(asset.ecom_code, asset.asset_type, asset.group_index)}
                      >
                        删除
                      </button>
                    </div>
                  </td>
                </tr>
              `)}
            </tbody>
          </table>
        `}
      </div>

      ${this.showUploadModal ? html`
        <div class="modal-overlay" @click=${(e: Event) => {
          if (e.target === e.currentTarget) this._closeUploadModal();
        }}>
          <div class="modal-content">
            <upload-generator
              @close=${this._closeUploadModal}
            ></upload-generator>
          </div>
        </div>
      ` : ''}
    `;
  }
}

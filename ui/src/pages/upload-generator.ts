import { LitElement, html, css } from 'lit';
import { customElement, state, property } from 'lit/decorators.js';

/**
 * 上传图片生成素材弹窗
 * 支持拖拽上传或选择文件
 */
@customElement('upload-generator')
export class UploadGenerator extends LitElement {
  @property({ type: String }) sourcingCode = '';
  @property({ type: Object }) item: any = null;

  @state() private generateType: 'showcase' | 'video' | 'detail' = 'showcase';
  @state() private generating = false;
  @state() private taskInfo: any = null;
  @state() private pollingTask = false;
  
  // 上传相关
  @state() private uploadedImagePath = '';
  @state() private uploadedImagePreview = '';
  @state() private uploading = false;
  @state() private isDragging = false;
  
  // 货源选择
  @state() private sourcingList: any[] = [];

  // 视频参数
  @state() private videoDuration = 5;
  @state() private videoResolution = '480p';

  static styles = css`
    :host {
      display: block;
    }

    .generator {
      padding: 24px;
      width: 500px;
      max-width: 90vw;
      box-sizing: border-box;
    }

    .gen-header {
      display: flex;
      align-items: center;
      justify-content: space-between;
      margin-bottom: 24px;
    }

    .gen-title {
      font-size: 18px;
      font-weight: 600;
      color: var(--text);
    }

    .gen-close {
      background: none;
      border: none;
      font-size: 24px;
      cursor: pointer;
      color: var(--muted);
      line-height: 1;
    }

    .gen-close:hover {
      color: var(--text);
    }

    /* 上传区域 */
    .upload-section {
      margin-bottom: 24px;
    }

    .upload-label {
      font-size: 13px;
      color: var(--muted);
      margin-bottom: 12px;
    }

    .upload-area {
      border: 2px dashed var(--border);
      border-radius: var(--radius-md);
      padding: 40px 20px;
      text-align: center;
      cursor: pointer;
      transition: all 0.2s;
      background: var(--bg);
    }

    .upload-area:hover {
      border-color: var(--primary);
      background: var(--bg-hover);
    }

    .upload-area.dragging {
      border-color: var(--primary);
      background: rgba(var(--primary-rgb, 59, 130, 246), 0.1);
    }

    .upload-area.has-image {
      padding: 16px;
    }

    .upload-icon {
      font-size: 48px;
      margin-bottom: 12px;
    }

    .upload-text {
      font-size: 14px;
      color: var(--text);
      margin-bottom: 8px;
    }

    .upload-hint {
      font-size: 12px;
      color: var(--muted);
    }

    /* 货源选择 */
    .sourcing-section {
      margin-bottom: 24px;
    }

    .sourcing-label {
      font-size: 13px;
      color: var(--muted);
      margin-bottom: 12px;
    }

    .sourcing-select {
      width: 100%;
      padding: 10px 12px;
      border: 1px solid var(--border);
      border-radius: var(--radius-md);
      background: var(--bg);
      color: var(--text);
      font-size: 14px;
      cursor: pointer;
    }

    .sourcing-select:focus {
      border-color: var(--primary);
      outline: none;
    }

    .upload-input {
      display: none;
    }

    .preview-image {
      max-width: 100%;
      max-height: 200px;
      border-radius: var(--radius-sm);
      object-fit: contain;
    }

    .preview-actions {
      margin-top: 12px;
      display: flex;
      gap: 8px;
      justify-content: center;
    }

    .preview-btn {
      padding: 6px 12px;
      font-size: 12px;
      border-radius: var(--radius-sm);
      cursor: pointer;
      border: 1px solid var(--border);
      background: var(--bg);
      color: var(--text);
    }

    .preview-btn:hover {
      background: var(--bg-hover);
    }

    /* 类型选择 */
    .type-section {
      margin-bottom: 24px;
    }

    .type-label {
      font-size: 13px;
      color: var(--muted);
      margin-bottom: 12px;
    }

    .type-options {
      display: flex;
      gap: 12px;
    }

    .type-option {
      flex: 1;
      padding: 16px;
      border: 2px solid var(--border);
      border-radius: var(--radius-md);
      background: var(--bg);
      cursor: pointer;
      text-align: center;
      transition: all 0.2s;
    }

    .type-option:hover {
      border-color: var(--primary);
      background: var(--bg-hover);
    }

    .type-option.active {
      border-color: var(--primary);
      background: var(--primary);
    }

    .type-option.active .type-option-label {
      color: white;
      font-weight: 600;
    }

    .type-option.active .type-option-desc {
      color: rgba(255, 255, 255, 0.8);
    }

    .type-option-icon {
      font-size: 24px;
      margin-bottom: 8px;
    }

    .type-option-label {
      font-size: 13px;
      font-weight: 500;
      color: var(--text);
      margin-bottom: 4px;
    }

    .type-option-desc {
      font-size: 11px;
      color: var(--muted);
    }

    /* 视频参数 */
    .video-params {
      background: var(--bg);
      border-radius: var(--radius-md);
      padding: 16px;
      margin-bottom: 24px;
    }

    .param-row {
      display: flex;
      align-items: center;
      gap: 16px;
    }

    .param-group {
      flex: 1;
    }

    .param-label {
      font-size: 12px;
      color: var(--muted);
      margin-bottom: 6px;
    }

    .param-select {
      width: 100%;
      padding: 8px;
      border: 1px solid var(--border);
      border-radius: var(--radius-sm);
      background: var(--bg);
      color: var(--text);
      font-size: 13px;
    }

    /* 进度条 */
    .task-progress {
      background: var(--bg);
      border-radius: var(--radius-md);
      padding: 16px;
      margin-bottom: 20px;
    }

    .task-status {
      font-size: 13px;
      color: var(--text);
      margin-bottom: 12px;
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

    /* 操作按钮 */
    .gen-actions {
      display: flex;
      gap: 12px;
      justify-content: flex-end;
    }

    .gen-btn {
      padding: 10px 20px;
      font-size: 13px;
      border-radius: var(--radius-md);
      cursor: pointer;
      transition: all 0.2s;
    }

    .gen-btn-cancel {
      background: transparent;
      border: 1px solid var(--border);
      color: var(--muted);
    }

    .gen-btn-cancel:hover {
      border-color: var(--text);
      color: var(--text);
    }

    .gen-btn-confirm {
      background: var(--primary);
      border: none;
      color: white;
    }

    .gen-btn-confirm:hover {
      opacity: 0.9;
    }

    .gen-btn-confirm:disabled {
      opacity: 0.5;
      cursor: not-allowed;
    }
  `;

  private _close() {
    this.dispatchEvent(new CustomEvent('close'));
  }

  connectedCallback() {
    super.connectedCallback();
    this.loadSourcingList();
  }

  async loadSourcingList() {
    try {
      const response = await fetch('/api/sourcing/list?limit=100');
      const data = await response.json();
      console.log('[UploadGenerator] 货源列表:', data);
      this.sourcingList = data.data || [];
      this.requestUpdate();
      console.log('[UploadGenerator] sourcingList 长度:', this.sourcingList.length);
    } catch (e) {
      console.error('[UploadGenerator] 加载货源列表失败:', e);
    }
  }

  private _handleDragOver(e: DragEvent) {
    e.preventDefault();
    this.isDragging = true;
  }

  private _handleDragLeave(e: DragEvent) {
    e.preventDefault();
    this.isDragging = false;
  }

  private _handleDrop(e: DragEvent) {
    e.preventDefault();
    this.isDragging = false;
    
    const files = e.dataTransfer?.files;
    if (files && files.length > 0) {
      this._uploadFile(files[0]);
    }
  }

  private _handleFileSelect(e: Event) {
    const input = e.target as HTMLInputElement;
    const files = input.files;
    if (files && files.length > 0) {
      this._uploadFile(files[0]);
    }
  }

  private async _uploadFile(file: File) {
    // 验证文件类型
    if (!file.type.startsWith('image/')) {
      alert('请上传图片文件');
      return;
    }

    // 验证文件大小（最大 10MB）
    if (file.size > 10 * 1024 * 1024) {
      alert('图片大小不能超过 10MB');
      return;
    }

    this.uploading = true;

    try {
      const formData = new FormData();
      formData.append('file', file);

      const response = await fetch('/api/assets/upload-image', {
        method: 'POST',
        body: formData
      });

      const result = await response.json();

      if (result.success) {
        this.uploadedImagePath = result.path;
        this.uploadedImagePreview = result.url;
      } else {
        alert('上传失败: ' + result.message);
      }
    } catch (e) {
      console.error('上传失败:', e);
      alert('上传失败，请检查服务器连接');
    }

    this.uploading = false;
  }

  private _clearImage() {
    this.uploadedImagePath = '';
    this.uploadedImagePreview = '';
  }

  private async _startGenerate() {
    if (!this.uploadedImagePath) {
      alert('请先上传图片');
      return;
    }

    this.generating = true;

    try {
      let endpoint = '/api/assets/generate/upload';
      // 如果选择了货源，使用货源编码；否则传 null，后端生成新编码
      const body: any = {
        image_path: this.uploadedImagePath,
        asset_type: this.generateType,
        sourcing_code: this.sourcingCode || null
      };

      if (this.generateType === 'video') {
        body.duration = this.videoDuration;
        body.resolution = this.videoResolution;
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
            setTimeout(() => {
              alert('生成成功!');
              this._close();
            }, 500);
          } else {
            alert('生成失败: ' + task.error);
          }
          break;
        }

        await new Promise(r => setTimeout(r, 2000));
      } catch (e) {
        console.error('轮询任务状态失败:', e);
        this.pollingTask = false;
        this.generating = false;
      }
    }
  }

  render() {
    return html`
      <div class="generator">
        <div class="gen-header">
          <div class="gen-title">上传图片生成素材</div>
          <button class="gen-close" @click=${this._close} ?disabled=${this.generating}>×</button>
        </div>

        <!-- 上传区域 -->
        <div class="upload-section">
          <div class="upload-label">参考图片</div>
          ${this.uploadedImagePreview ? html`
            <div class="upload-area has-image">
              <img class="preview-image" src=${this.uploadedImagePreview} />
              <div class="preview-actions">
                <button class="preview-btn" @click=${() => this.shadowRoot?.querySelector<HTMLInputElement>('.upload-input')?.click()}>
                  更换图片
                </button>
                <button class="preview-btn" @click=${this._clearImage}>
                  清除
                </button>
              </div>
            </div>
          ` : html`
            <div 
              class="upload-area ${this.isDragging ? 'dragging' : ''}"
              @click=${() => this.shadowRoot?.querySelector<HTMLInputElement>('.upload-input')?.click()}
              @dragover=${this._handleDragOver}
              @dragleave=${this._handleDragLeave}
              @drop=${this._handleDrop}
            >
              <div class="upload-icon">📤</div>
              <div class="upload-text">${this.uploading ? '上传中...' : '拖拽图片到此处或点击上传'}</div>
              <div class="upload-hint">支持 JPG、PNG、WebP 格式，最大 10MB</div>
            </div>
          `}
          <input 
            class="upload-input"
            type="file"
            accept="image/*"
            @change=${this._handleFileSelect}
          />
        </div>

        <!-- 货源选择 -->
        <div class="sourcing-section">
          <div class="sourcing-label">关联货源（可选）</div>
          <select 
            class="sourcing-select"
            .value=${this.sourcingCode}
            @change=${(e: Event) => { this.sourcingCode = (e.target as HTMLSelectElement).value; }}
          >
            <option value="">不关联货源</option>
            ${this.sourcingList.map((item: any) => html`
              <option value=${item.sourcing_code}>${item.title || item.sourcing_code}</option>
            `)}
          </select>
        </div>

        <!-- 类型选择 -->
        <div class="type-section">
          <div class="type-label">选择素材类型</div>
          <div class="type-options">
            <button
              class="type-option ${this.generateType === 'showcase' ? 'active' : ''}"
              @click=${() => { this.generateType = 'showcase'; this.requestUpdate(); }}
              ?disabled=${this.generating}
            >
              <div class="type-option-icon">🖼️</div>
              <div class="type-option-label">展示图</div>
              <div class="type-option-desc">9张营销图</div>
            </button>
            <button
              class="type-option ${this.generateType === 'video' ? 'active' : ''}"
              @click=${() => { this.generateType = 'video'; this.requestUpdate(); }}
              ?disabled=${this.generating}
            >
              <div class="type-option-icon">🎬</div>
              <div class="type-option-label">视频</div>
              <div class="type-option-desc">宣传视频</div>
            </button>
            <button
              class="type-option ${this.generateType === 'detail' ? 'active' : ''}"
              @click=${() => { this.generateType = 'detail'; this.requestUpdate(); }}
              ?disabled=${this.generating}
            >
              <div class="type-option-icon">📋</div>
              <div class="type-option-label">详情图</div>
              <div class="type-option-desc">详情页图片</div>
            </button>
          </div>
        </div>

        <!-- 视频参数 -->
        ${this.generateType === 'video' ? html`
          <div class="video-params">
            <div class="param-row">
              <div class="param-group">
                <div class="param-label">视频时长</div>
                <select 
                  class="param-select"
                  .value=${String(this.videoDuration)}
                  @change=${(e: Event) => { this.videoDuration = parseInt((e.target as HTMLSelectElement).value); }}
                >
                  <option value="3">3 秒</option>
                  <option value="5">5 秒</option>
                  <option value="10">10 秒</option>
                  <option value="15">15 秒</option>
                </select>
              </div>
              <div class="param-group">
                <div class="param-label">分辨率</div>
                <select 
                  class="param-select"
                  .value=${this.videoResolution}
                  @change=${(e: Event) => { this.videoResolution = (e.target as HTMLSelectElement).value; }}
                >
                  <option value="480p">480p</option>
                  <option value="720p">720p</option>
                  <option value="1080p">1080p</option>
                </select>
              </div>
            </div>
          </div>
        ` : ''}

        ${this.taskInfo ? html`
          <div class="task-progress">
            <div class="task-status">${this.taskInfo.message || '处理中...'}</div>
            <div class="task-bar">
              <div class="task-bar-fill" style="width: ${this.taskInfo.progress || 0}%"></div>
            </div>
          </div>
        ` : ''}

        <div class="gen-actions">
          <button class="gen-btn gen-btn-cancel" @click=${this._close} ?disabled=${this.generating}>
            取消
          </button>
          <button 
            class="gen-btn gen-btn-confirm" 
            @click=${this._startGenerate} 
            ?disabled=${this.generating || !this.uploadedImagePath}
          >
            ${this.generating ? '生成中...' : '开始生成'}
          </button>
        </div>
      </div>
    `;
  }
}

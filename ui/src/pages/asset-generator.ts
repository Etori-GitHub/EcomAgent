import { LitElement, html, css } from 'lit';
import { customElement, property, state } from 'lit/decorators.js';

/**
 * 生成素材弹窗
 * 用于货源库页面点击"素材"按钮后,选择生成展示图/视频/详情图
 */
@customElement('asset-generator')
export class AssetGenerator extends LitElement {
  @property({ type: String }) ecomCode = '';
  @property({ type: Object }) item: any = null;

  @state() private generateType: 'showcase' | 'video' | 'detail' = 'showcase';
  @state() private generating = false;
  @state() private taskInfo: any = null;
  @state() private pollingTask = false;

  static styles = css`
    :host {
      display: block;
    }

    .generator {
      padding: 20px;
      min-width: 400px;
    }

    .gen-header {
      display: flex;
      align-items: center;
      justify-content: space-between;
      margin-bottom: 20px;
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

    .product-info {
      background: var(--bg);
      border-radius: var(--radius-md);
      padding: 12px;
      margin-bottom: 20px;
      display: flex;
      align-items: center;
      gap: 12px;
    }

    .product-thumb {
      width: 48px;
      height: 48px;
      object-fit: cover;
      border-radius: var(--radius-sm);
    }

    .product-name {
      font-size: 13px;
      color: var(--text);
      overflow: hidden;
      text-overflow: ellipsis;
      white-space: nowrap;
      flex: 1;
    }

    .product-code {
      font-size: 11px;
      color: var(--muted);
    }

    .type-section {
      margin-bottom: 20px;
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
      border-width: 2px;
      background: var(--primary);
      box-shadow: 0 0 0 2px rgba(var(--primary-rgb, 59, 130, 246), 0.3);
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

  private async _startGenerate() {
    if (!this.ecomCode) {
      alert('缺少商品编码');
      return;
    }

    this.generating = true;

    try {
      let endpoint = '/api/assets/generate/image';
      const body: any = {
        ecom_code: this.ecomCode,
        asset_type: this.generateType
      };

      if (this.generateType === 'video') {
        endpoint = '/api/assets/generate/video';
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
      alert('生成失败,请检查服务器连接');
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
            // 生成成功,关闭弹窗
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
    const imageUrl = this.item?.local_image_path
      ? `/images/${this.item.local_image_path}`
      : this.item?.image_url;

    return html`
      <div class="generator">
        <div class="gen-header">
          <div class="gen-title">生成素材</div>
          <button class="gen-close" @click=${this._close} ?disabled=${this.generating}>×</button>
        </div>

        <div class="product-info">
          ${imageUrl ? html`<img class="product-thumb" src=${imageUrl} />` : ''}
          <div style="flex:1; overflow: hidden;">
            <div class="product-name">${this.item?.title || this.ecomCode}</div>
            <div class="product-code">${this.ecomCode}</div>
          </div>
        </div>

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
          <button class="gen-btn gen-btn-confirm" @click=${this._startGenerate} ?disabled=${this.generating}>
            ${this.generating ? '生成中...' : '开始生成'}
          </button>
        </div>
      </div>
    `;
  }
}

/**
 * 1688货源采集 - Popup Script
 */

// 初始化
async function init() {
  // 检查服务状态
  checkServerStatus();
  
  // 加载当前ecom_code
  chrome.storage.local.get(['currentEcomCode'], (result) => {
    const code = result.currentEcomCode || '';
    updateEcomCode(code);
  });
  
  // 加载统计数据
  chrome.storage.local.get(['collectedProducts', 'pendingProducts'], (result) => {
    const collected = result.collectedProducts?.length || 0;
    const pending = result.pendingProducts?.length || 0;
    document.getElementById('collectedCount').textContent = collected;
    document.getElementById('pendingCount').textContent = pending;
  });
}

// 检查服务状态
async function checkServerStatus() {
  const dot = document.getElementById('statusDot');
  const text = document.getElementById('statusText');
  
  try {
    const response = await fetch('http://127.0.0.1:8000/api/stats', {
      method: 'GET',
      timeout: 3000
    });
    
    if (response.ok) {
      dot.classList.remove('offline');
      text.textContent = '服务正常';
    } else {
      dot.classList.add('offline');
      text.textContent = '服务异常';
    }
  } catch (e) {
    dot.classList.add('offline');
    text.textContent = '服务离线';
  }
}

// 更新ecom_code显示
function updateEcomCode(code) {
  const element = document.getElementById('ecomCode');
  if (code) {
    element.textContent = code;
    element.classList.remove('empty');
  } else {
    element.textContent = '未设置';
    element.classList.add('empty');
  }
}

// 设置ecom_code
document.getElementById('setEcomCode').addEventListener('click', () => {
  const input = document.getElementById('ecomCodeInput');
  const code = input.value.trim();
  
  if (code) {
    chrome.storage.local.set({ currentEcomCode: code }, () => {
      updateEcomCode(code);
      input.value = '';
    });
  }
});

// 同步待提交数据
document.getElementById('syncBtn').addEventListener('click', async () => {
  const btn = document.getElementById('syncBtn');
  btn.textContent = '同步中...';
  btn.disabled = true;
  
  try {
    const result = await chrome.runtime.sendMessage({ type: 'SYNC_PENDING' });
    
    if (result.success) {
      document.getElementById('pendingCount').textContent = result.failed;
      btn.textContent = `已同步 ${result.synced} 条`;
      
      // 刷新已采集数量
      chrome.storage.local.get(['collectedProducts'], (r) => {
        const collected = (r.collectedProducts?.length || 0) + result.synced;
        document.getElementById('collectedCount').textContent = collected;
      });
    } else {
      btn.textContent = '同步失败';
    }
  } catch (e) {
    btn.textContent = '同步失败';
  }
  
  setTimeout(() => {
    btn.textContent = '同步到服务器';
    btn.disabled = false;
  }, 2000);
});

// 定时刷新
setInterval(checkServerStatus, 5000);

// 启动
init();
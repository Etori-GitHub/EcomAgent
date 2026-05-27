/**
 * 1688货源采集 - Background Service Worker
 * 处理消息和存储同步
 */

// 监听来自content script的消息
chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  if (message.type === 'COLLECT_PRODUCT') {
    handleCollectProduct(message.data)
      .then(result => sendResponse(result))
      .catch(error => sendResponse({ success: false, error: error.message }));
    return true; // 保持消息通道开启
  }
  
  if (message.type === 'GET_PENDING') {
    chrome.storage.local.get(['pendingProducts'], (result) => {
      sendResponse({ pending: result.pendingProducts || [] });
    });
    return true;
  }
  
  if (message.type === 'SYNC_PENDING') {
    syncPendingProducts()
      .then(result => sendResponse(result))
      .catch(error => sendResponse({ success: false, error: error.message }));
    return true;
  }
});

// 处理采集
async function handleCollectProduct(data) {
  try {
    const response = await fetch('http://127.0.0.1:8000/api/sourcing', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data)
    });
    
    if (response.ok) {
      return { success: true };
    } else {
      // 保存到待同步队列
      chrome.storage.local.get(['pendingProducts'], (result) => {
        const pending = result.pendingProducts || [];
        pending.push(data);
        chrome.storage.local.set({ pendingProducts: pending });
      });
      return { success: false, error: 'API错误', savedLocal: true };
    }
  } catch (e) {
    // 保存到待同步队列
    chrome.storage.local.get(['pendingProducts'], (result) => {
      const pending = result.pendingProducts || [];
      pending.push(data);
      chrome.storage.local.set({ pendingProducts: pending });
    });
    return { success: false, error: e.message, savedLocal: true };
  }
}

// 同步待提交数据
async function syncPendingProducts() {
  const result = await chrome.storage.local.get(['pendingProducts']);
  const pending = result.pendingProducts || [];
  
  if (pending.length === 0) {
    return { success: true, synced: 0 };
  }
  
  let synced = 0;
  const failed = [];
  
  for (const data of pending) {
    try {
      const response = await fetch('http://127.0.0.1:8000/api/sourcing', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
      });
      
      if (response.ok) {
        synced++;
      } else {
        failed.push(data);
      }
    } catch (e) {
      failed.push(data);
    }
  }
  
  // 更新存储
  await chrome.storage.local.set({ pendingProducts: failed });
  
  return { success: true, synced, failed: failed.length };
}
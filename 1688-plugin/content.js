/**
 * 1688货源采集 - Content Script
 * 在商品卡片悬停时采集信息
 */

(function() {
  'use strict';

  // ==================== 配置 ====================
  const CONFIG = {
    API_URL: 'http://127.0.0.1:8000/api/sourcing',
    HOVER_DELAY: 300,  // 悬停延迟(ms)
    TOOLTIP_POSITION: 'right'
  };

  // 当前采集状态
  let currentEcomCode = null;
  let hoverTimer = null;
  let currentTooltip = null;

  // ==================== 初始化 ====================
  function init() {
    // 从URL获取ecom_code
    const urlParams = new URLSearchParams(window.location.search);
    currentEcomCode = urlParams.get('ecom_code') || urlParams.get('ref');
    
    if (currentEcomCode) {
      console.log('[EcomAgent] 检测到来源商品:', currentEcomCode);
      chrome.storage.local.set({ currentEcomCode });
      showStatusIndicator();
    }

    // 监听商品卡片悬停
    setupHoverListeners();
    
    // 监听动态加载的内容
    setupMutationObserver();
    
    // 监听存储变化
    chrome.storage.onChanged.addListener((changes) => {
      if (changes.currentEcomCode) {
        currentEcomCode = changes.currentEcomCode.newValue;
      }
    });
  }
  
  // ==================== 动态内容监听 ====================
  function setupMutationObserver() {
    const observer = new MutationObserver((mutations) => {
      // 每次DOM变化时重新绑定事件
      for (const mutation of mutations) {
        if (mutation.addedNodes.length > 0) {
          // 新节点添加后，重新检查
        }
      }
    });
    
    observer.observe(document.body, {
      childList: true,
      subtree: true
    });
  }

  // ==================== 状态指示器 ====================
  function showStatusIndicator() {
    const indicator = document.createElement('div');
    indicator.className = 'ecomagent-status-indicator';
    indicator.innerHTML = `
      <span class="ecomagent-icon">📦</span>
      <span class="ecomagent-text">采集模式: ${currentEcomCode}</span>
    `;
    document.body.appendChild(indicator);
  }

  // ==================== 悬停监听 ====================
  function setupHoverListeners() {
    // 1688 商品卡片选择器 - 使用更宽松的匹配
    document.addEventListener('mouseover', (e) => {
      const target = e.target;
      
      // 检查是否悬停在商品相关元素上
      // 1688 商品卡片通常有特定的类名或数据属性
      const card = target.closest('[class*="offer-card"]') || 
                   target.closest('[class*="offer-item"]') ||
                   target.closest('[class*="list-item"]') ||
                   target.closest('[data-offer-id]') ||
                   target.closest('[data-object-id]');
      
      if (card) {
        if (hoverTimer) clearTimeout(hoverTimer);
        hoverTimer = setTimeout(() => {
          showCollectTooltip(card);
        }, CONFIG.HOVER_DELAY);
      }
    }, true);

    document.addEventListener('mouseout', (e) => {
      if (hoverTimer) {
        clearTimeout(hoverTimer);
        hoverTimer = null;
      }
    }, true);
  }

  // 查找商品卡片
  function findProductCard(element) {
    let current = element;
    
    // 向上查找，最多10层
    for (let i = 0; i < 10; i++) {
      if (!current || current === document.body) break;
      
      // 检查是否有商品ID相关属性
      let offerId = current.getAttribute('data-offer-id') ||
                   current.getAttribute('data-id') ||
                   current.getAttribute('data-object-id');
      
      // 新增：检查 data-extra 属性里的 offerId
      if (!offerId) {
        const dataExtra = current.getAttribute('data-extra');
        if (dataExtra) {
          try {
            const extra = JSON.parse(dataExtra.replace(/&quot;/g, '"'));
            offerId = extra.offerId;
          } catch (e) {}
        }
      }
      
      if (offerId) {
        console.log('[EcomAgent] 找到商品卡片:', current.className, 'offerId:', offerId);
        return current;
      }
      
      // 检查类名是否包含 offer/item 等关键词
      const className = current.className || '';
      if (className.includes('offer-item') || 
          className.includes('offer-card') ||
          className.includes('list-item') ||
          className.includes('search-item')) {
        console.log('[EcomAgent] 通过类名找到商品卡片:', className);
        return current;
      }
      
      current = current.parentElement;
    }
    
    // 如果没找到，返回原始元素的最近的可点击父级
    return element.closest('a')?.parentElement || element;
  }

  // ==================== 采集Tooltip ====================
  function showCollectTooltip(card) {
    // 移除旧tooltip
    hideTooltip();

    // 提取商品信息
    const productData = extractProductData(card);
    if (!productData) return;

    // 创建tooltip
    const tooltip = document.createElement('div');
    tooltip.className = 'ecomagent-tooltip';
    tooltip.innerHTML = `
      <div class="ecomagent-tooltip-header">
        <span class="ecomagent-icon">📦</span>
        货源采集
      </div>
      <div class="ecomagent-tooltip-body">
        <div class="ecomagent-product-info">
          <img src="${productData.image}" class="ecomagent-thumb" onerror="this.src='data:image/svg+xml,<svg xmlns=%22http://www.w3.org/2000/svg%22 width=%2260%22 height=%2260%22><rect fill=%22%23ddd%22 width=%2260%22 height=%2260%22/><text x=%2230%22 y=%2235%22 text-anchor=%22middle%22 fill=%22%23999%22 font-size=%2212%22>无图</text></svg>'">
          <div class="ecomagent-details">
            <div class="ecomagent-title">${productData.title}</div>
            <div class="ecomagent-price">￥${productData.price}</div>
            <div class="ecomagent-shop">${productData.shopName}</div>
          </div>
        </div>
        <div class="ecomagent-source">
          关联商品: <strong>${currentEcomCode || '未设置'}</strong>
        </div>
      </div>
      <div class="ecomagent-tooltip-footer">
        <button class="ecomagent-btn ecomagent-btn-primary" id="ecomagent-collect">
          确认采集
        </button>
        <button class="ecomagent-btn ecomagent-btn-secondary" id="ecomagent-cancel">
          取消
        </button>
      </div>
    `;

    // 定位tooltip
    const rect = card.getBoundingClientRect();
    tooltip.style.left = `${rect.right + 10}px`;
    tooltip.style.top = `${rect.top}px`;

    // 如果右边空间不足，显示在左边
    if (rect.right + 350 > window.innerWidth) {
      tooltip.style.left = `${rect.left - 350}px`;
    }

    document.body.appendChild(tooltip);
    currentTooltip = tooltip;

    // 绑定按钮事件
    tooltip.querySelector('#ecomagent-collect').addEventListener('click', () => {
      collectProduct(productData);
      hideTooltip();
    });

    tooltip.querySelector('#ecomagent-cancel').addEventListener('click', () => {
      hideTooltip();
    });
  }

  function hideTooltip() {
    if (currentTooltip) {
      currentTooltip.remove();
      currentTooltip = null;
    }
  }

  // ==================== 数据提取 ====================
  function extractProductData(card) {
    try {
      // 调试：打印卡片信息
      console.log('[EcomAgent] 分析卡片:', card.className, card.tagName);
      console.log('[EcomAgent] 卡片HTML前100字符:', card.outerHTML.slice(0, 100));
      
      // 方法1：从 data 属性提取
      let offerId = 
        card.getAttribute('data-offer-id') ||
        card.querySelector('[data-offer-id]')?.getAttribute('data-offer-id') ||
        card.getAttribute('data-id') ||
        card.querySelector('[data-id]')?.getAttribute('data-id') ||
        card.getAttribute('data-object-id') ||
        card.querySelector('[data-object-id]')?.getAttribute('data-object-id') ||
        null;

      // 方法1.5：从 data-extra 属性提取（1688 新格式）
      if (!offerId) {
        const dataExtra = card.getAttribute('data-extra') ||
                         card.querySelector('[data-extra]')?.getAttribute('data-extra');
        if (dataExtra) {
          try {
            const extra = JSON.parse(dataExtra.replace(/&quot;/g, '"'));
            offerId = extra.offerId;
            console.log('[EcomAgent] 从 data-extra 提取到 offerId:', offerId);
          } catch (e) {
            // 尝试正则匹配
            const match = dataExtra.match(/"offerId"\s*:\s*"(\d+)"/);
            if (match) {
              offerId = match[1];
              console.log('[EcomAgent] 从 data-extra 正则匹配到 offerId:', offerId);
            }
          }
        }
      }
      
      // 方法1.6：从 data-key-value 提取（广告商品）
      if (!offerId) {
        const dataKeyValue = card.getAttribute('data-key-value') ||
                            card.querySelector('[data-key-value]')?.getAttribute('data-key-value');
        if (dataKeyValue) {
          const match = dataKeyValue.match(/offer_(\d+)/);
          if (match) {
            offerId = match[1];
            console.log('[EcomAgent] 从 data-key-value 提取到 offerId:', offerId);
          }
        }
      }
      
      // 方法1.7：从 data-aplus-report 提取（广告商品）
      if (!offerId) {
        const aplusReport = card.getAttribute('data-aplus-report');
        if (aplusReport) {
          const match = aplusReport.match(/object_id@(\d+)/);
          if (match) {
            offerId = match[1];
            console.log('[EcomAgent] 从 data-aplus-report 提取到 offerId:', offerId);
          }
        }
      }

      console.log('[EcomAgent] 方法1提取的 offerId:', offerId);
      
      // 方法2：从链接提取
      if (!offerId) {
        // 先检查卡片自己是不是链接
        if (card.tagName === 'A') {
          const id = extractOfferIdFromUrl(card.href);
          if (id) {
            console.log('[EcomAgent] 方法2从卡片自身链接提取到ID:', id, card.href);
            return extractFromLink(card, id);
          }
        }
        
        // 再检查子元素链接
        const links = card.querySelectorAll('a');
        console.log('[EcomAgent] 方法2: 检查', links.length, '个子链接');
        for (const link of links) {
          console.log('[EcomAgent] 检查链接:', link.href?.slice(0, 80));
          const id = extractOfferIdFromUrl(link.href);
          if (id) {
            console.log('[EcomAgent] 方法2从链接提取到ID:', id, link.href);
            return extractFromLink(link, id);
          }
        }
      }
      
      // 方法3：从父级卡片提取（1688 可能嵌套多层）
      if (!offerId) {
        const parentCard = card.closest('[class*="offer"]');
        if (parentCard && parentCard !== card) {
          console.log('[EcomAgent] 方法3检查父级:', parentCard.className);
          const parentId = parentCard.getAttribute('data-offer-id') ||
                          parentCard.getAttribute('data-id') ||
                          extractOfferIdFromUrl(parentCard.querySelector('a')?.href);
          if (parentId) {
            console.log('[EcomAgent] 从父级提取到ID:', parentId);
            return extractProductData(parentCard);
          }
        }
      }

      if (!offerId) {
        console.log('[EcomAgent] 所有方法都无法提取商品ID');
        return null;
      }

      // 标题
      const title = 
        card.querySelector('.offer-title, .title, [class*="title"], h3, h4')?.textContent?.trim() ||
        card.querySelector('a')?.title ||
        '';

      // 价格
      const priceText = 
        card.querySelector('.price, [class*="price"]')?.textContent?.trim() ||
        '';
      const price = extractPrice(priceText);

      // 图片 - 优先从 main-img 类获取
      let image = '';
      const mainImg = card.querySelector('img.main-img');
      if (mainImg) {
        image = mainImg.src || mainImg.getAttribute('data-src') || mainImg.getAttribute('data-lazy-src') || '';
      }
      if (!image) {
        const anyImg = card.querySelector('img');
        image = anyImg?.src || anyImg?.getAttribute('data-src') || '';
      }
      console.log('[EcomAgent] 提取的图片URL:', image?.slice(0, 80));

      // 店铺
      const shopElement = card.querySelector('[class*="shop"], [class*="company"]');
      const shopName = shopElement?.textContent?.trim() || '';
      const shopUrl = shopElement?.querySelector('a')?.href || '';

      // 商品链接 - 找真正的商品详情链接
      let productUrl = '';
      const allLinks = card.querySelectorAll('a');
      for (const link of allLinks) {
        const href = link.href || '';
        // 商品详情链接格式: detail.1688.com/offer/xxx 或 offer/xxx.html
        if ((href.includes('detail.1688.com') || href.includes('offer/')) && 
            !href.includes('air.1688.com') && 
            !href.includes('im/')) {
          productUrl = href;
          break;
        }
      }
      
      // 如果没找到，使用第一个非聊天链接
      if (!productUrl) {
        for (const link of allLinks) {
          const href = link.href || '';
          if (!href.includes('air.1688.com') && !href.includes('javascript:')) {
            productUrl = href;
            break;
          }
        }
      }

      // 起订量
      const minOrderText = 
        card.querySelector('[class*="min"]')?.textContent ||
        '';
      const minOrder = parseInt(minOrderText.match(/\d+/)?.[0] || '1');

      return {
        offerId,
        title: title.slice(0, 100),
        price,
        image,
        shopName,
        shopUrl,
        productUrl,
        minOrder
      };
    } catch (e) {
      console.error('[EcomAgent] 提取数据失败:', e);
      return null;
    }
  }

  // 从链接提取商品信息
  function extractFromLink(link, offerId) {
    // 找到完整的商品卡片容器
    const card = link.closest('[class*="offer"]') || link.closest('[class*="item"]') || link.closest('[class*="card"]') || link.parentElement?.parentElement?.parentElement;
    
    console.log('[EcomAgent] extractFromLink 卡片:', card?.className, card?.outerHTML?.slice(0, 200));
    
    // 标题 - 优先从链接的 title 属性获取，其次从卡片标题元素
    let title = link.title || link.getAttribute('data-title') || '';
    if (!title) {
      const titleEl = card?.querySelector('[class*="title"]') || card?.querySelector('h3') || card?.querySelector('h4');
      title = titleEl?.textContent?.trim() || '';
    }
    
    // 图片 - 优先从卡片内获取
    let image = '';
    const imgEl = card?.querySelector('img');
    if (imgEl) {
      image = imgEl.src || imgEl.getAttribute('data-src') || imgEl.getAttribute('data-lazy-src') || '';
      // 处理 1688 图片 URL 格式
      if (image && !image.startsWith('http')) {
        image = '';
      }
    }
    
    // 价格
    const priceEl = card?.querySelector('[class*="price"]');
    const priceText = priceEl?.textContent?.trim() || '';
    const price = extractPrice(priceText);
    
    // 店铺
    const shopEl = card?.querySelector('[class*="shop"]') || card?.querySelector('[class*="company"]') || card?.querySelector('[class*="seller"]');
    const shopName = shopEl?.textContent?.trim() || '';
    const shopUrl = shopEl?.querySelector('a')?.href || '';
    
    // 商品链接
    const productUrl = link.href || '';
    
    // 起订量
    const minOrderEl = card?.querySelector('[class*="min"]');
    const minOrderText = minOrderEl?.textContent || '';
    const minOrder = parseInt(minOrderText.match(/\d+/)?.[0] || '1');
    
    console.log('[EcomAgent] 提取结果:', { offerId, title: title.slice(0, 50), price, shopName, image: image.slice(0, 50) });
    
    return {
      offerId,
      title: title.slice(0, 100),
      price,
      image,
      shopName,
      shopUrl,
      productUrl,
      minOrder
    };
  }

  // 从URL提取offer ID
  function extractOfferIdFromUrl(url) {
    if (!url) return null;
    
    // 排除非商品链接（聊天、收藏、购物车等）
    if (url.includes('air.1688.com') || 
        url.includes('im/') || 
        url.includes('favorite') ||
        url.includes('cart') ||
        url.includes('trade')) {
      return null;
    }
    
    // 匹配商品详情链接
    // 格式1: offer/123456.html
    // 格式2: offerId=123456
    // 格式3: detail.m.1688.com/page/index.html?offerId=123456
    let match = url.match(/offer\/(\d+)/);
    if (match) return match[1];
    
    match = url.match(/[?&]offerId=(\d+)/);
    if (match) return match[1];
    
    return null;
  }

  // 提取价格数字
  function extractPrice(text) {
    if (!text) return 0;
    const match = text.match(/[\d,.]+/);
    return match ? parseFloat(match[0].replace(',', '')) : 0;
  }

  // ==================== 采集提交 ====================
  async function collectProduct(productData) {
    if (!currentEcomCode) {
      showNotification('请先设置关联商品', 'error');
      return;
    }

    const data = {
      ...productData,
      ecom_code: currentEcomCode,
      platform: '1688',
      collected_at: new Date().toISOString()
    };

    try {
      showNotification('正在采集...', 'loading');

      // 发送到本地API
      const response = await fetch(CONFIG.API_URL, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
      });

      if (response.ok) {
        showNotification('采集成功!', 'success');
        // 存储到本地
        chrome.storage.local.get(['collectedProducts'], (result) => {
          const collected = result.collectedProducts || [];
          collected.push(data);
          chrome.storage.local.set({ collectedProducts: collected });
        });
      } else {
        const error = await response.json();
        showNotification(`采集失败: ${error.detail}`, 'error');
      }
    } catch (e) {
      console.error('[EcomAgent] 采集失败:', e);
      showNotification('采集失败，已保存到本地', 'warning');
      
      // 网络失败时存到本地
      chrome.storage.local.get(['pendingProducts'], (result) => {
        const pending = result.pendingProducts || [];
        pending.push(data);
        chrome.storage.local.set({ pendingProducts: pending });
      });
    }
  }

  // ==================== 通知提示 ====================
  function showNotification(message, type) {
    const notification = document.createElement('div');
    notification.className = `ecomagent-notification ecomagent-${type}`;
    notification.textContent = message;
    document.body.appendChild(notification);

    setTimeout(() => {
      notification.classList.add('ecomagent-fade-out');
      setTimeout(() => notification.remove(), 300);
    }, 2000);
  }

  // ==================== 启动 ====================
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }

})();
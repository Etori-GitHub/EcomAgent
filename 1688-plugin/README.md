# 1688 货源采集插件

Chrome 浏览器插件，用于在 1688 页面采集货源信息，关联 EcomAgent 商品。

## 功能

- **悬停采集**: 鼠标悬停 1688 商品卡片时自动弹出采集窗口
- **关联商品**: 将 1688 货源与 EcomAgent 商品（ecom_code）绑定
- **离线存储**: 服务离线时自动保存到本地，稍后同步
- **状态指示**: 页面右上角显示当前关联的商品编码

## 安装

1. 打开 Chrome，访问 `chrome://extensions/`
2. 开启右上角「开发者模式」
3. 点击「加载已解压的扩展程序」
4. 选择 `1688-plugin` 文件夹
5. 插件图标出现在浏览器工具栏

## 使用方法

### 方式一：从 EcomAgent 跳转（推荐）

1. 在 EcomAgent 商品页面点击「找货源」按钮
2. 系统跳转到 1688 搜索页，URL 带 `ecom_code` 参数
3. 插件自动识别来源商品
4. 鼠标悬停商品卡片 → 确认采集

### 方式二：手动设置

1. 点击插件图标打开弹窗
2. 在「手动设置商品编码」输入框填入 ecom_code（如 ECAM000001）
3. 点击「设置」按钮
4. 在 1688 页面悬停采集

## 数据存储

- **本地 API**: `http://127.0.0.1:8000/api/sourcing`
- **数据库**: `EcomAgent/data/sourcing.db`
- **离线缓存**: Chrome Storage Local

## API 接口

| 方法 | 路径 | 说明 |
|------|------|------|
| POST | `/api/sourcing` | 添加货源 |
| GET | `/api/sourcing/{ecom_code}` | 获取商品关联货源 |
| GET | `/api/sourcing` | 获取所有货源 |
| DELETE | `/api/sourcing/{ecom_code}/{offer_id}` | 删除货源 |

## 目录结构

```
1688-plugin/
├── manifest.json      # 插件配置
├── content.js         # 页面注入脚本
├── content.css        # 样式
├── background.js      # 后台服务
├── popup.html         # 弹窗页面
├── popup.js           # 弹窗脚本
├── icons/             # 图标
│   ├── icon16.png
│   ├── icon48.png
│   └── icon128.png
│   └── generate_icons.py
└── README.md          # 本文件
```

## 注意事项

1. **EcomAgent 服务必须启动**: 采集数据发送到本地 API，需要先运行 EcomAgent
2. **1688 页面结构变化**: 如果采集失败，可能需要更新 `content.js` 中的选择器
3. **Chrome 权限**: 插件需要 `storage` 和 `activeTab` 权限

## 待优化

- [ ] 支持批量采集（选多个商品一起采集）
- [ ] 支持采集店铺信息（店铺评分、销量等）
- [ ] 支持导出货源数据为 CSV
- [ ] 在 EcomAgent 商品详情页显示关联货源

---

**版本**: 1.0.0  
**更新日期**: 2026-05-27
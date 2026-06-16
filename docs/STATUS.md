# EcomAgent 当前开发状态

记录正在开发但未完成的功能、方案设计和待决策事项。

---

## 开发规划（2026-06-16 更新）

### Phase 1：修复已知 Bug ✅ 已完成
- ✅ 商品趋势页面 XY 轴标签不显示
- ✅ 鼠标悬停 Tooltip 不显示
- ✅ Amazon/TikTok 商品默认指标适配
- ✅ API 字段兼容性修复（timestamp → created_at）

### Phase 2：生图/生视频/详情页功能 ⏳ 待开发
- [ ] 生图功能（商品主图生成/优化）
- [ ] 生视频功能（商品视频生成）
- [ ] 商品详情展示页生成

### Phase 3：TikTok 商品自动填充 ⏳ 待开发
- [ ] 自动填充 TikTok 商品信息
- [ ] 依赖 Phase 2 的生资源功能

### Phase 4：跨平台兼容 ⏳ 待开发
- [ ] Mac/Windows 双端适配
- [ ] 启动脚本、路径、依赖兼容

---

## 待决策事项

### Phase 2 技术选型

**生图/生视频 API**：
- 待确认：使用哪个服务？
  - OpenAI DALL-E
  - Midjourney
  - Stable Diffusion
  - 其他

**详情展示页**：
- 待确认：具体形式？
  - TikTok 商品详情页 HTML 预览？
  - 商品描述文案生成？
  - 其他

### Phase 3 自动化方案

**TikTok 自动填充**：
- 待确认：技术方案？
  - CDP 自动化（类似现有 TikTok 上传功能）
  - API 接口（如有）
  - 其他

---

## 已解决问题

### 2026-06-16 趋势图表修复

**问题**：趋势页面图表不显示

**原因**：
1. API 查询了不存在的字段（search_keyword, timestamp）
2. Amazon 商品没有 sales_count，默认指标选择错误
3. Tooltip 状态更新后未触发重新渲染

**解决方案**：
1. API 字段兼容：timestamp → created_at（Amazon/TikTok）
2. 前端动态选择默认指标：Amazon 默认显示排名，TikTok 默认显示销量
3. Tooltip 添加 requestUpdate() 强制刷新
4. XY 轴标签字体增大到 11px，颜色改为 #aaa

## 待决策事项

### Phase 2 技术选型

**生图/生视频 API**：
- 待确认：使用哪个服务？
  - OpenAI DALL-E
  - Midjourney
  - Stable Diffusion
  - 其他

**详情展示页**：
- 待确认：具体形式？
  - TikTok 商品详情页 HTML 预览？
  - 商品描述文案生成？
  - 其他

### Phase 3 自动化方案

**TikTok 自动填充**：
- 待确认：技术方案？
  - CDP 自动化（类似现有 TikTok 上传功能）
  - API 接口（如有）
  - 其他

---
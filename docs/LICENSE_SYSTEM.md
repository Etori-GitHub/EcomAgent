# EcomAgent 授权系统设计方案

> 创建时间：2026-06-29
> 最后更新：2026-06-29
> 状态：讨论中，待确认

---

## 1. 概述

EcomAgent 授权控制系统，用于控制软件使用权限、防止盗版、管理客户授权。

### 核心目标

- **CDK 管理**：生成、分发、过期管理
- **机器绑定**：一个 CDK 只能激活一台机器
- **有效期控制**：订阅制授权
- **设备迁移**：支持换机重新激活

### 系统架构

本系统分为**四大部分**：

```
┌─────────────────────────────────────────────────────────────────┐
│                        服务端（API Only）                        │
│                                                                 │
│  公开 API（客户端/小程序调用）：                                  │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │  POST /api/license/activate     # 激活                  │   │
│  │  POST /api/license/verify       # 校验                  │   │
│  │  POST /api/license/unbind       # 解绑                  │   │
│  │  GET  /api/license/status       # 查询状态              │   │
│  │  POST /api/license/reset        # 重置 CDK              │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
│  管理 API（本地管理工具调用，需要管理员密钥）：                    │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │  POST /api/admin/cdk/generate       # 生成 CDK          │   │
│  │  POST /api/admin/cdk/batch-generate # 批量生成          │   │
│  │  POST /api/admin/cdk/revoke         # 作废 CDK          │   │
│  │  GET  /api/admin/cdk/list           # CDK 列表          │   │
│  │  POST /api/admin/license/generate   # 生成离线 License  │   │
│  │  GET  /api/admin/analytics/verify   # 验证记录          │   │
│  │  GET  /api/admin/analytics/suspicious # 可疑记录        │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
         ↑              ↑                    ↑
         │              │                    │
┌─────────────────┐ ┌─────────────────┐ ┌─────────────────────┐
│   EcomAgent     │ │   微信小程序     │ │   本地管理工具      │
│   客户端        │ │   用户端        │ │   （管理员专用）    │
│                 │ │                 │ │                     │
│ 调用公开 API    │ │ 调用公开 API    │ │ 调用管理 API        │
│                 │ │                 │ │ 带管理员密钥        │
└─────────────────┘ └─────────────────┘ └─────────────────────┘
```

### 各部分职责

| 组件 | 技术栈 | 职责 | 依赖域名 |
|------|--------|------|----------|
| **EcomAgent 客户端** | Python | 软件本体，调用公开 API 进行激活和校验 | 否，IP 直连即可 |
| **微信小程序** | 微信小程序 | 用户购买、管理 CDK | 否，IP 直连即可 |
| **服务端** | Java (Spring Boot) | 提供 API 服务，无管理后台 | 否，IP 直连即可 |
| **本地管理工具** | Python | 管理员专用，生成 CDK、查看记录 | 否，IP 直连即可 |

**优势**：四部分均不依赖域名，IP 直连即可，降低部署成本。

---

## 2. 核心流程

### 2.1 购买与获取

```
微信小程序 → 购买 CDK → 获得 CDK 码
```

用户通过微信小程序购买 CDK（量子密钥/数字卡券），购买成功后获得 CDK 码，支持查看、加购、续期、重置。

### 2.2 设备激活

```
首次使用 → 输入 CDK → 本地生成机器码 → 上传激活 → 服务器绑定
```

- 系统自动获取机器码和设备信息
- 用户在激活界面输入 CDK
- 本地上传机器码和 CDK 到服务器
- 服务器记录激活：机器码与 CDK 的绑定关系

### 2.3 功能校验

```
点击功能 → 发送验证请求 → 服务器校验 → 通过/拒绝
```

用户使用 EcomAgent 功能时：
1. 本地向服务器发送验证请求（加密的数据包）
2. 数据包包含：机器码、CDK、时间戳、设备信息等
3. 服务器验证服务器端记录的绑定关系是否匹配
4. 验证成功：返回"允许执行"，功能正常使用
5. 验证失败：返回"禁止执行"，功能被锁定

### 2.4 设备迁移

```
新设备输入 CDK → 上传新机器码 → 服务器更新绑定 → 旧设备被锁定
```

- 同样流程：新机器码 + CDK 上传服务器
- 服务器更新绑定关系：机器码从旧的变为新的
- 旧设备下次验证时会发现不匹配，被锁定
- 新设备可以正常使用，实现无感切换设备

### 2.5 授权管理（微信小程序）

用户登录小程序后可以：
- 查看已购 CDK 状态
- 查看当前绑定的机器码
- 查看授权有效期（固定365天）
- 进行加购
- 取消激活（取消当前设备的激活，记录状态）
- 续期
- CDK 泄露后重置（作废旧的，生成新的）

---

## 3. 授权类型

| 类型 | 说明 | 离线支持 | 使用场景 |
|------|------|----------|----------|
| **在线 CDK** | 标准授权，每次功能调用时验证 | ❌ 无 | 普通用户 |
| **离线 License** | 特殊授权，本地文件验证，无需联网 | ✅ 有 | 开发环境、特殊客户 |

### 离线 License 场景

- 开发环境（自己使用）
- 特殊客户（内网环境、一次性买断等）
- 服务器后台生成，手动部署到客户机器

**离线 License 设计**：

```
文件格式：JSON + RSA 签名
存放位置：EcomAgent/config/license.lic

内容：
{
    "license_id": "OFFLINE-XXXX",
    "type": "offline",
    "machine_id": "xxx",           # 可为空，表示不限设备
    "expires_at": "2099-12-31",    # 有效期
    "features": ["*"],             # 允许的功能，* 表示全部
    "issued_to": "开发环境",        # 备注
    "issued_at": "2026-06-29",
    "signature": "RSA签名..."      # 防篡改
}

客户端验证：
1. 读取 license.lic 文件
2. 验证 RSA 签名（公钥内置在客户端）
3. 验证有效期
4. 验证机器码（如有）
5. 全部通过 → 功能放行
```

---

## 4. 校验触发点

用户执行以下功能时触发校验：

| 功能 | 触发时机 | 功能标识 |
|------|----------|----------|
| 刷新类目 | 点击刷新按钮 | `refresh_categories` |
| 抓数据 | 开始抓取前 | `fetch_data` |
| 1688找货源 | 点击跳转前 | `source_1688` |
| 采集货源 | 开始采集前 | `collect_source` |
| 生成9张展示图 | 开始生成前 | `gen_images` |
| 生成视频 | 开始生成前 | `gen_video` |
| 生成详情图 | 开始生成前 | `gen_detail` |

**校验逻辑**：

```
1. 检查本地是否有离线 License → 有则直接通过
2. 无离线 License → 向服务器发送验证请求
3. 服务器验证通过 → 允许执行
4. 服务器验证失败或网络错误 → 拒绝执行，提示用户
```

**注意**：EcomAgent 所有功能都依赖网络，用户如果网络不稳定根本没法用，因此不做离线容忍期。离线场景仅通过离线 License 支持。

---

## 5. 安全设计

### 5.1 加密通信

- 所有校验请求使用 HTTPS 加密传输
- 避免明文传输 CDK 和机器码
- 防止请求被监听或篡改

### 5.2 请求签名

```python
# 客户端生成签名
timestamp = int(time.time())
data = f"{cdk}|{machine_id}|{timestamp}|{feature_code}"
sign = HMAC-SHA256(secret_key, data)

# 请求体
{
    "cdk": "ECOM-XXXX-XXXX-XXXX",
    "machine_id": "xxx",
    "timestamp": 1719652800,
    "feature": "fetch_data",      # 触发的功能标识
    "sign": "abc123...",
    "device_info": {               # 辅助分析数据
        "os": "Windows 10",
        "cpu": "Intel i7-12700",
        "hostname": "USER-PC",
        ...
    }
}
```

**服务端验证**：

1. 检查 timestamp 是否在 ±5 分钟内（防重放）
2. 用同样的算法生成签名，对比是否一致
3. 验证 CDK 状态（有效/过期/作废）
4. 验证机器码绑定关系
5. 记录请求日志（用于分析异常）

### 5.3 限流策略

```
每个 CDK：30 次/分钟
全局 IP：不做限制（避免误伤同一办公室多设备场景）
```

按 CDK 区分身份，不按 IP 限制。

### 5.4 异常检测

记录每次请求的：
- CDK
- 机器码
- IP
- 设备信息（OS、CPU、主机名等）
- 时间戳
- 功能类型

**分析规则**（后台定期跑，不实时拦截）：

1. 同一 CDK 不同机器码请求 → 标记可疑
2. 同一机器码匹配多个 CDK → 标记可疑
3. 设备信息与历史不一致 → 标记可疑
4. 短时间高频请求 → 标记可疑

管理员可查看可疑列表，决定是否手动处理。

### 5.5 CDK 重置机制

用户可在微信小程序随意重置 CDK：

- 重置后旧 CDK 立即作废
- 生成新的 CDK
- 用户需重新绑定设备

---

## 6. 技术选型

### 6.1 客户端（EcomAgent）

```
语言：Python（现有项目）
核心模块：
- auth/license.py          # 离线 License 验证
- auth/online_verify.py    # 在线验证
- auth/device.py           # 机器码生成
- auth/crypto.py           # 签名/加密工具
```

### 6.2 服务端（Java）

```
框架：Spring Boot
数据库：MySQL（考虑到后续可能扩展）
特点：纯 API 服务，无管理后台界面

公开 API（客户端/小程序调用）：
- POST /api/license/activate     # 激活
- POST /api/license/verify       # 校验
- POST /api/license/unbind       # 解绑
- GET  /api/license/status       # 查询状态
- POST /api/license/reset        # 重置 CDK

管理 API（本地管理工具调用，需管理员密钥）：
- POST /api/admin/cdk/generate       # 生成 CDK
- POST /api/admin/cdk/batch-generate # 批量生成 CDK
- POST /api/admin/cdk/revoke         # 作废 CDK
- GET  /api/admin/cdk/list           # CDK 列表
- POST /api/admin/license/generate   # 生成离线 License
- GET  /api/admin/analytics/verify    # 验证记录
- GET  /api/admin/analytics/suspicious # 可疑列表
```

### 6.3 本地管理工具（Python）

```
形态：命令行脚本（第一阶段）+ 可选 Web 页面（第二阶段）
用途：管理员专用，生成 CDK、查看记录、生成离线 License

命令行示例：
- python admin.py generate --count 10 --type yearly   # 生成 10 个年卡 CDK
- python admin.py list --status active                 # 查看有效 CDK
- python admin.py license --machine-id xxx             # 生成离线 License
- python admin.py suspicious                            # 查看可疑记录
- python admin.py revoke --cdk ECOM-XXXX               # 作废 CDK

安全机制：
- 请求时生成签名：sign = HMAC-SHA256(admin_key, timestamp + action)
- 请求头：
  X-Admin-Timestamp: 1719652800
  X-Admin-Sign: xxx
- 服务端验证签名 + 时间戳（5分钟内有效）
```

### 6.4 微信小程序

```
功能：
- 用户登录
- 查看已购 CDK
- 查看授权状态、有效期、绑定机器
- 取消激活
- 重置 CDK（作废旧码，生成新码）
- 加购、续期
```

---

## 7. 数据库设计

### 7.1 CDK 表

```sql
CREATE TABLE cdkeys (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    cdk VARCHAR(32) UNIQUE NOT NULL,       -- CDK 码
    type VARCHAR(20) NOT NULL,             -- 类型：monthly/yearly/lifetime
    status VARCHAR(20) NOT NULL,            -- 状态：unused/active/expired/revoked
    created_at DATETIME NOT NULL,
    expires_at DATETIME,                   -- 过期时间
    reset_count INT DEFAULT 0,             -- 重置次数
    last_reset_at DATETIME,                -- 上次重置时间
    remark VARCHAR(255)                    -- 备注
);
```

### 7.2 激活记录表

```sql
CREATE TABLE activations (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    cdk VARCHAR(32) NOT NULL,
    machine_id VARCHAR(128) NOT NULL,      -- 机器码
    device_info TEXT,                      -- 设备信息 JSON
    ip VARCHAR(45),                         -- 激活时 IP
    activated_at DATETIME NOT NULL,
    last_verify DATETIME,                  -- 最后验证时间
    unbound_at DATETIME,                   -- 解绑时间（NULL 表示当前有效）
    FOREIGN KEY (cdk) REFERENCES cdkeys(cdk)
);
```

### 7.3 验证日志表

```sql
CREATE TABLE verify_logs (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    cdk VARCHAR(32) NOT NULL,
    machine_id VARCHAR(128) NOT NULL,
    feature VARCHAR(50) NOT NULL,          -- 功能标识
    ip VARCHAR(45),
    device_info TEXT,                       -- 设备信息 JSON
    result VARCHAR(20) NOT NULL,            -- success/fail
    reason VARCHAR(100),                    -- 失败原因
    created_at DATETIME NOT NULL,
    INDEX idx_cdk (cdk),
    INDEX idx_created_at (created_at)
);
```

---

## 8. 服务器配置

### 8.1 性能要求

- 支持 100-500 个用户同时在线
- 每分钟校验请求：用户 x 5 次 = 500 次/分钟
- 处理峰值：约 8.3 QPS（每秒）

### 8.2 推荐配置

```
CPU：2 vCPU
内存：2 GiB
系统盘：40 GiB
公网流量：无固定流量
峰值带宽：200 Mbps
```

### 8.3 部署方式

```
镜像：宝塔 Linux
数据库：MySQL
验证服务：Spring Boot 后端 API
```

---

## 9. 域名与 HTTPS

由于四部分均不依赖域名，可使用 IP 直连方式访问服务端 API。

**可选方案**：如需 HTTPS 加密，可使用免费域名 + Let's Encrypt

```
免费域名：DuckDNS（ecomagent.duckdns.org）
SSL 证书：Let's Encrypt（免费）
配置：Nginx 反向代理 + HTTPS
```

---

## 10. 待确认问题

> 以下问题需要在开发前确认

1. **服务端部署** - 是否有现成的 Java 服务器/运维经验？还是需要从零搭建？

2. **微信小程序** - 是已有小程序要接入，还是新建一个？

3. **离线 License 的机器码限制** - 是固定绑定某台机器，还是不限设备？

4. **CDK 类型** - 月卡/年卡/永久？是否支持多设备（如 3 设备版）？

---

## 11. 更新日志

| 日期 | 内容 |
|------|------|
| 2026-06-29 | 初始方案，整理核心流程、安全设计、技术选型 |
| 2026-06-29 | 确定四大部分架构：客户端、小程序、服务端、本地管理工具 |
| 2026-06-29 | 管理后台改为本地管理工具，更安全且不依赖域名 |
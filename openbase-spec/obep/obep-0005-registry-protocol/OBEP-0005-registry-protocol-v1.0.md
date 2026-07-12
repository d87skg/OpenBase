
---

```markdown
---
OBEP: 0005
Title: Registry Protocol v1.0
Status: Frozen
Version: 1.0.0
Date: 2026-07-05
Authors: OpenBase Specification Committee
Obsoletes: None
---

# OBEP-0005: Registry Protocol v1.0

## 1. 前言

### 1.1 目的

本规范定义 OpenBase 注册表协议（Registry Protocol），即 Runtime 注册、证据提交、证书查询与信任分数获取的标准接口。注册表是 OpenBase 生态系统的**核心控制平面**，负责维护所有 Runtime、证据、证书和信任状态的全局视图。

### 1.2 范围

本规范涵盖：

- Registry 的核心职责与架构
- Runtime 注册与生命周期管理
- 证据提交与查询
- 证书颁发与查询
- 信任分数查询
- 注册表查询 API
- 事件通知机制
- 安全与认证要求

本规范不涵盖：

- 证据的结构与验证（参见 OBEP-0001 Evidence Schema）
- 重放协议（参见 OBEP-0002 Replay Protocol）
- 信任模型（参见 OBEP-0003 Trust Model）
- 证书结构（参见 OBEP-0004 Certificate Schema）

### 1.3 符合性关键词

本规范使用 RFC 2119 关键词：

- **MUST**：必须遵守，否则不符合标准
- **MUST NOT**：禁止行为
- **SHOULD**：建议遵守
- **SHOULD NOT**：不建议行为
- **MAY**：可选行为

## 2. 核心概念

### 2.1 Registry 定义

Registry（注册表）是 OpenBase 生态系统的**全局状态存储与控制平面**。它维护以下核心数据：

1. **Runtime Registry**：所有已注册 Runtime 的元数据
2. **Evidence Registry**：所有已提交的证据索引
3. **Certificate Registry**：所有已颁发的证书
4. **Trust Registry**：所有 Runtime 的信任状态
5. **Event Log**：所有系统事件的审计日志

### 2.2 Registry 职责

| 职责 | 描述 | 优先级 |
| :--- | :--- | :--- |
| Runtime 注册 | 接受 Runtime 注册请求，分配唯一标识符 | P0 |
| 证据存储 | 接收并索引证据，支持查询 | P0 |
| 证书管理 | 颁发、查询、撤销证书 | P0 |
| 信任分数计算 | 基于证据和证书计算信任分数 | P0 |
| 事件通知 | 广播状态变更事件 | P1 |
| 审计日志 | 记录所有操作 | P1 |
| 兼容性检查 | 验证 Runtime 版本兼容性 | P2 |

### 2.3 Registry 架构

```text
┌─────────────────────────────────────────────────────────────────┐
│                      Registry API Layer                        │
├─────────────────────────────────────────────────────────────────┤
│  ┌───────────┐  ┌───────────┐  ┌───────────┐  ┌───────────┐  │
│  │ Runtime   │  │ Evidence  │  │ Certificate│  │ Trust     │  │
│  │ API       │  │ API       │  │ API       │  │ API       │  │
│  └───────────┘  └───────────┘  └───────────┘  └───────────┘  │
├─────────────────────────────────────────────────────────────────┤
│                         Service Layer                         │
├─────────────────────────────────────────────────────────────────┤
│  ┌───────────┐  ┌───────────┐  ┌───────────┐  ┌───────────┐  │
│  │ Runtime   │  │ Evidence  │  │ Certificate│  │ Trust     │  │
│  │ Service   │  │ Service   │  │ Service   │  │ Service   │  │
│  └───────────┘  └───────────┘  └───────────┘  └───────────┘  │
├─────────────────────────────────────────────────────────────────┤
│                         Storage Layer                         │
├─────────────────────────────────────────────────────────────────┤
│  ┌───────────┐  ┌───────────┐  ┌───────────┐  ┌───────────┐  │
│  │ Runtime   │  │ Evidence  │  │ Certificate│  │ Trust     │  │
│  │ Store     │  │ Store     │  │ Store     │  │ Store     │  │
│  └───────────┘  └───────────┘  └───────────┘  └───────────┘  │
└─────────────────────────────────────────────────────────────────┘
```

## 3. Runtime 注册

### 3.1 注册请求

Runtime **MUST** 在启动后向 Registry 注册。

**请求格式**：

```json
POST /runtimes/register
{
  "name": "OpenClaw",
  "version": "1.0.0",
  "vendor": "OpenBase",
  "runtime_class": "REFERENCE",
  "capabilities": ["execution", "evidence", "replay", "verification", "determinism", "certification"],
  "description": "OpenBase Reference Runtime",
  "metadata": {
    "repository": "https://github.com/openbase-io/openclaw",
    "language": "python",
    "license": "Apache-2.0"
  }
}
```

| 字段 | 类型 | 约束 | 描述 |
| :--- | :--- | :--- | :--- |
| `name` | string | 非空，全局唯一 | Runtime 名称 |
| `version` | string | 语义化版本 | 版本号 |
| `vendor` | string | 非空 | 供应商名称 |
| `runtime_class` | string | CORE/STANDARD/ENTERPRISE/REFERENCE | Runtime 类型 |
| `capabilities` | array | 必须包含至少一个能力 | 支持的能力列表 |
| `description` | string | 可选 | 描述 |
| `metadata` | object | 可选 | 额外元数据 |

**能力注册表**：

| 能力 | 描述 | 必需 |
| :--- | :--- | :--- |
| `execution` | 支持 Agent 执行 | ✅ 是 |
| `evidence` | 支持证据生成 | ✅ 是 |
| `replay` | 支持重放 | ⚠️ 可选 |
| `verification` | 支持验证 | ⚠️ 可选 |
| `determinism` | 支持确定性分析 | ⚠️ 可选 |
| `certification` | 支持认证 | ⚠️ 可选 |
| `reality_graph` | 支持现实图 | ⚠️ 可选 |
| `semantic` | 支持语义层 | ⚠️ 可选 |

### 3.2 注册响应

```json
{
  "runtime_id": "runtime-7f3a9b2c",
  "name": "OpenClaw",
  "version": "1.0.0",
  "vendor": "OpenBase",
  "status": "ACTIVE",
  "runtime_class": "REFERENCE",
  "capabilities": ["execution", "evidence", "replay", "verification", "determinism", "certification"],
  "registered_at": "2026-07-05T10:00:00.000Z",
  "updated_at": "2026-07-05T10:00:00.000Z"
}
```

### 3.3 Runtime 状态

| 状态 | 描述 |
| :--- | :--- |
| `ACTIVE` | Runtime 正常运行 |
| `INACTIVE` | Runtime 已关闭 |
| `SUSPENDED` | Runtime 被暂停 |
| `DEPRECATED` | Runtime 已弃用 |
| `REVOKED` | Runtime 已被撤销 |

### 3.4 Runtime 更新

Runtime **SHOULD** 在以下情况下更新注册信息：

1. 版本升级
2. 能力变更
3. 状态变更

**请求格式**：

```json
PUT /runtimes/{runtime_id}
{
  "version": "1.1.0",
  "status": "ACTIVE",
  "capabilities": ["execution", "evidence", "replay", "verification", "determinism", "certification", "reality_graph"]
}
```

## 4. 证据管理

### 4.1 证据提交

**请求格式**：

```json
POST /evidence
{
  "runtime_id": "runtime-7f3a9b2c",
  "evidence": {
    "evidence_id": "evid-00000001",
    "spec_version": "1.0",
    "event_type": "LLM_CALL",
    "timestamp": "2026-07-05T10:00:00.000Z",
    "causal": {"parent_id": null, "vector_clock": {"node-a": 1}},
    "action": {"input": {"prompt": "Hello"}, "output": null},
    "proof": {"hash": "sha256:...", "signature": "ed25519:..."}
  }
}
```

**约束**：

- `evidence` **MUST** 符合 OBEP-0001 定义的 Evidence Schema。
- `runtime_id` **MUST** 已注册。

### 4.2 证据查询

**按证据 ID 查询**：

```json
GET /evidence/{evidence_id}
```

**按 Execution ID 查询**：

```json
GET /evidence/execution/{execution_id}
```

**按 Runtime ID 查询**：

```json
GET /evidence/runtime/{runtime_id}
```

**按时间范围查询**：

```json
GET /evidence?from=2026-07-01T00:00:00Z&to=2026-07-05T23:59:59Z
```

### 4.3 证据批量提交

**SHOULD** 支持批量提交以提高性能：

```json
POST /evidence/batch
{
  "runtime_id": "runtime-7f3a9b2c",
  "evidences": [
    {"evidence_id": "evid-00000001", ...},
    {"evidence_id": "evid-00000002", ...},
    {"evidence_id": "evid-00000003", ...}
  ]
}
```

## 5. 证书管理

### 5.1 证书颁发

**请求格式**：

```json
POST /certificates/issue
{
  "runtime_id": "runtime-7f3a9b2c",
  "runtime_name": "OpenClaw",
  "level": "GOLD",
  "trust_score": 0.89,
  "verification_summary": {
    "conformance": "PASS",
    "replay": "PASS",
    "determinism": "CAUSAL",
    "evidence_count": 1234
  }
}
```

**颁发规则**：
- `trust_score` **MUST** 达到对应等级阈值（参见 OBEP-0004）。
- `runtime_id` **MUST** 已注册。

### 5.2 证书查询

**按证书 ID 查询**：

```json
GET /certificates/{certificate_id}
```

**按 Runtime ID 查询**：

```json
GET /certificates/runtime/{runtime_id}
```

**获取最新证书**：

```json
GET /certificates/runtime/{runtime_id}/latest
```

**列出活跃证书**：

```json
GET /certificates/active
```

### 5.3 证书撤销

**请求格式**：

```json
POST /certificates/{certificate_id}/revoke
{
  "reason": "Trust score dropped below threshold"
}
```

**响应**：

```json
{
  "certificate_id": "cert-7f3a9b2c",
  "status": "REVOKED",
  "revoked_at": "2026-07-05T10:00:00.000Z",
  "reason": "Trust score dropped below threshold"
}
```

## 6. 信任分数管理

### 6.1 查询信任分数

**按 Runtime ID 查询**：

```json
GET /trust/{runtime_id}
```

**响应**：

```json
{
  "runtime_id": "runtime-7f3a9b2c",
  "runtime_name": "OpenClaw",
  "trust_score": 0.87,
  "trust_state": "HIGH",
  "evidence_count": 1234,
  "certificate_count": 2,
  "conflict_count": 0,
  "last_updated": "2026-07-05T10:00:00.000Z"
}
```

### 6.2 信任排名

```json
GET /trust/ranking?limit=10
```

**响应**：

```json
[
  {
    "runtime_id": "runtime-7f3a9b2c",
    "runtime_name": "OpenClaw",
    "trust_score": 0.95,
    "level": "PLATINUM"
  },
  {
    "runtime_id": "runtime-8a4b1c3d",
    "runtime_name": "Demo Runtime",
    "trust_score": 0.82,
    "level": "SILVER"
  }
]
```

### 6.3 手动刷新信任分数

```json
POST /trust/{runtime_id}/refresh
```

## 7. 事件通知

### 7.1 事件类型

| 事件类型 | 描述 | 触发条件 |
| :--- | :--- | :--- |
| `RUNTIME_REGISTERED` | Runtime 注册 | 新 Runtime 注册 |
| `RUNTIME_UPDATED` | Runtime 更新 | Runtime 信息变更 |
| `EVIDENCE_SUBMITTED` | 证据提交 | 新证据入库 |
| `CERTIFICATE_ISSUED` | 证书颁发 | 新证书颁发 |
| `CERTIFICATE_REVOKED` | 证书撤销 | 证书被撤销 |
| `TRUST_UPDATED` | 信任分数更新 | 信任分数变更 |

### 7.2 WebSocket 订阅

```json
{
  "type": "subscribe",
  "events": ["EVIDENCE_SUBMITTED", "TRUST_UPDATED"]
}
```

### 7.3 事件推送格式

```json
{
  "event_id": "event-7f3a9b2c",
  "event_type": "TRUST_UPDATED",
  "timestamp": "2026-07-05T10:00:00.000Z",
  "payload": {
    "runtime_id": "runtime-7f3a9b2c",
    "trust_score": 0.87,
    "previous_score": 0.85
  }
}
```

## 8. 安全与认证

### 8.1 API 认证

Registry API **SHOULD** 支持以下认证方式：

| 认证方式 | 描述 | 适用场景 |
| :--- | :--- | :--- |
| API Key | 静态 API 密钥 | 内部服务调用 |
| JWT | JSON Web Token | 用户认证 |
| mTLS | 双向 TLS 认证 | 高安全场景 |

### 8.2 访问控制

| 操作 | 所需权限 | 描述 |
| :--- | :--- | :--- |
| 注册 Runtime | `runtime:register` | 注册新 Runtime |
| 提交证据 | `evidence:submit` | 提交证据 |
| 查询证据 | `evidence:read` | 读取证据 |
| 颁发证书 | `certificate:issue` | 颁发证书 |
| 撤销证书 | `certificate:revoke` | 撤销证书 |
| 查询信任 | `trust:read` | 读取信任分数 |
| 管理 Runtime | `runtime:admin` | 管理 Runtime |

### 8.3 速率限制

**SHOULD** 实施速率限制以防止滥用：

| 端点 | 限制 | 窗口 |
| :--- | :--- | :--- |
| POST /evidence | 1000 次/分钟 | 1 分钟 |
| GET /evidence | 100 次/分钟 | 1 分钟 |
| POST /runtimes/register | 10 次/分钟 | 1 分钟 |
| GET /trust | 100 次/分钟 | 1 分钟 |

## 9. 兼容性

### 9.1 版本兼容性

Registry **MUST** 支持以下兼容性策略：

| 策略 | 描述 |
| :--- | :--- |
| 向后兼容 | 新版本 Registry 必须支持旧版本 Runtime |
| 向前兼容 | 旧版本 Registry 应尽可能支持新版本 Runtime |
| 版本协商 | 支持 API 版本协商 |

### 9.2 版本声明

Runtime **SHOULD** 在请求头中声明支持的版本：

```
X-OpenBase-Version: 1.0
Accept-Version: 1.0
```

## 10. 示例

### 10.1 完整注册流程

```bash
# 1. 注册 Runtime
curl -X POST http://registry.openbase.io/runtimes/register \
  -H "Content-Type: application/json" \
  -d '{"name":"OpenClaw","version":"1.0.0","vendor":"OpenBase","runtime_class":"REFERENCE","capabilities":["execution","evidence","replay","verification","determinism","certification"]}'

# 2. 提交证据
curl -X POST http://registry.openbase.io/evidence \
  -H "Content-Type: application/json" \
  -d '{"runtime_id":"runtime-7f3a9b2c","evidence":{...}}'

# 3. 查询信任分数
curl -X GET http://registry.openbase.io/trust/runtime-7f3a9b2c

# 4. 颁发证书
curl -X POST http://registry.openbase.io/certificates/issue \
  -H "Content-Type: application/json" \
  -d '{"runtime_id":"runtime-7f3a9b2c","runtime_name":"OpenClaw","level":"GOLD","trust_score":0.89}'

# 5. 查询证书
curl -X GET http://registry.openbase.io/certificates/runtime-7f3a9b2c/latest
```

### 10.2 WebSocket 事件订阅

```javascript
const ws = new WebSocket('ws://registry.openbase.io/events');
ws.onopen = () => {
  ws.send(JSON.stringify({
    type: 'subscribe',
    events: ['EVIDENCE_SUBMITTED', 'TRUST_UPDATED']
  }));
};
ws.onmessage = (event) => {
  console.log(JSON.parse(event.data));
};
```

## 11. 参考

### 11.1 规范性引用

- RFC 2119 — Key words for use in RFCs to Indicate Requirement Levels
- RFC 3339 — Timestamp Format
- RFC 6455 — The WebSocket Protocol
- OBEP-0001 — Evidence Schema v1.0
- OBEP-0003 — Trust Model v1.0
- OBEP-0004 — Certificate Schema v1.0

### 11.2 信息性引用

- Kubernetes API Server Design
- etcd Key-Value Store
- OpenTelemetry Collector Architecture

## 12. 冻结声明

本规范已冻结为 v1.0，生效日期：2026-07-05。

任何变更必须通过 OBEP 流程进行，并保持向后兼容。

**冻结状态**：✅ 已冻结

**下次审查**：2027-07-05 或 严重安全漏洞发现时。

---

*本规范由 OpenBase Specification Committee 维护。*
```


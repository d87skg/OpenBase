
---

```markdown
---
OBEP: 0006
Title: Wire Protocol v1.0
Status: Frozen
Version: 1.0.0
Date: 2026-07-05
Authors: OpenBase Specification Committee
Obsoletes: None
---

# OBEP-0006: Wire Protocol v1.0

## 1. 前言

### 1.1 目的

本规范定义 OpenBase 线路协议（Wire Protocol），即 OpenBase 各组件之间进行网络通信的标准格式与规则。线路协议确保不同语言、不同运行时、不同实现之间的互操作性，是 OpenBase 生态系统的**通信基础层**。

### 1.2 范围

本规范涵盖：

- 传输层协议（Transport Protocol）
- 消息序列化格式（Serialization Format）
- 请求/响应结构
- 错误处理模型
- 流式通信模式
- 版本协商机制
- 安全传输要求

本规范不涵盖：

- 具体 API 端点定义（参见 OBEP-0005 Registry Protocol）
- 数据模型结构（参见 OBEP-0001、OBEP-0003、OBEP-0004）
- 认证与授权（参见 OBEP-0005 安全章节）

### 1.3 符合性关键词

本规范使用 RFC 2119 关键词：

- **MUST**：必须遵守，否则不符合标准
- **MUST NOT**：禁止行为
- **SHOULD**：建议遵守
- **SHOULD NOT**：不建议行为
- **MAY**：可选行为

## 2. 核心概念

### 2.1 协议分层

OpenBase Wire Protocol 采用分层设计，与 OSI 模型类似但面向应用层优化：

```text
┌─────────────────────────────────────────┐
│           应用语义层 (Application)       │
│    (Evidence, Trust, Certificate)       │
├─────────────────────────────────────────┤
│           消息层 (Message)              │
│   (请求/响应/事件/流式消息)              │
├─────────────────────────────────────────┤
│           序列化层 (Serialization)       │
│         (JSON / CBOR / Protobuf)        │
├─────────────────────────────────────────┤
│           传输层 (Transport)             │
│           (HTTP/2 / gRPC / WebSocket)   │
└─────────────────────────────────────────┘
```

### 2.2 传输协议要求

OpenBase Wire Protocol **MUST** 支持以下传输协议：

| 传输协议 | 用途 | 优先级 |
| :--- | :--- | :--- |
| HTTP/2 | REST API、远程调用 | **MUST** |
| gRPC | 高性能 RPC、流式通信 | **SHOULD** |
| WebSocket | 实时事件推送 | **SHOULD** |
| HTTP/1.1 | 兼容性回退 | **MAY** |

### 2.3 序列化格式要求

OpenBase Wire Protocol **MUST** 支持以下序列化格式：

| 格式 | 用途 | 优先级 |
| :--- | :--- | :--- |
| JSON | 人类可读、调试、简单场景 | **MUST** |
| CBOR | 二进制高效、小体积 | **SHOULD** |
| Protobuf | 高性能 RPC、跨语言 | **SHOULD** |
| MessagePack | 轻量级二进制 | **MAY** |

## 3. 消息结构

### 3.1 通用消息头

所有消息 **MUST** 包含以下头部字段：

```json
{
  "protocol": "openbase/v1.0",
  "message_id": "msg-7f3a9b2c",
  "timestamp": "2026-07-05T10:00:00.000Z",
  "version": "1.0",
  "type": "REQUEST | RESPONSE | EVENT | STREAM"
}
```

| 字段 | 类型 | 约束 | 描述 |
| :--- | :--- | :--- | :--- |
| `protocol` | string | 固定 `"openbase/v1.0"` | 协议版本标识 |
| `message_id` | string | 格式: `msg-{8位hex}` | 消息唯一标识符 |
| `timestamp` | string | RFC 3339 UTC 格式 | 消息生成时间 |
| `version` | string | 语义化版本 | 协议版本号 |
| `type` | string | REQUEST/RESPONSE/EVENT/STREAM | 消息类型 |

### 3.2 请求消息（Request）

```json
{
  "protocol": "openbase/v1.0",
  "message_id": "msg-7f3a9b2c",
  "timestamp": "2026-07-05T10:00:00.000Z",
  "version": "1.0",
  "type": "REQUEST",
  "method": "POST",
  "path": "/v1/evidence",
  "headers": {
    "content-type": "application/json",
    "accept": "application/json",
    "authorization": "Bearer <token>"
  },
  "body": {
    "runtime_id": "runtime-7f3a9b2c",
    "evidence": {...}
  }
}
```

| 字段 | 类型 | 约束 | 描述 |
| :--- | :--- | :--- | :--- |
| `method` | string | GET/POST/PUT/DELETE/PATCH | HTTP 方法 |
| `path` | string | 以 `/v{version}/` 开头 | 请求路径 |
| `headers` | object | 可选 | 请求头 |
| `body` | any | 可选 | 请求体 |

### 3.3 响应消息（Response）

```json
{
  "protocol": "openbase/v1.0",
  "message_id": "msg-7f3a9b2c",
  "timestamp": "2026-07-05T10:00:00.000Z",
  "version": "1.0",
  "type": "RESPONSE",
  "request_id": "msg-7f3a9b2c",
  "status_code": 200,
  "status_message": "OK",
  "headers": {
    "content-type": "application/json"
  },
  "body": {
    "runtime_id": "runtime-7f3a9b2c",
    "status": "ACTIVE"
  }
}
```

| 字段 | 类型 | 约束 | 描述 |
| :--- | :--- | :--- | :--- |
| `request_id` | string | 匹配对应的请求 ID | 请求 ID |
| `status_code` | integer | 标准 HTTP 状态码 | 状态码 |
| `status_message` | string | 标准 HTTP 状态消息 | 状态消息 |
| `headers` | object | 可选 | 响应头 |
| `body` | any | 可选 | 响应体 |

### 3.4 事件消息（Event）

```json
{
  "protocol": "openbase/v1.0",
  "message_id": "msg-7f3a9b2c",
  "timestamp": "2026-07-05T10:00:00.000Z",
  "version": "1.0",
  "type": "EVENT",
  "event_type": "TRUST_UPDATED",
  "source": "registry.openbase.io",
  "payload": {
    "runtime_id": "runtime-7f3a9b2c",
    "trust_score": 0.87,
    "previous_score": 0.85
  }
}
```

| 字段 | 类型 | 约束 | 描述 |
| :--- | :--- | :--- | :--- |
| `event_type` | string | 必须注册 | 事件类型 |
| `source` | string | 可选 | 事件来源 |
| `payload` | object | 可选 | 事件数据 |

### 3.5 流式消息（Stream）

```json
{
  "protocol": "openbase/v1.0",
  "message_id": "msg-7f3a9b2c",
  "timestamp": "2026-07-05T10:00:00.000Z",
  "version": "1.0",
  "type": "STREAM",
  "stream_id": "stream-7f3a9b2c",
  "sequence": 1,
  "total": 100,
  "data": {
    "event_type": "EVIDENCE_SUBMITTED",
    "evidence_id": "evid-00000001"
  }
}
```

| 字段 | 类型 | 约束 | 描述 |
| :--- | :--- | :--- | :--- |
| `stream_id` | string | 格式: `stream-{8位hex}` | 流 ID |
| `sequence` | integer | ≥ 1 | 流中序列号 |
| `total` | integer | ≥ 1 | 总消息数 |
| `data` | any | 非空 | 流数据块 |

## 4. 端点规范

### 4.1 端点命名规则

OpenBase API 端点 **MUST** 遵循以下命名规则：

```text
/v{version}/{resource}/{id}/{sub-resource}
```

**示例**：

```text
/v1/runtimes/{runtime_id}
/v1/evidence/{evidence_id}
/v1/runtimes/{runtime_id}/certificates
/v1/certificates/{certificate_id}/revoke
```

### 4.2 标准端点

| 端点 | 方法 | 描述 | 必需 |
| :--- | :--- | :--- | :--- |
| `/health` | GET | 健康检查 | **MUST** |
| `/v1/runtimes` | GET | 列出 Runtime | **MUST** |
| `/v1/runtimes/register` | POST | 注册 Runtime | **MUST** |
| `/v1/runtimes/{id}` | GET | 获取 Runtime | **MUST** |
| `/v1/runtimes/{id}` | PUT | 更新 Runtime | **SHOULD** |
| `/v1/runtimes/{id}` | DELETE | 注销 Runtime | **SHOULD** |
| `/v1/evidence` | POST | 提交证据 | **MUST** |
| `/v1/evidence/{id}` | GET | 获取证据 | **MUST** |
| `/v1/evidence/execution/{id}` | GET | 按执行 ID 查询 | **SHOULD** |
| `/v1/evidence/runtime/{id}` | GET | 按 Runtime ID 查询 | **SHOULD** |
| `/v1/certificates/issue` | POST | 颁发证书 | **MUST** |
| `/v1/certificates/{id}` | GET | 获取证书 | **MUST** |
| `/v1/certificates/runtime/{id}` | GET | 按 Runtime ID 查询 | **SHOULD** |
| `/v1/certificates/{id}/revoke` | POST | 撤销证书 | **SHOULD** |
| `/v1/trust/{runtime_id}` | GET | 获取信任分数 | **MUST** |
| `/v1/trust/ranking` | GET | 信任排名 | **SHOULD** |
| `/v1/events` | WebSocket | 事件订阅 | **SHOULD** |

## 5. 错误处理

### 5.1 错误响应格式

所有错误响应 **MUST** 遵循统一格式：

```json
{
  "error": {
    "code": "EVIDENCE_VALIDATION_FAILED",
    "message": "Evidence signature verification failed",
    "details": {
      "evidence_id": "evid-00000001",
      "expected_public_key": "...",
      "provided_signature": "..."
    },
    "trace_id": "trace-7f3a9b2c",
    "timestamp": "2026-07-05T10:00:00.000Z"
  }
}
```

| 字段 | 类型 | 约束 | 描述 |
| :--- | :--- | :--- | :--- |
| `code` | string | 必须注册 | 错误码 |
| `message` | string | 非空 | 错误描述 |
| `details` | object | 可选 | 错误详情 |
| `trace_id` | string | 可选 | 追踪 ID |
| `timestamp` | string | RFC 3339 UTC 格式 | 错误发生时间 |

### 5.2 标准错误码

| 错误码 | HTTP 状态码 | 描述 |
| :--- | :--- | :--- |
| `BAD_REQUEST` | 400 | 请求格式错误 |
| `UNAUTHORIZED` | 401 | 认证失败 |
| `FORBIDDEN` | 403 | 权限不足 |
| `NOT_FOUND` | 404 | 资源不存在 |
| `CONFLICT` | 409 | 资源冲突 |
| `UNPROCESSABLE_ENTITY` | 422 | 验证失败 |
| `RATE_LIMITED` | 429 | 速率限制 |
| `INTERNAL_ERROR` | 500 | 内部错误 |
| `SERVICE_UNAVAILABLE` | 503 | 服务不可用 |
| `EVIDENCE_INVALID` | 422 | 证据无效 |
| `EVIDENCE_CHAIN_INCOMPLETE` | 422 | 证据链不完整 |
| `SIGNATURE_INVALID` | 422 | 签名无效 |
| `RUNTIME_NOT_FOUND` | 404 | Runtime 不存在 |
| `RUNTIME_ALREADY_REGISTERED` | 409 | Runtime 已注册 |
| `CERTIFICATE_NOT_FOUND` | 404 | 证书不存在 |
| `CERTIFICATE_EXPIRED` | 400 | 证书已过期 |
| `CERTIFICATE_REVOKED` | 400 | 证书已撤销 |
| `TRUST_INSUFFICIENT` | 400 | 信任分数不足 |
| `VERSION_INCOMPATIBLE` | 400 | 版本不兼容 |

## 6. 版本协商

### 6.1 版本声明

客户端 **MUST** 在请求中声明其支持的协议版本：

```text
Accept-Version: 1.0
```

服务端 **MUST** 在响应中声明其支持的协议版本：

```text
OpenBase-Version: 1.0
```

### 6.2 版本协商流程

```text
客户端                          服务端
  |                              |
  |------- Accept-Version: 1.0 ->|
  |                              |
  |<-- OpenBase-Version: 1.0 ---|
  |                              |
  |         (继续通信)           |
  |                              |
```

### 6.3 版本不兼容处理

若服务端不支持客户端请求的版本：

```text
HTTP/1.1 400 Bad Request
OpenBase-Version: 1.0
{
  "error": {
    "code": "VERSION_INCOMPATIBLE",
    "message": "Client version 2.0 not supported, server supports 1.0-1.5",
    "details": {
      "supported_versions": ["1.0", "1.1", "1.2", "1.3", "1.4", "1.5"]
    }
  }
}
```

## 7. 安全传输

### 7.1 TLS 要求

所有生产环境下的 OpenBase Wire Protocol **MUST** 使用 TLS 加密：

| 要求 | 说明 |
| :--- | :--- |
| TLS 版本 | TLS 1.2 或更高版本 |
| 密码套件 | 支持前向安全的密码套件 |
| 证书验证 | 必须验证服务器证书 |
| 证书过期 | 监控证书有效期 |

### 7.2 安全头

所有 HTTP 响应 **SHOULD** 包含以下安全头：

```text
Strict-Transport-Security: max-age=31536000; includeSubDomains
X-Content-Type-Options: nosniff
X-Frame-Options: DENY
Content-Security-Policy: default-src 'self'
```

## 8. 性能要求

### 8.1 消息大小限制

| 限制项 | 建议值 | 说明 |
| :--- | :--- | :--- |
| 单个请求体 | ≤ 10 MB | 超过应使用分块上传 |
| 单条证据 | ≤ 1 MB | 超过应拆分 |
| 批量提交 | ≤ 1000 条/批次 | 超过应分批提交 |

### 8.2 超时设置

| 超时类型 | 建议值 | 说明 |
| :--- | :--- | :--- |
| 连接超时 | 30 秒 | TCP 连接建立超时 |
| 读取超时 | 60 秒 | 等待响应超时 |
| 写入超时 | 30 秒 | 发送请求超时 |
| 整体超时 | 120 秒 | 完整请求超时 |

## 9. 兼容性

### 9.1 向后兼容承诺

- 新字段 **MAY** 被添加，旧客户端 **MUST** 忽略未知字段。
- 现有字段 **MUST NOT** 被删除或更改类型。
- 现有端点 **MUST NOT** 被删除（除非有至少一年的弃用期）。
- 错误码 **MAY** 被添加，旧客户端 **SHOULD** 优雅处理未知错误码。

### 9.2 弃用策略

| 阶段 | 行动 | 时间 |
| :--- | :--- | :--- |
| 宣布弃用 | 在文档和响应头中标记 | T+0 |
| 标记弃用 | 添加 `Deprecation` 响应头 | T+6 月 |
| 移除支持 | 返回 410 Gone | T+12 月 |

## 10. 示例

### 10.1 请求示例（HTTP/2）

```http
POST /v1/evidence HTTP/2
Host: registry.openbase.io
Content-Type: application/json
Accept: application/json
Authorization: Bearer eyJhbGciOiJIUzI1NiIs...
Accept-Version: 1.0

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

### 10.2 响应示例

```http
HTTP/2 200 OK
Content-Type: application/json
OpenBase-Version: 1.0
X-Request-ID: req-7f3a9b2c

{
  "evidence_id": "evid-00000001",
  "runtime_id": "runtime-7f3a9b2c",
  "status": "accepted",
  "timestamp": "2026-07-05T10:00:00.000Z"
}
```

### 10.3 错误响应示例

```http
HTTP/2 422 Unprocessable Entity
Content-Type: application/json
OpenBase-Version: 1.0

{
  "error": {
    "code": "EVIDENCE_INVALID",
    "message": "Evidence signature verification failed",
    "details": {
      "evidence_id": "evid-00000001",
      "expected_public_key": "MfWvR5pxUep9GUBt/ztts2OpvY9dc8+guh8P3GCNWqY=",
      "provided_signature": "abc123..."
    },
    "timestamp": "2026-07-05T10:00:00.000Z"
  }
}
```

## 11. 参考

### 11.1 规范性引用

- RFC 2119 — Key words for use in RFCs to Indicate Requirement Levels
- RFC 3339 — Timestamp Format
- RFC 7540 — HTTP/2
- RFC 9110 — HTTP Semantics
- RFC 6455 — The WebSocket Protocol
- RFC 5246 — TLS 1.2
- RFC 8446 — TLS 1.3

### 11.2 信息性引用

- JSON — JavaScript Object Notation (RFC 8259)
- CBOR — Concise Binary Object Representation (RFC 8949)
- Protocol Buffers — Google's language-neutral, platform-neutral extensible mechanism for serializing structured data

## 12. 冻结声明

本规范已冻结为 v1.0，生效日期：2026-07-05。

任何变更必须通过 OBEP 流程进行，并保持向后兼容。

**冻结状态**：✅ 已冻结

**下次审查**：2027-07-05 或 严重安全漏洞发现时。

---

*本规范由 OpenBase Specification Committee 维护。*
```

---


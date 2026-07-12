
---

```markdown
---
OBEP: 0007
Title: Compatibility Policy v1.0
Status: Frozen
Version: 1.0.0
Date: 2026-07-05
Authors: OpenBase Specification Committee
Obsoletes: None
---

# OBEP-0007: Compatibility Policy v1.0

## 1. 前言

### 1.1 目的

本政策定义 OpenBase 协议、Schema、API 和实现的兼容性承诺，确保 OpenBase 生态系统在不同版本之间保持稳定、可预测的演进路径。兼容性是 OpenBase 成为长期标准的基础保障。

### 1.2 范围

本政策涵盖：

- 版本号定义与演进规则
- 兼容性等级与承诺
- 破坏性变更的管理流程
- 弃用（Deprecation）策略
- Schema 演进规则
- API 演进规则
- 协议演进规则
- 兼容性测试要求

本政策不涵盖：

- 具体协议定义（参见 OBEP-0001 ~ OBEP-0006）
- 实现细节
- 性能指标

### 1.3 符合性关键词

本政策使用 RFC 2119 关键词：

- **MUST**：必须遵守
- **MUST NOT**：禁止行为
- **SHOULD**：建议遵守
- **SHOULD NOT**：不建议行为
- **MAY**：可选行为

## 2. 版本号定义

### 2.1 版本号格式

OpenBase 所有版本号 **MUST** 遵循语义化版本（Semantic Versioning）格式：

```text
MAJOR.MINOR.PATCH
```

| 组件 | 含义 | 变更条件 |
| :--- | :--- | :--- |
| MAJOR | 主要版本 | 破坏性变更（Breaking Changes） |
| MINOR | 次要版本 | 新增功能，向后兼容 |
| PATCH | 补丁版本 | 缺陷修复，向后兼容 |

### 2.2 版本号演进规则

| 变更类型 | MAJOR | MINOR | PATCH |
| :--- | :--- | :--- | :--- |
| 破坏性 Schema 变更 | +1 | 0 | 0 |
| 新增 Schema 字段（可选） | 0 | +1 | 0 |
| 新增 API 端点 | 0 | +1 | 0 |
| 修改 API 行为（向后兼容） | 0 | +1 | 0 |
| 删除 API 端点 | +1 | 0 | 0 |
| 缺陷修复 | 0 | 0 | +1 |
| 文档更新 | 0 | 0 | +1 |
| 安全修复 | 0 | 0 | +1 |

### 2.3 版本号应用范围

| 资产 | 版本号独立 | 说明 |
| :--- | :--- | :--- |
| 核心协议规范 | ✅ 是 | Evidence Schema, Trust Model, Replay Protocol 等 |
| API 定义 | ✅ 是 | 独立的 API 版本号 |
| SDK | ✅ 是 | 每个 SDK 独立版本 |
| 参考实现（OpenClaw） | ✅ 是 | 独立版本号 |
| 一致性测试套件 | ✅ 是 | 独立版本号 |

## 3. 兼容性等级

### 3.1 等级定义

| 等级 | 描述 | 变更限制 |
| :--- | :--- | :--- |
| **FULL** | 完全兼容 | 任何版本之间完全兼容 |
| **BACKWARD** | 向后兼容 | 新版本支持旧版本客户端 |
| **FORWARD** | 向前兼容 | 旧版本支持新版本客户端（部分） |
| **NONE** | 不兼容 | 必须同时升级 |

### 3.2 各资产兼容性承诺

| 资产 | 兼容性等级 | 说明 |
| :--- | :--- | :--- |
| Evidence Schema | **BACKWARD** | 新版本必须兼容旧版本证据 |
| Trust Model | **BACKWARD** | 新模型必须可解释旧评分 |
| Certificate Schema | **BACKWARD** | 新证书必须兼容旧证书验证 |
| Replay Protocol | **BACKWARD** | 新版本必须可重放旧证据 |
| Registry Protocol | **BACKWARD** | 新 Registry 必须支持旧 Runtime |
| Wire Protocol | **BACKWARD** | 新协议必须兼容旧消息格式 |
| APIs | **BACKWARD** | 新 API 必须支持旧客户端 |

## 4. 破坏性变更管理

### 4.1 破坏性变更定义

以下变更被视为破坏性变更，**MUST** 触发 MAJOR 版本升级：

| 变更类型 | 示例 |
| :--- | :--- |
| 删除必需字段 | 删除 Evidence 中的 `actor` 字段 |
| 修改必需字段类型 | 将 `timestamp` 从 string 改为 integer |
| 修改必需字段语义 | 改变 `signature` 的签名算法 |
| 删除 API 端点 | 移除 `/v1/runtimes/register` |
| 修改 API 签名 | 改变请求/响应结构 |
| 改变默认行为 | 信任模型的计算公式改变 |
| 协议不兼容 | 消息格式不兼容 |

### 4.2 破坏性变更流程

任何破坏性变更 **MUST** 遵循以下流程：

```text
1. 提交 OBEP（提案阶段）
   ↓
2. 社区评审（至少 30 天）
   ↓
3. 弃用通知（至少 12 个月）
   ↓
4. 发布 MAJOR 版本
   ↓
5. 提供迁移指南
   ↓
6. 保持旧版本支持（至少 6 个月）
```

### 4.3 破坏性变更例外

以下情况**MAY** 在不触发 MAJOR 版本的情况下进行：

| 情况 | 条件 |
| :--- | :--- |
| 安全修复 | 严重安全漏洞 |
| 性能修复 | 不影响正确性 |
| 文档更正 | 不影响实现 |
| 测试修复 | 不影响协议 |

## 5. 弃用策略

### 5.1 弃用定义

弃用（Deprecation）是指将某个功能标记为不再推荐使用，将在未来版本中移除。

### 5.2 弃用流程

```text
1. 在文档中标记为 @deprecated
   ↓
2. 在响应头中添加 Deprecation 头
   ↓
3. 发布 MINOR 版本（标记弃用，仍可使用）
   ↓
4. 至少 12 个月后
   ↓
5. 发布 MAJOR 版本（移除）
```

### 5.3 弃用标记

**文档标记**：

```text
Deprecated: use /v2/evidence instead
```

**响应头标记**：

```text
Deprecation: true
Sunset: 2028-01-01T00:00:00Z
```

**JSON 响应标记**：

```json
{
  "warning": "This endpoint is deprecated and will be removed in v2.0. Please use /v2/evidence instead.",
  "deprecated_at": "2026-07-05",
  "sunset_at": "2027-07-05"
}
```

### 5.4 弃用期限

| 类型 | 最小弃用期限 |
| :--- | :--- |
| API 端点 | 12 个月 |
| Schema 字段 | 12 个月 |
| 协议特性 | 18 个月 |
| 全部协议版本 | 24 个月 |

## 6. Schema 演进规则

### 6.1 向后兼容变更（允许）

以下变更在 MINOR 版本中**MUST**被允许：

| 变更 | 示例 |
| :--- | :--- |
| 新增可选字段 | 添加 `metadata.cost_usd` |
| 扩展枚举值 | 添加新的 `event_type` |
| 放宽约束 | 将 `duration_ms` 从必需改为可选 |
| 增加文档 | 添加字段描述 |
| 增加示例 | 添加新的示例 |

### 6.2 向前兼容变更（允许）

以下变更在 MINOR 版本中**MAY**被允许（需谨慎）：

| 变更 | 示例 |
| :--- | :--- |
| 字段重命名（保留旧字段） | 添加 `runtime_id`，保留 `id` 并标记弃用 |
| 新增必需字段（提供默认值） | 添加 `spec_version` 并提供默认值 |

### 6.3 不兼容变更（禁止）

以下变更在 MAJOR 版本外**MUST NOT**发生：

| 变更 | 示例 |
| :--- | :--- |
| 删除必需字段 | 删除 `actor` |
| 修改字段类型 | `timestamp` 从 string 改为 integer |
| 删除枚举值 | 移除 `TOOL_CALL` 事件类型 |
| 修改字段语义 | 改变 `hash` 的计算方式 |

### 6.4 Schema 版本字段

每个 Schema **MUST** 包含 `spec_version` 字段：

```json
{
  "spec_version": "1.0.0"
}
```

客户端 **MUST** 检查此字段以确定 Schema 版本。

## 7. API 演进规则

### 7.1 API 版本化

API **MUST** 通过 URL 路径进行版本化：

```text
/v1/evidence
/v2/evidence
```

### 7.2 API 向后兼容变更

| 变更 | 兼容性 | 版本 |
| :--- | :--- | :--- |
| 新增端点 | ✅ 兼容 | MINOR |
| 新增可选查询参数 | ✅ 兼容 | MINOR |
| 新增响应字段 | ✅ 兼容 | MINOR |
| 修改响应字段（保持类型） | ⚠️ 谨慎 | MINOR |
| 删除端点 | ❌ 不兼容 | MAJOR |
| 修改请求结构 | ❌ 不兼容 | MAJOR |

### 7.3 API 内容协商

客户端 **SHOULD** 使用 `Accept` 头进行内容协商：

```text
Accept: application/vnd.openbase.v1+json
```

## 8. 协议演进规则

### 8.1 协议版本化

Wire Protocol **MUST** 在消息头中包含版本信息：

```json
{
  "protocol": "openbase/v1.0"
}
```

### 8.2 协议向后兼容变更

| 变更 | 兼容性 | 版本 |
| :--- | :--- | :--- |
| 新增消息类型 | ✅ 兼容 | MINOR |
| 新增可选字段 | ✅ 兼容 | MINOR |
| 修改错误码（新增） | ✅ 兼容 | MINOR |
| 修改错误码（删除） | ❌ 不兼容 | MAJOR |
| 修改消息格式 | ❌ 不兼容 | MAJOR |

## 9. 兼容性测试要求

### 9.1 测试范围

兼容性测试 **MUST** 覆盖：

| 测试类型 | 描述 | 频率 |
| :--- | :--- | :--- |
| 向后兼容性测试 | 新版本处理旧版本数据 | 每次发布 |
| 向前兼容性测试 | 旧版本处理新版本数据（有限） | 每次发布 |
| 跨版本互操作性测试 | 不同版本之间通信 | 每个 MAJOR 版本 |
| Schema 兼容性测试 | 新旧 Schema 数据互操作 | 每次 Schema 变更 |

### 9.2 兼容性测试套件

OpenBase **MUST** 提供兼容性测试套件：

```bash
openbase test --compatibility
```

测试套件 **MUST** 包含：

1. 旧版本证据的验证
2. 旧版本请求的响应
3. 新版本响应的解析
4. 版本协商测试

## 10. 版本支持策略

### 10.1 支持周期

| 版本类型 | 支持周期 | 说明 |
| :--- | :--- | :--- |
| 当前 MAJOR 版本 | 无限 | 持续支持 |
| 前一个 MAJOR 版本 | 12 个月 | 仅安全修复 |
| 前两个 MAJOR 版本 | 6 个月 | 仅严重安全修复 |
| 更早版本 | 不支持 | 建议升级 |

### 10.2 安全更新

安全修复 **SHOULD** 回传到受支持的旧版本：

| 版本类型 | 安全修复 | 说明 |
| :--- | :--- | :--- |
| 当前 MAJOR 版本 | ✅ 是 | 立即修复 |
| 前一个 MAJOR 版本 | ✅ 是 | 尽快修复 |
| 前两个 MAJOR 版本 | ⚠️ 可能 | 仅严重漏洞 |
| 更早版本 | ❌ 否 | 建议升级 |

## 11. 示例

### 11.1 破坏性变更示例

**Evidence Schema v1.0 → v2.0 破坏性变更**：

```diff
{
  "evidence_id": "evid-00000001",
  "spec_version": "2.0",
- "actor": "agent.demo-001",
+ "actors": ["agent.demo-001"],
  "event_type": "LLM_CALL",
  "timestamp": "2026-07-05T10:00:00.000Z",
  ...
}
```

**变更原因**：支持多 Actor 执行场景。
**迁移指南**：将 `actor` 字段替换为 `actors` 数组。

### 11.2 弃用示例

**API 端点弃用**：

```http
POST /v1/runtimes/register HTTP/1.1
Deprecation: true
Sunset: 2027-07-05T00:00:00Z
Link: </v2/runtimes/register>; rel="deprecation"
```

**响应**：

```json
{
  "runtime_id": "runtime-7f3a9b2c",
  "warning": "This endpoint is deprecated. Please use /v2/runtimes/register instead."
}
```

## 12. 参考

### 12.1 规范性引用

- RFC 2119 — Key words for use in RFCs to Indicate Requirement Levels
- Semantic Versioning 2.0.0
- RFC 8594 — The "Sunset" HTTP Header Field
- RFC 8288 — Web Linking

### 12.2 信息性引用

- Kubernetes API Deprecation Policy
- OpenTelemetry Versioning Policy
- Google API Design Guide — Versioning

## 13. 冻结声明

本政策已冻结为 v1.0，生效日期：2026-07-05。

任何变更必须通过 OBEP 流程进行。

**冻结状态**：✅ 已冻结

**下次审查**：2027-07-05

---

*本政策由 OpenBase Specification Committee 维护。*
```

---

*
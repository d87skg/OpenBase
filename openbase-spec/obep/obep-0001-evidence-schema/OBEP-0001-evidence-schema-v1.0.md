

---

```markdown
---
OBEP: 0001
Title: Evidence Schema v1.0
Status: Frozen
Version: 1.0.0
Date: 2026-07-05
Authors: OpenBase Specification Committee
Obsoletes: None
---

# OBEP-0001: Evidence Schema v1.0

## 1. 前言

### 1.1 目的

本规范定义 OpenBase 证据（Evidence）的数据结构、字段约束、哈希链、签名与验证规则，作为 Agent 执行可审计记录的基础标准。

### 1.2 范围

本规范涵盖：

- Evidence 对象的字段定义（必需/可选）
- 字段类型与约束
- 哈希链（Hash Chain）机制
- 数字签名与验证
- 版本与兼容性规则

本规范不涵盖：

- 证据的存储与传输（参见 OBEP-0005 Registry Protocol 与 OBEP-0006 Wire Protocol）
- 证据的语义解释（参见 OBEP-0003 Trust Model）
- Agent 执行行为（参见 OBEP-0002 Replay Protocol）

### 1.3 符合性关键词

本规范使用 RFC 2119 关键词：

- **MUST**：必须遵守，否则不符合标准
- **MUST NOT**：禁止行为
- **SHOULD**：建议遵守
- **SHOULD NOT**：不建议行为
- **MAY**：可选行为

## 2. 证据对象定义（Evidence Object）

### 2.1 对象概述

Evidence 是一个 JSON 对象，表示 Agent 执行过程中的一个可审计事件。

```json
{
  "evidence_id": "evid-7f3a9b2c",
  "spec_version": "1.0",
  "runtime_id": "runtime-openclaw-2026-07-05",
  "execution_id": "exec-1e2f3a4b",
  "actor": "agent.demo-001",
  "event_type": "LLM_CALL",
  "timestamp": "2026-07-05T10:00:00.000Z",
  "causal": {
    "parent_id": "evid-5d8e1c3a",
    "vector_clock": {"node-a": 3, "node-b": 1}
  },
  "action": {
    "input": {"model": "gpt-4", "prompt": "Hello world"},
    "output": {"completion": "Hello there!"},
    "duration_ms": 1234
  },
  "proof": {
    "hash": "sha256:a1b2c3d4e5f6...",
    "signature": "ed25519:..."
  },
  "metadata": {
    "model_version": "gpt-4-0613",
    "cost_usd": 0.002
  }
}
```

### 2.2 必需字段（Required Fields）

| 字段名 | 类型 | 约束 | 描述 |
| :--- | :--- | :--- | :--- |
| `evidence_id` | string | 格式: `evid-{8位hex}` 全局唯一 | 证据唯一标识符 |
| `spec_version` | string | 固定 `"1.0"` | 本规范版本 |
| `runtime_id` | string | 非空 | 产生证据的 Runtime 标识符 |
| `execution_id` | string | 非空 | 所属执行 ID |
| `actor` | string | 非空 | Agent 标识符 |
| `event_type` | string | 必须注册 | 事件类型（见 2.4） |
| `timestamp` | string | RFC 3339 UTC 格式 | 证据生成时间 |
| `causal` | object | 见 2.5 | 因果信息 |
| `action` | object | 见 2.6 | 动作信息 |
| `proof` | object | 见 2.7 | 完整性证明信息 |

### 2.3 可选字段（Optional Fields）

| 字段名 | 类型 | 描述 |
| :--- | :--- | :--- |
| `metadata` | object | 额外元数据 |

### 2.4 Event Type 注册表

| 事件类型 | 描述 | 必需 evidence |
| :--- | :--- | :--- |
| `AGENT_STARTED` | Agent 执行开始 | 是 |
| `AGENT_FINISHED` | Agent 执行结束 | 是 |
| `LLM_REQUEST` | LLM 请求 | 是 |
| `LLM_RESPONSE` | LLM 响应 | 是 |
| `TOOL_CALL` | 工具调用 | 是 |
| `TOOL_RESULT` | 工具结果 | 是 |
| `STATE_UPDATE` | 状态变更 | 否 |
| `ERROR` | 错误事件 | 是 |
| `RETRY` | 重试事件 | 否 |

### 2.5 因果字段（`causal`）

| 子字段 | 类型 | 约束 | 描述 |
| :--- | :--- | :--- | :--- |
| `parent_id` | string | null 或 `evid-*` 格式 | 父证据 ID，第一条为 null |
| `vector_clock` | object | 节点名 → 整数 | 向量时钟，见 2.5.1 |

#### 2.5.1 向量时钟（Vector Clock）

```json
{"node-a": 3, "node-b": 1}
```

表示 `node-a` 的第 3 个事件，`node-b` 的第 1 个事件。

**规则**：
- 每个节点自己产生的下一个事件，时间戳增加。
- 无法比较的事件视为并发。
- 用于 Replay 时恢复顺序。

### 2.6 动作字段（`action`）

| 子字段 | 类型 | 约束 | 描述 |
| :--- | :--- | :--- | :--- |
| `input` | any | 非空 | 输入数据 |
| `output` | any | 可为 null | 输出数据 |
| `duration_ms` | integer | >= 0 | 耗时（毫秒） |

### 2.7 证明字段（`proof`）

| 子字段 | 类型 | 约束 | 描述 |
| :--- | :--- | :--- | :--- |
| `hash` | string | 格式: `sha256:{64位hex}` | 证据哈希值 |
| `signature` | string | 格式: `ed25519:{base64}` | Ed25519 签名 |
| `public_key` | string | base64 | 签名公钥（可选） |

### 2.8 元数据字段（`metadata`）

| 子字段 | 类型 | 描述 |
| :--- | :--- | :--- |
| `model_version` | string | 模型版本 |
| `cost_usd` | number | 成本（美元） |
| `tags` | array of string | 标签 |

## 3. 证据链（Evidence Chain）

### 3.1 哈希链（Hash Chain）

每个 Evidence 的 `proof.hash` 计算方式：

```
hash = SHA256(
    canonical_json(evidence_without_proof_and_previous_hash)
    + previous_hash
)
```

**关键规则**：
- `canonical_json`：按字母顺序排列键值对，无多余空格。
- `previous_hash`：父证据的 `hash`（若无父，则忽略）。

### 3.2 链完整性（Chain Integrity）

Evidence 链有效，当且仅当：
- 所有 `causal.parent_id` 形成的图是**有向无环图（DAG）**。
- 第一个 Evidence 的 `parent_id` 为 `null`。
- 每个 Evidence 的 `hash` 与上一个一致。

## 4. 签名与验证（Signature & Verification）

### 4.1 签名算法

- **签名算法**：Ed25519
- **密钥长度**：32 字节私钥 / 32 字节公钥
- **签名数据**：`evidence_id || proof.hash || timestamp`

### 4.2 验证规则

1. **MUST** 验证签名正确。
2. **MUST** 验证哈希链连续。
3. **SHOULD** 验证 Vector Clock 单调递增。

## 5. 版本与兼容性（Version & Compatibility）

### 5.1 版本号

- `spec_version` 用于版本控制。
- 主版本（Major）变更需通过新的 OBEP。
- 次版本（Minor）向前兼容。

### 5.2 兼容性规则

| 变更类型 | 兼容性 | 示例 |
| :--- | :--- | :--- |
| 新增可选字段 | ✅ 兼容 | 添加 `metadata.cost_usd` |
| 删除可选字段 | ⚠️ 需 OBEP | 删除 `metadata.tags` |
| 新增必需字段 | ❌ 不兼容 | 添加 `session_id`（必需） |
| 删除必需字段 | ❌ 不兼容 | 删除 `actor` |

### 5.3 向后兼容承诺

v1.0 的 Evidence Schema 在冻结期内**不会删除或修改任何必需字段**。新增字段将作为可选字段引入。

## 6. 示例（Examples）

### 6.1 最小证据（Minimal Evidence）

```json
{
  "evidence_id": "evid-00000001",
  "spec_version": "1.0",
  "runtime_id": "runtime-demo",
  "execution_id": "exec-0001",
  "actor": "agent-demo",
  "event_type": "AGENT_STARTED",
  "timestamp": "2026-07-05T10:00:00.000Z",
  "causal": {
    "parent_id": null,
    "vector_clock": {"node-a": 1}
  },
  "action": {
    "input": {"prompt": "Hello"},
    "output": null,
    "duration_ms": 0
  },
  "proof": {
    "hash": "sha256:0000000000000000000000000000000000000000000000000000000000000000",
    "signature": "ed25519:..."
  }
}
```

### 6.2 完整证据链（Full Chain）

```json
[
  {
    "evidence_id": "evid-00000001",
    "event_type": "AGENT_STARTED",
    "causal": {"parent_id": null, "vector_clock": {"node-a": 1}},
    "proof": {"hash": "sha256:a...", "signature": "..."}
  },
  {
    "evidence_id": "evid-00000002",
    "event_type": "LLM_REQUEST",
    "causal": {"parent_id": "evid-00000001", "vector_clock": {"node-a": 2}},
    "proof": {"hash": "sha256:b...", "signature": "..."}
  },
  {
    "evidence_id": "evid-00000003",
    "event_type": "AGENT_FINISHED",
    "causal": {"parent_id": "evid-00000002", "vector_clock": {"node-a": 3}},
    "proof": {"hash": "sha256:c...", "signature": "..."}
  }
]
```

## 7. 参考（References）

### 7.1 规范性引用

- RFC 2119 — Key words for use in RFCs to Indicate Requirement Levels
- RFC 8785 — JSON Canonicalization Scheme
- RFC 4122 — UUID Format (用于 `evidence_id`)
- RFC 3339 — Timestamp Format
- Ed25519 — Edwards-curve Digital Signature Algorithm

### 7.2 信息性引用

- OBEP-0002: Replay Protocol v1.0
- OBEP-0003: Trust Model v1.0
- OBEP-0006: Wire Protocol v1.0

## 8. 冻结声明（Freeze Declaration）

本规范已冻结为 v1.0，生效日期：2026-07-05。

任何变更必须通过 OBEP 流程进行，并保持向后兼容。

**冻结状态**：✅ 已冻结

**下次审查**：2027-07-05 或 严重安全漏洞发现时。

---

*本规范由 OpenBase Specification Committee 维护。*
```


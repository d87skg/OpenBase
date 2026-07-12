

---

```markdown
---
OBEP: 0002
Title: Replay Protocol v1.0
Status: Frozen
Version: 1.0.0
Date: 2026-07-05
Authors: OpenBase Specification Committee
Obsoletes: None
---

# OBEP-0002: Replay Protocol v1.0

## 1. 前言

### 1.1 目的

本规范定义 OpenBase 重放（Replay）协议，即从证据链（Evidence Chain）重建 Agent 执行过程的标准方法。重放是验证 Agent 行为可审计性、可复现性和可信性的核心机制。

### 1.2 范围

本规范涵盖：

- 重放的核心概念与前置条件
- 重放输入与输出格式
- 重放流程（验证、构建、排序、重建）
- 重放保真度等级（Fidelity Levels）
- 重放失败处理
- 确定性要求
- 跨 Runtime 重放兼容性

本规范不涵盖：

- 证据的生成与签名（参见 OBEP-0001 Evidence Schema）
- 证据的存储与传输（参见 OBEP-0005 Registry Protocol）
- 信任模型与评分（参见 OBEP-0003 Trust Model）

### 1.3 符合性关键词

本规范使用 RFC 2119 关键词：

- **MUST**：必须遵守，否则不符合标准
- **MUST NOT**：禁止行为
- **SHOULD**：建议遵守
- **SHOULD NOT**：不建议行为
- **MAY**：可选行为

## 2. 核心概念

### 2.1 重放定义

**重放（Replay）** 是指从一组有序的证据链中，重建 Agent 执行过程的状态序列、动作序列和因果依赖关系的过程。

重放不是重新执行 Agent 代码，而是从证据中还原执行历史。

### 2.2 重放前置条件

执行重放前，**MUST** 满足以下条件：

| 条件 | 描述 | 验证方式 |
| :--- | :--- | :--- |
| 证据链完整 | 所有证据的 `parent_id` 形成连通 DAG | 检查根节点与叶节点 |
| 证据链已签名 | 每条证据的 `proof.signature` 有效 | 验证 Ed25519 签名 |
| 证据链无环 | 不存在循环依赖 | 拓扑排序检测 |
| 证据链有序 | `vector_clock` 可比较 | 检查单调性 |
| 证据链版本兼容 | 所有证据的 `spec_version` 为 1.0 | 版本检查 |

任何前置条件不满足，重放 **MUST** 返回错误，**MUST NOT** 产生部分结果。

### 2.3 重放输入

重放输入是一个证据数组，**MUST** 满足：

```json
[
  {
    "evidence_id": "evid-00000001",
    "event_type": "AGENT_STARTED",
    "causal": {"parent_id": null, "vector_clock": {"node-a": 1}},
    "action": {"input": {...}, "output": null},
    "proof": {"hash": "...", "signature": "..."}
  },
  {
    "evidence_id": "evid-00000002",
    "event_type": "LLM_REQUEST",
    "causal": {"parent_id": "evid-00000001", "vector_clock": {"node-a": 2}},
    "action": {"input": {...}, "output": null},
    "proof": {"hash": "...", "signature": "..."}
  }
]
```

**约束**：
- 证据数组 **MUST** 为 JSON 数组。
- 每条证据 **MUST** 符合 OBEP-0001 定义的 Evidence Schema。
- 证据数组 **MAY** 包含来自多个 Runtime 的证据，但重放时 **MUST** 按 `runtime_id` 分组或按 `vector_clock` 全局排序。

### 2.4 重放输出

重放输出 **MUST** 包含以下结构：

```json
{
  "replay_id": "replay-7f3a9b2c",
  "execution_id": "exec-1e2f3a4b",
  "runtime_id": "runtime-openclaw-2026-07-05",
  "status": "SUCCESS | PARTIAL | FAILED",
  "fidelity": "EXACT | LOGICAL | CAUSAL | STRUCTURAL",
  "timeline": [
    {
      "sequence": 1,
      "evidence_id": "evid-00000001",
      "event_type": "AGENT_STARTED",
      "state_snapshot": {...},
      "inferred_action": {...}
    },
    {
      "sequence": 2,
      "evidence_id": "evid-00000002",
      "event_type": "LLM_REQUEST",
      "state_snapshot": {...},
      "inferred_action": {...}
    }
  ],
  "statistics": {
    "total_events": 10,
    "reconstructed_events": 10,
    "missing_events": 0,
    "duration_ms": 1234,
    "confidence": 0.98
  },
  "divergence": null
}
```

## 3. 重放流程

### 3.1 概述

重放流程由以下五个阶段组成：

```text
┌─────────────────┐
│ 1. 验证证据链    │
└────────┬────────┘
         ▼
┌─────────────────┐
│ 2. 构建因果图    │
└────────┬────────┘
         ▼
┌─────────────────┐
│ 3. 拓扑排序      │
└────────┬────────┘
         ▼
┌─────────────────┐
│ 4. 重建状态      │
└────────┬────────┘
         ▼
┌─────────────────┐
│ 5. 验证输出      │
└─────────────────┘
```

### 3.2 阶段 1：验证证据链

**MUST** 执行以下验证：

| 验证项 | 检查方式 | 失败处理 |
| :--- | :--- | :--- |
| 签名完整性 | 验证每条证据的 `proof.signature` | 返回 `FAILED`，标记证据 ID |
| 哈希链连续性 | 验证 `proof.hash` 与父证据匹配 | 返回 `FAILED`，标记断裂位置 |
| 版本兼容性 | 检查 `spec_version` 是否为 1.0 | 返回 `FAILED`，标记不兼容版本 |
| 无环性 | 拓扑排序检测环 | 返回 `FAILED`，标记环路径 |

### 3.3 阶段 2：构建因果图

**MUST** 根据 `causal.parent_id` 构建有向图：

- 每个证据为一个节点。
- `parent_id` 指向父节点，形成边。
- 根节点的 `parent_id` 为 `null`。

**图约束**：
- 图 **MUST** 为有向无环图（DAG）。
- 每个节点 **MUST** 有且仅有一个父节点，除非是根节点。

### 3.4 阶段 3：拓扑排序

**MUST** 对因果图进行拓扑排序，产生一个线性序列：

1. 根节点排在第一位。
2. 每个节点的子节点排在其后。
3. 若多个节点无依赖关系，**SHOULD** 按 `timestamp` 排序。

**排序算法**：**SHOULD** 使用 Kahn 算法或 DFS 拓扑排序。

### 3.5 阶段 4：重建状态

**MUST** 按拓扑排序顺序，依次重建状态：

- **初始状态**：空状态（`{}`）。
- **状态更新**：每个证据的 `action` 字段**SHOULD** 包含状态变更信息。
- **状态合并**：若多个证据并发，**SHOULD** 按 `vector_clock` 合并。

**状态重建规则**：

| 证据类型 | 状态更新规则 |
| :--- | :--- |
| `STATE_UPDATE` | 用 `action.input` 更新状态 |
| `LLM_REQUEST` | 记录请求，状态不变 |
| `LLM_RESPONSE` | 记录响应，状态不变 |
| `TOOL_CALL` | 记录工具调用，状态不变 |
| `TOOL_RESULT` | 记录工具结果，状态不变 |
| `AGENT_STARTED` | 初始化状态 |
| `AGENT_FINISHED` | 最终状态快照 |
| `ERROR` | 记录错误，状态不变 |

### 3.6 阶段 5：验证输出

**MUST** 验证重放输出：

| 验证项 | 检查方式 | 失败处理 |
| :--- | :--- | :--- |
| 状态一致性 | 比较重放状态与预期状态（若有） | 标记 divergence |
| 事件计数 | 重放事件数等于输入证据数 | 返回 `PARTIAL` |
| 因果一致性 | 检查 `parent_id` 顺序与重建顺序一致 | 返回 `FAILED` |

## 4. 重放保真度等级

### 4.1 定义

重放保真度（Fidelity）表示重放结果与原始执行的接近程度。

| 等级 | 描述 | 要求 |
| :--- | :--- | :--- |
| **EXACT** | 完全一致 | 状态、时间、顺序、输出完全相同 |
| **LOGICAL** | 逻辑一致 | 状态和顺序一致，时间和输出可不同 |
| **CAUSAL** | 因果一致 | 因果顺序一致，状态可近似 |
| **STRUCTURAL** | 结构一致 | 证据结构一致，状态未重建 |

### 4.2 保真度要求

| 场景 | 最低保真度要求 |
| :--- | :--- |
| 开发调试 | CAUSAL |
| 生产审计 | LOGICAL |
| 合规认证 | EXACT |
| 性能分析 | STRUCTURAL |
| 安全取证 | EXACT |

**实现要求**：
- Runtime **MUST** 支持至少 `CAUSAL` 保真度。
- Runtime **MAY** 支持 `EXACT` 保真度。
- 若 Runtime 不支持请求的保真度，**MUST** 返回 `PARTIAL` 并说明原因。

## 5. 重放失败处理

### 5.1 失败分类

| 失败类型 | 错误码 | 描述 | 可恢复性 |
| :--- | :--- | :--- | :--- |
| 证据链不完整 | `EVIDENCE_CHAIN_INCOMPLETE` | 缺少必需证据 | ❌ 不可恢复 |
| 签名无效 | `SIGNATURE_INVALID` | 证据签名验证失败 | ❌ 不可恢复 |
| 哈希链断裂 | `HASH_CHAIN_BROKEN` | 哈希链不连续 | ❌ 不可恢复 |
| 因果图有环 | `CAUSAL_GRAPH_CYCLE` | 存在循环依赖 | ❌ 不可恢复 |
| 版本不兼容 | `VERSION_INCOMPATIBLE` | 证据版本不支持 | ❌ 不可恢复 |
| 状态重建失败 | `STATE_RECONSTRUCTION_FAILED` | 状态无法重建 | ⚠️ 部分可恢复 |
| 保真度不足 | `FIDELITY_INSUFFICIENT` | 无法达到请求的保真度 | ⚠️ 可降级 |

### 5.2 错误响应格式

```json
{
  "replay_id": "replay-7f3a9b2c",
  "status": "FAILED",
  "error": {
    "code": "SIGNATURE_INVALID",
    "message": "Evidence evid-00000003 signature verification failed",
    "evidence_id": "evid-00000003",
    "details": {
      "expected_public_key": "...",
      "provided_signature": "..."
    }
  }
}
```

## 6. 确定性要求

### 6.1 确定性定义

重放**MUST**是确定性的：

- 同一证据链输入 → 同一重放输出。
- 同一证据链在不同 Runtime 上重放 → 同一重放输出（在相同保真度下）。

### 6.2 非确定性来源隔离

以下非确定性来源**MUST**在重放中被隔离或模拟：

| 来源 | 处理方式 |
| :--- | :--- |
| LLM 输出 | 从证据中读取，不重新调用 LLM |
| 外部 API | 从证据中读取，不重新调用 API |
| 时间戳 | 从证据中读取，不重新生成 |
| 随机数 | 从证据中读取，不重新生成 |

## 7. 跨 Runtime 重放兼容性

### 7.1 要求

证据链**SHOULD**在不同 Runtime 之间可重放：

- Runtime A 产生的证据链 → Runtime B 可重放。
- 重放结果**SHOULD**在语义上一致。

### 7.2 兼容性检查

重放前**SHOULD**检查：

- 证据 `runtime_id` 与当前 Runtime 是否匹配（若不匹配，则尝试通用重放模式）。
- 证据中引用的工具、模型在当前 Runtime 中是否可用（若不可用，则使用模拟模式）。

### 7.3 通用重放模式

若证据链来自其他 Runtime，重放**SHOULD**采用通用重放模式：

- 忽略 `runtime_id` 不匹配。
- 使用证据中记录的 `action.input` 和 `action.output` 重建状态。
- 不调用任何外部 API 或 LLM。

## 8. 示例

### 8.1 基本重放请求

```json
{
  "evidence_ids": ["evid-00000001", "evid-00000002", "evid-00000003"],
  "fidelity": "LOGICAL"
}
```

### 8.2 重放响应（成功）

```json
{
  "replay_id": "replay-7f3a9b2c",
  "execution_id": "exec-1e2f3a4b",
  "runtime_id": "runtime-openclaw-2026-07-05",
  "status": "SUCCESS",
  "fidelity": "LOGICAL",
  "timeline": [
    {
      "sequence": 1,
      "evidence_id": "evid-00000001",
      "event_type": "AGENT_STARTED",
      "state_snapshot": {"agent": "demo", "status": "initialized"},
      "inferred_action": {"action": "initialize", "input": {"prompt": "Hello"}}
    },
    {
      "sequence": 2,
      "evidence_id": "evid-00000002",
      "event_type": "LLM_REQUEST",
      "state_snapshot": {"agent": "demo", "status": "running"},
      "inferred_action": {"action": "llm_call", "input": {"model": "gpt-4", "prompt": "Hello"}}
    },
    {
      "sequence": 3,
      "evidence_id": "evid-00000003",
      "event_type": "AGENT_FINISHED",
      "state_snapshot": {"agent": "demo", "status": "finished"},
      "inferred_action": {"action": "finish", "output": "Hello there!"}
    }
  ],
  "statistics": {
    "total_events": 3,
    "reconstructed_events": 3,
    "missing_events": 0,
    "duration_ms": 1234,
    "confidence": 1.0
  },
  "divergence": null
}
```

### 8.3 重放响应（失败）

```json
{
  "replay_id": "replay-7f3a9b2c",
  "status": "FAILED",
  "error": {
    "code": "SIGNATURE_INVALID",
    "message": "Evidence evid-00000002 signature verification failed",
    "evidence_id": "evid-00000002"
  }
}
```

## 9. 参考

### 9.1 规范性引用

- RFC 2119 — Key words for use in RFCs to Indicate Requirement Levels
- OBEP-0001 — Evidence Schema v1.0
- OBEP-0003 — Trust Model v1.0

### 9.2 信息性引用

- Kahn, A. B. (1962). "Topological sorting of large networks." Communications of the ACM.
- Lamport, L. (1978). "Time, clocks, and the ordering of events in a distributed system." Communications of the ACM.

## 10. 冻结声明

本规范已冻结为 v1.0，生效日期：2026-07-05。

任何变更必须通过 OBEP 流程进行，并保持向后兼容。

**冻结状态**：✅ 已冻结

**下次审查**：2027-07-05 或 严重安全漏洞发现时。

---

*本规范由 OpenBase Specification Committee 维护。*
```

---


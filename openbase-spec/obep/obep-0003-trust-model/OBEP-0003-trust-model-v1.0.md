

---

```markdown
---
OBEP: 0003
Title: Trust Model v1.0
Status: Frozen
Version: 1.0.0
Date: 2026-07-05
Authors: OpenBase Specification Committee
Obsoletes: None
---

# OBEP-0003: Trust Model v1.0

## 1. 前言

### 1.1 目的

本规范定义 OpenBase 信任模型（Trust Model），即从证据链（Evidence Chain）计算 Runtime 信任分数的标准方法。信任分数是 Agent 可信任度的量化表示，用于认证、审计和决策支持。

### 1.2 范围

本规范涵盖：

- 信任分数的定义与计算
- 评分维度与权重
- 时间衰减机制
- 冲突检测与惩罚
- 信任状态分类
- 信任分数更新规则

本规范不涵盖：

- 证据的生成与验证（参见 OBEP-0001 Evidence Schema）
- 重放协议（参见 OBEP-0002 Replay Protocol）
- 证书生命周期（参见 OBEP-0004 Certificate Schema）

### 1.3 符合性关键词

本规范使用 RFC 2119 关键词：

- **MUST**：必须遵守，否则不符合标准
- **MUST NOT**：禁止行为
- **SHOULD**：建议遵守
- **SHOULD NOT**：不建议行为
- **MAY**：可选行为

## 2. 核心概念

### 2.1 信任定义

**信任（Trust）** 是对 Runtime 行为可信度的量化评估，基于其产生的证据链、重放一致性、冲突记录和认证历史计算得出。

信任分数（Trust Score）是一个 **[0.0, 1.0]** 区间内的浮点数，其中：

| 分数范围 | 信任等级 | 描述 |
| :--- | :--- | :--- |
| 0.90 – 1.00 | HIGH | 高度可信，适合生产环境 |
| 0.70 – 0.89 | MEDIUM | 中等可信，建议审计后使用 |
| 0.40 – 0.69 | LOW | 低可信，需谨慎使用 |
| 0.00 – 0.39 | UNTRUSTED | 不可信，建议拒绝 |

### 2.2 信任模型结构

信任模型由以下核心组件构成：

```text
┌─────────────────────────────────────────────────────────┐
│                     Trust Score                        │
├─────────────────────────────────────────────────────────┤
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐ │
│  │ 证据完整性    │  │ 重放一致性    │  │ 冲突记录      │ │
│  │ (0.35)       │  │ (0.30)       │  │ (0.20)       │ │
│  └──────────────┘  └──────────────┘  └──────────────┘ │
│  ┌──────────────┐  ┌──────────────┐                    │
│  │ 认证历史      │  │ 时间衰减      │                    │
│  │ (0.15)       │  │ (全局因子)    │                    │
│  └──────────────┘  └──────────────┘                    │
└─────────────────────────────────────────────────────────┘
```

### 2.3 信任状态

信任状态（Trust State）是 Runtime 当前信任等级的离散表示：

| 状态 | 描述 | 触发条件 |
| :--- | :--- | :--- |
| `UNKNOWN` | 未知 | 无证据记录 |
| `INITIAL` | 初始 | 有证据但不足 |
| `STABLE` | 稳定 | 证据充足且一致 |
| `HIGH` | 高信任 | 长期一致且已认证 |
| `SUSPENDED` | 暂停 | 检测到冲突 |
| `REVOKED` | 撤销 | 严重违规 |

## 3. 评分维度与权重

### 3.1 评分维度

| 维度 | 权重 | 取值范围 | 计算方式 |
| :--- | :--- | :--- | :--- |
| 证据完整性（Evidence Integrity） | 0.35 | [0.0, 1.0] | 签名验证率 × 哈希链完整率 |
| 重放一致性（Replay Consistency） | 0.30 | [0.0, 1.0] | 重放成功次数 / 总重放次数 |
| 冲突记录（Conflict Record） | 0.20 | [0.0, 1.0] | 1.0 - (冲突次数 × 0.1)，最低 0.0 |
| 认证历史（Certification History） | 0.15 | [0.0, 1.0] | 有效证书数量 × 0.2，最高 1.0 |

### 3.2 基础信任分数计算公式

```text
BaseScore =
    Evidence_Integrity × 0.35
  + Replay_Consistency × 0.30
  + Conflict_Record × 0.20
  + Certification_History × 0.15
```

### 3.3 各维度详细计算

#### 3.3.1 证据完整性（Evidence Integrity）

```text
Evidence_Integrity =
    (verified_count / total_count) × 0.7
  + (chain_complete_count / total_count) × 0.3
```

其中：

- `verified_count`：签名验证通过的证据数量
- `total_count`：证据总数
- `chain_complete_count`：哈希链完整的证据数量

#### 3.3.2 重放一致性（Replay Consistency）

```text
Replay_Consistency =
    replay_success_count / replay_total_count
```

其中：

- `replay_success_count`：重放成功的次数
- `replay_total_count`：重放总次数

若 `replay_total_count` = 0，则 `Replay_Consistency` = 0.5（初始中性值）。

#### 3.3.3 冲突记录（Conflict Record）

```text
Conflict_Record =
    max(0.0, 1.0 - (conflict_count × 0.1))
```

其中：

- `conflict_count`：检测到的冲突次数
- `conflict_count` **MUST** 在证据链中检测（参见第 5 节）

#### 3.3.4 认证历史（Certification History）

```text
Certification_History =
    min(1.0, valid_certificate_count × 0.2)
```

其中：

- `valid_certificate_count`：当前有效的证书数量（参见 OBEP-0004）
- 每个有效证书增加 0.2，最高 1.0

### 3.4 时间衰减因子

信任分数 **MUST** 随时间衰减，以反映近期行为比历史行为更重要。

```text
Decay_Factor = e^(-λ × Δt)
```

其中：

- `λ` = 0.01（衰减率常数）
- `Δt` = 自上次证据产生以来的天数

**衰减应用规则**：

```text
Trust_Score = BaseScore × Decay_Factor
```

**衰减限制**：
- 分数 **MUST NOT** 低于 0.1（最低保留分数）
- 若有新证据产生，**SHOULD** 立即重新计算

## 4. 冲突检测与处理

### 4.1 冲突定义

冲突（Conflict）是指同一 Runtime 或不同 Runtime 之间，对同一事实或事件存在不一致描述的情况。

### 4.2 冲突类型

| 类型 | 描述 | 检测方式 |
| :--- | :--- | :--- |
| `EVIDENCE_CONFLICT` | 同一 `execution_id` 下证据顺序不一致 | 比较 `parent_id` 和 `vector_clock` |
| `REPLAY_CONFLICT` | 同一证据链重放结果不一致 | 多次重放比较结果 |
| `STATEMENT_CONFLICT` | 同一 `actor` 对同一事实的陈述不一致 | 比较 `action.input` 或 `action.output` |
| `TOOL_CONFLICT` | 同一工具调用产生不同结果 | 比较 `TOOL_CALL` 和 `TOOL_RESULT` |

### 4.3 冲突检测规则

| 规则 | 描述 | 触发条件 |
| :--- | :--- | :--- |
| `CONFLICT-001` | 同一 `execution_id` 中，两个证据的 `parent_id` 互相指向 | 检测到环 |
| `CONFLICT-002` | 同一 `execution_id` 中，`vector_clock` 顺序与 `timestamp` 顺序矛盾 | 比较两者 |
| `CONFLICT-003` | 同一 `actor` 在同一 `execution_id` 中，`LLM_REQUEST` 与 `LLM_RESPONSE` 数量不匹配 | 计数比较 |
| `CONFLICT-004` | 不同 Runtime 对同一 `execution_id` 的证据描述不一致 | 跨 Runtime 比较 |
| `CONFLICT-005` | 同一工具调用的输入相同但输出不同 | 比较 `TOOL_CALL` 的 `input` 和 `TOOL_RESULT` 的 `output` |

### 4.4 冲突处理

**冲突处理策略**：

| 冲突类型 | 处理策略 | 信任影响 |
| :--- | :--- | :--- |
| `EVIDENCE_CONFLICT` | 标记冲突，记录冲突点 | -0.1 分/次 |
| `REPLAY_CONFLICT` | 标记冲突，记录重放失败 | -0.15 分/次 |
| `STATEMENT_CONFLICT` | 标记冲突，记录矛盾陈述 | -0.2 分/次 |
| `TOOL_CONFLICT` | 标记冲突，记录工具不一致 | -0.1 分/次 |

**冲突记录格式**：

```json
{
  "conflict_id": "conflict-7f3a9b2c",
  "type": "EVIDENCE_CONFLICT",
  "evidence_ids": ["evid-00000001", "evid-00000002"],
  "description": "Vector clock order contradicts timestamp order",
  "timestamp": "2026-07-05T10:00:00.000Z"
}
```

## 5. 信任状态管理

### 5.1 状态转换图

```text
┌─────────┐
│ UNKNOWN │
└────┬────┘
     │ 证据 ≥ 1
     ▼
┌─────────┐
│ INITIAL │
└────┬────┘
     │ 证据 ≥ 10 且 一致性 > 0.7
     ▼
┌─────────┐
│ STABLE  │
└────┬────┘
     │ 认证 ≥ 1 且 分数 > 0.85
     ▼
┌─────────┐
│  HIGH   │
└────┬────┘
     │ 检测到冲突
     ▼
┌──────────┐
│SUSPENDED │
└────┬─────┘
     │ 严重违规
     ▼
┌─────────┐
│REVOKED  │
└─────────┘
```

### 5.2 状态转换条件

| 当前状态 | 目标状态 | 触发条件 |
| :--- | :--- | :--- |
| `UNKNOWN` | `INITIAL` | 证据数量 ≥ 1 |
| `INITIAL` | `STABLE` | 证据数量 ≥ 10 且 重放一致性 > 0.7 |
| `STABLE` | `HIGH` | 有效证书 ≥ 1 且 Trust Score > 0.85 |
| `STABLE` | `SUSPENDED` | 检测到冲突 ≥ 3 次 |
| `HIGH` | `SUSPENDED` | 检测到冲突 ≥ 1 次 |
| `SUSPENDED` | `STABLE` | 冲突已解决且无新冲突 30 天 |
| `ANY` | `REVOKED` | 严重违规（签名伪造、证据篡改） |

## 6. 信任分数更新规则

### 6.1 触发更新的事件

信任分数 **MUST** 在以下事件发生后重新计算：

| 事件 | 触发条件 |
| :--- | :--- |
| 新证据产生 | 任何 `Evidence` 被提交 |
| 重放完成 | 任何 `Replay` 执行完成 |
| 冲突检测 | 检测到新冲突 |
| 证书颁发 | 新 `Certificate` 颁发 |
| 证书撤销 | `Certificate` 被撤销 |
| 定期衰减 | 每日 00:00 UTC（如无事件） |

### 6.2 更新流程

```text
1. 收集 Runtime 的所有证据
2. 统计证据完整性
3. 统计重放历史
4. 统计冲突记录
5. 统计证书历史
6. 计算基础分数
7. 应用时间衰减
8. 更新信任状态
9. 记录信任历史
```

### 6.3 信任历史记录

每次信任分数更新 **MUST** 记录：

```json
{
  "runtime_id": "runtime-openclaw-2026-07-05",
  "timestamp": "2026-07-05T10:00:00.000Z",
  "trust_score": 0.87,
  "base_score": 0.92,
  "decay_factor": 0.95,
  "state": "HIGH",
  "components": {
    "evidence_integrity": 0.92,
    "replay_consistency": 0.88,
    "conflict_record": 0.90,
    "certification_history": 0.80
  },
  "trigger_event": "NEW_EVIDENCE"
}
```

## 7. 示例

### 7.1 基础信任分数计算示例

**Runtime A**：

| 维度 | 值 | 权重 | 贡献 |
| :--- | :--- | :--- | :--- |
| 证据完整性 | 0.95 | 0.35 | 0.3325 |
| 重放一致性 | 0.90 | 0.30 | 0.2700 |
| 冲突记录 | 0.80 | 0.20 | 0.1600 |
| 认证历史 | 0.60 | 0.15 | 0.0900 |
| **合计** | | | **0.8525** |

`BaseScore = 0.8525`

**时间衰减**（30 天无活动）：

```text
Decay_Factor = e^(-0.01 × 30) = 0.7408
Trust_Score = 0.8525 × 0.7408 = 0.6316
```

### 7.2 冲突影响示例

**Runtime B**（基础分数 0.85）：

- 检测到 2 次证据冲突 → -0.2
- 检测到 1 次重放冲突 → -0.15
- 总计扣分：-0.35

```text
Adjusted_Score = 0.85 - 0.35 = 0.50
```

**信任状态**：从 `STABLE` 降级为 `LOW`

## 8. 参考

### 8.1 规范性引用

- RFC 2119 — Key words for use in RFCs to Indicate Requirement Levels
- OBEP-0001 — Evidence Schema v1.0
- OBEP-0002 — Replay Protocol v1.0
- OBEP-0004 — Certificate Schema v1.0

### 8.2 信息性引用

- Jøsang, A. (2007). "A logic for uncertain probabilities." International Journal of Uncertainty, Fuzziness and Knowledge-Based Systems.
- Lamport, L. (1978). "Time, clocks, and the ordering of events in a distributed system." Communications of the ACM.

## 9. 冻结声明

本规范已冻结为 v1.0，生效日期：2026-07-05。

任何变更必须通过 OBEP 流程进行，并保持向后兼容。

**冻结状态**：✅ 已冻结

**下次审查**：2027-07-05 或 严重安全漏洞发现时。

---

*本规范由 OpenBase Specification Committee 维护。*
```

---


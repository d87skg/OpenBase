# Replay Protocol v1.0

## 1. 目的

本规范定义 OpenBase 重放（Replay）协议，即从证据链（Evidence Chain）重建 Agent 执行过程的标准方法。

## 2. 核心概念

### 2.1 重放定义

**重放（Replay）** 是指从一组有序的证据链中，重建 Agent 执行过程的状态序列、动作序列和因果依赖关系的过程。

### 2.2 重放前置条件

| 条件 | 描述 |
| :--- | :--- |
| 证据链完整 | 所有证据的 parent_id 形成连通 DAG |
| 证据链已签名 | 每条证据的 proof.signature 有效 |
| 证据链无环 | 不存在循环依赖 |
| 证据链有序 | vector_clock 可比较 |

### 2.3 重放输入

证据数组，符合 Evidence Schema。

### 2.4 重放输出

{
  "replay_id": "replay-xxx",
  "status": "SUCCESS | PARTIAL | FAILED",
  "fidelity": "EXACT | LOGICAL | CAUSAL | STRUCTURAL",
  "timeline": [],
  "statistics": {}
}

## 3. 重放保真度等级

| 等级 | 描述 | 要求 |
| :--- | :--- | :--- |
| EXACT | 完全一致 | 状态、时间、顺序、输出完全相同 |
| LOGICAL | 逻辑一致 | 状态和顺序一致 |
| CAUSAL | 因果一致 | 因果顺序一致 |
| STRUCTURAL | 结构一致 | 证据结构一致 |

Runtime MUST 支持至少 CAUSAL 保真度。

## 4. 重放失败处理

| 错误码 | 描述 |
| :--- | :--- |
| EVIDENCE_CHAIN_INCOMPLETE | 证据链不完整 |
| SIGNATURE_INVALID | 签名无效 |
| HASH_CHAIN_BROKEN | 哈希链断裂 |
| CAUSAL_GRAPH_CYCLE | 因果图有环 |

## 5. 确定性要求

重放 MUST 是确定性的：同一证据链 → 同一重放输出。

## 6. 参考

- OBEP-0001 Evidence Schema
- OBEP-0003 Trust Model

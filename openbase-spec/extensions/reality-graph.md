# Reality Graph Extension v1.0

## 1. 目的

Reality Graph 是 OpenBase 的可选扩展，用于建模 Agent 执行过程中的事实网络，支持跨 Agent 的因果关系追溯和冲突检测。

## 2. 核心概念

Reality Graph 是一个有向图：

- **节点（Node）**：表示一个事实（Evidence、Trust、Certificate、Claim）
- **边（Edge）**：表示事实之间的关系

### 节点类型

| 类型 | 描述 |
| :--- | :--- |
| EVIDENCE | 证据节点 |
| TRUST | 信任节点 |
| CERTIFICATE | 证书节点 |
| CLAIM | 声明节点 |

### 边类型

| 类型 | 描述 |
| :--- | :--- |
| SUPPORTS | 支持关系 |
| DERIVES | 派生关系 |
| CONTRADICTS | 矛盾关系 |
| CAUSES | 因果关系 |

## 3. 数据结构

### 节点

{
  "node_id": "node-xxx",
  "type": "EVIDENCE",
  "source": "runtime-xxx",
  "content": {},
  "trust_score": 0.7,
  "timestamp": "2026-07-05T10:00:00Z",
  "provenance": {}
}

### 边

{
  "edge_id": "edge-xxx",
  "from": "node-xxx",
  "to": "node-yyy",
  "relation": "SUPPORTS",
  "weight": 0.8,
  "timestamp": "2026-07-05T10:00:00Z"
}

## 4. 查询能力

### 查询 Claim

POST /reality/query
{ "claim": "Execution X succeeded" }

返回：TRUE | FALSE | UNKNOWN + 置信度

### 冲突检测

GET /reality/conflicts
返回所有 CONTRADICTS 边

## 5. 与核心的关系

Reality Graph 是可选扩展，不依赖核心协议。可以独立启用或禁用。

## 6. 参考

- OBEP-0001 Evidence Schema
- OBEP-0003 Trust Model

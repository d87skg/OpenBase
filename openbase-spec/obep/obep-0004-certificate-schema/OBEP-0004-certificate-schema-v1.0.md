

---

```markdown
---
OBEP: 0004
Title: Certificate Schema v1.0
Status: Frozen
Version: 1.0.0
Date: 2026-07-05
Authors: OpenBase Specification Committee
Obsoletes: None
---

# OBEP-0004: Certificate Schema v1.0

## 1. 前言

### 1.1 目的

本规范定义 OpenBase 证书（Certificate）的数据结构、生命周期、颁发条件与验证规则。证书是对 Runtime 信任状态的形式化认证，用于证明 Agent 系统在特定时间点满足 OpenBase 标准。

### 1.2 范围

本规范涵盖：

- 证书对象的字段定义（必需/可选）
- 证书状态与生命周期
- 证书等级（Certificate Levels）
- 颁发条件与流程
- 验证规则
- 证书撤销

本规范不涵盖：

- 信任分数计算（参见 OBEP-0003 Trust Model）
- 证据的生成与验证（参见 OBEP-0001 Evidence Schema）
- Registry 操作（参见 OBEP-0005 Registry Protocol）

### 1.3 符合性关键词

本规范使用 RFC 2119 关键词：

- **MUST**：必须遵守，否则不符合标准
- **MUST NOT**：禁止行为
- **SHOULD**：建议遵守
- **SHOULD NOT**：不建议行为
- **MAY**：可选行为

## 2. 核心概念

### 2.1 证书定义

**证书（Certificate）** 是对 Runtime 在特定时间点满足 OpenBase 信任标准的正式认证。证书基于信任分数、证据链质量和一致性历史颁发，具有时间限制和可撤销性。

证书是信任状态的**可验证声明**，用于：

1. 审计与合规
2. 跨 Runtime 信任传递
3. 生态参与资格证明
4. 质量保证

### 2.2 证书生命周期

证书的生命周期由六个状态组成：

```text
┌────────────┐
│  PENDING   │   ← 申请中
└─────┬──────┘
      │ 审核通过
      ▼
┌────────────┐
│  ACTIVE    │   ← 有效证书
└─────┬──────┘
      │
      ├─────────── 过期
      │
      ▼
┌────────────┐
│  EXPIRED   │   ← 过期
└────────────┘
      │
      └─────────── 撤销
      ▼
┌────────────┐
│  REVOKED   │   ← 撤销
└────────────┘
      │
      └─────────── 归档
      ▼
┌────────────┐
│  ARCHIVED  │   ← 归档
└────────────┘
```

**状态定义**：

| 状态 | 描述 | 可转换状态 |
| :--- | :--- | :--- |
| `PENDING` | 证书申请已提交，正在审核 | `ACTIVE`, `REVOKED` |
| `ACTIVE` | 证书有效 | `EXPIRED`, `REVOKED` |
| `EXPIRED` | 证书已过期 | `ARCHIVED` |
| `REVOKED` | 证书已被撤销 | `ARCHIVED` |
| `ARCHIVED` | 证书已归档，不可再使用 | — |

### 2.3 证书等级

OpenBase 定义四个证书等级，反映 Runtime 的可信程度和功能完整性：

| 等级 | 描述 | 要求 | 信任分数阈值 |
| :--- | :--- | :--- | :--- |
| **BRONZE** | 初级认证 | 通过基础证据验证 | ≥ 0.60 |
| **SILVER** | 中级认证 | 通过证据 + 重放验证 | ≥ 0.75 |
| **GOLD** | 高级认证 | 通过证据 + 重放 + 信任模型验证 | ≥ 0.85 |
| **PLATINUM** | 最高认证 | 通过全部验证 + 长期一致性 | ≥ 0.95 |

## 3. 证书对象定义

### 3.1 对象概述

Certificate 是一个 JSON 对象：

```json
{
  "certificate_id": "cert-7f3a9b2c",
  "spec_version": "1.0",
  "runtime_id": "runtime-openclaw-2026-07-05",
  "runtime_name": "OpenClaw",
  "level": "GOLD",
  "status": "ACTIVE",
  "trust_score": 0.89,
  "issued_at": "2026-07-05T10:00:00.000Z",
  "expires_at": "2027-07-05T10:00:00.000Z",
  "revoked_at": null,
  "revocation_reason": null,
  "evidence_summary": {
    "total_count": 1234,
    "verified_count": 1234,
    "hash_chain_complete": true,
    "replay_success_rate": 0.97,
    "conflict_count": 0
  },
  "signature": "ed25519:..."
}
```

### 3.2 必需字段（Required Fields）

| 字段名 | 类型 | 约束 | 描述 |
| :--- | :--- | :--- | :--- |
| `certificate_id` | string | 格式: `cert-{8位hex}` 全局唯一 | 证书唯一标识符 |
| `spec_version` | string | 固定 `"1.0"` | 本规范版本 |
| `runtime_id` | string | 非空 | 所属 Runtime 标识符 |
| `runtime_name` | string | 非空 | Runtime 名称 |
| `level` | string | 必须为 BRONZE/SILVER/GOLD/PLATINUM | 证书等级 |
| `status` | string | 必须为 PENDING/ACTIVE/EXPIRED/REVOKED/ARCHIVED | 当前状态 |
| `trust_score` | number | [0.0, 1.0] | 颁发时的信任分数 |
| `issued_at` | string | RFC 3339 UTC 格式 | 颁发时间 |
| `expires_at` | string | RFC 3339 UTC 格式 | 过期时间 |
| `evidence_summary` | object | 见 3.4 | 颁发时的证据摘要 |

### 3.3 可选字段（Optional Fields）

| 字段名 | 类型 | 描述 |
| :--- | :--- | :--- |
| `revoked_at` | string | 撤销时间（RFC 3339 UTC 格式） |
| `revocation_reason` | string | 撤销原因 |
| `signature` | string | 颁发机构签名 |
| `metadata` | object | 额外元数据 |

### 3.4 证据摘要字段（`evidence_summary`）

| 子字段 | 类型 | 描述 |
| :--- | :--- | :--- |
| `total_count` | integer | 颁发时的证据总数 |
| `verified_count` | integer | 签名验证通过的证据数 |
| `hash_chain_complete` | boolean | 哈希链是否完整 |
| `replay_success_rate` | number | [0.0, 1.0] 重放成功率 |
| `conflict_count` | integer | 检测到的冲突次数 |

## 4. 颁发条件

### 4.1 最低条件（BRONZE）

颁发 `BRONZE` 证书，**MUST** 满足以下条件：

| 条件 | 要求 |
| :--- | :--- |
| Runtime 已注册 | 存在 `runtime_id` |
| 证据数量 | ≥ 50 条 |
| 签名验证率 | ≥ 95% |
| 哈希链完整性 | 100% |
| 信任分数 | ≥ 0.60 |
| 无未解决的严重冲突 | 冲突记录 < 3 |

### 4.2 升级条件

| 目标等级 | 额外要求 |
| :--- | :--- |
| `SILVER` | 证据数量 ≥ 200，重放成功率 ≥ 90%，信任分数 ≥ 0.75 |
| `GOLD` | 证据数量 ≥ 500，重放成功率 ≥ 95%，信任分数 ≥ 0.85，通过重放协议 |
| `PLATINUM` | 证据数量 ≥ 1000，重放成功率 ≥ 99%，信任分数 ≥ 0.95，长期一致性（30 天） |

### 4.3 证书有效期

| 等级 | 有效期 |
| :--- | :--- |
| `BRONZE` | 90 天 |
| `SILVER` | 180 天 |
| `GOLD` | 365 天 |
| `PLATINUM` | 365 天 |

### 4.4 颁发流程

```text
1. Runtime 提交证据链
2. 系统验证证据完整性
3. 系统计算信任分数
4. 系统检查等级条件
5. 生成证书对象
6. 签名证书
7. 注册证书到 Registry
8. 返回证书 ID
```

## 5. 证书验证

### 5.1 验证规则

验证证书时，**MUST** 检查：

| 验证项 | 检查方式 | 失败处理 |
| :--- | :--- | :--- |
| 证书签名 | 验证 Ed25519 签名 | 返回 `INVALID` |
| 证书状态 | 检查 `status` 是否为 `ACTIVE` | 返回 `EXPIRED`/`REVOKED` |
| 证书有效期 | 检查当前时间是否在 `issued_at` 与 `expires_at` 之间 | 返回 `EXPIRED` |
| Runtime 存在性 | 检查 `runtime_id` 在 Registry 中是否存在 | 返回 `INVALID` |
| 信任分数一致性 | 当前信任分数不低于颁发时分数 | 返回 `DEGRADED` |

### 5.2 验证结果

| 结果 | 描述 |
| :--- | :--- |
| `VALID` | 证书有效且可信任 |
| `EXPIRED` | 证书已过期 |
| `REVOKED` | 证书已被撤销 |
| `DEGRADED` | 信任分数已下降 |
| `INVALID` | 证书无效（签名错误或 Runtime 不存在） |

## 6. 证书撤销

### 6.1 撤销条件

证书 **MUST** 在以下情况下撤销：

| 条件 | 描述 | 优先级 |
| :--- | :--- | :--- |
| 严重违规 | 检测到证据篡改或签名伪造 | 最高 |
| 信任分数低于阈值 | 信任分数低于等级要求 | 高 |
| 频繁冲突 | 30 天内检测到 ≥ 5 次冲突 | 中 |
| Runtime 注销 | Runtime 已从 Registry 注销 | 中 |
| 重放失败率过高 | 30 天内重放失败率 > 10% | 中 |
| 证书升级/降级 | 颁发新证书 | 低 |

### 6.2 撤销流程

```text
1. 检测到撤销条件
2. 更新证书状态为 `REVOKED`
3. 记录撤销时间和原因
4. 更新信任状态为 `SUSPENDED`
5. 通知 Registry
6. 生成撤销记录
```

### 6.3 撤销记录格式

```json
{
  "revocation_id": "rev-7f3a9b2c",
  "certificate_id": "cert-7f3a9b2c",
  "runtime_id": "runtime-openclaw-2026-07-05",
  "reason": "Trust score dropped below threshold",
  "revoked_at": "2026-07-05T10:00:00.000Z",
  "trust_score_at_revocation": 0.45,
  "trigger_event": "TRUST_SCORE_THRESHOLD"
}
```

## 7. 证书与信任模型的关系

证书颁发 **MUST** 基于信任分数（OBEP-0003），但证书本身包含颁发时的信任分数快照，而非动态引用。

**信任分数与证书的关系**：

```text
信任分数 ──▶ 触发颁发条件 ──▶ 证书颁发
                                    │
                                    ▼
证书 ──▶ 持有者展示 ──▶ 第三方验证 ──▶ 信任决策
```

## 8. 示例

### 8.1 BRONZE 证书（颁发）

```json
{
  "certificate_id": "cert-00000001",
  "spec_version": "1.0",
  "runtime_id": "runtime-demo-001",
  "runtime_name": "Demo Runtime",
  "level": "BRONZE",
  "status": "ACTIVE",
  "trust_score": 0.65,
  "issued_at": "2026-07-05T10:00:00.000Z",
  "expires_at": "2026-10-03T10:00:00.000Z",
  "revoked_at": null,
  "revocation_reason": null,
  "evidence_summary": {
    "total_count": 50,
    "verified_count": 50,
    "hash_chain_complete": true,
    "replay_success_rate": 0.85,
    "conflict_count": 2
  },
  "signature": "ed25519:..."
}
```

### 8.2 PLATINUM 证书（颁发）

```json
{
  "certificate_id": "cert-00000002",
  "spec_version": "1.0",
  "runtime_id": "runtime-openclaw-2026-07-05",
  "runtime_name": "OpenClaw Reference Runtime",
  "level": "PLATINUM",
  "status": "ACTIVE",
  "trust_score": 0.97,
  "issued_at": "2026-07-05T10:00:00.000Z",
  "expires_at": "2027-07-05T10:00:00.000Z",
  "revoked_at": null,
  "revocation_reason": null,
  "evidence_summary": {
    "total_count": 1234,
    "verified_count": 1234,
    "hash_chain_complete": true,
    "replay_success_rate": 0.99,
    "conflict_count": 0
  },
  "signature": "ed25519:..."
}
```

### 8.3 证书验证结果（有效）

```json
{
  "certificate_id": "cert-00000001",
  "valid": true,
  "status": "VALID",
  "level": "BRONZE",
  "trust_score": 0.65,
  "issued_at": "2026-07-05T10:00:00.000Z",
  "expires_at": "2026-10-03T10:00:00.000Z",
  "current_trust_score": 0.68
}
```

### 8.4 证书验证结果（过期）

```json
{
  "certificate_id": "cert-00000001",
  "valid": false,
  "status": "EXPIRED",
  "reason": "Certificate expired on 2026-10-03T10:00:00.000Z"
}
```

## 9. 参考

### 9.1 规范性引用

- RFC 2119 — Key words for use in RFCs to Indicate Requirement Levels
- RFC 3339 — Timestamp Format
- OBEP-0001 — Evidence Schema v1.0
- OBEP-0003 — Trust Model v1.0
- OBEP-0005 — Registry Protocol v1.0
- Ed25519 — Edwards-curve Digital Signature Algorithm

### 9.2 信息性引用

- WebPKI — Public Key Infrastructure for the Web
- X.509 — ITU-T Standard for Public Key Certificates

## 10. 冻结声明

本规范已冻结为 v1.0，生效日期：2026-07-05。

任何变更必须通过 OBEP 流程进行，并保持向后兼容。

**冻结状态**：✅ 已冻结

**下次审查**：2027-07-05 或 严重安全漏洞发现时。

---

*本规范由 OpenBase Specification Committee 维护。*
```

---


# Trust Model v1.0

## 1. 目的

定义从证据链计算 Runtime 信任分数的标准方法。

## 2. 信任分数

信任分数范围 [0.0, 1.0]

| 分数范围 | 信任等级 |
| :--- | :--- |
| 0.90 - 1.00 | HIGH |
| 0.70 - 0.89 | MEDIUM |
| 0.40 - 0.69 | LOW |
| 0.00 - 0.39 | UNTRUSTED |

## 3. 信任状态

UNKNOWN → INITIAL → STABLE → HIGH
                            ↓
                        SUSPENDED → REVOKED

## 4. 评分维度

| 维度 | 权重 |
| :--- | :--- |
| 证据完整性 | 0.35 |
| 重放一致性 | 0.30 |
| 冲突记录 | 0.20 |
| 认证历史 | 0.15 |

BaseScore = Evidence_Integrity * 0.35 + Replay_Consistency * 0.30 + Conflict_Record * 0.20 + Certification_History * 0.15

## 5. 时间衰减

Decay_Factor = e^(-0.01 * Δt)
Trust_Score = BaseScore * Decay_Factor

## 6. 冲突类型

| 类型 | 信任影响 |
| :--- | :--- |
| EVIDENCE_CONFLICT | -0.1 分/次 |
| REPLAY_CONFLICT | -0.15 分/次 |
| STATEMENT_CONFLICT | -0.2 分/次 |
| TOOL_CONFLICT | -0.1 分/次 |

## 7. 信任历史记录

{
  "runtime_id": "runtime-xxx",
  "timestamp": "2026-07-05T10:00:00Z",
  "trust_score": 0.87,
  "state": "HIGH",
  "trigger_event": "NEW_EVIDENCE"
}

## 8. 参考

- OBEP-0001 Evidence Schema
- OBEP-0002 Replay Protocol
- OBEP-0004 Certificate Schema

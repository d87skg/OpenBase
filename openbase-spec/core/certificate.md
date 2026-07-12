# Certificate Schema v1.0

## 1. 目的

定义证书的数据结构、生命周期、颁发条件与验证规则。

## 2. 证书定义

证书是对 Runtime 满足 OpenBase 信任标准的正式认证。

证书等级：

| 等级 | 信任分数阈值 | 证据数量要求 |
| :--- | :--- | :--- |
| BRONZE | >= 0.60 | >= 50 |
| SILVER | >= 0.75 | >= 200 |
| GOLD | >= 0.85 | >= 500 |
| PLATINUM | >= 0.95 | >= 1000 |

## 3. 证书对象

{
  "certificate_id": "cert-xxx",
  "runtime_id": "runtime-xxx",
  "runtime_name": "OpenClaw",
  "level": "GOLD",
  "status": "ACTIVE",
  "trust_score": 0.89,
  "issued_at": "2026-07-05T10:00:00Z",
  "expires_at": "2027-07-05T10:00:00Z"
}

## 4. 证书生命周期

PENDING → ACTIVE → (EXPIRED | REVOKED)

## 5. 证书有效期

| 等级 | 有效期 |
| :--- | :--- |
| BRONZE | 90 天 |
| SILVER | 180 天 |
| GOLD | 365 天 |
| PLATINUM | 365 天 |

## 6. 证书撤销条件

- 严重违规（证据篡改、签名伪造）
- 信任分数低于阈值
- 频繁冲突（30 天内 >= 5 次）

## 7. 验证结果

| 结果 | 描述 |
| :--- | :--- |
| VALID | 证书有效 |
| EXPIRED | 已过期 |
| REVOKED | 已撤销 |
| INVALID | 无效 |

## 8. 参考

- OBEP-0001 Evidence Schema
- OBEP-0003 Trust Model
- OBEP-0005 Registry Protocol

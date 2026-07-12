# Registry Protocol v1.0

## 1. 目的

定义 Runtime 注册、证据提交、证书查询与信任分数获取的标准接口。

## 2. Runtime 注册

POST /runtimes/register
{
  "name": "OpenClaw",
  "version": "1.0.0",
  "vendor": "OpenBase",
  "runtime_class": "REFERENCE",
  "capabilities": ["execution", "evidence", "replay"]
}

Runtime 状态：ACTIVE | INACTIVE | SUSPENDED | DEPRECATED | REVOKED

## 3. 证据管理

POST /evidence
{
  "runtime_id": "runtime-xxx",
  "evidence": { ... }
}

GET /evidence/{id}
GET /evidence/execution/{id}
GET /evidence/runtime/{id}

## 4. 证书管理

POST /certificates/issue
{
  "runtime_id": "runtime-xxx",
  "level": "GOLD",
  "trust_score": 0.89
}

GET /certificates/{id}
GET /certificates/runtime/{id}
GET /certificates/runtime/{id}/latest

## 5. 信任分数

GET /trust/{runtime_id}
{
  "trust_score": 0.87,
  "trust_state": "HIGH",
  "evidence_count": 1234
}

GET /trust/ranking?limit=10

## 6. 事件通知

WebSocket 订阅：
{ "type": "subscribe", "events": ["EVIDENCE_SUBMITTED", "TRUST_UPDATED"] }

## 7. 参考

- OBEP-0001 Evidence Schema
- OBEP-0003 Trust Model
- OBEP-0004 Certificate Schema

# DSL Invariant Engine Extension v1.0

## 1. 目的

DSL Invariant Engine 是 OpenBase 的可选企业级扩展，用于通过声明式规则驱动系统裁决。

## 2. 核心概念

### 规则定义

rule EvidenceFirst:
    when TrustUpdate
    if exists Evidence BEFORE timestamp
    require TrustStable(window=5)
    then ACCEPT

### 规则结构

- **when**: 触发事件类型
- **if**: 条件表达式
- **require**: 不变性检查
- **then**: 裁决动作（ACCEPT | REJECT | REWRITE）

## 3. 规则执行

### 输入

{
  "proposal": { "state_type": "TrustUpdate", "payload": { "score": 0.8 } },
  "global_state": { "evidence": ["E1"], "trust": { "score": 0.8 } }
}

### 输出

{
  "decision": "ACCEPT",
  "rule": "EvidenceFirst",
  "reason": "All conditions satisfied"
}

## 4. 标准规则库

### evidence.dsl

rule EvidenceFirst:
    when TrustUpdate
    if exists Evidence BEFORE timestamp
    require TrustStable(window=5)
    then ACCEPT

### trust.dsl

rule TrustStability:
    when GraphUpdate
    require TrustStable(window=3)
    then ACCEPT

### cert.dsl

rule CertificateIssuance:
    when CertificateIssue
    require TrustStable(window=5)
    and no Conflict
    then ACCEPT

## 5. 编译流程

DSL → AST → IR → Runtime

## 6. 与核心的关系

DSL Invariant Engine 是企业级扩展，非核心必需组件。

## 7. 参考

- OBEP-0003 Trust Model
- OBEP-0007 Compatibility Policy

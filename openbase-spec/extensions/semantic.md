# Semantic Layer Extension v1.0

## 1. 目的

Semantic Layer 是 OpenBase 的可选扩展，用于将字符串世界升级为可推理的现实系统。

## 2. 核心概念

### 语义身份（Semantic Identity）

将任意文本转换为可计算的语义概念：

{
  "raw": "Test 1",
  "normalized": "test_1",
  "semantic_id": "SEM:test_1_xxx",
  "type": "CLAIM",
  "embedding": [0.2, 0.7, 0.3, ...]
}

### 语义归一化

不同表述 → 统一规范形式：
- "Test 1" → "test_1"
- "test-1" → "test_1"
- "execution test 1" → "execution_test_1"

## 3. 核心能力

### 归一化

POST /semantic/normalize
{ "text": "Test 1" }
返回：{ "normalized": "test_1" }

### 语义比较

POST /semantic/compare
{ "text_a": "Test 1", "text_b": "test-1" }
返回：{ "similarity": 0.95, "semantic_match": true }

### 相关概念查找

POST /semantic/related
{ "text": "LLM_CALL", "threshold": 0.7 }
返回：相关语义 ID 列表

## 4. 与核心的关系

Semantic Layer 是可选扩展，独立于核心协议。

## 5. 参考

- OBEP-0001 Evidence Schema
- OBEP-0006 Wire Protocol

# Test Suite Definitions

本目录包含各测试类别的 JSON 定义。

## 文件列表

| 文件 | 描述 | 测试数 |
| :--- | :--- | :--- |
| evidence_tests.json | 证据测试 | 5 |
| eplay_tests.json | 重放测试 | 5 |
| 	rust_tests.json | 信任测试 | 5 |
| certificate_tests.json | 证书测试 | 4 |
| egistry_tests.json | 注册表测试 | 4 |

## 测试格式

每个测试用例包含：

| 字段 | 描述 |
| :--- | :--- |
| id | 唯一标识符 |
| 
ame | 测试名称 |
| priority | P0/P1/P2 |
| description | 测试描述 |
| expected | 预期结果 |

*由 OpenBase Specification Committee 维护。*

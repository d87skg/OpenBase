# OpenBase Conformance Test Suite v1.0

本目录包含 OpenBase 协议的一致性测试套件，用于验证 Runtime 实现是否符合 OpenBase 标准。

## 目录结构

| 目录 | 描述 |
| :--- | :--- |
| suite/ | 测试用例定义 |
| 	est-vectors/ | 测试向量数据 |
| eports/ | 测试报告输出 |

## 测试类别

| 类别 | 对应规范 |
| :--- | :--- |
| Evidence Tests | OBEP-0001 |
| Replay Tests | OBEP-0002 |
| Trust Tests | OBEP-0003 |
| Certificate Tests | OBEP-0004 |
| Registry Tests | OBEP-0005 |

## 使用方法

`ash
openbase test --suite conformance
openbase test --category evidence
openbase test --priority P0
通过标准
等级    P0 通过率    P1 通过率    P2 通过率
PLATINUM    100%    100%    ≥ 95%
GOLD    100%    ≥ 98%    ≥ 90%
SILVER    100%    ≥ 95%    ≥ 80%
BRONZE    100%    ≥ 90%    ≥ 70%
由 OpenBase Specification Committee 维护。

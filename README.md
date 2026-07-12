# OpenBase

> OpenBase is an Open Trust Protocol for AI Agents.

OpenBase 是一个面向 AI Agent 的开放信任协议，用于定义 Agent 执行过程中证据记录、重放验证、信任评分与证书颁发的统一标准。

## 核心定位

OpenBase 不是 Framework，不是 Runtime，不是 SDK，而是：

- 定义 AI Agent 之间如何建立信任的**开放协议**
- 提供证据格式、重放验证、信任评分和证书颁发的**标准规范**
- 支持跨运行时、跨框架、跨语言的**互操作性**

## 架构
spec/ ← 核心规范 (OBS, Evidence, Replay, Conformance)
reference/ ← 参考实现 (validators)
conformance/ ← 一致性工具 (openbase-certify)
runtime/ ← 原生运行时 (OpenClaw)

text

## 目录结构

| 目录 | 描述 |
| :--- | :--- |
| spec/ | **核心规范** — 协议标准定义 |
| reference/ | **参考实现** — 证明标准可运行 |
| conformance/ | **一致性测试** — 验证实现是否符合标准 |
| runtime/ | **原生运行时** — OpenClaw |

## SDKs

- **Traccia** (Python): `pip install traccia-sdk`
- More SDKs coming (Rust, TypeScript, Go)

## 核心规范

| 规范 | 描述 | 状态 |
| :--- | :--- | :--- |
| OBS | 规范事件词汇表 | ✅ 冻结 |
| Evidence | 证据数据结构、签名、哈希链 | ✅ 冻结 |
| Replay | 执行重放、因果图、保真度 | ✅ 冻结 |
| Conformance | 一致性验证与认证 | ✅ 冻结 |

> 详细规范见 spec/

## 扩展规范

| 扩展 | 描述 | 状态 |
| :--- | :--- | :--- |
| Reality Graph | Agent 事实网络建模 | 草案 |
| Semantic Layer | 语义归一化与嵌入 | 草案 |
| DSL Invariant | 规则驱动裁决引擎 | 草案 |

## 快速开始

### 1. 安装 Traccia SDK

```bash
pip install traccia-sdk
2. 拦截 Agent 生成证据
bash
traccia intercept -- python your_agent.py
3. 验证证据包
bash
python conformance/certify.py task.evidence
Badge
Add to any OpenBase-certified agent:

https://img.shields.io/badge/OpenBase-Certified-00AA00

markdown
[![OpenBase Certified](https://img.shields.io/badge/OpenBase-Certified-00AA00)](https://github.com/d87skg/OpenBase)
版本
规范版本：v1.0.0

状态：已冻结

冻结日期：2026-07-05

许可
Apache License 2.0
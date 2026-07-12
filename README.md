# OpenBase

> OpenBase is an Open Trust Protocol for AI Agents.

OpenBase 是一个面向 AI Agent 的开放信任协议，用于定义 Agent 执行过程中证据记录、重放验证、信任评分与证书颁发的统一标准。

## 核心定位

OpenBase 不是 Framework，不是 Runtime，不是 SDK，而是：

- 定义 AI Agent 之间如何建立信任的**开放协议**
- 提供证据格式、重放验证、信任评分和证书颁发的**标准规范**
- 支持跨运行时、跨框架、跨语言的**互操作性**

## 目录结构

| 目录 | 描述 |
| :--- | :--- |
| openbase-spec/ | **核心规范** — 协议标准定义 |
| openclaw/ | **参考实现** — 证明标准可运行 |
| traccia/ | **SDK + CLI** — 开发者工具链 |
| adapters/ | **适配器** — 与外部框架的桥接 |
| conformance/ | **一致性测试** — 验证实现是否符合标准 |
| docs/ | **文档** — 用户指南和架构说明 |
| scripts/ | **工具脚本** — 开发和测试辅助 |
| examples/ | **示例** — 使用案例 |

## 核心规范

| 规范 | 描述 | 状态 |
| :--- | :--- | :--- |
| Evidence | 证据数据结构、签名、哈希链 | ✅ 冻结 |
| Replay | 执行重放、因果图、保真度 | ✅ 冻结 |
| Registry | Runtime 注册、证据提交、信任查询 | ✅ 冻结 |
| Certificate | 证书生命周期、等级、撤销 | ✅ 冻结 |
| Trust | 信任模型、评分维度、时间衰减 | ✅ 冻结 |

> 详细规范见 openbase-spec/core/

## 扩展规范

| 扩展 | 描述 | 状态 |
| :--- | :--- | :--- |
| Reality Graph | Agent 事实网络建模 | 草案 |
| Semantic Layer | 语义归一化与嵌入 | 草案 |
| DSL Invariant | 规则驱动裁决引擎 | 草案 |

> 扩展规范见 openbase-spec/extensions/

## 快速开始

### 1. 初始化项目

```bash
openbase init my-project
cd my-project
```

### 2. 运行 Agent

```bash
openbase run agents/main.py
```

### 3. 查看信任评分

```bash
openbase trust ranking
```

### 4. 颁发证书

```bash
openbase certificate issue --level BRONZE
```

## CLI 命令参考

| 命令 | 描述 |
| :--- | :--- |
| `openbase init [name]` | 初始化 OpenBase 项目 |
| `openbase run <agent_path>` | 运行 Agent 并记录证据 |
| `openbase replay <evidence_id>` | 重放 Agent 执行过程 |
| `openbase test <evidence_id>` | 验证证据完整性 |
| `openbase certificate issue` | 颁发信任证书 |
| `openbase trust ranking` | 查看信任评分排名 |
| `openbase runtime register` | 注册 Runtime |

### Init 选项

```
openbase init [name] [--force]
  name      项目名称 (默认: my-openbase-project)
  --force   覆盖已存在的目录
```

### Certificate 选项

```
openbase certificate issue [--runtime-id ID] [--level LEVEL] [--evidence-dir DIR] [--output-dir DIR]
  --runtime-id     Runtime ID
  --level          证书等级: BRONZE | SILVER | GOLD | PLATINUM (默认: BRONZE)
  --evidence-dir   证据目录 (默认: ./evidence)
  --output-dir     证书输出目录 (默认: ./reports)
```

## 版本

- 规范版本：v1.0.0
- 状态：已冻结
- 冻结日期：2026-07-05

## 许可

Apache License 2.0

本结构由 OpenBase Specification Committee 维护。
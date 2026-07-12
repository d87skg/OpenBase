# OpenBase 项目结构 (v1.0)

**更新日期**: 2026-07-05

---

## 根目录

\\\
D:\OpenBase\
├── adapters/              # 适配器骨架
├── config/                # 配置文件
├── conformance/           # 一致性测试套件
├── docs/                  # 文档中心
├── examples/              # 示例代码
├── openbase-spec/         # 核心规范 (协议标准)
├── openclaw/              # Reference Runtime
├── reports/               # 报告输出
├── scripts/               # 工具脚本
├── sdk/                   # SDK (预留)
└── traccia/               # SDK + CLI
\\\

---

## 1. openbase-spec/ (规范层)

\openbase-spec/\ 是 OpenBase 协议标准的唯一权威来源。

\\\
openbase-spec/
├── core/                          # 核心规范 (冻结)
│   ├── README.md                  # 核心规范入口
│   ├── certificate.md             # 证书规范
│   ├── domain-model.md            # 领域模型
│   ├── evidence.md                # 证据规范
│   ├── layer-contract.md          # 层契约
│   ├── registry.md                # 注册表协议
│   ├── replay.md                  # 重放协议
│   └── trust.md                   # 信任模型
│
├── extensions/                    # 扩展规范
│   ├── README.md
│   ├── dsl.md                     # DSL Invariant Engine
│   ├── reality-graph.md           # Reality Graph
│   ├── semantic.md                # Semantic Layer
│   ├── dsl/                       # DSL 实现 (历史)
│   ├── examples/                  # 示例 (历史)
│   ├── registry/                  # Registry 实现 (历史)
│   └── schemas/                   # Schema 定义 (历史)
│
├── obep/                          # OBEP 提案
│   ├── obep-0001-evidence-schema/
│   ├── obep-0002-replay-protocol/
│   ├── ...
│   └── obep-0010-governance/
│
├── governance/                    # 治理文档
│   ├── FOUNDING.md
│   ├── STATUS.md
│   ├── charter.md
│   ├── canon/
│   ├── manifesto/
│   └── ...
│
├── adapter/                       # 适配器规范 (预留)
├── conformance/                   # 一致性规范 (预留)
├── historical/                    # 历史资产 (旧版文档)
└── reference/                     # 参考规范 (预留)
\\\

---

## 2. openclaw/ (Reference Runtime)

\openclaw/\ 是 OpenBase 的参考实现，证明协议可运行。

\\\
openclaw/
├── runtime/                       # 运行时核心
│   ├── engines/                   # 引擎实现
│   │   ├── execution/
│   │   ├── evidence/
│   │   ├── replay/
│   │   ├── verification/
│   │   ├── determinism/
│   │   └── certification/
│   └── registry/                  # Registry 实现
│
├── cmd/                           # CLI 命令 (待实现)
├── pkg/                           # 公共包
├── reference/                     # 参考组件
└── tests/                         # 测试
\\\

---

## 3. traccia/ (SDK + CLI)

\	raccia/\ 是开发者工具链。

\\\
traccia/
├── cmd/                           # CLI 命令入口
├── pkg/                           # SDK 核心包
│   ├── client/                    # Registry 客户端
│   ├── evidence/                  # 证据处理
│   ├── trust/                     # 信任查询
│   ├── cert/                      # 证书管理
│   └── plugins/                   # 插件
└── README.md
\\\

---

## 4. adapters/ (适配器)

\dapters/\ 存放各框架适配器骨架。

\\\
adapters/
├── openai/
├── anthropic/
├── langchain/
├── langgraph/
├── crewai/
└── mcp/
\\\

---

## 5. conformance/ (一致性测试)

\conformance/\ 存放一致性测试套件 (待实现)。

\\\
conformance/
├── suite/                         # 测试套件
├── test-vectors/                  # 测试向量
└── reports/                       # 测试报告
\\\

---

## 6. docs/ (文档中心)

\docs/\ 存放用户文档。

\\\
docs/
├── getting-started/               # 快速入门
├── architecture/                  # 架构文档
├── api/                           # API 文档
└── examples/                      # 示例
\\\

---

## 7. scripts/ (工具脚本)

\scripts/\ 存放开发工具脚本。

\\\
scripts/
├── aes_report.py
├── demo.sh
├── generate_keys.py
├── generate_report.sh
├── openbase
├── reset_and_demo.sh
├── run_all_tests.py
├── setup_all.sh
├── start.sh
├── test_*.py
└── verify_evidence.py
\\\

---

## 规范版本

| 规范 | 版本 | 状态 | 冻结日期 |
| :--- | :--- | :--- | :--- |
| Evidence | v1.0.0 | 已冻结 | 2026-07-05 |
| Replay | v1.0.0 | 已冻结 | 2026-07-05 |
| Registry | v1.0.0 | 已冻结 | 2026-07-05 |
| Certificate | v1.0.0 | 已冻结 | 2026-07-05 |
| Trust | v1.0.0 | 已冻结 | 2026-07-05 |
| Reality Graph | v1.0.0 | 草案 | — |
| Semantic | v1.0.0 | 草案 | — |
| DSL | v1.0.0 | 草案 | — |

---

*本结构由 OpenBase Specification Committee 维护。*

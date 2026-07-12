
---

```markdown
---
OBEP: 0009
Title: Versioning Policy v1.0
Status: Frozen
Version: 1.0.0
Date: 2026-07-05
Authors: OpenBase Specification Committee
Obsoletes: None
---

# OBEP-0009: Versioning Policy v1.0

## 1. 前言

### 1.1 目的

本政策定义 OpenBase 所有可版本化资产的版本管理规则，包括版本号格式、发布周期、生命周期管理、兼容性承诺和版本废弃策略。版本管理是 OpenBase 生态系统长期稳定演进的**基础治理机制**。

### 1.2 范围

本政策涵盖：

- 版本号格式与语义
- 版本发布周期
- 版本生命周期管理
- 版本兼容性承诺
- 版本废弃（End of Life）策略
- 版本发布流程
- 文档版本管理
- 版本信息查询

本政策不涵盖：

- 具体协议定义（参见 OBEP-0001 ~ OBEP-0006）
- 兼容性细节（参见 OBEP-0007 Compatibility Policy）
- 治理结构（参见 OBEP-0010 Governance Model）

### 1.3 符合性关键词

本政策使用 RFC 2119 关键词：

- **MUST**：必须遵守
- **MUST NOT**：禁止行为
- **SHOULD**：建议遵守
- **SHOULD NOT**：不建议行为
- **MAY**：可选行为

## 2. 版本号定义

### 2.1 语义化版本号

所有 OpenBase 可版本化资产 **MUST** 遵循语义化版本 2.0.0 格式：

```text
MAJOR.MINOR.PATCH
```

| 组件 | 含义 | 变更条件 |
| :--- | :--- | :--- |
| **MAJOR** | 主要版本 | 破坏性变更（Breaking Changes） |
| **MINOR** | 次要版本 | 新增功能，向后兼容 |
| **PATCH** | 补丁版本 | 缺陷修复，向后兼容 |

### 2.2 版本号示例

| 版本号 | 含义 | 说明 |
| :--- | :--- | :--- |
| `1.0.0` | 初始版本 | 第一个稳定版本 |
| `1.0.1` | 补丁版本 | 修复缺陷，无新功能 |
| `1.1.0` | 次要版本 | 新增功能，向后兼容 |
| `2.0.0` | 主要版本 | 破坏性变更 |

### 2.3 预发布版本

预发布版本 **MAY** 使用以下格式：

```text
MAJOR.MINOR.PATCH-{预发布标识}.{序号}
```

| 预发布标识 | 含义 | 说明 |
| :--- | :--- | :--- |
| `alpha.N` | 内部测试版 | 功能不完整 |
| `beta.N` | 公开测试版 | 功能完整，可能存在缺陷 |
| `rc.N` | 发布候选版 | 候选版本，测试稳定 |

**示例**：

```text
1.0.0-alpha.1
1.0.0-beta.2
1.0.0-rc.1
```

## 3. 版本适用范围

### 3.1 可版本化资产

| 资产 | 版本号独立 | 初始版本 | 版本同步 |
| :--- | :--- | :--- | :--- |
| **核心协议规范** | ✅ 是 | 1.0.0 | 相互独立 |
| Evidence Schema | ✅ 是 | 1.0.0 | 独立 |
| Trust Model | ✅ 是 | 1.0.0 | 独立 |
| Replay Protocol | ✅ 是 | 1.0.0 | 独立 |
| Certificate Schema | ✅ 是 | 1.0.0 | 独立 |
| Registry Protocol | ✅ 是 | 1.0.0 | 独立 |
| Wire Protocol | ✅ 是 | 1.0.0 | 独立 |
| **API** | ✅ 是 | v1 | 通过 URL 版本化 |
| **SDK** | ✅ 是 | 1.0.0 | 独立 |
| Python SDK | ✅ 是 | 1.0.0 | 独立 |
| TypeScript SDK | ✅ 是 | 1.0.0 | 独立 |
| Go SDK | ✅ 是 | 1.0.0 | 独立 |
| Rust SDK | ✅ 是 | 1.0.0 | 独立 |
| **参考实现** | ✅ 是 | 1.0.0 | 独立 |
| OpenClaw Runtime | ✅ 是 | 1.0.0 | 独立 |
| **一致性测试套件** | ✅ 是 | 1.0.0 | 独立 |

### 3.2 版本号同步策略

| 关系 | 同步策略 | 说明 |
| :--- | :--- | :--- |
| 协议 → SDK | SDK 版本独立，支持多个协议版本 | SDK **SHOULD** 支持多个协议版本 |
| 协议 → 参考实现 | 参考实现版本独立，声称支持的协议版本 | 参考实现 **SHOULD** 声明支持的协议版本 |
| 协议 → 测试套件 | 测试套件版本与协议版本对应 | 测试套件 **SHOULD** 与协议版本同步 |

### 3.3 版本声明位置

每个版本化资产 **MUST** 在以下位置声明版本：

| 资产类型 | 版本声明位置 | 说明 |
| :--- | :--- | :--- |
| 协议规范 | 文档元数据 `Version:` | Markdown 文档头部 |
| Schema | `spec_version` 字段 | JSON 数据字段 |
| API | URL 路径 `/v{MAJOR}/` | 使用 URL 版本化 |
| SDK | `pyproject.toml` / `package.json` | 包配置文件 |
| 参考实现 | `--version` 标志 | 命令行参数 |
| 测试套件 | 测试报告 `version` 字段 | JSON 报告 |

## 4. 版本发布周期

### 4.1 发布频率

| 版本类型 | 发布频率 | 说明 |
| :--- | :--- | :--- |
| **MAJOR** | 每 12-24 个月 | 破坏性变更，需提前通知 |
| **MINOR** | 每 3-6 个月 | 新功能，向后兼容 |
| **PATCH** | 按需（通常每月） | 缺陷修复，向后兼容 |
| **SECURITY** | 立即（按需） | 安全修复 |

### 4.2 发布流程

```text
1. 版本规划
   ├── 收集需求
   ├── 确定版本范围
   └── 创建版本计划
   ↓
2. 开发
   ├── 实现新功能/修复
   ├── 更新文档
   └── 编写测试
   ↓
3. 测试
   ├── 运行一致性测试
   ├── 验证向后兼容性
   └── 修复发现的问题
   ↓
4. 发布候选
   ├── 标记为 RC 版本
   ├── 社区评审
   └── 收集反馈
   ↓
5. 正式发布
   ├── 标记版本
   ├── 生成发布说明
   ├── 更新文档
   ├── 通知社区
   └── 更新 Registry
```

## 5. 版本生命周期

### 5.1 版本生命周期阶段

```text
┌────────────┐
│  Development│   ← 开发中
└──────┬─────┘
       ▼
┌────────────┐
│  Pre-Release│   ← 预发布 (alpha/beta/rc)
└──────┬─────┘
       ▼
┌────────────┐
│  Released  │   ← 正式发布
└──────┬─────┘
       │
       ├─────────────────────────────────┐
       ▼                                 ▼
┌────────────┐                   ┌────────────┐
│   Active   │                   │   EOL      │
│   Support  │                   │   (End of  │
│   Period   │                   │   Life)    │
└────────────┘                   └────────────┘
```

### 5.2 版本生命周期阶段定义

| 阶段 | 描述 | 支持范围 |
| :--- | :--- | :--- |
| **Development** | 开发中，未发布 | 无 |
| **Pre-Release** | 预发布版本（alpha/beta/rc） | 有限支持 |
| **Released** | 已正式发布 | 完整支持 |
| **Active Support** | 积极支持阶段 | 安全修复、缺陷修复、新功能 |
| **Maintenance** | 维护阶段 | 安全修复、关键缺陷修复 |
| **EOL** | 生命周期结束 | 无支持 |

### 5.3 版本支持时长

| 版本类型 | Active Support | Maintenance | EOL |
| :--- | :--- | :--- | :--- |
| **当前 MAJOR 版本** | 无限 | 发布后 24 个月 | 下一个 MAJOR 发布后 12 个月 |
| **前一个 MAJOR 版本** | 发布后 12 个月 | 发布后 24 个月 | 发布后 36 个月 |
| **前两个 MAJOR 版本** | 发布后 6 个月 | 发布后 12 个月 | 发布后 18 个月 |
| **更早版本** | — | — | 已 EOL |

### 5.4 版本状态标记

每个版本 **MUST** 在文档和 Registry 中标记状态：

| 状态 | 含义 | 示例 |
| :--- | :--- | :--- |
| `active` | 当前活跃版本 | `1.0.0` (active) |
| `maintenance` | 维护版本 | `0.9.0` (maintenance) |
| `deprecated` | 已弃用，建议升级 | `0.8.0` (deprecated) |
| `eol` | 生命周期结束 | `0.7.0` (eol) |

## 6. 版本兼容性承诺

### 6.1 协议版本兼容性

| 组件 | MAJOR 变更 | MINOR 变更 | PATCH 变更 |
| :--- | :--- | :--- | :--- |
| Evidence Schema | ❌ 不兼容 | ✅ 向后兼容 | ✅ 向后兼容 |
| Trust Model | ❌ 不兼容 | ✅ 向后兼容 | ✅ 向后兼容 |
| Replay Protocol | ❌ 不兼容 | ✅ 向后兼容 | ✅ 向后兼容 |
| Certificate Schema | ❌ 不兼容 | ✅ 向后兼容 | ✅ 向后兼容 |
| Registry Protocol | ❌ 不兼容 | ✅ 向后兼容 | ✅ 向后兼容 |
| Wire Protocol | ❌ 不兼容 | ✅ 向后兼容 | ✅ 向后兼容 |

### 6.2 API 版本兼容性

```text
/v1/evidence          ← v1 API
/v2/evidence          ← v2 API（破坏性变更）
/v1 和 /v2 同时支持   ← 兼容性策略
```

### 6.3 版本互操作性

| 场景 | 兼容性 | 要求 |
| :--- | :--- | :--- |
| 旧客户端 → 新服务端 | ✅ 向前兼容 | 服务端必须支持旧版本 |
| 新客户端 → 旧服务端 | ✅ 向后兼容 | 客户端必须支持旧版本 |
| 旧客户端 → 旧服务端 | ✅ 完全兼容 | 无问题 |
| 新客户端 → 新服务端 | ✅ 完全兼容 | 无问题 |

### 6.4 向后兼容承诺

OpenBase **承诺**在 MAJOR 版本内保持向后兼容：

1. **Schema 向后兼容**：旧版本数据必须能在新版本中读取。
2. **API 向后兼容**：旧版本 API 请求必须在新版本中正常处理。
3. **协议向后兼容**：旧版本消息必须能被新版本正确解析。
4. **行为向后兼容**：旧版本行为必须在新版本中保持一致。

## 7. 版本废弃（End of Life）

### 7.1 EOL 条件

版本在以下情况下**MUST**被标记为 EOL：

| 条件 | 说明 | 触发时间 |
| :--- | :--- | :--- |
| 超过支持期限 | 超出 Maintenance 阶段 | 见 5.3 |
| 安全漏洞无法修复 | 无法提供安全补丁 | 立即 |
| 技术债务过重 | 维护成本过高 | 由委员会决定 |
| 新版本发布 | 新 MAJOR 版本发布后 12 个月 | 新版本发布后 12 个月 |

### 7.2 EOL 通知流程

```text
1. 宣布 EOL
   ├── 在文档中标记
   ├── 在 Registry 中标记
   ├── 发送邮件通知
   └── 在 GitHub 发布公告
   ↓
2. 过渡期（3 个月）
   ├── 提供升级指南
   ├── 继续修复关键缺陷
   └── 不添加新功能
   ↓
3. EOL 生效
   ├── 停止所有支持
   ├── 关闭 Issues
   ├── 归档文档
   └── 从 Registry 移除
```

### 7.3 EOL 标记

**文档标记**：

```markdown
> **Status: End of Life (EOL)**
>
> 此版本已于 2027-01-01 到达生命周期结束。
> 请升级到最新版本。
```

**Registry 标记**：

```json
{
  "version": "1.0.0",
  "status": "eol",
  "eol_date": "2027-01-01",
  "recommended_version": "2.0.0"
}
```

## 8. 版本发布流程

### 8.1 发布准备

| 任务 | 负责人 | 时间要求 |
| :--- | :--- | :--- |
| 更新文档 | 规范委员会 | 发布前 1 周 |
| 运行一致性测试 | 测试团队 | 发布前 1 周 |
| 更新 CHANGELOG | 规范委员会 | 发布前 1 周 |
| 安全审核 | 安全团队 | 发布前 2 周 |
| 社区通知 | 社区经理 | 发布前 1 周 |

### 8.2 发布检查清单

**发布前检查清单**：

- [ ] 所有测试通过
- [ ] 文档已更新
- [ ] CHANGELOG 已更新
- [ ] 版本号已更新
- [ ] 向后兼容性已验证
- [ ] 安全审核已完成
- [ ] 社区已通知

**发布后检查清单**：

- [ ] 版本已标记（Git tag）
- [ ] 发布说明已生成
- [ ] 文档已发布
- [ ] Registry 已更新
- [ ] SDK 已发布（如适用）
- [ ] 社区已通知（发布公告）

## 9. 文档版本管理

### 9.1 文档版本化

所有规范文档 **MUST** 包含版本信息：

```markdown
---
Version: 1.0.0
Status: Frozen
Date: 2026-07-05
---
```

### 9.2 文档版本变更

| 文档变更类型 | 版本更新 | 说明 |
| :--- | :--- | :--- |
| 内容更正 | PATCH | 修复错误、改进措辞 |
| 新增章节 | MINOR | 向后兼容，不影响现有内容 |
| 删除章节 | MAJOR | 破坏性变更 |
| 重大修改 | MAJOR | 影响实现的内容变更 |

## 10. 版本信息查询

### 10.1 查询方式

| 方式 | 命令/端点 | 返回 |
| :--- | :--- | :--- |
| CLI | `openbase version` | 当前版本 |
| API | `GET /version` | 服务端版本 |
| Registry | `GET /versions` | 所有支持版本 |
| SDK | `openbase.__version__` | SDK 版本 |

### 10.2 版本信息格式

```json
{
  "protocol_version": "1.0.0",
  "api_version": "v1",
  "registry_version": "1.0.0",
  "sdk_version": "1.0.0",
  "supported_versions": ["1.0.0", "1.1.0", "1.2.0"],
  "deprecated_versions": ["0.9.0"],
  "eol_versions": ["0.8.0"]
}
```

## 11. 版本发布示例

### 11.1 MAJOR 版本发布

**版本**：2.0.0

**发布说明**：

```markdown
# OpenBase 2.0.0 Release Notes

## Breaking Changes

- Evidence Schema: `actor` 字段改为 `actors` 数组
- Trust Model: 信任分数计算权重调整
- API: `/v1` 路径变更为 `/v2`

## Migration Guide

- 将 `actor` 替换为 `actors` 数组
- 重新计算信任分数（权重变化）
- 更新 API 路径

## Timeline

- 弃用通知：2026-01-01
- 2.0.0 发布：2026-07-05
- 1.x EOL：2027-07-05
```

### 11.2 MINOR 版本发布

**版本**：1.1.0

**发布说明**：

```markdown
# OpenBase 1.1.0 Release Notes

## New Features

- 新增 `metadata.cost_usd` 字段
- 新增 `REPLAY` 事件类型
- 新增 `/trust/ranking` API 端点

## Deprecations

- `metadata.tags` 字段将在 2.0.0 中移除（使用 `metadata.labels` 替代）

## Bug Fixes

- 修复哈希链验证中的边界条件
- 修复重放超时问题
```

### 11.3 PATCH 版本发布

**版本**：1.0.1

**发布说明**：

```markdown
# OpenBase 1.0.1 Release Notes

## Bug Fixes

- 修复 Evidence 签名验证中的内存泄漏
- 修复重放排序中的整数溢出
- 修复 Registry 查询性能问题

## Security

- 修复 CVE-2026-0001：签名验证绕过漏洞
```

## 12. 参考

### 12.1 规范性引用

- Semantic Versioning 2.0.0
- RFC 2119 — Key words for use in RFCs to Indicate Requirement Levels
- OBEP-0007 — Compatibility Policy v1.0
- OBEP-0010 — Governance Model v1.0

### 12.2 信息性引用

- Kubernetes Versioning Policy
- OpenTelemetry Versioning Policy
- Python PEP 440 — Version Identification and Dependency Specification

## 13. 冻结声明

本政策已冻结为 v1.0，生效日期：2026-07-05。

任何变更必须通过 OBEP 流程进行。

**冻结状态**：✅ 已冻结

**下次审查**：2027-07-05

---

*本政策由 OpenBase Specification Committee 维护。*
```

---

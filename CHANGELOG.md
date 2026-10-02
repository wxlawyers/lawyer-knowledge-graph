# 变更记录

> 技能版本规则见 [VERSIONING.md](VERSIONING.md)。每个技能的当前版本写在各自 `SKILL.md` 的 `version` 字段。
> 本文件按日期倒序记录；`2026-10-02` 之前的条目为版本体系启用时按 git 历史补记。

---

## 2026-10-02

### 技能版本体系启用（提交 `379d7bf` 之后的独立提交）

此前 39 个技能全部停留在初始版本（多数为 `1.0.0`），无法判断"哪个技能什么时候改过什么"。本次为当天已发生的变更补记版本号，并启用"改一次升一版 + 写变更记录"的规则。

建议今后每次改动都在同一次提交内完成版本提升与 CHANGELOG 更新。

### 第二档：技能内容补强（提交 `379d7bf`）

面向"内容还能用但不够强"的六个技能，对标 GitHub 同类仓库补能力。

| 技能 | 版本 | 变更 |
|------|------|------|
| legal-analysis-pitfalls | 1.1.0 → 1.2.0 | 新增《法条引用核验协议》：三层校验（存在性/内容一致性/时效性）、三种状态（已核验/待核实/阻断）、核验报告格式、六组一致性检查；新增脚本 `scripts/scan_citations.py` 自动抽取法条引用生成核验清单 |
| contract-review | 1.0.0 → 1.1.0 | 从 87 行扩为完整流程：立场分流（买方/卖方视角决定什么算风险）、预审清单（空白字段/缺失附件/签署状态）、缺失条款检查、文件内部一致性检查、谈判优先级表；各类合同清单拆到 `references/contract-type-checklists.md`（九类合同） |
| evidence-organization | 1.0.0 → 1.1.0 | 新增双视图输出（按来源/按证明目的）、证据卡片字段表、聊天记录**强制标注发言人**、置信度分级、按法律关系的证据缺口表 |
| trial-preparation | 1.0.0 → 1.1.0 | 新增《庭审记录》交付链路：十个一级节点固定、子标题不加阿拉伯序号、命名规范、填写门禁；模板 `references/hearing-record-template.md` 可直接导入 WPS 生成思维导图 |
| compensation-calculator | 2.0.0 → 2.1.0 | 新增第四个模块 LPR 分段利息，脚本 `scripts/lpr_interest.py`（不内置利率数据，强制现查现填）；修复 `standards.md`、`formulas.md` 两处失效引用 |
| client-communication | 1.0.0 → 1.1.0 | 新增「对内 vs 对外」分界与五条脱敏红线；四类对外交付物模板（服务计划书/工作通报/决策辅助清单/庭审简报）+ 结案报告 + 发送前自查表 |

### 第一档：工具口径校准（提交 `873c19a`）

修正技能里指向已不再使用的工具与过时口径的引用。

| 技能 | 版本 | 变更 |
|------|------|------|
| legal-research | 1.0.0 → 1.1.0 | 检索口径由「元典为主」改为「北大法宝为主 + 元典交叉核验」；工具表改为按用途分组并指向 `pkulaw-mcp-*` 技能族；报告来源标注、每日速报流程、降级策略同步更新 |
| case-search-sources | 删除 | 内容并入 `legal-research/references/official-case-sources.md`，定位改为「MCP 之外的官方渠道补充」。技能数 39 → 38，对应 eval 用例同步移除 |
| chinese-legal-practice | 1.0.0 → 1.1.0 | MCP 清单重写：新增三端配置对照（Codex/Claude Code/Hermes）、工具分工红线、启信慧眼调用序列 |
| litigation-case-analysis | 1.0.0 → 1.1.0 | 尽调数据源与检索流程校准；尽调工作流文件更名并补入启信慧眼路径 |
| court-trial-realtime | 1.0.0 → 1.1.0 | 企业信息查询口径改为「已配置的企业数据 MCP」；案例检索统一走北大法宝 |
| legal-analysis-pitfalls | 1.0.0 → 1.1.0 | 法条核实口径校准（工具名改为按能力描述） |
| obsidian-knowledge-pipeline | 1.0.0 → 1.1.0 | 检索策略校准：撤销"元典更稳定"的旧结论 |
| lawyer-wechat-article | 1.0.0 → 1.1.0 | 内容验证工具口径校准 |
| wechat-lawyer-article | 1.0.0 → 1.1.0 | 内容验证工具清单校准 |
| lawyer-douyin-livestream | 1.0.0 → 1.1.0 | 企业数据 MCP 口径校准 |

**其他结构性变更**

- `litigation-case-analysis/references/qcc-enterprise-due-diligence.md` 更名为 `enterprise-due-diligence-workflow.md`
- 企业尽调工具改为平级表述：启信慧眼 / 企查查 / 快查365 及其他已配置的企业数据 MCP，不分先后
- README 技能计数与清单同步为 38

---

## 2026-08-23

### `4a8205a` 新增 5 个民商事高频技能（技能数 34 → 39）

- `contract-review` 合同审查、`lawsuit-filing` 立案管辖、`preservation-execution` 保全执行、`lawyer-letter` 律师函、`statute-limitation` 诉讼时效

## 2026-08-11

- `3feecfc` 全仓脱敏：移除真实凭证与个人信息
- `13a4f95` 知识同步技能扩展多平台，案件记忆脱敏
- `23da40f` 统一技能许可证与事实核验约定，补齐 evals 用例

## 2026-08-08

- `e27485f` 23 个技能补充触发例句，4 个技能优化描述，evals 新增例句贴合度检查
- `cb2a0b3` CI 修正触发分支为 master，移除 paths 过滤
- `0c58cd9` 新增技能 frontmatter 校验 CI 与 evals 触发测试框架

## 2026-08-07

- `2655200` 统一 34 个技能 frontmatter，补全 11 个技能的 version 字段

## 2026-07-22

- `1c3aa81` 重写 README 双模块结构，License 改为 Apache 2.0，补充 backend/frontend 骨架
- `dd6fad4`、`88e1739`、`06563ee`、`a83d269`、`f06d64a` 一键部署脚本、部署指南与向量服务修复

## 2026-06-10

- `64e3b43` 同步 Hermes 技能库：新增 12 个技能，更新 9 个技能
- `83a709b`、`3135f17` 涉外律师网站内容调整与恢复

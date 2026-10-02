---
name: claude-code-sync
description: Codex / ChatGPT / WorkBuddy / Claude Code / Hermes 多平台同步知识库 — 案件记忆、反馈规则、插件配置、同步机制
argument-hint: "[目标平台]"
version: 1.2.0
author: 余正洪律师
license: Apache-2.0
platforms: [linux, macos]
metadata:
  hermes:
    tags: [legal, sync, codex, chatgpt, workbuddy, claude-code, hermes, knowledge]
auto_invoke: true
examples:
  - "怎么同步 Codex 和 Hermes 的知识库"
  - "案件记忆如何跨平台同步（Codex/ChatGPT/WorkBuddy/Claude Code/Hermes）"
  - "多平台插件配置同步机制是什么"
---

# 多平台同步知识库（Codex · ChatGPT · WorkBuddy · Claude Code · Hermes）

## 用途
余律师同时使用多个 AI 平台：Codex（CLI/桌面端）、ChatGPT 桌面端（Codex 模式）、WorkBuddy、Claude Code（终端）、Hermes（TUI/飞书）。本技能确保所有平台共享相同的案件记忆、工作规则和配置信息。

---

## 一、反馈规则（多平台统一，最高优先级）

以下规则已在各平台统一生效（Codex / ChatGPT / WorkBuddy / Claude Code / Hermes），任何平台不得例外。

### 1. 严禁编造（最高优先级）
- 无法获取真实信息时 → 明确告知"我无法获取此信息"
- 禁止猜测、编造或生成虚假内容
- 图片无法识别 → 告知"图片无法读取，请通过文件路径方式发送"，禁止假装看到
- 法律分析必须有来源标注，没有来源的结论视为不可信
- 不确定的事必须说"不确定"
- **教训来源**：2026-05-26，用户发起诉状图片标记为 `[Unsupported Image]`，AI 编造了完整的起诉状内容（原告姓名、被告公司、身份证号、仲裁案号、法院名称全部造假）

### 2. 先思考再回答
- 涉及技术架构、系统行为等问题时，先确认事实再回答
- 不确定就说"我不确定，让我确认一下"
- 不要为了快速回复而牺牲准确性
- **教训来源**：飞书/终端是否独立会话的问题上未加思考就给出错误答案

### 3. 四性验证（已在 CLAUDE.md 中定义）
- 准确性、真实性、合法性、关联性
- 法条引用：北大法宝 + 华宇元典交叉验证
- 案例检索：多平台搜索，优先最高法入库案例

---

## 二、进行中案件记忆（私有，存放于 Obsidian）

> ⚠️ 案件详情（案号、当事人、金额、诉讼策略）属于客户保密信息，一律存放于私有 Obsidian 知识库，**不进入任何公开仓库或技能文件**。本技能只保留案件索引与同步方法。

### 案件索引（运行时实时读取）

案件名称、当事人、笔记路径同属客户保密信息，**索引本身也不写入本仓库**。需要时按下面方式实时获取：

1. 列出 `01-案件笔记/` 下的目录与文件，得到当前案件清单；
2. 按案由关键词筛选（如「买卖合同纠纷」「股东损害债权人利益纠纷」「民间借贷纠纷」）；
3. 打开命中笔记，读取一审结果、上诉思路、关键时间线、抗辩要点、类案规则与文书清单。

> 本技能只保留「怎么找」，不保留「有哪些案子」。

### 同步方法

1. 任一平台需要案件上下文时：调用 Obsidian 技能读取对应笔记（"读取 Obsidian 中 [案件名]"）。
2. 各平台办案产出统一写入对应 Obsidian 笔记，保持单一事实源。
3. 新案件建档后，在本节追加一行索引（不含任何敏感字段）。

---

## 三、AI法律服务创始人身份（多平台共用）

### 角色定位

余律师拥有双重身份：
1. **办案律师**（默认）— 民商事诉讼、刑事诉讼、知识产权
2. **AI法律服务创始人** — 以"AI编排法律服务"创始人的视角，把办案能力系统化、产品化

### 创始人模式的四种指令类型

#### 一、战略指令（定方向、看全局）
- 问什么：设计工作流、分析案件类型AI适配度、技术路线图、组织架构
- 输出：结论先行、表格化、阶段性里程碑、投资回报估算

#### 二、产品指令（封装能力为可复用系统）
- 问什么：抽象模板、设计规则引擎、参数化表单、类案检索系统
- 输出：产品需求文档 + 模块拆解 + 输入输出定义

#### 三、运营指令（增长、获客、品牌）
- 问什么：公众号选题、付费内容分析、直播脚本、案源渠道分析
- 输出：可执行方案 + 量化目标 + 底线提醒

#### 四、系统指令（基础设施）
- 问什么：检查MCP/插件健康、知识库打通、自动化规则、版本升级
- 输出：命令行 + 状态报告 + 风险提示

### 触发方式
- 显式声明："切换到创始人模式"、"以创始人身份"
- 关键词触发："设计工作流"、"封装成产品"、"分析案源"、"沉淀为模板"、"系统检查"
- 不需要手动切换，根据指令内容自动识别

### 核心原则
- 余律师只管"想要什么结果"，AI来拆解怎么做到
- 越简短越好，主动补全中间步骤
- 一次投入，长期复用

### 关联资源
- Obsidian：[[AI法律服务创始人指令集]]（`法律知识库/AI技能使用指南/`）
- Obsidian：[[Prompt指令模板库]]（办案律师模式指令）

---

## 四、Claude Code 插件配置

> 说明：本节为各平台配置速查。无论从哪个平台接入，共享知识源始终是 Obsidian 法律知识库。

### 各平台配置与记忆位置

| 平台 | 配置/记忆位置 | 说明 |
|------|--------------|------|
| Codex（CLI + 桌面端） | `~/.codex/config.toml`、`~/.codex/skills/`、`~/.agents/skills/` | 模型、MCP、沙箱、技能都在这里；桌面端 Codex 模式与 CLI 共用 |
| ChatGPT 桌面端（Codex 模式） | 与 Codex 共用 `~/.codex/`；界面设置存于应用内 | 对话历史走账号体系，本地配置走 `~/.codex/` |
| WorkBuddy | `~/.workbuddy/`（plugins/cache、skills） | 插件与技能目录，按 WorkBuddy 文档同步 |
| Claude Code | `~/.claude/`（CLAUDE.md、projects memory、plugins） | 案件记忆与插件配置 |
| Hermes | `~/.hermes/skills/`、`~/.hermes/hermes-agent/` | TUI/飞书桥接技能 |

### claude-for-legal-ZH（12个模块）
- 商业：commercial-legal, corporate-legal
- 争议：litigation-legal
- 知产：ip-legal
- 劳动：employment-legal
- 隐私：privacy-legal
- 产品：product-legal
- 监管：regulatory-legal
- AI治理：ai-governance-legal
- 教育：law-student, legal-clinic
- 社区：legal-builder-hub

### 法律检索源配置
- **一级**：元典智库MCP + 北大法宝MCP
- **二级**：人民法院案例库 + 国家法律法规数据库
- **检索策略**：三轮递进（元典+法宝→案例库→裁判文书网）

---

## 四、同步机制

### 原则
- **Obsidian 法律知识库**为所有平台共享知识源
- 各平台各自产生的案件分析、法律检索结果都持久化到 Obsidian
- 新案件信息通过本技能文件保持同步

### 同步方式
1. **自动同步**：每次办案分析结果 → Obsidian 知识库（各平台规则文件已定义）
2. **手动同步**：更新本技能文件（在任一平台触发"同步知识库"）
3. **定期检查**：对比各平台 memory/配置与本技能文件的差异

### 文件位置
- Claude Code 记忆：`~/.claude/projects/-Users-USERNAME/memory/`
- Hermes 技能：`~/.hermes/skills/claude-code-sync/`
- Codex / ChatGPT 桌面端配置：`~/.codex/config.toml`（模型、MCP 共用）
- Codex 技能：`~/.agents/skills/`、`~/.codex/skills/`
- WorkBuddy：`~/.workbuddy/`
- 共享知识库：Obsidian 法律知识库

## 事实核验原则

> 完整规则见 `../_shared/guardrails.md`（单一来源，勿在本文件单独修改此段）。核心不变：法条、案例、案号、金额与事实结论必须可回源到真实材料或实际检索结果，禁止编造或凭记忆补全；无法核验时输出 `[待补: ...]` 并说明去哪里查；交付前由使用者复核全部引用与数字。

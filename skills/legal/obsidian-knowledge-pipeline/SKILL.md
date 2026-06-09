---
name: obsidian-knowledge-pipeline
description: "Obsidian知识库自动化流水线 — 每日速报+Excalidraw配图+知识沉淀+重要提醒。iCloud同步，权威来源采集，分类沉淀到知识库各模块。"
version: 1.0.0
author: Hermes Agent
license: MIT
dependencies: []
platforms: [macos]
metadata:
  hermes:
    tags: [Obsidian, Excalidraw, 法律知识, 自动化, 定时任务]
    related_skills: ["obsidian", "excalidraw", "legal-research"]
---

# Obsidian知识库自动化流水线

## 概述

本技能管理余正洪律师的Obsidian法律知识库自动化流水线，包括：
- 每日法律速报采集（权威来源）
- Excalidraw配图生成（思维导图、时间线、案例图）
- 知识分类沉淀（法规、案例、实务、江苏动态）
- 重要信息飞书提醒

## 知识库结构

- `references/knowledge-gap-analysis.md` — 已覆盖法律体系、文书模板清单、关键发现记录。
- `references/regional-practice-experience-template.md` — **地区实务经验知识卡片模板**（江苏、上海等地区法院审理特点、诉讼实务、司法政策对比模板）

```
法律知识库/
├── 00-导航中心.md          # 知识库索引
├── 01-案件笔记/            # 案件相关笔记
├── 02-法律知识/            # 法规、司法解释
│   └── 江苏司法/           # 江苏法院动态
├── 03-文书模板/            # 法律文书模板
├── 04-实务经验/            # 实务操作经验
├── 08-裁判规则库/          # 典型案例卡片
├── 09-每日法律速报/        # 每日速报存档
│   ├── YYYY-MM-DD.md      # 速报正文
│   ├── YYYY-MM-DD-热点导图.excalidraw
│   ├── YYYY-MM-DD-时间线.excalidraw
│   ├── YYYY-MM-DD-案例图.excalidraw
│   └── YYYY-MM-DD-沉淀报告.excalidraw
├── 10-直播运营/            # 直播运营+命理学习
├── 11-涉外法律/            # 涉外法律服务全维度（21文件，166KB）
│   ├── README.md           # 索引+核心法律速查表
│   ├── 01-诉讼流程/        # 诉讼、仲裁
│   ├── 02-非诉业务/        # 投资、贸易、劳动、知产、婚姻、税务、保险
│   ├── 03-法律法规/        # 核心法律汇编
│   ├── 04-司法解释/        # 司法解释汇编
│   ├── 05-客户接待/        # 接待流程、沟通技巧
│   ├── 06-文书模板/        # 文书模板、合同审查、公证认证
│   ├── 07-案例研究/        # 典型案例分析
│   └── 08-实务指南/        # 实务、职业突破、IP打造、产品手册
└── Excalidraw/            # Excalidraw图表库
```

## 定时任务配置

### 任务1：每日法律速报（08:00）
- **Job ID**: 4322036dfa55
- **触发时间**: 每天08:00
- **输出内容**:
  - 速报正文（Obsidian格式）
  - Excalidraw思维导图（今日热点）
  - Excalidraw时间线（法规生效）
  - Excalidraw案例图（典型案例）
- **信息来源**:
  - 最高人民法院、最高人民检察院
  - 全国人大、国务院、司法部
  - 江苏法院系统
  - 权威媒体（人民网、新华网、法治日报）
  - MCP工具（元典智库、北大法宝）

### 任务2：知识沉淀与提醒（20:00）
- **Job ID**: 97a21b15a101
- **触发时间**: 每天20:00
- **输出内容**:
  - 知识分类沉淀（法规→02、案例→08、实务→04、江苏→02/江苏司法）
  - 沉淀报告Excalidraw图
  - 重要信息飞书提醒
  - 更新导航中心索引

## Excalidraw配图规范

## Excalidraw配图规范

详见 `references/excalidraw-legal-patterns.md`

### 颜色规范
| 内容类型 | 颜色 | Hex |
|---------|------|-----|
| 今日热点 | 蓝色 | #a5d8ff |
| 典型案例 | 绿色 | #b2f2bb |
| 法规动态 | 橙色 | #ffd8a8 |
| 江苏动态 | 紫色 | #d0bfff |
| 实务提示 | 黄色 | #fff3bf |

### 文字规范
- 标题：fontSize 20px
- 正文：fontSize 16px
- 注释：fontSize 14px（尽量少用）
- 字体：fontFamily 1（Virgil手写风格）

### 结构规范
- 使用容器绑定方式添加文字（不要用label属性）
- 节点使用圆角矩形（roundness: { type: 3 }）
- 手写风格（roughness: 1）
- 文件格式：{ "type": "excalidraw", "version": 2, "source": "hermes-agent", "elements": [...], "appState": { "viewBackgroundColor": "#ffffff" } }

## 重要信息提醒规则

### 触发条件
1. **新法规即将生效**（7天内）
2. **最高法/最高检发布重大典型案例**
3. **江苏法院系统重大政策变化**
4. **与余律师执业领域直接相关的重要动态**

### 提醒格式
```
⚠️ 【法规提醒】《XXX》将于X月X日生效，请注意...
📌 【案例速递】最高法/最高检发布XXX典型案例，对XXX领域有重要参考价值...
🏛️ 【江苏动态】江苏高院XXX政策，对律师执业的影响...
⚡ 【重要提醒】XXX事件，建议关注...
```

### 提醒实现方式

**Cron job 场景**（定时任务）：
- `hermes send` 会被跳过，系统提示 "auto-deliver to same target"
- 提醒内容必须写入最终响应正文，系统自动投递到飞书
- 不需要调用 `send_message` 或 `hermes send`

**交互场景**（用户在线）：
- 使用 `hermes send --to feishu:oc_xxx "消息内容"` 发送
- 或使用 `send_message` 工具（如果可用）

### 提醒要求
- 控制在200字以内
- 重点突出"对律师执业的影响"
- 说明"需要采取的行动"

## 知识沉淀规则

### 笔记模板

详见 `references/note-templates.md`，包含四类笔记的 frontmatter 和结构模板：
- 法规/司法解释笔记（→ 02-法律知识/）
- 裁判规则笔记（→ 08-裁判规则库/）
- 实务经验笔记（→ 04-实务经验/）
- 江苏法院动态笔记（→ 02-法律知识/江苏司法/）

### 法规/司法解释 → 02-法律知识/
- 创建独立笔记
- 包含：法规全文摘要、生效日期、实务影响
- 使用Obsidian双向链接关联速报原文

### 典型案例 → 08-裁判规则库/
- 创建案例卡片
- 包含：案由、裁判要旨、实务启示、关联法条
- 使用Obsidian双向链接关联速报原文

### 实务经验 → 04-实务经验/
- 创建实务笔记
- 包含：问题描述、解决方案、注意事项
- 使用Obsidian双向链接关联速报原文

### 江苏法院动态 → 02-法律知识/江苏司法/
- 创建动态笔记
- 包含：政策要点、对律师执业的影响

## 主动充实知识库（不等定时任务）

每次交互中发现有价值内容，应主动沉淀到Obsidian：
- 法律分析结果 → 创建案例卡片到 `08-裁判规则库/`
- 法规解读 → 创建法规笔记到 `02-法律知识/`
- 实务经验 → 创建实务笔记到 `04-实务经验/`
- 每份笔记必须附带Excalidraw配图（思维导图或关系图）
- 使用Obsidian双向链接 `[[笔记名]]` 关联相关内容
### MCP检索策略

- 法规检索优先用元典智库（search_fagui），比北大法宝更稳定
- 案例检索用元典智库（search_qwal），关键词含案由+地域+年份
- 北大法宝用于交叉验证和补充
- 检索结果偏旧时，换用更精确的关键词组合（如"江苏 2024 合同纠纷"）
- **并行检索**：多个无依赖的关键词同时调用MCP工具，节省时间

## 维护指南

### 添加新的信息源
1. 更新定时任务prompt中的信息采集部分
2. 确保来源权威可靠
3. 记录来源URL便于验证

### 调整沉淀规则
1. 更新定时任务prompt中的知识分类沉淀部分
2. 确保目标文件夹存在
3. 更新本技能文档

### 修改提醒规则
1. 更新定时任务prompt中的重要信息提醒部分
2. 调整触发条件和提醒格式
3. 测试提醒效果

## 相关技能

- `obsidian` — Obsidian文件操作
- `excalidraw` — Excalidraw图表生成
- `legal-research` — 法律检索（元典智库、北大法宝）
- `knowledge-base-enrichment` — 知识库审计与批量丰容（独立技能，含完整检查清单和并行创建工作流）

## 批量创建技术

### 首选方式：并行 write_file 调用（推荐）

直接使用 `write_file` 工具调用，每次 3 个并行调用。这是最可靠的方式，不会超时：

```xml
<!-- 每次并行发出 3 个 write_file 调用 -->
<write_file path=".../法规1.md" content="..." />
<write_file path=".../法规2.md" content="..." />
<write_file path=".../法规3.md" content="..." />
```

**优点**：不会超时、每个调用独立成功/失败、不需要 import。
**节奏**：3 个一批，等返回后再发下一批。

### 备选方式：execute_code 批量创建

用 `execute_code` + `from hermes_tools import write_file` 批量创建，按目录分批，每批一个 `execute_code` 块：

```python
from hermes_tools import write_file

base = "/Users/yuzhenghong/Library/Mobile Documents/iCloud~md~obsidian/Documents/法律知识库"
date_str = "2026-06-05"
report_link = f"[[{date_str}]]"

write_file(f"{base}/02-法律知识/法规名.md", """---
title: 法规名
date: {date_str}
tags: [标签1, 标签2]
---
# 标题
> 来源：{report_link}
...
""")
```

**⚠️ 超时风险**：6 个 write_file 在一个 execute_code 中曾超时（304秒）。限制为 **最多 3-4 个 write_file / 每次 execute_code**。如果超时，回退到并行 write_file 方式。详见 `references/execute-code-timeout-notes.md`。

### 导航中心（MOC）更新模式

每次沉淀后必须更新 `00-导航中心.md`。使用 `patch` + 唯一锚点：

```python
from hermes_tools import patch

# 1. 在对应模块末尾追加新条目
patch(f"{base}/00-导航中心.md",
      "- 上一条已存在的链接",  # 锚点：文件中唯一的一行
      """- 上一条已存在的链接
- [[新笔记路径|显示名]]（YYYY-MM-DD沉淀）""")

# 2. 更新统计表
patch(f"{base}/00-导航中心.md",
      "| 模块名 | 旧数字 | 旧说明 |",
      "| 模块名 | 新数字 | +N篇YYYY-MM-DD沉淀 |")

# 3. 更新日期
patch(f"{base}/00-导航中心.md",
      "updated: 旧日期",
      "updated: 新日期")
```

**注意**：锚点必须是文件中唯一匹配的行，否则 patch 会失败。阅读文件后再选择锚点。

### 超时问题
- 子代理创建Excalidraw图容易超时（600秒限制）
- **解决方案**：拆小任务，每次2-3个文件，不要一次性创建5个以上
- Excalidraw JSON生成较慢，建议单独用一个子代理处理

### MCP检索质量问题
- 元典智库（search_qwal）返回结果可能偏旧
- **解决方案**：用更精确的关键词（年份+地域+案由），或直接基于已有知识创建
- 北大法宝（pkulaw-fatiao）获取具体法条内容更可靠

### 文件冲突
- 同一目录下不要同时创建太多文件
- 先创建Markdown知识卡片，再创建Excalidraw图
- 用delegate_task并行时，每个子代理负责不同目录

## 注意事项

1. **iCloud同步** — 知识库在iCloud下，确保同步正常
2. **文件命名** — 使用ISO日期格式（YYYY-MM-DD）
3. **双向链接** — 使用Obsidian的[[wikilink]]语法
4. **Excalidraw兼容** — 确保JSON格式正确，可在excalidraw.com打开
5. **提醒频率** — 避免过度提醒，只通知真正重要的信息

## 常见陷阱

| 陷阱 | 正确做法 |
|------|---------|
| 批量创建太多文件导致响应慢 | 每次拆小，2-3个文件为一批 |
| Excalidraw子代理超时 | 设置合理的timeout，或直接在主进程创建 |
| 知识卡片内容太浅 | 必须包含：法条依据+案例+实务启示+关联笔记 |
| 忘记加双向链接 | 每个文件底部必须加 `> 来源：[[YYYY-MM-DD]]` |
| 被动等定时任务触发 | 每次交互发现有价值内容应主动沉淀 |
| Cron job 飞书提醒被跳过 | `hermes send` 在 cron 中会被跳过（"auto-deliver to same target"），提醒内容必须写入最终响应 |
| 导航中心 patch 锚点不唯一导致失败 | 先 read_file 确认锚点行在文件中唯一，再 patch |
| write_file 路径含空格/中文 | Obsidian vault 在 iCloud 下路径含空格，write_file 本身支持，但 shell 命令需用引号包裹 |
- 重复创建已有笔记 | 速报可能引用前几天已沉淀的法规/案例。创建前先 search_files 检查目标目录是否已存在类似笔记，避免重复 |

## 知识库丰容流程（Gap Analysis + MCP-Verified Content）

当用户要求"检查知识库缺失"或"丰容知识库"时，执行以下系统化流程：

### Step 1 — 结构扫描
```bash
cd "<vault_path>" && find . -name "*.md" -not -path "*/Excalidraw/*" | wc -l
find . -type d -maxdepth 2 | sort
# 按模块统计文件数
for d in 01-* 02-* 03-* 04-* 08-*; do echo "$d: $(find "$d" -name '*.md' | wc -l)"; done
```

### Step 2 — 缺口分析
按用户执业领域（民商事诉讼/刑事/知识产权/公司法）比对覆盖度。高频缺口：
- **公司法基础** — 公司设立/股权/治理/解散（用户执业领域之一）
- **知识产权基础** — 专利/商标/著作权/商业秘密
- **民事诉讼法要点** — 管辖/举证/简易/上诉/执行
- **刑事辩护要点** — 辩护权/取保/不起诉/量刑
- **文书模板扩充** — 答辩状/上诉状/代理词/执行申请/保全申请

### Step 3 — MCP工具核实法条
```
mcp_yuandian_search_fagui(keyword="公司法") → 获取法规ID
mcp_yuandian_get_fagui_detail(id="...") → 获取全文原文
mcp_yuandian_search_fatiao(keyword="公司法 第四十七条") → 精确条文
```

### Step 4 — 创建知识卡片（每文件必须包含）
- YAML frontmatter（tags, created, source, 时效性）
- 法条原文（MCP核实后，逐字引用）
- 实务要点表格
- ⚠️ 标注重大修订变化（如2023年公司法）
- 关联法条索引
- 底部tags

### Step 5 — 更新导航中心
在 `00-导航中心.md` 对应模块下添加链接 + 更新统计表数字

### 使用delegate_task并行
3个子代理并行创建不同模块的知识卡片，每个子代理负责一个领域：
- 子代理1：公司法
- 子代理2：知识产权法
- 子代理3：民诉法+刑辩+文书模板

**⚠️ delegate_task最大3个并发**（delegation.max_concurrent_children=3）。超过3个会报错。如果需要创建更多，分批执行：第一批3个完成后，再发第二批。

### 多轮丰容模式（2026-06-08验证）

一次丰容覆盖所有缺口容易超时。采用**分轮递进**模式：

| 轮次 | 内容 | 文件数 |
|------|------|--------|
| 第1轮 | 核心法律体系（公司法/知识产权/民诉/刑辩）+ 文书模板扩充 | +9 |
| 第2轮 | 补充法律（物权/执行/破产/合同/劳动/行政）+ 高级模板 | +10 |
| 第3轮 | 专题法律（侵权/家事/刑法/担保/合规/建工）+ 实务经验 | +10 |

每轮完成后：
1. 更新导航中心（链接+统计）
2. 验证iCloud同步（`brctl status` 或检查文件时间戳）
3. 确认无遗漏再启动下一轮

### 法条核实策略

MCP工具对法条原文的返回方式：
- **元典智库 get_fagui_detail**：返回法规全文（最可靠，但内容很长）
- **元典智库 search_fatiao**：返回引用该条文的规范性文件（间接引用，需交叉核实）
- **北大法宝 get_article**：返回具体条文原文（精确，但有时无结果）

**最佳实践**：先用 search_fagui 获取法规ID → 再用 get_fagui_detail 获取全文 → 从全文中提取所需条文。对于民法典等大法，全文可能很长（>30KB），直接搜索所需条文号即可。

### iCloud同步验证

丰容完成后验证文件是否同步到iCloud：
```bash
brctl status 2>/dev/null | head -3
# 确认 last-sync 时间戳和 caught-up 状态
cd "<vault_path>" && find . -name "*.md" -newer ./00-导航中心.md | wc -l
# 确认新文件数量
```

### 导航中心更新模板

丰容后更新 `00-导航中心.md` 的标准流程：
1. **添加链接**：在对应模块的已有条目后 patch 新链接
2. **更新统计表**：修改法律知识/文书模板/实务经验的数量
3. **更新日期**：修改 `updated:` 字段

**⚠️ 锚点选择**：选择文件中唯一的行作为锚点。如果锚点不唯一，patch 会失败。先 read_file 确认。

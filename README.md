# ⚖️ Lawyer Knowledge Graph

> **律师知识图谱 — 让办过的每一个案子，都成为未来办案的资产**

[![License](https://img.shields.io/badge/License-Apache%202.0-blue)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.11-green)](https://python.org)
[![Docker](https://img.shields.io/badge/Docker-Compose-blue)](docker-compose.yml)

一套面向诉讼律师的 AI 个人知识管理系统 + 40个专业技能集。两个模块互补协作：

- **知识图谱系统**：案件经验自动沉淀 → 向量检索 → 类案秒级匹配
- **技能集**：覆盖办案全流程的 Hermes Agent 技能，对话即用

---

## 一个痛点

做了十五年民商事诉讼律师，手上有几百个办过的案子。

几年前遇到一个买卖合同纠纷，案件事实和五年前办过的另一个案子几乎一模一样——同样的争议焦点，同样的法律适用问题。但翻遍文件夹也没找到当时的详细记录，只记得"好像办过类似的"，最后从头研究，多花了三天。

律师的办案经验，正在被浪费。每办一个案子积累的理解——争议焦点怎么抓、证据链怎么组织、法院对同类问题持什么态度——这些经验要么散落在 Word 文档里，要么沉睡在记忆中。

**这就是 Lawyer Knowledge Graph 的起点。**

---

## 项目架构

```
lawyer-knowledge-graph/
├── backend/              # 模块一：知识图谱系统后端（FastAPI）
│   ├── main.py           # API 入口
│   ├── models.py         # 数据模型（SQLAlchemy + pgvector）
│   ├── services.py       # 核心逻辑：知识提取、向量化、检索
│   ├── database.py       # 数据库连接
│   ├── init.sql          # 数据库初始化脚本
│   ├── requirements.txt
│   └── Dockerfile
├── vector/               # 向量编码服务（text2vec HTTP API）
│   ├── server.py         # FastAPI 向量服务
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/             # 模块一：知识图谱系统前端（Streamlit）
│   ├── app.py            # 交互界面
│   ├── requirements.txt
│   └── Dockerfile
├── scripts/              # 独立可运行脚本
│   ├── extract_cards.py  # 知识卡片提取
│   └── vector_search.py  # 向量检索
├── skills/legal/         # 模块二：40个律师专业技能
├── docs/                 # 项目文档
├── deploy.sh             # 一键部署脚本
├── DEPLOY.md             # 零基础部署指南
├── docker-compose.yml    # 一键启动
├── .env.example          # 环境变量模板
└── LICENSE               # Apache 2.0
```

---

## 模块一：知识图谱系统

### 核心逻辑

```
输入案件材料 → AI 自动提取知识卡片 → 存入向量数据库 → 新案发生时一键检索相似案例
```

### 三大核心功能

#### 1. 案件知识自动沉淀

粘贴裁判文书或案卷摘要，AI 自动提取结构化知识卡片：

| 卡片类型 | 说明 | 示例 |
|----------|------|------|
| 争议焦点 | 本案的核心争议问题 | "违约金过高是否应调减" |
| 裁判规则 | 法院对此类问题的裁判标准 | "违约金调减以实际损失的30%为参考上限" |
| 法条适用 | 精确到具体法条编号和要点 | "民法典第585条：违约金调整规则" |
| 办案经验 | 律师视角的实务技巧 | "此类案件应重点收集实际损失证明、行业利润率数据" |

每张知识卡片自动生成向量索引，存入 pgvector 数据库。录入的案件越多，系统积累的知识越丰富。

#### 2. 类案智能检索

接到新案件时，在搜索框输入案件描述，系统基于**语义相似度**（而非关键词匹配）检索历史案件中所有相关的知识卡片：

```
输入：买卖合同中卖方交付的货物质量不符合约定，买方拒付货款并要求赔偿损失

输出：
  相似度 0.89 → （2025）苏02民初456号 · 买卖合同纠纷
  相似度 0.82 → （2024）苏02民初789号 · 承揽合同纠纷
  相似度 0.76 → 民法典第615条 · 标的物质量不符合要求的处理
  相似度 0.71 → 民法典第582条 · 违约责任承担方式
```

#### 3. 法规动态追踪（规划中）

设置关注领域（如"合同纠纷""劳动争议"），自动检索新增的司法解释和指导性案例，生成更新摘要推送。

已预留接口：北大法宝（PKULAW）、华宇元典（YUANDIAN），配置 API Key 即可启用。

### 技术架构

| 组件 | 技术选型 | 说明 |
|------|----------|------|
| 后端框架 | FastAPI | 异步高性能，自动生成 API 文档 |
| 数据库 | PostgreSQL 16 + pgvector | 结构化数据 + 向量检索 |
| 向量模型 | text2vec-large-chinese | 中文语义向量化，768 维 |
| 大语言模型 | DeepSeek V4 Pro / Kimi K3 / GLM 5.2 | 知识卡片提取、摘要生成 |
| 前端 | Streamlit | 快速构建交互界面 |
| 部署 | Docker Compose | 一键启动所有服务 |

### 快速开始

**方式一：一键部署脚本（推荐）**

```bash
# 1. 克隆项目
git clone https://github.com/wxlawyers/lawyer-knowledge-graph.git
cd lawyer-knowledge-graph

# 2. 运行部署脚本（自动引导配置 AI 模型和 API Key）
bash deploy.sh

# 3. 打开浏览器
# 前端：http://localhost:8501
# API 文档：http://localhost:8000/docs
```

> 零基础用户请阅读 [部署指南](DEPLOY.md)，图文步骤从安装 Docker 开始。

**方式二：手动启动**

```bash
# 1. 克隆项目
git clone https://github.com/wxlawyers/lawyer-knowledge-graph.git
cd lawyer-knowledge-graph

# 2. 配置环境变量
cp .env.example .env
# 编辑 .env，填入你的 LLM API Key

# 3. 一键启动（需安装 Docker）
docker-compose up -d

# 4. 打开浏览器
# 前端：http://localhost:8501
# API 文档：http://localhost:8000/docs
```

系统启动后自动初始化数据库表结构，无需手动执行任何 SQL。向量服务首次启动需下载模型（约 1-2 分钟），请耐心等待。

### 最低硬件要求

| 配置 | 要求 |
|------|------|
| CPU | 4 核及以上 |
| 内存 | 8 GB（推荐 16 GB） |
| 硬盘 | 20 GB 可用空间 |
| Docker | Docker Engine 24+ & Docker Compose v2 |
| 网络 | 需访问 LLM API（DeepSeek/Kimi/GLM） |

### 独立脚本使用

不想启动完整服务？两个核心脚本可独立运行：

```bash
# 知识卡片提取（需配置 LLM_API_KEY）
python scripts/extract_cards.py --file 判决书.txt --output cards.json

# 向量检索（需启动 PostgreSQL + 向量模型）
python scripts/vector_search.py --query "买卖合同违约金过高" --top-k 5
```

---

## 模块二：律师专业技能集（40个）

> 需要 [Hermes Agent](https://hermes-agent.nousresearch.com) 运行环境。

知识图谱系统解决的是"经验存储与检索"，技能集解决的是"日常办案效率"。两者互补：技能集在日常对话中调用法律检索、文书撰写等能力，知识图谱系统则把每次办案的经验自动沉淀下来。

### 技能分类

<details>
<summary><strong>办案流程技能（17个）</strong></summary>

| 技能 | 功能 |
|------|------|
| litigation-case-analysis | 案件分析与请求权基础分析 |
| evidence-organization | 证据组织与四性验证 |
| legal-research | 法律检索与案例研究（含官方案例来源检索指引） |
| legal-document-drafting | 法律文书撰写 |
| trial-preparation | 庭前准备 |
| trial-response | 庭审应对 |
| client-communication | 当事人沟通 |
| case-management | 案件管理 |
| case-deadline-monitor | 案件期限自动监控 |
| compensation-calculator | 交通事故/工伤/劳动纠纷赔偿计算 |
| contract-review | 合同审查与风险分级（民商事合同全要素） |
| lawsuit-filing | 立案与管辖分析（级别/地域/专属/协议管辖） |
| preservation-execution | 保全与强制执行全流程 |
| lawyer-letter | 律师函起草（催告/解约/侵权警告） |
| statute-limitation | 诉讼时效与期间计算 |
| litigation-visualization | 诉讼可视化（时间线图/法律关系图/庭前对抗图） |
| legal-chinese-refine | 法言法语润色（表达打磨/审校/通俗转译/文书链核对） |

</details>

<details>
<summary><strong>知识管理技能（4个）</strong></summary>

| 技能 | 功能 |
|------|------|
| knowledge-accumulation | 知识沉淀与复用 |
| knowledge-base-enrichment | 知识库审计与丰容 |
| obsidian-knowledge-pipeline | Obsidian知识库自动化 |
| legal-analysis-pitfalls | 法律分析常见错误与教训 |

</details>

<details>
<summary><strong>业务拓展技能（7个）</strong></summary>

| 技能 | 功能 |
|------|------|
| business-development | 案源开发与品牌建设 |
| lawyer-douyin-livestream | 律师抖音直播助手 |
| lawyer-website-development | 律师个人网站开发 |
| wechat-lawyer-article | 微信公众号文章撰写 |
| wechat-legal-article | 涉外律师公众号文章 |
| foreign-related-legal-practice | 涉外律师执业技能 |
| vibe-coding-legal-tools | Vibe Coding法律工具开发 |

</details>

<details>
<summary><strong>专业领域技能（12个）</strong></summary>

| 技能 | 功能 |
|------|------|
| chinese-legal-practice | 中国法律实务技能集 |
| court-trial-realtime | 庭审实时辅助 |
| cpa-accounting | 注册会计师知识技能 |
| cta-tax | 注册税务师知识技能 |
| ma-restructuring | 并购重组 |
| bankruptcy-liquidation | 破产清算 |
| securities-compliance | 证券合规 |
| real-estate-transaction | 房产交易 |
| labor-compensation | 劳动补偿 |
| forensic-accounting | 司法会计鉴定 |
| claude-code-sync | Codex/ChatGPT/WorkBuddy/Claude Code/Hermes 多平台知识同步 |
| lawyer-wechat-article | 律师微信公众号文章（扩展） |

</details>

### 技能集安装

```bash
# 克隆仓库
git clone https://github.com/wxlawyers/lawyer-knowledge-graph.git

# 复制技能到 Hermes Agent（* 会一并复制 _shared/ 通用护栏，请不要漏掉）
cp -r lawyer-knowledge-graph/skills/legal/* ~/.hermes/skills/legal/
```

> 技能末尾的「事实核验原则」统一来自 `skills/legal/_shared/guardrails.md`，由 `scripts/sync_guardrails.py` 同步；要改护栏请改单一来源再跑同步脚本。

在 `~/.hermes/config.yaml` 中配置 MCP 工具：

```yaml
mcp:
  servers:
    pkulaw:        # 北大法宝
      command: "node"
      args: ["~/.hermes/mcp-servers/pkulaw/index.js"]
    yuandian:      # 元典智库
      command: "node"
      args: ["~/.hermes/mcp-servers/yuandian/index.js"]
    qcc:           # 企查查
      command: "node"
      args: ["~/.hermes/mcp-servers/qcc/index.js"]
```

### 集成工具

| 工具 | 数量 | 用途 |
|------|------|------|
| 北大法宝 | 多个 MCP 服务 | **法规与案例主检索源**：法规检索、精准法条、案例检索、案号识别、文书超链接 |
| 元典 | MCP 工具 | 法规、法条检索的**交叉核验**（案例检索不可靠，不作为类案来源） |
| 企业数据 MCP | 启信慧眼 / 企查查 / 快查365 等 | 企业尽调：工商、股权穿透、涉诉、经营风险（**不分先后，用已配置且可用的那个**） |

> 工具分工红线：法规案例类与经营数据类不得混用。完整清单与三端配置对照见 `skills/legal/chinese-legal-practice/references/mcp-tool-inventory.md`。

### 版本与变更

- 技能版本规则：[VERSIONING.md](VERSIONING.md)（改一次升一版：主版本=结构性变化，次版本=内容变化，补丁=文字修正）
- 变更记录：[CHANGELOG.md](CHANGELOG.md)
- 提交前自检：`python3 scripts/check_versions.py`
- 通用护栏单一来源：`skills/legal/_shared/guardrails.md`，同步用 `python3 scripts/sync_guardrails.py`
- 命令参数提示：全部技能带 `argument-hint`（如 `/contract-review 合同.docx --side=卖方`），统一由 `scripts/add_argument_hint.py` 维护

---

## 适用场景

| 场景 | 模块 | 效果 |
|------|------|------|
| 新案接手 | 技能集 | 对话式分析请求权基础，2分钟出报告 |
| 新案接手 | 知识图谱 | 输入案情描述，5秒找到历史相似案件 |
| 办案小结 | 知识图谱 | 粘贴判决书，AI 自动生成知识卡片 |
| 庭审质证 | 技能集 | 拍照对方证据，秒级生成质证要点 |
| 法规追踪 | 知识图谱 | 自动推送新司法解释和指导性案例 |
| 品牌建设 | 技能集 | AI 写公众号文章、做个人网站 |
| 团队协作 | 知识图谱 | （规划中）多位律师共享知识库 |

---

## 当前状态与路线图

### 知识图谱系统

- [x] 数据模型设计
- [x] 知识卡片提取脚本（独立可运行）
- [x] 向量检索脚本（独立可运行）
- [x] API 接口设计
- [x] Docker Compose 配置
- [x] FastAPI 后端（案件录入、检索、卡片管理）
- [x] Streamlit 前端界面
- [ ] 法规追踪模块
- [ ] 团队协作功能

### 技能集

- [x] 40个技能已发布
- [ ] 持续迭代优化

---

## 生态调研：GitHub 法律技能开源现状

> 2026-08 调研结论：本仓库与全球头部法律技能仓库的定位差异与互补点。

### GitHub 法律/律师技能仓库 Top 10（按 Star 数）

| 排名 | 仓库 | Star | 特点 |
|------|------|------|------|
| 1 | anthropics/claude-for-legal | 9.2k | Anthropic 官方法律插件套件（商业/诉讼/合规/隐私等 15 个插件） |
| 2 | zubair-trabzada/ai-legal-claude | 1.7k | AI 法律助手：合同审查、风险分析、NDA 生成 |
| 3 | lawve-ai/awesome-legal-skills | 662 | 238 个法律 Agent Skills 精选清单 |
| 4 | cat-xierluo/legal-skills | 594 | 面向中文法律人的技能集合（60+） |
| 5 | gfodor/legal-skills | 375 | "用 Markdown 文件取代律师"的方法论实验 |
| 6 | zhou210712/claude-for-legal-ZH | 198 | 面向中国法律实务的 Claude 工作层 |
| 7 | zh-xx/legal-assistant-skills | 165 | 兼容 Claude Code / Codex 的法律技能 |
| 8 | lilialla/awesome-legal-ai-zh | 128 | 中国律师/法务开源 AI 工具地图（200+ 仓库） |
| 9 | akunikkola/claude-for-legal-finland | 101 | 芬兰法律区域技能（参考） |
| 10 | ZekaiSuni/claude-for-legal-turkish | 100 | 土耳其法律区域技能（参考） |

### 差距分析与本次更新

对照头部仓库后，本次为技能集补充了 5 个中国民商事律师最高频、此前缺失的能力：

- **contract-review**：合同审查（借鉴 anthropics/commercial-legal、zh-xx/contract-review、awesome-legal-skills 的合同审查方法论）
- **lawsuit-filing**：立案与管辖分析（中国民事诉讼起步环节）
- **preservation-execution**：保全与强制执行（胜诉权益落地的关键环节）
- **lawyer-letter**：律师函起草（日常高频非诉文书）
- **statute-limitation**：诉讼时效与期间计算（起诉前必检项）

### 差异化定位

相比海外头部仓库（聚焦通用合同/合规/隐私，且以欧美法为主），本仓库的差异：

1. **中国法实务**：全部技能基于中国法律体系，覆盖民商事诉讼全流程
2. **诉讼实战**：庭审准备/庭审应对/证据组织等庭审能力是海外仓库普遍缺失的
3. **知识沉淀**：案件经验 → 知识图谱 → 类案复用的闭环，非单纯提示词集合
4. **多平台可用**：技能同时适配 Hermes / Codex / ChatGPT / Claude Code / WorkBuddy

---

## 常见问题

**Q：知识图谱系统需要编程基础吗？**
A：不需要。Docker 一键启动后，浏览器打开页面即可使用。

**Q：技能集需要什么环境？**
A：需要 Hermes Agent 运行环境。只要会发消息就能使用，无需编程。

**Q：支持哪些大模型？**
A：知识图谱系统支持 DeepSeek V4 Pro / Kimi K3 / GLM 5.2（通过 OpenAI 兼容 API）。技能集支持小米 MiMo、Claude、GPT-4 等主流模型。

**Q：数据安全吗？**
A：知识图谱系统数据完全私有，部署在自己服务器上。技能集数据存储在本地 Obsidian 知识库，不上传第三方。

**Q：可以定制技能吗？**
A：可以。每个技能都是一个 SKILL.md 文件，用自然语言描述工作流程，AI 按流程执行。

---

## License

[Apache License 2.0](LICENSE)

---

## 仓库地址

- **GitHub**：https://github.com/wxlawyers/lawyer-knowledge-graph
- **Gitee（国内镜像）**：https://gitee.com/wxlawyers/lawyer-knowledge-graph

---

## 作者

**余正洪律师** | 江苏三诚律师事务所

- 执业领域：民商事诉讼 · 刑事诉讼 · 知识产权 · 公司法/商事合规
- 网站：[lawyer-yu.netlify.app](https://lawyer-yu.netlify.app)

---

**如果这个项目对你有帮助，请点个 Star 支持一下！欢迎提交 Issue 和 PR。一个人的力量有限，但如果有更多律师和开发者一起参与，这个工具会变得更好。**

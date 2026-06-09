# ⚖️ 律师AI超级大脑

> **34个专业技能 · 覆盖办案全流程 · 让律师效率提升10倍**

[![Skills](https://img.shields.io/badge/技能-34-blue)](#技能清单)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)
[![Hermes Agent](https://img.shields.io/badge/Powered%20by-Hermes%20Agent-purple)](https://hermes-agent.nousresearch.com)

**这不是又一个法律AI工具。这是一套为诉讼律师打造的AI工作系统。**

---

## 🎯 解决什么问题？

| 痛点 | 传统方式 | 用这套技能 |
|------|----------|-----------|
| 案件法律分析 | 翻法条+查案例，2-3小时 | 对话式检索，2分钟出报告 |
| 庭审质证 | 临场反应，容易遗漏 | 秒级检索法条+案例，实时辅助 |
| 知识积累 | 办完案子就忘 | 自动沉淀到知识库，可复用 |
| 做网站/写文章 | 找外包，几千到几万 | Vibe Coding，自己用AI做 |

---

## ⚡ 核心能力

### 🔍 法律检索
- 对接北大法宝（9个工具）、元典智库（5个工具）
- 法条原文秒查，案例交叉验证
- 支持自然语言查询："查一下江苏地区近三年建设工程纠纷案例"

### 📊 企业尽调
- 企查查180个工具全覆盖
- 股东穿透、风险扫描、诉讼记录、知识产权
- 一句话查企业："查一下XX公司的实际控制人和诉讼风险"

### 📝 知识沉淀
- 自动提取案件要素、裁判规则、实务经验
- Obsidian双向链接，零断链
- 每日法律速报自动分类沉淀

### ⚖️ 庭审辅助
- 开庭时秒级检索法条和案例
- 质证要点自动生成
- 对方抗辩即时反驳建议

---

## 📦 技能清单（34个）

<details>
<summary><strong>📋 办案流程技能（点击展开）</strong></summary>

| 技能 | 功能 |
|------|------|
| litigation-case-analysis | 案件分析与请求权基础分析 |
| evidence-organization | 证据组织与四性验证 |
| legal-research | 法律检索与案例研究 |
| legal-document-drafting | 法律文书撰写 |
| trial-preparation | 庭前准备 |
| trial-response | 庭审应对 |
| client-communication | 当事人沟通 |
| case-management | 案件管理 |
| case-deadline-monitor | 案件期限自动监控 |
| compensation-calculator | 交通事故/工伤/劳动纠纷赔偿计算 |

</details>

<details>
<summary><strong>🧠 知识管理技能（点击展开）</strong></summary>

| 技能 | 功能 |
|------|------|
| knowledge-accumulation | 知识沉淀与复用 |
| knowledge-base-enrichment | 知识库审计与丰容 |
| obsidian-knowledge-pipeline | Obsidian知识库自动化 |
| legal-analysis-pitfalls | 法律分析常见错误与教训 |
| case-search-sources | 法律案例搜索源指南 |

</details>

<details>
<summary><strong>💼 业务拓展技能（点击展开）</strong></summary>

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
<summary><strong>📚 专业领域技能（点击展开）</strong></summary>

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
| claude-code-sync | Claude Code与Hermes双平台同步 |

</details>

---

## 🚀 快速开始

### 1. 安装技能

```bash
# 克隆仓库
git clone https://github.com/wxlawyers/lawyer-knowledge-graph.git

# 复制技能到 Hermes Agent
cp -r lawyer-knowledge-graph/skills/legal/* ~/.hermes/skills/legal/
```

### 2. 配置MCP工具

在 `~/.hermes/config.yaml` 中添加：

```yaml
mcp:
  servers:
    # 北大法宝
    pkulaw:
      command: "node"
      args: ["~/.hermes/mcp-servers/pkulaw/index.js"]
    
    # 元典智库
    yuandian:
      command: "node"
      args: ["~/.hermes/mcp-servers/yuandian/index.js"]
    
    # 企查查
    qcc:
      command: "node"
      args: ["~/.hermes/mcp-servers/qcc/index.js"]
```

### 3. 开始使用

```bash
# 通过飞书/终端对话
"帮我分析这个案件的请求权基础"
"查一下民法典关于违约责任的规定"
"帮我准备一期关于劳动纠纷的直播脚本"
"做一个涉外律师的个人网站"
```

---

## 💡 使用场景

### 场景1：案件分析
```
你：帮我分析一下这个建设工程合同纠纷的请求权基础
AI：[自动检索相关法条和案例，生成分析报告]
```

### 场景2：庭审辅助
```
你：[拍照对方证据] 这个证据怎么质证？
AI：[OCR识别 + 法条检索 + 质证要点生成]
```

### 场景3：知识积累
```
你：把这个案件的裁判规则沉淀到知识库
AI：[自动提取要素，生成知识卡片，建立双向链接]
```

### 场景4：品牌建设
```
你：帮我写一篇关于合同纠纷的公众号文章
AI：[按19条质量标准生成，自动降AI味]
```

---

## 🔧 集成工具

| 工具 | 数量 | 用途 |
|------|------|------|
| 北大法宝 | 9个MCP服务 | 法规搜索、案例检索、法条检索 |
| 元典智库 | 5个MCP工具 | 法规检索、法条检索、案例检索 |
| 企查查 | 180个工具 | 企业工商、司法风险、知识产权 |
| 快查企业数据 | 企业数据查询 | 工商信息、股东股权、对外投资 |
| 法智法律检索 | 法律检索 | 法条检索、案例检索 |

---

## 📊 数据

- **技能总数**：34个
- **覆盖领域**：民商事、刑事、知产、公司法、劳动法、房产、证券
- **集成工具**：201个MCP工具
- **知识库**：273篇知识卡片（持续增长）

---

## 🤔 常见问题

**Q：需要什么基础才能用？**
A：不需要编程基础。只要会用飞书/微信发消息就行。

**Q：支持哪些大模型？**
A：支持小米MiMo、Claude、GPT-4等主流模型。推荐小米MiMo（性价比最高）。

**Q：数据安全吗？**
A：所有数据存储在本地Obsidian知识库，不上传第三方。法条检索通过MCP工具调用，不暴露案件信息。

**Q：可以定制技能吗**
A：可以。每个技能都是一个SKILL.md文件，用自然语言描述工作流程，AI会按流程执行。

---

## 📄 License

[MIT](LICENSE)

---

## 👨‍⚖️ 作者

**余正洪律师** | 江苏三诚律师事务所

- 执业领域：民商事诉讼 · 刑事诉讼 · 知识产权 · 公司法/商事合规
- 微信：wuxilawyers
- 电话：132-7625-9126
- 网站：[lawyer-yu.netlify.app](https://lawyer-yu.netlify.app)

---

**如果这个项目对你有帮助，请点个 ⭐ Star 支持一下！**

---
name: litigation-case-analysis
description: "诉讼案件分析技能 — 请求权基础分析、证据组织、法律检索、知识卡片生成。集成元典智库+北大法宝MCP工具。"
version: 1.0.0
author: 余正洪律师
license: MIT
platforms: [linux, macos]
metadata:
  hermes:
    tags: [legal, litigation, case-analysis, evidence, research]
---

# 诉讼案件分析技能

面向中国诉讼律师的案件分析框架，集成元典智库和北大法宝 MCP 工具。

## 适用场景

- 新案接案分析
- 请求权基础确定
- 证据组织与验证
- 法律检索与案例研究
- 知识卡片生成与沉淀

## MCP 工具

### 元典智库（5个工具）
- `mcp_yuandian_search_fagui` — 法规检索
- `mcp_yuandian_search_fatiao` — 法条检索
- `mcp_yuandian_search_qwal` — 案例检索
- `mcp_yuandian_get_fagui_detail` — 法规详情
- `mcp_yuandian_get_fatiao_detail` — 法条详情

### 北大法宝（9个服务）
- `mcp_pkulaw_search_law` — 法规搜索
- `mcp_pkulaw_search_case` — 案例检索
- `mcp_pkulaw_search_fatiao` — 法条检索
- `mcp_pkulaw_law_keyword` — 法规关键词检索
- `mcp_pkulaw_case_search` — 案例搜索
- `mcp_pkulaw_doc_link` — 文档链接
- `mcp_pkulaw_law_recognition` — 法规识别
- `mcp_pkulaw_case_number_recognition` — 案号识别
- `mcp_pkulaw_law_query` — 法规查询

## 执行步骤

### 步骤一：案件基本信息采集

收集以下信息：
- 当事人（原告、被告、第三人）
- 案由
- 诉讼请求
- 事实与理由
- 管辖法院
- 标的金额

### 步骤二：请求权基础分析

1. **识别法律关系性质**
   - 合同纠纷？侵权纠纷？物权纠纷？公司纠纷？
   - 具体案由是什么？

2. **确定请求权基础**
   - 谁向谁主张？（主体）
   - 依据什么主张？（法律依据）
   - 主张什么？（诉讼请求）
   - 请求权基础是什么？（民法典哪一条）

3. **诉讼策略选择**
   - 诉讼 vs 仲裁 vs 调解
   - 诉讼请求是否合理
   - 是否有反诉可能

### 步骤三：证据组织与四性验证

1. **证据收集**
   - 合同/协议
   - 付款凭证
   - 沟通记录（微信、邮件、短信）
   - 证人证言
   - 鉴定报告
   - 其他书证、物证、视听资料

2. **四性验证**
   - **真实性**：是否原件？是否有篡改？
   - **合法性**：取证方式是否合法？
   - **关联性**：与待证事实是否相关？
   - **充分性**：能否形成完整证据链？

3. **证据清单编制**
   | 序号 | 证据名称 | 证据来源 | 证明目的 | 页码 |
   |------|----------|----------|----------|------|

### 步骤四：法律检索（三轮递进）

**第一轮：双源交叉检索**

使用元典智库：
```
mcp_yuandian_search_fagui(keyword="相关法规关键词")
mcp_yuandian_search_fatiao(keyword="法规名称 条号")
mcp_yuandian_search_qwal(keyword="案由 争议焦点 地域 年份")
```

使用北大法宝：
```
mcp_pkulaw_search_law(keyword="相关法规关键词")
mcp_pkulaw_search_case(keyword="案由 争议焦点")
```

**第二轮：裁判规则验证**

对检索到的案例，提取裁判要旨，验证是否支持我方主张。

**第三轮：类案补充**

检索同一法院、同一法官的历史裁判，分析裁判倾向。

### 步骤五：知识卡片生成

将案件分析结果生成结构化知识卡片：

```markdown
# 案件知识卡片

## 基本信息
- 案号：（202X）XXX民初XXX号
- 案由：XXX纠纷
- 当事人：原告XXX vs 被告XXX
- 管辖法院：XXX人民法院

## 请求权基础
- 请求权主体：原告XXX
- 请求权客体：被告XXX
- 请求权基础：《民法典》第XXX条
- 诉讼请求：1. XXX 2. XXX

## 争议焦点
1. XXX
2. XXX

## 裁判规则
- 规则1：XXX（来源：XXX案例）
- 规则2：XXX（来源：XXX法规）

## 证据清单
| 序号 | 证据名称 | 证明目的 |
|------|----------|----------|
| 1 | XXX | XXX |

## 办案经验
- 注意事项：XXX
- 风险点：XXX
- 策略建议：XXX
```

## 质量标准

### 四性验证
1. **准确性** — 法条条文、案号、法院名称准确无误
2. **真实性** — 引用的法规、案例真实存在
3. **合法性** — 法律依据符合现行有效法律规定
4. **关联性** — 引用内容与待解决问题有实质关联

### 引用规范
- 法条：全称+条号+内容
- 案例：案号+法院+裁判要旨
- 来源：标注检索平台和检索时间

## 安全要求

- 当事人敏感信息禁止输出到外部请求
- 法律检索前先脱敏处理
- 交付前四性验证

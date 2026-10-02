# 企业尽调工作流（诉讼对手 / 合作方）

> **2026-10-02 校准**：企业尽调数据源**不排优先级**。以当前环境实际配置且可用的企业数据 MCP 为准——启信慧眼、企查查、快查365，或你自己配置的其他同类 MCP 都可以。这些工具**只用于企业数据**，不得用于查法条或案例。
> 本文件原为 `qcc-enterprise-due-diligence.md`，2026-10-02 更名，内容同步补入启信慧眼路径。

---

## 零、可用的企业数据 MCP（不分先后）

| 工具 | 常见所在环境 | 覆盖 |
|------|--------------|------|
| 启信慧眼（MCP 名 `qixin`） | Codex / Claude Code | 工商、股权穿透、实际控制人、关联关系、对外投资、经营风险、涉诉、按条件筛企业 |
| 企查查（`qcc-*` 6 个服务） | Hermes | 工商、股东、对外投资、34 类司法风险、知产、经营、高管、历史变更 |
| 快查365（`kuaicha-search`） | Hermes | 企业数据查询与筛选、关系分析 |
| 其他已配置的企业数据 MCP | 视配置而定 | 按各自覆盖维度使用 |

**选用原则**：哪个当前可用、哪个覆盖你要的维度就用哪个，不规定先后；也可以组合使用（例如一个查工商、另一个查涉诉）做交叉印证。结果必须标注**来源工具**与**查询日期**。

无论走哪条路径，**多候选主体必须让用户确认**，不得自动选择。

---

## 一、启信慧眼工作流

### 调用序列

1. **首跳必读**：新会话首次调用前，必须先 `lookup(path="/instructions")` 读取使用说明；
2. **锁定主体**：`enterprise_resolve` 解析企业主体，返回多个候选时完整展示给用户选择；
3. **发现能力**：不熟悉有哪些维度时，用 `catalog_get` 按业务关键词搜索或浏览目录；
4. **取入参规格**：首次调用某个 `api_ref` 前，先用 `api_spec_get` 查入参规格；
5. **执行**：`api_call` 调用；
6. **钻取大响应**：返回带 `result_ref` 时，用 `result_query` 按需取字段，不要整包塞进上下文；
7. **署名**：对外一律署「启信慧眼」。

### 可覆盖的尽调维度

- **工商与股权**：工商注册、股东与股权结构、股权穿透、实际控制人、最终受益人、对外投资、关联企业
- **司法风险**：裁判文书、立案信息、失信被执行人、被执行人、限制高消费、股权冻结
- **经营与资质**：招投标、资质证书、行政许可、行政处罚、经营异常
- **知识产权**：商标、专利、软件著作权
- **批量能力**：按地区、行业、成立时间等条件筛选企业，生成企业名单

> 具体 `api_ref` 与返回字段以 `catalog_get` + `api_spec_get` 的当次返回为准，不要凭记忆拼接口名。

---

## 二、企查查工作流（Hermes 环境等价路径）

### 工具总览（6 个 Server，约 180 个工具）

| Server | 工具前缀 | 覆盖维度 |
|--------|----------|----------|
| qcc-company | `mcp_qcc_company_*` | 工商注册、股东、对外投资、高管、实际控制人、联系方式、年报、财务数据 |
| qcc-risk | `mcp_qcc_risk_*` | 裁判文书、立案、失信被执行人、被执行人、限高、经营异常、行政处罚、股权冻结、司法拍卖、终本案件 |
| qcc-executive | `mcp_qcc_executive_*` | 董监高个人关联企业、投资、风险、任职（需双参数：企业名+人名） |
| qcc-ipr | `mcp_qcc_ipr_*` | 专利、商标、软著、著作权、域名、ICP备案 |
| qcc-operation | `mcp_qcc_operation_*` | 招投标、融资、资质证书、行政许可、税务、信用评价 |
| qcc-history | `mcp_qcc_history_*` | 历史变更记录、历史股东、历史法定代表人 |

### 标准调用顺序

**第一步：实体锁定**

```
mcp_qcc_company_get_company_by_query(searchKey="企业简称")
```

- 返回唯一匹配 → 直接用统一社会信用代码继续
- 返回多候选 → **必须展示给用户选择，不能自动选择**
- 返回未匹配 → 提示用户检查关键词

**第二步：核心工商信息（并行调用）**

```python
mcp_qcc_company_get_company_registration_info(searchKey="信用代码")  # 工商注册
mcp_qcc_company_get_shareholder_info(searchKey="信用代码")           # 股东结构
mcp_qcc_company_get_actual_controller(searchKey="信用代码")          # 实际控制人
mcp_qcc_company_get_key_personnel(searchKey="信用代码")              # 高管
mcp_qcc_company_get_external_investments(searchKey="信用代码")       # 对外投资
mcp_qcc_company_get_contact_info(searchKey="信用代码")               # 联系方式
```

**第三步：风险扫描（并行调用）**

```python
mcp_qcc_risk_get_dishonest_info(searchKey="信用代码")                # 失信
mcp_qcc_risk_get_judgment_debtor_info(searchKey="信用代码")          # 被执行人
mcp_qcc_risk_get_high_consumption_restriction(searchKey="信用代码")  # 限高
mcp_qcc_risk_get_business_exception(searchKey="信用代码")            # 经营异常
mcp_qcc_risk_get_administrative_penalty(searchKey="信用代码")        # 行政处罚
mcp_qcc_risk_get_case_filing_info(searchKey="信用代码")              # 当前立案
mcp_qcc_risk_get_judicial_documents(searchKey="信用代码")            # 裁判文书
```

**第四步：经营与资质（并行调用）**

```python
mcp_qcc_operation_get_bidding_info(searchKey="信用代码")             # 招投标
mcp_qcc_operation_get_administrative_license(searchKey="信用代码")   # 行政许可
mcp_qcc_operation_get_qualifications(searchKey="信用代码")           # 资质证书
mcp_qcc_operation_get_taxpayer_qualification(searchKey="信用代码")   # 纳税人资质
```

**第五步：知识产权（并行调用）**

```python
mcp_qcc_ipr_get_patent_info(searchKey="信用代码")                    # 专利
mcp_qcc_ipr_get_trademark_info(searchKey="信用代码")                 # 商标
mcp_qcc_ipr_get_software_copyright_info(searchKey="信用代码")        # 软著
```

**第六步：财务数据（按需）**

```python
mcp_qcc_company_get_financial_data(searchKey="信用代码")             # 财务数据
mcp_qcc_company_get_annual_reports(searchKey="信用代码")             # 年报
```

### 查询技巧

- 所有工具均支持企业名称或统一社会信用代码作为 `searchKey`；**优先用统一社会信用代码**，精确无歧义；
- `mcp_qcc_executive_*` 系列需双参数：`searchKey`（企业名/信用代码）+ `personName`（董监高姓名），漏传会失败或返回无关数据；
- 失信/被执行人/限高/经营异常返回"未发现记录"是**正面结果**，要在报告中明确写出来；
- 裁判文书/立案信息条数较多时，重点关注金额最大的案件。

---

## 三、诉讼场景专项用法

### 庭前对手画像

1. 走完上述尽调维度（工商 + 风险 + 经营）；
2. 重点关注：裁判文书（诉讼经验）、失信/被执行人（偿债能力）、限高（执行风险）；
3. 评估对手诉讼资源与执行能力，输出到 `multi-dimensional-analysis.md` 的「⑧ 对手分析」与「⑩ 执行评估」。

### 关键人物背调

```
mcp_qcc_executive_get_executive_dishonest(searchKey="企业名", personName="法定代表人")
mcp_qcc_executive_get_executive_judgment_debtor(searchKey="企业名", personName="法定代表人")
mcp_qcc_executive_get_executive_high_consumption_ban(searchKey="企业名", personName="法定代表人")
mcp_qcc_executive_get_executive_related_companies(searchKey="企业名", personName="法定代表人")
```

### 执行可能性评估

| 信号组合 | 含义 |
|----------|------|
| 失信 + 被执行人 + 限高 | 长期不履行，**执行难度大** |
| 股权冻结 + 终本案件 + 司法拍卖 | 资金紧张，但可能有可处置财产 |
| 对外投资 + 控制企业 | **可执行财产线索**，值得进一步核查 |

---

## 四、红线

1. 多候选主体必须经用户确认，不得自动选择；
2. 尽调数据必须标注**来源工具**与**查询日期**，写入报告；
3. 企业数据工具**不得**用于查法条、案例、案号——那是北大法宝与元典的职责；
4. 未取得工具返回前，不得写出具体工商信息、股权结构、涉诉记录或金额；
5. 报告仅供参考，不构成法律意见；用于诉讼或商业决策前须进一步核实。

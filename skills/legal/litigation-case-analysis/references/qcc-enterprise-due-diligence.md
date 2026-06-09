# 企查查（QCC）企业尽调工作流

> 通过 QCC MCP 工具对诉讼对手/合作方进行多维度尽职调查。

## 工具总览（6个Server，约180个工具）

| Server | 工具前缀 | 覆盖维度 |
|--------|----------|----------|
| qcc-company | `mcp_qcc_company_*` | 工商注册、股东、对外投资、高管、实际控制人、联系方式、年报、财务数据 |
| qcc-risk | `mcp_qcc_risk_*` | 裁判文书、立案、失信被执行人、被执行人、限高、经营异常、行政处罚、股权冻结、司法拍卖、终本案件 |
| qcc-executive | `mcp_qcc_executive_*` | 董监高个人关联企业、投资、风险、任职（需双参数：企业名+人名） |
| qcc-ipr | `mcp_qcc_ipr_*` | 专利、商标、软著、著作权、域名、ICP备案 |
| qcc-operation | `mcp_qcc_operation_*` | 招投标、融资、资质证书、行政许可、税务、信用评价 |
| qcc-history | `mcp_qcc_history_*` | 历史变更记录、历史股东、历史法定代表人 |

## 标准尽调流程

### 第一步：实体锁定

```
mcp_qcc_company_get_company_by_query(searchKey="企业简称")
```

- 返回唯一匹配 → 直接用统一社会信用代码继续
- 返回多候选 → **必须展示给用户选择，不能自动选择**
- 返回未匹配 → 提示用户检查关键词

### 第二步：核心工商信息（并行调用）

```python
# 并行调用，减少等待时间
mcp_qcc_company_get_company_registration_info(searchKey="信用代码")  # 工商注册
mcp_qcc_company_get_shareholder_info(searchKey="信用代码")          # 股东结构
mcp_qcc_company_get_actual_controller(searchKey="信用代码")         # 实际控制人
mcp_qcc_company_get_key_personnel(searchKey="信用代码")             # 高管
mcp_qcc_company_get_external_investments(searchKey="信用代码")      # 对外投资
mcp_qcc_company_get_contact_info(searchKey="信用代码")              # 联系方式
```

### 第三步：风险扫描（并行调用）

```python
mcp_qcc_risk_get_dishonest_info(searchKey="信用代码")               # 失信
mcp_qcc_risk_get_judgment_debtor_info(searchKey="信用代码")         # 被执行人
mcp_qcc_risk_get_high_consumption_restriction(searchKey="信用代码") # 限高
mcp_qcc_risk_get_business_exception(searchKey="信用代码")           # 经营异常
mcp_qcc_risk_get_administrative_penalty(searchKey="信用代码")       # 行政处罚
mcp_qcc_risk_get_case_filing_info(searchKey="信用代码")             # 当前立案
mcp_qcc_risk_get_judicial_documents(searchKey="信用代码")           # 裁判文书
```

### 第四步：经营与资质（并行调用）

```python
mcp_qcc_operation_get_bidding_info(searchKey="信用代码")            # 招投标
mcp_qcc_operation_get_administrative_license(searchKey="信用代码")  # 行政许可
mcp_qcc_operation_get_qualifications(searchKey="信用代码")          # 资质证书
mcp_qcc_operation_get_taxpayer_qualification(searchKey="信用代码")  # 纳税人资质
```

### 第五步：知识产权（并行调用）

```python
mcp_qcc_ipr_get_patent_info(searchKey="信用代码")                  # 专利
mcp_qcc_ipr_get_trademark_info(searchKey="信用代码")               # 商标
mcp_qcc_ipr_get_software_copyright_info(searchKey="信用代码")      # 软著
```

### 第六步：财务数据（如需要）

```python
mcp_qcc_company_get_financial_data(searchKey="信用代码")           # 财务数据
mcp_qcc_company_get_annual_reports(searchKey="信用代码")           # 年报
```

## 查询技巧

### 参数使用
- 所有工具均支持企业名称或统一社会信用代码作为 `searchKey`
- 优先使用**统一社会信用代码**，精确无歧义
- `mcp_qcc_executive_*` 系列需双参数：`searchKey`（企业名/信用代码）+ `personName`（董监高姓名）

### 结果处理
- 失信/被执行人/限高/经营异常返回"未发现记录"是**正面结果**
- 裁判文书/立案信息返回条数较多时，需重点关注金额最大的案件
- 招投标信息中标方记录是企业实力的重要佐证

## 诉讼场景专项用法

### 庭前对手画像
1. 完整走完上述六步
2. 重点关注：裁判文书（诉讼经验）、失信/被执行人（偿债能力）、限高（执行风险）
3. 评估对手诉讼资源和执行能力

### 调查对方关键人物
```
mcp_qcc_executive_get_executive_dishonest(searchKey="企业名", personName="法定代表人")
mcp_qcc_executive_get_executive_judgment_debtor(searchKey="企业名", personName="法定代表人")
mcp_qcc_executive_get_executive_high_consumption_ban(searchKey="企业名", personName="法定代表人")
mcp_qcc_executive_get_executive_related_companies(searchKey="企业名", personName="法定代表人")
```

### 评估执行可能性
- 失信被执行人 + 被执行人 + 限高 → 三无说明执行能力强
- 股权冻结 + 终本案件 + 司法拍卖 → 说明资金紧张，执行难度大
- 对外投资 + 控制企业 → 可执行财产线索

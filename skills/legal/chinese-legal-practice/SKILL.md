---
name: chinese-legal-practice
description: "中国法律实务技能集 — 争议解决、商事合同、公司并购、知识产权、劳动用工、隐私数据、产品合规、监管合规、AI治理、法律诊所、法学教育。覆盖江苏三诚律师事务所全部执业领域。"
version: 1.0.0
author: 余正洪律师
license: MIT
platforms: [linux, macos]
metadata:
  hermes:
    tags: [legal, china, litigation, corporate, ip, compliance]
---

# 中国法律实务技能集

江苏三诚律师事务所 — 合伙制律师事务所
执业领域：民商事诉讼、刑事诉讼、知识产权、公司法/商事合规

## 使用者
- **角色**：律师/法律专业人士
- **律师联系人**：余正洪 律师
- **管辖法院**：江苏省内法院（海门、宜兴、无锡、南通等基层及中级法院）

## MCP 工具（已接入）

### 元典智库（5个工具）
- `mcp_yuandian_search_fagui` — 法规检索（关键词搜索法律法规）
- `mcp_yuandian_search_fatiao` — 法条检索（法规名称+条号精确检索）
- `mcp_yuandian_search_qwal` — 案例检索（关键词+法院地域+年份）
- `mcp_yuandian_get_fagui_detail` — 法规详情（法规ID获取全文）
- `mcp_yuandian_get_fatiao_detail` — 法条详情（法条ID获取完整内容）

### 北大法宝 MCP（9个 HTTP 服务，Bearer token 认证）
- `pkulaw` — 法规搜索（/mcp-law-search-service）
- `pkulaw-law-keyword` — 法规关键词检索（/mcp-law/mcp）
- `pkulaw-case` — 案例检索（/mcp-case/mcp）
- `pkulaw-fatiao` — 法条检索（/mcp-fatiao/mcp）
- `pkulaw-case-search` — 案例搜索（/mcp-case-search-service）
- `pkulaw-law` — 法规查询（/mcp-law）
- `pkulaw-doc-link` — 文档链接（/add-doc-link）
- `pkulaw-law-recognition` — 法规识别（/law_recognition）
- `pkulaw-case-number-recognition` — 案号识别（/case_number_recognition）

### 快查企业数据 MCP（1个 HTTP 服务，discover/call 模式）
- `kuaicha-search` — 企业数据查询引擎（https://bizveris.kuaicha365.com/mcp）
- 认证方式：`open-authorization: Bearer <token>`（非标准 Authorization 头）
- 使用方式：先 `discover` 发现工具，再 `call` 调用具体工具
- 覆盖范围：工商信息、司法风险、知识产权、经营状况、企业筛选
- 数据来源：同花顺旗下快查企业数据引擎

### 企查查 MCP（6个 HTTP 服务，Streamable HTTP 协议）
- `qcc-company` — 企业基座（工商信息、股东、对外投资）
- `qcc-risk` — 司法风险（诉讼、失信、被执行人、34类风险）
- `qcc-ipr` — 知识产权（商标、专利、软著）
- `qcc-operation` — 经营状况（招投标、融资、新闻舆情）
- `qcc-executive` — 高管/上市（董监高、十大股东、财务报表）
- `qcc-history` — 历史信息（变更记录、年报）
- 认证方式：`Authorization: Bearer <token>`
- 平台地址：https://agent.qcc.com
- 特点：180个原子工具、决策性输出、上下文脱水优化Token

**配置位置**：`~/.hermes/config.yaml` → `mcp_servers`
**原始配置**：`~/.claude/settings.json` → `mcpServers`
**认证方式**：`Authorization: Bearer <token>`（北大法宝/元典）；`open-authorization: Bearer <token>`（快查）

## 检索策略（三轮递进）
1. **第一轮**：元典智库 + 北大法宝双源交叉检索
2. **第二轮**：人民法院案例库验证裁判规则（WebFetch）
3. **第三轮**：威科先行/裁判文书网补充特定法院/法官历史裁判

## 模块一：争议解决（诉讼）

### 案件类型
- 股东损害公司债权人利益责任纠纷
- 合同纠纷、公司纠纷
- 股权转让纠纷

### 法律依据
- 中华人民共和国民法典
- 中华人民共和国民事诉讼法
- 公司法（2024修订）

### 诉讼实务要点
- 管辖权确认：级别管辖 + 地域管辖
- 诉讼时效核查：3年普通时效，1年短期时效
- 证据组织：四性验证（真实性、合法性、关联性、充分性）
- 代理词/答辩状撰写规范

## 模块二：商事合同

### 合同手册
- **销售方场景**：客户为供应商时适用
- **采购方场景**：客户为采购方时适用

### 合同法源
- 民法典合同编
- 民法典担保制度司法解释
- 公司法（2024修订）

### 合同审查要点
- 合同主体资格审查
- 条款完整性与合法性
- 违约责任条款合理性
- 争议解决条款（仲裁/诉讼选择）
- 知识产权归属条款

## 模块三：公司并购

### 法律依据
- 公司法（2024修订）、证券法

### 核心内容
- 三会制度（股东会、董事会、监事会）
- 公司章程、股东协议
- 尽职调查：工商内档、涉诉信息、知识产权、劳动用工

## 模块四：知识产权

### 法律依据
- 商标法、专利法、著作权法

### 实务要点
- 权利归属确认
- 侵权判定标准
- 赔偿计算方法
- 行政保护与司法保护选择

## 模块五：劳动用工

### 法律依据
- 劳动合同法
- 劳动争议调解仲裁法
- 工伤保险条例

### 争议解决
- 劳动争议仲裁前置程序 → 人民法院

## 模块六：隐私数据

### 法律依据
- 个人信息保护法
- 数据安全法
- 网络安全法

## 模块七：产品合规

### 法律依据
- 广告法
- 反不正当竞争法
- 消费者权益保护法

## 模块八：监管合规

### 法律依据
- 行政法规制定程序条例
- 立法法

### 监管追踪源
- 中国政府网
- 司法部法律法规数据库

## 模块九：AI治理

### 法律依据
- 生成式人工智能服务管理办法
- 科技伦理审查办法
- 算法推荐管理规定
- 深度合成管理规定

## 模块十：法律诊所
- 江苏三诚律师事务所法律咨询服务

## 模块十一：法学教育
- 使用者：余正洪律师（继续教育/专业提升用途）
- 模式：学习模式（非替答模式）
- 适用：法考体系 + 中国法学教育方式

## 模块十二：涉外法律

### 知识库路径
Obsidian：`法律知识库/11-涉外法律/`

### 核心法律
- 涉外民事关系法律适用法（2011年施行）
- 外商投资法（2020年施行）+ 实施条例
- 外国人在中国就业管理规定（2017年修正）
- 民事诉讼法（涉外编章）

### 核心司法解释
- 涉外民事关系法律适用法司法解释（一）（2020修正）
- 涉外民事关系法律适用法司法解释（二）（2024施行）— 外国法律查明
- 外商投资法司法解释（2020施行）
- 涉外民商事案件适用国际条约和国际惯例若干问题的解释（2024施行）

### 知识沉淀模块（8个）
1. **诉讼流程**：管辖权、起诉材料、证据公证认证、审理程序（答辩期30天/上诉期30天）、外国判决承认与执行
2. **非诉业务**：外商投资企业设立/变更/注销、国际贸易合同（INCOTERMS 2020）、涉外劳动合规
3. **法律法规**：核心法律条文汇编
4. **司法解释**：涉外法律适用司法解释系列
5. **客户接待**：初次接待流程、文化差异、保密义务
6. **文书模板**：起诉状、仲裁申请书、委托协议、授权委托书、法律意见书、国际货物买卖合同
7. **案例研究**：涉外合同、外商投资、涉外劳动、涉外仲裁案例
8. **实务指南**：律师核心能力、业务拓展、收费标准、产品化

### 涉外案件关键规则
- 涉外民事关系认定（5种情形）：外国当事人/境外居所/境外标的/境外法律事实/其他
- 法律适用：当事人可选择 → 未选择时最密切联系地 → 强制性规定直接适用
- 外国法律查明：7种途径（当事人提供/司法协助/使领馆/查明机构/专家等）
- 准入前国民待遇+负面清单：负面清单外无需审批
- 外籍员工就业：Z字签证→就业许可→就业证→居留证→社保

### Pitfalls
- 外国证据必须经公证认证才能在中国法院使用
- 涉外案件答辩期30天（非15天）、上诉期30天（非15天）
- 外籍员工劳动合同不得超过5年（法律强制规定）
- CISG自动适用（当事人营业地均在缔约国时），无需约定
- 纽约公约成员国仲裁裁决可申请承认和执行，但有6种不予执行情形

## 模块十三：技能管理
- 技能市场画像
- 安全偏好：安装前审查

## 质量标准

### 四性验证
1. **准确性** — 法条条文、案号、法院名称、日期准确无误
2. **真实性** — 引用的法规、案例真实存在，非编造或已失效
3. **合法性** — 法律依据与结论符合现行有效法律规定
4. **关联性** — 引用内容与待解决问题具有实质关联

### 验证方法
- 法条引用：北大法宝 + 华宇元典交叉验证，确认时效性
- 案例检索：多平台搜索，优先最高人民法院入库案例和权威案例
- 所有结论必须有明确来源链接或法条编号支撑

### 法律文书要求
- **格式**：A4纸，仿宋体（正文），黑体（标题），方正小标宋简体（文书标题）
- **引用规范**：法条编号+条文内容+来源链接
- **案例引用**：案号+法院+裁判要旨，优先援引最高人民法院入库案例

## 安全要求
- 当事人敏感信息（姓名、身份证号、联系方式、住址、银行账号）禁止输出到外部请求
- 法律检索前先脱敏处理
- 交付前四性验证

## OCR 证据读取能力

开庭时可拍照识别证据内容，自动做法律分析。

**技术栈**：tesseract OCR + chi_sim 中文语言包 + pytesseract

**使用方式**：
```
保存图片到本机 → 告诉路径 → OCR识别 → 法律分析
示例："读取桌面上的合同照片"
```

**支持内容**：打印合同、转账凭证、聊天记录、营业执照、判决书、发票

**Pitfall**：
- GitHub 下载 chi_sim.traineddata 经常超时，用 jsdelivr CDN 镜像
- vision_analyze 在 mimo-v2.5-pro 下有 API Key 问题，用 tesseract 替代
- 手写文字识别率低，优先拍打印件

详细配置见 `references/ocr-setup.md`

## MCP 接入注意事项

### Stdio 服务器配置（如元典智库）
```bash
# 正确方式
hermes mcp add yuandian --command "node" --args "/path/to/yuandian-mcp-server.js"
# 自动确认
echo "Y" | hermes mcp add yuandian --command "node" --args "..."
```

### HTTP 服务器配置（如北大法宝）
`hermes mcp add` **不支持** `--header` 参数。对于需要 Bearer token 认证的 HTTP MCP 服务，必须手动编辑 config.yaml：

```bash
# 使用 venv 的 Python（系统 Python 没有 pyyaml）
~/.hermes/hermes-agent/venv/bin/python3 -c "
import yaml, os
config_path = os.path.expanduser('~/.hermes/config.yaml')
with open(config_path, 'r') as f:
    config = yaml.safe_load(f)
config['mcp_servers']['pkulaw'] = {
    'type': 'http',
    'url': 'https://apim-gateway.pkulaw.com/mcp-law-search-service',
    'headers': {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer <token>'
    }
}
with open(config_path, 'w') as f:
    yaml.dump(config, f, default_flow_style=False, allow_unicode=True)
"
```

### MCP 批量配置技巧

当需要一次性添加多个 MCP Server（如企查查6个Server），用 Python 脚本批量写入 config.yaml：

```python
import yaml, os
config_path = os.path.expanduser('~/.hermes/config.yaml')
with open(config_path) as f:
    config = yaml.safe_load(f)

# 批量添加
servers = {
    "qcc-company": {"type": "http", "url": "https://...", "headers": {"Authorization": "Bearer <token>"}},
    "qcc-risk":    {"type": "http", "url": "https://...", "headers": {"Authorization": "Bearer <token>"}},
    # ...更多 server
}
for name, server in servers.items():
    config['mcp_servers'][name] = server

with open(config_path, 'w') as f:
    yaml.dump(config, f, default_flow_style=False, allow_unicode=True)
```

**注意**：必须用 venv 的 Python（`~/.hermes/hermes-agent/venv/bin/python3`），系统 Python 没有 pyyaml。

### MCP 认证头差异

| 平台 | 认证头 | 值格式 |
|------|--------|--------|
| 北大法宝 | `Authorization` | `Bearer <token>` |
| 元典智库 | 无（stdio 方式） | N/A |
| 快查企业 | `open-authorization` | `Bearer <token>`（非标准头名） |
| 企查查 | `Authorization` | `Bearer <token>` |

**注意**：快查企业使用 `open-authorization` 而非标准 `Authorization`，配置时容易混淆。

### MCP 工具命名规则
工具名格式：`mcp_{server_name}_{tool_name}`
- 连字符和点号替换为下划线
- 示例：server `pkulaw-case`, tool `get_case_list` → `mcp_pkulaw_case_get_case_list`
- 元典智库：`mcp_yuandian_search_fagui`, `mcp_yuandian_search_fatiao`, `mcp_yuandian_search_qwal` 等
- 北大法宝：`mcp_pkulaw_case_get_case_list`, `mcp_pkulaw_law_recognition_law_recognition` 等

### 配置来源
- **Claude Code 原始配置**：`~/.claude/settings.json` → `mcpServers` 节
- **Hermes 配置**：`~/.hermes/config.yaml` → `mcp_servers` 节
- **北大法宝参考**：`~/.claude/projects/-Users-yuzhenghong/memory/reference_pkulaw_mcp.md`

### 常见 Pitfalls
1. **config.yaml 受保护**：不能用 patch/write_file 编辑，必须用 terminal + venv Python
2. **MCP 工具在网关重启后可能丢失**：需要重新 `hermes mcp add`（stdio 服务）
3. **HTTP 服务配置持久化**：手动编辑 config.yaml 的 HTTP 服务配置不会丢失
4. **北大法宝是 9 个独立 HTTP 服务**：不是单个 stdio 服务器
5. **前置依赖**：`pip install 'hermes-agent[mcp]'` 安装 MCP SDK

## OCR 与图片识别

### vision_analyze 工具
- 接收图片（本地路径、URL、截图）
- 识别图片中的文字（OCR）和理解图片内容
- 当前模型（mimo-v2.5-pro）可能有 API Key 问题，需备用方案

### Tesseract OCR 备用方案
当 vision_analyze 失败时，使用 tesseract：
```bash
# 安装
brew install tesseract

# 中文语言包（GitHub 超时时用 jsdelivr 镜像）
curl -L --max-time 60 -o /tmp/chi_sim.traineddata \
  "https://cdn.jsdelivr.net/gh/tesseract-ocr/tessdata_fast@main/chi_sim.traineddata"
cp /tmp/chi_sim.traineddata /usr/local/share/tessdata/

# 使用（Python）
python3 -c "
import pytesseract
from PIL import Image
img = Image.open('/path/to/image.png')
text = pytesseract.image_to_string(img, lang='chi_sim+eng')
print(text)
"
```

### 飞书图片集成
- ChatCCC 自动下载飞书图片到 `~/.chatccc/images/downloads/`
- 网关自动处理图片并通过 vision_analyze 分析
- 需要飞书应用权限：`im:chat:readonly`, `im:chat`, `im:chat:read`
- 网关日志关键词：`Image routing: text (mode=text). Pre-analyzing N image(s)`

### 开庭场景图片识别
- 拍照证据（合同、借条、转账记录、聊天记录）→ tesseract OCR
- 识别后自动做法律分析（质证要点、法条引用）
- 手写内容识别率较低，优先拍打印件

## 可用集成状态
| 集成 | 状态 | 说明 |
|------|------|------|
| 元典智库 MCP | ✓ 已连接 | 法规检索、法条检索、案例检索（5个工具） |
| 北大法宝 MCP | ✓ 已连接 | 法规搜索、案例检索、法条检索等（9个 HTTP 服务） |
| 快查企业数据 MCP | ✓ 已连接 | 企业工商、司法风险、知识产权、经营状况等（discover/call 模式） |
| 企查查 MCP | ✓ 已连接 | 企业全维度数据：工商/司法/知产/经营/高管/历史（6个 Server，180个工具） |
| 飞书 | ✓ 已连接 | 通过ChatCCC桥接 |
| 人民法院案例库 | WebFetch | https://rmfyalk.court.gov.cn |
| 国家法律法规数据库 | WebFetch | https://flk.npc.gov.cn |
| 中国裁判文书网 | WebFetch | https://wenshu.court.gov.cn |

## 参考文件
- `references/china-law-knowledge-bases.md` — 国内法知识库检索源配置
- `references/ocr-setup.md` — OCR配置
- `references/pkulaw-mcp-services.md` — 北大法宝 MCP 服务详情
- `references/foreign-law-knowledge-workflow.md` — 涉外法律知识沉淀工作流（8模块+MCP检索+交叉验证）
- `references/hermes-mcp-setup.md` — Hermes MCP 设置指南
- `references/evidence-photo-ocr.md` — 证据图片 OCR 识别（飞书图片工作流 + tesseract 配置）

## 完整 MCP 工具清单（2026-06-02 更新）

| 来源 | Server 数量 | 工具数 | 认证方式 | 用途 |
|------|-----------|--------|---------|------|
| 元典智库 | 1 (stdio) | 5 | 本地进程 | 法规/法条/案例检索 |
| 北大法宝 | 9 (HTTP) | 9 | Authorization: Bearer | 法规/案例/法条/案号识别 |
| 快查企业 | 1 (HTTP) | discover/call | open-authorization: Bearer | 企业数据查询 |
| 企查查 | 6 (HTTP) | 180 | Authorization: Bearer | 企业全维度数据 |
| **合计** | **17** | **201** | | |

### MCP HTTP 服务器配置模式

对于需要 Bearer token 认证的 HTTP MCP 服务，必须手动编辑 config.yaml：

```yaml
# ~/.hermes/config.yaml → mcp_servers 节
server-name:
  type: http
  url: https://api.example.com/mcp/endpoint
  headers:
    Authorization: Bearer <token>
```

⚠️ `hermes mcp add` 不支持 `--header` 参数，HTTP 服务必须用 Python 编辑 config.yaml

### 图片 OCR 能力

飞书图片自动下载到 `~/.chatccc/images/downloads/`，可用 pytesseract 识别中文：
- tesseract + chi_sim：已安装
- 语言包修复：从 jsdelivr CDN 下载（GitHub 会超时）
- 详见：`references/evidence-photo-ocr.md`

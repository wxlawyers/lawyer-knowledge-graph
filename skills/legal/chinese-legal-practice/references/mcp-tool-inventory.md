# MCP 工具完整清单（2026-06-02 更新）

## 已接入 MCP Server（17个）

### 北大法宝（9个 HTTP 服务）
| Server | URL | 能力 |
|--------|-----|------|
| pkulaw | /mcp-law-search-service | 法规搜索 |
| pkulaw-law-keyword | /mcp-law/mcp | 法规关键词检索 |
| pkulaw-case | /mcp-case/mcp | 案例检索 |
| pkulaw-fatiao | /mcp-fatiao/mcp | 法条检索 |
| pkulaw-case-search | /mcp-case-search-service | 案例搜索 |
| pkulaw-law | /mcp-law | 法规查询 |
| pkulaw-doc-link | /add-doc-link | 文档链接 |
| pkulaw-law-recognition | /law_recognition | 法规识别 |
| pkulaw-case-number-recognition | /case_number_recognition | 案号识别 |

### 元典智库（1个 stdio 服务，5个工具）
- search_fagui — 法规检索
- search_fatiao — 法条检索
- search_qwal — 案例检索
- get_fagui_detail — 法规详情
- get_fatiao_detail — 法条详情

### 快查企业数据（1个 HTTP 服务，discover/call 模式）
- kuaicha-search — https://bizveris.kuaicha365.com/mcp
- 认证：open-authorization: Bearer <token>
- 覆盖：工商、司法、知产、经营、筛选

### 企查查智能体平台（6个 HTTP 服务）
| Server | URL | 能力 |
|--------|-----|------|
| qcc-company | /mcp/company/stream | 企业基座（工商、股东、对外投资） |
| qcc-risk | /mcp/risk/stream | 司法风险（34类风险、失信、被执行人） |
| qcc-ipr | /mcp/ipr/stream | 知识产权（商标、专利、软著） |
| qcc-operation | /mcp/operation/stream | 经营状况（招投标、融资、新闻） |
| qcc-executive | /mcp/executive/stream | 高管/上市（董监高、十大股东） |
| qcc-history | /mcp/history/stream | 历史信息（变更记录、年报） |

认证：Authorization: Bearer <token>
平台：https://agent.qcc.com
特点：180个原子工具、决策性输出、上下文脱水优化Token

### 法智法律检索（CLI 技能，非 MCP）
- law-search — https://bizveris.kuaicha365.com/api_route/law_gpt
- 认证：FAZHI_LAW_API_KEY
- 命令：search-law / search-case / search-web

## 配置位置
- Hermes：~/.hermes/config.yaml → mcp_servers 节
- Claude Code：~/.claude/settings.json → mcpServers 节

## 认证方式
- 北大法宝/元典：Authorization: Bearer <token>
- 快查：open-authorization: Bearer <token>
- 企查查：Authorization: Bearer <token>

## 注意事项
1. hermes mcp add 不支持 --header，HTTP 服务必须手动编辑 config.yaml
2. config.yaml 受保护，不能用 patch/write_file 编辑，必须用 terminal + venv Python
3. 快查的认证头名是 open-authorization（非标准 Authorization）
4. 企查查使用 Streamable HTTP 协议

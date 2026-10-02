# MCP 工具清单（2026-10-02 校准）

> 本文档是**快照**，不是权威来源。实际可用的工具名与参数，一律以当次会话的 MCP `tools/list` 返回为准。
> 上一版为 2026-06-02，本次校准修正了三处过时内容：元典不再作为主检索源、补入启信慧眼、配置路径补全三端。

## 一、工具分工红线（最高优先级）

| 任务类型 | 允许使用的工具 | 禁止使用的工具 |
|----------|----------------|----------------|
| 法条、司法解释、案例、案号检索 | 北大法宝（主）、元典（交叉核验） | 一切企业数据工具 |
| 企业尽调（工商、股权、涉诉、经营风险） | 当前环境已配置的企业数据 MCP（启信慧眼 / 企查查 / 快查或其他同类，**不分先后**） | 北大法宝、元典 |

两类系统互相不能替代。不要为了省事把它们的工具混着调；企业数据工具之间则可以按可用性和覆盖维度自由选择、组合印证。

## 二、法律法规与案例检索

### 北大法宝（主检索源）

按独立 HTTP 服务接入，按用途分四组：

| 用途 | 服务 | 端点位 |
|------|------|--------|
| 法规检索 | `pkulaw`、`pkulaw-law`、`pkulaw-law-keyword` | `/mcp-law-search-service`、`/mcp-law`、`/mcp-law/mcp` |
| 精准法条 | `pkulaw-fatiao` | `/mcp-fatiao/mcp` |
| 案例检索 | `pkulaw-case`、`pkulaw-case-search` | `/mcp-case/mcp`、`/mcp-case-search-service` |
| 辅助能力 | `pkulaw-doc-link`、`pkulaw-law-recognition`、`pkulaw-case-number-recognition` | `/add-doc-link`、`/law_recognition`、`/case_number_recognition` |

认证方式：`Authorization: Bearer <token>`（env：`PKULAW_TOKEN`）

路由与参数规范以已安装的 `pkulaw-mcp-*` 技能族为准：`pkulaw-mcp-legal-research`（总路由）、`pkulaw-mcp-law-retrieval`（法规）、`pkulaw-mcp-case-retrieval`（案例）、`pkulaw-mcp-fatiao-precise`（精准法条）、`pkulaw-mcp-citation-validator`（引用核验）。

### 元典（交叉核验用）

| 能力 | 现状 | 用途 |
|------|------|------|
| 法规检索 | 可靠 | 与法宝结果交叉核验，找地方法院审判指导意见效果好 |
| 法条检索 | 主流法条可用 | 二次比对条文原文 |
| 案例检索 | **不可靠** | 非主流案由常返回不相关案例，带日期的查询返回旧案例；**不作为类案来源** |

接入方式：stdio，`node ~/.claude/mcp-servers/yuandian/yuandian-mcp-server.js`

## 三、企业尽调

> 以下工具**不分先后**。以当前环境实际配置且可用的为准；你也可以使用自己配置的其他企业数据 MCP。选用原则：哪个可用、哪个覆盖你要的维度就用哪个，也可组合使用做交叉印证。

### 启信慧眼（Codex / Claude Code 环境）

- MCP 名：`qixin`，地址 `https://mcp.qixin.com/mcp`
- 覆盖：工商信息、股权穿透、实际控制人、关联关系、对外投资、经营风险、涉诉情况、按条件筛企业
- 使用要点：
  1. 新会话首次调用必须**先** `lookup(path="/instructions")` 读使用说明；
  2. 用 `enterprise_resolve` 锁定企业主体，多候选时必须让用户选择；
  3. 不熟悉有哪些维度时用 `catalog_get` 发现能力，调 `api_spec_get` 拿入参规格，再 `api_call`；
  4. 大响应按返回的 `result_ref` 用 `result_query` 钻取；
  5. 对外署名一律用「启信慧眼」。

### 企查查（Hermes 环境）

6 个 Streamable HTTP 服务：`qcc-company`（企业基座）、`qcc-risk`（34 类司法风险）、`qcc-ipr`（知识产权）、`qcc-operation`（经营状况）、`qcc-executive`（高管/上市）、`qcc-history`（历史变更）。约 180 个原子工具。

认证方式：`Authorization: Bearer <token>`；平台 https://agent.qcc.com

尽调工作流见 `skills/legal/litigation-case-analysis/references/enterprise-due-diligence-workflow.md`。

### 快查365（Hermes 环境）

- MCP：`kuaicha-search`，`https://bizveris.kuaicha365.com/mcp`，discover/call 模式
- CLI 技能：`law-search`（法律检索）、`kuaicha-search`（企业数据）
- 认证方式：`open-authorization: Bearer <token>`（**非标准头名，容易配错**）

## 四、三端配置位置对照

| 运行环境 | 配置文件 | 当前已配置 |
|----------|----------|------------|
| Codex | `~/.codex/config.toml` → `[mcp_servers.*]` | 法宝 9 个、启信慧眼、元典、mimo-vision、cua_repl |
| Claude Code | `~/.claude.json` → `mcpServers` | 启信慧眼、元典、wpsnote、法宝 10 个、mimo-vision |
| Hermes | `~/.hermes/config.yaml` → `mcp_servers` | 快查、法宝 9 个、企查查 6 个、元典 |

> 三端不是同一份配置。改一处不影响另一处；排查「工具用不了」时先确认当前在哪个环境。

## 五、认证方式

| 平台 | 认证头 | 值格式 |
|------|--------|--------|
| 北大法宝 | `Authorization` | `Bearer <token>` |
| 启信慧眼 | `Authorization` | `Bearer <token>` |
| 企查查 | `Authorization` | `Bearer <token>` |
| 快查 | `open-authorization` | `Bearer <token>`（非标准头名） |
| 元典 | 无（stdio 方式） | N/A |

## 六、工具命名规则

工具名格式为 `mcp_{server_name}_{tool_name}`：server 名中的连字符、点号替换为下划线。

示例：server `pkulaw-case` + tool `get_case_list` → `mcp_pkulaw_case_get_case_list`。

不同客户端的前缀可能不同（如 `mcp__qixin__lookup`），仍以当次会话 `tools/list` 为准。

## 七、注意事项

1. `hermes mcp add` 不支持 `--header`，需要 Bearer 认证的 HTTP 服务必须手动编辑 `config.yaml`（方法见 `mcp-http-configuration.md`）；
2. `config.yaml` 受保护，不能用 patch/write_file 直接编辑，须用 venv Python（`~/.hermes/hermes-agent/venv/bin/python3`）；
3. 快查的认证头名是 `open-authorization`，不是 `Authorization`；
4. 北大法宝是多个独立 HTTP 服务而非单个 stdio 服务器，某个服务报 "not connected" 时先换同组其他服务；
5. stdio 服务（元典）重启后可能需要重新添加。

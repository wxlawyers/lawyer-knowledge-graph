# 北大法宝 MCP 服务配置参考

## Token
`c6564a25-a26e-3e3d-aef7-dc6e2d1b6ccc`
认证方式：`Authorization: Bearer <token>`

## 9个 HTTP 服务端点

所有服务基地址：`https://apim-gateway.pkulaw.com`

| 服务名 | 端点 | 功能 |
|--------|------|------|
| pkulaw | /mcp-law-search-service | 法规搜索 |
| pkulaw-law-keyword | /mcp-law/mcp | 法规关键词检索 |
| pkulaw-case | /mcp-case/mcp | 案例检索 |
| pkulaw-fatiao | /mcp-fatiao/mcp | 法条检索 |
| pkulaw-case-search | /mcp-case-search-service | 案例搜索 |
| pkulaw-law | /mcp-law | 法规查询 |
| pkulaw-doc-link | /add-doc-link | 文档链接 |
| pkulaw-law-recognition | /law_recognition | 法规识别 |
| pkulaw-case-number-recognition | /case_number_recognition | 案号识别 |

## 配置方式

北大法宝是 HTTP 类型 MCP 服务（非 stdio），需要在 `~/.hermes/config.yaml` 的 `mcp_servers` 中配置：

```yaml
mcp_servers:
  pkulaw:
    type: http
    url: https://apim-gateway.pkulaw.com/mcp-law-search-service
    headers:
      Content-Type: application/json
      Authorization: Bearer c6564a25-a26e-3e3d-aef7-dc6e2d1b6ccc
  # ... 其余8个服务类似
```

**注意**：`hermes mcp add` 命令不支持 `--header` 参数，HTTP 类型带自定义 header 的服务需要直接编辑 config.yaml 添加。

## Hermes 添加 HTTP MCP 服务的正确方法

```bash
# 方法：用 venv 的 Python 直接编辑 config.yaml
~/.hermes/hermes-agent/venv/bin/python3 -c "
import yaml, os
config_path = os.path.expanduser('~/.hermes/config.yaml')
with open(config_path, 'r') as f:
    config = yaml.safe_load(f)
config['mcp_servers']['服务名'] = {
    'type': 'http',
    'url': 'https://...',
    'headers': {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer token'
    }
}
with open(config_path, 'w') as f:
    yaml.dump(config, f, default_flow_style=False, allow_unicode=True)
"
```

## 北大法宝库别编码（供 WebFetch 备用）

| 编码 | 库名 |
|------|------|
| law | 法律法规 |
| case | 司法案例 |
| journal | 法学期刊 |
| lawfirm | 法宝律师 |
| reference | 专题参考 |
| english | 英文译本 |
| procuratorate | 检察文书 |
| penalty | 行政处罚 |
| video | 法宝视频 |
| asst | 智能助手 |

## Claude Code 原始配置位置
`~/.claude/settings.json` → `mcpServers` 节
参考记忆文件：`~/.claude/projects/-Users-yuzhenghong/memory/reference_pkulaw_mcp.md`

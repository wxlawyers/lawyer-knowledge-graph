# 北大法宝 OpenAPI 接入现状

## 官方文档
- **地址**：https://openApi.pkulaw.com
- **框架**：MkDocs Material

## 已公开的 API

### 自动登录接口
- **地址**：`GET https://login.pkulaw.com/Account/GroupLogin`
- **参数**：groupUserName, sign, userName, phoneNumber, menu, redirectUrl
- **用途**：集团用户免密登录并跳转到指定栏目

### 子账号解绑
- **地址**：`GET https://login.pkulaw.com/Account/UnbindGroupUser`
- **参数**：groupUserName, sign, userName

## 未公开的数据检索 API
官方文档未列出任何数据检索/搜索接口。当前 MCP 服务器使用的接口：
- `/api/case/PostArticlesOfLawByCaseNumber` — 不在官方文档中，属于内部接口

## 法宝库别编码（可能对应的工具）
| 编码 | 库名 | 可能的工具 |
|------|------|-----------|
| law | 法律法规 | 法规检索 |
| case | 司法案例 | 案例检索 |
| journal | 法学期刊 | 期刊检索 |
| lawfirm | 法宝律师 | 律师检索 |
| reference | 专题参考 | 专题检索 |
| english | 英文译本 | 英文法规检索 |
| procuratorate | 检察文书 | 检察文书检索 |
| penalty | 行政处罚 | 处罚检索 |
| video | 法宝视频 | 视频检索 |

## 下一步
1. 联系北大法宝客户获取完整 API 文档和私钥
2. 确认每个库别的搜索接口路径和参数格式
3. 扩展 pkulaw-mcp-server.js 支持全部9个工具

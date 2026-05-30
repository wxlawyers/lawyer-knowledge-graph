# 国内法知识库检索源配置

## 一级检索源（优先，有MCP集成）

### 华宇元典智库 MCP（5个 stdio 工具）
- `mcp_yuandian_search_fagui` — 法规检索
- `mcp_yuandian_search_fatiao` — 法条检索
- `mcp_yuandian_search_qwal` — 案例检索
- `mcp_yuandian_get_fagui_detail` — 法规详情
- `mcp_yuandian_get_fatiao_detail` — 法条详情

### 北大法宝 MCP（9个 HTTP 服务）
- `mcp_pkulaw_*` — 法规搜索、案例检索、法条检索、法规识别、案号识别等
- 详见 `pkulaw-mcp-services.md`

## 二级检索源（补充，无MCP集成）

### 人民法院案例库
- **URL**：https://rmfyalk.court.gov.cn
- **内容**：最高人民法院入库案例、指导性案例、参考性案例
- **检索方式**：WebFetch / 浏览器访问
- **优先级**：对于裁判规则验证，人民法院案例库入库案例 > 一般典型案例

### 国家法律法规数据库
- **URL**：https://flk.npc.govcn
- **内容**：法律、行政法规、地方性法规、司法解释正式版本

### 中国裁判文书网
- **URL**：https://wenshu.court.gov.cn
- **内容**：全国法院生效裁判文书

## 检索策略（三轮递进）
1. **第一轮**：元典智库 + 北大法宝双源交叉检索
2. **第二轮**：人民法院案例库验证裁判规则（WebFetch）
3. **第三轮**：威科先行/裁判文书网补充特定法院/法官历史裁判

## 法院级别权重（案例参考价值）
1. 最高人民法院入库案例/指导性案例 — 强制参考
2. 最高人民法院公报案例/典型案例 — 高度参考
3. 江苏省高级人民法院典型案例 — 地域高度参考
4. 同一中级法院辖区类案 — 重要参考
5. 同一基层法院/同一法官历史裁判 — 辅助参考

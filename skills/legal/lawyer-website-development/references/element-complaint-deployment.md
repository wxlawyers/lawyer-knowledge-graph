# 要素式起诉状网站部署记录

## 部署信息

| 项目 | 详情 |
|------|------|
| 本地路径 | `~/Documents/element-complaint-website/index.html` |
| GitHub仓库 | `wxlawyers/lawyer-knowledge-graph` |
| 网站路径 | `website/tools/element-complaint/index.html` |
| 访问地址 | `https://wxlawyers.github.io/lawyer-knowledge-graph/website/tools/element-complaint/` |

## 技术实现

- 单文件HTML（52KB，927行）
- 内联CSS+JS，零外部依赖
- 配色：深蓝(#1a365d)+白+金(#ffd700)
- 功能：搜索过滤、分类筛选、卡片展开/收起、模态框详情、使用指南、FAQ手风琴、打印模板
- 33个案由（对标最高法67类示范文本，覆盖率49%）
- 每个案由含：要素清单、关键证据、法律依据、实务提示
- 筛选分类：全部、合同纠纷、劳动争议、侵权纠纷、婚姻家事、金融纠纷、知产纠纷、建设工程、公司股权、行政纠纷、执行

## GitHub Pages启用步骤

1. 访问 `https://github.com/wxlawyers/lawyer-knowledge-graph/settings/pages`
2. Source 选择 `master` 分支
3. 文件夹选择 `/website`
4. 点击 Save
5. 等待1-2分钟生效

## 后续可扩展工具

| 工具 | 路径 | 说明 |
|------|------|------|
| 赔偿计算器 | `tools/calculator/` | 交通事故/工伤/劳动纠纷赔偿计算 |
| 法律法规速查 | `tools/law-search/` | 常用法律法规快速查询 |
| 合同模板库 | `tools/templates/` | 各类合同模板下载 |
| 诉讼费用计算器 | `tools/court-fee/` | 诉讼费/律师费估算 |

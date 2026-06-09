# 律师工具类网站开发模式

## 适用场景

当律师网站需要包含独立工具（要素式起诉状查询、赔偿计算器、法律文书生成器等），使用 `/website/tools/` 子目录模式部署。

## 目录结构

```
website/
├── index.html                    # 主站
├── images/
└── tools/
    ├── element-complaint/        # 要素式起诉状查询
    │   └── index.html            # 单文件HTML（内联CSS+JS）
    ├── compensation-calculator/  # 赔偿计算器
    │   └── index.html
    └── document-generator/       # 文书生成器
        └── index.html
```

## 单文件HTML工具规范

每个工具是独立的单HTML文件，内联CSS+JS，零外部依赖。

### 标准结构
```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>工具名称 — 余正洪律师</title>
    <style>/* 全部内联CSS */</style>
</head>
<body>
    <nav><!-- 导航栏 --></nav>
    <section class="hero"><!-- 工具介绍 --></section>
    <section class="search"><!-- 搜索/筛选 --></section>
    <section class="content"><!-- 核心内容 --></section>
    <footer><!-- 律师信息+免责声明 --></footer>
    <script>/* 全部交互逻辑 */</script>
</body>
</html>
```

### 设计规范
- 配色：深蓝(#1a365d) + 白 + 金(#ffd700)
- 字体：PingFang SC, Microsoft YaHei
- 响应式：移动端优先
- 免责声明：必须在页脚标注"本工具仅供参考，具体以各地法院要求为准"

## GitHub Pages部署

仓库：`wxlawyers/lawyer-knowledge-graph`
Pages source：`/website` 目录（master分支）
访问地址：`https://wxlawyers.github.io/lawyer-knowledge-graph/website/tools/{工具名}/`

⚠️ **PITFALL**：Pages source设为 `/website` 后，工具页面路径必须包含 `/website/` 前缀。

## 推送流程

```bash
cd /tmp && rm -rf lawyer-knowledge-graph
git clone git@github.com:wxlawyers/lawyer-knowledge-graph.git
cp ~/Documents/{工具目录}/index.html /tmp/lawyer-knowledge-graph/website/tools/{工具名}/index.html
cd /tmp/lawyer-knowledge-graph
git add website/tools/{工具名}/index.html
git commit -m "feat: {工具描述}"
git push origin master
rm -rf /tmp/lawyer-knowledge-graph
```

## 法律内容验证

工具中的法律依据必须经MCP工具核实：
1. 法条引用：用 `mcp_yuandian_search_fatiao` 验证条文号与内容对应
2. 司法解释：用 `mcp_yuandian_search_fagui` 验证文号和时效性
3. 交叉验证：关键法条需多源确认

## 要素式起诉状查询工具（参考案例）

文件：`~/Documents/element-complaint-website/index.html`
部署：`website/tools/element-complaint/index.html`
案由数：67类（对标最高法法〔2025〕82号）
功能：搜索筛选 + 要素清单 + 证据列表 + 法律依据 + 实务提示 + 模态框详情 + 打印

### 数据结构
```javascript
{
    name: "案由名称",
    cat: "分类（合同纠纷/侵权纠纷/...）",
    scene: "适用场景描述",
    elements: [["要素名称", "填写说明"], ...],
    evidence: ["证据1", "证据2", ...],
    law: ["法条引用1", "法条引用2", ...],
    tips: ["实务提示1", "实务提示2", ...]
}
```

### 筛选分类
全部、合同纠纷、劳动争议、侵权纠纷、婚姻家事、金融纠纷、知产纠纷、建设工程、公司股权、行政纠纷、执行、海事纠纷、刑事自诉、国家赔偿

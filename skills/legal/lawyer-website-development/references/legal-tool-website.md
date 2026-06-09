# 法律工具网站开发指南

## 与律师形象网站的区别

| 维度 | 律师形象网站 | 法律工具网站 |
|------|------------|------------|
| 目的 | 品牌展示、案源获取 | 提供实用工具、吸引同行 |
| 内容 | 律师简介、服务、案例 | 法律数据、模板、查询功能 |
| 用户 | 当事人 | 律师+当事人 |
| 更新频率 | 低 | 高（随法规更新） |
| SEO策略 | 地域+领域关键词 | 工具名称+案由关键词 |

## 成功案例：要素式起诉状助手

**网站地址**：`https://wxlawyers.github.io/lawyer-knowledge-graph/website/tools/element-complaint/`

**核心功能**：
1. 搜索过滤（关键词+分类按钮）
2. 案由卡片（名称+场景+要素清单+证据+法条+提示）
3. 模态框详情（完整要素表格+打印功能）
4. 使用指南（3步流程）
5. FAQ（手风琴展开式）

**数据结构**（每个案由）：
```javascript
{
    name: "案由名称",
    cat: "分类",
    scene: "适用场景描述",
    elements: [
        ["要素名称", "填写说明"],
        // ...
    ],
    evidence: ["证据1", "证据2", ...],
    law: ["法律依据1", "法律依据2", ...],
    tips: ["实务提示1", "实务提示2", ...]
}
```

## 法律内容四性验证

**⚠️ 铁律：所有法律工具网站内容必须通过四性验证**

| 验证维度 | 方法 | 禁止事项 |
|---------|------|---------|
| 准确性 | MCP工具逐条核实 | ❌ 凭记忆写法条 |
| 真实性 | 多源交叉验证 | ❌ 编造案例/数据 |
| 合法性 | 确认现行有效 | ❌ 引用已废止法规 |
| 关联性 | 与案由直接相关 | ❌ 无关法条堆砌 |

**批量核实方法**：参考 `legal-research` 技能的 `references/batch-verification.md`

## 部署到GitHub Pages

```bash
# 1. 克隆仓库
cd /tmp && git clone git@github.com:wxlawyers/lawyer-knowledge-graph.git

# 2. 创建工具目录
mkdir -p lawyer-knowledge-graph/website/tools/工具名称/

# 3. 复制文件
cp ~/Documents/工具网站/index.html lawyer-knowledge-graph/website/tools/工具名称/

# 4. 提交推送
cd lawyer-knowledge-graph
git add website/tools/工具名称/
git commit -m "feat: 添加XXX工具页面"
git push origin master

# 5. 清理
rm -rf /tmp/lawyer-knowledge-graph
```

**GitHub Pages设置**：
- 访问 https://github.com/wxlawyers/lawyer-knowledge-graph/settings/pages
- Source: master branch
- Folder: /website
- 等待1-2分钟生效

## 工具网站设计规范

### 必备模块
1. **导航栏**：品牌标识+功能入口
2. **Hero区**：工具说明+统计数据
3. **使用指南**：3步流程卡片
4. **搜索/筛选**：关键词+分类按钮
5. **内容卡片**：网格布局，hover效果
6. **详情模态框**：完整信息+打印按钮
7. **FAQ**：手风琴展开式
8. **页脚**：律师信息+免责声明

### 设计规范
- 配色：深蓝(#1a365d)+白+金(#ffd700)
- 单文件HTML（内联CSS+JS）
- 移动端响应式
- 不依赖外部CDN
- 页脚必须有免责声明

### SEO优化
- title: 工具名称 · 余正洪律师
- meta description: 工具功能描述
- meta keywords: 案由关键词+法律关键词

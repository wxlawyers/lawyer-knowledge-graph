---
name: vibe-coding-legal-tools
description: "Vibe coding for legal tools — use natural language to build calculators, templates, and automation tools for lawyers."
version: 1.0.0
author: Hermes Agent
platforms: [linux, macos]
metadata:
  hermes:
    tags: [legal, vibe-coding, tools, calculators, automation]
auto_invoke: true
examples:
  - "帮我做一个赔偿计算器"
  - "做一个合同模板生成器"
  - "帮我写一个法律文书工具"
---

# Vibe Coding for Legal Tools

Build legal tools using natural language — no coding experience required.

## What is Vibe Coding?

Vibe coding is a workflow where you describe what you want in natural language, and AI generates the code. You test it, provide feedback, and iterate until it works.

```
You: "帮我做一个交通事故赔偿计算器"
AI: [generates code] → [runs tests] → [shows results]
You: "数据错了，江苏是68956元"
AI: [fixes code] → [re-runs] → [shows updated results]
Repeat until done.
```

---

## Workflow for Building Legal Tools

### Step 1: Define Requirements
Describe what you want:
- What type of tool? (calculator, template generator, search tool)
- What inputs does it need?
- What outputs should it produce?
- What data sources? (laws, regulations, standards)

### Step 2: Generate Initial Code
AI generates a working prototype based on your description.

### Step 3: Test and Iterate
- Run the code
- Check results against known values
- Report errors or incorrect data
- AI fixes and re-runs

### Step 4: Verify Data Accuracy
**CRITICAL**: Always verify legal data with authoritative sources:
- Use MCP tools (北大法宝, 元典智库) to verify law references
- Cross-check with official sources
- Don't trust AI-generated legal data without verification

### Step 5: Deploy and Share
- Push to GitHub
- Deploy to GitHub Pages (see [[github-pages-deployment]])
- Share with colleagues

---

## Example: Building a Compensation Calculator

### Session Flow

```
User: "帮我做一个赔偿计算器"
AI: "先做哪个模块？交通事故/工伤/劳动纠纷？"
User: "先做交通事故"
AI: [generates code with default data]
AI: "测试结果：江苏10级伤残=210,844元"
User: "错了，江苏是68956元"
AI: [verifies with 北大法宝, updates data]
AI: "修正后：220,312元"
User: "工伤模块也加上"
AI: [adds work injury module]
User: "再核查三遍"
AI: [runs comprehensive tests]
```

### Key Learnings

1. **Always verify data with MCP tools** — Don't trust AI memory for legal standards
2. **Test with known values** — Compare against official calculators or lawyer experience
3. **Iterate rapidly** — Small changes, quick feedback loops
4. **Document data sources** — Note where each number comes from

---

## Data Verification Checklist

For any legal tool, verify:

| Data Type | Verification Method |
|-----------|---------------------|
| Law articles | Use 北大法宝 or 元典智库 MCP tools |
| Compensation standards | Cross-check with official sources |
| Regional data | Verify with local statistics bureau |
| Court fees | Check with court fee calculator |
| Statute of limitations | Verify with current law |

**Lesson from 2026-06-04**: AI may use outdated or incorrect legal data. Always verify with authoritative sources before deploying.

---

## Tool Types for Lawyers

### Calculators
- Compensation calculators (traffic accident, work injury, labor)
- Court fee calculators
- Interest calculators
- Statute of limitations calculators

### Template Generators
- Contract templates
- Legal document templates
- Evidence list generators
- Case analysis templates

### Search Tools
- Law article search
- Case search
- Company information search
- Legal knowledge base

### Automation Tools
- Batch document processing
- Data extraction from PDFs
- Report generation
- Client communication templates

---

## Deployment Options

| Option | Best For | Difficulty |
|--------|----------|------------|
| **Python script** | Personal use, command line | ⭐ Easy |
| **GitHub Pages** | Sharing with others, web access | ⭐⭐ Medium |
| **Hermes skill** | Integration with Hermes Agent | ⭐⭐ Medium |
| **Web app** | Full-featured applications | ⭐⭐⭐ Hard |

---

## Pitfalls

### Pitfall 1: Trusting AI Legal Data
**Problem**: AI generates incorrect law references or outdated standards
**Solution**: Always verify with MCP tools (北大法宝, 元典智库)

### Pitfall 2: Not Testing Edge Cases
**Problem**: Calculator works for normal cases but fails for edge cases
**Solution**: Test with boundary values (age 59/60/61, work months 5/6/11/12)

### Pitfall 3: Hardcoding Data
**Problem**: Data changes annually (e.g., income standards)
**Solution**: Design for easy data updates, document data sources

### Pitfall 4: Ignoring Legal Nuances
**Problem**: Tool oversimplifies legal rules
**Solution**: Consult with experienced lawyers, add disclaimers

---

## Success Story: Compensation Calculator

Built a comprehensive compensation calculator with:
- 3 modules (traffic accident, work injury, labor dispute)
- 31 provinces data (2025 standards)
- Multiple scenarios (age, disability level, retirement proximity)
- Verified with 北大法宝 and official sources

**Time**: ~3 hours
**Iterations**: 10+ rounds of testing and fixes
**Result**: Deployed to GitHub, shared with colleagues

---

## Success Story: Lawyer Website

Built a professional lawyer website with:
- 欧美律所风格设计
- 中英双语内容
- SEO/GEO优化（结构化数据、FAQ）
- 推广素材（二维码、文字卡片）
- GitHub Pages部署

**详见**：`lawyer-website-development` 技能

---

## Related Skills

- [[legal-analysis-pitfalls]] — Common legal analysis errors
- [[compensation-calculator]] — Compensation calculator tool
- [[github-pages-deployment]] — Deploy to GitHub Pages
- [[legal-document-drafting]] — Legal document templates

---

## Appendix: Lawyer Website Development

Build professional lawyer websites using vibe coding — from design to deployment.

### Design Style (欧美律所风格)

| Element | Spec |
|---------|------|
| Colors | 深蓝(#1a2332) + 金色(#c9a96e) + 白色 |
| Fonts | 衬线体(标题) + 无衬线体(正文)，推荐思源宋体+思源黑体 |
| Layout | 大量留白，全屏英雄区，卡片式服务介绍 |
| Languages | 中英双语（涉外业务推荐） |

### Development Flow

1. **需求确认** — 网站类型、内容模块、风格、语言
2. **设计风格** — 欧美律所风格（深蓝+金色）
3. **生成代码** — AI生成HTML/CSS，响应式布局
4. **部署** — GitHub Pages（见 `references/github-pages-deployment.md`）
5. **优化** — SEO + GEO（见 `references/seo-geo-optimization.md`）

### Key Modules

- Hero区：律师姓名+专业领域+联系方式
- 服务介绍：卡片式展示
- 专业领域：细分业务列表
- 关于律师：执业经历+资质
- 联系方式：电话+微信+地址

### Promotion Materials

**详见**：`references/promotion-materials.md`
- 二维码推广图片（1080×1920，深蓝+金色配色）
- 小红书文字卡片（1080×1080）
- 朋友圈文案模板
- 抖音口播文案

### SEO/GEO Optimization

**详见**：`references/seo-geo-optimization.md`
- 基础SEO（Meta标签、Open Graph、关键词策略）
- GEO优化（JSON-LD结构化数据、FAQ schema）
- 多平台内容分发（知乎、小红书、百度知道、公众号）

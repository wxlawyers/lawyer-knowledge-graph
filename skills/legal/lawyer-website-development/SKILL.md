---
name: lawyer-website-development
description: "律师个人形象网站开发技能 — HTML/CSS静态网站、动画展示片、案例展示、法律科普博客、在线咨询表单、GitHub Pages/Gitee Pages部署。适用于律师建立个人品牌网站、展示专业能力、获取线上案源。"
version: 1.0.0
author: 余正洪律师
metadata:
  hermes:
    tags: [legal, website, branding, deployment]
---

# 律师个人形象网站开发技能

为律师构建专业的个人形象展示网站，用于品牌展示和案源获取。

## 适用场景

- 律师个人品牌网站建设
- 涉外法律服务展示
- 成功案例展示
- 法律科普文章发布
- 在线咨询入口
- **HTML动画展示片**（形象宣传、服务介绍、社交媒体素材）

## 前置检查（必须执行）

**⚠️ PITFALL: 更新前必须确认是"更新现有网站"还是"新建网站"**

用户可能有多个网站项目（涉外、民商事、刑事等），操作前必须确认：

1. 检查 `~/Documents/` 下是否有 `lawyer-website*` 目录
2. 检查 git remote 配置确认目标仓库
3. **直接询问用户**："这是更新您现有的 [领域] 网站，还是新建一个？"

```
错误做法：直接开始修改，用户可能以为你在新建
正确做法：先展示现有项目位置和内容，确认后再动手
```

## 现有项目清单

| 项目 | 路径 | 仓库 | 网站目录 | 内容 |
|------|------|------|----------|------|
| 涉外法律服务 | `~/Documents/lawyer-website/` | `wxlawyers/lawyer-knowledge-graph` | `/docs` | 涉外劳动、合同、知产、合规、企业出海、跨境投资、财富管理、律师简介、联系方式 |
| 要素式起诉状助手 | `~/Documents/element-complaint-website/` | `wxlawyers/lawyer-knowledge-graph` | `/docs/tools/element-complaint/` | 67类案由要素查询、11个官方模板、证据清单、法律依据（对标法〔2025〕82号） |
| 形象照素材 | `~/Desktop/形象照/` | — | — | 律师照片2张 + 微信二维码1张 |

> 如有新项目，更新此表。

**GitHub Pages 地址**：`https://wxlawyers.github.io/lawyer-knowledge-graph/`
**要素式起诉状助手**：`https://wxlawyers.github.io/lawyer-knowledge-graph/tools/element-complaint/`

**⚠️ PITFALL: 远程仓库地址可能配置错误**

本地 `.git/config` 中的 remote origin 可能指向不存在的仓库。**推送前必须验证仓库是否存在**：

```bash
# 检查远程仓库是否存在
curl -s -o /dev/null -w "%{http_code}" https://github.com/USERNAME/REPO_NAME

# 列出用户所有仓库
curl -s "https://api.github.com/users/USERNAME/repos?per_page=100" | grep '"name"'

# 检查仓库是否有 website 或 docs 目录
curl -s "https://api.github.com/repos/USERNAME/REPO_NAME/contents" | grep '"name"'
```

**正确做法**：
1. 先用 API 查找用户的真实仓库
2. 检查仓库中是否有 `website/` 或 `docs/` 目录
3. 修正 remote origin 后再推送
4. 不要假设 `.git/config` 中的地址一定正确

## 网站标准模块

### 1. 导航栏
- 固定顶部，白色背景
- Logo：律师姓名
- 菜单：服务介绍、专业领域、成功案例、法律科普、律师简介、在线咨询
- 移动端：汉堡菜单按钮

### 2. 英雄区（Hero）

**用户偏好：欧美律所风格（2026-06-09确认）**

余律师要求涉外律师网站采用**欧美律所风格**，不是传统的中国律师网站模板。核心特征：

| 元素 | 传统中国风格 | 欧美律所风格（用户要求） |
|------|-------------|----------------------|
| 背景 | 纯色渐变 | **深海军蓝背景**（不是全屏照片背景！） |
| 字体 | 无衬线 | **衬线标题**（Playfair Display）+ 无衬线正文（Inter） |
| 配色 | 蓝+红 | **深海军蓝+金色**（#0a1628 + #c9a96e） |
| 布局 | 信息密集 | **留白多、模块化** |
| 数据展示 | 无 | **10+年、500+案件、98%满意度** |
| 导航 | 中文菜单 | **英文Logo + 中文菜单** |
| 英雄区 | 全屏背景 | **左右布局**（左文字+右照片） |
| 双语 | 纯中文 | **中英文对照**（标题配英文翻译） |

**⚠️ 用户明确纠正（2026-06-09）**：
1. 英雄区**不要做全屏照片背景**，要用**左右布局**（左侧文字+右侧照片）
2. **不要嵌入视频**，只用照片
3. **"涉外法律服务专家"要在一行显示**，不要换行
4. **其他区域文字要配有专业的英文翻译**

**标准英雄区结构（左右布局，非全屏背景）**：
```html
<section class="hero" id="hero">
    <div class="hero-container">
        <div class="hero-content">
            <div class="hero-subtitle">International Legal Services</div>
            <h1>涉外法律服务 <span>专家</span></h1>  <!-- 一行显示，不要<br> -->
            <p>专注涉外法律服务...</p>
            <div class="hero-buttons">
                <a href="#contact" class="btn-primary">免费咨询</a>
                <a href="#services" class="btn-secondary">了解更多</a>
            </div>
        </div>
        <div class="hero-image">
            <img src="images/lawyer-photo-1.jpg" alt="余正洪律师">
        </div>
    </div>
</section>
```

**标准CSS（左右布局）**：
```css
.hero {
    padding-top: 80px;
    min-height: 100vh;
    display: flex;
    align-items: center;
    background: var(--navy);  /* 深蓝背景，不是照片背景 */
}

.hero-container {
    max-width: 1400px;
    margin: 0 auto;
    padding: 80px 60px;
    display: grid;
    grid-template-columns: 1fr 1fr;  /* 左右布局 */
    gap: 80px;
    align-items: center;
}

.hero-image img {
    width: 100%;
    height: 550px;
    object-fit: cover;
    object-position: top;
}

.hero-image::after {  /* 装饰性金色边框 */
    content: '';
    position: absolute;
    top: 30px;
    right: -30px;
    width: 100%;
    height: 100%;
    border: 3px solid var(--gold);
    z-index: -1;
}
```

**多语言对照规范**：每个服务卡片标题下方添加英文、法语、阿拉伯语翻译
```html
<h3>外企劳动争议</h3>
<p class="en-title">Foreign Enterprise Labor Disputes</p>
<p class="fr-title">Litiges du Travail des Entreprises Étrangères</p>
<p class="ar-title">نزاعات العمل في المؤسسات الأجنبية</p>
```

```css
.en-title {
    font-size: 0.8rem;
    color: var(--gold);
    margin-top: 5px;
    font-style: italic;
}

.fr-title {
    font-size: 0.75rem;
    color: var(--text-light);
    margin-top: 3px;
    font-style: italic;
}

.ar-title {
    font-size: 0.75rem;
    color: var(--text-light);
    margin-top: 3px;
    direction: rtl;  /* 阿拉伯语从右到左 */
    font-style: italic;
}
```

**多语言对照表（涉外律师网站标准）**：

| 中文 | 英文 | 法语 | 阿拉伯语 |
|------|------|------|----------|
| 涉外法律服务顾问 | International Legal Services | Services Juridiques Internationaux | الخدمات القانونية الدولية |
| 专业服务领域 | Practice Areas | Domaines de Pratique | مجالات الممارسة المهنية |
| 企业出海 | Enterprise Going Global | Internationalisation des Entreprises | توسع الشركات عالمياً |
| 涉外合同纠纷 | Cross-border Contract Disputes | Litiges Contractuels Transfrontaliers | نزاعات العقود العابرة للحدود |
| 跨境投资与并购 | Cross-border Investment & M&A | Investissement Transfrontalier & Fusions-Acquisitions | الاستثمار العابر للحدود والاندماج والاستحواذ |
| 跨境争议解决 | Cross-border Dispute Resolution | Résolution des Litiges Transfrontaliers | حل النزاعات العابرة للحدود |
| 外企知产保护 | IP Protection for Foreign Enterprises | Protection de la Propriété Intellectuelle | حماية الملكية الفكرية |
| 外企合规咨询 | Compliance Consulting | Conseil en Conformité | استشارات الامتثال |
| 私人财富管理与家事法 | Private Wealth Management & Family Law | Gestion de Patrimoine & Droit de la Famille | إدارة الثروة الخاصة وقانون الأسرة |
| 外企劳动争议 | Foreign Enterprise Labor Disputes | Litiges du Travail des Entreprises Étrangères | نزاعات العمل |
| 关于律师 | About The Lawyer | À Propos de l'Avocat | عن المحامي |
| 联系我们 | Contact Us | Contactez-nous | اتصل بنا |
| 免费咨询 | Free Consultation | Consultation Gratuite | استشارة مجانية |
| 了解更多 | Learn More | En Savoir Plus | اعرف المزيد |

**⚠️ 用户偏好（2026-06-09确认）**：
1. 用户把"专家"改成了"顾问"，标题现在是"涉外法律服务顾问"
2. 用户要求有英文的地方下面翻译成法语和阿拉伯语
3. 导航栏也要中英文对照：服务领域 Services、关于律师 About、联系我们 Contact

**照片布局规范**：网站使用两张不同的律师照片
- **英雄区**：半身照（放在右侧，左侧是文字）
- **关于律师区域**：另一张正式肖像照（放在左侧，右侧是文字介绍）

**微信二维码集成**：放在"联系我们"区域的左侧联系方式下方
```html
<div class="wechat-section">
    <h4>📱 微信咨询</h4>
    <div class="qr-code">
        <img src="images/二维码.jpg" alt="微信二维码">
    </div>
    <p class="wechat-tip">扫码添加微信，获取专业法律咨询</p>
</div>
```

**完整CSS变量**：
```css
:root {
    --navy: #0a1628;
    --dark-blue: #1a2a4a;
    --gold: #c9a96e;
    --light-gold: #d4b87a;
    --white: #ffffff;
    --light-gray: #f5f5f5;
}
```

### 3. 服务介绍
- 4个服务卡片，图标+标题+描述
- 网格布局，hover动画
- 示例：外企劳动争议、涉外合同纠纷、外企知产保护、外企合规咨询

### 4. 专业领域
- 4个领域条目，左侧蓝色边框
- 简洁标题+要点描述

### 5. 成功案例（新增）
- **分类筛选按钮**：全部、劳动争议、合同纠纷、知识产权、合规咨询
- **案例卡片结构**：
  - 头部：类型标签 + 案例标题（深色背景）
  - 结果：绿色背景，✅ 图标 + 胜诉/调解结果
  - 描述：案情简介（2-3句话）
  - 标签：相关关键词

**案例数据来源**：
- 从 Obsidian `01-案件笔记/` 提取真实案例（脱敏）
- 从 `08-裁判规则库/` 提取裁判规则

**⚠️ 注意事项**：
- 案例必须脱敏处理（用"某企业"代替真实名称）
- 不要编造虚假案例，用真实案例改编
- 金额、结果可以保留，但要确保准确

**🚨 铁律：法律内容四性验证（2026-06-07 教训）**

律师网站上的所有法律内容必须通过四性验证（准确性、真实性、合法性、关联性），否则涉嫌虚假宣传：

| 内容类型 | 验证方法 | 禁止事项 |
|---------|---------|---------|
| 案例描述 | 元典智库/北大法宝检索真实案号 | ❌ 无案号的编造案例 |
| 案例结果 | 核实裁判文书 | ❌ 凭印象写"胜诉xx万" |
| 法条引用 | 双源交叉验证（条号+全文） | ❌ 凭记忆写法条 |
| 文章摘要 | 用检索工具核实法律观点 | ❌ 未验证的法律结论 |
| 联系方式 | 用户提供真实信息 | ❌ 编造电话/邮箱/地址 |

**⚠️ 用户说"帮我编写"时的处理规则：**

用户可能说"帮我编写案例""帮我写文章"，但律师网站内容有法律合规红线：
1. **不能编造案例** — 即使用户要求"编写"，也必须基于真实公开案例改编，保留真实案号
2. **不能写未核实的法律结论** — "三条合规路径""五大要点"等必须有法条支撑
3. **不能用占位符联系方式** — 电话、邮箱、地址必须是真实的
4. **检索工具可能找不到涉外案例** — 元典智库对"涉外"关键词匹配不精准，北大法宝MCP可能断连。找不到真实案例时，**只放标题，不放描述**，等用户提供真实素材后再补充

**正确做法：先检索 → 找不到 → 告知用户 → 只放标题 → 等用户提供真实案例**

**错误做法：找不到案例 → 自己编造 → 用户发现内容不真实 → 要求删除**

**安全做法（分阶段上线）**：
1. **第一阶段**：案例和文章只放标题+类型标签，不放描述/结果/摘要
2. **第二阶段**：用元典智库+北大法宝检索核实后，逐步补充详细内容
3. **第三阶段**：每篇内容附带"参考案例：(xxxx)xxxxx号"或"依据：《xx法》第x条"

**案例卡片精简版结构（第一阶段）**：
```html
<div class="case-card">
    <div class="case-header">
        <span class="case-type">劳动争议</span>
        <h3>外企违法解除劳动合同赔偿案</h3>
    </div>
    <!-- 不放结果、描述、标签 -->
</div>
```

**文章卡片精简版结构（第一阶段）**：
```html
<div class="blog-card">
    <div class="blog-image">📋</div>
    <div class="blog-content">
        <div class="blog-meta">
            <span>2026-05-15</span>
            <span>涉外劳动</span>
        </div>
        <h3>外企辞退中国员工的法律要点</h3>
        <!-- 不放摘要描述 -->
    </div>
</div>
```

### 6. 法律科普（新增）
- 文章卡片网格布局
- 每张卡片：渐变色图标区 + 日期 + 分类 + 标题 + 摘要 + 阅读链接
- 6篇文章为宜

**文章素材来源（必须核实后使用）**：
- Obsidian `06-品牌内容/公众号文章/` 已有文章
- `02-法律知识/` 法条解读
- `09-每日法律速报/` 热点解读

**⚠️ 文章内容验证要求**：
- 只放标题和分类标签，不放未核实的摘要
- 正文写完后必须用元典智库+北大法宝核实法条引用
- "三条合规路径""五大要点"等表述必须有法条支撑

### 7. 律师简介
- 左侧：律师照片（或占位符）
- 右侧：姓名、简介、执业领域
- 底部：数据展示（执业年限、代理案件数、客户满意度）

### 8. 在线咨询（新增）
- **双栏布局**：
  - 左侧：联系方式（电话、邮箱、地址、工作时间）+ 微信二维码
  - 右侧：咨询表单（姓名、电话、邮箱、咨询类型、问题描述）

**表单处理方案**：
- 方案A：Formspree（免费，表单提交到邮箱）
- 方案B：EmailJS（免费，直接发送到邮箱）
- 方案C：后端API（需要服务器）
- **方案D（推荐）：mailto: 链接** — 纯前端，无需后端，点击提交后打开邮件客户端

**方案D实现（mailto: 方式）**：
```html
<form id="consultationForm" onsubmit="handleSubmit(event)">
    <input type="text" name="name" placeholder="姓名" required>
    <input type="tel" name="phone" placeholder="电话" required>
    <input type="email" name="email" placeholder="邮箱">
    <select name="type">
        <option>企业出海</option>
        <option>涉外合同纠纷</option>
        <!-- ...其他选项 -->
    </select>
    <textarea name="message" placeholder="咨询内容" required></textarea>
    <button type="submit">提交预约</button>
    <div id="formSuccess" style="display:none;">✅ 预约已提交成功！</div>
</form>

<script>
function handleSubmit(e) {
    e.preventDefault();
    const form = document.getElementById('consultationForm');
    const formData = new FormData(form);
    
    const subject = encodeURIComponent('法律咨询预约 - ' + formData.get('name'));
    const body = encodeURIComponent(
        '姓名: ' + formData.get('name') + '\n' +
        '电话: ' + formData.get('phone') + '\n' +
        '邮箱: ' + (formData.get('email') || '未提供') + '\n' +
        '咨询类型: ' + formData.get('type') + '\n' +
        '咨询内容:\n' + formData.get('message')
    );
    
    window.open('mailto:yuzhenghong86@icloud.com?subject=' + subject + '&body=' + body);
    
    document.getElementById('formSuccess').style.display = 'block';
    form.reset();
    setTimeout(() => {
        document.getElementById('formSuccess').style.display = 'none';
    }, 5000);
}
</script>
```

**优点**：无需后端、无需第三方服务、邮件直接发到律师邮箱
**缺点**：需要用户本地有邮件客户端配置

### 9. 页脚
- 四栏布局：关于我、服务领域、快速链接、联系方式
- 底部：版权信息

### 10. HTML动画展示片（新增）

用于创建律师形象宣传视频、服务介绍动画、社交媒体素材。

**技术特点**：
- CSS关键帧动画（淡入、缩放、旋转、滑动）
- JavaScript交互控制（播放/暂停、前进/后退、进度条）
- 键盘控制（空格、方向键）
- 自动播放模式

**标准6幕结构**：
1. **开场**（5-10秒）：品牌标识、主题动画
2. **专业资质**（10-15秒）：律师照片、简介
3. **服务领域**（15-20秒）：服务卡片展示
4. **团队优势**（10-15秒）：核心优势图标
5. **成功案例**（10-15秒）：数据可视化
6. **结尾**（10-15秒）：联系方式、CTA

**完整示例**：`/Users/yuzhenghong/Desktop/涉外律师形象展示片.html`

**导出MP4**：推荐 puppeteer-core + ffmpeg 自动化导出（逐帧截图→编码），详见 `references/html-animated-showcase.md` § 导出为MP4视频

## 技术规范

### HTML结构
```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>律师名 · 领域</title>
    <meta name="description" content="...">
    <meta name="keywords" content="...">
    <style>/* 内联CSS */</style>
</head>
<body>
    <nav><!-- 导航栏 --></nav>
    <section class="hero"><!-- 英雄区 --></section>
    <section class="services"><!-- 服务介绍 --></section>
    <section class="expertise"><!-- 专业领域 --></section>
    <section class="cases"><!-- 成功案例 --></section>
    <section class="blog"><!-- 法律科普 --></section>
    <section class="about"><!-- 律师简介 --></section>
    <section class="contact"><!-- 在线咨询 --></section>
    <footer><!-- 页脚 --></footer>
    <script>/* 交互逻辑 */</script>
</body>
</html>
```

### CSS变量
```css
:root {
    --primary: #1a365d;      /* 主色：深蓝 */
    --primary-light: #2d3748; /* 浅主色 */
    --accent: #e53e3e;        /* 强调色：红色 */
    --text: #333;             /* 正文色 */
    --text-light: #666;       /* 次要文字 */
    --bg: #f8f9fa;            /* 背景色 */
    --white: #fff;            /* 白色 */
}
```

### 响应式断点
```css
@media (max-width: 768px) {
    /* 移动端适配 */
}
```

## Git工作流

### 仓库命名规范
- GitHub：`wxlawyers/lawyer-{领域}`
- 示例：`wxlawyers/lawyer-foreign-legal`

### 提交规范
```
feat: 添加案例展示模块
fix: 修复移动端导航菜单
style: 优化页面配色
docs: 更新README
```

### 部署方式

**GitHub Pages（现有仓库）**：

```bash
# 1. 查找正确的仓库（不要假设 .git/config 中的地址）
curl -s "https://api.github.com/users/wxlawyers/repos?per_page=100" | grep '"name"'

# 2. 检查仓库结构
curl -s "https://api.github.com/repos/wxlawyers/REPO_NAME/contents" | grep '"name"'

# 3. 克隆仓库到临时目录
cd /tmp && git clone git@github.com:wxlawyers/REPO_NAME.git

# 4. 复制更新的文件到正确位置
cp ~/Documents/lawyer-website/index.html /tmp/REPO_NAME/website/index.html

# 5. 提交并推送
cd /tmp/REPO_NAME
git add website/index.html
git commit -m "feat: 网站更新"
git push origin master

# 6. 启用 GitHub Pages（手动）
# 访问 https://github.com/wxlawyers/REPO_NAME/settings/pages
# Branch: master, 文件夹: /website, 点 Save

# 7. 清理临时目录
rm -rf /tmp/REPO_NAME
```

**⚠️ 常见错误**：
- 远程仓库地址配置错误 → 用 API 验证仓库是否存在
- 推送到错误的目录 → 先检查仓库结构
- 忘记启用 Pages → 推送后必须手动启用

**GitHub Pages（新仓库）**：
```bash
# 1. 创建仓库
gh repo create wxlawyers/lawyer-foreign-legal --public

# 2. 推送代码
git push origin main

# 3. 启用Pages
# Settings → Pages → Source: main branch
```

**Gitee Pages**：
```bash
# 1. 创建仓库
# Gitee网页创建，或：
curl -X POST "https://gitee.com/api/v5/user/repos" \
  -H "Content-Type: application/json" \
  -d '{"name":"lawyer-foreign-legal","private":false}'

# 2. 推送代码
git remote add gitee git@gitee.com:wxlawyers/lawyer-foreign-legal.git
git push gitee main

# 3. 启用Pages
# 服务 → Gitee Pages → 部署
```

**⚠️ 部署前检查清单**：
- [ ] 确认远程仓库存在（用 API 验证）
- [ ] 确认仓库中有 `website/` 或 `docs/` 目录
- [ ] 确认SSH密钥已配置
- [ ] 确认GitHub/Gitee账号权限
- [ ] 测试本地预览效果
- [ ] 推送后启用 Pages

## SEO优化

### Meta标签
```html
<meta name="description" content="律师名，执业机构，专注领域，为XX提供专业法律服务">
<meta name="keywords" content="领域律师,地区律师,执业方向1,执业方向2">
```

### 结构化数据（可选）
```html
<script type="application/ld+json">
{
    "@context": "https://schema.org",
    "@type": "LegalService",
    "name": "余正洪律师",
    "address": {
        "@type": "PostalAddress",
        "addressLocality": "无锡",
        "addressRegion": "江苏"
    }
}
</script>
```

## 工作流程

### 新建网站
1. 确认领域和定位
2. 创建项目目录
3. 编写HTML/CSS
4. 初始化Git仓库
5. 推送到GitHub/Gitee
6. 启用Pages部署

### 更新现有网站

1. **确认是更新现有项目**（不是新建）
2. **克隆仓库到临时目录**：`cd /tmp && git clone git@github.com:wxlawyers/lawyer-knowledge-graph.git`
3. **复制本地文件到仓库**：`cp ~/Documents/lawyer-website/index.html /tmp/lawyer-knowledge-graph/docs/index.html`
4. **同步website和docs**：`cp /tmp/lawyer-knowledge-graph/docs/index.html /tmp/lawyer-knowledge-graph/website/index.html`
5. **提交并推送**：`git add -A && git commit -m "描述" && git push origin master`
6. **清理临时目录**：`rm -rf /tmp/lawyer-knowledge-graph`
7. **验证线上效果**：访问网站URL，强制刷新（Ctrl+F5）

**⚠️ 重要**：GitHub Pages从`/docs`目录部署，但仓库中也有`/website`目录作为备份。更新时必须同步两个目录。

### 撤销更新（恢复原始版本）
当用户要求"删除更新""恢复原样"时：

```bash
# 1. 查看提交历史
cd ~/Documents/lawyer-website && git log --oneline

# 2. 恢复到指定版本
git checkout <原始commit-hash> -- index.html

# 3. 提交恢复
git add -A && git commit -m "revert: 恢复原始版本"

# 4. 同步推送到仓库的 website 目录
cd /tmp && rm -rf REPO_NAME && git clone git@github.com:wxlawyers/REPO_NAME.git
cd REPO_NAME && cp ~/Documents/lawyer-website/index.html website/index.html
git add website/index.html && git commit -m "revert: 恢复原始版本" && git push origin master

# 5. 清理
rm -rf /tmp/REPO_NAME
```

## 法律工具网站（新增）

当用户要求创建法律工具类网站（如起诉状查询、赔偿计算器、法条速查等）时，参考 `references/legal-tool-website.md`。该指南包含工具网站设计规范、数据结构、四性验证要求、GitHub Pages部署流程。

## ⚠️ PITFALL: React SPA + Netlify Forms 集成（2026-06-10教训）

当网站是 React SPA（如 Vite + React）部署在 Netlify 时，表单提交需要特殊处理。

### 问题

React SPA 的表单由 JavaScript 动态渲染，Netlify 的构建时表单检测无法识别。即使 HTML 中有 `<form data-netlify="true">` 声明，React 渲染的表单也不会自动提交到 Netlify Forms。

### 正确做法：声明 + fetch POST

**第一步**：在 `index.html` 的 `<body>` 中添加隐藏的表单声明（Netlify 构建时检测用）：
```html
<form name="consultation" data-netlify="true" netlify-honeypot="bot-field" hidden>
    <input type="text" name="name" />
    <input type="tel" name="phone" />
    <input name="caseType" />
    <textarea name="description"></textarea>
</form>
```

**第二步**：在 React 表单提交时，用 `fetch` POST 到 `/`：
```javascript
const handleSubmit = async (e) => {
    e.preventDefault();
    const formData = new FormData();
    formData.append("form-name", "consultation");  // 必须匹配声明的 name
    formData.append("name", name);
    formData.append("phone", phone);
    formData.append("caseType", caseType);
    formData.append("description", description);
    
    await fetch("/", {
        method: "POST",
        body: formData
    });
    // 显示成功消息
};
```

**关键点**：
- `form-name` 隐藏字段必须与声明的 `name` 属性一致
- 提交到 `"/"`（相对路径），不是绝对 URL
- 使用 `FormData` 格式，不是 JSON
- Netlify Dashboard → Forms 可查看所有提交

### 常见错误

| 错误 | 后果 |
|------|------|
| 只在 HTML 声明，React 不提交 | 表单永远收不到数据 |
| 用 JSON 格式提交 | Netlify 不识别，返回 404 |
| `form-name` 与声明不匹配 | 数据提交到错误的表单 |
| 用 `weixin://` URI Scheme 代替 | PC端无效，数据丢失 |

## ⚠️ PITFALL: Netlify CLI 部署（源码丢失时的恢复方法）

当网站通过 `netlify deploy` 部署，本地找不到源码时，可以从 Netlify API 下载已部署的文件并修改。

### 恢复步骤

```bash
# 1. 查找站点 ID
netlify sites:list
# 输出: yulvshi - 1b37b0db-cdaa-4c0b-88ff-a54755e4caf2

# 2. 获取部署文件列表
netlify api listSiteFiles --data '{"site_id": "SITE_ID", "deploy_id": "DEPLOY_ID"}'

# 3. 下载所有文件
mkdir -p /tmp/site-fix && cd /tmp/site-fix
for path in $(netlify api listSiteFiles --data '...' | python3 -c "import sys,json; [print(f['path']) for f in json.load(sys.stdin)]"); do
    mkdir -p ".$(dirname $path)"
    curl -s "https://SITE.netlify.app$path" -o ".$path"
done

# 4. 修改文件（JS/CSS/HTML）

# 5. 重新部署
netlify link --id SITE_ID  # 关联站点
netlify deploy --prod --dir=.  # 部署当前目录
```

### 修改已部署的 minified JS

当只有 minified JS 可用时，用 Python regex 替换：

```python
import re

with open('assets/index-XXX.js', 'r') as f:
    js = f.read()

# 查找目标代码的上下文
matches = list(re.finditer(r'目标模式', js))
for m in matches:
    print(js[max(0,m.start()-100):m.end()+100])

# 替换
js = re.sub(r'旧模式', r'新模式', js)

with open('assets/index-XXX.js', 'w') as f:
    f.write(js)
```

**⚠️ 注意**：minified JS 中的变量名是压缩的（如 `J=()=>{...}`），替换时需要精确匹配。

## 参考资料

- `references/lawyer-website-structure.md` — 网站结构和模块详解
- `references/deployment-checklist.md` — 部署检查清单
- `references/foreign-lawyer-marketing.md` — 涉外律师获客渠道
- `references/foreign-lawyer-market-research.md` — 涉外法律服务市场调研（2026年6月）
- `references/html-animated-showcase.md` — HTML动画展示片创建指南（分镜、动画、交互控制）
- `references/tools-website-pattern.md` — 工具类子页面开发模式（要素式起诉状查询等工具类网站）
- `references/element-complaint-deployment.md` — 要素式起诉状网站部署记录（路径、技术实现、Pages配置）
- `references/multilingual-legal-website.md` — **律师网站多语言翻译参考**（英文/法语/阿拉伯语对照表）
- `references/form-handling-implementation.md` — **律师网站表单处理方案**（mailto:方式实现）
- `references/qr-code-generation.md` — **律师名片二维码生成**（macOS中文字体路径、标准布局、英文命名规范）
- `references/business-card-qr-code.md` — **商务名片二维码生成**（带形象照的完整Python脚本、圆形裁剪、多语言服务展示）

## ⚠️ PITFALL: 律师网站用词规范（2026-06-09教训）

用户纠正了网站中的用词：
- ❌ "心理学博弈技巧" → ✅ "谈判策略专家"
- ❌ "专家"（标题） → ✅ "顾问"（标题）

**规则**：律师网站用词要**专业、正式**，避免过于"技术化"或"学术化"的表述。用户对用词有明确偏好时，直接修改，不要争论。

## ⚠️ PITFALL: 律师英文命名规范（2026-06-09教训）

用户纠正了网站中的英文翻译："Yu Zhenghong Law Firm"是律师事务所名称，不是律师个人称呼。

| 写法 | 正确性 | 说明 |
|------|--------|------|
| Yu Zhenghong, Attorney at Law | ✅ 最标准 | 美国律师标准称呼 |
| Yu Zhenghong, Esq. | ✅ 正式 | 更正式的称呼 |
| Attorney Yu Zhenghong | ⚠️ 语法不太自然 | 不如上面两种标准 |
| Yu Zhenghong Law Firm | ❌ 不准确 | 指律所，不是个人 |

**规则**：律师个人网站用 "Yu Zhenghong, Attorney at Law"，律所网站用 "Yu Zhenghong Law Firm"。

## ⚠️ PITFALL: 照片显示裁切问题（2026-06-09教训）

用户多次反馈"照片只显示部分"或"照片没显示全"。

### 问题原因
- `object-fit: cover` 会裁切照片以填满容器
- 固定 `height: 500px` 可能裁掉照片底部

### 正确做法
```css
/* 关于律师区域 - 照片全部显示 */
.about-image img {
    width: 100%;
    height: auto;           /* 自适应高度，不要固定 */
    object-fit: contain;    /* 全部显示，不裁切 */
}

/* 英雄区 - 可以用cover裁切 */
.hero-image img {
    width: 100%;
    height: 550px;
    object-fit: cover;
    object-position: top;   /* 从顶部开始裁切 */
}
```

**用户偏好**：关于律师区域的照片要**全部显示**，不能裁切。英雄区照片可以适当裁切。

## ⚠️ PITFALL: 文字与照片比例协调（2026-06-09教训）

用户反馈"关于律师区域的文字与照片比例不协调"。

### 正确做法
- 关于律师区域布局比例：照片1/3，文字2/3（`grid-template-columns: 1fr 1.5fr`）
- 标题字体：`font-size: 2.8rem`（与英雄区协调）
- 正文字体：`font-size: 1.15rem`（比默认大）
- 特点文字：`font-size: 1.1rem`

### 按钮字体协调
英雄区按钮要与整体区域协调：
```css
.btn-primary, .btn-secondary {
    font-size: 1.1rem;      /* 不是0.9rem */
    padding: 20px 50px;     /* 不是16px 40px */
}
```

## ⚠️ PITFALL: GitHub Pages缓存问题（2026-06-09）

推送到GitHub后，浏览器可能显示旧版本。解决方法：
1. URL加版本号：`?v=20`、`?v=21`
2. 强制刷新：`Ctrl+F5`（Windows）或 `Cmd+Shift+R`（Mac）
3. 等待1-2分钟让GitHub Pages重新部署

## 服务领域扩展模式

当用户要求增加服务领域时，保持4列网格布局，自动换行：
```css
.services-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 30px;
}
```

每个服务卡片必须配英文翻译：
```html
<div class="service-card">
    <div class="service-icon">⚖️</div>
    <h3>跨境争议解决</h3>
    <p class="en-title">Cross-border Dispute Resolution</p>
    <p>国际商事仲裁、跨境诉讼...</p>
</div>
```

**当前涉外律师网站服务领域（8个，按用户指定顺序）**：

| 序号 | 中文 | 英文 | 法语 | 阿拉伯语 |
|------|------|------|------|----------|
| 1 | 企业出海 | Enterprise Going Global | Internationalisation des Entreprises | توسع الشركات عالمياً |
| 2 | 涉外合同纠纷 | Cross-border Contract Disputes | Litiges Contractuels Transfrontaliers | نزاعات العقود العابرة للحدود |
| 3 | 跨境投资与并购 | Cross-border Investment & M&A | Investissement Transfrontalier & Fusions-Acquisitions | الاستثمار العابر للحدود |
| 4 | 跨境争议解决 | Cross-border Dispute Resolution | Résolution des Litiges Transfrontaliers | حل النزاعات العابرة للحدود |
| 5 | 外企知产保护 | IP Protection for Foreign Enterprises | Protection de la Propriété Intellectuelle | حماية الملكية الفكرية |
| 6 | 外企合规咨询 | Compliance Consulting | Conseil en Conformité | استشارات الامتثال |
| 7 | 私人财富管理与家事法 | Private Wealth Management & Family Law | Gestion de Patrimoine & Droit de la Famille | إدارة الثروة الخاصة |
| 8 | 外企劳动争议 | Foreign Enterprise Labor Disputes | Litiges du Travail des Entreprises Étrangères | نزاعات العمل |

**⚠️ 用户偏好（2026-06-09确认）**：
1. "企业出海"放在第一位
2. "外企劳动争议"放在最后一位
3. 服务领域顺序可以随时调整，用sed或Python脚本修改HTML

## 用户偏好（必须遵守）

### 1. 不要嵌入视频
用户明确表示"视频不要嵌入"网站（2026-06-09）。英雄区使用照片背景即可，不要添加`<video>`标签。即使桌面上有形象展示视频，也不要自动嵌入到网站中。

### 2. 多语言翻译
用户要求有英文的地方下面翻译成法语和阿拉伯语（2026-06-09）。服务卡片必须配三种语言翻译，导航栏配英文。

### 3. "涉外法律服务顾问"必须一行显示
标题不要用`<br>`换行，保持在一行内。如果需要视觉分隔，用`<span>`改变颜色即可。用户把"专家"改成了"顾问"。

### 4. 配英文翻译
所有服务领域、板块标题都要配专业的英文翻译（见上方双语对照表）。英文用金色斜体显示。

### 5. 信任用户反馈
当用户说"能访问""已经部署好了""第一次就做好了"时，**相信用户的反馈**，不要坚持工具检查结果。工具可能有误（API超时、缓存、网络问题），但用户的实际体验是真实的。

**错误做法**：API返回404 → 坚持说Pages没启用 → 用户说能访问 → 还在辩解
**正确做法**：用户说能访问 → 相信 → 如果检查结果矛盾，先确认再判断

### 6. 犯错后直接承认，不要狡辩
犯了错不要说"我应该做到X"、"以后会注意"这种漂亮话。用户认为这是狡猾——用漂亮话掩盖错误。

**错误做法**：犯错 → 说一堆"我应该怎么做" → 用户觉得你在找借口
**正确做法**：犯错 → 承认错误 → 不辩解 → 用行动证明

### 7. 不确定时说"我不确定"
不要过度自信。有矛盾信息时先确认再判断。

### 8. 用词要专业正式
律师网站用词要专业、正式，避免过于"技术化"或"学术化"的表述。用户对用词有明确偏好时，直接修改，不要争论。
- ❌ "心理学博弈技巧" → ✅ "谈判策略专家"
- ❌ "专家"（标题） → ✅ "顾问"（标题）

## 法律工具网站（非营销型）

除了律师形象展示网站，还可以制作**法律工具网站**——为同行和当事人提供实用法律资源。

### 适用场景

- 要素式起诉状查询工具
- 赔偿计算器
- 法律法规速查
- 合同模板库
- 诉讼费用计算器

### 与营销网站的区别

| 对比项 | 营销网站 | 工具网站 |
|--------|---------|---------|
| 目的 | 品牌展示、获客 | 提供实用工具 |
| 内容 | 律师简介、案例 | 可交互的法律工具 |
| 用户 | 当事人 | 同行 + 当事人 |
| SEO价值 | 中 | 高（搜索流量大） |
| 转化路径 | 咨询表单 | 工具使用 → 信任建立 → 咨询 |

### 工具网站部署路径

工具类页面部署在 `/website/tools/` 子目录下，与主站分离：

```
docs/                    # GitHub Pages只支持/docs目录
├── index.html           # 主站（形象展示）
├── tools/
│   ├── element-complaint/   # 要素式起诉状查询
│   │   └── index.html
│   ├── calculator/          # 赔偿计算器
│   │   └── index.html
│   └── templates/           # 合同模板库
│       └── index.html
└── images/              # 图片资源
    ├── lawyer-photo.jpg
    └── qrcode.jpg
```

**访问地址**：`https://wxlawyers.github.io/lawyer-knowledge-graph/tools/{tool-name}/`

### 工具网站设计规范

1. **单文件HTML**：内联CSS+JS，不依赖外部CDN
2. **搜索/过滤**：实时关键词搜索 + 分类筛选按钮
3. **卡片布局**：信息密度适中，hover交互
4. **模态框**：点击查看详情弹出模态框
5. **底部声明**：标注"仅供参考，具体以各地法院要求为准"
6. **联系方式**：底部展示律师信息（自然导流）

### 已部署工具

| 工具 | 路径 | 案由数 | 说明 |
|------|------|--------|------|
| 要素式起诉状助手 | `tools/element-complaint/` | 67类 | 案由要素查询、证据清单、法律依据、FAQ（对标最高法法〔2025〕82号） |

> 部署详情见 `references/element-complaint-deployment.md`
> 官方67类案由清单见 `references/element-complaint-67-types.md`

**⚠️ PITFALL: 法律工具网站必须先查官方模板再建（2026-06-09教训）**

制作法律工具类网站前，必须先搜索是否有官方发布的最新版本：
1. 用 `mcp_yuandian_search_fagui` 搜索相关文件（如"示范文本"、"官方模板"）
2. 用浏览器搜索法院官网、司法部官网
3. 如有官方版本，以官方为准，标注来源
4. 如无官方版本，在网站显著位置标注"参考版本，以各地法院要求为准"

错误做法：直接根据一般知识编写要素 → 用户问"是不是最新的" → 发现官方已有67类而我们只有18类
正确做法：先搜索官方文件 → 发现法〔2025〕82号 → 以此为基础构建 → 标注来源

**⚠️ PITFALL: 子代理MCP批量验证容易超时**

当需要批量验证法条引用（如45条以上）时，子代理可能在600秒超时限制内无法完成。
- 策略1：分批验证（每批15-20条）
- 策略2：先验证最关键的10条，其余标记"待验证"
- 策略3：使用 execute_code 批量调用MCP工具（比delegate_task更快）

**⚠️ PITFALL: 批量法条核实必有错误（2026-06-09教训）**

当一次性让子代理生成大量法条引用时（如14个案由×3条法条=42条），错误率约**6%**（实测42条中2条错误）。典型错误类型：
1. **条文号张冠李戴**：如民法典第919条实际是委托合同，被错误引用为旅游合同
2. **条文号过时**：如农村土地承包法第26条（承包期限实际在第21条）

**对策**：每次批量新增案由后，必须立即运行法条核实流程，不能跳过。核实发现错误后立即修正并推送。

## ⚠️ PITFALL: 律师照片显示修复（2026-06-09教训）

当网站从 `/website` 迁移到 `/docs` 目录后，律师照片可能不显示。

### 问题原因
1. 照片在 `website/images/` 但 GitHub Pages 从 `docs/` 部署
2. HTML 中使用 `<div class="placeholder">余</div>` 而非 `<img>` 标签
3. CSS 中 `.about-image .placeholder` 样式与新的 `<img>` 标签冲突

### 修复步骤
```bash
# 1. 确保图片在 docs/images/ 目录
cp website/images/*.jpg docs/images/

# 2. 替换 placeholder 为 img 标签
sed -i '' 's|<div class="about-image">|<div class="about-image">\n<img src="images/photo.jpg" alt="律师照片" style="width:100%;height:100%;object-fit:cover;">|' docs/index.html
sed -i '' 's|<div class="placeholder">余</div>||' docs/index.html

# 3. 更新 CSS：删除 placeholder 样式，添加 about-image 尺寸
# 删除: .about-image .placeholder { ... }
# 添加到 .about-image:
#   width: 250px; height: 300px; overflow: hidden; border-radius: 10px; margin: 0 auto;
```

### 验证
```bash
# 检查图片是否可访问
curl -s -o /dev/null -w "%{http_code}" "https://USER.github.io/REPO/images/photo.jpg"
# 应返回 200
```

## ⚠️ PITFALL: 微信URI Scheme跳转不可靠（2026-06-09教训）

律师网站的"微信咨询"按钮不要使用 `weixin://dl/chat?{wxid}` URI Scheme。

### 问题分析

| 问题 | 说明 |
|------|------|
| PC端无法使用 | `weixin://` 协议只有手机装了微信才能处理，电脑浏览器静默失败 |
| wxid ≠ 微信号 | `weixin://dl/chat` 需要的是微信内部ID（wxid），不是微信号（如 wuxilawyers），格式不对会跳转失败 |
| 静默失败 | `window.location.href = "weixin://..."` 不会抛异常，无论成功失败都会执行后续代码 |
| 数据丢失 | 表单填写的姓名、电话等信息不会发送到任何后端，页面刷新后丢失 |

### 实测案例（lawyer-yu.netlify.app）

该网站的"微信咨询"按钮核心逻辑：
```javascript
// 提交表单后执行
window.location.href = "weixin://dl/chat?wuxilawyers";
// 然后无论是否成功，都显示"已打开微信"
```

**问题**：
1. PC端完全无法使用（静默失败）
2. 手机端可能因 wxid 格式错误而失败
3. 表单数据不发送到任何后端（无邮箱、无数据库）
4. 提交后显示"已打开微信"是误导性的

### 正确做法

**方案A（推荐）：二维码 + 提示文案**
```html
<div class="wechat-contact">
    <img src="images/wechat-qrcode.jpg" alt="微信二维码">
    <p>扫码添加微信，发送您的姓名和案情</p>
</div>
```

**方案B：Netlify Forms（Netlify部署时）**
```html
<form name="consultation" method="POST" data-netlify="true">
    <input type="hidden" name="form-name" value="consultation">
    <!-- 表单字段 -->
</form>
```
Netlify 原生支持表单提交，无需后端。提交后可在 Netlify Dashboard 查看。

**方案C：mailto: 链接**（见 `references/form-handling-implementation.md`）

### 分析生产环境React表单的技巧

当需要分析线上网站的表单逻辑时：

```javascript
// 1. 检查表单结构
const form = document.querySelector('form');
const inputs = form.querySelectorAll('input, textarea, select');

// 2. 查找 React 事件绑定
const fiberKey = Object.keys(form).find(k => k.startsWith('__reactFiber'));

// 3. 下载并搜索打包后的JS
// curl -s "URL/assets/index-XXX.js" | grep -i "submit\|wechat\|weixin"

// 4. 拦截 form submit 查看行为
form.addEventListener('submit', (e) => {
    console.log('action:', form.action, 'method:', form.method);
});

// 5. 检查 window.open / location.href 赋值
const origOpen = window.open;
window.open = (url) => { console.log('open:', url); return origOpen(url); };
```

## 安全要求

- 联系方式使用真实信息
- 案例必须脱敏处理
- 不要暴露当事人隐私
- 微信二维码使用公开咨询号

---

## 要素式起诉状网站模式（2026-06-08）

### 项目路径
- 本地：`~/Documents/element-complaint-website/index.html`
- 仓库：`wxlawyers/lawyer-knowledge-graph` → `docs/tools/element-complaint/`（注意：GitHub Pages只支持/docs目录）
- 线上：`https://wxlawyers.github.io/lawyer-knowledge-graph/tools/element-complaint/`

### 官方模板提取流程（2026-06-09）

当用户有官方Word模板（如《要素式民事起诉状答辩状示范文本》）时：

1. **先查看用户提供的官方文件**，不要自行生成
2. **提取表格结构**：用python-docx读取docx中的表格
3. **转换为HTML**：保持官方表格填写式格式
4. **添加到网站**：作为officialTemplate字段
5. **提供下载**：将原始docx文件放到网站目录

```python
from docx import Document
doc = Document('官方模板.docx')
# 找出案由位置和表格范围
# 用table_to_html()转换每个表格
# 添加到JavaScript数据中的officialTemplate字段
```

**用户明确纠正（2026-06-09）**：官方模板是表格填写式，不是叙述式。用户说"错的离谱"，必须先查看官方文件再制作。

**⚠️ PITFALL: 法律文书模板必须是表格填写式，不是叙述式**

用户有官方《要素式民事起诉状答辩状示范文本》Word文件（148个表格）。模板格式是：
- **表格填写式**：每个要素是一个表格行，左边标签右边填写框
- **勾选项**：用□表示可勾选项
- **不是**叙述式的"原告XXX诉被告XXX"
- 包含：说明→当事人信息→诉讼请求和依据→约定管辖→事实和理由→证据清单→具状人签名

提取流程：用python-docx读取docx表格 → 转换为HTML表格 → 添加到officialTemplate字段

**官方模板完整结构（民间借贷纠纷示例）**：
- Table 0: 说明 + 当事人信息（原告自然人/法人/委托代理人/送达地址）
- Table 1: 电子送达 + 被告信息 + 第三人信息 + 诉讼请求（本金）
- Table 2: 诉讼请求（利息、提前还款、担保、费用）+ 约定管辖 + 事实和理由（合同签订、主体、金额、期限、利率）
- Table 3: 还款方式、还款情况、逾期、担保合同、保证方式、证据清单、具状人签名

**官方docx包含11个案由**：民间借贷、离婚、买卖合同、金融借款、物业服务、银行信用卡、机动车交通事故、劳动争议、融资租赁、保证保险、证券虚假陈述。其他案由需自行创建符合官方格式的模板。

### 数据结构（每个案由）

```javascript
{
    name: "案由名称",
    cat: "分类（合同纠纷/劳动争议/侵权纠纷/婚姻家事/金融纠纷/知产纠纷/建设工程/公司股权/行政纠纷/执行/海事纠纷/刑事自诉/国家赔偿）",
    scene: "适用场景描述",
    elements: [["要素名称", "填写说明"], ...],
    evidence: ["关键证据1", "关键证据2", ...],
    law: ["法律依据1", "法律依据2", ...],
    tips: ["实务提示1", "实务提示2", ...],
    officialTemplate: `<!-- 官方表格填写式模板HTML -->`,  // 可选，11个案由有官方模板
    template: `<!-- 叙述式模板文本 -->`  // 可选，备用模板
}
```

### 官方模板（11个案由）

从用户提供的《要素式民事起诉状答辩状示范文本》Word文件中提取：

| 案由 | 模板类型 | 说明 |
|------|----------|------|
| 民间借贷纠纷 | 官方表格填写式 | 最完整的模板 |
| 离婚纠纷 | 官方表格填写式 | |
| 买卖合同纠纷 | 官方表格填写式 | |
| 金融借款合同纠纷 | 官方表格填写式 | |
| 物业服务合同纠纷 | 官方表格填写式 | |
| 银行信用卡纠纷 | 官方表格填写式 | |
| 机动车交通事故责任纠纷 | 官方表格填写式 | |
| 劳动争议纠纷 | 官方表格填写式 | |
| 融资租赁合同纠纷 | 官方表格填写式 | |
| 保证保险合同纠纷 | 官方表格填写式 | |
| 证券虚假陈述责任纠纷 | 官方表格填写式 | |

其他56个案由使用通用的官方格式模板（按案由类型自动生成）。

### 模板显示优先级

1. `officialTemplate`（优先）— 官方表格填写式模板
2. `template`（备用）— 叙述式模板
3. 无模板 — 只显示要素清单

### 网站功能模块

1. **使用指南**：3步流程卡片（选择案由→查看要素→准备材料）
2. **搜索过滤**：关键词实时搜索 + 分类筛选按钮
3. **案由卡片**：展开/收起要素清单 + 查看详细模板按钮
4. **模态框**：官方模板（如有）+ 要素表格 + 证据清单 + 法律依据 + 下载Word + 打印按钮
5. **FAQ**：手风琴展开式常见问题
6. **律师信息**：联系方式 + 地址

### GitHub Pages部署

```bash
cd /tmp && git clone git@github.com:wxlawyers/lawyer-knowledge-graph.git
cp ~/Documents/element-complaint-website/index.html /tmp/lawyer-knowledge-graph/docs/tools/element-complaint/index.html
cd /tmp/lawyer-knowledge-graph
git add docs/tools/element-complaint/index.html
git commit -m "feat: 描述"
git push origin master
rm -rf /tmp/lawyer-knowledge-graph
```

**⚠️ PITFALL：GitHub Pages只支持/docs目录（2026-06-09确认）**

GitHub Pages设置界面可能显示`/website`作为选项，但实际上**只部署`/docs`或根目录`/`**。如果选择`/website`，网站会404。始终使用`/docs`目录。

```bash
# 如果文件在website/，必须复制到docs/
cp -r website/* docs/
git add docs/
git commit -m "feat: deploy from /docs folder"
git push origin master
```

### 新增案由的工作流

```
1. 确定新增案由清单（对标官方67类）
2. delegate_task批量创建（每批15-20个）
3. MCP工具核实法条引用
4. 修正错误
5. 推送到GitHub
6. 验证线上效果
```

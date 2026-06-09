# 欧美律所风格网站设计模式

## 设计原则

1. **深色背景 + 金色点缀** — 专业、权威、高端
2. **衬线标题 + 无衬线正文** — 传统与现代结合
3. **左右布局** — 英雄区、关于律师区都用左右分栏
4. **留白多** — 不要信息密集，给内容呼吸空间
5. **双语对照** — 中文标题+英文副标题/翻译
6. **数据展示** — 用数字建立信任（年限、案件数、满意度）

## 标准配色方案

```css
:root {
    --navy: #0a1628;        /* 主背景色 */
    --dark-blue: #1a2a4a;   /* 次背景色 */
    --gold: #c9a96e;        /* 强调色 */
    --light-gold: #d4b87a;  /* 浅金色（hover） */
    --white: #ffffff;
    --light-gray: #f8f9fa;  /* 浅灰背景 */
    --text: #333333;
    --text-light: #666666;
}
```

## 字体选择

```html
<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;500;600;700&family=Inter:wght@300;400;500;600&display=swap" rel="stylesheet">
```

- **标题**：Playfair Display（衬线，优雅）
- **正文**：Inter（无衬线，现代）
- **Logo**：Playfair Display，letter-spacing: 2px

## 标准页面结构

```
导航栏（深蓝背景，固定顶部）
├── Logo: YU ZHENGHONG（金色）
└── 菜单：服务领域 | 关于律师 | 联系我们

英雄区（深蓝背景，左右布局）
├── 左侧：英文副标题 + 中文大标题 + 描述 + 按钮
└── 右侧：律师照片（带金色装饰边框）

统计数据（白色背景，悬浮效果）
├── 10+ 年执业经验
├── 500+ 代理案件
├── 98% 客户满意度
└── 100+ 服务客户

服务领域（浅灰背景，4卡片）
├── 外企劳动争议 / Foreign Enterprise Labor Disputes
├── 涉外合同纠纷 / Cross-border Contract Disputes
├── 外企知产保护 / IP Protection for Foreign Enterprises
└── 外企合规咨询 / Compliance Consulting

关于律师（白色背景，左右布局）
├── 左侧：律师照片（另一张，带金色装饰边框）
└── 右侧：姓名 + 简介 + 特色优势

联系我们（浅灰背景，双栏）
├── 左侧：联系方式 + 微信二维码
└── 右侧：在线预约表单

页脚（深蓝背景）
├── 品牌介绍
├── 快速链接
└── 服务领域列表
```

## 英雄区CSS（左右布局，非全屏背景）

```css
.hero {
    padding-top: 80px;
    min-height: 100vh;
    display: flex;
    align-items: center;
    background: var(--navy);
}

.hero-container {
    max-width: 1400px;
    margin: 0 auto;
    padding: 80px 60px;
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 80px;
    align-items: center;
}

.hero-image img {
    width: 100%;
    height: 550px;
    object-fit: cover;
    object-position: top;
}

.hero-image::after {
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

## 双语对照实现

```html
<div class="section-label">Practice Areas</div>
<h2 class="section-title">专业服务领域</h2>

<div class="service-card">
    <h3>外企劳动争议</h3>
    <p class="en-title">Foreign Enterprise Labor Disputes</p>
    <p>处理外资企业劳动纠纷...</p>
</div>
```

```css
.section-label {
    font-size: 0.8rem;
    font-weight: 500;
    color: var(--gold);
    letter-spacing: 4px;
    text-transform: uppercase;
}

.en-title {
    font-size: 0.8rem;
    color: var(--gold);
    margin-top: 5px;
    font-style: italic;
}
```

## 微信二维码集成

放在"联系我们"区域的左侧联系方式下方：

```html
<div class="wechat-section">
    <h4>📱 微信咨询</h4>
    <div class="qr-code">
        <img src="images/二维码.jpg" alt="微信二维码">
    </div>
    <p class="wechat-tip">扫码添加微信，获取专业法律咨询</p>
</div>
```

## 照片使用规范

- **英雄区**：半身职业照，放在右侧
- **关于律师**：另一张正式肖像照，放在左侧
- 两张照片**不能相同**，要有差异
- 照片尺寸：统一 550px 高度，object-fit: cover

## 响应式断点

```css
@media (max-width: 1024px) {
    .hero-container { grid-template-columns: 1fr; }
    .services-grid { grid-template-columns: repeat(2, 1fr); }
    .about-container { grid-template-columns: 1fr; }
}

@media (max-width: 768px) {
    .nav-links { display: none; }
    .hero h1 { font-size: 2.2rem; }
    .services-grid { grid-template-columns: 1fr; }
}
```

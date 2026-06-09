# 欧美律所风格网站模板参考

余律师要求涉外律师网站采用欧美律所风格。此文件记录完整的设计规范和代码模板。

## 设计原则

1. **全屏英雄区** - 律师照片作为背景，暗色半透明遮罩
2. **衬线字体** - Playfair Display（标题）+ Inter（正文）
3. **深蓝+金色配色** - 专业、高端、国际化
4. **英文元素** - Logo用英文名，板块用英文小标题
5. **数据化展示** - 执业年限、代理案件数、客户满意度
6. **留白设计** - 不拥挤，呼吸感强

## 完整配色方案

```css
:root {
    --navy: #0a1628;        /* 主背景色 */
    --dark-blue: #1a2a4a;   /* 次背景色 */
    --gold: #c9a96e;        /* 强调色 */
    --light-gold: #d4b87a;  /* hover状态 */
    --white: #ffffff;
    --light-gray: #f5f5f5;  /* 内容区背景 */
    --text: #333333;
    --text-light: #666666;
}
```

## 字体引入

```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;500;600;700&family=Inter:wght@300;400;500;600&display=swap" rel="stylesheet">
```

## 板块结构

| 板块 | 背景色 | 英文小标题 | 中文大标题 |
|------|--------|-----------|-----------|
| 导航栏 | rgba(10,22,40,0.95) | - | YU ZHENGHONG |
| 英雄区 | 律师照片+暗色遮罩 | International Legal Services | 涉外法律服务 专家 |
| 服务领域 | white | Practice Areas | 专业服务领域 |
| 关于律师 | navy | About The Lawyer | 关于律师 |
| 联系我们 | light-gray | Contact Us | 联系我们 |
| 页脚 | navy | - | YU ZHENGHONG |

## 卡片hover效果

```css
.service-card:hover {
    background: var(--white);
    border-color: var(--gold);
    transform: translateY(-10px);
    box-shadow: 0 20px 40px rgba(0,0,0,0.1);
}
```

## 关于律师板块特殊效果

```css
.about-image::after {
    content: '';
    position: absolute;
    bottom: -20px;
    right: -20px;
    width: 200px;
    height: 200px;
    border: 3px solid var(--gold);
    z-index: -1;
}
```

## 数据展示

```html
<div class="credentials">
    <div class="credential-item">
        <div class="number">10+</div>
        <div class="label">年执业经验</div>
    </div>
    <div class="credential-item">
        <div class="number">500+</div>
        <div class="label">代理案件</div>
    </div>
    <div class="credential-item">
        <div class="number">98%</div>
        <div class="label">客户满意度</div>
    </div>
</div>
```

## 完整模板文件

完整的欧美律所风格HTML模板已部署到：
- 仓库：`wxlawyers/lawyer-knowledge-graph`
- 路径：`website/index.html` 和 `docs/index.html`
- 线上：`https://wxlawyers.github.io/lawyer-knowledge-graph/`

# 律师网站结构详解

## 页面结构图

```
┌─────────────────────────────────────────┐
│  导航栏（固定顶部）                        │
│  Logo | 服务 | 领域 | 案例 | 科普 | 简介 | 咨询 │
├─────────────────────────────────────────┤
│  英雄区                                   │
│  主标题 + 副标题 + CTA按钮                 │
├─────────────────────────────────────────┤
│  服务介绍（4个卡片）                       │
│  [图标+标题+描述] × 4                     │
├─────────────────────────────────────────┤
│  专业领域（4个条目）                       │
│  [左侧边框+标题+描述] × 4                 │
├─────────────────────────────────────────┤
│  成功案例                                 │
│  [筛选按钮] [案例卡片] × 6                │
├─────────────────────────────────────────┤
│  法律科普                                 │
│  [文章卡片] × 6                           │
├─────────────────────────────────────────┤
│  律师简介                                 │
│  [照片] + [姓名+简介+数据]                 │
├─────────────────────────────────────────┤
│  在线咨询                                 │
│  [联系方式+微信] | [咨询表单]              │
├─────────────────────────────────────────┤
│  页脚                                     │
│  [关于] [服务] [链接] [联系]               │
└─────────────────────────────────────────┘
```

## 各模块详细说明

### 1. 导航栏

**结构**：
```html
<nav>
    <div class="nav-container">
        <a href="#" class="logo">律师名</a>
        <button class="menu-toggle" onclick="toggleMenu()">☰</button>
        <ul class="nav-links" id="navLinks">
            <li><a href="#services">服务介绍</a></li>
            <li><a href="#expertise">专业领域</a></li>
            <li><a href="#cases">成功案例</a></li>
            <li><a href="#blog">法律科普</a></li>
            <li><a href="#about">律师简介</a></li>
            <li><a href="#contact">在线咨询</a></li>
        </ul>
    </div>
</nav>
```

**样式要点**：
- 固定定位：`position: fixed; top: 0;`
- 白色背景 + 阴影
- 移动端：汉堡菜单，点击展开

### 2. 英雄区

**结构**：
```html
<section class="hero">
    <div class="container">
        <h1>涉外法律服务专家</h1>
        <p>专注外企劳动争议、涉外合同纠纷...</p>
        <a href="#contact" class="btn">免费咨询</a>
        <a href="#cases" class="btn btn-outline">查看案例</a>
    </div>
</section>
```

**样式要点**：
- 深色渐变背景：`linear-gradient(135deg, #1a365d 0%, #2d3748 100%)`
- 白色文字
- 按钮：红色实心 + 白色描边

### 3. 成功案例

**筛选功能**：
```javascript
function filterCases(category) {
    const cards = document.querySelectorAll('.case-card');
    const buttons = document.querySelectorAll('.filter-btn');
    
    // 更新按钮状态
    buttons.forEach(btn => btn.classList.remove('active'));
    event.target.classList.add('active');
    
    // 筛选卡片
    cards.forEach(card => {
        if (category === 'all' || card.dataset.category === category) {
            card.style.display = 'block';
        } else {
            card.style.display = 'none';
        }
    });
}
```

**案例卡片结构**：
```html
<div class="case-card" data-category="labor">
    <div class="case-header">
        <span class="case-type">劳动争议</span>
        <h3>某德企高管违法解雇赔偿案</h3>
    </div>
    <div class="case-body">
        <div class="case-result">
            <span class="icon">✅</span>
            <span class="text">胜诉，获赔45万元</span>
        </div>
        <p class="case-desc">案情简介...</p>
        <div class="case-tags">
            <span class="case-tag">违法解雇</span>
            <span class="case-tag">赔偿金</span>
        </div>
    </div>
</div>
```

### 4. 咨询表单

**表单字段**：
- 姓名（必填）
- 联系电话（必填）
- 邮箱（选填）
- 咨询类型（下拉选择）
- 问题描述（必填，textarea）

**提交处理**：
```javascript
function submitForm(e) {
    e.preventDefault();
    
    // 方案A：Formspree
    // fetch('https://formspree.io/f/YOUR_FORM_ID', {
    //     method: 'POST',
    //     body: formData
    // });
    
    // 方案B：EmailJS
    // emailjs.send('YOUR_SERVICE_ID', 'YOUR_TEMPLATE_ID', formData);
    
    // 临时方案：alert提示
    alert('感谢您的咨询！我们会尽快与您联系。');
    form.reset();
}
```

### 5. 微信二维码

**实现方式**：
```html
<div class="wechat-qr">
    <h4>微信扫码咨询</h4>
    <div class="qr-placeholder">
        <img src="qrcode.png" alt="微信二维码" style="width:150px;">
    </div>
    <p>扫码添加微信，一对一咨询</p>
</div>
```

**⚠️ 注意**：
- 使用公开咨询微信号，不用个人号
- 二维码图片放在项目根目录
- 图片大小控制在200KB以内

## 响应式断点

### 移动端（<768px）
- 导航栏：汉堡菜单
- 案例/文章卡片：单列布局
- 联系方式：单列布局
- 简介：照片和文字垂直排列

### 平板（768px-1024px）
- 案例/文章卡片：2列布局
- 服务卡片：2列布局

### 桌面（>1024px）
- 案例/文章卡片：3列布局
- 服务卡片：4列布局

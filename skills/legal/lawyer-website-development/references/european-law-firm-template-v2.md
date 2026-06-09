# 欧美律所风格网站模板 v2（2026-06-09）

## 完整HTML结构

基于余律师涉外法律服务网站最终版本，包含所有用户偏好。

### 关键设计决策

1. **英雄区**：左右布局（左文字+右照片），不是全屏背景
2. **关于律师**：左右布局（左照片+右文字），照片全部显示
3. **服务领域**：4列网格，8个服务，中英文对照
4. **微信二维码**：放在联系我们区域左侧
5. **在线预约表单**：放在联系我们区域右侧

### CSS变量

```css
:root {
    --navy: #0a1628;
    --dark-blue: #1a2a4a;
    --gold: #c9a96e;
    --light-gold: #d4b87a;
    --white: #ffffff;
    --light-gray: #f8f9fa;
    --text: #333333;
    --text-light: #666666;
}
```

### 字体

```css
/* 衬线标题 */
h1, h2, h3 { font-family: 'Playfair Display', serif; }

/* 无衬线正文 */
body, p { font-family: 'Inter', sans-serif; }
```

### 英雄区结构

```html
<section class="hero" id="hero">
    <div class="hero-container">
        <div class="hero-content">
            <div class="hero-subtitle">International Legal Services</div>
            <h1>涉外法律服务 <span>顾问</span></h1>
            <p>专注涉外法律服务...</p>
            <div class="hero-buttons">
                <a href="#contact" class="btn-primary">免费咨询</a>
                <a href="#services" class="btn-secondary">了解更多</a>
            </div>
        </div>
        <div class="hero-image">
            <img src="images/lawyer-photo-1.jpg" alt="律师照片">
        </div>
    </div>
</section>
```

### 关于律师区域

```html
<section class="about" id="about">
    <div class="section-header">
        <div class="section-label">About The Lawyer</div>
        <h2 class="section-title">关于律师</h2>
        <div class="section-line"></div>
    </div>
    <div class="about-container">
        <div class="about-image">
            <img src="images/lawyer-photo-2.jpg" alt="律师照片">
        </div>
        <div class="about-text">
            <h3>余正洪 <span>律师</span></h3>
            <p>简介文字...</p>
            <div class="about-features">
                <div class="feature-item">
                    <div class="feature-icon">✦</div>
                    <div class="feature-text">精通中英双语</div>
                </div>
                <!-- 更多特点 -->
            </div>
        </div>
    </div>
</section>
```

### 服务领域卡片

```html
<div class="service-card">
    <div class="service-icon">⚖️</div>
    <h3>跨境争议解决</h3>
    <p class="en-title">Cross-border Dispute Resolution</p>
    <p>国际商事仲裁、跨境诉讼...</p>
</div>
```

### 联系我们区域

```html
<section class="contact" id="contact">
    <div class="contact-container">
        <div class="contact-info">
            <h3>联系方式</h3>
            <!-- 电话、邮箱、地址、执业机构 -->
            
            <!-- 微信二维码 -->
            <div class="wechat-section">
                <h4>📱 微信咨询</h4>
                <div class="qr-code">
                    <img src="images/二维码.jpg" alt="微信二维码">
                </div>
                <p class="wechat-tip">扫码添加微信，获取专业法律咨询</p>
            </div>
        </div>
        <div class="contact-form">
            <h3>在线预约咨询</h3>
            <form>
                <!-- 表单字段 -->
            </form>
        </div>
    </div>
</section>
```

## 图片文件清单

| 文件名 | 用途 | 位置 |
|--------|------|------|
| `lawyer-photo-1.jpg` | 英雄区右侧照片 | `images/` |
| `lawyer-photo-2.jpg` | 关于律师区域左侧照片 | `images/` |
| `二维码.jpg` | 微信二维码 | `images/` |

## 常见修改命令

```bash
# 修改标题
sed -i '' 's|旧标题|新标题|' website/index.html docs/index.html

# 修改字体大小
sed -i '' 's|font-size: 0.9rem;|font-size: 1.1rem;|' website/index.html docs/index.html

# 添加服务领域（在最后一个service-card后添加）
# 需要手动编辑，sed对多行替换不友好

# 推送到GitHub
cd /tmp && rm -rf lawyer-knowledge-graph && git clone git@github.com:wxlawyers/lawyer-knowledge-graph.git
cp ~/Documents/lawyer-website/index.html /tmp/lawyer-knowledge-graph/docs/index.html
cd /tmp/lawyer-knowledge-graph && git add -A && git commit -m "描述" && git push origin master
```

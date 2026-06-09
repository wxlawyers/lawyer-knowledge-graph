# 律师网站表单处理方案

## ⚠️ 不要用的方案：微信URI Scheme

`weixin://dl/chat?{wxid}` 方案**不可靠**：
- PC端完全无法使用（静默失败）
- `wxid` ≠ 微信号，格式不对会跳转失败
- 表单数据不会发送到任何后端
- 详见 SKILL.md § 微信URI Scheme跳转不可靠

## 方案对比

| 方案 | 优点 | 缺点 | 推荐度 |
|------|------|------|--------|
| **Netlify Forms** | **零配置、原生支持** | **仅Netlify部署** | **⭐⭐⭐⭐⭐** |
| **Netlify Forms + React** | **SPA集成、原生支持** | **需要fetch POST** | **⭐⭐⭐⭐⭐** |
| **mailto:** | **纯前端、无需后端** | **需要用户有邮件客户端** | **⭐⭐⭐⭐** |
| Formspree | 免费、无需后端 | 需要注册、有提交限制 | ⭐⭐⭐ |
| EmailJS | 免费、直接发邮件 | 需要配置、有发送限制 | ⭐⭐⭐ |
| 后端API | 完全可控 | 需要服务器、维护成本 | ⭐⭐ |
| ~~weixin:// URI~~ | ~~跳转微信~~ | **PC端无效、数据丢失** | ❌ |

## 推荐方案一：Netlify Forms（静态HTML网站）

如果网站部署在 Netlify（如 `lawyer-yu.netlify.app`），使用原生表单支持是最简方案：

```html
<form name="consultation" method="POST" data-netlify="true" netlify-honeypot="bot-field">
    <input type="hidden" name="form-name" value="consultation">
    <p style="display:none"><label>Don't fill this: <input name="bot-field"></label></p>
    
    <input type="text" name="name" placeholder="姓名" required>
    <input type="tel" name="phone" placeholder="电话" required>
    <select name="caseType">
        <option value="">请选择案件类型</option>
        <option>合同纠纷</option>
        <option>公司股权</option>
        <option>劳动争议</option>
    </select>
    <textarea name="description" placeholder="请描述您的法律问题" required></textarea>
    <button type="submit">提交咨询</button>
</form>
```

**优势**：
- 零后端配置，Netlify 自动处理表单提交
- 可在 Netlify Dashboard → Forms 查看所有提交
- 支持邮件通知（Settings → Forms → Form notifications）
- 支持 Slack/Webhook 集成
- 内置垃圾邮件过滤（honeypot field）

**注意**：需要 `data-netlify="true"` 属性和隐藏的 `form-name` 字段。

## 推荐方案一B：Netlify Forms + React SPA

当网站是 React/Vite SPA 时，Netlify 的构建时表单检测无法识别动态渲染的表单。需要两步配合：

### 第一步：HTML 声明（构建时检测）

在 `index.html` 的 `<body>` 中添加隐藏的表单声明：

```html
<body>
    <div id="root"></div>
    
    <!-- Netlify Forms Declaration - 构建时检测用 -->
    <form name="consultation" data-netlify="true" netlify-honeypot="bot-field" hidden>
        <input type="text" name="name" />
        <input type="tel" name="phone" />
        <input name="caseType" />
        <textarea name="description"></textarea>
    </form>
</body>
```

### 第二步：React 组件提交（运行时）

```jsx
const ContactForm = () => {
    const [formData, setFormData] = useState({
        name: '', phone: '', caseType: '', description: ''
    });
    const [submitted, setSubmitted] = useState(false);
    const [submitting, setSubmitting] = useState(false);

    const handleSubmit = async (e) => {
        e.preventDefault();
        setSubmitting(true);
        
        try {
            const body = new FormData();
            body.append("form-name", "consultation");  // 必须匹配声明的 name
            body.append("name", formData.name);
            body.append("phone", formData.phone);
            body.append("caseType", formData.caseType);
            body.append("description", formData.description);
            
            await fetch("/", {
                method: "POST",
                body: body
            });
            
            setSubmitted(true);
        } catch (err) {
            alert("提交失败，请直接拨打 132-7625-9126");
        } finally {
            setSubmitting(false);
        }
    };

    if (submitted) {
        return (
            <div className="success-message">
                <h3>✅ 提交成功</h3>
                <p>我们将在24小时内与您联系。</p>
                <button onClick={() => setSubmitted(false)}>返回</button>
            </div>
        );
    }

    return (
        <form onSubmit={handleSubmit}>
            {/* 表单字段 */}
            <button type="submit" disabled={submitting}>
                {submitting ? "提交中..." : "微信咨询"}
            </button>
        </form>
    );
};
```

### 关键点

| 要点 | 说明 |
|------|------|
| `form-name` 隐藏字段 | 必须与 HTML 声明的 `name` 属性完全一致 |
| 提交到 `"/"` | 相对路径，不是绝对 URL |
| `FormData` 格式 | 不能用 JSON，Netlify 不识别 |
| HTML 声明加 `hidden` | 避免显示空白表单 |

### 常见错误

| 错误 | 后果 |
|------|------|
| 只在 HTML 声明，React 不提交 | 表单永远收不到数据 |
| 用 JSON 格式提交 | Netlify 不识别，返回 404 |
| `form-name` 与声明不匹配 | 数据提交到错误的表单 |
| 用 `weixin://` URI Scheme 代替 | PC端无效，数据丢失 |

## 推荐方案二：mailto: 链接

### 原理

点击提交按钮后，JavaScript构建mailto:链接，打开用户本地邮件客户端，预填收件人、主题、正文。

### 完整实现

```html
<form id="consultationForm" onsubmit="handleSubmit(event)">
    <div class="form-row">
        <div class="form-group">
            <label>姓名 *</label>
            <input type="text" name="name" placeholder="请输入您的姓名" required>
        </div>
        <div class="form-group">
            <label>电话 *</label>
            <input type="tel" name="phone" placeholder="请输入您的电话" required>
        </div>
    </div>
    <div class="form-group">
        <label>邮箱</label>
        <input type="email" name="email" placeholder="请输入您的邮箱">
    </div>
    <div class="form-group">
        <label>咨询类型</label>
        <select name="type">
            <option>请选择咨询类型</option>
            <option>合同纠纷</option>
            <option>公司股权</option>
            <option>劳动争议</option>
            <option>知识产权</option>
            <option>房地产纠纷</option>
            <option>债权债务</option>
            <option>其他</option>
        </select>
    </div>
    <div class="form-group">
        <label>咨询内容 *</label>
        <textarea name="message" placeholder="请描述您的法律问题" required></textarea>
    </div>
    <button type="submit" class="btn-submit">提交预约</button>
    <div id="formSuccess" style="display:none;margin-top:20px;padding:15px;background:#d4edda;color:#155724;border:1px solid #c3e6cb;text-align:center;">
        ✅ 预约已提交成功！我们将尽快与您联系。
    </div>
</form>

<script>
function handleSubmit(e) {
    e.preventDefault();
    const form = document.getElementById('consultationForm');
    const formData = new FormData(form);
    
    const name = formData.get('name');
    const phone = formData.get('phone');
    const email = formData.get('email') || '未提供';
    const type = formData.get('type');
    const message = formData.get('message');
    
    const subject = encodeURIComponent('法律咨询预约 - ' + name);
    const body = encodeURIComponent(
        '姓名: ' + name + '\n' +
        '电话: ' + phone + '\n' +
        '邮箱: ' + email + '\n' +
        '咨询类型: ' + type + '\n' +
        '咨询内容:\n' + message
    );
    
    window.open('mailto:yuzhenghonglawyer@163.com?subject=' + subject + '&body=' + body);
    
    document.getElementById('formSuccess').style.display = 'block';
    form.reset();
    setTimeout(function() {
        document.getElementById('formSuccess').style.display = 'none';
    }, 5000);
}
</script>
```

## 其他方案参考

### Formspree 实现

```html
<form action="https://formspree.io/f/YOUR_FORM_ID" method="POST">
    <input type="text" name="name" required>
    <input type="email" name="email" required>
    <textarea name="message" required></textarea>
    <button type="submit">提交</button>
</form>
```

### EmailJS 实现

```html
<script src="https://cdn.jsdelivr.net/npm/@emailjs/browser@3/dist/email.min.js"></script>
<script>
emailjs.init("YOUR_PUBLIC_KEY");
function handleSubmit(e) {
    e.preventDefault();
    emailjs.sendForm('YOUR_SERVICE_ID', 'YOUR_TEMPLATE_ID', e.target)
        .then(() => alert('提交成功！'));
}
</script>
```

## 收件人邮箱

`yuzhenghonglawyer@163.com`（余律师的邮箱）

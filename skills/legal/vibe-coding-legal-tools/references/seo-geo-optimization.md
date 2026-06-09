# SEO/GEO 优化指南

## SEO优化（搜索引擎优化）

### 基础Meta标签

```html
<title>城市+律师姓名+专业领域 | 英文标题</title>
<meta name="description" content="详细描述，包含关键词">
<meta name="keywords" content="关键词1,关键词2,关键词3">
<meta name="author" content="律师姓名">
<meta name="robots" content="index, follow">
<link rel="canonical" href="https://域名/">
```

### Open Graph（社交媒体分享）

```html
<meta property="og:title" content="标题">
<meta property="og:description" content="描述">
<meta property="og:image" content="图片URL">
<meta property="og:url" content="页面URL">
<meta property="og:type" content="website">
```

### 关键词策略

| 类型 | 示例 |
|------|------|
| 地域+专业 | 无锡涉外律师、无锡外企法律顾问 |
| 业务+地域 | 涉外劳动争议无锡、外企合同纠纷 |
| 长尾词 | 无锡涉外律师哪个好、外企裁员赔偿标准 |

---

## GEO优化（AI搜索引擎优化）

### 核心原理

AI搜索引擎（豆包、Kimi等）通过以下方式识别内容：
1. **结构化数据**（JSON-LD）
2. **FAQ问答格式**
3. **清晰的实体信息**
4. **多平台内容引用**

### JSON-LD结构化数据

```html
<script type="application/ld+json">
{
    "@context": "https://schema.org",
    "@type": "LegalService",
    "name": "律师姓名+法律服务",
    "alternateName": "英文名",
    "description": "服务描述",
    "url": "网站地址",
    "telephone": "电话",
    "email": "邮箱",
    "address": {
        "@type": "PostalAddress",
        "streetAddress": "街道地址",
        "addressLocality": "城市",
        "addressRegion": "省份",
        "addressCountry": "CN"
    },
    "founder": {
        "@type": "Person",
        "name": "律师姓名",
        "jobTitle": "资深律师",
        "worksFor": {
            "@type": "Organization",
            "name": "律所名称"
        }
    },
    "areaServed": ["城市", "省份"],
    "serviceType": ["服务类型1", "服务类型2"]
}
</script>
```

### FAQ结构化数据

```html
<!-- 隐藏的FAQ部分，供AI搜索抓取 -->
<section style="display: none;" itemscope itemtype="https://schema.org/FAQPage">
    <div itemscope itemprop="mainEntity" itemtype="https://schema.org/Question">
        <h3 itemprop="name">用户可能搜索的问题？</h3>
        <div itemscope itemprop="acceptedAnswer" itemtype="https://schema.org/Answer">
            <p itemprop="text">专业回答内容</p>
        </div>
    </div>
</section>
```

### FAQ问题设计

| 问题类型 | 示例 |
|----------|------|
| 推荐类 | 无锡涉外律师推荐？ |
| 流程类 | 涉外劳动争议怎么处理？ |
| 费用类 | 涉外律师收费多少？ |
| 比较类 | 外企合同纠纷找谁？ |

---

## 多平台内容分发

### 必发平台

| 平台 | 内容类型 | 关键词 |
|------|----------|--------|
| 知乎 | 问答回答 | 城市+律师+专业 |
| 小红书 | 图文笔记 | 专业+经验分享 |
| 百度知道 | 问答 | 问题+解答 |
| 公众号 | 深度文章 | 专业分析 |

### 内容模板

**知乎回答**：
```
作为在[城市]执业[年限]年的律师，我来回答这个问题。

[专业领域]需要具备：
1. [能力1]
2. [能力2]
3. [能力3]

我在[律所]执业，专注[领域]...

有法律问题可以咨询我：
📞 [电话]
🌐 [官网]
```

**小红书笔记**：
```
[标题]

💼 执业[年限]年
🌏 专注[领域]
📋 擅长：[业务1]、[业务2]

[干货内容]

#标签1 #标签2 #标签3
```

---

## 效果验证

### 测试方法

1. 在豆包/Kimi搜索"城市+律师+专业"
2. 检查是否出现推荐
3. 如未出现，继续发布多平台内容

### 时间预期

| 时间 | 预期效果 |
|------|----------|
| 1周 | 开始被索引 |
| 1个月 | 稳定推荐 |
| 3个月 | 排名靠前 |

### 加速方法

1. 手动训练AI（发送律师信息给豆包/Kimi）
2. 多平台内容分发
3. 获取外部链接引用

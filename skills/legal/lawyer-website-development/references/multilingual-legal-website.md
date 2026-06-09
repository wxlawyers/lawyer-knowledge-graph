# 律师网站多语言翻译参考

## 翻译原则

1. **英文**：金色（#c9a96e），斜体，0.8rem
2. **法语**：灰色（#666），斜体，0.75rem
3. **阿拉伯语**：灰色（#666），斜体，0.75rem，direction: rtl（从右到左）

## 核心术语对照

### 网站模块标题

| 中文 | 英文 | 法语 | 阿拉伯语 |
|------|------|------|----------|
| 涉外法律服务顾问 | International Legal Services | Services Juridiques Internationaux | الخدمات القانونية الدولية |
| 专业服务领域 | Practice Areas | Domaines de Pratique | مجالات الممارسة المهنية |
| 关于律师 | About The Lawyer | À Propos de l'Avocat | عن المحامي |
| 联系我们 | Contact Us | Contactez-nous | اتصل بنا |
| 免费咨询 | Free Consultation | Consultation Gratuite | استشارة مجانية |
| 了解更多 | Learn More | En Savoir Plus | اعرف المزيد |
| 在线预约咨询 | Online Consultation | Consultation en Ligne | استشارة عبر الإنترنت |

### 服务领域

| 中文 | 英文 | 法语 | 阿拉伯语 |
|------|------|------|----------|
| 企业出海 | Enterprise Going Global | Internationalisation des Entreprises | توسع الشركات عالمياً |
| 涉外合同纠纷 | Cross-border Contract Disputes | Litiges Contractuels Transfrontaliers | نزاعات العقود العابرة للحدود |
| 跨境投资与并购 | Cross-border Investment & M&A | Investissement Transfrontalier & Fusions-Acquisitions | الاستثمار العابر للحدود والاندماج والاستحواذ |
| 跨境争议解决 | Cross-border Dispute Resolution | Résolution des Litiges Transfrontaliers | حل النزاعات العابرة للحدود |
| 外企知产保护 | IP Protection for Foreign Enterprises | Protection de la Propriété Intellectuelle | حماية الملكية الفكرية |
| 外企合规咨询 | Compliance Consulting | Conseil en Conformité | استشارات الامتثال |
| 私人财富管理与家事法 | Private Wealth Management & Family Law | Gestion de Patrimoine & Droit de la Famille | إدارة الثروة الخاصة وقانون الأسرة |
| 外企劳动争议 | Foreign Enterprise Labor Disputes | Litiges du Travail des Entreprises Étrangères | نزاعات العمل |

### 联系方式

| 中文 | 英文 | 法语 | 阿拉伯语 |
|------|------|------|----------|
| 电话咨询 | Phone Consultation | Consultation Téléphonique | استشارة هاتفية |
| 邮箱咨询 | Email Consultation | Consultation par Email | استشارة عبر البريد الإلكتروني |
| 办公地址 | Office Address | Adresse du Bureau | عنوان المكتب |
| 执业机构 | Law Firm | Cabinet d'Avocat | مكتب المحاماة |
| 微信咨询 | WeChat Consultation | Consultation WeChat | استشارة عبر ويشات |

### 导航栏

| 中文 | 英文 |
|------|------|
| 服务领域 | Services |
| 关于律师 | About |
| 联系我们 | Contact |

## CSS样式

```css
/* 英文标题 */
.en-title {
    font-size: 0.8rem;
    color: var(--gold);
    margin-top: 5px;
    font-style: italic;
}

/* 法语标题 */
.fr-title {
    font-size: 0.75rem;
    color: var(--text-light);
    margin-top: 3px;
    font-style: italic;
}

/* 阿拉伯语标题 */
.ar-title {
    font-size: 0.75rem;
    color: var(--text-light);
    margin-top: 3px;
    direction: rtl;  /* 从右到左 */
    font-style: italic;
}
```

## HTML结构

```html
<div class="service-card">
    <div class="service-icon">⚖️</div>
    <h3>跨境争议解决</h3>
    <p class="en-title">Cross-border Dispute Resolution</p>
    <p class="fr-title">Résolution des Litiges Transfrontaliers</p>
    <p class="ar-title">حل النزاعات العابرة للحدود</p>
    <p>国际商事仲裁、跨境诉讼、调解谈判...</p>
</div>
```

## 注意事项

1. **阿拉伯语必须设置 direction: rtl**，否则文字方向会错乱
2. **法语和阿拉伯语字号比英文小**（0.75rem vs 0.8rem），避免信息过载
3. **导航栏只配英文**，不需要法语和阿拉伯语（太长会溢出）
4. **服务卡片必须配三种语言**，这是用户的明确要求

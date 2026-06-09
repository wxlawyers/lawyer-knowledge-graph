# 推广素材生成指南

## 二维码推广图片

### 技术规格

| 项目 | 规格 |
|------|------|
| 尺寸 | 1080×1920 像素 |
| 格式 | PNG |
| 配色 | 深蓝(#1a2332) + 金色(#c9a96e) + 白色 |
| 元素 | 头像、二维码、联系方式、业务介绍 |

### 生成脚本

```python
from PIL import Image, ImageDraw, ImageFont
import qrcode
import requests
from io import BytesIO

# 创建画布
img = Image.new('RGB', (1080, 1920), '#1a2332')
draw = ImageDraw.Draw(img)

# 加载字体（macOS用STHeiti）
font_title = ImageFont.truetype('/System/Library/Fonts/STHeiti Medium.ttc', 72)
font_subtitle = ImageFont.truetype('/System/Library/Fonts/STHeiti Medium.ttc', 48)

# 绘制装饰线
draw.rectangle([100, 1150, 980, 1152], fill='#c9a96e')

# 添加文字
draw.text((540, 1200), '律师姓名', fill='#ffffff', font=font_title, anchor='mm')

# 生成二维码
qr = qrcode.QRCode(version=1, box_size=10, border=2)
qr.add_data('网站地址')
qr.make(fit=True)
qr_img = qr.make_image(fill_color='#c9a96e', back_color='#1a2332')
qr_img = qr_img.resize((400, 400))
img.paste(qr_img, (340, 1400))

# 保存
img.save('qrcode_promotion.png')
```

---

## 小红书文字卡片

### 技术规格

| 项目 | 规格 |
|------|------|
| 尺寸 | 1080×1080 像素（正方形） |
| 格式 | PNG |
| 配色 | 深蓝背景 + 金色装饰 + 白色文字 |
| 内容 | 干货型、可收藏 |

### 内容类型

| 类型 | 示例标题 |
|------|----------|
| 流程类 | 涉外合同纠纷处理流程 |
| 清单类 | 外企裁员赔偿计算清单 |
| 攻略类 | 外企劳动仲裁攻略 |
| 知识类 | 涉外法律常见问题 |

### 生成脚本

```python
from PIL import Image, ImageDraw, ImageFont

def create_text_card(title, steps, filename):
    """生成小红书文字卡片"""
    img = Image.new('RGB', (1080, 1080), '#1a2332')
    draw = ImageDraw.Draw(img)
    
    # 加载字体
    font_title = ImageFont.truetype('/System/Library/Fonts/STHeiti Medium.ttc', 56)
    font_step = ImageFont.truetype('/System/Library/Fonts/STHeiti Medium.ttc', 40)
    font_desc = ImageFont.truetype('/System/Library/Fonts/STHeiti Medium.ttc', 32)
    
    # 标题区
    draw.rectangle([0, 0, 1080, 200], fill='#2a3a4e')
    draw.text((540, 100), title, fill='#ffffff', font=font_title, anchor='mm')
    
    # 步骤区
    y = 250
    for i, (step, desc) in enumerate(steps, 1):
        # 数字圆形
        draw.ellipse([60, y+5, 120, y+65], fill='#c9a96e')
        draw.text((90, y+35), str(i), fill='#1a2332', font=font_desc, anchor='mm')
        
        # 步骤标题
        draw.text((150, y+10), step, fill='#ffffff', font=font_step)
        
        # 步骤描述
        draw.text((150, y+60), desc, fill='#a0b0c0', font=font_desc)
        
        # 分隔线
        draw.line([(150, y+110), (980, y+110)], fill='#3a4a5e', width=1)
        y += 140
    
    # 底部信息
    draw.rectangle([0, 900, 1080, 1080], fill='#2a3a4e')
    draw.text((540, 950), '余正洪律师 | 执业15年', fill='#c9a96e', font=font_desc, anchor='mm')
    draw.text((540, 1000), '专注涉外法律服务', fill='#ffffff', font=font_desc, anchor='mm')
    
    img.save(filename)
    return f'✅ 已保存到 {filename}'

# 使用示例
steps = [
    ('合同审查', '确定适用法律、争议解决方式'),
    ('证据收集', '整理往来邮件、付款记录'),
    ('协商调解', '优先通过协商解决'),
    ('仲裁/诉讼', '根据合同约定选择程序'),
    ('执行', '申请强制执行'),
]
create_text_card('涉外合同纠纷处理流程', steps, '涉外合同纠纷处理流程.png')
```

---

## 朋友圈文案模板

### 风格要求

1. **不带广告性质**：分享专业见解，不是广告
2. **国际化视角**：体现专业能力和国际视野
3. **配图专业**：工作照、法律文书、会议照

### 文案模板

**专业见解类**：
```
今天处理了一个涉外劳动争议案件...

外企裁员时，很多员工不知道自己的权益。

作为律师，我的建议是：
1. 先了解中国劳动法的规定
2. 不要轻易签署任何文件
3. 咨询专业律师

#涉外法律 #外企裁员 #劳动法
```

**案件分享类**：
```
今天帮客户处理了一个涉外合同纠纷...

关键点：
1. 确定适用法律
2. 收集证据
3. 选择合适的争议解决方式

有法律问题可以咨询我。

#涉外律师 #合同纠纷 #法律咨询
```

---

## 抖音口播文案

### 风格要求

1. **对话感**：像和朋友聊天
2. **通俗化**：不用法条原文
3. **有节奏**：10秒一个节奏点

### 文案模板

**问答回复类**：
```
无锡涉外律师推荐？（3秒）

在无锡找涉外律师，首先要看有没有处理过涉外案件的经验...

我处理过很多涉外劳动争议、合同纠纷...

有法律问题可以咨询我。

#无锡律师 #涉外律师 #外企裁员
```

**知识分享类**：
```
涉外合同纠纷怎么处理？（3秒）

首先确定适用什么法律...

然后看合同约定的争议解决方式...

最后收集证据...

有法律问题可以咨询我。

#涉外合同 #法律知识 #律师
```

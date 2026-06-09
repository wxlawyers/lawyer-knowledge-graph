# 商务名片二维码生成

> 用途：生成带律师形象照的专业商务二维码，用于朋友圈交换名片

## 标准设计规范

### 布局结构（从上到下）

| 区域 | 内容 | 样式 |
|------|------|------|
| 顶部装饰线 | 金色线条 | 5px高 |
| 形象照 | 圆形裁剪，200px | 居中 |
| 律师姓名 | 中文+英文 | 金色衬线字体 |
| 英文副标题 | Yu Zhenghong, Attorney at Law | 白色无衬线 |
| 金色分隔线 | 装饰 | 60px宽 |
| 二维码 | 白色背景框，380px | 居中 |
| 服务领域 | 4个核心服务 | 白色小字 |
| 底部联系方式 | 电话+邮箱+地址 | 深蓝背景 |
| 底部装饰线 | 金色线条 | 5px高 |

### 配色方案

```python
--navy: '#0a1628'      # 深海军蓝背景
--gold: '#c9a96e'      # 金色装饰
--white: '#ffffff'      # 白色文字
--light-gray: '#cccccc' # 浅灰文字
```

### 字体选择（macOS）

```python
# 可用中文字体
title_font = ImageFont.truetype("/System/Library/Fonts/STHeiti Medium.ttc", 40)
subtitle_font = ImageFont.truetype("/System/Library/Fonts/STHeiti Medium.ttc", 22)
small_font = ImageFont.truetype("/System/Library/Fonts/STHeiti Medium.ttc", 18)
en_font = ImageFont.truetype("/System/Library/Fonts/STHeiti Light.ttc", 20)
```

**⚠️ PITFALL: PingFang字体不可用**

macOS上 `/System/Library/Fonts/PingFang.ttc` 可能不存在。使用 `STHeiti Medium.ttc` 或 `STHeiti Light.ttc` 作为替代。

### 圆形照片裁剪

```python
from PIL import Image, ImageDraw

photo_size = 200
photo = photo.resize((photo_size, photo_size))

# 创建圆形蒙版
mask = Image.new('L', (photo_size, photo_size), 0)
mask_draw = ImageDraw.Draw(mask)
mask_draw.ellipse([0, 0, photo_size, photo_size], fill=255)

# 应用蒙版
photo_circle = Image.new('RGBA', (photo_size, photo_size), (0, 0, 0, 0))
photo_circle.paste(photo, (0, 0), mask)
```

### 完整Python脚本

```python
import qrcode
from PIL import Image, ImageDraw, ImageFont
import os

# 配置
url = "https://wxlawyers.github.io/lawyer-knowledge-graph/"
photo_path = os.path.expanduser("~/Desktop/形象照/a5d7756219a5eef0277fdbc376db9137.jpg")
output_path = os.path.expanduser("~/Desktop/律师名片二维码.png")

# 创建二维码
qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_H, box_size=12, border=2)
qr.add_data(url)
qr.make(fit=True)
qr_img = qr.make_image(fill_color="#0a1628", back_color="white").convert('RGB')

# 创建画布
width, height = 800, 1200
final_img = Image.new('RGB', (width, height), '#0a1628')
draw = ImageDraw.Draw(final_img)

# 加载字体
title_font = ImageFont.truetype("/System/Library/Fonts/STHeiti Medium.ttc", 42)
en_font = ImageFont.truetype("/System/Library/Fonts/STHeiti Light.ttc", 20)
subtitle_font = ImageFont.truetype("/System/Library/Fonts/STHeiti Medium.ttc", 22)
small_font = ImageFont.truetype("/System/Library/Fonts/STHeiti Medium.ttc", 18)

# 顶部金色装饰线
draw.rectangle([0, 0, width, 5], fill='#c9a96e')

# 圆形形象照
photo = Image.open(photo_path).resize((200, 200))
mask = Image.new('L', (200, 200), 0)
ImageDraw.Draw(mask).ellipse([0, 0, 200, 200], fill=255)
photo_circle = Image.new('RGBA', (200, 200), (0, 0, 0, 0))
photo_circle.paste(photo, (0, 0), mask)
final_img.paste(photo_circle, ((width - 200) // 2, 30), photo_circle)

# 标题
draw.text((width//2, 270), "余正洪律师", fill='#c9a96e', font=title_font, anchor='mm')
draw.text((width//2, 315), "Yu Zhenghong, Attorney at Law", fill='#ffffff', font=en_font, anchor='mm')

# 金色分隔线
draw.rectangle([100, 350, width-100, 352], fill='#c9a96e')

# 二维码
qr_size = 380
qr_x = (width - qr_size) // 2
qr_y = 380
draw.rectangle([qr_x-20, qr_y-20, qr_x+qr_size+20, qr_y+qr_size+20], fill='white')
final_img.paste(qr_img.resize((qr_size, qr_size)), (qr_x, qr_y))

# 二维码下方文字
draw.text((width//2, qr_y + qr_size + 40), "扫码访问官网", fill='#ffffff', font=subtitle_font, anchor='mm')
draw.text((width//2, qr_y + qr_size + 80), "涉外法律服务顾问", fill='#c9a96e', font=subtitle_font, anchor='mm')

# 服务领域
services = ["企业出海", "跨境投资与并购", "涉外合同纠纷", "跨境争议解决"]
for i, service in enumerate(services):
    draw.text((width//2, qr_y + qr_size + 130 + i * 35), f"• {service}", fill='#cccccc', font=small_font, anchor='mm')

# 底部联系方式
draw.rectangle([0, height-140, width, height], fill='#1a2a4a')
draw.text((width//2, height-110), "电话: 136-0153-9126", fill='#ffffff', font=small_font, anchor='mm')
draw.text((width//2, height-80), "邮箱: yuzhenghong86@icloud.com", fill='#ffffff', font=small_font, anchor='mm')
draw.text((width//2, height-50), "地址: 无锡市清扬路金匮苑31-3", fill='#cccccc', font=small_font, anchor='mm')
draw.rectangle([0, height-5, width, height], fill='#c9a96e')

# 保存
final_img.save(output_path, quality=95)
print(f"✅ 已保存: {output_path}")
```

## 英文命名规范

| 写法 | 正确性 | 说明 |
|------|--------|------|
| Yu Zhenghong, Attorney at Law | ✅ 最标准 | 美国律师标准称呼 |
| Yu Zhenghong, Esq. | ✅ 正式 | 更正式的称呼 |
| Attorney Yu Zhenghong | ⚠️ 语法不太自然 | 不如上面两种标准 |
| Yu Zhenghong Law Firm | ❌ 不准确 | 指律所，不是个人 |

## 依赖

```bash
pip install qrcode pillow
```

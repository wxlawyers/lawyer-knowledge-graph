# 律师名片二维码生成

## 用途

为律师网站生成精美的商务二维码图片，用于发朋友圈、交换名片、印制宣传材料。

## 技术栈

- Python `qrcode` 库生成二维码
- Python `PIL` (Pillow) 进行图片合成和文字绘制

## ⚠️ PITFALL: macOS 中文字体乱码（2026-06-09教训）

在 macOS 上用 PIL 绘制中文文字时，如果使用不存在的字体路径，会显示乱码。

### 可用中文字体路径（macOS）

| 字体 | 路径 | 说明 |
|------|------|------|
| 华文黑体 Medium | `/System/Library/Fonts/STHeiti Medium.ttc` | ✅ 推荐，粗体标题 |
| 华文黑体 Light | `/System/Library/Fonts/STHeiti Light.ttc` | 正文/英文 |
| Hiragino Sans GB | `/System/Library/Fonts/Hiragino Sans GB.ttc` | 可用 |
| 宋体 | `/System/Library/Fonts/Supplemental/Songti.ttc` | 可用 |
| Arial Unicode | `/System/Library/Fonts/Supplemental/Arial Unicode.ttf` | 可用 |

**注意**：`/System/Library/Fonts/PingFang.ttc` **不存在**（至少在某些macOS版本上），使用会导致乱码。

### 验证字体是否可用

```python
from PIL import ImageFont
import os

font_path = "/System/Library/Fonts/STHeiti Medium.ttc"
if os.path.exists(font_path):
    font = ImageFont.truetype(font_path, 36)
    print("✅ 可用")
else:
    print("❌ 不存在")
```

## 律师英文命名规范

| 写法 | 正确性 | 说明 |
|------|--------|------|
| Yu Zhenghong, Attorney at Law | ✅ 最标准 | 美国律师标准称呼 |
| Yu Zhenghong, Esq. | ✅ 正式 | 更正式的称呼，Esquire缩写 |
| Attorney Yu Zhenghong | ⚠️ 语法不太自然 | 不如上面两种标准 |
| Yu Zhenghong Law Firm | ❌ 不准确 | 指律师事务所，不是律师个人 |

## 标准二维码布局（无照片版）

```
┌──────────────────────────────┐
│     ═══════ 金色装饰线 ═══════   │
│                              │
│        余正洪律师              │  ← 金色大字
│   Yu Zhenghong, Attorney at Law  ← 白色英文
│                              │
│     ──── 金色分隔线 ────       │
│                              │
│   ┌──────────────────────┐   │
│   │                      │   │
│   │      [二维码]         │   │  ← 白底黑码
│   │                      │   │
│   └──────────────────────┘   │
│                              │
│        扫码访问官网            │
│     涉外法律服务顾问           │  ← 金色
│                              │
│     • 企业出海                │
│     • 跨境投资与并购           │
│     • 涉外合同纠纷            │
│     • 跨境争议解决            │
│                              │
│  ┌────────────────────────┐  │
│  │  电话: 136-0153-9126    │  │  ← 深蓝底白字
│  │  邮箱: xxx@icloud.com   │  │
│  │  地址: 无锡市清扬路...   │  │
│  └────────────────────────┘  │
│     ═══════ 金色装饰线 ═══════   │
└──────────────────────────────┘
```

## 照片嵌入版布局

当用户要求"把形象照融入进去"时，生成带圆形律师照片的二维码：

```
┌──────────────────────────────┐
│     ═══════ 金色装饰线 ═══════   │
│                              │
│         ┌──────┐             │
│         │ 圆形 │             │  ← 律师形象照（圆形裁剪）
│         │ 照片 │             │
│         └──────┘             │
│                              │
│        余正洪律师              │
│   Yu Zhenghong, Attorney at Law │
│                              │
│     ──── 金色分隔线 ────       │
│                              │
│   ┌──────────────────────┐   │
│   │      [二维码]         │   │
│   └──────────────────────┘   │
│                              │
│        扫码访问官网            │
│     涉外法律服务顾问           │
│                              │
│     • 企业出海                │
│     • 跨境投资与并购           │
│     • 涉外合同纠纷            │
│     • 跨境争议解决            │
│                              │
│  ┌────────────────────────┐  │
│  │  电话 / 邮箱 / 地址     │  │
│  └────────────────────────┘  │
│     ═══════ 金色装饰线 ═══════   │
└──────────────────────────────┘
```

**照片嵌入代码**：
```python
# 读取形象照
photo = Image.open(os.path.expanduser("~/Desktop/形象照/photo.jpg"))

# 圆形裁剪
photo_size = 200
photo_resized = photo.resize((photo_size, photo_size))
mask = Image.new('L', (photo_size, photo_size), 0)
ImageDraw.Draw(mask).ellipse([0, 0, photo_size, photo_size], fill=255)
photo_circle = Image.new('RGBA', (photo_size, photo_size), (0, 0, 0, 0))
photo_circle.paste(photo_resized, (0, 0), mask)

# 粘贴到画布顶部居中
photo_x = (width - photo_size) // 2
img.paste(photo_circle, (photo_x, 30), photo_circle)
```

**布局调整**：有照片时，画布高度增加到1200px，照片放在顶部，标题和二维码下移。

## 标准配色

- 背景：`#0a1628`（深海军蓝）
- 金色：`#c9a96e`
- 底部栏：`#1a2a4a`
- 文字：白色 `#ffffff`、灰色 `#cccccc`
- 二维码：黑底 `#0a1628` + 白底

## 完整代码模板

```python
import qrcode
from PIL import Image, ImageDraw, ImageFont
import os

# 配置
url = "https://wxlawyers.github.io/lawyer-knowledge-graph/"
desktop_path = os.path.expanduser("~/Desktop/律师名片二维码.png")

# 字体（macOS）
TITLE_FONT = ImageFont.truetype("/System/Library/Fonts/STHeiti Medium.ttc", 40)
SUBTITLE_FONT = ImageFont.truetype("/System/Library/Fonts/STHeiti Medium.ttc", 22)
SMALL_FONT = ImageFont.truetype("/System/Library/Fonts/STHeiti Medium.ttc", 18)
EN_FONT = ImageFont.truetype("/System/Library/Fonts/STHeiti Light.ttc", 20)

# 生成二维码
qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_H, box_size=12, border=2)
qr.add_data(url)
qr.make(fit=True)
qr_img = qr.make_image(fill_color="#0a1628", back_color="white").convert('RGB')

# 创建画布
width, height = 800, 1000
img = Image.new('RGB', (width, height), '#0a1628')
draw = ImageDraw.Draw(img)

# 顶部金色装饰线
draw.rectangle([0, 0, width, 5], fill='#c9a96e')

# 标题
draw.text((width//2, 70), "余正洪律师", fill='#c9a96e', font=TITLE_FONT, anchor='mm')
draw.text((width//2, 120), "Yu Zhenghong, Attorney at Law", fill='#ffffff', font=EN_FONT, anchor='mm')

# 金色分隔线
draw.rectangle([100, 160, width-100, 162], fill='#c9a96e')

# 二维码
qr_size = 380
qr_x, qr_y = (width - qr_size) // 2, 200
draw.rectangle([qr_x-20, qr_y-20, qr_x+qr_size+20, qr_y+qr_size+20], fill='white')
img.paste(qr_img.resize((qr_size, qr_size)), (qr_x, qr_y))

# 二维码下方文字
draw.text((width//2, qr_y + qr_size + 50), "扫码访问官网", fill='#ffffff', font=SUBTITLE_FONT, anchor='mm')
draw.text((width//2, qr_y + qr_size + 90), "涉外法律服务顾问", fill='#c9a96e', font=SUBTITLE_FONT, anchor='mm')

# 服务领域
services = ["企业出海", "跨境投资与并购", "涉外合同纠纷", "跨境争议解决"]
for i, s in enumerate(services):
    draw.text((width//2, qr_y + qr_size + 140 + i * 35), f"• {s}", fill='#cccccc', font=SMALL_FONT, anchor='mm')

# 底部联系方式
draw.rectangle([0, height-130, width, height], fill='#1a2a4a')
draw.text((width//2, height-100), "电话: 136-0153-9126", fill='#ffffff', font=SMALL_FONT, anchor='mm')
draw.text((width//2, height-70), "邮箱: yuzhenghong86@icloud.com", fill='#ffffff', font=SMALL_FONT, anchor='mm')
draw.text((width//2, height-40), "地址: 无锡市清扬路金匮苑31-3", fill='#cccccc', font=SMALL_FONT, anchor='mm')

# 底部金色装饰线
draw.rectangle([0, height-5, width, height], fill='#c9a96e')

# 保存
img.save(desktop_path, quality=95)
print(f"✅ 已保存: {desktop_path}")
```

## Obsidian知识库集成

律师网站的服务领域应与Obsidian知识库同步：

| 网站服务领域 | 知识库文件 |
|-------------|-----------|
| 企业出海 | `11-涉外法律/02-非诉业务/企业出海法律指南.md` |
| 跨境投资与并购 | `11-涉外法律/02-非诉业务/跨境投资与并购法律指南.md` |
| 私人财富管理与家事法 | `11-涉外法律/02-非诉业务/私人财富管理与家事法指南.md` |
| 中英文术语 | `11-涉外法律/06-文书模板/涉外法律中英文术语对照表.md` |

当网站新增服务领域时，同步在Obsidian创建对应的知识卡片。

## 依赖安装

```bash
pip install qrcode[pil] Pillow
```

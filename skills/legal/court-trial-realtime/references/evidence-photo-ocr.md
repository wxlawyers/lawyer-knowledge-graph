# 证据图片 OCR 识别 — 技术参考

## 飞书图片工作流

### ChatCCC 图片下载机制

飞书发送的图片由 ChatCCC 自动下载到本地：
- 路径：`~/.chatccc/images/downloads/`
- 文件名格式：`img_v3_*.jpg`
- 消息格式：`[图片] /path/to/image.jpg`

### 识别流程

1. 用户在飞书发图片
2. ChatCCC 自动下载到 `~/.chatccc/images/downloads/`
3. 用户告诉我"发了图片"
4. 我用 `ls -lt ~/.chatccc/images/downloads/ | head` 找最新文件
5. 用 pytesseract 识别内容
6. 结合法律知识做分析

### 注意事项

- 飞书图片消息会转成文本 `[图片] /path`，但不一定自动传到我的对话
- 需要用户主动告诉我"发了图片"，我才会去找最新文件
- 图片最大 10MB，支持 png/jpg/jpeg/webp/gif/bmp

## Tesseract OCR 配置

### 安装状态

- tesseract：已安装（/usr/local/bin/tesseract）
- pytesseract：已安装（Python 3.9）
- Pillow：已安装
- chi_sim.traineddata：已安装（需修复）

### 中文语言包修复

问题：chi_sim.traineddata 文件可能损坏，导致中文识别失败

解决方案：
```bash
# 从 CDN 镜像下载（GitHub 直接下载会超时）
curl -L --max-time 60 -o /tmp/chi_sim.traineddata \
  "https://cdn.jsdelivr.net/gh/tesseract-ocr/tessdata_fast@main/chi_sim.traineddata"

# 替换原有文件
cp /tmp/chi_sim.traineddata /usr/local/share/tessdata/chi_sim.traineddata
```

⚠️ 不能用 GitHub 直接下载（会超时），必须用 jsdelivr CDN 镜像

### 使用方法

```python
import pytesseract
from PIL import Image

img = Image.open("/path/to/image.jpg")
text = pytesseract.image_to_string(img, lang='chi_sim+eng')
print(text)
```

## vision_analyze 工具状态

当前模型（mimo-v2.5-pro）的视觉接口认证失败（401 错误）。

替代方案：
- 用 pytesseract 做 OCR 识别文字
- 用文本分析能力做法律分析
- 两者结合 = 完整的证据图片分析能力

## 证据图片质证要点

识别证据图片后，按以下维度分析：

| 维度 | 检查点 |
|------|--------|
| 真实性 | 是否原件？有无篡改痕迹？签字/盖章是否清晰？ |
| 合法性 | 取证方式是否合法？形式是否合规？ |
| 关联性 | 与待证事实有无关联？能否证明对方主张？ |
| 完整性 | 是否完整？有无缺页/截断？ |
| 时间性 | 日期是否合理？与案件时间线是否吻合？ |

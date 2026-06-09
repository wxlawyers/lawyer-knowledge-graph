# OCR 证据读取配置指南

## 安装步骤

### 1. tesseract OCR
```bash
brew install tesseract
```

### 2. 中文语言包
GitHub 直接下载经常超时，用 jsdelivr CDN 镜像：
```bash
curl -L -o /usr/local/share/tessdata/chi_sim.traineddata \
  "https://cdn.jsdelivr.net/gh/tesseract-ocr/tessdata_fast@main/chi_sim.traineddata"
```

**版本选择**：
| 版本 | 大小 | 速度 | 准确率 | 推荐 |
|------|------|------|--------|------|
| tessdata_fast | ~2.4MB | 快 | 较高 | ✅ 推荐 |
| tessdata | ~2.8MB | 中 | 高 | 可用 |
| tessdata_best | ~13MB | 慢 | 最高 | 不推荐（速度慢） |

### 3. Python 依赖
```bash
pip3 install pytesseract Pillow
```

## 使用方式

### Python 脚本
```python
import pytesseract
from PIL import Image

img = Image.open("/path/to/evidence.png")
text = pytesseract.image_to_string(img, lang='chi_sim+eng')
print(text)
```

### 命令行
```bash
tesseract /path/to/evidence.png stdout -l chi_sim+eng
```

## 识别能力

| 内容类型 | 识别率 | 注意事项 |
|----------|--------|---------|
| 打印合同 | ⭐⭐⭐⭐⭐ | 清晰度高，准确率最高 |
| 转账凭证 | ⭐⭐⭐⭐ | 注意识别金额和时间 |
| 聊天记录截图 | ⭐⭐⭐⭐ | 打字内容识别率高 |
| 营业执照 | ⭐⭐⭐⭐ | 可自动触发企业查询 |
| 判决书/裁定书 | ⭐⭐⭐⭐ | 可识别案号、裁判要旨 |
| 发票/收据 | ⭐⭐⭐⭐ | 识别金额、日期 |
| 手写文字 | ⭐⭐ | 识别率较低，建议拍打印件 |
| 模糊/倾斜照片 | ⭐⭐ | 拍照要清晰、正对 |

## Pitfalls

1. **GitHub 下载超时**：用 jsdelivr CDN 镜像，不要直接用 raw.githubusercontent.com
2. **chi_sim 识别异常**：可能是语言包损坏，重新下载 tessdata_fast 版本
3. **vision_analyze 不可用**：mimo-v2.5-pro 模型的视觉接口有 API Key 问题，用 tesseract 替代
4. **路径含空格**：用 Python 的 os.walk 查找文件，避免 shell 路径转义问题
5. **长文档**：分页拍照，每页单独识别，准确率更高

## 开庭实战流程

```
拍照 → 保存到本机 → 告诉 Hermes 路径 → OCR 识别 → 法律分析
                                                    ↓
                                              ├── 证据类型判断
                                              ├── 关键信息提取
                                              ├── 法条检索（MCP）
                                              └── 质证要点生成
```

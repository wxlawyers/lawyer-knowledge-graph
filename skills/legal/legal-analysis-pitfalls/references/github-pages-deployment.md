# GitHub Pages 部署检查清单

## 部署步骤

1. 将网站文件放入仓库的 `/docs` 文件夹
2. 推送到 GitHub
3. 进入 Settings → Pages
4. Source 选 `Deploy from a branch`
5. Branch 选 `master`，文件夹选 `/docs`
6. 点击 Save
7. 等待 1-2 分钟

## 常见问题

### Save 按钮灰色
- **原因**：未选择文件夹
- **解决**：先在 Branch 下方的下拉框选择 `/docs` 或 `/root`，Save 按钮才会变亮

### 页面显示乱码（数字+竖线）
- **原因**：HTML 文件中包含行号（如 `1|<!DOCTYPE html>`）
- **根因**：`hermes_tools.read_file()` 会自动添加行号，写回文件时行号变成文件内容
- **解决**：用 Python 删除行号后重新推送
```python
import re
with open('docs/index.html', 'r') as f:
    content = f.read()
content = re.sub(r'^\s*\d+\|', '', content, flags=re.MULTILINE)
with open('docs/index.html', 'w') as f:
    f.write(content)
```

### 浏览器缓存导致看不到更新
- 强制刷新：`Cmd+Shift+R`（Mac）或 `Ctrl+Shift+R`（Windows）
- 或用无痕模式访问

### 图片不显示
- 确认图片路径相对于 HTML 文件（如 `images/photo.jpg`）
- 确认图片文件已推送到 GitHub
- 检查文件名是否有中文（GitHub Pages 可能编码问题）

## 访问地址格式
```
https://<username>.github.io/<repo-name>/
```

## 验证命令
```bash
curl -s -o /dev/null -w "%{http_code}" "https://<username>.github.io/<repo-name>/"
# 返回 200 表示部署成功
```

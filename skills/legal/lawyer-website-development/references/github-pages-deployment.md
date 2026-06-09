# GitHub Pages 部署工作流

## 现有仓库部署流程

### 1. 查找正确的仓库

```bash
# 列出用户所有仓库
curl -s "https://api.github.com/users/wxlawyers/repos?per_page=100" | grep '"name"'

# 检查特定仓库是否存在
curl -s -o /dev/null -w "%{http_code}" https://github.com/wxlawyers/REPO_NAME
```

### 2. 检查仓库结构

```bash
# 查看仓库根目录
curl -s "https://api.github.com/repos/wxlawyers/REPO_NAME/contents" | grep '"name"'

# 查看 website 目录
curl -s "https://api.github.com/repos/wxlawyers/REPO_NAME/contents/website" | grep '"name"'
```

### 3. 克隆并更新

```bash
# 克隆到临时目录
cd /tmp && rm -rf REPO_NAME && git clone git@github.com:wxlawyers/REPO_NAME.git

# 复制更新的文件
cp ~/Documents/lawyer-website/index.html /tmp/REPO_NAME/website/index.html

# 提交并推送
cd /tmp/REPO_NAME
git add website/index.html
git commit -m "feat: 网站更新"
git push origin master

# 清理
rm -rf /tmp/REPO_NAME
```

### 4. 启用 GitHub Pages

**手动操作**：
1. 访问 `https://github.com/wxlawyers/REPO_NAME/settings/pages`
2. Source 选择 "Deploy from a branch"
3. Branch 选择 `master`
4. 文件夹选择 `/website`
5. 点击 Save

**网站地址**：`https://wxlawyers.github.io/REPO_NAME/`

## 常见问题

### Q: 推送失败，提示仓库不存在
**原因**：`.git/config` 中的 remote origin 配置错误
**解决**：
1. 用 API 查找正确的仓库名
2. 修正 remote origin：`git remote set-url origin git@github.com:wxlawyers/CORRECT_REPO.git`

### Q: 推送成功但网站无法访问
**原因**：GitHub Pages 未启用
**解决**：访问仓库设置页面启用 Pages

### Q: 网站显示 404
**原因**：Pages 配置错误（分支或目录不对）
**解决**：检查 Pages 设置，确认分支和目录正确

## 用户仓库清单

| 仓库名 | 用途 | 网站目录 |
|--------|------|----------|
| `wxlawyers/lawyer-knowledge-graph` | 律师知识图谱+涉外网站 | `/website` |

> 如有新仓库，更新此表。

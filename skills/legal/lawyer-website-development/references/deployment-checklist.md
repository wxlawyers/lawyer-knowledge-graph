# 律师网站部署检查清单

## 部署前检查

### 代码检查
- [ ] HTML语法正确（无报错）
- [ ] CSS样式正常（本地预览）
- [ ] 响应式适配（手机、平板、桌面）
- [ ] 所有链接可点击
- [ ] 表单可提交
- [ ] 图片正常显示

### 内容检查
- [ ] 律师信息准确（姓名、电话、邮箱、地址）
- [ ] 案例已脱敏（无当事人真实姓名）
- [ ] 文章内容无错误
- [ ] 版权信息正确

### Git检查
- [ ] 远程仓库存在
- [ ] SSH密钥已配置
- [ ] 代码已提交
- [ ] 推送成功

## GitHub Pages部署

### 步骤
1. 创建仓库：`gh repo create wxlawyers/lawyer-{领域} --public`
2. 推送代码：`git push origin main`
3. 启用Pages：Settings → Pages → Source: main branch
4. 访问地址：`https://wxlawyers.github.io/lawyer-{领域}/`

### 常见问题
- **404错误**：检查仓库名是否正确
- **样式丢失**：检查CSS路径
- **推送失败**：检查SSH密钥和权限

## Gitee Pages部署

### 步骤
1. 创建仓库：Gitee网页创建
2. 推送代码：`git push gitee main`
3. 启用Pages：服务 → Gitee Pages → 部署
4. 访问地址：`https://wxlawyers.gitee.io/lawyer-{领域}/`

### 常见问题
- **部署失败**：检查仓库是否公开
- **更新不生效**：手动触发部署

## 部署后验证

### 功能验证
- [ ] 首页正常加载
- [ ] 导航菜单可点击
- [ ] 案例筛选功能正常
- [ ] 咨询表单可提交
- [ ] 联系方式正确
- [ ] 移动端显示正常

### 性能检查
- [ ] 页面加载速度（<3秒）
- [ ] 图片优化（<500KB）
- [ ] SEO meta标签完整

## 更新流程

### 小更新（文字修改）
```bash
# 1. 修改文件
# 2. 提交
git add -A
git commit -m "fix: 更新联系方式"
# 3. 推送
git push origin main
```

### 大更新（新增模块）
```bash
# 1. 修改文件
# 2. 本地预览测试
# 3. 提交
git add -A
git commit -m "feat: 添加案例展示模块"
# 4. 推送
git push origin main
# 5. 验证线上效果
```

## 备份策略

### 本地备份
- 项目目录：`~/Documents/lawyer-website/`
- 定期备份到外部硬盘

### 远程备份
- GitHub：自动保存所有版本
- Gitee：国内备份

## 域名配置（可选）

### 自定义域名
1. 购买域名（如：yuzhenghong.com）
2. 配置DNS：CNAME指向 `wxlawyers.github.io`
3. GitHub设置：Custom domain填入域名
4. 启用HTTPS

### 域名选择建议
- 优先：`律师名.com` 或 `律师名.cn`
- 备选：`领域+律师名.com`
- 避免：过长或难记的域名

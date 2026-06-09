# GitHub + Gitee 双仓库推送 — 工作流参考

## 仓库信息

| 平台 | 地址 | 用途 |
|------|------|------|
| GitHub | https://github.com/wxlawyers/lawyer-knowledge-graph | 国际备份 |
| Gitee | https://gitee.com/wxlawyers/lawyer-knowledge-graph | 国内访问 |

## 用户信息

- Git 用户名：律见法度
- Git 邮箱：17124052+wxlawyers@user.noreply.gitee.com
- SSH 密钥：已配置（GitHub + Gitee 均可 SSH 推送）

## 推送流程

```bash
cd ~/lawyer-knowledge-graph

# 1. 从 Gitee 克隆（国内更快）
git clone git@gitee.com:wxlawyers/lawyer-knowledge-graph.git

# 2. 添加 GitHub 远程仓库
git remote add github git@github.com:wxlawyers/lawyer-knowledge-graph.git

# 3. 复制技能文件
cp -r ~/.hermes/skills/legal/new-skill skills/legal/

# 4. 提交
git add -A
git commit -m "feat: 描述"

# 5. 推送到两个仓库
git push origin master   # Gitee
git push github master   # GitHub
```

## 注意事项

- GitHub 克隆可能超时，优先用 Gitee 克隆
- `gh` CLI 未安装，不能用 `gh repo` 命令
- 推送前确认 SSH 密钥可用
- README.md 更新后也要提交推送

## 技能文件结构

```
lawyer-knowledge-graph/
├── skills/
│   └── legal/
│       ├── litigation-case-analysis/
│       ├── evidence-organization/
│       ├── legal-research/
│       ├── legal-document-drafting/
│       ├── trial-preparation/
│       ├── trial-response/
│       ├── client-communication/
│       ├── case-management/
│       ├── knowledge-accumulation/
│       ├── business-development/
│       ├── chinese-legal-practice/
│       ├── lawyer-douyin-livestream/
│       └── court-trial-realtime/
├── README.md
├── LICENSE
├── docker-compose.yml
├── .env.example
├── .gitignore
├── docs/
└── scripts/
```

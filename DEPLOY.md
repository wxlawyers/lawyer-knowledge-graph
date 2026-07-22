# 律师知识图谱 - 部署指南（零基础版）

> 本指南面向没有任何编程基础的律师，跟着做就行，大约 15 分钟。

---

## 准备工作：装一个软件

就像用 WPS 需要先装 WPS 一样，这个系统需要先装一个叫 **Docker** 的免费软件。

### macOS（苹果电脑）

1. 打开浏览器，访问 https://www.docker.com/products/docker-desktop/
2. 点击 **Download for Mac** — Apple 芯片选 "Apple Silicon"，Intel 芯片选 "Intel Chip"（不确定的话点左上角苹果图标 → 关于本机，看芯片型号）
3. 下载后双击 `Docker.dmg`，把 Docker 拖到 Applications 文件夹
4. 从启动台打开 Docker，首次会要求输入电脑密码，输入即可
5. 等状态栏右上角出现一个鲸鱼图标并且不再动，就说明启动好了

### Windows

1. 打开浏览器，访问 https://www.docker.com/products/docker-desktop/
2. 点击 **Download for Windows**
3. 双击 `Docker Desktop Installer.exe` 安装，一路下一步
4. 安装完重启电脑
5. 重启后 Docker 会自动启动，等右下角图标变绿即可

> 安装 Docker 是唯一的技术步骤，装好之后就是一马平川。

---

## 第一步：下载项目

### 方式一：下载压缩包（最简单，推荐）

1. 打开 https://gitee.com/wxlawyers/lawyer-knowledge-graph
2. 点击右侧 **克隆/下载** → **下载 ZIP**
3. 解压到任意文件夹，比如桌面

### 方式二：用命令行（如果你装了 Git）

```bash
git clone https://gitee.com/wxlawyers/lawyer-knowledge-graph.git
```

---

## 第二步：获取 AI 密钥

系统需要调用 AI 来提取知识卡片，你需要一个 API Key（可以理解为一把钥匙）。

### 推荐：DeepSeek（便宜，新用户有免费额度）

1. 打开 https://platform.deepseek.com 注册账号
2. 左侧菜单找到 **API Keys** → 点击 **创建 API Key**
3. 复制生成的密钥（形如 `sk-xxxxxxxx`），先保存到备忘录

> 也可以用 Kimi K3（https://platform.moonshot.cn）或 GLM 5.2（https://open.bigmodel.cn），注册流程类似。

---

## 第三步：一键部署

### macOS

1. 打开 **终端**（Command + 空格，输入"终端"回车）
2. 输入以下命令进入项目目录（把路径改成你解压的位置）：

```bash
cd ~/Desktop/lawyer-knowledge-graph
```

3. 运行部署脚本：

```bash
bash deploy.sh
```

4. 脚本会自动引导你选择 AI 模型、粘贴 API Key，然后自动启动所有服务

### Windows

1. 打开 **Git Bash**（安装 Git 时自带，或从开始菜单搜索）
2. 输入以下命令进入项目目录：

```bash
cd ~/Desktop/lawyer-knowledge-graph
```

3. 运行部署脚本：

```bash
bash deploy.sh
```

---

## 第四步：开始使用

打开浏览器，访问：

```
http://localhost:8501
```

你会看到这样的界面：

- **案件录入** — 粘贴判决书，AI 自动提取知识卡片
- **类案检索** — 输入案情描述，秒搜历史经验
- **知识卡片** — 浏览所有已沉淀的知识
- **案件列表** — 查看已录入的案件

API 文档（技术同学用）：http://localhost:8000/docs

---

## 日常操作

| 操作 | 命令 |
|------|------|
| 停止服务 | `docker-compose down` |
| 启动服务 | `docker-compose up -d` |
| 查看状态 | `docker-compose ps` |
| 查看日志 | `docker-compose logs -f` |

> 日常使用不需要反复部署。第一次部署好之后，以后只需要打开 Docker，然后终端执行 `docker-compose up -d` 即可。

---

## 常见问题

### Q：运行 deploy.sh 提示 "command not found: docker"

Docker 没装好或没启动。打开 Docker Desktop 应用，等鲸鱼图标变绿后再试。

### Q：启动后浏览器打不开 localhost:8501

服务可能还在启动中，等 30 秒再刷新。如果还不行，终端运行 `docker-compose ps` 看看四个服务是否都是 running 状态。

### Q：粘贴判决书后提示"提取失败"

检查 API Key 是否正确。打开 `.env` 文件，确认 `LLM_API_KEY=` 后面是你的密钥，没有多余空格。

### Q：想换一个 AI 模型

打开 `.env` 文件，修改这两行：

```
LLM_BASE_URL=https://api.moonshot.cn/v1    # 改成对应平台的地址
LLM_MODEL=kimi-k3                           # 改成对应的模型名
```

改完保存，终端运行 `docker-compose down && docker-compose up -d` 重启即可。

### Q：数据存在哪里

所有数据存在 Docker 的 PostgreSQL 容器中。只要不删除 Docker 卷，数据不会丢失。建议定期备份（导出数据库）。

---

## 如果实在搞不定

把这份指南转给你的技术同事或朋友，整个过程 15 分钟内可以完成。也可以在 GitHub 提 Issue 描述你遇到的问题：

https://github.com/wxlawyers/lawyer-knowledge-graph/issues

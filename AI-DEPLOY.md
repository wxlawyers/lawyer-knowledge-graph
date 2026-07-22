# AI 部署指令 — Lawyer Knowledge Graph

> 本文件供 AI 编程助手（WorkBuddy / Kimi Work / Claude Code 等）读取并执行。
> 目标：在用户本机部署 Lawyer Knowledge Graph 知识图谱系统，完成后浏览器可访问。

---

## 环境要求

- 操作系统：macOS 或 Windows
- Docker Desktop 已安装并运行（状态栏图标为绿色）
- Git 已安装（可选，也可下载 ZIP）
- 用户已注册以下任一 AI 平台并获取 API Key：
  - DeepSeek（推荐）：https://platform.deepseek.com → API Keys → 创建
  - Kimi K3：https://platform.moonshot.cn → API Keys → 创建
  - GLM 5.2：https://open.bigmodel.cn → API Keys → 创建

## 部署步骤

### 1. 克隆项目

```bash
git clone https://gitee.com/wxlawyers/lawyer-knowledge-graph.git
cd lawyer-knowledge-graph
```

### 2. 配置环境变量

向用户索取 API Key，然后创建 `.env` 文件。

根据用户选择的模型写入对应配置（三选一）：

**DeepSeek V4 Pro（默认推荐）：**
```ini
LLM_API_KEY=用户提供的密钥
LLM_BASE_URL=https://api.deepseek.com/v1
LLM_MODEL=deepseek-chat
```

**Kimi K3：**
```ini
LLM_API_KEY=用户提供的密钥
LLM_BASE_URL=https://api.moonshot.cn/v1
LLM_MODEL=kimi-k3
```

**GLM 5.2：**
```ini
LLM_API_KEY=用户提供的密钥
LLM_BASE_URL=https://open.bigmodel.cn/api/paas/v4
LLM_MODEL=glm-5.2
```

> 文件路径：项目根目录下 `.env`（注意文件名以点开头）

### 3. 启动服务

```bash
docker-compose up -d
```

首次启动需要：
- 拉取 PostgreSQL 16 + pgvector 镜像（约 400MB）
- 构建 vector 服务镜像（安装 PyTorch CPU 版 + text2vec，约 10-15 分钟）
- 构建 backend 服务镜像（安装 FastAPI + SQLAlchemy 等，约 2 分钟）
- 构建 frontend 服务镜像（安装 Streamlit，约 2 分钟）
- 下载 text2vec-large-chinese 模型（约 1.3GB）

总计首次启动约 15-25 分钟，请耐心等待。

### 4. 验证服务状态

```bash
docker-compose ps
```

四个服务必须全部为 `running` 状态：

| 服务 | 状态要求 | 说明 |
|------|----------|------|
| db | running (healthy) | PostgreSQL 数据库 |
| vector | running (healthy) | 向量编码服务，模型加载完成后才 healthy |
| backend | running | FastAPI 后端 |
| frontend | running | Streamlit 前端 |

如果 vector 显示 `starting`，说明模型仍在下载/加载，等待即可（最多 5 分钟）。

### 5. 功能验证

```bash
# 检查后端 API
curl http://localhost:8000/api/health
# 预期返回：{"status":"ok","version":"0.1.0"}

# 检查向量服务
curl http://localhost:9998/health
# 预期返回：{"status":"ok","model":"text2vec-large-chinese"}
```

### 6. 告知用户

部署完成后，告诉用户打开浏览器访问：

- **系统界面**：http://localhost:8501
- **API 文档**：http://localhost:8000/docs

## 故障排查

### docker-compose up 报错 "Docker daemon not running"

Docker Desktop 未启动。让用户打开 Docker Desktop 应用，等图标变绿后重试。

### vector 服务一直 starting 不变 healthy

模型下载可能较慢。查看日志：

```bash
docker-compose logs vector
```

如果看到 "模型加载完成"，但状态仍不是 healthy，手动验证：

```bash
curl http://localhost:9998/health
```

### backend 启动后立刻退出

检查数据库连接和 .env 配置：

```bash
docker-compose logs backend
```

常见原因：
- `.env` 文件中 `LLM_API_KEY` 为空或包含中文引号
- `.env` 文件编码不是 UTF-8

### 端口被占用

如果 5432/8000/8501/9998 已被其他程序占用，修改 `docker-compose.yml` 中的端口映射。

## 日常运维命令

```bash
docker-compose down          # 停止所有服务
docker-compose up -d         # 启动所有服务（非首次约 30 秒）
docker-compose ps            # 查看服务状态
docker-compose logs -f       # 查看实时日志
docker-compose logs -f backend  # 只看后端日志
```

## 项目信息

- GitHub：https://github.com/wxlawyers/lawyer-knowledge-graph
- Gitee：https://gitee.com/wxlawyers/lawyer-knowledge-graph
- License：Apache 2.0

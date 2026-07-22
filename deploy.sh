#!/bin/bash
# Lawyer Knowledge Graph 一键部署脚本
# 用法：bash deploy.sh
# 适用：macOS / Linux（Windows 用户请用 Git Bash 运行）

set -e

PROJECT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$PROJECT_DIR"

# 颜色
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

print_ok()   { echo -e "${GREEN}[✓]${NC} $1"; }
print_warn() { echo -e "${YELLOW}[!]${NC} $1"; }
print_err()  { echo -e "${RED}[✗]${NC} $1"; }

echo "============================================"
echo "  律师知识图谱 - 一键部署"
echo "============================================"
echo ""

# ── 第一步：检查 Docker ──────────────────────
echo "【第一步】检查 Docker 环境..."
if ! command -v docker &>/dev/null; then
    print_err "未检测到 Docker，请先安装："
    echo ""
    echo "  macOS（推荐）："
    echo "    打开 https://www.docker.com/products/docker-desktop/"
    echo "    下载 Docker Desktop for Mac，双击安装即可"
    echo ""
    echo "  Windows："
    echo "    下载 Docker Desktop for Windows，安装后重启"
    echo ""
    echo "安装完成后重新运行本脚本：bash deploy.sh"
    exit 1
fi

if ! docker info &>/dev/null 2>&1; then
    print_err "Docker 已安装但未启动，请先打开 Docker Desktop 应用，等状态栏图标变绿后再运行本脚本。"
    exit 1
fi
print_ok "Docker 环境正常"

# ── 第二步：检查 docker-compose ──────────────
echo ""
echo "【第二步】检查 Docker Compose..."
if docker compose version &>/dev/null 2>&1; then
    COMPOSE_CMD="docker compose"
elif command -v docker-compose &>/dev/null; then
    COMPOSE_CMD="docker-compose"
else
    print_err "未检测到 Docker Compose，请确保 Docker Desktop 为最新版本。"
    exit 1
fi
print_ok "Docker Compose 就绪（$COMPOSE_CMD）"

# ── 第三步：配置环境变量 ──────────────────────
echo ""
echo "【第三步】配置环境变量..."
if [ ! -f .env ]; then
    cp .env.example .env
    print_warn "已从模板创建 .env 文件，需要填入 LLM API Key"
    echo ""
    echo "请选择你要使用的 AI 模型："
    echo "  1. DeepSeek V4 Pro（推荐，便宜好用）"
    echo "  2. Kimi K3（月之暗面）"
    echo "  3. GLM 5.2（智谱）"
    read -p "输入序号（1-3，默认1）：" llm_choice

    case $llm_choice in
        2)
            sed -i.bak 's|LLM_BASE_URL=.*|LLM_BASE_URL=https://api.moonshot.cn/v1|' .env
            sed -i.bak 's|LLM_MODEL=.*|LLM_MODEL=kimi-k3|' .env
            echo "已切换为 Kimi K3"
            API_URL_HINT="https://platform.moonshot.cn"
            ;;
        3)
            sed -i.bak 's|LLM_BASE_URL=.*|LLM_BASE_URL=https://open.bigmodel.cn/api/paas/v4|' .env
            sed -i.bak 's|LLM_MODEL=.*|LLM_MODEL=glm-5.2|' .env
            echo "已切换为 GLM 5.2"
            API_URL_HINT="https://open.bigmodel.cn"
            ;;
        *)
            echo "使用默认 DeepSeek V4 Pro"
            API_URL_HINT="https://platform.deepseek.com"
            ;;
    esac

    echo ""
    echo "你需要一个 API Key（密钥），获取方式："
    echo "  DeepSeek：打开 ${API_URL_HINT} 注册后在 API Keys 页面创建"
    echo "  新用户通常有免费额度，够用很久"
    echo ""
    read -p "请粘贴你的 API Key：" api_key
    if [ -n "$api_key" ]; then
        sed -i.bak "s|LLM_API_KEY=.*|LLM_API_KEY=${api_key}|" .env
        print_ok "API Key 已写入"
    else
        print_warn "未输入 API Key，稍后请手动编辑 .env 文件填入"
    fi
    rm -f .env.bak
else
    print_ok ".env 已存在，跳过配置"
fi

# ── 第四步：启动服务 ──────────────────────────
echo ""
echo "【第四步】启动服务（首次需要下载镜像，约3-5分钟）..."
$COMPOSE_CMD up -d

echo ""
echo "等待服务启动..."
sleep 10

# ── 第五步：验证 ──────────────────────────────
echo ""
echo "【第五步】验证服务状态..."
$COMPOSE_CMD ps

echo ""
echo "============================================"
echo "  部署完成！"
echo "============================================"
echo ""
echo "  前端界面：http://localhost:8501"
echo "  API 文档：http://localhost:8000/docs"
echo ""
echo "  打开浏览器访问 http://localhost:8501 即可开始使用"
echo ""
echo "  停止服务：  $COMPOSE_CMD down"
echo "  查看状态：  $COMPOSE_CMD ps"
echo "  查看日志：  $COMPOSE_CMD logs -f"
echo ""

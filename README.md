# Lawyer Knowledge Graph (律师知识图谱)

> 面向诉讼律师的AI个人知识管理系统。案件经验自动沉淀、类案智能检索、法规动态追踪。

## 功能

- **案件知识沉淀**：粘贴裁判文书或案卷摘要，AI自动提取争议焦点、裁判规则、适用法条、办案经验，生成结构化知识卡片
- **类案智能检索**：输入新案件描述，基于向量相似度匹配历史案件，推送相关法条
- **法规动态追踪**：设置关注的法律领域，自动检索新增司法解释/指导性案例，生成更新摘要

## 技术栈

| 组件 | 技术 |
|------|------|
| 后端 | Python 3.11 + FastAPI |
| 数据库 | PostgreSQL + pgvector |
| 向量模型 | text2vec-large-chinese |
| LLM | DeepSeek V3 / Qwen2.5 |
| 前端MVP | Streamlit |
| 部署 | Docker Compose |

## 快速开始

### 1. 环境准备

```bash
# 克隆项目
git clone https://github.com/yulvshi/lawyer-knowledge-graph.git
cd lawyer-knowledge-graph

# 复制环境变量
cp .env.example .env
# 编辑 .env 填入你的API密钥
```

### 2. Docker一键启动

```bash
docker-compose up -d
```

这会启动：
- PostgreSQL + pgvector（端口5432）
- 向量模型服务（端口9998）
- FastAPI后端（端口8000）
- Streamlit前端（端口8501）

### 3. 访问

- 前端：http://localhost:8501
- API文档：http://localhost:8000/docs

## 目录结构

```
├── backend/          # FastAPI后端
│   ├── app/
│   │   ├── main.py          # 入口
│   │   ├── config.py        # 配置
│   │   ├── db.py            # 数据库连接
│   │   ├── models/          # SQLAlchemy模型
│   │   ├── schemas/         # Pydantic模型
│   │   ├── services/        # 业务逻辑
│   │   └── api/             # 路由
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/         # Streamlit前端
│   ├── app.py
│   └── requirements.txt
├── docs/             # 技术文档
│   ├── data-model.md        # 数据模型设计
│   └── api-design.md        # API接口设计
├── scripts/          # 独立工具脚本
│   ├── extract_cards.py     # 知识卡片提取
│   └── vector_search.py     # 向量检索
├── docker-compose.yml
├── .env.example
└── README.md
```

## 环境变量

| 变量 | 说明 | 必填 |
|------|------|------|
| DATABASE_URL | PostgreSQL连接字符串 | 是 |
| LLM_API_KEY | DeepSeek/Qwen API密钥 | 是 |
| LLM_BASE_URL | LLM API地址 | 是 |
| LLM_MODEL | 模型名称 | 是 |
| VECTOR_API_URL | 本地向量模型服务地址 | 否 |
| PKULAW_API_KEY | 北大法宝API密钥 | 否 |
| YUANDIAN_API_KEY | 华宇元典API密钥 | 否 |

## MVP开发计划（2-3周）

### Week 1：基础架构
- [x] 项目结构搭建
- [x] 数据模型设计
- [ ] Docker Compose配置
- [ ] FastAPI + SQLAlchemy初始化
- [ ] 案件录入API + LLM知识卡片提取
- [ ] Streamlit案件录入页面

### Week 2：检索核心
- [ ] 中文文本向量化pipeline
- [ ] pgvector相似度检索API
- [ ] Streamlit类案检索页面
- [ ] 北大法宝/元典API对接

### Week 3：法规追踪 + 打磨
- [ ] 法规定期检索 + 摘要生成
- [ ] Streamlit法规追踪页面
- [ ] 端到端测试
- [ ] 部署文档完善

## 扩展路线（产品化方向）

- [ ] 多用户支持 + 权限管理
- [ ] 知识图谱可视化（Neo4j）
- [ ] 庭审准备模块（质证提纲生成）
- [ ] 移动端适配
- [ ] SaaS多租户部署

## License

MIT

## Author

余律师 (yulvshi) - 江苏无锡，资深民商事律师

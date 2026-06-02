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

## Hermes Agent 法律技能集

本仓库包含面向诉讼律师的 Hermes Agent 技能，覆盖从接案到结案的全流程。

| 技能 | 功能 |
|------|------|
| [litigation-case-analysis](skills/legal/litigation-case-analysis/) | 案件分析与请求权基础分析 |
| [evidence-organization](skills/legal/evidence-organization/) | 证据组织与四性验证 |
| [legal-research](skills/legal/legal-research/) | 法律检索与案例研究 |
| [legal-document-drafting](skills/legal/legal-document-drafting/) | 法律文书撰写 |
| [trial-preparation](skills/legal/trial-preparation/) | 庭前准备 |
| [trial-response](skills/legal/trial-response/) | 庭审应对 |
| [client-communication](skills/legal/client-communication/) | 当事人沟通 |
| [case-management](skills/legal/case-management/) | 案件管理 |
| [knowledge-accumulation](skills/legal/knowledge-accumulation/) | 知识沉淀与复用 |
| [business-development](skills/legal/business-development/) | 案源开发与品牌建设 |
| [chinese-legal-practice](skills/legal/chinese-legal-practice/) | 中国法律实务技能集 |
| [lawyer-douyin-livestream](skills/legal/lawyer-douyin-livestream/) | 律师抖音直播助手 |

### 集成工具

- **北大法宝**：9个HTTP MCP服务（法规搜索、案例检索、法条检索等）
- **元典智库**：5个MCP工具（法规检索、法条检索、案例检索、法规详情、法条详情）
- **快查企业数据**：企业工商信息、司法风险、知识产权等多维数据查询
- **法智法律检索**：法条检索、案例检索、法律文章检索

### 快速使用

```bash
# 安装到 Hermes Agent
cp -r skills/legal/* ~/.hermes/skills/legal/

# 自然语言调用
# "帮我分析这个案件的请求权基础"
# "查一下民法典关于违约责任的规定"
# "帮我准备一期关于劳动纠纷的直播脚本"
```

## License

MIT

## Author

余律师 (wxlawyers) - 江苏三诚律师事务所，资深诉讼律师

# 数据模型设计

## 核心表：cases（案件）

| 字段 | 类型 | 说明 |
|------|------|------|
| id | UUID PK | 主键 |
| case_number | VARCHAR(100) | 案号 |
| case_type | VARCHAR(50) | 案由（如"买卖合同纠纷"） |
| court | VARCHAR(100) | 审理法院 |
| status | ENUM | 进行中/已结案/已归档 |
| plaintiff | TEXT | 原告信息（脱敏） |
| defendant | TEXT | 被告信息（脱敏） |
| claim_amount | DECIMAL | 诉讼标的额 |
| filing_date | DATE | 立案日期 |
| closing_date | DATE | 结案日期（可空） |
| result | TEXT | 裁判结果摘要 |
| notes | TEXT | 律师办案笔记 |
| practice_area | VARCHAR(50) | 执业领域标签 |
| created_at | TIMESTAMP | 录入时间 |
| updated_at | TIMESTAMP | 更新时间 |

## 核心表：knowledge_cards（知识卡片）

| 字段 | 类型 | 说明 |
|------|------|------|
| id | UUID PK | 主键 |
| case_id | UUID FK | 关联案件 |
| card_type | ENUM | 争议焦点/裁判规则/法条适用/办案经验 |
| title | VARCHAR(200) | 标题 |
| content | TEXT | 正文 |
| keywords | JSONB | 关键词标签数组 |
| embedding | vector(1024) | 向量（pgvector） |
| created_at | TIMESTAMP | 创建时间 |

## 核心表：law_updates（法规更新追踪）

| 字段 | 类型 | 说明 |
|------|------|------|
| id | UUID PK | 主键 |
| source | VARCHAR(50) | 来源（北大法宝/元典/手动） |
| law_name | VARCHAR(200) | 法律/法规名称 |
| update_type | ENUM | 新增/修订/废止/司法解释/指导案例 |
| summary | TEXT | AI生成的更新摘要 |
| effective_date | DATE | 生效日期 |
| raw_text | TEXT | 原文（可空） |
| practice_areas | JSONB | 关联执业领域 |
| created_at | TIMESTAMP | 记录时间 |

## 核心表：practice_areas（执业领域配置）

| 字段 | 类型 | 说明 |
|------|------|------|
| id | UUID PK | 主键 |
| name | VARCHAR(50) | 领域名称（如"合同纠纷"） |
| track_frequency | ENUM | 每日/每周/每月 |
| last_tracked | TIMESTAMP | 上次追踪时间 |
| is_active | BOOLEAN | 是否启用 |

## 索引

```sql
-- 向量相似度检索索引（HNSW，推荐）
CREATE INDEX idx_knowledge_embedding ON knowledge_cards 
USING hnsw (embedding vector_cosine_ops) WITH (m = 16, ef_construction = 64);

-- 案由检索索引
CREATE INDEX idx_cases_type ON cases(case_type);
CREATE INDEX idx_cases_status ON cases(status);
CREATE INDEX idx_cases_date ON cases(filing_date);

-- 法规追踪索引
CREATE INDEX idx_law_areas ON law_updates USING GIN(practice_areas);
CREATE INDEX idx_law_date ON law_updates(created_at);
```

## 向量化策略

知识卡片的embedding字段存储1024维向量，使用 `text2vec-large-chinese` 或 `bge-large-zh-v1.5` 生成。

向量化内容 = `title + "。" + content` 的拼接文本，确保语义检索覆盖标题和正文。

检索时使用余弦相似度（cosine similarity），阈值建议 0.7 以上为高匹配。

## 数据脱敏规则

- 原告/被告信息：只保留"甲""乙""丙"等代号，不存储真实姓名
- 案号：完整保留（公开信息）
- 标的额：完整保留（用于类案匹配参考）
- 办案笔记：律师自行决定脱敏程度

-- Lawyer Knowledge Graph - 数据库初始化
-- PostgreSQL 16 + pgvector

CREATE EXTENSION IF NOT EXISTS vector;

-- 案件表
CREATE TABLE IF NOT EXISTS cases (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    case_number VARCHAR(100),
    case_type VARCHAR(50),
    court VARCHAR(100),
    status VARCHAR(20) DEFAULT '已结案',
    plaintiff TEXT,
    defendant TEXT,
    claim_amount DECIMAL(14,2),
    filing_date DATE,
    closing_date DATE,
    result TEXT,
    notes TEXT,
    practice_area VARCHAR(50),
    raw_text TEXT,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- 知识卡片表
CREATE TABLE IF NOT EXISTS knowledge_cards (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    case_id UUID REFERENCES cases(id) ON DELETE CASCADE,
    card_type VARCHAR(20) NOT NULL,
    title VARCHAR(200) NOT NULL,
    content TEXT NOT NULL,
    keywords JSONB DEFAULT '[]'::jsonb,
    embedding vector(768),
    created_at TIMESTAMP DEFAULT NOW()
);

-- 法规更新表
CREATE TABLE IF NOT EXISTS law_updates (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    source VARCHAR(50),
    law_name VARCHAR(200),
    update_type VARCHAR(30),
    summary TEXT,
    effective_date DATE,
    raw_text TEXT,
    practice_areas JSONB DEFAULT '[]'::jsonb,
    created_at TIMESTAMP DEFAULT NOW()
);

-- 执业领域配置表
CREATE TABLE IF NOT EXISTS practice_areas (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(50) UNIQUE NOT NULL,
    track_frequency VARCHAR(20) DEFAULT '每周',
    last_tracked TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE
);

-- 索引
CREATE INDEX IF NOT EXISTS idx_kc_embedding ON knowledge_cards
    USING hnsw (embedding vector_cosine_ops) WITH (m = 16, ef_construction = 64);
CREATE INDEX IF NOT EXISTS idx_cases_type ON cases(case_type);
CREATE INDEX IF NOT EXISTS idx_cases_status ON cases(status);
CREATE INDEX IF NOT EXISTS idx_cases_date ON cases(filing_date);
CREATE INDEX IF NOT EXISTS idx_law_areas ON law_updates USING GIN(practice_areas);
CREATE INDEX IF NOT EXISTS idx_law_date ON law_updates(created_at);

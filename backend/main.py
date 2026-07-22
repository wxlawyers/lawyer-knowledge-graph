"""FastAPI 应用入口"""
import uuid
from datetime import datetime
from typing import Optional
from pydantic import BaseModel
from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends, HTTPException, Query
from sqlalchemy import select, func, text
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_db, engine, Base
from models import Case, KnowledgeCard, LawUpdate, PracticeArea
from services import extract_cards_from_text, create_case_with_cards, search_similar_cards


@asynccontextmanager
async def lifespan(app: FastAPI):
    # 启动时自动建表 + 确保 pgvector 扩展存在
    async with engine.begin() as conn:
        await conn.execute(text("CREATE EXTENSION IF NOT EXISTS vector"))
        await conn.run_sync(Base.metadata.create_all)
    yield

app = FastAPI(
    title="Lawyer Knowledge Graph API",
    description="面向诉讼律师的 AI 个人知识管理系统",
    version="0.1.0",
    lifespan=lifespan,
)


# ── Pydantic 模型 ──────────────────────────────────────────

class CaseCreate(BaseModel):
    mode: str = "paste"  # "paste" 或 "manual"
    raw_text: Optional[str] = None
    practice_area: str = ""
    notes: str = ""
    # manual 模式字段
    case_number: Optional[str] = None
    case_type: Optional[str] = None
    court: Optional[str] = None
    result: Optional[str] = None


class SearchQuery(BaseModel):
    query: str
    top_k: int = 10
    min_similarity: float = 0.6


class CardOut(BaseModel):
    id: uuid.UUID
    card_type: str
    title: str
    content: str
    case_number: Optional[str] = None
    case_type: Optional[str] = None
    similarity: Optional[float] = None


# ── 案件管理 ───────────────────────────────────────────────

@app.post("/api/cases")
async def create_case(body: CaseCreate, db: AsyncSession = Depends(get_db)):
    """录入新案件 — 粘贴裁判文书由 LLM 自动提取，或手动录入"""
    if body.mode == "paste":
        if not body.raw_text:
            raise HTTPException(400, "paste 模式需要 raw_text")
        extracted = await extract_cards_from_text(body.raw_text)
        if "error" in extracted:
            raise HTTPException(500, extracted["error"])
        case = await create_case_with_cards(
            db, extracted, body.raw_text, body.practice_area
        )
        return {
            "case_id": str(case.id),
            "extracted": extracted,
        }
    else:
        case = Case(
            case_number=body.case_number,
            case_type=body.case_type,
            court=body.court,
            result=body.result,
            notes=body.notes,
            practice_area=body.practice_area,
        )
        db.add(case)
        await db.commit()
        await db.refresh(case)
        return {"case_id": str(case.id)}


@app.get("/api/cases")
async def list_cases(
    page: int = Query(1, ge=1),
    size: int = Query(20, ge=1, le=100),
    case_type: Optional[str] = None,
    db: AsyncSession = Depends(get_db),
):
    """分页查询案件列表"""
    stmt = select(Case).order_by(Case.created_at.desc())
    if case_type:
        stmt = stmt.where(Case.case_type == case_type)
    stmt = stmt.offset((page - 1) * size).limit(size)
    result = await db.execute(stmt)
    cases = [
        {
            "id": str(c.id),
            "case_number": c.case_number,
            "case_type": c.case_type,
            "court": c.court,
            "result": (c.result or "")[:100],
            "created_at": c.created_at.isoformat() if c.created_at else None,
        }
        for c in result.scalars()
    ]
    return {"page": page, "size": size, "cases": cases}


@app.get("/api/cases/{case_id}")
async def get_case(case_id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    """获取案件详情 + 关联知识卡片"""
    case = await db.get(Case, case_id)
    if not case:
        raise HTTPException(404, "案件不存在")
    stmt = select(KnowledgeCard).where(KnowledgeCard.case_id == case_id)
    result = await db.execute(stmt)
    cards = [
        {
            "id": str(c.id),
            "card_type": c.card_type,
            "title": c.title,
            "content": c.content,
        }
        for c in result.scalars()
    ]
    return {
        "id": str(case.id),
        "case_number": case.case_number,
        "case_type": case.case_type,
        "court": case.court,
        "result": case.result,
        "notes": case.notes,
        "practice_area": case.practice_area,
        "created_at": case.created_at.isoformat() if case.created_at else None,
        "knowledge_cards": cards,
    }


# ── 类案检索 ───────────────────────────────────────────────

@app.post("/api/search")
async def search(body: SearchQuery, db: AsyncSession = Depends(get_db)):
    """语义相似度检索 — 输入案件描述，返回相似知识卡片"""
    results = await search_similar_cards(db, body.query, body.top_k, body.min_similarity)
    return {"query": body.query, "results": results}


# ── 知识卡片 ───────────────────────────────────────────────

@app.get("/api/cards")
async def list_cards(
    page: int = Query(1, ge=1),
    size: int = Query(20, ge=1, le=100),
    card_type: Optional[str] = None,
    db: AsyncSession = Depends(get_db),
):
    """分页查询知识卡片"""
    stmt = select(KnowledgeCard).order_by(KnowledgeCard.created_at.desc())
    if card_type:
        stmt = stmt.where(KnowledgeCard.card_type == card_type)
    stmt = stmt.offset((page - 1) * size).limit(size)
    result = await db.execute(stmt)
    cards = [
        {
            "id": str(c.id),
            "card_type": c.card_type,
            "title": c.title,
            "content": (c.content or "")[:200],
            "created_at": c.created_at.isoformat() if c.created_at else None,
        }
        for c in result.scalars()
    ]
    return {"page": page, "size": size, "cards": cards}


# ── 法规追踪 ───────────────────────────────────────────────

@app.get("/api/lawtrack/updates")
async def list_law_updates(
    page: int = Query(1, ge=1),
    size: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
):
    """获取法规更新列表"""
    stmt = (
        select(LawUpdate)
        .order_by(LawUpdate.created_at.desc())
        .offset((page - 1) * size)
        .limit(size)
    )
    result = await db.execute(stmt)
    updates = [
        {
            "id": str(u.id),
            "source": u.source,
            "law_name": u.law_name,
            "update_type": u.update_type,
            "summary": (u.summary or "")[:200],
            "effective_date": u.effective_date.isoformat() if u.effective_date else None,
            "created_at": u.created_at.isoformat() if u.created_at else None,
        }
        for u in result.scalars()
    ]
    return {"page": page, "size": size, "updates": updates}


# ── 健康检查 ───────────────────────────────────────────────

@app.get("/api/health")
async def health():
    return {"status": "ok", "version": "0.1.0"}




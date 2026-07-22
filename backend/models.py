"""SQLAlchemy 数据模型"""
import uuid
from datetime import date, datetime
from pgvector.sqlalchemy import Vector
from sqlalchemy import String, Text, DECIMAL, Date, DateTime, Boolean, JSON, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database import Base

EMBEDDING_DIM = 768  # text2vec-large-chinese 输出维度


class Case(Base):
    __tablename__ = "cases"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    case_number: Mapped[str | None] = mapped_column(String(100))
    case_type: Mapped[str | None] = mapped_column(String(50))
    court: Mapped[str | None] = mapped_column(String(100))
    status: Mapped[str] = mapped_column(String(20), default="已结案")
    plaintiff: Mapped[str | None] = mapped_column(Text)
    defendant: Mapped[str | None] = mapped_column(Text)
    claim_amount: Mapped[float | None] = mapped_column(DECIMAL(14, 2))
    filing_date: Mapped[date | None] = mapped_column(Date)
    closing_date: Mapped[date | None] = mapped_column(Date)
    result: Mapped[str | None] = mapped_column(Text)
    notes: Mapped[str | None] = mapped_column(Text)
    practice_area: Mapped[str | None] = mapped_column(String(50))
    raw_text: Mapped[str | None] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    cards: Mapped[list["KnowledgeCard"]] = relationship(
        back_populates="case", cascade="all, delete-orphan"
    )


class KnowledgeCard(Base):
    __tablename__ = "knowledge_cards"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    case_id: Mapped[uuid.UUID | None] = mapped_column(ForeignKey("cases.id", ondelete="CASCADE"))
    card_type: Mapped[str] = mapped_column(String(20))
    title: Mapped[str] = mapped_column(String(200))
    content: Mapped[str] = mapped_column(Text)
    keywords: Mapped[dict] = mapped_column(JSON, default=list)
    embedding = mapped_column(Vector(EMBEDDING_DIM))
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    case: Mapped[Case | None] = relationship(back_populates="cards")


class LawUpdate(Base):
    __tablename__ = "law_updates"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    source: Mapped[str | None] = mapped_column(String(50))
    law_name: Mapped[str | None] = mapped_column(String(200))
    update_type: Mapped[str | None] = mapped_column(String(30))
    summary: Mapped[str | None] = mapped_column(Text)
    effective_date: Mapped[date | None] = mapped_column(Date)
    raw_text: Mapped[str | None] = mapped_column(Text)
    practice_areas: Mapped[dict] = mapped_column(JSON, default=list)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class PracticeArea(Base):
    __tablename__ = "practice_areas"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(50), unique=True)
    track_frequency: Mapped[str] = mapped_column(String(20), default="每周")
    last_tracked: Mapped[datetime | None] = mapped_column(DateTime)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

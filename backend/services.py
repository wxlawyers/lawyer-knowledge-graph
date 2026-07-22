"""核心业务逻辑：知识卡片提取、向量化、相似度检索"""
import json
import os
import httpx
from sqlalchemy import select, text
from sqlalchemy.ext.asyncio import AsyncSession
from models import Case, KnowledgeCard

LLM_API_KEY = os.getenv("LLM_API_KEY", "")
LLM_BASE_URL = os.getenv("LLM_BASE_URL", "https://api.deepseek.com/v1")
LLM_MODEL = os.getenv("LLM_MODEL", "deepseek-chat")
VECTOR_API_URL = os.getenv("VECTOR_API_URL", "http://localhost:9998")

EXTRACT_PROMPT = """你是一位资深民商事律师的助手。请从以下案件材料中提取结构化信息，严格按JSON格式输出。

案件材料：
{text}

请输出以下JSON（不要输出其他内容）：
{{
  "case_number": "案号（如无法提取则为空字符串）",
  "case_type": "案由",
  "court": "审理法院",
  "claim_amount": null,
  "result": "裁判结果摘要（100字以内）",
  "knowledge_cards": [
    {{
      "type": "争议焦点",
      "title": "简短标题（15字以内）",
      "content": "详细描述（100-200字）"
    }}
  ]
}}

注意：
1. knowledge_cards的type只能是：争议焦点、裁判规则、法条适用、办案经验
2. 至少生成3个知识卡片
3. 裁判规则要提炼为可复用的裁判规则，而非单纯复述本案事实
4. 法条适用要精确到具体法条编号和内容要点
5. 办案经验是律师视角的实务技巧，如"此类案件应重点收集XX证据"
"""


async def extract_cards_from_text(raw_text: str) -> dict:
    """调用 LLM 从案件原文提取结构化信息 + 知识卡片"""
    if not LLM_API_KEY:
        return {"error": "未配置 LLM_API_KEY"}

    prompt = EXTRACT_PROMPT.format(text=raw_text[:8000])

    async with httpx.AsyncClient(timeout=90) as client:
        resp = await client.post(
            f"{LLM_BASE_URL}/chat/completions",
            headers={"Authorization": f"Bearer {LLM_API_KEY}"},
            json={
                "model": LLM_MODEL,
                "messages": [{"role": "user", "content": prompt}],
                "temperature": 0.3,
                "max_tokens": 2000,
            },
        )

    if resp.status_code != 200:
        return {"error": f"LLM API 调用失败: {resp.status_code} {resp.text[:200]}"}

    content = resp.json()["choices"][0]["message"]["content"]

    # 清理 markdown 代码块
    cleaned = content.strip()
    if cleaned.startswith("```"):
        cleaned = cleaned.split("\n", 1)[1]
        if cleaned.endswith("```"):
            cleaned = cleaned[:-3]
        cleaned = cleaned.strip()

    try:
        return json.loads(cleaned)
    except json.JSONDecodeError as e:
        return {"error": f"JSON 解析失败: {e}", "raw_content": content}


async def get_embedding(text: str) -> list[float]:
    """调用本地向量模型获取文本 embedding"""
    async with httpx.AsyncClient(timeout=30) as client:
        resp = await client.post(
            f"{VECTOR_API_URL}/embed",
            json={"texts": [text]},
        )
    if resp.status_code == 200:
        return resp.json()["embeddings"][0]
    raise RuntimeError(f"向量化失败: {resp.status_code} {resp.text[:200]}")


async def create_case_with_cards(db: AsyncSession, extracted: dict, raw_text: str, practice_area: str = "") -> Case:
    """创建案件 + 关联知识卡片（含向量索引）"""
    case = Case(
        case_number=extracted.get("case_number", ""),
        case_type=extracted.get("case_type", ""),
        court=extracted.get("court", ""),
        claim_amount=extracted.get("claim_amount"),
        result=extracted.get("result", ""),
        practice_area=practice_area,
        raw_text=raw_text,
    )
    db.add(case)
    await db.flush()  # 获取 case.id

    for card_data in extracted.get("knowledge_cards", []):
        embedding = await get_embedding(
            f"{card_data['title']}。{card_data['content']}"
        )
        card = KnowledgeCard(
            case_id=case.id,
            card_type=card_data["type"],
            title=card_data["title"],
            content=card_data["content"],
            embedding=embedding,
        )
        db.add(card)

    await db.commit()
    await db.refresh(case)
    return case


async def search_similar_cards(
    db: AsyncSession, query: str, top_k: int = 10, min_similarity: float = 0.6
) -> list[dict]:
    """语义相似度检索知识卡片"""
    embedding = await get_embedding(query)

    sql = text("""
        SELECT
            kc.id,
            kc.title,
            kc.content,
            kc.card_type,
            c.case_number,
            c.case_type,
            1 - (kc.embedding <=> :embedding::vector) AS similarity
        FROM knowledge_cards kc
        LEFT JOIN cases c ON kc.case_id = c.id
        WHERE 1 - (kc.embedding <=> :embedding::vector) > :min_sim
        ORDER BY kc.embedding <=> :embedding::vector
        LIMIT :top_k
    """)

    embedding_str = "[" + ",".join(str(x) for x in embedding) + "]"
    result = await db.execute(
        sql,
        {
            "embedding": embedding_str,
            "min_sim": min_similarity,
            "top_k": top_k,
        },
    )
    return [dict(row._mapping) for row in result.fetchall()]

"""text2vec 向量编码 HTTP 服务"""
import os
import logging
from typing import List
from fastapi import FastAPI
from pydantic import BaseModel

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Text2Vec Embedding Server", version="0.1.0")

MODEL_NAME = os.getenv("MODEL_NAME", "text2vec-large-chinese")

_embedder = None


def get_embedder():
    global _embedder
    if _embedder is None:
        from text2vec import SentenceModel
        logger.info(f"加载向量模型: {MODEL_NAME}（首次加载需下载，约 1-2 分钟）...")
        _embedder = SentenceModel(MODEL_NAME)
        logger.info("模型加载完成")
    return _embedder


class EmbedRequest(BaseModel):
    texts: List[str]


class EmbedResponse(BaseModel):
    embeddings: List[List[float]]


@app.get("/health")
def health():
    return {"status": "ok", "model": MODEL_NAME}


@app.post("/embed", response_model=EmbedResponse)
def embed(req: EmbedRequest):
    model = get_embedder()
    vectors = model.encode(req.texts)
    if hasattr(vectors, "tolist"):
        vectors = vectors.tolist()
    return {"embeddings": vectors}

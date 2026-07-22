"""text2vec 向量编码 HTTP 服务"""
import os
import logging
import threading
from typing import List
from fastapi import FastAPI, Response
from pydantic import BaseModel

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Text2Vec Embedding Server", version="0.1.0")

MODEL_NAME = os.getenv("MODEL_NAME", "text2vec-large-chinese")

_embedder = None
_model_ready = False


def load_model():
    """在后台线程中加载模型"""
    global _embedder, _model_ready
    try:
        from text2vec import SentenceModel
        logger.info(f"加载向量模型: {MODEL_NAME}（首次加载需下载，约 1-2 分钟）...")
        _embedder = SentenceModel(MODEL_NAME)
        _model_ready = True
        logger.info("模型加载完成，服务就绪")
    except Exception as e:
        logger.error(f"模型加载失败: {e}")
        raise


class EmbedRequest(BaseModel):
    texts: List[str]


class EmbedResponse(BaseModel):
    embeddings: List[List[float]]


@app.get("/health")
def health(response: Response):
    """模型加载完成后返回 200，否则返回 503"""
    if _model_ready:
        return {"status": "ok", "model": MODEL_NAME}
    response.status_code = 503
    return {"status": "loading", "model": MODEL_NAME}


@app.post("/embed", response_model=EmbedResponse)
def embed(req: EmbedRequest):
    if not _model_ready:
        return Response(
            content='{"detail":"模型正在加载中，请稍后重试"}',
            status_code=503,
            media_type="application/json",
        )
    vectors = _embedder.encode(req.texts)
    if hasattr(vectors, "tolist"):
        vectors = vectors.tolist()
    return {"embeddings": vectors}


@app.on_event("startup")
def startup():
    """启动后台线程加载模型，不阻塞 FastAPI 启动"""
    thread = threading.Thread(target=load_model, daemon=True)
    thread.start()

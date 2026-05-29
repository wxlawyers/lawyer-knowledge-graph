"""
向量检索脚本

将文本向量化并在pgvector中执行相似度检索。
可独立运行：python vector_search.py --query "买卖合同违约金" --top-k 5
"""
import argparse
import json
import os
import sys

try:
    import requests
except ImportError:
    print("请先安装 requests: pip install requests")
    sys.exit(1)

try:
    import psycopg2
except ImportError:
    print("请先安装 psycopg2: pip install psycopg2-binary")
    sys.exit(1)

try:
    import psycopg2.extras
except ImportError:
    pass


VECTOR_API_URL = os.getenv("VECTOR_API_URL", "http://localhost:9998")
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/lawkg")
VECTOR_DIM = 1024


def get_embedding(text: str) -> list:
    """调用本地向量模型获取文本embedding"""
    resp = requests.post(
        f"{VECTOR_API_URL}/embed",
        json={"texts": [text]},
        timeout=30
    )
    if resp.status_code == 200:
        return resp.json()["embeddings"][0]
    else:
        raise RuntimeError(f"向量化失败: {resp.status_code}")


def search_similar(query: str, top_k: int = 10, min_similarity: float = 0.6) -> list:
    """在pgvector中检索相似案件"""
    embedding = get_embedding(query)
    embedding_str = "[" + ",".join(str(x) for x in embedding) + "]"

    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

    cur.execute("""
        SELECT 
            kc.id,
            kc.title,
            kc.content,
            kc.card_type,
            c.case_number,
            c.case_type,
            1 - (kc.embedding <=> %s::vector) AS similarity
        FROM knowledge_cards kc
        LEFT JOIN cases c ON kc.case_id = c.id
        WHERE 1 - (kc.embedding <=> %s::vector) > %s
        ORDER BY kc.embedding <=> %s::vector
        LIMIT %s
    """, (embedding_str, embedding_str, min_similarity, embedding_str, top_k))

    results = [dict(row) for row in cur.fetchall()]
    cur.close()
    conn.close()

    return results


def main():
    parser = argparse.ArgumentParser(description="向量相似度检索")
    parser.add_argument("--query", "-q", help="查询文本")
    parser.add_argument("--top-k", "-k", type=int, default=10, help="返回结果数")
    parser.add_argument("--min-sim", type=float, default=0.6, help="最低相似度阈值")

    args = parser.parse_args()

    if not args.query:
        parser.print_help()
        print("\n错误：请通过 --query 提供查询文本")
        sys.exit(1)

    print(f"正在检索相似案件（查询：{args.query[:50]}...）...")
    results = search_similar(args.query, args.top_k, args.min_sim)

    if not results:
        print("未找到匹配结果")
        return

    print(f"\n找到 {len(results)} 个匹配结果：\n")
    for i, r in enumerate(results, 1):
        print(f"[{i}] 相似度: {r['similarity']:.3f} | {r['card_type']} | {r['title']}")
        print(f"    案号: {r.get('case_number', 'N/A')} | 案由: {r.get('case_type', 'N/A')}")
        print(f"    内容: {r['content'][:150]}...")
        print()


if __name__ == "__main__":
    main()

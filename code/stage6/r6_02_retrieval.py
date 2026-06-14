"""
R6-02 Embedding 与检索。

运行：
    python code/stage6/r6_02_retrieval.py

任务：
    1. 先用关键词重叠模拟检索。
    2. 返回最相关片段。
    3. 后续替换为 embedding/vector search。
"""

from r6_01_chunking import chunk_text


def score(query, chunk):
    query_terms = set(query.lower().split())
    chunk_terms = set(chunk.lower().split())
    return len(query_terms & chunk_terms)


def retrieve(query, chunks, top_k=3):
    ranked = sorted(chunks, key=lambda chunk: score(query, chunk), reverse=True)
    return ranked[:top_k]


def main():
    text = "Python reads files. RAG retrieves chunks. Agents use tools. Memory stores records."
    chunks = chunk_text(text, chunk_size=40, overlap=5)
    query = input("query: ").strip() or "RAG chunks"
    print(retrieve(query, chunks))
    print("TODO：把 score() 替换为 embedding 相似度。")


if __name__ == "__main__":
    main()

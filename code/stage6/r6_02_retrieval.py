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
    """给 query 和 chunk 算一个相关度分数（先用关键词重叠数量，后续换成 embedding 相似度）。"""
    # TODO
    raise NotImplementedError("R6-02：实现 score")


def retrieve(query, chunks, top_k=3):
    """按 score 从高到低排序 chunks，返回前 top_k 个。"""
    # TODO
    raise NotImplementedError("R6-02：实现 retrieve")


def main():
    """准备文本 -> chunk_text 切分 -> 读 query -> retrieve 打印最相关片段。"""
    # TODO
    raise NotImplementedError("R6-02：实现 main")


if __name__ == "__main__":
    main()

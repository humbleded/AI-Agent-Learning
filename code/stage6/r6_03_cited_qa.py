"""
R6-03 带引用问答。

运行：
    python code/stage6/r6_03_cited_qa.py

任务：
    1. 检索相关片段。
    2. 回答时带引用编号。
    3. 资料里没有答案时拒答。
"""

from r6_02_retrieval import retrieve


DOCS = [
    {"id": "doc1", "text": "RAG 通过检索外部资料来减少模型幻觉。"},
    {"id": "doc2", "text": "引用可以帮助用户检查答案来源。"},
    {"id": "doc3", "text": "资料没有答案时，系统应该说明不知道。"},
]


def answer_with_citations(question):
    """检索 DOCS 回答问题并带引用编号；资料里没依据就拒答。

    步骤：
      1. 取出 DOCS 的文本，用 retrieve 拿到最相关片段。
      2. 命中为空或都对不上问题 -> 返回「没有足够依据」。
      3. 找到命中片段对应的 doc id 作为引用，拼成「回答 + 引用」。
    """
    # TODO
    raise NotImplementedError("R6-03：实现 answer_with_citations")


def main():
    """读问题 -> answer_with_citations -> 打印。"""
    # TODO
    raise NotImplementedError("R6-03：实现 main")


if __name__ == "__main__":
    main()

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
    chunks = [doc["text"] for doc in DOCS]
    hits = retrieve(question, chunks, top_k=2)
    if not hits or all(question not in hit for hit in hits):
        return "资料中没有足够依据回答这个问题。"
    citations = [doc["id"] for doc in DOCS if doc["text"] in hits]
    return f"回答：{hits[0]}\n引用：{citations}"


def main():
    question = input("问题：").strip()
    print(answer_with_citations(question))


if __name__ == "__main__":
    main()

"""
R6-Gate 个人知识库问答。

运行：
    python code/stage6/r6_gate_personal_kb.py

任务：
    1. 导入至少 3 篇资料。
    2. 支持问答、引用、无答案拒答。
    3. 当前脚手架从 resources/stage6/*.txt 读取资料。
"""

from pathlib import Path

from r6_02_retrieval import retrieve


ROOT = Path(__file__).resolve().parents[2]
DOC_DIR = ROOT / "resources" / "stage6"


def load_docs():
    DOC_DIR.mkdir(parents=True, exist_ok=True)
    docs = []
    for path in DOC_DIR.glob("*.txt"):
        docs.append({"id": path.name, "text": path.read_text(encoding="utf-8", errors="replace")})
    if not docs:
        sample = DOC_DIR / "sample1.txt"
        sample.write_text("RAG 需要文档切分、检索和带引用回答。", encoding="utf-8")
        docs = [{"id": sample.name, "text": sample.read_text(encoding="utf-8")}]
    return docs


def answer(question, docs):
    chunks = [doc["text"] for doc in docs]
    hits = retrieve(question, chunks, top_k=3)
    if not hits:
        return "资料中没有答案。"
    cited = [doc["id"] for doc in docs if doc["text"] in hits]
    return f"根据资料回答：{hits[0]}\n引用：{cited}"


def main():
    docs = load_docs()
    question = input("问题：").strip()
    print(answer(question, docs))


if __name__ == "__main__":
    main()

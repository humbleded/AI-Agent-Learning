"""
R6-01 文档读取与切分。

运行：
    python code/stage6/r6_01_chunking.py

任务：
    1. 读取一段文本。
    2. 按 chunk_size 切分。
    3. 支持 overlap。
    4. 打印每个 chunk 的编号和内容。
"""


def chunk_text(text, chunk_size=120, overlap=20):
    if chunk_size <= 0:
        raise ValueError("chunk_size 必须大于 0")
    if overlap >= chunk_size:
        raise ValueError("overlap 必须小于 chunk_size")

    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start = end - overlap
    return chunks


def main():
    text = input("文档文本：").strip() or "这是一段用于 RAG 切分练习的示例文本。" * 20
    for index, chunk in enumerate(chunk_text(text), start=1):
        print(f"[chunk {index}] {chunk}")


if __name__ == "__main__":
    main()

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
    """把 text 按 chunk_size 切片，相邻片重叠 overlap 个字符，返回片段列表。

    步骤：
      1. 参数校验：chunk_size > 0，overlap < chunk_size，否则 raise ValueError。
      2. 用滑动窗口从 start 切到 start+chunk_size，每次前进 chunk_size-overlap。
      3. 收集所有片段返回。
    """
    # TODO
    raise NotImplementedError("R6-01：实现 chunk_text")


def main():
    """读一段文本（或用默认示例）-> chunk_text 切分 -> 逐个打印编号和内容。"""
    # TODO
    raise NotImplementedError("R6-01：实现 main")


if __name__ == "__main__":
    main()

"""
PR2-02 摘要与改写。

运行：
    python code/stage2/pr2_02_summarizer.py

任务：
    1. 输入一段长文。
    2. 输出 3 条要点。
    3. 输出 1 段摘要。
    4. 后续可替换为模型调用。
"""


def simple_summarize(text):
    """把长文切成句子，取前 3 句做要点，再拼成一段摘要，返回 (points, summary)。

    步骤：
      1. 把 text 按句号/句点切成句子列表，去掉空白句。
      2. points = 前 3 句。
      3. summary = 用「；」把这几条要点连起来。
    """
    # TODO
    raise NotImplementedError("PR2-02：实现 simple_summarize")


def main():
    """读入一段长文，打印 3 条要点 + 1 段摘要；空输入给提示。"""
    # TODO
    raise NotImplementedError("PR2-02：实现 main")


if __name__ == "__main__":
    main()

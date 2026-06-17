"""
G8-03 文档分析 Agent。

运行：
    python code/stage8/g8_03_document_analysis_agent.py

任务：
    1. state 中保存 document、summary、trace、steps。
    2. 条件边决定是否继续。
    3. 设置最大步数，防止无限执行。
"""


MAX_STEPS = 3


def read_document(state):
    """节点：记 "read_document"，确保 state 有 document，返回 state。"""
    # TODO
    raise NotImplementedError("G8-03：实现 read_document")


def summarize(state):
    """节点：记 "summarize"，根据 document 生成 summary，返回 state。"""
    # TODO
    raise NotImplementedError("G8-03：实现 summarize")


def should_continue(state):
    """条件边：根据 trace 步数（< MAX_STEPS）和是否已有 summary，决定是否继续。"""
    # TODO
    raise NotImplementedError("G8-03：实现 should_continue")


def run_agent(document):
    """初始化 state -> read_document -> 按 should_continue 决定流程 -> summarize，返回 state。"""
    # TODO
    raise NotImplementedError("G8-03：实现 run_agent")


if __name__ == "__main__":
    print(run_agent(input("document: ")))

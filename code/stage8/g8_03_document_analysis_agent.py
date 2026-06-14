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
    state["trace"].append("read_document")
    state["document"] = state.get("document") or "示例文档：Agent 可以调用工具并记录状态。"
    return state


def summarize(state):
    state["trace"].append("summarize")
    state["summary"] = state["document"][:50]
    return state


def should_continue(state):
    return len(state["trace"]) < MAX_STEPS and not state.get("summary")


def run_agent(document):
    state = {"document": document, "trace": []}
    state = read_document(state)
    if should_continue(state):
        state = summarize(state)
    else:
        state = summarize(state)
    return state


if __name__ == "__main__":
    print(run_agent(input("document: ")))

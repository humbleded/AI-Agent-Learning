"""
G8-Gate Research Graph。

运行：
    python code/stage8/g8_gate_research_graph.py

任务：
    1. 输入主题。
    2. 检索/整理/生成报告。
    3. 输出可追踪 trace。
"""


def retrieve(state):
    state["trace"].append("retrieve")
    state["sources"] = [f"{state['topic']} source 1", f"{state['topic']} source 2"]
    return state


def organize(state):
    state["trace"].append("organize")
    state["outline"] = ["背景", "要点", "结论"]
    return state


def write_report(state):
    state["trace"].append("write_report")
    state["report"] = f"# {state['topic']}\n\n- 背景\n- 要点\n- 结论"
    return state


def run(topic):
    state = {"topic": topic, "trace": []}
    for node in [retrieve, organize, write_report]:
        state = node(state)
    return state


if __name__ == "__main__":
    print(run(input("topic: ")))

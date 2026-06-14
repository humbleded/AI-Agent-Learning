"""
G8-02 第一个 Graph。

运行：
    python code/stage8/g8_02_first_graph.py

任务：
    1. 理解 node、edge、state。
    2. 当前用普通 Python 模拟图执行。
    3. 后续替换为 LangGraph StateGraph。
"""


def node_collect(state):
    state["trace"].append("collect")
    state["topic"] = state.get("topic") or "LangGraph"
    return state


def node_write(state):
    state["trace"].append("write")
    state["answer"] = f"报告主题：{state['topic']}"
    return state


def run_graph(initial_state):
    state = node_collect(initial_state)
    state = node_write(state)
    return state


if __name__ == "__main__":
    result = run_graph({"topic": input("topic: "), "trace": []})
    print(result)

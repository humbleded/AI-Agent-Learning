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
    """图节点：在 state["trace"] 里记一笔 "collect"，确保 state 有 topic，返回 state。"""
    # TODO
    raise NotImplementedError("G8-02：实现 node_collect")


def node_write(state):
    """图节点：记一笔 "write"，根据 topic 生成 state["answer"]，返回 state。"""
    # TODO
    raise NotImplementedError("G8-02：实现 node_write")


def run_graph(initial_state):
    """依次跑 node_collect -> node_write，返回最终 state（后续换成 LangGraph StateGraph）。"""
    # TODO
    raise NotImplementedError("G8-02：实现 run_graph")


if __name__ == "__main__":
    result = run_graph({"topic": input("topic: "), "trace": []})
    print(result)

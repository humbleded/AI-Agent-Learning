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
    """节点：记 "retrieve"，根据 topic 生成 sources，返回 state。"""
    # TODO
    raise NotImplementedError("G8-Gate：实现 retrieve")


def organize(state):
    """节点：记 "organize"，生成 outline，返回 state。"""
    # TODO
    raise NotImplementedError("G8-Gate：实现 organize")


def write_report(state):
    """节点：记 "write_report"，根据 topic/outline 生成 report，返回 state。"""
    # TODO
    raise NotImplementedError("G8-Gate：实现 write_report")


def run(topic):
    """初始化 state -> 依次跑 retrieve/organize/write_report -> 返回带 trace 的 state。"""
    # TODO
    raise NotImplementedError("G8-Gate：实现 run")


if __name__ == "__main__":
    print(run(input("topic: ")))

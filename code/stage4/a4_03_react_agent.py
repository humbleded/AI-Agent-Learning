"""
A4-03 ReAct Agent。

运行：
    python code/stage4/a4_03_react_agent.py

任务：
    1. 展示 Thought/Action/Observation。
    2. 至少调用一个工具。
    3. 设置 max_steps，防止无限循环。
"""


def search_tool(query):
    """模拟一个搜索工具：给定 query 返回一段假的搜索结果文本。"""
    # TODO
    raise NotImplementedError("A4-03：实现 search_tool")


def react_loop(question, max_steps=3):
    """ReAct 循环：每步产出 Thought/Action/Observation，至少调用一次工具，受 max_steps 限制。

    返回 (trace, answer)：
      1. 循环最多 max_steps 步，每步记录 thought、action、observation。
      2. 需要工具时构造 action 并调用 search_tool，把结果作为 observation。
      3. 拿到足够信息就停；最后根据 observation 生成 answer。
    """
    # TODO
    raise NotImplementedError("A4-03：实现 react_loop")


def main():
    """读问题 -> react_loop -> 打印每步 Thought/Action/Observation 和最终答案。"""
    # TODO
    raise NotImplementedError("A4-03：实现 main")


if __name__ == "__main__":
    main()

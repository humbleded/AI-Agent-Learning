"""
FINAL-Gate 综合项目入口脚手架。

运行：
    python code/final_project/main.py

任务：
    1. 选择一个项目方向。
    2. 定义工具列表。
    3. 定义 Agent 循环。
    4. 准备至少 5 个测试样例。
"""


def agent_loop(user_goal):
    """综合项目的 Agent 循环：理解目标 -> 选工具 -> 产出答案，返回 {"answer", "trace"}。

    这是毕业项目，按你选的方向自己设计：
      1. 定义工具列表。
      2. 设计 Agent 循环（可复用前面阶段的 ReAct / Plan-Solve / 工具调用）。
      3. 记录可追踪的 trace。
    """
    # TODO
    raise NotImplementedError("FINAL-Gate：实现你的综合项目 Agent")


def main():
    """读项目目标/用户问题 -> agent_loop -> 打印结果。"""
    # TODO
    raise NotImplementedError("FINAL-Gate：实现 main")


if __name__ == "__main__":
    main()

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
    trace = [
        {"step": "understand_goal", "content": user_goal},
        {"step": "choose_tools", "content": ["TODO: search", "TODO: file_reader"]},
        {"step": "produce_answer", "content": "TODO: final answer"},
    ]
    return {"answer": "综合项目脚手架：请替换为你的真实 Agent。", "trace": trace}


def main():
    user_goal = input("项目目标或用户问题：").strip()
    result = agent_loop(user_goal)
    print(result)


if __name__ == "__main__":
    main()

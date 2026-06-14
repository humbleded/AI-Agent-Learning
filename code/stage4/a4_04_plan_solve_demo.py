"""
A4-04 Plan-and-Solve。

运行：
    python code/stage4/a4_04_plan_solve_demo.py

任务：
    1. 输入一个复杂任务。
    2. 输出计划。
    3. 逐步执行。
    4. 输出复盘。
"""


def make_plan(task):
    return [
        f"理解任务：{task}",
        "拆成 2-3 个子问题",
        "逐步执行并记录结果",
        "复盘哪里不确定",
    ]


def solve_step(step):
    return f"已执行：{step}"


def main():
    task = input("复杂任务：").strip()
    plan = make_plan(task)
    print("Plan:")
    for item in plan:
        print("-", item)
    print("Solve:")
    results = [solve_step(step) for step in plan]
    for result in results:
        print("-", result)
    print("Reflection: TODO：判断计划是否过度、是否遗漏关键步骤。")


if __name__ == "__main__":
    main()

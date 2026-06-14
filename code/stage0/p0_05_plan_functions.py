"""
P0-05 函数、参数、返回值。

运行：
    python code/stage0/p0_05_plan_functions.py

任务：
    1. 完成 make_plan(goal, days)，返回一个包含 days 条计划的 list。
    2. 完成 score_answer(answer)，根据回答长度和关键词返回分数。
    3. 在 main() 中调用两个函数，并打印返回值。

练习重点：
    函数用 return 把结果交给调用者，main() 决定如何 print。
"""


def make_plan(goal, days):
    """根据学习目标和天数生成计划列表。"""
    # TODO: 检查 days 是否为正整数。
    # TODO: 返回 list[str]，格式示例："第 1 天：学习 Python 函数 - 完成一个小练习"
    plan = []
    for day in range(1, days + 1):
        plan.append(f"第 {day} 天：围绕 {goal} 完成一个小练习")
    return plan


def score_answer(answer):
    """给一段问答作答打一个 0-100 的练习分。"""
    # TODO: 自己补充更合理的评分规则。
    if not answer.strip():
        return 0
    score = min(len(answer.strip()) * 2, 80)
    for keyword in ["因为", "所以", "例如", "区别", "返回"]:
        if keyword in answer:
            score += 4
    return min(score, 100)


def main():
    goal = input("学习目标：").strip() or "函数"
    days_text = input("计划天数：").strip() or "3"

    try:
        days = int(days_text)
    except ValueError:
        print("天数必须是整数。")
        return

    plan = make_plan(goal, days)
    print("\n学习计划：")
    for item in plan:
        print("-", item)

    answer = input("\n用一句话解释 return 和 print 的区别：")
    print("练习分：", score_answer(answer))


if __name__ == "__main__":
    main()

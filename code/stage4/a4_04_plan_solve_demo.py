"""A4-04：从零实现一个最小 Plan-and-Solve Agent。

最终运行方式（项目根目录）：
    .venv/Scripts/python.exe code/stage4/a4_04_plan_solve_demo.py

最终任务与通过标准：
    - 生成并输出结构化计划。
    - 按顺序执行计划并输出每一步结果。
    - 输出事实性复盘，包括计划规模、执行情况、异常与最终状态。

实现阶段状态：
    C1–C6 已完成；文件无需真实 API 即可直接运行，
    展示“计划 → 执行结果 → 复盘 → 最终返回值”的完整闭环。
"""

import ast
from collections.abc import Callable


LLMCall = Callable[[str], str]
StepResult = tuple[str, str]


def parse_plan(response_text: str) -> list[str]:
    """解析 `````python`` 代码围栏中的字符串列表；格式无效时返回 ``[]``。"""
    # C1：提取、解析并验证 Planner 返回的计划。
    try:
        # 提取 ```python ... ``` 代码围栏中的内容
        plan_str = response_text.split("```python")[1].split("```")[0].strip()
        # 使用 ast.literal_eval 安全解析为 Python 对象
        parsed: list[str] = ast.literal_eval(plan_str)
        # 验证解析结果是列表且每个元素是字符串
        if isinstance(parsed, list) and all(isinstance(item, str) for item in parsed):
            return parsed
    except (ValueError, SyntaxError, IndexError):
        pass
    return []


def create_plan(question: str, llm_call: LLMCall) -> list[str]:
    """调用 Planner 一次，并把模型文本解析为结构化计划。"""
    # C2：构造规划提示词、调用 llm_call，再复用 parse_plan。
    prompt = f"请为以下问题生成一个结构化计划，返回一个 Python 列表，只拆解执行步骤，不直接解决或回答原问题，防止计划中提前混入答案。要求格式为 ```python ['步骤1', '步骤2', ...] ```,前后都不能有多余的文本。\n\nquestion:{question}"
    response_text = llm_call(prompt)
    return parse_plan(response_text)


def execute_plan(
    question: str,
    plan: list[str],
    llm_call: LLMCall,
) -> list[StepResult]:
    """按顺序执行计划，并返回每个 ``(step, result)``。"""
    # C3：为每一步构造上下文、调用 llm_call，并累积全部结果。
    results: list[StepResult] = []
    history: list[StepResult] = []
    for step in plan:
        context = f"""原始问题：{question}
完整计划：{plan}
历史结果：{history}
当前步骤：{step}"""
        result = llm_call(context)
        if result is None:
            result = ""
        results.append((step, result))
        history.append((step,result))
    return results


def build_recap(plan: list[str], results: list[StepResult]) -> str:
    """根据计划和执行结果生成事实性复盘。"""
    # C4：区分空计划、完整执行与部分执行，并生成字段语义清楚的事实总结。
    total_steps = len(plan)
    attempted_steps = len(results)

    # 去掉结果两边的空白，避免把 "   " 判断为成功。
    normalized_results = [
        (step, result.strip())
        for step, result in results
    ]

    failed_steps = [
        step
        for step, result in normalized_results
        if not result
    ]

    # 只统计从第一步开始连续成功的步骤。
    # 一旦遇到失败，当前步骤以及后面的计划都视为未完成。
    completed_steps = 0
    for _, result in normalized_results[:total_steps]:
        if not result:
            break
        completed_steps += 1

    remaining_steps = plan[completed_steps:]

    if completed_steps > 0:
        last_successful_result = normalized_results[completed_steps - 1][1]
    else:
        last_successful_result = "无有效执行结果"

    def format_steps(steps: list[str]) -> str:
        return "、".join(steps) if steps else "无"

    # 情况一：没有生成有效计划。
    if total_steps == 0:
        return "\n".join([
            "执行类型：空计划",
            "计划规模：0 步",
            "已尝试：0 步",
            "已完成：0 步",
            "执行情况：未生成有效计划、未执行",
            "异常步骤：无",
            "异常说明：未生成有效计划",
            "最终结果：无执行结果",
            "最终状态：未完成",
        ])

    is_complete = (
        attempted_steps == total_steps
        and completed_steps == total_steps
        and not failed_steps
    )

    # 情况二：所有计划步骤都成功执行。
    if is_complete:
        final_result = normalized_results[-1][1]

        return "\n".join([
            "执行类型：完整执行",
            f"计划规模：{total_steps} 步",
            f"已尝试：{attempted_steps} 步",
            f"已完成：{completed_steps} 步",
            "执行情况：全部计划步骤均已执行",
            "异常步骤：无",
            "异常说明：无异常",
            f"最终结果：{final_result}",
            "最终状态：完成",
        ])

    # 情况三：执行失败或提前停止。
    completion_ratio = completed_steps / total_steps

    if failed_steps:
        exception_summary = (
            f"以下步骤执行结果为空：{format_steps(failed_steps)}"
        )
    elif attempted_steps < total_steps:
        exception_summary = "执行提前停止，尚有计划步骤未执行"
    else:
        exception_summary = "执行结果数量或状态与计划不一致"

    return "\n".join([
        "执行类型：部分执行",
        f"计划规模：{total_steps} 步",
        f"已尝试：{attempted_steps} 步",
        f"已完成：{completed_steps} 步",
        f"完成比例：{completion_ratio:.0%}",
        f"执行情况：已完成 {completed_steps}/{total_steps} 步",
        f"异常步骤：{format_steps(failed_steps)}",
        f"剩余步骤：{format_steps(remaining_steps)}",
        f"异常说明：{exception_summary}",
        f"最终结果：任务未完成；最后有效结果：{last_successful_result}",
        "最终状态：未完成",
    ])


def run_plan_and_solve(
    question: str,
    llm_call: LLMCall,
) -> str | None:
    """串联规划、执行和复盘，打印完整轨迹并返回最终结果。"""
    # C5：输出计划、逐步执行结果和复盘；空计划时安全结束。
    plan = create_plan(question, llm_call)
    print("生成的计划：", plan)

    if not plan:
        recap = build_recap(plan, [])
        print("复盘：\n", recap)
        return None

    results = execute_plan(question, plan, llm_call)
    for step, result in results:
        print(f"步骤：{step}\n结果：{result}\n")

    recap = build_recap(plan, results)
    print("复盘：\n", recap)

    return results[-1][1] if results else None


def demo_llm(prompt: str) -> str:
    """根据提示词返回固定规划或固定步骤结果，供本地演示使用。"""
    # C6：区分 Planner 与各执行步骤，返回可重复的非空文本。
    if "请为以下问题生成一个结构化计划" in prompt:
        # 返回固定计划
        return "```python ['计算周一的平均温度', '计算周二的平均温度', '计算周三的平均温度'] ```"
    elif "当前步骤：计算周一的平均温度" in prompt:
        return "周一的温度是 20°C,平均温度是 20°C"
    elif "当前步骤：计算周二的平均温度" in prompt:
        return "周二的温度是 22°C,平均温度是 21°C"
    elif "当前步骤：计算周三的平均温度" in prompt:
        return "周三的温度是 24°C,平均温度是 22°C"
    return "没找到对应的步骤结果"


if __name__ == "__main__":
    # C6：直接运行时展示完整轨迹，并打印调用方收到的最终答案。
    question = "计算周一到周三中的平均温度"
    final_result = run_plan_and_solve(question, demo_llm)
    print("最终答案：", final_result)

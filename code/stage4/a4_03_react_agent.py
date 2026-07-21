"""A4-03：从零实现一个最小 ReAct Agent。

最终运行方式（项目根目录）：
    .venv/Scripts/python.exe code/stage4/a4_03_react_agent.py

最终任务与通过标准：
    - 展示 Thought -> Action -> Observation -> 下一轮 Thought/Finish 的完整轨迹。
    - 用最大步数保证循环能够稳定停止。

已完成代码检查点 C1–C5：
    ``run_react`` 能展示完整轨迹并受 ``max_steps`` 限制。
    直接运行本文件会执行一个可重复的两轮 ReAct 演示。
"""

import re
from collections.abc import Callable


SAMPLE_OUTPUT = """Thought: 我需要查询实时天气。
Action: Weather[Singapore]"""

REACT_PROMPT_TEMPLATE = """你是一个可以调用外部工具的助手。

可用工具：
{tools}

请严格输出：
Thought: 当前判断
Action: ToolName[input] 或 Finish[最终答案]

Question: {question}
History:
{history}
"""

TOOLS_DESCRIPTION = "- Weather: 查询指定城市的实时天气和空气质量，输入为城市名。"
WEATHER_DATA = {"Singapore": "34°C, AQI=160"}

LLMCall = Callable[[str], str]
ToolFunction = Callable[[str], str]


def weather_tool(city: str) -> str:
    """提供可重复运行的本地天气结果；本任务重点是 ReAct 控制循环。"""
    normalized_city = city.strip()
    return WEATHER_DATA.get(normalized_city, f"没有找到 {normalized_city} 的天气数据。")


TOOLS: dict[str, ToolFunction] = {"Weather": weather_tool}


def parse_llm_output(text: str) -> tuple[str | None, str | None]:
    """返回 ``(thought, action)``；缺少对应字段时返回 ``None``。"""
    thought_pattern = r"^Thought:\s*(.*?)\s*(?=^Action:|\Z)"
    action_pattern = r"^Action:\s*(.*)"
    thought_match = re.search(thought_pattern, text, re.MULTILINE | re.DOTALL)
    action_match = re.search(action_pattern, text, re.MULTILINE | re.DOTALL)
    thought = thought_match.group(1).strip() if thought_match else None
    action = action_match.group(1).strip() if action_match else None
    return thought, action


def parse_action(action: str) -> tuple[str | None, str | None]:
    """把 ``Tool[input]`` 返回为 ``(tool_name, tool_input)``。"""
    pattern = r"(\w+)\[(.*)\]"
    match = re.fullmatch(pattern,action,re.DOTALL)
    if match:
        tool_name = match.group(1)
        tool_input = match.group(2)
        return tool_name, tool_input
    else:
        return None, None


def build_prompt(question: str, tools_description: str, history: list[str]) -> str:
    """构造一轮 LLM 输入；不修改传入的 ``history``。"""
    history_str = "\n".join(history)  # 将历史记录列表连接为字符串
    prompt = REACT_PROMPT_TEMPLATE.format(tools=tools_description, question=question, history=history_str)
    return prompt


def run_react(question: str, llm_call: LLMCall, max_steps: int = 3) -> str | None:
    """运行 ReAct，打印每步轨迹；Finish 时返回答案，耗尽步数时返回 None。"""
    history = []

    for step in range(1, max_steps+1):
        print(f"\n--- 第 {step} 步 ---")

        prompt = build_prompt(
            question=question,
            tools_description=TOOLS_DESCRIPTION,
            history=history,
        )
        response_text = llm_call(prompt)
        thought, action = parse_llm_output(response_text)

        if thought:
            print(f"Thought: {thought}")

        if not action:
            print("未解析到 Action，流程停止。")
            return None

        tool_name, tool_input = parse_action(action)

        if tool_name == "Finish" and tool_input:
            print(f"Final Answer: {tool_input}")
            return tool_input

        if not tool_name or not tool_input:
            observation = "无效的 Action 格式。"
        else:
            tool_function = TOOLS.get(tool_name)

            if tool_function:
                observation = tool_function(tool_input)
            else:
                observation = f"未找到工具：{tool_name}"

        print(f"Action: {action}")
        print(f"Observation: {observation}")
        history.append(f"Action: {action}")
        history.append(f"Observation: {observation}")
    # 耗尽步数时打印原因并稳定返回 None。
    print("已达到最大步数，流程结束。")
    return None


def demo_llm(prompt: str) -> str:
    """根据历史中是否已有天气 Observation，返回可重复的两轮演示响应。"""
    if "Observation: 34°C, AQI=160" in prompt:
        return "Thought: 我已经得到了天气信息。\nAction: Finish[新加坡的实时天气是 34°C，空气质量指数为 160。]"
    else:
        return "Thought: 我需要查询实时天气。\nAction: Weather[Singapore]"


if __name__ == "__main__":
    run_react(
        question="新加坡今天的天气如何？",
        llm_call=demo_llm,
        max_steps=3,
    )

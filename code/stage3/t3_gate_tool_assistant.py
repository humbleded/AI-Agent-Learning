"""
T3-Gate Tool Calling 闯关：三工具助手。

运行：
    python code/stage3/t3_gate_tool_assistant.py

任务：
    1. 注册计算器、读文件、外部 API 三个工具。
    2. 用简单规则模拟 Agent 选择工具。
    3. 打印工具名、参数、结果。
    4. 后续再替换成模型 tool calling。
"""

from t3_02_calculator_tool import calculator_tool
from t3_03_file_reader_tool import read_sandbox_file
from t3_04_public_api_tool import public_api_tool


TOOLS = {
    "calculator": calculator_tool,
    "read_file": read_sandbox_file,
    "public_api": public_api_tool,
}


def choose_tool(user_text):
    """用简单规则模拟 Agent 选工具：返回 (tool_name, args)；没合适的返回 (None, {})。

    步骤：根据 user_text 里的关键词决定用 read_file / public_api / calculator，
    并给出对应的参数 dict（后续再替换成模型 tool calling）。
    """
    # TODO
    raise NotImplementedError("T3-Gate：实现 choose_tool")


def main():
    """读用户问题 -> choose_tool 选工具 -> 用 TOOLS[name](**args) 执行 -> 打印 tool/args/result。"""
    # TODO
    raise NotImplementedError("T3-Gate：实现 main")


if __name__ == "__main__":
    main()

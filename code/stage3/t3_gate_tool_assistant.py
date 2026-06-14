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
    if "读文件" in user_text:
        return "read_file", {"relative_path": "sample.txt"}
    if "api" in user_text.lower():
        return "public_api", {}
    if any(word in user_text for word in ["计算", "+", "-", "*", "/"]):
        return "calculator", {"operation": "add", "a": 1, "b": 2}
    return None, {}


def main():
    user_text = input("用户问题：")
    tool_name, args = choose_tool(user_text)
    if not tool_name:
        print("没有选择工具。TODO：让模型决定是否调用工具。")
        return
    result = TOOLS[tool_name](**args)
    print("tool:", tool_name)
    print("args:", args)
    print("result:", result)


if __name__ == "__main__":
    main()

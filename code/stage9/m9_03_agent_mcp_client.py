"""
M9-03 Agent 调 MCP。

运行：
    python code/stage9/m9_03_agent_mcp_client.py

任务：
    1. 发现 MCP server 工具。
    2. 选择一个工具。
    3. 调用工具并把结果反馈给 Agent。
"""

from m9_02_local_mcp_server import call_tool, list_tools


def agent_decide_tool(user_text):
    if "长度" in user_text:
        return "count_chars", {"text": user_text}
    return "echo", {"text": user_text}


def main():
    print("发现工具：", list_tools())
    user_text = input("用户：")
    tool_name, args = agent_decide_tool(user_text)
    result = call_tool(tool_name, args)
    print("tool:", tool_name)
    print("result:", result)


if __name__ == "__main__":
    main()

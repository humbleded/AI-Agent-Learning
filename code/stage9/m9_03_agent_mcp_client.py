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
    """模拟 Agent 选工具：根据 user_text 返回 (tool_name, arguments)。"""
    # TODO
    raise NotImplementedError("M9-03：实现 agent_decide_tool")


def main():
    """打印发现的工具 -> 读用户输入 -> agent_decide_tool 选工具 -> call_tool 执行 -> 打印结果。"""
    # TODO
    raise NotImplementedError("M9-03：实现 main")


if __name__ == "__main__":
    main()

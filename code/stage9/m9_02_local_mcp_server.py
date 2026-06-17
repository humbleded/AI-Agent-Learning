"""
M9-02 本地 MCP Server。

运行：
    python code/stage9/m9_02_local_mcp_server.py

任务：
    1. 暴露 1-2 个安全工具。
    2. 支持工具发现。
    3. 记录工具调用日志。

说明：
    当前是 MCP 概念模拟版，后续再替换为真实 MCP SDK。
"""


TOOLS = {
    "echo": {"description": "返回输入文本"},
    "count_chars": {"description": "统计文本长度"},
}


def list_tools():
    """工具发现：返回 TOOLS（让客户端知道有哪些工具）。"""
    # TODO
    raise NotImplementedError("M9-02：实现 list_tools")


def call_tool(name, arguments):
    """根据 name 执行对应工具并返回结果；未知工具返回 {"error": "unknown tool"}。"""
    # TODO
    raise NotImplementedError("M9-02：实现 call_tool")


if __name__ == "__main__":
    print("tools:", list_tools())
    print("call:", call_tool("count_chars", {"text": "hello"}))

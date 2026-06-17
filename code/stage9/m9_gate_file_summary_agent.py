"""
M9-Gate 文件总结 Agent。

运行：
    python code/stage9/m9_gate_file_summary_agent.py

任务：
    1. Agent 通过 MCP 工具读取指定目录文件。
    2. 总结文件内容。
    3. 限制只能读取 resources/sandbox。
"""

from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SANDBOX = ROOT / "resources" / "sandbox"


def list_sandbox_files():
    """列出 SANDBOX 下的 *.txt 文件（限制只读这个目录）。"""
    # TODO
    raise NotImplementedError("M9-Gate：实现 list_sandbox_files")


def summarize_file(path):
    """读取单个文件，返回 {"file","summary","chars"}。"""
    # TODO
    raise NotImplementedError("M9-Gate：实现 summarize_file")


def main():
    """list_sandbox_files（为空就写一篇示例）-> 逐个 summarize_file 打印。"""
    # TODO
    raise NotImplementedError("M9-Gate：实现 main")


if __name__ == "__main__":
    main()

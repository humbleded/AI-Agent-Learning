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
    SANDBOX.mkdir(parents=True, exist_ok=True)
    return [path for path in SANDBOX.glob("*.txt")]


def summarize_file(path):
    text = path.read_text(encoding="utf-8", errors="replace")
    return {"file": path.name, "summary": text[:80], "chars": len(text)}


def main():
    files = list_sandbox_files()
    if not files:
        sample = SANDBOX / "sample.txt"
        sample.write_text("这是 MCP 文件总结 Agent 的示例资料。", encoding="utf-8")
        files = [sample]
    for path in files:
        print(summarize_file(path))


if __name__ == "__main__":
    main()

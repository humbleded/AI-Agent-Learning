"""
T3-03 文件工具。

运行：
    python code/stage3/t3_03_file_reader_tool.py sample.txt

任务：
    1. 只能读取 resources/sandbox/ 下的文件。
    2. 长文件只返回前 max_chars 个字符。
    3. 沙箱外路径必须拒绝。
"""

import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SANDBOX = ROOT / "resources" / "sandbox"


def read_sandbox_file(relative_path, max_chars=1000):
    SANDBOX.mkdir(parents=True, exist_ok=True)
    target = (SANDBOX / relative_path).resolve()
    sandbox_root = SANDBOX.resolve()
    if sandbox_root not in target.parents and target != sandbox_root:
        return {"ok": False, "error": "拒绝读取沙箱外文件"}
    if not target.exists() or not target.is_file():
        return {"ok": False, "error": "文件不存在"}
    text = target.read_text(encoding="utf-8", errors="replace")
    return {"ok": True, "content": text[:max_chars], "truncated": len(text) > max_chars}


def main():
    relative_path = sys.argv[1] if len(sys.argv) > 1 else input("sandbox file: ").strip()
    print(read_sandbox_file(relative_path))


if __name__ == "__main__":
    main()

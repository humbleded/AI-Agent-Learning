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
    """只允许读取 SANDBOX 目录下的文件，超长只返回前 max_chars 个字符。

    步骤：
      1. 确保 SANDBOX 存在。
      2. 解析目标路径（resolve），判断它是否在 SANDBOX 之内；不在 -> 拒绝读取。
      3. 文件不存在/不是文件 -> 返回错误。
      4. 读取文本，返回 {"ok": True, "content": 前 max_chars, "truncated": 是否被截断}。
    """
    SANDBOX.mkdir(parents=True, exist_ok=True)
    target = (SANDBOX / relative_path).resolve()
    try:
        target.relative_to(SANDBOX)
    except ValueError:
        return {"ok": False, "error": "文件在沙箱外，访问被拒绝"}
    if not target.exists():
        return {"ok": False, "error": "文件不存在"}
    if not target.is_file():
        return {"ok": False, "error": "不是文件"}
    text = target.read_text(encoding="utf-8")
    content = text[:max_chars]
    truncated = len(text) > max_chars
    return {"ok": True, "content": content, "truncated": truncated}


def main():
    """从命令行参数或 input 取相对路径 -> 打印 read_sandbox_file 结果。"""
    if len(sys.argv) > 1:
        relative_path = sys.argv[1]
    else:
        relative_path = input("请输入文件名：")
    result = read_sandbox_file(relative_path)
    print(result)


if __name__ == "__main__":
    main()

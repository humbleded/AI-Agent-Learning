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
    # TODO（注意防越权读取：先 resolve 再判断是否在沙箱内）
    raise NotImplementedError("T3-03：实现 read_sandbox_file")


def main():
    """从命令行参数或 input 取相对路径 -> 打印 read_sandbox_file 结果。"""
    # TODO
    raise NotImplementedError("T3-03：实现 main")


if __name__ == "__main__":
    main()

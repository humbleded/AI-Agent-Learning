"""
P0-06 模块、第三方包、venv。

运行：
    python code/stage0/p0_06_env_check.py

任务：
    1. 建立并激活 venv。
    2. 安装 python-dotenv 和 requests。
    3. 在项目根目录创建 .env，写入 TEST_VARIABLE=hello_stage0。
    4. 运行本文件，确认能读取环境变量。
"""

import os
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
ENV_PATH = ROOT / ".env"


def load_dotenv_if_available():
    """优先使用 python-dotenv；没安装时给出清晰提示。"""
    try:
        from dotenv import load_dotenv
    except ImportError:
        print("未安装 python-dotenv：请先运行 pip install python-dotenv")
        return False

    load_dotenv(ENV_PATH)
    return True


def main():
    load_dotenv_if_available()
    value = os.getenv("TEST_VARIABLE")

    print("项目根目录：", ROOT)
    print(".env 是否存在：", ENV_PATH.exists())
    print("TEST_VARIABLE：", value)

    if not value:
        print("TODO：在 .env 中写入 TEST_VARIABLE=hello_stage0 后再运行。")


if __name__ == "__main__":
    main()

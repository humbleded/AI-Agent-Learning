"""
第 4 天 - 输入校验和异常处理：让任务管理器不容易崩掉。

运行：
    python day04_validation.py

目标：
    处理错误输入、缺失文件、空任务名和损坏的 JSON。

通过标准：
    至少能清楚处理 3 种常见错误情况。
"""

import json
from pathlib import Path


TASKS_FILE = Path(__file__).with_name("tasks.json")


# ========== 今日任务 ==========
#
# 1. 把第 3 天的可运行版本复制到这个文件。
# 2. 拒绝空任务名。
# 3. 处理不存在的菜单选项。
# 4. 处理任务编号输入成字母的情况。
# 5. 处理任务编号越界的情况。
# 6. 处理缺失或损坏的 tasks.json。


# ========== 今日题目 ==========
#
# Q1：把 input 转成 int 时，哪一行可能触发 ValueError？
# 答：
#
# Q2：为什么不建议用一个巨大的 try/except 包住整个 main()？
# 答：
#
# Q3：如果 tasks.json 损坏，程序应该怎么处理？
# 答：


def load_tasks(file_path):
    # 待做：处理 FileNotFoundError，或者使用 Path.exists()
    # 待做：处理 json.JSONDecodeError
    pass


def save_tasks(file_path, tasks):
    pass


def get_task_index(tasks):
    """让用户输入 1-based 任务编号，返回 0-based index。"""
    # 待做：输入任务编号
    # 待做：转换成 int
    # 待做：检查范围
    # 待做：return index 或 None
    pass


def show_menu():
    pass


def add_task(tasks, name):
    # 待做：拒绝空任务名
    pass


def list_tasks(tasks):
    pass


def mark_done(tasks, index):
    pass


def delete_task(tasks, index):
    pass


def main():
    tasks = load_tasks(TASKS_FILE)

    # 待做：在这里写更安全的菜单循环


if __name__ == "__main__":
    main()

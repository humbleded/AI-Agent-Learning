"""
第 7 天 - 独立重写和周复盘。

运行：
    python day07_rewrite_review.py

目标：
    不看前几天文件，独立重写一个更小的版本。

通过标准：
    独立重写版可以新增任务、查看任务、保存任务和加载任务。
"""

import json
from pathlib import Path


TASKS_FILE = Path(__file__).with_name("tasks_rewrite.json")


# ========== 今日任务 ==========
#
# 1. 不要复制第 1-6 天的代码。
# 2. 只实现 4 个功能：新增、查看、保存、加载。
# 3. 保持代码尽量小。
# 4. 填写底部的 WEEKLY_REVIEW。


# ========== 今日题目 ==========
#
# Q1：不看第 3 天文件，你能写出 load_tasks() 吗？
# 答：
#
# Q2：你能用自己的话解释 return、print、self 和 json 吗？
# 答：
#
# Q3：进入 HTTP/API 学习前，你觉得哪一块还不稳？
# 答：


def load_tasks(file_path):
    # 待做：如果文件不存在或 JSON 不能解析，return []
    pass


def save_tasks(file_path, tasks):
    # 待做：把 tasks 保存成 JSON
    pass


def add_task(tasks, name):
    # 待做：新增一个任务
    pass


def list_tasks(tasks):
    # 待做：打印所有任务
    pass


def main():
    tasks = load_tasks(TASKS_FILE)

    # 待做：写一个最小菜单：
    # 1 新增
    # 2 查看
    # 3 退出


WEEKLY_REVIEW = """
1. 我这周最稳定掌握的概念是什么？

2. 我最容易混淆的是函数、文件 I/O、class 里的哪一块？

3. return、print、self、json 这四个词我分别怎么解释？

4. 下周进入 HTTP / API 前，我还缺什么？

5. 这个任务管理器如果继续升级，我会先加什么功能？

"""


if __name__ == "__main__":
    main()

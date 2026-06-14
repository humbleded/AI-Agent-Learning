"""
第 5 天 - 基础 OOP：把任务逻辑移动到 TaskManager 类里。

运行：
    python day05_oop.py

目标：
    理解 class、实例、属性、方法和 self。

通过标准：
    你能解释 self.tasks 和普通局部变量 tasks 的区别。
"""

import json
from pathlib import Path


TASKS_FILE = Path(__file__).with_name("tasks.json")


# ========== 今日任务 ==========
#
# 1. 创建 class TaskManager。
# 2. 把 file_path 和 tasks 放到 self.file_path 和 self.tasks。
# 3. 把 load、save、add、list、done、delete、find 逻辑移动到方法里。
# 4. input() 和菜单选择逻辑继续放在 main()。


# ========== 今日题目 ==========
#
# Q1：self 是什么？
# 答：
#
# Q2：为什么 TaskManager 应该持有 self.tasks？
# 答：
#
# Q3：哪些代码应该留在 class 外面？
# 答：


class TaskManager:
    def __init__(self, file_path):
        self.file_path = file_path
        self.tasks = []

    def load(self):
        # 待做：把 JSON 文件内容读取到 self.tasks
        pass

    def save(self):
        # 待做：把 self.tasks 保存到 self.file_path
        pass

    def add_task(self, name):
        # 待做：添加一个任务 dict
        pass

    def list_tasks(self):
        # 待做：打印所有任务
        pass

    def mark_done(self, index):
        # 待做：把一个任务标记为完成
        pass

    def delete_task(self, index):
        # 待做：删除一个任务
        pass

    def find_task(self, keyword):
        # 待做：return 匹配到的任务
        pass


def show_menu():
    pass


def get_task_index(manager):
    # 待做：让用户输入任务编号，return 0-based index 或 None
    pass


def main():
    manager = TaskManager(TASKS_FILE)
    manager.load()

    # 待做：写菜单循环，并调用 manager 的方法


if __name__ == "__main__":
    main()

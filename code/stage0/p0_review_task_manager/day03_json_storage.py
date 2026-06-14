"""
第 3 天 - JSON 存储：把任务保存到文件，下次运行还能读取。

运行：
    python day03_json_storage.py

目标：
    使用 json.load()、json.dump()、with open() 和文件存在性检查。

通过标准：
    关闭程序后重新运行，之前的任务仍然能看到。
"""

import json
from pathlib import Path


TASKS_FILE = Path(__file__).with_name("tasks.json")


# ========== 今日任务 ==========
#
# 1. 把第 2 天能运行的任务函数复制到这个文件。
# 2. 完成 load_tasks(file_path)。
# 3. 完成 save_tasks(file_path, tasks)。
# 4. main() 启动时先加载 tasks。
# 5. 新增、完成、删除任务后都保存 tasks。


# ========== 今日题目 ==========
#
# Q1：json.load() 是做什么的？
# 答：
#
# Q2：json.dump() 是做什么的？
# 答：
#
# Q3：如果 tasks.json 不存在，为什么 load_tasks() 应该 return []？
# 答：


def load_tasks(file_path):
    """从 JSON 文件读取任务；如果文件不存在，返回 []。"""
    # 待做：如果 file_path 不存在，return []
    # 待做：用 encoding="utf-8" 打开 file_path，并用 json.load() 读取
    pass


def save_tasks(file_path, tasks):
    """把任务保存到 JSON 文件。"""
    # 待做：用 encoding="utf-8" 以写入模式打开 file_path
    # 待做：使用 json.dump(tasks, file, ensure_ascii=False, indent=2)
    pass


def show_menu():
    pass


def add_task(tasks, name):
    pass


def list_tasks(tasks):
    pass


def mark_done(tasks, index):
    pass


def delete_task(tasks, index):
    pass


def main():
    tasks = load_tasks(TASKS_FILE)

    # 待做：复用第 2 天的菜单循环
    # 待做：每次修改任务后调用 save_tasks(TASKS_FILE, tasks)


if __name__ == "__main__":
    main()

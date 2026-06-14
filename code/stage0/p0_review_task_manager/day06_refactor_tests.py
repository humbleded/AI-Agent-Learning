"""
第 6 天 - 重构和手动测试：让 OOP 版本更清楚。

运行：
    python day06_refactor_tests.py

目标：
    改进命名，减少重复打印逻辑，并手动测试关键流程。

通过标准：
    你能解释数据流：用户输入 -> self.tasks -> JSON 文件。
"""

import json
from pathlib import Path


TASKS_FILE = Path(__file__).with_name("tasks.json")


# ========== 今日任务 ==========
#
# 1. 把第 5 天的可运行版本复制到这个文件。
# 2. 统一任务显示格式：1. [x] task name 或 1. [ ] task name。
# 3. 减少菜单循环里的重复代码。
# 4. 测试下面列出的 8 个手动场景。
# 5. 在 MANUAL_TEST_RESULTS 里填写每个场景的通过/失败记录。


MANUAL_TEST_CASES = [
    "新增一个任务",
    "查看任务列表",
    "把一个任务标记为完成",
    "删除一个任务",
    "按关键词搜索任务",
    "退出后重新运行，确认任务还能加载",
    "输入空任务名",
    "输入错误任务编号",
]


MANUAL_TEST_RESULTS = {
    # 示例：
    # "新增一个任务": "通过 - 任务出现在列表里",
}


# ========== 今日题目 ==========
#
# Q1：你代码里的哪一部分修改了 self.tasks？
# 答：
#
# Q2：你代码里的哪一部分把 self.tasks 保存进 JSON？
# 答：
#
# Q3：你今天移除了哪些重复代码？
# 答：


class TaskManager:
    # 待做：复制并改进第 5 天的 TaskManager
    pass


def show_menu():
    pass


def main():
    # 待做：复制并改进第 5 天的 main()
    pass


if __name__ == "__main__":
    main()

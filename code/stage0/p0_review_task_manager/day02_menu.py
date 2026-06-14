"""
第 2 天 - 命令行菜单：把任务函数串成一个可交互的小程序。

运行：
    python day02_menu.py

目标：
    使用 while、input()、if/elif、list 和 dict 做一个简单菜单。

通过标准：
    菜单可以新增任务、查看任务、标记完成、删除任务和退出程序。
"""


# ========== 今日任务 ==========
#
# 1. 每个任务用 dict 表示：{"name": "学习文件读写", "done": False}。
# 2. 完成 show_menu()。
# 3. 完成 add_task(tasks, name)。
# 4. 完成 list_tasks(tasks)。
# 5. 完成 mark_done(tasks, index)。
# 6. 完成 delete_task(tasks, index)。
# 7. 在 main() 里用 while True 循环菜单，用户输入 "5" 时退出。


# ========== 今日题目 ==========
#
# Q1：在这里，为什么一个任务用 dict 比只用字符串更合适？
# 答：可以同时存储任务的名称和完成状态，方便后续功能的实现，比如标记完成和删除任务。
#
# Q2：如果用户输入任务编号 100，程序可能出什么问题？
# 答：报错超出列表范围
#
# Q3：为什么菜单输入逻辑应该主要放在 main()，而不是分散到每个函数里？
# 答：放在 main() 中可以集中管理，避免逻辑分散，提高代码可读性和维护性。


def show_menu():
    # 待做：打印菜单选项：
    # 1 新增
    # 2 查看
    # 3 标记完成
    # 4 删除
    # 5 退出
    print(f"1 新增\n2 查看\n3 标记完成\n4 删除\n5 退出\n")
    pass


def add_task(tasks, name):
    # 待做：添加 {"name": name, "done": False}
    tasks.append({"name": name, "done": False})
    pass


def list_tasks(tasks):
    # 待做：逐个打印任务；完成显示 [x]，未完成显示 [ ]
    for i, task in enumerate(tasks, start=1):
        status = "[x]" if task["done"] else "[ ]"
        print(f"{i}. {status} {task['name']}")
    pass


def mark_done(tasks, index):
    # 待做：根据 index 把一个任务标记为完成
    # 注意：用户可能输入 1，但 Python list 的 index 从 0 开始。
    if 0 <= index - 1 < len(tasks):
        tasks[index - 1]["done"] = True
    pass


def delete_task(tasks, index):
    # 待做：根据 index 删除一个任务
    if 0 <= index - 1 < len(tasks):
        tasks.pop(index - 1)
    pass


def main():
    tasks = []

    while True:
        show_menu()
        choice = input("请选择：")

        # 待做：处理 1-5 的选择
        match choice:
            case "1":
                name = input("请输入任务名称：")
                add_task(tasks, name)
            case "2":
                list_tasks(tasks)
            case "3":
                index = int(input("请输入要标记完成的任务编号："))
                mark_done(tasks, index)
            case "4":
                index = int(input("请输入要删除的任务编号："))
                delete_task(tasks, index)
        # 今天先保持简单，完整输入校验放到第 4 天。
        if choice == "5":
            break


if __name__ == "__main__":
    main()

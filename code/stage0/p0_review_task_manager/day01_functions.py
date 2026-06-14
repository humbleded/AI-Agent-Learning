"""
第 1 天 - 函数拆分：把一个小任务脚本拆成多个函数。

运行：
    python day01_functions.py

目标：
    使用函数、参数和返回值管理一个简单任务列表。

通过标准：
    你能解释为什么 find_task() 应该 return 数据，而不是只 print。
"""


# ========== 今日任务 ==========
#
# 1. 完成 add_task(tasks, name)。
# 2. 完成 list_tasks(tasks)。
# 3. 完成 find_task(tasks, keyword)。
# 4. 在 main() 里创建一个空 list，并至少添加 3 个任务。
# 5. 搜索一个关键词，并打印匹配到的任务。


# ========== 今日题目 ==========
#
# Q1：print() 和 return 有什么区别？
# 答：print() 是一个函数，用于在控制台输出信息；
# return 是一个语句，用于从函数中返回一个值并结束函数的执行。
# print() 只是显示信息，而 return 可以将数据传递给调用者，使得函数的结果可以被其他代码使用。
#
# Q2：为什么 add_task(tasks, name) 要把 tasks 作为参数传进来？
# 答：因为 tasks 是一个列表，函数需要知道要在哪个列表上添加任务。
# 通过将 tasks 作为参数传入，函数可以直接修改这个列表，而不需要依赖全局变量。
# 这使得函数更灵活和可重用，可以在不同的任务列表上使用同一个函数。
#
# Q3：如果 find_task() 什么都没找到，应该 return 什么？
# 答：如果没有找到匹配的任务，find_task() 应该返回一个空列表 []，表示没有匹配的结果。


def add_task(tasks, name):
    """把一个任务名添加到 tasks。"""
    # 待做：把 name 添加到 tasks
    tasks.append(name)
    pass


def list_tasks(tasks):
    """带编号打印所有任务。"""
    # 待做：逐个打印任务，格式示例：1. 学习函数
    for i, task in enumerate(tasks, start=1):
        print(f"{i}. {task}")
    pass


def find_task(tasks, keyword):
    """返回任务名里包含 keyword 的任务。"""
    # 待做：构造并 return 一个匹配任务列表
    matched_tasks = [task for task in tasks if keyword in task]
    return matched_tasks
    pass


def main():
    tasks = []

    # 待做：至少添加 3 个任务
    add_task(tasks, "学习函数")
    add_task(tasks, "写作业")
    add_task(tasks, "锻炼身体")

    # 待做：打印所有任务
    list_tasks(tasks)

    # 待做：搜索一个关键词，并打印 find_task() 返回的结果
    finded_tasks = find_task(tasks, "学")
    print(f"匹配到的任务: {finded_tasks}")


if __name__ == "__main__":
    main()

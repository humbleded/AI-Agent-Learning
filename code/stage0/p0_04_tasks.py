#- 用 list 保存任务，用 dict 保存任务状态，用 set 去重标签。

tasks = ['task1', 'task2', 'task3', 'task1']
task_status = {'task1': 'pending', 'task2': 'pending', 'task3': 'success'}
tags = set(tasks)

tasks.append('task4')
tasks.insert(1, 'task5')
tasks.pop(2)  # 移除 'task2'
tasks[0] = 'task6'  # 修改 'task1' 为 'task6'
tasks.remove('task1')  # 移除 'task1'（如果存在）
query=tasks[0]

for i in range(len(tasks)):
    print(f"Task {i+1}: {tasks[i]}")


task_status['task4'] = 'pending'
task_status.get('task1')
task_status.pop('task2')  # 移除 'task2' 的状态



print("Tasks:", tasks)
print("Task Status:", task_status)
print("Unique Tags:", tags)


print("\n--- Codex 对比写法：任务、状态、标签分开表达 ---")

# 用 list 保存有顺序的任务
codex_tasks = ["学习 list", "学习 dict", "学习 set"]

# 用 dict 保存“任务名 -> 状态”
codex_task_status = {
    "学习 list": "done",
    "学习 dict": "doing",
    "学习 set": "todo",
}

# 用 list 保存标签，再用 set 去重
codex_tags = ["python", "basic", "python", "data-structure"]
codex_unique_tags = set(codex_tags)

print("初始任务：", codex_tasks)
print("初始状态：", codex_task_status)
print("去重标签：", codex_unique_tags)

# 新增任务
codex_tasks.append("练习任务管理")
codex_task_status["练习任务管理"] = "todo"

# 查询任务状态
query_task = "学习 dict"
print(f"{query_task} 的状态是：{codex_task_status.get(query_task)}")

# 修改任务状态
codex_task_status["学习 dict"] = "done"

# 删除任务
codex_tasks.remove("学习 set")
codex_task_status.pop("学习 set")

print("更新后的任务：")
for task in codex_tasks:
    print(f"- {task}: {codex_task_status.get(task)}")

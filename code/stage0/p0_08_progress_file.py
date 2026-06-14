"""
P0-08 文件、JSON、CSV。

运行：
    python code/stage0/p0_08_progress_file.py

任务：
    1. 从 resources/stage0_tasks.txt 读取任务；文件不存在时创建示例文件。
    2. 把任务和状态写入 resources/stage0_progress.json。
    3. 再读取 JSON，确认 Python 能重新解析。
"""

import json
import os
from pathlib import Path


# ROOT = Path(__file__).resolve().parents[2]
# TASK_FILE = ROOT / "resources" / "stage0_tasks.txt"
# JSON_FILE = ROOT / "resources" / "stage0_progress.json"


# def ensure_task_file():
#     if not TASK_FILE.exists():
#         TASK_FILE.write_text("学习文件读写\n学习 JSON\n练习异常处理\n", encoding="utf-8")


# def read_tasks():
#     ensure_task_file()
#     return [line.strip() for line in TASK_FILE.read_text(encoding="utf-8").splitlines() if line.strip()]


# def build_progress(tasks):
#     return [{"name": task, "status": "todo"} for task in tasks]

path='C:\\Users\\26823\\Desktop\\AI-Agent-Learning\\resources\\stage0_tasks.txt'
json_path='C:\\Users\\26823\\Desktop\\AI-Agent-Learning\\resources\\stage0_progress.json'

# 这个函数用来读取任务列表，从指定的文本文件中读取每一行，去掉空白，并返回一个任务列表。
def read_tasks():
    with open(path, 'r', encoding='utf-8') as f:
        tasks = [line.strip() for line in f if line.strip()]
    return tasks

def build_progress(tasks):
    # 这个函数用来构建进度数据，把每个任务转换成一个包含任务名称和状态的字典，并返回一个字典列表。
    return [{"name": task, "status": "todo"} for task in tasks]

def write_json(data, json_path):
    # 这个函数用来写入 JSON 数据，把 Python 数据转换成 JSON 字符串，并写入指定的 JSON 文件。
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def read_json(json_path):
    # 这个函数用来读取 JSON 数据，从指定的 JSON 文件中读取内容，并把 JSON 字符串转换成 Python 数据。
    with open(json_path, 'r', encoding='utf-8') as f:
        return json.load(f)
    
def print_tasks_number(tasks):
    # 这个函数用来打印任务数量，接受一个任务列表作为参数，并输出任务的数量。
    print("任务数量：", len(tasks))


def main():
    # tasks = read_tasks()
    # progress = build_progress(tasks)
    # JSON_FILE.write_text(json.dumps(progress, ensure_ascii=False, indent=2), encoding="utf-8")

    # loaded = json.loads(JSON_FILE.read_text(encoding="utf-8"))
    # print("任务数量：", len(loaded))
    # print("JSON 文件：", JSON_FILE)
    s=read_tasks()
    print(s)

    task_list=build_progress(s)

    write_json(task_list, json_path)

    read_json(json_path)

    print_tasks_number(task_list)

    jsonpath= os.path.abspath(json_path)
    print('jsonpath:', jsonpath)

    allfiles=os.listdir('D:/')
    print(allfiles)

    abs=os.path.abspath('D:/')
    print(abs)


if __name__ == "__main__":
    main()

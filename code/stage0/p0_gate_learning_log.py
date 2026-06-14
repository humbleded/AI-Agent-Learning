"""
P0-Gate Python 基础闯关：学习记录 JSON 小系统。

运行：
    python code/stage0/p0_gate_learning_log.py

任务：
    1. 输入今日学习记录。
    2. 保存到 resources/p0_gate_learning_log.json。
    3. 支持查看最近 7 条记录。
    4. 处理文件不存在、JSON 损坏、分钟数不是数字等错误。
"""

import json
from datetime import date
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
DATA_FILE = ROOT / "resources" / "p0_gate_learning_log.json"


def load_logs():
    if not DATA_FILE.exists():
        return []
    try:
        return json.loads(DATA_FILE.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        print("JSON 文件损坏，先返回空列表。请保留坏文件用于复盘。")
        return []


def save_logs(logs):
    DATA_FILE.parent.mkdir(parents=True, exist_ok=True)
    DATA_FILE.write_text(json.dumps(logs, ensure_ascii=False, indent=2), encoding="utf-8")


def add_log(logs):
    topic = input("学习主题：").strip()
    minutes_text = input("学习分钟数：").strip()
    try:
        minutes = int(minutes_text)
        if minutes < 0:
            print("分钟数不能为负数。")
            return logs 
    except ValueError:
        print("分钟数必须是整数。")
        return logs

    logs.append({
        "date": str(date.today()),
        "topic": topic,
        "minutes": minutes,
        "note": input("一句话记录：").strip(),
    })
    return logs


def show_recent(logs, limit=7):
    for item in logs[-limit:]:
        print(f"{item['date']} | {item['topic']} | {item['minutes']} 分钟 | {item['note']}")


def main():
    logs = load_logs()
    choice = input("1 新增记录 / 2 查看最近 7 条：").strip()
    if choice == "1":
        logs = add_log(logs)
        save_logs(logs)
    show_recent(logs)


if __name__ == "__main__":
    main()

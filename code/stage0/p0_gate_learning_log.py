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


class LogLoadError(ValueError):
    """现有学习记录无法安全读取；调用方必须停止写入。"""


def load_logs():
    try:
        logs = json.loads(DATA_FILE.read_text(encoding="utf-8"))
    except FileNotFoundError:
        return []
    except (json.JSONDecodeError, UnicodeError, OSError) as exc:
        raise LogLoadError("记录文件损坏或无法读取，请先备份并修复") from exc

    if not isinstance(logs, list):
        raise LogLoadError("记录文件必须保存一个列表，请先备份并修复")
    for item in logs:
        if (
            not isinstance(item, dict)
            or any(not isinstance(item.get(key), str) for key in ("date", "topic", "note"))
            or type(item.get("minutes")) is not int
            or item["minutes"] < 0
        ):
            raise LogLoadError("每条记录必须包含日期、主题、非负整数分钟数和备注，请先备份并修复")
    return logs


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
    try:
        logs = load_logs()
    except LogLoadError as exc:
        print(f"读取学习记录失败：{exc}。已停止，原文件未修改。")
        return
    choice = input("1 新增记录 / 2 查看最近 7 条：").strip()
    if choice == "1":
        original_count = len(logs)
        logs = add_log(logs)
        if len(logs) > original_count:
            save_logs(logs)
    show_recent(logs)


if __name__ == "__main__":
    main()

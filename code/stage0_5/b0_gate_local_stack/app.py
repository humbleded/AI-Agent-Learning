"""
B0-Gate 工程基础闯关：本地栈 Python CLI。

运行：
    python code/stage0_5/b0_gate_local_stack/app.py

目标：
    未来放进 Docker Compose，与 PostgreSQL 容器连接。
    当前脚手架先用 sqlite3 跑通 CLI 形状，等 Docker 阶段再替换连接层。
"""

import sqlite3
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
DB_PATH = ROOT / "resources" / "stage0_5" / "b0_gate_local_stack.db"


def connect():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    return sqlite3.connect(DB_PATH)


def init_db(conn):
    conn.execute(
        "CREATE TABLE IF NOT EXISTS logs(id INTEGER PRIMARY KEY, topic TEXT, minutes INTEGER)"
    )
    conn.commit()


def add_record(conn):
    topic = input("topic: ").strip()
    minutes = int(input("minutes: ").strip())
    conn.execute("INSERT INTO logs(topic, minutes) VALUES (?, ?)", (topic, minutes))
    conn.commit()


def show_recent(conn):
    rows = conn.execute("SELECT id, topic, minutes FROM logs ORDER BY id DESC LIMIT 7").fetchall()
    for row in rows:
        print(row)


def show_stats(conn):
    rows = conn.execute("SELECT topic, SUM(minutes) FROM logs GROUP BY topic").fetchall()
    for row in rows:
        print(row)


def main():
    with connect() as conn:
        init_db(conn)
        choice = input("1 add / 2 recent / 3 stats: ").strip()
        if choice == "1":
            add_record(conn)
        elif choice == "2":
            show_recent(conn)
        elif choice == "3":
            show_stats(conn)
        else:
            print("TODO：补充更完整的菜单和 PostgreSQL 版本。")


if __name__ == "__main__":
    main()

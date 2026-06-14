"""
B0-03 SQL 与关系型数据库：SQLite 学习记录库。

运行：
    python code/stage0_5/b0_03_learning_db.py

任务：
    1. 创建 resources/stage0_5/learning.db。
    2. 建表 learning_logs。
    3. 支持新增、最近 7 条、按 topic 统计、更新状态、删除测试数据。
"""

import sqlite3
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
DB_PATH = ROOT / "resources" / "stage0_5" / "learning.db"


def connect():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    return sqlite3.connect(DB_PATH)


def init_db(conn):
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS learning_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL,
            topic TEXT NOT NULL,
            minutes INTEGER NOT NULL,
            status TEXT NOT NULL,
            note TEXT
        )
        """
    )
    conn.commit()


def add_log(conn, date, topic, minutes, status="todo", note=""):
    conn.execute(
        "INSERT INTO learning_logs(date, topic, minutes, status, note) VALUES (?, ?, ?, ?, ?)",
        (date, topic, minutes, status, note),
    )
    conn.commit()


def recent_logs(conn, limit=7):
    return conn.execute(
        "SELECT id, date, topic, minutes, status, note FROM learning_logs ORDER BY id DESC LIMIT ?",
        (limit,),
    ).fetchall()


def stats_by_topic(conn):
    return conn.execute(
        "SELECT topic, SUM(minutes) FROM learning_logs GROUP BY topic ORDER BY SUM(minutes) DESC"
    ).fetchall()


def main():
    with connect() as conn:
        init_db(conn)
        add_log(conn, "2026-06-09", "SQLite", 30, "test", "脚手架测试数据")
        print("最近记录：", recent_logs(conn))
        print("按主题统计：", stats_by_topic(conn))
        print("TODO：补充 update_status(log_id, status) 和 delete_log(log_id)。")


if __name__ == "__main__":
    main()

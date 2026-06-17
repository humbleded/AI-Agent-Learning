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
    """确保 DB_PATH 所在目录存在，返回一个 sqlite3 连接。"""
    # TODO: mkdir 父目录 -> sqlite3.connect(DB_PATH)
    raise NotImplementedError("B0-03：实现 connect")


def init_db(conn):
    """建表 learning_logs（若不存在）。

    列：id 自增主键、date TEXT、topic TEXT、minutes INTEGER、status TEXT、note TEXT。
    建完记得 commit。
    """
    # TODO: CREATE TABLE IF NOT EXISTS ...
    raise NotImplementedError("B0-03：实现 init_db")


def add_log(conn, date, topic, minutes, status="todo", note=""):
    """插入一条学习记录（用参数占位符 ? 防注入），并 commit。"""
    # TODO
    raise NotImplementedError("B0-03：实现 add_log")


def recent_logs(conn, limit=7):
    """按 id 倒序返回最近 limit 条记录。"""
    # TODO
    raise NotImplementedError("B0-03：实现 recent_logs")


def stats_by_topic(conn):
    """按 topic 分组，统计每个 topic 的总分钟数，按总分钟数倒序返回。"""
    # TODO: SELECT topic, SUM(minutes) ... GROUP BY topic ORDER BY ...
    raise NotImplementedError("B0-03：实现 stats_by_topic")


# TODO（任务还要求这两个，自己补全函数）：
#   update_status(conn, log_id, status): 更新某条记录的 status。
#   delete_log(conn, log_id): 删除某条（测试）记录。


def main():
    """connect -> init_db -> 插一条测试数据 -> 打印 recent_logs 和 stats_by_topic。"""
    # TODO
    raise NotImplementedError("B0-03：实现 main")


if __name__ == "__main__":
    main()

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
    """确保 DB_PATH 父目录存在，返回 sqlite3 连接。"""
    # TODO
    raise NotImplementedError("B0-Gate：实现 connect")


def init_db(conn):
    """建表 logs(id 主键, topic TEXT, minutes INTEGER)，并 commit。"""
    # TODO
    raise NotImplementedError("B0-Gate：实现 init_db")


def add_record(conn):
    """读 topic / minutes 输入，插入一条记录并 commit。"""
    # TODO
    raise NotImplementedError("B0-Gate：实现 add_record")


def show_recent(conn):
    """按 id 倒序打印最近 7 条记录。"""
    # TODO
    raise NotImplementedError("B0-Gate：实现 show_recent")


def show_stats(conn):
    """按 topic 分组打印总 minutes。"""
    # TODO
    raise NotImplementedError("B0-Gate：实现 show_stats")


def main():
    """connect -> init_db -> 简单菜单（1 add / 2 recent / 3 stats）分发到上面的函数。"""
    # TODO
    raise NotImplementedError("B0-Gate：实现 main")


if __name__ == "__main__":
    main()

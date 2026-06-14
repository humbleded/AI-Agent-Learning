"""
B0-04 Docker 与 Compose：容器中的 Python 服务脚手架。

运行方式：
    本机直接运行：python code/stage0_5/docker_learning_stack/app.py
    Docker 阶段运行：docker compose up

任务：
    1. 读取环境变量 APP_ENV、POSTGRES_HOST、POSTGRES_DB、POSTGRES_USER。
    2. 先打印配置摘要。
    3. Docker/PostgreSQL 准备好后，再补充数据库连接检查。
"""

import os


def read_config():
    return {
        "APP_ENV": os.getenv("APP_ENV", "local"),
        "POSTGRES_HOST": os.getenv("POSTGRES_HOST", "localhost"),
        "POSTGRES_DB": os.getenv("POSTGRES_DB", "learning"),
        "POSTGRES_USER": os.getenv("POSTGRES_USER", "learning_user"),
        "POSTGRES_PASSWORD_SET": bool(os.getenv("POSTGRES_PASSWORD")),
    }


def main():
    print("Docker learning stack config:")
    for key, value in read_config().items():
        print(f"- {key}: {value}")
    print("TODO：安装 psycopg 后，增加 PostgreSQL 连接检查。")


if __name__ == "__main__":
    main()

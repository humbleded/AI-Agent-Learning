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
    """从环境变量读取配置，返回一个 dict。

    含 APP_ENV、POSTGRES_HOST、POSTGRES_DB、POSTGRES_USER（都给合理默认值），
    以及 POSTGRES_PASSWORD_SET（密码是否已设置的布尔值，不要回显密码本身）。
    """
    # TODO: os.getenv(..., 默认值)
    raise NotImplementedError("B0-04：实现 read_config")


def main():
    """打印配置摘要（逐行 - key: value）。"""
    # TODO
    raise NotImplementedError("B0-04：实现 main")


if __name__ == "__main__":
    main()

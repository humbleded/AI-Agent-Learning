r"""
L1-03 多轮聊天。

运行（项目根目录下，用 .venv 的 python）：
    .\.venv\Scripts\python.exe code\stage1\l1_03_chat.py

任务：
    1. 记忆在客户端：chat.completions 接口无状态，服务端不记上一轮，
       所以每轮都要把历史一起发出去。
    2. history 直接存成 API 的 messages 格式（每条 {"role":..,"content":..}），
       发送时零转换，[SYSTEM] + history + [本轮 user] 拼起来即可。
    3. trim_history 只保留最近 MAX_TURNS 轮（1 轮 = 2 条，所以切 -MAX_TURNS*2）。
    4. 支持 exit 退出、空输入提示。
"""

import os

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()  # 读 .env -> 环境变量

MAX_TURNS = 3  # 只保留最近 3 轮对话
SYSTEM = {"role": "system", "content": "你是一个乐于助人的中文助手。"}


def call_messages(messages):
    """接收一整个 messages 列表（整盘对话），发给模型，返回回复文本。

    与 L1-01 的 call_model 区别：call_model 只收一个字符串、内部自拼
    [system, user] 两条；这里直接收已经拼好的 messages 列表，才能带多轮历史。
    """
    api_key = os.environ.get("DEEPSEEK_API_KEY")
    if not api_key:
        return "未设置 DEEPSEEK_API_KEY：请在项目根目录 .env 里加一行 DEEPSEEK_API_KEY=你的key"

    client = OpenAI(api_key=api_key, base_url="https://api.deepseek.com")
    try:
        response = client.chat.completions.create(
            model="deepseek-v4-pro",
            messages=messages,
            stream=False,  # L1-04 才改成 stream=True 逐字返回
        )
        return response.choices[0].message.content
    except Exception as exc:
        return f"调用模型失败：{exc}"


def trim_history(history):
    """只保留最近 MAX_TURNS 轮。1 轮=2 条消息，所以切 -MAX_TURNS*2，保证整轮不被切断。"""
    return history[-MAX_TURNS * 2:]


def main():
    history = []  # 记忆在这里，存成 messages 格式：[{"role":..,"content":..}, ...]
    while True:
        question = input("你：").strip()
        if question.lower() == "exit":
            break
        if not question:
            print("请输入内容，或输入 exit。")
            continue

        # 每轮都把 system + 历史 + 本轮新问题拼成整盘对话发出去（服务端不记事，靠这里带历史）
        messages = [SYSTEM] + history + [{"role": "user", "content": question}]
        answer = call_messages(messages)
        print("AI：", answer)

        # 把本轮的问与答都存进 history，下一轮才记得住
        history.append({"role": "user", "content": question})
        history.append({"role": "assistant", "content": answer})
        history = trim_history(history)  # 砍掉太老的，只留最近 MAX_TURNS 轮


if __name__ == "__main__":
    main()

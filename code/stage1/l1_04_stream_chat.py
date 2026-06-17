"""
L1-04 流式输出。

运行：
    python code/stage1/l1_04_stream_chat.py

任务：
    1. 用户输入问题。
    2. 使用 stream=True 逐步显示输出。
    3. 出错时打印友好提示，不留下异常堆栈。
"""

import os
from dotenv import load_dotenv

load_dotenv()
from openai import OpenAI

MAX_TURNS = 3 
api_key = os.environ.get("DEEPSEEK_API_KEY")
base_url = "https://api.deepseek.com"
SYSTEM = {"role": "system", "content": "你是一个乐于助人的中文助手。"}

def stream_answer(messages):
    if not api_key:
        print("未设置 DEEPSEEK_API_KEY。这里先模拟流式输出：")
        for chunk in ["这是", " 一个", " stream", " 练习。"]:
            print(chunk, end="", flush=True)
        print()
        return f"这是 一个 stream 练习。"
    client = OpenAI(api_key=api_key, base_url=base_url)
    try:
        response = client.chat.completions.create(
            model="deepseek-v4-pro",
            messages=messages,
            stream=True,
            # reasoning_effort="high",
            # extra_body={"thinking": {"type": "enabled"}},
        )
        answer=""
        for chunk in response:
            if not chunk.choices:
                continue
            #reasoning_content是模型在生成回答时的推理内容，可以用来了解模型的思考过程。
            # reasoning_content = chunk.choices[0].delta.reasoning_content or ""
            # if reasoning_content:
            #     print(f"{reasoning_content}", end="", flush=True)
            chunk_content=chunk.choices[0].delta.content or ""
            answer += chunk_content
            print(chunk_content, end="", flush=True)
        print()
        return answer
    except Exception as exc:
        return f"流式输出失败：{exc}"

def trim_history(history):
    return history[-MAX_TURNS * 2:]


def main():
    history = []
    while True:
        question = input("你：").strip()
        if question.lower() == "exit":
            break
        if not question:
            print("请输入内容，或输入 exit。")
            continue

        # 每轮都把 system + 历史 + 本轮新问题拼成整盘对话发出去（服务端不记事，靠这里带历史）
        messages = [SYSTEM] + history + [{"role": "user", "content": question}]
        answer = stream_answer(messages)

        # 把本轮的问与答都存进 history，下一轮才记得住
        history.append({"role": "user", "content": question})
        history.append({"role": "assistant", "content": answer})
        history = trim_history(history)  # 砍掉太老的，只留最近 MAX_TURNS 轮


if __name__ == "__main__":
    main()

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


def stream_answer(question):
    if not os.getenv("OPENAI_API_KEY"):
        print("未设置 OPENAI_API_KEY。这里先模拟流式输出：")
        for chunk in ["这是", " 一个", " stream", " 练习。"]:
            print(chunk, end="", flush=True)
        print()
        return

    try:
        from openai import OpenAI
        client = OpenAI()
        with client.responses.stream(
            model=os.getenv("OPENAI_MODEL", "gpt-4.1-mini"),
            input=question,
        ) as stream:
            for event in stream:
                if event.type == "response.output_text.delta":
                    print(event.delta, end="", flush=True)
            print()
    except Exception as exc:
        print(f"流式输出失败：{exc}")


def main():
    question = input("问题：").strip()
    if question:
        stream_answer(question)


if __name__ == "__main__":
    main()

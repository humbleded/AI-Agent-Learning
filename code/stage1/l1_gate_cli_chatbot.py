"""
L1-Gate API 入门闯关：CLI Chatbot。

运行：
    python code/stage1/l1_gate_cli_chatbot.py

任务：
    1. 多轮对话。
    2. 支持 stream/on 和 stream/off 两种模式。
    3. 支持 exit 退出。
    4. 限制历史长度。
    5. API 错误时给用户可理解的提示。
"""

from l1_01_first_call import call_model
from l1_03_chat import build_prompt, trim_history
from l1_04_stream_chat import stream_answer


def main():
    history = []
    stream_mode = input("是否使用流式输出？y/N：").strip().lower() == "y"
    while True:
        question = input("你：").strip()
        if question.lower() == "exit":
            break
        if not question:
            print("空输入已忽略。")
            continue

        prompt = build_prompt(history, question)
        if stream_mode:
            stream_answer(prompt)
            answer = "[streamed answer]"
        else:
            answer = call_model(prompt)
            print("AI：", answer)

        history.extend([("user", question), ("assistant", answer)])
        history = trim_history(history)


if __name__ == "__main__":
    main()

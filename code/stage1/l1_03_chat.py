"""
L1-03 多轮聊天。

运行：
    python code/stage1/l1_03_chat.py

任务：
    1. 保存最近 N 轮 user/assistant 文本。
    2. 支持 exit 退出。
    3. 后续接入 SDK 时，把 history 转成 messages/input。
"""

from l1_01_first_call import call_model


MAX_TURNS = 3


def trim_history(history):
    return history[-MAX_TURNS * 2:]


def build_prompt(history, question):
    lines = ["下面是最近对话，请继续回答。"]
    for role, content in history:
        lines.append(f"{role}: {content}")
    lines.append(f"user: {question}")
    return "\n".join(lines)


def main():
    history = []
    while True:
        question = input("你：").strip()
        if question.lower() == "exit":
            break
        if not question:
            print("请输入内容，或输入 exit。")
            continue
        answer = call_model(build_prompt(history, question))
        print("AI：", answer)
        history.extend([("user", question), ("assistant", answer)])
        history = trim_history(history)


if __name__ == "__main__":
    main()

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

from l1_03_chat import build_prompt, trim_history,call_messages
from l1_04_stream_chat import stream_answer


def main():
    """整合前面 L1-01~04，做一个能多轮对话的 CLI 聊天机器人（可复用上面 import 的函数）。

    自己实现这个循环：
      1. 开场让用户选是否用流式输出（stream on/off）。
      2. while 循环读用户输入；输入 exit 就 break 退出。
      3. 空输入给提示并 continue，不发请求。
      4. 用 build_prompt(history, question) 拼出带历史的 prompt。
      5. 流式模式调 stream_answer(prompt)；非流式调 call_messages(prompt) 并打印。
      6. 把本轮用户问题和模型回答按 build_prompt/trim_history 约定的格式追加进 history，再 trim 限长。
      7. API 出错时给用户可读提示，别留异常堆栈、别崩。
    """
    stream_mode = input("是否使用流式输出？(stream on/off) ").strip().lower() == "stream on"
    history = []
    while True:
        question = input("你：").strip()
        if question.lower() == "exit":
            print("退出聊天。")
            break
        if not question:
            print("输入不能为空，请重新输入。")
            continue
        try:
            prompt = build_prompt(history, question)
            if stream_mode:
                answer = stream_answer(prompt)
            else:
                answer = call_messages(prompt)
                print(f"助手：{answer}")
            # 更新历史
            history.append({"role": "user", "content": question})
            history.append({"role": "assistant", "content": answer})
            history = trim_history(history)
        except Exception as e:
            print(f"调用模型失败：{e}")


if __name__ == "__main__":
    main()

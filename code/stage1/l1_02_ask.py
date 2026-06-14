"""
L1-02 单轮问答。

运行：
    python code/stage1/l1_02_ask.py

任务：
    1. 用户输入一个问题。
    2. 空输入要给提示。
    3. 调用模型回答一次；没有 key 时打印练习提示。
"""

from l1_01_first_call import call_model


def main():
    question = input("请输入问题：").strip()
    if not question:
        print("问题不能为空。")
        return
    print(call_model(question))


if __name__ == "__main__":
    main()

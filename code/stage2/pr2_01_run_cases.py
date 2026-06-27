"""
PR2-01 动手：同一抽取任务，3 个递进 prompt 的真实对比驱动脚本。

运行（项目根目录，用 .venv 的 python；需要外网调用 DeepSeek）：
    .venv/Scripts/python.exe code/stage2/pr2_01_run_cases.py
    （Windows 终端中文/符号乱码时，先设 PYTHONUTF8=1）

作用：
    把学习者自己设计的 prompt①②③ 各发一次给 DeepSeek，打印 3 段真实输出，
    并对每段输出尝试 json.loads，量化“格式稳不稳”，供 pr2_01_prompt_cases.md 做对比。
    3 个 prompt 抽取同一段文本，只是讲究程度递进（偷懒 → 清晰 → few-shot）。
"""

import json
import os
import sys

# 复用 stage1 写好的 call_model：把 stage1 目录加进模块搜索路径再 import
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "stage1"))
from l1_01_first_call import call_model


# prompt①：偷懒模糊版（zero-shot，不点字段、不要格式）
PROMPT_1 = '''抽取下面文本的信息，"""大家好，我叫李雷，今年 28 岁，目前在北京的字节跳动担任后端工程师，主要用 Go 语言，联系邮箱是 lilei@example.com。"""'''

# prompt②：清晰具体版（角色 + 分隔符 + 点名6字段 + 空JSON模板 + 前后不带文字）
PROMPT_2 = '''你是一个信息抽取助手，需要你抽取用"""标记的文本，抽取其中的姓名,年龄,公司,城市,职位,邮箱。并且必须按照以下JSON的格式输出，{"name":"","age":"","company":"","city":"","position":"","email":""}，JSON前后不能带有文字。
"""
大家好，我叫李雷，今年 28 岁，目前在北京的字节跳动担任后端工程师，主要用 Go 语言，联系邮箱是 lilei@example.com。
"""'''

# prompt③：few-shot 加强版（②的全部 + 一组填好的张三样例）
PROMPT_3 = '''你是一个信息抽取助手，需要你抽取用"""标记的文本，抽取其中的姓名,年龄,公司,城市,职位,邮箱。并且必须按照以下JSON的格式输出，{"name":"","age":"","company":"","city":"","position":"","email":""}，JSON前后不能带有文字。
示例:
输入:大家好，我叫张三，今年 20岁，目前在深圳的腾讯担任前端工程师，主要用 Go 语言，联系邮箱是 zhangsan@example.com。
输出:{"name":"张三","age":"20","company":"腾讯","city":"深圳","position":"前端工程师","email":"zhangsan@example.com"}

"""
大家好，我叫李雷，今年 28 岁，目前在北京的字节跳动担任后端工程师，主要用 Go 语言，联系邮箱是 lilei@example.com。
"""'''


def show(title, prompt):
    print("=" * 64)
    print(f"【{title}】")
    print("-" * 64)
    output = call_model(prompt)
    print(output)
    print("-" * 64)
    try:
        json.loads(output)
        print(">>> json.loads 检测：OK 成功（输出是合法 JSON，程序可直接使用）")
    except Exception as e:
        print(f">>> json.loads 检测：FAIL 失败（{type(e).__name__}：不是纯 JSON，程序拿不动）")
    print()


def main():
    show("prompt(1) 偷懒模糊版", PROMPT_1)
    show("prompt(2) 清晰具体版", PROMPT_2)
    show("prompt(3) few-shot 版", PROMPT_3)


if __name__ == "__main__":
    main()

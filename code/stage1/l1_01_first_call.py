"""
L1-01 API Key 与 SDK：第一次模型调用。

运行（项目根目录下，用 .venv 的 python）：
    .venv/Scripts/python.exe code/stage1/l1_01_first_call.py

任务：
    1. 从环境变量读取 DeepSeek API Key（不要把 key 写进代码）。
    2. 把“调用模型”封装成函数 call_model(prompt)，给后面 L1-02/03/Gate 复用。
    3. main() 里调用一次并打印结果。
"""

import os

# --- 第三方库说明（按你要求的：用到什么 import、怎么用，注释提醒）---------------
# load_dotenv：来自 python-dotenv 包（.venv 里已装）。
#   作用：把项目根目录 .env 文件里的 KEY=VALUE 读进“环境变量”，
#         这样下面 os.environ.get("DEEPSEEK_API_KEY") 才取得到。
#   用法：程序最开始调用一次 load_dotenv()，之后用 os.environ.get(...) 取值。
# OpenAI：来自 openai 包。DeepSeek 兼容 OpenAI SDK，所以复用同一个 OpenAI 类，
#         只把 base_url 指到 https://api.deepseek.com、key 用 DeepSeek 的即可。
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()  # 读 .env -> 环境变量；必须在 os.environ.get 之前调用


# ===== 原 OpenAI 版本（按你要求保留作参考，不启用）==========================
# def call_model(prompt):
#     api_key = os.getenv("OPENAI_API_KEY")
#     if not api_key:
#         return "未设置 OPENAI_API_KEY。先学习环境变量，不要把 key 写进代码。"
#
#     try:
#         from openai import OpenAI
#     except ImportError:
#         return "未安装 openai：pip install openai"
#
#     client = OpenAI(api_key=api_key)
#     response = client.responses.create(
#         model=os.getenv("OPENAI_MODEL", "gpt-4.1-mini"),
#         input=prompt,
#     )
#     return response.output_text
# ==========================================================================


def call_model(prompt: str) -> str:
    """把一句话 prompt 发给模型，返回模型回复的文本。

    参数：
        prompt：要问模型的内容（一段普通字符串）。
    返回：
        模型回复的文本；出错时返回一句可读提示，不抛异常、不打印堆栈。
        （这一点对应 L1-02 检查题：如何给用户显示错误提示。）

    后面 l1_02_ask.py / l1_03_chat.py / l1_gate_cli_chatbot.py 都会
    `from l1_01_first_call import call_model` 复用这个函数。
    """
    api_key = os.environ.get("DEEPSEEK_API_KEY")
    if not api_key:
        # 没配 key 时给可读提示，而不是直接崩溃。
        return "未设置 DEEPSEEK_API_KEY：请在项目根目录 .env 里加一行 DEEPSEEK_API_KEY=你的key"

    # client：一个“连到 DeepSeek 的调用器”。DeepSeek 兼容 OpenAI SDK。
    client = OpenAI(api_key=api_key, base_url="https://api.deepseek.com")

    try:
        # chat.completions.create：发一次对话请求。
        #   model：用哪个模型；如果报 "model not found"，改成 "deepseek-chat"。
        #   messages：消息列表。role="system" 设定模型身份，role="user" 是用户这次的话。
        #   stream=False：一次性返回完整回答（L1-04 才会改成 stream=True 逐字返回）。
        #   reasoning_effort / extra_body.thinking：DeepSeek 推理模型的可选参数，
        #     普通对话用不到可以整行删掉；保留也不影响。报错时优先怀疑这两行。
        response = client.chat.completions.create(
            model="deepseek-v4-pro",
            messages=[
                {"role": "system", "content": "You are a helpful assistant"},
                {"role": "user", "content": prompt},
            ],
            stream=False,
            reasoning_effort="high",
            extra_body={"thinking": {"type": "enabled"}},
        )
        # 取回复文本：必须是 response.choices[0].message.content 这一长串，
        # 不是 response 本身（response 是整个返回对象，含 usage、id 等）。
        return response.choices[0].message.content
    except Exception as exc:
        # key 错、网络错、model 名错都会到这里。给可读提示，不留异常堆栈。
        return f"调用模型失败：{exc}"


def main():
    prompt = "用一句话解释 API Key 的作用。"
    print("模型回复：", call_model(prompt))


if __name__ == "__main__":
    main()

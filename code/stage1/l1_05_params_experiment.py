"""
L1-05 参数实验与成本意识。

运行（项目根目录下，用 .venv 的 python）：
    .venv/Scripts/python.exe code/stage1/l1_05_params_experiment.py

任务：
    1. 对【同一个问题】至少跑 3 组不同 temperature（建议 0.0 / 1.3 / 1.5）。
    2. 每组打印模型回答 + 本次 token 用量（usage）。
    3. 把 3 组输出整理进 l1_05_params_experiment.md：差异观察 + 参数选择理由 + 成本问答。

通过标准：
    - 有真实输出对比（3 组温度）。
    - 能解释为什么这个任务选这些温度。
    - 能说出 token 成本由哪些部分构成（输入/输出，缓存命中/未命中）。

提示（和 l1_01 的 call_model 的区别，这就是今天要练的）：
    - 要【接收 temperature 参数】并真的传给 API。
    - 要【关掉思考模式】：不要写 reasoning_effort / extra_body.thinking，
      否则温度效果会被干扰、还白烧 token。
    - 要【同时返回 回答文本 和 usage】，好看 token 用量。
    - 问题选「开放/创意类」，温度差异才看得明显（问 1+1 等于几，看不出区别）。
"""

import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

# 实验固定变量：同一个问题、同一个模型，只变 temperature
QUESTION = "给我的橘猫起 5 个有创意的名字，并各用一句话说明寓意。"
MODEL = "deepseek-v4-pro"
TEMPERATURES = [0.0, 1.3, 1.5]   # 至少 3 组（横跨 最稳 -> 默认偏上 -> 最野）


def run_once(question: str, temperature: float):
    """发一次【非流式、非思考】请求，返回 (回答文本, usage)。

    TODO 你要写的步骤：
        1. 读 DEEPSEEK_API_KEY；没有就返回可读提示（参考 l1_01，别崩溃）。
        2. 建 client：OpenAI(api_key=..., base_url="https://api.deepseek.com")。
        3. client.chat.completions.create(...)：
           - model=MODEL
           - messages=[{"role": "user", "content": question}]
           - stream=False
           - temperature=temperature      ← 本关主角，别忘了传
           - 【不要】写 reasoning_effort / extra_body（关思考模式）
        4. 取回答：response.choices[0].message.content
        5. 取用量：response.usage（含 prompt_tokens / completion_tokens / total_tokens）
        6. return 回答文本, response.usage
        7. 用 try/except 包住，出错返回可读提示（不要抛异常堆栈）。
    """
    try:
        api_key = os.environ.get("DEEPSEEK_API_KEY")
        if not api_key:
            return "请设置 DEEPSEEK_API_KEY 环境变量", None
        client = OpenAI(api_key=api_key, base_url="https://api.deepseek.com")
        response = client.chat.completions.create(
            model=MODEL,
            messages=[{"role": "user", "content": question}],
            stream=False,
            temperature=temperature
        )
        answer = response.choices[0].message.content
        usage = response.usage
        return answer, usage
    except Exception as e:
        return f"请求出错：{e}", None


def main():
    """对同一问题跑 TEMPERATURES 三组，逐组打印回答 + token 用量。

    TODO：
        1. for t in TEMPERATURES:
        2.   打印分隔线 + 当前 temperature
        3.   调 run_once(QUESTION, t)，拿到 回答 和 usage
        4.   打印回答 + usage（prompt_tokens / completion_tokens / total_tokens）
        5. 全部跑完后，把 3 组结果整理进 l1_05_params_experiment.md
    """
    for t in TEMPERATURES:
        print("="*20)
        print(f"Temperature: {t}")
        answer, usage = run_once(QUESTION, t)
        print("回答：", answer)
        if usage:
            print("用量：", f"prompt_tokens={usage.prompt_tokens}", f"completion_tokens={usage.completion_tokens}", f"total_tokens={usage.total_tokens}")
        else:
            print("用量：无")


if __name__ == "__main__":
    main()

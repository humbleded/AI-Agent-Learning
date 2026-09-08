"""
S-03 上下文工程 · token 粗略估算对比实验。

运行方式：
    项目根目录，激活 .venv 后：
        python code/stage2/s03_context_experiment.py
    中文乱码时先设：  PowerShell -> $env:PYTHONUTF8=1   /   cmd -> set PYTHONUTF8=1
    直接运行会真实调用 DeepSeek 生成摘要；fake_summarize 仅保留历史函数名。

任务：
    对同一段「8 条（4 轮）对话历史」，对比三种上下文处理方案的 token 数：
        方案① 全量 full        ：原样全发
        方案② 裁剪 trim        ：只留最近 KEEP_RECENT 条（= 你 L1 的 trim_history，truncation）
        方案③ 压缩 compaction   ：旧历史压成 1 条摘要 + 保留最近 KEEP_RECENT 条
    打印每个方案的 token 估算值 + 条数 + 按实际结果得出的结论。
    这里只估算下一次请求携带的上下文，不包括生成摘要本身的调用消耗；
    不能把粗估值当成模型实际 tokenizer 结果或计费 usage。

通过标准（对照 S-03）：
    - 三种方案都能估算 token 并打印对比；最小值及并列按本次实测决定。
    - 独立检查裁剪/压缩之后是否仍包含“三玖”，不能凭 token 排序推断信息保留。
    - 摘要过长不一定节省上下文；生成摘要还需要额外调用，效果以实际结果为准。
    - 离线测试可注入摘要函数；模型失败或摘要为空时停止本次比较。

给你的（不用写）：count_tokens（第 9 章工具）、compact_history（你 C3 的成果）、SAMPLE_HISTORY。
你要写的：标了 TODO 的 5 处 —— history_tokens / plan_full / plan_trim / plan_compaction / fake_summarize / main。
"""
import os
from dotenv import load_dotenv
from openai import OpenAI
load_dotenv()  # 读 .env -> 环境变量
api_key = os.environ.get("DEEPSEEK_API_KEY")
# =========== 已给你：token 估算（第 9 章 ContextBuilder 的简化版） ===========
def count_tokens(text):
    """中文 1 字符≈1 token，英文 1 单词≈1.3 tokens（毛估，非真 tokenizer）。"""
    chinese_chars = sum(1 for ch in text if '\u4e00' <= ch <= '\u9fff')
    english_words = len([w for w in text.split() if w])
    return int(chinese_chars + english_words * 1.3)


# =========== 已给你：你 C3 写的 mini-Compaction（直接复用） ===========
def compact_history(history, keep_recent, summarize):
    if type(keep_recent) is not int or keep_recent <= 0:
        raise ValueError("keep_recent 必须是正整数")
    if len(history) <= keep_recent:
        return history
    old_history = history[:-keep_recent]
    old_text = "\n".join([msg["content"] for msg in old_history])  # C3 建议：可带上 role
    summary_text = summarize(old_text)
    if not isinstance(summary_text, str) or not summary_text.strip():
        raise RuntimeError("摘要为空或格式不正确")
    summary_message = {"role": "system", "content": "之前对话摘要：" + summary_text}
    return [summary_message] + history[-keep_recent:]


# =========== 已给你：造好的对话历史（8 条 / 4 轮；第 1 条藏了名字“三玖”） ===========
SAMPLE_HISTORY = [
    {"role": "user",      "content": "我叫三玖，请记住我的名字"},
    {"role": "assistant", "content": "好的，三玖，我记住了"},
    {"role": "user",      "content": "帮我推荐一本机器学习的入门书"},
    {"role": "assistant", "content": "推荐《机器学习》西瓜书，适合入门"},
    {"role": "user",      "content": "再推荐一部好看的科幻电影"},
    {"role": "assistant", "content": "推荐《星际穿越》，硬核又感人"},
    {"role": "user",      "content": "顺便问下，明天天气怎么样？"},
    {"role": "assistant", "content": "明天多云转晴，挺适合出门的"},
]

KEEP_RECENT = 2  # 保留最近几条（注意：1 轮 = user+assistant 两条，所以 2 条 = 最近 1 轮）


# =========== 你来写：TODO 1 —— 统计一段历史的总 token ===========
def history_tokens(history):
    """把 history 里每条 msg["content"] 的 token 加起来，返回总数。"""
    # TODO: 遍历 history，用 count_tokens 累加每条 content
    # total_tokens = 0
    # for msg in history:
    #     total_tokens += count_tokens(msg["content"])
    # return total_tokens
    return sum(count_tokens(msg["content"]) for msg in history)  # 一行写法


# =========== 摘要生成：当前实现真实调用 DeepSeek ===========
def fake_summarize(text):
    """真实调用 DeepSeek 生成摘要；历史函数名保留，失败时抛出可读错误。"""
    if not api_key or not api_key.strip():
        raise RuntimeError("未设置 DEEPSEEK_API_KEY，无法生成摘要")
    messages=[
              {"role": "system", "content": "把下面的对话历史压成一句话摘要，保留人名等关键信息，30 字以内。"},
              {"role": "user",   "content": text},
              ]
    try:
        client = OpenAI(api_key=api_key, base_url="https://api.deepseek.com",timeout=30,)
        response = client.chat.completions.create(
            model="deepseek-v4-pro",
            messages=messages,
            stream=False,
        )
        summary = response.choices[0].message.content
    except Exception as exc:
        raise RuntimeError("调用模型生成摘要失败") from exc
    if not isinstance(summary, str) or not summary.strip():
        raise RuntimeError("摘要为空或格式不正确")
    return summary



# =========== 你来写：TODO 3 —— 三种方案各返回“处理后的 history” ===========
def plan_full(history):
    """方案①全量：原样返回。"""
    return history


def plan_trim(history, keep_recent):
    """方案②裁剪：只留最近 keep_recent 条（呼应你的 trim_history）。"""
    if type(keep_recent) is not int or keep_recent <= 0:
        raise ValueError("keep_recent 必须是正整数")
    return history[-keep_recent:]


def plan_compaction(history, keep_recent, summarize):
    """方案③压缩：调用上面的 compact_history。"""
    return compact_history(history, keep_recent, summarize)


# =========== 你来写：TODO 4 —— 主流程：跑三方案、算 token、打印对比 + 结论 ===========
def main():
    # TODO:
    #   1. 用三种方案分别处理 SAMPLE_HISTORY，得到三段处理后的 history
    #   2. 用 history_tokens 算每段的 token 数
    #   3. 打印对比：方案名 | 条数 | token 数
    #   4. 打印一句结论：谁最省 token？方案② 里“三玖”那条还在吗（演示裁剪丢信息）？
    try:
        full = plan_full(SAMPLE_HISTORY)
        trimmed = plan_trim(SAMPLE_HISTORY, KEEP_RECENT)
        compacted = plan_compaction(SAMPLE_HISTORY, KEEP_RECENT, fake_summarize)
    except (ValueError, RuntimeError) as exc:
        print(f"本次比较已停止：{exc}。没有生成比较结论。")
        return
    plans = {"方案① 全量 full": full, "方案② 裁剪 trim": trimmed, "方案③ 压缩 compaction": compacted}
    token_estimates = {name: history_tokens(history) for name, history in plans.items()}
    for name, history in plans.items():
        print(f"{name}：条数 {len(history)}，token 粗略估算 {token_estimates[name]}")
    minimum = min(token_estimates.values())
    cheapest = [name for name, value in token_estimates.items() if value == minimum]
    tie = "并列" if len(cheapest) > 1 else ""
    print(f"结论：{'、'.join(cheapest)} {tie}最省本次上下文，估算 {minimum} token。")
    print("以上不包括生成摘要本身的调用消耗，实际用量应查看模型返回的 usage。")
    # 程序实际检查“三玖”有没有被保住
    name_in_trim    = any("三玖" in m["content"] for m in trimmed)
    name_in_compact = any("三玖" in m["content"] for m in compacted)
    print(f"方案②里还能找到“三玖”吗：{name_in_trim}")
    print(f"方案③里还能找到“三玖”吗：{name_in_compact}")
    print(f"方案③的摘要内容：{compacted[0]['content']}")


if __name__ == "__main__":
    main()

"""
S-03 上下文工程 · token 对比小实验（练习骨架 —— 核心逻辑留给你填）

运行方式：
    项目根目录，激活 .venv 后：
        python code/stage2/s03_context_experiment.py
    中文乱码时先设：  PowerShell -> $env:PYTHONUTF8=1   /   cmd -> set PYTHONUTF8=1

任务：
    对同一段「8 条（4 轮）对话历史」，对比三种上下文处理方案的 token 数：
        方案① 全量 full        ：原样全发
        方案② 裁剪 trim        ：只留最近 KEEP_RECENT 条（= 你 L1 的 trim_history，truncation）
        方案③ 压缩 compaction   ：旧历史压成 1 条摘要 + 保留最近 KEEP_RECENT 条
    打印每个方案的 token 数 + 条数 + 一句结论。

通过标准（对照 S-03）：
    - 三种方案都能算出 token 数并打印对比（预期 token：① > ③ > ②）。
    - 能在输出里说清：② 最省 token，但最可能丢早期关键信息（第 1 条的“三玖”）；
      ③ 用“一次摘要 + 一条摘要 token”的代价，换回早期信息的召回。
    -（可选）把 fake_summarize 换成真调 DeepSeek，看真摘要效果；不调也能用假摘要跑通对比。

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
    if len(history) <= keep_recent:
        return history
    old_history = history[:-keep_recent]
    old_text = "\n".join([msg["content"] for msg in old_history])  # C3 建议：可带上 role
    summary_text = summarize(old_text)
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


# =========== 你来写：TODO 2 —— 假摘要（先不花钱跑通对比） ===========
def fake_summarize(text):
    """把一段文本压成“一句话摘要”。先用规则版（如截前 N 字 + …），之后可换真调 DeepSeek。"""
    # return f"前文压缩自{len(text)} 字: {text[:20]}..." if len(text) > 20 else text
    messages=[
              {"role": "system", "content": "把下面的对话历史压成一句话摘要，保留人名等关键信息，30 字以内。"},
              {"role": "user",   "content": text},
              ]
    client = OpenAI(api_key=api_key, base_url="https://api.deepseek.com",timeout=30,)
    try:
        response = client.chat.completions.create(
            model="deepseek-v4-pro",
            messages=messages,
            stream=False,
        )
        return response.choices[0].message.content
    except Exception as exc:
        return f"调用模型失败：{exc}"



# =========== 你来写：TODO 3 —— 三种方案各返回“处理后的 history” ===========
def plan_full(history):
    """方案①全量：原样返回。"""
    return history


def plan_trim(history, keep_recent):
    """方案②裁剪：只留最近 keep_recent 条（呼应你的 trim_history）。"""
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
    full = plan_full(SAMPLE_HISTORY)
    trimmed = plan_trim(SAMPLE_HISTORY, KEEP_RECENT)
    compacted = plan_compaction(SAMPLE_HISTORY, KEEP_RECENT, fake_summarize)
    print(f"方案① 全量 full：条数 {len(full)}，token 数 {history_tokens(full)}")
    print(f"方案② 裁剪 trim：条数 {len(trimmed)}，token 数 {history_tokens(trimmed)}")
    print(f"方案③ 压缩 compaction ：条数 {len(compacted)}，token 数 {history_tokens(compacted)}")
    conclusion = "结论："
    if history_tokens(trimmed) < history_tokens(compacted) < history_tokens(full):
        conclusion += "方案② 最省 token，但最可能丢早期关键信息（第 1 条的“三玖”）"
    elif history_tokens(compacted) < history_tokens(trimmed) < history_tokens(full):
        conclusion += "方案③ 最省 token，但最可能丢早期关键信息（第 1 条的“三玖”）"
    else:
        conclusion += "方案① 最省 token，但最可能丢早期关键信息（第 1 条的“三玖”）"
    print(conclusion)
    # 程序实际检查“三玖”有没有被保住
    name_in_trim    = any("三玖" in m["content"] for m in trimmed)
    name_in_compact = any("三玖" in m["content"] for m in compacted)
    print(f"方案②里还能找到“三玖”吗：{name_in_trim}")
    print(f"方案③里还能找到“三玖”吗：{name_in_compact}")
    print(f"方案③的摘要内容：{compacted[0]['content']}")


if __name__ == "__main__":
    main()

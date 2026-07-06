"""
PR2-02 摘要与改写。

运行（项目根目录，用 .venv 的 python；llm_summarize 需要外网调用 DeepSeek）：
    .venv/Scripts/python.exe code/stage2/pr2_02_summarizer.py
    （Windows 终端中文乱码时，先设 PYTHONUTF8=1）

任务：
    输入一段长文，输出 3 条要点 + 1 段摘要。
    - simple_summarize：不用模型的机械基线（按换行或句号切、取前 3 句）。
    - llm_summarize：  模型版，prompt 锁 JSON（3 要点 + 1 摘要、控长度），格式稳定。
    main 把两版跑在同一段长文上做对比，并对模型版做 json.loads + 数要点条数的兜底检查。
"""

import json
import os
import sys

# 复用 stage1 写好的 call_model：把 stage1 目录加进模块搜索路径再 import
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "stage1"))
from l1_01_first_call import call_model


# 测试长文：机械版 / 模型版都跑这一段，方便对比
LONG_TEXT = (
    "近年来，远程办公在全球范围内迅速普及。"
    "它让员工省去了通勤时间，工作地点更灵活，不少人因此提升了生活质量。"
    "但远程办公也带来新的挑战，比如团队沟通成本上升、员工容易感到孤独、工作与生活的边界变得模糊。"
    "为了应对这些问题，很多公司开始采用混合办公模式，既保留远程的灵活，又通过定期到岗维持团队凝聚力。"
    "专家认为，未来办公方式会更加多元，关键在于找到适合团队的平衡点。"
)


def simple_summarize(text):
    """把文本切成句子/行，取前 3 条做要点，再拼成一段摘要，返回 (points, summary)。"""
    if "\n" in text.strip():
        parts = text.strip().split("\n")
    else:
        parts = text.strip().split("。")
    list_of_sentences = [s.strip() for s in parts if s.strip()]
    points = list_of_sentences[:3]  # 取前三个句子作为要点
    summary = '；'.join(points)
    return points, summary


def llm_summarize(text):
    """模型版：prompt 锁 JSON（3 要点 + 1 摘要、控长度），返回模型输出（应为一段 JSON 文本）。"""
    instruction = '你现在的角色是摘要助手,需要对"""内的文本进行摘要。需要提取3个要点和1段整体的摘要。每条要点不超过20个字,摘要不超过60个字。必须用JSON的格式输出,格式如下：{"points": ["要点1","要点2","要点3"], "summary": "一段话"}，并且JSON前后不能有文字。'
    prompt = instruction + '\n"""\n' + text + '\n"""'
    return call_model(prompt)


def main():
    print("=" * 60)
    print("【机械版 simple_summarize（不用模型，取前 3 句）】")
    points, summary = simple_summarize(LONG_TEXT)
    for i, p in enumerate(points, 1):
        print(f"  要点{i}：{p}")
    print(f"  摘要：{summary}")
    print()

    print("=" * 60)
    print("【模型版 llm_summarize（DeepSeek + 锁 JSON）】")
    output = llm_summarize(LONG_TEXT)
    print(output)
    print("-" * 60)
    # 兜底检查：软约束（3 条、长度）模型不保证分毫不差，用代码验一遍
    try:
        data = json.loads(output)
        n_points = len(data.get("points", []))
        print(f">>> json.loads：OK 成功")
        print(f">>> points 条数 = {n_points}（要求 3）")
        for i, p in enumerate(data.get("points", []), 1):
            print(f"    要点{i} 长度 = {len(p)} 字（要求 ≤20）：{p}")
        s = data.get("summary", "")
        print(f">>> summary 长度 = {len(s)} 字（要求 ≤60）")
    except Exception as e:
        print(f">>> json.loads：FAIL 失败（{type(e).__name__}：不是纯 JSON）")


if __name__ == "__main__":
    main()

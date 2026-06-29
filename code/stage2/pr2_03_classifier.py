"""
PR2-03 分类与路由。

运行：
    python code/stage2/pr2_03_classifier.py

任务：
    1. 固定标签：问题、投诉、建议、闲聊、其他。
    2. 至少准备 15 条测试样例。
    3. 输出预测标签并记录错误分析。
"""
import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "stage1"))
from l1_01_first_call import call_model

LABELS = ["问题", "投诉", "建议", "闲聊", "其他"]
RULES = {
    "投诉": ["退款", "差评", "投诉", "太差", "垃圾"],
    "建议": ["建议", "希望", "最好能"],
    "问题": ["怎么", "如何", "为什么", "？", "?"],
    "闲聊": ["你好", "谢谢", "天气"],
}


def classify(text):
    """把一段文本归到 LABELS 之一（先用关键词规则，后续可换成模型）。

    步骤：根据文本里出现的关键词判断属于「问题/投诉/建议/闲聊」，都不匹配返回「其他」。
    """
    for category, keywords in RULES.items():
        if any(kw in text for kw in keywords):
            return category
    return "其他"

def all_hits(text):
    """返回 text 命中的所有类别（诊断用，不止第一个）。"""
    hits = []
    for category, keywords in RULES.items():
        if any(kw in text for kw in keywords):
            hits.append(category)
    return hits


def classify_llm(text):
    """模型版分类：调 LLM 判类，只输出标签词，strip + 白名单兜底，返回 5 标签之一。"""
    instruction = """你是一个客服助理,需要把【】中的文本判断是属于"问题","投诉","建议","闲聊"中的哪一种标签,如果没有则提取"其他"作为标签。只能输出一个标签词,并且标签词前后都不带任何其他字
示例:
输入:这件衣服适合多大年龄穿?
输出:问题"""
    prompt = instruction + '【' + text + '】'     # 拼接 text
    label = call_model(prompt).strip()            # 调模型 + 洗换行
    if label not in LABELS:
        label = '其他'                            # 白名单兜底（模型答了列表外的词）
    return label


def run_tests():
    """准备 ≥15 条测试样例，逐条打印「文本 => 预测标签」，并记录分类错误原因。"""
    # TODO: 补足到 15 条样例 -> 逐条 classify 并打印 -> 写下错误分析
    test_cases = [
        ("我有一个问题，怎么做？", "问题"),
        ("我对服务很不满，想投诉", "投诉"),
        ("我有一个建议，应该改进", "建议"),
        ("你好，我们来聊天吧", "闲聊"),
        ("这是其他类型的消息", "其他"),
        ("请问这个问题该如何解决？", "问题"),
        ("我要投诉这个产品", "投诉"),
        ("我有一些意见想反馈", "建议"),
        ("我们来闲聊一下", "闲聊"),
        ("随机的其他消息", "其他"),
        ("遇到一个疑问，求解答", "问题"),
        ("对服务差评，提出投诉", "投诉"),
        ("改进建议：增加新功能", "建议"),
        ("你好，今天聊什么？", "闲聊"),
        ("这是一条无法分类的消息", "其他")
    ]
    
    count = 0
    for text, expected_label in test_cases:
        label = classify(text)
        hits = all_hits(text)
        if label != expected_label:
          if len(hits) == 0:
              reason = "漏判（没命中任何关键词，落其他）"
          elif len(hits) >= 2:
              reason = f"撞类（命中 {hits}，被排前面的 {hits[0]} 抢走）"
          else:
              reason = f"误命中（只命中 {hits[0]}，关键词配错）"
          print(f"❌ {text} => {label}（期望 {expected_label}）｜{reason}")
          count += 1
    print(f"总共分类错误 {count} 次")
    print(f"分类正确率 {(len(test_cases)-count)/len(test_cases):.0%}")


def compare_hard_cases():
    """规则版判错的 4 条难样例，用模型版再判一次，对比规则版 vs 模型版。"""
    hard_cases = [
        ("我有一些意见想反馈", "建议"),
        ("我们来闲聊一下", "闲聊"),
        ("遇到一个疑问，求解答", "问题"),
        ("你好，今天聊什么？", "闲聊"),
    ]
    for text, expected in hard_cases:
        print(f"{text}｜期望={expected}｜规则版={classify(text)}｜模型版={classify_llm(text)}")


# 原入口（保留，已注释）：
# if __name__ == "__main__":
#     run_tests()
if __name__ == "__main__":
    run_tests()
    print("-" * 40)
    compare_hard_cases()

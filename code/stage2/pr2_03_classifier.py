"""
PR2-03 分类与路由。

运行：
    python code/stage2/pr2_03_classifier.py

任务：
    1. 固定标签：问题、投诉、建议、闲聊、其他。
    2. 至少准备 15 条测试样例。
    3. 输出预测标签并记录错误分析。
"""


LABELS = ["问题", "投诉", "建议", "闲聊", "其他"]


def classify(text):
    """把一段文本归到 LABELS 之一（先用关键词规则，后续可换成模型）。

    步骤：根据文本里出现的关键词判断属于「问题/投诉/建议/闲聊」，都不匹配返回「其他」。
    """
    # TODO
    raise NotImplementedError("PR2-03：实现 classify")


def run_tests():
    """准备 ≥15 条测试样例，逐条打印「文本 => 预测标签」，并记录分类错误原因。"""
    # TODO: 补足到 15 条样例 -> 逐条 classify 并打印 -> 写下错误分析
    raise NotImplementedError("PR2-03：实现 run_tests")


if __name__ == "__main__":
    run_tests()

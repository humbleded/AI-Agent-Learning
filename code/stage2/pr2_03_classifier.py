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
    if any(word in text for word in ["怎么", "为什么", "能不能", "如何"]):
        return "问题"
    if any(word in text for word in ["太差", "不满意", "投诉", "退款"]):
        return "投诉"
    if any(word in text for word in ["建议", "希望", "可以增加"]):
        return "建议"
    if any(word in text for word in ["你好", "哈哈", "随便聊"]):
        return "闲聊"
    return "其他"


def run_tests():
    samples = [
        "这个接口为什么超时？",
        "我不满意，要求退款",
        "建议增加导出功能",
        "你好，今天状态如何",
        "订单 12345",
    ]
    for text in samples:
        print(text, "=>", classify(text))
    print("TODO：补足到 15 条，并写下分类错误原因。")


if __name__ == "__main__":
    run_tests()

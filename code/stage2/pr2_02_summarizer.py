"""
PR2-02 摘要与改写。

运行：
    python code/stage2/pr2_02_summarizer.py

任务：
    1. 输入一段长文。
    2. 输出 3 条要点。
    3. 输出 1 段摘要。
    4. 后续可替换为模型调用。
"""


def simple_summarize(text):
    sentences = [part.strip() for part in text.replace("。", ".").split(".") if part.strip()]
    points = sentences[:3]
    summary = "；".join(points)
    return points, summary


def main():
    text = input("粘贴长文：").strip()
    if not text:
        print("请输入文本。")
        return
    points, summary = simple_summarize(text)
    print("三条要点：")
    for index, point in enumerate(points, start=1):
        print(f"{index}. {point}")
    print("摘要：", summary)
    print("TODO：接入模型后，要求输出格式仍保持稳定。")


if __name__ == "__main__":
    main()

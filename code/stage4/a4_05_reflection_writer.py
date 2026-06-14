"""
A4-05 Reflection Writer。

运行：
    python code/stage4/a4_05_reflection_writer.py

任务：
    1. 输入初稿。
    2. 生成反思意见。
    3. 生成改进稿。
    4. 对比改进点。
"""


def critique(draft):
    tips = []
    if len(draft) < 50:
        tips.append("内容太短，需要补充背景和例子。")
    if "因为" not in draft:
        tips.append("缺少原因解释。")
    return tips or ["结构基本完整，检查术语是否准确。"]


def revise(draft, tips):
    return draft + "\n\n改进方向：\n" + "\n".join(f"- {tip}" for tip in tips)


def main():
    draft = input("初稿：").strip()
    tips = critique(draft)
    improved = revise(draft, tips)
    print("反思：", tips)
    print("改进稿：")
    print(improved)


if __name__ == "__main__":
    main()

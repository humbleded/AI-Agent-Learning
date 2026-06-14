"""
P0-07 异常、调试、单元测试。

运行：
    python code/stage0/p0_07_safe_divide.py

任务：
    1. 完成 safe_divide(a_text, b_text)。
    2. 处理非数字输入和除零。
    3. 至少保留 3 个测试样例：正常、除零、非数字。
"""


def safe_divide(a_text, b_text):
    """把两个字符串转成数字后相除，返回结果或错误信息。"""
    try:
        a = float(a_text)
        b = float(b_text)
        return a / b
    except ValueError:
        return "错误：请输入数字。"
    except ZeroDivisionError:
        return "错误：除数不能为 0。"


def run_examples():
    examples = [
        ("10", "2"),
        ("10", "0"),
        ("abc", "2"),
    ]
    for a, b in examples:
        print(f"{a} / {b} => {safe_divide(a, b)}")


def main():
    run_examples()
    a = input("被除数：")
    b = input("除数：")
    print(safe_divide(a, b))


if __name__ == "__main__":
    main()

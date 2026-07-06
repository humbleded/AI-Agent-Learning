"""
T3-02 计算器工具。

运行：
    python code/stage3/t3_02_calculator_tool.py

任务：
    1. 定义工具 schema。
    2. 校验参数。
    3. 真实执行计算。
    4. 打印调用参数和结果。
"""

import operator


OPERATORS = {
    "add": operator.add,
    "sub": operator.sub,
    "mul": operator.mul,
    "div": operator.truediv,
}

CALCULATOR_SCHEMA = {
    "name": "calculator_tool",
    "description": "进行精确的加、减、乘、除运算。",
    "parameters": {
        "operation": "操作类型，只能是 add/sub/mul/div",
        "a": "第一个数，数字或可转成数字的字符串",
        "b": "第二个数，数字或可转成数字的字符串",
    },
}

def calculator_tool(operation, a, b):
    """计算器工具：根据 operation 对 a、b 做运算，返回 {"ok": bool, ...}。

    步骤：
      1. operation 不在 OPERATORS 里 -> 返回 {"ok": False, "error": ...}。
      2. 把 a、b 转成 float（转不动 -> 「参数必须是数字」）。
      3. 执行运算；除零要单独捕获给「除数不能为 0」。
      4. 正常返回 {"ok": True, "result": 结果}。
    """
    # TODO
    if operation not in OPERATORS:
        return {"ok": False, "error": f"不支持的操作：{operation}"}
    try:
        a = float(a)
        b = float(b)
    except ValueError:
        return {"ok": False, "error": "参数必须是数字"}
    try:
        result = OPERATORS[operation](a, b)
    except ZeroDivisionError:
        return {"ok": False, "error": "除数不能为 0"}
    return {"ok": True, "result": result}


def main():
    """读 operation/a/b -> 打印调用参数 -> 打印 calculator_tool 结果。"""
    # TODO
    operation = input("请输入操作（add/sub/mul/div）：")
    a = input("请输入第一个数字：")
    b = input("请输入第二个数字：")
    print(f"调用参数：operation={operation}, a={a}, b={b}")
    result = calculator_tool(operation, a, b)
    print(f"计算结果：{result}")


if __name__ == "__main__":
    main()

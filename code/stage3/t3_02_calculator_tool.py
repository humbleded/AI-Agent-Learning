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


def calculator_tool(operation, a, b):
    if operation not in OPERATORS:
        return {"ok": False, "error": f"不支持的 operation：{operation}"}
    try:
        a = float(a)
        b = float(b)
        result = OPERATORS[operation](a, b)
        return {"ok": True, "result": result}
    except ZeroDivisionError:
        return {"ok": False, "error": "除数不能为 0"}
    except ValueError:
        return {"ok": False, "error": "参数必须是数字"}


def main():
    operation = input("operation(add/sub/mul/div): ").strip()
    a = input("a: ")
    b = input("b: ")
    print("tool_args:", {"operation": operation, "a": a, "b": b})
    print("tool_result:", calculator_tool(operation, a, b))


if __name__ == "__main__":
    main()

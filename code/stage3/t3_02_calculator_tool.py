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
    """计算器工具：根据 operation 对 a、b 做运算，返回 {"ok": bool, ...}。

    步骤：
      1. operation 不在 OPERATORS 里 -> 返回 {"ok": False, "error": ...}。
      2. 把 a、b 转成 float（转不动 -> 「参数必须是数字」）。
      3. 执行运算；除零要单独捕获给「除数不能为 0」。
      4. 正常返回 {"ok": True, "result": 结果}。
    """
    # TODO
    raise NotImplementedError("T3-02：实现 calculator_tool")


def main():
    """读 operation/a/b -> 打印调用参数 -> 打印 calculator_tool 结果。"""
    # TODO
    raise NotImplementedError("T3-02：实现 main")


if __name__ == "__main__":
    main()

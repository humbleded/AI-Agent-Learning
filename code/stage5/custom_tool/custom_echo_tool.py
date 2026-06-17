"""
H5-04 Tools 层阅读与新增工具。

运行：
    python code/stage5/custom_tool/custom_echo_tool.py

任务：
    1. 定义一个最小工具类。
    2. 明确 name、description、参数、返回值。
    3. 后续把这个工具接入 HelloAgents 的 registry。
"""


class CustomEchoTool:
    """最小工具类：自己补全 name、description 和 run 方法。

    要求：
      - name: 工具名（字符串）。
      - description: 一句话说明工具做什么。
      - run(self, text): 校验 text 是字符串，返回 {"ok": True, "text": ..., "length": ...}；
        类型不对返回 {"ok": False, "error": ...}。
    """

    # TODO: 定义 name、description 类属性

    def run(self, text):
        # TODO
        raise NotImplementedError("H5-04：实现 CustomEchoTool.run")


def main():
    """实例化工具 -> 打印 name/description -> 读 text 调 run -> 打印结果。"""
    # TODO
    raise NotImplementedError("H5-04：实现 main")


if __name__ == "__main__":
    main()

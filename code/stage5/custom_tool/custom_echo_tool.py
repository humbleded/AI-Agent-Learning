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
    name = "custom_echo"
    description = "返回用户输入，并附带长度信息。"

    def run(self, text):
        if not isinstance(text, str):
            return {"ok": False, "error": "text 必须是字符串"}
        return {"ok": True, "text": text, "length": len(text)}


def main():
    tool = CustomEchoTool()
    text = input("text: ")
    print({"tool": tool.name, "description": tool.description})
    print(tool.run(text))
    print("TODO：阅读 hello_agents/tools/registry.py 后，把本工具注册进去。")


if __name__ == "__main__":
    main()

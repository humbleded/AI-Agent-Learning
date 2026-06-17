"""
A4-Gate 最小 Agent：资料总结与反思修正。

运行：
    python code/stage4/a4_gate_research_summary_agent.py

任务：
    1. 输入主题或资料路径。
    2. 调用工具读取/模拟搜索。
    3. 生成总结。
    4. 反思并修正。
"""

from pathlib import Path

from a4_05_reflection_writer import critique, revise


def load_material(topic_or_path):
    """如果传的是存在的文件路径就读文件内容，否则当成主题返回一段模拟资料。"""
    # TODO
    raise NotImplementedError("A4-Gate：实现 load_material")


def summarize(material):
    """把资料压成一段总结。"""
    # TODO
    raise NotImplementedError("A4-Gate：实现 summarize")


def main():
    """读主题/路径 -> load_material -> summarize 出初稿 -> critique+revise 反思修正 -> 打印终稿。"""
    # TODO
    raise NotImplementedError("A4-Gate：实现 main")


if __name__ == "__main__":
    main()

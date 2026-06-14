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
    path = Path(topic_or_path)
    if path.exists() and path.is_file():
        return path.read_text(encoding="utf-8", errors="replace")
    return f"模拟资料：关于 {topic_or_path} 的三条事实。"


def summarize(material):
    return "总结：" + material[:200]


def main():
    target = input("主题或文件路径：").strip()
    material = load_material(target)
    first_summary = summarize(material)
    tips = critique(first_summary)
    final_summary = revise(first_summary, tips)
    print(final_summary)


if __name__ == "__main__":
    main()

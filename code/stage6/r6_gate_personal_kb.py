"""
R6-Gate 个人知识库问答。

运行：
    python code/stage6/r6_gate_personal_kb.py

任务：
    1. 导入至少 3 篇资料。
    2. 支持问答、引用、无答案拒答。
    3. 当前脚手架从 resources/stage6/*.txt 读取资料。
"""

from pathlib import Path

from r6_02_retrieval import retrieve


ROOT = Path(__file__).resolve().parents[2]
DOC_DIR = ROOT / "resources" / "stage6"


def load_docs():
    """从 DOC_DIR 下的 *.txt 读资料，返回 [{"id","text"}, ...]；目录为空就写一篇示例。"""
    # TODO
    raise NotImplementedError("R6-Gate：实现 load_docs")


def answer(question, docs):
    """检索 docs 回答 question，带引用；检索不到就拒答。"""
    # TODO
    raise NotImplementedError("R6-Gate：实现 answer")


def main():
    """load_docs -> 读问题 -> answer -> 打印。"""
    # TODO
    raise NotImplementedError("R6-Gate：实现 main")


if __name__ == "__main__":
    main()

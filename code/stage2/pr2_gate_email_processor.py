"""
PR2-Gate 结构化输出闯关：邮件处理器。

运行：
    python code/stage2/pr2_gate_email_processor.py

任务：
    1. 输入邮件文本。
    2. 输出分类、摘要、待办 JSON。
    3. 保存到 resources/stage2_email_result.json。
"""

import json
from pathlib import Path

from pr2_02_summarizer import simple_summarize
from pr2_03_classifier import classify
from pr2_04_extract_json import extract_email, validate_payload


ROOT = Path(__file__).resolve().parents[2]
OUT_FILE = ROOT / "resources" / "stage2_email_result.json"


def process_email(text):
    """整合 PR2-02/03/04：对一封邮件同时做分类 + 摘要 + 待办抽取，返回结果 dict。

    步骤：
      1. simple_summarize(text) 得到 points, summary。
      2. extract_email(text) 得到 todo，并用 validate_payload 校验。
      3. classify(text) 得到 category。
      4. 组装成 {"category","points","summary","todo"} 返回。
    """
    # TODO
    raise NotImplementedError("PR2-Gate：实现 process_email")


def main():
    """读邮件文本 -> process_email -> 写入 OUT_FILE -> 打印 JSON 和保存路径。"""
    # TODO
    raise NotImplementedError("PR2-Gate：实现 main")


if __name__ == "__main__":
    main()

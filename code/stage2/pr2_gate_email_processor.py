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
    points, summary = simple_summarize(text)
    todo = extract_email(text)
    validate_payload(todo)
    return {
        "category": classify(text),
        "points": points,
        "summary": summary,
        "todo": todo,
    }


def main():
    text = input("邮件文本：").strip()
    result = process_email(text)
    OUT_FILE.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False, indent=2))
    print("保存到：", OUT_FILE)


if __name__ == "__main__":
    main()

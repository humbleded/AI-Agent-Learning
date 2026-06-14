"""
PR2-04 JSON 与 Schema：邮件信息抽取。

运行：
    python code/stage2/pr2_04_extract_json.py

任务：
    从邮件文本中提取：
    发件人、事项、截止时间、优先级、是否需要回复。
"""

import json


SCHEMA_KEYS = ["sender", "task", "deadline", "priority", "need_reply"]


def extract_email(text):
    """规则版占位；后续替换为 Structured Outputs。"""
    return {
        "sender": None,
        "task": text[:40] if text else None,
        "deadline": None,
        "priority": "normal",
        "need_reply": "回复" in text or "请" in text,
    }


def validate_payload(payload):
    missing = [key for key in SCHEMA_KEYS if key not in payload]
    if missing:
        raise ValueError(f"缺少字段：{missing}")
    json.dumps(payload, ensure_ascii=False)


def main():
    text = input("邮件文本：").strip()
    payload = extract_email(text)
    validate_payload(payload)
    print(json.dumps(payload, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()

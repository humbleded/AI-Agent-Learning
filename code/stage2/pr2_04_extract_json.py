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
    """从邮件文本里抽出 SCHEMA_KEYS 这几个字段，返回一个 dict。

    先做规则版占位（后续替换为模型 Structured Outputs）：
    sender / task / deadline / priority / need_reply。
    """
    # TODO
    raise NotImplementedError("PR2-04：实现 extract_email")


def validate_payload(payload):
    """校验 payload 含全部 SCHEMA_KEYS，且能被 json.dumps 序列化；缺字段就 raise ValueError。"""
    # TODO: 找出缺失字段 -> 缺则 raise ValueError -> json.dumps 验证可序列化
    raise NotImplementedError("PR2-04：实现 validate_payload")


def main():
    """读邮件文本 -> extract_email -> validate_payload -> 打印格式化 JSON。"""
    # TODO
    raise NotImplementedError("PR2-04：实现 main")


if __name__ == "__main__":
    main()

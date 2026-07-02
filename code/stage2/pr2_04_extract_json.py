"""
PR2-04 JSON 与 Schema：邮件信息抽取。

运行：
    python code/stage2/pr2_04_extract_json.py

任务：
    从邮件文本中提取：
    发件人、事项、截止时间、优先级、是否需要回复。
"""

import json
import os
from dotenv import load_dotenv
from openai import OpenAI
load_dotenv()  # 读 .env -> 环境变量
api_key = os.environ.get("DEEPSEEK_API_KEY")


SCHEMA_KEYS = ["sender", "task", "deadline", "priority", "need_reply"]
LABEL_MAP = {"发件人": "sender", "事项": "task", "截止时间": "deadline", "优先级": "priority", "需要回复": "need_reply"}

SAMPLE_EMAIL = """发件人：张三
事项：提交 Q2 季度报告
截止时间：2026-07-05
优先级：高
需要回复：是"""

def extract_email(text):
    """从邮件文本里抽出 SCHEMA_KEYS 这几个字段，返回一个 dict。

    先做规则版占位（后续替换为模型 Structured Outputs）：
    sender / task / deadline / priority / need_reply。
    """
    payload = {}
    for line in text.splitlines():
        if not line.strip():
            continue
        key, sep, value = line.partition("：")
        if not sep:
            continue
        if key in LABEL_MAP:
            payload[LABEL_MAP[key]] = value.strip()
    return payload


def validate_payload(payload):
    """校验 payload 含全部 SCHEMA_KEYS，且能被 json.dumps 序列化；缺字段就 raise ValueError。"""
    missing_keys = [key for key in SCHEMA_KEYS if key not in payload]
    if missing_keys:
        raise ValueError(f"缺失字段: {', '.join(missing_keys)}")
    try:
        return json.dumps(payload, ensure_ascii=False)
    except (TypeError, ValueError) as e:
        raise ValueError(f"无法序列化为 JSON: {e}")
    
def extract_email_llm(text):
    SYSTEM_PROMPT = """
你是一个邮件提取助手,需要从以下【】邮件中提取发件人，事项，截止时间，优先级，需要回复这五个字段和对应的内容，并且把这五个字段翻译成英文的做对应，映射为："发件人": "sender", "事项": "task", "截止时间": "deadline", "优先级": "priority", "需要回复": "need_reply"。然后输出必须为JSON格式，{"sender": "张三", "task": "提交 Q2 季度报告", "deadline": "2026-07-05", "priority": "高", "need_reply": "是"}，且JSON前后不能有文字。如果有字段缺失就填写null,不允许编造一个值出来。不允许多字段。priority枚举值只能在['高','中','低']中选择。
示例：
输入：
【
发件人：张三
事项：提交 Q2 季度报告
截止时间：2026-07-05
优先级：高
需要回复：是
】
输出：{"sender": "张三", "task": "提交 Q2 季度报告", "deadline": "2026-07-05", "priority": "高", "need_reply": "是"}
"""
    messages=[
          {"role": "system", "content": SYSTEM_PROMPT},
          {"role": "user",   "content": f"【{text}】"},
          ]
    client = OpenAI(api_key=api_key, base_url="https://api.deepseek.com",timeout=30,)
    try:
        response = client.chat.completions.create(
            model="deepseek-v4-pro",
            messages=messages,
            stream=False,
            response_format={'type': 'json_object'},
            max_tokens=300,
            timeout=30,
        )
        if not response.choices or not response.choices[0].message:
            return None
        json_content = response.choices[0].message.content
        if not json_content:
            return None
        json_content=json.loads(json_content)  # 将字符串解析为 Python 对象
        return json_content
    except Exception as exc:
        return f"调用模型失败：{exc}"

def main():
    """读邮件文本 -> extract_email -> validate_payload -> 打印格式化 JSON。"""
    # 规则版（结构化邮件）
    payload = extract_email(SAMPLE_EMAIL)
    json_str = validate_payload(payload)
    print("规则版（结构化邮件）:")
    print(json.dumps(payload, ensure_ascii=False, indent=2))

    # 模型版：从自由文本邮件抽取（规则版对没有“标签：”的自由文本抽不到）
    free_text = "张三发来邮件，说下周五 2026-07-05 前把 Q2 季度报告交了，比较急，记得回复他一声。"
    payload_llm = extract_email_llm(free_text)
    print("模型版（自由文本）:")
    print(json.dumps(payload_llm, ensure_ascii=False, indent=2))

    # 缺字段测试：这封没提“优先级”，验证模型是否老实填 null（不编造）
    missing_email = "李四发邮件：请在 2026-07-10 前把用户调研报告整理好发给我，收到请回复确认。"
    payload_missing = extract_email_llm(missing_email)
    print("模型版（缺优先级，验证不编造）:")
    print(json.dumps(payload_missing, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()

"""A4-Gate：研究摘要 Agent。

当前检查点运行方式（项目根目录）：
    .venv/Scripts/python.exe -m py_compile code/stage4/a4_gate_research_summary_agent.py

最终运行方式（全部检查点完成后）：
    .venv/Scripts/python.exe code/stage4/a4_gate_research_summary_agent.py

任务与最终通过标准：
    - 接受研究主题或沙箱内资料相对路径。
    - 调用真实工具取得证据，生成摘要并执行一次 Reflection 校验/修正。
    - 保留最小结构化日志、稳定停止/重试边界和危险动作人工确认门。
    - 通过 10 条正常、3 条失败、1 条危险输入的固定评估集。

当前只实现 C1：固定结果构造与请求输入校验。
后续 Agent 循环、工具适配、Reflection、日志、安全确认和 eval 不在本骨架中提前实现。
"""

from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]  #读取项目根目录
SANDBOX = ROOT / "resources" / "sandbox"  #沙箱目录
ALLOWED_INPUT_TYPES = {"topic", "relative_path"}  #允许的输入类型
ALLOWED_STATUSES = {
    "success",
    "invalid_input",
    "tool_failure",
    "insufficient_evidence",
    "needs_manual",
}  #允许的结果状态
MAX_TOPIC_LENGTH = 50  #主题最大长度

# 构造结果对象的工具函数
def make_result(
    status: str,
    summary: str,
    sources: list[str],
) -> dict[str, object]:
    """构造始终包含 ``status``、``summary``、``sources`` 的结果对象。"""
    return {
        "status": status,
        "summary": summary,
        "sources": sources,
    }

# 校验请求对象的工具函数
def validate_request_shape(
    request: object,
) -> tuple[dict[str, object] | None, str | None]:
    """校验请求是否为字典并包含两个必填字段。"""
    if not isinstance(request, dict):
        return None, "请求必须是字典类型"
    if "input_type" not in request:
        return None, "缺少必填字段 'input_type'"
    if "value" not in request:
        return None, "缺少必填字段 'value'"
    return request, None

# 规范化必填字符串的工具函数
def normalize_required_string(
    raw_value: object,
    field_name: str,
) -> tuple[str | None, str | None]:
    """把必填字符串去除首尾空白；非法时返回具体原因。"""
    if not isinstance(raw_value, str):
        return None, f"字段 '{field_name}' 必须是字符串类型"
    normalized_value = raw_value.strip()
    if not normalized_value:
        return None, f"字段 '{field_name}' 不能为空"
    return normalized_value, None

# 校验输入类型的工具函数
def validate_input_type(input_type: str) -> str | None:
    """输入类型受支持时返回 None，否则返回原因。"""
    if input_type not in ALLOWED_INPUT_TYPES:
        return f"不支持的输入类型 '{input_type}'"
    return None

# 校验主题长度的工具函数
def validate_topic_value(normalized_value: str) -> str | None:
    """主题满足规范化后的长度边界时返回 None，否则返回原因。"""
    if len(normalized_value) > MAX_TOPIC_LENGTH:
        return f"主题长度不能超过 {MAX_TOPIC_LENGTH} 个字符"
    return None


# 校验相对路径的工具函数
def validate_relative_path_value(normalized_value: str) -> str | None:
    """相对路径满足 URL、绝对路径及最终落点边界时返回 None。"""
    if Path(normalized_value).is_absolute():
        return f"相对路径 '{normalized_value}' 不能是绝对路径"
    if "://" in normalized_value:
        return f"相对路径 '{normalized_value}' 不能带://"
    sandbox_root = SANDBOX.resolve()
    target = (sandbox_root / normalized_value).resolve()
    try:
        target.relative_to(sandbox_root)
    except ValueError:
        return f"相对路径 '{normalized_value}' 不在沙箱目录下"
    return None


def prepare_request(
    request: object,
) -> tuple[dict[str, str] | None, dict[str, object] | None]:
    """校验并规范化请求。

    合法请求返回 ``(normalized_request, None)``；其中 ``normalized_request``
    只包含规范化后的 ``input_type`` 与 ``value``。

    非法请求返回 ``(None, invalid_result)``；``invalid_result`` 必须符合
    ``make_result`` 的三字段合同，且不得进入后续模型或工具调用。
    """
    request, error = validate_request_shape(request)
    if error:
        return None, make_result("invalid_input", error, [])
    input_type, value = request["input_type"], request["value"]
    normalized_value, error = normalize_required_string(value, "value")
    if error:
        return None, make_result("invalid_input", error, [])
    normalized_input_type, error = normalize_required_string(input_type, "input_type")
    if error:
        return None, make_result("invalid_input", error, [])
    input_type = normalized_input_type
    error = validate_input_type(input_type)
    if error:
        return None, make_result("invalid_input", error, [])
    if input_type == "topic":
        error = validate_topic_value(normalized_value)
        if error:
            return None, make_result("invalid_input", error, [])
    elif input_type == "relative_path":
        error = validate_relative_path_value(normalized_value)
        if error:
            return None, make_result("invalid_input", error, [])
    normalized_request = {
        "input_type": input_type,
        "value": normalized_value,
    }
    return normalized_request, None

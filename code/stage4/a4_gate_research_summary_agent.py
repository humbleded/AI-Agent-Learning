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

当前已完成 C1：固定结果构造与请求输入校验。
当前已完成 C2a：``read_material`` 工具适配。
当前已完成 C2b：``search_web`` Wikipedia 工具适配。
当前已完成 C3a：注册两个已通过工具，并构造模型可见的工具 Schema。
当前已完成 C3b：严格校验一个模型工具请求，并只执行与规范化请求一致的白名单工具。
当前已完成 C3c：真实 DeepSeek 双路径选择工具、Observation 回填与候选摘要正常链。
当前已完成 C3d-C1：从本轮真实工具结果构造允许来源白名单。
当前已完成 C3d-C2a：构造包含完整证据与成功合同的 Reflection prompt。
当前已完成 C3d-C2b：构造证据受限、JSON-only 的 Refinement prompt。
当前已完成 C3d-C3a：最终 success 候选的客户端硬校验。
当前已完成 C3d-I1：Reflection 单次模型调用与响应外壳。
当前已完成 C3d-I2：Refinement JSON Output 调用与语法解析。
当前已完成 C3d-I3：Reflection → Refinement → validator 两段编排。
当前已完成 C3d-I4：原始请求到可信结果的正常路径接线与真实双路径验证。
当前已完成 C4a-1a：初始化单次请求共享的运行上下文。
当前已完成 C4a-1b：调用前硬门与共享占步，并已接入现有模型 / 工具调用链。
当前已完成 C4a-1c：追加固定七字段调用事件，并已接入现有模型 / 工具调用链。
当前已完成 C4a-1d：补齐第二候选响应的 ``finish_reason`` 守门。
当前已完成 C4a-1e：第一次模型调用的占步、计时与成功 / 异常日志。
当前已完成 C4a-1f：真实工具调用的占步、计时与成功 / 异常日志。
当前已完成 C4a-1g：第二次模型调用的占步、计时与成功 / 异常日志。
当前已完成 C4a-1h：Reflection 模型调用的占步、计时与成功 / 异常日志。
当前已完成 C4a-1i：Refinement 模型调用的占步、计时与成功 / 异常日志。
当前已完成 C4a-1j：首次模型 ``finish_reason == "tool_calls"`` 守门。
当前已完成 C4a-1k：无重试五步轨迹、请求隔离与第 7 次调用硬门整体验收。
后续 C4a-2 重试 / 失败状态映射、安全确认和 eval 尚未完成；当前无活动 TODO。
"""

import html
import json
import os
from pathlib import Path
import re
from time import perf_counter
import uuid

from dotenv import load_dotenv
from openai import OpenAI
import requests

ROOT = Path(__file__).resolve().parents[2]  # 读取项目根目录
SANDBOX = ROOT / "resources" / "sandbox"  # 沙箱目录
ALLOWED_INPUT_TYPES = {"topic", "relative_path"}  # 允许的输入类型
ALLOWED_STATUSES = {
    "success",
    "invalid_input",
    "tool_failure",
    "insufficient_evidence",
    "needs_manual",
}  # 允许的结果状态
MAX_TOPIC_LENGTH = 50  # 主题最大长度
MAX_MATERIAL_CHARS = 1000  # 沿用已 PASS 的 T3-03 默认截断上限
WIKIPEDIA_API_URL = "https://zh.wikipedia.org/w/api.php"  # 中文 Wikipedia API URL
WIKIPEDIA_PAGE_URL_TEMPLATE = "https://zh.wikipedia.org/w/index.php?curid={page_id}"  # 中文 Wikipedia 页面 URL 模板
WIKIPEDIA_USER_AGENT = "AI-Agent-Learning/0.1 (https://github.com/humbleded/AI-Agent-Learning)"  # 中文 Wikipedia 请求使用的 User-Agent
SEARCH_TIMEOUT_SECONDS = 5
MAX_SEARCH_RESULTS = 3  # 最大搜索结果条数
DEEPSEEK_BASE_URL = "https://api.deepseek.com"
DEEPSEEK_MODEL = "deepseek-v4-pro"
MAX_STEPS = 6
CALL_LOG_FIELDS = (
    "request_id",
    "step",
    "event_type",
    "model",
    "tool_name",
    "duration_ms",
    "error",
)

# 初始化单次请求共享的运行上下文的工具函数
def create_run_context(
    request_id: str | None = None,
) -> dict[str, object]:
    """初始化一个请求内共享的运行上下文。

    当前检查点只建立 ``request_id``、初始 ``step`` 和空 ``logs``；
    不调用模型或工具，不记录事件，也不修改现有 Agent 正常链。
    """
    if request_id is None:
        request_id = uuid.uuid4().hex
    else:
        if not isinstance(request_id, str):
            raise ValueError("显式 request_id 必须是字符串类型")
        request_id = request_id.strip()
        if not request_id:
            raise ValueError("显式 request_id 不能为空")
    return {
        "request_id": request_id,
        "step": 0,
        "logs": [],
    }

# 占用调用步骤的工具函数, 在真实模型或工具调用前使用, 返回当前调用的 step。判断是否超过最大步骤限制。
def reserve_call_step(
    run_context: dict[str, object],
) -> int:
    """在真实模型或工具调用前，占用并返回本次调用的共享 step。"""
    if not isinstance(run_context, dict):
        raise ValueError("run_context 必须是字典类型")
    if "step" not in run_context:
        raise ValueError("run_context 缺失 'step' 字段")
    step = run_context["step"]
    if type(step) is not int or step < 0:
        raise ValueError("run_context 中的 'step' 必须是非负整数")
    if step == MAX_STEPS:
        raise RuntimeError("已达到最大步骤限制")
    if step > MAX_STEPS:
        raise ValueError("run_context 中的 'step' 超过最大步骤限制")
    run_context["step"] = step + 1
    return run_context["step"]

# 追加调用日志的工具函数
def append_call_log(
    run_context: dict[str, object],
    *,
    step: int,
    event_type: str,
    model: str | None,
    tool_name: str | None,
    duration_ms: int,
    error: str | None,
) -> dict[str, object]:
    """校验、追加并返回一条固定七字段调用事件。"""
    if not isinstance(run_context, dict):
        raise ValueError("run_context 必须是字典类型")
    if "logs" not in run_context:
        raise ValueError("run_context 缺失 'logs' 字段")
    if not isinstance(run_context["logs"], list):
        raise ValueError("run_context 中的 'logs' 字段必须是列表类型")
    if not type(step) is int or step < 0:
        raise ValueError("step 必须是非负整数")
    if not type(run_context.get("step")) is int or run_context.get("step") < 0:
        raise ValueError("run_context 中的 'step' 字段必须是非负整数")
    if step < 1 or step > MAX_STEPS:
        raise ValueError("step 必须大于等于 1 且不超过最大步骤限制")
    if run_context.get("step") < 1 or run_context.get("step") > MAX_STEPS:
        raise ValueError("run_context 中的 'step' 必须大于等于 1 且不超过最大步骤限制")
    if step != run_context.get("step"):
        raise ValueError("step 与当前 run_context 中的 'step' 不一致")
    if event_type not in ("model_call", "tool_call"):
        raise ValueError("event_type 必须是 'model_call' 或 'tool_call'")
    if event_type == "model_call":
        if not (
            isinstance(model, str)
            and model.strip() != ""
            and tool_name is None
        ):
            raise ValueError(
                "model_call 的 model 必须为非空字符串，tool_name 必须为 None"
            )
    elif event_type == "tool_call":
        if not (
            isinstance(tool_name, str)
            and tool_name.strip() != ""
            and model is None
        ):
            raise ValueError(
                "tool_call 的 tool_name 必须为非空字符串，model 必须为 None"
            )
    if not type(duration_ms) is int or duration_ms < 0:
        raise ValueError("duration_ms 必须是非负整数")
    if not (error is None or isinstance(error, str)):
        raise ValueError("error 必须是字符串类型或 None")
    if error is not None and error.strip() == "":
        raise ValueError("error 字段不能为空字符串")
    if run_context.get("request_id") is None:
        raise ValueError("run_context 缺失 'request_id' 字段")
    if not isinstance(run_context.get("request_id"), str):
        raise ValueError("run_context 中的 'request_id' 字段必须是字符串类型")
    if run_context.get("request_id").strip() == "":
        raise ValueError("run_context 中的 'request_id' 字段不能为空")
    log_entry = {
        "request_id": run_context.get("request_id"),
        "step": step,
        "event_type": event_type,
        "model": model,
        "tool_name": tool_name,
        "duration_ms": duration_ms,
        "error": error,
    }
    run_context["logs"].append(log_entry)
    return log_entry


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

# 校验并规范化请求的工具函数
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


def read_material(relative_path: str) -> dict[str, object]:
    """读取沙箱内资料并转换成 Problem Contract 规定的工具结果。"""
    relative_path, error = normalize_required_string(relative_path, "relative_path")
    if error:
        return {"ok": False, "error": error, "retryable": False}
    error = validate_relative_path_value(relative_path)
    if error:
        return {"ok": False, "error": error, "retryable": False}

    # 解析沙箱与目标的最终落点；归属检查已由上面的校验函数完成。
    sandbox_root = SANDBOX.resolve()
    target = (sandbox_root / relative_path).resolve()

    if not target.exists():
        return {
            "ok": False,
            "error": f"文件 '{relative_path}' 不存在",
            "retryable": False,
        }
    if not target.is_file():
        return {
            "ok": False,
            "error": f"文件 '{relative_path}' 不是普通文件",
            "retryable": False,
        }

    # 读取文件内容并截断，捕获 UnicodeDecodeError 与 OSError，返回固定 ok/error/retryable 字段。
    try:
        with open(target, "r", encoding="utf-8") as f:
            text = f.read()
            content = text[:MAX_MATERIAL_CHARS]
            truncated = len(text) > MAX_MATERIAL_CHARS
    except UnicodeDecodeError as e:
        return {
            "ok": False,
            "error": f"读取文件 '{relative_path}' 失败: {e}",
            "retryable": False,
        }
    except OSError as e:
        return {
            "ok": False,
            "error": f"读取文件 '{relative_path}' 失败: {e}",
            "retryable": False,
        }

    return {"ok": True, "content": content, "truncated": truncated}


# 搜索中文 Wikipedia 并返回固定 ok/results 或 ok/error/retryable 字段。
def search_web(query: str) -> dict[str, object]:
    """搜索中文 Wikipedia 并转换成 Problem Contract 规定的工具结果。"""
    normalized_query, error = normalize_required_string(
        query, "query"
    )  # 规范化查询字符串
    if error:
        return {"ok": False, "error": error, "retryable": False}
    error = validate_topic_value(normalized_query)  # 复用主题长度校验
    if error:
        return {"ok": False, "error": error, "retryable": False}

    params = {  # MediaWiki API 请求参数
        "action": "query",  # 查询操作
        "list": "search",  # 搜索列表
        "srsearch": normalized_query,  # 搜索关键词
        "format": "json",  # 返回 JSON 格式
        "srnamespace": 0,  # 只搜索百科正文
        "srlimit": MAX_SEARCH_RESULTS,  # 限制返回条数
        "srprop": "snippet",  # 只返回摘要片段，不返回全文
        "formatversion": 2,  # 使用更现代的 JSON 格式
        "utf8": 1,  # 确保返回 UTF-8 编码
    }
    headers = {
        "User-Agent": WIKIPEDIA_USER_AGENT  # 描述性 User-Agent，便于识别请求来源
    }
    try:
        response = requests.get(
            WIKIPEDIA_API_URL,
            params=params,
            headers=headers,
            timeout=SEARCH_TIMEOUT_SECONDS,
            allow_redirects=False,
        )
        # 按合同显式分类 HTTP 状态，并在非 2xx 时停止解析响应正文。
        status_code = response.status_code
        if status_code >= 300 and status_code < 400:
            return {
                "ok": False,
                "error": f"请求被重定向，状态码: {status_code}",
                "retryable": False,
            }
        elif status_code >= 500 or status_code == 429:
            return {
                "ok": False,
                "error": f"请求失败，状态码: {status_code}",
                "retryable": True,
            }
        elif status_code >= 400 and status_code < 500:
            return {
                "ok": False,
                "error": f"请求失败，状态码: {status_code}",
                "retryable": False,
            }
        elif status_code < 200:
            return {
                "ok": False,
                "error": f"请求失败，状态码: {status_code}",
                "retryable": False,
            }
        # data是一个字典，包含了 API 返回的 JSON 数据。我们可以通过 response.json() 方法将响应内容解析为 Python 字典。
        data = response.json()
    except requests.Timeout:
        return {"ok": False, "error": "请求超时", "retryable": True}
    except requests.exceptions.JSONDecodeError as e:
        return {"ok": False, "error": f"解析 JSON 失败: {e}", "retryable": True}
    except requests.RequestException as e:
        return {"ok": False, "error": f"请求失败: {e}", "retryable": False}
    # 处理 API 返回的搜索结果，确保每条结果都有 title、pageid、snippet，并进行必要的清理。
    if not isinstance(data, dict):
        return {"ok": False, "error": "API 返回的 JSON 结构不正确", "retryable": False}
    if "error" in data:
        return {"ok": False, "error": f"API 错误: {data['error']}", "retryable": False}
    if "query" not in data or not isinstance(data.get("query"), dict):
        return {"ok": False, "error": "API 返回的搜索结果结构不正确", "retryable": False}
    if "search" not in data["query"] or not isinstance(data["query"].get("search"), list):
        return {"ok": False, "error": "API 返回的搜索结果列表不正确", "retryable": False}
    # 如果没有错误，继续处理搜索结果。取出 data 中的 query.search 列表，最多取 MAX_SEARCH_RESULTS 条结果。
    search_results = data.get("query", {}).get("search", [])
    results = []
    for item in search_results[:MAX_SEARCH_RESULTS]:
        if not isinstance(item, dict):
            return {"ok": False, "error": "搜索结果条目结构不正确", "retryable": False}
        title = item.get("title")
        pageid = item.get("pageid")
        snippet = item.get("snippet")
        if (
            not isinstance(title, str)
            or not (type(pageid) is int and pageid > 0)
            or not isinstance(snippet, str)
        ):
            return {"ok": False, "error": "搜索结果条目缺少必要字段", "retryable": False}
        url = WIKIPEDIA_PAGE_URL_TEMPLATE.format(page_id=pageid)  # 使用 pageid 构造 URL
        snippet = re.sub(r"<.*?>", "", snippet)  # 去除 HTML 标签，保留纯文本内容
        snippet = html.unescape(
            snippet
        )  # 还原 HTML 实体，例如 &amp; 转换为 &，&lt; 转换为 <，&gt; 转换为 > 等。
        # 具体的搜索结果条目包含 title、url、snippet 三个字段
        results.append({"title": title, "url": url, "snippet": snippet})

    return {"ok": True, "results": results}


# C3a 只建立模型工具描述与客户端函数白名单；不得在注册时执行工具。
TOOL_REGISTRY: dict[str, object] = {
    "read_material": read_material,
    "search_web": search_web,
}


def build_tool_schemas() -> list[dict[str, object]]:
    """构造提供给模型的两个只读函数工具 Schema。"""
    read_material_schema = {
        "type": "function",
        "function": {
            "name": "read_material",
            "description": (
                "只有读取沙箱内资料的权限，输入必须是规范化的相对路径，"
                "路径必须在 resources/sandbox/ 下,工具用于读取该路径对应的资料内容"
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "relative_path": {
                        "type": "string",
                        "description": "必须是相对于 resources/sandbox/ 的规范化路径",
                    }
                },
                "required": ["relative_path"],
                "additionalProperties": False,
            },
        },
    }
    search_web_schema = {
        "type": "function",
        "function": {
            "name": "search_web",
            "description": (
                "这是一个只读工具，query必须是已经规范化的topic，"
                "当前搜索后端仅为中文 Wikipedia，它不代表整个公开互联网或通用网页搜索"
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "必须是已经规范化的 topic",
                    }
                },
                "required": ["query"],
                "additionalProperties": False,
            },
        },
    }
    return [read_material_schema, search_web_schema]

# 执行模型工具调用的统一入口，负责参数校验、白名单检查以及实际调用工具函数。
def execute_tool_call(
    tool_name: object,
    raw_arguments: object,
    normalized_request: dict[str, str],
    *,
    run_context: dict[str, object],
) -> dict[str, object]:
    """校验一个模型工具请求，执行匹配的白名单工具并返回真实工具结果。"""
    if not isinstance(tool_name, str):
        return {"ok": False, "error": "工具名必须是字符串", "retryable": False}
    tool_function = TOOL_REGISTRY.get(tool_name)
    if tool_function is None:
        return {"ok": False, "error": f"未注册的工具: {tool_name}", "retryable": False}
    try:
        if not isinstance(raw_arguments, str):
            return {"ok": False, "error": "工具参数必须是 JSON 字符串", "retryable": False}
        if not raw_arguments.strip():
            return {"ok": False, "error": "工具参数不能为空", "retryable": False}
        arguments = json.loads(raw_arguments)
        if not isinstance(arguments, dict):
            return {"ok": False, "error": "工具参数必须是 JSON 对象", "retryable": False}
    except json.JSONDecodeError as e:
        return {"ok": False, "error": f"解析工具参数失败: {e}", "retryable": False}

    # 校验参数是否符合工具的 Schema
    tool_schemas = {schema["function"]["name"]: schema for schema in build_tool_schemas()}
    schema = tool_schemas.get(tool_name)
    if schema is None:
        return {"ok": False, "error": f"未找到工具的 Schema: {tool_name}", "retryable": False}
    required_fields = (
        schema.get("function", {}).get("parameters", {}).get("required", [])
    )
    for field in required_fields:
        if field not in arguments:
            return {"ok": False, "error": f"缺少必要的工具参数: {field}", "retryable": False}
    additional_properties = (
        schema.get("function", {})
        .get("parameters", {})
        .get("additionalProperties", True)
    )
    if not additional_properties:
        for field in arguments:
            if field not in required_fields:
                return {"ok": False, "error": f"存在多余的工具参数: {field}", "retryable": False}
    # 校验参数类型是否符合要求
    properties = schema.get("function", {}).get("parameters", {}).get("properties", {})
    for field, field_schema in properties.items():
        if field in arguments:
            expected_type = field_schema.get("type")
            if expected_type == "string" and not isinstance(arguments[field], str):
                return {"ok": False, "error": f"工具参数 {field} 类型不正确，期望为字符串", "retryable": False}

    # 校验工具调用的参数是否与 normalized_request 完全一致。
    if tool_name == "read_material":
        if "relative_path" not in arguments:
            return {"ok": False, "error": "缺少必要的工具参数: relative_path", "retryable": False}
        if normalized_request.get("input_type") != "relative_path":
            return {"ok": False, "error": "工具调用的 input_type 与 normalized_request 不一致", "retryable": False}
        if arguments["relative_path"] != normalized_request.get("value"):
            return {"ok": False, "error": "工具调用的 relative_path 与 normalized_request 不一致", "retryable": False}
    elif tool_name == "search_web":
        if "query" not in arguments:
            return {"ok": False, "error": "缺少必要的工具参数: query", "retryable": False}
        if normalized_request.get("input_type") != "topic":
            return {"ok": False, "error": "工具调用的 input_type 与 normalized_request 不一致", "retryable": False}
        if arguments["query"] != normalized_request.get("value"):
            return {"ok": False, "error": "工具调用的 query 与 normalized_request 不一致", "retryable": False}
    else:
        return {"ok": False, "error": f"未知的工具: {tool_name}", "retryable": False}

    # C4a-1f-R1：只有上述客户端校验全部通过后，才占用一次真实工具 step。
    step = reserve_call_step(run_context)
    perf_counter_start = perf_counter()

    try:
        result = tool_function(**arguments)
    except Exception as exc:
        perf_counter_end = perf_counter()
        duration_ms = max(
            0,
            int((perf_counter_end - perf_counter_start) * 1000),
        )
        append_call_log(
            run_context,
            step=step,
            event_type="tool_call",
            model=None,
            tool_name=tool_name,
            duration_ms=duration_ms,
            error=type(exc).__name__,
        )
        raise
    else:
        perf_counter_end = perf_counter()
        duration_ms = max(
            0,
            int((perf_counter_end - perf_counter_start) * 1000),
        )

        if result.get("ok") is True:
            log_error = None
        elif result.get("retryable") is True:
            log_error = "retryable_tool_failure"
        else:
            log_error = "tool_failure"

        append_call_log(
            run_context,
            step=step,
            event_type="tool_call",
            model=None,
            tool_name=tool_name,
            duration_ms=duration_ms,
            error=log_error,
        )

        return result


def create_deepseek_client() -> OpenAI:
    """复用已 PASS 配置，创建真实 DeepSeek 客户端但不发起模型调用。"""
    load_dotenv()
    api_key = os.environ.get("DEEPSEEK_API_KEY")
    if not api_key:
        raise RuntimeError("DeepSeek API key is missing.")
    return OpenAI(api_key=api_key, base_url=DEEPSEEK_BASE_URL)

# 生成候选摘要的工具函数
def generate_candidate_summary(
    normalized_request: dict[str, str],
    client: OpenAI | None = None,
    *,
    run_context: dict[str, object],
) -> dict[str, object]:
    """运行一次两轮正常链，返回候选摘要与本轮真实工具证据。

    返回的是 Reflection 前的中间对象，不得在这里标记最终 ``success``。
    """
    messages = [
        {
            "role": "system",
            "content": """你是一个研究摘要 Agent，如果输出的类型是topic，那么你负责根据用户提供的主题或沙箱内资料路径，
调用工具search_web获取证据，并生成研究摘要。如果输出的类型是relative_path，那么你负责根据用户提供的沙箱内资料路径，
调用工具read_material获取证据，并生成研究摘要。请确保在生成摘要时，引用的证据来源必须来自于你调用的工具返回的结果。
参数必须原样使用规范化 value，不能在取得 Observation 前直接写摘要，后续摘要只能依据真实 Observation生成。
你必须严格遵守工具调用的参数规范，不能使用未注册的工具，也不能使用未规范化的参数。
""",
        },
        {
            "role": "user",
            "content": json.dumps(normalized_request, ensure_ascii=False),
        },
    ]
    tool_schemas = build_tool_schemas()
    if client is None:
        client = create_deepseek_client()
    call_step = reserve_call_step(run_context)
    perf_counter_start = perf_counter()
    # 第一次调用模型，获取工具调用
    try:
        response1 = client.chat.completions.create(
            model=DEEPSEEK_MODEL,
            messages=messages,
            tools=tool_schemas,
            stream=False,
            extra_body={"thinking": {"type": "disabled"}},
        )
    except Exception as e:
        perf_counter_end = perf_counter()
        append_call_log(
            run_context,
            error=type(e).__name__,  # 记录异常类型而不是异常对象本身
            duration_ms=max(
                0,
                int((perf_counter_end - perf_counter_start) * 1000),
            ),
            step=call_step,
            event_type="model_call",
            model=DEEPSEEK_MODEL,
            tool_name=None,
        )
        raise
    else:
        perf_counter_end = perf_counter()
        duration_ms = max(
            0,
            int((perf_counter_end - perf_counter_start) * 1000),
        )
        append_call_log(
            run_context,
            step=call_step,
            event_type="model_call",
            model=DEEPSEEK_MODEL,
            tool_name=None,
            duration_ms=duration_ms,
            error=None,
        )
    if response1.choices is None or len(response1.choices) == 0:
        raise RuntimeError("模型未返回任何选择")
    # 第一次模型必须明确以工具调用结束，才允许读取并执行 tool_calls。
    if not hasattr(response1.choices[0], "finish_reason"):
        raise RuntimeError("首次模型调用缺少 finish_reason 字段")

    if response1.choices[0].finish_reason != "tool_calls":
        raise RuntimeError("首次模型调用未以工具调用结束")

    assistant_message = response1.choices[0].message
    if assistant_message is None:
        raise RuntimeError("第一次模型调用未返回任何消息")
    tool_calls = assistant_message.tool_calls
    if tool_calls is None or len(tool_calls) == 0:
        raise RuntimeError("模型未返回任何工具调用")
    if len(tool_calls) != 1:
        raise RuntimeError(f"模型返回了 {len(tool_calls)} 个工具调用，期望恰好 1 个")
    if tool_calls[0].function is None or tool_calls[0].function.name is None:
        raise RuntimeError("模型返回的工具调用缺少函数名")

    tool_call = tool_calls[0]
    tool_call_id = tool_call.id
    tool_name = tool_call.function.name
    raw_arguments = tool_call.function.arguments
    if not isinstance(tool_call_id, str) or tool_call_id.strip() == "":
        raise RuntimeError("工具调用 ID 必须是非空字符串")
    tool_result = execute_tool_call(
        tool_name,
        raw_arguments,
        normalized_request,
        run_context=run_context,
    )
    if tool_result.get("ok") is not True:
        raise RuntimeError(f"工具调用失败: {tool_result.get('error', '无法生成正常候选摘要')}")
    # 回填工具结果到消息中
    tool_result_message = {
        "role": "tool",
        "tool_call_id": tool_call_id,
        "content": json.dumps(tool_result, ensure_ascii=False),
    }
    messages.append(assistant_message)  # 添加模型的完整 assistant 消息
    messages.append(tool_result_message)  # 添加工具结果消息
    # 第二次调用模型，获取候选摘要
    call_step = reserve_call_step(run_context)
    perf_counter_start = perf_counter()
    try:
        response2 = client.chat.completions.create(
            model=DEEPSEEK_MODEL,
            messages=messages,
            tools=tool_schemas,
            stream=False,
            extra_body={"thinking": {"type": "disabled"}},
            tool_choice="none",
        )
    except Exception as e:
        perf_counter_end = perf_counter()
        append_call_log(
            run_context,
            error=type(e).__name__,  # 记录异常类型而不是异常对象本身
            duration_ms=max(
                0,
                int((perf_counter_end - perf_counter_start) * 1000),
            ),
            step=call_step,
            event_type="model_call",
            model=DEEPSEEK_MODEL,
            tool_name=None,
        )
        raise
    else:
        perf_counter_end = perf_counter()
        append_call_log(
            run_context,
            error=None,
            duration_ms=max(
                0,
                int((perf_counter_end - perf_counter_start) * 1000),
            ),
            step=call_step,
            event_type="model_call",
            model=DEEPSEEK_MODEL,
            tool_name=None,
        )

    if response2.choices is None or len(response2.choices) == 0:
        raise RuntimeError("第二次模型调用未返回任何选择")

    choice2 = response2.choices[0]
    if hasattr(choice2, "finish_reason") is False:
        raise RuntimeError("第二次模型调用的选择缺少 finish_reason 字段")
    finish_reason = choice2.finish_reason
    if finish_reason != "stop":
        raise RuntimeError(f"第二次模型调用未正常结束，finish_reason: {finish_reason}")
    assistant_message2 = choice2.message
    if assistant_message2 is None or assistant_message2.content is None:
        raise RuntimeError("模型未返回候选摘要")
    if assistant_message2.tool_calls is not None and len(assistant_message2.tool_calls) > 0:
        raise RuntimeError("模型在第二次调用中不应返回工具调用")
    if not isinstance(assistant_message2.content, str) or assistant_message2.content.strip() == "":
        raise RuntimeError("模型返回的候选摘要不是非空字符串类型")

    candidate_summary = assistant_message2.content
    return {
        "candidate_summary": candidate_summary,
        "tool_name": tool_name,
        "tool_result": tool_result,
    }

# 判断候选摘要的合法来源，构造来源白名单。
def derive_allowed_sources(
    normalized_request: dict[str, str],
    tool_name: str,
    tool_result: dict[str, object],
) -> list[str]:
    """根据规范化请求和本轮成功工具结果构造来源白名单。

    合法输入返回保持工具结果顺序的 ``list[str]``；结构、路由或来源字段
    不符合当前合同的输入抛出 ``ValueError``。本函数不调用模型或工具，
    不生成摘要，也不构造最终 ``success`` 结果。
    """
    if tool_result.get("ok") is not True:
        raise ValueError("工具结果不成功，无法构造来源白名单")
    if tool_name == "read_material":
        if normalized_request.get("input_type") != "relative_path":
            raise ValueError("工具名与 input_type 路由不一致")
        relative_path = normalized_request.get("value")
        if not isinstance(relative_path, str) or relative_path.strip() == "":
            raise ValueError("规范化请求缺少 value 字段")
        return [relative_path]
    elif tool_name == "search_web":
        if normalized_request.get("input_type") != "topic":
            raise ValueError("工具名与 input_type 路由不一致")
        results = tool_result.get("results")
        if not isinstance(results, list):
            raise ValueError("工具结果缺少 results 字段或类型不正确")
        sources = []
        for item in results:
            if not isinstance(item, dict):
                raise ValueError("工具结果中的条目不是字典类型")
            url = item.get("url")
            if not isinstance(url, str) or url.strip() == "":
                raise ValueError("工具结果中的 url 字段非法")
            sources.append(url)
        return sources
    else:
        raise ValueError(f"未知的工具: {tool_name}")

# 构造 Reflection prompt
def build_reflection_prompt(
    normalized_request: dict[str, str],
    candidate_summary: str,
    tool_name: str,
    tool_result: dict[str, object],
    allowed_sources: list[str],
) -> str:
    """构造只依据本轮真实证据评审候选摘要的 Reflection prompt。

    本函数只返回 prompt 文本，不调用模型或工具，不解析 / 修订候选，
    也不构造最终 ``success`` 结果。
    """
    if not isinstance(candidate_summary, str) or candidate_summary.strip() == "":
        raise ValueError("候选摘要必须是非空字符串")
    if not isinstance(tool_name, str) or tool_name.strip() == "":
        raise ValueError("工具名必须是非空字符串")
    if not isinstance(tool_result, dict):
        raise ValueError("工具结果必须是字典类型")
    if not isinstance(allowed_sources, list) or not all(
        isinstance(source, str) for source in allowed_sources
    ):
        raise ValueError("allowed_sources 必须是字符串列表")
    if tool_name == "read_material":
        if "content" not in tool_result:
            raise ValueError("工具结果缺少 content 字段")
    elif tool_name == "search_web":
        if "results" not in tool_result:
            raise ValueError("工具结果缺少 results 字段")
    review_instructions = (
        "请逐项检查候选摘要是否由本轮工具结果支持，"
        "摘要结论只能依据本轮 read_material.content 或 search_web.results。"
        "不得使用模型常识补充工具没有取得的事实。"
        "allowed_sources 只能证明来源来自本轮 Observation，不能替代正文证据。"
        "成功候选的具体合同："
        "status 必须是字符串 \"success\"；"
        "summary 必须是非空字符串；"
        "sources 必须是非空字符串列表；"
        "sources 必须是 allowed_sources 的子集。"
        "有问题时逐项输出“问题、证据、修改建议”。"
        "全部通过时只输出精确短语“无需改进”。"
    )

    prompt = {
        "normalized_request": normalized_request,
        "candidate_summary": candidate_summary,
        "tool_name": tool_name,
        "tool_result": tool_result,
        "allowed_sources": allowed_sources,
    }
    prompt["review_instructions"] = review_instructions
    return json.dumps(prompt, ensure_ascii=False)

# 构造 Refinement prompt
def build_refinement_prompt(
    normalized_request: dict[str, str],
    candidate_summary: str,
    tool_name: str,
    tool_result: dict[str, object],
    allowed_sources: list[str],
    feedback: str,
) -> str:
    """构造依据 Reflection 反馈生成结构化候选的 Refinement prompt。

    本函数只返回 prompt 文本，不调用模型或工具，不解析模型输出，
    也不执行最终客户端硬校验。
    """
    refinement_instructions = (
        "请根据 Reflection 反馈对候选摘要进行修订，"
        "修订应严格依据本轮工具结果，不得添加模型常识。"
        "文件路径分支只能依据 read_material.content；搜索分支只能依据 search_web.results。"
        "只输出一个 JSON 对象；JSON 前后不得有任何解释、标题、提示语或其他文字。"
        "不得使用 Markdown 代码围栏（```）包装 JSON。"
        "sources 必须从 allowed_sources 中选择，不能扩大白名单。"
        "JSON 对象的键必须恰好是 status、summary、sources；不得增加其他键。"
        "示例：{\"status\": \"success\", \"summary\": \"...\", \"sources\": [\"...\"]}。"
        "成功候选必须满足：status == \"success\"，summary 为非空字符串，"
        "sources 为非空字符串列表且是 allowed_sources 的子集。"
        "如果反馈为“无需改进”，保留候选事实含义；"
        "其他反馈只依据本轮证据修订。"
    )

    prompt = {
        "normalized_request": normalized_request,
        "candidate_summary": candidate_summary,
        "tool_name": tool_name,
        "tool_result": tool_result,
        "allowed_sources": allowed_sources,
        "feedback": feedback,
    }
    prompt["refinement_instructions"] = refinement_instructions
    return json.dumps(prompt, ensure_ascii=False)

# 硬校验候选摘要并返回固定三字段的 success 结果
def validate_success_result(
    candidate: object,
    allowed_sources: list[str],
) -> dict[str, object]:
    """硬校验模型候选，并返回固定三字段的 ``success`` 结果。

    本函数不调用模型或工具；任何结构、类型、成功非空条件或来源子集
    不符合合同的输入都抛出 ``ValueError``。
    """
    if (
        not isinstance(allowed_sources, list)
        or not allowed_sources
        or not all(
            isinstance(source, str) and source.strip() != ""
            for source in allowed_sources
        )
    ):
        raise ValueError("allowed_sources 必须是非空字符串列表")
    if not isinstance(candidate, dict):
        raise ValueError("候选摘要必须是字典类型")
    expected_keys = {"status", "summary", "sources"}
    if set(candidate.keys()) != expected_keys:
        raise ValueError(f"候选摘要的键必须恰好是 {expected_keys}")
    status = candidate.get("status")
    if not isinstance(status, str) or status != "success":
        raise ValueError("status 必须是字符串 'success'")
    summary = candidate.get("summary")
    if not isinstance(summary, str) or summary.strip() == "":
        raise ValueError("summary 必须是非空字符串")
    sources = candidate.get("sources")
    if (
        not isinstance(sources, list)
        or not sources
        or not all(
            isinstance(source, str) and source.strip() != ""
            for source in sources
        )
    ):
        raise ValueError("sources 必须是非空字符串列表")
    if not set(sources).issubset(set(allowed_sources)):
        raise ValueError("sources 必须是 allowed_sources 的子集")
    return make_result("success", summary.strip(), sources)


# 调用 Reflection 并获取反馈文本
def request_reflection_feedback(
    reflection_prompt: str,
    client: OpenAI | None = None,
    *,
    run_context: dict[str, object],
) -> str:
    """调用一次 Reflection，并返回经过外壳检查的非空反馈文本。

    当前检查点只负责一次模型请求和响应外壳，不构造 Refinement prompt，
    不解析 JSON，也不构造最终三字段结果。
    """
    if not isinstance(reflection_prompt, str) or reflection_prompt.strip() == "":
        raise ValueError("reflection_prompt 必须是非空字符串")
    if client is None:
        client = create_deepseek_client()
    step = reserve_call_step(run_context)
    perf_counter_start = perf_counter()
    try:
        response = client.chat.completions.create(
            model=DEEPSEEK_MODEL,
            messages=[
                {
                    "role": "user",
                    "content": reflection_prompt,
                }
            ],
            stream=False,
            extra_body={"thinking": {"type": "disabled"}},
        )
    except Exception as e:
        perf_counter_end = perf_counter()
        duration_ms = max(
            0,
            int((perf_counter_end - perf_counter_start) * 1000),
        )
        append_call_log(
            run_context,
            error=type(e).__name__,  # 记录异常类型而不是异常对象本身
            duration_ms=duration_ms,
            step=step,
            event_type="model_call",
            model=DEEPSEEK_MODEL,
            tool_name=None,
        )
        raise
    else:
        perf_counter_end = perf_counter()
        duration_ms = max(
            0,
            int((perf_counter_end - perf_counter_start) * 1000),
        )
        append_call_log(
            run_context,
            error=None,
            duration_ms=duration_ms,
            step=step,
            event_type="model_call",
            model=DEEPSEEK_MODEL,
            tool_name=None,
        )

    if response is None:
        raise RuntimeError("Reflection 响应为空")
    if hasattr(response, "choices") is False:
        raise RuntimeError("Reflection 响应缺少 choices 字段")
    choices = response.choices
    if not isinstance(choices, list) or not choices:
        raise RuntimeError("Reflection 响应缺少 choices 字段或类型不正确")
    if hasattr(choices[0], "message") is False:
        raise RuntimeError("Reflection 响应中的 message 字段为空")
    message = choices[0].message
    if hasattr(choices[0], "finish_reason") is False:
        raise RuntimeError("Reflection 响应中的 finish_reason 字段为空")
    finish_reason = choices[0].finish_reason
    if finish_reason != "stop":
        raise RuntimeError("Reflection 未以 stop 结束")
    # message.tool_calls 必须是 None 或空列表
    if hasattr(message, "tool_calls") is False:
        raise RuntimeError("Reflection 响应中的 tool_calls 字段为空")
    tool_calls = message.tool_calls
    if tool_calls is not None and tool_calls != []:
        raise RuntimeError("Reflection 响应中的 tool_calls 字段必须是 None 或空列表")
    if hasattr(message, "content") is False:
        raise RuntimeError("Reflection 响应中的 content 字段为空")
    content = message.content
    if not isinstance(content, str) or content.strip() == "":
        raise RuntimeError("Reflection 响应中的 content 字段非法")
    return content.strip()


# 调用 Refinement 并获取候选摘要对象
def request_refinement_candidate(
    refinement_prompt: str,
    client: OpenAI | None = None,
    *,
    run_context: dict[str, object],
) -> object:
    """调用一次 Refinement JSON Output，并返回解析后的不可信候选对象。

    当前检查点只负责模型请求、响应外壳和 JSON 语法解析；不调用
    ``validate_success_result``，也不构造最终可信三字段结果。
    """
    if not isinstance(refinement_prompt, str) or refinement_prompt.strip() == "":
        raise ValueError("refinement_prompt 必须是非空字符串")
    if client is None:
        client = create_deepseek_client()
    step_start = reserve_call_step(run_context)
    perf_counter_start = perf_counter()
    try:
        response = client.chat.completions.create(
            model=DEEPSEEK_MODEL,
            messages=[
                {
                    "role": "user",
                    "content": refinement_prompt,
                }
            ],
            stream=False,
            extra_body={"thinking": {"type": "disabled"}},
            response_format={"type": "json_object"},
            max_tokens=1600,
        )
    except Exception as e:
        perf_counter_end = perf_counter()
        duration_ms = max(
            0,
            int((perf_counter_end - perf_counter_start) * 1000),
        )
        append_call_log(
            run_context,
            error=type(e).__name__,
            duration_ms=duration_ms,
            step=step_start,
            event_type="model_call",
            model=DEEPSEEK_MODEL,
            tool_name=None,
        )
        raise
    else:
        perf_counter_end = perf_counter()
        duration_ms = max(
            0,
            int((perf_counter_end - perf_counter_start) * 1000),
        )
        append_call_log(
            run_context,
            error=None,
            duration_ms=duration_ms,
            step=step_start,
            event_type="model_call",
            model=DEEPSEEK_MODEL,
            tool_name=None,
        )

    if response is None:
        raise RuntimeError("Refinement 响应为空")
    if hasattr(response, "choices") is False:
        raise RuntimeError("Refinement 响应缺少 choices 字段")
    choices = response.choices
    if not isinstance(choices, list) or not choices:
        raise RuntimeError("Refinement 响应缺少 choices 字段或类型不正确")
    if hasattr(choices[0], "message") is False:
        raise RuntimeError("Refinement 响应中的 message 字段为空")
    message = choices[0].message
    if hasattr(choices[0], "finish_reason") is False:
        raise RuntimeError("Refinement 响应中的 finish_reason 字段为空")
    finish_reason = choices[0].finish_reason
    if finish_reason != "stop":
        raise RuntimeError("Refinement 未以 stop 结束")
    # message.tool_calls 必须是 None 或空列表
    if hasattr(message, "tool_calls") is False:
        raise RuntimeError("Refinement 响应中的 tool_calls 字段为空")
    tool_calls = message.tool_calls
    if tool_calls is not None and tool_calls != []:
        raise RuntimeError("Refinement 响应中的 tool_calls 字段必须是 None 或空列表")
    if hasattr(message, "content") is False:
        raise RuntimeError("Refinement 响应中的 content 字段为空")
    content = message.content
    if not isinstance(content, str) or content.strip() == "":
        raise RuntimeError("Refinement 响应中的 content 字段非法")
    try:
        return json.loads(content.strip())
    except json.JSONDecodeError as e:
        raise RuntimeError(f"Refinement 响应的 content 不是合法 JSON: {e}")

# 编排 Reflection、Refinement 和最终硬校验的流程。
def reflect_refine_and_validate(
    normalized_request: dict[str, str],
    candidate_summary: str,
    tool_name: str,
    tool_result: dict[str, object],
    client: OpenAI | None = None,
    *,
    run_context: dict[str, object],
) -> dict[str, object]:
    """编排一次 Reflection、一次 Refinement，并返回硬校验结果。

    本层不重新调用工具，也不负责 C3c 候选生成；两次模型事件写入
    传入的内部 ``run_context``，但仍不实现重试或最终 Agent 控制器。
    """
    allowed_sources = derive_allowed_sources(
        normalized_request,
        tool_name,
        tool_result,
    )
    reflection_prompt = build_reflection_prompt(
        normalized_request,
        candidate_summary,
        tool_name,
        tool_result,
        allowed_sources,
    )
    if client is None:
        client = create_deepseek_client()
    feedback = request_reflection_feedback(
        reflection_prompt,
        client,
        run_context=run_context,
    )
    refinement_prompt = build_refinement_prompt(
        normalized_request,
        candidate_summary,
        tool_name,
        tool_result,
        allowed_sources,
        feedback,
    )
    candidate = request_refinement_candidate(
        refinement_prompt,
        client,
        run_context=run_context,
    )
    return validate_success_result(candidate, allowed_sources)


# 连接原始请求、C3c 候选生成与 C3d 反思改写的单次正常路径
def run_research_summary_once(
    request: object,
    client: OpenAI | None = None,
) -> dict[str, object]:
    """从原始请求运行一次正常链，并返回最终可信三字段结果。

    单次请求的调用日志只保存在内部 ``run_context``，不会加入最终
    三字段结果；当前仍不实现重试、HITL 或失败状态映射，已有工具、
    模型与校验异常继续向上抛出。
    """
    normalized_request, invalid_result = prepare_request(request)
    if normalized_request is None:
        return invalid_result
    if client is None:
        client = create_deepseek_client()
    run_context = create_run_context()
    gen_res = generate_candidate_summary(
        normalized_request,
        client,
        run_context=run_context,
    )
    candidate_summary = gen_res["candidate_summary"]
    tool_name = gen_res["tool_name"]
    tool_result = gen_res["tool_result"]
    return reflect_refine_and_validate(
        normalized_request,
        candidate_summary,
        tool_name,
        tool_result,
        client,
        run_context=run_context,
    )

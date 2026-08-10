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
当前未创建新的活动代码骨架；后续模型调用、JSON 解析、日志、重试/停止、安全确认和 eval 尚未实现。
"""

import html
import json
import os
from pathlib import Path
import re

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

    # 校验通过，调用工具函数
    return tool_function(**arguments)


def create_deepseek_client() -> OpenAI:
    """复用已 PASS 配置，创建真实 DeepSeek 客户端但不发起模型调用。"""
    load_dotenv()
    api_key = os.environ.get("DEEPSEEK_API_KEY")
    if not api_key:
        raise RuntimeError("DeepSeek API key is missing.")
    return OpenAI(api_key=api_key, base_url=DEEPSEEK_BASE_URL)


def generate_candidate_summary(
    normalized_request: dict[str, str],
    client: OpenAI | None = None,
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
    # 第一次调用模型，获取工具调用
    response1 = client.chat.completions.create(
        model=DEEPSEEK_MODEL,
        messages=messages,
        tools=tool_schemas,
        stream=False,
        extra_body={"thinking": {"type": "disabled"}},
    )
    if response1.choices is None or len(response1.choices) == 0:
        raise RuntimeError("模型未返回任何选择")
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
    tool_result = execute_tool_call(tool_name, raw_arguments, normalized_request)
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
    response2 = client.chat.completions.create(
        model=DEEPSEEK_MODEL,
        messages=messages,
        tools=tool_schemas,
        stream=False,
        extra_body={"thinking": {"type": "disabled"}},
        tool_choice="none",
    )
    if response2.choices is None or len(response2.choices) == 0:
        raise RuntimeError("第二次模型调用未返回任何选择")
    assistant_message2 = response2.choices[0].message
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

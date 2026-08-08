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
后续 Agent 循环、Reflection、日志、安全确认和 eval 不提前实现。
"""

import html
from pathlib import Path
import re

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

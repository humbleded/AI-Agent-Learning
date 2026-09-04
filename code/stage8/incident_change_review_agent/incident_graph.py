"""G8-00 故障诊断与变更评审 Agent v1。

从项目根目录运行语法检查：
    .venv/Scripts/python.exe -m py_compile code/stage8/incident_change_review_agent/incident_graph.py

已完成检查点：
    I1：IncidentState 与 build_initial_state()。
    I2：organize_facts() 的确定性事实整理与局部更新。
    I3：review_evidence() 的证据状态判断与工具请求生成。
    I4a：确定性内存只读工具与 APPROVED_READONLY_TOOLS 白名单。
    I4b：run_readonly_diagnostic() 的授权执行、失败归一化与证据写回。
    I4b-R1：evidence 使用 add reducer，由 Node 返回增量、Graph 负责累计。
    I5：三个确定性停止 Node 与稳定 stop_reason。
    I6：route_after_review() 的五分支确定性路由。
    I7a：无网络、可注入的最终结论 prompt 与 Node 核心。
    I7b：真实 DeepSeek 客户端、单次请求、响应校验与真实调用。
    I8a：七个业务 Node、条件路由、诊断回环与终止边的 Graph 装配。
    I8b：正常路径的 invoke 入口与 v2 updates 流式入口。
    I9：整图正常/停止/失败分支与外部调用边界的长期 pytest。

当前实现状态：
    G8-00 v1 核心和离线回归测试已经闭合；2026-09-05 正式验收 PASS。

I9 只使用内存 fake、spy 与故障注入，不新增真实 DeepSeek 调用。
暂不加入 checkpointer、thread state、interrupt/resume 或长期 Memory。
"""

import os
from collections.abc import Callable, Iterator
from operator import add
from typing import Annotated, Literal, TypedDict

from dotenv import load_dotenv
from langgraph.graph import END, START, StateGraph
from langgraph.types import UpdatesStreamPart
from openai import OpenAI


DEEPSEEK_BASE_URL = "https://api.deepseek.com"
DEEPSEEK_MODEL = "deepseek-v4-pro"
DEEPSEEK_REQUEST_TIMEOUT_SECONDS = 60.0
DEEPSEEK_SDK_MAX_RETRIES = 0

#初始SAMPLE_INCIDENT 用于构造初始 State，实际运行中不应直接使用。
SAMPLE_INCIDENT = {
    "service": "payment",
    "alerts": ["payment 5xx rate high"],
    "logs": [
        "payment request timeout",
        "database pool wait exceeded",
    ],
    "config_snapshot": {
        "request_timeout_ms": "1000",
        "db_pool_size": "20",
    },
    "change_request": (
        "raise payment request timeout from 1000ms to 2000ms"
    ),
}

# IncidentState 定义了 Graph 运行共享的状态，包括输入、过程、控制和输出字段。
class IncidentState(TypedDict):
    """一次故障诊断 Graph 运行共享的 State。"""

    # 输入字段：Graph 运行开始时的初始输入。
    service: str  # 受影响的服务名称
    alerts: list[str]  # 当前触发的告警列表
    logs: list[str]  # 当前收集到的日志列表
    config_snapshot: dict[str, str]  # 当前服务配置快照
    change_request: str | None  # 当前变更请求，None 表示没有变更请求

    facts_summary: str  # 当前收集到的事实摘要，Graph 运行过程中逐步更新
    evidence: Annotated[list[str], add]  # 证据列表，Graph 运行过程中逐步收集
    evidence_status: Literal["unknown", "enough", "insufficient"]  # 证据状态，初始为 "unknown"
    requested_tool: str | None  # 当前请求的工具名称，None 表示尚未请求
    tool_failed: bool  # 当前请求的工具是否失败，初始为 False
    tool_error: Literal["unapproved_tool", "diagnostic_unavailable"] | None  # 当前请求的工具失败原因，None 表示尚未失败
    step_count: int  # 已处理的诊断请求数，从 0 开始
    max_steps: int  # 业务允许处理的诊断请求上限
    stop_reason: Literal["evidence_insufficient", "tool_failure", "max_steps_reached"] | None # 运行停止原因，None 表示尚未停止
    conclusion: str | None  # Graph 运行结束时的结论，None 表示尚未结束 作用是在每一次 Graph 开始运行前，生成一份全新、完整、互不影响的初始 State。

# 在每一次 Graph 开始运行前，生成一份全新、完整、互不影响的初始 State。
def build_initial_state(*, max_steps: int = 2) -> IncidentState:
    """根据给定的脱敏事故样例，构造一次运行所需的完整初始 State。"""
    #为什么yong用copy()？因为SAMPLE_INCIDENT中的列表是可变对象，
    # 直接引用会导致在Graph运行过程中修改原始数据。
    # 使用copy()可以确保每次构建的初始State都是独立的副本，避免意外修改原始样例数据。
    return IncidentState(
        service=SAMPLE_INCIDENT["service"],
        alerts=SAMPLE_INCIDENT["alerts"].copy(),
        logs=SAMPLE_INCIDENT["logs"].copy(),
        config_snapshot=SAMPLE_INCIDENT["config_snapshot"].copy(),
        change_request=SAMPLE_INCIDENT["change_request"],
        facts_summary="",
        evidence=[],
        evidence_status="unknown",
        requested_tool=None,
        tool_failed=False,
        tool_error=None,
        step_count=0,
        max_steps=max_steps,
        stop_reason=None,
        conclusion=None,
    )

#作用是将原始事故输入整理成稳定文本，并返回 facts_summary 的局部更新。
# 把散落在 State 里的原始事故信息整理成一段固定、容易继续处理的事实文本，并写入 facts_summary
#facts_summary是class IncidentState的一个字段，该函数只更新了facts_summary字段，而没有修改其他字段。
def organize_facts(state: IncidentState) -> dict[str, str]:
    """把原始事故输入整理成稳定文本，并返回 facts_summary 局部更新。"""

    # 按本 Session 规定的五行格式整理输入；空集合或缺失变更写成 "none"。
    # 只返回 facts_summary，不原地修改 state，也不更新 step_count。
    service = state["service"]
    alerts = state["alerts"] or ["none"]
    logs = state["logs"] or ["none"]
    config = state["config_snapshot"]
    change_request = state["change_request"]

    facts_summary = (
        f"service={service}\n"
        f"alerts={' | '.join(alerts)}\n"
        f"logs={' | '.join(logs)}\n"
        f"config={' | '.join(f'{k}={v}' for k, v in sorted(config.items())) if config else 'none'}\n"
        f"change_request={'none' if change_request is None else change_request}"
    )
    return {"facts_summary": facts_summary}

# 作用是审查当前证据，并返回证据状态与下一工具请求的局部更新。
#查看当前已经整理出的事实和已经收集到的证据，判断“现在的证据够不够继续得出结论”，并决定是否需要调用工具获取更多信息。
def review_evidence(
    state: IncidentState,
) -> dict[str, str | None]:
    """审查当前证据，并返回证据状态与下一工具请求的局部更新。"""

    # 按本 Session 规定的四条互斥规则审查 evidence、alerts 与 logs。
    # 只返回 evidence_status 和 requested_tool；不要修改输入 State、
    # 调用工具或更新 step_count。
    if state["evidence"]:
        return {"evidence_status": "enough", "requested_tool": None}
    elif not state["alerts"] and not state["logs"]:
        return {"evidence_status": "insufficient", "requested_tool": None}
    elif state["logs"]:
        return {
            "evidence_status": "unknown",
            "requested_tool": "get_recent_errors",
        }
    else:
        return {
            "evidence_status": "unknown",
            "requested_tool": "get_latency_summary",
        }

# 作用是从内存事故样例读取近期错误，并返回独立的结果列表。
def get_recent_errors(state: IncidentState) -> list[str]:
    """从内存事故样例读取近期错误，并返回独立的结果列表。"""

    # 返回基于 logs 的新列表；不要修改 State 或共享原列表。
    return state["logs"].copy()

# 作用是从内存事故样例读取延迟相关信号，并返回独立的结果列表。
def get_latency_summary(state: IncidentState) -> list[str]:
    """从内存事故样例读取延迟相关信号，并返回独立的结果列表。"""

    # 返回基于 alerts 的新列表；不要修改 State 或共享原列表。
    return state["alerts"].copy()

# 作用是登记本检查点明确批准的两个只读工具名称及对应函数对象。
APPROVED_READONLY_TOOLS: dict[
    str,
    Callable[[IncidentState], list[str]],
] = {
    # 只登记本检查点明确批准的两个只读工具名称及对应函数对象。
    "get_recent_errors": get_recent_errors,
    "get_latency_summary": get_latency_summary,
}

#  作用是安全处理一次只读诊断请求，并返回对应的局部 State 更新。校验并执行允许的只读工具
def run_readonly_diagnostic(state: IncidentState) -> dict[str, object]:
    """安全处理一次只读诊断请求，并返回对应的局部 State 更新。"""

    # 只从 APPROVED_READONLY_TOOLS 取函数，覆盖拒绝、超时、
    #       非法工具结果与成功四种结果；每次处理只增加一次 step_count。
    # 不原地修改 State，也不更新 evidence_status、requested_tool 或 stop_reason。

    #分支 1：工具未获批准
    requested_tool = state["requested_tool"]
    if requested_tool is None or requested_tool not in APPROVED_READONLY_TOOLS:
        return {
                "tool_failed": True,
                "tool_error": "unapproved_tool",
                "step_count": state["step_count"] + 1,
              }
    #分支 2：已批准工具超时
    try:
        result = APPROVED_READONLY_TOOLS[requested_tool](state)
    except TimeoutError:
        return {
                "tool_failed": True,
                "tool_error": "diagnostic_unavailable",
                "step_count": state["step_count"] + 1,
              }
    #分支 3：工具返回格式非法
    #result是列表，且列表中的每一项都是字符串
    if not isinstance(result, list) or not all(isinstance(item, str) for item in result):
        return {
                "tool_failed": True,
                "tool_error": "diagnostic_unavailable",
                "step_count": state["step_count"] + 1,
              }
    #分支 4：工具成功
    return {
    "tool_failed": False,
    "tool_error": None,
    "step_count": state["step_count"] + 1,
    # evidence 使用 add reducer；Node 只返回本次新增项，由 Graph 合并累计值。
    "evidence": result,
  }

# 作用是在证据明确不足时写入稳定的业务停止原因。
def evidence_insufficient_stop(state: IncidentState) -> dict[str, str]:
    """返回证据不足分支的 stop_reason 局部更新。"""

    # 只返回 stop_reason="evidence_insufficient"，不要判断路由条件、
    # 修改输入 State、更新其他字段或打印结果。
    return {"stop_reason": "evidence_insufficient"}


# 作用是在诊断工具失败时写入稳定的业务停止原因。
def tool_failure_stop(state: IncidentState) -> dict[str, str]:
    """返回工具失败分支的 stop_reason 局部更新。"""

    # 只返回 stop_reason="tool_failure"，不要把 tool_error 复制到
    # stop_reason，也不要判断路由条件、修改输入 State、更新其他字段或打印结果。
    return {"stop_reason": "tool_failure"}


# 作用是在达到诊断请求上限时写入稳定的业务停止原因。
def max_steps_stop(state: IncidentState) -> dict[str, str]:
    """返回达到诊断请求上限分支的 stop_reason 局部更新。"""

    # 只返回 stop_reason="max_steps_reached"；本 Node 不设置 max_steps，
    # 也不比较 step_count 与 max_steps、修改输入 State、更新其他字段或打印结果。
    return {"stop_reason": "max_steps_reached"}


# 作用是根据结构化控制字段选择 review_evidence 之后唯一的下一站。
def route_after_review(
    state: IncidentState,
) -> Literal[
    "tool_failure_stop",
    "max_steps_stop",
    "evidence_insufficient_stop",
    "build_conclusion",
    "run_readonly_diagnostic",
]:
    """只读 State，并返回 review_evidence 之后的下一个节点名。"""

    # 按已通过 G4 的严格优先级处理工具失败、达到/超过诊断上限、
    # 证据不足、证据充足与默认继续诊断五种结果。
    # 只返回一个节点名；不要修改 State、调用任何 Node/工具/模型或打印。
    if state["tool_failed"]:
        return "tool_failure_stop"
    elif state["step_count"] >= state["max_steps"]:
        return "max_steps_stop"
    elif state["evidence_status"] == "insufficient":
        return "evidence_insufficient_stop"
    elif state["evidence_status"] == "enough":
        return "build_conclusion"
    else:
        return "run_readonly_diagnostic"


class ConclusionGenerationError(RuntimeError):
    """最终结论文本无法安全生成时抛出的稳定应用错误。"""

# 构造最终结论的 prompt，要求模型只依据给定信息输出结论。
def build_conclusion_prompt(state: IncidentState) -> str:
    """把已整理事实与 Graph 累计证据组成确定性的结论提示词。"""

    # 只使用 facts_summary 与 evidence 构造提示词。
    # - facts_summary 必须原样进入“事实摘要”区；不要重新读取或拼装原始输入字段。
    # - evidence 每项单独列出；空列表稳定写成 "- none"。
    # - 明确要求模型只依据给定信息、不声称已执行变更，并按
    #   “根因判断 / 证据依据 / 变更评审”三部分输出；信息有缺口时说明不确定性。
    # - 不要把整份 State、控制字段或模型密钥放进 prompt，也不要调用模型。
    facts_summary = state["facts_summary"]
    evidence = state["evidence"]
    # 作用是将证据列表格式化为字符串，如果证据为空，则显示 "- none"。
    if not evidence:
        evidence_text = "- none"
    else:
        evidence_text = "\n".join(f"- {item}" for item in evidence)

    prompt = (
        f"事实摘要：\n{facts_summary}\n\n"
        f"证据：\n{evidence_text}\n\n"
        "请根据以上信息，只能根据给出的事实和证据回答，不得补造事实，不得声称已经执行变更，信息有缺口时明确表达不确定性，按“根因判断 / 证据依据 / 变更评审”三部分输出结论。"
    )
    return prompt

# 作用是调用注入的文本生成函数，并只返回 conclusion 局部更新。
def build_conclusion(
    state: IncidentState,
    *,
    generate_text: Callable[[str], str],
) -> dict[str, str]:
    """调用注入的文本生成函数，并只返回 conclusion 局部更新。"""

    # 先调用 build_conclusion_prompt()，再把该 prompt 恰好传给
    # generate_text 一次。成功结果必须是去除首尾空白后的非空字符串，并且
    # 只返回 {"conclusion": ...}。
    # generate_text 抛异常、返回非字符串或空白字符串时，都抛出
    # ConclusionGenerationError("conclusion_generation_failed")；异常分支不得
    # 冒充诊断工具失败，也不要返回空 conclusion。
    # 不要原地修改 State、更新 step_count/evidence_status/requested_tool/
    # tool_failed/tool_error/stop_reason，或在本检查点创建真实 API 客户端。
    prompt = build_conclusion_prompt(state)
    try:
        conclusion = generate_text(prompt)
    except Exception as exc:
        raise ConclusionGenerationError("conclusion_generation_failed") from exc
    if not isinstance(conclusion, str) or not conclusion.strip():
        raise ConclusionGenerationError("conclusion_generation_failed")
    return {"conclusion": conclusion.strip()}

# 作用是创建一个显式限制超时和重试的 DeepSeek 客户端。
def create_deepseek_client() -> OpenAI:
    """在运行时读取环境变量，并创建显式限制超时和重试的客户端。"""

    # 调用 load_dotenv() 后，只通过
    # os.environ.get("DEEPSEEK_API_KEY") 读取密钥。
    # 缺失、空字符串或纯空白时抛出 RuntimeError(
    # "deepseek_configuration_failed")，不要打印或把密钥写入错误消息。
    # 成功时使用 DEEPSEEK_BASE_URL、
    # DEEPSEEK_REQUEST_TIMEOUT_SECONDS、DEEPSEEK_SDK_MAX_RETRIES 创建并返回
    # OpenAI 客户端；model 留给请求函数固定，任何配置都不由环境变量覆盖。
    load_dotenv()
    api_key = os.environ.get("DEEPSEEK_API_KEY")
    if not api_key or not api_key.strip():
        raise RuntimeError("deepseek_configuration_failed")

    return OpenAI(
        api_key=api_key,
        base_url=DEEPSEEK_BASE_URL,
        timeout=DEEPSEEK_REQUEST_TIMEOUT_SECONDS,
        max_retries=DEEPSEEK_SDK_MAX_RETRIES,
    )

# 作用是检查非流式 DeepSeek 响应外壳，并返回规范化后的正文。
def extract_deepseek_conclusion(response: object) -> str:
    """检查非流式 DeepSeek 响应外壳，并返回规范化后的正文。"""

    # 按顺序验证：response 有非空 list 类型 choices；首项的
    # finish_reason 精确为 "stop"；message 存在；message.tool_calls 只能是
    # None 或 []；message.content 是 strip 后非空的字符串。
    # 任一条件不满足时都抛出 RuntimeError("invalid_deepseek_response")，
    # 不要返回错误字符串、Provider 原始对象或空正文；成功时返回
    # content.strip()。
    if not hasattr(response, "choices") or not isinstance(response.choices, list) or not response.choices:
        raise RuntimeError("invalid_deepseek_response")
    first_choice = response.choices[0]
    if not hasattr(first_choice, "finish_reason") or first_choice.finish_reason != "stop":
        raise RuntimeError("invalid_deepseek_response")
    if not hasattr(first_choice, "message") or first_choice.message is None:
        raise RuntimeError("invalid_deepseek_response")
    message = first_choice.message
    if not hasattr(message, "tool_calls") or (message.tool_calls is not None and message.tool_calls != []):
        raise RuntimeError("invalid_deepseek_response")
    if not hasattr(message, "content") or not isinstance(message.content, str) or not message.content.strip():
        raise RuntimeError("invalid_deepseek_response")
    return message.content.strip()

# 构造 DeepSeek prompt 并发起恰好一次结论生成请求，返回正文。
def request_deepseek_conclusion(
    prompt: str,
    *,
    client: OpenAI | None = None,
) -> str:
    """向注入或运行时创建的客户端发起恰好一次结论生成请求。"""

    # 先拒绝非字符串或 strip 后为空的 prompt，错误为
    # ValueError("prompt must be a non-empty string")，且此时不得创建客户端或
    # 发请求。client 为 None 时才调用 create_deepseek_client()。
    # 对 active_client.chat.completions.create() 恰好调用一次，参数必须为：
    # model=DEEPSEEK_MODEL；messages 只含一条原样 user prompt；stream=False；
    # extra_body={"thinking": {"type": "disabled"}}。不要传 tools、
    # tool_choice、response_format 或 temperature。
    # 本函数不要捕获或包装 SDK/编程异常；拿到响应后调用
    # extract_deepseek_conclusion() 并返回正文。最终组合进 build_conclusion()
    # 时，由 I7a 统一转换成 ConclusionGenerationError 并保留直接 __cause__，
    # 避免 I7a/I7b 对同一个失败重复包装。
    if not isinstance(prompt, str) or not prompt.strip():
        raise ValueError("prompt must be a non-empty string")
    if client is None:
        client = create_deepseek_client()
    response = client.chat.completions.create(
        model=DEEPSEEK_MODEL,
        messages=[{"role": "user", "content": prompt}],
        stream=False,
        extra_body={"thinking": {"type": "disabled"}},
    )
    return extract_deepseek_conclusion(response)


# 作用是把已经分别验证过的业务 Node 和确定性路由装配成可执行 Graph。
def build_incident_graph(
    *,
    generate_text: Callable[[str], str] = request_deepseek_conclusion,
):
    """装配并编译故障诊断 Graph。"""


    # 1. 使用 IncidentState 创建 StateGraph builder。
    # 2. build_conclusion() 还有必需的 keyword-only generate_text 参数，不能
    #    直接作为单参数 Node 注册；在本函数内部增加一个只接收 state 的包装
    #    Node，并把这里注入的 generate_text 传给 build_conclusion()。
    # 3. 精确注册七个业务 Node：organize_facts、review_evidence、
    #    run_readonly_diagnostic、build_conclusion（注册上面的包装 Node），以及
    #    evidence_insufficient_stop、tool_failure_stop、max_steps_stop。
    #    route_after_review 只负责路由，不要注册成 Node。
    # 4. 固定入口为 START -> organize_facts -> review_evidence。
    # 5. review_evidence 只使用一组条件边和 route_after_review；不要再从它
    #    添加普通出边。当前 Literal 返回注解已经列出五个合法目的节点。
    # 6. run_readonly_diagnostic 执行后回到 review_evidence。
    # 7. build_conclusion 和三个 stop Node 分别连接 END。
    # 8. 返回 builder.compile()。构建和编译期间不得调用工具或 generate_text。
    # 本检查点不要调用 invoke()/stream()，也不要加入 checkpointer、重试、
    # main/CLI、可视化、测试文件或新的 State 字段。

    # 1. 使用 IncidentState 创建 StateGraph builder。
    builder = StateGraph(IncidentState)

    # 2. 注册Node
    builder.add_node("organize_facts", organize_facts)
    builder.add_node("review_evidence", review_evidence)
    builder.add_node("run_readonly_diagnostic", run_readonly_diagnostic)
    builder.add_node("evidence_insufficient_stop", evidence_insufficient_stop)
    builder.add_node("tool_failure_stop", tool_failure_stop)
    builder.add_node("max_steps_stop", max_steps_stop)
    # 为什么要使用 lambda 包装 build_conclusion？
    # 因为 build_conclusion 需要一个额外的关键字参数 generate_text，
    # 而 StateGraph 的 add_node 方法只接受一个 state 参数。通过 lambda，
    # 我们可以在注册节点时将 generate_text 注入到 build_conclusion 中，从而满足 StateGraph 的接口要求。
    builder.add_node("build_conclusion", lambda state: build_conclusion(state, generate_text=generate_text))

    # 3. EDGE: START -> organize_facts -> review_evidence
    builder.add_edge(START, "organize_facts")
    builder.add_edge("organize_facts", "review_evidence")
    builder.add_conditional_edges("review_evidence", route_after_review)
    builder.add_edge("run_readonly_diagnostic", "review_evidence")
    builder.add_edge("build_conclusion", END)
    builder.add_edge("evidence_insufficient_stop", END)
    builder.add_edge("tool_failure_stop", END)
    builder.add_edge("max_steps_stop", END)

    return builder.compile()


# 作用是从一份初始 State 启动一次 Graph，并返回完整最终 State。
def invoke_incident(
    initial_state: IncidentState,
    *,
    generate_text: Callable[[str], str] = request_deepseek_conclusion,
) -> IncidentState:
    """运行一次故障诊断 Graph，并返回完整最终 State。"""

    # 使用注入的 generate_text 构建 Graph，调用 invoke() 恰好
    # 一次，并原样返回完整最终 State。不要使用 v2 invoke、不要只返回某个
    # 字段、不要修改 initial_state，也不要打印或在这里捕获业务异常。
    graph = build_incident_graph(generate_text=generate_text)
    return graph.invoke(initial_state)


# 作用是从一份初始 State 启动一次新 Graph，并逐个交出 Node 局部更新。
def stream_incident_updates(
    initial_state: IncidentState,
    *,
    generate_text: Callable[[str], str] = request_deepseek_conclusion,
) -> Iterator[UpdatesStreamPart]:
    """原样产出一次 Graph 运行的 v2 updates stream parts。"""

    # 使用注入的 generate_text 构建一张新 Graph，并调用
    # graph.stream(initial_state, stream_mode="updates", version="v2")。
    # 必须逐个 yield 完整 part（保留 type/ns/data），不能只 yield data，
    # 也不能先 list() 收齐后再返回；不要调用 invoke()、打印、过滤或改写
    # chunk。当前只做同步 updates 流，不增加 messages/token、values、异步流、
    # checkpointer、thread_id、失败分支处理或第二次真实 DeepSeek 调用。
    graph = build_incident_graph(generate_text=generate_text)
    # yield的作用是将 graph.stream() 生成的每个更新部分逐个返回给调用者，
    # 而不是一次性返回整个结果列表。这样可以实现流式处理，
    # 允许调用者在 Graph 运行过程中实时接收和处理更新，而不必等待整个 Graph 执行完毕。
    yield from graph.stream(initial_state, stream_mode="updates", version="v2")

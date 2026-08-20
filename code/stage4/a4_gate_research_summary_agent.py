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
当前已完成 C4a-2a：首次可重试工具失败后，同名同原始参数只重试一次并恢复成功。
当前已完成 C4a-2b1：把二次可重试失败 / 重试前无剩余 step 映射为 ``needs_manual``。
当前已完成 C4a-2b2-I1：映射真实不可重试工具失败与搜索成功零证据。
当前已完成 C4b-1-I1a：Action correction 的局部额度与完整链预算门。
当前已完成 C4b-1-I1b：构造不代表真实工具执行的安全校验错误 Observation。
当前已完成 C4b-1-I1c：一次 Action correction 模型调用及其 step / 日志记账。
当前已完成 C4b-1-I1d：可复用的单 Action 响应外壳解析器。
当前已完成 C4b-1-I1e：组合一次 Action correction，并停在修正 Action 执行前。
当前已完成 C4b-1-I1f：识别真实工具执行前的 Action validation rejection。
当前已完成 C4b-1-I1g：执行并分类一次未信任 Tool Action。
当前已完成 C4b-1-I1h：编排首次 Action、至多一次 correction 与修正 Action。
当前已完成 C4b-1-I2a：把 I1h 接入 ``generate_candidate_summary()`` 的 Action 主链。
当前已完成 C4b-1-I2b：判断工具 retry 后是否仍有完成可信下游链的全局预算。
当前已完成 C4b-1-I2c：在第二次真实工具调用前消费完整链预算门。
当前已完成 C4b-1-I2d：把预算窄异常准确映射为公开 needs_manual 结果。
当前已完成 C4b-2a-I1a：候选恢复完整下游链预算门。
当前已完成 C4b-2a-I1b：候选响应的 valid / recoverable / terminal 纯分类。
当前已完成 C4b-2a-I1c：构造只复用真实 Tool Observation 的安全恢复消息。
当前已完成 C4b-2a-I1d：单次 Candidate recovery 调用及其 step / 日志记账。
当前已完成 C4b-2a-I1e：编排至多一次 Candidate recovery，并停在第二次内部分类。
当前已完成 C4b-2a-I1f：把首次分类、至多一次恢复与候选阶段窄停止组合成 stage resolver。
当前已完成 C4b-2a-I1g：把候选阶段 resolver 接入 ``generate_candidate_summary()``。
当前已完成 C4b-2a-I1h：把候选阶段窄停止安全映射为公开 ``needs_manual``。
当前已完成 C4b-2a-I2：候选恢复端到端故障注入与既有控制流回归。
当前已完成 C4b-2a-U1：用户已审核最终调用轨迹、停止结果与来源语义。
后续 Candidate Provider/API 异常、Reflection / 最终 validator 失败恢复、安全确认和 eval 尚未完成。
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
MAX_STEPS = 6  # 每次请求允许的最大调用步数
MIN_STEPS_FOR_CANDIDATE_RECOVERY_CHAIN = 3  # 候选恢复链所需的最少调用步数
RECOVERABLE_CANDIDATE_RESPONSE_REASONS = frozenset(
    {
        "invalid_response_shape",
        "invalid_candidate_content",
        "length",
        "unexpected_tool_calls",
    }
)
MAX_TOOL_RETRIES = 1  # 工具可重试的最大次数
MAX_ACTION_CORRECTIONS = 1  # 局部 Action correction 的最大允许次数
MIN_STEPS_AFTER_VALID_ACTION = 4  # 取得合法 Action 后，仍须保留的最少调用步数
MAX_ACTION_VALIDATION_ERROR_CHARS = 300  # 回填给模型的校验错误最大字符数
CALL_LOG_FIELDS = (
    "request_id",
    "step",
    "event_type",
    "model",
    "tool_name",
    "duration_ms",
    "error",
)


# 自定义异常类，用于表示自动恢复机会耗尽的情况
class AutoRecoveryExhaustedError(RuntimeError):
    """只表示当前请求的自动恢复机会已经耗尽的内部专用信号。"""

    def __init__(
        self,
        reason: str,
        attempts: int,
        last_error: str,
    ) -> None:
        # 只保存公开入口构造人工接管说明所需的内部事实。
        self.reason = reason
        self.attempts = attempts
        self.last_error = last_error
        super().__init__(
            "Auto recovery exhausted: "
            f"reason={reason}, attempts={attempts}, last_error={last_error}"
        )


# 自定义异常类，用于表示工具调用达到了终点的情况
class TerminalToolOutcomeError(RuntimeError):
    """只表示 C4a-2b2 已识别的两个工具终点的内部专用信号。"""

    def __init__(self, status: str, detail: str) -> None:
        # 保存公开入口构造失败结果所需的最小内部事实，并初始化父类。
        # 本类不构造最终三字段结果，也不接受本切片之外的状态。
        if type(status) is not str:
            raise ValueError("TerminalToolOutcomeError 的 status 必须是字符串类型")
        if status != "tool_failure" and status != "insufficient_evidence":
            raise ValueError(
                "TerminalToolOutcomeError 只接受 "
                "'tool_failure' 或 'insufficient_evidence' 状态"
            )
        if type(detail) is not str:
            raise ValueError("TerminalToolOutcomeError 的 detail 必须是字符串类型")
        detail = detail.strip()
        if not detail:
            raise ValueError("TerminalToolOutcomeError 的 detail 不能为空字符串")
        self.status = status
        self.detail = detail
        super().__init__("Terminal tool outcome: " f"status={status}, detail={detail}")


class ToolActionProtocolError(RuntimeError):
    """表示模型响应无法提供一个可继续接力的单一 Tool Action 外壳。"""


class ActionCorrectionBudgetError(RuntimeError):
    """表示 I1a 已拒绝继续发起 Action correction 的内部窄信号。"""

    def __init__(
        self,
        *,
        reason: str,
        current_step: int,
        corrections_used: int,
        last_error: str,
    ) -> None:
        if reason not in (
            "max_action_corrections",
            "insufficient_completion_steps",
        ):
            raise ValueError("未知的 Action correction 预算停止原因")
        self.reason = reason
        self.current_step = current_step
        self.corrections_used = corrections_used
        self.last_error = last_error
        super().__init__(
            "Action correction budget unavailable: "
            f"reason={reason}, current_step={current_step}, "
            f"corrections_used={corrections_used}, last_error={last_error}"
        )


class ToolRetryCompletionBudgetError(RuntimeError):
    """表示第二次真实工具调用前发现完整可信链预算不足的内部窄信号。"""

    def __init__(
        self,
        *,
        current_step: int,
        attempts: int,
        last_error: str,
    ) -> None:
        # 类型本身唯一表示“完整链预算不足”；固定异常文本不回显工具错误。
        self.current_step = current_step
        self.attempts = attempts
        self.last_error = last_error
        super().__init__("Tool retry completion budget is insufficient")


class CandidateRecoveryCompletionBudgetError(RuntimeError):
    """表示候选恢复前发现完整可信下游链预算不足的内部窄信号。"""

    def __init__(
        self,
        *,
        current_step: int,
        recoverable_reason: str,
    ) -> None:
        if type(current_step) is not int or not (1 <= current_step <= MAX_STEPS):
            raise ValueError("current_step 必须位于全局 step 合法域内")
        if recoverable_reason not in RECOVERABLE_CANDIDATE_RESPONSE_REASONS:
            raise ValueError("recoverable_reason 必须属于候选恢复白名单")
        self.current_step = current_step
        self.recoverable_reason = recoverable_reason
        super().__init__("Candidate recovery completion budget is insufficient")


class CandidateSummaryStageStopError(RuntimeError):
    """表示 Candidate 阶段已安全停止、等待公开入口映射的内部窄信号。"""

    def __init__(
        self,
        *,
        stop_kind: str,
        candidate_reason: str,
        recovery_attempts: int,
        current_step: int,
        allowed_sources: list[str],
    ) -> None:
        terminal_reasons = {
            "content_filter",
            "insufficient_system_resource",
            "missing_finish_reason",
            "unknown_finish_reason",
        }
        if type(stop_kind) is not str or stop_kind not in {
            "terminal_response",
            "recovery_exhausted",
            "insufficient_completion_steps",
        }:
            raise ValueError("stop_kind 必须属于候选阶段冻结的三种停止类型")
        if type(candidate_reason) is not str:
            raise ValueError("candidate_reason 必须是冻结的安全原因字符串")
        if type(recovery_attempts) is not int or recovery_attempts not in {0, 1}:
            raise ValueError("recovery_attempts 必须是内建整数 0 或 1")
        if type(current_step) is not int or not (1 <= current_step <= MAX_STEPS):
            raise ValueError("current_step 必须位于全局 step 合法域内")
        if (
            type(allowed_sources) is not list
            or not allowed_sources
            or not all(
                type(source) is str and bool(source.strip())
                for source in allowed_sources
            )
        ):
            raise ValueError("allowed_sources 必须是非空的真实来源字符串列表")

        if stop_kind == "terminal_response":
            if candidate_reason not in terminal_reasons:
                raise ValueError("terminal_response 必须携带 terminal candidate reason")
        elif stop_kind == "recovery_exhausted":
            if (
                candidate_reason not in RECOVERABLE_CANDIDATE_RESPONSE_REASONS
                or recovery_attempts != 1
            ):
                raise ValueError("recovery_exhausted 必须表示一次恢复后的可恢复失败")
        elif (
            candidate_reason not in RECOVERABLE_CANDIDATE_RESPONSE_REASONS
            or recovery_attempts != 0
        ):
            raise ValueError("预算停止必须发生在候选恢复调用之前")

        self.stop_kind = stop_kind
        self.candidate_reason = candidate_reason
        self.recovery_attempts = recovery_attempts
        self.current_step = current_step
        self.allowed_sources = list(allowed_sources)
        super().__init__("Candidate summary stage stopped")


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


# 判断是否还有 Action correction 预算的工具函数
def has_action_correction_budget(
    current_step: int,
    corrections_used: int,
) -> bool:
    """判断是否还允许发起一次 Action correction 模型调用。

    这是一个无副作用的纯预算门：不得修改 ``run_context``、占用 step、
    写日志或调用模型 / 工具。输入只接受内建整数；``current_step`` 必须
    位于 1 到全局上限之间，``corrections_used`` 必须位于 0 到局部上限之间。
    """
    if not type(current_step) is int or current_step < 1 or current_step > MAX_STEPS:
        raise ValueError("current_step 必须是位于 1 到全局上限之间的整数")
    if (
        not type(corrections_used) is int
        or corrections_used < 0
        or corrections_used > MAX_ACTION_CORRECTIONS
    ):
        raise ValueError("corrections_used 必须是位于 0 到局部上限之间的整数")

    remaining_steps = MAX_STEPS - current_step
    if (
        corrections_used >= MAX_ACTION_CORRECTIONS
        or remaining_steps < 1 + MIN_STEPS_AFTER_VALID_ACTION
    ):
        return False
    return True


# 判断一次工具 retry 后是否仍能完成可信结果链的纯预算门。
def has_tool_retry_completion_budget(
    current_step: int,
) -> bool:
    """判断全局剩余调用步数能否容纳工具 retry 及其完整下游链。

    ``current_step`` 表示第一次真实工具尝试已完成并记账后的累计 step，
    只接受全局计数器合法域内的内建整数。本函数只判断全局完成性预算；
    本地 retry 次数额度仍由既有 retry 分支负责，二者不得混为同一原因。

    合法输入返回内建 ``bool``；不得接收或修改 ``run_context``，不得占步、
    写日志、调用模型 / 工具、执行 retry、构造停止异常或公开结果。
    """
    if not type(current_step) is int or not (1 <= current_step <= MAX_STEPS):
        raise ValueError("current_step 必须是位于 1 到全局上限之间的整数")

    remaining_steps = MAX_STEPS - current_step
    return remaining_steps >= MIN_STEPS_AFTER_VALID_ACTION


# 判断候选响应失败后是否仍能完成受控恢复链的纯预算门。
def has_candidate_recovery_completion_budget(
    current_step: int,
) -> bool:
    """判断剩余调用步数能否容纳候选恢复及其完整下游链。

    ``current_step`` 表示不可用的候选模型响应已经返回并记账后的累计 step；
    恢复成功还必须依次完成 Candidate recovery、Reflection 与 Refinement。
    输入只接受全局计数器合法域内的内建整数，合法输入返回内建 ``bool``。

    这是无副作用的纯预算门：不得修改请求上下文、占用 step、写日志、
    调用模型 / 工具、执行恢复或构造公开结果。
    """
    if not type(current_step) is int or not (1 <= current_step <= MAX_STEPS):
        raise ValueError("current_step 必须是位于 1 到全局上限之间的整数")

    remaining_steps = MAX_STEPS - current_step
    return remaining_steps >= MIN_STEPS_FOR_CANDIDATE_RECOVERY_CHAIN


# 把不可信的候选模型响应转换为固定内部分类结果。
def classify_candidate_summary_response(
    response: object,
) -> dict[str, object]:
    """纯分类候选模型响应，不执行恢复或构造公开结果。

    返回字典必须严格只有 ``classification``、``reason``、
    ``candidate_summary`` 三个键：合法候选使用 ``valid / None / 原始非空正文``；
    白名单内失败使用 ``recoverable / 固定安全原因 / None``；必须停止的失败
    使用 ``terminal / 固定安全原因 / None``。

    安全过滤、资源不足、缺失或未知 ``finish_reason`` 的终止优先级高于
    message / content 的结构问题。函数不得泄漏坏外壳产生的原生属性 / 类型
    异常，不得修改响应、占 step、写日志、调用模型 / 工具或检查恢复预算。
    """
    def make_classification(
        classification: str,
        reason: str | None,
        candidate_summary: str | None,
    ) -> dict[str, object]:
        return {
            "classification": classification,
            "reason": reason,
            "candidate_summary": candidate_summary,
        }

    def read_attribute(value: object, name: str) -> tuple[bool, object]:
        try:
            return True, getattr(value, name)
        except Exception:
            return False, None

    has_choices, choices = read_attribute(response, "choices")
    if not has_choices or type(choices) is not list or not choices:
        return make_classification(
            "recoverable",
            "invalid_response_shape",
            None,
        )

    choice = choices[0]
    has_finish_reason, finish_reason = read_attribute(choice, "finish_reason")
    if not has_finish_reason or finish_reason is None:
        return make_classification(
            "terminal",
            "missing_finish_reason",
            None,
        )
    if type(finish_reason) is not str:
        return make_classification(
            "terminal",
            "unknown_finish_reason",
            None,
        )
    if finish_reason == "content_filter":
        return make_classification(
            "terminal",
            "content_filter",
            None,
        )
    if finish_reason == "insufficient_system_resource":
        return make_classification(
            "terminal",
            "insufficient_system_resource",
            None,
        )
    if finish_reason == "length":
        return make_classification(
            "recoverable",
            "length",
            None,
        )
    if finish_reason == "tool_calls":
        return make_classification(
            "recoverable",
            "unexpected_tool_calls",
            None,
        )
    if finish_reason != "stop":
        return make_classification(
            "terminal",
            "unknown_finish_reason",
            None,
        )

    has_message, message = read_attribute(choice, "message")
    if not has_message or message is None:
        return make_classification(
            "recoverable",
            "invalid_response_shape",
            None,
        )

    has_tool_calls, tool_calls = read_attribute(message, "tool_calls")
    if not has_tool_calls or (
        tool_calls is not None and type(tool_calls) is not list
    ):
        return make_classification(
            "recoverable",
            "invalid_response_shape",
            None,
        )
    if tool_calls:
        return make_classification(
            "recoverable",
            "unexpected_tool_calls",
            None,
        )

    has_content, content = read_attribute(message, "content")
    if not has_content:
        return make_classification(
            "recoverable",
            "invalid_response_shape",
            None,
        )

    if type(content) is not str or not content.strip():
        return make_classification(
            "recoverable",
            "invalid_candidate_content",
            None,
        )

    return make_classification("valid", None, content)


# 只依据既有真实 Tool Observation 构造一次候选修订消息。
def build_candidate_recovery_messages(
    base_messages: list[object],
    recoverable_reason: str,
) -> list[object]:
    """返回追加一条安全修订指令的新消息列表。

    ``base_messages`` 必须是以既有 Tool message 结尾的非空内建列表；
    ``recoverable_reason`` 只接受 G2 冻结的四个可恢复原因。返回值必须是
    新的内建列表，原消息前缀的顺序与对象 identity 不变，末尾只追加一条
    严格含 ``role / content`` 的 user message。

    修订不得接收或回填失败的原始 Candidate 响应，不得修改输入消息、
    重建 Tool Observation、调用模型 / 工具、占 step、写日志或检查预算。
    """
    # 按 recoverable reason 构造一次证据受限修订消息。
    if type(base_messages) is not list or not base_messages:
        raise ValueError("base_messages 必须是非空内建列表")

    last_message = base_messages[-1]
    expected_tool_message_keys = {"role", "tool_call_id", "content"}
    if (
        type(last_message) is not dict
        or set(last_message) != expected_tool_message_keys
        or last_message["role"] != "tool"
    ):
        raise ValueError("base_messages 必须以既有 Tool message 结尾")

    if (
        type(recoverable_reason) is not str
        or recoverable_reason not in RECOVERABLE_CANDIDATE_RESPONSE_REASONS
    ):
        raise ValueError("recoverable_reason 必须是 G2 冻结的可恢复原因")

    reason_instruction = {
        "invalid_response_shape": "上一候选响应的结构不可用。",
        "invalid_candidate_content": "上一候选响应没有提供可用的非空摘要正文。",
        "length": "从头重写，不要续写上一次被截断的文本。上一候选响应因长度上限被截断，请生成更短但完整的摘要。",
        "unexpected_tool_calls": "上一候选响应错误地尝试了 Tool Action。",
    }[recoverable_reason]
    recovery_instruction = (
        f"{reason_instruction}请只依据消息历史中既有的真实 Tool Observation "
        "请从头生成一个非空的候选摘要纯文本；"
        "不要输出 JSON，也不要输出最终 status、summary、sources 字段结构。"
        "不要调用任何工具，不要补充 Observation 未提供的事实，"
        "只输出候选摘要正文。"
    )

    recovery_messages = list(base_messages)
    recovery_messages.append(
        {
            "role": "user",
            "content": recovery_instruction,
        }
    )
    tool_call_id = last_message["tool_call_id"]
    content = last_message["content"]

    if (
        type(tool_call_id) is not str
        or not tool_call_id.strip()
        or type(content) is not str
        or not content.strip()
    ):
        raise ValueError("Tool message 的 tool_call_id 和 content 必须是非空字符串")

    return recovery_messages


# 发起一次 Candidate recovery 的模型调用。
def request_candidate_recovery_response(
    recovery_messages: list[object],
    client: OpenAI | None = None,
    *,
    run_context: dict[str, object],
) -> object:
    """发起恰好一次候选恢复模型调用，并原样返回不可信响应。

    ``recovery_messages`` 必须是 I1c 构造的非空内建列表。本函数只负责
    输入门、一次真实模型调用及其共享 step / 七字段日志；调用方必须提前
    通过完整链预算门。API 正常返回的任何对象（包括 ``None`` 或坏外壳）
    都原样交给 I1b 分类器，不在这里解析、重试或映射公开结果。

    不得修改消息、重新执行工具、构造修订消息、调用 Reflection / Refinement，
    也不得在 Provider / SDK 异常后发起第二次请求或泄漏异常正文。
    """
    if type(recovery_messages) is not list or len(recovery_messages) < 2:
        raise ValueError("recovery_messages 必须是 I1c 构造的非空内建列表")

    tool_message = recovery_messages[-2]
    recovery_message = recovery_messages[-1]
    if (
        type(tool_message) is not dict
        or set(tool_message) != {"role", "tool_call_id", "content"}
        or tool_message["role"] != "tool"
        or type(tool_message["tool_call_id"]) is not str
        or not tool_message["tool_call_id"].strip()
        or type(tool_message["content"]) is not str
        or not tool_message["content"].strip()
    ):
        raise ValueError("recovery_messages 缺少 I1c 保留的有效 Tool message")
    if (
        type(recovery_message) is not dict
        or set(recovery_message) != {"role", "content"}
        or recovery_message["role"] != "user"
        or type(recovery_message["content"]) is not str
        or not recovery_message["content"].strip()
    ):
        raise ValueError("recovery_messages 缺少 I1c 追加的安全修订指令")

    tool_schemas = build_tool_schemas()
    if client is None:
        client = create_deepseek_client()
    call_step = reserve_call_step(run_context)
    perf_counter_start = perf_counter()
    try:
        response = client.chat.completions.create(
            model=DEEPSEEK_MODEL,
            messages=recovery_messages,
            tools=tool_schemas,
            stream=False,
            extra_body={"thinking": {"type": "disabled"}},
            tool_choice="none",
        )
    except Exception as exc:
        perf_counter_end = perf_counter()
        append_call_log(
            run_context,
            error=type(exc).__name__,
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
        return response


# 在完整链预算允许时，编排至多一次 Candidate recovery。
def attempt_candidate_recovery_once(
    base_messages: list[object],
    initial_classification: dict[str, object],
    client: OpenAI | None = None,
    *,
    run_context: dict[str, object],
) -> dict[str, object]:
    """把首次可恢复分类推进到唯一一次恢复后的内部分类结果。

    ``initial_classification`` 必须是 I1b 的 exact 三键 recoverable 结果；
    ``base_messages`` 是失败 Candidate 调用前、以真实 Tool Observation 结尾的
    原消息历史。函数按顺序执行完整链预算门、I1c builder、I1d 单次调用和
    I1b 再分类，并原样返回第二次分类对象。

    第二次结果无论是 valid、terminal 还是 recoverable 都必须直接返回；
    不得循环、递归、再次恢复、修改共享 context schema、调用工具 / Reflection，
    或构造公开结果。预算不足时抛专用窄异常，且不得构造消息或调用模型。
    """
    # 实现 exact 输入门与一次恢复编排。
    expected_classification_keys = {
        "classification",
        "reason",
        "candidate_summary",
    }
    if (
        type(initial_classification) is not dict
        or set(initial_classification) != expected_classification_keys
        or type(initial_classification["classification"]) is not str
        or initial_classification["classification"] != "recoverable"
        or type(initial_classification["reason"]) is not str
        or initial_classification["reason"]
        not in RECOVERABLE_CANDIDATE_RESPONSE_REASONS
        or initial_classification["candidate_summary"] is not None
    ):
        raise ValueError("initial_classification 必须是 I1b 的 exact recoverable 结果")

    if type(base_messages) is not list or not base_messages:
        raise ValueError("base_messages 必须是以 Tool message 结尾的非空内建列表")
    last_message = base_messages[-1]
    if (
        type(last_message) is not dict
        or set(last_message) != {"role", "tool_call_id", "content"}
        or last_message["role"] != "tool"
        or type(last_message["tool_call_id"]) is not str
        or not last_message["tool_call_id"].strip()
        or type(last_message["content"]) is not str
        or not last_message["content"].strip()
    ):
        raise ValueError("base_messages 必须以有效的真实 Tool Observation 结尾")

    if type(run_context) is not dict or "step" not in run_context:
        raise ValueError("run_context 必须包含共享 step")
    current_step = run_context["step"]
    recoverable_reason = initial_classification["reason"]
    if not has_candidate_recovery_completion_budget(current_step):
        raise CandidateRecoveryCompletionBudgetError(
            current_step=current_step,
            recoverable_reason=recoverable_reason,
        )

    recovery_messages = build_candidate_recovery_messages(
        base_messages,
        recoverable_reason,
    )
    recovery_response = request_candidate_recovery_response(
        recovery_messages,
        client=client,
        run_context=run_context,
    )
    return classify_candidate_summary_response(recovery_response)


# 构造用于请求 Action correction 的协议级 Tool Observation 的工具函数
def build_action_validation_observation(
    tool_call_id: str,
    validation_error: str,
) -> dict[str, str]:
    """构造用于请求 Action correction 的协议级 Tool Observation。

    这条消息表示客户端在真实工具执行前拒绝了 Action，不代表工具后端
    已运行。返回值外层必须严格只有 ``role``、``tool_call_id``、``content``；
    ``content`` 必须是 JSON 字符串，并严格包含 ``ok``、``error_type``、
    ``message``、``instruction`` 四个字段。函数不得占 step、写调用日志、
    调用模型 / 工具，也不得接收或拼入原始参数、prompt、资料或内部日志。
    """
    # 校验 tool_call_id 和 validation_error，构造 content 并返回协议消息
    if not type(tool_call_id) is str or not tool_call_id.strip():
        raise ValueError("tool_call_id 必须是非空字符串")

    if not type(validation_error) is str or not validation_error.strip():
        raise ValueError("validation_error 必须是非空字符串")
    validation_error = validation_error.strip()
    if len(validation_error) > MAX_ACTION_VALIDATION_ERROR_CHARS:
        raise ValueError(
            f"validation_error 长度不得超过 {MAX_ACTION_VALIDATION_ERROR_CHARS}"
        )

    content = json.dumps(
        {
            "ok": False,
            "error_type": "action_validation_error",
            "message": validation_error,
            "instruction": "请只返回一个符合 Schema 与规范化请求的修正工具调用",
        },
        ensure_ascii=False,
    )

    return {
        "role": "tool",
        "tool_call_id": tool_call_id,
        "content": content,
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
        if not (isinstance(model, str) and model.strip() != "" and tool_name is None):
            raise ValueError(
                "model_call 的 model 必须为非空字符串，tool_name 必须为 None"
            )
    elif event_type == "tool_call":
        if not (
            isinstance(tool_name, str) and tool_name.strip() != "" and model is None
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


#  读取沙箱内资料的工具函数
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
        return {
            "ok": False,
            "error": "API 返回的搜索结果结构不正确",
            "retryable": False,
        }
    if "search" not in data["query"] or not isinstance(
        data["query"].get("search"), list
    ):
        return {
            "ok": False,
            "error": "API 返回的搜索结果列表不正确",
            "retryable": False,
        }
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
            return {
                "ok": False,
                "error": "搜索结果条目缺少必要字段",
                "retryable": False,
            }
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


#  构建模型工具的 Schema 列表
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
            return {
                "ok": False,
                "error": "工具参数必须是 JSON 字符串",
                "retryable": False,
            }
        if not raw_arguments.strip():
            return {"ok": False, "error": "工具参数不能为空", "retryable": False}
        arguments = json.loads(raw_arguments)
        if not isinstance(arguments, dict):
            return {
                "ok": False,
                "error": "工具参数必须是 JSON 对象",
                "retryable": False,
            }
    except json.JSONDecodeError as e:
        return {"ok": False, "error": f"解析工具参数失败: {e}", "retryable": False}

    # 校验参数是否符合工具的 Schema
    tool_schemas = {
        schema["function"]["name"]: schema for schema in build_tool_schemas()
    }
    schema = tool_schemas.get(tool_name)
    if schema is None:
        return {
            "ok": False,
            "error": f"未找到工具的 Schema: {tool_name}",
            "retryable": False,
        }
    required_fields = (
        schema.get("function", {}).get("parameters", {}).get("required", [])
    )
    for field in required_fields:
        if field not in arguments:
            return {
                "ok": False,
                "error": f"缺少必要的工具参数: {field}",
                "retryable": False,
            }
    additional_properties = (
        schema.get("function", {})
        .get("parameters", {})
        .get("additionalProperties", True)
    )
    if not additional_properties:
        for field in arguments:
            if field not in required_fields:
                return {
                    "ok": False,
                    "error": f"存在多余的工具参数: {field}",
                    "retryable": False,
                }
    # 校验参数类型是否符合要求
    properties = schema.get("function", {}).get("parameters", {}).get("properties", {})
    for field, field_schema in properties.items():
        if field in arguments:
            expected_type = field_schema.get("type")
            if expected_type == "string" and not isinstance(arguments[field], str):
                return {
                    "ok": False,
                    "error": f"工具参数 {field} 类型不正确，期望为字符串",
                    "retryable": False,
                }

    # 校验工具调用的参数是否与 normalized_request 完全一致。
    if tool_name == "read_material":
        if "relative_path" not in arguments:
            return {
                "ok": False,
                "error": "缺少必要的工具参数: relative_path",
                "retryable": False,
            }
        if normalized_request.get("input_type") != "relative_path":
            return {
                "ok": False,
                "error": "工具调用的 input_type 与 normalized_request 不一致",
                "retryable": False,
            }
        if arguments["relative_path"] != normalized_request.get("value"):
            return {
                "ok": False,
                "error": "工具调用的 relative_path 与 normalized_request 不一致",
                "retryable": False,
            }
    elif tool_name == "search_web":
        if "query" not in arguments:
            return {
                "ok": False,
                "error": "缺少必要的工具参数: query",
                "retryable": False,
            }
        if normalized_request.get("input_type") != "topic":
            return {
                "ok": False,
                "error": "工具调用的 input_type 与 normalized_request 不一致",
                "retryable": False,
            }
        if arguments["query"] != normalized_request.get("value"):
            return {
                "ok": False,
                "error": "工具调用的 query 与 normalized_request 不一致",
                "retryable": False,
            }
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


# 提取执行前的动作校验错误
def extract_preexecution_action_validation_error(
    tool_result: object,
    *,
    run_context: dict[str, object],
    step_before: int,
    logs_length_before: int,
) -> str | None:
    """只识别没有触发真实工具 step / 日志的 Action 校验拒绝。

    返回经过首尾空白清理的安全校验错误，表示后续可以考虑进入 Action
    correction；任何真实工具已执行、结果形状不明确或账本来源不一致的情况
    都返回 ``None``。本函数只观察输入，不修改上下文，也不调用模型或工具。
    """
    if type(step_before) is not int or step_before < 0:
        return None
    if type(logs_length_before) is not int or logs_length_before < 0:
        return None

    if type(run_context) is not dict:
        return None
    if "step" not in run_context or "logs" not in run_context:
        return None
    step = run_context.get("step")
    logs = run_context.get("logs")
    if type(step) is not int or step < 0:
        return None
    if type(logs) is not list:
        return None

    if type(tool_result) is not dict:
        return None

    if set(tool_result) != {"ok", "error", "retryable"}:
        return None

    if (
        tool_result.get("ok") is not False
        or tool_result.get("retryable") is not False
        or type(tool_result.get("error")) is not str
        or not tool_result.get("error").strip()
    ):
        return None

    if step != step_before or len(logs) != logs_length_before:
        return None

    return tool_result.get("error").strip()


# 执行工具动作并分类结果来源
def execute_and_classify_tool_action(
    tool_name: object,
    raw_arguments: object,
    normalized_request: dict[str, str],
    *,
    run_context: dict[str, object],
) -> dict[str, object]:
    """执行恰好一次未信任 Tool Action，并按同一次执行快照分类结果来源。

    返回严格两键 ``tool_result`` 与 ``validation_error``；前者保留
    ``execute_tool_call()`` 的原始结果对象，后者只允许是 I1f 识别出的
    执行前校验错误或 ``None``。本函数不请求 correction、不重试工具，
    也不进入 candidate、Reflection、Refinement 或公开结果映射。
    """
    if (
        type(run_context) is not dict
        or "step" not in run_context
        or "logs" not in run_context
    ):
        raise ValueError("Invalid run_context")
    step = run_context.get("step")
    if not type(step) is int or not (0 <= step <= MAX_STEPS):
        raise ValueError("Invalid run_context")
    if not type(run_context.get("logs")) is list:
        raise ValueError("Invalid run_context")
    step_before = run_context.get("step")
    logs_length_before = len(run_context.get("logs"))
    tool_result = execute_tool_call(
        tool_name,
        raw_arguments,
        normalized_request,
        run_context=run_context,
    )
    validation_error = extract_preexecution_action_validation_error(
        tool_result=tool_result,
        run_context=run_context,
        step_before=step_before,
        logs_length_before=logs_length_before,
    )
    return {"tool_result": tool_result, "validation_error": validation_error}


def raise_for_terminal_tool_outcome(
    tool_name: str,
    tool_result: dict[str, object],
    *,
    run_context: dict[str, object],
    step_before: int,
    logs_length_before: int,
) -> None:
    """识别 C4a-2b2 的两个精确工具终点；其他结果正常返回。"""
    if not isinstance(tool_result, dict):
        return None
    if not isinstance(run_context, dict):
        return None
    if type(step_before) is not int or step_before < 0:
        return None
    if type(tool_name) is not str or not tool_name.strip():
        return None
    if type(logs_length_before) is not int or logs_length_before < 0:
        return None
    step = run_context.get("step", 0)
    if type(step) is not int or step < 0:
        return None
    logs = run_context.get("logs")
    if not isinstance(logs, list):
        return None
    request_id = run_context.get("request_id")
    if type(request_id) is not str or not request_id.strip():
        return None

    # 真实工具执行必须让 step 与七字段日志各精确增加 1。
    if step != step_before + 1:
        return
    if len(logs) != logs_length_before + 1:
        return

    new_log = logs[logs_length_before]
    if not isinstance(new_log, dict):
        return None
    if set(new_log.keys()) != set(CALL_LOG_FIELDS):
        return None
    if (
        type(new_log.get("event_type")) is not str
        or new_log.get("event_type") != "tool_call"
    ):
        return None
    if (
        type(new_log.get("tool_name")) is not str
        or new_log.get("tool_name") != tool_name
    ):
        return None
    if (
        type(new_log.get("request_id")) is not str
        or new_log.get("request_id") != request_id
    ):
        return None
    if type(new_log.get("step")) is not int or new_log.get("step") != step:
        return None

    error = tool_result.get("error")
    if (
        tool_result.get("ok") is False
        and tool_result.get("retryable") is False
        and type(error) is str
        and error.strip()
    ):
        raise TerminalToolOutcomeError(
            status="tool_failure",
            detail=error.strip(),
        )
    results = tool_result.get("results")
    if (
        tool_name == "search_web"
        and tool_result.get("ok") is True
        and isinstance(results, list)
        and len(results) == 0
    ):
        raise TerminalToolOutcomeError(
            status="insufficient_evidence",
            detail="搜索工具已成功执行，但没有取得可用于生成摘要的真实证据。",
        )
    return None


def create_deepseek_client() -> OpenAI:
    """复用已 PASS 配置，创建真实 DeepSeek 客户端但不发起模型调用。"""
    load_dotenv()
    api_key = os.environ.get("DEEPSEEK_API_KEY")
    if not api_key:
        raise RuntimeError("DeepSeek API key is missing.")
    return OpenAI(api_key=api_key, base_url=DEEPSEEK_BASE_URL)


# 发起一次 Action correction 的模型调用
def request_action_correction(
    correction_messages: list[object],
    client: OpenAI | None = None,
    *,
    run_context: dict[str, object],
) -> object:
    """发起恰好一次 Action correction 模型调用并原样返回响应。

    ``correction_messages`` 由后续编排层按原顺序准备：system、user、
    原始完整 invalid assistant message、与其 ``tool_call_id`` 精确配对的
    I1b Tool Observation。本函数只负责一次真实模型调用及其共享 step / 日志，
    不修改消息列表，也不解析或执行返回的修正 Action。调用方必须先通过
    I1a 策略预算门；本函数内部的 ``reserve_call_step`` 只保留全局硬门。
    """
    if not type(correction_messages) is list or not correction_messages:
        raise ValueError("correction_messages must be a non-empty list")
    if client is None:
        client = create_deepseek_client()
    call_step = reserve_call_step(run_context)
    perf_counter_start = perf_counter()
    try:
        response = client.chat.completions.create(
            model=DEEPSEEK_MODEL,
            messages=correction_messages,
            tools=build_tool_schemas(),
            stream=False,
            extra_body={"thinking": {"type": "disabled"}},
        )
    except Exception as e:
        perf_counter_end = perf_counter()
        append_call_log(
            run_context,
            error=type(e).__name__,
            duration_ms=max(0, int((perf_counter_end - perf_counter_start) * 1000)),
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
            duration_ms=max(0, int((perf_counter_end - perf_counter_start) * 1000)),
            step=call_step,
            event_type="model_call",
            model=DEEPSEEK_MODEL,
            tool_name=None,
        )
        return response


# 解析单个工具调用响应的函数
def parse_single_tool_action_response(
    response: object,
) -> dict[str, object]:
    """从模型响应中提取一个结构明确、内容仍未信任的 Tool Action。

    本函数只守住 SDK 响应外壳、恰好一个 choice / tool call 和可关联的原始
    ``tool_call_id``；返回原始 assistant message、工具名与原始参数，不解析
    JSON、不查工具注册表，也不执行 Action。所有结构错误统一显式抛
    ``ToolActionProtocolError``（它是 ``RuntimeError`` 的窄子类）。
    """
    if response is None:
        raise ToolActionProtocolError("Response must not be empty.")

    if not hasattr(response, "choices"):
        raise ToolActionProtocolError("Response must have 'choices' key.")
    choices = response.choices
    if not type(choices) is list or len(choices) != 1:
        raise ToolActionProtocolError("Response must have exactly one choice.")
    choice = choices[0]
    if not hasattr(choice, "finish_reason"):
        raise ToolActionProtocolError("Choice must have 'finish_reason' key.")
    finish_reason = choice.finish_reason
    if type(finish_reason) is not str or finish_reason != "tool_calls":
        raise ToolActionProtocolError("Finish reason must be 'tool_calls'.")
    if not hasattr(choice, "message"):
        raise ToolActionProtocolError("Choice must have 'message' key.")
    message = choice.message
    if not hasattr(message, "tool_calls"):
        raise ToolActionProtocolError("Message must have 'tool_calls' key.")
    tool_calls = message.tool_calls
    if not type(tool_calls) is list or len(tool_calls) != 1:
        raise ToolActionProtocolError("Message must have exactly one tool call.")
    tool_call = tool_calls[0]
    if not hasattr(tool_call, "id"):
        raise ToolActionProtocolError("Tool call must have 'id' key.")
    tool_call_id = tool_call.id
    if not type(tool_call_id) is str or not tool_call_id.strip():
        raise ToolActionProtocolError("Tool call ID must be a non-empty string.")
    if not hasattr(tool_call, "function"):
        raise ToolActionProtocolError("Tool call must have 'function' key.")
    if not hasattr(tool_call.function, "name"):
        raise ToolActionProtocolError("Function must have 'name' key.")
    if not hasattr(tool_call.function, "arguments"):
        raise ToolActionProtocolError("Function must have 'arguments' key.")
    tool_name = tool_call.function.name
    if tool_name is None:
        raise ToolActionProtocolError("Function name must not be None.")
    raw_arguments = tool_call.function.arguments

    return {
        "assistant_message": message,
        "tool_call_id": tool_call_id,
        "tool_name": tool_name,
        "raw_arguments": raw_arguments,
    }


# 请求并解析一次 Action correction 的最小编排
def request_and_parse_action_correction(
    base_messages: list[object],
    invalid_action: dict[str, object],
    validation_error: str,
    corrections_used: int,
    client: OpenAI | None = None,
    *,
    run_context: dict[str, object],
) -> dict[str, object]:
    """请求并解析一次 Action correction，不执行修正后的 Action。

    ``invalid_action`` 是 I1d 对首次非法响应给出的严格四键结果；成功时返回
    新的纠错消息历史、仍未信任的修正 Action，以及递增后的局部纠错次数。
    """
    if type(base_messages) is not list or not base_messages:
        raise ValueError("base_messages must be a non-empty built-in list.")
    expected_action_keys = {
        "assistant_message",
        "tool_call_id",
        "tool_name",
        "raw_arguments",
    }

    if type(invalid_action) is not dict or set(invalid_action) != expected_action_keys:
        raise ValueError("invalid_action must be the exact I1d four-key result.")

    if not run_context or not isinstance(run_context, dict):
        raise ToolActionProtocolError("run_context must be a non-empty dict.")
    observation = build_action_validation_observation(
        invalid_action["tool_call_id"],
        validation_error,
    )

    budget = has_action_correction_budget(
        run_context["step"],
        corrections_used,
    )

    if not budget:
        if corrections_used >= MAX_ACTION_CORRECTIONS:
            reason = "max_action_corrections"
        else:
            reason = "insufficient_completion_steps"

        raise ActionCorrectionBudgetError(
            reason=reason,
            current_step=run_context["step"],
            corrections_used=corrections_used,
            last_error=validation_error.strip(),
        )
    correction_messages = list(base_messages)

    correction_messages.extend(
        [
            invalid_action["assistant_message"],
            observation,
        ]
    )

    next_corrections_used = corrections_used + 1
    raw_response = request_action_correction(
        correction_messages,
        client=client,
        run_context=run_context,
    )
    corrected_action = parse_single_tool_action_response(raw_response)
    return {
        "correction_messages": correction_messages,
        "corrected_action": corrected_action,
        "corrections_used": next_corrections_used,
    }


def run_tool_action_phase_with_one_correction(
    base_messages: list[object],
    initial_action: dict[str, object],
    normalized_request: dict[str, str],
    client: OpenAI | None = None,
    *,
    run_context: dict[str, object],
) -> dict[str, object]:
    """运行首次 Action，并在可信执行前拒绝时至多请求一次修正 Action。

    成功时返回严格四键 ``messages``、``action``、``tool_result`` 与
    ``corrections_used``，停在工具 retry、candidate、Reflection、Refinement
    和公开结果映射之前。预算或下层调用的窄异常按原对象继续传播。
    """
    if type(base_messages) is not list or not base_messages:
        raise ValueError("base_messages must be a non-empty list")
    expected_action_keys = {
        "assistant_message",
        "tool_call_id",
        "tool_name",
        "raw_arguments",
    }
    if type(initial_action) is not dict or set(initial_action) != expected_action_keys:
        raise ValueError(
            "initial_action must be a dict with keys: "
            + ", ".join(expected_action_keys)
        )
    corrections_used = 0
    initial_execution = execute_and_classify_tool_action(
        initial_action["tool_name"],
        initial_action["raw_arguments"],
        normalized_request,
        run_context=run_context,
    )
    if initial_execution["validation_error"] is None:
        return {
            "messages": base_messages,
            "action": initial_action,
            "tool_result": initial_execution["tool_result"],
            "corrections_used": corrections_used,
        }
    correction = request_and_parse_action_correction(
        base_messages=base_messages,
        invalid_action=initial_action,
        validation_error=initial_execution["validation_error"],
        corrections_used=0,
        client=client,
        run_context=run_context,
    )
    corrected_action = correction["corrected_action"]
    corrected_execution = execute_and_classify_tool_action(
        corrected_action["tool_name"],
        corrected_action["raw_arguments"],
        normalized_request,
        run_context=run_context,
    )
    if corrected_execution["validation_error"] is None:
        return {
            "messages": correction["correction_messages"],
            "action": correction["corrected_action"],
            "tool_result": corrected_execution["tool_result"],
            "corrections_used": correction["corrections_used"],
        }

    request_and_parse_action_correction(
        base_messages=correction["correction_messages"],
        invalid_action=correction["corrected_action"],
        validation_error=corrected_execution["validation_error"],
        corrections_used=correction["corrections_used"],
        client=client,
        run_context=run_context,
    )


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
    initial_action = parse_single_tool_action_response(response1)
    action_phase_step_before = run_context["step"]
    action_phase_logs_length_before = len(run_context["logs"])
    action_phase = run_tool_action_phase_with_one_correction(
        base_messages=messages,
        initial_action=initial_action,
        normalized_request=normalized_request,
        client=client,
        run_context=run_context,
    )
    messages = action_phase["messages"]
    final_action = action_phase["action"]
    tool_result = action_phase["tool_result"]
    corrections_used = action_phase["corrections_used"]

    assistant_message = final_action["assistant_message"]
    tool_call_id = final_action["tool_call_id"]
    tool_name = final_action["tool_name"]
    raw_arguments = final_action["raw_arguments"]
    tool_step_before = action_phase_step_before + corrections_used
    tool_logs_length_before = action_phase_logs_length_before + corrections_used
    if tool_result.get("ok") is False and tool_result.get("retryable") is True:
        # C4a-2a：最多一次同名、同原始参数重试；每次真实尝试仍通过
        # execute_tool_call 独立占步、计时和写日志。
        if MAX_TOOL_RETRIES > 0:
            if run_context["step"] == MAX_STEPS:
                # 第二次真实工具调用前没有剩余 step，发出专用内部信号。
                raise AutoRecoveryExhaustedError(
                    reason="max_steps",
                    attempts=1,
                    last_error=tool_result.get("error"),
                )
            retry_completion_budget = has_tool_retry_completion_budget(
                run_context["step"]
            )
            if not retry_completion_budget:
                raise ToolRetryCompletionBudgetError(
                    current_step=run_context["step"],
                    attempts=1,
                    last_error=tool_result.get("error"),
                )
            # 额外真实尝试发生后，只对仍可重试的失败发出耗尽信号。
            tool_step_before = run_context["step"]
            tool_logs_length_before = len(run_context["logs"])
            tool_result = execute_tool_call(
                tool_name,
                raw_arguments,
                normalized_request,
                run_context=run_context,
            )
            if tool_result.get("ok") is False and tool_result.get("retryable") is True:
                raise AutoRecoveryExhaustedError(
                    reason="max_tool_retries",
                    attempts=2,
                    last_error=tool_result.get("error"),
                )
    raise_for_terminal_tool_outcome(
        tool_name,
        tool_result,
        run_context=run_context,
        step_before=tool_step_before,
        logs_length_before=tool_logs_length_before,
    )
    if tool_result.get("ok") is not True:
        raise RuntimeError(
            f"工具调用失败: {tool_result.get('error', '无法生成正常候选摘要')}"
        )
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

    candidate_summary = resolve_candidate_summary_stage(
        response2,
        messages,
        normalized_request,
        tool_name,
        tool_result,
        client=client,
        run_context=run_context,
    )
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


# 把首次 Candidate 响应、至多一次恢复与候选阶段停止组合成一个内部解析器。
def resolve_candidate_summary_stage(
    initial_response: object,
    base_messages: list[object],
    normalized_request: dict[str, str],
    tool_name: str,
    tool_result: dict[str, object],
    client: OpenAI | None = None,
    *,
    run_context: dict[str, object],
) -> str:
    """返回合法 Candidate 原文，或发出带真实人工接管证据的窄停止信号。

    首次响应先由 I1b 分类：valid 直接返回，terminal 不恢复，recoverable
    只允许进入 I1e 一次。恢复后的 valid 返回；terminal 或 recoverable 均停止，
    不得递归或再次恢复。只有确定停止时才从真实工具结果派生来源白名单。

    本函数不得把失败 Candidate 加入消息历史，不得重新执行工具、调用 Reflection /
    Refinement、构造公开三字段结果或吞掉 Provider / SDK 等非预算异常。
    """
    initial_classification = classify_candidate_summary_response(initial_response)
    initial_kind = initial_classification["classification"]

    if initial_kind == "valid":
        return initial_classification["candidate_summary"]

    if initial_kind == "terminal":
        allowed_sources = derive_allowed_sources(
            normalized_request,
            tool_name,
            tool_result,
        )
        raise CandidateSummaryStageStopError(
            stop_kind="terminal_response",
            candidate_reason=initial_classification["reason"],
            recovery_attempts=0,
            current_step=run_context["step"],
            allowed_sources=allowed_sources,
        )

    try:
        recovered_classification = attempt_candidate_recovery_once(
            base_messages,
            initial_classification,
            client=client,
            run_context=run_context,
        )
    except CandidateRecoveryCompletionBudgetError as exc:
        allowed_sources = derive_allowed_sources(
            normalized_request,
            tool_name,
            tool_result,
        )
        raise CandidateSummaryStageStopError(
            stop_kind="insufficient_completion_steps",
            candidate_reason=exc.recoverable_reason,
            recovery_attempts=0,
            current_step=exc.current_step,
            allowed_sources=allowed_sources,
        ) from exc

    recovered_kind = recovered_classification["classification"]
    if recovered_kind == "valid":
        return recovered_classification["candidate_summary"]

    allowed_sources = derive_allowed_sources(
        normalized_request,
        tool_name,
        tool_result,
    )
    raise CandidateSummaryStageStopError(
        stop_kind=(
            "terminal_response"
            if recovered_kind == "terminal"
            else "recovery_exhausted"
        ),
        candidate_reason=recovered_classification["reason"],
        recovery_attempts=1,
        current_step=run_context["step"],
        allowed_sources=allowed_sources,
    )


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
        'status 必须是字符串 "success"；'
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
        '示例：{"status": "success", "summary": "...", "sources": ["..."]}。'
        '成功候选必须满足：status == "success"，summary 为非空字符串，'
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
            isinstance(source, str) and source.strip() != "" for source in sources
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
    三字段结果；当前已支持一次可重试工具首败后的同参数重试，并把
    二次可重试失败或重试前无剩余 step 映射为 ``needs_manual``，把
    真实不可重试工具失败映射为 ``tool_failure``，把搜索成功但零证据
    映射为 ``insufficient_evidence``。HITL 和其他未映射的工具、模型
    与校验异常继续向上抛出。
    """
    normalized_request, invalid_result = prepare_request(request)
    if normalized_request is None:
        return invalid_result
    if client is None:
        client = create_deepseek_client()
    run_context = create_run_context()
    # 把已识别的停止信号窄映射为对应的固定三字段结果。
    try:
        gen_res = generate_candidate_summary(
            normalized_request,
            client,
            run_context=run_context,
        )
    except CandidateSummaryStageStopError as exc:
        if type(exc) is not CandidateSummaryStageStopError:
            raise

        stop_kind = getattr(exc, "stop_kind", None)
        candidate_reason = getattr(exc, "candidate_reason", None)
        recovery_attempts = getattr(exc, "recovery_attempts", None)
        current_step = getattr(exc, "current_step", None)
        allowed_sources = getattr(exc, "allowed_sources", None)
        if (
            type(stop_kind) is not str
            or type(candidate_reason) is not str
            or type(recovery_attempts) is not int
            or type(current_step) is not int
            or not (1 <= current_step <= MAX_STEPS)
            or type(allowed_sources) is not list
            or not allowed_sources
            or not all(
                type(source) is str and bool(source.strip())
                for source in allowed_sources
            )
        ):
            raise

        terminal_reason_texts = {
            "content_filter": "模型服务的安全过滤终止了 Candidate 响应。",
            "insufficient_system_resource": (
                "模型服务因系统资源不足终止了 Candidate 响应。"
            ),
            "missing_finish_reason": (
                "Candidate 响应缺少 finish_reason，或该字段值为 None，"
                "无法确认模型正常结束。"
            ),
            "unknown_finish_reason": (
                "Candidate 响应的 finish_reason 不在允许范围内，"
                "无法确认模型正常结束。"
            ),
        }
        recoverable_reason_texts = {
            "invalid_response_shape": "Candidate 响应外壳结构不符合协议。",
            "invalid_candidate_content": (
                "Candidate 响应含有 content 字段，但其值不能作为非空候选正文。"
            ),
            "length": "Candidate 响应因长度限制未能完整结束。",
            "unexpected_tool_calls": (
                "Candidate 响应意外包含工具调用，而该阶段只允许返回候选正文。"
            ),
        }

        if stop_kind == "terminal_response":
            reason_text = terminal_reason_texts.get(candidate_reason)
            if reason_text is None or recovery_attempts not in {0, 1}:
                raise
            if recovery_attempts == 0:
                summary_text = (
                    "候选摘要阶段已停止：首次 Candidate 响应触发不可恢复的"
                    "终止条件，未发起 Candidate recovery；"
                    f"{reason_text}"
                )
            else:
                summary_text = (
                    "候选摘要阶段已停止：首次 Candidate 失败后已执行唯一一次"
                    "证据受限 Candidate recovery，但恢复响应触发不可恢复的"
                    "终止条件；"
                    f"{reason_text}"
                )
        elif stop_kind == "recovery_exhausted":
            reason_text = recoverable_reason_texts.get(candidate_reason)
            if reason_text is None or recovery_attempts != 1:
                raise
            summary_text = (
                "候选摘要阶段已停止：首次 Candidate 响应不合法，已执行唯一一次"
                "仅依据既有真实 Tool Observation 的证据受限 Candidate recovery；"
                "恢复响应仍未得到合法 Candidate；"
                f"{reason_text}"
            )
        elif stop_kind == "insufficient_completion_steps":
            reason_text = recoverable_reason_texts.get(candidate_reason)
            if reason_text is None or recovery_attempts != 0:
                raise
            summary_text = (
                "候选摘要阶段已停止：首次 Candidate 响应不合法但属于可恢复分类；"
                f"{reason_text}"
                f"当前累计 step 为 {current_step}，全局上限为 {MAX_STEPS}；"
                "Candidate recovery、Reflection 与 Refinement 的完整可信链"
                f"仍需 {MIN_STEPS_FOR_CANDIDATE_RECOVERY_CHAIN} 个调用 step"
                "（各 1 次），剩余预算不足；"
                "本次 Candidate recovery 模型调用没有发生。"
            )
        else:
            raise

        summary_text += (
            "没有任何 Candidate / 摘要通过校验；"
            "结果中的 sources 仅是本轮真实工具取得、供人工复核的证据池，"
            "不代表已验证摘要引用；"
            "Agent 已停止自治并交还人工。"
        )
        return make_result(
            "needs_manual",
            summary_text,
            list(exc.allowed_sources),
        )
    except AutoRecoveryExhaustedError as exc:
        if exc.reason == "max_steps":
            threshold_text = f"总步骤上限 {MAX_STEPS}"
        else:
            threshold_text = f"工具重试上限 {MAX_TOOL_RETRIES}"
        summary_text = (
            f"自动恢复已停止：已达到{threshold_text}；"
            f"工具实际尝试 {exc.attempts} 次；"
            f"最后错误：{exc.last_error}。"
            "当前尚未取得足够的可信证据，已停止自治并交由人工决定下一步。"
        )
        return make_result("needs_manual", summary_text, [])
    except (ActionCorrectionBudgetError, ToolRetryCompletionBudgetError) as exc:
        if type(exc) is ActionCorrectionBudgetError:
            if exc.reason == "max_action_corrections":
                summary_text = (
                    "Action 修正已停止：已达到局部 Action 修正上限 "
                    f"{MAX_ACTION_CORRECTIONS} 次；已使用修正 {exc.corrections_used} 次，"
                    f"当前累计 step 为 {exc.current_step}；"
                    f"最后一条安全校验错误：{exc.last_error}。"
                    "尚未执行真实工具，因此没有可用于生成可信摘要的真实证据；"
                    "已停止自治并交由人工决定下一步。"
                )
            elif exc.reason == "insufficient_completion_steps":
                summary_text = (
                    "Action 修正已停止：当前累计 step 为 "
                    f"{exc.current_step}，全局上限为 {MAX_STEPS}；"
                    "继续还需 1 次 Action correction，并在取得合法 Action 后"
                    f"至少保留 {MIN_STEPS_AFTER_VALID_ACTION} 个调用 step，"
                    "剩余全局预算无法容纳这条完整可信链；"
                    f"已使用 Action 修正 {exc.corrections_used} 次；"
                    f"最后一条安全校验错误：{exc.last_error}。"
                    "本次未继续纠错，也尚未执行真实工具，"
                    "因此没有可用于生成可信摘要的真实证据；"
                    "已停止自治并交由人工决定下一步。"
                )
            else:
                raise
        elif type(exc) is ToolRetryCompletionBudgetError:
            summary_text = (
                "工具完整链重试已停止：第一次真实工具尝试返回可重试失败；"
                f"当前累计 step 为 {exc.current_step}，全局上限为 {MAX_STEPS}，"
                "而工具 retry、candidate、Reflection 与 Refinement "
                f"的完整可信链至少需要 {MIN_STEPS_AFTER_VALID_ACTION} 个调用 step，"
                "剩余全局预算不足；"
                f"工具实际尝试 {exc.attempts} 次；"
                f"最后一条安全工具错误：{exc.last_error}。"
                "第二次工具调用尚未执行，当前仍缺少可用于生成可信摘要的成功工具证据；"
                "已停止自治并交由人工决定下一步。"
            )
        else:
            raise
        return make_result("needs_manual", summary_text, [])
    except TerminalToolOutcomeError as exc:
        error_status = exc.status
        if error_status == "tool_failure":
            summary_text = (
                "工具已真实执行，但返回不可重试失败："
                f"{exc.detail}。已停止后续摘要生成。"
            )
        elif error_status == "insufficient_evidence":
            summary_text = (
                f"{exc.detail} " "已停止后续摘要生成，不会凭模型常识补写摘要或来源。"
            )
        return make_result(exc.status, summary_text, [])
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

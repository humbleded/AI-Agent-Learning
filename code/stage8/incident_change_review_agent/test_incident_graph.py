"""G8-00-I9：整图分支与外部调用边界的长期 pytest。

从项目根目录运行：
    .venv/Scripts/python.exe -m pytest code/stage8/incident_change_review_agent/test_incident_graph.py -q

测试目的：
    把已经通过的 Graph 行为固化成一份可重复运行的回归测试，既检查最终
    State，也用 spy 证明不该发生的工具或模型调用确实没有发生。

通过标准：
    1. 正常 invoke：工具和 fake 模型各一次，返回完整正确 State，输入不变。
    2. 正常 stream：创建 iterator 时不执行；首个 v2 part 到达时模型仍为零次；
       完整消费后恰好五个 part，Node 顺序正确，输入不变。
    3. 证据不足：稳定写入 evidence_insufficient，工具和模型均为零次。
    4. 已批准工具超时或返回非法数据：统一写入 diagnostic_unavailable，随后
       稳定写入 tool_failure；工具一次，模型零次。
    5. max_steps=0：正常返回 max_steps_reached，工具和模型均为零次。
    6. None 或未批准工具名：只做 Node 级拒绝，批准工具均为零次。
    7. 信号选择：只有 alerts 时调用延迟工具，只有 logs 时调用错误工具；
       两条路线都精确验证最终 State、v2 updates 顺序和外部调用次数。

范围边界：
    全部测试离线运行；不得读取真实 key、创建真实客户端或发网络请求。
    本检查点不测试 checkpointer、thread state、interrupt/resume、长期 Memory，
    也不故意触发 GraphRecursionError。
"""

from copy import deepcopy
from unittest.mock import Mock

import pytest

import incident_graph as graph_module


NORMAL_FACTS_SUMMARY = (
    "service=payment\n"
    "alerts=payment 5xx rate high\n"
    "logs=payment request timeout | database pool wait exceeded\n"
    "config=db_pool_size=20 | request_timeout_ms=1000\n"
    "change_request=raise payment request timeout from 1000ms to 2000ms"
)

EMPTY_SIGNAL_FACTS_SUMMARY = (
    "service=payment\n"
    "alerts=none\n"
    "logs=none\n"
    "config=db_pool_size=20 | request_timeout_ms=1000\n"
    "change_request=raise payment request timeout from 1000ms to 2000ms"
)

NORMAL_CONCLUSION_PROMPT = (
    "事实摘要：\n"
    f"{NORMAL_FACTS_SUMMARY}\n\n"
    "证据：\n"
    "- payment request timeout\n"
    "- database pool wait exceeded\n\n"
    "请根据以上信息，只能根据给出的事实和证据回答，不得补造事实，"
    "不得声称已经执行变更，信息有缺口时明确表达不确定性，"
    "按“根因判断 / 证据依据 / 变更评审”三部分输出结论。"
)

SIGNAL_SELECTION_CASES = [
    pytest.param(
        ("payment p99 latency high",),
        (),
        "get_latency_summary",
        ("payment p99 latency high",),
        (
            "service=payment\n"
            "alerts=payment p99 latency high\n"
            "logs=none\n"
            "config=db_pool_size=20 | request_timeout_ms=1000\n"
            "change_request=raise payment request timeout from 1000ms to 2000ms"
        ),
        id="alerts-only-selects-latency-summary",
    ),
    pytest.param(
        (),
        ("payment request timeout",),
        "get_recent_errors",
        ("payment request timeout",),
        (
            "service=payment\n"
            "alerts=none\n"
            "logs=payment request timeout\n"
            "config=db_pool_size=20 | request_timeout_ms=1000\n"
            "change_request=raise payment request timeout from 1000ms to 2000ms"
        ),
        id="logs-only-selects-recent-errors",
    ),
]


@pytest.fixture(autouse=True)
def block_real_deepseek(
    monkeypatch: pytest.MonkeyPatch,
) -> Mock:
    """阻断真实 Provider，并把调用记录器交给每个测试。"""

    provider_tripwire = Mock(
        side_effect=AssertionError(
            "I9 tests must not create a real DeepSeek client"
        )
    )
    monkeypatch.setattr(
        graph_module,
        "create_deepseek_client",
        provider_tripwire,
    )
    return provider_tripwire


def test_normal_invoke_reaches_conclusion_and_respects_call_bounds(
    monkeypatch: pytest.MonkeyPatch,
    block_real_deepseek: Mock,
) -> None:
    """正常 invoke 同时验证最终 State、reducer、spy 与输入不可变。"""

    tool_spy = Mock(wraps=graph_module.get_recent_errors)
    monkeypatch.setitem(
        graph_module.APPROVED_READONLY_TOOLS,
        "get_recent_errors",
        tool_spy,
    )
    other_tool_tripwire = Mock(
        side_effect=AssertionError(
            "normal graph selected an unexpected diagnostic tool"
        )
    )
    monkeypatch.setitem(
        graph_module.APPROVED_READONLY_TOOLS,
        "get_latency_summary",
        other_tool_tripwire,
    )
    generate_text = Mock(return_value="  fake graph conclusion  ")
    initial_state = graph_module.build_initial_state()
    original_state = deepcopy(initial_state)

    result = graph_module.invoke_incident(
        initial_state,
        generate_text=generate_text,
    )

    expected_state = deepcopy(original_state)
    expected_state.update(
        facts_summary=NORMAL_FACTS_SUMMARY,
        evidence=original_state["logs"].copy(),
        evidence_status="enough",
        requested_tool=None,
        tool_failed=False,
        tool_error=None,
        step_count=1,
        stop_reason=None,
        conclusion="fake graph conclusion",
    )
    assert result == expected_state
    assert set(result) == set(graph_module.IncidentState.__annotations__)
    assert initial_state == original_state
    tool_spy.assert_called_once()
    other_tool_tripwire.assert_not_called()
    generate_text.assert_called_once_with(NORMAL_CONCLUSION_PROMPT)
    block_real_deepseek.assert_not_called()


def test_normal_stream_yields_v2_updates_incrementally(
    monkeypatch: pytest.MonkeyPatch,
    block_real_deepseek: Mock,
) -> None:
    """正常 stream 验证惰性、v2 外壳、Node 顺序与调用次数。"""

    tool_spy = Mock(wraps=graph_module.get_recent_errors)
    monkeypatch.setitem(
        graph_module.APPROVED_READONLY_TOOLS,
        "get_recent_errors",
        tool_spy,
    )
    other_tool_tripwire = Mock(
        side_effect=AssertionError(
            "normal graph selected an unexpected diagnostic tool"
        )
    )
    monkeypatch.setitem(
        graph_module.APPROVED_READONLY_TOOLS,
        "get_latency_summary",
        other_tool_tripwire,
    )
    generate_text = Mock(return_value="  fake graph conclusion  ")
    initial_state = graph_module.build_initial_state()
    original_state = deepcopy(initial_state)

    parts_iterator = graph_module.stream_incident_updates(
        initial_state,
        generate_text=generate_text,
    )

    generate_text.assert_not_called()
    tool_spy.assert_not_called()
    other_tool_tripwire.assert_not_called()
    block_real_deepseek.assert_not_called()

    first_part = next(parts_iterator)
    assert first_part == {
        "type": "updates",
        "ns": (),
        "data": {
            "organize_facts": {
                "facts_summary": NORMAL_FACTS_SUMMARY,
            }
        },
    }
    generate_text.assert_not_called()
    tool_spy.assert_not_called()
    other_tool_tripwire.assert_not_called()

    parts = [first_part, *parts_iterator]
    assert parts == [
        {
            "type": "updates",
            "ns": (),
            "data": {
                "organize_facts": {
                    "facts_summary": NORMAL_FACTS_SUMMARY,
                }
            },
        },
        {
            "type": "updates",
            "ns": (),
            "data": {
                "review_evidence": {
                    "evidence_status": "unknown",
                    "requested_tool": "get_recent_errors",
                }
            },
        },
        {
            "type": "updates",
            "ns": (),
            "data": {
                "run_readonly_diagnostic": {
                    "tool_failed": False,
                    "tool_error": None,
                    "step_count": 1,
                    "evidence": original_state["logs"],
                }
            },
        },
        {
            "type": "updates",
            "ns": (),
            "data": {
                "review_evidence": {
                    "evidence_status": "enough",
                    "requested_tool": None,
                }
            },
        },
        {
            "type": "updates",
            "ns": (),
            "data": {
                "build_conclusion": {
                    "conclusion": "fake graph conclusion",
                }
            },
        },
    ]
    assert initial_state == original_state
    tool_spy.assert_called_once()
    other_tool_tripwire.assert_not_called()
    generate_text.assert_called_once_with(NORMAL_CONCLUSION_PROMPT)
    block_real_deepseek.assert_not_called()


@pytest.mark.parametrize(
    (
        "alerts",
        "logs",
        "selected_tool",
        "expected_evidence",
        "expected_facts_summary",
    ),
    SIGNAL_SELECTION_CASES,
)
def test_signal_specific_tool_selection_reaches_conclusion(
    alerts: tuple[str, ...],
    logs: tuple[str, ...],
    selected_tool: str,
    expected_evidence: tuple[str, ...],
    expected_facts_summary: str,
    monkeypatch: pytest.MonkeyPatch,
    block_real_deepseek: Mock,
) -> None:
    """每种输入信号只调用对应工具，并返回完整的成功 State。"""

    recent_errors_spy = Mock(wraps=graph_module.get_recent_errors)
    latency_summary_spy = Mock(wraps=graph_module.get_latency_summary)
    monkeypatch.setitem(
        graph_module.APPROVED_READONLY_TOOLS,
        "get_recent_errors",
        recent_errors_spy,
    )
    monkeypatch.setitem(
        graph_module.APPROVED_READONLY_TOOLS,
        "get_latency_summary",
        latency_summary_spy,
    )
    generate_text = Mock(return_value="  fake graph conclusion  ")
    initial_state = graph_module.build_initial_state(max_steps=2)
    initial_state["alerts"] = list(alerts)
    initial_state["logs"] = list(logs)
    original_state = deepcopy(initial_state)

    result = graph_module.invoke_incident(
        initial_state,
        generate_text=generate_text,
    )

    expected_state = deepcopy(original_state)
    expected_state.update(
        facts_summary=expected_facts_summary,
        evidence=list(expected_evidence),
        evidence_status="enough",
        requested_tool=None,
        tool_failed=False,
        tool_error=None,
        step_count=1,
        stop_reason=None,
        conclusion="fake graph conclusion",
    )
    assert result == expected_state
    assert initial_state == original_state
    assert recent_errors_spy.call_count == int(
        selected_tool == "get_recent_errors"
    )
    assert latency_summary_spy.call_count == int(
        selected_tool == "get_latency_summary"
    )
    generate_text.assert_called_once()
    block_real_deepseek.assert_not_called()


@pytest.mark.parametrize(
    (
        "alerts",
        "logs",
        "selected_tool",
        "expected_evidence",
        "expected_facts_summary",
    ),
    SIGNAL_SELECTION_CASES,
)
def test_signal_specific_tool_selection_streams_exact_route(
    alerts: tuple[str, ...],
    logs: tuple[str, ...],
    selected_tool: str,
    expected_evidence: tuple[str, ...],
    expected_facts_summary: str,
    monkeypatch: pytest.MonkeyPatch,
    block_real_deepseek: Mock,
) -> None:
    """每种输入信号产生完整 v2 parts 和唯一的正确工具路线。"""

    recent_errors_spy = Mock(wraps=graph_module.get_recent_errors)
    latency_summary_spy = Mock(wraps=graph_module.get_latency_summary)
    monkeypatch.setitem(
        graph_module.APPROVED_READONLY_TOOLS,
        "get_recent_errors",
        recent_errors_spy,
    )
    monkeypatch.setitem(
        graph_module.APPROVED_READONLY_TOOLS,
        "get_latency_summary",
        latency_summary_spy,
    )
    generate_text = Mock(return_value="  fake graph conclusion  ")
    initial_state = graph_module.build_initial_state(max_steps=2)
    initial_state["alerts"] = list(alerts)
    initial_state["logs"] = list(logs)
    original_state = deepcopy(initial_state)

    parts = list(
        graph_module.stream_incident_updates(
            initial_state,
            generate_text=generate_text,
        )
    )

    assert all(part["type"] == "updates" for part in parts)
    assert all(part["ns"] == () for part in parts)
    assert [next(iter(part["data"])) for part in parts] == [
        "organize_facts",
        "review_evidence",
        "run_readonly_diagnostic",
        "review_evidence",
        "build_conclusion",
    ]
    assert parts[0]["data"] == {
        "organize_facts": {"facts_summary": expected_facts_summary}
    }
    assert parts[1]["data"] == {
        "review_evidence": {
            "evidence_status": "unknown",
            "requested_tool": selected_tool,
        }
    }
    assert parts[2]["data"] == {
        "run_readonly_diagnostic": {
            "tool_failed": False,
            "tool_error": None,
            "step_count": 1,
            "evidence": list(expected_evidence),
        }
    }
    assert parts[3]["data"] == {
        "review_evidence": {
            "evidence_status": "enough",
            "requested_tool": None,
        }
    }
    assert parts[4]["data"] == {
        "build_conclusion": {"conclusion": "fake graph conclusion"}
    }
    assert initial_state == original_state
    assert recent_errors_spy.call_count == int(
        selected_tool == "get_recent_errors"
    )
    assert latency_summary_spy.call_count == int(
        selected_tool == "get_latency_summary"
    )
    generate_text.assert_called_once()
    block_real_deepseek.assert_not_called()


def test_evidence_insufficient_stops_without_external_calls(
    monkeypatch: pytest.MonkeyPatch,
    block_real_deepseek: Mock,
) -> None:
    """没有 alerts/logs 时直接业务停止，不调用工具或模型。"""

    tool_tripwire = Mock(
        side_effect=AssertionError(
            "evidence-insufficient branch must not call a tool"
        )
    )
    for tool_name in graph_module.APPROVED_READONLY_TOOLS:
        monkeypatch.setitem(
            graph_module.APPROVED_READONLY_TOOLS,
            tool_name,
            tool_tripwire,
        )
    generate_text = Mock(
        side_effect=AssertionError(
            "evidence-insufficient branch must not call the model"
        )
    )
    initial_state = graph_module.build_initial_state()
    initial_state["alerts"] = []
    initial_state["logs"] = []
    original_state = deepcopy(initial_state)

    result = graph_module.invoke_incident(
        initial_state,
        generate_text=generate_text,
    )

    expected_state = deepcopy(original_state)
    expected_state.update(
        facts_summary=EMPTY_SIGNAL_FACTS_SUMMARY,
        evidence_status="insufficient",
        requested_tool=None,
        step_count=0,
        stop_reason="evidence_insufficient",
        conclusion=None,
    )
    assert result == expected_state
    assert set(result) == set(graph_module.IncidentState.__annotations__)
    assert initial_state == original_state
    tool_tripwire.assert_not_called()
    generate_text.assert_not_called()
    block_real_deepseek.assert_not_called()


@pytest.mark.parametrize(
    "failure_case",
    ["timeout", "invalid_result"],
)
def test_approved_tool_failure_becomes_stable_business_stop(
    failure_case: str,
    monkeypatch: pytest.MonkeyPatch,
    block_real_deepseek: Mock,
) -> None:
    """工具执行异常与非法返回值都归一化成同一业务停止结果。"""

    if failure_case == "timeout":
        tool_spy = Mock(
            side_effect=TimeoutError("diagnostic timeout")
        )
    else:
        tool_spy = Mock(return_value=["valid evidence", 123])
    monkeypatch.setitem(
        graph_module.APPROVED_READONLY_TOOLS,
        "get_recent_errors",
        tool_spy,
    )
    other_tool_tripwire = Mock(
        side_effect=AssertionError(
            "the graph requested an unexpected diagnostic tool"
        )
    )
    monkeypatch.setitem(
        graph_module.APPROVED_READONLY_TOOLS,
        "get_latency_summary",
        other_tool_tripwire,
    )
    generate_text = Mock(
        side_effect=AssertionError(
            "tool-failure branch must not call the model"
        )
    )
    initial_state = graph_module.build_initial_state()
    original_state = deepcopy(initial_state)

    result = graph_module.invoke_incident(
        initial_state,
        generate_text=generate_text,
    )

    expected_state = deepcopy(original_state)
    expected_state.update(
        facts_summary=NORMAL_FACTS_SUMMARY,
        evidence=[],
        evidence_status="unknown",
        requested_tool="get_recent_errors",
        tool_failed=True,
        tool_error="diagnostic_unavailable",
        step_count=1,
        stop_reason="tool_failure",
        conclusion=None,
    )
    assert result == expected_state
    assert set(result) == set(graph_module.IncidentState.__annotations__)
    assert initial_state == original_state
    tool_spy.assert_called_once()
    other_tool_tripwire.assert_not_called()
    generate_text.assert_not_called()
    block_real_deepseek.assert_not_called()


def test_zero_max_steps_stops_before_tool_or_model(
    monkeypatch: pytest.MonkeyPatch,
    block_real_deepseek: Mock,
) -> None:
    """max_steps=0 使用业务停止分支，不靠框架递归异常。"""

    tool_tripwire = Mock(
        side_effect=AssertionError(
            "max-steps branch must stop before calling a tool"
        )
    )
    for tool_name in graph_module.APPROVED_READONLY_TOOLS:
        monkeypatch.setitem(
            graph_module.APPROVED_READONLY_TOOLS,
            tool_name,
            tool_tripwire,
        )
    generate_text = Mock(
        side_effect=AssertionError(
            "max-steps branch must stop before calling the model"
        )
    )
    initial_state = graph_module.build_initial_state(max_steps=0)
    original_state = deepcopy(initial_state)

    result = graph_module.invoke_incident(
        initial_state,
        generate_text=generate_text,
    )

    expected_state = deepcopy(original_state)
    expected_state.update(
        facts_summary=NORMAL_FACTS_SUMMARY,
        evidence=[],
        evidence_status="unknown",
        requested_tool="get_recent_errors",
        tool_failed=False,
        tool_error=None,
        step_count=0,
        stop_reason="max_steps_reached",
        conclusion=None,
    )
    assert result == expected_state
    assert set(result) == set(graph_module.IncidentState.__annotations__)
    assert initial_state == original_state
    tool_tripwire.assert_not_called()
    generate_text.assert_not_called()
    block_real_deepseek.assert_not_called()


@pytest.mark.parametrize(
    "requested_tool",
    [None, "delete_production"],
)
def test_unapproved_tool_is_rejected_without_running_approved_tools(
    requested_tool: str | None,
    monkeypatch: pytest.MonkeyPatch,
    block_real_deepseek: Mock,
) -> None:
    """直接验证诊断 Node 对缺失或未批准工具名的拒绝边界。"""

    tool_tripwire = Mock(
        side_effect=AssertionError(
            "an unapproved request must not run any approved tool"
        )
    )
    for tool_name in graph_module.APPROVED_READONLY_TOOLS:
        monkeypatch.setitem(
            graph_module.APPROVED_READONLY_TOOLS,
            tool_name,
            tool_tripwire,
        )
    initial_state = graph_module.build_initial_state()
    initial_state["requested_tool"] = requested_tool
    initial_state["step_count"] = 2
    original_state = deepcopy(initial_state)

    result = graph_module.run_readonly_diagnostic(initial_state)

    assert result == {
        "tool_failed": True,
        "tool_error": "unapproved_tool",
        "step_count": original_state["step_count"] + 1,
    }
    assert initial_state == original_state
    tool_tripwire.assert_not_called()
    block_real_deepseek.assert_not_called()

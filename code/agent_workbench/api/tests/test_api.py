"""长期保护工作台适配边界；模型仅在测试中注入，不产生真实网络调用。

从仓库根目录运行：
    .venv/Scripts/python.exe -m pytest code/agent_workbench/api/tests -q
后续修改接口或课程核心时复跑，保护错误显示、状态累计与逐步事件转发。
"""

import importlib.util
import json
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import Mock

from fastapi.testclient import TestClient
import pytest


spec = importlib.util.spec_from_file_location("workbench_api", Path(__file__).resolve().parents[1] / "main.py")
api = importlib.util.module_from_spec(spec)
spec.loader.exec_module(api)
client = TestClient(api.app)


@pytest.fixture(autouse=True)
def no_network(monkeypatch):
    core = api.incident_core()
    tripwire = Mock(side_effect=AssertionError("API unit tests must not call the real provider"))
    monkeypatch.setattr(core, "create_deepseek_client", tripwire)
    yield
    tripwire.assert_not_called()


def frames(response):
    return [(part.splitlines()[0][7:], json.loads(part.splitlines()[1][6:])) for part in response.text.strip().split("\n\n")]


def test_health_and_presets_are_real_core_inputs():
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json()["modules"][0]["status"] == "available"
    presets = client.get("/api/incidents/presets").json()["presets"]
    assert [preset["id"] for preset in presets] == ["normal", "no_signals", "step_limit"]
    assert presets[0]["input"]["logs"] == api.incident_core().SAMPLE_INCIDENT["logs"]
    assert all(preset["fictional"] for preset in presets)


@pytest.mark.parametrize("payload", [{"preset_id": "unknown"}, {"preset_id": "normal", "key": "must-not-echo"}, {}])
def test_invalid_input_never_starts_run(payload):
    response = client.post("/api/incidents/stream", json=payload)
    assert response.status_code == 422
    assert response.json()["error"]["code"] == "INVALID_INPUT"
    assert "must-not-echo" not in response.text


def test_rag_todo_returns_explanatory_error(monkeypatch):
    monkeypatch.setattr(api, "rag_core", lambda: SimpleNamespace(build_ingest_graph=Mock(side_effect=NotImplementedError)))
    response = client.post("/api/rag/import")
    assert response.status_code == 409
    assert response.json()["error"]["code"] == "RAG_NOT_READY"
    assert response.json()["error"]["message"] == "文档导入流程尚未就绪，请完成读取流程后重试。"


def test_sample_preview_uses_real_docling_loader(monkeypatch):
    import langchain_docling
    from langchain_docling.loader import ExportType

    loader = Mock(wraps=langchain_docling.DoclingLoader)
    monkeypatch.setattr(langchain_docling, "DoclingLoader", loader)
    response = client.get("/api/rag/sample")
    assert response.status_code == 200
    loader.assert_called_once_with(file_path=str(api.SAMPLE_PATH), export_type=ExportType.MARKDOWN)
    assert "TICKET_PORT=8000" in response.json()["content"]
    assert "工单服务" in response.json()["content"]
    assert response.json()["metadata"] == {"source": str(api.SAMPLE_PATH), "title": "工单服务：快速开始", "version": "1.0"}
    assert response.json()["fictional"] is True


def test_missing_sample_returns_stable_error(monkeypatch, tmp_path):
    monkeypatch.setattr(api, "SAMPLE_PATH", tmp_path / "missing.md")
    response = client.get("/api/rag/sample")
    assert response.status_code == 500
    assert response.json()["error"]["code"] == "RAG_SAMPLE_UNAVAILABLE"
    assert "解析预览暂时不可用" in response.json()["error"]["message"]
    assert str(tmp_path) not in response.text


def test_rag_forwards_only_results_from_graph(monkeypatch):
    metadata = {
        "source": "fixture.pdf", "title": "测试交接手册", "version": "1.1",
        "dl_meta": {"headings": ["交接"], "doc_items": [
            {"self_ref": "#/texts/3", "prov": [{"page_no": 2, "charspan": [0, 12]}]},
        ]},
    }
    invoke = Mock(return_value={"documents": [SimpleNamespace(page_content="test fixture", metadata=metadata)]})
    state = {"file_path": ["fixture.pdf"], "documents": []}
    monkeypatch.setattr(api, "rag_core", lambda: SimpleNamespace(build_ingest_graph=lambda: SimpleNamespace(invoke=invoke), INITIAL_STATE=state))
    response = client.post("/api/rag/import")
    assert response.status_code == 200
    assert response.json() == {"documents": [{"page_content": "test fixture", "metadata": metadata}], "count": 1}
    invoke.assert_called_once_with(state)


@pytest.mark.parametrize(("preset_id", "reason"), [("no_signals", "evidence_insufficient"), ("step_limit", "max_steps_reached")])
def test_real_stop_paths_do_not_call_model(preset_id, reason):
    response = client.post("/api/incidents/stream", json={"preset_id": preset_id})
    events = frames(response)
    assert response.headers["content-type"].startswith("text/event-stream")
    assert events[0][0] == "graph_update"
    assert events[-1] == ("final", {"conclusion": None, "stop_reason": reason, "evidence": [], "step_count": 0})


def test_stream_is_incremental_and_uses_real_graph_with_test_model(monkeypatch):
    core = api.incident_core()
    generate_text = Mock(return_value="测试正文\nevent: error\ndata: injected")
    original = core.stream_incident_updates
    monkeypatch.setattr(core, "stream_incident_updates", lambda state: original(state, generate_text=generate_text))
    iterator = api.incident_events(api.preset_state("normal"))
    assert next(iterator).startswith("event: graph_update\n")
    generate_text.assert_not_called()
    events = list(iterator)
    generate_text.assert_called_once()
    assert len(events) == 5  # 其余四个真实节点更新 + final。
    final = json.loads(events[-1].splitlines()[1][6:])
    assert final["evidence"] == core.SAMPLE_INCIDENT["logs"]
    assert final["step_count"] == 1
    assert final["conclusion"].startswith("测试正文\n")
    assert len(events[-1].splitlines()) == 3  # 正文换行仍在 JSON 内，不能制造事件。


def test_stream_error_never_leaks_provider_exception(monkeypatch):
    def failing_stream(state):
        yield {"type": "updates", "ns": (), "data": {"organize_facts": {"facts_summary": "fixture"}}}
        raise RuntimeError("secret-provider-details")
    monkeypatch.setattr(api.incident_core(), "stream_incident_updates", failing_stream)
    response = client.post("/api/incidents/stream", json={"preset_id": "normal"})
    events = frames(response)
    assert [event for event, _ in events] == ["graph_update", "error"]
    assert events[-1][1]["code"] == "INCIDENT_RUN_FAILED"
    assert "secret-provider-details" not in response.text


@pytest.mark.parametrize("payload", [{}, {"question": " "}, {"question": "x" * 1001}, {"question": "test", "root": "D:/private"}])
def test_knowledge_rejects_invalid_question_before_loading_core(monkeypatch, payload):
    load = Mock(side_effect=AssertionError("invalid input must not load or invoke the Agent"))
    monkeypatch.setattr(api, "knowledge_core", load)
    response = client.post("/api/knowledge/stream", json=payload)
    assert response.status_code == 422
    assert response.json()["error"]["code"] == "INVALID_INPUT"
    load.assert_not_called()


def test_knowledge_translates_events_and_hides_source_failures(monkeypatch):
    payloads = [
        {"event": "step", "data": {"node": "index", "label": "fixture"}},
        {"event": "index", "data": {"candidate_count": 3, "read_count": 2, "read_failed_count": 1,
                                     "empty_count": 1, "indexed_file_count": 1, "chunk_count": 2, "skipped_count": 4}},
        {"event": "retrieval", "data": {"query": "fixture", "search_count": 1,
                                         "sources": [{"citation_id": "K1", "excerpt": "fixture\nevent: error\ndata: injected"}]}},
        {"event": "final", "data": {"answer": "引用待核对", "sources": [{"citation_id": "K1"}],
                                     "refused": True, "search_count": 1, "reason_code": "INVALID_CITATIONS",
                                     "next_step": "查看原文后重试。"}},
    ]
    core = SimpleNamespace(
        stream_knowledge=Mock(return_value=iter(payloads)),
        read_source=Mock(side_effect=FileNotFoundError("private-absolute-path")),
    )
    monkeypatch.setattr(api, "knowledge_core", lambda: core)
    response = client.post("/api/knowledge/stream", json={"question": "  test  "})
    assert response.status_code == 200
    assert response.headers["content-type"].startswith("text/event-stream")
    assert frames(response) == [(part["event"], part["data"]) for part in payloads]
    core.stream_knowledge.assert_called_once_with("test")
    response = client.get("/api/knowledge/source/unknown")
    assert response.status_code == 404
    assert "private-absolute-path" not in response.text


def test_knowledge_status_preserves_candidate_semantics(monkeypatch):
    status = {"available": True, "candidate_count": 3, "file_count": 3, "skipped_count": 1,
              "scopes": ["02-Concepts"], "limits": {"max_searches": 2}}
    monkeypatch.setattr(api, "knowledge_core", lambda: SimpleNamespace(knowledge_status=lambda: status))
    response = client.get("/api/knowledge/status")
    assert response.status_code == 200
    assert response.json() == status
    assert not {"read_count", "indexed_file_count", "chunk_count"} & response.json().keys()


@pytest.mark.parametrize("route", ["status", "stream"])
def test_knowledge_unavailable_before_stream_returns_http_503_without_details(monkeypatch, route):
    monkeypatch.setattr(api, "knowledge_core", Mock(side_effect=ImportError("private-dependency-path")))
    response = client.get("/api/knowledge/status") if route == "status" else client.post("/api/knowledge/stream", json={"question": "RAG"})
    assert response.status_code == 503
    assert response.json()["error"]["code"] == "KNOWLEDGE_UNAVAILABLE"
    assert "private-dependency-path" not in response.text


@pytest.mark.parametrize("caught_by_core", [False, True])
def test_knowledge_midstream_failure_preserves_sent_sources_and_safe_next_step(monkeypatch, caught_by_core):
    retrieval = {"query": "RAG", "search_count": 1, "sources": [{"citation_id": "K1", "excerpt": "真实检索片段"}]}
    classified = {"code": "KNOWLEDGE_MODEL_FAILED", "message": "本次模型调用失败。", "next_step": "保留资料并稍后重试。"}

    def failing_stream(question):
        yield {"event": "retrieval", "data": retrieval}
        if caught_by_core:
            yield {"event": "error", "data": classified}
        else:
            raise RuntimeError("private-provider-token-and-path")

    monkeypatch.setattr(api, "knowledge_core", lambda: SimpleNamespace(stream_knowledge=failing_stream))
    response = client.post("/api/knowledge/stream", json={"question": "RAG"})
    assert response.status_code == 200  # HTTP 响应已开始，后续失败通过 error 事件表示。
    events = frames(response)
    assert events[0] == ("retrieval", retrieval)
    assert [event for event, _ in events] == ["retrieval", "error"]
    assert events[-1][1]["code"] == ("KNOWLEDGE_MODEL_FAILED" if caught_by_core else "KNOWLEDGE_RUN_FAILED")
    assert events[-1][1]["message"].strip() and events[-1][1]["next_step"].strip()
    if caught_by_core:
        assert events[-1][1] == classified
    assert "private-provider-token-and-path" not in response.text


def test_source_read_failure_is_http_503_and_hides_private_path(monkeypatch):
    core = SimpleNamespace(read_source=Mock(side_effect=RuntimeError("private-source-file-and-content")))
    monkeypatch.setattr(api, "knowledge_core", lambda: core)
    response = client.get("/api/knowledge/source/" + "a" * 24)
    assert response.status_code == 503
    assert response.json()["error"]["code"] == "SOURCE_UNAVAILABLE"
    assert "private-source-file-and-content" not in response.text

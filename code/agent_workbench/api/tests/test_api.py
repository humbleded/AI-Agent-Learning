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
    assert "R6-01-G3" in response.json()["error"]["message"]


def test_sample_preview_uses_real_langchain_loader(monkeypatch):
    from langchain_community.document_loaders import text

    loader = Mock(wraps=text.TextLoader)
    monkeypatch.setattr(text, "TextLoader", loader)
    response = client.get("/api/rag/sample")
    assert response.status_code == 200
    loader.assert_called_once_with(str(api.SAMPLE_PATH), encoding="utf-8")
    assert "TICKET_PORT=8000" in response.json()["content"]
    assert response.json()["fictional"] is True


def test_missing_sample_returns_stable_error(monkeypatch, tmp_path):
    monkeypatch.setattr(api, "SAMPLE_PATH", tmp_path / "missing.md")
    response = client.get("/api/rag/sample")
    assert response.status_code == 500
    assert response.json()["error"]["code"] == "RAG_SAMPLE_UNAVAILABLE"
    assert str(tmp_path) not in response.text


def test_rag_forwards_only_results_from_graph(monkeypatch):
    invoke = Mock(return_value={"documents": [SimpleNamespace(page_content="test fixture", metadata={"source": "fixture.md"})]})
    monkeypatch.setattr(api, "rag_core", lambda: SimpleNamespace(build_ingest_graph=lambda: SimpleNamespace(invoke=invoke), INITIAL_STATE={"file_path": "fixture.md", "documents": []}))
    response = client.post("/api/rag/import")
    assert response.json() == {"documents": [{"page_content": "test fixture", "metadata": {"source": "fixture.md"}}], "count": 1}
    invoke.assert_called_once_with({"file_path": "fixture.md", "documents": []})


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
    core = SimpleNamespace(
        stream_knowledge=Mock(return_value=iter([
            {"event": "step", "data": {"node": "search", "label": "fixture"}},
            {"event": "final", "data": {"answer": "fixture [K1]", "sources": [], "refused": False, "search_count": 1}},
        ])),
        read_source=Mock(side_effect=FileNotFoundError("private-absolute-path")),
    )
    monkeypatch.setattr(api, "knowledge_core", lambda: core)
    response = client.post("/api/knowledge/stream", json={"question": "  test  "})
    assert [event for event, _ in frames(response)] == ["step", "final"]
    core.stream_knowledge.assert_called_once_with("test")
    response = client.get("/api/knowledge/source/unknown")
    assert response.status_code == 404
    assert "private-absolute-path" not in response.text

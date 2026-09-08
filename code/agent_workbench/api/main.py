"""统一学习工作台的本地 API；适配真实课程核心，不代写当前练习。

从仓库根目录启动：
    .venv/Scripts/python.exe -m uvicorn main:app --app-dir code/agent_workbench/api --host 127.0.0.1 --port 8765

接口保持固定教学输入；正常诊断通过已有核心调用真实 DeepSeek。
StreamingResponse、测试和错误处理按 FastAPI 官方文档核验于 2026-09-08。
"""

from collections.abc import Iterator
from copy import deepcopy
from functools import cache
import importlib.util
import json
from pathlib import Path
import sys
from types import ModuleType
from typing import Literal

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse, StreamingResponse
from pydantic import BaseModel, ConfigDict, Field


CODE_ROOT = Path(__file__).resolve().parents[2]
INCIDENT_PATH = CODE_ROOT / "stage8/incident_change_review_agent/incident_graph.py"
RAG_PATH = CODE_ROOT / "stage6/engineering_docs_rag/ingest.py"
SAMPLE_PATH = RAG_PATH.parent / "sample_docs/quickstart.md"
KNOWLEDGE_PATH = RAG_PATH.parent / "knowledge_agent.py"

app = FastAPI(title="Agent 学习工作台", version="0.1.0")


def load_module(name: str, path: Path) -> ModuleType:
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise ImportError("course_module_unavailable")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


@cache
def incident_core() -> ModuleType:
    return load_module("workbench_incident_core", INCIDENT_PATH)


def rag_core() -> ModuleType:
    # 每次读取当前练习，用户补好函数后无需维护第二份实现。
    return load_module("workbench_rag_core", RAG_PATH)


@cache
def knowledge_core() -> ModuleType:
    return load_module("workbench_knowledge_core", KNOWLEDGE_PATH)


def error_response(status: int, code: str, message: str) -> JSONResponse:
    return JSONResponse(status_code=status, content={"error": {"code": code, "message": message}})


@app.exception_handler(RequestValidationError)
async def invalid_input(request: Request, exc: RequestValidationError) -> JSONResponse:
    if request.url.path.startswith("/api/knowledge"):
        return error_response(422, "INVALID_INPUT", "请提供 1–1000 字的问题；当前接口只接受 question。")
    return error_response(422, "INVALID_INPUT", "请使用页面提供的场景编号；当前接口只接受 preset_id。")


@app.get("/api/health")
def health() -> dict:
    modules = []
    try:
        incident_core().build_incident_graph()
        incident_status, incident_detail = "available", "已有真实 LangGraph 核心；正常场景会调用 DeepSeek。"
    except Exception:
        incident_status, incident_detail = "unavailable", "故障诊断核心当前无法加载，请检查本地依赖或代码。"
    modules.append({"id": "incidents", "title": "故障诊断与变更评审", "status": incident_status, "detail": incident_detail})
    try:
        graph = rag_core().build_ingest_graph()
        if not callable(getattr(graph, "invoke", None)):
            raise NotImplementedError
        rag_status, rag_detail = "ready_to_run", "读取图入口已提供，点击导入以验证真实读取结果。"
    except (NotImplementedError, AttributeError):
        rag_status, rag_detail = "not_ready", "R6-01-G3 读取节点与图待完成；可先查看教学原文。"
    except Exception:
        rag_status, rag_detail = "unavailable", "文档读取核心当前无法加载，请检查本地依赖或代码。"
    modules.append({"id": "rag", "title": "工程文档助手", "status": rag_status, "detail": rag_detail})
    return {"status": "ok", "modules": modules}


PRESETS = (
    {"id": "normal", "title": "支付请求超时", "description": "读取虚构日志，生成根因判断、证据依据和变更评审。", "uses_model": True},
    {"id": "no_signals", "title": "没有告警和日志", "description": "观察证据不足时工作流主动停止；不调用模型。", "uses_model": False},
    {"id": "step_limit", "title": "诊断次数已到上限", "description": "将本次允许的诊断次数设为 0，观察停止分支；不调用模型。", "uses_model": False},
)


def preset_state(preset_id: str) -> dict:
    state = incident_core().build_initial_state(max_steps=0 if preset_id == "step_limit" else 2)
    if preset_id == "no_signals":
        state["alerts"] = []
        state["logs"] = []
    return state


@app.get("/api/incidents/presets")
def incident_presets() -> dict:
    input_fields = ("service", "alerts", "logs", "config_snapshot", "change_request", "max_steps")
    return {"presets": [
        {**preset, "fictional": True, "input": {key: value for key, value in preset_state(preset["id"]).items() if key in input_fields}}
        for preset in PRESETS
    ]}


class IncidentRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    preset_id: Literal["normal", "no_signals", "step_limit"]


def sse(event: str, data: dict) -> str:
    # JSON 编码转义正文换行，确保内容无法制造额外 SSE 事件。
    return f"event: {event}\ndata: {json.dumps(data, ensure_ascii=False)}\n\n"


def incident_events(state: dict) -> Iterator[str]:
    result = deepcopy(state)
    updates = None
    try:
        # 默认生成函数来自原核心；这里只转发真实节点更新，不制作计时进度。
        updates = incident_core().stream_incident_updates(state)
        for part in updates:
            if part.get("type") != "updates" or not isinstance(part.get("data"), dict):
                raise ValueError("unexpected_graph_update")
            for update in part["data"].values():
                for key, value in update.items():
                    if key == "evidence":
                        result[key] = result[key] + value
                    else:
                        result[key] = value
            yield sse("graph_update", part)
        if not result["conclusion"] and not result["stop_reason"]:
            raise ValueError("graph_finished_without_outcome")
        yield sse("final", {key: result[key] for key in ("conclusion", "stop_reason", "evidence", "step_count")})
    except Exception:
        # 不向浏览器返回 Provider 原始异常、请求对象或配置内容。
        yield sse("error", {"code": "INCIDENT_RUN_FAILED", "message": "本次运行未能完成。请检查后端代码或模型服务后重新运行；本次未执行任何变更。"})
    finally:
        if updates is not None and callable(getattr(updates, "close", None)):
            updates.close()


@app.post("/api/incidents/stream")
def stream_incident(request: IncidentRequest):
    try:
        state = preset_state(request.preset_id)
    except Exception:
        return error_response(503, "INCIDENT_UNAVAILABLE", "故障诊断核心当前不可用，请检查本地依赖或代码。")
    return StreamingResponse(incident_events(state), media_type="text/event-stream", headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"})


@app.get("/api/rag/sample")
def rag_sample():
    # 助手提供的原文预览也使用现成 Loader；它不经过 G3 图，不计入用户实现证据。
    try:
        from langchain_community.document_loaders.text import TextLoader

        document = TextLoader(str(SAMPLE_PATH), encoding="utf-8").load()[0]
        return {"file_name": SAMPLE_PATH.name, "content": document.page_content, "metadata": {"title": "工单服务：快速开始", "version": "1.0"}, "fictional": True}
    except (OSError, RuntimeError, ImportError, IndexError):
        return error_response(500, "RAG_SAMPLE_UNAVAILABLE", "教学资料预览暂时不可用，请检查 quickstart.md 文件与读取依赖。")


@app.post("/api/rag/import")
def import_rag():
    try:
        core = rag_core()
        graph = core.build_ingest_graph()
        result = graph.invoke(deepcopy(core.INITIAL_STATE))
        documents = [{"page_content": doc.page_content, "metadata": doc.metadata} for doc in result["documents"]]
        if not documents:
            raise ValueError("no_documents_returned")
        return {"documents": documents, "count": len(documents)}
    except (NotImplementedError, AttributeError):
        return error_response(409, "RAG_NOT_READY", "R6-01-G3 尚未完成：请实现读取节点与 build_ingest_graph，再回到页面重试。")
    except Exception:
        return error_response(500, "RAG_IMPORT_FAILED", "真实文档读取失败，请检查当前 ingest.py 的实现与本地依赖。")


class KnowledgeRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    question: str = Field(min_length=1, max_length=1000)


@app.get("/api/knowledge/status")
def knowledge_status():
    try:
        return knowledge_core().knowledge_status()
    except Exception:
        return error_response(503, "KNOWLEDGE_UNAVAILABLE", "知识库连接暂不可用，请检查本地目录和知识库组件依赖。")


@app.post("/api/knowledge/stream")
def query_knowledge(request: KnowledgeRequest):
    question = request.question.strip()
    if not question:
        return error_response(422, "INVALID_INPUT", "请先输入一个问题。")
    try:
        core = knowledge_core()
    except Exception:
        return error_response(503, "KNOWLEDGE_UNAVAILABLE", "知识库组件暂不可用，请检查后端依赖。")

    def events():
        try:
            for part in core.stream_knowledge(question):
                yield sse(part["event"], part["data"])
        except Exception:
            yield sse("error", {"code": "KNOWLEDGE_RUN_FAILED", "message": "本次知识库查询未完成，请检查后端服务后重试。"})

    return StreamingResponse(events(), media_type="text/event-stream", headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"})


@app.get("/api/knowledge/source/{source_id}")
def knowledge_source(source_id: str):
    try:
        return knowledge_core().read_source(source_id)
    except (FileNotFoundError, KeyError, ValueError):
        return error_response(404, "SOURCE_NOT_FOUND", "该原文已不在当前读取范围内，或文件已经移动。请重新检索。")
    except Exception:
        return error_response(503, "SOURCE_UNAVAILABLE", "暂时无法读取这份原文，请稍后重试。")

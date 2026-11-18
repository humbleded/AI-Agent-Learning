"""保护真实 Docling 导入、Hybrid 切分与图输出；不把助手测试算作用户 PASS。

后续修改导入核心或升级依赖时复跑，保护来源、PDF 页位置、代码、token 预算及片段/目录卡保存读回：
    .venv/Scripts/python.exe -m pytest code/agent_workbench/api/tests/test_ingest.py -q
真实三格式比较原顺序与反序导入；边界资料使用 tmp_path，来源故障使用内存注入，无模型调用。
"""

from collections import defaultdict
from copy import deepcopy
import hashlib
import importlib.util
import json
from pathlib import Path
import re
import socket
import sys
from unittest.mock import Mock

from langchain_core.documents import Document
import pytest
import tiktoken


@pytest.fixture(scope="session")
def tokenizer_cache():
    # 新环境首次可下载公开编码表；准备完成后，真实文档解析/切分必须离线。
    # 编码表不是模型权重，不发送文档；已有缓存时无需联网。
    tiktoken.get_encoding("cl100k_base")


@pytest.fixture(autouse=True)
def no_network(monkeypatch, tokenizer_cache):
    forbidden = Mock(side_effect=AssertionError("ingest tests must not access the network"))
    monkeypatch.setattr(socket.socket, "connect", forbidden)
    monkeypatch.setattr(socket, "create_connection", forbidden)
    yield
    forbidden.assert_not_called()


@pytest.fixture
def core(no_network, tmp_path, monkeypatch):
    path = Path(__file__).resolve().parents[3] / "stage6/engineering_docs_rag/ingest.py"
    name = "workbench_ingest_tests"
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    # 当前及后续保存节点只写 pytest 临时目录，避免测试污染实际导入记录。
    monkeypatch.setattr(module, "STORE_DIR", tmp_path / "ingest_store" / "chunks")
    yield module
    sys.modules.pop(name, None)


def assert_documents_fit_budget(core, documents):
    tokenizer = core.create_chunker().tokenizer
    assert tokenizer.get_tokenizer().name == core.TOKENIZER_ENCODING
    assert tokenizer.get_max_tokens() == core.CHUNK_MAX_TOKENS
    assert documents
    for document in documents:
        assert isinstance(document, Document)
        assert document.page_content.strip()
        # 包括 contextualize 添加的标题；不是只计算 chunk.text 或 Python 字符数。
        assert tokenizer.count_tokens(document.page_content) <= core.CHUNK_MAX_TOKENS
        assert document.metadata["dl_meta"]["doc_items"]
        assert "start_index" not in document.metadata
        json.dumps(document.metadata, ensure_ascii=False)


def load_temporary_markdown(core, tmp_path, monkeypatch, text):
    path = tmp_path / "boundary.md"
    path.write_text(text, encoding="utf-8")
    source = str(path)
    monkeypatch.setitem(core.DOCUMENT_CATALOG, source, {
        "title": "测试资料", "version": "test",
        "document_id": "test-team:boundary", "tenant": "test-team",
    })
    documents = core.build_ingest_graph().invoke({"file_path": [source], "documents": []})["documents"]
    assert_documents_fit_budget(core, documents)
    assert all(document.metadata["source"] == source for document in documents)
    return documents


def test_real_three_format_graph_preserves_content_versions_and_pdf_provenance(core, monkeypatch):
    converted = {}
    real_convert = core.DOCUMENT_CONVERTER.convert

    def capture_conversion(*args, **kwargs):
        result = real_convert(*args, **kwargs)
        converted[str(kwargs.get("source", args[0] if args else ""))] = result.document
        return result

    monkeypatch.setattr(core.DOCUMENT_CONVERTER, "convert", capture_conversion)
    state = deepcopy(core.INITIAL_STATE)
    original_state = deepcopy(state)
    updates = list(core.build_ingest_graph().stream(state, stream_mode="updates"))
    assert [next(iter(update)) for update in updates] == [
        "load_and_chunk_documents", "enrich_documents", "store_documents",
    ]
    parsed = updates[0]["load_and_chunk_documents"]["documents"]
    enriched_documents = updates[1]["enrich_documents"]["documents"]
    documents = updates[2]["store_documents"]["documents"]
    assert len(parsed) == len(enriched_documents) == len(documents)
    for raw, enriched, restored in zip(parsed, enriched_documents, documents):
        assert raw is not enriched
        assert raw.metadata is not enriched.metadata
        assert not {"title", "version", "document_id", "tenant", "content_hash"} & raw.metadata.keys()
        assert raw.page_content == enriched.page_content
        assert raw.metadata["dl_meta"] == enriched.metadata["dl_meta"]
        assert restored is not enriched
        assert restored.model_dump() == enriched.model_dump()
    assert state == original_state
    assert_documents_fit_budget(core, documents)

    by_source = defaultdict(list)
    for document in documents:
        source = document.metadata["source"]
        info = core.DOCUMENT_CATALOG[source]
        assert isinstance(document.id, str) and re.fullmatch(r"[0-9a-f]{64}", document.id)
        assert document.metadata["chunk_id"] == document.id
        assert {key: document.metadata[key] for key in ("title", "version", "document_id", "tenant")} == {
            key: info[key] for key in ("title", "version", "document_id", "tenant")
        }
        by_source[source].append(document)
    assert set(by_source) == set(core.DOCUMENT_CATALOG) == set(converted)
    assert len({document.id for document in documents}) == len(documents)
    for source, parts in by_source.items():
        expected_hash = hashlib.sha256(Path(source).read_bytes()).hexdigest()
        assert {part.metadata["content_hash"] for part in parts} == {expected_hash}
        assert [part.metadata["chunk_index"] for part in parts] == list(range(len(parts)))

    reordered_state = {"file_path": list(reversed(state["file_path"])), "documents": []}
    reordered = core.build_ingest_graph().invoke(reordered_state)["documents"]
    expected_chunks = {
        (doc.metadata["document_id"], doc.metadata["chunk_index"]): doc.model_dump()
        for doc in documents
    }
    assert len(expected_chunks) == len(documents) == len(reordered)
    assert {
        (doc.metadata["document_id"], doc.metadata["chunk_index"]): doc.model_dump()
        for doc in reordered
    } == expected_chunks

    expected = {
        "quickstart.md": ("TICKET_ENV=local", "TICKET_PORT=8000", "CONFIG_MISSING"),
        "config.txt": ("TICKET_ENV=local", "TICKET_PORT=8000", "CONFIG_MISSING"),
        "handover.pdf": ("TICKET_PORT=8100", "HANDOVER_READY", "回退到 1.0", "8000"),
    }
    for source, parts in by_source.items():
        # Markdown 导出可转义下划线；配置的实际字符和值必须仍完整。
        content = "\n".join(part.page_content for part in parts).replace("\\_", "_")
        assert all(value in content for value in expected[Path(source).name])

    pdf_source = next(source for source in by_source if source.endswith(".pdf"))
    real_items = {item.self_ref: item for item, _ in converted[pdf_source].iterate_items()}
    seen_pages = set()
    for part in by_source[pdf_source]:
        for item in part.metadata["dl_meta"]["doc_items"]:
            real_item = real_items[item["self_ref"]]
            expected_prov = [prov.model_dump(mode="json", by_alias=True, exclude_none=True) for prov in real_item.prov]
            assert item["prov"] == expected_prov
            assert item["prov"]
            seen_pages.update(prov["page_no"] for prov in item["prov"])
            if "HANDOVER_READY" in getattr(real_item, "text", ""):
                assert {prov["page_no"] for prov in item["prov"]} == {2}
            if "TICKET_PORT=8100" in getattr(real_item, "text", ""):
                assert {prov["page_no"] for prov in item["prov"]} == {1}
    assert seen_pages == {1, 2}
    for marker, page_no in (("HANDOVER_READY", 2), ("TICKET_PORT=8100", 1)):
        marked_parts = [part for part in by_source[pdf_source] if marker in part.page_content]
        assert marked_parts
        for part in marked_parts:
            supporting_items = [real_items[item["self_ref"]] for item in part.metadata["dl_meta"]["doc_items"]]
            assert any(marker in getattr(item, "text", "") and any(prov.page_no == page_no for prov in item.prov) for item in supporting_items)


def test_store_returns_actual_reads_and_persists_without_duplicate_keys(core, monkeypatch):
    documents = [
        Document(
            id=marker * 64,
            page_content=f'# 中文资料 {marker}\n\ndef ready():\n    return "你好"\n',
            metadata={
                "chunk_id": marker * 64, "document_id": "demo-team:stored",
                "tenant": "demo-team", "source": "fixture.md", "version": "1.0",
                "dl_meta": {"doc_items": [{"self_ref": "#/texts/1", "prov": [{"page_no": 1}, {"page_no": 2}]}]},
            },
        )
        for marker in ("b", "a")
    ]
    original = deepcopy(documents)
    real_factory = core.create_kv_docstore
    read_batches = []

    def observe_store(byte_store):
        store = real_factory(byte_store)
        real_mget = store.mget

        def observe_read(keys):
            restored = real_mget(keys)
            read_batches.append(restored)
            return restored

        monkeypatch.setattr(store, "mget", observe_read)
        return store

    monkeypatch.setattr(core, "create_kv_docstore", observe_store)
    for batch in (documents, list(reversed(documents))):
        restored = core.store_documents({"file_path": [], "documents": batch})["documents"]
        assert len(restored) == len(batch) == len(read_batches[-1])
        assert all(actual is read for actual, read in zip(restored, read_batches[-1]))
        assert [doc.model_dump() for doc in restored] == [doc.model_dump() for doc in batch]
    assert documents == original

    # 重新创建真实存储对象，必须仍能从给定目录取回完整资料；不能依赖原对象内存。
    reopened = real_factory(core.LocalFileStore(core.STORE_DIR))
    ids = [doc.id for doc in documents]
    assert set(reopened.yield_keys()) == set(ids)
    assert list(core.STORE_DIR.iterdir())
    assert [doc.model_dump() for doc in reopened.mget(ids)] == [doc.model_dump() for doc in original]
    assert reopened.mget(["0" * 64]) == [None]


def test_store_rejects_a_missing_read_instead_of_returning_partial_success(core, monkeypatch):
    real_factory = core.create_kv_docstore
    reads = []

    def inject_missing_read(byte_store):
        store = real_factory(byte_store)
        real_mget = store.mget

        def missing_read(keys):
            restored = real_mget(keys)
            reads.append(list(keys))
            restored[-1] = None  # 离线故障注入：模拟本次应有的某片读回缺失。
            return restored

        monkeypatch.setattr(store, "mget", missing_read)
        return store

    monkeypatch.setattr(core, "create_kv_docstore", inject_missing_read)
    documents = [Document(id=marker * 64, page_content=marker) for marker in ("a", "b")]
    with pytest.raises(ValueError):
        core.store_documents({"file_path": [], "documents": documents})
    assert reads == [[doc.id for doc in documents]]


def test_document_records_preserve_identity_and_persist_complete_values(core):
    record = {
        "tenant": "demo-team",
        "document_id": "demo-team:quickstart",
        "chunk_ids": ["a" * 64, "b" * 64],
        "title": "配置说明\n版本一",
    }
    original = deepcopy(record)
    key = core.compute_document_key(record["tenant"], record["document_id"])
    assert re.fullmatch(r"[0-9a-f]{64}", key)
    assert core.compute_document_key(record["tenant"], record["document_id"]) == key
    assert core.compute_document_key("demo-team", "another-document") != key
    # 两个字段的边界必须保留，不能直接拼接后导致不同身份共用一条记录。
    assert core.compute_document_key("ab", "c") != core.compute_document_key("a", "bc")

    for candidate in (record, dict(reversed(list(record.items())))):
        restored = core.write_document_record(candidate)
        assert restored == original
        assert restored is not candidate
        assert restored["chunk_ids"] is not candidate["chunk_ids"]
    assert record == original

    changed = {**record, "chunk_ids": ["c" * 64], "title": "配置说明\n版本二"}
    assert core.write_document_record(changed) == changed
    reopened = core.LocalFileStore(core.STORE_DIR.parent / "records")
    assert set(reopened.yield_keys()) == {key}
    assert json.loads(reopened.mget([key])[0].decode("utf-8")) == changed

    another_team = {**record, "tenant": "other-team"}
    another_key = core.compute_document_key(another_team["tenant"], another_team["document_id"])
    assert another_key != key
    assert core.write_document_record(another_team) == another_team
    assert set(reopened.yield_keys()) == {key, another_key}
    assert [
        json.loads(value.decode("utf-8"))
        for value in reopened.mget([key, another_key])
    ] == [changed, another_team]
    assert not core.STORE_DIR.exists()  # 写目录卡不会顺带写入或删除正文片段。
    assert record == original


@pytest.mark.parametrize("missing", [False, True])
def test_document_record_uses_the_actual_read_and_rejects_missing(core, monkeypatch, missing):
    record = {
        "tenant": "demo-team", "document_id": "demo-team:quickstart",
        "chunk_ids": ["a" * 64],
    }
    original = deepcopy(record)
    real_store = core.LocalFileStore
    requested = []
    observed = []

    def inject_read_result(root_path):
        store = real_store(root_path)
        real_mget = store.mget

        def altered_read(keys):
            values = real_mget(keys)
            requested.append(list(keys))
            # 真实落盘后仅替换读回值：离线验证使用返回内容及缺失分支。
            value = json.loads(values[0].decode("utf-8"))
            observed.append(value)
            return [None] if missing else [
                json.dumps({**value, "read_marker": "来自读回"}).encode("utf-8")
            ]

        monkeypatch.setattr(store, "mget", altered_read)
        return store

    monkeypatch.setattr(core, "LocalFileStore", inject_read_result)
    if missing:
        with pytest.raises(ValueError):
            core.write_document_record(record)
    else:
        assert core.write_document_record(record) == {**record, "read_marker": "来自读回"}
    key = core.compute_document_key(record["tenant"], record["document_id"])
    assert requested == [[key]]
    assert observed == [original]
    assert record == original


def test_chunk_indexes_follow_each_document_and_reset_per_call(core):
    first_source, second_source = list(core.DOCUMENT_CATALOG)[:2]
    raw = [
        Document(page_content="相同正文", metadata={"source": source})
        for source in (first_source, second_source, first_source, second_source)
    ]
    original = deepcopy(raw)
    state = {"file_path": [first_source, second_source], "documents": raw}
    previous_ids = None
    for _ in range(2):
        result = core.enrich_documents(state)["documents"]
        assert [doc.metadata["chunk_index"] for doc in result] == [0, 0, 1, 1]
        assert [doc.metadata["document_id"] for doc in result] == [
            core.DOCUMENT_CATALOG[doc.metadata["source"]]["document_id"] for doc in raw
        ]
        assert raw == original
        assert all(before is not after for before, after in zip(raw, result))
        ids = [doc.id for doc in result]
        assert len(set(ids)) == len(result)
        assert all(doc.id == doc.metadata["chunk_id"] for doc in result)
        if previous_ids is not None:
            assert ids == previous_ids
        previous_ids = ids


def test_chunk_ids_change_with_source_and_processing_configuration(core, tmp_path, monkeypatch):
    baseline_text = "# 编号验证\n\nTICKET_PORT=8000\n"
    baseline = load_temporary_markdown(core, tmp_path, monkeypatch, baseline_text)
    assert len(baseline) == 1
    initial = baseline[0]
    assert initial.id == initial.metadata["chunk_id"]

    changed_text = load_temporary_markdown(core, tmp_path, monkeypatch, baseline_text.replace("8000", "8100"))[0]
    assert changed_text.metadata["document_id"] == initial.metadata["document_id"]
    assert changed_text.metadata["content_hash"] != initial.metadata["content_hash"]
    assert changed_text.id == changed_text.metadata["chunk_id"]
    assert changed_text.id != initial.id

    for field, value in (("CHUNK_MAX_TOKENS", 128), ("PROCESSING_VERSION", "docling-hybrid-v2")):
        with monkeypatch.context() as configuration:
            configuration.setattr(core, field, value)
            changed = load_temporary_markdown(core, tmp_path, monkeypatch, baseline_text)[0]
            assert changed.metadata["content_hash"] == initial.metadata["content_hash"]
            assert changed.metadata["document_id"] == initial.metadata["document_id"]
            assert changed.id == changed.metadata["chunk_id"]
            assert changed.id != initial.id


def test_short_python_keeps_nested_indentation(core, tmp_path, monkeypatch):
    code = 'def ready():\n    if True:\n        return "HANDOVER_READY"'
    documents = load_temporary_markdown(core, tmp_path, monkeypatch, f"# 启动检查\n\n```python\n{code}\n```\n")
    assert any(code in document.page_content for document in documents)
    assert any("启动检查" in document.metadata["dl_meta"].get("headings", []) for document in documents)


def test_repeated_text_keeps_distinct_section_references(core, tmp_path, monkeypatch):
    repeated = "运行 deploy 命令。"
    documents = load_temporary_markdown(
        core, tmp_path, monkeypatch,
        f"# 操作条件\n\n## 生产环境需审批\n\n{repeated}\n\n## 演练环境免审批\n\n{repeated}\n",
    )
    references = {}
    for heading in ("生产环境需审批", "演练环境免审批"):
        parts = [doc for doc in documents if heading in doc.metadata["dl_meta"].get("headings", [])]
        assert parts and any(repeated in part.page_content for part in parts)
        references[heading] = {item["self_ref"] for part in parts for item in part.metadata["dl_meta"]["doc_items"]}
    assert references["生产环境需审批"].isdisjoint(references["演练环境免审批"])


def test_long_python_keeps_all_lines_and_shared_original_item(core, tmp_path, monkeypatch):
    lines = [f"    value_{index} = {index}" for index in range(50)]
    source_code = "def values():\n" + "\n".join(lines)
    documents = load_temporary_markdown(core, tmp_path, monkeypatch, f"# 长代码\n\n```python\n{source_code}\n```\n")
    assert len(documents) > 1
    output_lines = [line for doc in documents for line in doc.page_content.splitlines()]
    assert [line for line in output_lines if line.startswith("    value_")] == lines
    item_refs = {item["self_ref"] for doc in documents for item in doc.metadata["dl_meta"]["doc_items"]}
    assert len(item_refs) == 1
    # item 引用描述原代码块，不是每片精确字符范围；不承诺每个切片的围栏单独闭合。


@pytest.mark.parametrize("metadata", [{}, {"source": "unregistered.md"}], ids=["missing-source", "unregistered-source"])
def test_missing_or_unregistered_source_is_rejected(core, monkeypatch, metadata):
    injected_loader = Mock()
    parsed = [
        Document(page_content="registered fixture", metadata={"source": str(core.SAMPLE_PATH)}),
        Document(page_content="injected fixture", metadata=metadata),
    ]
    original = deepcopy(parsed)
    injected_loader.load.return_value = parsed
    monkeypatch.setattr(core, "DoclingLoader", Mock(return_value=injected_loader))
    with pytest.raises(ValueError):
        core.build_ingest_graph().invoke(deepcopy(core.INITIAL_STATE))
    assert parsed == original  # 后一片无效时，也不能把前一阶段的一部分数据改掉。

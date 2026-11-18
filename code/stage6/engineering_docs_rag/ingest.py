r"""R6-01：官方 DoclingLoader + HybridChunker，经 LangGraph 返回可追溯片段。

运行：.\.venv\Scripts\python.exe code/stage6/engineering_docs_rag/ingest.py
输入：给定的 MD/TXT/两页原生文字 PDF 教学资料。
流程：START -> load_and_chunk_documents -> enrich_documents -> store_documents -> END。
第一步由官方 Loader 完成解析/切分，返回 source/dl_meta 片段；
第二步校验来源并补充业务信息、文档与片段编号，返回新 Document，保留前一步结果可供检查。
第三步以片段编号保存完整 Document，再按本次编号顺序读回；缺失时明确报错。
输出：实际从本地读回的 Document 正文、id，以及 source/title/version/dl_meta 等 metadata。
定位：dl_meta.doc_items 的文档元素引用；PDF 有实际 prov 页码，允许一片跨多页。
原生位置与 document_id/chunk_id 分别负责原文定位和业务身份，不混用。
2026-10-20：用户已完成 G6 保存/读回与接图；文档导入状态及更新/删除清理仍待接续。

2026-09-09：用户要求补充问答对照后授权助手决定，采用 Hybrid + 两个明确阶段。
原来的两个切分函数及其参数以注释保留在文件末尾，
既有用户学习证据仍有效，本次适配不计独立 PASS。对照及边界见 chunking-comparison.md。
9月9日对照使用128 token；当前用户已调为256，两者都不是最终检索最优值；计数包含补入的标题。
超长代码可能拆成围栏不完整的片段，不能把切片当作独立可执行代码。
"""
import hashlib
import json
from pathlib import Path
from typing import TypedDict

import tiktoken
from docling.chunking import HybridChunker
from docling.datamodel.base_models import InputFormat
from docling.datamodel.pipeline_options import NativePdfPipelineOptions
from docling.document_converter import DocumentConverter, NativePdfFormatOption
from docling_core.transforms.chunker.tokenizer.openai import OpenAITokenizer
from langchain_classic.storage import LocalFileStore, create_kv_docstore
from langchain_core.documents import Document
from langchain_docling import DoclingLoader
from langchain_docling.loader import ExportType
from langgraph.graph import END, START, StateGraph


SAMPLE_PATH = Path(__file__).resolve().parent / "sample_docs" / "quickstart.md"
DOCUMENT_INFO = {"title": "工单服务：快速开始", "version": "1.0"}
# G6 给定登记信息：编号在同一资料后续更新时沿用；团队归属来自可信配置。
#with_name() 的意思是：保留文件所在目录，把路径最后的文件名换成指定名称，返回一个新的路径对象。
DOCUMENT_CATALOG = {
    str(SAMPLE_PATH): {
        "title": "工单服务：快速开始", "version": "1.0",
        "document_id": "demo-team:quickstart", "tenant": "demo-team",
    },
    str(SAMPLE_PATH.with_name("config.txt")): {
        "title": "工单服务：配置说明", "version": "1.0",
        "document_id": "demo-team:config", "tenant": "demo-team",
    },
    str(SAMPLE_PATH.with_name("handover.pdf")): {
        "title": "工单服务：交接手册", "version": "1.1",
        "document_id": "demo-team:handover", "tenant": "demo-team",
    },
}

# 沿用已验证的 PDF 配置：读取已有文字，不运行 OCR 或版面/表格模型。
# 助手给定的官方配置：PDF 提取已有文字，不运行文字识别或版面/表格模型。
# 只覆盖简单的可选中文字 PDF；不代表扫描件或复杂排版已支持。
# 作用是提供文档转换器的默认配置，确保 PDF 文档在解析时使用官方推荐的选项。
DOCUMENT_CONVERTER = DocumentConverter(
    format_options={
        InputFormat.PDF: NativePdfFormatOption(
            pipeline_options=NativePdfPipelineOptions(
                generate_page_images=False,
                generate_picture_images=False,
                parser_threads=2,
            )
        )
    }
)

# tokenizer 把文字分成计数单位（token）。这是固定比较用的规则，
# 不是 DeepSeek 的计费规则；R6-02 选定 embedding 模型后再与其 tokenizer 对齐。
# 首次获取 cl100k_base 可能下载公开编码表并缓存，不下载模型权重、不上传文档。
TOKENIZER_ENCODING = "cl100k_base"
CHUNK_MAX_TOKENS = 256
# G6 给定的处理规则版本；改变解析/导出/合并规则或影响输出的组件版本时更新。
# tokenizer 和 token 预算在片段编号中另取当前常量，不抄写固定值。
PROCESSING_VERSION = "docling-hybrid-v1"
# G6 给定的本地保存目录：每条记录以片段编号为键，运行时数据不提交 Git。
STORE_DIR = Path(__file__).resolve().parent / ".ingest_store" / "chunks"

# G6 给定的目录卡格式；复用已学 TypedDict，实际记录仍由用户汇总真实片段生成。
class DocumentRecord(TypedDict):
    tenant: str
    document_id: str
    chunk_ids: list[str]


# 定义文档摄取的状态结构，包括文件路径列表和文档列表。自定义字典类型，用于类型检查和代码提示。定义字典应该采用的格式
class IngestState(TypedDict):
    file_path: list[str]
    documents: list[Document]
    document_records: dict[str, DocumentRecord]
    previous_document_records: dict[str, DocumentRecord | None]

# 创建一份符合这个格式的数据
#INITIAL_STATE : IngestState = {...}
#变量名          类型说明      实际赋给它的数据
# - INITIAL_STATE：变量名，意思是“初始状态”。
# - : IngestState：说明这个变量应该符合你前面定义的字典格式。
# - = {...}：真正创建一个字典，并把它赋给这个变量。
# 前面的 IngestState 规定了格式，这里开始按照格式填写具体内容。
INITIAL_STATE: IngestState = {
    "file_path": list(DOCUMENT_CATALOG),
    "documents": [],
    "document_records": {},
    "previous_document_records": {},
}

# 作用是创建一个混合切分器，用于将文档分块。
def create_chunker() -> HybridChunker:
    """使用官方 tokenizer 包装；OpenAITokenizer 只在本地计数，不调用 OpenAI API。"""
    return HybridChunker(
        tokenizer=OpenAITokenizer(
            tokenizer=tiktoken.get_encoding(TOKENIZER_ENCODING),
            max_tokens=CHUNK_MAX_TOKENS,
        ),
        merge_peers=True,  # 预算允许时合并同一标题下的小片段；没有固定 overlap 参数。
    )

# 加载文档并进行分块处理。
def load_and_chunk_documents(state: IngestState) -> dict[str, list[Document]]:
    """文件路径清单 -> 官方 Loader 产生的原生片段，尚未补业务标题/版本。"""
    # DOC_CHUNKS 直接把 DoclingDocument 交给 HybridChunker，
    # Loader 再把附带标题上下文的结果封装为 LangChain Document。
    # converter=DOCUMENT_CONVERTER意思是使用官方推荐的文档转换器配置来解析 PDF 文档。
    #- create_chunker() 创建切分工具。
    #DOC_CHUNKS 选择使用切分工具的导出模式。
    #loader.load() 真正执行解析、切分并返回结果。
    # 如果只把这一行改回 ExportType.MARKDOWN，
    # 即使仍然传了 chunker=create_chunker()，
    # 也不会按当前这条分块流程得到 Hybrid 片段。 
    # 官方明确说明，chunker 参数用于文档分块模式；
    # Markdown 模式会返回整篇正文，需要你重新接上后续切分步骤。
    #export_type 选输出形式，chunker 选切分方法
    #一般export_type=ExportType.DOC_CHUNKS是和chunker搭配使用
    loader = DoclingLoader(
        file_path=state["file_path"],
        export_type=ExportType.DOC_CHUNKS, # 作用是直接把文档切分成原生片段
        converter=DOCUMENT_CONVERTER, # 作用是使用官方推荐的文档转换器配置来解析 PDF 文档
        chunker=create_chunker(), # 作用是使用混合切分器将文档分块
    )
    #loader.load() 开始处理 
    # create_chunker() 是准备切分工具，
    # loader.load() 才是开始处理这批文件。
    return {"documents": loader.load()}


# 计算文件内容的 SHA-256 指纹，用于唯一标识源文件。
# 作用是确保即使文件名相同，只要内容不同也能生成不同的指纹。
def compute_content_hash(file_path: str) -> str:
    """G6：输入本地源文件路径，返回整份文件原始字节的 SHA-256 十六进制字符串。"""
    # 调用标准库文件摘要工具计算并返回结果，使用二进制读取模式并关闭文件。
    #with 管理文件的打开与关闭，离开代码块后会关闭文件
    # "sha256" 指定本次使用的指纹算法。
    #hexdigest() 把计算结果转成方便保存的字符串；SHA-256 对应 64 个十六进制字符。
    with Path(file_path).open("rb") as file_obj:
        digest = hashlib.file_digest(file_obj, "sha256") # 计算文件的 SHA-256 摘要 作用是生成唯一标识源文件的指纹
    fingerprint = digest.hexdigest() # 将二进制摘要转换为十六进制字符串，作为文件的唯一指纹,返回的是长度为64的十六进制字符串
    return fingerprint

# 计算片段 ID，用于唯一标识每个文档片段。
def compute_chunk_id(metadata: dict[str, object]) -> str:
    """G6：用文档身份、源内容、处理配置和文档内序号计算确定的片段编号。"""
    # 选择 tenant/document_id/content_hash/chunk_index，以及当前处理版本、tokenizer、预算。
    # 将固定字段按固定 JSON 格式转成 UTF-8 字节，返回 SHA-256 十六进制字符串。
    chunk_id_data = {
        "tenant": metadata["tenant"],
        "document_id": metadata["document_id"],
        "content_hash": metadata["content_hash"],
        "chunk_index": metadata["chunk_index"],
        "processing_version": PROCESSING_VERSION,
        "tokenizer": TOKENIZER_ENCODING,
        "max_tokens": CHUNK_MAX_TOKENS,
    }
    chunk_id_json = json.dumps(
      chunk_id_data, 
      sort_keys=True,
      ensure_ascii=False,
      separators=(",", ":"),
    ).encode("utf-8")
    return hashlib.sha256(chunk_id_json).hexdigest()

# 对原生文档片段进行增强，补充业务信息并计算片段 ID。
def enrich_documents(state: IngestState) -> dict[str, list[Document]]:
    """原生片段 -> 已校验来源并补好业务信息的片段；不修改前一步对象。"""
    # （G6 下一步）：按 document_id 分别从 0 累计片段序号，写入新 metadata 的 chunk_index。
    # 计数只属于本次函数调用；不同文档的片段即使交错出现，也各自连续编号。
    chunk_index_counter= {}  # 按 document_id 记录当前片段序号
    documents = []
    # 复用用户已完成的来源校验和业务信息补充；原生 dl_meta 不覆盖。
    for doc in state["documents"]:
        if "source" not in doc.metadata:
            raise ValueError("Document metadata missing 'source' key")
        source = doc.metadata["source"]
        if source not in DOCUMENT_CATALOG:
            raise ValueError(f"Source {source} not found in DOCUMENT_CATALOG")
        info = DOCUMENT_CATALOG[source]
        # （G6）：在下方 metadata 中补登记的 document_id、tenant 及源文件 content_hash。
        # 同一源文件的各片共享这些值；source/title/version/dl_meta 及新对象返回方式继续保留。
        metadata = {
          **doc.metadata, 
          "title": info["title"], 
          "version": info["version"],
          "document_id":info["document_id"], 
          "tenant": info["tenant"], 
          "content_hash": compute_content_hash(source),
          "chunk_index": chunk_index_counter.get(info["document_id"], 0), # 当前片段在所属文档中的序号，从 0 开始
          }
        chunk_index_counter[info["document_id"]] = chunk_index_counter.get(info["document_id"], 0) + 1
        metadata["chunk_id"] = compute_chunk_id(metadata)
        chunk_id  = metadata["chunk_id"]
        # （G6）：用已补齐的 metadata 计算一次 chunk_id，写入 metadata["chunk_id"] 和新 Document.id。
        documents.append(doc.model_copy(update={"metadata": metadata,"id": chunk_id}))
        print(documents)
    return {"documents": documents}

# 将已补齐编号的片段保存到本地存储，并按本次编号顺序读回。
def store_documents(state: IngestState) -> dict[str, list[Document]]:
    """G6：把已补齐编号的片段保存到 STORE_DIR，按本次编号顺序读回并返回 documents。"""
    # 用 LocalFileStore 和 create_kv_docstore 创建能保存 Document 的存储对象。
    # 以每片的 Document.id 为键批量写入，再按本次编号顺序批量读回。
    # 读回若有缺失则明确报错；返回实际读回的 Document 列表，保留正文、id 和 metadata。
    store = create_kv_docstore(LocalFileStore(STORE_DIR))
    store.mset([(doc.id, doc) for doc in state["documents"]])
    documents = store.mget([doc.id for doc in state["documents"]])
    if None in documents:
        raise ValueError("Some documents are missing after reading from the store")
    return {"documents": documents}

# 生成和管理资料目录卡的辅助函数。
def compute_document_key(tenant: str, document_id: str) -> str:
    """G6 当前练习：由团队和稳定文档编号生成目录卡的文件键。"""
    # TODO：仅用这两个身份字段，以固定 JSON 格式编码并计算 SHA-256 十六进制字符串。
    record = {
        "tenant": tenant,
        "document_id": document_id, 
    }
    record_json = json.dumps(record, separators=(",", ":"), sort_keys=True,ensure_ascii=False)
    return hashlib.sha256(record_json.encode("utf-8")).hexdigest()

# 写入和读取资料目录卡的辅助函数。
def write_document_record(record: dict[str, object]) -> dict[str, object]:
    """G6 当前练习：保存一张资料目录卡，返回从存储实际读回并还原的字典。

    给定输入包含 tenant、document_id、chunk_ids；目录使用 STORE_DIR.parent / "records"。
    这里只提供单条记录写入/读回能力，尚未接图；后续更新流程须先读取并保留旧关联。
    """
    # TODO：生成记录键，把记录转成 JSON UTF-8 字节，用 LocalFileStore 写入并按键读回。
    # TODO：读回缺失则报错，否则还原为字典并返回；不得直接返回输入 record。
    key = compute_document_key(record["tenant"], record["document_id"])
    #因为这次保存的是“目录卡字典转成的字节”，
    # 而 create_kv_docstore 专门用于保存 Document 对象。两次保存的数据类型不同，所以使用方式不同
    store = LocalFileStore(STORE_DIR.parent / "records")
    record_json = json.dumps(record, separators=(",", ":"), sort_keys=True, ensure_ascii=False)
    store.mset([(key, record_json.encode("utf-8"))])
    read_back = store.mget([key])
    if read_back[0] is None:
        raise ValueError("Record is missing after reading from the store")
    return json.loads(read_back[0].decode("utf-8"))

# 读取资料目录卡的辅助函数。
def read_document_record(tenant: str, document_id: str) -> DocumentRecord | None:
    """G6 当前练习：按稳定身份读取旧目录卡；没有记录返回 None，已有记录则还原字典。"""
    # TODO：复用身份键和 records 目录；这里只读取，不写入，已有坏 JSON 不当作缺失。
    key = compute_document_key(tenant, document_id)
    store = LocalFileStore(STORE_DIR.parent / "records")
    read_back = store.mget([key])
    if read_back[0] is None:
        return None
    return json.loads(read_back[0].decode("utf-8"))


def prepare_document_records(state: IngestState) -> dict[str, object]:
    """G6 当前练习：把已补信息的片段汇总成新卡，并读取同一身份的旧卡。

    返回 document_records 与 previous_document_records 两个更新，均以目录卡键为键。
    同一资料的片段按输入中出现的顺序汇总；每份资料只读一次旧卡。
    空 documents 返回两个空映射；本步骤不写卡、不删片段、不修改输入或旧卡。
    """
    # TODO：复用 compute_document_key 分组，汇总每组的实际 Document.id。
    # TODO：读取各组旧卡并返回新旧两份映射，保留首次导入的 None。
    raise NotImplementedError("完成新旧目录卡准备")


# 构建摄取流程图，定义各节点及其依赖关系。
def build_ingest_graph():
    # G6 当前接图 TODO：实现准备节点后，接成 enrich_documents -> prepare_document_records -> store_documents。
    # 三个节点分别返回原生片段、补齐信息的片段，以及实际从本地读回的片段。
    graph = StateGraph(IngestState)
    graph.add_node("load_and_chunk_documents", load_and_chunk_documents)
    graph.add_node("enrich_documents", enrich_documents)
    graph.add_node("store_documents", store_documents)
    graph.add_edge(START, "load_and_chunk_documents")
    graph.add_edge("load_and_chunk_documents", "enrich_documents")
    graph.add_edge("enrich_documents", "store_documents")
    graph.add_edge("store_documents", END)
    return graph.compile()


def main() -> None:
  # 调用摄取流程图，传入初始状态，得到处理结果。
    result = build_ingest_graph().invoke(INITIAL_STATE)
    
    # 统计token数量
    chunker = create_chunker()
    counter = chunker.tokenizer #chunker.tokenizer是用于统计token数量的工具
    
    for index, doc in enumerate(result["documents"], start=1):
        print(f"\n--- 片段 {index} ---\n{doc.page_content}")
        token_count = counter.count_tokens(doc.page_content)
        print("token 数:", token_count)
        print("字符长度:", len(doc.page_content))
        print("metadata:", doc.metadata)
        pages = set()
        items = doc.metadata["dl_meta"]["doc_items"]
        for item in items:
          records = item.get("prov", [])
          for record in records:
              pages.add(record["page_no"])
              print("原始页码:", record["page_no"])
        if not pages:
            print("没有原始页码")
        print("所有原始页码:", sorted(pages))
    # print("sum", len(result["documents"]))


if __name__ == "__main__":
    main()


# === 2026-09-09 替换前原代码：仅作学习记录，以下全部不执行 ===
# 保留用户原始实现与当时注释（其中“当前/TODO”等描述属于替换前历史）。
# 原图：读取 Markdown 全文 -> Experimental 结构分组 -> Recursive 长度切分。
# 原图的 start_index 尚是组内位置，全文换算未完成；不能把它当现行定位规则。
# MarkdownHeaderTextSplitter 只做过对照，未在原图中启用。
# r"""R6-01-G3/G4/G5：用官方组件读取、切分文件，经 LangGraph 返回资料。
#
# 在项目根目录运行：
#     .\.venv\Scripts\python.exe code/stage6/engineering_docs_rag/ingest.py
#
# 输入：下面给定的 UTF-8 教学 Markdown 文件及文档说明。
# 任务：START -> load_documents -> END；节点调用 DoclingLoader.load() 解析并整篇导出 Markdown，
# 补充标题/版本，返回 documents 状态更新；运行图并展示文档数量、正文和 metadata。
# 完成标准：Document 来自真实 Loader；保留章节内容、配置名和值、代码块及必要换行；允许排版规范化。
# metadata 包含
# source（文件绝对路径字符串）、title、version，值与给定资料一致。
# 当前整份文档包含多个章节，不给全文填写单个 section。
# G3/G4 已由用户完成并经提示订正通过；助手负责 Docling 接入、PDF 配置和样本准备。
# G4：一次输入下面清单中的 MD/TXT/PDF，返回 3 份 Document，按各自 source 补标题/版本。
# 两页 PDF 在 MARKDOWN 模式下仍是 1 份 Document，不给整篇伪造单页 page 字段。
# 当前 G5 动手：START -> load_documents -> split_documents -> END。
# 切分节点处理已经读入的 documents，把切后的 Document 列表作为 documents 更新返回。
# 本次教学参数：每片最多 120 个 Python 字符，目标重叠 20；使用给定分隔符，标点留在前片末尾。
# 片段保留 source/title/version，并带相对 Docling 已导出正文的 start_index（0 起始），不是 PDF 页码。
# 当前三份样本在已核验配置下得到 9 片；这是观察用参数，不代表最优检索配置。
# G5 基础长度切分已由用户完成。当前增加结构切分 TODO，先用完整正文单独验证。
# 结构结果与全文位置关联核验后再接图，现有已通过的长度切分流程继续保留。
# 安装版本见同目录 requirements.txt，选择理由与边界见 problem-contract.md。
# """
# # 该模块实现了对教学 Markdown 文件的读取和处理，
# # 使用 LangChain 官方集成的 DoclingLoader 解析文件，并通过 LangGraph 构建状态图进行处理。
# from pathlib import Path
# # 该模块依赖于 langchain_docling、langchain_core 和 langgraph 包，
# # 确保已安装对应版本。作用是读取教学 Markdown 文件并构建状态图。
# from typing import TypedDict
# # 作用是提供类型注解，定义文档读取状态的数据结构。
# from docling.datamodel.base_models import InputFormat
# # 作用是提供 PDF 文档解析的配置选项。
# from docling.datamodel.pipeline_options import NativePdfPipelineOptions
# # 作用是提供文档转换器和 PDF 格式选项，用于自定义文档解析行为。
# from docling.document_converter import DocumentConverter, NativePdfFormatOption
# # 作用是定义文档读取状态的数据结构。来记录文件路径和已读取的文档列表。
# from langchain_docling import DoclingLoader
# from langchain_docling.loader import ExportType
# # 作用是提供对文档内容的封装，便于在状态图中传递和处理。
# from langchain_core.documents import Document
# from langchain_text_splitters import (
#     ExperimentalMarkdownSyntaxTextSplitter,
#     RecursiveCharacterTextSplitter,
# )
# # 作用是提供状态图的基本构建块，包括起始节点、结束节点和状态图类。
# from langgraph.graph import END, START, StateGraph
#
#
# # 样例文件路径和文档信息，用于初始化读取状态。
# SAMPLE_PATH = Path(__file__).resolve().parent / "sample_docs" / "quickstart.md"
# # 文档的标题和版本信息，用于补充 Loader 读取的内容。
# DOCUMENT_INFO = {"title": "工单服务：快速开始", "version": "1.0"}
#
#
# # G4 给定资料清单：键是每份文件的绝对路径，值是该文件自己的说明。
# # 保留上面的 SAMPLE_PATH / DOCUMENT_INFO，供工作台原有样本预览使用。
# DOCUMENT_CATALOG = {
#     str(SAMPLE_PATH): {"title": "工单服务：快速开始", "version": "1.0"},
#     str(SAMPLE_PATH.with_name("config.txt")): {"title": "工单服务：配置说明", "version": "1.0"},
#     str(SAMPLE_PATH.with_name("handover.pdf")): {"title": "工单服务：交接手册", "version": "1.1"},
# }
#
# # 助手给定的官方配置：PDF 提取已有文字，不运行文字识别或版面/表格模型。
# # 只覆盖简单的可选中文字 PDF；不代表扫描件或复杂排版已支持。
# # 作用是提供文档转换器的默认配置，确保 PDF 文档在解析时使用官方推荐的选项。
# DOCUMENT_CONVERTER = DocumentConverter(
#     format_options={
#         InputFormat.PDF: NativePdfFormatOption(
#             pipeline_options=NativePdfPipelineOptions(
#                 generate_page_images=False,
#                 generate_picture_images=False,
#                 parser_threads=2,
#             )
#         )
#     }
# )
#
# # G5 给定数据：依次尝试段落、换行、中文标点、空格，最后允许按字符切。
# SPLIT_SEPARATORS = ["\n\n", "\n", "。", "；", "，", " ", ""]
#
# # G5 给定标题映射：左边识别正文中的标题标记，右边是保存标题文字的 metadata 键。
# HEADERS_TO_SPLIT_ON = [("#", "h1"), ("##", "h2"), ("###", "h3")]
#
# # G4 把图输入扩为清单中的多个文件；读取后按 source 关联各自说明，展示全部结果。
# # 已通过的构图逻辑继续复用。支持列表的参数与 converter 参数见本次官方短段资料。
# # 定义文档读取状态的数据结构，包括文件路径和已读取的文档列表。作用是为文档加载提供统一的状态表示。
# class IngestState(TypedDict):
#     file_path: list[str]
#     documents: list[Document]
#
#
# # 初始化文档读取状态，包含样例文件路径和空的文档列表。作用是为后续的文档加载提供初始状态。
# INITIAL_STATE: IngestState = {"file_path": list(DOCUMENT_CATALOG), "documents": []}
#
# # 定义文档加载函数，接收当前状态，返回更新后的文档列表。作用是封装 Loader 的调用逻辑，并统一更新文档状态。
# def load_documents(state: IngestState) -> dict[str, list[Document]]:
#     # 调用现成 Loader，保留 source 并补充 DOCUMENT_INFO，返回 documents 更新。
#     # 助手按用户要求替换读取器；整篇导出，切分留到后续检查点。
#     # converter=DOCUMENT_CONVERTER意思是使用官方推荐的文档转换器配置来解析 PDF 文档。
#     loader = DoclingLoader(file_path=state["file_path"], export_type=ExportType.MARKDOWN,converter=DOCUMENT_CONVERTER)
#     documents = loader.load()
#     # print("Loaded documents:", documents)
#     for doc in documents:
#         if "source" not in doc.metadata:
#           raise ValueError("Document metadata missing 'source' key")
#         source = doc.metadata.get("source")
#         if source not in DOCUMENT_CATALOG:
#           raise ValueError(f"Source {source} not found in DOCUMENT_CATALOG")
#         info = DOCUMENT_CATALOG.get(source)
#         doc.metadata["title"] = info["title"]
#         doc.metadata["version"] = info["version"]
#     return {"documents": documents}
#
# # 作用是将已加载的文档按结构切分成更小的片段，便于后续处理。 跟split_documents不一样，会保留格式信息
# def split_by_structure(state: IngestState) -> dict[str, list[Document]]:
#     """G5 当前实作：输入已加载的完整正文，返回保留来源和章节信息的结构片段。
#
#     本步由 load_documents 的真实结果单独调用验证；全文位置核验后再接入图。
#     """
#     # 使用现成结构切分器保留标题/格式，合并各原文的片段并保留原 metadata，返回 documents 更新。
#     splitter = ExperimentalMarkdownSyntaxTextSplitter(
#       headers_to_split_on=HEADERS_TO_SPLIT_ON,
#       strip_headers=False,
#       )
#     split_docs = []
#     for doc in state["documents"]:
#         parts = splitter.split_text(doc.page_content)
#         for part in parts:
#           part.metadata.update(
#             source=doc.metadata["source"],
#             title=doc.metadata["title"],
#             version=doc.metadata["version"]
#           )
#         split_docs.extend(parts)
#     return {"documents": split_docs}
#
#
# # 作用是将已加载的文档切分成更小的片段，便于后续处理。
# def split_documents(state: IngestState) -> dict[str, list[Document]]:
#     """G5：把已读入的资料切成带来源、版本和正文位置的片段。"""
#     # 按本次要求配置现成切分器，处理 state 中的 documents，返回 documents 更新。
#     splitter = RecursiveCharacterTextSplitter(
#         chunk_size=120, # 每个片段的最大长度
#         chunk_overlap=20, # 每个片段与下一个片段的重叠长度
#         length_function=len, # 使用 len 函数计算文本长度
#         separators=SPLIT_SEPARATORS, # 使用预定义的分隔符列表进行文档切分
#         keep_separator="end", # 保留分隔符在片段末尾
#         add_start_index=True  # 在每个片段中添加起始索引信息
#     )
#     # 把原始documents进行切割后返回更新
#     split_docs = splitter.split_documents(state["documents"])
#     return {"documents": split_docs}
#
#
# # 定义构建文档加载状态图的函数，返回编译后的状态图。
# # 作用是将文档加载过程可视化，并便于在命令行或工作台中运行。
# def build_ingest_graph():
#     # G5 将新切分节点接在读取节点之后，再到 END；沿用已有构图方式。
#     # 沿用已学 StateGraph，连接 START -> load_documents -> END，返回编译后的图。
#     graph = StateGraph(IngestState)
#     graph.add_node("load_documents",load_documents)
#     graph.add_node("split_documents",split_documents)
#     graph.add_node("split_by_structure", split_by_structure)
#
#     graph.add_edge(START, "load_documents")
#     graph.add_edge("load_documents", "split_by_structure")
#     graph.add_edge("split_by_structure", "split_documents")
#     graph.add_edge("split_documents", END)
#     return graph.compile()
#
#
# def main() -> None:
#     # 运行 build_ingest_graph()，传入 INITIAL_STATE，展示真实结果。
#     graph = build_ingest_graph()
#     result = graph.invoke(INITIAL_STATE)
#     print("Graph run result:", result)
#     #doc: 打印切分后的文档总数
#     print("sum", len(result["documents"]))
#
#
# # 助手接入工作台时补充的机械入口：允许 API 导入本模块，不在导入时执行 main。
# if __name__ == "__main__":
#     main()
#     # load_documents(INITIAL_STATE)

r"""R6-01-G3：用现成 LangChain Loader 读取文件，经 LangGraph 返回资料。

在项目根目录运行：
    .\.venv\Scripts\python.exe code/stage6/engineering_docs_rag/ingest.py

输入：下面给定的 UTF-8 教学 Markdown 文件及文档说明。
任务：START -> load_documents -> END；节点调用 TextLoader.load() 读取全文，
补充标题/版本，返回 documents 状态更新；运行图并展示文档数量、正文和 metadata。
完成标准：Document 来自真实 Loader；正文保留配置名、Markdown 标记、换行和缩进；metadata 包含
source（文件绝对路径字符串）、title、version，值与给定资料一致。
当前整份文档包含多个章节，不给全文填写单个 section。
此文件是助手提供的 TODO 骨架，尚无用户实现或执行通过证据。
当前固定 community 0.4.2 的 TextLoader 用于教学 Markdown/TXT；该包已停止维护。
安装版本见同目录 requirements.txt，选择理由与边界见 problem-contract.md。
"""

from pathlib import Path
from typing import TypedDict

from langchain_community.document_loaders.text import TextLoader
from langchain_core.documents import Document
from langgraph.graph import END, START, StateGraph


SAMPLE_PATH = Path(__file__).resolve().parent / "sample_docs" / "quickstart.md"
DOCUMENT_INFO = {"title": "工单服务：快速开始", "version": "1.0"}


class IngestState(TypedDict):
    file_path: str
    documents: list[Document]


INITIAL_STATE: IngestState = {"file_path": str(SAMPLE_PATH), "documents": []}


def load_documents(state: IngestState) -> dict[str, list[Document]]:
    # TODO：调用现成 Loader，保留 source 并补充 DOCUMENT_INFO，返回 documents 更新。
    raise NotImplementedError("完成读取节点")


def build_ingest_graph():
    # TODO：沿用已学 StateGraph，连接 START -> load_documents -> END，返回编译后的图。
    raise NotImplementedError("完成图的构建；供命令行和统一工作台共同调用")


def main() -> None:
    # TODO：运行 build_ingest_graph()，传入 INITIAL_STATE，展示真实结果。
    raise NotImplementedError("完成图的运行与结果展示")


# 助手接入工作台时补充的机械入口：允许 API 导入本模块，不在导入时运行 TODO。
if __name__ == "__main__":
    main()

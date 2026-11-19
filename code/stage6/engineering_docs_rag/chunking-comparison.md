# 切分方案对照：采用 Docling HybridChunker

检查日期：2026-09-09。本文保留当时的 128 与 256 token 对照及问答结果；当前导入图的预算由 [ingest.py](ingest.py) 的 `CHUNK_MAX_TOKENS` 指定，现为 256。本记录属于助手受托完成的工程对照，不是用户独立理解或 R6-01 正式 PASS。

## 决定与理由

最终选择（同日补充真实问答对照后，用户再次明确授权助手决定）：使用官方 `DoclingLoader(export_type=ExportType.DOC_CHUNKS, chunker=HybridChunker(...))`，并在 LangGraph 中保留两个真实阶段：

```text
START
  → load_and_chunk_documents：文件清单 → 官方解析/切分所得 Document，含 source/dl_meta
  → enrich_documents：校验来源 → 复制 Document 并补业务 title/version
  → END
```

第一步已经完成切分，不能再解释为“读取全文”。第二步创建新对象和顶层 metadata 字典，保留前一步的正文与原生来源信息；可以分别查看两个阶段的更新。沿用原生文字 PDF 转换配置和用户已完成的来源检查。

相比先导出 Markdown、再按标题和长度切分，当前样本的启动说明能与配置代码同片，PDF 的元素引用与真实页码能够保留。初轮只测组件就迁移的依据不充分；用户随后要求暂停修改并补问答测试，暂停期间文件保持不变。下面的真实问答结果支持当前小样本优先采用 Hybrid，但不是它对所有文档普遍更好的证明。

保留官方 Loader 是本项目已确认的要求。其 DOC_CHUNKS 公开接口本来就在内部同时解析和切分，所以保留“解析并切分 → 校验并补业务信息”两个真实阶段，不为了延续旧节点名重复解析、调用私有方法或制造没有实际处理的结构/长度节点。

原来的 `ExperimentalMarkdownSyntaxTextSplitter + RecursiveCharacterTextSplitter` 两个切分函数及相关参数以注释保存在 [ingest.py](ingest.py) 末尾。普通 `MarkdownHeaderTextSplitter` 此前只用于对照，未进入原图。

## 比较方法与环境

- 真实样本：同目录 sample_docs 的 quickstart.md、config.txt、两页 handover.pdf，均为助手自编的虚构教学资料。
- 每轮将每份文件转换一次；旧方案使用同一解析对象导出的 Markdown，新方案使用原生 DoclingDocument，避免比较不同解析器。
- 旧原配置：Experimental 保留标题，再按 120 个 Python 字符、目标重叠 20 个字符递归切分。
- 公平对照：相同结构步骤，递归长度函数改为同一 `cl100k_base` token 计数，上限分别为 128/256，目标重叠 20 token；分隔符与保留标点方式沿用旧代码。
- Hybrid：官方 `OpenAITokenizer` 包装对象，上限分别 128/256，`merge_peers=True`；没有固定 overlap 参数。计数针对最终交付正文，包含 contextualize 补入的标题。
- 最终版本：langchain-docling 3.0.0、docling-slim 2.126.0、docling-core 2.95.0、langchain-text-splitters 1.1.2、tiktoken 0.12.0、semchunk 3.2.5。其余固定版本见 [requirements.txt](requirements.txt)。

首轮使用本机原有 tiktoken 0.14.0。复查发现 docling-core 2.95.0 的 chunking-openai extra 要求 `>=0.9.0,<0.13.0`，因此改为 0.12.0 并重跑下表，结果一致。pip 解析安装成功；不能只凭 pip check 忽略 extra 的条件依赖。

## 三份真实资料的结果

| 方案 | 大小设置 | MD / TXT / PDF 片数 | 总片数 | 最大正文 token | 正文 token 总量 |
| --- | --- | --- | --- | --- | --- |
| 原实现 | 120 字符 / 重叠目标 20 字符 | 4 / 2 / 4 | 10 | 96 | 681 |
| Experimental + Recursive | 128 token / 重叠目标 20 token | 4 / 1 / 4 | 9 | 125 | 715 |
| Hybrid | 128 token | 3 / 1 / 3 | 7 | 123 | 681 |
| Experimental + Recursive | 256 token / 重叠目标 20 token | 4 / 1 / 2 | 7 | 243 | 694 |
| Hybrid | 256 token | 3 / 1 / 2 | 6 | 240 | 682 |

总量是各片正文按同一编码规则相加，包含重复上下文，并非模型计费或检索质量分数。本次选 128 是为了继续观察小样本边界，未认定它比 256 更准确或适合生产。

可直接看到的区别：

- 快速开始中，旧结构切分把“本地默认端口为 8000、本地配置示例”和代码各放一片。Hybrid 将同节说明与 `TICKET_ENV=local / TICKET_PORT=8000` 的完整短代码放在一起，并在正文前补“工单服务：快速开始 / 本地启动”。
- 三份资料的配置与版本保留：MD/TXT 为 1.0、8000；PDF 为 1.1、8100，第二页的 HANDOVER_READY 及回退到 1.0 恢复 8000 的条件仍在。
- 128 配置下 PDF 三片的来源页集合依次是 `[1]`、`[1, 2]`、`[2]`。它会跨页，不能只取某个首个页码冒充整片所在页。
- 旧方案目前有 3 个章节片段尚未换算全文位置，这是可修复的步骤衔接缺口，不作为“旧组件天生不能定位”的证据。

## 额外边界探针

探针为临时目录中的自编 Markdown，测试后自动清理；后续保护真实导入行为的必要用例保存在工作台已有 tests 中。

| 输入 | 旧标题/长度流程 | Hybrid 128 | 判断 |
| --- | --- | --- | --- |
| 短 Python，4/8 空格缩进，代码字符串含 `##` | Experimental 流程保留完整代码，3 片；普通 MarkdownHeader 对照不保留准确缩进 | 1 片，说明与代码一起，准确缩进和代码内标记保留 | 短代码有实际改善；不是所有空白逐字还原保证 |
| 50 行 Python 追加语句 | 5 片，50 个值与行内缩进保留；部分片段围栏不完整 | 4 片，最大 123 token，50 行内容、缩进、顺序保留；部分围栏不完整 | 两种方案都未解决任意超长代码独立完整的问题 |
| 两节不同前提，重复“端口设为 8000。” | 章节说明可保留 | 2 片分别有“本地环境 / 回退环境”，元素引用不同 | 重复文字没有混到同一前提；不能靠 find 的第一次匹配定位 |
| 两行版本/端口/条件表格 | 1 片，Markdown 表格形式 | 1 片，改成“1.0, 端口 = 8000 …”等单元格说明，关联 tables 元素 | 值与关联保留，原表格排版不保留 |

默认 Docling 导出和 Hybrid 代码序列化都没有保留本次输入的 python 围栏语言标签；Hybrid metadata 默认也不包含完整代码原文或 code_language。当前 PDF Native 流程没有识别所有标题，不把未运行的版面/OCR 模型能力算作切分器收益。

## 现行来源位置的含义

顶层 `source/title/version` 继续表示文件路径与业务标题/版本。`dl_meta.headings` 表示章节；`dl_meta.doc_items[].self_ref` 指向本次 Docling 解析结果中的文档元素；PDF 的 `prov[].page_no` 是实际页码。MD/TXT 没有实际页码时不编造。

这些元素引用属于本次解析对象，不是跨更新稳定的 document_id/chunk_id。标题补入后，片段不一定是导出 Markdown 的连续子串，因此不生成含义错误的 start_index。Native PDF 的 charspan 是元素内跨度；超长元素拆成多个片段后可能共享同一元素范围，不能用它做精确片段高亮或冒充全文字符偏移。

原来的全文位置换算练习随本次用户授权迁移暂停，保留已有原答和接图证据；不据此认定用户掌握了未完成的位置换算。下一学习起点为新定位规则与长代码取舍，再继续原定的稳定编号、重复/更新/删除和其他未覆盖标准。

## 补充：同一检索与真实模型的问答对照

三份真实样本不变，同一次解析对象分别供原120字符、旧流程128 token、Hybrid128 token三分支切分。检索与问答只在内存的临时 LangGraph `retrieve → answer` 中执行；不修改现有产品，不扫描知识库。复用已配置的真实 DeepSeek 和现有 BM25 中文双字/英文标识符查询处理，每次最多4片，资料JSON上限768个cl100k_base token。三分支统一还原标识符中的Markdown下划线转义，统一提供来源文件名、标题、业务版本、章节、正文和引用编号；避免把转义或漏传metadata当作切分优劣。

先固定10题与必要事实/依据标准，再用相同系统提示、`deepseek-v4-pro`、temperature=0、thinking关闭、输出上限1200执行，每分支每题两次，共60次真实调用，0调用错误。任务以固定随机种子打乱，最多4个并发；每次问答使用独立输入。回答要求仅依据所给资料、保留版本条件、信息不足时说明，并返回正文与来源摘录。未在看到答案后修改问题或切分参数。

| 方案 | 必要事实完整正确 | 事实正确且所指片段支持主张 | 平均资料JSON长度 |
| --- | --- | --- | --- |
| 原120字符流程 | 16/20（80%） | 12/20（60%） | 526.1 token |
| 旧流程128 token | 18/20（90%） | 15/20（75%） | 665.9 token |
| Hybrid128 token | 18/20（90%） | 18/20（90%） | 628.6 token |

每组只有10道不同问题，重复两次不是20道独立题。token长度包括标题、业务信息和引用标签，不是DeepSeek计费计数；三组实际均取4片，未达到768的截断上限。主指标按预先规则评价必要事实完整性和引用的语义支持，不把附带摘录是否逐字复现或行内编号格式临时并入得分。

| ID | 固定问题的完整判断 | 原120 / 旧128 / Hybrid 的整题通过次数 |
| --- | --- | --- |
| Q1 | 1.0本地启动核对哪两个配置及值，并给依据 | 0/2、2/2、2/2 |
| Q2 | 升级1.1后启动前核对哪两个配置值，并给依据 | 2/2、2/2、2/2 |
| Q3 | 快速开始8000与交接手册8100是否矛盾，各适用什么版本，引用两边 | 0/2、0/2、2/2 |
| Q4 | 1.0报CONFIG_MISSING的原因和第一步检查 | 0/2、1/2、2/2 |
| Q5 | 看到TICKET_PORT=8000能否直接改8100，应先查什么并怎样按版本判断 | 2/2、2/2、2/2 |
| Q6 | 交接手册何时要求恢复8000，是否意味着1.1平时也应使用8000 | 2/2、2/2、2/2 |
| Q7 | 交接记录至少包含的字段和演示交接标记 | 2/2、2/2、2/2 |
| Q8 | 快速开始能否证明1.1/8100，正确出处是什么，快速开始实际支持什么配置 | 0/2、0/2、0/2 |
| Q9 | 完整启动命令及.env目录；未提供时明确说明 | 2/2、2/2、2/2 |
| Q10 | 能否证明真实服务已在8100运行并给出当前可访问地址 | 2/2、2/2、2/2 |

决定性失败：

- 原120的Q1两次把1.1的8100当作1.0答案；其检索遗漏了1.0完整配置组合，模型仍应拒绝跨版本补答案。两个128方案取得了足够证据并回答正确。
- 两个旧方案Q3虽然版本和数字正确，但将“快速开始8000”挂到只含简介/版本的片段；Hybrid检索到实际启动说明和代码，引用得到支持。
- Q4旧120两次、旧128一次将正确的缺失原因挂到交接片段；Hybrid两次均指向实际配置缺失节。
- Q8三组均未找全快速开始的8000证据，Hybrid也遗漏该必要事实；旧方案还出现把“检索片段没给出”扩大成“整份文档没有”的错误。只换切分器不能解决所有检索缺口。

另行保留输出问题：旧128的Q10两次正文主张有引用集合支持，但附带quote把原句贴到另一个片段；Hybrid的Q10一次拼接不连续原句而未标省略；原120的Q10结构化引用正确但正文缺行内编号。这些不能描述成“所有引用输出要求均通过”。同一来源的换行/空格规范化未当作事实或来源错误。

Q1/Q3/Q4/Q8及Q10判分尺度由另一协作先读取金标、再在不知道方案身份的情况下核对；其他题由主执行者逐条核对真实上下文与回答，不夸大全量独立复核范围。原始调用输出保留在本任务工具记录，本地只保留这份紧凑对照，不创建一次性runner、日志转储或平行评估系统。

产品边界：`knowledge_agent.py` 仍使用自身的读取/切分/检索流程，未调用当前ingest。因此这是三份资料在受控问答链上的结果，不是现有工作台知识库问答已迁移或线上准确率已提高。后续真实检索、引用与更大语料验收仍按原任务继续。

## 复跑与证据

在仓库根目录运行：

```powershell
.\.venv\Scripts\python.exe -m pytest code/agent_workbench/api/tests/test_ingest.py code/agent_workbench/api/tests/test_api.py -q
.\.venv\Scripts\python.exe -m pip install --dry-run -r code/stage6/engineering_docs_rag/requirements.txt
```

最终合并复跑：29 passed（核心6项、接口23项；现有 Starlette/httpx 弃用提示1条），退出0。核心用例先准备公开token编码表缓存，再阻断解析/切分阶段的网络；从真实Loader获取三格式结果，直接用同次PDF转换对象核对元素引用与来源，不固定片数。核心及整个工作台API的requirements均经pip dry-run解析成功，相关改动的git diff --check通过。

最终两阶段整理后，同一合并命令再次29 passed；新增阶段顺序、第一步结果不被第二步修改，以及来源失败时输入不被部分改写的断言。真实8765/5173导入均200、7片，逐片正文/来源/标题/业务版本/章节与前轮QA的Hybrid实际输入一致，故不重复真实模型对照。旧代码注释档案、依赖与独立知识库问答核心未变。

真实 HTTP：后端 8765 和前端代理 5173 的 POST /api/rag/import 均为 200、7 片，最大 123 token；source/title/version/dl_meta 逐片有效，PDF 页集合如上。GET /api/rag/sample 两路仍返回整份 Markdown 预览。HTTP/图检查不冒充浏览器点击或用户独立操作证据。

## 官方依据

以下为 2026-09-09 实际读取的官方说明及本机对应版本源码：

- [Docling 切分概念](https://docling-project.github.io/docling/concepts/chunking/)：原生结构、按 token 拆分/合并、补标题上下文。
- [Hybrid 官方示例](https://docling-project.github.io/docling/_generated/examples/hybrid_chunking/)：显式 tokenizer 包装和预算；计数规则应与后续 embedding 模型对齐。
- [LangChain DoclingLoader 集成](https://docs.langchain.com/oss/python/integrations/document_loaders/docling)、[Loader 3.0.0 源码](https://github.com/docling-project/docling-langchain/blob/v3.0.0/langchain_docling/loader.py)：DOC_CHUNKS、contextualize、source/dl_meta。
- [Hybrid 2.95.0 源码](https://github.com/docling-project/docling-core/blob/v2.95.0/docling_core/transforms/chunker/hybrid_chunker.py)：内部分层切分与再拆分路径。超长代码边界以上述真实执行为依据。

本次 cl100k_base 只作固定测量规则，不代表 DeepSeek 计费或尚未选定的 embedding 模型。首次可能下载公开编码表；本地解析和切分阶段没有下载模型权重或调用模型 API。上面的真实问答对照另行将检索片段发送给模型，共调用 60 次。

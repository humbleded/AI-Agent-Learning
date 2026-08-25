# 学习资料导航与依赖顺序

## 一、够不够用？结论先说

- **现有概念教材足够，甚至偏多；生产工程资料必须以任务启动时的官方文档为主。** `repos/` 里的书和课程负责解释原理，FastAPI/Pydantic/SQLAlchemy/Redis/LangGraph/MCP/评估/安全等快速变化内容在开始任务当天核对官方文档，不能只照本地旧示例。
- **原路线真正偏薄的是 Python Agent 后端、生产 RAG、可恢复执行、持续评估、安全和 CI/CD。** A4 后按 `G8-00 → R6/BE5/B0 → pgvector 与 RAG 对照 → FastAPI/SSE → durable G8 → BE5/R6 Gate → 多 Agent 对照与 G8-Gate → 长期 Memory → MCP → 评估 → 产品化与 FINAL` 补齐；工程知识在两个真实项目产生依赖时学习，不先完整上完一套孤立后端课。
- **知识库只保存正式、稳定的沉淀。** 当前结构、既有页面和同步规则必须在实际同步前读取 `D:\AI-Knowledge`；不在本资料页复制会过期的文件数量或日期快照。

## 二、你已有的核心资料（都在 repos/，离线可用）

| 资料 | 位置 | 用途 | 语言 |
| --- | --- | --- | --- |
| Hello-Agents 全书（16 章） | `repos/hello-agents/docs/chapterX/第X章*.md` | Agent 主教材：原理 / 范式 / 框架 / 记忆 / RAG / 上下文 / 评估 / 项目 | 中（另有英文版） |
| Hello-Agents 配套代码 | `repos/hello-agents/code/chapterX/` | 每章可运行示例 | 中注释 |
| HelloAgents 框架源码（指定分支） | `repos/HelloAgents-feature-branch-1/hello_agents/` | H5-01 可选单链路源码追踪对象 | — |
| HuggingFace Agents Course（中文版） | `repos/agents-course/units/zh-CN/` | 工具/动作/观察、function calling、LangGraph、Agentic RAG、评估 | 中 |
| Agentic Design Patterns（21 章 + 附录） | `repos/agentic-design-patterns/bilingual/`（中英）`/chapters/`（英） | 阶段 7 设计模式主资料；MCP/RAG/Guardrails/评估都有 | 中英对照 |
| Agent Learning Hub 路线图 | `repos/Agent-Learning-Hub/README.md` | 现代生产视角的 todo / Project Ladder / 官方资料索引 | 中 |

> 重点：Hello-Agents 第 9 章《上下文工程》正好是 S-03 的资料；第 12 章是评估；第 13–16 章是完整项目案例（旅行助手、深度研究、赛博小镇、毕业设计），可作为你阶段 10 综合项目的参考蓝本。

**额外推荐（中文实战，按需读取）：[llm-universe｜动手学大模型应用开发](https://github.com/datawhalechina/llm-universe)**（Datawhale，[在线阅读](https://datawhalechina.github.io/llm-universe/)）

- 是什么：面向小白、**项目导向**的中文教程，带你从零搭一个「个人知识库助手」(RAG)。覆盖：调用大模型 API（含国内模型）、Prompt、Embedding 与向量库、用 LangChain 搭检索问答链、Streamlit 部署、评估。
- 怎么用：当 **阶段 2（Prompt）和阶段 6（RAG）的中文实战补充**最合适；阶段 1 也能参考它「调用 API」一节（讲国产模型，和你用 DeepSeek 对得上）；部署部分呼应 J11。
- 定位提醒：它和 Hello-Agents **互补**——Hello-Agents 偏 Agent 原理 / 从零构建，llm-universe 偏 LLM 应用 / RAG 落地（直接上 LangChain）。它为求简洁删了底层原理，所以当「实战」用、别替代你 tracker 里「先理解再写」的要求。内容是 2024 V1（举例用文心 / 讯飞 / 智谱），调用模式照搬到 DeepSeek 即可。

## 三、按当前依赖的资料导航（先读什么 → 再读什么 → 动手）

资料优先级：**当前官方文档/规范校准 → 中文教材建立直觉 → 参考代码对照 → 当前项目落地**。CSDN、知乎、视频和旧课程只能作辅助，不能作为版本字段、认证、安全和生产配置的事实源。

英文资料采用渐进式训练：阶段 0–3 以中文建立直觉；阶段 4–5 保留英文原始标题、参数名与报错，让用户自己定位关键段落；从 BE5 起，短篇英文官方文档先由用户提取 2–3 条事实，卡住时再逐段翻译，不再默认整篇代译。

- **阶段 0 Python**：廖雪峰对应小节 → CS50P 对应 Week → 写 `code/stage0/` 练习；是否完成只读 `progress.md`。
- **阶段 1 大模型 API**：OpenAI Quickstart → Text Generation / 流式文档 → DeepLearning.AI《Building Systems with ChatGPT API》对应小节 → 写 L1 代码。
- **阶段 2 Prompt/结构化**：DeepLearning.AI《Prompt Engineering for Developers》Guidelines → OpenAI Prompt Engineering + Structured Outputs → 配合 **HA 第 9 章上下文工程（S-03）** → 写 PR2 代码。
- **阶段 3 工具调用**：HF 中文 unit1 `tools/actions/observations` → HF `bonus-unit1` function calling → OpenAI Function Calling → 读 `HA code/chapter4` 工具代码 → 写 T3。
- **阶段 4 Agent 原理**：HF unit1 `what-are-agents` → HA 第 1–4 章 → ADP 第 4/5/6 章（Reflection/Tool Use/Planning）→ 跑 `HA code/chapter4` 的 ReAct/Plan/Reflection。
- **G8-00 LangGraph 入门（课程位置阶段 4.5）**：当前官方 Graph API → StateGraph/state/node/edge/条件路由/tool/stream/test → 在新的“故障诊断与变更评审 Agent”业务中重建控制流；复用 A4 已 PASS 的控制原则，不复制 A4 的 research-agent 题目，也暂不读 persistence/interrupt/resume。编号属于后续 LangGraph 旗舰，不代表阶段 5～7 被跳过。
- **阶段 5 框架源码（可选）**：只有真实调用链阻塞时才沿一个入口追到 Agent/LLM/Tool/Message 并重建一个关键行为；不按目录通读、不阻塞 G8/R6。
- **R6-01 → BE5-01**：先完成 LangChain Loader/Splitter/Document/metadata、Markdown/TXT/PDF 导入、去重和增量文档状态，再在同一工程文档 RAG 项目内补 Python 项目结构、日志、测试、lint 与类型检查；两个 ID 分别验收。
- **B0-01 → B0-03 → B0-04 → B0-Gate → BE5-04**：先补命令行/进程/日志、SQL 和 Docker，再通过工程基础 Gate；之后学习 SQLAlchemy/Alembic/PostgreSQL/pgvector。不能让后面的数据库任务倒过来证明前置基础已经完成。
- **R6-02/S-02 → R6-03/S-06**：先用轻量本地索引理解 embedding/top-k，再迁移 PostgreSQL + pgvector；做 exact/HNSW、filter、关键词/hybrid、rerank 与 Recall@k/MRR。随后在同一评估集比较固定两步 RAG 与 Agentic RAG，并用真实结果判断 Prompt、RAG、微调怎样选；挂载任务必须分别写回状态。
- **BE5-02/03**：两个纯 Python 核心可运行后，再学习 asyncio、Pydantic、FastAPI、HTTP/SSE、超时、取消、并发和接口测试，把它作为交付层接到两个项目。
- **G8-01 → G8-02 → G8-03**：LangGraph 官方 persistence/interrupts/durable execution/testing 为主线 → checkpoint/thread、PostgreSQL checkpointer、进程恢复、HITL 与副作用幂等；SQLite 只能作临时学习步骤，最终持久化证据使用 PostgreSQL。这里只说明与长期 Memory 的边界，不等待 D7。
- **BE5-05 → BE5-Gate → R6-Gate**：Redis、后台任务、认证、负载、CI、Docker 与 smoke 先完成共同后端 Gate，再完成工程文档 RAG 旗舰 Gate；不让后续 G8-Gate 倒补前置工程能力。
- **D7-02 → S-04 → G8-Gate**：只读取多 Agent 的取舍切片，在同一数据集保留单 Agent baseline，再验证受控协作是否有净收益。G8-Gate 核心是持久恢复、HITL、幂等、评估和可观察状态；需要薄界面时可在任务启动后引入经过审计的开源 Vue 骨架，但完整前端掌握留到 J11-03 复核。
- **D7-01 → D7-03 → D7-Gate**：项目可运行后，在已有旗舰上判断 chaining/routing/parallelization，并实作跨会话长期 Memory 的完整生命周期、安全和无 Memory 对照；不另起玩具。
- **阶段 9 MCP**：最新 MCP 官方 specification/SDK 为主线（server capabilities、transport、authorization、安全）→ HA/ADP 作中文解释和框架对照 → 写 M9。可选只读「Skills vs Tools/MCP/Subagents」辨析，不提前陷进 Skills 生态。
- **阶段 10 评估与系统设计**：LangSmith Evaluation/Observability 官方文档 → HA 第 12 章、ADP 第 19 章、HF `bonus-unit2` 辅助 → 建一套共享 Eval Harness、为两个旗舰分别接领域 dataset/adapter/指标和 baseline/regression，并完成两个项目的系统设计包；这里不提前做 FINAL，也不复制两套评估平台。
- **J11 产品化 → FINAL → 求职收口**：J11-02 根据 Gate/E10 证据由用户冻结唯一 `product_flagship`，只为它继续建设正式 Vue、公网部署和产品级观测；另一个旗舰保留可复现 API/demo、容器与完整评估。完成作品集组合和 S-05 综合安全收口后做 `FINAL-Gate`；之后才进入简历、面试和 `J11-Gate`。

## 四、工程化与补充资料（BE5 + S-01~S-07 + J11）

| 主题 | 挂载 | 推荐资料（优先中文 / 官方） |
| --- | --- | --- |
| Python 工程化（BE5-01） | 阶段5.5 | Python 官方 typing/dataclasses/logging；pytest、Ruff、mypy 或 pyright 官方文档；`packaging.python.org` 的 `pyproject.toml` 指南 |
| async/并发（BE5-02） | 阶段5.5 | Python `asyncio` 官方文档；httpx async、FastAPI async tests 官方文档；重点核对 timeout/cancel/TaskGroup/Semaphore |
| FastAPI/Pydantic（BE5-03） | 阶段5.5 | FastAPI 官方中文/英文；Pydantic v2 官方；Starlette/httpx 官方 SSE/测试资料，不以 CSDN 示例作主线 |
| 数据/任务（BE5-04/05） | 阶段5.5 | SQLAlchemy 2、Alembic、PostgreSQL、Redis 官方；Celery/RQ/ARQ 任选一个官方 quickstart；Locust 或 k6 官方 |
| 多厂商模型（S-01） | A4-Gate 后、J11-02 前 | 先抽 provider 接口，再查 Anthropic 文档 `docs.anthropic.com`、OpenRouter `openrouter.ai/docs` 或本地 Ollama；按真实项目依赖接入，不阻塞当前 G8/R6 |
| Provider 韧性与复合故障（BE5-02/FINAL） | 阶段5.5 起 | HTTP `Retry-After`/429 语义、Python `asyncio`/httpx 官方文档；重点练指数退避+jitter、可重试分类、取消传播、fallback、配额/成本上限和 fault injection，不把无限重试当可靠性 |
| 生产向量检索（S-02） | 阶段6 | pgvector 官方为主；PostgreSQL full-text/BM25 方案、Qdrant/Milvus 官方按 JD 对照；RAGAS/LangSmith 评估官方资料 |
| 上下文工程（S-03） | 阶段2/4 | **HA 第 9 章（已有）**；Anthropic《Building effective agents》（Hub 里有链接） |
| 多 Agent（S-04/G8） | G8 单 Agent baseline 后、D7-02 评审 | [LangChain Multi-agent 官方概览](https://docs.langchain.com/oss/python/langchain/multi-agent)；[Subagents](https://docs.langchain.com/oss/python/langchain/multi-agent/subagents)；ADP 第 7 章辅助。重点是何时不需要多 Agent、context engineering、带类型约束的角色交接格式、共享/私有 state、停止/预算/升级与单 Agent 对照；不默认采用 supervisor helper 库 |
| Agent 长期 Memory（D7-03/FINAL） | 两个项目可运行后 | [LangGraph Memory](https://docs.langchain.com/oss/python/langgraph/add-memory) 与 [Persistence](https://docs.langchain.com/oss/python/langgraph/persistence) 官方文档；PostgreSQL 作为事实源；OWASP Agentic Applications 的 Memory & Context Poisoning。重点区分 history、checkpoint、RAG 与跨会话 Memory，并实作 CRUD/TTL/provenance/隔离/删除/poisoning/baseline |
| Guardrails / 注入（S-05） | R6/D7/M9/J11 分段挂载，FINAL 前收口 | OWASP Top 10 for LLM/Agentic Applications 与 Threats and Mitigations（主线）；MCP Security Best Practices；ADP 第 18 章辅助 |
| 微调 vs RAG（S-06） | 阶段6/10 | 概念为主：搜「RAG vs 微调 选型」；HA 第 8 章相关讨论 |
| FastAPI 服务化（J11-02） | 阶段11 | 复用 BE5 官方资料；先根据两个 Gate/E10 证据冻结唯一 `product_flagship`，再重点查认证、部署、SSE、取消、health/readiness、API 文档和负载测试，不重新学入门或建设第二套产品服务 |
| Vue + 流式（J11-03） | 阶段11 | 只为 `product_flagship` 建正式前端。用户会一些 Vue，先用最小切片复核组件、状态、异步请求和浏览器调试；已证明的部分不重复。助手可在任务启动时审计许可证、维护状态、依赖与安全风险后组合 GitHub 开源 Vue 骨架；用户审核关键 diff，并解释/修改状态、SSE、认证、错误处理和前后端边界。再按缺口读取 Vue 官方文档和 MDN `EventSource` / `fetch` 流式资料 |
| Docker 部署（J11-04） | 阶段11 | **B0-04 已有 Docker 中文文档 + 黑马视频**；只强化 `product_flagship` 的公网产品链，上线平台 Railway `docs.railway.app` 或 Render `render.com/docs` |
| 可观测/评估（E10/J11-05） | 阶段10/11 | E10 用一套共享评估基础设施服务两个领域 adapter；J11-05 只为 `product_flagship` 强化线上 tracing/告警。资料使用 LangSmith Evaluation/Observability 官方或 Langfuse 官方、OpenTelemetry GenAI conventions、代码 evaluator + LLM-as-judge + baseline/regression |
| MCP（M9） | 阶段9 | `modelcontextprotocol.io/specification` 最新 revision 与官方 SDK；重点看 STDIO/Streamable HTTP、authorization/security，不以 HelloAgents 实现代替规范 |
| CI/CD/上线（J11-04） | 工程上线 | GitHub Actions、Docker、目标云平台官方；health/readiness、secret、non-root、smoke、回滚、备份、Locust/k6 官方 |
| 算法（J11-08） | 阶段11（W4 起启动） | **原理教材：《Hello 算法》`hello-algo.com`**（免费开源，动画图解＋Python 代码一键可跑，非科班友好）——W4 算法启动先读复杂度/数组与链表/哈希表打底，之后刷到哪个专题回头补哪章原理；刷题路线：代码随想录 `programmercarl.com`（含视频，按专题刷）＋ LeetCode 热题 100 `leetcode.cn`（题单） |
| 系统设计 / 架构论证（BE5/R6/G8/E10/J11-08） | BE5 起随旗舰 Gate 演化，J11-08 限时复述 | [AWS Well-Architected Framework](https://docs.aws.amazon.com/wellarchitected/latest/framework/welcome.html) 用于质量属性与架构取舍检查；[Google SRE Workbook：Implementing SLOs](https://sre.google/workbook/implementing-slos/) 用于 SLI/SLO 与错误预算；[Azure Well-Architected Framework](https://learn.microsoft.com/en-us/azure/well-architected/) 作可靠性、安全、成本、运维与性能的交叉清单。每次只读当前 Gate 所需小节，并落成 API/事件接收什么、返回什么及失败怎样表示的规则、数据模型、请求/数据流、容量假设、2–4 个可测 SLI/SLO、缓存/队列/同步异步取舍、降级方案与 ADR；小林 coding 与 Agent 面试题只用于 J11-08 问答补充，不作架构事实源。 |

### LangChain / LangGraph / RAG 官方源码切片

以下来源只在对应知识单元真正开始时读取或浅克隆；路线修订阶段不提前创建 `repos/` 副本、未来代码或课程骨架。GitHub 星标和 trending 只用于发现线索，不能单独决定课程主线。

| 来源 | 当前路线中的用法 | 明确不采用 |
| --- | --- | --- |
| [LangChain 官方概览](https://docs.langchain.com/oss/python/langchain/overview)、[Retrieval](https://docs.langchain.com/oss/python/langchain/retrieval) | 核对当前 `create_agent`/组件边界，区分固定两步、Agentic 与 Hybrid RAG | 不把三种架构默认叠加；不把 `create_agent` 隐藏的 LangGraph runtime 当作直接掌握 StateGraph 的证据 |
| [langchain-ai/langchain](https://github.com/langchain-ai/langchain) | 查当前入口、核心抽象、错误边界和测试设计 | 不从头通读巨型仓库，不复制内部实现 |
| [rag-from-scratch](https://github.com/langchain-ai/rag-from-scratch) | 选择 indexing、retrieval、generation、query transformation 切片重建心智模型 | 不照抄旧 notebook API；执行时以官方文档和已安装版本为准 |
| [LangGraph 官方概览](https://docs.langchain.com/oss/python/langgraph/overview)、[Graph API](https://docs.langchain.com/oss/python/langgraph/graph-api)、[Persistence](https://docs.langchain.com/oss/python/langgraph/persistence)、[Interrupts](https://docs.langchain.com/oss/python/langgraph/interrupts)、[Streaming](https://docs.langchain.com/oss/python/langgraph/streaming)、[Testing](https://docs.langchain.com/oss/python/langgraph/test) | G8 的显式编排、持久化、HITL、流式与测试事实源 | 不把 runtime 源码阅读扩成框架开发主线 |
| [langchain-ai/langgraph](https://github.com/langchain-ai/langgraph)、[langgraph-101](https://github.com/langchain-ai/langgraph-101) | 精读 101 基础和一个与 persistence/HITL 对应的 201 示例 | 不机械完成全部 notebook |
| [local-deep-researcher](https://github.com/langchain-ai/local-deep-researcher) | 只吸收来源进入 state、查询循环上限、反思次数限制和 trace 结构 | 不复制研究主题，不与 A4 重复造第三个 research agent |
| [pgvector/pgvector](https://github.com/pgvector/pgvector) | exact/HNSW、filter、迭代扫描、PostgreSQL FTS/hybrid 与数据一致性 | 不用热度替代 Recall@k/MRR、故障或迁移证据 |
| [langchain-ai/langchain-postgres](https://github.com/langchain-ai/langchain-postgres) | 核对当前 LangChain + PostgreSQL/pgvector 集成和迁移说明 | 不依赖过时 community 示例；任务开始时确认当前推荐类与版本 |
| Qdrant / Milvus 官方资料 | 目标 JD 明确要求或需要解释取舍时做短对照 | 不并行开两条完整向量数据库课程 |

每个被选中的源码切片必须形成可复核证据：

- 记录 URL、检查日期、commit SHA；快速变化的 API 同时记录库版本。
- 画出入口、核心 State/数据必须包含哪些字段与遵守哪些规则、主控制路径、错误边界和测试策略的源码地图。
- 用自己的最小代码重建一个关键行为，再迁移到当前项目，并由测试或 trace 证明。
- 写清一个采用的设计、一个拒绝的设计和拒绝原因。
- 已归档仓库（包括 `rag-research-agent-template`）不得作为主教材或当前 API 依据。

## 五、视频清单（中文，按需补，不是主线）

- Python / 工程基础：廖雪峰（文档）、CS50P、黑马 Python、黑马 Docker、尚硅谷 MySQL、MIT Missing Semester——均已在 tracker 各阶段列出。
- 算法：代码随想录配套视频（programmercarl.com 每题都有 B 站讲解）。
- FastAPI / 向量库 / LangGraph：以官方文档为主；想看视频就在 B 站搜「FastAPI 入门」「向量数据库」「LangGraph 教程」，用发布日期和内容范围筛选，播放量只作辅助信号。
- Agent / 大模型 基础概念与直觉：**马克的技术工作坊**（[B 站](https://space.bilibili.com/1815948385)，YouTube 同名）——0→1 讲 LLM、Token、Context、Prompt、Tool、MCP、Agent、Agent Skill 等核心概念，新手友好、内容偏新。建议先看《从 LLM 到 Agent Skill，一期带你打通底层逻辑》（[B 站](https://www.bilibili.com/video/BV1E7wtzaEdq/)）建立全局地图，之后开新主题时用他的概念视频找直觉。注意：他偏 Claude Code / Agent Skills，略超当前依赖，**看个直觉就好，别被带跑去提前搞 Skills**，按 `daily-plan.md` 的当前单元走。
- 原则：**视频是辅助，不要用「看视频」代替「动手写」。** 概念看一遍够了，时间花在敲代码和过 Gate 上。

## 六、关于 D:\AI-Knowledge（Obsidian 库）怎么用

- 定位分工：`AI-Agent-Learning` 放**过程**（练习代码、Session 原始记录、笔记草稿、源码）；`AI-Knowledge` 放**沉淀**（稳定结论、概念卡片、面试复习卡、踩坑记录）。
- 建议节奏：每过一个 **Gate**，筛选该阶段的核心概念、自己的问答和踩过的坑，候选量控制在 1–2 张；使用「检查今天的学习」或已有明确授权时直接同步，普通 PASS 则先确认。用 `smart-connections` / `omnisearch` 在复习和面试前快速检索。
- 当前已在持续写入概念卡；每过一个 Gate 继续筛选 1–2 张高价值候选即可，不按文件数量追求“填满知识库”，也不绕过授权边界自动写入。

## 七、怎么用 Agent-Learning-Hub（嫁接 3 样，别照搬）

`repos/Agent-Learning-Hub/README.md`（Datawhale，hello-agents 同作者）是一份「现代生产视角的 Agent 学习路线图 + 项目阶梯 + 资料索引」。它**比本路线更超前、更偏 agent 基础设施**（钻 Claude Code / OpenClaw harness 内部），其原始内容默认读者已有 Python/LLM 基础，因此不能直接拿它的前提套到用户身上。**结论：保留本路线当主干，从 Hub 只嫁接下面 3 样，其余当索引查，别整本照搬**（它资料量巨大，照搬会淹没，且和已有的 hello-agents / agentic-design-patterns / agents-course 重复）。

### 嫁接① Project Ladder = 你的「作品集项目菜单」（最有价值）

Hub 的 11 级项目阶梯，大半正好能套在你已有的 Gate / J11 上——本来就要做这些关卡，按「可运行 + README + 失败记录」的成品标准交付即可：

| Hub 阶梯 | 对应本路线任务 | 定位 |
| --- | --- | --- |
| L1 计算器 Agent | T3-02 计算器工具 | 已有 |
| L2 Web 研究 Agent | 阶段4 A4-Gate | 已 PASS 的手写 Agent Loop 证据，不再演化成第二个研究项目 |
| L3 PDF 问答 Agent | 阶段6 工程文档 RAG + FastAPI；若被选为 `product_flagship` 再接 Vue | 只借鉴文档导入模式；旗舰一采用公开/脱敏工程资料与可定位引用 |
| L4 代码审查 Agent | 额外可选 | 可使用 Python 项目或通用 Git diff 做代码审查场景；不引入第二套后端技术栈 |
| L9 多 Agent 写作 | S-04 / D7-02 / G8 | 只借鉴协作拓扑；真实证据放进故障诊断项目，并与单 Agent 对照 |
| L11 生产级 Harness | 阶段10 + J11-05 可观测 | 给最强旗舰补齐生产能力，不另起作品集④ |

### 嫁接② Stage 0 两篇必读 + 心法清单（阶段4 入门时读）

- [Anthropic《Building effective agents》](https://www.anthropic.com/engineering/building-effective-agents)、[OpenAI 实用 agent 指南](https://openai.com/business/guides-and-resources/a-practical-guide-to-building-ai-agents/)——尤其「**什么时候不该用 agent**」，应用岗面试高频。
- Learning Principles 当贯穿全程的检查清单：先做再深读、小而可靠胜过炫 demo、增加 Agent 复杂度前先定义最小验收与失败案例、工具用严格 schema、E10 前只记录排错所需的步骤/工具/错误/耗时、危险操作留人工确认；完整 eval 与 tracing 到 E10/J11 再系统建设。

### 嫁接③ README 当「到点查的索引」

到某阶段时瞄一眼 Hub 对应 Stage 的资料/论文/开源项目补充（如 RAG 阶段看它 Stage 2 项目表），**当字典查、不当作业做**。

### 了解即可、别陷进去

- 钻 Claude Code / OpenClaw harness 内部（Hub Stage 3、阶梯 L6/L7、Claude Code Study Path）：偏基础设施、非应用岗主路，且与可选的 `H5-01` 单链路源码追踪重复；只在真实 debug 需要时选一条。
- Stage 6 浏览器/电脑操作 Agent：有余力的加分项，不在主线。
- A2A / ACP 协议：知道「干嘛的」即可；MCP 阶段9 已覆盖。

## 八、一句话原则

资料不缺，关键是「按当前依赖读取 + 动手 + 验证 + 沉淀」。稳定概念优先用 `repos/` 中文资料建立直觉；API、框架、协议、安全、部署与评估必须在开始任务当天核对官方文档。按第四节补工程层，**不为收集而收集，也不拿旧教程替代当前规范。**

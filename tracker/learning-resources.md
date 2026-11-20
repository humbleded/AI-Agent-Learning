# 学习资料导航与依赖顺序

## 一、够不够用？结论先说

- **现有概念教材足够，甚至偏多；生产工程资料必须以任务启动时的官方文档为主。** `repos/` 里的书和课程负责解释原理，FastAPI/Pydantic/SQLAlchemy/Redis/LangGraph/MCP/评估/安全等快速变化内容在开始任务当天核对官方文档，不能只照本地旧示例。
- **原路线真正偏薄的是 Python Agent 后端、生产 RAG、可恢复执行、持续评估、安全和 CI/CD。** A4 后按 `G8-00 → R6/BE5/B0 → pgvector 与 RAG 对照 → FastAPI/SSE 工程补齐 → durable G8 → BE5/R6 Gate → 多 Agent 对照与 G8-Gate → 长期 Memory → MCP → 评估 → 产品化与 FINAL` 补齐；当前已授权的统一界面/HTTP 小切片先连接可运行成果，完整工程知识仍在两个真实项目产生依赖时学习，不先完整上完一套孤立后端课。
- **知识库只保存正式、稳定的沉淀。** 当前结构、既有页面和同步规则必须在实际同步前读取 `D:\AI-Knowledge`；不在本资料页复制会过期的文件数量或日期快照。

2026-09-07 再次分页核查本人 `humbleded` 的 8 个 Star 与 0 个 Watch 仓库。具体版本、章节、许可和任务用途保留在 [2026-09-05 GitHub 收藏资料映射](../resources/github-starred-learning-map-2026-09-05.md)；本次新读的学习建议、版本和采用理由见 [2026-09-07 学习方法评审](../resources/learning-method-review-2026-09-07.md)。每个当前知识单元选择一份概念主线，必要时加一个解决实际缺口的补充片段；官方 API 用于校准。收藏不自动变成整书必读或新框架课程。

## 二、你已有的核心资料（都在 repos/，离线可用）

| 资料 | 位置 | 用途 | 语言 |
| --- | --- | --- | --- |
| Hello-Agents 全书（16 章） | `repos/hello-agents/docs/chapterX/第X章*.md` | Agent 主教材：原理 / 范式 / 框架 / 记忆 / RAG / 上下文 / 评估 / 项目 | 中（另有英文版） |
| Hello-Agents 配套代码 | `repos/hello-agents/code/chapterX/` | 每章可运行示例 | 中注释 |
| HelloAgents 框架源码（指定分支） | `repos/HelloAgents-feature-branch-1/hello_agents/` | H5-01 可选单链路源码追踪对象 | — |
| HuggingFace Agents Course（中文版） | `repos/agents-course/units/zh-CN/` | 工具/动作/观察、function calling、LangGraph、Agentic RAG、评估 | 中 |
| Agentic Design Patterns（21 章 + 附录） | `repos/agentic-design-patterns/bilingual/`（中英）`/chapters/`（英） | 阶段 7 设计模式主资料；MCP/RAG/Guardrails/评估都有 | 中英对照 |
| Agent Learning Hub 路线图 | `repos/Agent-Learning-Hub/README.md` | 现代生产视角的 todo / Project Ladder / 官方资料索引 | 中 |

> Hello-Agents 第 9 章《上下文工程》对应已有 S-03 证据；第 12 章用于评估。第 13–16 章的项目只在当前两个旗舰出现具体问题时选读，不复制成阶段 10 的第三个项目。目录章数描述的是现有本地副本，远端更新以资料映射与任务启动时核验为准。

**额外推荐（中文实战，按需读取）：[llm-universe｜动手学大模型应用开发](https://github.com/datawhalechina/llm-universe)**（Datawhale，[在线阅读](https://datawhalechina.github.io/llm-universe/)）

- 是什么：面向小白、**项目导向**的中文教程，带你从零搭一个「个人知识库助手」(RAG)。覆盖：调用大模型 API（含国内模型）、Prompt、Embedding 与向量库、用 LangChain 搭检索问答链、Streamlit 部署、评估。
- 怎么用：当 **阶段 2（Prompt）和阶段 6（RAG）的中文实战补充**最合适；阶段 1 也能参考它「调用 API」一节（讲国产模型，和你用 DeepSeek 对得上）；部署部分呼应 J11。
- 定位提醒：Hello-Agents 用于原理，llm-universe 只补当前任务需要的文档处理/检索示例。旧 SDK、模型参数、Embedding 和 LangChain 链式接口不能直接迁移；逐项对照当前官方文档与已装版本，模型调用沿用项目已验证的真实 DeepSeek 路径。它的 Streamlit/Azure/其他框架示例不改变 Python/FastAPI + Vue 主线。

## 三、按当前依赖的资料导航（先读什么 → 再读什么 → 动手）

资料优先级：**当前官方文档/规范校准 → 中文教材建立直觉 → 参考代码对照 → 当前项目落地**。CSDN、知乎、视频和旧课程只能作辅助，不能作为版本字段、认证、安全和生产配置的事实源。

核验来源的优先级不等于课堂叙述顺序：概念课仍先用已选中文片段讲清原理，再看当前 API。官方链接发生重定向时记录最终页面与实际范围，不因导航换了产品名称就换课程主框架。2026-09-05 实际发现旧 LangChain Retrieval 路径跳到 `deepagents/retrieval`，`langgraph/durable-execution` 跳到 `langgraph/persistence`；保留其中相关内容，分别限定为 RAG 架构与持久化，不自动加入 Deep Agents 全套课程。

2026-09-08 用户明确要求后续项目统一使用 LangChain 现成组件 + LangGraph 显式应用流程，包括文件读取。两旗舰共享框架组合，分别保留 RAG 与可恢复工作流的业务和验收重点；已有 G8-00 基础图证据直接迁移，不重学节点/边。API、SQL、认证、配置和测试继续使用各自专业库，应用核心可以脱离 HTTP 单独运行；没有合适现成集成时只补必要适配。具体当前组件版本与范围见下方官方源码切片。

同日按用户授权已建立唯一集成产品 `product_flagship=agent_workbench`：一个 Vue 应用与共享 FastAPI 入口承载两个业务及后续实际完成的 Memory、MCP、评估和工具能力，不为每个历史脚本机械建页面。直接从 [工作台启动与数据流说明](../code/agent_workbench/README.md) 查看当前功能、运行和验证方法；[统一工作台选型记录](../resources/unified-workbench-review-2026-09-08.md) 保存 Vue 官方工程 + Element Plus 的采用依据、候选比较、固定来源及官方 Vue AI 接法的适用边界，[第三方来源声明](../code/agent_workbench/THIRD_PARTY_NOTICES.md) 保存实际模板与依赖许可。工作台先连接已 PASS 的故障诊断核心与真实步骤输出；样本预览由助手准备，RAG G3 导入仍由用户完成，未实现时明确未就绪。助手搭建不计学习 PASS；BE5/J11 保留完整标准并复用后续实际形成的独立证据。J11-02 再冻结发布范围和默认展示业务 `default_showcase`，不二选一排除另一业务的前端、上线或共享观测。

英文资料采用渐进式训练：阶段 0–3 以中文建立直觉；阶段 4–5 保留英文原始标题、参数名与报错，让用户自己定位关键段落；从 BE5 起，短篇英文官方文档先由用户提取 2–3 条事实，卡住时再逐段翻译，不再默认整篇代译。

- **阶段 0 Python**：廖雪峰对应小节 → CS50P 对应 Week → 写 `code/stage0/` 练习；是否完成只读 `progress.md`。
- **阶段 1 大模型 API**：OpenAI Quickstart → Text Generation / 流式文档 → DeepLearning.AI《Building Systems with ChatGPT API》对应小节 → 写 L1 代码。
- **阶段 2 Prompt/结构化**：DeepLearning.AI《Prompt Engineering for Developers》Guidelines → OpenAI Prompt Engineering + Structured Outputs → 配合 **HA 第 9 章上下文工程（S-03）** → 写 PR2 代码。
- **阶段 3 工具调用**：HF 中文 unit1 `tools/actions/observations` → HF `bonus-unit1` function calling → OpenAI Function Calling → 读 `HA code/chapter4` 工具代码 → 写 T3。
- **阶段 4 Agent 原理**：HF unit1 `what-are-agents` → HA 第 1–4 章 → ADP 第 4/5/6 章（Reflection/Tool Use/Planning）→ 跑 `HA code/chapter4` 的 ReAct/Plan/Reflection。
- **G8-00 LangGraph 入门（课程位置阶段 4.5）**：当前官方 Graph API → StateGraph/state/node/edge/条件路由/tool/stream/test → 在新的“故障诊断与变更评审 Agent”业务中重建控制流；复用 A4 已 PASS 的控制原则，不复制 A4 的 research-agent 题目，也暂不读 persistence/interrupt/resume。编号属于后续 LangGraph 旗舰，不代表阶段 5～7 被跳过。
- **阶段 5 框架源码（可选）**：只有真实调用链阻塞时才沿一个入口追到 Agent/LLM/Tool/Message 并重建一个关键行为；不按目录通读、不阻塞 G8/R6。
- **R6-01 → BE5-01**：先用 Hello-Agents 第 8 章 §8.3.1（1）（2）及 §8.3.2 的两流程说明讲清 RAG 为什么需要、“先查资料再带资料回答”、资料准备与查询生成两阶段；当前官方 Retrieval 的引言/From retrieval to RAG/2-step RAG 用于校准，不展开发展史或完整向量检索。再用具体场景说明文档从哪里来、导入后能看到什么；按授权固定最小设计，用现成 LangChain Loader 经最小 LangGraph 读入一份 Markdown/TXT，通过既有工作台展示真实 Document 正文与来源，之后逐步接入处理/切分节点，补 PDF、去重和增量文档状态。当前统一界面/HTTP 连接与用户 G3 实作分别记录，不重置检查点；随后在同一项目补结构、日志、测试、lint 与类型检查，两个 ID 分别验收。已有 RAG 入门与 G8-00 证据直接承接；没有整体理解证据时，不能把组件示例当作已经掌握整体流程。
- **R6-02 本地检索切片 → R6-03 最小问答切片**：在同一旗舰先讲 embedding/top-k，验证真实可用的本地模型或服务，并优先使用 LangChain 对应集成，不能假定 DeepSeek 聊天接口提供 embedding。沿用导入图建立索引，再用查询图连接检索、模型上下文整理和真实 DeepSeek 回答，完成带出处的固定两步回答和无答案例；不在每次提问时重新读入与索引所有资料。只记局部证据，尚未完成的任务保持 DOING；具体接力统一见 weekly-plan。
- **B0-01 → B0-03 → B0-04 → B0-Gate → BE5-04**：再补命令行/进程/日志、SQL 和 Docker；B0-03 保留最小 SQLite 练习，B0-04/Gate 复用同一 Compose/CLI，再迁入旗舰。通过工程基础 Gate 后学习 SQLAlchemy/Alembic/PostgreSQL/pgvector；async driver 前仍即时补 await/连接生命周期，不能倒置这些前置。
- **R6-02 剩余标准/S-02 → R6-03 剩余标准/S-06**：把已有本地检索迁移到 PostgreSQL + pgvector，完成 exact/HNSW、filter、关键词/hybrid、rerank 与 Recall@k/MRR；在同一查询流程中比较固定两步与 LangChain Agentic 检索路径，明确图节点与 Agent 各控制哪些步骤，完成完整引用/拒答和失败分层，再判断 Prompt、RAG、微调怎样选。复用已有产物与证据，挂载任务分别写回状态。
- **BE5-02/03**：复用工作台已有 FastAPI 入口与两个独立业务路由，读取早期 HTTP/界面的独立证据，按缺口补齐 asyncio、Pydantic、HTTP/SSE、超时、取消、并发和接口测试；两个 LangChain + LangGraph 核心始终可脱离 HTTP 独立运行，不重建两套产品服务，也不把助手的早期连接当作完整验收。
- **G8-01 → G8-02 → G8-03**：LangGraph 官方 persistence/interrupts/durable execution/testing 为主线 → checkpoint/thread、PostgreSQL checkpointer、进程恢复、HITL 与副作用幂等；SQLite 只能作临时学习步骤，最终持久化证据使用 PostgreSQL。这里只说明与长期 Memory 的边界，不等待 D7。
- **BE5-05 → BE5-Gate → R6-Gate**：Redis、后台任务、认证、负载、CI、Docker 与 smoke 先完成共同后端 Gate，再完成工程文档 RAG 旗舰 Gate；不让后续 G8-Gate 倒补前置工程能力。
- **D7-01 → D7-02 → S-04 → G8-Gate**：先按 D7-01 的 ADP 第 1–3 章，将已有项目中的串联、路由、并行证据用于适用条件和取舍回顾，只补未证明的判断；再读取 D7-02 的多 Agent 取舍切片，在同一数据集保留单 Agent baseline，验证受控协作是否有净收益。G8-Gate 在既有统一 Vue/FastAPI 工作台中验证持久恢复、HITL、幂等、评估和可观察状态；新增组件再按需审查，完整前端能力在 J11-03 复核时承认此前独立证据，只补缺口。
- **D7-03 → D7-Gate**：按 2026-09-08 用户要求，把工作/情景/语义/感知四类记忆和真实图片/音频记忆接入工程文档助手既有 LangGraph 流程，优先复用 LangChain/LangGraph 组件，补齐具体业务的长期生命周期与安全规则，比较无记忆/仅文本/完整配置。再复用前面已完成的模式取舍证据做设计模式验收；不另起玩具或平行编排、不重读已证明的 D7-01 内容。
- **阶段 9 MCP**：最新 MCP 官方 specification/SDK 为主线（server capabilities、transport、authorization、安全）→ HA/ADP 作中文解释和框架对照 → 写 M9。可选只读「Skills vs Tools/MCP/Subagents」辨析，不提前陷进 Skills 生态。
- **阶段 10 评估与系统设计**：LangSmith Evaluation/Observability 官方文档 → HA 第 12 章、ADP 第 19 章、HF `bonus-unit2` 辅助 → 建一套共享 Eval Harness、为两个旗舰分别接领域 dataset/adapter/指标和 baseline/regression，并完成两个项目的系统设计包；这里不提前做 FINAL，也不复制两套评估平台。
- **J11 产品化 → FINAL → 求职收口**：唯一集成产品已固定为 `agent_workbench`，J11-02 根据两个 Gate/E10 证据冻结发布范围、`default_showcase` 与质量要求，由用户最终审核。复用现有 Vue/FastAPI 补齐独立能力与产品标准，两个业务共享正式前端、公网发布链和观测入口，各自保留领域评估与回归。完成作品集组合和 S-05 综合安全收口后做 `FINAL-Gate`；之后才进入简历、面试和 `J11-Gate`。

## 四、工程化与补充资料（BE5 + S-01~S-07 + J11）

| 主题 | 挂载 | 推荐资料（优先中文 / 官方） |
| --- | --- | --- |
| Python 工程化（BE5-01） | 阶段5.5 | Python 官方 typing/dataclasses/logging；pytest、Ruff、mypy 或 pyright 官方文档；`packaging.python.org` 的 `pyproject.toml` 指南 |
| async/并发（BE5-02） | 阶段5.5 | Python `asyncio` 官方文档；httpx async、FastAPI async tests 官方文档；重点核对 timeout/cancel/TaskGroup/Semaphore |
| FastAPI/Pydantic（BE5-03） | 阶段5.5 | FastAPI 官方中文/英文；Pydantic v2 官方；Starlette/httpx 官方 SSE/测试资料，不以 CSDN 示例作主线 |
| 数据/任务（BE5-04/05） | 阶段5.5 | SQLAlchemy 2、Alembic、PostgreSQL、Redis 官方；Celery/RQ/ARQ 任选一个官方 quickstart；Locust 或 k6 官方 |
| 多厂商模型（S-01） | BE5-02 核查可用路线，FINAL-Gate 前收口 | 优先使用 LangChain 模型/provider 集成与配置边界，再查替代厂商官方文档、OpenRouter `openrouter.ai/docs` 或本地 Ollama；只为真实差异补必要适配。真实凭据/运行条件不足时记录缺口，不阻塞当前 G8/R6 与 J11 产品化；完整 PASS 仍要求真实第二 provider，不用 mock 代替 |
| Provider 韧性与复合故障（BE5-02/FINAL） | 阶段5.5 起 | HTTP `Retry-After`/429 语义、Python `asyncio`/httpx 官方文档；重点练指数退避+jitter、可重试分类、取消传播、fallback、配额/成本上限和 fault injection，不把无限重试当可靠性 |
| 生产向量检索（S-02） | 阶段6 | pgvector 官方为主；PostgreSQL full-text/BM25 方案、Qdrant/Milvus 官方按 JD 对照；RAGAS/LangSmith 评估官方资料 |
| 上下文工程（S-03） | 阶段2/4 | **HA 第 9 章（已有）**；Anthropic《Building effective agents》（Hub 里有链接） |
| 多 Agent（S-04/G8） | G8 单 Agent baseline 后、D7-02 评审 | [LangChain Multi-agent 官方概览](https://docs.langchain.com/oss/python/langchain/multi-agent)；[Subagents](https://docs.langchain.com/oss/python/langchain/multi-agent/subagents)；ADP 第 7 章辅助。重点是何时不需要多 Agent、context engineering、带类型约束的角色交接格式、共享/私有 state、停止/预算/升级与单 Agent 对照；不默认采用 supervisor helper 库 |
| 四类记忆与图片/音频 Memory（D7-03/FINAL） | 前置见 weekly-plan；在工程文档助手内分 Session 实现 | [Hello-Agents 第八章](../repos/hello-agents/docs/chapter8/第八章%20记忆与检索.md) §8.1.3、§8.2.1、§8.2.3–§8.2.5 负责架构、生命周期、管理器及四类实现；[LangGraph Memory](https://docs.langchain.com/oss/python/langgraph/add-memory) 与 [Persistence](https://docs.langchain.com/oss/python/langgraph/persistence) 在任务启动时校准状态/存储接口及长期记忆/执行恢复边界，向工程文档助手既有图增加记忆步骤。优先使用合适的 LangChain/LangGraph 组件，四类业务规则与缺少的媒体能力补必要适配，不引入教材的另一套编排。PostgreSQL/pgvector 沿用；图片/音频模型、转写、中文支持、许可证及官方 API 在实际实现时选定核验。结合 OWASP Memory & Context Poisoning 完成来源/隔离/删除/污染与三配置对照，具体标准见 D7-03 |
| Guardrails / 注入（S-05） | R6/D7/M9/J11 分段挂载，FINAL 前收口 | OWASP Top 10 for LLM/Agentic Applications 与 Threats and Mitigations（主线）；MCP Security Best Practices；ADP 第 18 章辅助 |
| 微调 vs RAG（S-06） | 阶段6/10 | 概念为主：搜「RAG vs 微调 选型」；HA 第 8 章相关讨论 |
| FastAPI 服务化（J11-02） | 阶段11 | 复用 BE5 官方资料与 `agent_workbench/api`；根据两个 Gate/E10 证据冻结集成产品的发布范围、default_showcase 与质量，再重点查认证、部署、SSE、取消、health/readiness、API 文档和负载测试。两个业务共享入口，不重新学入门或建设第二套产品服务 |
| Vue + 流式（J11-03） | 当前授权切片逐步积累，阶段11 完整验收 | 复用 `agent_workbench/web` 的统一 Vue 应用及上述选型/来源记录，先核对已有独立证据，再补组件、状态、异步请求、浏览器调试、SSE、认证、错误处理和前后端边界的真实解释/修改。新增组件按需审查，助手搭建不计 PASS。按缺口读取 Vue 官方文档和 MDN `EventSource` / `fetch` 流式资料；不因默认展示业务不同重建或排除另一业务页面 |
| Docker 部署（J11-04） | 阶段11 | **B0-04 已有 Docker 中文文档 + 黑马视频**；强化 `agent_workbench` 唯一公网发布链，发布范围内两个业务共同交付；上线平台 Railway `docs.railway.app` 或 Render `render.com/docs` |
| 可观测/评估（E10/J11-05） | 阶段10/11 | E10 用一套共享评估基础设施服务两个领域 adapter；J11-05 为 `agent_workbench` 建统一线上 tracing/告警入口，以业务模块区分运行与指标，保留两个领域各自回归。资料使用 LangSmith Evaluation/Observability 官方或 Langfuse 官方、OpenTelemetry GenAI conventions、代码 evaluator + LLM-as-judge + baseline/regression |
| MCP（M9） | 阶段9 | `modelcontextprotocol.io/specification` 最新 revision 与官方 SDK；重点看 STDIO/Streamable HTTP、authorization/security，不以 HelloAgents 实现代替规范 |
| CI/CD/上线（J11-04） | 工程上线 | GitHub Actions、Docker、目标云平台官方；health/readiness、secret、non-root、smoke、回滚、备份、Locust/k6 官方 |
| 算法（J11-08） | 阶段11（W4 起启动） | **原理教材：《Hello 算法》`hello-algo.com`**（免费开源，动画图解＋Python 代码一键可跑，非科班友好）——W4 算法启动先读复杂度/数组与链表/哈希表打底，之后刷到哪个专题回头补哪章原理；刷题路线：代码随想录 `programmercarl.com`（含视频，按专题刷）＋ LeetCode 热题 100 `leetcode.cn`（题单） |
| 系统设计 / 架构论证（BE5/R6/G8/E10/J11-08） | BE5 起随旗舰 Gate 演化，J11-08 限时复述 | [AWS Well-Architected Framework](https://docs.aws.amazon.com/wellarchitected/latest/framework/welcome.html) 用于质量属性与架构取舍检查；[Google SRE Workbook：Implementing SLOs](https://sre.google/workbook/implementing-slos/) 用于 SLI/SLO 与错误预算；[Azure Well-Architected Framework](https://learn.microsoft.com/en-us/azure/well-architected/) 作可靠性、安全、成本、运维与性能的交叉清单。每次只读当前 Gate 所需小节，并落成 API/事件接收什么、返回什么及失败怎样表示的规则、数据模型、请求/数据流、容量假设、2–4 个可测 SLI/SLO、缓存/队列/同步异步取舍、降级方案与 ADR；小林 coding 与 Agent 面试题只用于 J11-08 问答补充，不作架构事实源。 |

### LangChain / LangGraph / RAG 官方源码切片

R6-01 的当前官方入口（2026-09-05 已读对应正文）：[Document loaders 的 Interface](https://docs.langchain.com/oss/python/integrations/document_loaders#interface)、[Text splitter integrations](https://docs.langchain.com/oss/python/integrations/splitters)。只覆盖读入统一文档、按长度/结构切分、metadata 和文档生命周期；具体 PDF/Markdown 依赖在实际 Session 再按文件类型核验，不从整页集成清单批量安装。

2026-09-08 S2 用户明确要求 G3 改用官方 DoclingLoader，取代同日较早的 TextLoader 选择（历史依据保留在 daily）。当时依据为 [LangChain 官方 Docling 集成](https://docs.langchain.com/oss/python/integrations/document_loaders/docling)、[langchain-docling 3.0.0 发布](https://pypi.org/project/langchain-docling/3.0.0/)、[v3.0.0 Loader 源码](https://github.com/docling-project/docling-langchain/blob/v3.0.0/langchain_docling/loader.py) 和 [Docling 2.126.0 Markdown backend](https://github.com/docling-project/docling/blob/v2.126.0/docling/backend/md_backend.py)。G3 历史切片只看 file_path、export_type、load 与 source，固定 `langchain-docling[local]==3.0.0`、`docling-slim==2.126.0`、`docling-core==2.95.0`，保留 LangChain core 1.6.1/graph 1.2.11；当时使用 `ExportType.MARKDOWN` 整篇输出，没有 encoding 参数。该选择已由 9/9 用户授权的 `DOC_CHUNKS + HybridChunker` 替代，选型与历史实现依据见 [切分对照与选择](../code/stage6/engineering_docs_rag/chunking-comparison.md)、[9/9 原始证据](../daily/2026-09-09.md) 和 [9/10 G6 记录](../daily/2026-09-10.md)。保存与目录卡资料的实际选读范围、固定版本及已完成/待实现边界见 [10/20 S1](../daily/2026-10-20.md)，当前动手起点只读 [daily-plan](daily-plan.md)；不按旧整篇输出方案续学。来源、格式与依赖实测范围按这些记录区分；组件准备不计用户 PASS。

[LangGraph Workflows and agents](https://docs.langchain.com/oss/python/langgraph/workflows-agents) 已于 2026-09-08 核验，用来校准固定流程与由模型决定步骤的区别；当前先把现成 Loader 放进最小图，后续在原图上增加处理、索引和查询节点。既有 G8-00 能力直接迁移，持久化/恢复仍按原依赖到 G8-01～03 学习，不能由一个读取节点提前判作已掌握。

以下来源只在对应知识单元真正开始时读取或浅克隆；路线修订阶段不提前创建 `repos/` 副本、未来代码或课程骨架。GitHub 星标和 trending 只用于发现线索，不能单独决定课程主线。

| 来源 | 当前路线中的用法 | 明确不采用 |
| --- | --- | --- |
| [LangChain 官方概览](https://docs.langchain.com/oss/python/langchain/overview)、[Retrieval](https://docs.langchain.com/oss/python/langchain/retrieval) | 核对当前 `create_agent`/组件边界，区分固定两步、Agentic 与 Hybrid RAG | 不把三种架构默认叠加；不把 `create_agent` 隐藏的 LangGraph runtime 当作直接掌握 StateGraph 的证据 |
| [langchain-ai/langchain](https://github.com/langchain-ai/langchain) | 查当前入口、核心抽象、错误边界和测试设计 | 不从头通读巨型仓库，不复制内部实现 |
| [rag-from-scratch](https://github.com/langchain-ai/rag-from-scratch) | 选择 indexing、retrieval、generation、query transformation 切片重建心智模型 | 不照抄旧 notebook API；执行时以官方文档和已安装版本为准 |
| [LangGraph 官方概览](https://docs.langchain.com/oss/python/langgraph/overview)、[Graph API](https://docs.langchain.com/oss/python/langgraph/graph-api)、[Persistence](https://docs.langchain.com/oss/python/langgraph/persistence)、[Interrupts](https://docs.langchain.com/oss/python/langgraph/interrupts)、[Streaming](https://docs.langchain.com/oss/python/langgraph/streaming)、[Testing](https://docs.langchain.com/oss/python/langgraph/test) | 两个旗舰的显式编排事实源；R6 迁移已有基础图，G8 再深入持久化、HITL、流式与恢复测试 | 不把 runtime 源码阅读扩成框架开发主线，不为迁移重复教授已 PASS 的图概念 |
| [langchain-ai/langgraph](https://github.com/langchain-ai/langgraph)、[langgraph-101](https://github.com/langchain-ai/langgraph-101) | 精读 101 基础和一个与 persistence/HITL 对应的 201 示例 | 不机械完成全部 notebook |
| [local-deep-researcher](https://github.com/langchain-ai/local-deep-researcher) | 只吸收来源进入 state、查询循环上限、反思次数限制和 trace 结构 | 不复制研究主题，不与 A4 重复造第三个 research agent |
| [pgvector/pgvector](https://github.com/pgvector/pgvector) | exact/HNSW、filter、迭代扫描、PostgreSQL FTS/hybrid 与数据一致性 | 不用热度替代 Recall@k/MRR、故障或迁移证据 |
| [langchain-ai/langchain-postgres](https://github.com/langchain-ai/langchain-postgres) | 核对当前 LangChain + PostgreSQL/pgvector 集成和迁移说明 | 不依赖过时 community 示例；任务开始时确认当前推荐类与版本 |
| Qdrant / Milvus 官方资料 | 目标 JD 明确要求或需要解释取舍时做短对照 | 不并行开两条完整向量数据库课程 |

只有为实际实现或 debug 而精读源码的切片，才形成以下可复核证据；普通概念小节只需记录来源、适用结论与当前题/产物，不每读一页都要求重建代码：

- 记录 URL、检查日期、commit SHA；快速变化的 API 同时记录库版本。
- 画出入口、核心 State/数据必须包含哪些字段与遵守哪些规则、主控制路径、错误边界和测试策略的源码地图。
- 用自己的最小代码重建一个关键行为，再迁移到当前项目，并由测试或 trace 证明。
- 写清一个采用的设计、一个拒绝的设计和拒绝原因。
- 已归档仓库（包括 `rag-research-agent-template`）不作为维护中的推荐主线或未来 API 承诺。R6-01 当前教学使用上述 Docling 方案；另一个由助手实现的只读知识库问答演示仍使用 TextLoader，范围与版本见 [工作台说明](../code/agent_workbench/README.md)。演示选型不能据此扩成其他旧 community 组件的默认推荐，后续扩大格式或交付范围时重新核验。

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

`repos/Agent-Learning-Hub/README.md` 是一份 Agent 学习路线图、项目阶梯和资料索引。2026-09-07 实读当前 README 后，我们判断它的粒度更适合导航和工程方向检查，不能代替新手所需的具体讲解；这是本项目的使用判断，不能说成作者明确要求已有 Python/LLM 基础。保留本路线主干，只采用下面三类材料及“小成果先运行、再深入”的组织方式；基础设施内部研究按真实需要选读，不因索引很长就扩成全部必修。

### 嫁接① Project Ladder = 你的「作品集项目菜单」（最有价值）

Hub 的 11 级项目阶梯，大半正好能套在你已有的 Gate / J11 上——本来就要做这些关卡，按「可运行 + README + 失败记录」的成品标准交付即可：

| Hub 阶梯 | 对应本路线任务 | 定位 |
| --- | --- | --- |
| L1 计算器 Agent | T3-02 计算器工具 | 已有 |
| L2 Web 研究 Agent | 阶段4 A4-Gate | 已 PASS 的手写 Agent Loop 证据，不再演化成第二个研究项目 |
| L3 PDF 问答 Agent | 阶段6 工程文档 RAG 核心，经 `agent_workbench` 的共享 FastAPI/Vue 展示 | 只借鉴文档导入模式；旗舰一采用公开/脱敏工程资料与可定位引用，能力实现后直接加入统一界面 |
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

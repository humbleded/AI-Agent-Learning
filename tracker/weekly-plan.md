# AI Agent 应用岗 · 依赖驱动内容块

本文件把课程任务按知识依赖组织成内容块。W1–W20 是兼容 tracker、历史证据和算法台账的稳定 ID，不是日历周、完成期限或学习时长；一个内容块可以跨任意数量的日期与 Session。课程状态只读 `tracker/progress.md`，当前入口只读 `tracker/daily-plan.md`。

最后路线校准：2026-08-25。

## 路线原则

- 主目标是初级/初中级 Agent 应用开发，次目标是大模型应用后端与 RAG/知识库工程，AI 全栈只作邻接优势。
- A4-Gate 已证明 Agent Loop、ReAct、Plan-and-Solve、Reflection、工具边界、停止与受控恢复；后续只迁移和组合这些能力，不换名字重复教学。
- A4 后先接触 LangGraph，再进入 LangChain/RAG；工程基础在两个真实项目需要时即时补齐，不等待完整 BE5 前置课。
- FastAPI 是两个纯 Python 核心的交付层，不是 Agent 编排框架，也不再单独创建聊天玩具。
- LangChain 与 LangGraph 可以互用组件，但两个旗舰必须分别有明确主框架、业务问题、目录、测试和 Gate 证据。
- PostgreSQL + pgvector 是向量检索主线；轻量本地索引只用于理解原理，Qdrant/Milvus 只在 JD 或架构取舍需要时短对照。
- 多 Agent 不是单 Agent 的自动升级。先建立单 Agent baseline；只有任务拆分、上下文隔离或并行专长产生可测收益时，才在 `S-04` 引入受控协作。
- checkpoint/thread state 负责一次工作流的执行状态；`D7-03` 的长期 Memory 负责跨会话事实生命周期。二者不得混称。
- H5 保持可选：只在真实框架问题需要时追一条源码路径，不阻塞主线。
- 用户会一些 Vue，前端不扩成独立主线：先做最小独立复核；真正进入界面任务时，助手可审计许可证、维护状态、依赖和安全风险后组合 GitHub 开源 Vue 骨架。若 G8-Gate 提前采用，用户当场做第三方代码最小准入审核；完整状态/SSE/认证/错误处理和亲自修改能力留到 J11-03。助手搭建不算用户独立掌握证据，也不提前克隆。J11-02 冻结唯一 `product_flagship`，不建设两套正式前端/公网产品链。

## 两个旗舰项目

| 主框架 | 项目 | 规划目录 | 需要证明的核心能力 |
| --- | --- | --- | --- |
| LangChain | 工程文档 RAG 助手 | `code/stage6/engineering_docs_rag/` | Loader/Splitter/Document/metadata、检索、固定两步 RAG、Agentic RAG、引用、权限、评估、API 与部署 |
| LangGraph | 故障诊断与变更评审 Agent | `code/stage8/incident_change_review_agent/` | 显式 State/Node/Edge、route/loop/stop、stream、checkpoint、interrupt/resume、幂等、受控多 Agent、评估与恢复 |

两个项目的交付层统一为：

```text
HTTP / SSE / Auth / Validation / 统一错误返回规则
                       │
                 Application Adapter
              ┌────────┴─────────┐
              │                  │
      LangChain RAG Core   LangGraph Workflow Core
```

## 内容块顺序

W1–W5 是已发生的历史学习块，精确任务状态和证据仍以 `progress.md` 与历史 daily 为准，不重写历史。

| 内容块 | 依赖驱动任务顺序 | 可验证产物 / 里程碑 |
| --- | --- | --- |
| W1–W3 | Python、LLM API、Prompt、结构化输出 | Python Gate、流式 CLI、结构化输出与上下文实验 |
| W4 | Tool Calling 与算法启动 | T3-Gate；算法首块 4 道新题替代无旧题的复测位 |
| W5 | Agent 基础与 A4-Gate | 手写 Agent Loop、ReAct、Plan-and-Solve、Reflection、正式 14-case Gate |
| W6 | `G8-00`（课程位置：阶段 4.5）；并行开启 `J11-01` 的证据积累与首轮岗位审计 | LangGraph 故障诊断与变更评审 Agent v1：typed state、node/edge、条件路由、工具、停止、stream、测试；这不是直接跳到完整阶段 8。岗位审计当前为 RETRY，不阻塞 G8-00，但必须在其 PASS 后、W7/R6-01 前用独立 Session 关闭 |
| W7 | `R6-01 → BE5-01`（同一项目、分别验收） | 先完成 Markdown/TXT/PDF 导入、切分、metadata、去重和文档状态，再补项目分层、日志、pytest、Ruff 与类型检查 |
| W8 | `B0-01 → B0-03 → B0-04 → B0-Gate → BE5-04 → R6-02`；联合核验 `S-02` | 从命令行/进程/日志基础进入 PostgreSQL + pgvector；migration、CRUD、tenant filter、hybrid、rerank、Recall@k/MRR |
| W9 | `R6-03 → S-06` | 同一数据集的固定两步 RAG baseline 与 Agentic RAG 对照；可定位引用、无答案拒答与失败分层；再用真实证据判断 Prompt/RAG/微调怎样选 |
| W10 | `BE5-02 → BE5-03`；`S-01` 可从 provider 边界开始但不阻塞本块 | 两个纯 Python 核心分别接 FastAPI/Pydantic/SSE；timeout、cancel、并发限制、系统出错时怎样返回结果与接口测试；Graph 的 HITL 决策接口留到 G8-03 增量实现 |
| W11 | `G8-01 → G8-02 → G8-03` | LangGraph v2：PostgreSQL 持久 checkpoint、thread 隔离、重启恢复、approve/edit/reject API、幂等副作用和故障注入 |
| W12 | `BE5-05 → BE5-Gate`；第二轮岗位审计 | Redis、后台任务、认证、重复提交、负载、CI、Docker、smoke 与生产后端 Gate；复用两个项目，不建第三个教学项目 |
| W13 | `R6-Gate`；完成 `S-05` 的 RAG/ACL/间接注入切片 | LangChain 工程文档 RAG 旗舰：完整导入/检索/问答/API/权限/评估/部署证据 |
| W14 | `D7-02 → S-04 → G8-Gate` | 先用单 Agent baseline 做多 Agent 准入判断，再完成带类型约束的交接格式、共享/私有 state、预算/停止/升级与同集对照；G8-Gate 验收 FastAPI/SSE 和可观察状态输出，可使用 curl/调试页或任务启动后引入的已审计开源 Vue 薄界面；完整 Vue 掌握仍在 J11-03 复核 |
| W15 | `D7-01 → D7-03 → D7-Gate`；完成 `S-05` 的 Memory/PII/poisoning 切片 | 复用已有项目做模式取舍；完成跨会话 Memory CRUD/TTL/provenance/delete/隔离/poisoning 与无 Memory 对照，不另建玩具 |
| W16 | `M9-01 → M9-02 → M9-03 → M9-Gate`；第三轮岗位审计 | MCP 与外部工具连接、授权、断连与审计证据；补齐 `S-05` 的 MCP 授权/恶意 server 切片 |
| W17 | `E10-01 → E10-02` | 一套共享 Eval Harness + 两个领域 adapter；两个旗舰分别完成 baseline/candidate、回归门禁和系统设计包，不复制两套评估平台 |
| W18 | `S-01（若待完成）→ J11-02 → J11-03 → J11-04 → J11-05 → S-05 正式收口` | 先冻结唯一 `product_flagship`，再为它完成产品 API、Vue、公网部署和产品级观测；另一旗舰保留可复现 API/demo、容器与 E10 评估，随后收口权限、恢复、幂等、SLO、成本、回滚与生产事故闭环 |
| W19 | `J11-01 收口 → J11-06 → FINAL-Gate → J11-07 → J11-08 → J11-Gate`；第四轮岗位审计 | 先完成作品工程化、部署和持续评估，再做综合答辩；随后收束作品集、简历、模拟面试与正式岗位证据 |
| W20 | 证据债务、算法债务、交叉复核与投递前收口 | 不新增课程主题，只闭合既有缺口并稳定投递 |

## 多 Agent 与长期 Memory 的准入边界

### `S-04` 受控多 Agent

- 先在同一故障诊断数据集上保留单 Agent baseline，再引入 supervisor/subagent、handoff 或 router 中最符合场景的一种模式。
- handoff 必须使用带类型约束的交接格式，明确输入、输出、证据引用、失败、超时和所有权；共享 state 与私有 context 分开。
- 必须有 `max_handoffs`、总 step/成本预算、停止与人工升级；worker 不能绕过工具权限和副作用确认。
- 比较任务成功、遗漏/冲突、延迟、token/成本与 trace 可诊断性。没有净收益就回退单 Agent，不因术语热度保留复杂度。

### `D7-03` 长期 Memory

- 覆盖跨会话显式写入、检索注入、更新、冲突、TTL、删除/忘记、provenance、租户隔离、PII 与 poisoning。
- PostgreSQL 是长期事实源；Redis 只作缓存。未受信工具输出或 RAG 文本不得自动晋升为长期记忆。
- 用同一数据集比较有/无 Memory 的任务成功、误记、遗漏、延迟和成本；checkpoint 的恢复证据不能冒充长期 Memory 证据。

## 算法保护项

- W4–W20 共 17 个内容块，最低累计 **52 道新题**。
- 每个内容块固定 `3 新 + 1 旧错题`；W4 因无旧题，以第 4 道新题替代。
- 算法以独立 Session 推进。债务先清：旧债未清时不启动下一完整 `3+1`；同一块跨 7 个自然日仍追加旧题复测。
- 路线重排不削减题量、复测、独立解释、复杂度或测试证据。

当前纠偏：W5 结束时没有留下 `3 新 + 1 旧` 的合格证据，`algorithm-progress.md` 已正式记为 `DEBT 4`。它不撤销 A4 课程 PASS，但下一算法 Session 必须先清 W5，清完前不启动 W6 完整配额。

## 使用与审计

- 每次 Session 读取当前任务全部关联 daily；跨日不重置题量、覆盖或上下文。
- `W6/W12/W16/W19` 做双轨岗位审计：4–6 个高工程标准标杆与恰好 10 个 `HARD_ELIGIBLE` 可投样本分开统计。
- 岗位审计债务不会阻塞同块的课程任务，但不能跨过规定的最晚收口点：当前 W6 RETRY 最晚在 `G8-00` PASS 后、`R6-01` 启动前补齐；W12 必须新建自己的快照，不能覆盖 W6 未关闭记录。
- 课程 PASS 不自动升级岗位证据。`JOB_EVIDENCE`、`FINAL-Gate`、`J11-Gate` 和投递前就绪必须经过另一工具的独立交叉复核。
- 未开始任务只在 tracker 中保留目标路径与 rubric；真正进入动手 Session 时才创建骨架。
- 每个 `progress.md` 中的独立 `TODO` 必须在主队列或“挂载任务”中有明确触发点、最晚收口点和状态写回规则；不能只把能力隐含在别的任务里。
- Gate 不得要求路线后面才首次学习的能力；若某能力是后续增量，当前任务只验收已经具备的最小接口，并把完整交付明确放到后续 ID。
- 每个内容块结束都要分别核对课程任务、挂载任务和算法 `PASS/DEBT`；其中一条未完成不能被另一条的 PASS 静默覆盖。

# AI Agent 学习总进度

表结构/规则校准：2026-09-05；各任务状态与证据日期以对应行“最近日期”为准。

状态取值：`TODO`、`DOING`、`RETRY`、`PASS`、`FAIL`。

本表是任务状态的唯一事实源，只保留状态、日期、目标产物路径和 1 句结论。详细代码检查、练习订正和易错点分别放在 `daily/`、知识库与 `tracker/weak-points.md`。

本表按稳定任务 ID 汇总，不代表从上到下的执行顺序；真实执行顺序只读 `tracker/daily-plan.md` 与 `tracker/weekly-plan.md`。例如 `G8-00` 位于课程阶段 4.5，只是沿用 LangGraph 旗舰的任务编号。

本表的 `PASS` 是课程完成状态，不等于岗位就绪；岗位能力、作品证据和 JD 差距见 `tracker/job-readiness.md`。

“代码/笔记”是计划目标路径：TODO 任务的文件可能尚未创建；只有真正进入该任务的动手或设计/实现 Session 时才即时建立当前骨架。

| 编号 | 任务 | 状态 | 最近日期 | 代码/笔记 | 批改反馈 |
| --- | --- | --- | --- | --- | --- |
| P0-01 | 环境与第一个程序 | PASS | 2026-05-27 | code/stage0/p0_01_hello.py | 已通过；详见 daily/2026-05-27.md。 |
| P0-02 | 数据类型与变量 | PASS | 2026-05-28 | code/stage0/p0_02_profile.py | 已通过；详见 daily/2026-05-28.md。 |
| P0-03 | 条件判断、模式匹配、循环 | PASS | 2026-05-28 | code/stage0/p0_03_scheduler.py | 已通过；详见 daily/2026-05-28.md。 |
| P0-04 | list、tuple、dict、set | PASS | 2026-06-02 | code/stage0/p0_04_tasks.py | 已通过；详见 daily/2026-06-02.md。 |
| P0-05 | 函数、参数、返回值 | PASS | 2026-06-09 | code/stage0/p0_05_plan_functions.py | 已通过；详见 daily/2026-06-09.md。 |
| P0-06 | 模块、第三方包、venv | PASS | 2026-06-10 | code/stage0/p0_06_env_check.py | 已通过；详见 daily/2026-06-10.md。 |
| P0-07 | 异常、调试、单元测试 | PASS | 2026-06-11 | code/stage0/p0_07_safe_divide.py | 已通过；详见 daily/2026-06-11.md。 |
| P0-08 | 文件、JSON、CSV | PASS | 2026-06-13 | code/stage0/p0_08_progress_file.py | 已通过；详见 daily/2026-06-13.md。 |
| P0-09 | HTTP 请求 | PASS | 2026-06-13 | code/stage0/p0_09_http_request.py | 已通过；详见 daily/2026-06-13.md。 |
| P0-Gate | Python 基础闯关 | PASS | 2026-06-14 | code/stage0/p0_gate_learning_log.py | 已通过；详见 daily/2026-06-14.md。 |
| B0-01 | Linux 命令行与环境 | TODO |  | notes/stage0_5/b0_01_linux_cli.md | 穿插补课项：遇到命令行、环境变量、进程、端口、日志时补。 |
| B0-02 | 网络基础与 HTTP | PASS | 2026-06-23 | code/stage0_5/b0_02_http_probe.py | 已通过；详见 daily/2026-06-23.md。 |
| B0-03 | SQL 与关系型数据库 | TODO |  | code/stage0_5/b0_03_learning_db.py | 穿插补课项：做 Memory、学习记录持久化、RAG 数据存储时补。 |
| B0-04 | Docker 与 Compose | TODO |  | code/stage0_5/docker_learning_stack/ | 穿插补课项：需要本地多服务、数据库容器、部署和日志排错时补。 |
| B0-Gate | 工程基础闯关 | TODO |  | code/stage0_5/docker_learning_stack/ | 复用 B0-04 的 Compose/CLI 补整合与故障证据；在 B0-01/03/04 完成后、BE5-04 前分别验收，不另建相似工程。 |
| L1-01 | API Key 与 SDK | PASS | 2026-06-14 | code/stage1/l1_01_first_call.py | 已通过；详见 daily/2026-06-14.md。 |
| L1-02 | 单轮问答 | PASS | 2026-06-15 | code/stage1/l1_02_ask.py | 已通过；详见 daily/2026-06-15.md。 |
| L1-03 | 多轮聊天 | PASS | 2026-06-16 | code/stage1/l1_03_chat.py | 已通过；详见 daily/2026-06-16.md。 |
| L1-04 | 流式输出 | PASS | 2026-06-17 | code/stage1/l1_04_stream_chat.py | 已通过；详见 daily/2026-06-17.md。 |
| L1-05 | 参数实验与成本意识 | PASS | 2026-06-18 | code/stage1/l1_05_params_experiment.py | 已通过；详见 daily/2026-06-18.md。 |
| L1-Gate | API 入门闯关 | PASS | 2026-06-27 | code/stage1/l1_gate_cli_chatbot.py | 已通过；详见 daily/2026-06-27.md。 |
| PR2-01 | Prompt 基础 | PASS | 2026-06-27 | code/stage2/pr2_01_prompt_cases.md | 已通过；详见 daily/2026-06-27.md。 |
| PR2-02 | 摘要与改写 | PASS | 2026-06-27 | code/stage2/pr2_02_summarizer.py | 已通过；详见 daily/2026-06-27.md。 |
| PR2-03 | 分类与路由 | PASS | 2026-06-28 | code/stage2/pr2_03_classifier.py | 已通过；详见 daily/2026-06-28.md。 |
| PR2-04 | JSON 与 Schema | PASS | 2026-06-30 | code/stage2/pr2_04_extract_json.py | 已通过；详见 daily/2026-06-30.md。 |
| PR2-Gate | 结构化输出闯关 | PASS | 2026-07-05 | code/stage2/pr2_gate_email_processor.py | 已通过；详见 daily/2026-07-05.md。 |
| T3-01 | 函数调用概念 | PASS | 2026-07-01 | notes/stage3/t3_01_function_calling.md | 已通过；详见 daily/2026-07-01.md。 |
| T3-02 | 计算器工具 | PASS | 2026-07-06 | code/stage3/t3_02_calculator_tool.py | 已通过；详见 daily/2026-07-06.md。 |
| T3-03 | 文件工具 | PASS | 2026-07-07 | code/stage3/t3_03_file_reader_tool.py | 已通过；详见 daily/2026-07-07.md。 |
| T3-04 | 外部 API 工具 | PASS | 2026-07-08 | code/stage3/t3_04_public_api_tool.py | 已通过；详见 daily/2026-07-08.md。 |
| T3-Gate | Tool Calling 闯关 | PASS | 2026-07-12 | code/stage3/t3_gate_tool_assistant.py + code/stage3/eval_cases.json | 原生三工具闭环与直接回答均真跑；`t3-gate-v2`（SHA `766649…C042F`）normal 10/10、failure 3/3、danger 1/1、holdout 3/3，详见 daily/2026-07-11.md。 |
| A4-01 | 什么是 Agent | PASS | 2026-07-09 | notes/stage4/a4_01_what_is_agent.md | 已通过；详见 daily/2026-07-09.md。 |
| A4-02 | LLM 与 Agent 基础 | PASS | 2026-07-15 | notes/stage4/a4_02_llm_agent_basics.md | 三个学习单元、12 个有效证据位及 Instruction Data/Tuning/Few-shot 独立迁移均通过；详见 daily/2026-07-14.md、daily/2026-07-15.md。 |
| A4-03 | ReAct | PASS | 2026-07-22 | code/stage4/a4_03_react_agent.py + notes/stage4/a4_03_react.md | 完整两轮轨迹可运行，15/15 边界断言通过；能解释职责、停止条件与 max_steps，详见 daily/2026-07-21.md、daily/2026-07-22.md。 |
| A4-04 | Plan-and-Solve | PASS | 2026-07-30 | code/stage4/a4_04_plan_solve_demo.py | 可运行 demo 输出计划、3 步结果、事实复盘和最终答案；39/39 聚焦边界断言通过，G1–G7 与 F1–F3 全部闭合，详见 daily/2026-07-22.md～2026-07-30.md。 |
| A4-05 | Reflection | PASS | 2026-08-04 | code/stage4/a4_05_reflection_writer.py | 初稿/反思/改进稿/同标准对比闭环可运行；39/39 确定性断言、真实 2 调用提前停止与受控坏初稿后的真实修正分支均通过，10 个语义证据闭合；详见 daily/2026-08-04.md。 |
| A4-Gate | 最小 Agent 闯关 | PASS | 2026-08-24 | code/stage4/problem-contract.md + code/stage4/a4_gate_research_summary_agent.py + code/stage4/eval_cases.json | `FINAL / PASS` 版输入输出、失败和验收规则、冻结生产源码与 V5 自包含 14-case 已闭合；唯一 RUN-5 为 normal 10/10、holdout 3/3、exact/supportedness 10/10、semantic 10/10 cases（20/20 keypoints）、failure 3/3、danger 1/1（A～K 11/11），五道 Gate 问题全部通过；共享 step/七字段日志、受控恢复、安全停止与 action-bound HITL 均由真实运行及离线 70/70、独立 85/85 + 55/55 复核支持，详见 daily/2026-08-05.md～daily/2026-08-24.md。 |
| G8-00 | LangGraph 基础工作流（课程阶段 4.5） | PASS | 2026-09-05 | code/stage8/incident_change_review_agent/ | 15 字段 typed State、7 个业务 Node、五路条件路由/回环/稳定停止与 v2 `updates` 已闭合；最终回归 12/12、真实 DeepSeek Node 链与 G1～G11 + F1 均通过，持久化/恢复仍留到 G8-01~03，详见 daily/2026-08-25.md～daily/2026-09-05.md。 |
| H5-01 | 框架源码单链路追踪（可选） | TODO |  | notes/stage5/h5_01_framework_trace.md | 只在真实调用链阻塞时追一个入口、重建一个关键行为并迁移到当前项目；不按目录通读，不阻塞 G8/R6。 |
| BE5-01 | Python 工程化基础 | TODO |  | code/stage6/engineering_docs_rag/ | 在 LangChain 工程文档 RAG 项目中建立 typing、分层、pytest/mock、Ruff、类型检查、配置与日志，不另建教学项目。 |
| BE5-02 | asyncio、并发与可靠 I/O | TODO |  | （复用两个旗舰项目） | 在两个现有 core 中验证并发上限、timeout/cancel、阻塞隔离和部分失败，不建独立教学服务。 |
| BE5-03 | FastAPI、Pydantic v2 与流式接口 | TODO |  | code/stage6/engineering_docs_rag/ + code/stage8/incident_change_review_agent/ | 作为两个纯 Python core 的 REST/SSE/认证/校验交付层；统一系统出错时返回什么及调用方怎样处理。Graph 的 approve/edit/reject 接口在 G8-03 增量完成。 |
| BE5-04 | PostgreSQL、Alembic 与 pgvector | TODO |  | code/stage6/engineering_docs_rag/ | SQLAlchemy/Alembic、async driver、pgvector、事务、幂等、tenant filter 与 migration；Redis 移到 BE5-05。 |
| BE5-05 | Redis、后台任务、认证与负载测试 | TODO |  | （复用两个旗舰项目） | Redis 缓存/限流/幂等/任务状态、后台任务、最小授权、取消/重试、p50/p95 压测。 |
| BE5-Gate | Agent 后端工程闯关 | TODO |  | （复用两个旗舰项目） | 对两个既有项目共用的后端能力做一次可维护、可测试、可并发、可持久化、可部署验证，不建第三个业务项目。 |
| R6-01 | LangChain 文档导入与切分 | DOING | 2026-10-20 | code/stage6/engineering_docs_rag/ | 已有文档导入/切分、编号及片段保存/读回证据；10/20新增目录卡身份键与单条保存/读回，按实际带读、示例和独立实现程度记录。新旧关联汇总、更新/删除及其余完整验收标准尚未闭合，助手适配不计独立PASS。原答与执行结果见9/7–9/10关联daily和[10/20 S1](../daily/2026-10-20.md)；当前动手起点只读[daily-plan](daily-plan.md)。 |
| R6-02 | Embedding、pgvector 与检索 | TODO |  | code/stage6/engineering_docs_rag/ | BE5-01 后先做真实本地 embedding/top-k 切片；BE5-04 后完成 pgvector、exact/HNSW、filter、hybrid、rerank 与指标。提前切片不自动 PASS。 |
| R6-03 | 固定两步 RAG、Agentic RAG 与引用 | TODO |  | code/stage6/engineering_docs_rag/ | 本地检索后先做带出处的固定两步最小问答；R6-02 完整验收后补同集架构对照、引用/拒答及失败分层。提前切片不自动 PASS。 |
| R6-Gate | LangChain 工程文档 RAG 闯关 | TODO |  | code/stage6/engineering_docs_rag/ | 用公开/脱敏工程文档、业务验收指标和生产 RAG 链路形成旗舰一。 |
| D7-01 | 基础编排模式 | TODO |  | notes/stage7/d7_01_orchestration_patterns.md | 在已有旗舰上判断 chaining、routing、parallelization 的适用边界，并用一条真实 trace/测试说明采用或拒绝。 |
| D7-02 | Agent 核心模式与协作边界 | TODO |  | code/stage8/incident_change_review_agent/ | 复用 A4 已 PASS 概念；S-04 在 G8 项目以单 Agent baseline、带类型约束的角色交接和对照证据落地。 |
| D7-03 | 可靠性、长期 Memory 与工程模式 | TODO |  | code/stage6/engineering_docs_rag/ | 2026-09-08 用户授权扩展：在工程文档助手实现四类记忆及真实图片/音频存储与检索，覆盖生命周期、隔离/poisoning 和有/无记忆对照；已纳入规划，尚未启动。 |
| D7-Gate | 设计模式闯关 | TODO |  | notes/stage7/d7_gate_architecture_review.md | 实施一个真实模式变更并用同一 eval 比较质量、延迟、成本和失败分组。 |
| G8-01 | 持久化与恢复边界 | TODO |  | notes/stage8/g8_01_durable_boundary.md | 区分 checkpoint/thread state、长期 Memory、replay 与副作用幂等。 |
| G8-02 | 持久化 Graph | TODO |  | code/stage8/incident_change_review_agent/ | 在 G8-00 项目增量使用持久化 checkpointer、thread 隔离并验证进程重启恢复。 |
| G8-03 | 故障诊断、变更评审与 HITL | TODO |  | code/stage8/incident_change_review_agent/ | transient/non-retryable/user-fixable 分支、interrupt approve/edit/reject、幂等键与 replay 故障验证。 |
| G8-Gate | LangGraph 故障诊断与变更评审闯关 | TODO |  | code/stage8/incident_change_review_agent/ | 持久工作流、重启恢复、HITL、受控多 Agent、trace、版本化评估、FastAPI/SSE；复用统一agent_workbench的Vue/FastAPI验证真实状态、工具和人工处理入口，已有独立证据直接复用，完整Vue能力仍在J11-03验收。 |
| M9-01 | MCP 概念 | TODO |  | notes/stage9/m9_01_mcp_concepts.md | 能用当前官方规范解释 host/client/server、capability、transport 与安全边界。 |
| M9-02 | 本地 MCP Server | TODO |  | code/stage9/m9_02_local_mcp_server.py | 用官方 SDK 实现可发现、可审计且拒绝越权参数/路径的 STDIO server。 |
| M9-03 | Agent 调 MCP | TODO |  | code/stage9/m9_03_agent_mcp_client.py | 真实调用 MCP 工具，并解释 STDIO/HTTP、认证、scope/audience 与失败反馈。 |
| M9-Gate | MCP 闯关 | TODO |  | code/stage9/m9_gate_file_summary_agent.py | 验收发现、权限、断连恢复、审计、恶意 server 边界和冻结分组门槛的版本化评估。 |
| E10-01 | Agent 评估 | TODO |  | notes/stage10/e10_01_agent_evaluation.md | 用一套共享评估基础设施和两个领域 adapter，分别为 RAG/G8 旗舰建立 dataset/evaluator/baseline-candidate、trace 与 CI 回归门禁。 |
| E10-02 | 综合项目设计 | TODO |  | notes/stage10/e10_02_project_design.md + notes/stage10/e10_02_system_design.md | 为两个现有旗舰分别把评估结论映射到架构、容量/SLO、安全、成本与 ADR，不新建第三个项目。 |
| FINAL-Gate | 综合项目答辩 | TODO |  | notes/stage10/final_defense.md | 执行位置在 J11-02~06 与 S-05 收口后；使用已冻结并产品化的 `product_flagship` 完成上线、评估、恢复和事故答辩。 |
| J11-01 | GitHub 与工程习惯 | TODO |  | （整理 code/ 现有项目） | 随真实项目持续积累；W6 起纳入正式 README/branch/PR/CI/review/revert 证据记录，最晚在 J11-06 前收口。 |
| J11-02 | Agent 后端服务（FastAPI） | TODO |  | code/agent_workbench/api/ + 两个旗舰核心 | 唯一集成产品已固定为 `agent_workbench`；根据 Gate/E10 证据冻结发布范围、默认展示业务 `default_showcase` 与质量要求，强化共享认证、持久化、观测和产品 API。 |
| J11-03 | Vue 前端界面 | TODO |  | code/agent_workbench/web/ | 复用现有三模式界面与真实独立证据，补齐用户解释/修改组件状态、SSE、认证、错误处理和密钥边界的能力；两个业务共用一套正式前端，助手搭建不计用户 PASS。 |
| J11-04 | CI/CD、容器化与上线强化 | TODO |  | （复用 `product_flagship`） | BE5-Gate 先完成最小 CI/Docker/测试部署/smoke；本任务只为冻结的产品旗舰补 secret、告警、负载、备份、回滚和公网 demo。 |
| J11-05 | 可观测与持续评估 | TODO |  | agent_workbench + 两个领域 E10 adapter | 共享 tracing、线上失败回灌和产品级告警；两个业务分别维持版本化 eval/baseline/regression，不复制观测栈。 |
| J11-06 | 作品集组合（2 旗舰 + 1 小项目） | TODO |  | notes/stage11/j11_06_portfolio.md | 一个集成产品展示 RAG 与可控 Agent 两个领域旗舰，另保留结构化抽取小项目；两业务共用正式前端/公网发布链，分别提供可复现 API、容器与领域评估，不重复计算共享实现。 |
| J11-07 | 简历与岗位匹配 | TODO |  | notes/stage11/j11_07_resume.md | W6/W12/W16/W19 做“京东/腾讯等大厂标杆 + 10 条真实可投样本”双轨审计；用 Python/FastAPI + Vue Agent 作品证明可迁移工程能力。 |
| J11-08 | 面试准备 | TODO |  | notes/stage11/j11_08_interview.md | 中等算法 + 系统设计 + AI 八股。 |
| J11-Gate | 求职冲刺关 | TODO |  | notes/stage11/j11_06_portfolio.md + notes/stage11/j11_07_resume.md + notes/stage11/j11_08_interview.md | 公开作品集 + 简历 + 面试自测；核心岗位能力与旗舰证据须按明确集合交叉复核。 |
| S-01 | 多厂商模型切换 | TODO |  | （BE5-02 核查路线、FINAL-Gate 前完成） | 先抽 provider 边界，再接第二个真实 provider；外部条件不足记录缺口，不阻塞 G8/R6 与 J11 产品化，FINAL 门槛保留。 |
| S-02 | 生产向量检索 | TODO |  | （与 R6-02/R6-Gate 共用产物） | pgvector 主线；hybrid、rerank、权限 filter、增量更新与检索指标；正式检查必须单独写回本 ID。 |
| S-03 | 上下文工程 | PASS | 2026-06-30 | notes/stage2/s03_context_engineering.md ＋ code/stage2/s03_context_experiment.py | 已通过；详见 daily/2026-06-30.md。 |
| S-04 | 受控多 Agent 协作 | TODO |  | code/stage8/incident_change_review_agent/ | 在单 Agent baseline 后完成最小候选实验，验证交接格式、共享/私有 state、预算/停止/升级与质量-成本取舍；默认采用取决于实测净收益，无净收益则保留单 Agent。 |
| S-05 | 安全与 Guardrails | TODO |  | code/（复用 R6/D7/M9/J11 产物） | A4 已完成最小基线；R6、D7-03、M9 分别补 RAG/Memory/MCP 安全切片，J11 综合攻击回归后再正式判定。 |
| S-06 | 微调 vs RAG vs Prompt 判断 | TODO |  | notes/stage6/s06_prompt_rag_finetune_decision.md | 在 R6-03 同集对照后用真实项目案例完成三选一判断；不动手微调。 |

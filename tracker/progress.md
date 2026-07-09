# AI Agent 学习总进度

最后校准：2026-07-10。

状态取值：`TODO`、`DOING`、`RETRY`、`PASS`、`FAIL`。

本表是任务状态的唯一事实源，只保留状态、日期、目标产物路径和 1 句结论。详细代码检查、练习订正和易错点分别放在 `daily/`、知识库与 `tracker/weak-points.md`。

“代码/笔记”是计划目标路径：TODO 任务的文件可能尚未创建；代码骨架只在任务开始动手或 Gate 设计准备时即时建立。

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
| B0-Gate | 工程基础闯关 | TODO |  | code/stage0_5/b0_gate_local_stack/ | 项目化整合关卡；不阻塞 L1，建议在 L1-Gate/基础 Tool Calling 后或做 Memory/RAG/部署前完成。 |
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
| T3-Gate | Tool Calling 闯关 | TODO |  | code/stage3/t3_gate_tool_assistant.py | 当前硬检查点；即时骨架已按真实 `tools/tool_calls → 客户端执行 → role="tool" 回填 → 最终回答` 重建，待用户动手完成并跑 14 条评估。 |
| A4-01 | 什么是 Agent | PASS | 2026-07-09 | notes/stage4/a4_01_what_is_agent.md | 已通过；详见 daily/2026-07-09.md。 |
| A4-02 | LLM 与 Agent 基础 | TODO |  |  |  |
| A4-03 | ReAct | TODO |  |  |  |
| A4-04 | Plan-and-Solve | TODO |  |  |  |
| A4-05 | Reflection | TODO |  |  |  |
| A4-Gate | 最小 Agent 闯关 | TODO |  |  |  |
| H5-01 | 跑通指定分支 | TODO |  |  |  |
| H5-02 | Core 层阅读 | TODO |  |  |  |
| H5-03 | Agents 层阅读 | TODO |  |  |  |
| H5-04 | Tools 层阅读与新增工具 | TODO |  |  |  |
| H5-05 | Memory、Context、Protocol 阅读 | TODO |  |  |  |
| H5-Gate | 源码学习闯关 | TODO |  |  |  |
| R6-01 | 文档读取与切分 | TODO |  |  |  |
| R6-02 | Embedding 与检索 | TODO |  |  |  |
| R6-03 | 带引用问答 | TODO |  |  |  |
| R6-Gate | RAG 闯关 | TODO |  |  |  |
| D7-01 | 基础编排模式 | TODO |  |  |  |
| D7-02 | Agent 核心模式 | TODO |  |  |  |
| D7-03 | 可靠性与工程模式 | TODO |  |  |  |
| D7-Gate | 设计模式闯关 | TODO |  |  |  |
| G8-01 | LangGraph 适用场景 | TODO |  |  |  |
| G8-02 | 第一个 Graph | TODO |  |  |  |
| G8-03 | 文档分析 Agent | TODO |  |  |  |
| G8-Gate | LangGraph 闯关 | TODO |  |  |  |
| M9-01 | MCP 概念 | TODO |  |  |  |
| M9-02 | 本地 MCP Server | TODO |  |  |  |
| M9-03 | Agent 调 MCP | TODO |  |  |  |
| M9-Gate | MCP 闯关 | TODO |  |  |  |
| E10-01 | Agent 评估 | TODO |  |  |  |
| E10-02 | 综合项目设计 | TODO |  |  |  |
| FINAL-Gate | 综合项目答辩 | TODO |  |  |  |
| J11-01 | GitHub 与工程习惯 | TODO |  | （整理 code/ 现有项目） | 应用岗作品集阶段；从阶段 3 起并行启动。 |
| J11-02 | Agent 后端服务（FastAPI） | TODO |  | code/stage11/j11_02_agent_api/ | 顺带补 async 和接口设计，弥补后端基础。 |
| J11-03 | Vue 前端界面 | TODO |  | code/stage11/j11_03_agent_web/ | 发挥你现有 Vue 优势，做差异化作品。 |
| J11-04 | 容器化与上线 | TODO |  | code/stage11/j11_04_deploy/ | 依赖 B0-04 Docker；产出公网可点开的 demo 链接。 |
| J11-05 | 可观测与评估 | TODO |  | code/stage11/j11_05_observability/ | 接 LangSmith/Langfuse，呼应阶段 10 评估。 |
| J11-06 | 作品集组合（2 旗舰 + 1 小项目） | TODO |  | notes/stage11/j11_06_portfolio.md | RAG 与可控 Agent 两个旗舰持续演化，另保留一个结构化抽取小项目；至少一个旗舰带前端并部署。 |
| J11-07 | 简历与岗位匹配 | TODO |  | notes/stage11/j11_07_resume.md | 把 .NET+Vue+AI 串成「全栈 AI 应用落地」故事。 |
| J11-08 | 面试准备 | TODO |  | notes/stage11/j11_08_interview.md | 中等算法 + 系统设计 + AI 八股。 |
| J11-Gate | 求职冲刺关 | TODO |  |  | 公开作品集 + 简历 + 面试自测。 |
| S-01 | 多厂商模型切换 | TODO |  | （A4-Gate 后、J11-02 前） | 先抽 provider 边界，再接第二个真实 provider；不与 T3-Gate 挤在同一周末。 |
| S-02 | 真实向量数据库 | TODO |  | （挂阶段6 R6-02） | 补充项：Chroma/FAISS 或 pgvector，别手写相似度。 |
| S-03 | 上下文工程 | PASS | 2026-06-30 | notes/stage2/s03_context_engineering.md ＋ code/stage2/s03_context_experiment.py | 已通过；详见 daily/2026-06-30.md。 |
| S-04 | 多 Agent 动手 | TODO |  | code/（挂阶段7 D7-02） | 补充项：supervisor+worker 最小协作 demo。 |
| S-05 | 安全与 Guardrails | TODO |  | code/（A4-Gate 基线 + W11 强化） | A4-Gate 先做白名单/限步/人工确认，W11 再补注入、越权与攻击测试。 |
| S-06 | 微调 vs RAG vs Prompt 判断 | TODO |  | notes/（挂阶段6 或 10） | 补充项：概念笔记，应用岗不动手微调但要会判断。 |
| S-07 | async 基础与异步接口 | TODO |  | code/（J11-02 前，W9） | async/await、FastAPI 异步接口与 SSE；J11-02 前完成。 |
| S-08 | Microsoft Agent Framework 扫读（可选） | TODO |  | notes/（挂求职期 W16） | 以 Microsoft Agent Framework 为主，Semantic Kernel/AutoGen 仅作迁移背景；形成 .NET 团队 Agent 选型表达。 |

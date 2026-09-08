# 2026-09-07 学习项目审查与修复记录

本次按用户“阅读整个项目，补全项目中所有的漏洞，然后给一份现在学习的路径流程”的要求，检查学习路线、任务标准、学习记录、笔记、自有代码与 Codex 学习规则，并修复已确认的问题。完整学习路径集中在 [weekly-plan 的流程图与内容块表](../tracker/weekly-plan.md#学习路径总览)，当前继续点集中在 [daily-plan](../tracker/daily-plan.md#当前执行入口)。

本记录是一次有日期的项目维护检查，不是课程完整验收。助手修改的代码和笔记不计为用户独立能力，历史作答、评分及已通过任务保留。仓库在本次开始前已有未提交修改，本次在其基础上继续维护，未提交或推送 Git。

## 检查范围与方法

- 对自有文件做目录与链接检查，核对课程任务编号、状态、产物路径和任务入口；逐段审查主 tracker 的任务与通过标准，以及路线、当前起点、岗位、算法和工作场景规则。
- 审查全部 14 份任务 notes 与 2 份模拟面试记录中的稳定结论，并回到相应代码、历史 daily 和官方资料核对；原始回答与订正过程不按今天的结论重写。
- 对 67 份日期 daily 与 TEMPLATE 的任务状态、未覆盖项、补救项和接力位置做全量扫描；旧等待项按后续证据核对是否收口，没有重审全部历史长答案。逐篇读取 resources 中 5 份既有自有 Markdown，区分当前生效规则与有日期的历史报告。
- 对 46 个自有 Python 文件做语法检查，并审查已有程序的输入、文件读写、调用失败与结果判断。对确认的故障做内存注入和系统临时目录验证；复用现有 Graph 测试、算法断言与离线演示。
- 检查 3 个 Codex 学习 skill 的分工和现行规则；本次只修改正式检查 skill 中残留的 Claude 读取入口。
- 第三方学习仓库作为资料源按课程引用核对，不把第三方全部源码、依赖包或未完成课程当作已经做完全面安全审计。本次未重跑未修改的 T3/A4 全部真实模型 Gate，因此验证结论限于下面列出的范围。

## 已修正的学习安排

| 原问题 | 修复后的行为 | 主要文件 |
| --- | --- | --- |
| RAG 全貌没有落实成组件学习前的明确前置 | 先讲清为什么查资料、资料准备与提问回答两个阶段、找到的片段怎样进入模型输入；再学读取和切分。承认当天已经补讲的内容，理解核对与原 G2 合并，不重开课程或加一套题 | [任务标准](../tracker/ai-agent-learning-tracker.md)、[当前入口](../tracker/daily-plan.md)、[资料](../tracker/learning-resources.md) |
| 编排方式的取舍放在多 Agent 之后，容易先选复杂实现再补判断 | 在多 Agent 前完成 D7-01 的串联、分支、并行取舍回顾，复用已有 Graph 和并发证据；长期 Memory 在项目、数据库和恢复能力之后学习 | [完整路线](../tracker/weekly-plan.md) |
| README 和岗位导航复制旧顺序，容易与主路线分叉 | 两处统一指向 weekly 的完整顺序和 daily 的当前起点 | [README](../README.md)、[岗位导航](../tracker/job-readiness.md) |
| 通用判定容易把“还没学完”判成整项 RETRY，Gate 列表容易被误读为固定课序 | 明确局部检查只记本次证据、缺口与起点；完整交付验收才判整项 PASS/RETRY/FAIL。技术前置以 weekly 明确的依赖为准 | [任务标准](../tracker/ai-agent-learning-tracker.md)、[README](../README.md) |
| BE5-Gate 后的早期求职材料检查只写在 J11-07 正文，执行路线容易漏掉 | W12 增加局部材料校准，复用 2–3 条已核清硬门槛岗位；不重复创建正式岗位审计，也不提前通过 J11-07 | [完整路线及挂载规则](../tracker/weekly-plan.md) |
| 正式检查 skill 残留读取 Claude 项目记忆的入口 | 改为读取 AGENTS，并明确遵守 Codex-only 的维护范围 | Codex 的 ai-agent-learning-review/SKILL.md |
| 根目录缺少已有程序的环境复现入口，配置模板仍用旧模型名 | 补虚拟环境、现有依赖与离线测试命令；模板默认模型与当前课程一致 | [README](../README.md)、[配置模板](../.env.example) |

独立复查确认：Mermaid 总览、精确任务表、当前接力点和任务标准一致，没有发现尚未解决的硬性循环依赖。44 个尚未完成任务均有任务标准与路线或挂载入口；可选源码追踪保留按真实问题触发。

## 已修正的运行问题

| 文件 | 确认的问题与修复 |
| --- | --- |
| [P0 学习记录程序](../code/stage0/p0_gate_learning_log.py) | 损坏、不可读或结构错误的 JSON 曾可能被当成空记录后覆盖；现在明确停止并保留原文件。非法分钟数不触发保存 |
| [HTTP 探测](../code/stage0_5/b0_02_http_probe.py) | 畸形网址解析可能直接异常；现在显示非法 URL。成功按 2xx 判断，304 不再误报成功 |
| [流式聊天](../code/stage1/l1_04_stream_chat.py) | 失败信息可能只作为返回值而没有显示；现在打印错误。缺 key 明确说明没有调用模型，移除自动模拟回复，同时保留原返回类型以兼容已有 CLI |
| [温度实验](../code/stage1/l1_05_params_experiment.py) | 当前思考模式默认开启且忽略 temperature；现在显式关闭思考再比较三种温度。对应说明同步订正 |
| [上下文实验](../code/stage2/s03_context_experiment.py) | 原结论直接写死；现在根据实际估算计算最小值并允许并列，姓名保留另行检查。摘要失败、为空或类型错误时停止比较，保留条数必须为正整数；区分上下文估算和真实 API 消耗 |

温度实验的维护依据是 [DeepSeek 当前思考模式说明](https://api-docs.deepseek.com/guides/thinking_mode/)，核验日期为 2026-09-07。这只说明当前运行方式需要修正，不反推历史实验当时的响应无效。

## 已订正的笔记与实验记录

- [提示词笔记](../notes/stage2/pr2_01_prompt_notes.md)：样例和分步提示是引导方法，不保证格式或正确性；模型系列名不代表其中所有模型采用相同训练方式。
- [结构化输出预读](../notes/stage2/pr2_04_structured_output_preview.md)：结构约束不等于事实正确；区分普通 JSON 回答、严格结构输出和工具参数的功能范围；补齐截断处理，并将任务字段数改回实际的 5 个。[OpenAI 结构化输出](https://developers.openai.com/api/docs/guides/structured-outputs)、[DeepSeek JSON Output](https://api-docs.deepseek.com/guides/json_mode/) 与 [Tool Calls](https://api-docs.deepseek.com/guides/tool_calls/) 支持这些边界。
- [文件工具笔记](../notes/stage3/t3_03_file_reader_tool.md)与[公共 API 工具笔记](../notes/stage3/t3_04_public_api_tool.md)：按实际代码说明已处理的异常；当前 API 的工具消息需把 Python 字典转换为 JSON 字符串。Requests 的 timeout 不是整次下载的总时限，缓慢持续传输可能超过该数值。[Requests 官方说明](https://requests.readthedocs.io/en/latest/user/quickstart/#timeouts)
- [Agent 基础](../notes/stage4/a4_01_what_is_agent.md)：JSON 的键名和字符串值用双引号；数字、布尔值、null、数组与对象按各自类型表示。
- [模型与 Agent 流程](../notes/stage4/a4_02_llm_agent_basics.md)：托管模型 API 中，客户端提交 messages，模型服务负责模板格式化与分词；“本地保存了历史”与“本次请求带上了历史”分开说明。
- [8 月 5 日面试记录](../interviews/2026-08-05-agent-模拟面试.md)与[8 月 6 日面试记录](../interviews/2026-08-06-agent-模拟面试.md)：订正每次写文件都要再次确认、调用工具后必然还需模型一轮等过度概括；补清短期记忆也可以保存到数据库，长期记忆关注跨会话信息，RAG 是查找并利用资料回答，两者可配合。原答、反馈和评分保留。[LangChain Memory 概览](https://docs.langchain.com/oss/python/concepts/memory)
- [温度实验记录](../code/stage1/l1_05_params_experiment.md)：从真实历史 daily 补回已有用量和回答摘要；完整旧响应没有保存的部分明确标注，未补造输出。将历史结果与本次维护验证分开。
- [复习台账](../tracker/weak-points.md)的 WP-05：同步订正仍会用于出题的“低温=可复现”说法，改为较低温度通常更集中，但不保证输出完全一致或答案正确；历史复测日期、间隔档和下次复习日期保持原样。

## 验证结果

精确的可复跑命令与决定性输出统一保存在 [当天维护记录](../daily/2026-09-07.md#全项目审查与维护验证)，本报告只汇总结论：

- 自有 Python 语法检查 46/46；2 个 eval JSON 可解析；现有 Graph 自动测试 12/12；5 份算法脚本内置断言通过。
- 5 处代码修复的详细离线校验：P0 14 项、HTTP 8 项网址/请求路径与 3 项状态、流式 3 项、温度参数 3 项、上下文实验 25 项通过；主审另行复跑五组关键回归通过。只使用内存 mock 和自动清理的临时目录，没有新增一次性 runner。
- 三组温度真实请求都有非空回答和 usage；真实流式请求返回“测试成功”；真实摘要请求完成三方案比较。后两项及温度请求均由助手执行，不新增用户课程证据。
- 原有 T3/A4 沙箱 fixture 与评估文件声明一致；A4-03、A4-04 离线演示可运行。完整 T3/A4 真实评估未在本轮重跑。
- Codex 正式检查 skill 的结构校验通过；修改的 Markdown 和代码通过 git diff --check；本地 Markdown 文件链接已检查。
- AGENTS、progress、algorithm-progress、work-scenario-coverage 与本次开始时的内容逐一比较一致；weak-points 只订正 WP-05 的助手说明，状态和排期不变。两份面试记录的 66 行原答、反馈和判定与原 Git 记录一致。

## 仍需实际学习和补齐的事项

截至本次检查，课程为 35 个 PASS、1 个 DOING、43 个 TODO；这只是本报告的检查快照，后续状态仍以 [progress](../tracker/progress.md) 为准。

1. 当前 R6-01 已补讲 RAG 全貌，但还没有有效独立理解证据。下次先核对“找到的资料怎样进入模型输入”，再接回来源与版本、第一份文档读取。不要因为本次审查而跳过。
2. 跨会话长期 Memory 仍是 D7-03 的后续学习内容。已有历史消息、裁剪、摘要和一次任务内反思不能代替它的写入、更新、遗忘与隔离证据。
3. W5 算法尚余 DEBT 3；独立算法 Session 先补这些欠项。路线重排不扣减配额，也不因跨日增加配额。
4. W6 岗位审计的合格样本仍未齐，保持独立补齐；不因此阻塞技术课，也不能生成正式匹配率或自动升级岗位就绪。
5. 当前复习台账保留 WP-28 的后续独立检验；其状态与复习规则没有被此次文件修复覆盖，按后续合适的练习目标继续。
6. 本轮未完成任何未来项目要求。完整问答、长期记忆、线上安全、部署、系统评估和求职答辩都要在对应任务实际完成后验收。

下一次学习继续位置以 [当前执行入口](../tracker/daily-plan.md#当前执行入口) 为准。全路径只维护在 [weekly-plan](../tracker/weekly-plan.md#学习路径总览)，本报告不再保存第二条任务队列。


## 2026-09-08 提交前验证与知识库同步

用户在独立侧边会话授权“提交并推送，同步更新知识库”。本次复跑 `daily/2026-09-07.md` 的五组离线关键故障检查（PowerShell：`$checkLines = Get-Content -LiteralPath daily/2026-09-07.md; $checkLines[290..361] | .\.venv\Scripts\python.exe -`），损坏日志保留、非法 URL/非 2xx、流式异常可见、温度参数传递及摘要失败/比较五项全部通过。另用 `ast.parse` 检查自有 46 个 Python 文件；现有 `python -m pytest code/stage8/incident_change_review_agent/test_incident_graph.py -q` 为 12 passed，`git -c core.safecrlf=false diff --check` 通过。未重跑真实模型，前一日真实调用结果仍按原日期引用。

知识库按此次明确授权更新过期课程入口、带学偏好和已有知识订正，保留 R6-01 DOING、算法余量和岗位欠项；助手维护不计用户独立学习证据。没有启动新教学、修改复习排期或生成新的课程判定。知识库具体更新和链接验证记录在 `D:\AI-Knowledge\log.md`。

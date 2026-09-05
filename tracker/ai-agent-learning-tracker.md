# AI Agent 开发学习追踪清单

根目录：`C:\Users\26823\Desktop\AI-Agent-Learning`

本清单用于按知识单元与 Session 记录学习、提交代码、回答检查题，并由批改者（Claude / Codex 均可）判定是否通过。日期只用于原始证据归档，不构成每日课表。

## 文件夹约定

| 路径                                   | 用途                           |
| -------------------------------------- | ------------------------------ |
| `tracker/ai-agent-learning-tracker.md` | 总学习路线、任务清单、通过标准 |
| `tracker/progress.md`                  | 总进度表，只记录每项状态       |
| `tracker/job-readiness.md`             | 岗位能力、作品证据与 JD 差距   |
| `tracker/work-scenario-coverage.md`    | 工作场景、复合故障与实跑证据   |
| `daily/`                               | 按日期保存 Session 原始证据    |
| `code/`                                | 你自己写的练习代码             |
| `notes/`                               | 视频、文档、源码阅读笔记       |
| `repos/`                               | 参考仓库源码                   |
| `resources/`                           | 补充资料、截图、PDF、运行记录  |

代码文件采用“即时建骨架”：未来任务只在本清单中预留目标路径，不提前批量生成 `code/` 文件。真正启动当前任务的动手/设计 Session 时，先核对本单元资料、当前官方 API 和已 PASS 代码，再创建只含 TODO 的当前任务骨架；PASS 后保留用户完成的代码。

已放入 `repos/` 的参考仓库：

- `hello-agents`：Datawhale《从零开始构建智能体》
- `Agent-Learning-Hub`：Datawhale Agent 学习路线资料库
- `HelloAgents-feature-branch-1`：jjyaoao/HelloAgents 指定分支
- `agentic-design-patterns`：Agentic Design Patterns 中文/双语内容
- `agents-course`：Hugging Face Agents Course

## 判定规则

- `PASS`：课程任务的代码能运行，能独立解释核心概念，问答没有明显漏洞。
- `RETRY`：代码能跑但理解不稳，或答案不完整，需要补答。
- `FAIL`：代码未跑通，概念混淆，或明显复制材料但不能解释。

课程 `PASS` 只表示当前学习任务达标，不自动等于“已经达到招聘要求”。岗位能力与作品证据另记在 `tracker/job-readiness.md`：只有当能力已经落到可复现项目、测试/评估结果、工程说明和独立讲解时，才可以升为 `JOB_EVIDENCE`；能在限时面试或现场任务中稳定完成，才升为 `INTERVIEW_READY`。

强制顺序关卡没通过时，不进入后续同类阶段：

- `P0-Gate` Python 基础闯关
- `L1-Gate` 大模型 API 闯关
- `T3-Gate` Tool Calling 闯关
- `A4-Gate` 最小 Agent 闯关
- `BE5-Gate` Agent 后端工程闯关
- `R6-Gate` RAG 闯关
- `G8-Gate` LangGraph 闯关
- `M9-Gate` MCP 闯关
- `FINAL-Gate` 综合项目答辩

从 `T3-Gate` 起，需要评估集的 Gate 通过标准额外包含固定评估集、分项结果与失败案例：`T3/A4-Gate` 至少 14 条，`R6/G8/M9-Gate` 至少 20 条，`FINAL-Gate` 至少 30 条。这里的最低条数是**回归/调试集与未揭示 holdout 的总数**。不能只报一句总通过率；按任务拆分检索、答案、工具选择、参数、轨迹、安全、延迟或成本等指标。

所有 Gate 都使用“最小但充分”的证据：接口接收什么、返回什么以及状态怎样变化的确定性规则，优先进入项目现有 pytest/接口/集成/安全测试；非确定性模型质量才使用 eval cases。一次性核验使用直接执行、内存 mock/spy 或清理后的系统临时文件，结果写当天 `daily`。只有会持续保护真实代码、支持领域对照实验，或 task rubric 明确要求的测试、fixture、指标脚本、CI 和评估工程才长期保留。E10 前不得仅因案例数量创建通用 runner、独立 baseline 管理、报告归档或 tracing 平台；但本原则不得删除 BE5 以后真实软件所需的自动测试，也不得替代 E10、J11 产品化与 FINAL-Gate 明确要求的 eval、CI、负载和恢复证据。

`T3-Gate` 只长期保留自包含的 `code/stage3/eval_cases.json`，正式复核者直接执行全部案例并把数据集版本/SHA、逐类/逐组件结果、holdout、失败 ID、安全证据和精确命令写入当天 `daily`；不保留专用 runner、独立 baseline 或原始运行报告。重要修改与上一次同版本 daily 结果或 Git 历史比较。

Gate 不能只有“题数”，还必须在第一次调参前写清验收阈值。确定性单元/接口/迁移测试必须全部通过；危险操作、越权、跨租户和敏感信息泄漏等关键安全案例必须 100% 拦截；非确定性任务按 Gate 预先定义任务成功、检索、引用、延迟和成本阈值。`T3/A4-Gate` 的 holdout 至少占总集 20% 且不少于 3 条，`R6/G8/M9/FINAL-Gate` 至少占 20% 且不少于 5 条；holdout 不能参与 prompt、规则或参数调优，若为修复而揭示就转入回归集并补充新的未揭示案例，不能看完结果后再倒推合格线。

实际工作问题以 `tracker/work-scenario-coverage.md` 为事实源。`T3-Gate` 先完成一个受控复合危险输入；从 `A4-Gate` 起，编码、Gate、项目练习至少包含一个绑定真实代码/日志/trace/失败测试的工作场景；从 `BE5` 起至少包含一个同时叠加 2–4 类问题的复合事故。一个事故可以覆盖多个类别，但必须分别记录“止损/隔离 → 复现 → 根因定位 → 修复 → 回归/恢复 → 取舍”，纯口述不能冒充可执行证据。

从 A4-Gate 开始记录最小结构化日志（模型/工具/耗时/错误/步数），危险或不可逆工具必须有人为确认点；完整 tracing、离线/在线评估与回归门禁留到 E10/J11-05。进入作品集的 Gate 还必须满足：无真实密钥、依赖可复现、README 可从零运行、自动测试通过、至少有 lint/type-check 中一项、保留架构图和失败复盘。

从 `BE5-Gate` 起，每个旗舰 Gate 还要维护一份逐步演化的系统设计包：API/事件接收什么、返回什么以及必须遵守的规则，数据模型，请求/数据流，容量假设，2–4 个可测 SLI/SLO，缓存/队列/同步异步取舍，关键 ADR，失败/降级路径和成本边界。不要等到 W19 才第一次练系统设计。

工程基础不再作为进入阶段 1 的整块前置。`B0-01` 到 `B0-04` 改为穿插补课项：P0-Gate 通过后可以先进入 `L1` 大模型 API；后续遇到环境、HTTP、数据库、Docker、Memory、RAG、本地服务部署时，再补对应 B0 项。

`B0-Gate` 改为项目化整合关卡：在需要本地多服务、数据库持久化、Docker Compose、长期 Memory/RAG 或可部署 Agent 项目前完成，不再卡住第一次进入 L1/API。

## Session 证据格式

`daily/TEMPLATE.md` 是唯一字段模板，本文件不复制第二套 schema。新建或续写 `daily/YYYY-MM-DD.md` 时必须遵守：

- 不记录计划或实际学习时长；daily 是按日期归档的证据日志，不是课表。
- 同日多任务先维护 Session/任务索引；跨日续学链接并读取该任务全部前序 daily，按“本 Session 已覆盖/未覆盖、任务总剩余、下次 Session 起点”接力。
- 即时与正式证据 ID 使用 `<任务ID>-G1`、`<任务ID>-F1` 等任务命名空间。
- 通用批改、工程验证、复习、算法与岗位候选字段均以模板为准。

说明：批改者检查时会根据代码/产物位置实际运行代码并验证结果。只有当代码不是默认入口、需要特殊参数、需要先启动服务或配置环境变量时，才填写“运行提示”。

`本 Session 进度小结`、`任务总进度小结`、`对问题/不确定点的解释`、`问答点评与补充` 由批改者（Claude / Codex 均可）检查后填写。普通任务的 `复核判定` 留空；任何 `JOB_EVIDENCE` 升级、`FINAL-Gate`、`J11-Gate` 结论和正式投递前检查都必须由**另一个**工具交叉复核（Claude 主审 → Codex 复核，反之亦然），未复核只能记录“候选证据”。固定口令 **「交叉复核 <任务/Gate ID>」** 启动复核；复核者必须先独立读取 rubric、全部关联 daily 与真实产物并形成临时结论，之后才能读取主审结论。主审与复核者的同意项、分歧项、各自证据和处理必须记录；分歧未解决不得升级岗位证据或正式投递就绪。

---

## Loop / Harness 术语与既有任务映射

本节只给既有能力建立共同语言，不新增任务 ID、课程阶段、顺序关卡或 PASS rubric。“Loop Engineering”仍是较新的术语，不同来源会与 Agent Engineering、Harness Engineering 或 Durable Workflow 重叠；术语新不代表底层能力新。

```text
一次运行内部
Agent Loop
  └─ Inner Loop Engineering
     state → decide → act/tool → observe → retry/recover → stop
                       │
一次可靠运行的外部环境 │
Agent Harness ─────────┘
model/tool adapters · permissions/sandbox · context/state
budgets/retries · logging/tracing · tests · human control
        │
        ├─ Harness Engineering：构建、测试、演化上述环境
        └─ Eval Harness：dataset + evaluator + baseline/candidate + regression

跨多次运行
Outer Loop Engineering
discover → schedule → execute → independent verify
   → persist/escalate → stop
        │
        └─ Improvement Loop
           trace/failure → eval → change → regression → deploy
```

| 术语 | 本路线中的含义 | 已有承载位置 | 边界 |
| --- | --- | --- | --- |
| Agent Loop | 一次运行内部的“判断—行动—观察—停止”控制循环 | A4 已 PASS；G8 只把它显式图化 | 不换名重教，不因使用框架重复判 PASS |
| Agent Harness | 支撑一次可靠运行的外部环境，而非单一框架名 | A4 工具/安全/预算；BE5 服务环境；G8 persistence/HITL；M9 connector；J11 产品化与 FINAL-Gate 部署/协作 | LangChain 可提供高层 Agent Harness，但会用 `create_agent` 不自动证明理解底层 StateGraph |
| Harness Engineering | 构建、测试、迭代 Harness 的工程工作 | BE5、G8、E10、J11、FINAL | 不新增“完整无人值守编码工厂”主线 |
| Inner Loop Engineering | 一次运行内的 state、action、route、stop、retry、recovery | A4、G8-00、G8-01~03 | 已 PASS 的 Agent Loop 原理只迁移，不重复定义教学 |
| Outer Loop Engineering | 跨运行的发现、调度、执行、独立验证、持久状态、升级和停止 | G8 durable state、S-04 handoff、J11 CI/automation、FINAL 恢复演练 | worktree/subagent/automation 只在真实项目需要时使用，不另开平台课程 |
| Eval Harness | 为质量判断和回归提供专门证据的子系统 | T3/A4/R6/G8 的局部 eval；E10 系统化；J11 产品化与 FINAL-Gate 接 CI | 早期紧凑评估不能冒充 E10 的版本化 harness |
| Improvement Loop | 生产 trace/故障进入 eval，再改进、回归和部署 | E10、J11-05、J11-04、FINAL | 必须有失败样例回灌和门禁证据，不以“持续优化”口号代替 |

术语准入规则：若新词只是上述组合关系或别名，优先映射到 A4、G8、BE5、E10、J11、FINAL；只有现有任务无法承载、存在明确岗位/生产价值且能形成可执行证据时，才考虑新增任务。

---

# 阶段 0：Python 与开发环境

目标：能写基础 Python 脚本，能读写文件，能安装包，能调用 HTTP API。

主资料：

- 廖雪峰 Python：简介、安装、第一个程序、Python 基础、函数、模块、错误调试、IO、requests、venv
- CS50P：Week 0 到 Week 6，后续 Week 7-9 作为补充
- 视频：CS50P 官方课程、freeCodeCamp Python、B站黑马 Python

## P0-01 环境与第一个程序

资料：

- 廖雪峰：`简介`、`安装Python`、`第一个Python程序`、`输入和输出`
- CS50P：Week 0 `Functions, Variables`

要做：

- 在 `code/stage0/p0_01_hello.py` 写一个输入姓名和学习目标的脚本。
- 能在终端运行。

问答：

1. Python 解释器的作用是什么？
2. `print()` 和 `input()` 分别做什么？
3. 终端运行 `.py` 文件和在交互模式里敲代码有什么区别？

通过标准：

- 能运行脚本。
- 能解释输入、处理、输出三步。

## P0-02 数据类型与变量

资料：

- 廖雪峰：`数据类型和变量`、`字符串和编码`
- CS50P：Week 0

要做：

- 写 `code/stage0/p0_02_profile.py`，保存姓名、年龄、学习目标、每日学习分钟数，输出一段学习档案。

问答：

1. 字符串、整数、浮点数、布尔值分别适合表示什么？
2. 变量名为什么要有意义？
3. f-string 解决什么问题？

通过标准：

- 能正确使用至少 4 种数据类型。
- 能解释变量和值的关系。

## P0-03 条件判断、模式匹配、循环

资料：

- 廖雪峰：`条件判断`、`模式匹配`、`循环`
- CS50P：Week 1 `Conditionals`，Week 2 `Loops`

要做：

- 写 `code/stage0/p0_03_scheduler.py`。
- 输入今天学习时长，判断：不足、合格、优秀。
- 用循环打印未来 7 天学习计划。

问答：

1. `if/elif/else` 适合解决什么问题？
2. `match/case` 和多层 `elif` 相比有什么优势？
3. `for` 和 `while` 的典型使用场景有什么不同？

通过标准：

- 判断逻辑正确。
- 能解释为什么不用复制 7 次 `print()`。

## P0-04 list、tuple、dict、set

资料：

- 廖雪峰：`使用list和tuple`、`使用dict和set`
- CS50P：Week 2

要做：

- 写 `code/stage0/p0_04_tasks.py`。
- 用 list 保存任务，用 dict 保存任务状态，用 set 去重标签。

问答：

1. list 和 dict 的最大区别是什么？
2. 为什么 dict 适合保存结构化状态？
3. set 去重的代价是什么？

通过标准：

- 能增删改查任务。
- 能解释不同容器的选择理由。

## P0-05 函数、参数、返回值

资料：

- 廖雪峰：`函数`、`调用函数`、`定义函数`、`函数的参数`
- CS50P：Week 0，Week 5 `Unit Tests`

要做：

- 写 `code/stage0/p0_05_plan_functions.py`。
- 实现 `make_plan(goal, days)` 和 `score_answer(answer)`。
- 先独立实现；批改时再把参考实现作为示范写入反馈。

问答：

1. 为什么要把代码封装成函数？
2. `return` 和 `print` 有什么区别？
3. 如何判断一个函数是否职责过多？

通过标准：

- 至少两个函数被主程序调用。
- 能说明输入、处理、输出。

## P0-06 模块、第三方包、venv

资料：

- 廖雪峰：`模块`、`安装第三方模块`、`venv`
- CS50P：Week 4 `Libraries`

要做：

- 建立虚拟环境。
- 安装 `python-dotenv` 和 `requests`。
- 写 `code/stage0/p0_06_env_check.py` 读取 `.env` 中的测试变量。

问答：

1. 为什么项目要用虚拟环境？
2. `pip install` 安装到哪里？
3. 为什么 API Key 不应该写死在代码里？

通过标准：

- 能激活虚拟环境并运行脚本。
- `.env` 不提交真实密钥。

## P0-07 异常、调试、单元测试

资料：

- 廖雪峰：`错误处理`、`调试`、`单元测试`
- CS50P：Week 3 `Exceptions`，Week 5 `Unit Tests`

要做：

- 写 `code/stage0/p0_07_safe_divide.py`。
- 处理除零、非数字输入。
- 写最少 3 个测试样例。

问答：

1. try/except 捕获的是什么？
2. 为什么不能什么异常都直接忽略？
3. 单元测试的价值是什么？

通过标准：

- 错误输入不会让程序崩溃。
- 测试覆盖正常和异常场景。

## P0-08 文件、JSON、CSV

资料：

- 廖雪峰：`文件读写`、`操作文件和目录`、`序列化`
- CS50P：Week 6 `File I/O`

要做：

- 写 `code/stage0/p0_08_progress_file.py`。
- 读取任务文本，写入 `resources/stage0_progress.json`。

问答：

1. 文本文件和 JSON 文件分别适合保存什么？
2. 文件路径错误时如何定位？
3. 读写文件为什么要考虑编码？

通过标准：

- 能读写文件。
- JSON 能被 Python 重新解析。

## P0-09 HTTP 请求

资料：

- 廖雪峰：`requests`、`HTTP协议简介`
- CS50P：Week 4

要做：

- 写 `code/stage0/p0_09_http_request.py`。
- 请求一个公开 API，打印状态码、headers、JSON。

问答：

1. URL、headers、body 分别是什么？
2. 200、401、404、500 大概代表什么？
3. 为什么调用 API 必须处理失败和超时？

通过标准：

- 能成功请求 API。
- 能解释一次 HTTP 调用的过程。

## P0-Gate Python 基础闯关

任务：

- 写 `code/stage0/p0_gate_learning_log.py`。
- 输入今日学习记录，保存到 JSON。
- 支持查看最近 7 条记录。
- 有错误处理。

必须回答：

1. 你的数据结构为什么这样设计？
2. 哪些地方用了函数？
3. 如果文件不存在，你怎么处理？
4. 这个脚本后续如何变成学习追踪系统的一部分？

通过标准：

- 代码可运行。
- 能解释核心代码。
- 有 3 条以上测试记录。

---

# 阶段 0.5：工程基础（穿插补课：Linux / 网络 / 数据库 / Docker）

目标：补齐 AI Agent 项目运行、排错、存储和部署所需的最小工程基础。暂时不加入 Web 前端基础，也不把工程基础当成进入 Agent 前必须整块学完的前置课程。

安排原则：

- P0-Gate 通过后，优先进入阶段 1：大模型 API 入门。
- 工程基础按项目触发点补齐，保持“边做 Agent、边补工程基础”。
- 每次只补当前任务需要的最小内容，避免把 Linux、网络、数据库、Docker 学成独立长线。
- `B0-Gate` 作为后续本地栈整合关卡，不阻塞 L1/API、Prompt、基础 Tool Calling 的学习。

触发点：

- 学 `P0-06`、`L1-01` 时补环境变量、venv、包安装和命令行。
- 学 `P0-09`、`L1`、`T3-04` 时补 HTTP、DNS、headers、status code、timeout。
- 做 Memory、RAG、学习记录持久化时补 SQL、SQLite/PostgreSQL。
- 做本地多服务、部署、日志排错时补 Docker、Compose、volume、network。

主资料：

- 阅读规则：中文文档负责主讲与理解；命令参数、版本、安全和部署配置在任务启动时用当前官方文档校准，中文镜像/译文不代替官方依据；视频只补操作演示。英文定位按项目渐进规则执行，不为核验资料提前展开未来课程。
- Linux 文档：[Linux 命令大全（菜鸟教程）](https://www.runoob.com/linux/linux-command-manual.html)、[Missing Semester 中文版：Shell 入门](https://missing-semester-cn.github.io/2026/course-shell/)
- Linux 视频：[MIT Missing Semester 2020 - B站双语字幕](https://www.bilibili.com/video/BV1w7411477L/)、[Shell Tools and Scripting - B站双语字幕](https://www.bilibili.com/video/BV1xa4y1g7sZ/)
- 网络文档：[MDN HTTP 概述（中文）](https://developer.mozilla.org/zh-CN/docs/Web/HTTP/Guides/Overview)、[MDN HTTP 标头（中文）](https://developer.mozilla.org/zh-CN/docs/Web/HTTP/Reference/Headers)、[MDN HTTP 响应状态码（中文）](https://developer.mozilla.org/zh-CN/docs/Web/HTTP/Reference/Status)、[Cloudflare：什么是 DNS（中文）](https://www.cloudflare.com/zh-cn/learning/dns/what-is-dns/)
- 网络视频：[湖科大教书匠《计算机网络微课堂》](https://www.bilibili.com/list/ml962700202?bvid=BV1c4411d7jb&oid=64605483)、[Computer Networking: A Top-Down Approach - YouTube playlist](https://www.youtube.com/playlist?list=PL1ya5dD_M8uX-BLUF1FEvUNsYWQL5_l0O)
- 数据库文档：[SQLite 5 分钟快速上手（中文）](https://sqlite.ac.cn/quickstart.html)、[SQLite SQL 语言（中文）](https://sqlite.ac.cn/lang.html)、[PostgreSQL 教程（中文）](https://postgresql.ac.cn/docs/current/tutorial.html)、[PostgreSQL SQL 语言（中文）](https://postgresql.ac.cn/docs/current/sql.html)
- 数据库视频：[尚硅谷 MySQL 入门到高级](https://www.bilibili.com/video/BV1eC4y1M7c3/)、[CMU Intro to Database Systems - YouTube](https://www.youtube.com/@CMUDatabaseGroup)
- Docker 文档：[Docker 中文文档：Docker 教程](https://dockerdocs.xuanyuan.me/)、[Docker Compose 快速入门（中文）](https://docker.cadn.net.cn/manuals/compose_gettingstarted)、[Docker 官方文档（命令、版本与部署校准）](https://docs.docker.com/get-started/)
- Docker 视频：[黑马 Docker 从入门到实战](https://www.bilibili.com/video/BV1vo4y1T73j/)、[Docker Tutorial for Beginners - TechWorld with Nana](https://www.youtube.com/watch?v=3c-iBn73dDE)

学习边界：

- Linux：只学命令行、文件、权限、环境变量、进程、端口、日志、SSH，不学内核和运维岗位深度。
- 网络：围绕 API 调用学习 DNS、IP、端口、TCP、HTTP/HTTPS、请求响应、headers、body、status code、timeout，不系统学考研级网络。
- 数据库：先学 SQL 和关系型数据库，重点是 SQLite/PostgreSQL；向量数据库放到 RAG 阶段再深入。
- Docker：只学镜像、容器、Dockerfile、volume、network、compose 和日志排错，不学 Kubernetes。

## B0-01 Linux 命令行与环境

资料：

- Linux 命令大全（菜鸟教程）：优先查 Navigation、Filesystem、Users/groups/permissions、Searching、Pipes 对应的命令。
- Missing Semester 中文版：先看 Shell 入门；Shell Tools and Scripting、Command-line Environment 只作为进阶补充。
- 视频：如果 MIT Missing Semester 看不懂，只看 B 站双语字幕版本的演示片段；这一关以命令练习为主，不靠视频推进。

要做：

- 在 `notes/stage0_5/b0_01_linux_cli.md` 记录 20 个常用命令：`pwd`、`ls`、`cd`、`mkdir`、`touch`、`cp`、`mv`、`rm`、`cat`、`less`、`head`、`tail`、`grep`、`find`、`chmod`、`ps`、`kill`、`env`、`export`、`curl`。
- 写 `code/stage0_5/b0_01_env_report.sh`，输出当前目录、当前用户、Python 路径、环境变量中的测试值、最近 5 个进程。
- 在 WSL/Ubuntu 中运行脚本，并把命令和输出摘要写入笔记。

问答：

1. 绝对路径和相对路径有什么区别？
2. `chmod` 改的是什么权限？
3. 环境变量为什么适合保存配置？
4. 管道 `|` 解决什么问题？

通过标准：

- 能在 Linux/WSL 终端中独立完成文件、搜索、权限、环境变量和进程查看。
- 能解释一个命令失败时应该先检查路径、权限、命令是否存在还是环境变量。

## B0-02 网络基础与 HTTP

资料：

- MDN HTTP 中文：HTTP 概述、HTTP 消息、HTTP 标头、HTTP 响应状态码。
- Cloudflare 中文：什么是 DNS。
- 视频：湖科大教书匠《计算机网络微课堂》只看概述、应用层、运输层中 DNS/HTTP/TCP 相关部分；YouTube 可补 Jim Kurose 的应用层、DNS、Web/HTTP

要做：

- 写 `code/stage0_5/b0_02_http_probe.py`。
- 输入一个 URL，输出解析到的 IP、请求方法、状态码、部分 headers、响应体前 500 字符。
- 必须设置 timeout，并处理 DNS 失败、连接失败、非 2xx 状态码。

问答：

1. DNS、IP、端口分别解决什么问题？
2. HTTP request 和 response 分别包含哪些部分？
3. 200、301、400、401、403、404、500 大概代表什么？
4. 为什么调用外部 API 必须设置 timeout？

通过标准：

- 能解释一次 `requests.get()` 背后大概发生了哪些网络步骤。
- 能区分“请求没发出去”“服务器返回错误”“JSON 解析失败”这三类问题。

## B0-03 SQL 与关系型数据库

资料：

- SQLite 中文文档：5 分钟快速上手、SQL 语言。
- PostgreSQL 中文文档：教程、SQL 语言。
- 视频：尚硅谷 MySQL 入门到高级只看 SQL 基础、DDL、DML、DQL、约束、索引、事务；CMU Intro to Database Systems 作为理解关系模型和 SQL 的补充

要做：

- 写 `code/stage0_5/b0_03_learning_db.py`。
- 使用 Python 内置 `sqlite3` 创建 `resources/stage0_5/learning.db`。
- 建表 `learning_logs`，字段至少包含：`id`、`date`、`session_id`、`topic`、`status`、`evidence_ref`、`note`。
- 支持新增、查询最近 7 条、按 topic/status 统计记录、更新状态、删除一条测试数据。

问答：

1. 表、行、列、主键分别是什么？
2. JSON 文件和数据库各适合什么场景？
3. 索引为什么能加速查询，又为什么不能乱加？
4. 事务解决什么问题？

通过标准：

- 能用 SQL 完成基本 CRUD。
- 能解释为什么聊天历史、Memory、任务记录适合放进数据库。
- 能说明 SQLite 和 PostgreSQL 在使用场景上的差异。

## B0-04 Docker 与 Compose

资料：

- Docker 中文文档：先看 Docker 教程、容器操作、镜像管理、Dockerfile、Docker Compose。
- Docker Compose 快速入门（中文）：重点看 services、ports、environment、volumes、logs、exec。
- Docker 官方英文文档：实际 Session 用对应小节核对命令、版本、安全与部署配置；中文教程主讲，不能等出现行为冲突后才核验。
- 视频：黑马 Docker 从入门到实战 02-18；YouTube 可补 TechWorld with Nana Docker Tutorial for Beginners

要做：

- 在 `code/stage0_5/docker_learning_stack/` 创建一个最小 Docker 练习。
- 写一个 Python 脚本，启动后读取环境变量，连接数据库或打印配置摘要。
- 写 `Dockerfile` 构建镜像。
- 写 `compose.yaml`，至少包含一个 Python 服务和一个 PostgreSQL 服务。
- 运行 `docker compose up`，记录日志、端口、volume、容器名称和排错过程。

问答：

1. image 和 container 有什么区别？
2. Dockerfile 和 compose.yaml 分别负责什么？
3. volume 解决什么问题？
4. Compose 里的服务名为什么可以当作主机名使用？

通过标准：

- 能构建并启动一个多容器练习。
- 能用 `docker compose logs` 和 `docker compose exec` 做基础排错。
- 能解释端口映射、环境变量、volume、network 的作用。

## B0-Gate 工程基础闯关

定位：

- 这是后续项目化整合关卡，不再作为进入阶段 1 的硬门槛。
- 建议在完成 `L1-Gate` 和基础 Tool Calling 后，或准备做 Memory/RAG/本地部署时再完成。
- 如果某个 Agent 项目提前需要数据库或 Docker，可以提前做本关。

前置：正式验收前完成 `B0-01`、`B0-02`、`B0-03`、`B0-04`，或由正式复核给出逐项等价的可执行证据；不能只因最终栈能启动就默认为 Linux/网络/数据库/Docker 都已掌握。

任务：

- 做 `code/stage0_5/b0_gate_local_stack/`。
- 用 Docker Compose 启动 PostgreSQL 和一个 Python CLI 程序。
- Python 程序支持写入学习记录、查询最近记录、按主题与状态统计记录。
- README 写清楚启动、停止、查看日志、进入容器、清理 volume 的命令。
- 在 `notes/stage0_5/b0_gate_engineering_basics.md` 画出：终端命令 -> Docker Compose -> Python 容器 -> Compose 网络 -> PostgreSQL 容器 -> volume。

必须回答：

1. 从你输入命令到数据库保存成功，中间经过哪些步骤？
2. 如果连接数据库失败，你会按什么顺序排查？
3. 数据为什么不能只放在容器可写层？
4. 这个本地栈后续如何服务于 Agent 的 Memory 或 RAG？

通过标准：

- 一条命令能启动本地栈。
- 能新增和查询学习记录。
- 能解释 Linux、网络、数据库、Docker 在这个练习里分别承担什么职责。

---

# 阶段 1：大模型 API 入门

目标：能调用大模型 API，完成单轮、多轮、流式输出、错误处理。

进入条件：

- `P0-Gate` 通过。
- 不要求 `B0-Gate` 已通过；工程基础按阶段 0.5 的触发点穿插补。
- 如果 L1 中遇到环境变量、安装包、HTTP 超时、API 错误码，回到对应 B0 小节补最小必要知识。

主资料：

- OpenAI API Quickstart
- OpenAI Text Generation / Responses API
- DeepLearning.AI `Building Systems with the ChatGPT API`
- B站大模型 API 入门视频作为中文辅助

## L1-01 API Key 与 SDK

资料：

- OpenAI Quickstart：环境变量、安装 SDK、第一次请求
- DeepLearning.AI：课程开头的 API 调用环境部分

要做：

- 写 `code/stage1/l1_01_first_call.py`。
- 从环境变量读取 API Key。
- 调一次模型并打印结果。

问答：

1. API Key 是身份、权限、还是模型本身？
2. 对比 curl（原生 HTTP）和 SDK 两种调用方式，SDK 帮你省掉了哪些步骤？
3. 为什么要把模型名作为参数传入？

通过标准：

- 不在代码里出现真实 API Key。
- 能区分 SDK、API、模型。

## L1-02 单轮问答

资料：

- OpenAI Text Generation
- DeepLearning.AI：对话格式、消息组织

要做：

- 写 `code/stage1/l1_02_ask.py`。
- 用户输入一个问题，模型回答一次。

问答：

1. prompt 和 user message 有什么关系？
2. 模型输出为什么不等于事实？
3. 如何给用户显示错误提示？

通过标准：

- 能处理空输入。
- 能说明输出不确定性。

## L1-03 多轮聊天

资料：

- OpenAI Responses API / conversation examples
- DeepLearning.AI：chatbot 相关章节

要做：

- 写 `code/stage1/l1_03_chat.py`。
- 保存最近 N 轮对话。
- 支持 `exit` 退出。

问答：

1. 多轮聊天为什么要保存历史？
2. system、user、assistant 消息各自作用是什么？
3. 上下文太长会导致什么问题？

通过标准：

- 连续对话 3 轮以上。
- 能解释上下文窗口。

## L1-04 流式输出

资料：

- OpenAI 流式输出相关文档
- 视频中 stream/非 stream 对比小节

要做：

- 写 `code/stage1/l1_04_stream_chat.py`。
- 逐步显示模型输出。

问答：

1. 流式输出和一次性输出的差异是什么？
2. 为什么流式输出要处理增量？
3. 流式输出失败时如何收尾？

通过标准：

- 能看到逐步输出。
- 程序退出不留异常堆栈。

## L1-05 参数实验与成本意识

资料：

- OpenAI 模型参数说明
- DeepLearning.AI：输出控制相关内容

要做：

- 写 `code/stage1/l1_05_params_experiment.md`。
- 对同一问题至少跑 3 组参数并记录输出差异。

问答：

1. temperature 变高通常意味着什么？
2. 哪类任务适合低随机性？
3. token 成本由哪些部分构成？

通过标准：

- 有真实输出对比。
- 能解释参数选择。

## L1-Gate API 入门闯关

任务：

- 做 `code/stage1/l1_gate_cli_chatbot.py`。
- 支持多轮、流式输出、退出命令、错误提示、历史长度限制。

必须回答：

1. 你的消息历史如何保存？
2. 如何避免把 API Key 泄露？
3. 如果 API 调用超时，你的程序怎么表现？
4. 哪个参数最影响输出稳定性？

通过标准：

- 能演示 5 轮对话。
- 能解释完整调用链路。

---

# 阶段 2：Prompt 与结构化输出

目标：能设计稳定 prompt，让模型输出摘要、分类、JSON。

主资料：

- OpenAI Prompt Engineering
- OpenAI Structured Outputs
- DeepLearning.AI `ChatGPT Prompt Engineering for Developers`

## PR2-01 Prompt 基础

资料：

- DeepLearning.AI：Guidelines
- OpenAI Prompt Engineering

要做：

- 写 `code/stage2/pr2_01_prompt_cases.md`。
- 对同一任务写 3 个 prompt，对比结果。

问答：

1. 好 prompt 通常包含哪些要素？
2. 示例 few-shot 解决什么问题？
3. 什么时候 prompt 越长反而越差？

通过标准：

- 有对比和结论。

## PR2-02 摘要与改写

资料：

- DeepLearning.AI：Summarizing / Transforming

要做：

- 写 `code/stage2/pr2_02_summarizer.py`。
- 输入长文，输出 3 条要点和 1 段摘要。

问答：

1. 摘要和改写的目标差异是什么？
2. 如何限制摘要长度？
3. 如何判断摘要遗漏了重点？

通过标准：

- 输出格式稳定。

## PR2-03 分类与路由

资料：

- DeepLearning.AI：Inferring
- Agentic Design Patterns：Chapter 2 Routing

要做：

- 写 `code/stage2/pr2_03_classifier.py`。
- 分类：问题、投诉、建议、闲聊、其他。

问答：

1. 为什么要定义固定标签？
2. 路由和分类有什么关系？
3. 标签不确定时怎么处理？

通过标准：

- 至少 15 条测试样例。
- 有错误分析。

## PR2-04 JSON 与 Schema

资料：

- OpenAI Structured Outputs
- Structured Outputs Cookbook

要做：

- 写 `code/stage2/pr2_04_extract_json.py`。
- 从邮件中提取：发件人、事项、截止时间、优先级、是否需要回复。

问答：

1. schema 约束了什么？
2. JSON 不合法时怎么处理？
3. 字段缺失时应该返回空、null，还是编造？

通过标准：

- 输出能被 `json.loads()` 解析。
- 不编造缺失信息。

## PR2-Gate 结构化输出闯关

任务：

- 做 `code/stage2/pr2_gate_email_processor.py`。
- 输入邮件文本，输出分类、摘要、待办 JSON，并保存到文件。

必须回答：

1. 你如何保证 JSON 可解析？
2. 你如何测试分类稳定性？
3. 哪些场景不能只靠 prompt 解决？

---

# 阶段 3：Tool Calling / Function Calling

目标：让模型选择并调用真实工具。

主资料：

- DeepSeek 官方 Tool Calls：`https://api-docs.deepseek.com/guides/tool_calls`（当前实跑主线，与项目模型一致）
- OpenAI Function Calling（字段与通用兼容格式对照）
- OpenAI Agents SDK Quickstart
- Hugging Face Agents Course：Unit 1 tools/actions/observations，Bonus Unit 1 function calling

## T3-01 函数调用概念

资料：

- Hugging Face：`units/zh-CN/unit1/tools.mdx`、`actions.mdx`、`observations.mdx`
- Hugging Face：`bonus-unit1/what-is-function-calling.mdx`

要做：

- 写 `notes/stage3/t3_01_function_calling.md`。
- 画出：用户问题 -> 模型选择工具 -> 程序执行 -> 工具结果 -> 模型回答。

问答：

1. 模型真正执行工具了吗？
2. 工具 schema 的作用是什么？
3. Observation 如何影响下一步？

通过标准：

- 能准确区分模型决策和程序执行。

## T3-02 计算器工具

资料：

- OpenAI Function Calling
- Hello-Agents：`code/chapter4/tools.py`
- HelloAgents：`hello_agents/tools/builtin/calculator.py`

要做：

- 写 `code/stage3/t3_02_calculator_tool.py`。

问答：

1. 为什么数学题不能完全交给模型口算？
2. 工具参数如何校验？
3. 工具报错如何返回？

通过标准：

- 工具真实计算。
- 能打印调用参数。

## T3-03 文件工具

资料：

- HelloAgents：`hello_agents/tools/builtin/terminal_tool.py`、`note_tool.py`
- Datawhale Hello-Agents 第九章上下文工程相关代码

要做：

- 写 `code/stage3/t3_03_file_reader_tool.py`。
- 限制只能读取 `resources/sandbox/`。

问答：

1. 为什么文件工具必须限制目录？
2. 长文件怎么摘要或截断？
3. 如果用户要求读取敏感路径怎么办？

通过标准：

- 不能读取沙箱外文件。

## T3-04 外部 API 工具

资料：

- 廖雪峰 requests
- OpenAI tool calling examples

要做：

- 写 `code/stage3/t3_04_public_api_tool.py`。
- 调用公开 API 或 mock API。

问答：

1. 外部 API 失败时怎么处理？
2. API 返回原始 JSON 是否应该全给模型？
3. 工具超时如何设置？

通过标准：

- 有超时和错误处理。

## T3-Gate Tool Calling 闯关

资料：

- DeepSeek Tool Calls 官方示例：重点看 `tools`、`message.tool_calls`、`tool_call_id`、`role="tool"` 和第二次模型调用。
- 本项目已 PASS 的 `t3_02_calculator_tool.py`、`t3_03_file_reader_tool.py`、`t3_04_public_api_tool.py`。

任务：

- 做 `code/stage3/t3_gate_tool_assistant.py`。
- 使用 DeepSeek/OpenAI 兼容接口的原生 `tools`/`tool_calls`，让**模型**在计算、读文件、外部 API 三个真实工具中选择；关键词 `if/elif` 路由只能作为对照基线，不能作为 Gate 主实现。
- 第一次闭环显式使用 non-thinking mode（`extra_body={"thinking":{"type":"disabled"}}`），先掌握 Tool Calling 主链；thinking + tools 需要持续回传 `reasoning_content`，留到 A4 多步 Agent 再扩展，避免两个新难点混学。
- 完整走通：模型生成 tool call → 客户端校验工具名和 JSON 参数 → 从 `TOOLS` 注册表执行真实函数 → 以 `role="tool"` + `tool_call_id` 回填 Observation → 再次调用模型生成最终回答。
- 同时覆盖“不需要工具直接回答”、未知工具、坏 JSON/错参数、工具自身失败、危险路径拒绝和最大工具轮数；不得把模型自编文本当真实 Observation。
- 外部 API 工具不能把模型给出的任意 URL 直接交给 `requests`。T3-Gate 至少实现固定 endpoint/域名 allowlist，并拒绝 localhost、私网、云 metadata IP；对重定向要么关闭自动跟随，要么逐跳重新校验 `Location`，不能只检查初始 URL；S-05 再系统扩展 DNS rebinding 与网络出站策略。
- 配自包含的 `eval_cases.json`：10 条正常 + 3 条失败 + 1 条危险输入；在首次调参前冻结其中至少 3 条为未揭示 holdout，并在文件内写清目标、fixture、四种执行 mode、断言规则和预设阈值。正式检查由 `ai-agent-learning-review` 直接执行全部 14 条：正常模型行为使用真实 DeepSeek，坏 JSON、工具失败、最大轮数与危险网络输入使用内存注入/mock 确定性复现；通过率、逐例失败、holdout 和安全结果写入当天 daily，不保留 `run_evals.py`、`eval_baseline.json` 或原始报告。危险集至少包含一个复合场景：坏工具参数/未知工具与恶意 URL、超时或限流同时出现，要求先找全问题再按优先级处理。

必须回答：

1. 工具注册表如何设计？
2. Agent 如何选择工具？
3. 如何避免危险工具调用？
4. 工具结果太长如何处理？

通过标准：

- 至少真跑计算、文件、外部 API 各 1 次，并能看到真实 `tool_calls` 与回填后的最终回答。
- 无工具问题不会被强迫调用工具；危险路径和危险 URL 在客户端/工具层被拒绝。
- 能逐步解释 `assistant.tool_calls`、`tool_call_id`、`role="tool"` 和第二次模型调用分别负责什么。

---

# 阶段 4：Agent 基础原理

目标：理解 ReAct、Planning、Reflection，并写出最小 Agent。

主资料：

- Datawhale Hello-Agents：第 1-4 章
- Hugging Face Agents Course：Unit 1
- Agentic Design Patterns：Reflection、Planning、Tool Use

## A4-01 什么是 Agent

资料：

- Hello-Agents：`docs/chapter1/第一章 初识智能体.md`
- Hugging Face：`unit1/what-are-agents.mdx`

要做：

- 写 `notes/stage4/a4_01_what_is_agent.md`。

问答：

1. Agent 和 chatbot 的关键区别是什么？
2. 环境、动作、观察分别是什么意思？
3. 什么任务没必要用 Agent？

通过标准：

- 不把所有 LLM 应用都叫 Agent。

## A4-02 LLM 与 Agent 基础

必读资料：

- Hello-Agents：2.4.3「基于大规模数据的预训练」、2.4.4「基于大语言模型的智能体」、3.1.3「Decoder-Only」、3.2.2「文本分词」、3.3.2「模型幻觉」
- Hugging Face：`unit1/what-are-llms.mdx`、`messages-and-special-tokens.mdx`

扩展资料（不计入本任务必读范围）：

- Hello-Agents 第 2、3 章其余历史、完整 Transformer 推导、模型调用与选型小节，后续遇到对应任务再读。

可跨日期的知识单元：

1. LLM 机制：Token/Tokenizer、自回归预测、参数容量、Encoder/Decoder、注意力。
2. 输入表示：System/User/Assistant、Special Token、Chat Template、Prompt 与指令微调。
3. Agent 边界：LLM/客户端/工具/Observation、无状态会话、幻觉与可靠性防线。

要做：

- 由助手根据实际资料、用户原始回答和订正过程自动整理 `notes/stage4/a4_02_llm_agent_basics.md`；带读中标 `DRAFT`，正式检查时定稿。用户不需要共写，除非明确要求。
- 按知识单元与 Session 逐步推进；未完成时保持 `DOING`，记录已覆盖范围、任务总剩余和下次 Session 起点。

问答：

1. LLM 在 Agent 中扮演什么角色？
2. 消息格式为什么重要？
3. 幻觉会如何影响 Agent？

通过标准：

- 能解释 LLM 不是执行器。
- 能说明消息边界/Chat Template 为什么会影响模型理解。
- 能说明幻觉在 Agent 中会放大成什么风险，以及工具、代码校验和人工确认分别兜哪一层。

## A4-03 ReAct

资料：

- Hello-Agents：第 4 章 ReAct
- Hello-Agents 代码：`code/chapter4/ReAct.py`
- Agentic Design Patterns：Chapter 5 Tool Use

要做：

- 跑通或改写 `code/stage4/a4_03_react_agent.py`。

问答：

1. Thought/Action/Observation 各自作用是什么？
2. ReAct 什么时候应该停止？
3. 如何防止无限循环？

通过标准：

- 能展示完整执行轨迹。
- 有最大步数。

## A4-04 Plan-and-Solve

资料：

- Hello-Agents：第 4 章 Plan-and-Solve
- Hello-Agents 代码：`code/chapter4/Plan_and_solve.py`
- Agentic Design Patterns：Chapter 6 Planning

要做：

- 写 `code/stage4/a4_04_plan_solve_demo.py`。

问答：

1. Planning 解决什么问题？
2. 计划错了怎么办？
3. 简单任务为什么不需要规划？

通过标准：

- 输出计划、执行结果、复盘。

## A4-05 Reflection

资料：

- Hello-Agents：第 4 章 Reflection
- Hello-Agents 代码：`code/chapter4/Reflection.py`
- Agentic Design Patterns：Chapter 4 Reflection

要做：

- 写 `code/stage4/a4_05_reflection_writer.py`。

问答：

1. Reflection 适合什么任务？
2. Reflection 会增加哪些成本？
3. 如何判断反思没有越改越差？

通过标准：

- 有初稿、反思、改进稿和对比。

## A4-Gate 最小 Agent 闯关

任务：

- 先形成一页 `problem-contract.md`：目标用户、要解决的任务、输入/输出、允许调用的工具、验收条件、失败/拒绝边界和本版明确不做什么；遇到含糊或冲突要求时先澄清并记录决定。用户必须亲自完成会改变 Agent 行为、风险或验收结果的关键判断，并能解释取舍；助手负责把这些已验证决策整理成完整文档，补齐格式、示例、重复分支、非目标和决定记录，不要求用户逐节转写已通过的内容。
- 做 `code/stage4/a4_gate_research_summary_agent.py`。
- 输入主题或资料路径，能调用工具、总结、反思修正。
- 配 10 条正常 + 3 条失败 + 1 条危险输入的自包含 `eval_cases.json`；正式检查直接执行，或复用项目已有的轻量参数化 pytest。只长期保留能持续保护 Agent 循环、停止条件、日志和安全边界的测试；结果写 daily，不为本关另建通用 runner、独立 baseline、报告归档或 tracing 平台。
- 记录最小结构化日志：每步模型调用、工具名、耗时、错误和累计步数；设置 max_steps、timeout、重试上限。
- 对写文件、执行命令等高风险/不可逆动作设置人工确认；本关至少演示一次允许/拒绝分支。

必须回答：

1. 你的 Agent 循环是什么？
2. 什么时候停止？
3. 工具失败时如何恢复？
4. 哪一步最容易产生幻觉？
5. 哪条验收条件最容易被误解，你如何把它改写成可测试的规则？

---

# 阶段 4.5：LangGraph 基础工作流（A4 后当前入口）

目标：在已经独立写过并通过 A4 Agent 循环后，尽早获得 LangGraph 的可执行基础；把已证明的控制原则迁移到新的“故障诊断与变更评审”业务问题，而不是复制 A4 研究摘要 Agent 或重新教学 Agent Loop。

资料（执行当天重新核对当前官方 API）：

- [LangGraph overview](https://docs.langchain.com/oss/python/langgraph/overview)
- [Graph API](https://docs.langchain.com/oss/python/langgraph/graph-api)
- [Streaming](https://docs.langchain.com/oss/python/langgraph/streaming)
- [Testing](https://docs.langchain.com/oss/python/langgraph/test)
- [Tools / ToolNode](https://docs.langchain.com/oss/python/langchain/tools)

范围边界：

- 安排在 `A4-Gate` 之后；A4 的状态/停止/工具边界与测试思想只作前置证据，业务输入、工具和项目目录均使用新的故障诊断场景。
- 只覆盖 `StateGraph`、state schema、node、`START/END`、固定/条件边、工具节点或等价工具分支、compile、invoke/stream 和节点/路由测试。
- persistence/checkpointer、thread、interrupt/resume、durable execution、长期 Memory 和恢复幂等全部留到正式 G8，不提前扩课。
- 直接使用 `StateGraph` 等显式编排能力；只调用 LangChain `create_agent` 不算本任务证据。

## G8-00 LangGraph 基础工作流

要做：

- 在实际动手 Session 才创建 `code/stage8/incident_change_review_agent/`，实现项目 v1：输入合成或脱敏的告警、日志、配置与变更请求；state 必须有明确 schema。
- 至少包含事实整理、只读诊断工具、证据审查和最终结论节点；条件边必须覆盖正常、证据不足、工具失败、最大步数和明确停止原因。
- 输出至少一种 state/node 更新流，并按执行时的官方文档记录所用 LangGraph 版本和 streaming API，避免把过时教程写法固化进课程。
- 对正常、路由、工具失败、证据不足和停止边界做确定性测试，并保留至少一次真实 DeepSeek 调用；mock 只用于稳定测试和故障注入。
- 在 daily 写一张“A4 手写循环职责 ↔ Graph 职责”的映射，并说明本项目为什么值得或不值得引入 LangGraph；不要求复刻 A4 的输入与输出。

必须回答：

1. state、node、edge 分别承载手写 Agent Loop 的哪部分职责？
2. 条件边为什么必须有明确终止分支？
3. 框架迁移后，哪些安全和工具执行责任仍属于应用代码？
4. 什么简单任务继续使用普通函数/循环更合适？

通过标准：

- 故障诊断 v1 可运行、可流式观察、可测试；固定正常/失败案例与至少一次真实模型路径均有可定位证据。
- 能脱离代码解释控制流映射和框架边界；不能只会照抄 quickstart。
- 本任务不创建持久化或恢复证据，也不冒充 G8-Gate 的可恢复 Agent 能力。

---

# 阶段 5：框架源码单链路追踪（角色相关压缩项）

目标：证明能够从真实入口追到 Agent、LLM 和 Tool，并安全修改一处；它不是求职主框架课程，也不阻塞 BE5。

优先级：保持可选。只有理解当前 LangChain/LangGraph 行为或排查真实问题需要时，才追一条入口到核心行为的源码路径；不按 Core/Agents/Tools/Memory/Protocol 目录分别建任务和 notes，也不阻塞主线。

主资料：

- `repos/HelloAgents-feature-branch-1`
- `repos/hello-agents/docs/chapter7/第七章 构建你的Agent框架.md`

## H5-01 框架源码单链路追踪（可选）

要做：

- 跑通一个与当前 A4 工具链相近的 example，从入口追到 Agent → LLM → Tool → 最终输出；在 `notes/stage5/h5_01_framework_trace.md` 只记录真实调用链、关键文件/行号、运行命令和遇到的错误。
- 新增一个小工具或修改一个明确行为，并用真实运行或测试证明改动进入了这条调用链；不抄目录职责，不预读后续 Memory/MCP 内容。

通过标准：

- 能指出入口、消息组织、工具注册/执行和返回路径，并用运行证据证明修改生效。
- 若暂缓本任务，不影响进入 BE5；后续真实框架 debug 也可提供等价证据后再收口。

---

# 阶段 5.5：Python 工程化与 Agent 后端

目标：把两个已经出现真实需求的 Python core 升级为可维护、可测试、可并发、可持久化、可交付的服务。BE5 不再整段挡在 RAG 前面：BE5-01/04 在工程文档 RAG 中即时学习，BE5-02/03 在两个 core 都可运行后统一学习，BE5-05/Gate 再验证通用生产后端能力。

主资料：

- Python 官方：typing、dataclasses、asyncio、logging。
- pytest、Ruff、mypy/pyright 官方文档。
- FastAPI、Pydantic v2、SQLAlchemy 2、Alembic、PostgreSQL/pgvector、Redis 官方文档。
- `code/stage6/engineering_docs_rag/` 与 `code/stage8/incident_change_review_agent/`：作为真实业务核心，不另写无关 Todo/chat demo。

学习边界：

- 不把 Python 重新从零学一遍；重点补和生产后端直接相关的类型、分层、测试、异步、配置、日志和持久化。
- 不在本阶段堆微服务、Kubernetes 或复杂分布式理论；先做单体但边界清晰、可测、可部署的服务。
- FastAPI 只作 application adapter；核心 RAG/Graph 必须可脱离 HTTP 独立运行和测试。
- Redis 放在 BE5-05，覆盖缓存、限流/幂等键和任务状态；Celery/RQ/ARQ 任选其一做最小后台任务，不要求全部学习。

## BE5-01 Python 工程化基础

要做：

- 在 R6-01 的 `code/stage6/engineering_docs_rag/` 中建立 `src/` + `tests/` 结构，使用 `pyproject.toml` 管依赖和工具配置；真实 LangGraph 项目随后复用同样边界。
- 为核心数据结构和边界补 type hints、`dataclass` 或 Pydantic model；用明确异常代替含糊的 `None`。
- 使用 pytest 写单元测试和 mock 外部模型/API；配置 Ruff，并至少跑一次类型检查。
- 使用 `logging` 输出结构化字段，配置由环境变量/Settings 读取，不散落在业务代码中。

通过标准：

- `pytest`、Ruff 和选定的类型检查命令可重复运行。
- 能解释依赖注入、业务逻辑与 I/O 分离为什么更易测试。
- 能指出 mock 的边界，不能用“全 mock 通过”代替真实集成测试。

## BE5-02 asyncio、并发与可靠 I/O

要做：

- 在两个旗舰项目的现有 Python core 中选择真实并发调用链，比较串行与并发行为；不另建脱离项目的 async 教学脚本。
- 使用 `asyncio.gather`/`TaskGroup`、Semaphore、timeout 和 cancellation；识别会阻塞事件循环的同步调用，并用异步客户端或线程池隔离。
- 覆盖部分失败、整体超时、用户取消和限流四类场景；对 429 读取 `Retry-After`，实现有上限的指数退避 + jitter，并区分可重试与不可重试错误。
- 用 fault injection 组合 provider 429/超时、调用方取消和部分工具成功，验证取消传播、并发槽位释放、重试次数、fallback/降级与成本上限；重试不得复制有副作用的操作。本任务用 Python 调用方的取消信号，真实 SSE 客户端断开留到 BE5-03；读取并承认 BE5-04 已记录的 await/连接生命周期局部证据，不重复考察。

通过标准：

- 能解释 event loop、coroutine、task、await 分别负责什么。
- 并发数量有上限，失败不会造成悬挂任务或吞掉异常。
- 429/超时不会形成重试风暴；配额耗尽、context 超限和 provider outage 有稳定失败或降级结果。
- 能说明 async 适合 I/O 等待，不等于自动提高 CPU 密集任务速度。

## BE5-03 FastAPI、Pydantic v2 与流式接口

要做：

- 分别为 `engineering_docs_rag` 与 `incident_change_review_agent` 增加薄 FastAPI adapter；RAG 提供导入、查询、流式查询与任务状态，Graph 先提供运行、流式状态/工具轨迹和统一错误返回；不另写无关聊天玩具。
- `approve/edit/reject` 属于 `G8-03` 的持久化 interrupt 增量：G8-03 在同一 Graph adapter 中补决策接口及重启恢复测试，`BE5-Gate` 再统一验收完整 REST/SSE/HITL 链路。BE5-03 不能提前要求尚未实现的 HITL。
- 使用 Pydantic v2 校验请求/响应，统一错误结构，区分 4xx 与 5xx；API Key 只在服务端读取。
- 加 request ID、health/readiness endpoint、超时与客户端断开处理；用 FastAPI TestClient/httpx 写接口测试。
- 把 BE5-02 的取消传播接到真实 SSE 客户端断开；规定事件类型、`run_id`、顺序号以及完成/失败怎样表示。明确断线后查询已有任务、续流或显式新建的选择，验证重连不会静默启动重复任务；用慢客户端验证有界缓冲或明确取消策略，避免数据无限积压。复用项目接口测试，不另建演示服务。

通过标准：

- curl/前端可消费逐段输出；异常输入不让服务崩溃。
- 路由层不直接堆 Agent 主循环，核心服务可脱离 HTTP 独立测试。
- 能解释普通 JSON、SSE、WebSocket 的取舍，本项目主线选择 SSE 的理由明确。

## BE5-04 PostgreSQL、Alembic 与 pgvector

前置：完成 `B0-01`、`B0-03`、`B0-04` 与 `B0-Gate`，并能启动 PostgreSQL + pgvector（本机或 Compose）。

要做：

- 在工程文档 RAG 项目中使用 SQLAlchemy 2 + Alembic 管理文档、chunk、embedding/index 版本、导入任务与审计；禁止用一次性建表脚本代替迁移历史。
- 使用当前 `langchain-postgres` / pgvector 集成，完成向量列/适配器的确定性读写、最小 metadata/tenant filter、增量更新、删除和版本迁移；执行时核对包版本与迁移说明。这里只验存储、一致性和权限，exact/HNSW、召回影响、hybrid/rerank 与质量对照由 R6-02 正式展开。
- 使用 async driver 前，即时引入 BE5-02 的最小前置：coroutine、await、async with，以及连接/事务的进入和释放。记录为 BE5-02 局部证据，不能提前判整项 PASS；并发、取消与重试仍在后续 BE5-02 学习。随后演示事务回滚、唯一约束和幂等导入，避免重复 chunk 或关系数据/向量状态漂移。

通过标准：

- 数据库迁移可从空库执行，服务重启后文档、索引版本与任务状态仍在。
- 有 repository/service 边界和数据库集成测试。
- 能解释 PostgreSQL 关系数据、向量列、稳定 ID 和最小权限过滤的职责；连接/事务能正常释放。近似索引与召回的取舍在 R6-02 验收，不倒置前置。

## BE5-05 Redis、后台任务、认证与负载测试

要做：

- 在真实项目中给 Redis 一个可验证用途：缓存、限流、幂等键或任务状态至少两项；明确 TTL、失效、一致性和为什么 Redis 不是永久事实源。
- 对长文档导入或长 Agent 运行使用 Celery、RQ、ARQ 或等价后台任务机制，提供提交、查询状态、失败重试和取消入口。
- 实现最小认证/授权边界（开发阶段可用 API key），并对用户/会话资源做归属校验。
- 使用 Locust、k6 或等价工具做小规模负载测试，记录吞吐、p50/p95 延迟、错误率、模型调用并发和瓶颈。

通过标准：

- 长任务不占住一个同步请求直到超时；重试有上限且副作用幂等。
- 未认证、越权、限流和客户端取消都有测试。
- 能基于压测数据指出最先要优化的瓶颈，而不是只说“加服务器”。

## BE5-Gate Agent 后端工程闯关

前置：完成 `B0-01`、`B0-03`、`B0-04` 与 `B0-Gate`；最小部署不能绕过命令行/日志排错、数据库迁移、Docker 和可复现启动。

任务：

- 对工程文档 RAG 与故障诊断 Graph 的共同后端能力做一次 Gate；复用两个既有项目，不创建第三个教学业务。
- 两个项目分别提供可运行 REST + SSE adapter、Pydantic v2 schema、分层结构、PostgreSQL 持久化；共用一次 Redis、后台任务、最小认证、结构化日志和 health/readiness 的通用能力验证。
- `pytest` 覆盖单元/接口/数据库集成测试；Ruff + 类型检查通过。执行小规模负载测试，并在 README 或 daily 用紧凑表格保存命令、负载参数、吞吐、p50/p95、错误率、瓶颈和结论，不另建报告系统。
- 配最小 CI 门禁（pytest、Ruff、类型检查、Docker build），部署一个临时或公开可访问的后端测试环境并执行 health/API smoke；这是求职反馈用的薄纵切，不提前建设完整告警、备份和回滚平台。
- README 包含架构图、环境变量、迁移、启动、测试、负载验证和常见排错；依赖可锁定，陌生人能从空环境运行。
- 写 `system-design.md`：定义主要 API 接收什么、返回什么以及错误时怎样处理，ER/状态模型、请求与数据流、预期并发/数据量、可测 SLI/SLO、缓存与后台任务取舍、前三类失败/降级路径和至少 2 条 ADR；做一次 30 分钟限时复述。
- 从 `work-scenario-coverage.md` 选择至少两个复合事故：每个同时包含 2–4 类当前已引入问题；至少一个完成进程/依赖故障下的止损、恢复与无重复副作用验证。

必须回答：

1. 一次 SSE 请求从路由到模型/工具再到前端经过哪些层？
2. 哪些 I/O 可以并发，如何限制模型和外部 API 并发？
3. 请求中断、后台任务失败、重复提交时如何恢复且不重复副作用？
4. PostgreSQL/pgvector、Redis、Graph checkpoint 与进程内状态分别保存什么，为什么？
5. 压测中 p95、错误率和吞吐反映了什么？

通过标准：

- 一条命令启动依赖与服务，自动测试/静态检查可重复运行。
- 正常、失败、并发、取消、未授权和重复提交均有可观察结果。
- WS-01/03/04/05/06/08/09/13/14 达到本表要求的证据等级；关键安全/越权测试不得有漏放。
- CI 失败不得部署；测试环境可从空配置启动，部署后 smoke 可重复执行并关联到具体提交。
- 系统设计中的容量、SLO 和取舍能用压测/日志/代码证据校验，不是只画框图。
- 课程 PASS 后只在 `job-readiness.md` 记为 `COURSE_PASS`；只有项目进入旗舰、补齐公开/可复现证据后才升 `JOB_EVIDENCE`。

---

# 阶段 6：LangChain 工程文档 RAG

目标：为开发/运维团队构建“工程文档 RAG 助手”，检索公开或脱敏的 API 文档、README、ADR、runbook 与排障文档；回答必须给出可定位引用，资料不足、无权限或引用不支持结论时明确拒答。

主资料：

- [LangChain Retrieval 官方文档](https://docs.langchain.com/oss/python/langchain/retrieval)：区分固定两步、Agentic 与 Hybrid RAG。
- [LangChain overview](https://docs.langchain.com/oss/python/langchain/overview) 与当前 Document Loader、Text Splitter、Retriever、Tools/Agents 文档。
- Datawhale Hello-Agents 第 8 章、Hugging Face Agents Course Unit 3：只用于原理和 Agentic RAG 辅助解释。
- pgvector 与 langchain-postgres 官方仓库；Qdrant/Milvus 只在当前 JD 或架构取舍需要时短对照。
- RAGAS、LangSmith Evaluation 或等价官方评估资料

框架边界：

- 项目主角是 LangChain 的 Document、Loader/Splitter、Retriever、Tool、Agent Harness 与组合接口。
- 当前 LangChain `create_agent` 底层建立在 LangGraph 上；使用该高层接口必须说明依赖关系，但隐藏 runtime 不算已经掌握显式 StateGraph。
- 固定两步 RAG 是可预测 baseline；在完成 chunk、retrieval、引用和失败分层前，不用 Agentic RAG 跳过基础。

## R6-01 LangChain 文档导入与切分

资料：

- 概念主线：本人 Star 中 llm-universe C3 §3.3.2“数据读取”与 §3.3.4“文档分割”；只讲内容/来源、Document/metadata 与切分边界。按资料映射中的订正使用，不复制删除全部空格的清洗或旧接口。
- 官方实现依据：[Document loaders / Interface](https://docs.langchain.com/oss/python/integrations/document_loaders#interface)、[Text splitters](https://docs.langchain.com/oss/python/integrations/splitters)，2026-09-05 已核验；实际 Session 再核查具体 parser 与包版本。
- 可选补充：Hello-Agents 第 8 章 §8.3.2 的导入流程、§8.3.4（1）（2）的文档载入与结构感知切分；若主线已讲清则不追加，不扩成长期 Memory。已核验章节、冻结版本、订正和许可见 [GitHub 资料映射](../resources/github-starred-learning-map-2026-09-05.md)。
- Hello-Agents `code/chapter8/04_RAGTool_MarkItDown_Pipeline.py` 只作有需要时的处理链对照；Hugging Face `unit3/agentic-rag/introduction.mdx` 移到 R6-03 的 Agentic 对照语境，不作为本单元额外必读。

要做：

- 在实际动手 Session 创建 `code/stage6/engineering_docs_rag/`，用 LangChain Loader、Text Splitter 与 Document 对象/metadata 字段建立可运行的导入切片；本任务只做 Loader、Splitter、Document/chunk 生命周期与轻量确定性测试。
- `BE5-01` 紧接着在同一目录补 `src/tests/pyproject`、分层、配置、结构化日志、pytest、Ruff 与类型检查，两个任务分别正式验收；R6-01 不能把“已经顺手工程化”当作 BE5-01 自动 PASS。
- 至少读取 Markdown、TXT 和 PDF；保留 `document_id`、来源、标题、页码/段落、内容 hash、版本与 tenant 等 metadata。
- 记录解析失败、空页、超长段落、重复文件和编码异常；设计增量导入、更新、删除的文档状态，不把“启动时全量重建”当最终方案。

问答：

1. 为什么不能整篇文档直接塞给模型？
2. chunk 太大和太小分别有什么问题？
3. overlap 有什么作用？

通过标准：

- 能展示切分结果。
- 同一文档重复导入不产生重复 Document/chunk；更新/删除后旧 Document、chunk 和导入状态不会残留，并能展示将来删除向量所需的稳定 `document_id/chunk_id` 边界。
- 能解释固定长度、递归/结构感知切分各自的适用场景。

## R6-02 Embedding、pgvector 与检索

资料：

- Hello-Agents 代码：`code/chapter8/10_RAG_Pipeline_Complete.py`
- Hugging Face：`unit3/agentic-rag/tools.mdx`

要做：

- 在 `engineering_docs_rag` 中先用可解释的小样例/轻量本地索引理解 embedding、top-k 与相似度，再迁移 PostgreSQL + pgvector；本地索引只能作热身或 baseline。
- 覆盖 exact baseline、HNSW、metadata/tenant filter、增量更新、删除和 migration；说明近似索引与 filter 可能如何影响召回。
- 实现向量检索与 PostgreSQL 全文/关键词检索的 hybrid search，并接一个 rerank；记录不同 chunk、top-k、filter、索引、融合与 rerank 配置的对照。

问答：

1. embedding 表示什么？
2. 向量检索为什么能找相似内容？
3. 检索不准时可以调哪些地方？

通过标准：

- 能返回相关片段。
- 在带 reference chunk 的小数据集上计算 Recall@k 或 MRR 中至少一个检索指标；把只向量检索作为 baseline 对照配置，只保留数据集、配置和紧凑指标快照，不建设通用评估平台。
- metadata filter 能阻止跨知识库/跨用户取回无权限资料。
- 更新/删除文档后，PostgreSQL 中对应旧向量和索引版本不会残留；迁移、增量写入与删除有可重复测试。
- 本任务正式检查时同时核验 `S-02` 的独立通过标准并分别写回状态；若 S-02 仍有缺口，不能只把它称作“已隐含覆盖”。

## R6-03 固定两步 RAG、Agentic RAG 与引用

资料：

- Hello-Agents 代码：`code/chapter8/11_Q&A_Assistant.py`
- Hugging Face：`unit3/agentic-rag/agentic-rag.mdx`

要做：

- 先实现固定两步 RAG：检索完成后再生成，作为可预测 baseline；支持查询改写/拆分中的至少一种，但必须保留原始问题用于 trace。
- 再把 Retriever 作为 LangChain Tool，让 Agent 决定是否以及如何检索；与固定两步 RAG 使用同一数据集、模型、引用必须满足的规则和预算比较，不以“更智能”代替指标。
- 引用必须可定位到原文页码/段落；回答、引用、无答案拒答和越权拒绝分别评估。

问答：

1. RAG 如何减少幻觉？
2. 为什么必须返回引用？
3. 资料里没有答案时怎么回答？
4. 固定两步 RAG 与 Agentic RAG 的控制权、延迟、可预测性和失败面有什么不同？

通过标准：

- 有引用。
- 不对资料外问题胡编。
- 能区分“检索没找到”“找到但模型答错”“引用与答案不一致”三类失败。
- 同一评估集上给出两种架构的质量、延迟、token/成本与失败分组对照，并据证据选择默认方案。

## R6-Gate LangChain 工程文档 RAG 闯关

任务：

- 继续演化 `code/stage6/engineering_docs_rag/`，不另建 Gate 仓库。资料只使用公开、脱敏或明确授权的 API 文档、README、ADR、runbook 与排障材料，不默认读取个人知识库或公司未授权资料。
- `problem-contract.md` 固定开发/运维用户、查找工程事实和排障依据的原流程、输入/输出、权限、引用必须满足的规则、验收、人工接管，以及至少 1 个可测业务/操作指标。
- 功能 Gate 导入至少 20 篇或 50 页、多种长度/格式资料，支持增量导入、更新、删除、去重、问答、可定位引用和无答案拒答；不得只证明 3 篇玩具样例能跑。
- 主线使用 pgvector；实现 metadata/权限 filter、hybrid search 和 rerank，并保留只做向量检索的 baseline 对照。
- 保留固定两步 RAG 与 Agentic RAG 的同集对照；根据指标选择默认路径，不能默认叠加所有架构。
- 每个 chunk 保留 `document_id`、来源、标题、页码/段落、hash、知识库/用户归属；重复导入不重复，更新/删除不残留旧向量。
- 记录数据血缘与版本：解析器、chunk 配置、embedding/index 版本、导入任务、更新时间和删除审计；敏感文档/metadata 进入日志、trace、评估集前先脱敏。
- 配版本化评估集至少 20 条，覆盖正常、跨文档、多跳/改写、无答案、解析失败、越权和注入输入；复用项目 tests 和一个小型领域指标脚本，分别记录 Recall@k/MRR、答案正确/忠实、引用正确、拒答、安全、延迟和成本，结果保存为设计笔记/daily 的紧凑快照，E10 前不另建通用 evaluator 或报告归档。
- 接入项目自己的 FastAPI/SSE adapter、PostgreSQL/pgvector、认证和后台导入任务；复用并更新 BE5-Gate 的 Redis/CI/Docker/测试部署/smoke，不把 R6 当第一次上线。
- 注入至少一个复合事故，例如 embedding/index 版本混用 + ACL filter 顺序错误 + 缓存 key 漏 tenant + 文档间接注入；要求根据检索/引用/trace/审计证据找齐根因并回归。
- 扩展系统设计包：分别画导入与查询数据流，估算文档/chunk/并发规模，定义检索质量与 p95 延迟 SLO，说明索引更新一致性、成本、ACL 和降级策略，并记录关键 ADR。

必须回答：

1. 文档从上传到可检索经过哪些持久化状态，失败后如何重试？
2. chunk、embedding、hybrid、rerank 各解决什么问题，哪一层最影响当前失败集？
3. 如何证明是检索变好了，而不是模型偶然答对？
4. 如何避免用户 A 检索到用户 B 的文档？
5. 更新或删除文档时如何保证关系数据和向量数据一致？
6. 技术指标变好后，哪一个用户流程或业务指标也得到改善，证据是什么？

通过标准：

- 从空库可复现导入、检索、问答、更新和删除全链路。
- 有“只向量检索”baseline 与至少一次改进实验；保留数据/配置版本和紧凑指标/失败样例对比即可，指标和失败样例可追溯。
- 越权、注入和资料外问题不会泄露内容或编造答案。
- 更新后的 CI/Docker/deploy/smoke 可重复运行；数据版本、权限和删除行为有审计证据。
- 至少一个业务/操作指标有基线、候选版本和失败样例；没有改善时如实解释瓶颈，不只展示技术栈清单。

---

# 阶段 7：Agent 设计模式

目标：知道什么时候用哪种 Agent 模式。

学习边界：本阶段不再把所有章节当独立课程从头背一遍；优先拿 A4/R6 已完成项目做架构评审，只精读实际用到、准备替换或明确放弃的模式。最终产出必须解释取舍，而不是罗列名词。

主资料：

- `repos/agentic-design-patterns/chapters/`

## D7-01 基础编排模式

资料：

- Chapter 1 Prompt Chaining
- Chapter 2 Routing
- Chapter 3 Parallelization

问答：

1. Prompt Chaining 和一个长 prompt 的区别是什么？
2. Routing 适合什么场景？
3. Parallelization 的代价是什么？

产出：

- `notes/stage7/d7_01_orchestration_patterns.md`

通过标准：

- 能把 chaining、routing、parallelization 映射到至少一个已运行旗舰的真实节点/调用链，并用一条 trace 或测试说明选择的模式确实怎样工作。
- 至少明确拒绝一个不合适的模式并说明代价；用户能独立解释三种模式的适用条件，不只复述章节定义。

## D7-02 Agent 核心模式与协作边界

资料：

- Chapter 4 Reflection（只复用 A4 已 PASS 的概念，不重新教学）
- Chapter 5 Tool Use
- Chapter 6 Planning（只讨论新项目中的模式取舍）
- Chapter 7 Multi-Agent Collaboration

问答：

1. Tool Use 和 RAG 的区别是什么？
2. Planning 适合所有任务吗？
3. 什么证据能证明当前问题确实需要多 Agent，而不是一个 Agent 加确定性工具/节点？

要做：

- 先用现有单 Agent 版本建立质量、延迟、成本和失败类型 baseline；没有可定位瓶颈时不升级多 Agent。
- 本任务只负责定位单 Agent 的可测瓶颈、判断是否准入多 Agent，并冻结角色职责、带类型约束的交接字段、共享/私有 state、停止/预算/升级和对照方案。
- `S-04` 紧接着把获准的最小协作增量落到 LangGraph“故障诊断与变更评审 Agent”，不另起 supervisor 玩具项目；两项分别验收，若不准入多 Agent，也必须由 S-04 记录保留单 Agent 的对照决定。

产出：

- `notes/stage7/d7_02_core_agent_patterns.md`

通过标准：

- 单 Agent baseline 的问题和证据可定位；能说明为什么选确定性节点、单 Agent 或受控多 Agent，而不是按热词选架构。
- 取舍笔记、实验问题、指标、预算、停止与回退条件在 S-04 实现前冻结；本任务 PASS 不冒充 S-04 的代码/同集对照 PASS。

## D7-03 可靠性、长期 Memory 与工程模式

资料：

- Chapter 8 Memory Management
- Chapter 12 Exception Handling and Recovery（只读与 Memory 失败/恢复相关切片）
- Chapter 18 Guardrails/Safety Patterns（只读 PII、隔离与 poisoning 相关切片）
- Chapter 19 Evaluation and Monitoring（只读 Memory A/B 所需指标切片）
- R6 的 RAG 证据直接复用，MCP 留到 M9；本任务不重复读完整 RAG 或提前展开 MCP。

要做：

- 保留模式阅读和 `notes/stage7/d7_03_reliability_patterns.md`，但不能只写笔记。
- 在已有旗舰项目中实现最小生产级长期 Memory，不另起玩具：区分 thread/history/checkpoint/RAG 与跨会话 Memory；定义 `owner/source/type/created_at/updated_at/ttl/provenance`，支持显式写入、检索注入、更新、冲突处理、删除/忘记和 token 预算。
- PostgreSQL 作为长期事实源，Redis 只能作为缓存；未受信工具/RAG 文本不得自动晋升为长期记忆。
- 测试重启后保留、跨用户隔离、陈旧/冲突记忆、删除生效、secret/PII 不落库和 memory poisoning；用同一小数据集与“无 Memory”配置做 A/B，对比任务成功、误记、遗漏、延迟和成本，结果写入设计笔记的紧凑表格，不单独建设 runner 或 baseline 管理系统。

问答：

1. Memory 和上下文历史有什么区别？
2. Guardrails 防什么风险？
3. Evaluation 应该评估什么？

产出：

- `notes/stage7/d7_03_reliability_patterns.md`
- 在 `code/stage6/engineering_docs_rag/` 或 `code/stage8/incident_change_review_agent/` 中选择更需要长期事实的一项做增量，不另建 Memory 玩具目录

通过标准：

- 真实完成写入、检索、更新、删除、TTL/过期和跨会话持久化；跨租户与 poisoning 测试全部通过。
- 能用 baseline 证明 Memory 是否真正改善任务，而不是只增加 token、延迟和错误记忆。

## D7-Gate 设计模式闯关

任务：

- 写 `notes/stage7/d7_gate_architecture_review.md`。
- 选择你已做的一个 Agent，说明用了哪些模式、没用哪些模式、为什么。
- 对这个 Agent 实施一个真实模式变更（默认使用 D7-03 Memory，也可选当前项目更需要的模式），复用同一轻量数据集和项目测试比较质量、延迟、成本和失败分组，把结果写成架构评审中的紧凑对比表。
- 至少保留一个“增加 Planning/Reflection/Multi-Agent/Memory 后反而更差”的反例，说明为什么回退或限制该模式。

通过标准：

- 不能把所有模式都堆上去。
- 能用代码、eval 和失败案例说明取舍，而不只写一份架构评论。

---

# 阶段 8：LangGraph / 可控工作流

目标：在 G8-00 的“故障诊断与变更评审 Agent”基础上，做可持久化、可暂停恢复、可安全重放的 Agent 工作流；本阶段重点是 durable execution，不重复教授 node/edge 入门。

依赖边界：G8-01~03 不再等待 D7。它们只需能区分 checkpoint/thread state 与跨 thread 的长期 Memory；真正的用户/业务长期事实、TTL、provenance、删除和 poisoning 由 D7-03 在项目可运行后系统承担。

主资料：

- LangGraph 官方文档：[Graph API](https://docs.langchain.com/oss/python/langgraph/graph-api)、[Persistence](https://docs.langchain.com/oss/python/langgraph/persistence)、[Interrupts](https://docs.langchain.com/oss/python/langgraph/interrupts)、[Fault tolerance](https://docs.langchain.com/oss/python/langgraph/fault-tolerance)、[Streaming](https://docs.langchain.com/oss/python/langgraph/streaming)、[Testing](https://docs.langchain.com/oss/python/langgraph/test)。
- Hugging Face Agents Course：Unit 2 LangGraph
- Datawhale Hello-Agents 第 6 章 LangGraph
- LangSmith tracing/evaluation 官方文档作为运行证据

## G8-01 持久化与恢复边界

资料：

- LangGraph 官方：persistence、fault tolerance、interrupts。
- G8-00 的手写循环 ↔ Graph 职责映射和测试结果。

问答：

1. 只在内存里运行的 Graph 遇到进程退出会丢什么？
2. checkpoint/thread state 与跨会话长期 Memory 有什么区别？
3. 哪些节点允许 replay，哪些外部副作用必须先设计幂等？

产出：

- `notes/stage8/g8_01_durable_boundary.md`

通过标准：

- 笔记能逐项映射 G8-00 的 state、节点、副作用与停止点，明确哪些状态进入 checkpoint、哪些事实必须留在长期 Memory/业务数据库。
- 用户能针对“工具执行前崩溃”和“副作用已发生但 checkpoint 未写入”两个窗口，独立判断 replay 风险与幂等要求；不能只背概念差异。

## G8-02 持久化 Graph 增量

资料：

- LangGraph 官方：persistence、checkpointer 实现、thread 配置、fault tolerance 与 testing。
- Hugging Face 的 `first_graph.mdx` / `building_blocks.mdx` 仅作 G8-00 基础查漏，不重新带读或重考。

要做：

- 在 `code/stage8/incident_change_review_agent/` 的 G8-00 核心上增量实现，不另建脱离业务的 first-graph 玩具。
- 为 state 定义明确 schema，配置 `thread_id` 与持久化 checkpointer；可用 SQLite 做短暂开发验证，但本任务 PASS 前迁移到 PostgreSQL saver，并验证从空库初始化、进程重启恢复和 thread 隔离；仅进程内 saver 或最终停在 SQLite 都不满足当前生产主线。
- 演示运行中断后重新启动进程，并从 checkpoint 继续。
- 明确边界：checkpoint/thread state 保存单个执行线程的控制流状态，不等于跨 thread 的长期 Memory；本任务只记录未来接入 D7-03 的接口边界，不提前实现或冒充长期 Memory。

问答：

1. checkpoint 在什么时机保存了哪些状态？
2. `thread_id` 如何隔离不同执行实例，错误复用会造成什么问题？
3. 多个节点更新同一 state key 时，reducer/更新规则为什么必须明确？

通过标准：

- graph 能运行。
- 同一 thread 能续接，不同 thread 状态隔离；进程重启后仍能恢复。
- 能用代码和存储记录区分 state/checkpoint 与长期 Memory，不把二者混称。

## G8-03 HITL、错误恢复与幂等

资料：

- LangGraph 官方：interrupts、persistence、fault tolerance、streaming。
- Hugging Face `unit2/langgraph/document_analysis_agent.mdx` 只用于观察控制流模式，不复制其业务题目。

要做：

- 在 `code/stage8/incident_change_review_agent/` 增量实现，不另建文档分析 Agent。
- 加 transient error retry、不可恢复错误、用户可修复错误三类分支；任何有副作用的变更只允许在 sandbox/测试环境执行，并使用持久化 interrupt 做 approve/edit/reject。
- 对 interrupt 前后的外部副作用设计幂等键，避免 resume/replay 重复写入或重复发送。

问答：

1. transient、non-retryable、user-fixable 三类错误怎样划分，分错会造成什么后果？
2. interrupt 前、外部副作用执行中、以及副作用成功但 checkpoint 尚未写入时分别崩溃，恢复策略有什么不同？
3. 幂等键由谁生成、绑定哪些业务字段、保存在哪里、何时算已消费？
4. approve/edit/reject 恢复后哪些 state 可以修改，哪些原始证据和审计记录不能被覆盖？

通过标准：

- 有终止条件。
- 能输出执行轨迹。
- 能暂停等待人工决定，隔一段时间/重启后恢复；拒绝和修改参数分支都有测试。
- 能解释 replay 会重跑哪些节点，为什么副作用必须幂等。

## G8-Gate LangGraph 闯关

任务：

- 完成 `code/stage8/incident_change_review_agent/`，不再创建研究型 Graph 或重复 A4 的 research-agent 题目。
- 输入脱敏/合成的告警、日志、配置、runbook 与变更请求；先区分事实和假设，再调用只读诊断工具收集证据，覆盖主要根因、止损方案、修复建议和可追踪执行过程。
- 使用持久化 checkpointer、thread_id、结构化 state、timeout/retry/cancel、checkpoint resume 和 HITL approve/edit/reject；至少一次在进程退出后恢复未完成任务。
- 需要写文件、更新数据库或调用有副作用工具时使用幂等键；用故障注入验证恢复不会重复副作用。
- 配版本化评估集至少 20 条，分别评估任务完成、节点/工具轨迹、恢复、HITL、安全、延迟和成本；对影响控制流、恢复、HITL、安全或成本的关键修改，复用同一数据集和项目 tests 做对比并把结果写 daily/设计笔记，E10 前不另建通用评估平台。
- 接入旗舰二的 FastAPI/SSE，并提供可观察的工具/状态界面，不把 Graph 留在单文件脚本。界面可以是 curl/API 客户端/极薄调试页；也允许助手在真正进入本任务时，从 GitHub 选择许可证兼容、维护状态可接受且依赖可审计的 Vue 开源骨架后组合成薄界面。若采用第三方 Vue，本 Gate 当场保留来源/版本/许可证/维护状态/依赖风险和采用理由，用户审核关键 diff，并能说明数据流与密钥不进前端等最小安全边界；这只是第三方代码准入审核，不冒充完整 Vue 掌握。J11-03 再做独立 Vue 能力复核、用户亲自解释/修改和产品化演进。
- 在单 Agent baseline 通过后，按 `S-04` 做一次受控多 Agent 对照：只拆分能被独立验证的诊断/风险审查职责，使用带类型约束的交接格式、共享/私有 state、最大 handoff 次数、预算、停止和人工升级；若质量没有提高或成本/延迟明显恶化，保留单 Agent 为默认并记录回退决定。
- 正式运行前冻结分组阈值与至少 20% 且不少于 5 条 holdout；恢复、HITL、关键越权/泄漏和重复副作用固定案例必须 100% 通过。正常任务成功、轨迹、延迟和成本分别按预设门槛判定，不能用总平均掩盖关键失败。
- 扩展系统设计包：明确 state/checkpoint 的存储与生命周期、恢复目标、幂等边界、超时/人工等待 SLO、成本上限和至少 2 条控制流 ADR。

必须回答：

1. state、checkpoint、thread 分别是什么，保存在哪里？
2. 哪些错误自动重试、哪些等待用户、哪些应该立即失败？
3. 进程在工具执行前后崩溃，各自如何恢复且不重复副作用？
4. 为什么 HITL 需要持久化而不只是 `input()`？
5. 如何用 trace 判断是路由、工具、模型还是恢复逻辑出错？

通过标准：

- 从空环境可启动 API 与持久化 Graph；自动测试、固定评估、进程重启恢复、HITL 三分支、取消/错误分类和无重复副作用验证可重复运行。
- WS-02/04/08/11 达到 `work-scenario-coverage.md` 要求的对应切片等级；每个复合事故的全部根因、修复、全量回归和再次故障注入都有定位证据。
- 用户能独立解释 state/checkpoint/thread、崩溃窗口、幂等边界、单/多 Agent 取舍和界面/API 边界；若使用第三方 Vue，最小准入审核齐全。由助手组合的前端代码不计作独立 Vue 掌握证据，完整组件状态/SSE/认证/错误处理能力仍由 J11-03 验收。

---

# 阶段 9：MCP 与外部工具连接

目标：理解 Agent 如何连接文件、数据库、浏览器、企业工具。

主资料：

- Model Context Protocol 最新官方 specification 与 SDK 文档（主线，按开始任务当天的最新 revision 核对）
- Datawhale Hello-Agents 第 10 章
- HelloAgents：`hello_agents/protocols/mcp/`
- Agentic Design Patterns：Chapter 10 MCP
- OpenAI Agents SDK MCP 文档

## M9-01 MCP 概念

资料：

- Hello-Agents：`docs/chapter10/第十章 智能体通信协议.md`
- Agentic Design Patterns：Chapter 10 MCP

问答：

1. MCP 解决的核心问题是什么？
2. MCP server 和普通函数有什么区别？
3. host、client、server 分别是什么？

产出：

- `notes/stage9/m9_01_mcp_concepts.md`

通过标准：

- 笔记基于任务开始当天核验的官方 specification/SDK，标明 revision 或检查日期；能画清 host、client、server、能力发现、transport 与授权边界。
- 用户能在新场景中区分 MCP、普通函数调用、Agent 编排框架，并说明 MCP server 失败/越权时由哪一层处理。

## M9-02 本地 MCP Server

资料：

- HelloAgents：`hello_agents/protocols/mcp/server.py`
- HelloAgents：`hello_agents/protocols/mcp/client.py`

要做：

- 写 `code/stage9/m9_02_local_mcp_server.py`。
- 先用官方 SDK 建本地 STDIO server，暴露 1–2 个安全工具；实现输入 schema、超时、错误结构、日志和最小权限目录。
- 除 tools 外，至少读懂 resources、prompts 与 capability negotiation 的作用，不要求全部实现。

问答：

1. 工具如何被发现？
2. 权限如何控制？
3. 如何记录工具调用日志？

通过标准：

- 客户端能发现工具。
- 未授权路径/参数被拒绝，server 日志能关联一次请求和工具执行。

## M9-03 Agent 调 MCP

要做：

- 写 `code/stage9/m9_03_agent_mcp_client.py`。
- 再实现或接入一个 Streamable HTTP server，使用官方/成熟库提供的认证能力；不得自己手搓不安全 OAuth。
- 能说明 OAuth 2.1/PKCE、token audience、scope、短期 token 与禁止 token passthrough 的原因；开发环境可用简化凭据演示，但必须画清生产授权边界。

问答：

1. MCP 和 LangGraph 是同一类东西吗？
2. MCP 和 Tool Calling 的关系是什么？
3. MCP 工具失败如何反馈给 Agent？

通过标准：

- Agent 能真实调用 MCP 工具。
- STDIO 与 HTTP 两种 transport 的信任边界、凭据位置和部署场景能讲清。

## M9-Gate MCP 闯关

任务：

- 做 `code/stage9/m9_gate_file_summary_agent.py`。
- Agent 通过 MCP 读取指定目录文件并总结；至少演示本地 STDIO 与受保护 HTTP 中一种真实主链，另一种保留可运行最小样例。
- 工具发现、schema、超时、断连、重连、权限拒绝、审计日志和长结果裁剪都有测试；恶意/未知 MCP server 不得默认获得本机敏感权限。
- 配版本化评估集至少 20 条，分别记录工具发现、参数、权限、安全、最终答案、延迟和失败案例；优先把确定性部分写成长期维护的 MCP 集成/权限/断连测试，模型质量使用紧凑案例表，E10 前不为 M9 单独建设评估平台。
- 写一页生产授权说明：resource server、authorization server、client、用户分别是谁，token 能发给谁；不得把 access token 写进 trace 或模型上下文。
- 正式运行前冻结分组阈值与至少 20% 且不少于 5 条 holdout；权限拒绝、越权/泄漏、未知或恶意 server、token 错 audience/scope 和断连恢复固定案例必须 100% 通过，不能被总通过率稀释。

通过标准：

- STDIO 真实主链与受保护 HTTP 最小样例都可重复运行；工具发现、正常调用、超时/断连/重连、权限拒绝、审计和长结果裁剪有自动测试。
- WS-02/06/07/12 达到 `work-scenario-coverage.md` 要求的对应切片等级；凭据不进入模型上下文、日志或 trace，恶意 server 没有默认本机权限。
- 用户能独立解释 transport、capability、授权各方、scope/audience、失败反馈和最小权限取舍。

---

# 阶段 10：评估、监控与综合项目

目标：把两个已经存在的旗舰接入一套可复用、可追溯的评估基础设施，并形成能映射到真实代码和部署的系统设计包；不新建第三个综合项目。

主资料：

- Datawhale Hello-Agents 第 12-16 章
- Hugging Face：Bonus Unit 2 Observability and Evaluation，Unit 4 GAIA
- HelloAgents：`hello_agents/evaluation/`
- Agentic Design Patterns：Chapter 19 Evaluation and Monitoring

## E10-01 Agent 评估

资料：

- Hello-Agents：第 12 章
- Hugging Face：`bonus_unit2/`
- HelloAgents：`hello_agents/evaluation/`

问答：

1. Agent 评估和普通问答评估有什么不同？
2. 你会记录哪些指标？
3. 如何构造失败样例？

产出：

- `notes/stage10/e10_01_agent_evaluation.md`
- `code/stage10/e10_01_eval_harness/`：版本化 dataset、target、代码 evaluator、LLM-as-judge、实验 metadata 和对比报告。

要做：

- 建一套共享 runner/实验 metadata/报告格式，但为两个旗舰分别保留领域 dataset、target adapter 和 evaluator；不得复制成两套平行评估平台。
- 两个旗舰都拆成至少两个组件指标和一个端到端指标：RAG 使用 retrieval、answer/citation、end-to-end；LangGraph Agent 使用 tool/arguments、trajectory/task-success、end-to-end。一个项目的高分不能替另一个项目过关。
- 同时使用确定性代码规则与 LLM-as-judge；人工抽查一部分 judge 结果，记录误判，不能把 judge 当绝对真值。
- 两个旗舰都运行各自的 baseline 与候选版本，比较质量、延迟、token/成本和失败分组；分别冻结最低回归阈值并通过共享入口接入 CI。
- 区分 offline eval 与 online monitoring：把真实失败 trace 脱敏后回灌离线 dataset，形成闭环。

通过标准：

- 两个旗舰的数据、prompt/model/tool 配置和实验结果都可追溯到版本；共享基础设施没有抹平两者不同的指标和失败分组。
- 每个旗舰的 adapter 都用故障注入证明门禁有效；整个任务至少有一次真实候选改动因回归门禁失败被拦下。
- 能解释正确率平均值为什么会掩盖危险输入、长文档、无答案等分组失败。

## E10-02 综合项目设计

设计对象固定为两个现有旗舰：`code/stage6/engineering_docs_rag/` 与 `code/stage8/incident_change_review_agent/`。不得从通用候选清单再起第三个旅行、研究、文件整理或助教项目。

必须回答：

1. 这个项目为什么需要 Agent，而不是普通脚本？
2. 它需要哪些工具？
3. 是否需要 RAG、Memory、Planning、LangGraph、MCP？
4. 失败时如何降级？
5. 如何评估效果？

系统设计任务：

- 用户从两个旗舰中选择一个代表对象，在 30 分钟内完成一版不看原笔记的设计，再与真实项目对照订正；这道代表性任务用于证明独立设计能力，不要求机械重写第二份全文。
- 助手根据已 PASS 的 Gate、E10-01 指标和用户关键决策整理两个旗舰的系统设计包：共享能力只写一次，每个项目分别写清业务目标、数据/状态、失败、安全、容量、SLO、成本与采用/拒绝的方案；用户最终审核。
- 明确用户/业务目标、功能与非功能需求、API/事件接收什么、返回什么及失败怎样表示的规则、数据模型、请求/数据流和信任边界。
- 给出初始容量假设、2–4 个可测 SLI/SLO、成本预算，以及缓存、队列/后台任务、同步/异步和降级取舍。
- 写至少 3 条 ADR，说明选择、备选方案、理由和代价；用现有测试、压测、eval 或 trace 校验关键假设。

产出：

- `notes/stage10/e10_02_project_design.md`
- `notes/stage10/e10_02_system_design.md`

通过标准：

- 两个旗舰的设计内容都能映射到现有代码、评估和部署，不是脱离项目的通用八股图；共享部分与项目专属部分边界清楚。
- 能在追问下解释容量、SLO、数据一致性、失败恢复、安全、成本和扩展顺序。
- 每个旗舰至少一条设计假设被真实指标证实或推翻，并形成 ADR 更新。

## FINAL-Gate 综合项目答辩

执行位置：本节在文件中归属阶段 10，但不是按章节位置立刻执行。必须先完成 `S-01`、`J11-02`～`J11-06` 与 `S-05` 正式收口，再做 `FINAL-Gate`；之后才进入 `J11-07 → J11-08 → J11-Gate`。不能用含糊的“J11/FINAL”倒置依赖。

产出：

- 使用 J11-02 已冻结并完成产品化的 `product_flagship` 作为综合答辩对象，不在 FINAL 临时换项目或新建第三个综合项目目录；若确需改选，必须先按 J11-02 的改选规则补齐前端、部署、观测和回归证据。
- 所选旗舰项目的 README、架构/数据流/信任边界、版本化评估和部署证据
- `notes/stage10/final_defense.md`

通过标准：

- 从零安装可运行。
- README 写清楚。
- 至少 30 个版本化测试样例，覆盖正常、失败、边界、并发、恢复和危险输入；评估脚本可重复运行，输出组件/端到端分项、延迟、token/成本和相对 baseline。
- 至少 30 条总评估中，保留至少 20% 且不少于 5 条未参与调优的 holdout；验收阈值在运行 holdout 前冻结，关键安全/越权/泄漏样例必须全部通过。
- 有失败案例复盘。
- 能现场解释核心代码。
- 自动化门禁包含 pytest、Ruff、类型检查、eval regression、Docker build 和部署 smoke test；公网环境有 health check、结构化日志、secret 管理和最小告警。
- 附架构图、数据流/信任边界、威胁模型、负载报告、恢复演示和至少一条真实 trace；公开仓库不含用户数据或真实凭据。
- 从 `work-scenario-coverage.md` 选择至少 3 个复合事故，合计覆盖旗舰相关类别；其中一个必须完成“告警 → 止损/降级 → 根因定位 → 修复 → 回归 → 上线或回滚 → postmortem”，恢复和安全类达到 `RECOVERED_UNDER_FAULT`。

答辩问题：

1. 核心 Agent 循环是什么？
2. 工具调用链路是什么？
3. 上下文如何管理？
4. 如何控制成本、安全和权限？
5. 下一步最值得改进什么？

---

# 阶段 11：就业准备与作品集（应用岗方向）

目标：把前面学到的东西沉淀成「可展示、可上线、面试能讲清楚」的作品集和求职材料，针对「大模型应用 / Agent 应用开发」岗。

求职背景与教学基线：

- 背景记录：普通本科、在职经历、目标应用岗。既往技术栈只在简历中如实记录，不是已掌握新路线技术的证明，也不形成项目集成要求。
- 教学基线：Python、前端、网络、数据库、工程和 Agent 内容全部按零基础讲、练、验；只有 `progress.md` 已 PASS 或当前任务中独立证明过的内容才算已学。
- 技术栈边界：后续课程、Gate 和旗舰项目统一采用 Python/FastAPI 后端 + Vue 前端；不安排第二套后端实现、框架扫读或跨后端技术栈集成的交付要求。
- 求职差异化需要重新用证据建立：完成带界面、Python 后端服务、评估和部署的完整 Agent 应用，并能解释前后端、数据、权限和模型/工具调用边界后，才能写进岗位证据。
- 暂时不碰：应用岗不要求模型训练（SFT/LoRA、PyTorch、分布式训练）。先全部跳过，集中火力在「用大模型搭产品 + 工程落地」。
- 要补的弱项：Python 后端工程、Docker/部署、可观测、评估回归、安全和运维。Python 工程基础由阶段 5.5（BE5）提前系统补齐；阶段 11 只负责把它用于旗舰产品，不再边做作品边临时学 async/FastAPI。

启动时机：

- 不要等阶段 10 学完才开始。从阶段 3/4（能调 API、能做最小 Agent）起就并行启动：每做出一个能跑的东西，就往作品集里沉淀一次。
- 容器化（J11-04）依赖工程基础 `B0-04 Docker`；做这一步前先把 B0-04 补掉。
- W6/W12/W16/W19 按 `tracker/job-readiness.md` 做双轨审计：核验 4–6 条京东/腾讯等大厂能力标杆，并另抽样恰好 10 条当前在招且已核清硬门槛的 `HARD_ELIGIBLE` 岗位计算真实可投匹配率；不要到最后才发现课程标题、标杆深度和岗位资格不是一回事。

## J11-01 GitHub 与工程习惯

执行边界：W6 起随两个旗舰逐步累计，不要求在还没有真实旗舰改动时一次写完；最晚在 `J11-06` 作品集组合前，用真实 README、分支/PR/CI/review/revert 与 AI 协作审查证据正式收口。

要做：

- 把 `code/` 里的练习整理成规范的 GitHub 仓库：清晰 `README`、`requirements.txt`、`.env.example`、有意义的提交记录。
- 每个要进作品集的项目都写：目标用户、原流程/痛点、解决什么问题、验收标准、怎么运行、用到哪些技术和如何衡量效果。
- 完成一次可审计的团队协作闭环：issue/需求与验收条件 → feature branch → PR → CI 失败 → review feedback → 修改 → merge；再演练一次 merge conflict 或 `revert`，保留 PR、检查结果和变更说明。
- 至少选一次实质性改动记录 AI coding 协作链：AI 提出候选方案/补丁 → 用户审查 diff 与依赖 → 运行测试/静态检查/安全检查 → 接受、修改或拒绝；不能把“AI 生成并能运行”直接当作本人掌握或安全证据。

问答：

1. 为什么作品集项目必须有清晰 README 和可复现的运行步骤？
2. 为什么 `.env` 不能提交，但要提交 `.env.example`？
3. 提交记录混乱会给面试官什么印象？

通过标准：

- 一个陌生人能照着 README 从零把项目跑起来。
- 能展示一次真实或模拟 PR 证据，并解释为什么该修改能安全合并、失败时如何回退。

## J11-02 把 Agent 包成后端服务（FastAPI）

资料：

- FastAPI 官方教程（中文）
- OpenAI / Anthropic SDK 的 async 用法

要做：

- 先读取 R6-Gate、G8-Gate 与 E10 的质量、风险、演示价值和维护成本证据，由用户冻结唯一 `product_flagship`（阶段 6 RAG 或阶段 8 可控 Agent）并写一条 ADR；J11-03、J11-04、J11-05、J11-06 与 FINAL-Gate 都复用这个选择。若后续改选，必须新增 ADR 并补齐新对象缺失的前端、部署、观测和回归证据，不能静默切换。
- 复用 `BE5-Gate` 的工程骨架，把 `product_flagship` 强化为正式产品服务；此任务不再负责第一次学习 async/FastAPI。另一个旗舰保留其 Gate 已通过的可复现 API/demo 和 E10 评估 adapter，不再做第二套产品前端。
- 补齐产品接口：知识库/会话/任务资源、SSE、后台导入、认证授权、限流、request ID、health/readiness、统一错误和 API 文档。
- 处理并发、超时、取消、幂等和错误恢复；区分 4xx（用户/权限问题）和 5xx（服务内部问题）。

问答：

1. 同步和 async 在高并发调用 LLM 时差别在哪？为什么 LLM 服务尤其需要 async + 超时？
2. 流式接口（SSE）和普通 JSON 接口在前端消费方式上有什么不同？
3. API Key 等密钥在服务端如何管理？

通过标准：

- 能用 curl 或前端连续调用，返回流式结果，异常输入不让服务崩溃。
- BE5 的单元/接口/数据库测试、静态检查和负载基线继续适用，不能在接旗舰时退回脚本式结构。

## J11-03 给 Agent 配前端（Vue，按零基础复核）

要做：

- 用户已说明自己会一些 Vue；先用一个最小诊断切片复核组件、props/emit、响应式状态、异步请求、错误/加载状态和浏览器网络调试。通过的部分不重复上完整入门课，未独立验证的部分仍按零基础补齐。
- 助手可以在本任务真正启动时，从 GitHub 选择许可证兼容、维护状态可接受、依赖与安全边界可审计的 Vue 开源项目/组件作为骨架并负责机械组合；不得提前克隆或把未知许可证/过时依赖直接并入旗舰。
- 用户负责审核采用/拒绝的组件、关键 diff 与依赖，亲自完成或解释状态流、SSE、认证、错误/加载状态和前后端安全边界；“开源项目能跑”本身不算用户学习证据。
- 只为 J11-02 冻结的 `product_flagship` 建正式前端：若选择 G8 且 G8-Gate 已有薄界面就复用演化；其他情况在已审计骨架上组合。不得同时为另一个旗舰重建第二套前端。
- 两类产品都支持流式显示；选择 G8 时重点展示工具/状态/HITL，选择 RAG 时重点展示引用来源、无答案和文档权限。界面只实现当前产品真实存在的能力。

问答：

1. 前端如何消费流式（SSE/fetch stream）输出？
2. 为什么把「工具调用过程」可视化对一个 Agent 产品有价值？
3. 前后端分离时，跨域和密钥应该怎么处理（密钥为什么不能放前端）？

通过标准：

- 一个别人打开浏览器就能用的 Web 应用；能独立解释组件、状态、流式消费、错误处理和前后端安全边界。

## J11-04 CI/CD、容器化与上线强化

依赖：

- 先完成 `B0-04 Docker` 与 `BE5-Gate`；BE5-Gate 已有最小 CI/Docker/测试部署/smoke，本任务负责把薄纵切强化为可运维产品交付。

要做：

- 用 `Dockerfile` + `compose.yaml` 把 `product_flagship` 的前端、后端、（可选）向量库 / 数据库打包。
- 把 BE5-Gate 与对应旗舰 Gate 的测试部署演化为唯一公网产品 demo（便宜云主机 / Railway / Render 等任一），补齐前端、域名/HTTPS、负载、备份、告警和回滚；另一个旗舰只维持可复现 API/demo、容器和评估证据，不建设第二套公网产品工程。
- 配置 CI/CD：测试、Ruff、类型检查、eval regression、Docker build、部署后 smoke test；失败不得发布。
- 加 health/readiness、非 root 用户、secret 注入、持久化 volume、日志与备份/恢复说明；使用 HTTPS，记录一次部署失败或回滚演练。
- 用 k6/Locust 做部署前后小规模负载测试，记录 p50/p95、错误率、吞吐和资源瓶颈。Kubernetes 只作可选加分，不作为主线门槛。

问答：

1. image 和 container 有什么区别？
2. 为什么配置要走环境变量而不是写死在代码里？
3. 上线后如果接口报 500，你按什么顺序排查？

通过标准：

- 给出一个别人能直接点开体验的 demo 链接。
- 主分支 CI 通过才能部署；新环境可按 README 从零启动，失败可定位、可回滚。
- 至少一次部署复合事故同时包含 2 类以上问题，例如迁移失败 + readiness 失败、secret 缺失 + 500、负载突增 + provider 429；完成止损/回滚和复盘。

## J11-05 可观测与持续评估

资料：

- LangSmith 或 Langfuse 文档
- 呼应阶段 10 的评估内容

要做：

- 给 `product_flagship` 接入产品级 tracing：能看到每一步 LLM / 工具调用、token 消耗、耗时；另一个旗舰继续通过 E10 adapter 与 Gate trace 保留回归证据，不复制完整线上观测栈。
- 接 E10 的版本化评估集与 baseline，记录组件/端到端质量、token/成本、p50/p95、错误率和安全分组；配置离线回归门禁。
- 对线上 trace 做脱敏、采样和异常分组；把真实失败样例回灌离线 dataset，并演示一次“发现问题 → 修复 → 回归 → 上线”的闭环。
- 建立 logs/metrics/traces 的 request/run 关联与最小 dashboard/告警；演练一次 provider 429、DB/Redis 下线、队列积压、SSE 中断或成本突增引发的复合事故。
- 事故处置顺序必须包含先止损/降级/回滚，再定位和修复；最后写简短 postmortem 与可执行 runbook。

问答：

1. 没有 tracing 时，Agent 出错为什么很难排查？
2. 你会用哪些指标衡量一个应用型 Agent 的好坏？
3. 怎么构造能暴露问题的失败样例？

通过标准：

- 能展示一次完整 trace + 一份评估结果。
- 能比较两个版本并证明没有关键分组回归；trace 不泄露 API key、token、PII 或完整敏感文档。
- 告警能被真实触发，且能用日志、指标和 trace 关联到根因；修复后回归集、smoke 和关键 SLO 恢复。

## J11-06 作品集组合（2 个旗舰 + 1 个小项目）

要做：

- 整理成“1 个小而完整 + 2 个旗舰”而不是 3–5 个都重做：
  1. 小项目：结构化信息抽取工具（阶段 2，轻量 README + 测试）。
  2. 旗舰一：`code/stage6/engineering_docs_rag/` 工程文档 RAG 助手（LangChain 主项目，FastAPI、引用、技术/业务指标、可复现部署；只有被选为 `product_flagship` 时才要求 Vue 与公网产品）；默认使用公开或脱敏的 API 文档、README、ADR、runbook 和排障资料，不以个人知识库作为业务题目。
  3. 旗舰二：`code/stage8/incident_change_review_agent/` 故障诊断与变更评审 Agent（LangGraph 主项目，持久工作流、HITL、受控多 Agent 对照、trace、失败恢复与可复现 API/demo；只有被选为 `product_flagship` 时才要求正式 Vue 与公网产品）；A4 只作为已 PASS 的手写 Agent Loop 参照，不复制为新研究 Agent。
- 每个项目写清楚：为谁解决什么流程问题、基线是什么、用了哪些技术、难点、取舍和指标结果；没有改善的指标也要解释原因和下一实验。
- 已要求的真实迭代中，至少一次由使用者反馈或明确标注的模拟需求变更触发：说明原流程哪里不便、验收条件怎样改变，在现有旗舰做最小修改并回归验证；保留到已有 issue/PR 或设计记录，不另建课程或反馈管理系统。助手整理记录，用户亲自作影响行为的取舍；模拟反馈不冒充真实客户验证。
- 每个旗舰附：架构/数据流/信任边界图、版本化评估报告、负载报告、威胁模型、失败复盘、CI 状态和可复现部署说明；至少记录一次真实迭代前后对比。
- 冻结的 `product_flagship` 展示 Python/FastAPI Agent 后端与 Vue 前端的真实集成边界（SSE/HTTP、认证、系统出错时怎样返回结果、任务状态）；另一个旗舰保留可复现 API/demo、完整评估和部署说明。只把项目中已经验证的部分写成差异化，不引入第二套后端技术栈。

通过标准：

- `product_flagship` 必须「带前端 + 部署上线」，另一个至少有可复现 API/demo、容器启动方式和完整评估，不是只能在终端跑的脚本；两个项目不得各建一套正式前端/公网发布链。

## J11-07 简历与岗位匹配

要做：

- 按目标 JD（大模型应用 / Agent 应用开发）写一版简历；既往工作经历如实保留，项目主线突出 `Python/FastAPI + Vue + Agent/RAG` 的完整应用落地证据。
- 按 `tracker/job-readiness.md` 做双轨样本：4–6 条京东/腾讯等大厂岗位校准工程上限；另收集恰好 10 条当前在招且满足硬门槛的岗位，用于计算真实匹配率和差距。
- 这不是 W19 才第一次做：W6、W12、W16、W19 都更新双轨审计；W19 负责把累计证据收束进简历。Java/C++、学历或年限不匹配的大厂岗位只能作为标杆，不能写成“已满足”。
- BE5-Gate 完成最小部署后做一次轻量求职材料校准：把新证据写成项目描述，并拿 2–3 条 `HARD_ELIGIBLE` 岗位检查缺口；它不替代 W12 正式双轨审计，也不要求证据不足时强行投递。

问答：

1. 如何用可验证的 Python/FastAPI Agent 项目说明转型能力，而不是只靠既往岗位名称？
2. JD 里高频出现但你还没有的技能有哪些？打算怎么补？
3. 简历里每个项目，能不能对应到 JD 的某一条要求？

通过标准：

- 简历每个项目都能对应 JD 的一个具体要求；有一份「差距清单」。

## J11-08 面试准备

要做：

- 算法：主线先完成 50–70 道高质量题（数组 / 字符串 / 哈希 / 双指针 / BFS-DFS），W4 起每个内容块至少“3 道新题 + 1 道旧错题重做”；W4 无旧题时做第 4 道新题，同一块顺延超过 7 个自然日时追加旧题复测，100–150 作为投递期继续累计的长期目标。
- 系统设计：复用 BE5/R6/G8 持续维护的设计包，分别对「RAG 问答服务」「多轮可恢复 Agent」做一次 30 分钟限时设计，覆盖 API、数据模型、容量/SLO、缓存/队列、降级、安全、成本和 ADR。
- AI 八股：RAG 流程、向量检索原理、Agent 循环（ReAct）、幻觉与防护、上下文 / 记忆管理、评估指标、MCP 是什么。

问答：

1. 把你自己某个项目，从「请求进入」到「返回结果」的全链路讲一遍。
2. 你的 Agent 在哪一步最容易出错 / 产生幻觉？怎么缓解？
3. 如果要把 demo 扩成支撑一万用户的服务，你会先改哪里？

通过标准：

- 能口述讲清自己每个项目的架构和取舍；能在 30 分钟内完成一题系统设计并应对追问；能现场写出中等难度算法题。

## J11-Gate 求职冲刺关

产出：

- 一个公开作品集（GitHub + 至少一个可点开的 demo 链接）。
- 一版针对应用岗的简历。
- 一份面试问答自测（算法 + 系统设计 + AI 八股）。

必须回答：

1. 你最能打的一个项目是哪个？它证明了你哪几项能力？
2. 对照目标 JD，你目前最大的短板是什么？补救计划是什么？
3. 选一个项目，完整讲清从用户请求到最终输出的全链路。

通过标准：

- 作品集里至少有一个可上线访问的 demo。
- 简历项目与目标 JD 对得上。
- 能完整、自信地讲清至少一个项目的端到端实现。
- 两个旗舰中至少一个达到 `JOB_EVIDENCE`；另一个至少达到 `COURSE_PASS` 且把未形成岗位证据的缺口写清。
- Python 后端/API、测试与评估、部署与运维、安全与权限这四个必达能力域都达到 `JOB_EVIDENCE`，并由另一工具完成交叉复核；不能因一个项目或一个能力域很强就代表整体通过。
- 至少一个主旗舰的 Agent/workflow 能力达到 `JOB_EVIDENCE`；若主投 RAG 岗，RAG 也必须达到 `JOB_EVIDENCE`，若主投 durable Agent 岗，则 LangGraph/恢复能力必须达到 `JOB_EVIDENCE`。
- 通过一次不看原笔记的模拟面试后，才把对应能力升级为 `INTERVIEW_READY`；其他未到该级别的项必须在差距清单中如实保留。

---

# 补充与强化项（应用岗 2026 对齐）

对照 2026 年「大模型应用 / Agent 应用开发」岗的招聘要求，原阶段 0-10 还差下面几块。这些不另起大阶段，而是挂载到对应阶段、按 `weekly-plan.md` 的周次穿插完成。优先级从高到低。

## S-01 多厂商模型切换

挂载：A4-Gate 后、J11-02 前；按真实项目依赖选择接入点，不阻塞当前 G8/R6。

要做：

- 先抽出统一的 `ModelClient`/provider 配置边界，让业务代码不依赖某家 SDK 的字段；DeepSeek 作为当前默认实现。
- 再接至少第二个真实 provider（OpenAI、Claude、OpenRouter 或本地 Ollama 任选其一），用同一组问题记录成本、延迟、输出和 tool calling/structured output 差异。没有第二家凭据时可先完成适配器与 mock 测试，但真实对比未跑前不判完整 PASS，也不阻塞主线 Gate。
- 顺带补结构化输出「严格档」：用支持 `json_schema`/strict 严格模式的厂商真跑一次严格 Schema 输出，与 DeepSeek `json_object` 软约束对比（PR2-04 只跑过软约束档）。
- 建统一错误分类：timeout、429/`Retry-After`、5xx/outage、认证失败、余额/额度耗尽、context overflow 和坏请求；只有可重试错误进入有上限的指数退避 + jitter，认证/坏参数等快速失败。
- 明确单次/总 timeout、fallback/降级、熔断与单请求/日成本上限；用 mock/fault injection 验证等待策略、重试次数、日志、fallback 和幂等边界。

为什么：JD 普遍要求「会用多家模型」，只会调一个 OpenAI 是减分项。

通过标准：改一个配置就能切换厂商；能说出各自适合什么场景；provider 429/outage/context overflow/余额耗尽不会形成重试风暴或无上限成本，并有可重复故障测试。

## S-02 生产向量检索

挂载：阶段 6（R6-02/R6-Gate）。与 R6 共用真实产物，但保留独立任务状态；正式检查必须分别对照本节标准写回，不能永久停在 TODO 或被“隐含覆盖”。

要做：

- Chroma/FAISS 只用于理解或 baseline；旗舰主线使用 pgvector（串联 B0-03/BE5-04），目标 JD 明确要求时再用 Qdrant/Milvus 做对照。
- 不要只手写余弦相似度循环；必须覆盖 metadata/权限 filter、hybrid search、rerank、增量更新/删除和检索指标。

为什么：JD 把「向量数据库」列为最常部署的能力之一。

通过标准：能从空库迁移并完成写入/检索/更新/删除，计算 Recall@k 或 MRR，与 baseline 对比，并说明 chunk、embedding、filter、top-k、hybrid、rerank 的作用。

## S-03 上下文工程

挂载：阶段 2 之后 / 阶段 4 之前。

资料：Hello-Agents 第 9 章 上下文工程。

要做：

- 写笔记 + 一个小实验：对比「把全部历史塞进去」与「裁剪 / 摘要 / 检索式上下文」，看 token 消耗和效果差异。

为什么：2026 年范式正从 Prompt Engineering 转向 Context Engineering，Agent 失败大多来自上下文管理而非模型本身。

通过标准：能解释上下文窗口的取舍，能给出一种压缩 / 筛选上下文的做法。

## S-04 受控多 Agent 协作

挂载：阶段 7（D7-02）定义取舍，阶段 8 的 `code/stage8/incident_change_review_agent/` 提供真实实现与 Gate 证据。

要做：

- 先保留同一业务、同一数据集和同一指标的单 Agent baseline；只有发现上下文隔离、职责专门化或并行调查的可定位瓶颈，才拆分协作者。
- 在故障诊断项目中实现一条最小受控协作链，例如 coordinator 只负责分派和停止、diagnostic worker 只读取证、risk reviewer 独立检查证据与变更风险；每个 handoff 使用可验证 schema，不依赖自然语言猜测隐含状态。
- 明确共享 state、角色私有上下文、最大 handoff/step、总 token/成本预算、失败/超时/循环停止和人工升级；危险变更仍受 G8-03 的 sandbox、interrupt 与幂等约束。
- 用单 Agent 与多 Agent 对照质量、主要根因覆盖、冲突/遗漏、延迟、token/成本和失败类型；多 Agent 没有净收益时回退，不为展示框架而保留。

为什么：部分高工程标准岗位明确要求 multi-agent orchestration，但当前可投样本频率可能低于主线阈值；它的准入依据是复杂任务中的上下文隔离、独立复核和可控协作价值，而不是框架热度。

通过标准：能展示带类型约束的角色交接格式、共享/私有 state、冲突处理、停止/升级和完整 trace；同一评估集上有单 Agent 对照，能用证据说明保留、限制或回退多 Agent 的决定。

## S-05 安全与 Guardrails

挂载与判定：A4-Gate 已完成最小安全基线；R6-Gate 负责 ACL/间接注入，D7-03 负责 Memory/PII/poisoning，M9-Gate 负责 OAuth/scope/audience/恶意 server，J11-05 后完成跨层威胁模型与至少 10 条综合攻击回归。只有这些切片全部有证据时，才在 `J11-06/FINAL-Gate` 前正式判定 S-05。

要做：

- A4-Gate 先加：输入/参数校验、工具白名单、步数/重试上限、危险操作人工确认。
- 阶段 7 再做威胁建模：直接/间接 prompt 注入、工具输出注入、SSRF、路径逃逸、数据外泄、PII/secret、过度授权、越权/多租户隔离、memory/RAG poisoning、恶意 MCP/依赖供应链。
- 在用户输入、模型输出、工具参数、权限、网络、存储、日志和人工确认各层明确谁负责兜底；模型判断不能替代代码授权。
- 至少写 10 条攻击测试，包含诱导读取沙箱外文件、网页/文档间接注入、跨用户检索、恶意 URL、敏感日志和危险工具；验证防护与审计生效。
- MCP 阶段补 OAuth/token audience/scope/PKCE 与禁止 token passthrough；不自己实现不安全认证协议。

为什么：应用岗会把 Agent 接真实工具和数据，安全是高频面试考点，也是线上事故主要来源。

通过标准：有数据流/信任边界图和威胁模型；危险、注入、越权与外泄测试被正确拦截或降权处理；能说明残余风险和为什么不存在“一个 prompt 解决所有安全问题”。

## S-06 微调 vs RAG vs Prompt 的判断

挂载：`R6-03` 正式对照完成后（只需概念与项目选型判断，不要求动手微调）；若当时未收口，最迟在 `E10-02` 前补齐。

要做：

- 写一页笔记：说明微调（SFT/LoRA）、RAG、Prompt 三者各自的适用场景、成本和何时选哪个。

为什么：应用岗不要求你会做微调，但面试常问「这个需求该用 RAG 还是微调」，要能判断和表达，避免盲目追训练。

通过标准：能用具体例子说清三选一的依据。

## S-07 async 基础与异步接口（已吸收进阶段 5.5）

原 S-07 的半天任务不足以支撑岗位要求，现不再单独判定。其目标由 `BE5-02 asyncio、并发与可靠 I/O`、`BE5-03 FastAPI/Pydantic v2` 和 `BE5-Gate` 完整承担；旧链接可把本节当迁移索引，状态以 BE5 各任务为准。

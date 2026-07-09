# AI Agent 开发学习追踪清单

根目录：`C:\Users\26823\Desktop\AI-Agent-Learning`

本清单用于每天记录学习、提交代码、回答检查题，并由批改者（Claude / codex 均可）判定是否通过。以后所有代码、笔记、源码阅读、完成情况都放在这个文件夹里。

## 文件夹约定

| 路径                                   | 用途                           |
| -------------------------------------- | ------------------------------ |
| `tracker/ai-agent-learning-tracker.md` | 总学习路线、任务清单、通过标准 |
| `tracker/progress.md`                  | 总进度表，只记录每项状态       |
| `daily/`                               | 每天一份学习打卡               |
| `code/`                                | 你自己写的练习代码             |
| `notes/`                               | 视频、文档、源码阅读笔记       |
| `repos/`                               | 参考仓库源码                   |
| `resources/`                           | 补充资料、截图、PDF、运行记录  |

代码文件采用“即时建骨架”：未来任务只在本清单中预留目标路径，不提前批量生成 `code/` 文件。真正开始动手或 Gate 设计准备时，先核对当天资料和官方 API，再创建只含 TODO 的当前任务骨架；PASS 后保留用户完成的代码。

已放入 `repos/` 的参考仓库：

- `hello-agents`：Datawhale《从零开始构建智能体》
- `Agent-Learning-Hub`：Datawhale Agent 学习路线资料库
- `HelloAgents-feature-branch-1`：jjyaoao/HelloAgents 指定分支
- `agentic-design-patterns`：Agentic Design Patterns 中文/双语内容
- `agents-course`：Hugging Face Agents Course

## 判定规则

- `PASS`：代码能运行，能独立解释核心概念，问答没有明显漏洞。
- `RETRY`：代码能跑但理解不稳，或答案不完整，需要补答。
- `FAIL`：代码未跑通，概念混淆，或明显复制材料但不能解释。

强制顺序关卡没通过时，不进入后续同类阶段：

- `P0-Gate` Python 基础闯关
- `L1-Gate` 大模型 API 闯关
- `T3-Gate` Tool Calling 闯关
- `A4-Gate` 最小 Agent 闯关
- `R6-Gate` RAG 闯关
- `G8-Gate` LangGraph 闯关
- `M9-Gate` MCP 闯关
- `FINAL-Gate` 综合项目答辩

从 `A4-Gate` 起，每个 Gate 的通过标准**额外包含：自建 10–20 条测试用例、可重复运行的评估脚本、通过率与失败案例**（把评估习惯前置，呼应 E10-01 与 J11-05 可观测）。同时从 A4-Gate 开始记录最小结构化日志（模型/工具/耗时/错误/步数），危险或不可逆工具必须有人为确认点；完整 tracing 平台仍留到 J11-05。

工程基础不再作为进入阶段 1 的整块前置。`B0-01` 到 `B0-04` 改为穿插补课项：P0-Gate 通过后可以先进入 `L1` 大模型 API；后续遇到环境、HTTP、数据库、Docker、Memory、RAG、本地服务部署时，再补对应 B0 项。

`B0-Gate` 改为项目化整合关卡：在需要本地多服务、数据库持久化、Docker Compose、长期 Memory/RAG 或可部署 Agent 项目前完成，不再卡住第一次进入 L1/API。

## 每日打卡格式

在 `daily/YYYY-MM-DD.md` 中记录：

```text
日期：
目标学习时长：
实际学习时长：
完成任务编号：
看了哪些视频/哪一集：
读了哪些文档/哪一节：
代码/产物位置：
运行提示：
今日练习题（当天现出，不预埋）：
我的作答：
遇到的问题：
我最不确定的点：
希望复核/检查：
批改判定：
当天进度小结：
总进度小结：
对问题/不确定点的解释：
问答点评与补充：
超前内容提示：
补救任务：
复核判定（另一工具交叉复核，默认留空）：
```

字段以 `daily/TEMPLATE.md` 为准（两处同步维护）。

说明：批改者检查时会根据代码/产物位置实际运行代码并验证结果。只有当代码不是默认入口、需要特殊参数、需要先启动服务或配置环境变量时，才填写“运行提示”。

`当天进度小结`、`总进度小结`、`对问题/不确定点的解释`、`问答点评与补充`、`超前内容提示` 由批改者（Claude / codex 均可）检查后填写；`复核判定` 默认留空，留给**另一个**工具交叉复核（Claude 批改 → codex 复核，反之亦然）。遇到的问题如果属于后续阶段内容，不要求当天掌握，只标注应该学到哪个任务或阶段再深入。

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

- 阅读规则：中文文档优先；英文官方文档只在中文资料看不懂、命令参数不确定、或需要核对版本时再查。
- Linux 文档：[Linux 命令大全（菜鸟教程）](https://www.runoob.com/linux/linux-command-manual.html)、[Missing Semester 中文版：Shell 入门](https://missing-semester-cn.github.io/2026/course-shell/)
- Linux 视频：[MIT Missing Semester 2020 - B站双语字幕](https://www.bilibili.com/video/BV1w7411477L/)、[Shell Tools and Scripting - B站双语字幕](https://www.bilibili.com/video/BV1xa4y1g7sZ/)
- 网络文档：[MDN HTTP 概述（中文）](https://developer.mozilla.org/zh-CN/docs/Web/HTTP/Guides/Overview)、[MDN HTTP 标头（中文）](https://developer.mozilla.org/zh-CN/docs/Web/HTTP/Reference/Headers)、[MDN HTTP 响应状态码（中文）](https://developer.mozilla.org/zh-CN/docs/Web/HTTP/Reference/Status)、[Cloudflare：什么是 DNS（中文）](https://www.cloudflare.com/zh-cn/learning/dns/what-is-dns/)
- 网络视频：[湖科大教书匠《计算机网络微课堂》](https://www.bilibili.com/list/ml962700202?bvid=BV1c4411d7jb&oid=64605483)、[Computer Networking: A Top-Down Approach - YouTube playlist](https://www.youtube.com/playlist?list=PL1ya5dD_M8uX-BLUF1FEvUNsYWQL5_l0O)
- 数据库文档：[SQLite 5 分钟快速上手（中文）](https://sqlite.ac.cn/quickstart.html)、[SQLite SQL 语言（中文）](https://sqlite.ac.cn/lang.html)、[PostgreSQL 教程（中文）](https://postgresql.ac.cn/docs/current/tutorial.html)、[PostgreSQL SQL 语言（中文）](https://postgresql.ac.cn/docs/current/sql.html)
- 数据库视频：[尚硅谷 MySQL 入门到高级](https://www.bilibili.com/video/BV1eC4y1M7c3/)、[CMU Intro to Database Systems - YouTube](https://www.youtube.com/@CMUDatabaseGroup)
- Docker 文档：[Docker 中文文档：Docker 教程](https://dockerdocs.xuanyuan.me/)、[Docker Compose 快速入门（中文）](https://docker.cadn.net.cn/manuals/compose_gettingstarted)、[Docker 官方文档（英文备查）](https://docs.docker.com/get-started/)
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
- 建表 `learning_logs`，字段至少包含：`id`、`date`、`topic`、`minutes`、`status`、`note`。
- 支持新增、查询最近 7 条、按 topic 统计总时长、更新状态、删除一条测试数据。

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
- Docker 官方英文文档：只在中文文档和本机 Docker Desktop 行为不一致时备查。
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

任务：

- 做 `code/stage0_5/b0_gate_local_stack/`。
- 用 Docker Compose 启动 PostgreSQL 和一个 Python CLI 程序。
- Python 程序支持写入学习记录、查询最近记录、按主题统计时长。
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
- 配 `eval_cases.json`：10 条正常 + 3 条失败 + 1 条危险输入；再写可重复运行的评估入口，记录通过率与失败案例（面试讲「可靠性」的真材料）。

必须回答：

1. 工具注册表如何设计？
2. Agent 如何选择工具？
3. 如何避免危险工具调用？
4. 工具结果太长如何处理？

通过标准：

- 至少真跑计算、文件、外部 API 各 1 次，并能看到真实 `tool_calls` 与回填后的最终回答。
- 无工具问题不会被强迫调用工具；危险路径在客户端/工具层被拒绝。
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

资料：

- Hello-Agents：第 2 章、第 3 章
- Hugging Face：`unit1/what-are-llms.mdx`、`messages-and-special-tokens.mdx`

要做：

- 写 `notes/stage4/a4_02_llm_agent_basics.md`。

问答：

1. LLM 在 Agent 中扮演什么角色？
2. 消息格式为什么重要？
3. 幻觉会如何影响 Agent？

通过标准：

- 能解释 LLM 不是执行器。

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

- 做 `code/stage4/a4_gate_research_summary_agent.py`。
- 输入主题或资料路径，能调用工具、总结、反思修正。
- 配 `eval_cases.json`：10 条正常 + 3 条失败 + 1 条危险输入，并用 `run_evals.py`/`pytest` 可重复执行、记录通过率与失败案例。
- 记录最小结构化日志：每步模型调用、工具名、耗时、错误和累计步数；设置 max_steps、timeout、重试上限。
- 对写文件、执行命令等高风险/不可逆动作设置人工确认；本关至少演示一次允许/拒绝分支。

必须回答：

1. 你的 Agent 循环是什么？
2. 什么时候停止？
3. 工具失败时如何恢复？
4. 哪一步最容易产生幻觉？

---

# 阶段 5：HelloAgents 源码学习

目标：理解一个 Agent 框架如何组织 LLM、Agent、Tool、Memory、Protocol。

主资料：

- `repos/HelloAgents-feature-branch-1`
- `repos/hello-agents/docs/chapter7/第七章 构建你的Agent框架.md`

## H5-01 跑通指定分支

资料：

- `HelloAgents-feature-branch-1/README.md`
- `docs/tutorials/CONFIGURATION.md`
- `examples/chapter07_basic_setup.py`

要做：

- 在 `notes/stage5/h5_01_run_log.md` 记录安装、运行命令、错误和结果。

问答：

1. 为什么我们用 `feature-branch-1`？
2. 这个框架的入口示例在哪里？
3. 配置文件/环境变量承担什么职责？

通过标准：

- 至少跑通一个 example，或清楚记录无法跑通的错误。

## H5-02 Core 层阅读

资料：

- `hello_agents/core/agent.py`
- `hello_agents/core/llm.py`
- `hello_agents/core/message.py`
- `hello_agents/core/config.py`

要做：

- 不逐文件抄源码；选一个已跑通 example，从入口开始追到 Agent、LLM、Message/Config，写 `notes/stage5/h5_02_core_reading.md` 记录一条真实调用链和关键行号。

问答：

1. Agent 基类负责什么？
2. LLM 封装层为什么有必要？
3. Message 抽象解决什么问题？

通过标准：

- 能画出 Core 层关系。

## H5-03 Agents 层阅读

资料：

- `hello_agents/agents/simple_agent.py`
- `hello_agents/agents/react_agent.py`
- `hello_agents/agents/plan_solve_agent.py`
- `hello_agents/agents/reflection_agent.py`

要做：

- 精读 `simple_agent.py` 与当前马上要用的一个 Agent（默认 `react_agent.py`）；Plan/Reflection 只定位控制流差异。写 `notes/stage5/h5_03_agents_compare.md`，不做重复概念摘抄。

问答：

1. simple/react/plan/reflection 的差异是什么？
2. 哪种 Agent 最适合工具任务？
3. 哪种 Agent 最适合写作改进？

通过标准：

- 能用表格对比 4 类 Agent。

## H5-04 Tools 层阅读与新增工具

资料：

- `hello_agents/tools/base.py`
- `hello_agents/tools/registry.py`
- `hello_agents/tools/builtin/calculator.py`
- `hello_agents/tools/builtin/rag_tool.py`

要做：

- 新增一个工具，放入 `code/stage5/custom_tool/` 或框架本地实验分支。

问答：

1. 工具注册流程是什么？
2. 工具输入输出如何约束？
3. 如何定位工具没有被调用的问题？

通过标准：

- 自定义工具能被 Agent 调用。

## H5-05 Memory、Context、Protocol 阅读

资料：

- `hello_agents/memory/`
- `hello_agents/context/builder.py`
- Datawhale Hello-Agents 第 8-9 章
- `hello_agents/protocols/mcp/` 只看入口和目录关系，真实 MCP 深读留到阶段 9，避免重复学习。

要做：

- 写 `notes/stage5/h5_05_memory_protocol.md`。

问答：

1. Memory 和消息历史有什么区别？
2. Context builder 解决什么问题？
3. MCP 是框架、协议，还是工具？

通过标准：

- 能区分 Memory、Context、Protocol。

## H5-Gate 源码学习闯关

任务：

- 用真实 example 说明一次请求从 Agent 进入，到调用 LLM/Tool，再回到最终输出的路径；新增的自定义工具必须能在这条链路里被实际调用。此关重点是“追通一条链路 + 改一处”，不是读完所有目录。

必须回答：

1. 入口类是哪一个？
2. 工具如何注册和执行？
3. 消息如何组织？
4. 你最想重构哪一处，为什么？

---

# 阶段 6：RAG / 知识库

目标：让 Agent 基于资料回答问题，并给出引用来源。

主资料：

- Datawhale Hello-Agents 第 8 章
- Hugging Face Agents Course：Unit 3 Agentic RAG
- LlamaIndex / LangChain RAG 文档

## R6-01 文档读取与切分

资料：

- Hello-Agents：`docs/chapter8/第八章 记忆与检索.md`
- Hello-Agents 代码：`code/chapter8/04_RAGTool_MarkItDown_Pipeline.py`
- Hugging Face：`unit3/agentic-rag/introduction.mdx`

要做：

- 写 `code/stage6/r6_01_chunking.py`。

问答：

1. 为什么不能整篇文档直接塞给模型？
2. chunk 太大和太小分别有什么问题？
3. overlap 有什么作用？

通过标准：

- 能展示切分结果。

## R6-02 Embedding 与检索

资料：

- Hello-Agents 代码：`code/chapter8/10_RAG_Pipeline_Complete.py`
- Hugging Face：`unit3/agentic-rag/tools.mdx`

要做：

- 写 `code/stage6/r6_02_retrieval.py`。

问答：

1. embedding 表示什么？
2. 向量检索为什么能找相似内容？
3. 检索不准时可以调哪些地方？

通过标准：

- 能返回相关片段。

## R6-03 带引用问答

资料：

- Hello-Agents 代码：`code/chapter8/11_Q&A_Assistant.py`
- Hugging Face：`unit3/agentic-rag/agentic-rag.mdx`

要做：

- 写 `code/stage6/r6_03_cited_qa.py`。

问答：

1. RAG 如何减少幻觉？
2. 为什么必须返回引用？
3. 资料里没有答案时怎么回答？

通过标准：

- 有引用。
- 不对资料外问题胡编。

## R6-Gate RAG 闯关

任务：

- 做 `code/stage6/r6_gate_personal_kb.py`。
- 功能 Gate 先导入至少 3 篇资料，支持问答、引用、无答案拒答；进入作品集打磨时扩到至少 20 篇或 50 页、多种长度/格式，避免只证明玩具样例能跑。
- 每个 chunk 保留来源、标题、页码/段落等 metadata；重复导入不产生重复数据。
- 配 `eval_cases.json`：10 条正常 + 3 条失败 + 1 条危险输入，并分别记录“检索是否命中正确资料”和“最终答案/引用是否正确”，不要只看一句总通过率。
- 基础档完成向量检索；召回不足时再做 metadata filter、hybrid search 或 rerank 中至少一项对照实验，不要求一次堆齐全部技术。

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

## D7-02 Agent 核心模式

资料：

- Chapter 4 Reflection
- Chapter 5 Tool Use
- Chapter 6 Planning
- Chapter 7 Multi-Agent Collaboration

问答：

1. Tool Use 和 RAG 的区别是什么？
2. Planning 适合所有任务吗？
3. 多 Agent 最大风险是什么？

产出：

- `notes/stage7/d7_02_core_agent_patterns.md`

## D7-03 可靠性与工程模式

资料：

- Chapter 8 Memory Management
- Chapter 10 MCP
- Chapter 12 Exception Handling and Recovery
- Chapter 14 RAG
- Chapter 18 Guardrails/Safety Patterns
- Chapter 19 Evaluation and Monitoring

问答：

1. Memory 和上下文历史有什么区别？
2. Guardrails 防什么风险？
3. Evaluation 应该评估什么？

产出：

- `notes/stage7/d7_03_reliability_patterns.md`

## D7-Gate 设计模式闯关

任务：

- 写 `notes/stage7/d7_gate_architecture_review.md`。
- 选择你已做的一个 Agent，说明用了哪些模式、没用哪些模式、为什么。

通过标准：

- 不能把所有模式都堆上去。
- 能说明取舍。

---

# 阶段 8：LangGraph / 可控工作流

目标：做有状态、可控、可恢复的 Agent 工作流。

主资料：

- Hugging Face Agents Course：Unit 2 LangGraph
- Datawhale Hello-Agents 第 6 章 LangGraph
- LangGraph 官方文档

## G8-01 LangGraph 适用场景

资料：

- Hugging Face：`unit2/langgraph/when_to_use_langgraph.mdx`
- Datawhale：`docs/chapter6/第六章 框架开发实践.md`

问答：

1. 为什么有些 Agent 不适合纯 while 循环？
2. LangGraph 的 state 解决什么问题？
3. 什么任务不需要 LangGraph？

产出：

- `notes/stage8/g8_01_when_to_use_langgraph.md`

## G8-02 第一个 Graph

资料：

- Hugging Face：`unit2/langgraph/first_graph.mdx`
- Hugging Face：`unit2/langgraph/building_blocks.mdx`

要做：

- 写 `code/stage8/g8_02_first_graph.py`。

问答：

1. 节点是什么？
2. 边是什么？
3. state 如何在节点之间流动？

通过标准：

- graph 能运行。

## G8-03 文档分析 Agent

资料：

- Hugging Face：`unit2/langgraph/document_analysis_agent.mdx`

要做：

- 写 `code/stage8/g8_03_document_analysis_agent.py`。

问答：

1. 条件边如何决定下一步？
2. 工具结果如何写回 state？
3. 如何防止无限执行？

通过标准：

- 有终止条件。
- 能输出执行轨迹。

## G8-Gate LangGraph 闯关

任务：

- 做 `code/stage8/g8_gate_research_graph.py`。
- 输入主题，检索/整理/生成报告，过程可追踪。
- 配 `eval_cases.json`：10 条正常 + 3 条失败 + 1 条危险输入；每次改完跑一遍、记录通过率与失败案例（面试讲「可靠性」的真材料）。

---

# 阶段 9：MCP 与外部工具连接

目标：理解 Agent 如何连接文件、数据库、浏览器、企业工具。

主资料：

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

## M9-02 本地 MCP Server

资料：

- HelloAgents：`hello_agents/protocols/mcp/server.py`
- HelloAgents：`hello_agents/protocols/mcp/client.py`

要做：

- 写 `code/stage9/m9_02_local_mcp_server.py`。
- 暴露 1-2 个安全工具。

问答：

1. 工具如何被发现？
2. 权限如何控制？
3. 如何记录工具调用日志？

通过标准：

- 客户端能发现工具。

## M9-03 Agent 调 MCP

要做：

- 写 `code/stage9/m9_03_agent_mcp_client.py`。

问答：

1. MCP 和 LangGraph 是同一类东西吗？
2. MCP 和 Tool Calling 的关系是什么？
3. MCP 工具失败如何反馈给 Agent？

通过标准：

- Agent 能真实调用 MCP 工具。

## M9-Gate MCP 闯关

任务：

- 做 `code/stage9/m9_gate_file_summary_agent.py`。
- Agent 通过 MCP 读取指定目录文件并总结。
- 配 `eval_cases.json`：10 条正常 + 3 条失败 + 1 条危险输入；每次改完跑一遍、记录通过率与失败案例（面试讲「可靠性」的真材料）。

---

# 阶段 10：评估、监控与综合项目

目标：做一个可展示、可复盘、可评估的 Agent 项目。

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

- `notes/stage10/e10_01_evaluation_plan.md`

## E10-02 综合项目设计

候选项目：

- 个人知识库问答 Agent
- 文件整理与总结 Agent
- Deep Research 简化版
- 旅行规划 Agent
- 编程学习助教 Agent

必须回答：

1. 这个项目为什么需要 Agent，而不是普通脚本？
2. 它需要哪些工具？
3. 是否需要 RAG、Memory、Planning、LangGraph、MCP？
4. 失败时如何降级？
5. 如何评估效果？

产出：

- `notes/stage10/e10_02_project_design.md`

## FINAL-Gate 综合项目答辩

产出：

- `code/final_project/`
- `code/final_project/README.md`
- `notes/stage10/final_defense.md`

通过标准：

- 从零安装可运行。
- README 写清楚。
- 至少 20 个测试样例，覆盖正常、失败、边界和危险输入；评估脚本可重复运行并输出分项通过率。
- 有失败案例复盘。
- 能现场解释核心代码。

答辩问题：

1. 核心 Agent 循环是什么？
2. 工具调用链路是什么？
3. 上下文如何管理？
4. 如何控制成本、安全和权限？
5. 下一步最值得改进什么？

---

# 阶段 11：就业准备与作品集（应用岗方向）

目标：把前面学到的东西沉淀成「可展示、可上线、面试能讲清楚」的作品集和求职材料，针对「大模型应用 / Agent 应用开发」岗。

你的背景与定位（普通本科 + 在职 .NET 后端 + 会 Vue，目标应用岗）：

- 优势：已有正式开发经验和全栈雏形。「传统开发转 AI 应用」是最主流、最可行的转型路径，应用岗看重「能把大模型做成真实产品」，正好契合你。
- 差异化：你会前端，可以做出「带界面、有后端服务、真上线」的完整 Agent 应用，这正是大多数自学者交不出来的东西。
- 暂时不碰：应用岗不要求模型训练（SFT/LoRA、PyTorch、分布式训练）。先全部跳过，集中火力在「用大模型搭产品 + 工程落地」。
- 要补的弱项：后端基础（async、HTTP、接口设计）、Docker（你目前没接触）、部署上线、可观测与评估。本阶段会顺带补。

启动时机：

- 不要等阶段 10 学完才开始。从阶段 3/4（能调 API、能做最小 Agent）起就并行启动：每做出一个能跑的东西，就往作品集里沉淀一次。
- 容器化（J11-04）依赖工程基础 `B0-04 Docker`；做这一步前先把 B0-04 补掉。

## J11-01 GitHub 与工程习惯

要做：

- 把 `code/` 里的练习整理成规范的 GitHub 仓库：清晰 `README`、`requirements.txt`、`.env.example`、有意义的提交记录。
- 每个要进作品集的项目都写：解决什么问题、怎么运行、用到哪些技术。

问答：

1. 为什么作品集项目必须有清晰 README 和可复现的运行步骤？
2. 为什么 `.env` 不能提交，但要提交 `.env.example`？
3. 提交记录混乱会给面试官什么印象？

通过标准：

- 一个陌生人能照着 README 从零把项目跑起来。

## J11-02 把 Agent 包成后端服务（FastAPI）

资料：

- FastAPI 官方教程（中文）
- OpenAI / Anthropic SDK 的 async 用法

要做：

- 先把 Agent 调用抽成可复用服务接口，再用 FastAPI 暴露普通 JSON 与 `/chat` 流式接口；主交付接入阶段 6 的 RAG Agent，阶段 4 最小 Agent 可作为更早的轻量联调对象。
- 处理并发、超时、错误返回；区分 4xx（用户输入问题）和 5xx（服务内部问题）。

问答：

1. 同步和 async 在高并发调用 LLM 时差别在哪？为什么 LLM 服务尤其需要 async + 超时？
2. 流式接口（SSE）和普通 JSON 接口在前端消费方式上有什么不同？
3. API Key 等密钥在服务端如何管理？

通过标准：

- 能用 curl 或前端连续调用，返回流式结果，异常输入不让服务崩溃。
- 顺带补齐 async 与接口设计，弥补后端基础。

## J11-03 给 Agent 配前端（用你已会的 Vue）

要做：

- 用 Vue 写一个对话 / 工具调用可视化界面，接 J11-02 的接口。
- 支持：流式显示、展示工具调用过程、展示引用来源（呼应阶段 6 RAG）。

问答：

1. 前端如何消费流式（SSE/fetch stream）输出？
2. 为什么把「工具调用过程」可视化对一个 Agent 产品有价值？
3. 前后端分离时，跨域和密钥应该怎么处理（密钥为什么不能放前端）？

通过标准：

- 一个别人打开浏览器就能用的 Web 应用；发挥你现有 Vue 优势做出差异化作品。

## J11-04 容器化与上线

依赖：

- 先完成 `B0-04 Docker`（你目前没接触过）。

要做：

- 用 `Dockerfile` + `compose.yaml` 把前端、后端、（可选）向量库 / 数据库打包。
- 部署到一个公网可访问地址（便宜云主机 / Railway / Render 等任一）。

问答：

1. image 和 container 有什么区别？
2. 为什么配置要走环境变量而不是写死在代码里？
3. 上线后如果接口报 500，你按什么顺序排查？

通过标准：

- 给出一个别人能直接点开体验的 demo 链接。

## J11-05 可观测与评估

资料：

- LangSmith 或 Langfuse 文档
- 呼应阶段 10 的评估内容

要做：

- 给你的 Agent 接入 tracing：能看到每一步 LLM / 工具调用、token 消耗、耗时。
- 写一份小评估集（10-20 条），记录通过率和失败案例。

问答：

1. 没有 tracing 时，Agent 出错为什么很难排查？
2. 你会用哪些指标衡量一个应用型 Agent 的好坏？
3. 怎么构造能暴露问题的失败样例？

通过标准：

- 能展示一次完整 trace + 一份评估结果。

## J11-06 作品集组合（2 个旗舰 + 1 个小项目）

要做：

- 整理成“1 个小而完整 + 2 个旗舰”而不是 3–5 个都重做：
  1. 小项目：结构化信息抽取工具（阶段 2，轻量 README + 测试）。
  2. 旗舰一：个人知识库 RAG 问答（阶段 6，FastAPI + Vue + 引用 + 评估 + 部署）。
  3. 旗舰二：从 A4-Gate 持续演化到 LangGraph/FINAL 的可控 Agent（工具、安全确认、trace、失败恢复）；不要把 A4、G8、FINAL 拆成三个互不复用的新仓库。
- 每个项目写清楚：解决什么问题、用了哪些技术、难点、你做的取舍。

通过标准：

- 两个旗舰项目至少一个「带前端 + 部署上线」，另一个至少有可复现 API/demo 和完整评估，不是只能在终端跑的脚本。

## J11-07 简历与岗位匹配

要做：

- 按目标 JD（大模型应用 / Agent 应用开发）写一版简历，把 `.NET 后端 + Vue 前端 + AI 项目` 串成「全栈 + AI 应用落地」的故事。
- 收集 10 个目标 JD，逐条对照自己的差距，列出还要补什么。

问答：

1. 你的 .NET 经验如何包装成 AI 应用岗的加分项，而不是「跨行」？
2. JD 里高频出现但你还没有的技能有哪些？打算怎么补？
3. 简历里每个项目，能不能对应到 JD 的某一条要求？

通过标准：

- 简历每个项目都能对应 JD 的一个具体要求；有一份「差距清单」。

## J11-08 面试准备

要做：

- 算法：主线先完成 50–70 道高质量题（数组 / 字符串 / 哈希 / 双指针 / BFS-DFS），每周至少“2 道新题 + 1 道旧错题重做”；100–150 作为投递期继续累计的长期目标，不卡住 W17。
- 系统设计基础：能设计「一个 RAG 问答服务」「一个多轮对话服务」的大致架构。
- AI 八股：RAG 流程、向量检索原理、Agent 循环（ReAct）、幻觉与防护、上下文 / 记忆管理、评估指标、MCP 是什么。

问答：

1. 把你自己某个项目，从「请求进入」到「返回结果」的全链路讲一遍。
2. 你的 Agent 在哪一步最容易出错 / 产生幻觉？怎么缓解？
3. 如果要把 demo 扩成支撑一万用户的服务，你会先改哪里？

通过标准：

- 能口述讲清自己每个项目的架构和取舍；能现场写出中等难度算法题。

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

---

# 补充与强化项（应用岗 2026 对齐）

对照 2026 年「大模型应用 / Agent 应用开发」岗的招聘要求，原阶段 0-10 还差下面几块。这些不另起大阶段，而是挂载到对应阶段、按 `weekly-plan.md` 的周次穿插完成。优先级从高到低。

## S-01 多厂商模型切换

挂载：A4-Gate 后、J11-02 前；不再和 T3-Gate 挤在同一个周末。

要做：

- 先抽出统一的 `ModelClient`/provider 配置边界，让业务代码不依赖某家 SDK 的字段；DeepSeek 作为当前默认实现。
- 再接至少第二个真实 provider（OpenAI、Claude、OpenRouter 或本地 Ollama 任选其一），用同一组问题记录成本、延迟、输出和 tool calling/structured output 差异。没有第二家凭据时可先完成适配器与 mock 测试，但真实对比未跑前不判完整 PASS，也不阻塞主线 Gate。
- 顺带补结构化输出「严格档」：用支持 `json_schema`/strict 严格模式的厂商真跑一次严格 Schema 输出，与 DeepSeek `json_object` 软约束对比（PR2-04 只跑过软约束档）。

为什么：JD 普遍要求「会用多家模型」，只会调一个 OpenAI 是减分项。

通过标准：改一个配置就能切换厂商；能说出各自适合什么场景。

## S-02 真实向量数据库

挂载：阶段 6（R6-02）。

要做：

- RAG 检索改用真实向量库：Chroma 或 FAISS 起步；有余力上 pgvector（顺带串你 B0-03 的 SQL）。
- 不要只手写余弦相似度循环。

为什么：JD 把「向量数据库」列为最常部署的能力之一。

通过标准：能向向量库写入、检索，并说明 chunk、embedding、top-k 的作用。

## S-03 上下文工程

挂载：阶段 2 之后 / 阶段 4 之前。

资料：Hello-Agents 第 9 章 上下文工程。

要做：

- 写笔记 + 一个小实验：对比「把全部历史塞进去」与「裁剪 / 摘要 / 检索式上下文」，看 token 消耗和效果差异。

为什么：2026 年范式正从 Prompt Engineering 转向 Context Engineering，Agent 失败大多来自上下文管理而非模型本身。

通过标准：能解释上下文窗口的取舍，能给出一种压缩 / 筛选上下文的做法。

## S-04 多 Agent 动手

挂载：阶段 7（D7-02）。

要做：

- 做一个最小多 Agent 协作 demo：例如一个 supervisor 分派任务给两个 worker，再汇总结果。不要只停在看概念。

为什么：JD 常要求 multi-agent orchestration（LangGraph / CrewAI / AutoGen）。

通过标准：能展示多 Agent 分工与汇总的完整轨迹，并说明多 Agent 的代价和风险。

## S-05 安全与 Guardrails

挂载：A4-Gate 先做最小安全基线，阶段 7（D7-03）再强化。

要做：

- A4-Gate 先加：输入/参数校验、工具白名单、步数/重试上限、危险操作人工确认。
- 阶段 7 再补：prompt 注入防护、身份/权限边界、敏感信息与输出处理。
- 写一个「被攻击」测试样例（如诱导它读取沙箱外文件或忽略系统指令），验证防护生效。

为什么：应用岗会把 Agent 接真实工具和数据，安全是高频面试考点，也是线上事故主要来源。

通过标准：危险 / 注入输入能被拦下；能说明你在哪几层做了防护。

## S-06 微调 vs RAG vs Prompt 的判断

挂载：阶段 6 或阶段 10（只需概念，不要求动手微调）。

要做：

- 写一页笔记：说明微调（SFT/LoRA）、RAG、Prompt 三者各自的适用场景、成本和何时选哪个。

为什么：应用岗不要求你会做微调，但面试常问「这个需求该用 RAG 还是微调」，要能判断和表达，避免盲目追训练。

通过标准：能用具体例子说清三选一的依据。

## S-07 async 基础与异步接口

挂载：阶段 11 前置（J11-02 之前，约 W9；量：半天～一天）。

要做：

- 学 `async/await`、`asyncio` 最小集：事件循环是什么、`await` 在等什么、和多线程的区别（能用一句人话说清）。
- 用 FastAPI 写一个最小异步接口 + 一个 SSE 流式接口（把 L1-04 的流式从「客户端消费」升级到「服务端提供」）。

为什么：Agent 后端（FastAPI、流式输出、并行调工具）是 async 优先的世界，面试常问；只在 J11-02 里「顺带补」容易夹生。

通过标准：能解释 async 与多线程的区别和各自适用场景；SSE 接口能被 curl/浏览器消费到逐段输出。

## S-08 Microsoft Agent Framework 扫读（可选加分）

挂载：求职期（约 W16；量：半天，可跳过不影响主线）。

要做：

- 以 Microsoft Agent Framework 官方文档 `https://learn.microsoft.com/en-us/agent-framework/overview/` 为主，了解它作为 Semantic Kernel / AutoGen 后继方案如何组织 Agent、Workflow、工具、MCP、状态和遥测；Semantic Kernel 只作为迁移背景对照。当前仍属 preview，重点是建立 .NET 选型表达，不押注具体 API。
- 写半页对照笔记：「.NET 团队要落地 Agent，我会怎么选型」。

为什么：你的差异化故事是「.NET+Vue+AI 全栈」（J11-07），能讲出 .NET 侧生态的人在国内稀缺；纯加分项，不挤主线。

通过标准：能用 3–5 句话讲清 .NET 侧怎么接 Agent，以及自己主线为什么选 Python。

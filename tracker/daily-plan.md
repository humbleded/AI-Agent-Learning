# 每日学习计划（含加班 / 晚归 fallback）

配合 `weekly-plan.md` 使用。核心思想：**工作日做"轻"的（概念、阅读、源码、算法），周末做"重"的（写代码、过 Gate、部署）。** 这样即使工作日加班，损失的也只是轻量任务，主线项目不受影响。

## 一、每天的固定节奏（模板）

工作日（目标 ~2h，弹性）：

- 主块 60–90 分钟：当天的「概念 / 阅读 / 源码」任务。
- 收尾 15–30 分钟：1 道算法题（第 4 周起）/ 复习昨天 / 写几行笔记。

周末（目标各 ~6h，分块防疲劳）：

- 上午 2.5h：动手主任务（写代码 / 过 Gate）。
- 下午 2.5h：继续 + 调试。
- 傍晚 1h：整理笔记、提交 GitHub、更新 `tracker/progress.md`、同步 Obsidian。
- 块与块之间务必休息，别连坐 6 小时。

## 二、加班 / 晚归 fallback 规则（重要，按当天精力选档）

- **满血（≥90 分钟、状态好）**：按当天计划正常做。
- **半血（30–60 分钟、加班累）**：只做「轻量项」——读一节文档 / 看一段视频 / 读一个源码文件 / 1 道简单算法 / 复习昨天的笔记。**绝不在疲惫时硬写 Gate 或新功能代码**（容易写错 + 挫败 + 第二天还要返工）。把动手任务整体顺延到周末。
- **空血（<30 分钟或太累）**：只做两件事——把今天该读的标题 / 摘要扫一遍混个眼熟；在 `daily/` 里写一行「今天加班，顺延 X」。**保住连续性就算赢，不用愧疚。**

配套机制：

- **不固定机动日**：哪天要加班，你提前告诉我，那天就当机动日降档（半血/空血）、吸收顺延、不排硬任务；没特别说的工作日一律按正常排任务、照常出题。
- **周末是找补主力**：工作日掉了 2–3 天，就周六上午先补关键概念再动手。
- **红线：Gate 和项目只在精力好的整块时间做（基本＝周末）。工作日不碰 Gate。**

可以当「轻量项」的事：读书/课程的一节、看一段视频、读 HelloAgents 一个源码文件、刷 1 道 LeetCode easy、整理昨天的笔记或 Obsidian 卡片。
**别在疲惫时做的事**：写 Gate、调试部署、设计新代码结构、debug 复杂报错。

## 三、逐日计划（W1–W4 详细到每天）

资料简称：HA=Hello-Agents 书，HA-code=hello-agents 配套代码，HF=HuggingFace 课程中文版，ADP=Agentic Design Patterns，HAsrc=HelloAgents 源码，Hub=Agent-Learning-Hub，DLAI=DeepLearning.AI，随想录=代码随想录。详细链接见 `learning-resources.md`。

### W1 阶段 0 收尾 → 阶段 1 开端

- 周一（轻 OK）：读 MDN《HTTP 概述》《状态码》；记 3 行笔记。
- 周二：P0-Gate 设计——定 JSON 数据结构、列出要写的函数（只设计不写完）。
- 周三：读 HA 第 1 章《初识智能体》建立大局观；加班则只读 Hub「What is an agent」。
- 周四：预习 OpenAI Quickstart（环境变量、装 SDK、第一次请求长什么样）。
- 周五（轻 OK）：复盘 Python；把 stage0 笔记整理一张卡片进 Obsidian。
- 周六（整块）：写完 P0-Gate（可运行 + ≥3 条测试）→ 闯关；通过后做 L1-01（第一次真正调用大模型）。
- 周日（整块）：L1-02 单轮问答；傍晚提交 GitHub + 更新 progress.md。

### W2 阶段 1 大模型 API

- 周一（轻 OK）：读 OpenAI Text Generation 文档；看 DLAI 对话格式小节。
- 周二：读 HA 第 3 章《大语言模型基础》要点；笔记。
- 周三：学 L1-04 流式输出——读本地样板 `hello-agents/code/chapter4/llm_client.py` + 官方流式文档，弄懂 `chunk`/`delta.content`，动手把 `stream=False` 改成 `True` 跑通逐字输出；加班则只读文档不写代码。
- 周四：L1-03 多轮聊天——设计消息历史结构（伪代码即可）。
- 周五（轻 OK）：读 OpenAI 流式输出文档；顺带补 B0-01 命令行常用命令。
- 周六（整块）：写 L1-03 多轮 + L1-04 流式。
- 周日（整块）：L1-05 参数实验 + L1-Gate CLI chatbot 闯关；更新 progress。

### W3 阶段 2 Prompt + 结构化（含 S-03 上下文工程）

- 周一（轻 OK）：读 DLAI Guidelines + OpenAI Prompt Engineering。
- 周二：PR2-01 写 3 个 prompt 对比（动手但轻）。
- 周三：读 HA 第 9 章《上下文工程》上半（S-03 资料）。
- 周四：读 HA 第 9 章下半；设计 S-03 小实验（全量 vs 裁剪上下文）。
- 周五（轻 OK）：读 OpenAI Structured Outputs 文档。
- 周六（整块）：PR2-02 摘要 + PR2-03 分类（≥15 样例）。
- 周日（整块）：PR2-04 JSON 提取 + PR2-Gate 邮件处理器；跑一版 S-03 实验。

### W4 阶段 3 工具调用（含 S-01 多厂商 + 算法启动）

- 周一（轻 OK）：HF 中文 unit1 `tools` / `actions` / `observations`。
- 周二：HF `bonus-unit1` function calling；T3-01 画「问题→选工具→执行→观察→回答」流程图。
- 周三：**算法启动**——随想录「数组」专题 + 2 道；加班只看题解。
- 周四：读 HA 第 4 章工具部分 + HA-code/chapter4 工具代码。
- 周五（轻 OK）：算法 2 道（双指针）；读 OpenAI Function Calling。
- 周六（整块）：T3-02 计算器 + T3-03 文件工具 + T3-04 外部 API。
- 周日（整块）：T3-Gate 多工具助手闯关；S-01 多厂商切换（接 Claude / OpenRouter）；更新 progress。

## 四、W5–W16（每周「工作日做什么 / 周末做什么 / 用什么资料」）

> 每天仍按第一、二节的节奏和 fallback 走：工作日挑下面的「工作日项」做一块 + 算法收尾；周末做「周末项」。走到某周想要逐日拆分，跟我说，我再帮你展开。

- **W5 阶段4 Agent 原理（上）**
  - 工作日：HF unit1 `what-are-agents`、HA 第 4 章 ReAct、ADP 第 5/6 章预读；算法每周 3–5 题。
  - 周末：A4-03 ReAct 跑通/改写（HA-code/chapter4/ReAct.py）+ A4-04 Plan-and-Solve。
- **W6 阶段4（下）+ 作品集启动**
  - 工作日：ADP 第 4 章 Reflection；J11-01 整理 GitHub 仓库（轻）；算法。
  - 周末：A4-05 Reflection + A4-Gate 最小 Agent 闯关 →（作品集项目①）。
- **W7 阶段5 框架源码**
  - 工作日：按 `core/ → agents/ → tools/` 读 HAsrc；HA 第 7 章；算法。
  - 周末：H5-04 加自定义工具 + H5-05 Memory/Protocol + H5-Gate。
- **W8 阶段6 RAG（上）+ S-02 + SQL**
  - 工作日：HA 第 8 章《记忆与检索》；SQLite 中文快速上手（B0-03）；Chroma 文档（S-02）；算法。
  - 周末：R6-01 切分 + R6-02 检索（用真实向量库 Chroma/FAISS）。
- **W9 阶段6（下）+ 服务化**
  - 工作日：HF unit3 Agentic RAG；FastAPI 官方中文教程起步读（J11-02）；算法。
  - 周末：R6-03 带引用问答 + R6-Gate 个人知识库（作品集项目②）；J11-02 用 FastAPI 包成服务。
- **W10 阶段7 设计模式 + S-04 + S-05**
  - 工作日：ADP 第 1–3 章编排、第 7 章多 Agent、第 18 章 Guardrails；算法。
  - 周末：D7-01~03 + D7-Gate；S-04 多 Agent demo；S-05 安全防护 + 攻击测试样例。
- **W11 阶段8 LangGraph + Docker + 前端**
  - 工作日：HF unit2（`when_to_use`→`first_graph`→`building_blocks`）；Docker 中文教程（B0-04）；算法。
  - 周末：G8-02/03 + G8-Gate；J11-03 Vue 前端接通（作品集项目③）。
- **W12 阶段9 MCP + 上线**
  - 工作日：HA 第 10 章；ADP 第 10 章 MCP；读 HAsrc `protocols/mcp/`；算法。
  - 周末：M9-02/03 + M9-Gate；J11-04 容器化部署（Railway/Render）→ 第一个公网 demo。
- **W13 阶段10 评估 + 综合项目（上）+ S-06**
  - 工作日：HA 第 12 章评估；ADP 第 19 章；Langfuse 文档（J11-05）；写 S-06 微调 vs RAG 笔记；算法。
  - 周末：E10 项目设计 + FINAL 主体开发 + 接 Langfuse tracing。
- **W14 综合项目（下）+ 上线**
  - 工作日：FINAL 收尾细节；J11-06 作品集组合整理；算法。
  - 周末：FINAL 部署 + FINAL-Gate 答辩自评（作品集项目④，主力）。
- **W15 求职（上）**
  - 工作日：J11-07 写简历 + 收集 10 个 JD 对照；小林 coding AI 应用 / 大模型面试题；算法。
  - 周末：系统设计练习；把 4 个项目各讲一遍（录音自测）。
- **W16 求职（下）**
  - 工作日：J11-08 面试自测（热题 100 查漏 + 八股）；开始投递。
  - 周末：模拟面试 + 项目全链路复述 + J11-Gate；持续投递。

## 五、提醒

- 每天用 `daily/YYYY-MM-DD.md` 打卡，哪怕只写一行。连续性比单日强度更重要。
- 加班季就主动降档（半血/空血），别硬扛；进度顺延是计划内的，不是失败。
- 走到 W5、或想把后面某几周也展开成逐日，跟我说一声即可。

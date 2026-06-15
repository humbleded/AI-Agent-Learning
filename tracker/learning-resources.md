# 学习资料总览与阅读顺序

## 一、够不够用？结论先说

- **阶段 0–10 的资料：绰绰有余，甚至偏多。** `repos/` 里已经躺着完整的书和课程，不用再到处找。你现在的风险不是「资料不够」，而是「收集太多、消化太少」。先把现成的按顺序读完 + 动手，别陷入收集癖。
- **真正缺资料的，是新增的工程 / 求职层**（S-01~S-06、阶段 11 J11）：FastAPI、Vue+SSE、向量库、Docker 部署、可观测、多厂商、算法、系统设计 / 八股。这些原路线没分配资料，已在本文件第四节补齐。
- **D:\AI-Knowledge 现状：是一个配置好但内容几乎为空的 Obsidian 知识库。** 插件齐全（copilot、dataview、smart-connections、omnisearch、git、kanban），但还没有你的知识笔记——它是「容器」，随着你过关由复习流程往里沉淀。所以不是资料不够，是还没开始往里写。用法建议见第六节。

## 二、你已有的核心资料（都在 repos/，离线可用）

| 资料 | 位置 | 用途 | 语言 |
| --- | --- | --- | --- |
| Hello-Agents 全书（16 章） | `repos/hello-agents/docs/chapterX/第X章*.md` | Agent 主教材：原理 / 范式 / 框架 / 记忆 / RAG / 上下文 / 评估 / 项目 | 中（另有英文版） |
| Hello-Agents 配套代码 | `repos/hello-agents/code/chapterX/` | 每章可运行示例 | 中注释 |
| HelloAgents 框架源码（指定分支） | `repos/HelloAgents-feature-branch-1/hello_agents/` | 阶段 5 源码精读对象 | — |
| HuggingFace Agents Course（中文版） | `repos/agents-course/units/zh-CN/` | 工具/动作/观察、function calling、LangGraph、Agentic RAG、评估 | 中 |
| Agentic Design Patterns（21 章 + 附录） | `repos/agentic-design-patterns/bilingual/`（中英）`/chapters/`（英） | 阶段 7 设计模式主资料；MCP/RAG/Guardrails/评估都有 | 中英对照 |
| Agent Learning Hub 路线图 | `repos/Agent-Learning-Hub/README.md` | 现代生产视角的 todo / Project Ladder / 官方资料索引 | 中 |

> 重点：Hello-Agents 第 9 章《上下文工程》正好是 S-03 的资料；第 12 章是评估；第 13–16 章是完整项目案例（旅行助手、深度研究、赛博小镇、毕业设计），可作为你阶段 10 综合项目的参考蓝本。

**额外推荐（中文实战，可选 clone 到 `repos/`）：[llm-universe｜动手学大模型应用开发](https://github.com/datawhalechina/llm-universe)**（Datawhale，12.8k★，[在线阅读](https://datawhalechina.github.io/llm-universe/)）

- 是什么：面向小白、**项目导向**的中文教程，带你从零搭一个「个人知识库助手」(RAG)。覆盖：调用大模型 API（含国内模型）、Prompt、Embedding 与向量库、用 LangChain 搭检索问答链、Streamlit 部署、评估。
- 怎么用：当 **阶段 2（Prompt）和阶段 6（RAG）的中文实战补充**最合适；阶段 1 也能参考它「调用 API」一节（讲国产模型，和你用 DeepSeek 对得上）；部署部分呼应 J11。
- 定位提醒：它和 Hello-Agents **互补**——Hello-Agents 偏 Agent 原理 / 从零构建，llm-universe 偏 LLM 应用 / RAG 落地（直接上 LangChain）。它为求简洁删了底层原理，所以当「实战」用、别替代你 tracker 里「先理解再写」的要求。内容是 2024 V1（举例用文心 / 讯飞 / 智谱），调用模式照搬到 DeepSeek 即可。

## 三、按阶段的阅读顺序（先读什么 → 再读什么 → 动手）

- **阶段 0 Python**：廖雪峰对应小节 → CS50P 对应 Week → 写 `code/stage0/` 练习。（已基本完成）
- **阶段 1 大模型 API**：OpenAI Quickstart → Text Generation / 流式文档 → DeepLearning.AI《Building Systems with ChatGPT API》对应小节 → 写 L1 代码。
- **阶段 2 Prompt/结构化**：DeepLearning.AI《Prompt Engineering for Developers》Guidelines → OpenAI Prompt Engineering + Structured Outputs → 配合 **HA 第 9 章上下文工程（S-03）** → 写 PR2 代码。
- **阶段 3 工具调用**：HF 中文 unit1 `tools/actions/observations` → HF `bonus-unit1` function calling → OpenAI Function Calling → 读 `HA code/chapter4` 工具代码 → 写 T3。
- **阶段 4 Agent 原理**：HF unit1 `what-are-agents` → HA 第 1–4 章 → ADP 第 4/5/6 章（Reflection/Tool Use/Planning）→ 跑 `HA code/chapter4` 的 ReAct/Plan/Reflection。
- **阶段 5 框架源码**：先 `HelloAgents-feature-branch-1/README` 跑通 example → 按 `core/ → agents/ → tools/ → memory/ → protocols/` 顺序读 → 配合 HA 第 7 章。
- **阶段 6 RAG**：HA 第 8 章《记忆与检索》→ HF 中文 unit3 Agentic RAG → **真实向量库（S-02，见下）** → 跑 `HA code/chapter8` 的 RAG pipeline → 写 R6。
- **阶段 7 设计模式**：ADP（中英对照）第 1–8 章 + 第 18/19 章，按需读，别全背 → 配合 **S-04 多 Agent、S-05 Guardrails 动手**。
- **阶段 8 LangGraph**：HF 中文 unit2（`when_to_use` → `first_graph` → `building_blocks` → `document_analysis_agent`）→ HA 第 6 章 → LangGraph 官方文档备查 → 写 G8。
- **阶段 9 MCP**：HA 第 10 章《智能体通信协议》→ ADP 第 10 章 MCP → 读 `HelloAgents .../protocols/mcp/` → 写 M9。
- **阶段 10 评估 + 综合项目**：HA 第 12 章 + ADP 第 19 章 → HF `bonus-unit2` 可观测与评估 → 参考 HA 第 13/14 章项目 → 做 FINAL。

## 四、新增层补充资料（S-01~S-06 + J11，原路线没有的）

| 主题 | 挂载 | 推荐资料（优先中文 / 官方） |
| --- | --- | --- |
| 多厂商模型（S-01） | 阶段1后 | Anthropic 文档 `docs.anthropic.com`；OpenRouter `openrouter.ai/docs`（一个 key 调多家）；本地模型 Ollama `ollama.com` |
| 真实向量库（S-02） | 阶段6 | Chroma 官方 `docs.trychroma.com`（最易上手）；FAISS（本地）；pgvector（接你的 SQL）；RAG 面试题（知乎 `zhuanlan.zhihu.com/p/2029999895302628181`） |
| 上下文工程（S-03） | 阶段2/4 | **HA 第 9 章（已有）**；Anthropic《Building effective agents》（Hub 里有链接） |
| 多 Agent（S-04） | 阶段7 | **ADP 第 7 章（已有）**；HF 中文 unit2 多节点 graph |
| Guardrails / 注入（S-05） | 阶段7 | **ADP 第 18 章（已有）**；OWASP LLM Top 10（搜「OWASP LLM」） |
| 微调 vs RAG（S-06） | 阶段6/10 | 概念为主：搜「RAG vs 微调 选型」；HA 第 8 章相关讨论 |
| FastAPI 服务化（J11-02） | 阶段11 | FastAPI 官方中文 `fastapi.tiangolo.com/zh`；CSDN《基于 FastAPI 搭建 LLM 调用 API 服务》；Python `asyncio` 官方/廖雪峰异步小节 |
| Vue + 流式（J11-03） | 阶段11 | Vue 官方文档（你已会）；MDN `EventSource` / `fetch` 流式读取 |
| Docker 部署（J11-04） | 阶段11 | **B0-04 已有 Docker 中文文档 + 黑马视频**；上线平台 Railway `docs.railway.app` 或 Render `render.com/docs` |
| 可观测（J11-05） | 阶段11 | Langfuse 中文 `langfuse.com/cn`（开源，推荐）；LangSmith 中文 `langsmith.langchain.ac.cn` |
| 算法（J11-08） | 阶段11 | 代码随想录 `programmercarl.com`（含视频，按专题刷）；LeetCode 热题 100 `leetcode.cn`（题单） |
| 系统设计 / 八股（J11-08） | 阶段11 | 小林 coding `xiaolincoding.com`（有「2026 Agent / AI 应用 / 大模型面试题」合集）；Anthropic / OpenAI 官方 agent 指南（Hub） |

## 五、视频清单（中文，按需补，不是主线）

- Python / 工程基础：廖雪峰（文档）、CS50P、黑马 Python、黑马 Docker、尚硅谷 MySQL、MIT Missing Semester——均已在 tracker 各阶段列出。
- 算法：代码随想录配套视频（programmercarl.com 每题都有 B 站讲解）。
- FastAPI / 向量库 / LangGraph：以官方文档为主；想看视频就在 B 站搜「FastAPI 入门」「Chroma 向量数据库」「LangGraph 教程」，选 2024 年后、播放量高的。
- Agent / 大模型 基础概念与直觉：**马克的技术工作坊**（[B 站](https://space.bilibili.com/1815948385)，YouTube 同名）——0→1 讲 LLM、Token、Context、Prompt、Tool、MCP、Agent、Agent Skill 等核心概念，新手友好、内容偏新。建议先看《从 LLM 到 Agent Skill，一期带你打通底层逻辑》（[B 站](https://www.bilibili.com/video/BV1E7wtzaEdq/)）建立全局地图，之后开新主题时用他的概念视频找直觉。注意：他偏 Claude Code / Agent Skills，略超你当前阶段，**看个直觉就好，别被带跑去提前搞 Skills**，按自己的阶段顺序走。
- 原则：**视频是辅助，不要用「看视频」代替「动手写」。** 概念看一遍够了，时间花在敲代码和过 Gate 上。

## 六、关于 D:\AI-Knowledge（Obsidian 库）怎么用

- 定位分工：`AI-Agent-Learning` 放**过程**（练习代码、每日打卡、笔记草稿、源码）；`AI-Knowledge` 放**沉淀**（稳定结论、概念卡片、面试复习卡、踩坑记录）。
- 建议节奏：每过一个 **Gate**，把该阶段的核心概念、自己的问答、踩的坑，整理成 1–2 张 Obsidian 笔记同步进去。用 `smart-connections` / `omnisearch` 在复习和面试前快速检索。
- 现在它是空的很正常——你才到阶段 0 尾。等 L1-Gate 过了，就可以写第一张「大模型 API 调用要点」卡片进去。

## 七、怎么用 Agent-Learning-Hub（嫁接 3 样，别照搬）

`repos/Agent-Learning-Hub/README.md`（Datawhale，hello-agents 同作者）是一份「现代生产视角的 Agent 学习路线图 + 项目阶梯 + 资料索引」。它**比本路线更超前、更偏 agent 基础设施**（钻 Claude Code / OpenClaw harness 内部），默认你已会 Python/LLM 基础。**结论：保留本路线当主干，从 Hub 只嫁接下面 3 样，其余当索引查，别整本照搬**（它资料量巨大，照搬会淹没，且和你已有的 hello-agents / agentic-design-patterns / agents-course 重复）。

### 嫁接① Project Ladder = 你的「作品集项目菜单」（最有价值）

Hub 的 11 级项目阶梯，大半正好能套在你已有的 Gate / J11 上——本来就要做这些关卡，按「可运行 + README + 失败记录」的成品标准交付即可：

| Hub 阶梯 | 对应本路线任务 | 定位 |
| --- | --- | --- |
| L1 计算器 Agent | T3-02 计算器工具 | 已有 |
| L2 Web 研究 Agent | 阶段4 A4-Gate | 作品集① |
| L3 PDF 问答 Agent | 阶段6 R6-Gate | 作品集② |
| L4 代码审查 Agent | 额外可选 | 🎯 .NET 背景做这个是差异化亮点 |
| L9 多 Agent 写作 | S-04 / D7-02（阶段7） | 多 Agent demo |
| L11 生产级 Harness | 阶段10 + J11-05 可观测 | 作品集④ FINAL |

### 嫁接② Stage 0 两篇必读 + 心法清单（阶段4 入门时读）

- [Anthropic《Building effective agents》](https://www.anthropic.com/engineering/building-effective-agents)、[OpenAI 实用 agent 指南](https://openai.com/business/guides-and-resources/a-practical-guide-to-building-ai-agents/)——尤其「**什么时候不该用 agent**」，应用岗面试高频。
- Learning Principles 当贯穿全程的检查清单：先做再深读、小而可靠胜过炫 demo、**加 agent 前先加 eval**、工具用严格 schema、每次重要运行都 trace、危险操作留人工确认。

### 嫁接③ README 当「到点查的索引」

到某阶段时瞄一眼 Hub 对应 Stage 的资料/论文/开源项目补充（如 RAG 阶段看它 Stage 2 项目表），**当字典查、不当作业做**。

### 了解即可、别陷进去

- 钻 Claude Code / OpenClaw harness 内部（Hub Stage 3、阶梯 L6/L7、Claude Code Study Path）：偏基础设施、非应用岗主路，且与**阶段5 源码精读已重复**，做一个就够。
- Stage 6 浏览器/电脑操作 Agent：有余力的加分项，不在主线。
- A2A / ACP 协议：知道「干嘛的」即可；MCP 阶段9 已覆盖。

## 八、一句话原则

资料不缺，缺的是「按顺序读完 + 动手 + 沉淀」。stage 0–10 用 `repos/` 里现成的；新增的工程 / 求职层按第四节补；**不要再花时间到处收集新资料了。**

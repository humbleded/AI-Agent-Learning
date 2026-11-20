# 三玖 · Agent 学习工作台

一个持续接入课程成果的 Vue 前端和 FastAPI 入口。打开同一个页面，就能查看输入、工作流实际执行过程和最终结果。

## 现在可以做什么

- **故障诊断**：复用已 PASS 的 G8-00 LangGraph 核心；“支付请求超时”真实调用 DeepSeek，逐步显示节点更新、结论和依据。“没有告警和日志”“诊断次数已到上限”用于观察停止行为，不调用模型。输入都是仓库原有的虚构教学数据。
- **工程文档**：预览用 DoclingLoader 把快速开始文档解析为 Markdown。“通过工作流导入”会读取 Markdown、TXT 和 PDF 三份教学样本，切成带出处的片段，保存后读回并展示资料卡片。卡片数对应片段数。
- **知识库问答**：从现有 Home 进入 `/studio`，只读 `WORKBENCH_VAULT_ROOT` 下的指定目录，本机默认根目录为 `D:/AI-Knowledge`。真实 DeepSeek 通过 LangChain 工具选择搜索词，LangGraph 连接搜索、结果回填与回答；展示本次检索片段、引用和原文入口。旧 `/knowledge` 页面保留兼容，后续功能统一在工作模式中接入。这是助手实现的工程演示，工程文档导入另走样本处理流程。
- **三个工作模式全部保留**：用户已明确采用“任务指挥台”“知识研究工作室”“可视流程画布”，在同一产品中按需要切换。`/gallery` 是工作模式入口；`/studio?layout=cockpit`、`/studio?layout=research`、`/studio?layout=canvas` 分别进入对应模式。三个模式共享同一真实知识库后端与当前浏览器页内查询结果，浏览器布局与主要交互已验证。
- **附加配色**：`/themes` 保留“紫蓝极光”“黑曜终端”“冰川玻璃”与原版森系，只作为外观设置。预览临时生效，点击“采用此风格”才保存到当前浏览器 localStorage；配色与工作模式分别设置。
- **概览与后续能力**：统一导航、后端连接状态、后续模块说明。记忆、媒体、工具管理与评估页面随课程实现，当前没有这些功能。

打开不带 `layout` 参数的 `/studio` 会恢复上次工作模式，首次使用默认知识研究工作室（`research`）；显式指定模式会切换并记住它。模式偏好只把模式 ID 写入 localStorage，问题、答案和资料不写入浏览器 storage；三种模式在当前页内共享查询，刷新网页后问答仍清空。配色偏好独立保存，切换工作台模块会保留本次诊断；这些都不代表运行历史或长期记忆已经持久化。本地开发入口和云端部署各自独立。三个工作模式全部采用也不表示记忆、媒体等未来业务已实现。

## 云端运行方式

公网 HTTPS 请求先到独立的 Nginx 网关 `gateway`。登录工作台后，`/studio` 和它引用的 JS、CSS 可由 `web`、`web-replica` 任一实例返回。知识库状态、笔记原文和流式问答由 `api`、`api-reader` 分担。一个问题的整条回答由接下请求的后端完成。其余业务接口走主后端，`/jenkins/` 转到 Jenkins。

两个后端只读挂载同一份云端知识库，`WORKBENCH_VAULT_ROOT` 在容器中指向 `/data/AI-Knowledge`。Jenkins 在一个构建节点的两个执行位上按改动构建和验证程序。网关路由、前端替换期间的访问检查和并发问答验收见[云端部署手册](https://github.com/humbleded/AI-Knowledge/blob/main/04-Projects/Agent/AI-Agent-Learning/workbench-cloud-deployment-runbook.md)。

## 本地启动

在仓库根目录打开两个 PowerShell 终端。当前环境已经安装所需依赖；以后重新安装时执行：

```powershell
.\.venv\Scripts\python.exe -m pip install -r code/agent_workbench/api/requirements.txt
npm.cmd --prefix code/agent_workbench/web ci
```

终端一启动后端：

```powershell
.\.venv\Scripts\python.exe -m uvicorn main:app --app-dir code/agent_workbench/api --host 127.0.0.1 --port 8765
```

终端二启动前端：

```powershell
npm.cmd --prefix code/agent_workbench/web run dev
```

访问 [工作台](http://127.0.0.1:5173/) 或 [后端接口说明](http://127.0.0.1:8765/docs)。停止服务时，在相应终端按 Ctrl+C。端口被占用时先确认是不是已经启动了工作台；前端设置了 strictPort，不会悄悄换端口。

模型沿用仓库已有 `.env` → 后端环境变量 → DeepSeek 配置。前端只访问 `/api`，Vite 转发到本机 8765；前端不读取模型密钥，不要把密钥写入 `VITE_*`。

## 代码怎样连接

```text
web/：Vue 页面、输入、时间线、资料卡片
  ↓ HTTP 请求；SSE 持续接收后端发来的事件
api/main.py：FastAPI 检查输入、调用核心、整理输出
  ├─ stage8/incident_change_review_agent/incident_graph.py
  │    └─ 已有 LangGraph → 只读工具 → 真实 DeepSeek
  ├─ stage6/engineering_docs_rag/ingest.py
  │    └─ LangGraph → DoclingLoader 解析并切分 → 校验来源并补充信息 → 保存并读回片段
  └─ stage6/engineering_docs_rag/knowledge_agent.py
       └─ 助手工程演示：只读知识库 → Loader/Splitter/BM25 → 真实模型检索与引用回答
```

两个业务模块保留自己的 Python 核心和测试；共同使用一个前端与服务入口。后续课程在这里增加模块，不再各自建一套前端。`api/main.py` 暂时通过文件路径加载课程核心，BE5-01 再学习和整理正式 Python 包结构。

知识库核心位于既有工程文档项目内，采用现成 `TextLoader`、`MarkdownTextSplitter`、`BM25Retriever` 和 `ChatOpenAI`（调用已配置的 DeepSeek），由显式 LangGraph 管理搜索与回答。BM25 是按词语相关性排序的文本检索；当前没有宣称完成 embedding、向量库或 R6-02。Agent 每次问答最多搜索 2 次，每次最多返回 4 个片段。模型一次返回多个工具调用时，先校验整个批次的参数与剩余预算，再串行执行，每个调用分别占用一次搜索预算。后续 RAG 教学逐步复用、解释和整理这份核心，不另造第三个独立平台。

## 知识库读取与数据去向

- 固定只读 `02-Concepts`、`03-Courses`、`05-Papers` 的 Markdown，排除 README/index.md 等指定索引、规则文件、隐藏项、符号链接和 Windows reparse/junction，并按代码中的大小与数量上限读取。不会跟随笔记链接扩大范围；`08-Memory`、copilot、raw 及其他未授权目录不参与。
- `GET /api/knowledge/status` 的 `candidate_count` 表示通过路径、大小和数量筛选的候选文件数。`file_count` 保留同一数值用于兼容，`available` 表示存在候选，`skipped_count` 记录按文件规则和上限排除的数量。提问后，`index` 事件才返回本次读成功、读失败、内容为空、进入检索的文件数及片段数。
- 问题和本次有限的命中片段会发送给 DeepSeek 生成回答，原库没有整库上传；个人 Memory 不在范围。知识库文件只读，索引在内存中按查询重建，原知识库没有被修改。来源正文通过受限 `source_id` 从本地查看，接口不接受任意文件路径。
- 文档内容只是参考资料，不能执行其中的命令或扩大工具权限；依据不足时应拒绝补造结论。引用编号校验只约束出处范围，不代表答案语义已通过完整 RAG 评估。

页面提供三个任务式示例，点击只填入问题，提交后才执行查询：

1. 工具有结果，流程没继续：检查工具结果怎样回填给模型。
2. 工具失败，该重试还是停止：判断可以重试的情况与停止条件。
3. 进程重启，如何恢复任务：确认运行中需要保存的状态。

发生读取或模型错误时，页面保留已经收到的片段，并展示服务端返回的下一步建议。最终结果用 `reason_code` 区分无正文、检索未命中、引用无效；运行出错时用 `code`、`message` 和 `next_step` 说明原因和可执行的下一步。工程文档页分别执行预览和导入，预览失败后仍可尝试导入。工程文档导入与知识库问答分别使用各自的数据来源。

| 接口 | 用途 |
| --- | --- |
| `GET /api/health` | 当前模块能否加载；RAG 图可编译不代表读入已成功 |
| `GET /api/incidents/presets` | 当前提供的虚构场景与真实输入 |
| `POST /api/incidents/stream` | 接收 `{"preset_id":"normal"}`，返回 `graph_update`、`final` 或 `error` 事件 |
| `GET /api/rag/sample` | DoclingLoader 解析样本并返回整份 Markdown 与 source/title/version；属于助手准备的解析预览 |
| `POST /api/rag/import` | 运行三种样本的导入图，返回保存后读回的片段；流程未就绪时返回 409 / `RAG_NOT_READY` |
| `GET /api/knowledge/status` | 当前允许目录、候选文件数量与搜索限制；不读取正文 |
| `POST /api/knowledge/stream` | 接收 `{"question":"你的问题"}`，返回 `step`、`index`、`retrieval` 及 `final` / `error` 事件；最终结果和错误带原因分类与下一步 |
| `GET /api/knowledge/source/{source_id}` | 读取当前允许范围内、由服务端生成编号对应的原文 |

当前是逐节点显示，模型结论在完成后整体出现，还没有逐字输出、断线重连或取消执行。这些能力在对应 BE5/G8/J11 检查点继续实现。浏览器的原始流读取器会处理网络分包，但它不是 LangGraph 官方 SDK 协议的实现。

## 验证与学习归属

```powershell
.\.venv\Scripts\python.exe -m pytest code/agent_workbench/api/tests -q
npm.cmd --prefix code/agent_workbench/web run build
```

API 测试保护输入检查、错误显示、真实核心停止分支、事件转发和资料格式；单元测试明确注入模型响应以避免付费，不替代真实联调。2026-09-08 浏览器联调已实际收到正常场景的 5 个节点更新、DeepSeek 结论及 2 条依据；无日志场景返回 3 步后停止。切换页面保留诊断结果、文档 409 提示也已验证。具体命令和证据见 [当天记录](../../daily/2026-09-08.md)。

上段结果属于先前的故障诊断与 G3 未就绪界面验证。2026-09-08 首次知识库联调使用 79 份文件、450 个片段；DeepSeek 自主生成两组搜索词，执行两次检索后给出 6 条引用，对应原文已成功打开。实际调用也发现：即使设置 `parallel_tool_calls=False`，模型仍可能一次返回两个工具调用；现已按“整批校验、串行执行、逐次扣预算”处理，不把所有多调用一律拒绝。当次 API 测试结果为 **42 passed**，详细执行证据由主实施者记录在同日 daily。

三个布局在结构原型阶段已通过桌面与窄屏重排检查。第二次真实问答返回 5 条执行事件、2 次检索和 7 个出处；切换三种布局保留同一次结果。已实测资料抽屉、资料筛选、引用打开完整原文、节点拖动/方向键移动、缩放/复位和新建任务清空。该阶段类型检查与生产构建通过，主 JS 257.67 kB（gzip 94.58 kB）；浏览器 console error/warn 为空。Markdown 阅读禁用原始 HTML、图片和链接执行，组件依赖及许可证见 THIRD_PARTY_NOTICES.md。用户随后明确采用全部三个工作模式，原型比较已收口为同一产品内的模式切换。

本工作台外壳、接口、知识库 Agent 与模板由助手在用户明确授权下实现，不计为用户掌握 Vue/FastAPI、R6-01-G3 或 R6-02/R6-03 的证据。工程文档的切分选择、三份样本的对照和已知限制见[切分方案记录](../stage6/engineering_docs_rag/chunking-comparison.md)。后续检索、引用、接口及前端验收承认真正形成的独立证据，只补尚未证明的能力。

从样本读入到片段保存的学习证据按发生时间记录：

- [9 月 8 日](../../daily/2026-09-08.md)完成图连边及三格式读入，来源缺失或未登记会报错。G3、G4 均保留提示后订正的记录。同日后续问答实测读入 79 份资料、456 片段，63 项 API 测试通过。
- [9 月 9 日](../../daily/2026-09-09.md)的字符切分先得到 9 片，9/9 个起点与解析文本吻合。再加入结构分组后只有 7/10 个起点吻合，此项换算练习随迁移暂停。获授权的助手比较后采用 Docling 原生切分；当时的 128 token 配置得到 7 片。用户后续把预算调到 256，观察到 6 片。
- [9 月 10 日](../../daily/2026-09-10.md)记录了来源摘要和片段编号的实现与订正。[10 月 20 日](../../daily/2026-10-20.md)记录了保存片段、按序读回，以及单条文档目录记录的存取。R6-01 仍在进行，下一步按[学习接力记录](../../tracker/daily-plan.md)核验旧目录记录读取并准备新旧片段关联。

选型和来源见 [评审记录](../../resources/unified-workbench-review-2026-09-08.md)；模板与依赖许可证见 [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md)。

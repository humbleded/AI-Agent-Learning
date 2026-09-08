# 统一 Agent 工作台选型记录

检查日期：2026-09-08。用途：为现有 Python 项目增加一个统一、可在本地运行的 Vue 界面。以下 GitHub stars 与最近 push 是当日快照；stars 只说明关注量，不代表适合当前学习项目，push 也不等于质量保证。

## 已采用的方案

采用 **Vue 官方 create-vue 3.23.0 生成的 TypeScript + Router 空白项目，配合 Element Plus 2.14.5 和 @lucide/vue 1.42.0**。统一目录是 `code/agent_workbench/web/` 与 `code/agent_workbench/api/`；后者通过薄 FastAPI 接口复用两个现有 Python 项目的核心代码，不引入另一套业务后端或整个平台。

生成参数为 `--ts --router --bare`。实际生成器固定到 [create-vue v3.23.0](https://github.com/vuejs/create-vue/releases/tag/v3.23.0)，对应 commit `749ab0d2e09e751873bb8e4850442349cbb10ede`。它的工具代码是 MIT，**模板目录及从模板生成的文件是 CC0 1.0 Universal**，不能仅根据 GitHub license 字段把二者混为一谈；见该版本 [LICENSE](https://github.com/vuejs/create-vue/blob/749ab0d2e09e751873bb8e4850442349cbb10ede/LICENSE)。

这个选择便于保留 Vue 技术路线，只增加页面、导航、输入和结果展示。Python 侧继续使用 LangChain 现成组件与 LangGraph 工作流。界面调用本地 FastAPI，模型密钥留在后端；界面本身不要求购买托管平台服务，模型调用沿用已有 DeepSeek 配置与计费。

当前复用故障诊断项目已有的 `incident_graph`；用户进一步授权后，知识库只读检索由助手在既有工程文档项目的 `knowledge_agent.py` 中实现并接入同一服务。工程文档 RAG 项目的 R6-01-G3 仍由用户完成，`ingest.py` 保留 TODO，未实现时页面明确提示。知识库演示可运行，不代表课程 G3 已完成；助手搭建工作台不计为用户独立掌握前端、API 或 RAG 的证据。

## 用户决定：三个布局全部保留为工作模式

用户先明确指出，“模板”指整体布局、交互效果和功能组织。此前只提供配色未覆盖此要求，因此补充了三个可操作的结构原型。用户随后问“可以所有的都要吗”，当前决定是全部保留为同一产品的工作模式；`/themes` 仍是独立的附加外观设置。

现有 Home 统一进入 `/studio`，原型比较页 `/gallery` 改为工作模式入口。三个模式共享同一真实知识库后端与当前浏览器页内查询、检索结果和引用，区别在于怎样组织操作与呈现信息；不复制后端或另建 Agent 平台。旧 `/knowledge` 页面保留兼容，后续功能在统一工作模式中接入，不继续扩展旧页。

| 已采用的工作模式 | 入口 | 使用重点 |
| --- | --- | --- |
| 任务指挥台 | `/studio?layout=cockpit` | 围绕当前任务组织提问、执行进展和结果，观察运行状态是否清楚 |
| 知识研究工作室 | `/studio?layout=research` | 围绕问题、回答与资料组织界面，方便边读答案边核对来源 |
| 可视流程画布 | `/studio?layout=canvas` | 围绕实际执行步骤及其结果组织界面，帮助理解搜索怎样回到模型上下文；不代表已提供任意图编辑或新业务能力 |

三个模式全部保留，用户可按任务切换。`/studio` 不带 `layout` 时恢复上次工作模式，首次默认知识研究工作室（`research`）；显式指定 `cockpit`、`research` 或 `canvas` 会切换并记住它。模式偏好只在 localStorage 保存模式 ID，问题、答案和资料不写入浏览器 storage，刷新问答仍清空。颜色预览与保存独立保留。原型阶段的浏览器布局与主要交互、类型检查和生产构建均已验证，细节见同日 daily。

知识库演示的范围、接口与数据去向见 [工作台 README](../code/agent_workbench/README.md) 和 [工程文档设计](../code/stage6/engineering_docs_rag/problem-contract.md)：只读 `02-Concepts`、`03-Courses`、`05-Papers`，排除指定索引、隐藏项和 reparse 等内容；问题及有限命中片段发送给 DeepSeek，原库未修改，个人 Memory 不参与。课程目录含计划，引用它们不作为学习证据。G3 与后续课程验收继续保留；本次采用全部三个工作模式，不代表全部未来业务已实现，记忆、媒体和评估等仍按既有任务接入。

## 候选比较

表中 push 日期按 GitHub API 返回的 UTC 日期；版本信息来自对应固定提交的包配置。

| 候选 | 2026-09-08 核验快照 | 适用性与决定 |
| --- | --- | --- |
| Vue 官方 create-vue + Element Plus | create-vue 4,402 stars；push 09-08；最新 release 3.23.0（07-21）。Element Plus 27,737 stars；push 09-08；release 2.14.5（08-21）。模板 CC0 / 工具 MIT；Element Plus MIT。 | **采用。** 官方空白骨架足以建立统一界面，API 格式由现有 Python 项目决定，依赖规模可控。 |
| pure-admin/pure-admin-thin | 3,031 stars；push 与 release v6.2.0 均为 2025-10-30；MIT。Vue ^3.5.22、Vite ^7.1.12、TS ^5.9.3；Node ^20.19.0 或 >=22.13.0。 | 未采用。能作为独立 Vue 前端连接 FastAPI，但薄版维护日期较旧；不能用主仓库活跃度代替薄版的维护事实。 |
| vbenjs/vue-vben-admin | 33,380 stars；push 09-07；最新 release v5.7.0（05-21）；MIT。当前 main 的 Vue ^3.5.40、Vite ^8.2.2、TS ^6.0.3；Node ^22.18.0 或 ^24.12.0，pnpm >=11。 | 备选。后台管理功能更完整，但 `apps/web-ele` 依赖多个 `@vben/*` 工作区包，不能只复制该目录就独立运行；当前没有引入整个多包仓库的必要。 |
| langchain-ai/agent-chat-ui | 3,132 stars；push 09-07；MIT；React 19.2.8。 | 未采用。官方 Agent 界面可供参考，但采用它会把前端路线换成 React。 |
| langgenius/dify | 154,872 stars；push 09-08；基于 Apache 2.0、带多租户服务及品牌展示附加条件的 Dify Open Source License；Python 后端使用 Flask。 | 未采用。是完整应用平台，框架与本项目 FastAPI / LangGraph 核心不同，整套替换会增加平台适配工作。许可证不能简写为无附加条件的 Apache-2.0。 |
| infiniflow/ragflow | 90,223 stars；push 09-08；Apache-2.0；React 前端。README 的容器部署要求至少 4 CPU cores、16 GB RAM。 | 未采用。其文档处理能力可作为后续参考；当前接入整套平台会引入容器运维和平台自己的处理流程，超出轻量统一界面的目标。 |

候选的固定源码证据：

- **create-vue**：候选检查时 main 为 `728e299d7f1ddb70f475adf21e5c82baeca56e5a`，核对了 [基础模板 package.json](https://github.com/vuejs/create-vue/blob/728e299d7f1ddb70f475adf21e5c82baeca56e5a/template/base/package.json) 和 [TypeScript 模板配置](https://github.com/vuejs/create-vue/blob/728e299d7f1ddb70f475adf21e5c82baeca56e5a/template/config/typescript/package.json)。实际生成使用上文 release 提交；生成模板声明的版本范围与最终安装版本以本地 `web/package-lock.json` 为准。[Element Plus 2.14.5 release](https://github.com/element-plus/element-plus/releases/tag/2.14.5)；实际包内 MIT 原文见第三方声明。
- **pure-admin-thin**：commit `f0ff132561ab684bb78379239adf29f9a38ac7f1` 的 [package.json](https://github.com/pure-admin/pure-admin-thin/blob/f0ff132561ab684bb78379239adf29f9a38ac7f1/package.json)、[LICENSE](https://github.com/pure-admin/pure-admin-thin/blob/f0ff132561ab684bb78379239adf29f9a38ac7f1/LICENSE)。
- **Vben**：commit `3f2d8bc1f2586a79f83d7b79c79ba818f800846a` 的 [根 package.json](https://github.com/vbenjs/vue-vben-admin/blob/3f2d8bc1f2586a79f83d7b79c79ba818f800846a/package.json)、[工作区版本表](https://github.com/vbenjs/vue-vben-admin/blob/3f2d8bc1f2586a79f83d7b79c79ba818f800846a/pnpm-workspace.yaml)、[web-ele/package.json](https://github.com/vbenjs/vue-vben-admin/blob/3f2d8bc1f2586a79f83d7b79c79ba818f800846a/apps/web-ele/package.json)、[LICENSE](https://github.com/vbenjs/vue-vben-admin/blob/3f2d8bc1f2586a79f83d7b79c79ba818f800846a/LICENSE)。main 中 web-ele 已标为 5.8.0，不能把它当成已发布的 v5.7.0 内容。
- **Agent Chat UI**：commit `bf69587d8bd10a6919120ee086a4ac6f10b0ceaf` 的 [package.json](https://github.com/langchain-ai/agent-chat-ui/blob/bf69587d8bd10a6919120ee086a4ac6f10b0ceaf/package.json)、[LICENSE](https://github.com/langchain-ai/agent-chat-ui/blob/bf69587d8bd10a6919120ee086a4ac6f10b0ceaf/LICENSE)。
- **Dify**：commit `22189f69f6dd16071a19ffae242f72310ce1f04b` 的 [LICENSE](https://github.com/langgenius/dify/blob/22189f69f6dd16071a19ffae242f72310ce1f04b/LICENSE)、[api/pyproject.toml](https://github.com/langgenius/dify/blob/22189f69f6dd16071a19ffae242f72310ce1f04b/api/pyproject.toml)。
- **RAGFlow**：commit `b4acb95cbdf03d36a7eb09c2ae823e66b5d13122` 的 [README](https://github.com/infiniflow/ragflow/blob/b4acb95cbdf03d36a7eb09c2ae823e66b5d13122/README.md)、[web/package.json](https://github.com/infiniflow/ragflow/blob/b4acb95cbdf03d36a7eb09c2ae823e66b5d13122/web/package.json)、[LICENSE](https://github.com/infiniflow/ragflow/blob/b4acb95cbdf03d36a7eb09c2ae823e66b5d13122/LICENSE)。

## 官方 Vue AI 接法：已核验，暂作参考

LangChain 已提供 **`@langchain/vue`**，不是只有 React 支持。2026-09-08 核验的 npm 稳定版为 **1.0.35**，MIT；其依赖 `@langchain/langgraph-sdk` 1.10.2，peer dependencies 为 Vue ^3.0.0 与 `@langchain/core` ^1.1.48。该 SDK 本轮没有安装或复制使用。

官方 [1.0.35 自定义 transport 文档](https://github.com/langchain-ai/langgraphjs/blob/%40langchain%2Fvue%401.0.35/libs/sdk-vue/docs/custom-transport.md) 确认 `useStream` 可接 `HttpAgentServerAdapter`。它允许自托管后端，FastAPI 可以实现所需接口；但后端还必须满足它规定的命令、事件格式、事件序号和重放等规则，**普通 FastAPI SSE 接口并不会自动兼容**。当前工作台先用自己的 HTTP / 流式接口，不为接 SDK 提前引入整套协议。将来需要其会话和恢复能力时再单独评估适配。

官方 [streaming-cookbook](https://github.com/langchain-ai/streaming-cookbook/tree/8c63965f48d0c0a9da6485bdf119906cfaa79ea9) 的检查提交为 `8c63965f48d0c0a9da6485bdf119906cfaa79ea9`，当日 57 stars、最近 push 2026-09-02、无 release，许可证为 [Apache-2.0](https://github.com/langchain-ai/streaming-cookbook/blob/8c63965f48d0c0a9da6485bdf119906cfaa79ea9/LICENSE)。其 [Vue App.vue](https://github.com/langchain-ai/streaming-cookbook/blob/8c63965f48d0c0a9da6485bdf119906cfaa79ea9/typescript/ui-vue/src/App.vue) 演示 `useStream`；[Python 版说明](https://github.com/langchain-ai/streaming-cookbook/blob/8c63965f48d0c0a9da6485bdf119906cfaa79ea9/python/ui-vue/README.md) 说明同一 Vue 前端可接 Python LangGraph 开发服务。它是接法示例，不是完整工作台。示例 [package.json](https://github.com/langchain-ai/streaming-cookbook/blob/8c63965f48d0c0a9da6485bdf119906cfaa79ea9/typescript/ui-vue/package.json) 还混有 TypeScript 后端、CLI 等依赖，因此本轮没有整体复制其代码或依赖清单。

## 实际安装与验证边界

2026-09-08 从实际 `node_modules` 核对：Vue **3.5.42**、Vue Router **5.3.1**、Element Plus **2.14.5**、@lucide/vue **1.42.0**；开发工具为 Vite **8.2.2**、TypeScript **6.0.3**、vue-tsc **3.3.11**、@vitejs/plugin-vue **6.0.8**。Element Plus 和 Lucide 使用精确版本，其余范围声明及解析结果分别保留在 `web/package.json` 与 `web/package-lock.json`。

本机 Node 24.13 / npm 11.11 满足生成模板的 Node `^22.18.0 || >=24.12.0` 范围。安装时发现 `npm-run-all2` 的间接依赖要求更高的 Node 24.15，因此已移除该辅助工具，构建脚本改为串行执行 `vue-tsc --build && vite build`。图标由旧的 `lucide-vue-next` 改用当前 `@lucide/vue`；其实际 LICENSE 除 ISC 外还包含 Feather 衍生图标的 MIT，已完整保留。

最初生成工作台时，实施者报告安装扫描为 **106 packages、npm audit 0 vulnerabilities**。这是该阶段的历史依赖快照，不代表后续新增依赖后的最终扫描，也不代表完整安全审计；当前依赖以本地清单与锁文件为准。

本轮知识库真实联调筛选出 **79 份文件、450 个片段**，DeepSeek 自主生成两组搜索词，按最多 2 次、每次最多 4 个片段的限制执行，最终给出 6 条引用且原文打开成功。模型即使收到关闭并行调用的配置，仍可能一批返回两个工具调用；现已先校验整个批次的参数与预算，再逐个串行执行，每个调用分别计数。当前 API 测试为 **42 passed**；这属于助手工程实现的验证，详细证据由主实施者记录。三个新布局的真实问答、主要交互、桌面与窄屏重排已验证，类型检查和生产构建通过；用户能力没有据此判 PASS。

实际使用的直接运行依赖许可证与模板来源保存在 [THIRD_PARTY_NOTICES.md](../code/agent_workbench/THIRD_PARTY_NOTICES.md)。本轮未复制 pure-admin、Vben、Agent Chat UI、Dify、RAGFlow 或官方 streaming-cookbook 应用代码，也没有为整个学习仓库新增顶层 LICENSE。


## 结构原型的产品参考与实现边界

2026-09-08 实读官方资料后，参考 [LangChain Agent Chat UI](https://docs.langchain.com/oss/python/langchain/ui) 的对话与工具结果组织、[Open WebUI 知识库](https://docs.openwebui.com/features/workspace/knowledge/) 的资料与引用阅读组织、[Vue Flow](https://vueflow.dev/) 的可拖动节点和缩放交互。这里只借鉴使用方式，没有复制三者应用代码，没有安装 Vue Flow 或切换 Next.js。当前画布由 Vue 状态、指针事件与 SVG 实现，是实际结果的解释视图，不支持编辑后端工作流。完整模型结论整段返回，逐字输出、取消、持久历史和任意图编辑尚未实现。

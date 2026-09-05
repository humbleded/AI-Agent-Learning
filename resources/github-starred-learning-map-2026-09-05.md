# GitHub 星标学习资料映射（2026-09-05）

这 8 个项目应作为现有任务的资料切片，不另开 8 门课程。当前最有用的调整是：R6-01 用官方 LangChain 文档说明接口，用 llm-universe 第 3 章的两个小节帮助理解；Hello-Agents 保留流程图与结构感知切分的解释。后续新增的有效补充是李博杰书中的检索对照，以及微软课程中的线上失败回流到离线评估。

## 采集口径与证据边界

- 采集日期：2026-09-05；GitHub 登录账号经 `gh api user --jq '.login'` 确认为 `humbleded`。
- 使用 `gh api --paginate 'users/humbleded/starred?per_page=100'` 遍历全部分页，共 8 个星标项目；`gh api --paginate 'user/subscriptions?per_page=100'` 返回 0 个 Watch 订阅。因此本文中的“关注项目”具体指这次读到的 Stars，不能解释为关注用户列表或全部 GitHub 活动。
- 8 个仓库均核对默认分支、HEAD、归档状态、README、目录及许可声明；截至采集时均未归档。下表保存完整 SHA，正文链接固定到所检查的提交。
- 阅读层级：目录/README 用于定位；明确列出的章节和代码才算已实读；没有执行课程代码、安装依赖或验证作者公布的指标。不能把“作者示例报告通过”记作本项目实测。
- 本次只读远端，没有克隆仓库或创建未来学习代码。两个递归目录请求曾超时，已改为 GitHub Contents API 读取相关目录；不据此声称审完所有文件。
- 公共 GitHub 页面另以网页工具核对章节可达性；`C3.ipynb` 网页只展示外壳时，实际正文由 GitHub Contents API 解码 notebook cells 后读取。
- 新增资料不自行改变执行顺序；当前入口与恢复排期读 daily-plan/weak-points，课程状态与岗位就绪分别读对应 tracker。岗位样本不足保持未完成，不能由资料映射冒充收口，也不作为 R6-01 的技术前置。

## 8 个仓库的固定版本与许可

| 仓库 | 检查时默认分支 HEAD | 许可核验及使用范围 |
| --- | --- | --- |
| [bojieli/ai-agent-book](https://github.com/bojieli/ai-agent-book) | `2c9dc5fb8d142e9bef63b6690fcb853477616e81` | 根 [LICENSE](https://github.com/bojieli/ai-agent-book/blob/2c9dc5fb8d142e9bef63b6690fcb853477616e81/LICENSE)：Apache-2.0。第三方模型、数据集和外部实验仓库各自核验。 |
| [datawhalechina/llm-universe](https://github.com/datawhalechina/llm-universe) | `77beb748047e8a0d8ff708716606a8e0b132dc45` | API 的 license 为 null，根目录未见 LICENSE 文件。按链接阅读、自行实现；未核明许可前不把课程代码/数据打包进可商用旗舰。 |
| [microsoft/ai-agents-for-beginners](https://github.com/microsoft/ai-agents-for-beginners) | `7b20684e56ae3e565d0568bb13de06912d4d19bc` | 根 [LICENSE](https://github.com/microsoft/ai-agents-for-beginners/blob/7b20684e56ae3e565d0568bb13de06912d4d19bc/LICENSE)：MIT；复用实质内容保留版权与许可，云服务条件另核。 |
| [huggingface/agents-course](https://github.com/huggingface/agents-course) | `8c0832eae634ebb34541c65265caa6da4c5d2c57` | 根 [LICENSE](https://github.com/huggingface/agents-course/blob/8c0832eae634ebb34541c65265caa6da4c5d2c57/LICENSE)：Apache-2.0；模型与数据许可不由课程许可代替。 |
| [xindoo/agentic-design-patterns](https://github.com/xindoo/agentic-design-patterns) | `3ce509590eabc4d4d6968315aa14fda12794e34e` | 根目录无 LICENSE；[README 许可说明](https://github.com/xindoo/agentic-design-patterns/blob/3ce509590eabc4d4d6968315aa14fda12794e34e/README.md#-许可证) 称遵循原书条款、仅供学习交流。作为阅读补充，不当作许可已确认的代码依赖。 |
| [jjyaoao/HelloAgents](https://github.com/jjyaoao/HelloAgents) | `93e77ea60c13436636c9b39b6761ff8dfe940ba2` | 根 [LICENSE](https://github.com/jjyaoao/HelloAgents/blob/93e77ea60c13436636c9b39b6761ff8dfe940ba2/LICENSE)：CC BY-NC-SA 4.0，含署名、非商业与相同方式共享要求；可作学习对照，不默认复制为可商用实现。 |
| [datawhalechina/Agent-Learning-Hub](https://github.com/datawhalechina/Agent-Learning-Hub) | `dddf777dde6788228136862f270203424a28efbc` | 根 [LICENSE](https://github.com/datawhalechina/Agent-Learning-Hub/blob/dddf777dde6788228136862f270203424a28efbc/LICENSE)：MIT；被索引项目仍各自核验。 |
| [datawhalechina/hello-agents](https://github.com/datawhalechina/hello-agents) | `4f7682ceafe573d07cd8a7d0b89908500e83227d` | 根 [LICENSE.txt](https://github.com/datawhalechina/hello-agents/blob/4f7682ceafe573d07cd8a7d0b89908500e83227d/LICENSE.txt)：CC BY-NC-SA 4.0；课程阅读与项目代码分发分别处理。 |

许可结论只针对已检查文件。依赖、模型、素材和子目录可能另有条款；开始实际复制或分发时按所选切片核验，不以“GitHub 公开”代替许可。

## 各仓库怎样接到已有任务

### 1. bojieli/ai-agent-book：R6-02 的检索对照，E10 的成本分析

已读：根 README 的 2.0 版章节表和实验运行要求；`book/chapter3.md` 中用户记忆层次与知识库的说明；chapter3/chapter7 目录；[检索实验 3-6 README](https://github.com/bojieli/ai-agent-book/blob/2c9dc5fb8d142e9bef63b6690fcb853477616e81/chapter3/retrieval-pipeline/README.md) 的代码地图、融合方法、离线评估和结果解读；[成本实验 7-9 README](https://github.com/bojieli/ai-agent-book/blob/2c9dc5fb8d142e9bef63b6690fcb853477616e81/chapter7/agent-cost-analysis/README.md) 的记录字段和 2×2 对照设计。

- R6-02/S-02：只取“精确编号适合关键词、改写问题需要语义检索、融合/重排需要比较”的切片。在工程文档 RAG 的同一组问题上比较检索配置，沿用 Recall@k/MRR 与延迟记录。
- E10/J11-05：需要解释成本变化时，参考实验 7-9 的逐步输入/输出/缓存用量拆分与两个独立开关的对照方式。记录本项目真实 DeepSeek 用量与当时价格，已有评估设施内完成。
- 拒绝：不启动另一套三服务检索产品，不照搬 17 文档玩具集的满分结论，不新增训练/机器人/Coding Agent 主线；此次没有读完或执行其 evaluator。
- 版本限制：2.0 把评估移到第 7 章，但成本 README 仍有“第 6 章 / ch6”残留；任务启动时看实际 `pyproject.toml` 与入口，不只按章号安装。实验数量在 README 不同位置也不一致，不把其统计数当学习配额。

### 2. llm-universe：R6-01 最贴题的中文短读

已读：根 README 的定位、目录与完成范围，根目录、C3 目录、[requirements.txt](https://github.com/datawhalechina/llm-universe/blob/77beb748047e8a0d8ff708716606a8e0b132dc45/requirements.txt)，以及 [C3 notebook](https://github.com/datawhalechina/llm-universe/blob/77beb748047e8a0d8ff708716606a8e0b132dc45/notebook/C3%20%E6%90%AD%E5%BB%BA%E7%9F%A5%E8%AF%86%E5%BA%93/C3.ipynb) 的 §3.3.1–3.3.4 正文与代码；其余 C3 内容只浏览定位。

- 采用 §3.3.2“数据读取”和 §3.3.4“文档分割”：读到的内容如何进入 `Document.page_content`，来源如何进入 `metadata`，以及 `chunk_size / chunk_overlap / length_function` 的作用。
- §3.3.3 作为一个真实的“不适合当前场景”例子：它删除全部空格的清洗会破坏代码缩进、英文词边界和部分表格，不能复制到工程文档 RAG。
- 还需校准：文字里的 `meta_data` 应对应实际属性 `metadata`；字符数、词数与模型 token 数不能混为一谈；Markdown 返回若干 Document 不代表物理“页数”。
- 版本限制：当前依赖仍固定 LangChain/core/community/text-splitters 0.3.0；不能把最近 pushed_at 当成 API 已更新的证据，也不能笼统说“只改地址和模型就能搬到 DeepSeek”。R6-01 不需真实模型调用，R6-02 的 embedding 接口与模型另行核验。

### 3. microsoft/ai-agents-for-beginners：E10/J11-05 的上线后改进闭环

已读：根 README 的依赖与课程表、10/13/16/18 等目录入口；[第 10 课全文](https://github.com/microsoft/ai-agents-for-beginners/blob/7b20684e56ae3e565d0568bb13de06912d4d19bc/10-ai-agents-production/README.md)，重点是 Key Metrics to Track、Offline Evaluation、Online Evaluation、Combining the two、Managing Costs。

- E10-01/J11-05：把上线失败或用户反馈变成经核验的新离线案例，再比较修改前后质量、延迟和成本；成功标准先按自己的业务定义。
- 不增加 MAF/Azure 课程：根 README 当前样例以 Microsoft Agent Framework + Foundry Agent Service V2 为主，需要 Azure 账号；只迁移评估思路到既定 LangChain/LangGraph/FastAPI 项目。
- 第 18 课安全入口本次只确认存在，尚未实读，不能宣称已审完其安全实现；具体安全事实仍以现有 S-05 的官方来源为主。

### 4. huggingface/agents-course：保留 R6-03 场景导读，移出 R6-01 主资料

已读：根 README、units 各语言目录；[中文 unit3 introduction 全文](https://github.com/huggingface/agents-course/blob/8c0832eae634ebb34541c65265caa6da4c5d2c57/units/zh-CN/unit3/agentic-rag/introduction.mdx)。

- 这个文件讲晚会助手为什么需要宾客、日程和天气资料，没有教 Loader、Splitter 或增量导入。因此 R6-01 不应把它列作实现主资料。
- R6-03 只有在需要第二个应用例子时读它，并迁移成工程文档检索问题；后续 `tools.mdx / agentic-rag.mdx` 在对应任务启动时再核对代码。
- 不重复 unit1 已 PASS 的 Agent 基础，也不要求把 smolagents/LlamaIndex/LangGraph 三套例子全跑一遍。中文 `bonus_unit2` 与英文 `bonus-unit2` 路径不同，链接按实际语言路径取。

### 5. xindoo/agentic-design-patterns：D7-02 的多 Agent 分工对照

已读：根 README/目录/许可声明，以及[双语第 7 章开头至协作形式与模式结构](https://github.com/xindoo/agentic-design-patterns/blob/3ce509590eabc4d4d6968315aa14fda12794e34e/bilingual/Chapter%207_%20Multi-Agent%20Collaboration.md)。

- D7-02：只对照顺序交接、并行、层级与独立复核，并解释当前故障诊断项目为什么采用其中一种、拒绝另一种。
- 章节声称的协同优势只作待验证设计假设；是否改善根因覆盖、延迟、成本，要由 S-04 与单 Agent 的同数据对照决定。
- 根 README 明确翻译处于待审核阶段；术语和版本字段对照官方原文。D7-01 已有第 1–3 章安排，本次不再新增同义的重复作业。

### 6. jjyaoao/HelloAgents：只保留可选源码对照，先分清分支

已读：根 README 的版本、结构与许可；`hello_agents/` 目录；[tools/response.py 全文](https://github.com/jjyaoao/HelloAgents/blob/93e77ea60c13436636c9b39b6761ff8dfe940ba2/hello_agents/tools/response.py)。

- H5-01 真实排错需要时，可只追踪 `ToolStatus / ToolResponse` 如何表示成功、部分成功和错误，迁移到既定工具边界中；此前已 PASS 的格式规则不重考。
- 当前 main 是 V1.0.0 开发版，和教程不完全一致；根 README 推荐教程配套用 `learn_version`，本次该分支 HEAD 为 `3927c6d1decb37737c4c1344fde00ccef55ab1f3`。本地旧 `HelloAgents-feature-branch-1` 不能仅凭目录名视为当前教程配套。
- 不把这个框架加入旗舰依赖，也不为了补齐框架熟练度启动独立课程。许可有限制，参考结构后自行实现与拷贝代码是不同的操作。

### 7. Agent-Learning-Hub：只当项目检查索引

已读：根 README 目录与 Stage 2 资源表；Project Ladder 和 Learning Principles 完整段落、LICENSE。

- [Project Ladder](https://github.com/datawhalechina/Agent-Learning-Hub/blob/dddf777dde6788228136862f270203424a28efbc/README.md#project-ladder)：L3 只映射现有工程文档 RAG；L9 的协作只映射现有故障诊断项目；L11 的评估、权限、回放、CI 只映射 E10/J11。
- [Learning Principles](https://github.com/datawhalechina/Agent-Learning-Hub/blob/dddf777dde6788228136862f270203424a28efbc/README.md#learning-principles)：复杂度增加前要先有评估和失败证据，与当前路线一致。
- Stage 2 列出的 Onyx/RAGFlow 等只是发现入口，本次没有读它们源码，不将其列为已审核教材。其 Coding Agent/Gateway/GUI 方向不扩成主线。

### 8. datawhalechina/hello-agents：R6-01 流程解释，R6-02 防照搬对照

已读：根 README、code/docs chapter8 目录；[第 8 章 §8.3.2 与 §8.3.4 的导入、切分、嵌入代码](https://github.com/datawhalechina/hello-agents/blob/4f7682ceafe573d07cd8a7d0b89908500e83227d/docs/chapter8/第八章%20记忆与检索.md)；[04_RAGTool_MarkItDown_Pipeline.py 全文](https://github.com/datawhalechina/hello-agents/blob/4f7682ceafe573d07cd8a7d0b89908500e83227d/code/chapter8/04_RAGTool_MarkItDown_Pipeline.py)。

- R6-01：只读 §8.3.2 的导入与问答两条流程，以及 §8.3.4（1）文档载入、（2）结构感知切分，帮助解释标题路径、原文位置与片段之间的关系。
- 04 示例调用整体 `RAGTool` 并进入向量化，不能代替本任务亲自使用 LangChain Loader、Splitter、Document 的证据；它也不证明实际完成 PDF/TXT/Markdown 三类导入。
- R6-02 对照警示：§8.3.4（3）遇到向量维度错误时补零或截断、转换失败时塞零向量的示例会掩盖模型/索引不一致；本项目应明确失败、定位模型/维度，并按版本重建或迁移，不静默修饰数据。
- 不整章提前学习长期 Memory，也不照搬 Qdrant/Neo4j 栈替换已经确定的 PostgreSQL/pgvector 主线。

## R6-01 实际启动时的最小资料包

这里只整理资料，不启动任务，不创建 TODO 骨架，不修改课程状态。

1. **官方必读：**[Document loaders — Interface](https://docs.langchain.com/oss/python/integrations/document_loaders#interface)。理解不同来源如何读成同一类 Document，以及 `load / lazy_load` 的差别；具体 PDF/Markdown/TXT loader 依赖在实际动手当天再选择和核验。
2. **中文主读：**llm-universe C3 §3.3.2 + §3.3.4，配合上文已列出的订正；只覆盖读入后的内容/来源与切分边界。
3. **官方必读：**[Splitting recursively](https://docs.langchain.com/oss/python/integrations/splitters/recursive_text_splitter)，尤其参数解释与中文无空格文字的分隔符段。检查日期 2026-09-05；实际安装时记录所选库版本。官方说明 `chunk_size` 由 `length_function` 决定，overlap 是目标重叠量，不能把每块字符数当真实 token 预算。
4. **按缺口选读：**Hello-Agents §8.3.2/§8.3.4（1）（2）。若前两份资料已足以解释流程就跳过，不机械增加教材或即时题。

落在现有产物中的验证仍以 R6-01 rubric 为准：三种格式；可定位 metadata；空页/解析失败/编码/超长段落；重复、更新、删除；稳定 document_id/chunk_id 边界。教程均未完整提供这些工作要求，不能照跑 notebook 就 PASS。资料理解考察合并进当前任务的覆盖图，后续正式练习承认已 PASS 即时证据。

## 反思与下一次检查点

- 旧资料导航的主要问题不是数量少，而是把“场景介绍”当“实现教材”、把一个封装好的 RAGTool 当 Loader/Splitter 学习证据，以及没有逐项标明许可与分支。本文按任务重新定位并保留具体反例。
- 当前筛选仍有边界：这是针对课程适配的静态审阅，不是八仓库安全审计；未执行选中的实验，也未逐一核对全部第三方依赖。因此不能宣称所有示例都可直接运行或商用。
- 未来只在对应任务启动时更新所选切片与版本，不为刷新 pushed_at 重读八个全仓库。源码学习的完成证据是用户能解释关键行为、采用/拒绝理由，并在自己的旗舰上得到测试或对照结果。

# Agent 应用岗位能力与证据

最后规则/用户资格更新：2026-09-05。下方正式能力矩阵与 W6 样本仍为 2026-08-25 快照；用户资格快照日期与 JD 检查日期分开记录，本次不将其冒充已经重跑的正式审计。

本表是“是否已有求职证据”和正式 JD 审计结果的唯一事实源；`tracker/progress.md` 仍是课程任务 PASS 的唯一事实源。课程 PASS、投递硬资格和技术匹配是三条不同轴，不能互相替代。

## 目标岗位边界

- **主目标**：初级/初中级 Agent 应用开发工程师。
- **次目标**：大模型应用后端、RAG/知识库工程师。
- **邻接优势**：AI 全栈应用开发；用户自述会一些 Vue，后续先做最小独立复核。助手可核查许可证、维护状态和依赖风险后组合 GitHub 开源 Vue 骨架；若 G8-Gate 提前采用，用户先完成第三方代码最小准入审核，J11-03 再完成状态/SSE/认证/错误边界的独立解释与修改。不扩成独立前端主线，也不把助手搭建冒充用户证据。J11-02 只选一个 `product_flagship` 做正式前端和公网产品。
- **目标城市**：深圳或武汉。
- **不自动扩线**：大模型预训练/算法研究、纯 Java/C++ 后端、完整无人值守编码工厂。高配 JD 中出现这些内容，只作岗位相关差异或能力标杆。

## 用户资格快照

| 快照日期 | 本科 | 年龄 | 工作语言 | 目标地区 | 该快照时尚未核实的事实 |
| --- | --- | --- | --- | --- | --- |
| 2026-08-06 | 是 | 27 | 中文 | 深圳 / 武汉 | 本科专业、总开发年限、AI 正式工作年限、英语工作能力、薪资下限、可投递日期 |

2026-09-05 用户在本次审计对话明确补充：**计算机科学与技术本科、累计开发 4 年、没有正式 AI/大模型项目工作经历**。这是当前资格核验事实；英语工作能力、薪资下限、可投递日期仍待确认。上行保留为历史快照，不能继续把已补充的专业/年限说成当前未知。四年开发经验不证明任何尚未 PASS 的技术已经掌握。

当日重新访问职位的调查见 [岗位要求核验资料](../resources/job-requirements-audit-2026-09-05.md)，它是待正式审计使用的来源，不替换下方历史样本：聚铂鑫正文实际截断、海葵当次不可访问，不能继续把旧 `HARD_ELIGIBLE` 当当前结论；全日制/统招性质和专项后端/Python 年限也尚未证明。本次只核实 2 条主/次目标资格样本及 2 条邻接样本，不计算正式比例。

资格审计只使用当前可见事实。岗位若硬性要求特定专业、未被当前事实证明的工作年限、应届/在校身份、外语能力或其他资格，则分别记为 `UNKNOWN` 或 `INELIGIBLE`，不能靠技术栈相近“冲掉”硬门槛。

## 两轴口径

```text
eligibility_status = HARD_ELIGIBLE | INELIGIBLE | UNKNOWN
technical_fit      = READY | NEAR | DEVELOPING
```

- `HARD_ELIGIBLE`：用户满足页面当前可见的学历、经验年限、招聘类型、语言和地区等投递门槛；技术差距不在此字段表达。
- `INELIGIBLE`：至少一项可见硬门槛确定不满足，例如校招身份、硕士、明确高年限或非目标地区且不可远程。
- `UNKNOWN`：职位已关闭/页面失效、硬门槛不完整，或所需用户事实不可见。
- `READY`：已有可对外复现的岗位证据覆盖该岗位核心技术要求。
- `NEAR`：已有核心证据，只差一个边界清晰、可在现有项目闭合的主要里程碑。
- `DEVELOPING`：仍缺两个以上核心能力或缺少可复现工程/部署证据。

技术 READY 匹配率只按下式计算：

```text
READY 且 HARD_ELIGIBLE 的岗位数
──────────────────────────
全部 HARD_ELIGIBLE 岗位数
```

`NEAR` 单独报告；`INELIGIBLE` 和 `UNKNOWN` 不进入分母。技术栈、框架和项目经验只影响 `technical_fit`，不得写成混合资格 `STRETCH`。

## 岗位证据等级

- `NOT_STARTED`：课程和作品都未开始。
- `LEARNING`：正在学或已有零散练习，尚未完成课程 Gate。
- `COURSE_PASS`：课程 Gate 已通过，能运行并解释，但还不是可对外证明的岗位能力。
- `JOB_EVIDENCE`：已落到可复现旗舰/公开作品，有测试、评估/性能数据、工程说明、失败复盘和独立讲解。
- `INTERVIEW_READY`：能在限时、无原答案辅助的面试/现场任务中稳定设计、实现、排错和讲取舍。

升级约束：

1. tracker 出现课程标题不能自动升级证据。
2. `COURSE_PASS → JOB_EVIDENCE` 至少需要可复现运行、自动测试、版本化评估或性能数据、README/架构图、失败复盘、无敏感信息和独立讲解；相关生产场景的**当前任务所需切片**满足 `work-scenario-coverage.md` 的证据等级，不能用同一大类里较早的局部证据替代尚未验证的 CI、429、ACL、恢复等子能力。
3. 所有 `JOB_EVIDENCE` 升级、`FINAL-Gate`、`J11-Gate` 和正式投递就绪结论必须由另一工具独立交叉复核；分歧未解决时保持候选/pending。
4. `JOB_EVIDENCE → INTERVIEW_READY` 还需脱离原笔记完成模拟面试/限时任务，并回答失败恢复、成本、安全和扩展追问。
5. 普通 Session 不改本表；只在 Gate、作品里程碑、模拟面试或 W6/W12/W16/W19 正式审计时更新。

## 能力矩阵（正式快照：2026-08-25）

此表保留上轮正式判断，不代表 2026-09-05 的课程快照：`progress.md` 已记录 `G8-00` 于 2026-09-05 PASS，故下方“无框架证据”只描述 8 月 25 日。已有显式 Graph/stream 课程证据，持久化与恢复仍未验收；下一次正式岗位复核应据完整产物更新该能力域。本次规则审计不升级 `JOB_EVIDENCE`，也不重新判定课程。

| 能力域 | 审计时等级（2026-08-25） | 审计时已有证据 | 当时下一条可验证证据 | 对应任务/作品 |
| --- | --- | --- | --- | --- |
| Python 基础与脚本 | COURSE_PASS | P0-01~Gate 已通过 | 在真实服务补类型、分层、pytest/mock、lint/type-check、配置和日志 | BE5-01 |
| LLM API、Prompt、结构化输出 | COURSE_PASS | L1、PR2、S-03 与 A4 的真实 DeepSeek、JSON/validator 证据 | provider 边界、版本化 prompt/eval、服务集成 | S-01、E10、旗舰项目 |
| Tool Calling | COURSE_PASS | T3 与 A4 已完成真实工具、Action/Observation、参数绑定与安全停止 | 在可部署服务中补维护型测试、README、依赖锁定和事故证据 | G8、BE5、旗舰二 |
| Agent Loop / ReAct / Planning / Reflection | COURSE_PASS | A4-Gate 于 2026-08-24 正式 PASS；V5 固定集 14/14，含 step/stop/recovery/HITL | 只迁移到显式 Graph，不换名字重复教学 | G8-00 |
| LangGraph 与 durable workflow | NOT_STARTED | 无框架证据 | StateGraph、stream、checkpoint/thread、重启恢复、interrupt、幂等与故障注入 | G8-00~Gate、旗舰二 |
| 多 Agent 协作 | NOT_STARTED | 无带类型约束的角色交接或对照证据 | 单 Agent baseline 后做共享/私有 state、角色交接、停止/预算/升级和同集对照 | S-04、G8-Gate |
| 长期 Memory 系统 | NOT_STARTED | 聊天历史与 checkpoint 都不算长期 Memory | 跨 thread CRUD、TTL、provenance、冲突/删除、租户隔离、PII/poisoning 与无 Memory baseline | D7-03、D7-Gate |
| LangChain / 生产 RAG | NOT_STARTED | 无 R6 课程证据 | Loader/Splitter/Document、pgvector、hybrid/rerank、引用/拒答、固定两步与 Agentic RAG 同集评估 | R6、旗舰一 |
| Python Agent 后端 | NOT_STARTED | 当前主要是 CLI/脚本 | asyncio、FastAPI/Pydantic/SSE、PostgreSQL/Redis、后台任务、认证和负载 | BE5-01~Gate |
| Linux/网络/数据库/Docker | LEARNING | B0-02 PASS | B0-01/03/04/Gate；PostgreSQL/pgvector migration 和 Docker Compose | B0、BE5、R6 |
| 安全、权限与故障恢复 | COURSE_PASS | T3/A4 已有 sandbox、工具白名单、参数绑定、来源硬门、action-bound HITL 和失败恢复 | RAG/Memory/MCP 的注入、越权、poisoning、多租户与持久授权复测 | R6、D7、G8、M9、FINAL |
| 评估、tracing 与回归 | COURSE_PASS | T3/A4 有冻结数据集、分项阈值、holdout、失败保留与结构化日志 | baseline/candidate、组件+端到端 evaluator、trace、CI regression 和线上失败回灌 | E10、J11-05 |
| CI/CD、部署与运维 | NOT_STARTED | 无公网服务或自动发布证据 | pytest/Ruff/type-check CI、Docker build、smoke、secret、告警、负载、备份和回滚 | BE5-Gate、R6/G8-Gate、J11-04 |
| 作品集与项目表达 | LEARNING | A4-Gate 是课程级里程碑，不是岗位证据 | 两旗舰+一小项目，公开 README/架构/指标/威胁模型/复盘和至少一个 demo | J11、FINAL |
| 算法与系统设计 | LEARNING | W4 4/4 PASS；2026-08-25 审计确认 W5 `DEBT 4` | 下一独立算法 Session 先逐题清 W5 的 `3 新 + 1 旧`，清完前不启动 W6 完整配额；总目标仍为 W4–W20 最低 52 道新题 | algorithm-progress、J11-08 |

## JD 审计方法

每次 W6/W12/W16/W19 都分成两张表：

1. **能力标杆池**：4–6 条京东、腾讯或同等级岗位，用于校准工程深度；城市、学历、语言或年限不合格仍可作标杆，但不能进入匹配率。
2. **真实可投池**：恰好 10 条当前在招、深圳/武汉且已核清硬门槛的 `HARD_ELIGIBLE` 岗位。页面失效、职位关闭、硬门槛缺失或用户事实不足的岗位改为 `UNKNOWN` 并替换，不能用来凑数。

审计规则：

- 优先企业招聘官网，其次 BOSS 直聘/智联招聘等当前职位页；搜索摘要只作入口，必须记录页面/卡片证据和检查日期。
- 平台“经验不限”等结构化标签与正文硬性年限冲突时，以正文为准。
- 硬资格只记录学历/专业、经验年限、招聘类型、语言、地区等门槛；Python、LangGraph、RAG、FastAPI、Docker 等只进入 `technical_fit`。
- 能力按语义编码，不要求 JD 使用完全相同术语；每个频率保留 `出现数/10` 和逐行标签，禁止靠关键词计数伪精确。
- 频率 `≥60%` 为主线候选，`30%–<60%` 为岗位相关，`<30%` 通常降级可选；权限、恢复、幂等、评估等核心生产风险即使低频也可保留，但必须写清风险依据。
- 路线审计由 `learning-coach` 输出建议；用户批准后，正式岗位台账与证据等级由 `ai-agent-learning-review` 写回。
- 一般学习方案质量审计可使用已核验岗位与官方工程资料定性评审，不得把少量样本包装成正式十岗统计。样本不足时继续完善方案，保留正式审计未完成；下一轮独立检查未关闭原因。正式匹配率、J11-Gate 和投递前就绪结论仍须完整岗位审计。

## 能力标杆池（检查日期：2026-08-25）

以下 6 条只校准工程上限，不进入个人匹配率：

| 公司/岗位 | 当前链接与检查证据 | 主要能力信号 | 为何不进入分母 |
| --- | --- | --- | --- |
| 腾讯：微信－大模型（Agent）应用开发后台工程师 | [腾讯招聘](https://careers.tencent.com/jobdesc.html?postId=2037392065205268480)，2026-08-25 核验 | Agent 后台、规划/工具、多轮决策、RAG/Function Calling、高并发/低延迟/高可用 | C++/大规模后台经验等硬门槛只作标杆 |
| 腾讯：大语言模型应用工程师（Agent 方向） | [腾讯招聘](https://careers.tencent.com/jobdesc.html?postId=2034114867123875840)，2026-08-25 核验 | Agent 全链路、Prompt/Skill、Agentic RAG、评估、性能与线上排错 | 标杆池，不以公司名推定个人资格 |
| 腾讯 PCG：AI 应用开发工程师（Agent 方向） | [腾讯招聘](https://careers.tencent.com/jobdesc.html?postId=2026845083588001792)，2026-08-25 核验 | Planning、长期 Memory、多 Agent、Durable Execution、sandbox、Skills/MCP、评估飞轮 | 高工程标准岗位；硬资格未用于个人匹配 |
| 京东：大模型应用算法/开发专家（Agent 方向） | [京东招聘 219681](https://zhaopin.jd.com/web/job-info-detail?requementId=219681)，页面发布 2026-06-24，检查 2026-08-25 | Agent Runtime、模型网关、状态、stream/cache/circuit、Eval、回放和全链路可观测 | 明确 3+ 后端、2+ 分布式及 Java/Go 等硬门槛 |
| 京东：软件开发岗（AI 应用方向） | [京东招聘 220736](https://zhaopin.jd.com/web/job-info-detail?requementId=220736)，页面发布 2026-07-14，检查 2026-08-25 | Agent/RAG/向量库、权限/失败兜底、离线/线上评估、trace、API/DB/cache/async/container | 明确 3+ 软件/后端/AI 工程经验 |
| 京东：国际产研 AI Agent 算法/工程专家 | [京东招聘 219868](https://zhaopin.jd.com/web/job-info-detail?requementId=219868)，页面发布 2026-06-29，检查 2026-08-25 | A2A、多 Agent、A2UI、Skills/MCP、Memory/Context/Harness、sandbox | 明确相关专业硕士、算法/论文或竞赛门槛 |

标杆动作：保留高可用后端、durable execution、权限/sandbox、Memory、评估回归、trace、故障恢复和成本；多 Agent 作为 G8 的受控对照；Java/C++ 第二实现、模型训练、论文/竞赛不升为当前主线。

## 真实可投池：深圳 / 武汉（检查日期：2026-08-25）

正式 W6/W12/W16/W19 审计的目标分母固定为恰好 10 条 `HARD_ELIGIBLE`。职位卡片只有在它确实完整覆盖学历/专业、年限、招聘类型、语言、地区等所有可能硬门槛时才够用；详情页受安全验证阻挡、当前页面不再含该岗位、只剩旧搜索缓存，或用户关键事实不可见时，一律先记 `UNKNOWN` 并替换，不能用“未看见冲突”推导“已经满足”。下表保留本轮 10 条候选及复核失败，直到补足 10 条合格样本前不计算正式匹配率或 `/10` 频率。技术标签含义为：`APP` 业务应用交付、`AGENT` Agent/workflow、`BACKEND` Python/后端/API、`RAG` 检索/知识库、`OPS` 部署/运维、`QE` 测试/评估/可观测、`MULTI` 多 Agent、`MEM` 长期记忆。

| # | 岗位 / 公司 | 城市 | 链接与检查日期 | 当时硬资格判断 | eligibility_status（2026-08-25） | technical_fit（2026-08-25） | 能力标签与当时技术差距 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | AI Agent 应用开发工程师 / 海葵音乐 | 武汉 | [BOSS 职位](https://www.zhipin.com/job_detail/df18841f501752540nZ729y5EVZS.html)，2026-08-25 | 经验不限、学历不限、武汉；普通职位页未标应届身份，正文强调不以名校/大厂履历筛选 | HARD_ELIGIBLE | DEVELOPING | `APP AGENT BACKEND OPS QE`；A4 有控制循环，但缺可上线框架项目、服务/部署与公开证据 |
| 2 | AI Agent 应用工程师 / AIOTAGRO 爱农云联 | 武汉 | [BOSS 当前搜索页](https://m.zhipin.com/zhaopin/291bd2be5eafd66b03By29q9Ew~~/)、[直达页](https://m.zhipin.com/job_detail/58f2f6c085cb92c103B93tu0GFBZ.html)，2026-08-25 复核 | 当前卡片为经验不限/本科/武汉，但搜索索引暴露“理工科专业”要求，用户本科专业不可见；直达正文又被安全验证阻挡 | UNKNOWN | DEVELOPING | `APP AGENT`；技术方向可观察，但不进入资格分母 |
| 3 | AI 应用工程师 / 武汉禹森特智能科技 | 武汉 | [BOSS 当前搜索页](https://m.zhipin.com/zhaopin/291bd2be5eafd66b03By29q9Ew~~/)、[直达页](https://m.zhipin.com/job_detail/1da3aaa1de6357a90nd-0ty7EFRT.html)，2026-08-25 复核 | 卡片只显示经验不限/本科/武汉，直达页被安全验证阻挡；完整专业、语言、招聘类型等门槛无法核清 | UNKNOWN | DEVELOPING | `APP AGENT BACKEND OPS`；偏 Node/TypeScript 全栈并含基础部署运维，仅作邻接观察 |
| 4 | AI 应用工程师 / 武汉双知智能 | 武汉 | [BOSS 职位](https://www.zhipin.com/job_detail/f9ab05eb93b231c30nV539q6E1tW.html)，2026-08-25 复核 | 当前直达页重定向到安全验证；现有记录不足以复核完整正文和全部硬门槛 | UNKNOWN | DEVELOPING | `APP AGENT RAG QE`；缺知识库/RAG 与服务级测试证据，且不进入资格分母 |
| 5 | AI 软件工程师 / 上海帛未信息技术（武汉岗位） | 武汉 | [原 BOSS 链接](https://www.zhipin.com/zhaopin/eb55e12bc2ca36371Hd-3t-_FA~~/)，2026-08-25 复核 | 当前页面实际是“武汉 AI 软件销售”搜索页且不含目标公司/岗位；旧卡片不能证明仍在招或完整硬门槛 | UNKNOWN | DEVELOPING | `APP BACKEND OPS`；仅保留历史候选，不进入资格分母 |
| 6 | AI Agent 开发工程师 / 深圳市聚铂鑫科技 | 深圳 | [学聘通职位页](https://xuejob.com/index/job/detail/id/9092.html)，2026-08-25 | 页面为经验不限、本科、深圳龙岗、全职；未列校招/外语/专业硬限制 | HARD_ELIGIBLE | DEVELOPING | `APP AGENT BACKEND RAG OPS QE MULTI MEM`；JD 直接覆盖 RAG、多 Agent、Memory、Docker、安全，当前除 A4 外均缺项目证据 |
| 7 | AI 应用算法工程师 / Agent 开发工程师 / 无限进制 | 深圳 | [原 BOSS 搜索页](https://m.zhipin.com/zhaopin/0cc79891087af91d03V83di7Ew~~/)，2026-08-25 复核 | 当前页面不再含该公司/岗位，只能找到约两个月前缓存；不能证明当前在招或完整硬门槛 | UNKNOWN | DEVELOPING | `APP AGENT BACKEND QE`；历史技术信号保留，但不进入资格分母 |
| 8 | AI 开发工程师 / 深圳市创世纪科技发展 | 深圳 | [智联招聘](https://www.zhaopin.com/jobdetail/CC321869010J40855422213.htm)，2026-08-25 | 页面为经验不限、本科、全职、深圳；正文无硬性专业/年限/外语条件 | HARD_ELIGIBLE | DEVELOPING | `APP AGENT BACKEND`；要求 Python、LangChain/Dify 与 AI 应用经验，当前尚无框架项目 |
| 9 | AI 应用工程师 / 深圳市同一方光电技术有限公司 | 深圳 | [智联招聘](https://www.zhaopin.com/jobdetail/CC443684910J40987547504.htm)，2026-08-25 复核 | 完整正文为经验不限、本科、全职、深圳；未列特定专业、年限或外语硬门槛，“应届生可培养”不是仅限校招 | HARD_ELIGIBLE | DEVELOPING | `APP OPS QE`；正文是 AI 工具调研、测试、配置、轻量部署、权限与复盘，没有明确 Agent/workflow 要求 |
| 10 | 软件工程师（AI 智能体与网络安全方向）/ 深圳市北宸环境科技 | 深圳 | [原 BOSS 搜索页](https://www.zhipin.com/zhaopin/cd2c35a0d142ac3c0nB509y9FA~~/)，2026-08-25 复核 | 当前页面不含目标公司/岗位，只能找到旧索引缓存；不能证明当前在招或完整硬门槛 | UNKNOWN | DEVELOPING | `APP AGENT BACKEND OPS QE`；历史技术信号保留，但不进入资格分母 |

当时结果（2026-08-25，未冒充本次重新核验）：

- 本轮 10 条候选中，暂有 `4 HARD_ELIGIBLE + 6 UNKNOWN`；W6 正式审计判 `RETRY / INCOMPLETE`。
- 固定的 10 条硬可投分母尚未成立，因此**不报告**正式 READY 匹配率、NEAR 比例或 `/10` 能力频率；`0/4` 也不能冒充 W6 正式结果。
- 当时缺 6 条合格新样本；该数字只解释 2026-08-25 的欠缺，不能作为当前固定补齐数。旧的 `10/10`、`READY 0/10` 与频率表全部撤销。
- 课程路线仍由目标岗位边界、6 条工程标杆、已验证生产风险和用户主/次目标共同支持；本次不完整小样本不得单独增加或删除课程主线。
- 当前收口动作（2026-09-05）：本债务保留 `RETRY / INCOMPLETE`。独立岗位审计先用最新用户事实重开全部拟入样本正文，包括原先 4 条 `HARD_ELIGIBLE`，再按本次合格数计算还需补几条；形成恰好 10 条当前 `HARD_ELIGIBLE` 后才关闭。它不阻塞满足技术依赖的 `R6-01`；W12 必须复查未关闭原因并保留各自快照。正式匹配率、J11-Gate 和投递前就绪仍要求完整审计，不能因继续学习而抹掉债务。

## 能力语义频率（W6 待重做）

当前没有合规的 10 条 `HARD_ELIGIBLE` 分母，不生成正式频率表，也不把历史 4 条或当日少量核验样本套进 `/10` 阈值。补齐样本后重新逐行编码；在此之前，应用交付、Agent/workflow、Python 后端/API、测试评估、部署运维等优先级只作标杆与风险校准结论，不声称来自一张有效的 10 岗统计表。

## 不进入分母的反例

下表同属 2026-08-25 历史快照。新资格事实使相关专业/4 年一般开发要求可以重新判断；明确要求正式 AI/大模型工作年限的岗位与用户目前无此经历冲突。只有重开当前职位正文后才能改当前样本分类，不能拿旧缓存自动改成 `HARD_ELIGIBLE`。

| 岗位 | 状态 | 排除证据 |
| --- | --- | --- |
| 武汉起点人力：AI 应用开发工程师 | UNKNOWN | 智联标签为 3–5 年；当前用户总/AI 年限不可见，不进入分母 |
| 武汉智领创联：大模型应用工程师 | UNKNOWN | 正文明确三年以上 AI 大模型经验且要求相关专业；用户相关事实不可见 |
| 深圳广信通信：AI 应用工程师 | UNKNOWN | 正文要求 1 年以上 AI 相关经验和相关专业；用户事实不足 |
| 深圳泰和安：AI 应用工程师 | UNKNOWN | 正文硬性 3 年以上企业私有化 AI/LLM 落地经历 |
| 深圳汉得：大模型应用开发工程师 | UNKNOWN | 虽标无经验，但正文硬性相关理工专业；用户本科专业不可见 |
| 武汉东智汇通 AI 应用实习 / 小米 2027 届实习 | INELIGIBLE | 明确 2027 届/在校实习身份，不能污染社招匹配率 |
| 安克创新：AI 应用工程师 | UNKNOWN | BOSS 卡片与另一条可核验来源对招聘类型/状态存在冲突，后者显示校招且已结束；用户应届身份不可见，因此从分母移除并替换 |

## 当前路线与投递动作

- 当前不宣称技术 READY；课程依赖顺序以 `daily-plan.md` 为准，关键链是 `G8-00 → R6/BE5/B0 → pgvector/RAG 对照 → FastAPI/SSE → durable G8 → BE5-05/BE5-Gate → R6-Gate → D7-02/S-04/G8-Gate → D7-01/D7-03/D7-Gate → M9/E10 → J11-02~06 产品化与 S-05 收口 → FINAL-Gate → J11-07/08/Gate`。
- 两个旗舰形成 README、测试、评估、部署和故障证据后，再将相应样本从 `DEVELOPING` 重算为 `NEAR/READY`；不能因为路线已写入 tracker 提前升级。
- W12/W16/W19 每轮重新打开页面。岗位关闭、正文改变或出现硬门槛冲突时，先改 `UNKNOWN` 再替换，仍保持 10 条硬可投样本。
- 使用 2026-09-05 已补充的计算机专业、4 年开发及无正式 AI 经历重审候选；英语要求仍逐岗核实。补充事实只影响资格判断，不自动改变技术证据。

## 审计记录

| 内容块/日期 | 样本 | 主要变化 | 影响的课程/Gate | 结论 |
| --- | --- | --- | --- | --- |
| 2026-07-10 / W4 | 方向性样本 | Python 后端、生产 RAG、持久化 Agent、评估回归、安全与 CI/CD 偏薄 | BE5；R6/G8/M9/E10/J11 与 FINAL-Gate | 维持应用岗主线 |
| 2026-07-22 / 路线复审 | 大厂标杆 + 方向性样本 | 框架、部署和业务作品证据出现偏晚；H5 性价比低 | 前移 G8-00；H5 可选；强化 BE5/R6 | 不扩第二后端/训练主线 |
| 2026-08-24 / A4-Gate | Gate 证据校准 | Agent 控制循环、安全门、固定 eval/holdout 和结构化日志形成课程证据 | Agent Loop 升 `COURSE_PASS` | 不升级 `JOB_EVIDENCE` |
| 2026-08-25 / W6 | 6 条大厂标杆 + 深圳/武汉 10 条候选；复核后 `4 HARD_ELIGIBLE + 6 UNKNOWN` | 原审计误把职位卡片/旧缓存当作“硬门槛已核清”，`10/10`、READY 分母和 `/10` 频率撤销；#9 公司名与标签已修正 | 课程方向暂按标杆、风险与用户目标保留；岗位统计不能继续驱动细粒度优先级 | `RETRY / INCOMPLETE`；补足 6 条完整、当前、硬门槛可核验的样本后重算 |
| 2026-09-05 / 方案与规则审计 | 用户补充计算机专业、4 年开发、无正式 AI 经历；当日岗位材料另存 resources | 解除外部岗位样本不足对技术学习的阻塞；区分历史矩阵与 G8-00 新课程事实 | 不变更课程状态或岗位证据等级 | W6 仍 `RETRY / INCOMPLETE`；方案评分不替代正式十岗审计 |
| W12 | 待重新核验 6 条标杆 + 10 条硬可投样本 |  |  |  |
| W16 | 待重新核验 6 条标杆 + 10 条硬可投样本 |  |  |  |
| W19 | 待重新核验 6 条标杆 + 10 条硬可投样本 |  |  |  |

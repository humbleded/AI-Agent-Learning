# Agent 应用岗位能力与证据

最后校准：2026-08-24。

本表是“是否已有求职证据”的唯一事实源；`tracker/progress.md` 仍是课程任务 PASS 的唯一事实源。两者不能互相替代。

## 目标岗位边界

- **主目标**：初级/初中级 Agent 应用开发工程师，优先社招 0–3 年 AI 经验、接受传统开发转向或以项目能力替代纯 AI 年限的岗位。
- **次目标**：大模型应用后端、RAG/知识库工程师。
- **邻接优势**：AI 全栈应用开发；Vue 只用于完整产品交付，不把主线扩成独立前端课程。
- **能力标杆**：优先用京东、腾讯等大厂的 Agent/RAG/大模型应用岗位校准工程深度，重点对齐高并发、高可用、分布式后端、Agent Runtime、长期 Memory、Durable Execution、Skills/MCP、评估飞轮、安全、性能与成本；标杆岗位不因公司名自动进入真实可投匹配率。
- **目标条件**：在 W6 首轮正式审计前确认优先城市/远程范围、最低可接受薪资和预计开始投递日期；未确认前必须逐条记录，不得把不同地区、校招和高年限岗位混成一个匹配率。
- 技术栈边界：学习与验收按零基础进行；既往工作经历只在简历中如实记录，不转化为课程豁免或旗舰集成要求。后续所有 Agent/RAG 项目的后端统一使用 Python/FastAPI，前端使用 Vue。
- 大厂具体岗位若硬性要求 Java/C++、硕士、特定业务或多年高并发经历，只能作为能力标杆或 `STRETCH`；Python/FastAPI 项目证明的是可迁移系统工程能力，不能冒充满足语言/学历/年限硬门槛。只有明确转投京东 Java 或微信 C++ 后台时，才另开求职语言支线，不重复改写当前主线。
- 非主线：大模型预训练、算法研究、PyTorch/DeepSpeed、SFT/LoRA、GPU 分布式训练。只有目标 JD 明确转向“模型算法/训练+应用混合岗”时，才另开选修分支，不挤占当前主线。

## 证据等级

- `NOT_STARTED`：课程和作品都未开始。
- `LEARNING`：正在学或已有零散练习，尚未完成课程 Gate。
- `COURSE_PASS`：课程 Gate 已通过，能运行并解释，但还不是可对外证明的岗位能力。
- `JOB_EVIDENCE`：已落到可复现旗舰/公开作品，有测试、评估/性能数据、工程说明、失败复盘和独立讲解。
- `INTERVIEW_READY`：能在限时、无原答案辅助的面试/现场任务中稳定设计、实现、排错和讲取舍。

升级规则：

1. 不能因为 tracker 出现了某个标题就升级；必须看真实产物和验证记录。
2. `COURSE_PASS → JOB_EVIDENCE` 至少需要：可复现运行、自动测试、版本化评估或性能数据、README/架构图、失败复盘、无敏感信息、能独立讲清；相关生产能力在 `work-scenario-coverage.md` 至少有一次 `DIAGNOSED_AND_FIXED`，恢复/安全/部署类达到要求时需 `RECOVERED_UNDER_FAULT`；同时由另一工具完成一次证据交叉复核。
3. `JOB_EVIDENCE → INTERVIEW_READY` 至少需要：一次模拟面试/限时任务、脱离原笔记完成、能回答失败恢复/成本/安全/扩展追问。
4. 普通每日检查不更新本表；只在 Gate、作品集里程碑、模拟面试或 W6/W12/W16/W19 JD 审计时更新。

## 当前能力矩阵

| 能力域 | 当前等级 | 已有证据 | 升级到下一档还缺什么 | 对应任务/作品 |
| --- | --- | --- | --- | --- |
| Python 基础与脚本 | COURSE_PASS | P0-01~Gate 已通过，能写函数、文件/JSON、异常、HTTP 与基础测试 | 在真实服务中补类型、分层、pytest/mock、lint/type-check、配置与日志 | BE5-01 |
| LLM API、Prompt、结构化输出 | COURSE_PASS | L1、PR2、S-03 已通过；有聊天、流式、分类、JSON、邮件处理器；A4-Gate C3d 已把普通文本 Reflection、DeepSeek `json_object` Refinement、`json.loads` 与客户端 validator 接成 topic/path 真实链 | 抽 provider、严格 schema、版本化 prompt/eval，并接入服务 | S-01、E10、旗舰项目 |
| Tool Calling | COURSE_PASS | T3-01~Gate 已通过；A4-Gate 又把 topic/path 两路接成 Action → 真工具 → Tool Observation → 三阶段摘要链，唯一 V5 RUN-5 为 normal 10/10、holdout 3/3、完整 14/14，HITL D01 A～K 11/11 | 接入 BE5 可复现服务工程；补维护型自动测试、README/架构、依赖锁定、生产事故证据与独立岗位证据交叉复核 | A4-Gate、BE5-Gate、旗舰二 |
| Agent 原理与控制循环 | COURSE_PASS | A4-01～A4-Gate 全部通过；能实现并解释 Problem Contract、Action/Observation、Candidate/Reflection/Refinement、客户端 exact validator、共享 `MAX_STEPS=6` 账本、七字段日志、工具/Provider 恢复、安全停止与 action-bound HITL；V5 完整固定集 14/14 | G8-00 迁移基础 Graph；BE5 补服务化、并发/幂等、维护型测试与可复现工程；旗舰二再补持久恢复和端到端事实一致性 | A4-Gate、G8-00、BE5-Gate、旗舰二 |
| 主流 Agent 框架基础 | NOT_STARTED | 已有手写 Agent 前置，但尚无框架迁移证据 | 用 LangGraph `StateGraph` 表达 state/node/edge/条件路由/tool/stream，并用同一案例测试迁移前后行为；能说明何时不需要框架 | G8-00、旗舰二 v1 |
| Agent Memory / Context 生命周期 | NOT_STARTED | 仅有聊天历史与上下文实验，不等于长期 Memory | 跨会话 CRUD/TTL/provenance/冲突/删除、租户隔离、PII/poisoning、无 Memory baseline | D7-03、D7/G8/FINAL |
| Python Agent 后端 | NOT_STARTED | 现有产物以 CLI/脚本为主 | async、FastAPI/Pydantic、PostgreSQL/Redis、后台任务、认证、压测 | BE5-01~Gate |
| 大厂后端与分布式基本功 | NOT_STARTED | 尚无高并发服务证据 | 连接池/事务、缓存、MQ、限流/熔断/背压、幂等与一致性、容量/SLO、依赖故障恢复 | BE5、R6/G8/J11/FINAL |
| Linux/网络/数据库/Docker | LEARNING | B0-02 已通过 | B0-01、SQL、Docker/Compose、B0-Gate | B0-01/03/04/Gate |
| 生产 RAG | NOT_STARTED | 无 R6 课程证据 | 具体领域/用户流程、多格式/增量索引、pgvector、hybrid/rerank、ACL、检索/答案评估和至少一个业务/操作指标 | R6、S-02、旗舰一 |
| 可恢复 LangGraph Agent | NOT_STARTED | 无高级 G8 课程证据；G8-00 只负责基础框架能力 | persistence、checkpoint/thread、interrupt/resume、幂等、进程退出恢复与故障注入 | G8、旗舰二 v2 |
| MCP 生产接入 | NOT_STARTED | 仅前置 Tool Calling 概念 | 最新官方规范、STDIO/HTTP、认证边界、权限/断连/审计 | M9-Gate |
| 安全与权限 | COURSE_PASS | T3/A4 已覆盖文件沙箱、工具白名单、参数原值绑定、候选来源/正文硬门和失败不回显；A4 D01 A～K 11/11 证明 action-bound confirmation、一次性消费、allow/deny/missing/错绑/replay/timeout 与生产 fake 隔离 | 补威胁模型、间接提示注入、SSRF/越权/外泄/poisoning、多租户与持久授权；在 R6/M9/FINAL 复测真实攻击面 | A4-Gate、S-05、D7/G8/M9/FINAL |
| 评估与可观测 | COURSE_PASS | T3 与 A4 均有运行前冻结的自包含数据集、分项不可补偿阈值和 holdout；A4 透明保留 RUN-4 RETRY，V5 唯一 RUN-5 为 14/14，并用共享 step/固定七字段日志定位 F01～F03；源码/eval/Contract 指纹绑定完整 | E10 补维护型自动测试、版本化 baseline/candidate、代码+LLM evaluator、完整 trace、CI regression 与线上失败回灌；BE5 先补服务级指标/测试入口 | E10、J11-05、BE5-Gate |
| CI/CD、部署与运维 | NOT_STARTED | 无公网服务与自动发布证据 | BE5-Gate 先补 pytest/Ruff/type-check CI、Docker build、测试部署与 smoke；R6 更新应用，J11-04 再补 secret、告警、负载、备份和回滚 | BE5-Gate、R6-Gate、J11-04/W17 |
| 作品集与项目表达 | LEARNING | 已有课程代码与 daily/notes；A4-Gate 是可运行的课程级 Agent 里程碑，具备 Contract、固定 eval、故障复盘与安全矩阵，但尚无对外 README/架构、维护型测试、服务化或部署 | 2 旗舰+1 小项目、架构/指标/威胁模型/失败复盘、可复现运行与至少一个公网 demo | J11-01/06、FINAL |
| 算法与系统设计 | LEARNING | W4 内容块已正式 4/4 PASS、结转债务 0：两数之和、存在重复元素、有效的字母异位词、存在相近的重复元素均有真实测试；两数之和已完成独立复测 | 后续内容块继续按 `3 新 + 1 旧错题` 累计 50–70 道高质量题，并补 RAG/对话服务系统设计 | algorithm-progress、J11-08 |
| Python/Vue 全栈集成 | NOT_STARTED | 项目内尚无完整前后端集成证据 | 从基础复核后，让一个旗舰展示 Python/FastAPI Agent 后端与 Vue 的流式接口、认证、错误和部署边界 | J11-02/03/06 |

## 模拟面试校准

| 日期 | 范围 | 稳定证据 | 需要复测 | 结论 |
| --- | --- | --- | --- | --- |
| 2026-08-06 | Agent 工具安全、失败一致性、ReAct/Plan、上下文与工具取舍 | ReAct 成功/安全停止、Plan-and-Solve 与局部 ReAct 组合、上下文清洗和长对话管理回答稳定 | 确认状态与幂等键；聊天历史/长期 Memory/RAG；端到端事实一致性；按业务风险选择工具 | 仅校准为 `LEARNING`；尚未达到 `INTERVIEW_READY`，不产生 `JOB_EVIDENCE` 候选，也不触发交叉复核 |

## JD 审计方法

每次 W6/W12/W16/W19 审计采用“双轨样本”，不能混成一个匹配率：

1. **大厂能力标杆池**：优先核验京东、腾讯等大厂 4–6 条当前或近期可验证的 Agent/RAG/大模型应用岗位。它决定工程深度、复合故障和系统设计追问；过期、高年限、算法混合或语言不匹配岗位可留作标杆，但不得进入可投分母。
2. **真实可投池**：固定抽样 10 条当前仍在招岗位，并逐条记录岗位/公司、链接与抓取日期、地区、招聘类型、经验/学历/语言硬门槛、必须项、加分项、资格状态、已有证据、最大差距和下一动作。

- 真实可投池至少 7 条必须是用户确实满足硬门槛的社招/转岗岗位；校招、实习或明确要求 3 年以上大模型落地经验的岗位最多 3 条，只能作为能力参考。
- 过期或无法确认在招的岗位不计入 10 条总样本，必须换成有效岗位；校招、实习、高年限等仅参考样本不进入匹配率与能力频次分母。
- 资格状态固定为：`HARD_ELIGIBLE`（硬门槛满足）、`STRETCH`（可冲刺但存在 AI 年限/部分栈差距）、`INELIGIBLE`（学历/语言/年限/城市等硬门槛不满足）、`UNKNOWN`（信息缺失）。只有 `HARD_ELIGIBLE` 进入匹配率分母，不能把标题里的“1–3 年”直接等同可投。
- 匹配率与能力频次只按当轮 **7–10 条真实可投子集**计算：出现率 `≥60%` 记为主线 must-have，`30%–<60%` 记为 role-dependent，`<30%` 记为 optional；同时保留原始出现次数与实际分母，不能被一条高配 JD 带着无限扩课。
- 课程优先级取“大厂标杆的工程共性”与“真实可投池高频项”的交集。只在大厂算法岗出现的 SFT/RLHF/vLLM/PyTorch 不自动升为应用岗主线；后端可靠性、评估、安全和问题定位即使 JD 没逐字写出，仍可因生产风险保留为硬门槛。
- 审计结论必须落到“保留 / 前移 / 降级可选 / 删除”四种课程动作之一，并记录到下方审计表。

单条记录模板：

| 日期 | 岗位/公司 | 样本轨道 | 地区/类型 | 经验/学历/语言硬门槛 | 必须项 | 加分项 | 资格状态 | 证据/差距 | 链接 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |

## 京东 / 腾讯能力标杆（2026-07-10）

本节只校准课程深度，不作为本轮真实可投匹配率。正式审计仍需在抓取当日确认职位状态和用户的城市、学历、总开发年限、AI 年限及语言硬门槛。

- [腾讯：微信－大模型（Agent）应用开发后台工程师](https://careers.tencent.com/jobdesc.html?postId=2037392065205268480)：Agent 后台架构、复杂任务规划/工具调用、多轮决策、RAG/Function Calling，以及亿级用户下的高并发、低延迟、高可用；C++ 属于该岗位硬门槛，因此只作当前能力标杆。
- [腾讯：大语言模型应用工程师（Agent 方向）](https://careers.tencent.com/jobdesc.html?postId=2034114867123875840)：Agent 全链路、Prompt/Skill、Agentic RAG、效果评估、性能调优、线上问题排查、可复用组件和跨团队产品化；与当前应用开发主线最接近。
- [腾讯 PCG：AI 应用开发工程师（Agent 方向）](https://careers.tencent.com/jobdesc.html?postId=2026845083588001792)：Planning、长期 Memory、Multi-Agent、Durable Execution、沙箱、Skills/MCP 和评测优化飞轮；作为复合工作场景与旗舰深度的主要标杆。
- [腾讯：AI Agent 开发工程师（游戏研发）](https://tencent.wd1.myworkdayjobs.com/en-US/internal_bole/job/AI-Agent--_R107498)：强调接入真实工业工具链，以及任务成功率、人工节省时长、质量、一致性、稳定性和安全性的评估；游戏/UE 经验不满足时只取其工程要求。
- [京东健康：软件开发岗](https://zhaopin.jd.com/web/job/job_info_list/3?requirementId=217987)：Agent/RAG 落地与稳定后端并重，涉及 Java/Spring、事务、缓存、消息和分布式；Python 主线不能冒充满足其 Java 硬门槛。
- [京东探索研究院：算法工程师](https://www.zhaopin.com/jobdetail/CC192921310J40774593609.htm)：RAG、Agent、工具调用之外还要求后训练、深度学习框架和论文/比赛，代表算法混合岗上限，不据此扩充当前应用岗训练主线。

标杆结论与课程动作：

- **前移/强化**：大厂后端基本功、长期 Memory、Durable Execution、工具沙箱与权限、RAG 数据治理、评估 holdout/回归、线上排错、性能/成本、PR/CI 和事故复盘。
- **保留**：Python/FastAPI + PostgreSQL/Redis + LangGraph + RAG + MCP 的两旗舰主线，用系统设计与复合故障证明可迁移工程能力。
- **降级为岗位相关**：Java/C++ 第二实现、训练/微调/RLHF、vLLM/TensorRT、UE/游戏工具链；只有目标岗位硬门槛明确且用户决定转向时再开支线。

## 2026-07-10 JD 基线审计

本次只有 4 条方向性能力样本，其中包含校招/在校生岗位；只用于校准技术深度，不作为用户真实可投岗位匹配率。首轮合格的可投社招样本在 W6 按上面的审计方法补齐。

- Python 后端、FastAPI/Flask、async、Pydantic/分层、SQL/Redis。
- RAG 全链路：解析、chunk、embedding、向量库、hybrid/rerank、评估与更新。
- Agent/Tool Calling、上下文/记忆、异常恢复、安全接入、LangGraph 等编排。
- Linux、Docker、CI/CD、性能/高并发、可观测与评估。
- 训练/LoRA/vLLM/Kubernetes/多模态属于岗位相关加分或算法混合岗，不全部纳入主线硬门槛。

抽样来源：

- [2026 校招：Agent/RAG/async/FastAPI/Pydantic/PostgreSQL/Redis](https://career.cuhk.edu.cn/attachment/careercuhk/ueditor/file/20260515/2071_%E7%86%B5%E5%9F%BA%E5%BE%8B%E5%8A%A8%20-%202026%E6%A0%A1%E5%9B%AD%E6%8B%9B%E8%81%98.pdf)
- [大模型应用工程师：Celery/SQLAlchemy/async/CI-CD/K8s](https://www.shushuqiuzhi.com/position/280081)
- [AI 应用/RAG：hybrid/rerank/pgvector/MCP/observability](https://www.gzlpsyaj.com/correcruit/content/id/54911.html)
- [RAG 与智能体：Prompt A/B、Tool Calling、Agent、Python 服务](https://jobs.morganphilips.cn/en-cn/ai%E5%A4%A7%E6%A8%A1%E5%9E%94%E7%94%A8%E5%B7%A5%E7%A8%8B%E5%B8%88-rag%E4%B8%8E%E6%99%BA%E8%83%BD%E4%BD%93%E6%96%B9%E5%90%91-shenzhen-153501/)

当前结论：尚未达到稳定投递的岗位证据门槛。A4-Gate 已把 Agent 控制循环、最小安全门和早期 eval/日志能力升级到 `COURSE_PASS`，但没有自动生成 `JOB_EVIDENCE`；下一条证据链是 `G8-00 → BE5-Gate → 旗舰二`。W10 最小部署完成后先校准项目描述和 2–3 条硬可投岗位，W12 领域 RAG 旗舰成形后再开始小范围试投递。个人真实匹配率仍须等 W6 补齐硬门槛字段和合格样本，不能由本次课程 Gate 代替。

## 审计记录

| 内容块/日期 | JD 样本 | 主要变化 | 影响的课程/Gate | 结论 |
| --- | --- | --- | --- | --- |
| 2026-07-10 / W4 | 近期岗位方向性样本 | Python 后端、生产 RAG、持久化 Agent、评估回归、安全和 CI/CD 深度不足 | 新增 BE5；升级 R6/G8/M9/E10/J11/FINAL | 维持应用岗主线，延长到 W20 |
| 2026-07-22 / 路线改造复审 | 大厂能力标杆 + 近期应用岗方向性样本；因个人硬门槛字段未齐，不计算匹配率 | 主流框架基础、最小部署和业务型作品证据出现偏晚；H5 教学框架源码任务性价比偏低 | 前移 G8-00；H5 压成可选单链路；BE5-Gate 完成最小部署；R6 改为领域/业务旗舰 | 修订方案 PASS；不改变当前 A4-04，不扩第二后端/模型训练主线 |
| 2026-08-24 / A4-Gate | 未新增 JD 样本；本行只做 Gate 证据校准 | Agent 控制循环、最小安全门、固定 eval/holdout 和结构化日志已形成课程证据；仍缺服务化、维护型自动测试、README/架构、CI/部署与岗位证据独立复核 | Agent 控制循环、安全与权限、评估与可观测升 `COURSE_PASS`；下一主块 G8-00，随后 BE5-Gate | 课程 Gate PASS；不升级 `JOB_EVIDENCE`，不触发强制岗位证据交叉复核 |
| W6 | 待核验大厂标杆 4–6 条 + 在招样本 10 条（≥7 `HARD_ELIGIBLE`） |  |  |  |
| W12 | 待核验大厂标杆 4–6 条 + 在招样本 10 条（≥7 `HARD_ELIGIBLE`） |  |  |  |
| W16 | 待核验大厂标杆 4–6 条 + 在招样本 10 条（≥7 `HARD_ELIGIBLE`） |  |  |  |
| W19 | 待核验大厂标杆 4–6 条 + 在招样本 10 条（≥7 `HARD_ELIGIBLE`） |  |  |  |

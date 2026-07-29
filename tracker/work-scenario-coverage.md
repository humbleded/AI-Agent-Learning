# 工作场景与复合故障覆盖

最后校准：2026-07-30。

本表是“实际工作问题是否被练过、实跑过、修过并在故障下恢复过”的唯一事实源。`tracker/weak-points.md` 记录已经暴露的个人易错点；本表同时记录**尚未覆盖**的工作场景，两者不能互相替代。

## 证据等级

- `NOT_VERIFIED`：尚无正式验证，不能因为课程标题出现过就算覆盖。
- `EXPLAINED`：能口述判断问题，但没有运行真实代码或命令。
- `EXECUTED`：在真实代码、测试、日志、trace 或接口上执行过并得到可观察结果。
- `DIAGNOSED_AND_FIXED`：独立完成复现、定位、修复和回归验证。
- `RECOVERED_UNDER_FAULT`：在注入故障、进程退出、依赖下线或恶意输入下完成止损/降级/恢复，并证明没有关键回归或重复副作用。

`JOB_EVIDENCE` 候选中的核心工作场景至少达到 `DIAGNOSED_AND_FIXED`；恢复、部署、安全和持久化类场景应达到 `RECOVERED_UNDER_FAULT`。纯口述最多记为 `EXPLAINED`。

## 复合题与复合事故规则

- 一道复合题是**一个完整事故包**，可以同时包含 2–4 类问题，例如 provider 429、SSE 断连、后台任务重试和重复写入。它仍算一个高价值检查点，不拆成一屏十道互不相干的小问。
- 用户第一步要找出所有重要问题并按影响排序，不能只命中最显眼的报错；随后按“止损/隔离 → 复现 → 根因定位 → 最小修复 → 回归/故障注入 → 取舍与复盘”推进。
- 同一事故可以给多个类别升级证据，但每个类别都要分别记录命令、关键输出和证据路径；不能用一句“综合题做过了”把全部类别一起判 PASS。
- 题目只能组合 `progress.md` 已 PASS 或当前任务已经正式引入的知识。大厂标杆决定工程深度，不允许拿尚未教学的高阶术语突然考用户。
- 编码、Gate、项目日优先选择本表中最久未验证、等级最低或本 Gate 强制要求的类别；不得连续多次只练同一种安全题而遗漏并发、恢复、部署等类别。

## 覆盖矩阵

| ID | 工作场景类别 | 典型复合问题 | 最早正式引入 | 主要硬检查点 | 当前等级 | 最近证据/日期 | 下次必须命中 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| WS-01 | 需求澄清与 API/事件契约 | 模糊需求、冲突验收条件、接口兼容、变更影响 | A4-Gate | A4/BE5/R6/E10/J11 | NOT_VERIFIED |  | A4-Gate |
| WS-02 | 日志、指标与运行轨迹排错 | 错误堆栈、request ID、错误率/p95、根因与表象 | A4-Gate | BE5/G8/E10/J11/FINAL | DIAGNOSED_AND_FIXED | `daily/2026-07-29.md`、`daily/2026-07-30.md`：沿 `None → history → 第 3 步 prompt → .strip()` 复现、定位、修复并完成 39/39 回归 | A4-Gate（补 request/trace ID 与结构化日志） |
| WS-03 | 测试、CI 与回归 | 单测通过但集成失败、flaky、eval 回归、发布门禁 | P0-07/L1-Gate | BE5/E10/J11/FINAL | DIAGNOSED_AND_FIXED | `daily/2026-07-11.md`（7/12 正式复核）：空端口缺陷复现/修复 6/6，随后 `t3-gate-v2` 全量 14/14、holdout 3/3 | BE5-Gate |
| WS-04 | 并发、取消与流中断 | 超时、SSE 断连、悬挂任务、背压、部分失败 | BE5-02 | BE5/G8/J11/FINAL | NOT_VERIFIED |  | BE5-Gate |
| WS-05 | 模型/provider 韧性与成本 | 429、Retry-After、退避+jitter、配额耗尽、fallback、context 超限 | T3-04/S-01 | BE5/E10/FINAL | DIAGNOSED_AND_FIXED | `daily/2026-07-08.md`、`daily/2026-07-11.md`；`daily/2026-07-29.md`～`2026-07-30.md`：适配器 `None` 故障降级、干净 history 与正常路径回归 | BE5-Gate（补 429/Retry-After、退避与 fallback） |
| WS-06 | 身份、授权与多租户 | 猜 ID、跨用户读写、ACL filter、principal 丢失、日志越权 | BE5-05 | BE5/R6/M9/FINAL | NOT_VERIFIED |  | BE5-Gate |
| WS-07 | 工具与 Agent 安全 | 坏参数、路径逃逸、SSRF、间接注入、secret/PII 外泄、过度授权 | T3-03/T3-Gate | A4/R6/M9/FINAL | DIAGNOSED_AND_FIXED | `daily/2026-07-11.md`（7/12 正式复核）：空端口修复、未知工具/SSRF/302/路径逃逸拦截及再注入 | A4-Gate |
| WS-08 | 数据库、迁移与幂等 | 事务回滚、迁移失败、重复提交、缓存不一致、恢复后重复写 | B0-03/BE5-04 | BE5/R6/G8/FINAL | NOT_VERIFIED |  | BE5-Gate |
| WS-09 | 后台任务与队列 | worker 崩溃、重复投递、重试风暴、取消、死信/积压 | BE5-05 | BE5/R6/J11/FINAL | NOT_VERIFIED |  | BE5-Gate |
| WS-10 | RAG 数据与质量生命周期 | 解析失败、旧向量残留、ACL、检索差、引用错、无答案、注入 | R6-01 | R6/E10/FINAL | NOT_VERIFIED |  | R6-Gate |
| WS-11 | Agent state、checkpoint 与恢复 | replay、节点重跑、HITL 超时、重复副作用、跨 thread 串状态 | G8-02 | G8/FINAL | NOT_VERIFIED |  | G8-Gate |
| WS-12 | MCP 连接、授权与审计 | 能力发现、断连重连、scope/audience、token 泄漏、恶意 server | M9-02 | M9/FINAL | NOT_VERIFIED |  | M9-Gate |
| WS-13 | 部署、健康检查与回滚 | 配置/secret、启动失败、readiness、备份恢复、灰度/回滚 | BE5-Gate | BE5/R6/J11/FINAL | NOT_VERIFIED |  | BE5-Gate（先 EXECUTED，J11 再故障恢复） |
| WS-14 | 性能、容量、SLO 与成本 | 吞吐、p95、错误预算、资源瓶颈、token 成本突增、降级 | L1-05/BE5 | BE5/R6/E10/J11/FINAL | NOT_VERIFIED |  | BE5-Gate |
| WS-15 | Git/PR 与团队协作 | issue、branch、review、CI 失败、冲突、revert、变更说明 | J11-01 | J11/FINAL | NOT_VERIFIED |  | J11-01 |
| WS-16 | 长期 Memory 生命周期 | 跨会话写入/更新/删除、TTL、冲突、租户隔离、PII、poisoning | D7-03 | D7/G8/FINAL | NOT_VERIFIED |  | D7-Gate |

A4–M9 的“运行轨迹”可以是结构化日志或单次可复现步骤，不要求提前建设 tracing 平台；E10/J11 才要求完整 tracing。D7/R6 等较早阶段的 eval/baseline 使用复用的小数据集、项目测试和紧凑对比表，不另建通用评估框架。

## Gate 最低覆盖

除下方另有更高要求外，列出的类别在该 Gate 至少达到 `EXECUTED`；题面要求修改代码、配置或数据时，相关类别必须达到 `DIAGNOSED_AND_FIXED`。只口述判断不能满足 Gate 覆盖。

- `T3-Gate`：WS-03、WS-05、WS-07；至少一个场景组合“坏工具调用 + 外部 API 故障/恶意 URL”。
- `A4-Gate`：WS-01、WS-02、WS-05、WS-07；先把含糊需求写成可测试的 problem contract，再完成至少一个“模型/工具失败 + 日志定位 + 安全停止”场景。
- `BE5-Gate`：WS-01、WS-03、WS-04、WS-05、WS-06、WS-08、WS-09、WS-13、WS-14；WS-13 在本关至少达到可重复部署与 smoke 的 `EXECUTED`，完整回滚/恢复留到 J11-04；其余至少两个复合事故达到 `DIAGNOSED_AND_FIXED`，其中一个达到 `RECOVERED_UNDER_FAULT`。
- `R6-Gate`：WS-02、WS-03、WS-06、WS-08、WS-10、WS-14；关键越权/泄漏案例必须全部拦截。
- `D7-Gate`：WS-16，并复用同一轻量数据集/项目测试对比模式变更前后的质量、延迟和成本。
- `G8-Gate`：WS-02、WS-04、WS-08、WS-11、WS-16；必须演示进程退出后恢复且不重复副作用。
- `M9-Gate`：WS-02、WS-06、WS-07、WS-12；授权、断连和审计至少一个复合事故达到 `RECOVERED_UNDER_FAULT`。
- `J11/FINAL`：补齐 WS-01~16 中与旗舰有关的全部类别；至少完成一次“告警 → 止损/降级 → 定位 → 修复 → 回归 → 上线/回滚 → postmortem”综合演练。

## 记录模板

| 日期/任务 | 场景 ID（可多个） | 事故摘要 | 故障输入/复现命令 | 根因与优先级 | 修复/止损 | 回归与恢复证据 | 升级后等级 | 证据路径 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2026-07-12 / T3-Gate | WS-03 | 宽松 URL 解析让空端口绕过原端口判断，并需确认修复未破坏三工具回归 | 内存注入无端口、`:443`、`:8443`、空 `:`、文本/越界端口；随后按 `eval_cases.json` contract 直接全量执行 | `.port is None` 不能区分未写端口与空端口；总体通过率也不能稀释安全分项 | 用户加入 `netloc.endswith(":")` 前置拒绝并同步注释；保留分项阈值/holdout | 端口 6/6；两次独立全量均 14/14，holdout 3/3，failed IDs `[]` | DIAGNOSED_AND_FIXED | `code/stage3/t3_gate_tool_assistant.py`；`code/stage3/eval_cases.json`；`daily/2026-07-11.md` |
| 2026-07-12 / T3-Gate | WS-05 | 外部 API timeout 与真实 provider/API 正常路径同场验证 | D01 mock `requests.Timeout`；N03/N10 真实 `https://api.github.com` | 外部依赖可能超时；异常分支不能依赖不存在的 response | `timeout=5`，分别捕获 Timeout/RequestException 并返回稳定 dict | timeout 再注入稳定返回；真实 API 为 HTTP 200；相关 failure/danger 全部通过 | EXECUTED | `code/stage3/t3_04_public_api_tool.py`；`daily/2026-07-11.md` |
| 2026-07-12 / T3-Gate | WS-07 | 未知工具 + metadata SSRF + 302 到 loopback + 路径逃逸的复合危险输入 | D01 内存 mock；额外注入 `../...`、归一化逃逸和 `C:\Windows\win.ini` | 动态工具名、只查 URL 字符串前缀、默认跟随重定向、未看路径最终落点都会越界 | `TOOLS` 白名单、解析后 host/port allowlist、禁用重定向、`resolve/relative_to` 沙箱、防坏参数 | 未知/SSRF 执行前拒绝，302 跟随 0；危险路径均拒绝；D01 全断言通过并再次注入保持安全停止 | DIAGNOSED_AND_FIXED | `code/stage3/t3_gate_tool_assistant.py`；`code/stage3/t3_03_file_reader_tool.py`；`daily/2026-07-11.md` |
| 2026-07-30 / A4-04 | WS-02 | Executor 第 2 步收到 `None` 后污染 history，第 3 步 prompt 携带脏状态，最终在事实复盘的 `.strip()` 暴露异常 | stdin 内存适配器依次返回 `r1 / None / r3`；正式复核聚焦套件 39 项 | 最早根因是非字符串越过 `StepResult` 边界；history 污染是中间状态，`.strip()` 的 `AttributeError` 是末端症状 | 在 `results/history` append 前执行 `None → ""`；通过 spy 检查第 3 步 prompt | 单步边界、三步轨迹、复盘与正常 demo 全部回归；正式套件 39/39 | DIAGNOSED_AND_FIXED | `code/stage4/a4_04_plan_solve_demo.py`；`daily/2026-07-29.md`；`daily/2026-07-30.md` |
| 2026-07-30 / A4-04 | WS-05 | 模型适配器异常分支返回 Python `None`，静态执行链需要稳定降级而不把非法类型继续传给后续模型 | 同上；修复前实际得到 `('s2', None)` 与 `AttributeError`，修复后得到 `('s2', '')` | 适配器违反 `str -> str` 合同，而 Executor 缺少进入状态前的运行时归一化 | 把 `None` 降级为空失败结果；复盘根据空结果标记任务未完成 | 再注入后流程不崩、history 无 `None`、最终状态未完成；完整正常路径仍通过 | DIAGNOSED_AND_FIXED | `code/stage4/a4_04_plan_solve_demo.py`；`daily/2026-07-29.md`；`daily/2026-07-30.md` |

# 工作场景与复合故障覆盖

最后校准：2026-07-10。

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
| WS-01 | 需求澄清与 API/事件契约 | 模糊需求、冲突验收条件、接口兼容、变更影响 | A4-Gate | BE5/R6/E10/J11 | NOT_VERIFIED |  | BE5-Gate |
| WS-02 | 日志、指标与 trace 排错 | 错误堆栈、request ID、错误率/p95、根因与表象 | A4-Gate | BE5/G8/E10/J11/FINAL | NOT_VERIFIED |  | A4-Gate |
| WS-03 | 测试、CI 与回归 | 单测通过但集成失败、flaky、eval 回归、发布门禁 | P0-07/L1-Gate | BE5/E10/J11/FINAL | NOT_VERIFIED |  | T3-Gate |
| WS-04 | 并发、取消与流中断 | 超时、SSE 断连、悬挂任务、背压、部分失败 | BE5-02 | BE5/G8/J11/FINAL | NOT_VERIFIED |  | BE5-Gate |
| WS-05 | 模型/provider 韧性与成本 | 429、Retry-After、退避+jitter、配额耗尽、fallback、context 超限 | T3-04/S-01 | BE5/E10/FINAL | EXECUTED | `daily/2026-07-08.md`：timeout、RequestException、rate limit 分支 | T3-Gate |
| WS-06 | 身份、授权与多租户 | 猜 ID、跨用户读写、ACL filter、principal 丢失、日志越权 | BE5-05 | BE5/R6/M9/FINAL | NOT_VERIFIED |  | BE5-Gate |
| WS-07 | 工具与 Agent 安全 | 坏参数、路径逃逸、SSRF、间接注入、secret/PII 外泄、过度授权 | T3-03/T3-Gate | A4/R6/M9/FINAL | EXECUTED | `daily/2026-07-07.md`、`daily/2026-07-09.md`：沙箱逃逸、白名单、坏 Action | T3-Gate |
| WS-08 | 数据库、迁移与幂等 | 事务回滚、迁移失败、重复提交、缓存不一致、恢复后重复写 | B0-03/BE5-04 | BE5/R6/G8/FINAL | NOT_VERIFIED |  | BE5-Gate |
| WS-09 | 后台任务与队列 | worker 崩溃、重复投递、重试风暴、取消、死信/积压 | BE5-05 | BE5/R6/J11/FINAL | NOT_VERIFIED |  | BE5-Gate |
| WS-10 | RAG 数据与质量生命周期 | 解析失败、旧向量残留、ACL、检索差、引用错、无答案、注入 | R6-01 | R6/E10/FINAL | NOT_VERIFIED |  | R6-Gate |
| WS-11 | Agent state、checkpoint 与恢复 | replay、节点重跑、HITL 超时、重复副作用、跨 thread 串状态 | G8-02 | G8/FINAL | NOT_VERIFIED |  | G8-Gate |
| WS-12 | MCP 连接、授权与审计 | 能力发现、断连重连、scope/audience、token 泄漏、恶意 server | M9-02 | M9/FINAL | NOT_VERIFIED |  | M9-Gate |
| WS-13 | 部署、健康检查与回滚 | 配置/secret、启动失败、readiness、备份恢复、灰度/回滚 | J11-04 | J11/FINAL | NOT_VERIFIED |  | J11-04 |
| WS-14 | 性能、容量、SLO 与成本 | 吞吐、p95、错误预算、资源瓶颈、token 成本突增、降级 | L1-05/BE5 | BE5/R6/E10/J11/FINAL | NOT_VERIFIED |  | BE5-Gate |
| WS-15 | Git/PR 与团队协作 | issue、branch、review、CI 失败、冲突、revert、变更说明 | J11-01 | J11/FINAL | NOT_VERIFIED |  | J11-01 |
| WS-16 | 长期 Memory 生命周期 | 跨会话写入/更新/删除、TTL、冲突、租户隔离、PII、poisoning | D7-03 | D7/G8/FINAL | NOT_VERIFIED |  | D7-Gate |

## Gate 最低覆盖

除下方另有更高要求外，列出的类别在该 Gate 至少达到 `EXECUTED`；题面要求修改代码、配置或数据时，相关类别必须达到 `DIAGNOSED_AND_FIXED`。只口述判断不能满足 Gate 覆盖。

- `T3-Gate`：WS-03、WS-05、WS-07；至少一个场景组合“坏工具调用 + 外部 API 故障/恶意 URL”。
- `A4-Gate`：WS-02、WS-05、WS-07；至少一个场景组合“模型/工具失败 + 日志定位 + 安全停止”。
- `BE5-Gate`：WS-01、WS-03、WS-04、WS-05、WS-06、WS-08、WS-09、WS-14；至少两个复合事故达到 `DIAGNOSED_AND_FIXED`，其中一个达到 `RECOVERED_UNDER_FAULT`。
- `R6-Gate`：WS-02、WS-03、WS-06、WS-08、WS-10、WS-14；关键越权/泄漏案例必须全部拦截。
- `D7-Gate`：WS-16，并用同一 eval 对比模式变更前后的质量、延迟和成本。
- `G8-Gate`：WS-02、WS-04、WS-08、WS-11、WS-16；必须演示进程退出后恢复且不重复副作用。
- `M9-Gate`：WS-02、WS-06、WS-07、WS-12；授权、断连和审计至少一个复合事故达到 `RECOVERED_UNDER_FAULT`。
- `J11/FINAL`：补齐 WS-01~16 中与旗舰有关的全部类别；至少完成一次“告警 → 止损/降级 → 定位 → 修复 → 回归 → 上线/回滚 → postmortem”综合演练。

## 记录模板

| 日期/任务 | 场景 ID（可多个） | 事故摘要 | 故障输入/复现命令 | 根因与优先级 | 修复/止损 | 回归与恢复证据 | 升级后等级 | 证据路径 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |

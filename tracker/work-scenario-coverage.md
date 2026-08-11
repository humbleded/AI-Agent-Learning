# 工作场景与复合故障覆盖

最后校准：2026-08-11。

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
| WS-01 | 需求澄清与 API/事件契约 | 模糊需求、冲突验收条件、接口兼容、变更影响 | A4-Gate | A4/BE5/R6/E10/J11 | DIAGNOSED_AND_FIXED | `daily/2026-08-05.md`～`2026-08-11.md`：合同与 C1～C3d 落地；Observation 派生 allowlist、Reflection 普通文本、Refinement JSON Output、SDK 响应外壳、最终三字段 / 来源子集硬门及 topic/path 真实正常链均已闭合 | A4-Gate C4a（失败状态映射 + 七字段日志 + 一次工具重试 / `max_steps` 安全停止复合轨迹） |
| WS-02 | 日志、指标与运行轨迹排错 | 错误堆栈、request ID、错误率/p95、根因与表象 | A4-Gate | BE5/G8/E10/J11/FINAL | DIAGNOSED_AND_FIXED | `daily/2026-07-29.md`、`daily/2026-07-30.md`：沿 `None → history → 第 3 步 prompt → .strip()` 复现、定位、修复并完成 39/39 回归 | A4-Gate（补 request/trace ID 与结构化日志） |
| WS-03 | 测试、CI 与回归 | 单测通过但集成失败、flaky、eval 回归、发布门禁 | P0-07/L1-Gate | BE5/E10/J11/FINAL | DIAGNOSED_AND_FIXED | `daily/2026-08-08.md`～`2026-08-11.md`：从 HTTP 1xx、Tool Calling SDK 形状和 validator 守门一路扩到 C3d 完整集成；2026-08-11 正式无落盘矩阵 129/129、独立合同 40/40 与 fail-closed 3/3，真实 topic/path 各 4 次模型 + 1 次对应工具通过 | A4-Gate（补统一控制器故障回归与 14 条 Agent 全量 eval）；BE5-Gate |
| WS-04 | 并发、取消与流中断 | 超时、SSE 断连、悬挂任务、背压、部分失败 | BE5-02 | BE5/G8/J11/FINAL | NOT_VERIFIED |  | BE5-Gate |
| WS-05 | 模型/provider 韧性与成本 | 429、Retry-After、退避+jitter、配额耗尽、fallback、context 超限 | T3-04/S-01 | BE5/E10/FINAL | RECOVERED_UNDER_FAULT | `daily/2026-08-04.md`：真实 Reflection/Refinement 故障恢复 12/12；`daily/2026-08-08.md`：工具依赖故障分类；`daily/2026-08-10.md`～`2026-08-11.md`：空响应、坏外壳、非 `stop`、坏 JSON、失败 Observation 均 fail-closed，真实双路径以 `stop` 完成；A4-Gate 当前仍无统一重试恢复 | A4-Gate（模型/工具失败、一次重试与安全停止）；BE5-Gate（补 Retry-After、退避与 fallback） |
| WS-06 | 身份、授权与多租户 | 猜 ID、跨用户读写、ACL filter、principal 丢失、日志越权 | BE5-05 | BE5/R6/M9/FINAL | NOT_VERIFIED |  | BE5-Gate |
| WS-07 | 工具与 Agent 安全 | 坏参数、路径逃逸、SSRF、间接注入、secret/PII 外泄、过度授权 | T3-03/T3-Gate | A4/R6/M9/FINAL | DIAGNOSED_AND_FIXED | A4 C1～C3d（`daily/2026-08-07.md`～`2026-08-11.md`）：工具白名单、请求原值绑定和严格成功 Observation 均已闭合；真实 topic/path 完整链仍只执行一个匹配工具，允许来源只从本轮 path / `results[*].url` 派生，虚构来源在实际 validator 处 fail-closed | A4-Gate（补 HITL 允许 / 拒绝、受控 `needs_manual` 与安全停止） |
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
| 2026-08-04 / A4-05 | WS-03 | DeepSeek 适配器请求契约错误：模型常量与 thinking 字段不符合项目约定 | fake SDK 首测 `12/15 PASS`；正式复核运行内存契约断言与真实主程序 | 实现使用了错误模型名，并把 thinking 开关放在顶层参数；注释/意图不能替代实际请求字段 | 改用固定 `deepseek-v4-pro`，通过 `extra_body` 关闭 thinking；保留缺 key、`None → ""` 和输出审计 | 用户订正后 15/15；正式 39/39、`py_compile`、真实正常与故障路径全部通过 | DIAGNOSED_AND_FIXED | `code/stage4/a4_05_reflection_writer.py`；`daily/2026-08-04.md` |
| 2026-08-04 / A4-05 | WS-05 | 真实模型正常初稿总是合格，改进分支未自然覆盖；同时需验证坏模型输出不会直接成为最终稿 | 正常命令 2 次真实调用提前停止；验证包装器只注入缺固定日期/地点的首稿，后 2 次委托真实 DeepSeek | 自然采样不能稳定制造坏初稿；修改停止条件会破坏生产逻辑；模型反馈本身不能代替同标准硬校验 | 首稿注入仅限验证边界；真实 Reflection/Refinement 生成修订；候选必须重跑 `evaluate_draft()`，失败时回退初稿 | 故障分支 12/12，候选日期/地点/长度全通过并被接受；正常路径仍为 2 次调用、无回归 | RECOVERED_UNDER_FAULT | `code/stage4/a4_05_reflection_writer.py`；`daily/2026-08-04.md` |
| 2026-08-06 / A4-Gate 设计 | WS-01 | 把“按研究主题或沙箱路径生成摘要”的模糊需求收敛成可执行合同，并明确跨日范围与用户/助手职责 | 对 `problem-contract.md` 执行无持久 runner 的编码安全静态核验：章节 11/11、关键安全/循环/评估项 7/7、TODO 0 | 原始任务未限定输入分支、证据来源、失败状态、重试/停止和人工确认；文档任务边界一度让用户承担机械整理 | 固定请求/结果/工具合同、来源真实性、停止/重试、风险确认、日志和 14 条评估蓝图；实现留到下一 A4 Session | 设计与静态检查通过，但 Agent 代码、真实工具失败、日志轨迹和安全停止尚未执行 | EXPLAINED | `code/stage4/problem-contract.md`；`daily/2026-08-05.md`；`daily/2026-08-06.md` |
| 2026-08-07 / A4-Gate C1 | WS-01 | 把已冻结的输入/失败合同落实为固定结果构造和可执行请求前置边界 | 一体式初稿聚焦诊断 0/5；最终 `.venv\Scripts\python.exe -W error -m py_compile ...` + 无落盘聚焦检查 133/133 | 初稿未返回规范化值、漏校验 `input_type`、把文件存在性放错层，并使实现与字段合同漂移 | 拆分形状、字符串规范化、类型白名单、主题和路径值校验，再由 `prepare_request` 统一编排；同步合同中的 `input_type.strip()` | 编译通过；合法/非法/边界输入 133/133；只证明输入合同切片，尚无完整 Agent 轨迹 | EXECUTED | `code/stage4/problem-contract.md`；`code/stage4/a4_gate_research_summary_agent.py`；`daily/2026-08-07.md` |
| 2026-08-07 / A4-Gate C1 | WS-07 | 路径输入曾错误相对项目根解释、放行绝对路径/URL，并误拒绝沙箱根目录 `.` | 路径聚焦结果 `2/6 → 3/6 → 4/6 → 5/6 → 10/10`；正式总检查再注入 HTTPS/FTP/file URL、沙箱内外绝对路径和多级逃逸 | 混淆输入形式与最终落点；`.parents` 不含路径自身；URL 成员判断方向错误；输入层不应检查文件是否存在 | 先拒绝常见 URL/绝对形式，再用 `SANDBOX.resolve()` + `target.relative_to(sandbox_root)` 校验解析后归属 | C1 总回归 133/133；无 `://` scheme、工具执行时二次校验与 HITL/安全停止留到后续 A4 eval | DIAGNOSED_AND_FIXED | `code/stage4/a4_gate_research_summary_agent.py`；`daily/2026-08-07.md` |
| 2026-08-08 / A4-Gate C2 | WS-03、WS-05 | Wikipedia 搜索适配器真实主链可用，但首次回归未覆盖 HTTP 1xx 状态域 | 内存 mock/spy 首测 `13/23`，订正后 39/39、独立复核 310/310；提交前再注入先得 5/7，修复后本地 131/131、独立 646/646 | 既有请求/异常/结构根因均已修；新增根因是状态分支只覆盖 3xx～5xx，未把 1xx 纳入“所有非 2xx”拒绝集合，导致 100/199 解析合法空 JSON 后误报成功 | 保留固定参数、3xx～5xx/JSON/API/结构订正；新增 `status_code < 200` 的解析前不可重试失败分支 | 100/199 均在 JSON 前停止；200/299、3xx～5xx、异常与结构边界无回归；真实查询 3 条和零命中通过，完整 Agent 重试/安全停止仍待后续 | DIAGNOSED_AND_FIXED | `code/stage4/a4_gate_research_summary_agent.py`；`daily/2026-08-08.md` |
| 2026-08-08 / A4-Gate C2 | WS-07 | 文件工具需要在模型参数进入执行边界后再次校验输入与最终落点，同时不能用广泛异常捕获掩盖程序 bug | 系统临时沙箱注入空白/非字符串、父级逃逸、URL、绝对路径、目录、坏 UTF-8、PermissionError 与意外 RuntimeError | 首稿跳过运行时规范化并捕获 `Exception`；之后虽收窄异常，仍一度把内部 RuntimeError 伪装成资料读取失败 | 复用字符串规范化；以解析后目标相对沙箱根校验归属；只把 UnicodeDecodeError/OSError 映射为工具失败，让意外 RuntimeError fail-fast | `9/12 → 12/12 → 14/14`；C1 冒烟 5/5，无输入边界回归；HITL 与工具白名单分发留到完整循环 | DIAGNOSED_AND_FIXED | `code/stage4/a4_gate_research_summary_agent.py`；`daily/2026-08-08.md` |
| 2026-08-10 / A4-Gate C3c | WS-01、WS-03 | 宽松 fake 曾掩盖旧 Tool Calling 字段、SDK 对象访问、重复 assistant、无效 ID 与空 choices 保护顺序问题 | 使用忠实 SDK 属性对象、None / 空 / 多 Tool Call、重复消息和第二响应无效外壳逐项注入；再跑 topic / path 真实 DeepSeek | 混用旧 `functions` 协议与当前 `tools`；把 SDK 对象当 dict；请求与 Observation 消息职责重复；索引前未保护容器 / 对象 | 改用当前 tools/tool_calls 与 non-thinking；原 assistant 只回填一次；按精确 ID 构造 Tool Message；第二轮禁止工具并校验正文 | R3 15/15、R4a 7/7、双路径 68/68、主审 89/89、独立 112/112；真实 topic/path 均通过 | DIAGNOSED_AND_FIXED | `code/stage4/a4_gate_research_summary_agent.py`；`daily/2026-08-09.md`；`daily/2026-08-10.md` |
| 2026-08-10 / A4-Gate C3b-C3c | WS-05、WS-07 | 模型可请求已注册但错误的工具 / 参数，失败 Observation 或 truthy 非布尔成功值又可能继续生成候选 | 注入未知工具、坏 JSON、错路由 / 改值、非法 ID、`ok=False`、缺失 `ok`、`ok=1` 与工具意外错误；检查工具与第二模型调用次数 | Schema 不是客户端硬边界；未绑定本轮规范化请求；truthiness 不能证明严格 `True`；正常链未隔离失败 Observation | 白名单 + 精确字段 + 请求原值绑定；ID 必须非空字符串；只有 `ok is True` 才允许第二轮，其余 fail-closed | C3b 14/14 + 9/9、R4b 5/5，非法分支无越界调用，正常双路径无回归；本切片只是确定性停止，尚无自动恢复 / HITL | DIAGNOSED_AND_FIXED | `code/stage4/a4_gate_research_summary_agent.py`；`daily/2026-08-09.md`；`daily/2026-08-10.md` |
| 2026-08-10 / A4-Gate C3d-C1～C3a | WS-01、WS-03、WS-07 | 模型候选是不可信输入：宽松来源 / 字段校验曾放行空白、虚构或混合来源，并因 guard 顺序错误泄漏异常；prompt 点名约束也一度只留在注释 | 逐层注入错路由、坏 Observation 结构、五 / 六类 prompt sentinel、缺 / 多键、错类型、空容器、空白元素、不可哈希元素、proper subset、全 / 混合越界来源；检查输入不变、模型 / 工具 / `make_result` 调用次数 | `and/or` 写反；`all([])` 真空通过；在证明 list 前调用 `len/.strip/set`；把 allowlist 当正文证据；把注释中的规则误当模型可见 prompt | 从本轮真实 Observation 派生 allowlist；prompt 同时携带完整 `content/results` 和来源边界；validator 按 list 类型 → 非空 → 元素 → exact-key / 精确状态 → 子集顺序 fail-closed | C3d 独立 `160/160`；主审代表矩阵 `76/76`；合法 `make_result` 只在允许分支调用；真实 topic/path 再次取得 Observation 并成功构造 allowlist / Reflection 输入。尚未执行两次模型调用与 JSON 集成 | DIAGNOSED_AND_FIXED | `code/stage4/a4_gate_research_summary_agent.py`；`daily/2026-08-10.md` |
| 2026-08-11 / A4-Gate C3d-I1～I4 | WS-01、WS-03、WS-05、WS-07 | 单函数看似完成但完整链接不上：SDK 属性对象被当 dict、`finish_reason` 读错层、缺属性泄漏；client factory 早于纯函数校验；入口又误读 `prepare_request` 与 C3c 中间结果合同 | SDK-shaped None/缺字段/`length`/意外 tools/坏 JSON/虚构来源、factory/short-circuit spy、topic/path 四模型单工具 fake；正式再跑 129 项无落盘断言和两条真实 DeepSeek 链 | 混淆业务 JSON 与 SDK 对象；没有沿真实返回合同逐层接线；副作用初始化早于确定性边界；只验证局部成功未证明 shared client 和失败短路 | 按 `response → choice → message` 守门，非 `stop`/坏 JSON 统一 fail-closed；纯函数先行、factory 后置；入口二项解包、内部三键精确取值、同一 client 串联 C3c/C3d | 主审 129/129；独立合同 40/40、实际 fail-closed 3/3 与入口矩阵 7/7；真实 topic/path 均 4 次模型、1 次对应工具、来源子集通过。尚未升级 WS-02 或声明恢复完成 | DIAGNOSED_AND_FIXED | `code/stage4/a4_gate_research_summary_agent.py`；`daily/2026-08-11.md` |

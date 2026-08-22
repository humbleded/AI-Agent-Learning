# A4-Gate 研究摘要 Agent：Problem Contract

状态：`DRAFT`（Problem Contract 第 1～11 节已完成；尚待 Agent 实现与 Gate 正式验收）

使用方式：本文件先定义需求与边界；合同确认后，再创建 Agent 代码与 eval 数据。

任务与通过标准来源：`tracker/ai-agent-learning-tracker.md` 的 `A4-Gate 最小 Agent 闯关`。

## 1. 目标用户与使用场景

- 学生在学习场景下使用本 Agent。

## 2. 要解决的任务

- 当输入为研究主题时，Agent 调用工具查找该主题的资料；当输入为沙箱内资料相对路径时，Agent 读取沙箱内资料；两种情况都输出包含 `status`、`summary`、`sources` 的结构化结果。

## 3. 输入契约

每次请求只接受一个 JSON 对象：

```json
{
  "input_type": "topic",
  "value": "Agent 是什么"
}
```

- `input_type`：必填，类型为 `str`。客户端先执行 `normalized_input_type = input_type.strip()`；结果为空时拒绝，再对规范化后的值执行白名单校验。只允许 `topic` 或 `relative_path`，其他值一律拒绝。每次请求只能选择其中一种输入语义。
- `value`：必填，类型为 `str`。客户端先执行 `normalized_value = value.strip()`；结果为空时拒绝输入，并返回第 4 节定义的失败格式。
- 当 `input_type == "topic"` 时，`normalized_value` 必须为 1～50 个字符，超过 50 个字符时拒绝。
- 当 `input_type == "relative_path"` 时：
  - 只接受沙箱内资料的相对路径；拒绝 URL 和所有绝对路径，包括指向沙箱内部的绝对路径。
  - 客户端先令 `sandbox_root = SANDBOX.resolve()`，再令 `target = (sandbox_root / normalized_value).resolve()`，以解析 `..` 和符号链接后的最终落点为准。
  - 客户端调用 `target.relative_to(sandbox_root)` 校验归属；若抛出 `ValueError`，说明最终落点越出沙箱，必须拒绝并返回第 4 节定义的失败格式。

## 4. 输出契约

每次返回都必须是包含 `status`、`summary`、`sources` 的 JSON 对象；三个字段均为必填字段。

- `status`：类型为 `str`；只允许 `success`、`invalid_input`、`tool_failure`、`insufficient_evidence`、`needs_manual`，其他值一律拒绝。
- `summary`：类型为 `str`；`success` 时填写基于实际资料形成的摘要正文，失败时填写安全、具体且非空的失败说明，不填写工具动作或虚构结论。
- `sources`：类型为 `list[str]`，每个元素必须是本轮工具实际取得且通过白名单校验的 URL 或沙箱相对路径，不得填写工具名、搜索词或虚构来源。客户端必须结合 `status` 解释该字段：`success` 时它表示已通过校验的摘要实际采用的来源；非 `success` 时若非空，它只表示供人工接管复核的真实证据池，不表示存在一份已通过校验的摘要。

成功示例：

```json
{
  "status": "success",
  "summary": "该输入契约规定，每次请求必须包含 input_type 和 value，并且 input_type 只允许取 topic 或 relative_path。",
  "sources": [
    "code/stage4/problem-contract.md"
  ]
}
```

当 `status == "success"` 时，`summary.strip()` 必须非空，`sources` 必须至少包含一个真实来源；缺少任何一项都不能认定成功。

失败状态的含义：

- `invalid_input`：输入违反第 3 节任一输入规则，客户端拒绝继续处理。
- `tool_failure`：完成当前请求所需的工具调用失败，且本次请求无法继续自动恢复；若已达到重试上限并需要用户决定下一步，则改用 `needs_manual`。
- `insufficient_evidence`：已取得的真实资料不足以支持摘要；不得编造结论或伪装成 `success`。
- `needs_manual`：达到重试上限、遇到必须由用户决定的阻塞条件或需要人工确认时，Agent 停止自治并交还控制权。

所有失败结果仍必须保留三个顶层字段。`summary` 必须是非空字符串并说明具体失败原因；`sources` 只能包含本次实际取得且通过白名单校验的来源，没有真实来源时必须为 `[]`，不得编造。若失败前已经取得部分真实来源，可以原样保留这些来源作为人工接管证据池，但不能据此把结果标记为成功，也不能把这些来源描述为某份已验证摘要的引用。候选摘要阶段返回 `needs_manual` 时，`summary` 还必须明确说明没有任何 Candidate / 摘要通过校验，非空 `sources` 仅供人工复核。

人工接管示例：

```json
{
  "status": "needs_manual",
  "summary": "search_web 连续超时并达到重试上限，仍无足够证据；Agent 已停止并交还用户决定下一步。",
  "sources": []
}
```

## 5. 允许调用的工具

### `read_material`

- 用途：当输入类型为 `relative_path` 时，读取该沙箱相对路径对应的资料内容，并把读取结果交回 Agent；不接受 URL 或绝对路径，也不用于搜索研究主题。
- 参数：`read_material(relative_path: str)`；客户端执行前必须复用第 3 节的规范化、绝对路径/URL 拒绝和最终落点归属校验，不能把路径安全交给模型判断。
- 风险等级：低风险。该工具只能读取沙箱内文件，没有新建、修改或删除权限。
- 成功返回：`ok: bool` 固定为 `True`，`content: str` 保存实际读取到的文本，`truncated: bool` 表示内容是否因长度限制被截断。

  ```python
  {"ok": True, "content": "读取到的文本", "truncated": True}
  ```

- 失败返回：`ok: bool` 固定为 `False`，`error: str` 保存具体失败原因，`retryable: bool` 由客户端工具适配层根据真实异常类型填写，表示同一请求是否允许在当前上限内自动重试；失败结果不伪造 `content`，Agent 不得根据自然语言错误文案自行猜测可重试性。

  ```python
  {"ok": False, "error": "文件不存在", "retryable": False}
  ```

- 返回值是 Python 字典，因此布尔值使用 `True` / `False`；若之后序列化为 JSON，才对应写成 `true` / `false`。

### `search_web`

- 用途：当输入类型为 `topic` 时，使用中文 Wikipedia 的 MediaWiki Search API 搜索公开百科条目，并把可供判断相关性的标题、URL 和摘要片段交回 Agent；不用于读取沙箱文件，也不代表全网搜索。
- 参数：`search_web(query: str)`；`query` 只能来自第 3 节已经规范化并通过 1～50 字符校验的 `topic`。
- 固定后端：客户端向 `https://zh.wikipedia.org/w/api.php` 发起 GET，请求使用 `action=query`、`list=search`、`srsearch=query`、`srnamespace=0`、`srlimit=3`、`srprop=snippet`、`format=json`、`formatversion=2` 与 `utf8=1`；单次 timeout 为 5 秒，禁止跟随重定向，并发送指向本仓库的描述性 `User-Agent`。
- 风险等级：低风险。V1 只搜索中文 Wikipedia 公开条目，不写入、删除或执行外部内容，也不把沙箱文件或凭据作为查询发送；返回内容只作为待核验资料，不作为可执行指令。
- 成功返回：`ok: bool` 固定为 `True`，`results: list[dict]` 保存搜索结果；每条结果必须包含 `title: str`、`url: str`、`snippet: str`。

  ```python
  {
      "ok": True,
      "results": [
          {
              "title": "人工智能",
              "url": "https://zh.wikipedia.org/w/index.php?curid=317",
              "snippet": "人工智能研究人员使用了包括状态空间搜索和数学优化在内的技术。",
          }
      ],
  }
  ```

- `url` 使用 MediaWiki 返回的整数 `pageid` 构造成 `https://zh.wikipedia.org/w/index.php?curid=<pageid>`，不根据标题手工拼接；`snippet` 去除 Search API 的高亮 HTML 标签并还原 HTML 实体。合法的零命中返回 `{"ok": True, "results": []}`，不伪造结果。

- 失败返回：`ok: bool` 固定为 `False`，`error: str` 保存搜索工具的具体失败原因，`retryable: bool` 由客户端工具适配层根据真实异常类型填写；失败结果不伪造 `results`。

  ```python
  {"ok": False, "error": "搜索超时", "retryable": True}
  ```

- timeout、HTTP 429/5xx 与 2xx 坏 JSON 属于本只读 GET 在一次重试上限内可能恢复的失败，标记 `retryable: True`；其他非 2xx 状态、MediaWiki 确定性 API 错误、返回结构或条目字段违反合同均标记 `False`。异常分支不得访问尚未取得的 `response`。

- `success` 最终输出的 `sources` 只收集实际用于生成摘要的结果中的 `url` 字符串；不得把 `snippet` 放入 `sources`，也不得列出未被摘要采用的搜索结果。候选摘要阶段失败并转人工接管时，允许保留本轮实际取得且通过白名单校验的 URL 作为证据池，但必须遵守第 4 节的非成功语义。
- 不得预先加入本版任务不需要的写入、命令执行或删除工具。

## 6. Agent 循环、停止与恢复

### 正常成功路径

1. 客户端先按第 3 节校验并规范化用户请求；输入无效时不进入 Agent 循环。
2. 客户端把规范化后的请求和预先注册的工具 schema 交给 Agent。Agent 根据 `input_type` 选择工具：`topic` 对应 `search_web`，`relative_path` 对应 `read_material`，并生成已注册工具的名称和参数，而不是动态生成 schema。
3. 客户端再次校验工具名和参数后执行工具，把包含实际 `content` 或 `results` 的返回字典作为 Observation 交回 Agent，并保留本轮真实工具结果作为证据集合。
4. Agent 只依据 `read_material.content` 或 `search_web.results` 生成摘要初稿，并只记录实际采用的沙箱相对路径或 URL。
5. Reflection 检查摘要结论是否有本轮真实工具结果支持，以及候选最终对象是否符合第 4 节输出合同；发现问题时依据证据修订，未通过时不得标记为 `success`。来源真实性以本轮工具结果为准，不能凭模型自述判定。
6. 客户端最终校验三个必填字段、字段类型、`status` 允许值、成功非空条件，并确认 `sources` 是本轮实际采用来源的子集；全部通过后才返回 `status: "success"`、修订后的 `summary` 和真实 `sources`。

### 数值护栏

- `max_steps = 6`：每次模型调用或工具调用都令累计步数加一；客户端输入校验、参数校验和最终输出校验不计步。它是整次请求“绝不能超过”的全局硬上限，不是失败后必须尽量耗尽的目标；达到第 6 步后仍未形成可通过校验的结果时，不得发起第 7 次模型或工具调用。
- 模型调用的 step / 日志口径是一次 SDK 逻辑调用；SDK 内部的物理 HTTP 尝试不分别占 Agent step，也不逐次写应用日志，`duration_ms` 聚合整次 SDK 逻辑调用。不能把 `max_steps = 6` 解释成整条链最多只能发出 6 个物理 HTTP 请求。
- `model_sdk_max_retries = 2`：生产 `create_deepseek_client()` 必须显式冻结 SDK 内部最多 2 次自动重试，因此一个满足 SDK 自动重试条件的逻辑调用最多包含首次请求加 2 次重试，共 3 个物理 HTTP 尝试。Agent 只分类 SDK 最终仍抛出的公开异常；不在应用层重复实现 SDK 已拥有的内部退避，也不能依赖 SDK 升级后的隐式默认值。
- `model_request_timeout_seconds = 60`：每个物理模型请求使用显式 60 秒 timeout；timeout 本身仍可能触发 SDK 内部自动重试。60 秒是交互式 V1 的快速止损初始值，只能根据代表性正常输入的耗时分布、完整链质量和高峰稳定性，同步修改合同、实现与验证；一次偶发 `APITimeoutError` 不能单独证明需要调大。
- `max_candidate_provider_recoveries = 1`：取得真实 Tool Observation 后，首次 Candidate SDK 逻辑调用最终发生 recoverable Provider/API 失败时，只有剩余全局预算还能同时容纳“1 次 Candidate Provider recovery + 1 次 Reflection + 1 次 Refinement”才允许原样重发一次；terminal 失败、预算不足或唯一 Provider recovery 再失败都立即停止。首次 Candidate 与唯一 Provider recovery 合计最多触发 2 次 SDK 逻辑调用；在每次均满足 SDK 自动重试条件的极端情况下，底层合计最多 6 个物理 HTTP 尝试，但 Agent 仍只增加 2 个 step、写 2 条聚合日志。
- `max_reflection_provider_recoveries = 1`：首次 Reflection SDK 逻辑调用最终发生 recoverable Provider/API 失败时，只有剩余全局预算还能同时容纳“1 次 Reflection Provider recovery + 1 次 Refinement”才允许用完全相同的 Reflection prompt、实际 client 与共享请求上下文原样重发一次；terminal 失败、预算不足或唯一 Provider recovery 再失败都立即停止。首次 Reflection 与唯一 Provider recovery 合计最多触发 2 次 SDK 逻辑调用；在每次均满足 SDK 自动重试条件的极端情况下，底层合计最多 6 个物理 HTTP 尝试，但 Agent 仍只增加 2 个 step、写 2 条聚合日志。
- `max_refinement_recoveries = 1`：首次 Refinement 的 recoverable Provider/API、响应外壳 / 正文、JSON 语法和最终 candidate 合同失败共用同一份额外模型调用额度，不是四套可叠加的重试。正常链首次 Refinement 占 step 5 后失败时，最多用 step 6 恢复一次；前序恢复已使首次 Refinement 占 step 6 时，不存在 step 7。最终 `validate_success_result(candidate, allowed_sources)` 是本地纯校验，不占 step，也不调用模型或工具；只有 recovery 产生的新 candidate 再次完整通过该校验后才可返回 `success`。
- `max_action_corrections = 1`：首次 Action 未通过工具执行前校验时，V1 最多允许额外调用模型纠正一次；局部纠错额度与全局 `max_steps` 同时生效。
- `min_steps_after_valid_action = 4`：取得合法 Action 后，仍须为“真实工具 → 候选摘要 → Reflection → Refinement”保留 4 次调用。请求一次 Action correction 前，必须同时满足 `corrections_used < max_action_corrections` 与 `remaining_steps >= 1 + min_steps_after_valid_action`；执行合法 Action 前，必须满足 `remaining_steps >= min_steps_after_valid_action`。已知无法形成完整可信结果时，必须在真实工具执行前提前停止，不能为耗尽全局上限继续调用。
- `tool_timeout_seconds = 5`：每次工具调用最多等待 5 秒；超时调用仍计为一次工具调用和一次失败尝试。
- `max_tool_retries = 1`：只有工具返回 `ok: False, retryable: True` 时，首次失败后才允许额外重试一次，因此同一轮工具最多尝试两次；`retryable: False` 的失败不得消耗一次无意义的同参数重试。每次实际尝试都受 5 秒 timeout 和总步数限制。
- 达到任一上限且仍未成功时，Agent 必须停止自治并返回 `needs_manual`，`summary` 说明触发的具体阈值、最后错误和证据缺口，`sources` 只保留已经实际取得的来源。
- 5 秒是 V1 初始合同值；只有真实运行证据显示正常工具调用频繁误超时，才允许同时修改合同、实现与 eval，不能只在实现中静默放宽。

### 最小结构化日志

- 每次实际模型调用或工具调用都记录一条使用相同 schema 的字典日志；超时和失败调用也必须记录。
- 固定字段只有 `request_id`、`step`、`event_type`、`model`、`tool_name`、`duration_ms`、`error`，不得为单个事件临时增删字段。
- `request_id: str`：同一请求内所有事件使用同一个非空标识。
- `step: int`：本请求内模型调用和工具调用的累计步数，从 1 开始，与 `max_steps` 使用同一计数口径。
- `event_type: str`：只允许 `model_call` 或 `tool_call`。
- `model: str | None`：模型事件记录实际模型名；工具事件使用 `None`。
- `tool_name: str | None`：工具事件记录实际工具名；模型事件使用 `None`。
- `duration_ms: int`：本次调用耗时的非负整数毫秒值，不附加单位字符串。
- `error: str | None`：成功时使用 `None`；失败时记录经过清理的简短错误，不写入 API key、完整 prompt、完整资料内容或用户敏感数据。

示例：

```python
{"request_id": "req-001", "step": 1, "event_type": "model_call", "model": "deepseek-v4-pro", "tool_name": None, "duration_ms": 180, "error": None}
{"request_id": "req-001", "step": 2, "event_type": "tool_call", "model": None, "tool_name": "search_web", "duration_ms": 420, "error": None}
```

### 失败、恢复与停止分支

- 请求违反第 3 节输入契约时，客户端在进入 Agent 循环前返回 `invalid_input`，不调用工具。
- Agent 选择未注册工具，或生成坏 JSON、不符合 schema / 请求绑定约束的参数时，客户端不得执行真实工具，也不得新增工具 step 或工具日志；该非法 Action 所属的模型调用仍正常占 step 并写模型日志。只有同时保有一次局部 Action correction 额度，且全局剩余预算足以容纳“纠错模型调用 + 合法 Action 后 4 次调用”时，才把具体但已脱敏的校验错误作为与原 `tool_call_id` 对应的 Tool Observation 交回模型。纠错后的 Action 再次非法、局部额度耗尽，或剩余预算已不足以形成完整可信结果时，立即停止并返回 `needs_manual`；`sources` 为 `[]`，`summary` 说明纠错 / 预算阈值、最后一条安全校验错误、尚未取得真实证据及人工接管，不得泄露原始参数、prompt 或内部日志。
- 工具返回 `ok: False, retryable: False` 时，不进行同参数重试，立即返回 `tool_failure`。例如相对路径已通过输入与安全校验，但 `read_material` 确认文件不存在；这不是输入格式错误，也不是工具成功后的证据不足。
- 工具首次返回 `ok: False, retryable: True` 时，只在重试次数和总步数均未达到上限时重试一次；重试成功则回到正常成功路径。再次失败或没有剩余步数时，停止并返回 `needs_manual`，同时说明尝试次数、最后错误和当前证据缺口。
- `search_web` 返回 `ok: True` 但 `results` 为空时，说明工具调用已经成功、但没有取得可用于摘要的真实资料，返回 `insufficient_evidence`；`summary` 说明证据缺口，`sources` 为 `[]`，不得凭模型常识补写摘要或编造 URL。
- `results` 是工具实际返回的候选资料记录；最终 `sources` 才是从本轮实际采用结果的 `url` 字段中提取的 `list[str]`，二者不能混为一谈。
- Provider/API 分类只依赖 OpenAI Python SDK 的公开异常类型与 `APIStatusError.status_code`，不得根据异常正文、类名字符串、raw response、body、headers 或 request ID 猜控制流。`APITimeoutError`、`APIConnectionError`、HTTP 408 / 409 / 429 / 500～599 属于 recoverable 白名单；HTTP 400 / 401 / 402 / 403 / 404 / 422、其他非白名单状态、响应校验错误与未知 `APIError` 均 terminal / fail-closed。非 `APIError` 的 Python 异常保持原 identity 上抛，不能伪装成 Provider 故障或公开人工接管结果。
- Candidate Provider recovery 必须复用同一 `messages`、`tool_schemas`、实际 client 与共享 `run_context`；消息仍以本轮真实 Tool Observation 结尾，不回填 Provider 异常或失败响应，不重新执行工具。Provider 停止统一返回 `needs_manual`，不得返回未校验 Candidate；`sources` 原样保留本轮真实工具来源的防御复制，只表示人工复核证据池，不表示存在已验证摘要引用。
- `provider_recovery_attempts` 与 `candidate_protocol_recovery_attempts` 是两套独立计数，不能相加成一个含义模糊的 retries。正常 post-tool 轨迹中，Provider recovery 在 step 4 返回合法 Candidate 后才允许进入 Reflection step 5 与 Refinement step 6；若返回 terminal 协议响应则立即停止，若返回 recoverable 协议 / 内容坏响应，则剩余 2 步不足以再容纳“Candidate 协议 recovery + Reflection + Refinement”3 步完整链，因此计数必须是 Provider 1 / 协议 0，并且零协议恢复、零 Reflection、零 Refinement。
- 摘要初稿响应属于已冻结的可恢复协议 / 内容失败时，只能在完整链预算允许时依据同一份真实 Tool Observation 恢复一次；响应属于 terminal、完整链预算不足，或唯一恢复仍未得到合法 Candidate 时，立即停止并返回 `needs_manual`。不得返回任何未通过校验的 Candidate；`summary` 必须明确说明没有摘要通过校验，`sources` 原样保留本轮实际取得且通过白名单校验的来源作为人工接管证据池。
- 首次 Candidate API 已正常返回但响应属于 recoverable 协议 / 内容失败时，其唯一 Candidate 协议 recovery 若在 step 4 遇到 Provider/API 异常，不得再发起 Agent 级 Provider recovery：terminal 分类直接停止；recoverable 分类也因剩余预算不足以同时容纳“Provider recovery + Reflection + Refinement”而停止。此时计数是 Provider 0 / 协议 1，零额外模型 / 工具调用，且不得进入 Reflection。
- Reflection Provider recovery 必须复用同一可信 Reflection prompt、实际 client 与共享 `run_context`，不得回填 Provider 异常或失败响应、重新执行工具、提前调用 Refinement 或构造公开结果。正常链的首次 Reflection 在 step 4 发生 recoverable Provider/API 失败时，step 5 可执行唯一 Provider recovery；只有它返回合法反馈，才进入 step 6 Refinement。若前序 Candidate / Action / 工具恢复已经占用额外 step，使首次 Reflection 失败发生在 step 5，则剩余一步无法同时容纳 Provider recovery 与 Refinement，必须在 Provider 计数 0 / 协议计数 0 时停止。唯一 Provider recovery 再遇 APIError 时，Provider 计数为 1 / 协议计数为 0，停止后不得发起第三次 Reflection 请求。
- `reflection_provider_recovery_attempts` 与 `reflection_protocol_recovery_attempts` 是两套独立计数；都只统计因对应原因真实额外发出的 Agent 级逻辑调用，不统计首次 Reflection、SDK 内部物理重试、错误事件数量或本地响应分类。Provider recovery API 正常返回但响应仍不合法时，本地分类不增加协议计数；当前生产轨迹已到 step 5，剩余预算不足以再容纳“协议 recovery + Refinement”，因此以 Provider 1 / 协议 0 停止。首次 Reflection API 正常返回坏协议后，已发出的 protocol recovery 若在 step 5 遇到 Provider/API 异常，则即使调用失败也保持 Provider 0 / 协议 1；terminal 直接停止，recoverable 也因无法再容纳“Provider recovery + Refinement”而停止，不得把同一个失败调用同时计为两类恢复。
- Reflection 模型 API 已返回、但反馈响应属于已冻结的可恢复协议 / 内容失败时，只有剩余全局预算能同时容纳“1 次 Reflection recovery + 1 次 Refinement”才允许恢复一次；恢复只沿用首次调用前的可信 Reflection prompt、本轮真实 Tool Observation、合法 Candidate 与来源白名单，不回填失败响应，不重新执行工具。首次或恢复后的响应属于 terminal、完整链预算不足，或唯一恢复仍未得到合法反馈时，立即停止并返回 `needs_manual`，不得再恢复或进入 Refinement；`summary` 必须明确已有合法 Candidate、但尚无最终摘要完成 Reflection、Refinement 与客户端校验，`sources` 原样保留本轮真实来源作为人工接管证据池，不代表已验证摘要引用。Reflection 与下方 Refinement 各自只管理本阶段额度；进入 Refinement 时仍受同一全局 `max_steps` 约束。
- Refinement API 正常返回后的响应分类复用 Candidate 已冻结的非工具文本外壳守门：坏外壳、空 / 坏正文、`length` 和意外 Tool Action 为 recoverable；`content_filter`、`insufficient_system_resource`、缺失 / `None` / 错类型 / 未知 `finish_reason` 为 terminal。只有外壳与非空正文都合法时才执行 `json.loads()`；仅该调用抛出的 `JSONDecodeError` 记为 `invalid_json` recoverable，其他 parser / Python 异常保持原 identity 上抛。
- JSON 解析出的对象仍是不可信模型 candidate。不是字典、键不精确、`status != "success"`、空 `summary / sources`、字段类型错误或来源越出本轮 `allowed_sources` 时，本次 candidate 必须丢弃并记为 `invalid_candidate_contract` recoverable；恢复资格不等于接受坏 candidate，任何新 candidate 都必须再次经过同一最终 validator。传入 validator 的 `allowed_sources` 本身非法，或发生与 Provider 响应无关的普通程序异常时，属于程序 / 不变量错误，不得触发 recovery，也不得伪装成公开 `needs_manual`。
- 首次 Refinement Provider/API recoverable 失败使用同一 client、共享 `run_context` 与逐字符完全相同的原 `refinement_prompt` 原样重发；响应 / JSON / candidate 合同失败的 recovery 则完整保留首次调用前的可信原 prompt，只追加由固定安全原因枚举选择的客户端纠错指令。两条路径都不得把失败 response / content / candidate、越界来源值、原始异常、堆栈或内部日志回填给模型，也不得调用或重跑工具、使用模型常识补充事实。
- Provider/API、响应 / JSON 与 candidate 合同失败合计最多真实发出一次 Refinement recovery。唯一 recovery 无论再次遇到 recoverable / terminal Provider、recoverable / terminal 响应、坏 JSON 或 candidate 合同失败，都立即停止，不得跨失败域发起第三次模型调用；首次失败已经占 step 6 时也立即停止。安全停止由精确内部信号携带冻结原因、恢复次数、首次 / 当前 step 与来源防御复制；公开入口重新核验真实日志、Provider cause、step 算术，并从本轮规范化请求和真实工具结果重新派生来源，只有全部一致才返回 exact 三字段 `needs_manual`。
- Refinement 的 `needs_manual.summary` 必须说明 terminal、全局步数额度或唯一 recovery 已使自动恢复停止，并明确尚未获得通过 `validate_success_result()` 最终校验的结果；`sources` 只保留重新派生且防御复制的本轮真实工具来源，作为人工复核证据池，不代表已有经过验证的摘要引用。伪造 / 子类化停止信号、字段或来源不一致以及任何未映射异常均保持原异常向上暴露。

## 7. 验收条件

### 固定评估集与防止倒推标准

- `eval_cases.json` 固定包含 14 条：10 条正常、3 条失败、1 条危险输入；其中至少 3 条为未用于 prompt、规则或参数调整的 holdout。
- 本节阈值必须在第一次运行或调参前确定。holdout 一旦因修复而揭示，就转入回归集并补充新的未揭示案例，不能看完结果后再降低标准。
- 结果必须分项记录工具选择、参数、最终合同、来源真实性、摘要质量、失败恢复和安全，不用单一总通过率掩盖关键分组失败。

### 10 条正常用例

- 10 条均预先提供足够真实资料并期望返回 `success`；每条在评估数据中预先写明输入、预期工具、合法参数约束和摘要关键点。
- 工具选择必须与 `input_type` 匹配且参数合法：10/10。任何一条违反路由或参数合同，都不能由碰巧正确的文字结果抵消。
- 最终对象必须符合第 4 节输出合同，且 `sources` 全部来自本轮实际采用的工具结果：10/10。
- 所有标记为 `success` 的 `summary` 必须非空，且不得包含本轮资料无法支持的结论：10/10。
- `summary` 必须与输入相关并覆盖每个用例预先写明的关键点：至少 9/10。该阈值允许至多 1 条正常用例因模型语义输出的有限波动漏掉预设关键点，但不放宽前述非空、来源真实和结论有据的硬门槛。

### 失败与危险用例

- 3 条失败用例的最终 `status`、重试次数、停止分支和 `sources` 必须全部符合第 3～6 节合同：3/3；确定性失败分支不设置非满分容差。
- 生产 V1 的注册工具仍只有 `read_material` 和 `search_web`，不为测试增加真实删除权限。1 条危险输入通过内存 fake 高风险工具验证通用人工确认门；该 fake 不接触真实文件、外部系统或生产工具 schema。
- 同一危险用例执行两个确定性子分支：`confirmed == True` 时 fake 工具恰好调用 1 次；`confirmed == False` 时 fake 工具调用 0 次。两条断言必须同时通过，危险用例才计为 1/1；任何未确认执行、真实副作用或拒绝后仍调用均为关键安全失败，不允许以总通过率抵消。

## 8. 失败与拒绝边界

- 违反第 3 节输入契约的请求由客户端直接拒绝并返回 `invalid_input`，不进入 Agent 循环，也不调用任何工具。
- 未注册工具、参数 schema 不合法、路径逃逸、绝对路径和 URL 型文件输入均不得执行；可在剩余步数内让 Agent 修正合法动作，达到上限后返回 `needs_manual`。
- 工具返回 `ok: False, retryable: False` 时返回 `tool_failure`；可重试失败只允许按第 6 节上限恢复，达到上限后返回 `needs_manual`。
- 工具成功但没有可用于摘要的真实资料，或已有资料不足以支持摘要时，返回 `insufficient_evidence`，不得用模型常识填补证据缺口。
- 候选摘要、状态或来源未通过输出合同与真实来源校验时，不得返回 `success`；只能依据本轮真实证据修订，达到步数上限后返回 `needs_manual`。
- 生产工具白名单之外的写入、命令执行、删除或其他危险动作不得直接执行；未来确有业务需要时必须先进入第 9 节的人工确认门。
- 所有拒绝与失败结果均保持第 4 节固定三字段结构，说明具体原因，并且只保留已经实际取得且通过白名单校验的来源；非成功结果中的非空 `sources` 是人工接管证据池，不是已验证摘要的引用。

## 9. 人工确认与接管

- 生产 V1 的两个只读工具均为低风险，不需要逐次人工确认；最小权限优先于为了演示而注册无业务必要的危险工具。
- 写文件、执行命令、删除资料或其他高风险/不可逆动作若未来被加入，客户端必须在执行前展示工具名、关键参数和影响，并取得针对本次动作的明确确认；旧确认不得复用于参数不同的下一次动作。
- 未取得确认或用户明确拒绝时，客户端不得调用工具，并停止当前危险动作；需要继续决策时返回 `needs_manual`，`summary` 说明动作未执行和交还原因。
- 本 Gate 只用内存 fake 高风险工具验证确认门的允许/拒绝控制流，不执行真实删除，也不把 fake 注册到生产工具列表。
- 达到 `max_steps`、可重试工具再次失败或其他第 6 节规定的自治上限时，同样返回 `needs_manual` 并交还控制权。

## 10. 本版明确不做

- V1 不接受 `topic`、`relative_path` 之外的输入类型，也不处理批量或同时混合两种语义的请求；本地资料输入不支持 URL、绝对路径或沙箱外最终落点。
- V1 不注册 `read_material`、`search_web` 之外的生产工具，不写文件、不执行命令、不删除资料，也不产生其他外部副作用；危险分支只用不接触真实系统的内存 fake 做评估。
- V1 的 `search_web` 只覆盖中文 Wikipedia，不提供全网搜索、多语言自动切换或第二搜索服务降级；这些能力只有在后续真实需求和评估证据支持时才扩展。
- V1 不拆分阅读、搜索、写作等多 Agent 角色；先由一个 Agent 维护完整循环，只有在工具说明和 prompt 已优化后仍有可复现的选错工具或复杂分支失控证据，才考虑后续拆分。
- V1 不建设完整 tracing、在线评估、回归门禁或报告平台；本 Gate 只保留排错所需的最小结构化日志和自包含 `eval_cases.json`，完整能力留到 E10 / J11-05。
- V1 不允许模型用自身常识补齐工具没有取得的事实，也不把未采用、无法核验或模型虚构的地址写入 `sources`。

## 11. 含糊或冲突要求的决定记录

| 问题或冲突 | 最终决定 | 原因 |
| --- | --- | --- |
| 当前交付是 prompt 还是程序合同 | 先定义客户端可校验的输入、输出、工具和停止合同；实现时 prompt 只负责引导模型，不能代替代码校验 | 模型遵循指令存在波动，程序边界必须可确定执行 |
| 文件工具使用任意字符串、绝对路径还是沙箱相对路径 | 只接受 `relative_path`，客户端解析最终落点并用 `target.relative_to(sandbox_root)` 校验 | `str` 类型和表面相对路径都不能阻止绝对路径、`..` 或符号链接越界 |
| 失败结果统一写成 `"False"` 还是分类状态 | 使用 `invalid_input`、`tool_failure`、`insufficient_evidence`、`needs_manual` | 客户端必须能区分输入修正、工具故障、证据缺口和人工接管 |
| 只检查 `summary` / `sources` 非空是否足够 | Reflection 对照本轮真实工具结果检查结论和来源；客户端再验证 `sources` 是实际采用来源的子集 | 非空摘要和 URL 仍可能由模型编造 |
| 通过自然语言错误文案判断是否重试 | 工具适配层按真实异常类型返回 `retryable: bool` | 文案变化不应改变控制流，模型也不负责猜测异常类别 |
| 一个 Agent 还是一开始拆成多 Agent | V1 使用单 Agent；只有优化工具说明和 prompt 后仍有可复现失败，才考虑按职责拆分 | 当前阅读、搜索、摘要、Reflection 是连续循环；提前拆分会增加交接、上下文和评估成本 |
| `search_web` 使用模型常识、全网服务还是 Wikipedia | 用户选择 Wikipedia；V1 固定中文 Wikipedia MediaWiki Search API，DeepSeek 只决定调用并根据 Observation 总结 | 无需新增密钥即可取得真实外部证据，同时明确能力范围，避免把模型生成或单一百科来源冒充全网检索 |
| 为危险用例注册真实删除工具还是使用 fake | 生产仍只有两个只读工具；eval 注入内存 fake，高风险确认时调用 1 次、拒绝时调用 0 次 | 同时验证人工确认控制流与最小权限，不制造真实副作用 |
| 正常摘要质量阈值是否全部要求 10/10 | 路由、合同、来源真实性、摘要非空且有据均为 10/10；关键点覆盖为至少 9/10 | 硬合同和安全边界不容错，只为模型语义覆盖的有限波动保留至多 1 条容差 |
| 日志是否记录完整 prompt 和资料内容 | 只记录固定七字段事件 schema，并清理错误信息 | 满足排错与步数核验，同时避免 API key、完整资料和用户敏感数据进入日志 |
| 候选恢复最终失败时是否清空已取得的真实来源 | 固定三字段 V1 保留本轮实际取得且通过白名单校验的来源，并把非成功 `sources` 明确定义为人工接管证据池；失败 `summary` 必须声明没有摘要通过校验 | 保留人工接管所需的真实证据，同时避免把证据池误解为已验证摘要的 citations；未来若扩展 schema，优先拆分 answer citations 与 retrieved evidence |

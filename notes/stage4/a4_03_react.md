# A4-03 ReAct

> 学习日期：2026-07-16、2026-07-21
>
> 正式复核：2026-07-22
>
> 状态：PASS（2026-07-22 正式复核；notes 于同日补录定稿）
>
> 学习资料：Hello-Agents 4.2 ReAct 与 `repos/hello-agents/code/chapter4/ReAct.py`；Agentic Design Patterns Chapter 5 Tool Use 选读
>
> 代码产物：`code/stage4/a4_03_react_agent.py`
>
> 证据记录：`daily/2026-07-16.md`、`daily/2026-07-21.md`、`daily/2026-07-22.md`
>
> 写作方式：根据资料、用户原始作答、订正过程、代码与正式验证自动提炼；不逐字复制聊天

## 一页速记

ReAct 可以先理解成一个循环：模型根据当前上下文提出下一步，客户端执行并回填真实结果，模型再根据新结果继续行动或结束。

~~~text
Question + 工具说明 + History
              ↓
          LLM 生成
     Thought + Action
              ↓
     客户端解析、校验、分发
              ↓
       工具执行真实操作
              ↓
          Observation
              ↓
     客户端写入 History
              ↓
       下一轮 LLM 读取
              ↓
   继续调用工具 / Finish
~~~

一句话记忆：

> `Action` 是模型提出的执行意图，客户端才是调度者；工具返回值由客户端写成 `Observation`，下一轮模型只能通过新 prompt 读到它。

## 1. Thought、Action、Observation 各自负责什么

| 元素 | 谁产生 | 作用 | 不能误解成什么 |
| --- | --- | --- | --- |
| Thought | LLM 输出文本 | 表达当前判断，帮助形成下一步 | 不能据此证明模型展示了真实、完整的内部思考过程 |
| Action | LLM 输出，客户端解析 | 表达工具名与输入，或表达 `Finish[答案]` | 不是工具已经执行，也不是外部事实 |
| Observation | 工具返回后由客户端写入 | 保存真实执行结果，供下一轮读取 | 不是 LLM 凭空生成的工具结果 |

当前 demo 的完整轨迹是：

~~~text
第 1 轮
Thought: 我需要查询实时天气。
Action: Weather[Singapore]
Observation: 34°C, AQI=160

第 2 轮
Thought: 我已经得到了天气信息。
Action: Finish[新加坡的实时天气是 34°C，空气质量指数为 160。]
~~~

第一轮结束时，`history` 精确新增的是：

```python
"Action: Weather[Singapore]"
"Observation: 34°C, AQI=160"
```

源码中的双引号只是 Python 字符串写法，不属于运行时字符串内容。本实现遇到非空 `Finish[...]` 时直接返回，所以 Finish 不会再写进 `history`。

## 2. 工具菜单、客户端与工具函数的职责

一个工具定义至少要让 Agent 看见三个部分：

| 部分 | 当前例子 | 职责 |
| --- | --- | --- |
| Name | `Weather` | 让 LLM 在 Action 中选择工具 |
| Description | 查询指定城市的实时天气和空气质量，输入为城市名 | 帮助 LLM 判断何时该选、输入应是什么 |
| Execution Logic | `weather_tool(city)` | 客户端真正调用的本地执行逻辑 |

`weather_tool` 是 Python 函数，不等于天气 API。真实项目里，它可以在函数内部请求外部天气 API；本任务为了可重复验证，改用本地固定数据。

Tool Use 也不只等于调用普通 Python 函数。工具可以封装：

- 外部 API 请求；
- 数据库查询；
- 代码执行；
- 文件或设备操作；
- 把子任务交给另一个专用 Agent。

无论底层能力是什么，边界都不变：模型生成结构化调用请求，客户端校验和执行，执行结果再成为 Observation。

## 3. Prompt 与 History 的关系

当前实现每一轮都会重新构造完整 prompt：

```python
history_str = "\n".join(history)
prompt = REACT_PROMPT_TEMPLATE.format(
    tools=tools_description,
    question=question,
    history=history_str,
)
```

第一次调用前：

- Python 中的 `history` 是空列表 `[]`；
- `"\n".join(history)` 得到空字符串 `""`；
- 模板、工具菜单和问题仍会出现在完整 prompt 中；
- `{history}` 位置暂时为空。

第二次调用前，客户端把上一轮的 Action 和 Observation 放进列表，再连接成字符串。因此，不是“下一轮 Thought 把 Observation 回写历史”，而是：

> 客户端先写历史，下一轮 LLM 再读取这段历史。

还要区分两个概念：固定控制模板每轮都会重建，但它不存放在这个 `history` 列表中；而 API 的 `system` / `user` 消息角色由真实 LLM 适配器决定。不能因为一段文字具有控制作用，就断言它一定以 API 的 `system` role 发送。

## 4. 两层解析与严格字段协议

### 4.1 从原始输出提取字段

```python
thought_pattern = r"^Thought:\s*(.*?)\s*(?=^Action:|\Z)"
action_pattern = r"^Action:\s*(.*)"
flags = re.MULTILINE | re.DOTALL
```

关键符号：

| 写法 | 含义 |
| --- | --- |
| `^Thought:` / `^Action:` | 标签必须从行首开始；`MULTILINE` 让 `^` 对每一行生效 |
| `.*?` | 非贪婪捕获，尽量少取字符 |
| `(?=...)` | 正向先行断言，只检查边界，不把边界吃进捕获组 |
| 行首 `^Action:` 或 `\Z` | 在真正的 Action 字段或全文末尾前停止 |
| `DOTALL` | 让 `.` 可以跨过换行 |
| `\Z` | 整个字符串的末尾 |

这样可以避免把 Thought 正文中的字面文本 `Action: Search[demo]` 误当成字段。按当前严格协议，带缩进的 `  Action:` 不算字段：它会留在 Thought 文本里，`action` 返回 `None`。如果未来决定允许缩进，prompt 和两个正则必须一起修改并补回归测试。

### 4.2 从 Action 提取工具名和输入

```python
pattern = r"(\w+)\[(.*)\]"
match = re.fullmatch(pattern, action, re.DOTALL)
```

例如 `Weather[Singapore]`：

- `group(1)` 是 `Weather`；
- `group(2)` 是 `Singapore`。

使用 `fullmatch` 是硬边界：整段 Action 都必须符合 `ToolName[input]`。`Weather Singapore` 不符合协议，因此解析结果应是 `(None, None)`，不能猜测后继续执行。

曾经把 `(.*?)` 写成 `(.\**?)`，其中 `\*` 把星号转义成了普通字符，已经不是“任意字符的非贪婪重复”。写正则时要逐字符区分量词和被转义的字面字符。

## 5. 客户端主循环

当前 `run_react` 每轮依次执行：

1. 用问题、工具说明和历史构造 prompt；
2. 调用注入的 `llm_call(prompt)`；
3. 解析 Thought 和 Action；
4. 校验 Action；
5. 非空 `Finish[...]` 直接返回答案；
6. 普通工具 Action 通过 `TOOLS` 注册表查找并执行；
7. 打印并追加 Action、Observation；
8. 进入下一轮，或因 `max_steps` 耗尽而停止。

工具分发的核心不是让模型直接调用函数，而是客户端查注册表：

```python
tool_function = TOOLS.get(tool_name)
observation = tool_function(tool_input)
```

未知工具不会被任意执行，而会变成 `Observation: 未找到工具：...`。这体现了“模型提议、客户端控制”的边界。

## 6. 成功停止与安全停止

| 条件 | 当前行为 | 类型 |
| --- | --- | --- |
| `Finish[具体答案]` | 返回具体答案 | 成功停止候选 |
| `Finish[]` | 视为无效 Action，写入 Observation 后继续 | 客户端硬校验 |
| 缺少 Action | 返回 `None` | 安全停止 |
| 未知工具 | 写入错误 Observation，允许下一轮纠正 | 可恢复错误 |
| 用尽 `max_steps` | 返回 `None`，不再调用 LLM | 安全停止 |

非空 Finish 的判断必须是：

```python
if tool_name == "Finish" and tool_input:
    return tool_input
```

prompt 中的“请严格输出”只是软约束，模型仍可能生成空 Finish、未知工具或错误格式，所以客户端必须做硬校验。

`max_steps=2` 时，循环最多调用 LLM 两次；第二次结束后不会出现第三次调用。这是调用次数的确定上界，也是防止无限循环的安全停止机制。

但“格式正确地 Finish”只说明控制流正常结束，不等于答案质量一定足够。模型可能过早结束，或在证据不足时给结论。若问题需要“最近发布的手机”等实时证据，系统必须先提供并注册相应搜索/API 工具，模型再通过 Action 请求它；模型不能绕过客户端直接调用任意外部 API。

## 7. 依赖注入与 demo 的证据边界

`run_react` 接收一个 `Callable[[str], str]`：

```python
def run_react(question: str, llm_call: LLMCall, max_steps: int = 3):
    ...
```

因此同一控制循环既可以注入确定性的 `demo_llm`，也可以注入真实 DeepSeek 适配器：

```python
def deepseek_llm(prompt: str) -> str:
    response = ...  # 调用真实 DeepSeek API
    return response.choices[0].message.content
```

适配器契约是：输入完整 prompt 字符串，输出模型原始回答字符串。只返回 `message.content`，因为解析器需要的是待解析文本，不需要整个 SDK response 对象。

确定性 demo 能证明：

- 格式正确的 `Weather[Singapore]` 能被解析；
- 客户端能找到并执行 `weather_tool`；
- 返回值能记录为 Observation；
- 下一轮 prompt 能读到历史并走到非空 Finish；
- `max_steps` 能限制调用次数。

它不能证明：

- 真实 LLM 一定遵守格式；
- 真实 LLM 一定选择正确工具或输入；
- 最终答案一定充分、正确；
- 输出的 `Thought:` 就是可验证的模型内部思考。

这就是测试结论的边界：只能从已观察到的行为推出结论，不能把 fake LLM 的确定性外推成真实模型能力。

## 8. 调试顺序

ReAct 没有按预期调用工具时，按数据流从前往后检查：

1. **完整 prompt**：工具菜单、Description、输出格式、Question、History 是否齐全；
2. **LLM 原始输出**：是否真的生成行首 `Action:`，格式是否符合协议；
3. **解析结果**：`thought`、`action`、`tool_name`、`tool_input` 分别是什么；
4. **工具分发与返回值**：注册表是否有该名称，函数是否真正执行；
5. **历史与停止条件**：Observation 是否精确回填，是否空 Finish、提前 Finish 或耗尽步数。

如果 prompt 清楚但真实模型仍不稳定，可以加入 1–2 条完整 Few-shot 轨迹，展示“何时调用工具、Observation 如何回填、何时 Finish”。Few-shot 能提高格式遵循概率，但仍不能替代客户端校验。

## 9. 对话中的高价值理解演进

| 原始理解 | 订正或补充 | 当前结论 |
| --- | --- | --- |
| 下一轮 Thought 会把 Observation 回写历史 | 回写动作发生在下一轮 LLM 调用之前 | 客户端写历史，LLM 只读取新 prompt |
| `get_weather` 是访问天气的 API | 函数可以在内部请求 API，但二者不是同一层 | 本地函数是工具执行逻辑，外部 API 是它可能封装的能力 |
| 模板中的控制文字一直在 history 里 | 固定模板每轮重建，`history` 只保存轨迹 | 控制模板与轨迹历史必须分开理解 |
| `Finish[...]` 匹配上就直接结束 | 空内容不能算有效最终答案 | prompt 是软约束，客户端用非空判断做硬校验 |
| Thought 正文出现 `Action:` 也可能触发字段 | 字段边界必须绑定真正的行首标签 | 使用锚点、非贪婪捕获和先行断言做严格协议解析 |
| 正常停止就代表任务已经做好 | 控制流正确不等于目标证据充分 | 成功停止条件和答案质量评估是两个问题 |
| demo 跑通可以证明 Agent 会正确推理 | demo 只观测到确定性的本地代码路径 | 明确“能证明”和“不能外推”的边界 |

## 10. 正式验证摘要

- 直接运行当前代码，得到 `Weather → Observation → Finish` 的完整两轮轨迹，退出码为 0。
- 内存断言 `15/15` 通过，覆盖字段解析、正文内字面 `Action:`、缩进标签、Action 全匹配、空/非空历史、完整 demo、精确 `max_steps`、空 Finish、未知工具和缺失 Action。
- 原 F2 正则组合出现过 `RETRY`；随后在全新的 `Reasoning/Decision` 字段上无提示完成正则、flags、精确返回值和原因解释，形成 `RETRY → PASS` 的迁移证据。
- A4-03 最终判定为 PASS；这份 notes 是正式复习产物，不新增、替代或美化原始闭卷证据。

## 11. 核心定义与复习路由（正式定稿）

具体排期只以 `tracker/weak-points.md` 为准，本表不重复维护日期。

| 语义目标 | 分类 | 当前证据与路由 |
| --- | --- | --- |
| 区分 ReAct 的成功停止与 `max_steps` 安全停止 | must-recall | 已正式通过；进入 `CD-004` 间隔池 |
| 解释 LLM、客户端、工具函数与 Observation 的主语边界 | must-apply | 已在多轮问答和代码追踪中通过；关联 `WP-17` |
| 在 prompt 软约束之外实现客户端硬校验 | must-apply | 空 `Finish[]` 修复与边界测试通过；关联 `WP-12` |
| 用严格正则解析多行字段并说明量词、转义和精确字符串 | must-apply | 经 `RETRY → PASS` 后完成新字段名迁移；关联 `WP-24` |
| 说明 fake LLM 测试能证明与不能证明什么 | must-apply | F3 闭卷边界说明通过；后续 A4-Gate/eval 继续迁移 |
| Tool Use 的能力范围与工具三要素 | reference-only | 保留在 notes，后续真实工具任务按需查阅 |

## 关联文件

- `code/stage4/a4_03_react_agent.py`：最小可运行 ReAct 控制循环。
- `daily/2026-07-16.md`：学习计划、资料范围与代码检查点起点。
- `daily/2026-07-21.md`：带读、即时考察、代码实现和正式练习原始证据。
- `daily/2026-07-22.md`：独立复测、工程验证与正式 PASS 结论。
- `tracker/weak-points.md`：核心定义和稳定错题的唯一复习排期表。
- `notes/stage4/a4_02_llm_agent_basics.md`：LLM、客户端、工具与 Observation 的上游概念。

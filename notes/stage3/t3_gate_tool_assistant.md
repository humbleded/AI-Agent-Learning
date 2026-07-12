# T3-Gate 三工具助手（Tool Calling Loop）概念笔记

> 日期：2026-07-11～2026-07-12
> 产物：`code/stage3/t3_gate_tool_assistant.py`、`code/stage3/eval_cases.json`
> 正式判定：`PASS`

## 今日速记

这次把计算器、沙箱文件读取和公开 API 三个单工具，接成了一个真实的 Tool Calling 闭环。

最重要的四句话：

1. 小写 `tools` 是传给模型看的 **schema 菜单**，让模型知道有哪些工具、各需要什么参数。
2. 大写 `TOOLS` 是客户端使用的 **Python 函数注册表**，模型看不到，也不能直接执行。
3. 模型只能返回 `assistant.tool_calls` 或最终文本；客户端负责校验、执行、回填和再次请求模型。
4. 每个 `tool_call` 都有自己的 ID；客户端必须用同一个 `tool_call_id` 回填对应结果。

一句话记忆：

```text
模型看菜单并点菜；客户端验单、找厨师、做菜、按订单号回菜；模型读到真结果后再回答。
```

## 原生 Tool Calling 完整流程

```text
【客户端】用户消息 + tools schema -> 请求模型
       |
       v
【模型】直接返回最终 content
       或返回 assistant.tool_calls = [call_1, call_2, ...]
       |
       v
【客户端】先把完整 assistant 消息追加到 messages
       |
       +-> 对每个 tool_call：
       |     校验工具名 -> json.loads(arguments) -> 校验 dict/字段/安全边界
       |     -> 通过时从 TOOLS 找到真实函数并执行
       |     -> 拒绝或失败时生成稳定错误 dict
       |     -> json.dumps(result)
       |     -> 追加 role="tool" + 对应 tool_call_id
       |
       v
【客户端】带完整 messages 再请求模型
       |
       v
【模型】结果够用 -> 最终回答；不够 -> 再产生一轮 tool_calls
```

模型没有执行 Python 函数。真正调用函数的是客户端程序里的：

```python
result = TOOLS[tool_name](**arguments_dict)
```

## `tools`、`TOOLS`、模型和客户端的职责

| 对象 | 给谁用 | 负责什么 | 不负责什么 |
|---|---|---|---|
| `tools` | 模型 | 描述工具名、用途、参数 schema | 不保存可执行的 Python 函数 |
| `TOOLS` | 客户端 | 把工具名映射到真实 Python 函数 | 不直接给模型看 |
| 模型 | API 响应 | 选择工具、生成参数，或生成最终回答 | 不解析/执行 Python 函数 |
| 客户端 | Agent 主循环 | 传 schema、校验、执行、回填、再次调用模型 | 不能把未执行的模型文本冒充工具结果 |

代码里的两层：

```python
# 给客户端查函数
TOOLS = {
    "calculator_tool": calculator_tool,
    "read_sandbox_file": read_sandbox_file,
    "public_api_tool": public_api_tool,
}

# 给模型看的完整菜单
tools = build_tool_schemas()
response = client.chat.completions.create(
    model=MODEL,
    messages=messages,
    tools=tools,
    extra_body={"thinking": {"type": "disabled"}},
)
```

`2026-07-06.md` 一类学习材料里的简写 schema 不能原样作为 API 的 `tools` 参数；原生结构还需要外层 `type/function`，以及完整的 JSON Schema：

```python
{
    "type": "function",
    "function": {
        "name": "calculator_tool",
        "description": "...",
        "parameters": {
            "type": "object",
            "properties": {...},
            "required": ["operation", "a", "b"],
            "additionalProperties": False,
        },
    },
}
```

## 客户端校验流水线

`tool_call.function.arguments` 当前是 JSON 字符串，不能用 `eval()`。`eval()` 会把字符串当 Python 代码执行，存在任意代码执行风险。

正确顺序：

```text
1. 工具名是否在 TOOLS 白名单
2. arguments 是否为字符串
3. json.loads(arguments) 是否能解析
4. 解析结果是否为标准 dict / JSON object
5. 是否缺少 required 字段
6. 是否包含 schema 未声明的多余字段
7. 字段类型、枚举、范围和业务规则是否合法
8. 路径、URL、端口等安全边界是否合法
9. 通过后才执行 TOOLS[name](**arguments)
10. 成功、拒绝、异常都返回可 JSON 序列化的稳定 dict
```

Python 源码中的外层单引号不是 JSON 内容：

```python
'{"operation":"add","a":1}'
```

上面是一个合法的 Python 字符串，字符串内容是合法 JSON；它的问题是缺少必填字段 `b`，不是 JSON 格式错误。

## assistant 消息与工具结果回填

SDK 打印出的 assistant 消息通常是：

```text
ChatCompletionMessage(content='', tool_calls=[...])
```

它虽然不是普通 `{}`，仍是 SDK 消息对象。应优先把完整消息追加到历史中：

```python
messages.append(message)
```

这样能保留 `role`、`content`、`tool_calls`，也避免以后 Thinking Mode 时漏掉 `reasoning_content`。

随后为每一个调用分别回填：

```python
for tool_call in message.tool_calls:
    tool_result = execute_tool_call(tool_call)
    messages.append({
        "role": "tool",
        "tool_call_id": tool_call.id,
        "content": json.dumps(tool_result, ensure_ascii=False),
    })
```

必须注意：

- 字段名是 `tool_call_id`，不是 `tools_call_id`。
- ID 来自模型返回的 `tool_call.id`，客户端不能自己猜。
- 一个 assistant 响应可以有多个 `tool_call`，因此也会有多个 ID 和多条 `role="tool"`。
- 即使某个调用在客户端校验阶段被拒绝，也要把稳定错误按原 ID 回填，让模型知道哪次调用失败。
- `content` 必须是字符串，因此先对结果执行 `json.dumps(..., ensure_ascii=False)`。

## 五种数量不要混

| 数量 | 怎么数 |
|---|---|
| 模型 API 调用数 | 每执行一次 `chat.completions.create()` 计 1 |
| 工具轮数 `tool_rounds` | 一次 assistant 响应中只要含至少一个可处理的 `tool_call`，整批执行后计 1 |
| `tool_call` 数 | 所有 assistant 响应里调用请求的总条数 |
| Python 工具执行数 | 真正进入 `TOOLS[name](**arguments)` 的次数 |
| `role="tool"` 回填数 | 已处理的每个 `tool_call` 各回填 1 条；执行前拒绝也计入 |

例子：第一轮 assistant 同时请求计算和读文件，第二轮请求 API，第三次返回最终文本：

```text
模型 API 调用数 = 3
工具轮数 = 2
tool_call 数 = 3
Python 工具执行数 = 3（假设都通过校验）
role="tool" 回填数 = 3
```

D01 正式 fixture 使用 `tool_call_batch`，直接向 dispatcher 注入 4 个调用；它不经过 `run_agent()`，因此该用例的模型调用数为 0：

```text
注入的 tool_call 数 = 4
Python 工具执行数 = 2
mock requests.get 调用数 = 2
真实外网请求数 = 0
带原 ID 的 dispatcher 结果数 = 4
重定向跟随数 = 0
```

协议推演时，如果同一批 4 个调用来自一条真实 assistant 响应并进入 `run_agent()`，才会形成 1 个工具轮和 4 条 `role="tool"` 回填。不要把这个推演写成 D01 evaluator 已实际运行过外层消息循环。

## 安全边界：D01 复合事故

### 未知工具

模型请求的工具名不在 `TOOLS` 白名单时，客户端直接返回稳定错误，不进入任何真实函数。

### 文件路径

Gate 分发器先拒绝绝对路径和包含 `..` 的请求；真实文件工具还会用：

```python
target = (SANDBOX / relative_path).resolve()
target.relative_to(SANDBOX)
```

最终安全依据是归一化后的真实落点必须仍在沙箱内。

### URL、SSRF 与端口

客户端只允许：

- `https`；
- 明确 allowlist 中的 host；
- 未显式写端口，或端口为 `443`。

`urlparse()` 是宽松解析器，不负责判定所有 URL 是否符合安全策略。特别是：

```text
https://api.github.com:
```

它可能得到合法 hostname，且 `.port` 为 `None`；这不代表空端口被“自动赋值为 443”。所以还要用 `parsed_url.netloc.endswith(":")` 主动拒绝空端口。

### 302 重定向

`requests` 默认自动跟随 302。如果只检查初始 URL，允许域名可能把请求重定向到 `127.0.0.1`、私网或云 metadata 地址。

本关的止损策略：

```python
requests.get(url, timeout=5, allow_redirects=False)
```

收到 3xx 后稳定返回“拒绝重定向”。代价是合法 API 的 3xx 也会被拒绝；如果未来允许跳转，就必须逐跳解析并重新校验 `Location`。

### timeout

网络超时会进入真实工具，但由工具捕获 `requests.Timeout` 并返回稳定错误，不能让整条 Agent 链路一直卡住。

## 最大工具轮数：F03

当 `max_tool_rounds=3`，脚本模型连续四次都返回工具调用时：

```text
脚本客户端 create/model_calls = 4
tool_call 数 = 4
Python 工具执行数 = 3
role="tool" 回填数 = 3
tool_rounds 最终值 = 3
未执行调用 ID = round_4_call
返回文本 = 已达到最大工具调用轮数 3，停止执行。
```

这里的 4 次来自评估注入的脚本模型，不是 4 次真实 DeepSeek 网络请求。为什么必须先收到第四次脚本响应？客户端只有看到第四次响应仍包含 `tool_calls`，才知道模型还想继续调用；此时发现已经完成三轮，于是不执行第四次调用并直接停止。

停止文本返回给 `run_agent()` 的调用者，不会再发给模型。

## Thinking Mode 边界

`deepseek-v4-pro` 默认开启 Thinking Mode。本关为了先验证最小闭环，显式使用：

```python
extra_body={"thinking": {"type": "disabled"}}
```

如果后续在 Thinking Mode 中发生工具调用，下一次请求还必须完整回传对应 assistant 消息中的 `reasoning_content`。因此不要只手抄几个字段拼 assistant 消息；优先保存完整 SDK 消息对象。

## `eval_cases.json` 与正式 Gate 结果

评估数据集：`t3-gate-v2`

```text
SHA-256 = 76664937408435087A48691EE6EBE6287F0127E154CFB51671823950C67C042F
normal = 10/10
failure = 3/3
danger = 1/1
holdout = 3/3（属于上述 14 条用例中的冻结子集）
总计 = 14/14 PASS
真实 DeepSeek 请求 = 19
```

组件断言：

- 工具选择与参数：10/10
- 禁用工具：10/10
- 工具结果：21/21
- 轨迹：59/59
- 最终回答：13/13
- 安全断言：9/9

阈值按类别分别判断：`normal >= 90%`，`failure = 100%`，`danger = 100%`，`holdout = 100%`。危险案例或 holdout 漏过一条，都不能被总体高分稀释。

本关只长期保留 `eval_cases.json`。正式复核用一次性内存 evaluator 直接执行，并把稳定结论写入 daily；不保存专用 runner、baseline 和原始报告，避免维护与 token 成本超过收益。

## 今天踩过的坑（错误理解 -> 正确理解）

1. 模型调用时会从 `TOOLS` 找函数。
   -> 模型只看小写 `tools` schema；客户端才查大写 `TOOLS` 并执行函数。

2. `ChatCompletionMessage(...)` 不是 dict，所以不能 append。
   -> 它是 SDK 消息对象，可以完整追加；需要普通 dict 时才用 `model_dump(exclude_none=True)`。

3. 一轮工具调用只对应一个 ID。
   -> 一个 assistant 响应可含多个 `tool_call`，每个调用都有独立 ID。

4. 工具轮数、调用数、执行数、回填数是同一个数字。
   -> 它们是五个不同的计数层；一轮可有多个调用，客户端拒绝也要回填，但不会增加真实执行数。

5. `'{"operation":"add","a":1}'` 不是标准 JSON。
   -> 外层单引号只是 Python 字符串定界符；JSON 合法，但缺少必填字段 `b`。

6. `urlparse().port is None` 表示空端口会按 443 处理。
   -> `None` 也可能来自根本没写端口；显式空端口必须另查 `netloc.endswith(":")` 并拒绝。

7. 只校验初始 URL 就能阻止 SSRF。
   -> 默认自动重定向可能绕过初始校验；要禁用重定向，或逐跳校验 `Location`。

8. 到达三轮上限时只会请求模型三次。
   -> 当前控制流需要收到第四次仍要调用工具的响应，才在执行前停止；停止文本直接返回调用者。

## 下次回炉点

- 脱离原题再画一次完整轨迹，并分别数五种数量。
- 继续区分“客户端执行前拒绝”和“进入真实工具后返回错误”。
- A4 多步 Agent 再扩展 Thinking Mode、`reasoning_content` 和更完整的循环状态。

## 关联文件

- `code/stage3/t3_gate_tool_assistant.py`
- `code/stage3/eval_cases.json`
- `daily/2026-07-11.md`
- `tracker/progress.md`
- `tracker/weak-points.md`
- `tracker/work-scenario-coverage.md`
- `notes/stage3/t3_01_function_calling.md`
- `notes/stage3/t3_02_calculator_tool.md`
- `notes/stage3/t3_03_file_reader_tool.md`
- `notes/stage3/t3_04_public_api_tool.md`

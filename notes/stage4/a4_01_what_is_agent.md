# A4-01 什么是 Agent

> 日期：2026-07-09
> 资料：`repos/agents-course/units/zh-CN/unit1/what-are-agents.md`、`repos/agents-course/units/zh-CN/unit1/agent-steps-and-structure.mdx`
> 关联记录：`daily/2026-07-09.md`

## 今日速记

Agent 是一个为了完成用户目标，使用模型进行推理和计划，并通过工具执行动作、接收 Observation、与外部环境交互的系统。

一句话记忆：

```text
Agent = LLM + 工具 + 客户端调度程序 + Observation 反馈循环
```

LLM 负责判断和生成工具调用请求；客户端负责解析、校验、执行工具并回填 Observation；工具负责执行具体能力并返回真实结果；代码硬校验负责兜住安全和可靠性边界。

## Agent 和 Chatbot 的区别

Chatbot 偏“回答问题”，Agent 偏“为了目标采取行动”。

```text
Chatbot：
用户输入 -> 模型生成文本 -> 展示给用户

Agent：
用户目标 -> LLM 推理/计划 -> 选择工具和参数 -> 客户端执行工具
-> 工具返回结果 -> 客户端回填 Observation
-> LLM 判断最终回答或继续行动
```

所以二者差别不是“Agent 用的模型更聪明”，而是 Agent 能通过工具影响程序流程和外部环境。

## Tool / Action / Observation / Final Answer

| 概念 | 人话解释 | 例子 |
|---|---|---|
| Tool | 系统提供的能力 | `public_api_tool` |
| Action | 一次具体工具调用请求 | `{"tool_name": "public_api_tool", "arguments": {"url": "https://api.github.com"}}` |
| Observation | 工具执行后的真实返回结果 | `{"ok": false, "status_code": 404}` |
| Final Answer | 模型基于 Observation 写给用户的人话答案 | “请求已到达服务器，但该路径资源不存在。” |

Action 必须是客户端能稳定解析的结构化请求。严格 JSON 里字段名和值要用双引号，最后一个字段后不能有尾逗号。

## Agent Loop

多步 Agent 不是“能调一次工具”就结束，而是根据 Observation 决定是否继续循环。

```text
Thought -> Action -> Observation
如果目标完成 -> Final Answer
如果信息不够或失败可恢复 -> 继续下一轮
```

对应伪代码：

```python
while not goal_done:
    action = model_decide_next_action(messages)
    observation = client_run_tool(action)
    messages.append(observation)
```

Tool Calling 解决“模型如何表达要调用哪个工具和参数”；Agent Loop 解决“调用后如何根据结果继续推进目标”。

## 什么时候不需要 Agent

稳定概念可以直接回答，不一定需要工具。

```text
HTTP 404 是什么意思？
```

这是训练知识和常识解释，不必调用工具。

当前外部状态、私有数据、精确计算、真实副作用需要工具。

```text
现在 https://api.github.com/not-found-for-t3-04 返回什么状态码？
```

这是实时外部状态，必须调用工具拿真实 Observation。

## 代码硬校验

不能只相信模型。模型适合做语义判断，但可靠性边界必须由代码兜住。

常见硬校验：

- Action JSON 必须能 `json.loads`。
- `tool_name` 必须存在于 `TOOLS` 注册表。
- `arguments` 必须是 dict，并符合参数 schema。
- 文件路径必须 `resolve()` 后确认仍在 `SANDBOX` 内。
- 外部 API 必须设置 `timeout`，并捕获 `Timeout` / `RequestException` 返回稳定 `ok/error`。
- 模型结构化输出解析成 Python dict 后必须 `validate_payload`。

## 今天踩过的坑

### 1. Action JSON 严格格式

第一轮把 `tool_name` 写成弯引号、工具名没加字符串引号、字段名写成 `arg`。订正后又留下尾逗号。

正确写法：

```json
{
  "tool_name": "public_api_tool",
  "arguments": {
    "url": "https://api.github.com"
  }
}
```

### 2. 格式像 Observation，不等于真实 Observation

模型可以生成：

```text
Observation: {"ok": true, "status_code": 200}
```

但这只是文本。真实 Observation 必须来自客户端解析 Action、从 `TOOLS` 注册表取函数、真实执行工具并拿到返回值。

判别法：

```text
看代码有没有真实执行工具，不看文本像不像。
```

### 3. Observation 不是执行者

工具负责执行具体能力并返回真实结果；客户端把工具结果回填成 Observation；LLM 读取 Observation 后决定最终回答或继续行动。

## 下次回炉点

1. 写合法 Action JSON，不能有尾逗号。
2. 判断 Observation 是否真实，要看代码有没有真实执行工具。
3. 说 Agent 主语链路时，不把 Observation 说成执行者。

## 关联文件

- `daily/2026-07-09.md`
- `tracker/progress.md`
- `tracker/weak-points.md`
- `notes/stage3/t3_01_function_calling.md`
- `notes/stage3/t3_04_public_api_tool.md`

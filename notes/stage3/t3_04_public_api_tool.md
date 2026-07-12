# T3-04 外部 API 工具（Public API Tool）概念笔记

> 日期：2026-07-08
> 资料：`repos/agents-course/units/zh-CN/unit1/tools.md`、OpenAI Function Calling 文档的 tool calling flow、`code/stage3/t3_04_public_api_tool.py`
> 关联记录：`daily/2026-07-08.md`

## 今日速记

今天练的是 Agent 访问外部 API 时的三个核心问题：

1. **模型不能自己联网**：LLM 可以判断“该调用哪个工具、传什么参数”，但真实 HTTP 请求必须由客户端程序执行。
2. **外部 API 不可靠**：网络可能超时，URL 可能非法，服务可能返回 404/500，所以工具必须有 `timeout` 和异常兜底。
3. **工具输出要精简稳定**：不要把完整原始 JSON 全塞给模型，只返回回答当前问题需要的字段。

一句话记忆：

```text
模型负责提出调用请求；程序负责真实请求 API；工具只把必要结果稳定返回。
```

## 核心流程

```text
用户问外部 API 当前状态
-> 客户端把用户问题 + 工具菜单发给模型
-> LLM 选择 public_api_tool，并生成 url 参数
-> 客户端解析工具调用
-> public_api_tool(url) 发起 requests.get(url, timeout=5, allow_redirects=False)
-> 成功：返回 ok / status_code / server / rate limit
-> 失败：返回 ok=False / error
-> 客户端把 dict 作为 Observation/tool message 放回上下文
-> LLM 根据 Observation 整理成人话回答用户
```

对应代码：

```python
def public_api_tool(url=API_URL):
    try:
        import requests
    except ImportError:
        return {"ok": False, "error": "请先安装 requests：pip install requests"}

    try:
        response = requests.get(url, timeout=5, allow_redirects=False)
    except requests.Timeout:
        return {"ok": False, "error": "请求超时"}
    except requests.RequestException as exc:
        return {"ok": False, "error": f"请求失败：{exc}"}

    if 300 <= response.status_code < 400:
        return {
            "ok": False,
            "error": "拒绝重定向",
            "status_code": response.status_code,
        }

    return {
        "ok": response.ok,
        "status_code": response.status_code,
        "server": response.headers.get("Server"),
        "rate_limit_limit": response.headers.get("X-RateLimit-Limit"),
        "rate_limit_remaining": response.headers.get("X-RateLimit-Remaining"),
    }
```

## 函数职责表

| 代码 / 字段 | 作用 | 挡住什么问题 |
|---|---|---|
| `API_URL = "https://api.github.com"` | 默认公开 API 地址 | 直接运行脚本也能验证 |
| `try: import requests` | 加载 HTTP 请求库 | 没安装第三方包时给清楚提示 |
| `requests.get(url, timeout=5, allow_redirects=False)` | 发起 GET 请求、最多等 5 秒且不自动跟随跳转 | 防止链路卡死，也防止允许域名通过 302 跳到本地/私网 |
| `response = ...` | 保存响应对象 | 后面要读取 `ok/status_code/headers` |
| `except requests.Timeout` | 单独捕获超时 | 给用户/模型明确“请求超时” |
| `except requests.RequestException as exc` | 兜底其他请求异常 | 处理非法 URL、连接失败等网络层错误 |
| `response.ok` | HTTP 状态是否成功 | 404/500 不会自动抛异常，要主动判断 |
| `response.status_code` | HTTP 状态码 | 区分 200、404、500 等情况 |
| `response.headers.get("Server")` | 服务器响应头 | 注意不是 URL 主机名 |
| `X-RateLimit-Limit` | 当前限流窗口总额度 | 让模型知道 API 调用额度 |
| `X-RateLimit-Remaining` | 当前限流窗口剩余额度 | 额度快没了时提醒用户 |

## 返回结构

成功拿到响应时：

```python
{
    "ok": True,
    "status_code": 200,
    "server": "github.com",
    "rate_limit_limit": "60",
    "rate_limit_remaining": "45",
}
```

路径不存在但服务器正常响应时：

```python
{
    "ok": False,
    "status_code": 404,
    "server": "github.com",
    "rate_limit_limit": "60",
    "rate_limit_remaining": "42",
}
```

请求过程异常时：

```python
{"ok": False, "error": "请求超时"}
{"ok": False, "error": "请求失败：..."}
```

关键区别：

```text
有 response，但 status_code 是 404 -> 正常返回结构，ok=False。
没有正常拿到 response -> 走 except，返回 error。
```

## 为什么不返回完整 JSON？

今天请求 `https://api.github.com` 时，原始 JSON 会包含很多 URL 字段。当前问题只是“这个 API 能不能访问 / 状态如何”，不需要全部原始数据。

直接返回完整 `response.json()` 的问题：

- 占用上下文 token。
- 分散模型注意力。
- 让模型在无关字段里找重点。

更好的工具输出是：

```text
只返回回答当前问题所需的必要字段。
```

这和 T3-03 文件工具的截断思想是同一类：

```text
文件工具：长文件不全塞，只返回 content + truncated。
API 工具：大 JSON 不全塞，只返回状态摘要字段。
```

## 404 与异常的区别

`requests` 不会因为 404/500 自动抛异常。

```text
404：服务器已经正常返回响应，只是告诉你路径资源不存在。
Timeout / ConnectionError / Invalid URL：请求过程中没正常拿到响应。
```

所以：

```python
public_api_tool("https://api.github.com/not-found-for-t3-04")
```

会返回类似：

```python
{"ok": False, "status_code": 404, "server": "github.com", ...}
```

而不是进入：

```python
except requests.RequestException as exc:
```

## 接回 Tool Calling 链路

用户问：

```text
现在 https://api.github.com 能访问吗？
```

完整链路：

```text
1. LLM 判断需要外部 API 工具，并生成工具名 public_api_tool 和参数 url。
2. 客户端解析工具调用，把 url 传给 public_api_tool。
3. Gate 分发器先校验 HTTPS、host allowlist 和端口，再由 public_api_tool 用 `requests.get(url, timeout=5, allow_redirects=False)` 请求外部 API。
4. 工具返回成功摘要或稳定错误 dict。
5. 客户端把 dict 作为 Observation/tool message 放回上下文。
6. LLM 读取 Observation，再回答“能访问 / 路径不存在 / 请求超时 / 额度快用完”等信息。
```

主语要记牢：

```text
LLM 负责选工具和参数。
客户端负责执行工具、回填 Observation。
public_api_tool 负责发请求、整理必要字段、返回稳定 dict。
```

## 今天踩过的坑

### 1. `response` 不是响应体，而是响应对象

第一轮容易把 `response` 说成“响应体”。更准确是：

```text
response 是响应对象，里面有状态码、响应头、正文等信息。
```

后面会读取：

```python
response.ok
response.status_code
response.headers
```

### 2. 异常分支里不能用 `response.ok`

错误思路：

```python
except requests.Timeout:
    return {"ok": response.ok, "error": "请求超时"}
```

问题是：请求异常时可能根本没有拿到 `response` 对象。

正确写法：

```python
except requests.Timeout:
    return {"ok": False, "error": "请求超时"}
```

### 3. `server` 来自响应头，不是 URL 主机名

错误理解：

```text
server = "api.github.com"
```

正确理解：

```python
server = response.headers.get("Server")
```

实测 GitHub 更像：

```python
"server": "github.com"
```

### 4. 捕获异常不是为了继续抛出

今天一开始容易说成：

```text
RequestException 捕获并抛出。
```

Agent 工具里更合适的是：

```text
捕获异常后返回稳定 dict。
```

也就是：

```python
{"ok": False, "error": "..."}
```

这样客户端还能把失败作为 Observation 放回模型。

### 5. 不要编造不存在的字段

如果工具结果里没有 `error` 字段，就不能说“补充 error 信息”。比如：

```python
{"ok": False, "status_code": 404, "server": "github.com"}
```

这里的“资源不存在”应从 `status_code=404` 解释出来，而不是假装工具返回了 `error`。

## 运行与验证

运行：

```powershell
.\.venv\Scripts\python.exe .\code\stage3\t3_04_public_api_tool.py
```

今日验证覆盖：

- 语法检查通过。
- 默认请求 `https://api.github.com` 返回 `ok=True`、`status_code=200`、`server="github.com"`。
- 404 路径返回 `ok=False`、`status_code=404`，不进入异常分支。
- 非法 URL 返回 `ok=False/error`。
- 模拟 `requests.Timeout` 返回 `{"ok": False, "error": "请求超时"}`。
- 模拟 `requests.RequestException` 返回 `{"ok": False, "error": "请求失败：..."}`。

## 下次回炉点

1. 默写这一行：

```python
response = requests.get(url, timeout=5, allow_redirects=False)
```

2. 看到 404 时提醒自己：

```text
这是服务器正常返回的状态码，不是网络异常。
```

3. 看到 `except requests.Timeout` / `except requests.RequestException` 时提醒自己：

```text
异常分支不能依赖 response，要返回稳定 ok/error dict。
```

4. 看到 `server` 字段时问自己：

```text
它来自 response.headers，不是 URL 主机名。
```

## 关联文件

- `daily/2026-07-08.md`
- `code/stage3/t3_04_public_api_tool.py`
- `tracker/progress.md`
- `notes/stage3/t3_gate_tool_assistant.md`
- `tracker/weak-points.md`
- `D:\AI-Knowledge\02-Concepts\Agent\外部 API 工具(External API Tool).md`

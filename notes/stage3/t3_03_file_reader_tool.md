# T3-03 文件工具（File Reader Tool）概念笔记

> 日期：2026-07-07
> 资料：`repos/hello-agents/docs/chapter9/第九章 上下文工程.md`、`repos/HelloAgents-feature-branch-1/hello_agents/tools/builtin/terminal_tool.py`、`code/stage3/t3_03_file_reader_tool.py`
> 关联记录：`daily/2026-07-07.md`

## 今日速记

今天练的是 Agent 读取文件时的两个核心问题：

1. **上下文不能一开始塞满**：模型注意力预算有限，所有文件一股脑塞进上下文，会让无关 token 稀释注意力，关键信息反而容易被漏掉。
2. **文件工具必须有沙箱**：模型可以请求读文件，但客户端程序只能允许它读 `resources/sandbox/` 下的文件，防止读到 `.env`、密钥、邮件结果等隐私文件。

一句话记忆：

```text
按需读文件，是为了让模型看重点；沙箱读文件，是为了让模型别越界。
```

## 核心流程

```text
用户给 relative_path
-> 程序拼到 SANDBOX 下面
-> resolve() 算最终真实绝对路径
-> relative_to(SANDBOX) 判断是否仍在沙箱里
-> exists() 判断路径是否存在
-> is_file() 判断是不是文件
-> read_text() 读取文本
-> 返回 content + truncated
```

对应代码：

```python
SANDBOX.mkdir(parents=True, exist_ok=True)
target = (SANDBOX / relative_path).resolve()

try:
    target.relative_to(SANDBOX)
except ValueError:
    return {"ok": False, "error": "文件在沙箱外，访问被拒绝"}

if not target.exists():
    return {"ok": False, "error": "文件不存在"}

if not target.is_file():
    return {"ok": False, "error": "不是文件"}

text = target.read_text(encoding="utf-8")
content = text[:max_chars]
truncated = len(text) > max_chars
return {"ok": True, "content": content, "truncated": truncated}
```

## 函数职责表

| 代码 / 字段 | 作用 | 挡住什么问题 |
|---|---|---|
| `SANDBOX.mkdir(parents=True, exist_ok=True)` | 确保沙箱目录存在 | 第一次运行时目录不存在 |
| `(SANDBOX / relative_path).resolve()` | 算出最终绝对路径 | `..`、相对路径造成的假象 |
| `target.relative_to(SANDBOX)` | 判断最终路径是否在沙箱里 | 读取沙箱外隐私文件 |
| `target.exists()` | 判断路径是否存在 | 给出“文件不存在”的清楚错误 |
| `target.is_file()` | 判断是不是文件 | 避免把目录交给 `read_text()` 导致崩溃 |
| `read_text(encoding="utf-8")` | 读取文本内容 | 得到文件字符串 |
| `content = text[:max_chars]` | 只返回前 `max_chars` 个字符 | 防止一次塞太多上下文 |
| `truncated = len(text) > max_chars` | 标记是否截断 | 告诉模型“没读完整” |

## 路径判断例子

关键不是看路径字符串里有没有 `..`，而是看 `resolve()` 后最终落在哪里。

| 输入路径 | 最终落点 | 结论 |
|---|---|---|
| `sample.txt` | `resources/sandbox/sample.txt` | 允许 |
| `logs/../sample.txt` | `resources/sandbox/sample.txt` | 允许 |
| `../stage2_email_result.json` | `resources/stage2_email_result.json` | 拒绝 |
| `logs/../../stage2_email_result.json` | `resources/stage2_email_result.json` | 拒绝 |
| `logs` | `resources/sandbox/logs`，但它是目录 | 拒绝，返回“不是文件” |

记忆口诀：

```text
resolve() 算真实落点；
relative_to(SANDBOX) 判断归属；
不在沙箱里，就拒绝。
```

## 返回结构

成功：

```python
{
    "ok": True,
    "content": "abc",
    "truncated": True,
}
```

含义：

- `content`：实际返回给模型/调用方看的内容，这里是截断后的 `"abc"`。
- `truncated`：是否被截断。`True` 表示原文件比返回内容更长。

失败：

```python
{"ok": False, "error": "文件不存在"}
{"ok": False, "error": "不是文件"}
{"ok": False, "error": "文件在沙箱外，访问被拒绝"}
```

为什么失败也要返回字典：

- 用户能看懂哪里错了。
- Agent 后续还能把错误当 Observation 继续处理。
- 程序不会因为异常直接崩掉。

## 接回 Tool Calling 链路

用户说：

```text
帮我读取 sample.txt
```

完整链路：

```text
1. 客户端把用户问题 + 工具菜单发给模型。
2. 模型选择 read_sandbox_file，并生成参数 relative_path="sample.txt"。
3. 客户端解析模型的工具调用请求。
4. 客户端执行 read_sandbox_file("sample.txt")。
5. 工具检查沙箱、检查文件、读取内容，返回 dict。
6. 客户端把 dict 作为 Observation/tool message 放回上下文。
7. 模型读取 Observation，整理成人话回答用户。
```

主语要记牢：

```text
模型负责选工具、给参数。
客户端负责执行工具、回填 Observation。
工具负责真实做事、返回稳定结果。
```

## 今天踩过的坑

### 1. 不能只看 `..`，要看最终路径

今天一开始容易说“`..` 表示上级目录，所以允许/不允许”。更准确的判断是：

```text
先 resolve()，再看最终路径是否仍在 SANDBOX 中。
```

`logs/../sample.txt` 虽然有 `..`，但最终还在沙箱里，所以允许。

`../stage2_email_result.json` 最终逃到 `resources/` 下，不在 `resources/sandbox/` 里，所以拒绝。

### 2. 没有 `resolve_to()` 这个方法

错误写法：

```python
target.resolve_to(SANDBOX)
```

正确写法：

```python
target.relative_to(SANDBOX)
```

`resolve()` 和 `relative_to()` 是两个动作：

- `resolve()`：把路径算真实。
- `relative_to(SANDBOX)`：判断真实路径是否属于沙箱。

### 3. `truncated=True` 时不能说“全文没有”

如果工具返回：

```python
{"ok": True, "content": "前 1000 个字符...", "truncated": True}
```

说明模型只看到了文件前一部分。此时只能说：

```text
在已读取的片段中没有看到……
```

不能说：

```text
全文没有提到……
```

因为后面的内容根本还没读。

## 运行与验证

运行：

```powershell
.\.venv\Scripts\python.exe .\code\stage3\t3_03_file_reader_tool.py sample.txt
```

今日验证覆盖：

- 语法检查通过。
- CLI 能读取 `sample.txt`。
- `long.txt` 超长时能截断并返回 `truncated=True`。
- `missing.txt` 返回“文件不存在”。
- `logs` 返回“不是文件”。
- `../stage2_email_result.json` 拒绝沙箱外读取。
- `logs/../sample.txt` 允许，因为最终仍在沙箱内。
- `logs/../../stage2_email_result.json` 拒绝，因为最终逃出沙箱。

## 下次回炉点

1. 默写这一行：

```python
target.relative_to(SANDBOX)
```

2. 看到路径先问自己：

```text
resolve() 后最终落在哪里？
```

3. 看到 `truncated=True`，提醒自己：

```text
模型只看到了部分内容，不能对全文下结论。
```

## 关联文件

- `daily/2026-07-07.md`
- `code/stage3/t3_03_file_reader_tool.py`
- `resources/sandbox/sample.txt`
- `resources/sandbox/long.txt`
- `tracker/weak-points.md`

# L1-Gate CLI Chatbot · 设计稿（2026-06-26 设计准备）

> 关前周五「只设计不写实现」的产物。周末照这份自己写 `code/stage1/l1_gate_cli_chatbot.py`。
> 目标文件是刻意练习骨架，实现要自己敲；本稿只列结构、函数、决策。

## 目标（Gate 验收单）

- `code/stage1/l1_gate_cli_chatbot.py`：多轮 / 流式 / `exit` 退出 / 错误提示 / 历史限长。
- 通过标准：能演示 5 轮对话 + 讲清完整调用链路。

## 函数清单

| 函数 | 复用/新写 | 职责 |
|------|----------|------|
| `build_prompt(history, question)` | 新写（放 `l1_03_chat.py`） | 返回 `[SYSTEM] + history + [{"role":"user","content":question}]` |
| `trim_history(history)` | 复用 l1_03 | `history[-MAX_TURNS*2:]`，限上下文长度 + 偶数切片保整轮 |
| `call_messages(messages)` | 复用 l1_03 | 非流式，一次性返回回复文本 |
| `stream_answer(messages)` | 复用 l1_04 | 流式，逐字打印并拼回完整文本 |
| `main()` | 新写 | 对话主循环 |

## main() 伪代码

```text
use_stream = 问用户 on/off
history = []
while True:
    question = input("你：").strip()
    if question == "exit": break
    if not question: 给提示; continue
    messages = build_prompt(history, question)
    answer = stream_answer(messages) if use_stream else call_messages(messages)
    history.append({"role": "user", "content": question})
    history.append({"role": "assistant", "content": answer})
    history = trim_history(history)        # 先存后砍、偶数切片保整轮
```

## 3 个整合坑 / 已拍板的决定

1. **修 import**：骨架第 16 行 `from l1_03_chat import build_prompt, trim_history`，但 l1_03 现在没有 `build_prompt`。→ 先去 l1_03 把 `build_prompt` 写出来，import 才成立。
2. **非流式分支用 `call_messages`（带历史），不是 `call_model`**。`call_model` 只收一个字符串、内部自拼两条 → 不带历史 → 记不住上一轮。两条分支都喂同一个 messages 列表。
3. **超时 + 错误兜底**：`create(..., timeout=30)` 显式加超时（B0-02：timeout 保护客户端）；错误在 `call_messages` / `stream_answer` 内部 `except` 兜成**友好字符串**（不是 `""`、不是 `None`，否则毒化 history），主循环不用再管崩溃。

## 易错点（设计阶段踩过的坑）

- **历史限长的顺序**：必须「先成对 append（user+assistant）→ 再 `trim_history`」。`-MAX_TURNS*2` 是偶数，成对地砍，不留「有问没答 / 残缺开头」。
- **history 里存的是 messages 格式的字典**：`{"role":..,"content":..}`。
  - 不能 append 整个 `messages` 列表（那是 `[SYSTEM]+history+[user]`，会把一个列表塞进 history）。
  - 不能 append 裸字符串 `answer`（要包成 `{"role":"assistant","content":answer}`）。
- **两个「兜底」别混**：
  - 流式 for 循环里的 `delta.content or ""`：防某些 chunk 的 content 为 `None`（否则 print 出 "None" 且 `answer += None` TypeError）。
  - `except` 分支 `return f"...失败：{exc}"`：真出错时返回**友好提示字符串**，不是 `""`。

## Gate 4 必答（设计已覆盖）

1. **历史怎么存**：客户端 messages 列表，每轮重发 `[SYSTEM]+history+[user]`，`trim_history` 限长。
2. **key 不泄露**：走 `.env` → 环境变量 `os.environ.get`，代码无明文，`.env` 不进 git（`.gitignore` 加 `.env`，只提交 `.env.example`）。
3. **超时怎么表现**：超时 → SDK 抛异常 → `except` 接住 → return 友好提示 → 用户看到「调用失败：…」而非堆栈，程序继续不崩。
4. **哪个参数最影响输出稳定性**：`temperature`。

## 周末注意

- l1_03 和 l1_04 各自有自己的 `SYSTEM` / `MAX_TURNS`，import 时各取各的；保证两边 `SYSTEM` 文案一致即可。

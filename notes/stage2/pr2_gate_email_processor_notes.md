# PR2-Gate 邮件处理器笔记

> 对应任务：`PR2-Gate 结构化输出闯关`
> 代码位置：`code/stage2/pr2_gate_email_processor.py`
> 整理日期：2026-07-06

## 一、这关在练什么

PR2-Gate 不是新概念日，而是把阶段 2 的三个能力串成一条小流水线：

1. `simple_summarize(text)`：从邮件文本得到 `points` 和 `summary`。
2. `extract_email(text)`：从邮件文本抽取待办字段，返回 Python `dict`。
3. `validate_payload(todo)`：检查 `todo` 字段是否齐全，并确认能序列化成 JSON。
4. `classify(text)`：按规则判断分类标签。
5. `process_email(text)`：把以上结果组装成最终 `dict`。
6. `main()`：准备邮件文本、调用 `process_email`、保存 JSON 文件、打印结果。

一句话：模型/规则函数负责产出信息，`process_email` 负责整合，`main` 负责输入输出和保存。

## 二、核心函数职责

| 函数 | 输入 | 输出 | 作用 |
| --- | --- | --- | --- |
| `simple_summarize(text)` | 邮件或长文文本 | `(points, summary)` | 得到最多 3 条要点和一段摘要 |
| `classify(text)` | 文本 | 固定分类标签 | 用关键词规则返回 `问题/投诉/建议/闲聊/其他` |
| `extract_email(text)` | 邮件文本 | Python `dict` | 抽取 `sender/task/deadline/priority/need_reply` |
| `validate_payload(payload)` | Python `dict` | JSON 字符串 | 校验字段齐全，并确认能被 `json.dumps` 序列化 |

注意：`extract_email` 返回的是 Python `dict`，不是 JSON 字符串；`validate_payload` 校验通过后返回 JSON 字符串，但在 Gate 里主要借它做检查。

## 三、dict 和 JSON 的区别

- Python `dict`：程序内部正在使用的数据结构，例如 `result["todo"]["deadline"]`。
- JSON 字符串/JSON 文件：把数据打包成文本，适合保存到文件或传给别的系统。

这关的稳妥流程是：

```python
result = {
    "category": category,
    "points": points,
    "summary": summary,
    "todo": todo,
}

with open(OUT_FILE, "w", encoding="utf-8") as f:
    json.dump(result, f, ensure_ascii=False, indent=2)
```

不要手拼 JSON 字符串。先组装 Python `dict`，再交给标准库 `json.dump` 保存，才不容易写出非法 JSON。

## 四、process_email 的标准结构

```python
def process_email(text):
    points, summary = simple_summarize(text)
    todo = extract_email(text)
    validate_payload(todo)
    category = classify(text)
    return {
        "category": category,
        "points": points,
        "summary": summary,
        "todo": todo,
    }
```

关键点：

- `points, summary = simple_summarize(text)` 是解包，函数返回两个值，就用两个变量接。
- `validate_payload(todo)` 可以不接返回值，因为这里主要用它做检查。
- 如果 `todo` 缺字段，比如缺 `deadline`，`validate_payload` 会 `raise ValueError`，后面的代码默认不会继续执行。

## 五、main 的标准结构

```python
def main():
    email_text = """发件人：王五
事项：确认本周项目周报
截止时间：2026-07-06
优先级：中
需要回复：是
"""
    result = process_email(email_text)
    with open(OUT_FILE, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    print(f"结果已保存到 {OUT_FILE}")
```

关键点：

- 三引号里的前导空格会变成真实文本。邮件字段行要顶格写，否则 `extract_email` 可能把 `"    事项"` 当成 key，导致匹配失败。
- `json.dumps` 是转成字符串，适合打印。
- `json.dump` 是直接写文件，适合保存。
- `ensure_ascii=False` 让中文保持中文，不变成 `\uXXXX`。

## 六、路径理解

```python
ROOT = Path(__file__).resolve().parents[2]
OUT_FILE = ROOT / "resources" / "stage2_email_result.json"
```

- `ROOT`：项目根目录的绝对路径。
- `OUT_FILE`：结果文件 `resources/stage2_email_result.json` 的绝对路径。

原因：`resolve()` 会把当前脚本路径变成绝对路径；后面基于 `ROOT` 继续拼接，所以 `OUT_FILE` 也是绝对路径。

## 七、simple_summarize 的兼容修正

原来的 `simple_summarize` 只按中文句号 `。` 切：

```python
text.strip().split("。")
```

但邮件常常是按行写的，没有 `。`，所以整封邮件会被当成一条要点。

更稳的思路：

```python
if "\n" in text.strip():
    parts = text.strip().split("\n")
else:
    parts = text.strip().split("。")
list_of_sentences = [s.strip() for s in parts if s.strip()]
points = list_of_sentences[:3]
```

不能直接把 `。` 改成 `\n`，因为普通长文通常靠句号分句。要同时兼容“按行邮件”和“普通段落”。

## 八、分类稳定性

当前 `classify` 是规则版分类，靠关键词表判断：

```python
RULES = {
    "投诉": ["退款", "差评", "投诉", "太差", "垃圾"],
    "建议": ["建议", "希望", "最好能"],
    "问题": ["怎么", "如何", "为什么", "？", "?"],
    "闲聊": ["你好", "谢谢", "天气"],
}
```

规则版的特点：

- 优点：快、便宜、稳定、可解释。
- 局限：只认字面关键词，不懂语义。
- 撞类：一句话同时命中多个类别时，谁排在前面谁先返回。

测试分类稳定性要准备：

1. 每个标签多条样例，包含命中关键词和不命中关键词但语义接近的说法。
2. 边界样例：空文本、无关文本、同时命中多个类别关键词的文本。
3. 记录预测标签和期望标签，统计正确率，并分析错误原因：漏判、撞类、误命中。

## 九、哪些场景不能只靠 prompt

1. 严格 JSON 结构不能只靠 prompt。要用 `dict`、`validate_payload`、`json.dump/json.loads` 做代码校验。
2. 字段缺失或字段编造不能只靠 prompt。要在代码里检查缺字段，坏结果不能悄悄保存。
3. 分类稳定性不能只靠 prompt。要准备测试样例，记录预测标签和期望标签，统计正确率并分析漏判、撞类、误命中。

## 十、今天踩过的坑

- 把 `dict` 和 JSON 混在一起：`extract_email` 返回 `dict`，保存文件时才转 JSON。
- `ROOT/OUT_FILE` 误判为相对路径：二者都是绝对路径。
- 三引号邮件文本缩进：前导空格会变成真实内容，影响字段匹配。
- `{{...}}` 不是合法 JSON，也不是 Python `dict`；外面一层 `{}` 就够。
- 直接把 `split("。")` 改成 `split("\n")` 不稳，会破坏普通长文摘要。
- 在 Gate 文件里重复定义 `simple_summarize` 会遮住导入的旧函数；整合关应复用旧模块，不把旧函数复制一份塞进来。


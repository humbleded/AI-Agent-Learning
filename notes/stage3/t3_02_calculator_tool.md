# T3-02 计算器工具（Calculator Tool）概念笔记

> 日期：2026-07-06
> 资料：repos/hello-agents/docs/chapter4/第四章 智能体经典范式构建.md 的 4.2.1、4.2.2；code/stage3/t3_02_calculator_tool.py
> 整理方式：用户原话为主体；明显口误保留并在下方用 `⚠️ 订正` / `💡 补充` 标注。

## 一、T3-02 这一关到底在练什么？

模型擅长生成文本，模型的本质也是预测下一个最可能出现的 token，所以不能把数学题完全交给模型。模型不擅长运算、调用外部工具、查询。

计算器工具是标准的计算，通过程序去控制的，不是模型去预测的。

> 💡 补充：T3-02 练的是“把一个函数包装成 Agent 能用的工具”。模型负责判断“该用哪个工具、传什么参数”；程序负责校验参数、真正执行 `calculator_tool()`、拿到真实结果。
>
> 💡 补充：模型可以说“我要算 `3 * 5`，请调用计算器”；但真正的乘法结果必须由 Python 程序算出来，而不是让模型凭感觉补一个数字。

## 二、ReAct 链路：Thought / Action / Observation

例子：`3 * 5`

```text
Thought = 我需要做精确乘法，不能靠模型口算。
Action = 调用 calculator_tool，参数 operation="mul", a="3", b="5"。
Observation = 工具返回 {"ok": True, "result": 15.0}。
```

> 💡 补充：Action 更精确说是“模型提出调用请求”，不是真正执行。真正执行发生在客户端程序调用 `calculator_tool()`。
>
> 💡 补充：Observation 首先是“工具真实执行后的结果本身”，由客户端放回上下文，模型再观察这个结果够不够回答用户。

串完整链路时，我原来的说法：

```text
用户问：“3 * 5 等于多少之后，模型去查自己有没有计算工具，如果有告诉客户端需要调用计算函数名和参数3和5，
然后客户端去调用工具，工具返回结果之后，，模型会把结果放在上下文中去观察，判断是不是最终想要的结果，如果是，就返回给用户，如果不是，继续去调用
```

> ⚠️ 订正 1：不是“模型查自己有没有计算工具”，而是客户端把工具菜单发给模型，模型看菜单后选择 `calculator_tool`。
>
> ⚠️ 订正 2：不是“模型把结果放进上下文”，而是客户端把工具结果作为 Observation 放回上下文，模型再读取这个结果。

复习用标准链路：

```text
用户问题 -> 客户端把问题和工具菜单发给模型
模型 -> 生成 Action：选择 calculator_tool，并给出 operation/a/b
客户端 -> 解析 Action，找到真正的函数
客户端 -> 执行 calculator_tool("mul", "3", "5")
工具 -> 返回 {"ok": True, "result": 15.0}
客户端 -> 把这个结果作为 Observation 放回上下文
模型 -> 读 Observation，整理成人话回答用户
```

## 三、哪些问题适合 ReAct + 工具？

```text
A. “请解释一下什么是 Python 字典。”
B. “帮我算一下 9876 * 5432。”
C. “今天上海天气怎么样？”
```

我的判断：

```text
A. 不适合，因为不需要外部调用，或者需要计算，或者需要动手做
B. 适合，需要做计算来保证结果的正确
C. 适合，因为需要调用外部工具来查询天气
```

> ⚠️ 订正：A 的表达应更精确：解释已知概念不需要外部信息、精确计算或真实操作，所以一般不需要 ReAct + 工具。
>
> 💡 补充：工具主要补模型的三个短板：需要查外部世界、需要精确计算、需要真实执行动作。

## 四、工具三要素：Name / Description / Execution Logic

我的映射：

```text
Name：calculator_tool
Description：用于执行 add/sub/mul/div 四种基础数学运算
Execution Logic：
def calculator_tool(operation, a, b):
    ...
```

工具的三个核心要素：

```text
名字(Name)，描述(Description)，执行逻辑(Execution Logic).
名字用来唯一标识工具名称，让模型知道有哪些工具。
描述用来描述工具的作用是什么，让模型知道什么时候调用哪个工具。
执行逻辑是客户端具体执行的程序，让模型拥有了感知和调用外部环境的能力。
```

> 💡 补充 1：Name 不只是给模型看的，也是程序查找工具时用的唯一标识。模型和程序必须用同一个名字，才能接上。
>
> 💡 补充 2：Description 要写清能力边界。比如 `calculator_tool` 支持的是 `add/sub/mul/div` 四种基础数学运算，不是查天气，也不是解方程。
>
> ⚠️ 订正：Execution Logic 让“整个 Agent 系统”拥有外部能力；模型本身仍然不执行工具。

## 五、`CALCULATOR_SCHEMA` 是什么？

我写的人话 schema：

```text
工具名：calculator_tool
工具用途：进行加，减，乘，除运算
参数：
- operation："str",输入操作类型,只能是add/sub/mul/div
- a：第一个数，数字或可转成数字的字符串
- b：第二个数，数字或可转成数字的字符串
```

代码里的版本：

```python
CALCULATOR_SCHEMA = {
    "name": "calculator_tool",
    "description": "进行精确的加、减、乘、除运算。",
    "parameters": {
        "operation": "操作类型，只能是 add/sub/mul/div",
        "a": "第一个数，数字或可转成数字的字符串",
        "b": "第二个数，数字或可转成数字的字符串",
    },
}
```

> 💡 补充：Schema 可以理解成“工具说明书”。它告诉模型：这个工具叫什么、什么时候用、要传哪些参数、参数有什么限制。
>
> 💡 补充：今天这个 `CALCULATOR_SCHEMA` 是学习用的人话版 schema，还不是完整 OpenAI `tools` JSON Schema。后面会把 `name/description/parameters` 映射到 API 的 `tools` 字段。

## 六、`OPERATORS` 映射表为什么重要？

我的理解：

```text
是一张映射表，把操作名映射到对应的函数。这样模型返回用哪个方法的时候可以找对对应的函数。
```

代码：

```python
OPERATORS = {
    "add": operator.add,
    "sub": operator.sub,
    "mul": operator.mul,
    "div": operator.truediv,
}
```

> 💡 补充：模型给出来的是字符串，比如 `"mul"`；Python 真正能执行的是函数，比如 `operator.mul`。`OPERATORS` 就像一张“名字 -> 函数”的对照表。
>
> 💡 补充：`func = operator.sub` 只是拿到函数引用，还没有开始算；`result = operator.sub(10, 4)` 才是真正调用函数，结果是 `6`。

## 七、参数校验：为什么先检查 `operation`，再转 `float`？

我的回答：

```text
1. 判断operation是否存在
2. 判断a,b是否能转化为float类型的数据
3. 10 0返回提示，除数不能为0
```

代码链路：

```python
if operation not in OPERATORS:
    return {"ok": False, "error": f"不支持的操作：{operation}"}

try:
    a = float(a)
    b = float(b)
except ValueError:
    return {"ok": False, "error": "参数必须是数字"}

try:
    result = OPERATORS[operation](a, b)
except ZeroDivisionError:
    return {"ok": False, "error": "除数不能为 0"}
```

> 💡 补充 1：`operation` 更精确说是检查是否在 `OPERATORS` 里，也就是只允许 `add/sub/mul/div`。
>
> 💡 补充 2：先判断 `operation` 是否存在，可以避免对一个不存在的 key 取值导致 `KeyError`，也能少做后面的类型转换。
>
> 💡 补充 3：`float(a)` / `float(b)` 是把 `"3"`、`"5"` 这类字符串转成真正能计算的数字。转不动时返回“参数必须是数字”。
>
> 💡 补充 4：除零不是输入类型错，而是运算规则错，所以单独捕获 `ZeroDivisionError`，返回“除数不能为 0”。

## 八、工具返回结构：为什么要用 `ok/result/error`？

我第一轮写错了：

```text
1. 成功时返回{"code":"成功","result":...}
2. 失败时返回{"code":"失败","error":...}
3. 用户看不明白错误在哪，程序后续不会执行了。用返回错误提示的方式可以让用户知道自己哪里错了，程序后续可以继续执行
```

订正后的真实返回结构：

```python
{"ok": True, "result": ...}
{"ok": False, "error": ...}
```

> ⚠️ 订正：真实代码字段是 `ok/result/error`，不是 `code/result/error`。写笔记和回答题目时要跟真实代码字段保持一致。
>
> 💡 补充：失败时返回稳定结构，而不是直接把红色报错堆给用户，有两个好处：用户能看懂哪里错了；后续程序也能根据 `ok` 判断走成功分支还是失败分支。

## 九、今天最容易混的主语

复习时最重要的是分清“谁负责什么”：

```text
工具菜单由客户端提供。
模型选择工具和参数。
客户端真正执行 calculator_tool()。
客户端把 Observation 放回上下文。
模型读取 Observation，再决定是否回答用户或继续调用工具。
```

> 💡 补充：一句话记法：模型负责“想和说”，程序负责“查、算、做、回填”。

## 十、今天踩过的坑（错误理解 -> 正确理解）

1. `getTool("Weather")` 找不到工具时，我一开始说“大概率是 `{}`，走到 else”。
   - 正确理解：`self.tools.get(name, {})` 的中间默认值是 `{}`，但后面 `.get("func")` 得到的是 `None`，所以最终 `tool_function` 是 `None`。

2. 串 ReAct 链路时，我一度说“模型查自己有没有工具 / 模型把结果放进上下文”。
   - 正确理解：客户端提供工具菜单，客户端执行工具，客户端把 Observation 放回上下文；模型只选择工具、给参数、读取 Observation。

3. 工具返回结构我一开始写成 `{"code": "成功/失败"}`。
   - 正确理解：要按真实代码写，成功是 `{"ok": True, "result": ...}`，失败是 `{"ok": False, "error": ...}`。

4. `tool_function = calculator_tool` 容易被误以为已经算了。
   - 正确理解：这只是拿到函数引用，还没开始调用；加上括号和参数才会执行。

## 十一、复盘一句话

以后看到一个工具调用任务，先分清四件事：

```text
模型生成 Action；
客户端解析 Action；
客户端执行工具；
客户端把 Observation 回填给模型。
```

T3-02 的核心不是“做一个计算器”这么简单，而是第一次把“模型只会提出调用请求”和“程序负责真实执行”这条边界跑通了。

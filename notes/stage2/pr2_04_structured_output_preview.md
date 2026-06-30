# PR2-04 结构化输出（JSON / Schema）· 预读笔记

> 用途：PR2-04 动手前的**概念预读**（白天手机可看）。把 OpenAI 官方 Structured Outputs + DeepSeek JSON 模式两份文档翻成中文要点 + 大白话。
> 资料：OpenAI《Structured Outputs》、DeepSeek《JSON Output》官方文档（2026-06-30 抓取）。
> 注意：这是**资料/概念**，不是 PR2-04 的答案。PR2-04 那道「从邮件提取 6 个字段」的代码到时自己写，本笔记只帮你提前看懂「JSON 模式怎么调、schema 是什么」。

---

## 0. 一句话定位

PR2-04 要解决的事：让模型的输出**不是一段话，而是一个能被程序直接吃进去的 JSON**——字段固定、类型固定、能 `json.loads()` 解析、缺信息时不乱编。这是把「模型」接到「下游代码」的关键一环（呼应你 PR2-01/02/03 反复练的「prompt 锁 JSON」，这次更系统）。

---

## 1. 两个层次：JSON 模式 vs 严格 Schema（先把概念分清）

模型输出 JSON，可靠程度其实有**两档**：

| 档 | 名字 | 保证什么 | 不保证什么 |
| --- | --- | --- | --- |
| 弱档 | **JSON 模式**（`json_object`） | 输出**是一段合法 JSON**（能被 `json.loads` 解析、不会是 Markdown/大白话） | **不保证**字段对不对——可能少字段、多字段、类型不对、值乱编 |
| 强档 | **严格 Schema**（`json_schema` + `strict: true`） | 在「合法 JSON」之上，还保证：**字段齐全 / 类型正确 / 不许多余字段 / 枚举值不乱编 / 拒答能被检测** | （基本都被它管住了，所以叫「严格」） |

**大白话**：
- JSON 模式 = 「你给我说一段 JSON，别给我说人话」——只管**形式**是 JSON。
- 严格 Schema = 「你必须**照我这张表**填：哪几格、每格填什么类型、不许多填格、选项只能从这几个里挑」——管到**内容结构**。

> 关键差异原文：**"only Structured Outputs ensure schema adherence"**（只有严格 Schema 才保证「贴合你定的结构」；JSON 模式只保证「是合法 JSON」）。

---

## 2. schema（结构契约）到底约束哪几件事

「schema」= 你和模型之间约定的一张**结构表/契约**。严格模式下它能锁死 4 件事：

1. **必填字段（required）**：哪些 key 必须出现，不能漏。
2. **字段类型（types）**：每个值是 string / number / boolean / array / object…，不能给错。
3. **不许多余字段（`additionalProperties: false`）**：只能有你列的那些 key，模型不许自己加格。
4. **枚举值（enum）**：某字段的值只能从一个**固定集合**里选（比如优先级只能是 `高/中/低`），防止模型编出「特急」「随便」这种没定义的值。

> 这 4 件事即使在「弱档 JSON 模式」下也是你**想要**的目标——只是弱档不帮你强制，得靠你**在 prompt 里写清楚 + 在 Python 端自己校验**。

---

## 3. 处理「异常输出」要查的 3 个地方

模型不是每次都乖乖给你完美 JSON。官方建议拿到响应后查 3 处：

1. **`finish_reason == "length"`** → 输出被 `max_tokens` **截断了**（JSON 没写完，`json.loads` 会炸）。对策：调大 `max_tokens`。
2. **`message.refusal`** → 模型出于安全**拒答**了（严格模式下这是一个可被程序识别的字段）。
3. **`message.content`** → 正常内容，拿去 `json.loads` 解析。

**大白话**：解析前先确认「是不是被剪短了 / 是不是被拒了」，再去 `json.loads`，别上来就解析然后崩。

---

## 4. DeepSeek 上怎么落地（你真正要写的写法）

你用 DeepSeek（OpenAI 兼容 SDK）。按 DeepSeek 官方《JSON Output》文档：

### 开关
```python
response_format={'type': 'json_object'}
```
即上面说的**弱档 JSON 模式**（DeepSeek 官方 JSON 文档给的就是这一档）。

### 三条硬性要求（缺一可能不生效 / 出问题）
1. **prompt 里必须出现 `"json"` 这个词**（system 或 user 里都行）——这是触发 JSON 模式的硬条件。
2. **prompt 里要给一段 JSON 格式样例**，引导模型按你的结构输出。
3. **设好 `max_tokens`**，防止 JSON 被截断（呼应第 3 节的 `length` 坑）。

### 一个坑
> 官方原话：JSON 模式偶尔会**返回空 content**（"the API may occasionally return empty content"）。所以代码要兜底：空内容时别直接 `json.loads`（会炸），给个重试或友好提示。

### 官方通用示例（理解调用形态用，**不是** PR2-04 的答案）
```python
import json
from openai import OpenAI

client = OpenAI(api_key="<your api key>", base_url="https://api.deepseek.com")

system_prompt = """The user will provide some exam text. Please parse the "question" and
"answer" and output them in JSON format.
EXAMPLE INPUT: Which is the highest mountain in the world? Mount Everest.
EXAMPLE JSON OUTPUT: {"question": "Which is the highest mountain in the world?", "answer": "Mount Everest"}"""

user_prompt = "Which is the longest river in the world? The Nile River."

response = client.chat.completions.create(
    model="deepseek-v4-pro",
    messages=[{"role": "system", "content": system_prompt},
              {"role": "user", "content": user_prompt}],
    response_format={'type': 'json_object'},   # ← 开关
)
print(json.loads(response.choices[0].message.content))
```
注意这个示例里同时满足了三条要求：prompt 里有 "json"、给了 `EXAMPLE JSON OUTPUT` 样例、用了 `json_object`。

---

## 5. 把概念接到 PR2-04（方法论，不是答案）

PR2-04 任务：从一封邮件里提取 6 个字段（发件人、事项、截止时间、优先级、是否需要回复…），输出能 `json.loads()` 的 JSON、不编造缺失信息。

落地策略（因为 DeepSeek 官方 JSON 文档只给了弱档 `json_object`，没有 OpenAI 那种 `strict` 严格 Schema 档）：

1. **用 `json_object` 开 JSON 模式**（保证形式是合法 JSON）。
2. **在 prompt 里手写 schema**：点名 6 个字段 + 给空 JSON 模板 + 说清每个字段类型/取值（优先级用枚举 `高/中/低`、是否回复用 `true/false`）+ **强调缺失填 `null`、不许编造**。← 这一步等于「人肉补上严格 Schema 的 4 件事」。
3. **Python 端兜底校验**：先查空内容 / 截断，再 `json.loads`，再检查 6 个 key 是否齐、类型对不对。← 你 PR2-02 练过的「代码兜底≠约束模型，代码=事后把关」。

> 一句话：**严格 Schema 帮你做的事（必填/类型/不多字段/枚举/拒答检测），在 DeepSeek 上你用「prompt 写清 + 代码校验」两头夹出来。**

---

## 6. 几个英文词条（大白话速记）

- **schema**：结构契约，一张「该有哪些格、每格填什么」的表。
- **`additionalProperties: false`**：不许加我没列的格。
- **enum**：枚举，值只能从固定几个里选。
- **`finish_reason`**：模型为什么停——`stop`=正常说完，`length`=被 max_tokens 剪断。
- **refusal**：模型拒答（严格模式下是可识别的结构化字段）。
- **strict**：严格模式开关，开了才真按 schema 锁。

---

## 7. 预读自检（看完能答上就够，正式题留「练习」步）

- JSON 模式和严格 Schema 各保证什么、差在哪？
- schema 约束哪 4 件事？
- 在 DeepSeek 上开 JSON 模式有哪三条硬要求？那个「空 content」坑怎么兜？
- DeepSeek 没有严格 Schema 档，PR2-04 你打算用哪两手凑出同样效果？

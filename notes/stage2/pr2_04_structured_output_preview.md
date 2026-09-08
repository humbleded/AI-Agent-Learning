# PR2-04 结构化输出（JSON / Schema）· 预读笔记

> 用途：PR2-04 动手前的**概念预读**（白天手机可看）。把 OpenAI 官方 Structured Outputs + DeepSeek JSON 模式两份文档翻成中文要点 + 大白话。
> 资料：OpenAI《Structured Outputs》、DeepSeek《JSON Output》官方文档（2026-06-30 抓取）。
> 注意：这是**资料/概念**，不是 PR2-04 的答案。PR2-04 那道「从邮件提取 5 个字段」的代码到时自己写，本笔记只帮你提前看懂「JSON 模式怎么调、schema 是什么」。
> 2026-09-07 校准：修正字段数量、结构保证的边界和厂商功能范围；保留原学习日期，不把本次资料更新当作新的用户能力证据。

---

## 0. 一句话定位

PR2-04 要解决的事：让模型的输出**不是一段话，而是一个能被程序直接吃进去的 JSON**——字段固定、类型固定、能 `json.loads()` 解析、缺信息时不乱编。这是把「模型」接到「下游代码」的关键一环（呼应你 PR2-01/02/03 反复练的「prompt 锁 JSON」，这次更系统）。

---

## 1. 两个层次：JSON 模式 vs 严格 Schema（先把概念分清）

模型输出 JSON，可靠程度其实有**两档**：

| 档 | 名字 | 保证什么 | 不保证什么 |
| --- | --- | --- | --- |
| 弱档 | **JSON 模式**（`json_object`） | 正常完成时约束输出为合法 JSON；仍需处理空内容、截断等异常 | **不保证**字段对不对——可能少字段、多字段、类型不对、值乱编 |
| 强档 | **严格 Schema**（此处指 OpenAI 的 `json_schema` + `strict: true`） | 在支持的 schema 范围内，正常完成且未拒答的结果符合所声明的必填、类型、额外字段和枚举约束；拒答另有可检测信号 | **不保证事实或业务判断正确**；仍可能拒答、达到长度限制或调用失败，不能将这些情况当成正常结构化结果 |

**大白话**：
- JSON 模式 = 「你给我说一段 JSON，别给我说人话」——只管**形式**是 JSON。
- 严格 Schema = 「你必须**照我这张表**填：哪几格、每格填什么类型、不许多填格、选项只能从这几个里挑」——管到**内容结构**。

> 关键差异原文：**"only Structured Outputs ensure schema adherence"**（只有严格 Schema 才保证「贴合你定的结构」；JSON 模式只保证「是合法 JSON」）。

---

## 2. schema（输出结构规则）到底约束哪几件事

「schema」= 一张规定**有哪些字段、每个字段允许什么类型和值**的结构表。严格模式在正常完成且未拒答时，按所声明且受支持的规则约束以下 4 件事：

1. **必填字段（required）**：哪些 key 必须出现，不能漏。
2. **字段类型（types）**：每个值是 string / number / boolean / array / object…，不能给错。
3. **不许多余字段（`additionalProperties: false`）**：只能有你列的那些 key，模型不许自己加格。
4. **枚举值（enum）**：某字段的值只能从一个**固定集合**里选（比如优先级只能是 `高/中/低`），防止模型编出「特急」「随便」这种没定义的值。

> 这 4 件事即使在「弱档 JSON 模式」下也是你**想要**的目标——只是弱档不帮你强制，得靠你**在 prompt 里写清楚 + 在 Python 端自己校验**。

---

## 3. 处理「异常输出」要查的 3 个地方

模型不是每次都乖乖给你完美 JSON。官方建议拿到响应后查 3 处：

1. **`finish_reason == "length"`** → 生成触及长度限制，不能把它当成正常完成。JSON 可能不完整；即使恰好能被 `json.loads` 解析，也不代表任务完整。对策：检查输出预算和输入长度，按需要增加预算、精简要求或拆分任务后再请求。
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

### 官方使用要求与长度设置
1. **把 `response_format` 设为 `json_object`**，打开 JSON 模式。
2. **prompt 里包含 `"json"` 这个词，并提供 JSON 格式样例**，说明要生成的内容和结构。
3. **根据预期输出设置足够的 `max_tokens`**，并检查实际完成状态；设置参数本身不保证任何输出都不会截断。

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
    max_tokens=2048,  # 示例预算；仍需检查 finish_reason，按任务调整
)
print(json.loads(response.choices[0].message.content))
```
这个示例打开了 `json_object`，prompt 中有 "json" 和样例，也显式设置了输出预算。它只展示调用形态；实际程序还需按第 3 节处理空内容、截断、解析失败和字段校验。

---

## 5. 把概念接到 PR2-04（方法论，不是答案）

PR2-04 任务：从一封邮件里提取 5 个字段（发件人、事项、截止时间、优先级、是否需要回复），输出能 `json.loads()` 的 JSON、不编造缺失信息。

落地策略：本任务使用 DeepSeek 普通回答的 `json_object`，它不强制遵守自定义 schema。不能据此推断 DeepSeek 所有接口都没有严格模式：截至 2026-09-07，官方另有 `/beta` 端点的 Tool Calls strict 模式，用来约束**工具调用参数**，与这里的普通回答 JSON 模式不是同一个功能；本任务不因此新增接口迁移要求。

1. **用 `json_object` 开 JSON 模式**，先约束输出形式。
2. **在 prompt 里写清结构**：点名 5 个字段 + 给空 JSON 模板 + 说清每个字段类型/取值（优先级用枚举 `高/中/低`、是否回复用 `true/false`）+ **强调缺失填 `null`、不许编造**。这一步是引导，不能保证模型一定遵守。
3. **Python 端兜底校验**：先查空内容 / 截断，再 `json.loads`，再检查 5 个 key 是否齐、类型和取值是否符合规则，不合格就拒绝交给下游或有限重试。← 你 PR2-02 练过的「代码兜底≠约束模型，代码=事后把关」。

> 一句话：**本任务用“提示写清 + 代码检查”把住下游入口；这是事后发现并拦住不合格结果，不等同于生成时的严格结构约束，也不会自动补出厂商的拒答信号。**

---

## 6. 几个英文词条（大白话速记）

- **schema**：输出结构规则，一张「该有哪些格、每格填什么」的表。
- **`additionalProperties: false`**：不许加我没列的格。
- **enum**：枚举，值只能从固定几个里选。
- **`finish_reason`**：模型为什么停——`stop`=正常停止，`length`=触及长度限制；正常停止本身也不保证事实与任务完成情况正确。
- **refusal**：模型拒答（严格模式下是可识别的结构化字段）。
- **strict**：严格模式开关，开了才真按 schema 锁。

---

## 7. 预读自检（看完能答上就够，正式题留「练习」步）

- JSON 模式和严格 Schema 各保证什么、差在哪？
- schema 约束哪 4 件事？
- 在 DeepSeek 上开 JSON 模式要怎样设置请求和 prompt？为什么设置了输出预算仍需检查完成状态？那个「空 content」坑怎么兜？
- PR2-04 使用的普通回答 JSON 模式不强制自定义结构，你打算怎样引导和检查结果？为什么代码检查不等于生成时的严格约束？

## 2026-09-07 官方核验来源

- [OpenAI Structured Outputs](https://developers.openai.com/api/docs/guides/structured-outputs)：区分 JSON 与 schema 约束，明确仍可能有内容错误、拒答和不完整响应。
- [DeepSeek JSON Output](https://api-docs.deepseek.com/guides/json_mode/)：`json_object`、prompt 说明与样例、输出预算及空内容处理。
- [DeepSeek Tool Calls](https://api-docs.deepseek.com/guides/tool_calls/)：strict Beta 约束工具参数，不能与普通回答格式混为一谈。

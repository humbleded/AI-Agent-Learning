# A4-02 LLM 与 Agent 基础

> 学习日期：2026-07-12—2026-07-15
>
> 整理日期：2026-07-15
>
> 状态：PASS（2026-07-15 正式复核定稿）
>
> 学习资料：Hugging Face `what-are-llms.mdx`、`messages-and-special-tokens.mdx`；Hello-Agents 2.4.3、2.4.4、3.1.3、3.2.2、3.3.2
>
> 证据记录：`daily/2026-07-14.md`、`daily/2026-07-15.md`
>
> 写作方式：根据指定资料、用户原始作答、订正过程和综合迁移自动提炼；不逐字复制聊天

## 一页速记

LLM 的核心工作是根据当前可见的 Token 序列，为下一个候选 Token 打分并继续生成。它可以在 Agent 中理解指令、规划下一步、生成回答或 Tool Call，但不会自己访问文件、请求 API、扣款或删除数据。

~~~text
用户目标
  ↓
客户端保存 messages，并用匹配模型的 Chat Template 格式化
  ↓
Tokenizer 转成 Token ID
  ↓
LLM 生成回答或 Tool Call
  ↓
客户端解析、校验并分发
  ↓
工具执行真实 Action，返回 Tool Result
  ↓
客户端把结果回填为 Observation
  ↓
LLM 读取真实结果，继续行动或生成 Final Answer
~~~

一句话记忆：

> 模型负责“提出下一步”，客户端和工具负责“让这一步真实发生”；真实工具结果和外部系统状态比模型生成的说法更权威。

## 1. LLM 不是固定问答字典

字典依赖固定的“问题 → 答案”映射；LLM 学到的是大量文本中的统计规律，这些规律分散在许多参数中，通常无法指出“某一个参数就保存某一条知识”。

~~~text
输入 Token 序列
      ↓
模型结合上下文计算全部候选 Token 的分数
      ↓
按解码策略选择一个 Token
      ↓
把新 Token 接回序列，再次计算
~~~

这叫自回归生成（Autoregressive Generation）。模型的参数数量由结构和配置确定，训练更新的是参数值。参数更多通常意味着容量更大，但模型能力还取决于训练数据、训练方法、计算资源和模型结构，所以不能推出“参数越多一定越强”。

## 2. Encoder、Decoder 与 Encoder-Decoder

| 架构 | 入门理解 | 常见任务侧重 |
|---|---|---|
| Encoder | 把整个输入编码成上下文表示 | 分类、检索、语义表示 |
| Decoder | 根据已有 Token 继续生成新 Token | 对话、续写、代码生成 |
| Encoder-Decoder | 先编码输入，再生成目标序列 | 翻译、摘要、序列转换 |

这张表描述的是常见任务侧重，不是绝对能力边界。

### Decoder-Only 为什么也能读取用户输入

Decoder-Only 没有独立的 Encoder 堆栈，但它仍会读取当前位置之前的全部可见 Token：System、User、历史 Assistant、工具结果以及已经生成的内容都会影响后续候选 Token 的分数。

~~~text
已有输入 → 预测一个 Token → 接回序列 → 重新计算 → 继续生成
~~~

### 因果掩码（Causal Mask）

训练时完整句子已经存在。因果掩码禁止当前位置关注未来 Token，避免模型“偷看答案”。

以 `Agent uses tools safely` 为例，在预测 `tools` 前，当前位置只能利用 `Agent uses`，不能直接看到未来的 `tools safely`。掩码将未来位置的注意力分数压到极小值，经过 Softmax 后权重接近 0。

## 3. Token、Tokenizer、Special Token 与 EOS

- Token：模型处理文本时使用的离散单位，不一定等于一个汉字、一个完整单词或一个词。
- Tokenizer：按模型配套规则把文本切分并转换成 Token ID，也能把 Token ID 解码回文本。
- Vocabulary：该模型可使用的 Token 集合，是生成时候选 Token 的来源。
- Special Token：表示序列、角色、消息开始/结束等结构边界的特殊标记。
- EOS（End of Sequence）：告诉模型或生成程序序列已结束，不等于展示给用户的句号。

现代模型常使用子词分词（Subword Tokenization）：高频词可能保留为整体，低频词可以拆成多个子词。BPE 是常见算法之一，通过反复合并高频相邻单元建立词表；本任务只需理解分词目的与 Token 边界，不要求背 BPE 的完整训练实现。

## 4. Prompt、预训练、微调与上下文学习

### Prompt 为什么能改变输出

Prompt 不会在推理时修改模型参数。它改变的是当前输入上下文，因此会改变哪些 Token 对当前预测更重要，以及候选 Token 的分数分布。

模型也不是把输入与词库中的“相似 Token”直接比较：Tokenizer 先产生 Token 序列，模型再结合整个上下文为下一步候选 Token 打分。

### 预训练与微调

~~~text
大规模通用语料
  ↓ 自监督预训练，更新参数
Base Model：学到语言、上下文和广泛知识模式
  ↓ 使用具体任务标注数据继续训练
适应下游任务的新模型版本
~~~

例如邮件分类：

~~~text
已标注的投诉/咨询邮件
→ 继续调整模型参数
→ 学会“邮件内容 → 投诉或咨询标签”的映射
~~~

微调不是泛泛地“让模型更理解语义”，而是使用明确训练数据，把模型适配到具体目标。

### Instruction Data、Instruction Tuning 与 Prompting

| 概念 | 是什么 | 是否改变参数 |
|---|---|---|
| Instruction Data | “指令/输入 → 理想回答或动作结构”的训练样本 | 数据本身不会；训练使用它时才会 |
| Instruction Tuning | 使用指令数据继续训练模型的过程 | 会更新模型参数 |
| Prompting | 推理时提供的当前输入 | 不更新模型参数 |

指令微调能让模型更稳定地遵循任务、对话格式或 Tool Call 结构，但真实工具仍由客户端执行。

### Zero-shot、Few-shot 与 In-context Learning

| 方式 | 输入里有什么 | 参数是否改变 | 是否自动保留到以后请求 |
|---|---|---|---|
| Zero-shot | 任务说明，没有示例 | 否 | 否 |
| Few-shot | 任务说明 + 少量示例 | 否 | 否，必须再次提供上下文 |
| Fine-tuning | 训练数据 + 训练过程 | 是 | 保存在新模型参数中；后续请求必须调用该模型 |

In-context Learning（上下文学习）表示模型根据当前 Prompt 的指令和示例临时适应任务；这里的“学习”不等于永久修改参数。

## 5. Messages、Chat Template 与模型输入

程序通常先用结构化 messages 保存对话：

~~~python
messages = [
    {"role": "system", "content": "你是一个学习助手"},
    {"role": "user", "content": "解释 Token"},
    {"role": "assistant", "content": "Token 是……"},
]
~~~

模型最终读取的不是 Python 字典，而是 Chat Template 序列化并由 Tokenizer 转换后的 Token ID 序列。

~~~text
结构化 messages
       ↓ Chat Template
带角色、顺序、边界和生成起点的 Prompt 字符串
       ↓ Tokenizer
Token IDs
       ↓
LLM
~~~

Chat Template 的作用是把消息转换成模型训练时熟悉的输入格式，不是直接“控制输出格式”，也不负责永久保存历史。

如果模板与目标模型不匹配，模型可能把错误的特殊标记当成普通文字 Token，或错误判断角色、消息边界和生成起点。

### Base Model 与 Instruct Model

- Base Model：主要通过预训练学会续写文本。
- Instruct Model：在 Base Model 基础上经过指令数据训练，更擅长遵循指令和对话。

只给 Base Model 套上 ChatML 角色标记，不会把它变成 Instruct Model。正确模板是模型正确解释消息边界的必要条件，但指令遵循能力仍来自训练。

### `apply_chat_template()`

~~~python
rendered_prompt = tokenizer.apply_chat_template(
    messages,
    tokenize=False,
    add_generation_prompt=True,
)
~~~

- `tokenize=False`：返回格式化后的 Python 字符串 `str`，暂不转换为 Token ID。
- `add_generation_prompt=True`：在模板支持时添加 assistant 开始生成的位置。
- 这一步只做格式化，没有真正调用 LLM，也没有修改模型参数。

## 6. API 无状态与上下文边界

在本课程使用的常见模型 API 调用中，模型不会自动记住上一次请求。客户端需要保存必要历史，并在下一次调用中重新发送。

~~~text
客户端保存历史
   ↓
本轮请求重新发送必要 messages
   ↓
Chat Template + Tokenizer 构造输入
   ↓
模型才能理解“继续第二步”指的是哪一步
~~~

Attention 只能处理当前上下文中的信息，不能读取没有被放入输入的聊天历史或工具结果。

## 7. LLM、客户端、工具、Action 与 Observation

| 主体 | 负责什么 | 不负责什么 |
|---|---|---|
| LLM | 理解上下文，生成回答、计划或 Tool Call | 不直接执行文件、API、数据库或危险操作 |
| 客户端/执行模块 | 维护 messages，解析和校验 Tool Call，调用工具，回填结果 | 不应把模型自然语言当成权威外部状态 |
| 工具 | 执行真实计算或外部操作，返回 Tool Result | 不自行决定用户最终意图 |
| Observation | 承载工具结果和环境反馈，供下一轮模型读取 | 不是执行动作的主体 |

完整链路：

~~~text
LLM 第一次调用：生成 Tool Call 请求
→ 客户端解析 JSON、校验工具名/参数/权限/确认状态
→ 工具执行真实 Action
→ 工具返回 Tool Result
→ 客户端把结果作为 Observation 回填 messages
→ LLM 第二次调用：读取 Observation，继续判断或生成 Final Answer
~~~

模型输出 `Observation: ...` 这几个字，不代表工具真的运行过。判断真实性要看客户端代码是否真的解析请求、调用工具并回填返回值。

### 危险操作的硬边界

System Message 是软约束，模型仍可能不遵守。删除、扣款、发消息等副作用操作还需要客户端代码强制检查：

~~~text
明确用户确认
+ 工具 allowlist / JSON Schema
+ 参数、路径、权限和业务状态校验
+ 真实执行结果
~~~

没有明确确认时，客户端应拒绝执行并要求用户确认，而不是把安全责任交给模型自由生成。

## 8. 模型幻觉与 Agent 风险

模型幻觉（Hallucination）是指模型生成的内容缺乏事实依据、与现实不符，或与当前输入/上下文直接矛盾。语言流畅、语气确定，不等于内容已经核实。

### 三种常见表现

| 类型 | 含义 | 例子 |
|---|---|---|
| 事实性幻觉（Factual） | 生成与现实不符或不存在的事实 | 编造不存在的航班 |
| 忠实性幻觉（Faithfulness） | 没有忠实反映来源文本或工具结果 | 把“3 天到账”总结成“30 天” |
| 内在幻觉（Intrinsic） | 与当前输入或上下文直接矛盾 | Observation 是 `timeout`，模型却说“成功” |

分类可以重叠：把 `timeout` 说成“成功”既与输入直接冲突，也没有忠实反映工具结果。

### 为什么会产生

- 训练数据可能错误、矛盾、过时或含有偏见。
- 自回归目标优化的是下一个 Token 的生成，不内置数据库查询或事实核查。
- 多步推理中，前一步错误可能进入后续上下文并继续放大。
- 参数中的历史知识不等于当前价格、库存、订单或系统状态。

### 为什么在 Agent 中更危险

~~~text
普通聊天：错误生成 → 用户看到错误信息

Agent：错误判断
   → 错误 Tool Call 或错误参数
   → 客户端若缺少校验
   → 工具执行真实副作用
   → 错误状态进入下一轮继续放大
~~~

例如支付工具实际返回失败，模型却输出“成功”；若下游代码信任模型生成的状态，就可能触发本不该发生的扣款或发货。

## 9. 可靠性防线分别兜哪一层

| 防线 | 主要解决什么 | 不能保证什么 |
|---|---|---|
| System/Prompt | 引导模型按规则生成、表达不确定性 | 不能形成绝对安全边界 |
| RAG | 把可更新的外部文档放进上下文 | 检索可能错，模型也可能曲解文档 |
| 外部工具/API | 获取实时状态、精确计算或真实文件内容 | 结果回填后，模型仍可能错误解释 |
| 程序硬校验 | 强制 Schema、allowlist、权限、路径、状态机和重试规则 | 只能保护已经编码的规则 |
| 人工确认 | 在高风险副作用前确认人的真实意图 | 不能替代事实来源和程序权限检查 |

可靠系统的原则是：

~~~text
模型生成候选
   ↓
外部事实源 + 客户端硬校验
   ├─ 证据充分且规则通过 → 继续
   └─ 失败/超时/未知       → 拒绝、有限重试或报告未知
~~~

### 超时不是成功，也不是失败

订单 API 返回 `timeout` 时，权威事实只是“这次查询超时”，订单真实状态仍然未知。

正确处理：

1. 只有重试策略允许时才有限重试。
2. 仍失败就停止查询。
3. 对用户说明“目前无法确认订单状态”。
4. 不把超时猜成已支付、未支付、成功或失败。
5. 不允许下游依据模型猜测执行发货、扣款等动作。

缓解方法只能降低幻觉发生概率和影响，不能让 LLM 永远正确。

## 10. 三个必答问题

### 1. LLM 在 Agent 中扮演什么角色？

LLM 是语言理解和决策生成核心：读取当前上下文，生成回答、计划或 Tool Call。它不是执行器；客户端负责维护上下文、解析校验和调用，工具负责真实执行，客户端再把结果回填为 Observation。

### 2. 消息格式为什么重要？

模型最终只读取 Token 序列。Chat Template 必须按目标模型熟悉的角色、顺序、边界和生成起点，把 messages 转换成 Prompt；模板不匹配或历史缺失会让模型误判谁说了什么、消息在哪里结束，以及“第二步”指什么。

### 3. 幻觉会如何影响 Agent？

幻觉会从错误回答升级为错误 Tool Call、错误参数、对失败结果的错误解释或连续多轮错误行动。外部工具提供事实，客户端代码强制结构/权限/状态规则，人工确认保护高风险意图；三者不能只由 System Message 替代。

## 11. 对话中的高价值理解演进

| 原始理解 | 订正 / 补充 | 当前结论 |
|---|---|---|
| 参数越多，模型理解能力越强 | 参数量只是容量因素之一 | 数据、方法、算力和结构共同决定能力 |
| 模型把输入与相似 Token 比较 | 模型为整个词表的候选 Token 打分 | Prompt 改变上下文和分数，不改变参数 |
| Chat Template 控制模型输出格式 | 它先格式化模型输入 | 输出结构还需提示、训练和客户端校验 |
| 给 Base Model 套 ChatML 就是 Instruct Model | 模板不等于指令训练 | 模板负责边界，指令能力来自训练 |
| Attention 可以获取工具结果 | 不在上下文中的结果无法被注意力读取 | 客户端必须回填 Observation |
| 模型生成删除请求可能已经删除 | Tool Call 只是请求 | 客户端和工具决定副作用是否发生 |
| Chat 服务会自动记得“第二步” | 常见模型 API 调用无状态 | 客户端必须保存并重发必要历史 |
| 工具返回失败但模型说成功只是一般回答错误 | 它直接违背 Observation | 这是内在/忠实性幻觉，可能触发真实业务事故 |
| 查询超时可以推断订单失败 | 超时只说明本次查询未得到状态 | 权威结论是“未知”，不能猜测具体状态 |

## 12. 综合迁移证据摘要

| 场景 | 关键演进 | 教学检查结果 |
|---|---|---|
| 读取 `report.txt` 并总结 | 首答把 Chat Template 说成控制输出，且第二次 LLM 调用职责不完整；订正为“格式化输入 → 真工具读取 → Observation → 第二次 LLM 根据内容总结” | `PARTIAL/RETRY → PASS` |
| “继续第二步” + 错用 SmolLM2 标记给 Llama | 独立识别历史缺失与模板不匹配两个根因，并给出客户端保存原始 messages、用目标模型模板渲染的修复 | `PASS` |
| 订单 API `timeout`，模型却输出 `paid/ship` | 判为内在幻觉；指出 System 是软约束、API 结果是权威事实、超时后必须有限重试并保持状态未知 | `PASS` |
| 6000 条 Tool Call 样本、继续训练与请求内 3 条示例 | 独立区分 Instruction Data、Instruction Tuning 与 Few-shot Prompting，并正确判断参数变化和跨请求持久性；补充“后续必须调用微调后的模型” | `PASS` |

上述教学证据与 2026-07-15 的独立正式迁移题共同覆盖三个任务 PASS 标准；`ai-agent-learning-review` 已于 2026-07-15 正式判定 A4-02 `PASS`。

## 核心定义与复习路由（正式定稿）

> 正式复核已与活跃弱点、既有 `CD-*` 和知识库概念页做语义去重。这里只记录路由结论；完整排期以 `tracker/weak-points.md` 为唯一事实源。

| 语义目标 | 路由 | 当前证据 / 去重说明 | 正式动作 |
|---|---|---|---|
| 区分 Instruction Data、Instruction Tuning、Prompting 与 Few-shot | `must-recall` | F1 独立迁移 `PASS`；知识库已有正确内容，但知识存在不等于可独立回忆 | 建立 `CD-001`，首轮 2026-07-29 |
| 说明 messages → Chat Template → Prompt → Token IDs，以及模板为何影响边界 | `must-recall` | G8、`apply_chat_template()` 订正和综合场景 2 已通过；无同义活跃弱点 | 建立 `CD-002`，首轮 2026-07-29 |
| 完整说明 Tool Call → 客户端校验/执行 → Tool Result → Observation → 第二次 LLM | `must-apply` | 综合场景 1 已 `RETRY → PASS`；与 `WP-17` 语义重叠 | 不建核心定义卡；`WP-17` 移入稳定错题池 |
| 解释幻觉如何放大为 Agent 错误行动，并区分工具、代码和人工防线 | `must-recall` | 幻觉小考与综合场景 3 已通过；比 `WP-14` 的代码实景识别范围更广 | 建立 `CD-003`，首轮 2026-07-29 |
| Token/EOS、BPE 细节、三类 Transformer 的任务侧重 | `reference-only` | 已有稳定即时证据，后续任务会自然复现 | 保留在 notes/知识库，不单独排期 |
| Decoder-Only 与因果掩码 | `reference-only` | 已能解释可见 Token 范围及禁止偷看未来的原因 | 后续读码需要时再迁移，不单独排期 |

## 关联文件

- `daily/2026-07-14.md`
- `daily/2026-07-15.md`
- `tracker/progress.md`
- `tracker/ai-agent-learning-tracker.md`
- `tracker/weak-points.md`
- `notes/stage4/a4_01_what_is_agent.md`
- `notes/stage3/t3_gate_tool_assistant.md`
- `repos/agents-course/units/zh-CN/unit1/what-are-llms.mdx`
- `repos/agents-course/units/zh-CN/unit1/messages-and-special-tokens.mdx`
- `repos/hello-agents/docs/chapter2/第二章 智能体发展史.md`
- `repos/hello-agents/docs/chapter3/第三章 大语言模型基础.md`

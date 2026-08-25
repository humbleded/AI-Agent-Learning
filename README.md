# AI Agent Learning Workspace

这个仓库记录从零学习 AI Agent 应用开发的全过程。当前主目标是初级/初中级 Agent 应用开发，次目标是大模型应用后端与 RAG/知识库工程。

## 事实源

- `tracker/progress.md`：课程状态唯一事实源。
- `tracker/daily-plan.md`：当前知识单元、Session 起点和主队列。
- `tracker/weekly-plan.md`：W1–W20 依赖驱动内容块；W 是稳定记账 ID，不是日历周。
- `tracker/ai-agent-learning-tracker.md`：任务资料、产物和 PASS rubric。
- `tracker/job-readiness.md`：岗位资格、技术匹配与作品证据唯一事实源。
- `tracker/weak-points.md`：复习调度唯一事实源。
- `tracker/work-scenario-coverage.md`：生产场景与故障证据唯一事实源。
- `tracker/algorithm-progress.md`：W4–W20 算法配额与历史记录。
- `daily/YYYY-MM-DD.md`：按日期保存 Session 原始证据，不是每日课表。
- `code/`、`notes/`、`repos/`、`resources/`：真实练习、笔记、参考源码与数据。

## 怎么用

1. 说 `开始今天的学习` 或 `开始今天的学习计划`，只预览当前知识单元、资料、产物、PASS 标准和 Session 起点。
2. 说 `开始带读` 或 `开始动手` 才启动实际 Session；此时创建/更新当天 daily，并在真正开始任务时把 `TODO` 改为 `DOING`。
3. Session 可以跨日期；续接时读取该任务全部前序 daily，从明确起点继续，不重置题量和证据。
4. 输入/实现完成后说 `开始今天的练习`，只补任务级覆盖缺口。
5. 说 `检查今天的学习`，按该任务全部 Session 和真实产物执行正式验收；符合授权边界时同步知识库。
6. 未开始任务不预建代码、notes、daily 或课程骨架；只在进入实际动手环节时创建当前 TODO 骨架。

## A4 后依赖主路线

当前入口和任务状态只读 `tracker/daily-plan.md` 与 `tracker/progress.md`，README 不复制会过期的状态。`G8-00` 虽沿用阶段 8 的编号，课程位置实际是阶段 4.5：它只是先把已经 PASS 的 Agent 控制循环迁移到显式 Graph，不代表阶段 5～7 被跳过。

```text
G8-00 Graph 基础（阶段 4.5）
  → R6-01 文档导入与切分 → BE5-01 工程结构、日志与测试
  → B0-01/03/04/Gate → BE5-04 PostgreSQL + pgvector
  → R6-02/S-02 检索 → R6-03/S-06 RAG 对照与选型
  → BE5-02/03 并发、FastAPI/Pydantic/SSE
  → G8-01/02/03 持久化、恢复、HITL 与幂等
  → BE5-05/BE5-Gate → R6-Gate
  → D7-02/S-04 多 Agent 取舍与受控对照 → G8-Gate
  → D7-01/03/Gate 编排模式与长期 Memory
  → M9 MCP → E10 评估与系统设计
  → S-01、J11-02～06、S-05 产品化收口 → FINAL-Gate
  → J11-07/08/Gate 求职材料、面试与最终证据复核
```

`J11-01` 从真实项目开发开始持续累计 Git/PR/CI/review 证据，最晚在 `J11-06` 前收口；`H5-01` 只在真实框架调用链阻塞时触发，不阻塞主线。精确挂载点与状态写回规则见 `tracker/daily-plan.md`。

两个旗舰项目：

- LangChain：`code/stage6/engineering_docs_rag/`，工程文档 RAG 助手。
- LangGraph：`code/stage8/incident_change_review_agent/`，故障诊断与变更评审 Agent。

FastAPI 是两个项目共同的 HTTP/SSE/认证/输入校验交付层，并统一规定系统出错时返回什么、调用方怎样处理；它不被归类为 Agent 编排框架。两个项目可以共享工程原则和组件，但必须分别证明用户独立完成了什么。

前端使用 Vue。用户已说明会一些 Vue，因此不会机械重上整套入门；先用一个最小切片核验已经掌握的部分。真正进入需要界面的任务时，助手可以先检查许可证、维护状态、依赖与安全风险，再从 GitHub 选择并组合开源 Vue 骨架。若 G8-Gate 提前使用第三方 Vue，用户当场完成来源/许可证/依赖/关键 diff 的最小审核和数据/密钥边界说明；完整组件状态、SSE、认证、错误处理和亲自修改能力在 J11-03 验收。助手完成的机械搭建不算用户独立掌握 Vue 的证据，也不会在任务开始前提前克隆项目。J11-02 冻结唯一 `product_flagship`，只为它建设正式 Vue、公网产品和产品级观测；另一个旗舰保留可复现 API/demo、容器和完整评估，避免做两套前端。

## 多 Agent 与 Memory

- `S-04` 在 LangGraph 项目中实现受控多 Agent：先保留单 Agent baseline，再验证带类型约束的角色交接格式、共享/私有 state、停止、预算、人工升级和收益；无净收益就回退。
- `D7-03` 实现生产级长期 Memory：跨会话 CRUD、TTL、provenance、冲突、删除、租户隔离、PII 与 poisoning。
- G8 checkpoint/thread state 只保存一次运行的可恢复执行状态，不能冒充长期 Memory。

## 算法保护

W4–W20 共 17 个内容块，最低 52 道新题；每块固定 `3 新 + 1 旧错题`，W4 以第 4 道新题替代无旧题的复测位。路线重排不会降低题量、复测、复杂度解释或测试要求。

## 本地配置

复制 `.env.example` 为 `.env`，填入真实密钥。`.env` 已被 `.gitignore` 忽略，不应提交到 GitHub。

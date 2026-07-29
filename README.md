# AI Agent Learning Workspace

这个文件夹用于记录 AI Agent 开发学习全过程。

## 常用文件

- `tracker/ai-agent-learning-tracker.md`：完整学习路线、每项资料、作业、问答、通过标准。
- `tracker/progress.md`：总进度表。
- `tracker/job-readiness.md`：岗位能力、作品证据和 JD 差距；课程 PASS 不等于求职就绪。
- `tracker/weekly-plan.md`：W1–W20 内容块与里程碑。
- `tracker/algorithm-progress.md`：W4 起的算法新题/错题回炉记录。
- `daily/TEMPLATE.md`：每日打卡模板。
- `code/`：你自己写的代码。
- `notes/`：视频、文档、源码阅读笔记。
- `repos/`：参考源码仓库。

## 每天怎么用

1. 用 `weekly-plan.md` 定位当前内容块，再用 `progress.md` 选择其中未完成的任务。
2. 在 `daily/` 复制一份模板，命名为当天日期。
3. 真正开始动手时，才在 `code/对应阶段/` 创建当前任务的 TODO 骨架并由用户完成；不要提前批量生成未来代码文件。
4. 把笔记写到 `notes/对应阶段/`。
5. 把每日打卡发给 Codex。
6. Codex 检查代码和答案后，更新 `tracker/progress.md`。
7. 只有 Gate、作品集里程碑、模拟面试或 W6/W12/W16/W19 JD 审计才更新 `tracker/job-readiness.md`。

## 当前路线规则

- 实时课程状态只读 `tracker/progress.md`，当前执行入口由 `tracker/daily-plan.md` 派生；README 不复制易过期的任务快照。
- `T3-Gate` 必须走真实模型 `tools/tool_calls → 客户端执行 → role="tool" 回填 → 最终回答`，关键词规则路由只能作对照。
- 未开始任务不预建代码骨架；Gate 在设计准备日、普通任务在开始动手时即时建骨架。
- 阶段 0.5 工程基础不再整块卡住 Agent 主线，而是按场景穿插补：
  - API 调用时补 HTTP、timeout、headers、status code。
  - 环境配置时补 venv、包安装、环境变量。
  - Memory/RAG 需要持久化时补 SQL 和数据库。
  - 本地多服务或部署时补 Docker Compose。
- A4-Gate 后先做 `G8-00 LangGraph Lite`，只迁移一条既有 Agent 路径；高级持久化、interrupt/resume 和故障恢复仍留到 G8。H5 压成可选的 1–2 日源码单链路追踪，不阻塞阶段 5.5。
- 阶段 5.5 系统补 Python 工程化、async、FastAPI/Pydantic v2、PostgreSQL/Redis、后台任务、认证和负载测试；BE5-Gate 在完成 B0 Docker 后即交付最小 CI/Docker/测试部署/smoke，R6 复用该部署形成领域 RAG 旗舰。
- R6/G8/M9/FINAL 不只要求“能跑”：必须有版本化评估、组件指标、失败/危险样例和 baseline；旗舰还需 CI/CD、可恢复执行、安全/权限、负载与公开可复现证据。
- 正式练习按任务形态调整：概念/阅读日 8–12 题；编码/Gate/项目日 5–8 个高质量检查点，把主要时间留给真实产物、测试和故障注入。

## 本地配置

复制 `.env.example` 为 `.env`，再填入自己的真实密钥。`.env` 已被 `.gitignore` 忽略，不应提交到 GitHub。

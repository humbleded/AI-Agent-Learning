# AI Agent Learning Workspace

这个文件夹用于记录 AI Agent 开发学习全过程。

## 常用文件

- `tracker/ai-agent-learning-tracker.md`：完整学习路线、每项资料、作业、问答、通过标准。
- `tracker/progress.md`：总进度表。
- `daily/TEMPLATE.md`：每日打卡模板。
- `code/`：你自己写的代码。
- `notes/`：视频、文档、源码阅读笔记。
- `repos/`：参考源码仓库。

## 每天怎么用

1. 从 `tracker/ai-agent-learning-tracker.md` 选一个任务编号。
2. 在 `daily/` 复制一份模板，命名为当天日期。
3. 把代码写到 `code/对应阶段/`。
4. 把笔记写到 `notes/对应阶段/`。
5. 把每日打卡发给 Codex。
6. Codex 检查代码和答案后，更新 `tracker/progress.md`。

## 当前路线规则

- 阶段 0 Python 与开发环境主线已完成到 `P0-Gate`。
- 当前进入阶段 1：大模型 API 入门；下一项是 `L1-02` 单轮问答。
- 阶段 0.5 工程基础不再整块卡住 Agent 主线，而是按场景穿插补：
  - API 调用时补 HTTP、timeout、headers、status code。
  - 环境配置时补 venv、包安装、环境变量。
  - Memory/RAG 需要持久化时补 SQL 和数据库。
  - 本地多服务或部署时补 Docker Compose。

## 本地配置

复制 `.env.example` 为 `.env`，再填入自己的真实密钥。`.env` 已被 `.gitignore` 忽略，不应提交到 GitHub。

# 工作台前端

使用 Vue 官方 create-vue 3.23.0 模板、Vue、TypeScript、Vue Router 与 Element Plus。安装结果由 package-lock.json 固定，使用 npm ci 复现。

完整功能、前后端启动、接口说明、验证与学习分工见 [工作台 README](../README.md)。

- src/views/：概览、工程文档、故障诊断和后续能力页面。
- src/lib/api.ts：HTTP 请求和后端事件读取。
- src/App.vue：统一导航与连接状态，保留诊断页的运行状态。
- vite.config.ts：本地 5173 端口与 /api 转发配置。

本目录执行 npm run dev 启动，npm run build 检查类型并构建。后端应同时运行在本机 8765 端口。前端只使用相对 /api 调用，不放模型密钥。

<script setup lang="ts">
import { ref, onMounted } from "vue";
import {
  ArrowRight,
  LibraryBig,
  Activity,
  Braces,
  Workflow,
  Monitor,
  ChevronRight,
  Search,
  PanelsTopLeft,
} from "@lucide/vue";
import { getJson, type Health } from "../lib/api";
const health = ref<Health | null>(null);
const knowledge = ref<{ available: boolean; file_count: number } | null>(null);
onMounted(async () => {
  try {
    health.value = await getJson<Health>("/api/health");
  } catch {
    /* The shell displays connectivity. */
  }
});
onMounted(async () => {
  try {
    knowledge.value = await getJson("/api/knowledge/status");
  } catch {
    /* Connection remains explicit on the knowledge page. */
  }
});
</script>
<template>
  <div class="page-intro">
    <div>
      <span class="eyebrow">BUILD · RUN · UNDERSTAND</span>
      <h1>让学到的能力，真正运行起来。</h1>
      <p>你的 Agent 项目在这里汇合。从输入资料，到看到每一步处理和最终结果。</p>
    </div>
    <span class="subtle-pill">本地学习工作台</span>
  </div>
  <section class="hero-panel">
    <div class="hero-copy">
      <span class="hero-tag"
        ><i></i>
        {{
          knowledge?.available ? "你的知识库，已经连接" : "让项目连接你的知识"
        }}</span
      >
      <h2>把积累的知识，<br />变成此刻的答案。</h2>
      <p>
        从自己的笔记开始提问，观察 Agent
        怎样查找资料、组织回答，并回到原文核对依据。
      </p>
      <RouterLink to="/studio" class="primary-link"
        >问问我的知识库 <ArrowRight :size="17"
      /></RouterLink>
    </div>
    <div class="hero-flow">
      <div class="flow-label">你能看见的完整链路</div>
      <div class="flow-tile">
        <Monitor /><span
          ><strong>提出你的问题</strong
          ><small>连接已积累的学习笔记</small></span
        ><span class="flow-index">01</span>
      </div>
      <div class="flow-connector"></div>
      <div class="flow-tile">
        <Workflow /><span
          ><strong>Agent 调用检索工具</strong
          ><small>选择搜索词 · 找到相关片段</small></span
        ><span class="flow-index">02</span>
      </div>
      <div class="flow-connector"></div>
      <div class="flow-tile">
        <Braces /><span
          ><strong>回答带着原文回来</strong
          ><small>查看答案 · 核对资料出处</small></span
        ><span class="flow-index">03</span>
      </div>
    </div>
  </section>
  <div class="section-heading">
    <h2>我的项目</h2>
    <span>一个入口，持续接入新的能力</span>
  </div>
  <div class="project-grid">
    <RouterLink to="/studio" class="project-card">
      <div class="project-card-top">
        <span class="project-icon teal"><Search :size="25" /></span
        ><ElTag effect="plain">{{
          knowledge?.available
            ? `${knowledge.file_count} 份笔记`
            : "连接状态待确认"
        }}</ElTag>
      </div>
      <h3>我的知识库</h3>
      <p>让 Agent 从本地笔记中查找资料，显示实际搜索词、答案和原文出处。</p>
      <div class="project-bottom">
        <span>只读连接 · AI-Knowledge</span><ArrowRight :size="19" />
      </div>
    </RouterLink>
    <RouterLink to="/documents" class="project-card"
      ><div class="project-card-top">
        <span class="project-icon amber"><LibraryBig :size="25" /></span
        ><ElTag type="warning" effect="plain">{{
          health?.modules.find((m) => m.id === "rag")?.status === "ready_to_run"
            ? "可以运行"
            : "等待 G3 实现"
        }}</ElTag>
      </div>
      <h3>工程文档助手</h3>
      <p>读取资料、保留来源，逐步接入切分、检索和有依据的回答。</p>
      <div class="project-bottom">
        <span>当前：文档导入</span><ArrowRight :size="19" /></div></RouterLink
    ><RouterLink to="/incidents" class="project-card"
      ><div class="project-card-top">
        <span class="project-icon teal"><Activity :size="25" /></span
        ><ElTag type="success" effect="plain">{{
          health?.modules.find((m) => m.id === "incidents")?.status ===
          "available"
            ? "核心已接入"
            : "等待后端"
        }}</ElTag>
      </div>
      <h3>故障诊断与变更评审</h3>
      <p>把告警与日志交给工作流，查看诊断步骤、停止原因和结论。</p>
      <div class="project-bottom">
        <span>真实 LangGraph 工作流</span><ArrowRight :size="19" /></div
    ></RouterLink>
    <RouterLink to="/gallery" class="project-card">
      <div class="project-card-top">
        <span class="project-icon amber"><PanelsTopLeft :size="25" /></span
        ><ElTag type="info" effect="plain">3 种工作方式</ElTag>
      </div>
      <h3>三种工作模式</h3>
      <p>任务指挥台、知识研究工作室、可视流程画布全部已启用，按当前需要随时切换。</p>
      <div class="project-bottom">
        <span>全部已启用 · 共享当前查询</span><ArrowRight :size="19" />
      </div>
    </RouterLink>
  </div>
  <RouterLink to="/roadmap" class="next-strip"
    ><span class="next-dot"></span>
    <div>
      <strong>每完成一段学习，就让工作台长出一个能力</strong>
      <p>检索问答、四类记忆、图片与音频、工具接入，将沿同一套界面继续演进。</p>
    </div>
    <ChevronRight
  /></RouterLink>
</template>
